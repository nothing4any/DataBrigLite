<template>
  <div class="file-management">
    <div class="toolbar">
      <div class="left">
        <el-button link type="primary" @click="backToHome">
          <el-icon><Back /></el-icon>
          返回首页
        </el-button>
      </div>
      <div class="right">
        <div class="search-group">
          <el-input
            v-model="searchText"
            placeholder="搜索文件名"
            class="search-input"
            :prefix-icon="Search"
            @keyup.enter="handleSearch"
          />
          <el-input
            v-model="searchApplicant"
            placeholder="搜索申请人"
            class="search-input"
            :prefix-icon="User"
            @keyup.enter="handleSearch"
          />
          <el-button type="primary" @click="handleSearch">
            <el-icon><Search /></el-icon>
            搜索
          </el-button>
        </div>
        <el-radio-group v-model="viewMode" size="small">
          <el-radio-button label="list">
            <el-icon><Menu /></el-icon>
            列表
          </el-radio-button>
          <el-radio-button label="grid">
            <el-icon><Grid /></el-icon>
            网格
          </el-radio-button>
        </el-radio-group>
      </div>
    </div>

    <!-- 列表视图 -->
    <template v-if="viewMode === 'list'">
      <el-table
        :data="pagedFiles"
        v-loading="loading"
        row-key="id"
        class="file-table"
        :header-cell-style="{ background: '#f5f7fa' }"
        :row-style="{ height: '40px' }"
      >
        <el-table-column
          prop="name"
          label="文件名"
          min-width="300"
        >
          <template #default="{ row }">
            <div class="file-name-cell">
              <el-icon class="file-icon"><Document /></el-icon>
              <span>{{ row.name }}</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column
          prop="applicant"
          label="申请人"
          width="120"
        />
        <el-table-column
          prop="size"
          label="大小"
          width="120"
          align="right"
        >
          <template #default="{ row }">
            <span class="size-text">{{ formatFileSize(row.size) }}</span>
          </template>
        </el-table-column>
        <el-table-column
          prop="createTime"
          label="创建时间"
          width="180"
        />
        <el-table-column
          prop="updateTime"
          label="修改时间"
          width="180"
        />
        <el-table-column
          label="操作"
          width="100"
          fixed="right"
        >
          <template #default="{ row }">
            <el-popconfirm
              title="确定要删除这个文件吗?"
              @confirm="handleDelete(row)"
            >
              <template #reference>
                <el-button
                  type="danger"
                  link
                  size="small"
                >
                  <el-icon style="vertical-align: middle; margin-right: 4px"><Delete /></el-icon>
                  删除
                </el-button>
              </template>
            </el-popconfirm>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination-container">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="filteredFiles.length"
          :page-label="'页'"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        >
          <template #total="{ total }">
            总计 {{ total }} 条
          </template>
        </el-pagination>
      </div>
    </template>

    <!-- 网格视图 -->
    <template v-else>
      <el-scrollbar height="calc(100vh - 180px)">
        <div class="grid-view">
          <div v-for="file in pagedFiles" 
            :key="file.id" 
            class="grid-item"
          >
            <div class="grid-content">
              <el-icon class="grid-icon"><Document /></el-icon>
              <div class="grid-name">{{ file.name }}</div>
              <div class="grid-info">{{ formatFileSize(file.size) }}</div>
              <div class="grid-applicant">申请人：{{ file.applicant }}</div>
            </div>
            <div class="grid-actions">
              <el-popconfirm
                title="确定要删除这个文件吗?"
                @confirm="handleDelete(file)"
              >
                <template #reference>
                  <el-button
                    type="danger"
                    link
                    size="small"
                  >
                    <el-icon style="vertical-align: middle; margin-right: 4px"><Delete /></el-icon>
                    删除
                  </el-button>
                </template>
              </el-popconfirm>
            </div>
          </div>
        </div>
      </el-scrollbar>

      <!-- 网格视图的分页 -->
      <div class="pagination-container">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[12, 24, 48, 96]"
          :total="filteredFiles.length"
          :page-label="'页'"
          layout="total, jumper, sizes, prev, pager, next"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        >
          <template #total="{ total }">
            总计 {{ total }} 条
          </template>
        </el-pagination>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { 
  Search, Delete, Document, 
  Menu, Grid, Back, User
} from '@element-plus/icons-vue'


const router = useRouter();

// 测试数据
const mockFiles = [
  {
    id: '1',
    name: '研究报告2024.pdf',
    type: 'file',
    size: 1024 * 1024 * 2.5,
    createTime: '2024-03-15 14:30:00',
    updateTime: '2024-03-15 14:30:00',
    applicant: '张三'
  },
  {
    id: '2',
    name: '数据分析.xlsx',
    type: 'file',
    size: 1024 * 512,
    createTime: '2024-03-14 09:15:00',
    updateTime: '2024-03-14 09:15:00',
    applicant: '李四'
  },
  {
    id: '3',
    name: '会议记录.docx',
    type: 'file',
    size: 1024 * 128,
    createTime: '2024-03-13 16:45:00',
    updateTime: '2024-03-13 16:45:00',
    applicant: '王五'
  }
  // ... 可以添加更多测试数据
];

