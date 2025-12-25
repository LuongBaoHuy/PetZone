"""
PetZone AI Service - Main Integrated Service
=============================================
Tích hợp: AI Decision Engine + IoT Controller + Backend Communication + Video Detection
"""

import time
import requests
from datetime import datetime, timedelta
from threading import Thread, Lock
from flask import Flask, Response, jsonify, request
from typing import Dict, Optional
import json

# Import our AI modules
from ai_decision_engine import (
    get_ai_engine, 
    SensorData, 
    AIDecision, 
    AlertLevel, 
    ActionType
)
from iot_controller import get_iot_controller, DeviceType, DeviceState

# Configuration
BACKEND_API_URL = "http://localhost:5019/api"
ESP32_IP = "192.168.1.100"  # Thay đổi IP của ESP32 của bạn
CHECK_INTERVAL = 5  # Kiểm tra mỗi 5 giây
ALERT_COOLDOWN = 30  # Không gửi alert trùng trong 30s

# Flask app
app = Flask(__name__)

# Global state
ai_engine = None
iot_controller = None
last_decision = None
last_sensor_data = None
last_alert_time = {}
state_lock = Lock()
is_running = False


class AIService:
    """Main AI Service orchestrator"""
    
    def __init__(self):
        self.ai_engine = get_ai_engine()
        self.iot_controller = get_iot_controller(ESP32_IP, BACKEND_API_URL)
        self.is_running = False
        self.stats = {
            'decisions_made': 0,
            'actions_executed': 0,
            'alerts_sent': 0,
            'started_at': None
        }
    
    def start(self):
        """Start AI service"""
        self.is_running = True
        self.stats['started_at'] = datetime.now()
        print("\n" + "="*70)
        print("🧠 AI SERVICE STARTED")
        print("="*70)
        print(f"Backend API: {BACKEND_API_URL}")
        print(f"ESP32 IP: {ESP32_IP}")
        print(f"Check Interval: {CHECK_INTERVAL}s")
        print("="*70 + "\n")
        
        # Start monitoring thread
        monitor_thread = Thread(target=self._monitoring_loop, daemon=True)
        monitor_thread.start()
    
    def stop(self):
        """Stop AI service"""
        self.is_running = False
        print("\n🛑 AI Service stopped")
    
    def _monitoring_loop(self):
        """Main monitoring loop - đây là trái tim của AI system"""
        global last_decision, last_sensor_data
        
        while self.is_running:
            try:
                # 1. Fetch latest sensor data from backend
                sensor_data = self._fetch_sensor_data()
                
                if sensor_data is None:
                    print("⚠️ No sensor data available, waiting...")
                    time.sleep(CHECK_INTERVAL)
                    continue
                
                # 2. AI analyze sensor data
                decision = self.ai_engine.analyze(sensor_data)
                self.stats['decisions_made'] += 1
                
                # 3. Execute actions based on AI decision
                self._execute_decision(decision, sensor_data)
                
                # 4. Send alert to backend if needed
                if decision.alert_level != AlertLevel.SAFE:
                    self._send_alert(decision, sensor_data)
                
                # 5. Update global state
                with state_lock:
                    last_decision = decision
                    last_sensor_data = sensor_data
                
                # 6. Log decision
                self._log_decision(decision, sensor_data)
                
                # Wait before next check
                time.sleep(CHECK_INTERVAL)
                
            except Exception as e:
                print(f"❌ Error in monitoring loop: {e}")
                import traceback
                traceback.print_exc()
                time.sleep(CHECK_INTERVAL)
    
    def _fetch_sensor_data(self) -> Optional[SensorData]:
        """Lấy dữ liệu cảm biến mới nhất từ backend"""
        try:
            response = requests.get(
                f"{BACKEND_API_URL}/sensor/latest",
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                
                sensor_data = SensorData(
                    temperature=float(data.get('temperature', 0)),
                    humidity=float(data.get('humidity', 0)),
                    presence_energy=int(data.get('presenceEnergy', 0)),
                    movement_energy=int(data.get('movementEnergy', 0)),
                    timestamp=datetime.fromisoformat(data['createdAt'].replace('Z', '+00:00'))
                        if 'createdAt' in data else datetime.now()
                )
                
                return sensor_data
            else:
                print(f"⚠️ Backend returned {response.status_code}")
                return None
                
        except requests.exceptions.ConnectionError:
            print(f"⚠️ Cannot connect to backend at {BACKEND_API_URL}")
            return None
        except Exception as e:
            print(f"❌ Error fetching sensor data: {e}")
            return None
    
    def _execute_decision(self, decision: AIDecision, sensor_data: SensorData):
        """Execute actions từ AI decision"""
        for action in decision.actions:
            if action == ActionType.TURN_ON_FAN:
                # Tính fan intensity dựa trên nhiệt độ (AI adaptive control)
                temp = sensor_data.temperature
                if temp >= 35:
                    intensity = 100
                elif temp >= 32:
                    intensity = 80
                else:
                    intensity = 60
                
                print(f"\n🌀 AI Decision: Turn ON fan (intensity={intensity}%)")
                result = self.iot_controller.turn_on_fan(
                    intensity=intensity,
                    reason=f"Temperature {temp}°C - AI auto control"
                )
                self.stats['actions_executed'] += 1
                
            elif action == ActionType.TURN_OFF_FAN:
                print(f"\n❄️ AI Decision: Turn OFF fan")
                result = self.iot_controller.turn_off_fan(
                    reason="Temperature normalized - AI auto control"
                )
                self.stats['actions_executed'] += 1
                
            elif action == ActionType.EMERGENCY_ALERT:
                print(f"\n🚨 AI Decision: EMERGENCY ALERT!")
                self._send_emergency_alert(decision, sensor_data)
                self.stats['alerts_sent'] += 1
                
            elif action == ActionType.NOTIFY:
                print(f"\n📢 AI Decision: Send notification")
                self.stats['alerts_sent'] += 1
    
    def _send_alert(self, decision: AIDecision, sensor_data: SensorData):
        """Gửi alert tới backend với cooldown để tránh spam"""
        alert_key = f"{decision.alert_level.value}"
        
        # Check cooldown
        if alert_key in last_alert_time:
            time_since_last = (datetime.now() - last_alert_time[alert_key]).total_seconds()
            if time_since_last < ALERT_COOLDOWN:
                return  # Skip alert due to cooldown
        
        try:
            payload = {
                "alertLevel": decision.alert_level.value,
                "message": decision.message,
                "confidence": decision.confidence,
                "sensorData": {
                    "temperature": sensor_data.temperature,
                    "humidity": sensor_data.humidity,
                    "presenceEnergy": sensor_data.presence_energy,
                    "movementEnergy": sensor_data.movement_energy
                },
                "reasoning": decision.reasoning,
                "timestamp": datetime.now().isoformat()
            }
            
            response = requests.post(
                f"{BACKEND_API_URL}/ai/alert",
                json=payload,
                timeout=5
            )
            
            if response.status_code in [200, 201]:
                print(f"✅ Alert sent to backend")
                last_alert_time[alert_key] = datetime.now()
            else:
                print(f"⚠️ Failed to send alert: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error sending alert: {e}")
    
    def _send_emergency_alert(self, decision: AIDecision, sensor_data: SensorData):
        """Gửi emergency alert (không có cooldown)"""
        try:
            payload = {
                "alertType": "EMERGENCY",
                "alertLevel": decision.alert_level.value,
                "message": decision.message,
                "confidence": decision.confidence,
                "sensorData": {
                    "temperature": sensor_data.temperature,
                    "humidity": sensor_data.humidity,
                    "presenceEnergy": sensor_data.presence_energy,
                    "movementEnergy": sensor_data.movement_energy
                },
                "actions": [a.value for a in decision.actions],
                "reasoning": decision.reasoning,
                "timestamp": datetime.now().isoformat()
            }
            
            response = requests.post(
                f"{BACKEND_API_URL}/ai/emergency",
                json=payload,
                timeout=5
            )
            
            if response.status_code in [200, 201]:
                print(f"🚨 Emergency alert sent!")
            
        except Exception as e:
            print(f"❌ Error sending emergency: {e}")
    
    def _log_decision(self, decision: AIDecision, sensor_data: SensorData):
        """Log AI decision ra console"""
        print(f"\n{'─'*70}")
        print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'─'*70}")
        print(f"📊 Sensor Data:")
        print(f"   🌡️  Temperature: {sensor_data.temperature}°C")
        print(f"   💧 Humidity: {sensor_data.humidity}%")
        print(f"   📡 Presence Energy: {sensor_data.presence_energy}")
        print(f"   🏃 Movement Energy: {sensor_data.movement_energy}")
        print(f"{'─'*70}")
        print(f"🧠 AI Decision:")
        print(f"   ⚠️  Alert Level: {decision.alert_level.value.upper()}")
        print(f"   🎯 Actions: {[a.value for a in decision.actions]}")
        print(f"   💯 Confidence: {decision.confidence:.1%}")
        print(f"   💬 Message: {decision.message}")
        print(f"{'─'*70}\n")
    
    def get_stats(self) -> Dict:
        """Lấy thống kê của AI service"""
        uptime = None
        if self.stats['started_at']:
            uptime = str(datetime.now() - self.stats['started_at']).split('.')[0]
        
        return {
            **self.stats,
            'uptime': uptime,
            'is_running': self.is_running,
            'ai_engine_stats': self.ai_engine.get_statistics()
        }


