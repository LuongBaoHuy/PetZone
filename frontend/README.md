# 🐾 PetZone Frontend - ReactJS Dashboard

## 📋 Tổng Quan
Dashboard quản lý hệ thống giám sát chuồng nuôi thú cưng thông minh. Gồm 4 chức năng chính:
1. **Temperature Card** - Giám sát nhiệt độ & độ ẩm
2. **Pet Status Card** - Trạng thái thú cưng (Ngủ/Thức/Vắng)
3. **AI Status Card** - Nhận diện hình ảnh từ Camera
4. **Feed Button** - Điều khiển cho ăn từ xa

---

## 🎨 Features & Design

### ✨ Tính Năng Nổi Bật
- **Dark Mode Modern UI** - Giao diện tối hiệu ứng gradient
- **Real-time Updates** - Polling dữ liệu mỗi 3-5 giây
- **Smooth Animations** - Framer Motion animations chuyên nghiệp
- **Responsive Design** - Hoạt động tốt trên mobile/tablet/desktop
- **Loading States** - Hiển thị loading spinner & feedback
- **Mock Data** - Có sẵn dữ liệu fake để test UI

### 🎯 UI Components
```
📦 src/components/
├── Header.jsx          # Navigation + Status indicator
├── TemperatureCard.jsx # Nhiệt độ & độ ẩm với progress bars
├── PetStatusCard.jsx   # Trạng thái thú cưng với heart animation
├── AIStatusCard.jsx    # Nhận diện AI + confidence meter
├── FeedButton.jsx      # Button điều khiển với toast feedback
└── Footer.jsx          # Footer thông tin & links
```

### 🔌 API Integration
```
📦 src/api/
├── client.js           # Axios client với configs
├── mockData.js         # Mock data generators
```

---

## 🚀 Getting Started

### 1️⃣ Cài Đặt Dependencies
```bash
cd frontend
npm install
```

### 2️⃣ Khởi Chạy Dev Server
```bash
npm run dev
```
Server sẽ chạy tại `http://localhost:5173` (hoặc 5174 nếu port bận)

### 3️⃣ Build Production
```bash
npm run build
```

---

## 📱 Component Details

### **TemperatureCard**
```jsx
<TemperatureCard 
  temperature={28}     // °C
  humidity={65}        // %
  loading={false}      // Show spinner
/>
```
- Hiển thị thermometer icon & progress bars
- Gradient color based on temperature (red if > 30°C)
- Real-time updates mỗi 3 giây

### **PetStatusCard**
```jsx
<PetStatusCard 
  isPresent={true}           // Thú cưng có/không
  activityState="awake"      // awake | sleeping | absent
  loading={false}
/>
```
- Heart icon với pulse animation
- Energy indicators (tĩnh/động)
- Status badge thay đổi color

### **AIStatusCard**
```jsx
<AIStatusCard 
  hasPet={true}              // Phát hiện được/không
  confidence={0.95}          // 0-1 (0-100%)
  loading={false}
/>
```
- Camera status indicator
- Confidence progress bar
- Detection mode badges

### **FeedButton**
```jsx
<FeedButton 
  onClick={handleFeed}       // Async callback
  loading={loadingFeed}      // Show spinner
  disabled={false}           // Disable state
/>
```
- Orange-red gradient button
- Toast feedback (success/error)
- Shine effect animation

---

## 🔗 API Endpoints (Cần Backend)

Khi backend (.NET Core) sẵn sàng, cập nhật endpoints tại `src/api/client.js`:

```javascript
// Sensors
POST   /api/sensors                    // Gửi dữ liệu từ ESP32
GET    /api/sensors/latest             // Lấy dữ liệu mới nhất

// Control
POST   /api/control/feed               // Gửi lệnh cho ăn
GET    /api/control/commands/pending   // Lấy lệnh chưa thực hiện (ESP32 polling)
POST   /api/control/commands/{id}/executed  // Cập nhật lệnh đã thực hiện

// AI Status
POST   /api/ai/status                  // Gửi kết quả từ Python script
GET    /api/ai/pet-status              // Lấy trạng thái thú cưng
```

