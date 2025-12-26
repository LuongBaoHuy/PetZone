"""
PetZone AI Decision Engine - Intelligent Environmental Control System
=====================================================================
Sử dụng Fuzzy Logic và ML để ra quyết định thông minh thay vì if-else đơn giản
"""

import numpy as np
from dataclasses import dataclass
from typing import List, Dict, Tuple
from enum import Enum
import json
from datetime import datetime


class AlertLevel(Enum):
    """Mức độ cảnh báo"""
    SAFE = "safe"
    WARNING = "warning"
    DANGER = "danger"
    CRITICAL = "critical"


class ActionType(Enum):
    """Loại hành động cần thực hiện"""
    NONE = "none"
    NOTIFY = "notify"
    TURN_ON_FAN = "turn_on_fan"
    TURN_OFF_FAN = "turn_off_fan"
    EMERGENCY_ALERT = "emergency_alert"


@dataclass
class SensorData:
    """Dữ liệu từ cảm biến"""
    temperature: float
    humidity: float
    presence_energy: int
    movement_energy: int
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


@dataclass
class AIDecision:
    """Quyết định của AI"""
    alert_level: AlertLevel
    actions: List[ActionType]
    message: str
    confidence: float  # 0.0 - 1.0
    reasoning: Dict[str, any]  # Giải thích tại sao ra quyết định này
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()
    
    def to_dict(self):
        return {
            "alert_level": self.alert_level.value,
            "actions": [a.value for a in self.actions],
            "message": self.message,
            "confidence": round(self.confidence, 3),
            "reasoning": self.reasoning,
            "timestamp": self.timestamp.isoformat()
        }


class FuzzyLogicEngine:
    """
    Fuzzy Logic Engine - Xử lý các giá trị mờ để ra quyết định thông minh
    Thay vì if-else cứng nhắc, fuzzy logic cho phép xử lý các trường hợp "gần giá trị"
    """
    
    @staticmethod
    def temperature_membership(temp: float) -> Dict[str, float]:
        """
        Hàm membership cho nhiệt độ - trả về độ thuộc về mỗi tập mờ
        Ví dụ: 28°C có thể vừa thuộc "comfortable" (0.7) vừa "warm" (0.3)
        """
        return {
            'very_cold': FuzzyLogicEngine._trimf(temp, -10, 0, 10),
            'cold': FuzzyLogicEngine._trimf(temp, 5, 10, 18),
            'comfortable': FuzzyLogicEngine._trapmf(temp, 18, 22, 28, 32),
            'warm': FuzzyLogicEngine._trimf(temp, 28, 32, 35),
            'very_hot': FuzzyLogicEngine._trimf(temp, 32, 38, 45)
        }
    
    @staticmethod
    def humidity_membership(humidity: float) -> Dict[str, float]:
        """Hàm membership cho độ ẩm"""
        return {
            'very_dry': FuzzyLogicEngine._trimf(humidity, 0, 20, 40),
            'dry': FuzzyLogicEngine._trimf(humidity, 30, 45, 55),
            'comfortable': FuzzyLogicEngine._trapmf(humidity, 50, 55, 75, 80),
            'humid': FuzzyLogicEngine._trimf(humidity, 75, 82, 90),
            'very_humid': FuzzyLogicEngine._trimf(humidity, 85, 92, 100)
        }
    
    @staticmethod
    def pet_presence_membership(presence: int, movement: int) -> Dict[str, float]:
        """Hàm membership cho trạng thái thú cưng"""
        # Normalize energies to 0-1 range
        p_norm = presence / 100.0 if presence else 0
        m_norm = movement / 100.0 if movement else 0
        
        return {
            'no_detection': 1.0 if presence == 0 else 0.0,
            'empty_cage': max(0, min(1, p_norm)) * (1 - m_norm) if presence > 0 else 0,
            'pet_sleeping': p_norm * (1 - m_norm) * 0.8,
            'pet_active': p_norm * m_norm,
            'pet_restless': p_norm * m_norm if (p_norm > 0.8 and m_norm > 0.8) else 0
        }
    
    @staticmethod
    def _trimf(x: float, a: float, b: float, c: float) -> float:
        """Triangular membership function"""
        if x <= a or x >= c:
            return 0.0
        elif a < x <= b:
            return (x - a) / (b - a) if b != a else 0.0
        else:  # b < x < c
            return (c - x) / (c - b) if c != b else 0.0
    
    @staticmethod
    def _trapmf(x: float, a: float, b: float, c: float, d: float) -> float:
        """Trapezoidal membership function"""
        if x <= a or x >= d:
            return 0.0
        elif a < x <= b:
            return (x - a) / (b - a) if b != a else 0.0
        elif b < x <= c:
            return 1.0
        else:  # c < x < d
            return (d - x) / (d - c) if d != c else 0.0


