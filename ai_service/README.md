# 🐾 PetZone AI Service - Motion Detection & Video Streaming

## 📋 Tổng quan
AI Service sử dụng **OpenCV Motion Detection** để phát hiện thú cưng trong chuồng và **Flask** để stream video real-time về Frontend.

### ✨ Tính năng
- ✅ Phát hiện chuyển động (Background Subtraction - MOG2)
- ✅ Stream video real-time qua HTTP (30 FPS)
- ✅ Gửi trạng thái (`hasPet: true/false`) lên Backend API
- ✅ Hiển thị log console với timestamp
- ✅ Vẽ khung xanh quanh vùng chuyển động
- ✅ Tự động đánh dấu "Chuồng trống" sau 10s không có chuyển động

---

## 🚀 Cài đặt & Chạy

### 1️⃣ Cài đặt Python dependencies
```bash
cd ai_service
pip install -r requirements.txt
```

### 2️⃣ Cấu hình Backend API URL
Mở file `pet_detection.py` và sửa dòng:
```python
BACKEND_API_URL = "http://localhost:5000/api/ai/status"  # Thay bằng URL Backend thật
```

### 3️⃣ Chạy AI Service
```bash
python pet_detection.py
```

**Output mong đợi:**
```
============================================================
🐾 PETZONE AI SERVICE - MOTION DETECTION & STREAMING
============================================================
✅ Camera khởi tạo thành công!
⏳ Đang khởi động camera...
🚀 Bắt đầu phát hiện chuyển động...

📡 Video streaming:
   → http://localhost:5001/video_feed

📊 Status API:
   → http://localhost:5001/status

💡 Backend API: http://localhost:5000/api/ai/status

⏹️  Nhấn Ctrl+C để dừng

🐾 [14:30:45] Phát hiện thú cưng
✅ Đã gửi API: hasPet=True
⭕ [14:30:58] Chuồng trống
✅ Đã gửi API: hasPet=False
```

---

## 🔗 API Endpoints

### 1. Video Stream (cho Frontend)
```
GET http://localhost:5001/video_feed
```
- **Mô tả:** Stream video JPEG qua HTTP (MJPEG format)
- **Cách dùng trong React:**
```jsx
<img src="http://localhost:5001/video_feed" alt="Camera Feed" />
```

### 2. Status API (tùy chọn)
```
GET http://localhost:5001/status
```
- **Response:**
```json
{
  "hasPet": true,
  "lastMotionTime": 1703337045.123,
  "timestamp": 1703337050.456
}
```

### 3. Health Check
```
GET http://localhost:5001/health
```
- **Response:**
```json
{
  "status": "running",
  "camera": true
}
```

---

## ⚙️ Tùy chỉnh tham số

Mở file `pet_detection.py` và chỉnh phần **CẤU HÌNH**:

```python
CAMERA_INDEX = 0           # 0 = Webcam mặc định, 1 = External camera
MOTION_THRESHOLD = 500     # Càng cao càng khó phát hiện (pixel thay đổi)
CHECK_INTERVAL = 3         # Gửi API mỗi X giây
NO_MOTION_TIMEOUT = 10     # Sau X giây không chuyển động → Chuồng trống
```

---

## 🧪 Demo & Kiểm tra

### Test 1: Xem video stream
1. Chạy `python pet_detection.py`
2. Mở browser: `http://localhost:5001/video_feed`
3. **Kết quả:** Thấy video webcam với khung xanh quanh vùng chuyển động

### Test 2: Kiểm tra API
1. Vẫy tay trước camera
2. Check console → Thấy log: `🐾 [HH:MM:SS] Phát hiện thú cưng`
3. Đứng yên 10 giây
4. Check console → Thấy log: `⭕ [HH:MM:SS] Chuồng trống`

### Test 3: Tích hợp với Backend
1. Chạy Backend .NET trước
2. Chạy AI Service
3. Check log Backend → Nhận được POST request từ AI Service

---

## 🎯 Tích hợp với Frontend (React)

### Cách 1: Hiển thị video trực tiếp
```jsx
// src/components/CameraView.jsx
export function CameraView() {
  return (
    <div className="camera-container">
      <h3>📹 Camera giám sát</h3>
      <img 
        src="http://localhost:5001/video_feed" 
        alt="Pet Camera"
        style={{ width: '100%', borderRadius: '8px' }}
      />
    </div>
  );
}
```

### Cách 2: Kèm theo status (nâng cao)
```jsx
import { useState, useEffect } from 'react';

export function AIStatusCard() {
  const [status, setStatus] = useState(null);
  
  useEffect(() => {
    const interval = setInterval(async () => {
      const res = await fetch('http://localhost:5001/status');
      const data = await res.json();
      setStatus(data);
    }, 2000);
    
    return () => clearInterval(interval);
  }, []);
  
  return (
    <div>
      <img src="http://localhost:5001/video_feed" />
      <p>{status?.hasPet ? '🐾 Có thú cưng' : '⭕ Chuồng trống'}</p>
    </div>
  );
}
```

---

## 🔧 Troubleshooting

### ❌ Lỗi: "Cannot open camera"
**Nguyên nhân:** Webcam đang được ứng dụng khác sử dụng  
**Giải pháp:** 
- Đóng Zoom, Skype, Teams, OBS...
- Thử đổi `CAMERA_INDEX = 1` (nếu có nhiều camera)

### ❌ Lỗi: "Connection refused to Backend API"
**Nguyên nhân:** Backend chưa chạy  
**Giải pháp:** Chạy Backend .NET trước, hoặc comment dòng gửi API để test riêng

### ⚠️ Video bị giật lag
**Nguyên nhân:** CPU yếu  
**Giải pháp:**
- Giảm resolution: `camera.set(cv2.CAP_PROP_FRAME_WIDTH, 320)`
- Tăng sleep time: `time.sleep(0.05)` trong `generate_frames()`

---

## 🚀 Nâng cấp sau (nếu có thời gian)

### Plan B: YOLO Object Detection
Nếu muốn phát hiện **chó/mèo cụ thể** thay vì chỉ chuyển động:

1. Uncomment dòng `ultralytics` trong `requirements.txt`
2. Tải model YOLO:
```python
from ultralytics import YOLO
model = YOLO('yolov8n.pt')  # Nano model (nhẹ nhất)
```

3. Thay thế hàm `detect_motion()`:
```python
def detect_pets_yolo(frame):
    results = model(frame, classes=[15, 16])  # 15=Cat, 16=Dog
    has_pet = len(results[0].boxes) > 0
    annotated = results[0].plot()
    return has_pet, annotated
```

⚠️ **Lưu ý:** YOLO trên CPU chỉ đạt ~3-5 FPS, nên chạy mỗi 3 giây thay vì mỗi frame.

---

## 📊 Checklist Giai đoạn 4

- [x] Viết Python script với OpenCV
- [x] Implement Motion Detection (Background Subtraction)
- [x] Tạo Flask server để stream video
- [x] Gửi status lên Backend API mỗi 3 giây
- [x] In log ra console với format đẹp
- [x] Tạo requirements.txt
- [x] Viết README hướng dẫn

---

## 📞 Support
Nếu gặp vấn đề, check:
1. Camera có bật không? (`camera.isOpened()`)
2. Backend API có chạy không? (Postman test)
3. Port 5001 có bị chiếm không? (Đổi sang 5002)

---

**🎉 Chúc bạn demo thành công!**
