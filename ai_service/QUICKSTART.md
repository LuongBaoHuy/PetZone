# 🚀 PetZone AI Integration - Quick Start Guide

## 📋 Tổng Quan Hệ Thống

Bạn đã tích hợp thành công **AI thông minh** vào hệ thống PetZone với các tính năng:

✅ **Fuzzy Logic AI** - Không dùng if-else cứng nhắc  
✅ **Tự động điều khiển quạt** khi nhiệt độ ≥ 32°C  
✅ **Cảnh báo thông minh** cho nhiệt độ, độ ẩm, trạng thái thú cưng  
✅ **IoT Controller** - Điều khiển ESP32 qua HTTP  
✅ **Backend Integration** - Lưu logs và alerts vào database  

---

## 🎯 Yêu Cầu Đã Được Triển Khai

### 1. Nhiệt Độ
- ✅ **Temp ≥ 32°C**: AI tự động bật quạt với cường độ thích hợp
- ✅ **Temp < 10°C**: Cảnh báo quá lạnh (không bật quạt)

### 2. Độ Ẩm
- ✅ **Humidity > 80%**: Cảnh báo quá ẩm
- ✅ **Humidity < 50%**: Cảnh báo quá khô

### 3. Trạng Thái Thú Cưng
- ✅ **Presence = 0**: Cảnh báo không nhận dạng được thú cưng
- ✅ **Presence = 100, Movement = 0**: Thông báo chuồng trống
- ✅ **Presence = 100, Movement = 100**: Cảnh báo thú cưng mất ngủ

---

## 🔧 Cài Đặt & Chạy

### Bước 1: Cài Đặt Python Dependencies

```powershell
cd d:\PetZone\ai_service
pip install -r requirements.txt
```

### Bước 2: Cấu Hình ESP32 (Optional)

Nếu có ESP32, upload file `esp32_controller.ino`:

1. Mở Arduino IDE
2. Cài library: `WiFi`, `WebServer`, `ArduinoJson`
3. Sửa WiFi credentials trong file
4. Upload lên ESP32
5. Lấy IP của ESP32 (check Serial Monitor)

### Bước 3: Cấu Hình AI Service

Mở `ai_service_main.py` và sửa:

```python
BACKEND_API_URL = "http://localhost:5019/api"  # ✅ Đã đúng với backend của bạn
ESP32_IP = "192.168.1.100"  # 🔧 Thay bằng IP ESP32 thật (nếu có)
```

### Bước 4: Chạy Backend .NET

```powershell
cd d:\PetZone\PetZone
dotnet run
```

Backend sẽ chạy tại: `http://localhost:5019`

### Bước 5: Chạy AI Service

```powershell
cd d:\PetZone\ai_service
python ai_service_main.py
```

AI Service sẽ chạy tại: `http://localhost:5001`

---

## 🧪 Test Hệ Thống

### Test 1: Kiểm Tra AI Engine

```powershell
cd d:\PetZone\ai_service
python ai_decision_engine.py
```

Output mong đợi:
```
🧠 Testing AI Decision Engine with Fuzzy Logic

======================================================================
TEST CASE 1
======================================================================
Input: Temp=35°C, Humidity=60%, Presence=100, Movement=50

🎯 AI Decision:
   Alert Level: CRITICAL
   Actions: ['turn_on_fan', 'emergency_alert']
   Confidence: 92.3%

💬 Message:
   🔥 CẢNH BÁO NGHIÊM TRỌNG: Nhiệt độ 35°C - Cực kỳ nóng! AI đã bật quạt khẩn cấp.
```

### Test 2: Test AI Analysis API

```powershell
curl -X POST http://localhost:5001/test_analysis `
  -H "Content-Type: application/json" `
  -Body '{
    "temperature": 33,
    "humidity": 85,
    "presence_energy": 100,
    "movement_energy": 100
  }'
```

### Test 3: Test Manual Control

```powershell
curl -X POST http://localhost:5001/manual_control `
  -H "Content-Type: application/json" `
  -Body '{
    "device": "fan",
    "action": "on",
    "intensity": 80
  }'
```

### Test 4: Kiểm Tra Backend

```powershell
# Lấy sensor data mới nhất
curl http://localhost:5019/api/sensor/latest

# Lấy AI alerts
curl http://localhost:5019/api/ai/alerts

# Lấy device activities
curl http://localhost:5019/api/device/activity
```

---

## 📊 Monitoring Dashboard

### AI Service Status

```powershell
curl http://localhost:5001/status
```

Response:
```json
{
  "ai_service": {
    "is_running": true,
    "last_decision": {
      "alert_level": "warning",
      "actions": ["turn_on_fan"],
      "message": "⚠️ Nhiệt độ 32°C - Đang tăng cao...",
      "confidence": 0.87
    },
    "last_sensor_data": {
      "temperature": 32,
      "humidity": 65,
      "presence_energy": 80,
      "movement_energy": 40
    }
  },
  "iot_devices": {
    "fan": "on",
    "heater": "off",
    "humidifier": "off"
  }
}
```

### AI Statistics

