<template>
  <div class="request-management">
    <div class="page-header">
      <div class="header-left">
        <el-button @click="goBack">
            <el-icon><ArrowLeft /></el-icon>返回
          </el-button>
        <h2>请求管理</h2>
      </div>
      
      <div class="header-right">
        <el-button type="primary" @click="handleFilter">
          <el-icon><Search /></el-icon>查询
        </el-button>
        <el-button @click="resetFilter">
          <el-icon><Refresh /></el-icon>重置
        </el-button>
      </div>
    </div>

    <el-card class="filter-section">
      <el-form :inline="true" :model="filterForm" label-width="80px">
        <el-form-item label="状态">
          <el-select
            v-model="filterForm.status"
            placeholder="全部状态"
            clearable
            style="width: 120px"
          >
            <el-option
              v-for="item in statusOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        
        <el-form-item label="提交日期">
          <el-date-picker
            v-model="filterForm.dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            format="YYYY年MM月DD日"
            value-format="YYYY-MM-DD"
          />
        </el-form-item>
        
        <el-form-item label="提交者">
          <el-input 
            v-model="filterForm.submitter" 
            placeholder="请输入提交者"
            clearable
          />
        </el-form-item>
      </el-form>
    </el-card>

    <el-card class="data-table-section">
      <el-table
        ref="dataTable"
        :data="requestsList"
        style="width: 100%"
        v-loading="loading"
        border
        :height="tableHeight"
      >
        <el-table-column prop="requestId" label="请求编号" min-width="120" />
        <el-table-column prop="reqname" label="提交者" min-width="100" />
        <el-table-column prop="submitDate" label="提交日期" min-width="120" />
        <el-table-column prop="dataType" label="数据类型" min-width="120">
          <template #default="scope">
            {{ getDataTypeName(scope.row.dataType) }}
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" min-width="100">
          <template #default="scope">
            <el-tag :type="getStatusType(scope.row.status)">
              {{ getStatusName(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" min-width="200" fixed="right">
          <template #default="scope">
            <div class="operation-buttons">
              <el-button
                size="small"
                type="primary"
                @click="handleRequest(scope.row)"
                :disabled="scope.row.status !== 'processing'"
              >处理</el-button>
              <el-button
                size="small"
                type="success"
                :disabled="scope.row.status === 'processing' || scope.row.status === 'completed'"
                @click="acceptRequest(scope.row, 'processing')"
              >接受</el-button>
              <el-button
                  size="small"
                  type="danger"
                  :disabled="scope.row.status === 'processing' || scope.row.status === 'rejected' || scope.row.status === 'completed'"
                  @click="acceptRequest(scope.row, 'rejected')"
              >拒绝</el-button>
            </div>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-container">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>

    <el-drawer
      v-model="drawerVisible"
      title="请求处理"
      size="60%"
      :destroy-on-close="true"
      @open="handleDrawerOpen"
    >
      <template #default>
        <div class="request-detail">
          <el-descriptions title="基本信息" :column="2" border>
            <el-descriptions-item label="请求编号">{{ currentRequest.requestId }}</el-descriptions-item>
            <el-descriptions-item label="提交者">{{ currentRequest.reqname }}</el-descriptions-item>
            <el-descriptions-item label="提交日期">{{ currentRequest.submitDate }}</el-descriptions-item>
            <el-descriptions-item label="数据类型">{{ getDataTypeName(currentRequest.dataType) }}</el-descriptions-item>
            <el-descriptions-item label="状态">
              <el-tag :type="getStatusType(currentRequest.status)">
                {{ getStatusName(currentRequest.status) }}
              </el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="期望交付日期">{{ currentRequest.expectedDate }}</el-descriptions-item>
            <el-descriptions-item label="用途说明" :span="2">{{ currentRequest.purpose }}</el-descriptions-item>
          </el-descriptions>

          <div class="section-title">请求字段</div>
          <el-table 
            :data="currentRequest.fields || []" 
            border 
            style="width: 100%"
            :height="drawerTableHeight"
          >
            <el-table-column type="index" label="序号" width="80" />
            <el-table-column prop="name" label="字段名称" />
            <el-table-column prop="type" label="字段类型" />
            <el-table-column prop="description" label="字段描述" show-overflow-tooltip />
          </el-table>

          <div class="section-title">数据处理</div>
          <el-form :model="processForm" label-width="100px">
            <el-form-item label="数据文件" required v-if="currentRequest.status === 'processing'">
              <el-upload
                class="data-uploader"
                action="#"
                :auto-upload="false"
                :show-file-list="true"
                :on-change="handleFileChange"
                :on-remove="handleFileRemove"
                :limit="1"
                :file-list="processForm.fileList"
              >
                <template #trigger>
                  <el-button type="primary">选择文件</el-button>
                </template>
                <template #tip>
                  <div class="el-upload__tip">
                    支持 .xlsx, .csv 格式文件，单个文件不超过10MB
                  </div>
                </template>
              </el-upload>
            </el-form-item>

            <el-form-item label="处理说明" required>
              <el-input
                v-model="processForm.note"
                type="textarea"
                :rows="3"
                placeholder="请输入数据处理说明，例如：数据格式说明、注意事项等"
              />
            </el-form-item>

            <el-form-item>
<!--              <el-button -->
<!--                type="primary" -->
<!--                @click="updateStatus('processing')"-->
<!--                v-if="currentRequest.status === 'pending'"-->
<!--              >开始处理</el-button>-->
              <el-button 
                type="success" 
                @click="submitProcessing"
                v-if="currentRequest.status === 'processing'"
                :disabled="!canSubmitProcessing"
              >提交数据</el-button>
            </el-form-item>
          </el-form>

          <div class="section-title">处理记录</div>
          <el-timeline>
            <el-timeline-item
              v-for="(record, index) in processRecords"
              :key="index"
              :timestamp="record.time"
              :type="record.type"
            >
              <el-card class="record-card">
                <h4>{{ record.title }}</h4>
                <p>{{ record.content }}</p>
                <p v-if="record.user" class="operator">操作人：{{ record.user }}</p>
              </el-card>
            </el-timeline-item>
          </el-timeline>
        </div>
      </template>
    </el-drawer>
  </div>
</template>

<script>
import { ArrowLeft, Search, Refresh } from '@element-plus/icons-vue'
import {handlereqcount, handlereqlist, acceptreq, handlefileupdate, processrecords} from "../../api/api";

export default {
  name: 'RequestManagement',
  components: {
    ArrowLeft,
    Search,
    Refresh
  },
  data() {
    return {
      filterForm: {
        status: '',
        dateRange: [],
      },
      loading: false,
      requestsList: [],
      currentPage: 1,
      pageSize: 10,
      total: 0,
      drawerVisible: false,
      currentRequest: {},
      processForm: {
        note: '',
        file: null,
        fileList: []
      },
      processRecords: [],
      tableHeight: '500px',
      drawerTableHeight: '300px',
      statusOptions: [
        { label: '待处理', value: 'pending' },
        { label: '处理中', value: 'processing' },
        { label: '已完成', value: 'completed' },
        { label: '已拒绝', value: 'rejected' }
      ]
    }
  },
  created() {
    this.fetchRequests()
  },
  computed: {
    canSubmitProcessing() {
      return this.processForm.file && this.processForm.note.trim()
    }
  },
  mounted() {
    this.calculateTableHeight();
    window.addEventListener('resize', this.debounce(this.calculateTableHeight, 200))
  },
  beforeUnmount() {
    window.removeEventListener('resize', this.debounce(this.calculateTableHeight, 200))
  },
  methods: {
    // 获取请求列表
    async fetchRequests() {
      this.loading = true;
      try {
        // this.requestsList = [
        //   {
        //     requestId: 'REQ20240101001',
        //     submitter: '张三',
        //     submitDate: '2024-01-01',
        //     dataType: 'user_data',
        //     status: 'processing',
        //     expectedDate: '2024-01-10',
        //     purpose: '用户行为分析',
        //     fields: [
        //       { name: '用户ID', type: '文本', description: '用户唯一标识' },
        //       { name: '注册时间', type: '日期', description: '用户注册时间' }
        //     ]
        //   }
        // ];
        // this.total = this.requestsList.length
        if (this.filterForm.dateRange.length === 0){
          this.filterForm.dateRange[0] = "";
          this.filterForm.dateRange[1] = "";
        }
        let para = {
          "usernumber": localStorage.getItem("usernumber"),
          "status": this.filterForm.status,
          "stratdt": this.filterForm.dateRange[0],
          "enddt": this.filterForm.dateRange[1],
          "pagenumber": this.currentPage,
          "pagesize": this.pageSize
        };

        handlereqlist(para).then(res=>{
          if(res.data.code === "200"){
            this.requestsList = res.data.data
          }else{
            this.$message.warning(res.data.msg)
          }
        });

        handlereqcount(para).then(res=>{
          if(res.data.code === "200"){
            this.total = res.data.data
          }else{
            this.$message.warning(res.data.msg)
          }
        });
      } catch (error) {
        this.$message.error('获取数据失败')
      } finally {
        this.loading = false
      }
    },

    // 处理请求
    handleRequest(row) {
      this.currentRequest = { ...row }
      this.drawerVisible = true
      this.loadProcessRecords(this.currentRequest)
    },

    // 加载处理记录
    async loadProcessRecords(info) {
      try {
        const para = {
          "requestno": info.requestId
        }
        processrecords(para).then(res=>{
          if(res.data.code === "200"){
            this.processRecords = res.data.data
          }else{
            this.$message.warning(res.data.msg)
          }
        });
        // this.processRecords = [
        //   {
        //     time: '2024-01-01 10:00:00',
        //     type: 'primary',
        //     title: '请求提交',
        //     content: '用户提交了数据请求',
        //     user: '张三'
        //   }
        // ]
      } catch (error) {
        this.$message.error('获取处理记录失败')
      }
    },

    // 更新请求状态
    async updateStatus(status) {
      if (!this.processForm.note.trim()) {
        this.$message.warning('请输入处理说明')
        return
      }

      try {
        const record = {
          time: new Date().toLocaleString(),
          type: 'success',
          title: status === 'processing' ? '开始处理' : '处理完成',
          content: this.processForm.note,
          operator: '当前操作人'
        }

        this.currentRequest.status = status
        this.processRecords.unshift(record)
        this.$message.success('状态更新成功')
        
        if (status === 'completed') {
          this.drawerVisible = false
        }
        
        this.fetchRequests()
      } catch (error) {
        this.$message.error('状态更新失败')
      }
    },

    // 文件上传处理
    handleFileChange(file) {
      // 验证文件大小
      const isLt10M = file.size / 1024 / 1024 < 100
      if (!isLt10M) {
        this.$message.error('文件大小不能超过 10MB!')
        return false
      }

      // 验证文件类型
      const fileExtension = file.name.split('.').pop().toLowerCase()
      const allowedExtensions = ['xlsx', 'csv', 'xls', 'txt']
      if (!allowedExtensions.includes(fileExtension)) {
        this.$message.error('只支持 .xlsx, .csv 格式的文件!')
        return false
      }

      this.processForm.file = file
      this.processForm.fileList = [file]
    },

    handleFileRemove() {
      this.processForm.file = null
      this.processForm.fileList = []
    },

    // 提交数据处理
    async submitProcessing() {
      if (!this.canSubmitProcessing) {
        this.$message.warning('请上传数据文件并填写处理说明')
        return
      }

      try {
        const formData = new FormData()
        formData.append('file', this.processForm.file.raw)
        formData.append('note', this.processForm.note)
        formData.append('requestid', this.currentRequest.requestId)
        formData.append('usernumber', localStorage.getItem("usernumber"))
        formData.append('status', "completed")

        // 模拟上传过程
        handlefileupdate(formData).then(res=>{
          if(res.data.code === "200"){
            this.$message.success(res.data.msg)
            this.fetchRequests()
          }else{
            this.$message.warning(res.data.msg)
          }
        });

        // 更新处理记录
        const record = {
          time: new Date().toLocaleString(),
          type: 'success',
          title: '数据提交',
          content: this.processForm.note,
          operator: '当前操作人'
        }

        this.currentRequest.status = 'completed'
        this.processRecords.unshift(record)
        
        this.$message.success('数据提交成功')
        this.drawerVisible = false
        this.fetchRequests() // 刷新列表
      } catch (error) {
        this.$message.error('数据提交失败：' + error.message)
      }
    },

    // 其他辅助方法
    getStatusType(status) {
      const typeMap = {
        pending: 'warning',
        processing: 'primary',
        completed: 'success'
      };
      return typeMap[status] || 'info'
    },

    getStatusName(status) {
      const nameMap = {
        pending: '待处理',
        processing: '处理中',
        completed: '已完成',
        rejected: '已拒绝'
      };
      return nameMap[status] || status
    },

    getDataTypeName(type) {
      const typeMap = {
        user_data: '用户数据',
        transaction_data: '交易数据',
        system_logs: '系统日志'
      };
      return typeMap[type] || type
    },

    // 筛选和分页方法
    handleFilter() {
      this.currentPage = 1;
      this.fetchRequests()
    },

    resetFilter() {
      this.filterForm = {
        status: '',
        dateRange: [],
        submitter: ''
      };
      this.handleFilter()
    },

    handleSizeChange(val) {
      this.pageSize = val;
      this.fetchRequests()
    },

    handleCurrentChange(val) {
      this.currentPage = val;
      this.fetchRequests()
    },

    // 添加接受请求的方法
    async acceptRequest(row, status) {
      try {
        const record = {
          time: new Date().toLocaleString(),
          type: 'primary',
          title: '接受请求',
          content: '开始处理数据请求',
          operator: '当前操作人'
        };
        let para = {
          "requestid": row.submitter,
          "requestno": row.requestId,
          "status": status
        };

        acceptreq(para).then(res=>{
          if(res.data.code === "200"){
            // 更新状态
            row.status = 'processing';
            this.$message.success(res.data.msg);
            // 添加处理记录
            this.processRecords.unshift(record);

            this.fetchRequests() // 刷新列表
          }else{
            this.$message.warning(res.data.msg)
          }
        });

      } catch (error) {
        this.$message.error('操作失败：' + error.message)
      }
    },

    // 添加返回方法
    goBack() {
      this.$router.go(-1) // 返回上一页
    },

    // 添加防抖函数
    debounce(fn, delay) {
      let timer = null
      return function() {
        const context = this
        const args = arguments
        clearTimeout(timer)
        timer = setTimeout(() => {
          fn.apply(context, args)
        }, delay)
      }
    },

    // 计算表格高度
    calculateTableHeight() {
      this.$nextTick(() => {
        try {
          const windowHeight = window.innerHeight;
          const tableTop = this.$refs.dataTable.$el.getBoundingClientRect().top;
          const paginationHeight = 60;
          const padding = 40;
          this.tableHeight = `${windowHeight - tableTop - paginationHeight - padding}px`
        } catch (error) {
          console.log('计算表格高度失败:', error);
          this.tableHeight = '500px' // 设置默认高度
        }
      })
    },

    // 处理抽屉打开事件
    handleDrawerOpen() {
      this.$nextTick(() => {
        const drawerContent = document.querySelector('.el-drawer__body');
        if (drawerContent) {
          const contentHeight = drawerContent.clientHeight;
          this.drawerTableHeight = `${contentHeight - 400}px` // 根据实际内容调整偏移值
        }
      })
    }
  }
}
</script>

<style scoped>
.request-management {
  padding: 20px;
  background-color: #f5f7fa;
  min-height: 100vh;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.header-left h2 {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
  color: #303133;
}

.back-button {
  font-size: 16px;
}

.header-right {
  display: flex;
  gap: 12px;
}

.filter-section {
  margin-bottom: 20px;
}

.data-table-section {
  position: relative;
  margin-bottom: 20px;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

:deep(.el-card__body) {
  padding: 20px;
}

:deep(.el-table) {
  --el-table-header-bg-color: #f5f7fa;
  --el-table-header-text-color: #303133;
  --el-table-header-font-weight: 600;
  border-radius: 4px;
  overflow: hidden;
}

:deep(.el-table th) {
  background-color: var(--el-table-header-bg-color);
  color: var(--el-table-header-text-color);
  font-weight: var(--el-table-header-font-weight);
}

:deep(.el-form-item) {
  margin-bottom: 0;
}

:deep(.el-button) {
  display: flex;
  align-items: center;
  gap: 4px;
}

:deep(.el-tag) {
  text-align: center;
  min-width: 80px;
}

:deep(.el-drawer__body) {
  height: calc(100% - 60px);
  overflow: hidden;
  padding: 0;
}

.request-detail {
  height: 100%;
  overflow-y: auto;
  padding: 20px;
}

.section-title {
  margin: 24px 0 16px;
  padding-left: 10px;
  border-left: 4px solid #409EFF;
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}

.operation-buttons {
  display: flex;
  gap: 8px;
  flex-wrap: nowrap;
}

:deep(.el-button--small) {
  padding: 8px 15px;
  min-width: 68px;
}

:deep(.el-table__header-wrapper),
:deep(.el-table__body-wrapper) {
  overflow-y: hidden;
}

:deep(.el-table__body-wrapper) {
  overflow-y: auto;
}

:deep(.el-select) {
  width: 100%;
}

:deep(.el-select-dropdown__item) {
  padding: 0 20px;
}
</style>