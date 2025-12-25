# 📋 PLAN: HỆ THỐNG IOT & AI CHĂM SÓC THÚ CƯNG (PET ZONE)
**Môn học:** Chuyển đổi số
**Mục tiêu:** Demo MVP (Minimum Viable Product) hệ thống giám sát chuồng nuôi thông minh.

---

## 🛠️ 1. TECH STACK & PHẦN CỨNG
[cite_start]Dựa trên yêu cầu đồ án[cite: 17, 39]:
* **Hardware:** ESP32 (Core), HLK-LD2410C (Radar), DHT11 (Temp/Hum), Servo (Feeder), Relay (Fan), Webcam.
* **Frontend:** ReactJS (Dashboard quản lý).
* **Backend:** .NET Core Web API.
* **Database:** PostgreSQL (hoặc SQL Server).
* **AI:** Python Script (OpenCV/YOLO).

---

## 🗓️ GIAI ĐOẠN 1: SETUP & DATABASE
*(Mục tiêu: Chuẩn bị nền tảng lưu trữ dữ liệu)*

- [ ] **Cài đặt môi trường:**
    - [ ] Cài đặt .NET SDK, Node.js, PostgreSQL/SQL Server.
    - [ ] Cài đặt Arduino IDE (thêm board ESP32).
    - [ ] Cài đặt Python & thư viện (opencv-python, requests).
- [ ] [cite_start]**Thiết kế Database (PostgreSQL):** [cite: 21]
    - [ ] Table `SensorLogs`: `Id`, `Temperature`, `Humidity`, `PresenceEnergy`, `MovementEnergy`, `CreatedAt`.
    - [ ] Table `PetStatus`: `Id`, `IsPresent` (Có thú cưng không?), `ActivityState` (Ngủ/Thức), `Timestamp`.
    - [ ] Table `DeviceHistory`: `Id`, `DeviceName` (Fan/Feeder), `Action` (On/Off/Feed), `Timestamp`.
    - [ ] Table `ControlCommands`: `Id`, `DeviceName` (Fan/Feeder), `Action` (Feed/TurnOn/TurnOff), `Status` (Pending/Executed), `CreatedAt`, `ExecutedAt`.
        - **Lý do:** Dùng để ESP32 polling lệnh điều khiển từ ReactJS. Khi người dùng bấm "Cho ăn", tạo record `Status=Pending`. ESP32 đọc và thực hiện, sau đó update `Status=Executed`.
- [ ] **Khởi tạo Backend Project:**
    - [ ] Tạo solution .NET Core Web API.
    - [ ] Cấu hình Entity Framework Core (Database First hoặc Code First).
    - [ ] Kiểm tra kết nối Database thành công.

---

## 🔌 GIAI ĐOẠN 2: LẬP TRÌNH PHẦN CỨNG (IOT - ESP32)
[cite_start]*(Mục tiêu: Đọc cảm biến và điều khiển thiết bị theo danh sách [cite: 16])*

- [ ] **Đấu nối mạch (Wiring):**
    - [ ] DHT11 nối GPIO (VD: D15).
    - [ ] Relay nối GPIO (VD: D4).
    - [ ] Servo nối GPIO (VD: D18).
    - [ ] HLK-LD2410C nối Serial2 (TX2/RX2 - GPIO 16/17).