---

## 🛠️ Tech Stack

| Công Nghệ | Mục Đích |
|-----------|---------|
| **React 18** | UI Framework |
| **Vite** | Build tool (nhanh hơn Webpack) |
| **Tailwind CSS** | Styling (utility-first) |
| **Framer Motion** | Animations |
| **Lucide React** | Icons library |
| **Axios** | HTTP client |

---

## 🎯 Workflow

### Current (Mock Data)
```
React State → Mock Data Generator → Re-render
     ↓
Every 3-5 seconds (setInterval)
```

### When Backend Ready
```
React State → useEffect → Axios GET/POST → Backend API → Database
     ↓
Real sensor data from ESP32 & AI service
```

---

## 📝 Hướng Dẫn Thay Đổi

### 1. Thay Đổi Polling Interval
```jsx
// src/App.jsx - dòng ~48
useEffect(() => {
  const interval = setInterval(() => {
    // Update logic
  }, 3000);  // ← Thay 3000ms (3 giây) thành interval khác
  
  return () => clearInterval(interval);
}, []);
```

### 2. Thay Đổi API Endpoints
```jsx
// src/api/client.js - dòng ~5
const API_BASE_URL = 'http://your-api-url:5000/api';
```

### 3. Kích Hoạt Real API (Bỏ Comment)
```jsx
// src/App.jsx - handleFeed function - dòng ~122
const handleFeed = async () => {
  setLoadingFeed(true);
  try {
    // Thay dòng này:
    // await new Promise((resolve) => setTimeout(resolve, 1000));
    
    // Bằng dòng này:
    const response = await controlAPI.feed();
    console.log('✅ Feed command sent!', response);
  } catch (error) {
    console.error('❌ Error:', error);
  } finally {
    setLoadingFeed(false);
  }
};
```

---

## 🐛 Troubleshooting

### Port bận (5173 đã dùng)
```bash
# Vite tự động chuyển sang 5174, 5175, ...
# Hoặc chỉ định port
npm run dev -- --port 3000
```

### Tailwind CSS không hoạt động
```bash
# Build lại
npm run dev

# Hoặc clear cache
rm -rf node_modules/.vite
npm run dev
```

### Components không render
- Check console (F12 -> Console tab)
- Verify import paths
- Ensure all components exported properly

---

## 📦 Project Structure
```
frontend/
├── index.html
├── package.json
├── tailwind.config.js
├── postcss.config.js
├── vite.config.js
└── src/
    ├── main.jsx
    ├── App.jsx          # Main app component
    ├── App.css
    ├── index.css
    ├── api/
    │   ├── client.js    # Axios setup
    │   └── mockData.js  # Fake data
    └── components/
        ├── Header.jsx
        ├── TemperatureCard.jsx
        ├── PetStatusCard.jsx
        ├── AIStatusCard.jsx
        ├── FeedButton.jsx
        └── Footer.jsx
```

---

## 🎓 Learning Resources

- **Tailwind CSS** - https://tailwindcss.com/docs
- **Framer Motion** - https://www.framer.com/motion/
- **Lucide Icons** - https://lucide.dev/
- **Axios** - https://axios-http.com/docs/intro
- **React Hooks** - https://react.dev/reference/react

---

## ✅ Demo Checklist

- [x] Dashboard UI đẹp & ấn tượng ✨
- [x] Real-time data updates (mock)
- [x] Responsive design (mobile-first)
- [x] Smooth animations & transitions
- [x] Loading states & error handling
- [x] Toast notifications
- [x] API integration ready
- [ ] Connect to real backend (pending)
- [ ] Connect to AI service (pending)
- [ ] Deploy to production

---

**Happy Coding! 🚀**

The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [this documentation](https://react.dev/learn/react-compiler/installation).

## Expanding the ESLint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and [`typescript-eslint`](https://typescript-eslint.io) in your project.