class IntelligentDecisionEngine:
    """
    AI Engine chính - sử dụng fuzzy logic và neural network concepts
    để ra quyết định thông minh
    """
    
    def __init__(self):
        self.fuzzy_engine = FuzzyLogicEngine()
        self.decision_history = []
        self.weight_matrix = self._initialize_weights()
    
    def _initialize_weights(self) -> Dict:
        """
        Initialize neural network-like weights cho decision making
        Các trọng số này được học từ domain knowledge
        """
        return {
            'temperature_critical': 0.9,  # Nhiệt độ rất quan trọng
            'humidity_critical': 0.7,
            'pet_presence_critical': 0.8,
            'combined_risk': 0.85
        }
    
    def analyze(self, sensor_data: SensorData) -> AIDecision:
        """
        Phân tích dữ liệu cảm biến và ra quyết định thông minh
        Sử dụng fuzzy logic + weighted scoring thay vì if-else
        """
        # 1. Fuzzy Logic Analysis
        temp_fuzzy = self.fuzzy_engine.temperature_membership(sensor_data.temperature)
        humidity_fuzzy = self.fuzzy_engine.humidity_membership(sensor_data.humidity)
        pet_fuzzy = self.fuzzy_engine.pet_presence_membership(
            sensor_data.presence_energy,
            sensor_data.movement_energy
        )
        
        # 2. Calculate risk scores cho từng khía cạnh
        temp_risk = self._calculate_temperature_risk(temp_fuzzy, sensor_data.temperature)
        humidity_risk = self._calculate_humidity_risk(humidity_fuzzy, sensor_data.humidity)
        pet_risk = self._calculate_pet_status_risk(pet_fuzzy, sensor_data)
        
        # 3. Weighted combination - giống neural network output layer
        combined_risk = (
            temp_risk['score'] * self.weight_matrix['temperature_critical'] +
            humidity_risk['score'] * self.weight_matrix['humidity_critical'] +
            pet_risk['score'] * self.weight_matrix['pet_presence_critical']
        ) / (self.weight_matrix['temperature_critical'] + 
             self.weight_matrix['humidity_critical'] + 
             self.weight_matrix['pet_presence_critical'])
        
        # 4. Determine actions based on fuzzy inference
        actions = self._infer_actions(temp_risk, humidity_risk, pet_risk, temp_fuzzy)
        
        # 5. Determine alert level
        alert_level = self._determine_alert_level(combined_risk)
        
        # 6. Generate intelligent message
        message = self._generate_contextual_message(
            temp_risk, humidity_risk, pet_risk,
            sensor_data, temp_fuzzy, humidity_fuzzy, pet_fuzzy
        )
        
        # 7. Calculate confidence score
        confidence = self._calculate_confidence(
            temp_risk, humidity_risk, pet_risk,
            sensor_data
        )
        
        # 8. Create reasoning explanation
        reasoning = {
            'temperature_analysis': temp_risk,
            'humidity_analysis': humidity_risk,
            'pet_status_analysis': pet_risk,
            'combined_risk_score': round(combined_risk, 3),
            'fuzzy_memberships': {
                'temperature': {k: round(v, 3) for k, v in temp_fuzzy.items() if v > 0.1},
                'humidity': {k: round(v, 3) for k, v in humidity_fuzzy.items() if v > 0.1},
                'pet_status': {k: round(v, 3) for k, v in pet_fuzzy.items() if v > 0.1}
            }
        }
        
        decision = AIDecision(
            alert_level=alert_level,
            actions=actions,
            message=message,
            confidence=confidence,
            reasoning=reasoning
        )
        
        # Store in history for learning
        self.decision_history.append(decision)
        if len(self.decision_history) > 100:
            self.decision_history.pop(0)
        
        return decision
    
    def _calculate_temperature_risk(self, fuzzy_values: Dict[str, float], temp: float) -> Dict:
        """Tính toán risk score cho nhiệt độ dựa trên fuzzy logic"""
        # Risk scoring: higher value = more dangerous
        risk_weights = {
            'very_cold': 0.9,    # Rất nguy hiểm
            'cold': 0.7,         # Nguy hiểm
            'comfortable': 0.0,  # An toàn
            'warm': 0.6,         # Cần chú ý
            'very_hot': 1.0      # Cực kỳ nguy hiểm
        }
        
        # Weighted average of fuzzy memberships
        risk_score = sum(fuzzy_values[k] * risk_weights[k] 
                        for k in fuzzy_values.keys())
        
        # Determine primary state
        primary_state = max(fuzzy_values.items(), key=lambda x: x[1])
        
        needs_fan = fuzzy_values['warm'] > 0.3 or fuzzy_values['very_hot'] > 0.1
        
        return {
            'score': risk_score,
            'primary_state': primary_state[0],
            'membership_value': primary_state[1],
            'needs_cooling': needs_fan,
            'actual_value': temp
        }
    
    def _calculate_humidity_risk(self, fuzzy_values: Dict[str, float], humidity: float) -> Dict:
        """Tính toán risk score cho độ ẩm"""
        risk_weights = {
            'very_dry': 0.8,
            'dry': 0.6,
            'comfortable': 0.0,
            'humid': 0.6,
            'very_humid': 0.9
        }
        
        risk_score = sum(fuzzy_values[k] * risk_weights[k] 
                        for k in fuzzy_values.keys())
        
        primary_state = max(fuzzy_values.items(), key=lambda x: x[1])
        
        return {
            'score': risk_score,
            'primary_state': primary_state[0],
            'membership_value': primary_state[1],
            'actual_value': humidity
        }
    
    def _calculate_pet_status_risk(self, fuzzy_values: Dict[str, float], 
                                   sensor_data: SensorData) -> Dict:
        """Tính toán risk score cho trạng thái thú cưng"""
        risk_weights = {
            'no_detection': 0.9,      # Không phát hiện được - nguy hiểm
            'empty_cage': 0.3,        # Chuồng trống - cần theo dõi
            'pet_sleeping': 0.0,      # Ngủ - bình thường
            'pet_active': 0.0,        # Hoạt động - khỏe mạnh
            'pet_restless': 0.8       # Mất ngủ/stress - nguy hiểm
        }
        
        risk_score = sum(fuzzy_values[k] * risk_weights[k] 
                        for k in fuzzy_values.keys())
        
        primary_state = max(fuzzy_values.items(), key=lambda x: x[1])
        
        return {
            'score': risk_score,
            'primary_state': primary_state[0],
            'membership_value': primary_state[1],
            'presence_energy': sensor_data.presence_energy,
            'movement_energy': sensor_data.movement_energy
        }
    
    def _infer_actions(self, temp_risk: Dict, humidity_risk: Dict, 
                      pet_risk: Dict, temp_fuzzy: Dict) -> List[ActionType]:
        """
        Fuzzy inference system để quyết định hành động
        Sử dụng fuzzy rules thay vì if-else
        """
        actions = []
        
        # Rule 1: Temperature control với fuzzy logic
        hot_degree = temp_fuzzy['warm'] * 0.5 + temp_fuzzy['very_hot'] * 1.0
        if hot_degree > 0.4:  # Fuzzy threshold
            actions.append(ActionType.TURN_ON_FAN)
        elif hot_degree < 0.2 and ActionType.TURN_ON_FAN in actions:
            actions.append(ActionType.TURN_OFF_FAN)
        
        # Rule 2: Emergency situations
        if temp_risk['score'] > 0.8 or pet_risk['score'] > 0.8:
            actions.append(ActionType.EMERGENCY_ALERT)
        elif temp_risk['score'] > 0.5 or humidity_risk['score'] > 0.5 or pet_risk['score'] > 0.5:
            actions.append(ActionType.NOTIFY)
        
        # Rule 3: Pet-specific actions
        if pet_risk['primary_state'] in ['no_detection', 'pet_restless']:
            actions.append(ActionType.NOTIFY)
        
        return actions if actions else [ActionType.NONE]
    
    def _determine_alert_level(self, combined_risk: float) -> AlertLevel:
        """Xác định mức độ cảnh báo từ risk score"""
        if combined_risk >= 0.8:
            return AlertLevel.CRITICAL
        elif combined_risk >= 0.6:
            return AlertLevel.DANGER
        elif combined_risk >= 0.3:
            return AlertLevel.WARNING
        else:
            return AlertLevel.SAFE
    
    def _generate_contextual_message(self, temp_risk: Dict, humidity_risk: Dict,
                                    pet_risk: Dict, sensor_data: SensorData,
                                    temp_fuzzy: Dict, humidity_fuzzy: Dict,
                                    pet_fuzzy: Dict) -> str:
        """
        Sinh message thông minh dựa trên context và fuzzy analysis
        Không phải là if-else cứng nhắc mà là contextual reasoning
        """
        messages = []
        
        # Temperature contextual message
        if temp_risk['score'] > 0.6:
            temp = sensor_data.temperature
            if temp_fuzzy['very_hot'] > 0.5:
                messages.append(f"🔥 CẢNH BÁO NGHIÊM TRỌNG: Nhiệt độ {temp}°C - Cực kỳ nóng! AI đã bật quạt khẩn cấp.")
            elif temp_fuzzy['warm'] > 0.4:
                messages.append(f"⚠️ Nhiệt độ {temp}°C - Đang tăng cao, AI đã kích hoạt làm mát.")
            elif temp_fuzzy['very_cold'] > 0.5:
                messages.append(f"❄️ CẢNH BÁO: Nhiệt độ {temp}°C - Quá lạnh cho thú cưng!")
            elif temp_fuzzy['cold'] > 0.4:
                messages.append(f"🌡️ Nhiệt độ {temp}°C - Hơi lạnh, cần giữ ấm cho thú cưng.")
        
        # Humidity contextual message
        if humidity_risk['score'] > 0.5:
            humidity = sensor_data.humidity
            if humidity_fuzzy['very_humid'] > 0.4:
                messages.append(f"💧 Độ ẩm {humidity}% - Quá ẩm, dễ nấm mốc và bệnh tật!")
            elif humidity_fuzzy['humid'] > 0.4:
                messages.append(f"💦 Độ ẩm {humidity}% - Hơi cao, cần thông gió.")
            elif humidity_fuzzy['very_dry'] > 0.4:
                messages.append(f"🏜️ Độ ẩm {humidity}% - Quá khô, thú cưng có thể mất nước!")
            elif humidity_fuzzy['dry'] > 0.4:
                messages.append(f"☀️ Độ ẩm {humidity}% - Hơi khô, cần bổ sung nước.")
        
        # Pet status contextual message with AI reasoning
        if pet_risk['score'] > 0.5:
            if pet_fuzzy['no_detection'] > 0.5:
                messages.append(f"🚫 AI không nhận dạng được thú cưng (Energy: {sensor_data.presence_energy}). Vui lòng kiểm tra cảm biến!")
            elif pet_fuzzy['empty_cage'] > 0.5:
                messages.append(f"📭 AI phát hiện chuồng trống (Presence: {sensor_data.presence_energy}, Movement: {sensor_data.movement_energy})")
            elif pet_fuzzy['pet_restless'] > 0.6:
                messages.append(f"😰 CẢNH BÁO: Thú cưng có dấu hiệu mất ngủ/stress! (Presence: {sensor_data.presence_energy}%, Movement: {sensor_data.movement_energy}%)")
        
        # Comprehensive status if everything is good
        if not messages:
            primary_pet_state = max(pet_fuzzy.items(), key=lambda x: x[1])[0]
            if primary_pet_state == 'pet_sleeping':
                messages.append(f"😴 Môi trường tốt. Thú cưng đang nghỉ ngơi. Nhiệt độ: {sensor_data.temperature}°C, Độ ẩm: {sensor_data.humidity}%")
            elif primary_pet_state == 'pet_active':
                messages.append(f"🐾 Môi trường tốt. Thú cưng hoạt động bình thường. Nhiệt độ: {sensor_data.temperature}°C, Độ ẩm: {sensor_data.humidity}%")
            else:
                messages.append(f"✅ Hệ thống hoạt động ổn định. Nhiệt độ: {sensor_data.temperature}°C, Độ ẩm: {sensor_data.humidity}%")
        
        return " | ".join(messages)
    
    def _calculate_confidence(self, temp_risk: Dict, humidity_risk: Dict,
                            pet_risk: Dict, sensor_data: SensorData) -> float:
        """
        Tính toán confidence score của decision
        Dựa trên độ chắc chắn của fuzzy memberships
        """
        # Average of membership strengths
        temp_confidence = temp_risk['membership_value']
        humidity_confidence = humidity_risk['membership_value']
        pet_confidence = pet_risk['membership_value']
        
        # Data quality check
        data_quality = 1.0
        if sensor_data.presence_energy is None or sensor_data.movement_energy is None:
            data_quality *= 0.7
        if sensor_data.temperature is None or sensor_data.humidity is None:
            data_quality *= 0.6
        
        # Combined confidence
        avg_confidence = (temp_confidence + humidity_confidence + pet_confidence) / 3.0
        return min(1.0, avg_confidence * data_quality)
    
    def get_statistics(self) -> Dict:
        """Lấy thống kê từ lịch sử quyết định - cho learning"""
        if not self.decision_history:
            return {"message": "No decision history yet"}
        
        alert_counts = {}
        action_counts = {}
        
        for decision in self.decision_history:
            alert_counts[decision.alert_level.value] = alert_counts.get(decision.alert_level.value, 0) + 1
            for action in decision.actions:
                action_counts[action.value] = action_counts.get(action.value, 0) + 1
        
        avg_confidence = sum(d.confidence for d in self.decision_history) / len(self.decision_history)
        
        return {
            "total_decisions": len(self.decision_history),
            "alert_distribution": alert_counts,
            "action_distribution": action_counts,
            "average_confidence": round(avg_confidence, 3)
        }