- [ ] **Code Firmware (Arduino C++):**
    - [ ] **Task 1 (Mạng):** Kết nối Wifi dùng thư viện `WiFi.h`.
    - [ ] **Task 2 (Môi trường):** Đọc nhiệt độ/độ ẩm từ DHT11.
    - [ ] **Task 3 (Sự sống):** Đọc dữ liệu UART từ HLK-LD2410C. [cite_start]Tách lấy 2 chỉ số quan trọng: `stat_energy` (năng lượng tĩnh) và `m_energy` (năng lượng động)[cite: 30].
        - ⚠️ **Cảnh báo:** Cảm biến này trả frame binary phức tạp (header `0xF4F3F2F1`, checksum). **Tìm thư viện có sẵn** như `ld2410` trong Arduino Library Manager thay vì tự viết parser để tiết kiệm thời gian.
    - [ ] **Task 4 (HTTP Client):** Gửi dữ liệu (Temp, Hum, Energy) lên API `.NET Core` mỗi 5 giây (`HTTPClient.h`).
    - [ ] **Task 5 (Điều khiển):**
        - [ ] [cite_start]Logic tại chỗ: Nếu `Temp > 30` -> Kích Relay (Quạt quay)[cite: 27].
        - [ ] [cite_start]Logic từ xa: Nhận lệnh từ API -> Quay Servo 90 độ (Cho ăn)[cite: 34].
        - 💡 **Cơ chế đề xuất (HTTP Polling - đơn giản cho MVP):**
            - ESP32 gọi `GET /api/control/commands/pending` mỗi 3 giây.
            - Nếu có lệnh (`Status=Pending`), thực hiện → Gọi `POST /api/control/commands/{id}/executed`.
            - *Lưu ý: Có delay 1-3s, nhưng đơn giản hơn MQTT. Nếu cần realtime thật sự, xem xét thêm MQTT broker.*

---

## 💻 GIAI ĐOẠN 3: BACKEND DEVELOPMENT (.NET CORE)
[cite_start]*(Mục tiêu: API trung gian xử lý logic và giao tiếp dữ liệu [cite: 20])*

- [ ] **Controller: SensorDataController**
    - [ ] `POST /api/sensors`: Nhận dữ liệu JSON từ ESP32 và lưu vào DB.
    - [ ] `GET /api/sensors/latest`: Trả về dữ liệu mới nhất cho Frontend vẽ biểu đồ.
- [ ] **Controller: DeviceControlController**
    - [ ] `POST /api/control/feed`: Nhận yêu cầu từ ReactJS, tạo record trong `ControlCommands` với `Status=Pending`.
    - [ ] `GET /api/control/commands/pending`: ESP32 polling để lấy lệnh chưa thực hiện.
    - [ ] `POST /api/control/commands/{id}/executed`: ESP32 gọi sau khi thực hiện xong để update `Status=Executed`.
- [ ] **Controller: AIStatusController**
    - [ ] `POST /api/ai/status`: Nhận kết quả từ Python script (Có thú/Không có thú).

---

## 👁️ GIAI ĐOẠN 4: AI SERVICE (PYTHON)
[cite_start]*(Mục tiêu: Nhận diện hình ảnh từ Webcam [cite: 35])*

- [ ] **Viết Script Python:**
    - [ ] Mở Webcam Laptop bằng OpenCV.
    - [ ] **Plan A (Đề xuất cho MVP):** Phát hiện chuyển động (Motion Detection - Background Subtraction) - Nhanh, mượt, dễ implement.
    - [ ] **Plan B (Nếu có thời gian):** Dùng YOLOv8 (detect class: Cat/Dog) - Chạy mỗi 3-5 giây (không cần realtime) để tránh lag nếu chạy trên CPU.
    - ⚠️ **Cảnh báo:** YOLOv8 trên CPU (không GPU) chỉ đạt ~2-5 FPS, có thể giật lag. Motion Detection đơn giản hơn và đủ cho demo.
- [ ] **Xử lý Logic gửi API:**
    - [ ] Nếu phát hiện đối tượng -> Gửi JSON `{ "hasPet": true }` lên API `.NET Core`.
    - [ ] Nếu không thấy trong 10s -> Gửi JSON `{ "hasPet": false }`.
    - [ ] [cite_start]In log ra màn hình console: "Phát hiện thú cưng" / "Chuồng trống"[cite: 37, 38].

---

## 🖥️ GIAI ĐOẠN 5: FRONTEND (REACTJS)
[cite_start]*(Mục tiêu: Dashboard hiển thị trạng thái và điều khiển [cite: 19])*

