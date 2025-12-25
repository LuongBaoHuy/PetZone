# 🧠 PetZone AI Service - Intelligent Environmental Control System

## 🎯 Tổng Quan

PetZone AI Service là một hệ thống AI thông minh sử dụng **Fuzzy Logic** và **Machine Learning concepts** để tự động giám sát và điều khiển môi trường chuồng thú cưng. Hệ thống không sử dụng if-else đơn giản mà áp dụng các thuật toán AI để ra quyết định thông minh.

### ✨ Tính Năng Chính

1. **🌡️ Điều Khiển Nhiệt Độ Thông Minh**
   - Tự động bật quạt khi nhiệt độ ≥ 32°C
   - Cảnh báo khi nhiệt độ < 10°C (quá lạnh)
   - Điều chỉnh cường độ quạt dựa trên mức độ nóng

2. **💧 Giám Sát Độ Ẩm**
   - Cảnh báo khi độ ẩm > 80% (quá ẩm)
   - Cảnh báo khi độ ẩm < 50% (quá khô)

3. **🐾 Phát Hiện Trạng Thái Thú Cưng**
   - Năng lượng tĩnh = 0: Không nhận dạng được thú cưng
   - Năng lượng tĩnh = 100, động = 0: Chuồng trống
   - Năng lượng tĩnh = 100, động = 100: Thú cưng mất ngủ/stress

4. **🤖 AI Decision Engine**
   - Sử dụng Fuzzy Logic thay vì if-else cứng nhắc
   - Weighted scoring system (giống neural network)
   - Contextual reasoning và confidence scoring
   - Learning từ decision history

5. **🎮 IoT Controller**
   - Điều khiển quạt, máy sưởi, máy phun sương
   - Hỗ trợ HTTP và MQTT protocols
   - Manual override mode
   - Command history tracking

## 🏗️ Kiến Trúc Hệ Thống

```
┌─────────────────────────────────────────────────────────────────┐
│                        PetZone AI Service                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────────┐      ┌──────────────────┐                │
│  │  Sensor Data     │─────>│  AI Decision     │                │
│  │  Collection      │      │  Engine          │                │
│  └──────────────────┘      │  (Fuzzy Logic)   │                │
│          ▲                  └────────┬─────────┘                │
│          │                           │                           │
│          │                           ▼                           │
│  ┌───────┴────────┐      ┌──────────────────┐                  │
│  │  Backend API   │      │  IoT Controller  │                  │
│  │  (.NET Core)   │      │  (Device Control)│                  │
│  └────────────────┘      └────────┬─────────┘                  │
│                                    │                             │
│                                    ▼                             │
│                          ┌──────────────────┐                   │
│                          │  ESP32 Devices   │                   │
│                          │  (Fan, Heater)   │                   │
│                          └──────────────────┘                   │
└─────────────────────────────────────────────────────────────────┘
```

## 📦 Cài Đặt

### 1. Cài Đặt Dependencies

```bash
cd ai_service
pip install -r requirements.txt
```

### 2. Cấu Hình

Chỉnh sửa các thông số trong `ai_service_main.py`:

```python
BACKEND_API_URL = "http://localhost:5019/api"  # Backend .NET API
ESP32_IP = "192.168.1.100"                     # IP của ESP32
CHECK_INTERVAL = 5                              # Kiểm tra mỗi 5 giây
ALERT_COOLDOWN = 30                             # Cooldown giữa các alert
```

### 3. Chạy AI Service

```bash
python ai_service_main.py
```

## 🚀 API Endpoints

### AI Service (Port 5001)

| Endpoint | Method | Mô Tả |
|----------|--------|-------|
| `/health` | GET | Health check |
| `/status` | GET | Trạng thái AI và IoT hiện tại |
| `/stats` | GET | Thống kê AI service |
| `/manual_control` | POST | Điều khiển thiết bị thủ công |
| `/test_analysis` | POST | Test AI với custom sensor data |
| `/command_history` | GET | Lịch sử lệnh IoT |

### Backend API (Port 5019)

| Endpoint | Method | Mô Tả |
|----------|--------|-------|
| `/api/ai/alert` | POST | Nhận alert từ AI |
| `/api/ai/emergency` | POST | Nhận emergency alert |
| `/api/ai/alerts` | GET | Lấy danh sách alerts |
| `/api/device/activity` | POST | Log hoạt động thiết bị |
| `/api/device/activity` | GET | Lịch sử thiết bị |
| `/api/device/statistics` | GET | Thống kê thiết bị |

## 📊 Cách Hoạt Động của AI

### 1. Fuzzy Logic System

Thay vì if-else cứng nhắc:
```python
# ❌ Bad: Traditional if-else
if temperature > 32:
    turn_on_fan()
```

AI sử dụng Fuzzy Logic:
```python
# ✅ Good: Fuzzy Logic
temp_fuzzy = {
    'comfortable': 0.2,  # 20% comfortable
    'warm': 0.5,         # 50% warm
    'very_hot': 0.3      # 30% very hot
}
# AI quyết định dựa trên weighted combination
```

### 2. Membership Functions

```python
Temperature Fuzzy Sets:
- very_cold: [-10, 0, 10]°C
- cold: [5, 10, 18]°C
- comfortable: [18, 22, 28, 32]°C
- warm: [28, 32, 35]°C
- very_hot: [32, 38, 45]°C
```