const files = ref(mockFiles);
const searchText = ref('');
const searchApplicant = ref('');
const loading = ref(false);
const viewMode = ref('list');
const currentPage = ref(1);
const pageSize = ref(10);

// 格式化文件大小
const formatFileSize = (size) => {
  if (!size) return '0 B';
  if (size < 1024) return size + ' B';
  if (size < 1024 * 1024) return (size / 1024).toFixed(2) + ' KB';
  if (size < 1024 * 1024 * 1024) return (size / (1024 * 1024)).toFixed(2) + ' MB';
  return (size / (1024 * 1024 * 1024)).toFixed(2) + ' GB';
};

// 搜索过滤
const filteredFiles = computed(() => files.value);

// 分页数据
const pagedFiles = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value;
  const end = start + pageSize.value;
  return filteredFiles.value.slice(start, end)
});

// 分页处理
const handleSizeChange = (val) => {
  pageSize.value = val;
  currentPage.value = 1;
};

const handleCurrentChange = (val) => {
  currentPage.value = val
};

// 删除文件
const handleDelete = async (file) => {
  try {
    await new Promise(resolve => setTimeout(resolve, 300));
    ElMessage.success('删除文件成功');
    files.value = files.value.filter(item => item.id !== file.id)
  } catch (error) {
    ElMessage.error('删除失败')
  }
};

// 返回首页
const backToHome = () => {
  router.push('/workspace')
};

// 修改搜索处理函数
const handleSearch = async () => {
  loading.value = true;
  try {
    // 实际项目中这里应该调用后端API
    const params = new URLSearchParams({
      filename: searchText.value,
      applicant: searchApplicant.value
    });
    
    // 示例API调用
    // const response = await fetch(`/api/files/search?${params}`)
    // const data = await response.json()
    // files.value = data
    
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 500));
    files.value = mockFiles.filter(file => {
      const nameMatch = file.name.toLowerCase().includes(searchText.value.toLowerCase());
      const applicantMatch = file.applicant.toLowerCase().includes(searchApplicant.value.toLowerCase());
      return nameMatch && applicantMatch
    });
    
    ElMessage.success('搜索完成')
  } catch (error) {
    ElMessage.error('搜索失败')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.file-management {
  padding: 16px;
  background-color: #fff;
  min-height: calc(100vh - 32px);
}

.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  padding: 12px 16px;
  background-color: #fff;
  border-radius: 4px;
  border: 1px solid #e4e7ed;
}

.right {
  display: flex;
  gap: 16px;
  align-items: center;
}

.search-input {
  width: 250px;
}

.file-table {
  border: 1px solid #e4e7ed;
  border-radius: 4px;
}

.file-name-cell {
  display: flex;
  align-items: center;
  gap: 8px;
}

.folder-icon {
  color: #ffd04b;
  font-size: 16px;
}

.file-icon {
  color: #909399;
  font-size: 16px;
}

.size-text {
  color: #606266;
  font-family: monospace;
}

.grid-view {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  gap: 16px;
  padding: 16px;
}

.grid-item {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 12px;
  border-radius: 4px;
  border: 1px solid #e4e7ed;
  cursor: pointer;
  transition: all 0.3s;
}

.grid-item:hover {
  background-color: #f5f7fa;
}

.grid-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
}

.grid-icon {
  font-size: 32px;
  margin-bottom: 8px;
  color: #409eff;
}

.grid-name {
  font-size: 14px;
  color: #303133;
  text-align: center;
  margin-bottom: 4px;
  width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.grid-info {
  font-size: 12px;
  color: #909399;
}

.grid-actions {
  position: absolute;
  top: 8px;
  right: 8px;
  opacity: 0;
  transition: opacity 0.3s;
}

.grid-item:hover .grid-actions {
  opacity: 1;
}

:deep(.el-table__row) {
  height: 40px;
}

:deep(.el-table__cell) {
  padding-top: 4px !important;
  padding-bottom: 4px !important;
}

:deep(.el-breadcrumb__item) span {
  cursor: pointer;
  color: #606266;
}

:deep(.el-breadcrumb__item) span:hover {
  color: #409EFF;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 16px 0;
  width: 100%;
}

:deep(.el-pagination) {
  display: flex;
  justify-content: center;
  align-items: center;
}

.grid-applicant {
  font-size: 12px;
  color: #606266;
  margin-top: 4px;
}

.search-group {
  display: flex;
  gap: 8px;
  align-items: center;
}

:deep(.el-button--danger.el-button--link) {
  padding: 4px 8px;
  height: auto;
}

:deep(.el-button--danger.el-button--link:hover) {
  background-color: #fef0f0;
  border-radius: 4px;
}

:deep(.el-radio-button__inner) {
  display: flex;
  align-items: center;
  gap: 4px;
}
</style> 