# Initialize service
ai_service = None


# ============ FLASK ROUTES ============

@app.route('/health')
def health():
    """Health check"""
    return jsonify({
        "status": "running" if ai_service and ai_service.is_running else "stopped",
        "timestamp": datetime.now().isoformat()
    })


@app.route('/status')
def get_status():
    """Lấy trạng thái hiện tại của AI và IoT"""
    with state_lock:
        return jsonify({
            "ai_service": {
                "is_running": ai_service.is_running if ai_service else False,
                "last_decision": last_decision.to_dict() if last_decision else None,
                "last_sensor_data": {
                    "temperature": last_sensor_data.temperature,
                    "humidity": last_sensor_data.humidity,
                    "presence_energy": last_sensor_data.presence_energy,
                    "movement_energy": last_sensor_data.movement_energy,
                    "timestamp": last_sensor_data.timestamp.isoformat()
                } if last_sensor_data else None
            },
            "iot_devices": iot_controller.get_all_device_states() if iot_controller else {},
            "timestamp": datetime.now().isoformat()
        })


@app.route('/stats')
def get_stats():
    """Lấy thống kê của AI service"""
    if ai_service:
        return jsonify(ai_service.get_stats())
    return jsonify({"error": "AI service not initialized"}), 500


@app.route('/manual_control', methods=['POST'])
def manual_control():
    """Manual control cho IoT devices (override AI)"""
    data = request.get_json()
    
    device = data.get('device')
    action = data.get('action')
    intensity = data.get('intensity', 100)
    
    if not device or not action:
        return jsonify({"error": "Missing device or action"}), 400
    
    try:
        if device == 'fan':
            if action == 'on':
                result = iot_controller.turn_on_fan(intensity, "Manual control by user")
            else:
                result = iot_controller.turn_off_fan("Manual control by user")
        elif device == 'heater':
            if action == 'on':
                result = iot_controller.turn_on_heater(intensity, "Manual control by user")
            else:
                result = iot_controller.turn_off_heater("Manual control by user")
        elif device == 'humidifier':
            if action == 'on':
                result = iot_controller.turn_on_humidifier(intensity, "Manual control by user")
            else:
                result = iot_controller.turn_off_humidifier("Manual control by user")
        else:
            return jsonify({"error": f"Unknown device: {device}"}), 400
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/test_analysis', methods=['POST'])
def test_analysis():
    """Test AI analysis với custom sensor data"""
    data = request.get_json()
    
    sensor_data = SensorData(
        temperature=float(data.get('temperature', 25)),
        humidity=float(data.get('humidity', 60)),
        presence_energy=int(data.get('presence_energy', 0)),
        movement_energy=int(data.get('movement_energy', 0))
    )
    
    decision = ai_service.ai_engine.analyze(sensor_data)
    
    return jsonify({
        "sensor_data": {
            "temperature": sensor_data.temperature,
            "humidity": sensor_data.humidity,
            "presence_energy": sensor_data.presence_energy,
            "movement_energy": sensor_data.movement_energy
        },
        "decision": decision.to_dict()
    })


