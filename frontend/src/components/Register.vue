<template>
  <div class="register-container">
    <el-card class="register-card">
      <template #header>
        <div class="card-header">
          <span>用户注册</span>
        </div>
      </template>
      <el-form :model="registerForm" :rules="rules" ref="registerFormRef" label-width="100px">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="registerForm.username" placeholder="请输入用户名"></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input type="password" v-model="registerForm.password" placeholder="请输入密码" show-password></el-input>
        </el-form-item>
        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input type="password" v-model="registerForm.confirmPassword" placeholder="请再次输入密码" show-password></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleRegister" style="width: 100%;">注册</el-button>
        </el-form-item>
        <el-form-item>
          <el-button link type="primary" @click="goToLogin">已有账号？去登录</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue';
import { useRouter } from 'vue-router';
import { ElMessage } from 'element-plus';
import { registerUser } from '../api'; // 导入注册 API

const router = useRouter();
const registerFormRef = ref(null); // 表单引用

// 注册表单数据
const registerForm = reactive({
  username: '',
  password: '',
  confirmPassword: '',
});

// 自定义验证规则：确认密码
const validatePass = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请再次输入密码'));
  } else if (value !== registerForm.password) {
    callback(new Error('两次输入的密码不一致!'));
  } else {
    callback();
  }
};

// 表单验证规则
const rules = reactive({
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 15, message: '长度在 3 到 15 个字符', trigger: 'blur' },
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '长度在 6 到 20 个字符', trigger: 'blur' },
  ],
  confirmPassword: [
    { required: true, validator: validatePass, trigger: 'blur' },
  ],
});

// 处理注册按钮点击事件
const handleRegister = () => {
  registerFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        const response = await registerUser(registerForm.username, registerForm.password);
        if (response.data.code === 200) {
          // 注册成功提示已由 api/index.js 拦截器处理
          router.push('/'); // 注册成功后跳转到登录页
        } else {
          // 错误提示已由 api/index.js 拦截器处理
        }
      } catch (error) {
        // 错误捕获已由 api/index.js 拦截器处理
      }
    } else {
      ElMessage.warning('请填写完整的注册信息！');
      return false;
    }
  });
};

// 跳转到登录页面
const goToLogin = () => {
  router.push('/');
};
</script>

<style scoped>
/* 注册页面容器样式 */
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f0f2f5;
}

/* 注册卡片样式 */
.register-card {
  width: 450px;
  max-width: 90%;
  padding: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
}

/* 卡片头部样式 */
.card-header {
  font-size: 20px;
  font-weight: bold;
  text-align: center;
  margin-bottom: 20px;
}
</style>