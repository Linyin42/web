<template>
  <div class="home-container">
    <el-card class="welcome-card">
      <div class="welcome-message">
        <h1>欢迎，{{ username }}!</h1>
        <p>这是您的主页。</p>
        <p>您已成功登录系统。</p>
        <el-button type="info" @click="handleLogout" style="margin-top: 20px;">退出登录</el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { ElMessage } from 'element-plus';

const username = ref('');
const router = useRouter();

onMounted(() => {
  const storedUsername = localStorage.getItem('username');
  if (storedUsername) {
    username.value = storedUsername;
  }
});

const handleLogout = () => {
  localStorage.removeItem('username');
  localStorage.removeItem('isLoggedIn');
  ElMessage.success('已退出登录！');
  router.push('/'); // 返回登录页
};
</script>

<style scoped>
/* 此处的样式是为了让欢迎卡片在整个页面上居中显示 */
.home-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh; /* 占据整个视口高度 */
  background-color: #f0f2f5;
  padding: 20px;
  box-sizing: border-box; /* 确保 padding 不会超出 min-height */
}

.welcome-card {
  width: 80%;
  max-width: 600px;
  text-align: center;
  padding: 40px 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  border-radius: 10px;
}

.welcome-message h1 {
  font-size: 3em;
  color: #333;
  margin-bottom: 20px;
}

.welcome-message p {
  font-size: 1.2em;
  color: #666;
}
</style>
