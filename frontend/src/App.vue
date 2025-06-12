<template>
  <div class="common-layout" v-if="$route.path !== '/' && $route.path !== '/register'">
    <el-container>
      <el-header class="header">
        <div class="header-left">
          <img src="/vite.svg" alt="Logo" class="logo" /> <span class="system-title">网站登录系统</span> </div>
        <div class="user-info">
          <span>你好, {{ username }}</span> <el-dropdown trigger="click" @command="handleCommand">
            <span class="el-dropdown-link">
              <el-icon><Setting /></el-icon>
              <el-icon class="el-icon--right"><arrow-down /></el-icon>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="personal">个人信息</el-dropdown-item>
                <el-dropdown-item command="logout">退出</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>
      <el-container class="main-container">
        <el-aside :width="isCollapse ? '64px' : '200px'" class="aside">
          <el-menu
            :default-active="activeMenu"
            class="el-menu-vertical-demo"
            :collapse="isCollapse"
            @select="handleMenuSelect"
            background-color="#545c64"
            text-color="#fff"
            active-text-color="#ffd04b"
            router
          >
            <el-menu-item index="/main/home">
              <el-icon><HomeFilled /></el-icon>
              <span>主页</span>
            </el-menu-item>
            <el-menu-item index="/main/crawler-example">
              <el-icon><DataLine /></el-icon>
              <span>爬虫示例</span>
            </el-menu-item>
            <el-sub-menu index="2">
              <template #title>
                <el-icon><Setting /></el-icon>
                <span>系统设置</span>
              </template>
              <el-menu-item index="/main/personal-information">
                <el-icon><User /></el-icon>
                <span>修改密码</span>
              </el-menu-item>
            </el-sub-menu>
            <el-menu-item index="logout">
              <el-icon><SwitchButton /></el-icon>
              <span>退出</span>
            </el-menu-item>
          </el-menu>
          <div class="collapse-button" @click="toggleCollapse">
            <el-icon v-if="isCollapse"><Expand /></el-icon>
            <el-icon v-else><Fold /></el-icon>
            <span v-if="!isCollapse">折叠</span>
          </div>
        </el-aside>
        <el-main class="main-content">
          <router-view />
        </el-main>
      </el-container>
    </el-container>
  </div>
  <router-view v-else></router-view>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { ElMessage } from 'element-plus';
// Import Element Plus icon components
import {
  HomeFilled,
  DataLine,
  Setting,
  User,
  SwitchButton,
  ArrowDown,
  Expand,
  Fold
} from '@element-plus/icons-vue';

const router = useRouter();
const route = useRoute(); // Get current route information
const username = ref('');
const isCollapse = ref(false); // Sidebar collapse state
const activeMenu = ref(''); // Currently active menu item

// On component mount, get username and set default active menu
onMounted(() => {
  username.value = localStorage.getItem('username') || '用户';
  // Set active menu based on current route
  activeMenu.value = route.path;
});

// Watch for route changes to update active menu item
watch(
  () => route.path,
  (newPath) => {
    activeMenu.value = newPath;
  }
);

// Handle dropdown menu commands
const handleCommand = (command) => {
  if (command === 'personal') {
    router.push('/main/personal-information');
  } else if (command === 'logout') {
    logout();
  }
};

// Logout function
const logout = () => {
  localStorage.removeItem('username');
  localStorage.removeItem('isLoggedIn');
  ElMessage.info('您已退出登录');
  router.push('/');
};

// Menu selection handler
const handleMenuSelect = (index) => {
  if (index === 'logout') {
    logout();
  } else {
    // router="true" attribute already handles navigation
  }
};

// Toggle sidebar collapse state
const toggleCollapse = () => {
  isCollapse.value = !isCollapse.value;
};
</script>

<style scoped>
.common-layout {
  min-height: 100vh;
  display: flex; /* Ensure container is flex layout */
  flex-direction: column; /* Child items arrange vertically */
}

/* Header styles */
.header {
  background-color: #409eff;
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* Header shadow */
  z-index: 100; /* Ensure header is on top */
}

.header-left {
  display: flex;
  align-items: center;
}

.logo {
  height: 30px;
  margin-right: 10px;
}

.system-title {
  font-size: 20px;
  font-weight: bold;
  margin-right: 30px;
}

.user-info {
  display: flex;
  align-items: center;
}

.user-info span {
  margin-right: 15px;
  white-space: nowrap;
}

.el-dropdown-link {
  cursor: pointer;
  color: #fff;
  display: flex;
  align-items: center;
  margin-left: 10px;
}
.el-dropdown-link:hover {
  color: #ffd04b;
}

/* Main container, including sidebar and main content */
.main-container {
  flex-grow: 1; /* Occupy remaining vertical space */
}

/* Sidebar styles */
.aside {
  background-color: #545c64;
  height: 100%; /* Ensure sidebar fills height */
  box-shadow: 2px 0 6px rgba(0, 0, 0, 0.1);
  transition: width 0.3s; /* Animation for collapse/expand */
  display: flex;
  flex-direction: column;
}

.el-menu-vertical-demo:not(.el-menu--collapse) {
  width: 200px;
  min-height: 400px;
}

.el-menu {
  border-right: none; /* Remove default Element Plus menu border */
  flex-grow: 1; /* Menu occupies all space except for collapse button */
}

.collapse-button {
  background-color: #545c64;
  color: #fff;
  text-align: center;
  padding: 10px 0;
  cursor: pointer;
  border-top: 1px solid #666; /* Top border */
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.3s;
}

.collapse-button:hover {
  background-color: #434a50;
}

.collapse-button .el-icon {
  margin-right: 5px; /* Spacing between icon and text */
}


/* Main content area styles */
.main-content {
  background-color: #f0f2f5;
  padding: 20px;
  overflow-y: auto; /* Enable vertical scrolling for overflowing content */
}
</style>