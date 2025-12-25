import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

// Tạo axios instance với timeout
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 5000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Sensor API
export const sensorAPI = {
  getLatest: () => apiClient.get('/sensors/latest'),
  getHistory: (limit = 20) => apiClient.get(`/sensors/history?limit=${limit}`),
};

// Control API
export const controlAPI = {
  feed: () => apiClient.post('/control/feed', {}),
  getPendingCommands: () => apiClient.get('/control/commands/pending'),
  executeCommand: (id) => apiClient.post(`/control/commands/${id}/executed`, {}),
};

// AI Status API
export const aiAPI = {
  getStatus: () => apiClient.get('/ai/status'),
  getPetStatus: () => apiClient.get('/ai/pet-status'),
};

export default apiClient;
