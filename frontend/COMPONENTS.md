# 🎨 Components Architecture & Detailed Guide

## Mục Lục
- [TemperatureCard](#temperaturecard)
- [PetStatusCard](#petstatuscard)
- [AIStatusCard](#aistatuscard)
- [FeedButton](#feedbutton)
- [Header](#header)
- [Footer](#footer)

---

## TemperatureCard

### 📍 Location
`src/components/TemperatureCard.jsx`

### 🎯 Purpose
Hiển thị **Nhiệt độ & Độ ẩm** với các chỉ báo trực quan

### 🎨 Design Features
```
┌─────────────────────────────────────┐
│ 🌡️  Môi Trường                      │
├─────────────────────────────────────┤
│ Nhiệt độ:         28.5°C            │
│ ████████████░░░░░░░░░░ (71%)       │
│                                     │
│ 💧 Độ ẩm:         65.2%             │
│ ██████████████░░░░░░░░░░ (65%)     │
└─────────────────────────────────────┘
```

### 📊 Props
| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `temperature` | number | 28 | Nhiệt độ (°C) |
| `humidity` | number | 65 | Độ ẩm (%) |
| `loading` | boolean | false | Show loading spinner |

### 🎨 Color Logic
```javascript
// Color based on temperature
if (temperature > 30) {
  // Red/Orange - HOT (Bật quạt)
  color = 'from-red-600 to-orange-500'
} else if (temperature < 18) {
  // Blue/Cyan - COLD
  color = 'from-blue-600 to-cyan-500'
} else {
  // Green - NORMAL
  color = 'from-green-600 to-emerald-500'
}
```

### ✨ Animations
- **Pulse effect** khi nóng (temperature > 30°C)
- Progress bars animate from 0 to value
- Smooth hover transition
- Loading spinner

### 💡 Usage Example
```jsx
import TemperatureCard from './components/TemperatureCard';

<TemperatureCard 
  temperature={28.5}
  humidity={65.2}
  loading={false}
/>
```

### 🔧 Customization
```jsx
// Thay đổi threshold nhiệt độ
const getTempColor = () => {
  if (temperature > 35) return 'from-red-700 to-orange-600'; // Critical hot
  if (temperature > 30) return 'from-red-600 to-orange-500';  // Hot
  // ...
}
```

---

## PetStatusCard

### 📍 Location
`src/components/PetStatusCard.jsx`

### 🎯 Purpose
Hiển thị **Trạng thái thú cưng** (Ngủ/Thức/Vắng) với pulse animations

### 🎨 Design Features
```
┌─────────────────────────────────────┐
│ ❤️ Trạng Thái Thú Cưng              │
├─────────────────────────────────────┤
│ 🌙 Đang Ngủ                        │
│ (Thú cưng đang nghỉ ngơi)          │
│                                     │
│ ✓ Thú cưng có mặt                  │
│                                     │
│ Năng lượng tĩnh: ████░░░░░░       │
│ Năng lượng động: ██████░░░░░░      │
└─────────────────────────────────────┘
```

### 📊 Props
| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `isPresent` | boolean | true | Thú cưng có mặt hay không |
| `activityState` | string | 'awake' | 'awake' \| 'sleeping' \| 'absent' |
| `loading` | boolean | false | Show loading spinner |

### 🎨 Status States
```javascript
const states = {
  awake: {
    title: 'Đang Thức',
    icon: Eye,
    color: 'from-green-600 to-teal-600',
    pulse: true
  },
  sleeping: {
    title: 'Đang Ngủ',
    icon: Moon,
    color: 'from-indigo-600 to-purple-600',
    pulse: true
  },
  absent: {
    title: 'Chuồng Trống',
    icon: AlertCircle,
    color: 'from-gray-600 to-slate-600',
    pulse: false
  }
}
```

### ✨ Animations
- **Heartbeat animation** - ❤️ pulsing
- **Breathing effect** - gradient fades in/out
- **Energy bars** - random wave animations
- **Smooth state transitions**

### 💡 Usage Example
```jsx
import PetStatusCard from './components/PetStatusCard';

<PetStatusCard 
  isPresent={true}
  activityState="awake"
  loading={false}
/>
```

### 🔧 Customization
```jsx
// Thêm activity state mới
case 'playing':
  return {
    title: 'Đang Chơi',
    description: 'Thú cưng đang vui vẻ',
    color: 'from-yellow-600 to-orange-600',
    icon: Zap,
    pulse: true,
  };
```

---

## AIStatusCard

### 📍 Location
`src/components/AIStatusCard.jsx`

### 🎯 Purpose
Hiển thị **Kết quả nhận diện AI** từ Camera (Có thú cưng / Không)

### 🎨 Design Features
```
┌─────────────────────────────────────┐
│ 📷 Nhận Diện AI                     │
├─────────────────────────────────────┤
│ ✓ Phát Hiện Thú Cưng               │
│ (AI nhận diện có thú cưng)          │
│                                     │
│ Độ tin cây: ███████████░░░ (95%)   │
│                                     │
│ 🟢 Tình trạng Camera: Hoạt động     │
│                                     │
│ [Motion Detection] [Real-time]     │
└─────────────────────────────────────┘
```

### 📊 Props
| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `hasPet` | boolean | true | Có phát hiện thú cưng |
| `confidence` | number | 0.95 | Độ tin cây (0-1) |
| `loading` | boolean | false | Show loading spinner |

### 🎨 Detection States
```javascript
const states = {
  detected: {
    title: 'Phát Hiện Thú Cưng',
    icon: CheckCircle,
    color: 'from-pink-600 to-rose-600',
    textColor: 'text-pink-300'
  },
  notDetected: {
    title: 'Chuồng Trống',
    icon: AlertCircle,
    color: 'from-slate-600 to-gray-600',
    textColor: 'text-slate-300'
  }
}
```

### ✨ Animations
- **Glow effect** - khi phát hiện thú cưng
- **Confidence bar** - fills from 0 to percentage
- **Pulsing indicator** - camera status light
- **Smooth fade-in-out**

### 💡 Usage Example
```jsx
import AIStatusCard from './components/AIStatusCard';

<AIStatusCard 
  hasPet={true}
  confidence={0.95}
  loading={false}
/>
```

### 🔧 Customization
```jsx
// Thay đổi detection badges
<span className="px-3 py-1 rounded-full bg-gradient-to-r from-cyan-500/30 to-blue-500/30 border border-cyan-500/50 text-cyan-300">
  🎯 YOLOv8 Detection {/* Thay từ Motion Detection */}
</span>
```

---

## FeedButton

### 📍 Location
`src/components/FeedButton.jsx`

### 🎯 Purpose
**Nút điều khiển cho ăn** - Gửi lệnh tới Servo (quay 90°)

### 🎨 Design Features
```
┌─────────────────────────────────────┐
│                                     │
│      ┌─────────────────────┐       │
│      │ ➤ Cho Ăn Ngay       │       │
│      └─────────────────────┘       │
│    (Large, prominent, glowing)     │
│                                     │
│ ✓ Đã gửi lệnh cho ăn!             │
│   Servo đang quay...               │
└─────────────────────────────────────┘
```

### 📊 Props
| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `onClick` | function | () => {} | Callback khi click |
| `loading` | boolean | false | Show loading state |
| `disabled` | boolean | false | Disable button |

### 🎨 Button States
```javascript
// Normal
background: 'from-orange-500 to-red-500'
icon: Send
opacity: 1

// Hover
background: 'from-orange-600 to-red-600'
scale: 1.05
glow: active

// Loading
icon: Loader (spinning)
text: 'Đang Gửi...'
disabled: true

// Disabled
opacity: 0.5
cursor: not-allowed
```

### ✨ Animations
- **Shine effect** - moving gradient overlay
- **Pulse ring** - expanding border
- **Heat glow** - background blur animation
- **Button scale** - on hover & click
- **Icon animation** - loading spinner
- **Toast slide-in** - feedback notification

### 💡 Usage Example
```jsx
import FeedButton from './components/FeedButton';

const handleFeed = async () => {
  // Send to API
  await controlAPI.feed();
};

<FeedButton 
  onClick={handleFeed}
  loading={loadingFeed}
  disabled={false}
/>
```

### 🔧 Customization
```jsx
// Thay đổi button size & text
<button className={`py-8 px-10 text-2xl`}>
  {'🍽️ Cho Ăn Ngay'}
</button>

// Thay đổi feedback messages
feedback={feedbackType === 'success'
  ? '✅ Lệnh đã gửi! Servo quay 90°'
  : '❌ Lỗi. Vui lòng thử lại.'
}
```

---

## Header

### 📍 Location
`src/components/Header.jsx`

### 🎯 Purpose
**Sticky header** - Logo, tiêu đề, status indicators

### 🎨 Features
```
┌──────────────────────────────────────┐
│ 🐾 PetZone                 ✓ Kết nối │
│ Smart Pet Cage...    Cập nhật: 10:30 │
└──────────────────────────────────────┘
```

### 📊 Props
| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `isConnected` | boolean | true | Kết nối Backend |
| `lastUpdate` | Date | null | Lần cập nhật cuối |

### ✨ Features
- Sticky position (top: 0, z-index: 50)
- Rotating paw emoji logo
- Connection status indicator
- Last update timestamp
- Responsive (hides timestamp on mobile)

---

## Footer

### 📍 Location
`src/components/Footer.jsx`

### 🎯 Purpose
**Footer** - Thông tin dự án, tech stack, links

### 🎨 Features
- Tech stack list
- Quick links
- Copyright info
- Heart beating animation
- Responsive grid layout

---

## 🔗 Component Relationships

```
App.jsx (Main State Management)
├── Header
│   ├── Connection Status
│   └── Last Update Time
├── Main Content
│   ├── Cards Grid
│   │   ├── TemperatureCard (Temperature, Humidity)
│   │   ├── PetStatusCard (Activity State)
│   │   ├── AIStatusCard (Detection Confidence)
│   │   └── Stats Boxes
│   └── FeedButton
│       └── Toast Feedback
└── Footer
```

---

## 🎯 Props Flow

```
App (State)
│
├─ temperature ──────> TemperatureCard
├─ humidity ─────────> TemperatureCard
│
├─ isPresent ────────> PetStatusCard
├─ activityState ───> PetStatusCard
│
├─ hasPet ──────────> AIStatusCard
├─ confidence ──────> AIStatusCard
│
├─ loadingFeed ─────> FeedButton
└─ isConnected ─────> Header
```

---

## 🧪 Testing Components Individually

### Storybook Example
```jsx
// src/stories/TemperatureCard.stories.jsx
import { TemperatureCard } from '../components/TemperatureCard';

export default {
  title: 'Components/TemperatureCard',
  component: TemperatureCard,
};

export const Normal = {
  args: {
    temperature: 25,
    humidity: 60,
  },
};

export const Hot = {
  args: {
    temperature: 32,
    humidity: 45,
  },
};
```

---

## 📚 Best Practices Applied

✅ **Reusable Components** - Each component is independent  
✅ **Props-driven** - Data flows via props only  
✅ **Error Boundaries** - Loading & error states  
✅ **Animations** - Framer Motion for smooth UX  
✅ **Responsive** - Tailwind responsive classes  
✅ **Accessibility** - Semantic HTML, ARIA labels (can improve)  
✅ **Performance** - useEffect cleanup, no memory leaks  

---

## 🚀 Next Steps

1. **Connect to Backend API** - Replace mock data with real API calls
2. **Add Error Boundaries** - Wrap components with error handling
3. **Implement Toast System** - Global notification service
4. **Add Unit Tests** - Jest + React Testing Library
5. **Add Storybook** - Component documentation & testing
6. **Deploy to Production** - Vercel, Netlify, or AWS

---

**Ready to build amazing UI! 🎨✨**