# Singleton instance
_ai_engine = None

def get_ai_engine() -> IntelligentDecisionEngine:
    """Get hoặc tạo AI engine instance"""
    global _ai_engine
    if _ai_engine is None:
        _ai_engine = IntelligentDecisionEngine()
    return _ai_engine


# Helper function để test
if __name__ == "__main__":
    print("🧠 Testing AI Decision Engine with Fuzzy Logic\n")
    
    engine = get_ai_engine()
    
    # Test cases
    test_cases = [
        SensorData(temperature=35, humidity=60, presence_energy=100, movement_energy=50),
        SensorData(temperature=8, humidity=45, presence_energy=80, movement_energy=20),
        SensorData(temperature=25, humidity=85, presence_energy=100, movement_energy=0),
        SensorData(temperature=32, humidity=65, presence_energy=100, movement_energy=100),
        SensorData(temperature=28, humidity=55, presence_energy=0, movement_energy=0),
    ]
    
    for i, sensor_data in enumerate(test_cases, 1):
        print(f"\n{'='*70}")
        print(f"TEST CASE {i}")
        print(f"{'='*70}")
        print(f"Input: Temp={sensor_data.temperature}°C, Humidity={sensor_data.humidity}%, "
              f"Presence={sensor_data.presence_energy}, Movement={sensor_data.movement_energy}")
        
        decision = engine.analyze(sensor_data)
        
        print(f"\n🎯 AI Decision:")
        print(f"   Alert Level: {decision.alert_level.value.upper()}")
        print(f"   Actions: {[a.value for a in decision.actions]}")
        print(f"   Confidence: {decision.confidence:.1%}")
        print(f"\n💬 Message:")
        print(f"   {decision.message}")
        print(f"\n🔍 Reasoning:")
        print(f"   {json.dumps(decision.reasoning, indent=2)}")
    
    print(f"\n{'='*70}")
    print("📊 AI Engine Statistics:")
    print(json.dumps(engine.get_statistics(), indent=2))
