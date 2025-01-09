<template>
  <el-container class="home-overview">
    <!-- 上部分：卡片区域 -->
    <el-header class="overview-header">
      <el-row :gutter="20">
        <!-- 最新通知 -->
        <el-col :xs="24" :sm="12" :md="8" :lg="8" :xl="8">
          <el-card class="overview-card notice-card">
            <template #header>
              <div class="card-header">
                <i class="el-icon-bell header-icon"></i>
                <span>最新通知</span>
                <el-button class="more-btn" type="text">更多</el-button>
              </div>
            </template>
            <div v-for="notice in notices.slice(0, 3)" :key="notice.id" class="notice-item">
              <div class="notice-dot"></div>
              <span class="notice-title">{{ notice.title }}</span>
              <span class="notice-time">{{ notice.time }}</span>
            </div>
          </el-card>
        </el-col>

        <!-- 任务概览 -->
        <el-col :xs="24" :sm="12" :md="8" :lg="8" :xl="8">
          <el-card class="overview-card task-card">
            <template #header>
              <div class="card-header">
                <i class="el-icon-data-line header-icon"></i>
                <span>任务概览</span>
              </div>
            </template>
            <div class="task-stats">
              <el-loading v-if="loading" />
              <template v-else>
                <div class="stat-item urgent">
                  <div class="stat-value">{{ urgentTasks }}</div>
                  <div class="stat-label">已完成任务</div>
                </div>
                <div class="stat-item applied">
                  <div class="stat-value">{{ appliedTasks }}</div>
                  <div class="stat-label">申请中任务</div>
                </div>
                <div class="stat-item extracting">
                  <div class="stat-value">{{ extractingTasks }}</div>
                  <div class="stat-label">提取中任务</div>
                </div>
              </template>
            </div>
          </el-card>
        </el-col>

        <!-- 项目进度 -->
        <el-col :xs="24" :sm="12" :md="8" :lg="8" :xl="8">
          <el-card class="overview-card project-card">
            <template #header>
              <div class="card-header">
                <i class="el-icon-office-building header-icon"></i>
                <span>项目进度</span>
                <el-button class="more-btn" type="text"
                           @click="skipTotask"
                >查看全部</el-button>
              </div>
            </template>
            <div class="project-list">
              <el-loading v-if="loading1" />
              <div v-for="project in projects" :key="project.id" class="project-item">
                <div class="project-info">
                  <span class="project-name">{{ project.name }}</span>
                  <span class="project-address">{{ project.address }}</span>
                </div>
                <el-tag :type="getProjectStatusType(project.status)" size="small">
                  {{ project.nodeName }}
                </el-tag>
              </div>
            </div>
          </el-card>
        </el-col>

        <!-- 快捷入口 -->
<!--        <el-col :xs="24" :sm="12" :md="8" :lg="6" :xl="6">-->
<!--          <el-card class="overview-card shortcut-card">-->
<!--            <template #header>-->
<!--              <div class="card-header">-->
<!--                <i class="el-icon-menu header-icon"></i>-->
<!--                <span>快捷入口</span>-->
<!--              </div>-->
<!--            </template>-->
<!--            <div class="shortcut-buttons">-->
<!--              <el-button type="primary" @click="uploadFile">-->
<!--                <i class="el-icon-upload2"></i> 上传文件-->
<!--              </el-button>-->

<!--            </div>-->
<!--          </el-card>-->
<!--        </el-col>-->
      </el-row>
    </el-header>

    <el-main class="overview-main">
      <MainContent />
    </el-main>
  </el-container>
</template>

<style scoped>
.home-overview {
  background-color: #f5f7fa;
  min-height: 100vh;
}

.overview-header {
  padding: 24px;
  background: transparent;
  height: auto;
}

.overview-card {
  height: 280px;
  margin-bottom: 20px;
  border-radius: 8px;
  transition: all 0.3s;
  border: none;
}

.overview-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  align-items: center;
  padding: 16px;
  background: linear-gradient(to right, #f8f9fb, #ffffff);
  border-bottom: 1px solid #ebeef5;
}

.header-icon {
  font-size: 20px;
  margin-right: 8px;
  color: #409eff;
}

.more-btn {
  margin-left: auto;
  padding: 0;
  font-size: 13px;
  color: #909399;
}

/* 通知卡片样式 */
.notice-item {
  display: flex;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid #ebeef5;
}

.notice-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background-color: #409eff;
  margin-right: 10px;
}

.notice-title {
  flex: 1;
  font-size: 14px;
  color: #303133;
}

.notice-time {
  font-size: 12px;
  color: #909399;
}

/* 任务统计样式 */
.task-stats {
  display: flex;
  justify-content: space-around;
  padding: 20px 0;
}

.stat-item {
  text-align: center;
  padding: 15px;
  border-radius: 8px;
  background: #f8f9fb;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 8px;
}

.stat-label {
  font-size: 13px;
  color: #606266;
}

