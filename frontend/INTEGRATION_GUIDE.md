# 🔗 Frontend - Backend Integration Guide

## Tổng Quan
Phần Frontend hiện dùng **Mock Data** để demo UI. Khi Backend (.NET Core) sẵn sàng, chúng ta sẽ thay thế mock data bằng real API calls.

---

## 📊 Dòng Dữ Liệu (Data Flow)

```
┌─────────────────────────────────────────┐
│ Frontend (React)                        │
│ - Real-time polling (3-5 giây)         │
│ - Update UI state                      │
└──────────────┬──────────────────────────┘
               │ HTTP Request (Axios)
               ↓
┌──────────────────────────────────────────┐
│ Backend (.NET Core API)                 │
│ - Controllers (SensorController, etc)  │
│ - Entity Framework Core                │
│ - SQL Queries                          │
└──────────────┬──────────────────────────┘
               │ HTTP Response (JSON)
               ↓
┌──────────────────────────────────────────┐
│ Database (PostgreSQL / SQL Server)      │
│ - SensorLogs Table                      │
│ - PetStatus Table                       │
│ - DeviceHistory Table                   │
│ - ControlCommands Table                 │
└──────────────────────────────────────────┘
               │
               ↓
┌──────────────────────────────────────────┐
│ Hardware (ESP32)                        │
│ - Reads sensors (DHT11, Radar, etc)    │
│ - Executes commands (Servo, Relay)     │
│ - Sends data to API                    │
└──────────────────────────────────────────┘
```

---

## 🔄 API Endpoints Required

### 📡 **Sensors Controller**
```
GET /api/sensors/latest
├─ Response: {
│   "temperature": 28.5,
│   "humidity": 65.2,
│   "presenceEnergy": 120,
│   "movementEnergy": 45,
│   "timestamp": "2024-12-22T10:30:00Z"
│ }
└─ Used by: TemperatureCard component

POST /api/sensors
├─ Request: { temp, humidity, presenceEnergy, movementEnergy }
└─ Used by: ESP32 to send sensor data
```

### 🎮 **Control Controller**
```
POST /api/control/feed
├─ Request: {}
├─ Response: { "commandId": 1, "status": "pending" }
└─ Used by: FeedButton component

GET /api/control/commands/pending
├─ Response: [
│   { "id": 1, "deviceName": "Feeder", "action": "Feed" },
│   { "id": 2, "deviceName": "Fan", "action": "TurnOn" }
│ ]
└─ Used by: ESP32 polling

POST /api/control/commands/{id}/executed
├─ Request: {}
└─ Used by: ESP32 to confirm execution
```

### 🤖 **AI Status Controller**
```
GET /api/ai/pet-status
├─ Response: {
│   "isPresent": true,
│   "activityState": "awake",  // awake | sleeping | absent
│   "hasPet": true,
│   "confidence": 0.95,
│   "lastSeen": "2024-12-22T10:30:00Z"
│ }
└─ Used by: PetStatusCard & AIStatusCard components

POST /api/ai/status
├─ Request: { "hasPet": true, "confidence": 0.95 }
└─ Used by: Python AI service
```

---

## 🔧 Steps to Connect Backend

### **Step 1: Backend Setup (Task.md Giai Đoạn 3)**
Cần tạo 3 Controllers trong .NET Core:
1. ✅ **SensorDataController** - GET latest sensors
2. ✅ **DeviceControlController** - POST feed, GET pending
3. ✅ **AIStatusController** - GET/POST pet status

### **Step 2: Update API Base URL**

Edit file: **`src/api/client.js`**

```javascript
// ❌ BEFORE (localhost)
const API_BASE_URL = 'http://localhost:5000/api';

// ✅ AFTER (production)
const API_BASE_URL = 'http://your-server.com/api';
// hoặc lấy từ environment variable:
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';
```

### **Step 3: Replace Mock Calls with Real API**

Edit file: **`src/App.jsx`**

**Before (Mock):**
```jsx
// Line ~48
useEffect(() => {
  const interval = setInterval(() => {
    const newData = generateMockData();  // ← Mock function
    setTemperature(newData.temperature);
    // ...
  }, 3000);
}, []);
```

**After (Real API):**
```jsx
useEffect(() => {
  const interval = setInterval(async () => {
    try {
      setLoadingTemp(true);
      const response = await sensorAPI.getLatest();  // ← Real API call
      const { temperature, humidity } = response.data;
      setTemperature(temperature);
      setHumidity(humidity);
      setLastUpdate(new Date());
    } catch (error) {
      console.error('Sensor API Error:', error);
      setIsConnected(false);
    } finally {
      setLoadingTemp(false);
    }
  }, 3000);
  
  return () => clearInterval(interval);
}, []);
```

### **Step 4: Uncomment Real Feed API**

