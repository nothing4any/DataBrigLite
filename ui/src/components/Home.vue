<template>
  <div class="home" :key="componentKey">
    <header class="header">
      <div class="header-left">
        <div v-if="showLogo" class="logo"></div>
        <div v-else class="large-text">数据平台</div>
      </div>
      <div class="header-center">
        <el-input placeholder="请输入搜索内容" v-model="searchQuery" suffix-icon="el-icon-search"
                  class="search-input"></el-input>
      </div>
      <div class="header-right">
        <el-button type="text" @click="goToWorkspace" class="workspace-button">工作区</el-button>
        <el-dropdown @command="handleCommand">
                    <span class="el-dropdown-link">
                        <el-icon><User/></el-icon>{{ username }}<i class="el-icon-arrow-down el-icon--right"></i>
                    </span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="logout">注销</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </header>
    <main class="main">
      <div class="grid-container">
        <div class="grid-item" v-for="item in filteredItems" :key="item.id" @click="openInNewTab(item.url)"
             :style="{ backgroundImage: `url(${item.icon})` }">
          <span class="name">{{ item.name }}</span>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import {ref, computed, reactive, onMounted, watch, nextTick} from 'vue';
import {useRouter} from 'vue-router';
import {User} from '@element-plus/icons-vue';
import {unlogin} from "../api/api";
import {ElMessage} from "element-plus";
import {watchEffect} from "@vue/runtime-core";

export default {
  name: 'MyHome',
  components: {
    User,
  },
  setup() {
    const router = useRouter();
    const items = ref([
      {id: 1, name: '数据提取', icon: require('../assets/数据提取.png'), url: '/datarequest'},
    ]);
    const username = ref('用户名');
    const componentKey = ref(0);
    router.beforeEach((to, from, next) => {
      username.value = localStorage.getItem('username');
      next();
    });


    const updateUsername = () => {
      const storedUsername = localStorage.getItem('username');
      if (storedUsername && storedUsername !== 'null') {
        username.value = storedUsername;
      } else {
        username.value = '用户名';
      }
    };

    const initializeComponent = () => {
      updateUsername();
    };

    onMounted(() => {
      initializeComponent();
    });

    watchEffect(() => {
      const currentUsername = localStorage.getItem('username');
      if (currentUsername) {
        username.value = currentUsername;
      }
    });

    const searchQuery = ref('');
    const showLogo = ref(false);

    const filteredItems = computed(() => {
      return items.value.filter(item =>
          item.name.toLowerCase().includes(searchQuery.value.toLowerCase())
      );
    });

    const handleCommand = (command) => {
      if (command === 'logout') {
        logout();
      }
    };

    const data = reactive({
      "token": localStorage.getItem('token'),
    });
    const logout = async () => {
      try {
        const res = await unlogin(data);
        if (res.data.code === "200") {
          localStorage.removeItem("token");
          localStorage.removeItem("usernumber");
          localStorage.removeItem("username");
          localStorage.removeItem("userRole");
          router.push('/login');
        } else {
          ElMessage({
            message: res.data.msg,
            type: 'error'
          });
        }
      } catch (e) {
        ElMessage({
          message: "后端服务异常",
          type: 'error'
        });
      }
    };

    const openInNewTab = (url) => {
      window.open(url, '_blank');
    };

    const goToWorkspace = () => {
      window.open('/workspace', '_blank');
    };

    router.beforeEach((to, from, next) => {
      if (to.path === '/') {
        componentKey.value += 1;
      }
      next();
    });

    return {
      items,
      searchQuery,
      filteredItems,
      handleCommand,
      openInNewTab,
      showLogo,
      goToWorkspace,
      data,
      username,
      componentKey
    };
  },
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

body, html {
  margin: 0;
  padding: 0;
  height: 100%;
  font-family: 'Roboto', sans-serif;
}

#app {
  margin-top: 0 !important; /* 覆盖全局样式 */
}

.home {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background-color: #F0F4F8;
  color: #333;
  padding: 0; /* 移除所有内边距 */
}

.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px;
  background-color: #5a8bbc;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  color: #FFFFFF;
}

.header-left {
  display: flex;
  align-items: center;
  padding: 0 10px;
}

.logo {
  width: 40px;
  height: 40px;
  background-image: url('https://img.alicdn.com/tfs/TB1XjwKQXXXXXXFXVXXXXXXXXXX-64-64.png'); /* 替换为你的logo图片地址 */
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  border-radius: 50%;
}

.large-text {
  font-size: 24px;
  color: white;
  background-color: transparent;
  width: auto;
  height: auto;
  padding: 0 10px;
}

.header-center {
  flex: 1;
  text-align: center;
}

.search-input {
  width: 300px;
  background-color: #FFFFFF;
  border: 1px solid #D1D1D1;
  border-radius: 5px;
}

.el-dropdown-link {
  cursor: pointer;
  color: #FFFFFF;
  font-size: 16px;
  display: flex;
  align-items: center;
  writing-mode: horizontal-tb; /* 确保文本水平显示 */
}

.el-dropdown-link:focus {
  outline: none;
}

.header-right {
  display: flex;
  align-items: center;
}

.workspace-button {
  font-size: 18px; /* 设置更大的字体 */
  color: white; /* 设置白色字体 */
  margin-right: 10px; /* 设置与用户名之间的间隔 */
}

.main {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  background-color: #F0F4F8;
}

.grid-container {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 10px;
}

.grid-item {
  background-color: #FFFFFF;
  border: 1px solid #E0E0E0;
  padding: 20px;
  text-align: center;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border-radius: 10px;
  aspect-ratio: 1 / 1;
  color: #333;
  border-radius: 8px;
  background-size: cover; /* 使背景图覆盖整个卡片 */
  background-position: center; /* 使背景图居中 */
  background-repeat: no-repeat; /* 防止背景图重复 */
}

.grid-item:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.icon {
  font-size: 24px;
  color: #007bff;
  margin-bottom: 8px;
}

.name {
  font-size: 25px;
  color: #333;
}

@media (max-width: 768px) {
  .grid-container {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 480px) {
  .grid-container {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
