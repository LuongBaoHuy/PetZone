// Mock data để test UI khi backend chưa sẵn
export const mockSensorData = {
  temperature: 28,
  humidity: 65,
  presenceEnergy: 45,
  movementEnergy: 120,
  timestamp: new Date().toISOString(),
};

export const mockPetStatus = {
  isPresent: true,
  activityState: 'awake', // awake, sleeping, absent
  lastSeen: new Date(Date.now() - 5000).toISOString(),
  hasPet: true,
};

export const mockControlStatus = {
  lastFeedTime: new Date(Date.now() - 3600000).toISOString(),
  fanActive: false,
  pendingCommands: [],
};

// Hàm tạo dữ liệu fake realtime
export const generateMockData = () => {
  return {
    temperature: 25 + Math.random() * 8, // 25-33°C
    humidity: 50 + Math.random() * 30, // 50-80%
    presenceEnergy: Math.random() * 255,
    movementEnergy: Math.random() * 255,
    timestamp: new Date().toISOString(),
  };
};

export const generateMockPetStatus = () => {
  const states = ['awake', 'sleeping', 'absent'];
  const randomState = states[Math.floor(Math.random() * states.length)];
  return {
    isPresent: randomState !== 'absent',
    activityState: randomState,
    lastSeen: new Date().toISOString(),
    hasPet: randomState !== 'absent',
  };
};
