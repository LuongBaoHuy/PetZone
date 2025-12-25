import axios from 'axios';

// Tạo instance Axios với cấu hình tập trung
const api = axios.create({
  baseURL: 'http://localhost:5019',
  timeout: 10000, // 10 giây
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request Interceptor - Xử lý trước khi gửi request
api.interceptors.request.use(
  (config) => {
    // Có thể thêm token vào header ở đây nếu cần
    // const token = localStorage.getItem('token');
    // if (token) {
    //   config.headers.Authorization = `Bearer ${token}`;
    // }
    
    console.log(`📤 [API REQUEST] ${config.method.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('❌ [API REQUEST ERROR]', error);
    return Promise.reject(error);
  }
);

// Response Interceptor - Xử lý lỗi toàn cục
api.interceptors.response.use(
  (response) => {
    console.log(`✅ [API RESPONSE] ${response.config.url}`, response.status);
    return response;
  },
  (error) => {
    // Xử lý lỗi toàn cục
    if (error.response) {
      // Server trả về lỗi (status code ngoài 2xx)
      const { status, data } = error.response;
      
      switch (status) {
        case 400:
          console.error('❌ [400] Bad Request:', data);
          break;
        case 401:
          console.error('❌ [401] Unauthorized - Vui lòng đăng nhập lại');
          // Có thể redirect đến trang login
          break;
        case 403:
          console.error('❌ [403] Forbidden - Không có quyền truy cập');
          break;
        case 404:
          console.error('❌ [404] Not Found:', error.config.url);
          break;
        case 500:
          console.error('❌ [500] Internal Server Error');
          break;
        default:
          console.error(`❌ [${status}] Server Error:`, data);
      }
    } else if (error.request) {
      // Request đã được gửi nhưng không nhận được response
      console.error('❌ [NETWORK ERROR] Không thể kết nối đến server');
      console.error('Chi tiết:', error.message);
    } else {
      // Lỗi khác trong quá trình setup request
      console.error('❌ [ERROR]', error.message);
    }
    
    return Promise.reject(error);
  }
);

export default api;
