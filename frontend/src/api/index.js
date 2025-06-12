import axios from 'axios';
import { ElMessage } from 'element-plus';

const apiClient = axios.create({
  baseURL: '/api', // 前端请求会通过 Vite 代理到后端
  timeout: 10000, // 增加超时时间，以适应爬虫可能需要的时间
  headers: {
    'Content-Type': 'application/json'
  }
});

// 请求拦截器：可以在发送请求前做一些处理，例如添加 token
apiClient.interceptors.request.use(
  config => {
    // 可以在这里添加认证 token
    // const token = localStorage.getItem('token');
    // if (token) {
    //   config.headers.Authorization = `Bearer ${token}`;
    // }
    return config;
  },
  error => {
    return Promise.reject(error);
  }
);

// 响应拦截器：统一处理后端响应和错误
apiClient.interceptors.response.use(
  response => {
    // 爬虫接口的响应可能比较大，这里只对非爬虫接口的成功信息进行全局提示
    // 或者可以根据 response.config.url 来区分
    if (response.config.url !== '/crawl') { // 爬虫接口不自动显示成功消息，由调用方处理
      if (response.data.code === 200) {
        ElMessage.success(response.data.message || '操作成功！');
      } else {
        // 后端返回的非 200 状态码，通常表示业务逻辑错误
        ElMessage.error(response.data.message || '操作失败！');
      }
    }
    return response;
  },
  error => {
    // 处理网络错误、服务器错误等
    if (error.response) {
      // 服务器返回了响应，但状态码不在 2xx 范围内
      ElMessage.error(error.response.data.message || '服务器错误！');
    } else if (error.request) {
      // 请求已发出但未收到响应
      ElMessage.error('未能收到服务器响应。请检查您的网络连接或后端服务是否已启动。');
    } else {
      // 在设置请求时发生了错误
      ElMessage.error('请求错误: ' + error.message);
    }
    return Promise.reject(error);
  }
);

// 封装登录 API 调用
export const loginUser = (username, password) => {
  return apiClient.post('/login', { username, password });
};

// 封装注册 API 调用
export const registerUser = (username, password) => {
  return apiClient.post('/register', { username, password });
};

// 封装修改密码 API 调用
export const changePassword = (username, oldPassword, newPassword) => {
  return apiClient.post('/change_password', { username, oldPassword, newPassword });
};

// 新增：封装触发爬虫 API 调用
export const crawlMovies = () => {
  return apiClient.post('/crawl');
};

// 新增：封装获取电影数据 API 调用
export const getMovies = () => {
  return apiClient.get('/movies');
};