@app.route('/command_history')
def command_history():
    """Lấy lịch sử lệnh IoT"""
    if iot_controller:
        return jsonify({
            "history": iot_controller.get_command_history(20)
        })
    return jsonify({"error": "IoT controller not initialized"}), 500


# ============ MAIN ============

def initialize_service():
    """Initialize AI service"""
    global ai_service, ai_engine, iot_controller
    
    ai_service = AIService()
    ai_engine = ai_service.ai_engine
    iot_controller = ai_service.iot_controller
    
    # Start monitoring
    ai_service.start()


if __name__ == "__main__":
    print("="*70)
    print("🐾 PETZONE INTELLIGENT AI SERVICE")
    print("="*70)
    print("Features:")
    print("  ✅ AI Decision Engine with Fuzzy Logic")
    print("  ✅ IoT Device Control (Fan, Heater, Humidifier)")
    print("  ✅ Real-time Sensor Monitoring")
    print("  ✅ Backend Integration")
    print("  ✅ Emergency Alert System")
    print("="*70)
    
    # Initialize service
    initialize_service()
    
    print("\n📡 API Endpoints:")
    print(f"   → http://localhost:5001/status    (AI & IoT status)")
    print(f"   → http://localhost:5001/stats     (AI statistics)")
    print(f"   → http://localhost:5001/manual_control (Manual device control)")
    print(f"   → http://localhost:5001/test_analysis (Test AI with custom data)")
    print(f"   → http://localhost:5001/command_history (IoT command history)")
    print("\n⏹️  Press Ctrl+C to stop\n")
    
    try:
        app.run(host='0.0.0.0', port=5001, threaded=True, debug=False)
    except KeyboardInterrupt:
        print("\n\n👋 Stopping AI Service...")
        if ai_service:
            ai_service.stop()
        print("✅ AI Service stopped!")
