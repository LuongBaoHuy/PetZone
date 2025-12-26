"""
PetZone IoT Controller - Intelligent Device Control
===================================================
Điều khiển thiết bị IoT (quạt, đèn, máy sưởi) thông qua MQTT hoặc HTTP
"""

import requests
import json
from typing import Dict, Optional
from datetime import datetime
from dataclasses import dataclass
from enum import Enum


class DeviceType(Enum):
    """Các loại thiết bị IoT"""
    FAN = "fan"
    HEATER = "heater"
    LIGHT = "light"
    HUMIDIFIER = "humidifier"


class DeviceState(Enum):
    """Trạng thái thiết bị"""
    ON = "on"
    OFF = "off"
    AUTO = "auto"


@dataclass
class DeviceCommand:
    """Lệnh điều khiển thiết bị"""
    device_type: DeviceType
    action: DeviceState
    intensity: Optional[int] = None  # 0-100 cho fan speed, heater power, etc.
    duration: Optional[int] = None   # Thời gian hoạt động (seconds)
    reason: str = ""
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()
    
    def to_dict(self):
        return {
            "device_type": self.device_type.value,
            "action": self.action.value,
            "intensity": self.intensity,
            "duration": self.duration,
            "reason": self.reason,
            "timestamp": self.timestamp.isoformat()
        }