### 3. Risk Scoring System

```python
# Mỗi aspect có risk score 0.0-1.0
temp_risk = 0.85      # Temperature risk
humidity_risk = 0.60  # Humidity risk
pet_risk = 0.30       # Pet status risk

# Weighted combination (giống neural network)
combined_risk = (
    temp_risk * 0.9 +
    humidity_risk * 0.7 +
    pet_risk * 0.8
) / (0.9 + 0.7 + 0.8)
```

### 4. Action Inference

```python
# Fuzzy inference thay vì if-else
hot_degree = temp_fuzzy['warm'] * 0.5 + temp_fuzzy['very_hot'] * 1.0

if hot_degree > 0.4:  # Fuzzy threshold
    turn_on_fan(intensity=calculate_from_fuzzy())
```

## 📝 Ví Dụ Sử Dụng

### Test AI Analysis

```bash
curl -X POST http://localhost:5001/test_analysis \
  -H "Content-Type: application/json" \
  -d '{
    "temperature": 35,
    "humidity": 85,
    "presence_energy": 100,
    "movement_energy": 100
  }'
```

Response:
```json
{
  "sensor_data": {
    "temperature": 35,
    "humidity": 85,
    "presence_energy": 100,
    "movement_energy": 100
  },
  "decision": {
    "alert_level": "critical",
    "actions": ["turn_on_fan", "emergency_alert"],
    "message": "🔥 CẢNH BÁO NGHIÊM TRỌNG: Nhiệt độ 35°C...",
    "confidence": 0.923,
    "reasoning": {
      "temperature_analysis": {
        "score": 0.95,
        "primary_state": "very_hot",
        "needs_cooling": true
      },
      "fuzzy_memberships": {
        "temperature": {
          "warm": 0.5,
          "very_hot": 0.769
        }
      }
    }
  }
}
```

### Manual Control

```bash
curl -X POST http://localhost:5001/manual_control \
  -H "Content-Type: application/json" \
  -d '{
    "device": "fan",
    "action": "on",
    "intensity": 80
  }'
```

### Get AI Status

```bash
curl http://localhost:5001/status
```

## 🧪 Testing

```bash
# Test AI Decision Engine
python ai_decision_engine.py

# Test IoT Controller
python iot_controller.py

# Test Full Service
python ai_service_main.py
```

## 📈 Monitoring & Statistics

### View AI Statistics

```bash
curl http://localhost:5001/stats
```

Response:
```json
{
  "decisions_made": 1250,
  "actions_executed": 345,
  "alerts_sent": 89,
  "uptime": "2:34:56",
  "ai_engine_stats": {
    "total_decisions": 1250,
    "alert_distribution": {
      "safe": 980,
      "warning": 195,
      "danger": 60,
      "critical": 15
    },
    "average_confidence": 0.87
  }
}
```

## 🔧 Cấu Hình ESP32

ESP32 cần expose HTTP endpoint:

```cpp
// ESP32 Arduino Code
void setup() {
  server.on("/control", HTTP_POST, handleControl);
}

void handleControl() {
  String device = server.arg("device");
  int state = server.arg("state").toInt();
  int intensity = server.arg("intensity").toInt();
  
  if (device == "fan") {
    analogWrite(FAN_PIN, state ? intensity * 255 / 100 : 0);
  }
  
  server.send(200, "application/json", "{\"status\":\"ok\"}");
}
```

## 🎓 Advanced Features

### Custom Weights

Điều chỉnh trọng số trong AI Engine:

```python
engine.weight_matrix = {
    'temperature_critical': 0.95,  # Tăng ưu tiên nhiệt độ
    'humidity_critical': 0.6,
    'pet_presence_critical': 0.85,
    'combined_risk': 0.9
}
```

### Learning from History

AI tự động lưu decision history và có thể học:

```python
# Get statistics for learning
stats = engine.get_statistics()
print(stats)
```

## 🐛 Troubleshooting

### AI Service không kết nối Backend

```bash
# Check backend is running
curl http://localhost:5019/api/sensor/latest

# Check network connectivity
ping localhost
```

### ESP32 không nhận lệnh

```bash
# Test ESP32 connection
curl -X POST http://192.168.1.100/control \
  -H "Content-Type: application/json" \
  -d '{"device":"fan","state":1,"intensity":100}'
```

### Fuzzy Logic không chính xác

Điều chỉnh membership functions trong `ai_decision_engine.py`:

```python
def temperature_membership(temp: float):
    return {
        'very_cold': _trimf(temp, -10, 0, 10),
        'cold': _trimf(temp, 5, 10, 18),
        # ... adjust these values
    }
```

## 📚 Tài Liệu Tham Khảo

- Fuzzy Logic: https://en.wikipedia.org/wiki/Fuzzy_logic
- Membership Functions: https://www.mathworks.com/help/fuzzy/membership-functions.html
- IoT Control Systems: https://www.arduino.cc/en/Tutorial/HomePage

## 🤝 Contributing

Nếu muốn cải thiện AI:

1. Thêm membership functions mới
2. Điều chỉnh risk weights
3. Thêm learning algorithms
4. Tích hợp deep learning models

## 📄 License

MIT License - PetZone Project 2025

---

**Made with ❤️ by PetZone AI Team**
