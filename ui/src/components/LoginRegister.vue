<template>
  <div class="login-container">
    <div class="login-box">
      <div class="login-header">

        <h2>数据申请系统</h2>
        <p class="welcome-text">欢迎登录</p>
      </div>

      <el-form class="login-form" @submit.prevent="handleLogin">
        <el-form-item>
          <el-input
            v-model="data.usernumber"
            placeholder="请输入工号"
            :prefix-icon="User"
            size="large"
          />
        </el-form-item>

        <el-form-item>
          <el-input
            v-model="data.password"
            type="password"
            placeholder="请输入密码"
            :prefix-icon="Lock"
            show-password
            size="large"
          />
        </el-form-item>

        <el-form-item>
          <el-button 
            type="primary" 
            native-type="submit"
            size="large" 
            class="login-button"
          >
            登录
          </el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { login } from "@/api/api";
import { ElMessage } from 'element-plus';
import { User, Lock } from '@element-plus/icons-vue'

export default {
  name: 'LoginRegister',
  setup() {
    const router = useRouter();
    const data = ref({
      "usernumber": "",
      "password": ""
    });

    const handleLogin = () => {
      if (data.value.usernumber && data.value.password) {
        login(data.value).then(res=>{
          if(res.data.code === "200"){
            ElMessage({
              message: "欢迎 " + res.data.data.username + '，登陆',
              type: 'success'
            });
            localStorage.setItem("token", res.data.data.token);
            localStorage.setItem("usernumber", data.value.usernumber);
            localStorage.setItem("username", res.data.data.username);
            localStorage.setItem("userRole", res.data.data.role);
            router.push('/Home');
          }else{
            ElMessage({
              message: res.data.msg,
              type: 'error'
            });
          }
        });
      } else {
        ElMessage.warning('请输入工号和密码');
      }
    };

    return {
      data,
      handleLogin,
      User,
      Lock
    };
  }
};
</script>

<style scoped>
.login-container {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #f5f7fa;
}

.login-box {
  width: 420px;
  padding: 40px;
  background: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
}

.login-header {
  text-align: center;
  margin-bottom: 40px;
}

.logo {
  width: 84px;
  height: 84px;
  margin-bottom: 16px;
}

.login-header h2 {
  color: #303133;
  font-size: 24px;
  font-weight: 600;
  margin: 0;
  padding: 10px 0;
}

.welcome-text {
  color: #909399;
  font-size: 16px;
  margin: 8px 0;
}

.login-form {
  margin-top: 30px;
}

.login-form :deep(.el-input__wrapper) {
  padding: 1px 15px;
  box-shadow: 0 0 0 1px #dcdfe6 inset;
}

.login-form :deep(.el-input__wrapper:hover) {
  box-shadow: 0 0 0 1px #409eff inset;
}

.login-button {
  width: 100%;
  margin-top: 10px;
  height: 40px;
  font-size: 16px;
  background: #409eff;
  border: none;
}

.login-button:hover {
  background: #66b1ff;
}

:deep(.el-input__wrapper.is-focus) {
  box-shadow: 0 0 0 1px #409eff inset !important;
}
</style>

