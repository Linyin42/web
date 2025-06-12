import axios from 'axios';
import { ElMessage } from 'element-plus';

const apiClient = axios.create({
  baseURL: '/api', // 前端请求会通过 Vite 代理到后端
  timeout: 15000, // 增加超时时间，因为爬虫可能需要更多时间
  headers: {
    'Content-Type': 'application/json'
  }
});

apiClient.interceptors.request.use(
  config => {
    return config;
  },
  error => {
    return Promise.reject(error);
  }
);

apiClient.interceptors.response.use(
  response => {
    if (response.data.code === 200) {
      ElMessage.success(response.data.message || '操作成功！');
    } else {
      ElMessage.error(response.data.message || '操作失败！');
    }
    return response;
  },
  error => {
    if (error.response) {
      ElMessage.error(error.response.data.message || '服务器错误！');
    } else if (error.request) {
      ElMessage.error('未能收到服务器响应。请检查您的网络连接或后端服务是否已启动。');
    } else {
      ElMessage.error('请求错误: ' + error.message);
    }
    return Promise.reject(error);
  }
);

export const loginUser = (username, password) => {
  return apiClient.post('/login', { username, password });
};

export const registerUser = (username, password) => {
  return apiClient.post('/register', { username, password });
};

// 新增爬虫 API 调用
export const getDoubanTop250 = () => {
  return apiClient.get('/crawl_douban_top250');
};
