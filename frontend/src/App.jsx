import React, { useState, useEffect, useCallback, useMemo } from 'react';
import { motion } from 'framer-motion';
import Header from './components/Header';
import Footer from './components/Footer';
import TemperatureCard from './components/TemperatureCard';
import PetStatusCard from './components/PetStatusCard';
import AIStatusCard from './components/AIStatusCard';
import FeedButton from './components/FeedButton';
import api from './services/api';
import './App.css';

function App() {
  // State for theme
  const [isDarkTheme, setIsDarkTheme] = useState(true);

  // State for sensor data
  const [temperature, setTemperature] = useState(28);
  const [humidity, setHumidity] = useState(65);
  const [presenceEnergy, setPresenceEnergy] = useState(45);
  const [movementEnergy, setMovementEnergy] = useState(120);
  const [lastUpdate, setLastUpdate] = useState(new Date());

  // State for pet status
  const [isPresent, setIsPresent] = useState(true);
  const [activityState, setActivityState] = useState('awake');

  // State for AI status
  const [hasPet, setHasPet] = useState(true);
  const [confidence, setConfidence] = useState(0.95);

  // Loading states
  const [loadingTemp, setLoadingTemp] = useState(false);
  const [loadingPet, setLoadingPet] = useState(false);
  const [loadingAI, setLoadingAI] = useState(false);
  const [loadingFeed, setLoadingFeed] = useState(false);

  // Connection status
  const [isConnected, setIsConnected] = useState(true);

  // State for API data
  const [apiError, setApiError] = useState(null);
  const [initialLoad, setInitialLoad] = useState(true);

  // Fetch dữ liệu từ API - dùng useCallback để tránh re-create
  const fetchSensorData = useCallback(async () => {
    setLoadingTemp(true);
    try {
      const response = await api.get('/api/Sensor/latest');
      const data = response.data;
      
      // Log để debug
      console.log('📊 Dữ liệu nhận được từ API:', data);
      
      // Cập nhật sensor data - hỗ trợ cả PascalCase (C#) và camelCase
      setTemperature(data.Temperature || data.temperature || 0);
      setHumidity(data.Humidity || data.humidity || 0);
      setPresenceEnergy(data.PresenceEnergy || data.presenceEnergy || 0);
      setMovementEnergy(data.MovementEnergy || data.movementEnergy || 0);
      setLastUpdate(new Date(data.CreatedAt || data.createdAt || new Date()));
      
      // Cập nhật pet status (từ radar data)
      const presEnergy = data.PresenceEnergy || data.presenceEnergy || 0;
      const moveEnergy = data.MovementEnergy || data.movementEnergy || 0;
      
      if (presEnergy > 30) {
        setIsPresent(true);
        setActivityState(moveEnergy > 100 ? 'awake' : 'sleeping');
      } else {
        setIsPresent(false);
        setActivityState('awake');
      }
      
      // Cập nhật AI detection (nếu có trong response)
      const hasPetData = data.HasPet !== undefined ? data.HasPet : data.hasPet;
      if (hasPetData !== undefined) {
        setHasPet(hasPetData);
        setConfidence(data.Confidence || data.confidence || 0.85);
      }
      
      setIsConnected(true);
      setApiError(null);
      
      console.log('✅ Dữ liệu đã được cập nhật:', {
        temp: data.Temperature || data.temperature,
        hum: data.Humidity || data.humidity,
        presEnergy,
        moveEnergy
      });
    } catch (error) {
      console.error('Lỗi khi lấy dữ liệu sensor:', error);
      
      // Xử lý các loại lỗi khác nhau
      if (error.response) {
        // Server trả về response nhưng có lỗi
        if (error.response.status === 404) {
          console.warn('⚠️ Chưa có dữ liệu sensor trong database');
          // Vẫn giữ kết nối là true, chỉ là chưa có dữ liệu
          setIsConnected(true);
          setApiError('Chưa có dữ liệu');
        } else {
          setIsConnected(false);
          setApiError(`Lỗi server: ${error.response.status}`);
        }
      } else if (error.request) {
        // Request được gửi nhưng không nhận được response
        console.error('❌ Không thể kết nối đến backend. Vui lòng kiểm tra:');
        console.error('- Backend có đang chạy tại http://localhost:5019?');
        console.error('- CORS có được cấu hình đúng không?');
        setIsConnected(false);
        setApiError('Không thể kết nối backend');
      } else {
        // Lỗi khác
        setIsConnected(false);
        setApiError(error.message);
      }
    } finally {
      setLoadingTemp(false);
      setInitialLoad(false);
    }
  }, []); // Empty dependency array vì function này không phụ thuộc state nào

  // Fetch data lần đầu khi component mount
  useEffect(() => {
    fetchSensorData();
  }, []);

  // Polling: Tự động fetch data mỗi 5 giây (tăng từ 3s để giảm tải)
  useEffect(() => {
    const interval = setInterval(() => {
      fetchSensorData();
    }, 5000);

    return () => clearInterval(interval);
  }, [fetchSensorData]);

  // Handle feed button click - Gửi lệnh cho ăn đến API
  const handleFeed = useCallback(async () => {
    setLoadingFeed(true);
    try {
      // Gọi API POST để tạo lệnh cho ăn
      const response = await api.post('/api/Feeding/feed');
      console.log('✅ Lệnh cho ăn đã được gửi!', response.data);
    } catch (error) {
      console.error('❌ Lỗi khi gửi lệnh cho ăn:', error);
    } finally {
      setLoadingFeed(false);
    }
  }, []);

  // Handle theme toggle
  const handleThemeToggle = useCallback((isDark) => {
    setIsDarkTheme(isDark);
  }, []);

  return (
    <div className={`min-h-screen flex flex-col transition-colors duration-500 ${
      isDarkTheme 
        ? 'bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900' 
        : 'bg-gradient-to-br from-slate-50 via-slate-100 to-slate-50'
    }`}>
      {/* Header */}
      <Header isConnected={isConnected} lastUpdate={lastUpdate} onThemeToggle={handleThemeToggle} />

      {/* Main Content */}
      <main className="flex-grow w-full flex items-center justify-center">
        <div className="max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12">
          {/* Welcome Section - Distinct Header */}
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="mb-16 pb-8 border-b border-white/10"
          >
            <h2 className={`text-4xl md:text-5xl font-bold mb-4 ${
              isDarkTheme ? 'text-white' : 'text-slate-900'
            }`}>
              Chào mừng đến với <span className="bg-gradient-to-r from-orange-400 to-pink-400 bg-clip-text text-transparent">PetZone</span>
            </h2>
            <p className={`text-lg max-w-3xl leading-relaxed ${
              isDarkTheme ? 'text-white/70' : 'text-slate-700'
            }`}>
              Giám sát chuồng nuôi thú cưng của bạn một cách thông minh, tự động hóa các công việc hàng ngày, và luôn kết nối với thú yêu của mình.
            </p>
          </motion.div>

          {/* Cards Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-16">
            {/* Temperature & Humidity - Takes 2 columns on lg */}
            <motion.div
              className="md:col-span-2 lg:col-span-2"
            >
              <div className="h-full rounded-2xl border border-white/15 shadow-lg hover:shadow-xl hover:border-white/25 transition-all duration-300 backdrop-blur-sm">
                <TemperatureCard temperature={temperature} humidity={humidity} loading={loadingTemp} />
              </div>
            </motion.div>

            {/* Pet Status */}
            <motion.div>
              <div className="h-full rounded-2xl border border-white/15 shadow-lg hover:shadow-xl hover:border-white/25 transition-all duration-300 backdrop-blur-sm">
                <PetStatusCard isPresent={isPresent} activityState={activityState} loading={loadingPet} />
              </div>
            </motion.div>

            {/* AI Detection */}
            <motion.div>
              <div className="h-full rounded-2xl border border-white/15 shadow-lg hover:shadow-xl hover:border-white/25 transition-all duration-300 backdrop-blur-sm">
                <AIStatusCard hasPet={hasPet} confidence={confidence} loading={loadingAI} />
              </div>
            </motion.div>
          </div>

          {/* Feed Button Section */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.4 }}
            className="mb-16"
          >
            <div className={`${
              isDarkTheme
                ? 'bg-gradient-to-r from-white/8 to-white/3 border border-white/15'
                : 'bg-gradient-to-r from-slate-200/30 to-slate-100/20 border border-slate-300/30'
            } rounded-2xl p-8 backdrop-blur-md shadow-lg hover:shadow-xl transition-all duration-300`}>
              <div className="mb-6">
                <h3 className={`text-2xl font-bold mb-3 ${
                  isDarkTheme ? 'text-white' : 'text-slate-900'
                }`}>Điều Khiển Cho Ăn</h3>
                <p className={isDarkTheme ? 'text-white/70' : 'text-slate-700'}>Nhấn nút để gửi lệnh cho ăn tới ESP32. Servo sẽ quay 90 độ để xả thức ăn.</p>
              </div>
              <FeedButton onClick={handleFeed} loading={loadingFeed} />
            </div>
          </motion.div>

          {/* Stats Section */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-16"
          >
            <StatBox icon="🌡️" label="Nhiệt độ" value={`${temperature.toFixed(1)}°C`} isDark={isDarkTheme} />
            <StatBox icon="💧" label="Độ ẩm" value={`${humidity.toFixed(1)}%`} isDark={isDarkTheme} />
            <StatBox icon="⚡" label="Năng lượng tĩnh" value={`${presenceEnergy.toFixed(0)}`} isDark={isDarkTheme} />
            <StatBox icon="💫" label="Năng lượng động" value={`${movementEnergy.toFixed(0)}`} isDark={isDarkTheme} />
          </motion.div>

          {/* Information Section */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-16"
          >
            <InfoBox
              icon="🔧"
              title="Công Nghệ Sử Dụng"
              items={['ESP32 IoT Board', 'DHT11 Sensor', 'HLK-LD2410C Radar', 'Servo & Relay']}
              isDark={isDarkTheme}
            />
            <InfoBox
              icon="🎯"
              title="Tính Năng Chính"
              items={['Giám sát Real-time', 'Tự động hóa', 'Điều khiển từ xa', 'Phân tích AI']}
              isDark={isDarkTheme}
            />
            <InfoBox
              icon="⚙️"
              title="Backend & Database"
              items={['.NET Core API', 'PostgreSQL', 'Entity Framework Core', 'RESTful Services']}
              isDark={isDarkTheme}
            />
            <InfoBox
              icon="🎨"
              title="Frontend Stack"
              items={['React + Vite', 'Tailwind CSS', 'Framer Motion', 'Axios Client']}
              isDark={isDarkTheme}
            />
          </motion.div>
        </div>
      </main>

      {/* Footer */}
      <Footer />
    </div>
  );
}

// Stat Box Component
const StatBox = ({ icon, label, value, isDark }) => (
  <motion.div
    whileHover={{ y: -5 }}
    className={`p-8 rounded-xl text-center transition-all duration-300 ${
      isDark
        ? 'bg-gradient-to-br from-white/10 to-white/5 border border-white/15 shadow-lg hover:shadow-xl hover:border-white/25'
        : 'bg-gradient-to-br from-slate-200/40 to-slate-100/30 border border-slate-300/40 shadow-md hover:shadow-lg hover:border-slate-400/50'
    }`}
  >
    <div className="text-4xl mb-3">{icon}</div>
    <p className={`text-sm mb-3 font-medium ${isDark ? 'text-white/70' : 'text-slate-700'}`}>{label}</p>
    <p className={`text-3xl font-bold ${isDark ? 'text-white' : 'text-slate-900'}`}>{value}</p>
  </motion.div>
);

// Info Box Component
const InfoBox = ({ icon, title, items, isDark }) => (
  <motion.div
    whileHover={{ borderColor: isDark ? 'rgba(14, 165, 233, 0.6)' : 'rgba(71, 85, 105, 0.6)' }}
    className={`p-8 rounded-xl transition-all duration-300 ${
      isDark
        ? 'bg-gradient-to-br from-white/8 to-white/3 border border-white/15 shadow-lg hover:shadow-xl backdrop-blur-md'
        : 'bg-gradient-to-br from-slate-200/40 to-slate-100/30 border border-slate-300/40 shadow-md hover:shadow-lg'
    }`}
  >
    <h4 className={`text-xl font-bold mb-5 flex items-center gap-3 ${isDark ? 'text-white' : 'text-slate-900'}`}>
      <span className="text-2xl">{icon}</span>
      {title}
    </h4>
    <ul className="space-y-3">
      {items.map((item, idx) => (
        <motion.li
          key={idx}
          initial={{ opacity: 0, x: -10 }}
          whileInView={{ opacity: 1, x: 0 }}
          transition={{ delay: idx * 0.1 }}
          className={`flex items-center gap-3 transition-colors ${
            isDark ? 'text-white/80 hover:text-white' : 'text-slate-700 hover:text-slate-900'
          }`}
        >
          <span className={`w-2.5 h-2.5 rounded-full flex-shrink-0 ${
            isDark ? 'bg-gradient-to-r from-orange-400 to-pink-400' : 'bg-gradient-to-r from-orange-500 to-pink-500'
          }`} />
          {item}
        </motion.li>
      ))}
    </ul>
  </motion.div>
);

export default App;