class IoTController:
    """
    Controller cho các thiết bị IoT
    Hỗ trợ nhiều protocols: HTTP, MQTT, WebSocket
    """
    
    def __init__(self, esp32_ip: str = "192.168.1.100", backend_url: str = "http://localhost:5019"):
        """
        Initialize IoT Controller
        
        Args:
            esp32_ip: IP address của ESP32
            backend_url: URL của backend .NET API
        """
        self.esp32_ip = esp32_ip
        self.backend_url = backend_url
        self.device_states = {
            DeviceType.FAN: DeviceState.OFF,
            DeviceType.HEATER: DeviceState.OFF,
            DeviceType.LIGHT: DeviceState.OFF,
            DeviceType.HUMIDIFIER: DeviceState.OFF
        }
        self.command_history = []
    
    def execute_command(self, command: DeviceCommand) -> Dict:
        """
        Thực thi lệnh điều khiển thiết bị
        
        Returns:
            Dict với status và message
        """
        print(f"\n{'='*60}")
        print(f"🎮 IoT Controller - Executing Command")
        print(f"{'='*60}")
        print(f"Device: {command.device_type.value.upper()}")
        print(f"Action: {command.action.value.upper()}")
        print(f"Reason: {command.reason}")
        
        try:
            # 1. Send command to ESP32
            esp32_result = self._send_to_esp32(command)
            
            # 2. Log to backend
            backend_result = self._log_to_backend(command)
            
            # 3. Update local state
            self.device_states[command.device_type] = command.action
            
            # 4. Add to history
            self.command_history.append(command)
            if len(self.command_history) > 100:
                self.command_history.pop(0)
            
            result = {
                "success": True,
                "device": command.device_type.value,
                "action": command.action.value,
                "esp32_response": esp32_result,
                "backend_response": backend_result,
                "timestamp": command.timestamp.isoformat()
            }
            
            print(f"✅ Command executed successfully!")
            print(f"{'='*60}\n")
            
            return result
            
        except Exception as e:
            error_result = {
                "success": False,
                "error": str(e),
                "device": command.device_type.value,
                "action": command.action.value
            }
            print(f"❌ Error: {e}")
            print(f"{'='*60}\n")
            return error_result
    
    def _send_to_esp32(self, command: DeviceCommand) -> Dict:
        """
        Gửi lệnh tới ESP32 qua HTTP
        ESP32 cần expose endpoint như: http://192.168.1.100/control
        """
        try:
            # Chuẩn bị payload cho ESP32
            payload = {
                "device": command.device_type.value,
                "state": 1 if command.action == DeviceState.ON else 0,
                "intensity": command.intensity or 100
            }
            
            # Endpoint của ESP32 (cần cấu hình trong ESP32)
            esp32_url = f"http://{self.esp32_ip}/control"
            
            print(f"📡 Sending to ESP32: {esp32_url}")
            print(f"   Payload: {payload}")
            
            # Send HTTP POST request
            response = requests.post(
                esp32_url,
                json=payload,
                timeout=5,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                print(f"   ✅ ESP32 responded: {response.status_code}")
                return {
                    "status": "success",
                    "response": response.json() if response.text else {}
                }
            else:
                print(f"   ⚠️ ESP32 responded with error: {response.status_code}")
                return {
                    "status": "error",
                    "code": response.status_code,
                    "message": response.text
                }
                
        except requests.exceptions.Timeout:
            print(f"   ⚠️ ESP32 connection timeout - device may be offline")
            return {"status": "timeout", "message": "ESP32 not responding"}
        except requests.exceptions.ConnectionError:
            print(f"   ⚠️ Cannot connect to ESP32 at {self.esp32_ip}")
            return {"status": "connection_error", "message": "ESP32 not reachable"}
        except Exception as e:
            print(f"   ❌ Error sending to ESP32: {e}")
            return {"status": "error", "message": str(e)}
    
    def _log_to_backend(self, command: DeviceCommand) -> Dict:
        """
        Ghi log lệnh điều khiển vào backend .NET API
        """
        try:
            payload = {
                "deviceType": command.device_type.value,
                "action": command.action.value,
                "intensity": command.intensity,
                "duration": command.duration,
                "reason": command.reason,
                "timestamp": command.timestamp.isoformat()
            }
            
            backend_endpoint = f"{self.backend_url}/api/device/activity"
            
            print(f"📡 Logging to Backend: {backend_endpoint}")
            
            response = requests.post(
                backend_endpoint,
                json=payload,
                timeout=5,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code in [200, 201]:
                print(f"   ✅ Backend logged successfully")
                return {"status": "success", "data": response.json() if response.text else {}}
            else:
                print(f"   ⚠️ Backend error: {response.status_code}")
                return {"status": "error", "code": response.status_code}
                
        except Exception as e:
            print(f"   ⚠️ Backend logging failed: {e}")
            return {"status": "error", "message": str(e)}
    
    def turn_on_fan(self, intensity: int = 100, reason: str = "AI auto control") -> Dict:
        """Bật quạt với cường độ xác định"""
        command = DeviceCommand(
            device_type=DeviceType.FAN,
            action=DeviceState.ON,
            intensity=intensity,
            reason=reason
        )
        return self.execute_command(command)
    
    def turn_off_fan(self, reason: str = "AI auto control") -> Dict:
        """Tắt quạt"""
        command = DeviceCommand(
            device_type=DeviceType.FAN,
            action=DeviceState.OFF,
            reason=reason
        )
        return self.execute_command(command)
    
    def turn_on_heater(self, intensity: int = 100, reason: str = "AI auto control") -> Dict:
        """Bật máy sưởi"""
        command = DeviceCommand(
            device_type=DeviceType.HEATER,
            action=DeviceState.ON,
            intensity=intensity,
            reason=reason
        )
        return self.execute_command(command)
    
    def turn_off_heater(self, reason: str = "AI auto control") -> Dict:
        """Tắt máy sưởi"""
        command = DeviceCommand(
            device_type=DeviceType.HEATER,
            action=DeviceState.OFF,
            reason=reason
        )
        return self.execute_command(command)
    
    def turn_on_humidifier(self, intensity: int = 100, reason: str = "AI auto control") -> Dict:
        """Bật máy phun sương"""
        command = DeviceCommand(
            device_type=DeviceType.HUMIDIFIER,
            action=DeviceState.ON,
            intensity=intensity,
            reason=reason
        )
        return self.execute_command(command)
    
    def turn_off_humidifier(self, reason: str = "AI auto control") -> Dict:
        """Tắt máy phun sương"""
        command = DeviceCommand(
            device_type=DeviceType.HUMIDIFIER,
            action=DeviceState.OFF,
            reason=reason
        )
        return self.execute_command(command)
    
    def get_device_state(self, device_type: DeviceType) -> DeviceState:
        """Lấy trạng thái hiện tại của thiết bị"""
        return self.device_states.get(device_type, DeviceState.OFF)
    
    def get_all_device_states(self) -> Dict:
        """Lấy trạng thái tất cả thiết bị"""
        return {
            device.value: state.value 
            for device, state in self.device_states.items()
        }
    
    def get_command_history(self, limit: int = 10) -> list:
        """Lấy lịch sử lệnh điều khiển"""
        return [cmd.to_dict() for cmd in self.command_history[-limit:]]


# Singleton instance
_iot_controller = None

def get_iot_controller(esp32_ip: str = "192.168.1.100", 
                       backend_url: str = "http://localhost:5019") -> IoTController:
    """Get hoặc tạo IoT controller instance"""
    global _iot_controller
    if _iot_controller is None:
        _iot_controller = IoTController(esp32_ip, backend_url)
    return _iot_controller


if __name__ == "__main__":
    print("🎮 Testing IoT Controller\n")
    
    controller = get_iot_controller()
    
    # Test turn on fan
    print("\n1. Testing FAN control:")
    result = controller.turn_on_fan(intensity=80, reason="Temperature is 33°C")
    print(f"Result: {json.dumps(result, indent=2)}")
    
    print("\n2. Testing FAN off:")
    result = controller.turn_off_fan(reason="Temperature normalized")
    print(f"Result: {json.dumps(result, indent=2)}")
    
    print("\n3. All device states:")
    print(json.dumps(controller.get_all_device_states(), indent=2))
    
    print("\n4. Command history:")
    print(json.dumps(controller.get_command_history(), indent=2))
