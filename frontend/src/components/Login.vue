<template>
  <div class="login-container">
    <el-card class="login-card">
      <template #header>
        <div class="card-header">
          <span>用户登录</span>
        </div>
      </template>
      <el-form :model="loginForm" :rules="rules" ref="loginFormRef" class="login-form">
        <el-form-item prop="username">
          <el-input v-model="loginForm.username" placeholder="请输入用户名" prefix-icon="User"></el-input>
        </el-form-item>
        <el-form-item prop="password">
          <el-input type="password" v-model="loginForm.password" placeholder="请输入密码" show-password prefix-icon="Lock"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleLogin" class="login-button">登录</el-button>
        </el-form-item>
        <div class="register-link">
          <el-link type="primary" @click="goToRegister">注册新账号</el-link>
        </div>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue';
import { useRouter } from 'vue-router';
import { ElMessage } from 'element-plus';
import axios from 'axios';
import { User, Lock } from '@element-plus/icons-vue'; // 导入图标

const router = useRouter(); // 获取路由实例
const loginFormRef = ref(null); // 表单引用

// 登录表单数据
const loginForm = reactive({
  username: '',
  password: ''
});

// 表单验证规则
const rules = reactive({
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '长度在 6 到 20 个字符', trigger: 'blur' }
  ]
});

// 处理登录
const handleLogin = () => {
  loginFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        const response = await axios.post('/api/login', {
          username: loginForm.username,
          password: loginForm.password
        });

        if (response.data.code === 200) {
          ElMessage.success('登录成功！');
          // 存储登录状态和用户名
          localStorage.setItem('isLoggedIn', 'true');
          localStorage.setItem('username', response.data.username);
          // 跳转到主页面
          router.push('/main/home');
        } else {
          ElMessage.error(response.data.message || '登录失败，请检查用户名或密码');
        }
      } catch (error) {
        console.error('登录请求失败:', error);
        ElMessage.error('服务器错误或网络问题，请稍后再试。');
      }
    } else {
      ElMessage.warning('请检查输入，确保用户名和密码符合要求。');
      return false;
    }
  });
};

// 跳转到注册页面
const goToRegister = () => {
  router.push('/register');
};
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f0f2f5;
}

.login-card {
  width: 400px;
  max-width: 90%;
  text-align: center;
}

.card-header {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 20px;
}

.login-form {
  padding: 0 20px 20px;
}

.login-button {
  width: 100%;
}

.register-link {
  margin-top: 15px;
}
</style>