```powershell
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

---

## 🎮 Demo Scenarios

### Scenario 1: Nhiệt Độ Cao

**Input:**
```json
{
  "temperature": 35,
  "humidity": 60,
  "presence_energy": 80,
  "movement_energy": 50
}
```

**AI Decision:**
- ✅ Alert: CRITICAL
- ✅ Action: TURN_ON_FAN (100% intensity)
- ✅ Message: "🔥 CẢNH BÁO NGHIÊM TRỌNG: Nhiệt độ 35°C - Cực kỳ nóng!"

### Scenario 2: Độ Ẩm Cao

**Input:**
```json
{
  "temperature": 25,
  "humidity": 85,
  "presence_energy": 100,
  "movement_energy": 20
}
```

**AI Decision:**
- ✅ Alert: WARNING
- ✅ Action: NOTIFY
- ✅ Message: "💧 Độ ẩm 85% - Quá ẩm, dễ nấm mốc!"

### Scenario 3: Thú Cưng Mất Ngủ

**Input:**
```json
{
  "temperature": 28,
  "humidity": 60,
  "presence_energy": 100,
  "movement_energy": 100
}
```

**AI Decision:**
- ✅ Alert: DANGER
- ✅ Action: NOTIFY
- ✅ Message: "😰 CẢNH BÁO: Thú cưng có dấu hiệu mất ngủ/stress!"

### Scenario 4: Không Phát Hiện Thú Cưng

**Input:**
```json
{
  "temperature": 25,
  "humidity": 60,
  "presence_energy": 0,
  "movement_energy": 0
}
```

**AI Decision:**
- ✅ Alert: DANGER
- ✅ Action: EMERGENCY_ALERT
- ✅ Message: "🚫 AI không nhận dạng được thú cưng"

---

## 🔍 Kiến Trúc AI

### 1. AI Decision Engine (`ai_decision_engine.py`)
- Fuzzy Logic với membership functions
- Risk scoring system
- Weighted decision making
- Confidence calculation

### 2. IoT Controller (`iot_controller.py`)
- HTTP client cho ESP32
- Device state management
- Command history tracking

### 3. Main Service (`ai_service_main.py`)
- Integration layer
- Flask API server
- Background monitoring loop
- Alert system

---

## 📁 File Structure

```
ai_service/
├── ai_decision_engine.py       # 🧠 AI Engine với Fuzzy Logic
├── iot_controller.py            # 🎮 IoT Device Controller
├── ai_service_main.py           # 🚀 Main Service (chạy file này)
├── pet_detection.py             # 📹 Video detection (legacy)
├── requirements.txt             # 📦 Python dependencies
├── AI_INTEGRATION_GUIDE.md      # 📚 Chi tiết về AI
├── QUICKSTART.md                # 🚀 File này
└── esp32_controller.ino         # 🔧 ESP32 Arduino code
```

---

## ⚙️ Configuration

### Điều Chỉnh Fuzzy Logic

Trong `ai_decision_engine.py`, class `FuzzyLogicEngine`:

```python
# Thay đổi membership functions
@staticmethod
def temperature_membership(temp: float):
    return {
        'very_cold': _trimf(temp, -10, 0, 10),
        'cold': _trimf(temp, 5, 10, 18),
        'comfortable': _trapmf(temp, 18, 22, 28, 32),  # 🔧 Điều chỉnh ở đây
        'warm': _trimf(temp, 28, 32, 35),
        'very_hot': _trimf(temp, 32, 38, 45)
    }
```

### Điều Chỉnh Risk Weights

```python
# Trong ai_decision_engine.py, class IntelligentDecisionEngine
def _initialize_weights(self):
    return {
        'temperature_critical': 0.95,  # 🔧 Tăng ưu tiên nhiệt độ
        'humidity_critical': 0.7,
        'pet_presence_critical': 0.8,
        'combined_risk': 0.85
    }
```

---

## 🐛 Troubleshooting

### Issue 1: AI Service không kết nối Backend

**Giải pháp:**
```powershell
# Kiểm tra backend đang chạy
curl http://localhost:5019/api/sensor/latest

# Kiểm tra port
netstat -ano | findstr :5019
```

### Issue 2: ESP32 không nhận lệnh

**Giải pháp:**
1. Kiểm tra IP ESP32: `ping 192.168.1.100`
2. Test endpoint: `curl http://192.168.1.100/status`
3. Check Serial Monitor trong Arduino IDE

### Issue 3: Module import error

**Giải pháp:**
```powershell
pip install --upgrade flask requests numpy opencv-python scipy
```

---

## 🎓 Next Steps

### 1. Tích Hợp Frontend
- Hiển thị AI decisions real-time
- Dashboard cho device control
- Alert notifications

### 2. Nâng Cấp AI
- Thêm machine learning model
- Historical data analysis
- Predictive maintenance

### 3. Mở Rộng IoT
- Thêm camera detection
- MQTT protocol
- Multiple ESP32 devices

---

## 📞 Support

Nếu gặp vấn đề:

1. Check logs trong console
2. Test từng component riêng lẻ
3. Đọc `AI_INTEGRATION_GUIDE.md` để hiểu chi tiết

---

## ✅ Checklist Hoàn Thành

- [x] AI Decision Engine với Fuzzy Logic
- [x] IoT Controller cho ESP32
- [x] Backend API endpoints
- [x] Alert system
- [x] Device activity logging
- [x] Manual control API
- [x] Statistics & monitoring
- [x] Documentation

**🎉 Chúc mừng! Bạn đã tích hợp thành công AI vào hệ thống PetZone!**

---

Made with ❤️ by PetZone AI Team
