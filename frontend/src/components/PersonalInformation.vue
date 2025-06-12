<template>
  <div class="personal-information-container">
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span>个人信息</span>
        </div>
      </template>
      <el-form :model="form" :rules="rules" ref="formRef" label-width="100px" class="personal-form">
        <el-form-item label="用户名">
          <el-input v-model="form.username" disabled></el-input>
        </el-form-item>
        <el-form-item label="旧密码" prop="oldPassword">
          <el-input type="password" v-model="form.oldPassword" show-password placeholder="请输入旧密码"></el-input>
        </el-form-item>
        <el-form-item label="新密码" prop="newPassword">
          <el-input type="password" v-model="form.newPassword" show-password placeholder="请输入新密码"></el-input>
        </el-form-item>
        <el-form-item label="确认新密码" prop="confirmNewPassword">
          <el-input type="password" v-model="form.confirmNewPassword" show-password placeholder="请再次输入新密码"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitForm">保存</el-button>
          <el-button @click="resetForm">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';
import { useRouter } from 'vue-router'; // Import useRouter for navigation
import { ElMessage } from 'element-plus';
import axios from 'axios'; // Import axios for HTTP requests

const router = useRouter(); // Get router instance

const formRef = ref(null); // Form reference for validation
const form = reactive({
  username: '',
  oldPassword: '',
  newPassword: '',
  confirmNewPassword: ''
});

// Password validation rules
const validatePass = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请输入新密码'));
  } else if (value.length < 6 || value.length > 20) {
    callback(new Error('长度在 6 到 20 个字符'));
  } else {
    // If confirmNewPassword is not empty, validate it after newPassword changes
    if (form.confirmNewPassword !== '') {
      formRef.value.validateField('confirmNewPassword');
    }
    callback();
  }
};

const validatePass2 = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请再次输入新密码'));
  } else if (value !== form.newPassword) {
    callback(new Error('两次输入密码不一致!'));
  } else {
    callback();
  }
};

const rules = reactive({
  oldPassword: [
    { required: true, message: '请输入旧密码', trigger: 'blur' },
  ],
  newPassword: [
    { required: true, validator: validatePass, trigger: 'blur' }
  ],
  confirmNewPassword: [
    { required: true, validator: validatePass2, trigger: 'blur' }
  ]
});

// On component mount, get username from localStorage
onMounted(() => {
  form.username = localStorage.getItem('username') || '';
});

// Submit form handler
const submitForm = () => {
  formRef.value.validate(async (valid) => {
    if (valid) {
      try {
        const response = await axios.post('/api/change_password', {
          username: form.username,
          old_password: form.oldPassword,
          new_password: form.newPassword
        });

        if (response.data.code === 200) {
          ElMessage.success('密码修改成功！请重新登录');
          // On successful password change, clear login state and redirect to login page
          localStorage.removeItem('username');
          localStorage.removeItem('isLoggedIn');
          router.push('/');
        } else {
          ElMessage.error(response.data.message || '密码修改失败！');
        }
      } catch (error) {
        console.error('Change password request failed:', error);
        ElMessage.error('服务器错误或网络问题，请稍后再试。');
      }
    } else {
      ElMessage.warning('请检查输入，确保所有项都符合要求。');
      return false;
    }
  });
};

// Reset form handler
const resetForm = () => {
  form.oldPassword = '';
  form.newPassword = '';
  form.confirmNewPassword = '';
  formRef.value.clearValidate(); // Clear form validation errors
};
</script>

<style scoped>
.personal-information-container {
  display: flex;
  justify-content: center;
  align-items: flex-start; /* Align card to the top with padding */
  padding-top: 50px; /* Add some top padding */
  min-height: calc(100vh - 60px); /* Subtract header height for proper vertical alignment */
}

.box-card {
  width: 500px;
  max-width: 90%; /* Responsive width for smaller screens */
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 18px;
  font-weight: bold;
}

.personal-form {
  padding: 20px;
}
</style>