Edit file: **`src/App.jsx`** - `handleFeed` function

**Before:**
```jsx
const handleFeed = async () => {
  setLoadingFeed(true);
  try {
    // Mock call
    await new Promise((resolve) => setTimeout(resolve, 1000));
    console.log('✅ Mock feed sent');
  } finally {
    setLoadingFeed(false);
  }
};
```

**After:**
```jsx
const handleFeed = async () => {
  setLoadingFeed(true);
  try {
    const response = await controlAPI.feed();  // ← Real API
    console.log('✅ Feed command sent!', response);
  } catch (error) {
    console.error('❌ Feed error:', error);
    throw error;
  } finally {
    setLoadingFeed(false);
  }
};
```

### **Step 5: Setup CORS (if different domain)**

Nếu Frontend chạy ở http://localhost:5173 và Backend ở http://localhost:5000, cần config CORS:

**Backend (Program.cs):**
```csharp
var builder = WebApplication.CreateBuilder(args);

// Add CORS
builder.Services.AddCors(options =>
{
    options.AddPolicy("AllowFrontend", policy =>
    {
        policy.WithOrigins("http://localhost:5173", "http://localhost:3000")
              .AllowAnyMethod()
              .AllowAnyHeader();
    });
});

var app = builder.Build();
app.UseCors("AllowFrontend");
```

---

## 🧪 Testing Integration

### 1️⃣ **Backend Postman Test**
```bash
GET http://localhost:5000/api/sensors/latest
POST http://localhost:5000/api/control/feed
GET http://localhost:5000/api/ai/pet-status
```

### 2️⃣ **Frontend Network Tab**
1. Open Chrome DevTools (F12)
2. Go to **Network** tab
3. Reload page
4. Look for API calls to `/api/sensors/latest`, etc.

### 3️⃣ **Console Logs**
```javascript
// Add to src/App.jsx to debug
console.log('Fetching sensors...', sensorAPI.getLatest());
```

---

## 🚨 Error Handling

Current implementation includes:
- ✅ Try-catch in API calls
- ✅ Connection status indicator (Header)
- ✅ Loading states (spinner overlay)
- ✅ Toast notifications

**Improve with:**
```jsx
catch (error) {
  if (error.response?.status === 404) {
    console.error('Endpoint not found');
  } else if (error.request && !error.response) {
    console.error('No response from server - Check if Backend is running');
    setIsConnected(false);
  } else {
    console.error('Error:', error.message);
  }
}
```

---

## 📝 Example: Full Integration for Temperature Card

### **Backend (C#)**
```csharp
[ApiController]
[Route("api/[controller]")]
public class SensorsController : ControllerBase
{
    [HttpGet("latest")]
    public IActionResult GetLatest()
    {
        var sensor = _context.SensorLogs
            .OrderByDescending(s => s.CreatedAt)
            .FirstOrDefault();
            
        return Ok(new {
            sensor.Temperature,
            sensor.Humidity,
            sensor.PresenceEnergy,
            sensor.MovementEnergy,
            sensor.CreatedAt
        });
    }
}
```

### **Frontend (React)**
```jsx
// src/App.jsx
useEffect(() => {
  const interval = setInterval(async () => {
    try {
      setLoadingTemp(true);
      const response = await sensorAPI.getLatest();
      
      setTemperature(response.data.temperature);
      setHumidity(response.data.humidity);
      setPresenceEnergy(response.data.presenceEnergy);
      setMovementEnergy(response.data.movementEnergy);
      setLastUpdate(response.data.createdAt);
    } catch (error) {
      console.error('Failed to fetch sensors:', error);
    } finally {
      setLoadingTemp(false);
    }
  }, 3000);
  
  return () => clearInterval(interval);
}, []);

return (
  <TemperatureCard 
    temperature={temperature}
    humidity={humidity}
    loading={loadingTemp}
  />
);
```

---

## 🎯 Priority Integration Order

1. **Phase 1 (High)** - Sensor API
   - [ ] GET /api/sensors/latest
   - [ ] Connect Temperature & Humidity display

2. **Phase 2 (High)** - Control API
   - [ ] POST /api/control/feed
   - [ ] Connect Feed Button

3. **Phase 3 (Medium)** - AI Status API
   - [ ] GET /api/ai/pet-status
   - [ ] Connect Pet Status Card

4. **Phase 4 (Medium)** - Advanced
   - [ ] GET /api/control/commands/pending (ESP32 polling)
   - [ ] Error handling & retry logic
   - [ ] WebSocket for real-time (if needed)

---

## 📚 References

- **Axios Documentation** - https://axios-http.com/
- **React Hooks** - https://react.dev/reference/react
- **.NET Core API** - https://learn.microsoft.com/en-us/aspnet/core/
- **CORS** - https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS

---

**Ready to connect! Let's integrate the backend when it's ready. 🚀**
