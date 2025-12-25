"""
PetZone AI Service - Motion Detection & Video Streaming
========================================================
Chức năng:
1. Phát hiện chuyển động bằng Background Subtraction (OpenCV)
2. Stream video real-time qua HTTP để Frontend hiển thị
3. Gửi trạng thái phát hiện thú cưng lên Backend .NET API
"""

import cv2
import numpy as np
import requests
import time
from flask import Flask, Response
from threading import Thread
import datetime

# ============ CẤU HÌNH ============
BACKEND_API_URL = "http://localhost:5000/api/ai/status"  # Thay đổi theo Backend của bạn
CAMERA_INDEX = 0  # 0 = Webcam mặc định
MOTION_THRESHOLD = 500  # Số pixel thay đổi để coi là có chuyển động
CHECK_INTERVAL = 3  # Gửi API mỗi 3 giây
NO_MOTION_TIMEOUT = 10  # Sau 10s không có chuyển động → Chuồng trống

app = Flask(__name__)

# ============ BIẾN TOÀN CỤC ============
camera = None
output_frame = None
has_pet = False
last_motion_time = time.time()
background_subtractor = None


def init_camera():
    """Khởi tạo camera"""
    global camera, background_subtractor
    camera = cv2.VideoCapture(CAMERA_INDEX)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    # Sử dụng MOG2 Background Subtractor (tốt hơn cho motion detection)
    background_subtractor = cv2.createBackgroundSubtractorMOG2(
        history=500,  # Số frame lưu lịch sử
        varThreshold=16,  # Ngưỡng phát hiện
        detectShadows=True  # Loại bỏ bóng
    )
    
    print("✅ Camera khởi tạo thành công!")


def detect_motion(frame):
    """
    Phát hiện chuyển động trong frame
    Returns: (có chuyển động?, frame với khung vẽ)
    """
    global background_subtractor
    
    # Chuyển sang grayscale và làm mờ để giảm noise
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    
    # Áp dụng background subtraction
    fg_mask = background_subtractor.apply(gray)
    
    # Loại bỏ bóng (giá trị 127) và chỉ lấy foreground (255)
    _, fg_mask = cv2.threshold(fg_mask, 244, 255, cv2.THRESH_BINARY)
    
    # Morphological operations để loại bỏ noise
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_CLOSE, kernel)
    fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, kernel)
    
    # Đếm số pixel chuyển động
    motion_pixels = cv2.countNonZero(fg_mask)
    
    # Tìm contours (viền của vật thể chuyển động)
    contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    motion_detected = False
    annotated_frame = frame.copy()
    
    # Vẽ hình chữ nhật quanh vùng chuyển động
    for contour in contours:
        if cv2.contourArea(contour) > 500:  # Bỏ qua vùng nhỏ
            motion_detected = True
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(annotated_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
    # Hiển thị thông tin lên frame
    status_text = "🟢 PHÁT HIỆN THÚ CƯNG" if motion_detected else "🔴 CHUỒNG TRỐNG"
    color = (0, 255, 0) if motion_detected else (0, 0, 255)
    
    cv2.putText(annotated_frame, status_text, (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
    cv2.putText(annotated_frame, f"Motion Pixels: {motion_pixels}", (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    cv2.putText(annotated_frame, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
                (10, annotated_frame.shape[0] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    return motion_detected or motion_pixels > MOTION_THRESHOLD, annotated_frame


def send_status_to_backend(has_pet_status):
    """Gửi trạng thái phát hiện lên Backend API"""
    try:
        payload = {
            "hasPet": has_pet_status,
            "detectionMethod": "MotionDetection",
            "timestamp": datetime.datetime.now().isoformat(),
            "confidence": 0.85 if has_pet_status else 0.95
        }
        
        response = requests.post(BACKEND_API_URL, json=payload, timeout=5)
        
        if response.status_code == 200:
            print(f"✅ Đã gửi API: hasPet={has_pet_status}")
        else:
            print(f"⚠️ API trả về lỗi: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Lỗi kết nối Backend: {e}")


def process_video_stream():
    """Thread xử lý video và phát hiện chuyển động"""
    global output_frame, has_pet, last_motion_time
    
    last_api_call = time.time()
    
    while True:
        success, frame = camera.read()
        if not success:
            print("⚠️ Không thể đọc frame từ camera")
            time.sleep(1)
            continue
        
        # Phát hiện chuyển động
        motion_detected, annotated_frame = detect_motion(frame)
        
        # Cập nhật trạng thái
        current_time = time.time()
        if motion_detected:
            has_pet = True
            last_motion_time = current_time
        else:
            # Nếu không có chuyển động trong NO_MOTION_TIMEOUT giây
            if current_time - last_motion_time > NO_MOTION_TIMEOUT:
                has_pet = False
        
        # Gửi API mỗi CHECK_INTERVAL giây
        if current_time - last_api_call >= CHECK_INTERVAL:
            send_status_to_backend(has_pet)
            last_api_call = current_time
        
        # In log ra console
        status_emoji = "🐾" if has_pet else "⭕"
        status_text = "Phát hiện thú cưng" if has_pet else "Chuồng trống"
        print(f"{status_emoji} [{datetime.datetime.now().strftime('%H:%M:%S')}] {status_text}")
        
        # Cập nhật frame cho streaming
        output_frame = annotated_frame.copy()


def generate_frames():
    """Generator để stream video qua HTTP"""
    global output_frame
    
    while True:
        if output_frame is None:
            continue
        
        # Encode frame sang JPEG
        ret, buffer = cv2.imencode('.jpg', output_frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
        frame_bytes = buffer.tobytes()
        
        # Trả về frame dưới dạng multipart stream
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        
        time.sleep(0.033)  # ~30 FPS


# ============ FLASK ROUTES ============
@app.route('/video_feed')
def video_feed():
    """Endpoint để Frontend lấy video stream"""
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/status')
def get_status():
    """Endpoint để Frontend lấy trạng thái hiện tại"""
    return {
        "hasPet": has_pet,
        "lastMotionTime": last_motion_time,
        "timestamp": time.time()
    }


@app.route('/health')
def health():
    """Health check endpoint"""
    return {"status": "running", "camera": camera is not None and camera.isOpened()}


# ============ MAIN ============
if __name__ == "__main__":
    print("=" * 60)
    print("🐾 PETZONE AI SERVICE - MOTION DETECTION & STREAMING")
    print("=" * 60)
    
    # Khởi tạo camera
    init_camera()
    
    # Chờ camera ổn định
    print("⏳ Đang khởi động camera...")
    time.sleep(2)
    
    # Bắt đầu thread xử lý video
    print("🚀 Bắt đầu phát hiện chuyển động...")
    video_thread = Thread(target=process_video_stream, daemon=True)
    video_thread.start()
    
    # Chạy Flask server
    print("\n📡 Video streaming:")
    print(f"   → http://localhost:5001/video_feed")
    print(f"\n📊 Status API:")
    print(f"   → http://localhost:5001/status")
    print(f"\n💡 Backend API: {BACKEND_API_URL}")
    print("\n⏹️  Nhấn Ctrl+C để dừng\n")
    
    try:
        app.run(host='0.0.0.0', port=5001, threaded=True, debug=False)
    except KeyboardInterrupt:
        print("\n\n👋 Đang dừng AI Service...")
        if camera:
            camera.release()
        print("✅ Đã dừng!")