.urgent .stat-value { color: #f56c6c; }
.applied .stat-value { color: #409eff; }
.extracting .stat-value { color: #67c23a; }

/* 项目列表样式 */
.project-list {
  padding: 0 16px;
  max-height: 180px;
  overflow-y: auto;
  margin: 10px 0;
}

.project-list::-webkit-scrollbar {
  width: 4px;
}

.project-list::-webkit-scrollbar-track {
  background: #f4f4f5;
  border-radius: 2px;
}

.project-list::-webkit-scrollbar-thumb {
  background: #dcdfe6;
  border-radius: 2px;
}

.project-list::-webkit-scrollbar-thumb:hover {
  background: #c0c4cc;
}

.project-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 0;
  border-bottom: 1px solid #ebeef5;
}

.project-item:last-child {
  border-bottom: none;
}

.project-info {
  display: flex;
  flex-direction: column;
  flex: 1;
  margin-right: 12px;
  min-width: 0; /* 防止文本溢出 */
}

.project-name {
  font-size: 14px;
  font-weight: 500;
  color: #303133;
  margin-bottom: 4px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.project-address {
  font-size: 12px;
  color: #909399;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* 快捷按钮样式 */
.shortcut-buttons {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 16px;
}

.shortcut-buttons .el-button {
  width: 100%;
  justify-content: center;
  padding: 12px 20px;
}

.overview-main {
  padding: 0 24px 24px;
  background-color: transparent;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .overview-header {
    padding: 16px;
  }
  
  .overview-card {
    height: auto;
    min-height: 200px;
  }
}

/* 修改项目卡片样式 */
.project-card .el-card__body {
  padding: 0;  /* 移除默认内边距 */
  height: calc(100% - 55px); /* 减去header高度 */
  display: flex;
  flex-direction: column;
}
</style>

<script setup>
import { ref, onMounted } from 'vue';
import MainContent from './MainContent.vue';
import router from "@/router";
import {useRouter} from "vue-router";
import { ElMessage } from 'element-plus';
import {getnewinformation, getnewinformationview, taskoverview, taskoverviewinfo} from "../../api/api";

const notices = ref([
  { id: 1, title: '系统更新通知：新功能上线', time: '10分钟前' },
  { id: 2, title: '重要：年度工作计划发布', time: '2小时前' },
  { id: 3, title: '关于系统维护的通知', time: '1天前' }
]);

const urgentTasks = ref(0);
const appliedTasks = ref(0);
const extractingTasks = ref(0);

const loading = ref(false);
const loading1 = ref(false);

const projects = ref([
  // { id: 1, name: '企业数据中心项目', address: '北京市朝阳区', nodeName: '提取中', status: 'processing' }
]);

const timeAgo = (time) => {
  const now = dayjs();
  const diffSeconds = now.diff(dayjs(time), 'second');
  const diffMinutes = now.diff(dayjs(time), 'minute');
  const diffHours = now.diff(dayjs(time), 'hour');
  const diffDays = now.diff(dayjs(time), 'day');

  if (diffSeconds < 60) {
    return `${diffSeconds}秒前`;
  } else if (diffMinutes < 60) {
    return `${diffMinutes}分钟前`;
  } else if (diffHours < 24) {
    return `${diffHours}小时前`;
  } else {
    return `${diffDays}天前`;
  }
};

const getProjectStatusType = (status) => {
  const statusMap = {
    processing: 'primary',
    success: 'success',
    warning: 'warning',
    error: 'danger'
  };
  return statusMap[status] || 'info';
};

const createTask = () => {
  console.log('新建任务');
};

const uploadFile = () => {
  console.log('上传文件');
};

const skipTotask = () => {
  router.push("/requestmanagement")
}

// 获取任务统计数据
const getTaskInfo = async () => {
  loading.value = true;
  let para = {
    "usernumber" :localStorage.getItem("usernumber")
  };
  try {
    const response = await taskoverview(para);
    if (response.data.code === "200") {
      urgentTasks.value = response.data.data.urgentTasks;
      appliedTasks.value = response.data.data.appliedTasks;
      extractingTasks.value = response.data.data.extractingTasks;
    }
  } catch (error) {
    console.error('获取任务统计数据失败:', error);
    ElMessage.error('获取任务统计数据失败');
  } finally {
    loading.value = false;
  }
};

const getTaskStats = async () => {
  loading1.value = true;
  let para = {
    "usernumber" :localStorage.getItem("usernumber")
  };
  try {
    const response = await taskoverviewinfo(para);
    if (response.data.code === "200") {
      projects.value = response.data.data;
    }
  } catch (error) {
    console.error('获取任务统计数据失败:', error);
    ElMessage.error('获取任务统计数据失败');
  } finally {
    loading1.value = false;
  }
};

const getNotices = async () => {
  try {
    const response = await getnewinformationview();
    if (response.data.code === "200") {
      notices.value = response.data.data;
    }
  } catch (error) {
    console.error('获取通知数据失败:', error);
    ElMessage.error('获取通知数据失败');
  }
};

// 在组件挂载时获取数据
onMounted(() => {
  getTaskStats();
  getTaskInfo();
  getNotices();
});

</script>