- [ ] **Thiết kế UI Dashboard:**
    - [ ] Card 1: Nhiệt độ & Độ ẩm (Hiện màu đỏ nếu > 30 độ).
    - [ ] Card 2: Trạng thái thú cưng (Ngủ/Thức/Vắng mặt).
    - [ ] Card 3: Camera View (Nếu tích hợp được) hoặc Text trạng thái AI.
    - [ ] Button: "Cho ăn ngay" (Kích thước lớn, dễ bấm).
- [ ] **Tích hợp API:**
    - [ ] Sử dụng `axios` hoặc `fetch` để gọi API Backend.
    - [ ] Set interval 3-5 giây để refresh dữ liệu tự động (Polling với `async/await` + loading state để tránh blocking UI).
    - [ ] [cite_start]Xử lý sự kiện nút bấm "Cho ăn ngay" -> Gọi `POST /api/control/feed` và hiện thông báo "Đã gửi lệnh cho ăn"[cite: 33].
    - 💡 **Kỹ thuật:** Dùng `useEffect` với `setInterval` và cleanup function để tránh memory leak.

---

## � GIAI ĐOẠN 6: THỨ TỰ ƯU TIÊN THỰC HIỆN
*(Để đảm bảo demo sớm nhất và giảm thiểu rủi ro)*

**🎯 Ưu tiên cao (Làm trước - Nền tảng cốt lõi):**
1. ESP32 đọc DHT11 + Gửi HTTP POST lên Backend → Lưu DB.
2. Backend API `GET /api/sensors/latest` → ReactJS hiển thị nhiệt độ/độ ẩm realtime.
3. Logic tự động hóa: `Temp > 30` → Relay → Quạt quay (Demo tại chỗ).
4. ReactJS Dashboard cơ bản với 3 cards + Button "Cho ăn".

**⚙️ Ưu tiên trung bình (Làm tiếp - Tương tác 2 chiều):**
5. Cơ chế điều khiển từ xa: ReactJS → Backend → ESP32 polling → Servo quay.
6. AI Service đơn giản: Motion Detection (OpenCV) → Gửi `hasPet: true/false` lên Backend.

**🌟 Ưu tiên thấp (Làm cuối - Điểm cộng thêm):**
7. HLK-LD2410C (Radar phát hiện sự sống) - Chỉ làm nếu còn thời gian vì parsing phức tạp.
8. Nâng cấp AI lên YOLOv8 (detect Cat/Dog cụ thể) - Nếu có GPU hoặc chấp nhận FPS thấp.

---

## 🚀 GIAI ĐOẠN 7: KỊCH BẢN DEMO (QUAN TRỌNG)
[cite_start]*Chuẩn bị sẵn sàng để demo 4 chức năng ăn điểm tuyệt đối *

1.  [cite_start]**Demo 1: Giám sát môi trường & Tự động hóa** [cite: 25]
    * [ ] Hành động: Hà hơi nóng vào cảm biến DHT11.
    * [ ] Kết quả mong đợi: Web hiện nhiệt độ tăng -> Relay đóng -> Quạt quay.

2.  [cite_start]**Demo 2: Giám sát sự sống & Giấc ngủ (HLK-LD2410C)** [cite: 28]
    * [ ] Hành động: Để yên cảm biến trước ngực (giả lập ngủ).
    * [ ] Kết quả mong đợi: Web báo "Thú cưng đang ngủ/nghỉ ngơi".
    * [ ] Hành động: Cử động tay mạnh trước cảm biến.
    * [ ] Kết quả mong đợi: Web báo "Đang vận động".

3.  [cite_start]**Demo 3: Cho ăn từ xa** [cite: 32]
    * [ ] Hành động: Nhấn nút "Cho ăn ngay" trên ReactJS.
    * [ ] Kết quả mong đợi: Servo quay góc 90 độ (xả thức ăn).

4.  [cite_start]**Demo 4: Nhận diện hình ảnh (AI)** [cite: 35]
    * [ ] Hành động: Đưa ảnh chó/mèo vào trước Webcam.
    * [ ] Kết quả mong đợi: Web hiện "Phát hiện thú cưng trong chuồng".
    * [ ] Hành động: Che camera.
    * [ ] Kết quả mong đợi: Web hiện "Chuồng trống".