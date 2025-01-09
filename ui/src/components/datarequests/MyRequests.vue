<template>
  <div class="my-requests">
    <div class="page-header">
      <h2>我的数据请求</h2>
      
      <!-- 筛选条件 -->
      <div class="filter-section">
        <el-form :inline="true" :model="filterForm">
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
          
          <el-form-item>
            <el-button type="primary" @click="handleFilter">查询</el-button>
            <el-button @click="resetFilter">重置</el-button>
          </el-form-item>
        </el-form>
      </div>
    </div>

    <!-- 请求列表 -->
    <el-card class="table-card">
      <el-table
        ref="dataTable"
        :data="requestsList"
        style="width: 100%"
        v-loading="loading"
        :height="tableHeight"
        border
      >
        <el-table-column prop="requestId" label="请求编号" min-width="120" />
        <el-table-column prop="dataType" label="数据类型" min-width="120">
          <template #default="scope">
            {{ getDataTypeName(scope.row.dataType) }}
          </template>
        </el-table-column>
        <el-table-column prop="submitDate" label="提交日期" min-width="120" />
        <el-table-column prop="expectedDate" label="期望交付日期" min-width="120" />
        <el-table-column prop="handlername" label="处理人" min-width="120" />
        <el-table-column prop="status" label="状态" min-width="100">
          <template #default="scope">
            <el-tag :type="getStatusType(scope.row.status)">
              {{ getStatusName(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" min-width="380" fixed="right">
          <template #default="scope"> 
            <div class="operation-buttons">
              <el-button
                size="small"
                @click="viewDetails(scope.row)"
              >查看详情</el-button>
              <el-button
                size="small"
                type="success"
                :disabled="scope.row.status !== 'completed'"
                @click="downloadData(scope.row)"
              >下载数据</el-button>
              <el-button
                size="small"
                type="warning"
                v-if="scope.row.status === 'completed'"
                @click="showStatusChange(scope.row)"
              >变更状态</el-button>
              <el-button
                size="small"
                type="primary"
                @click="showFeedbackHistory(scope.row)"
              >反馈记录</el-button>
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

    <!-- 详情对话框 -->
    <el-dialog
      v-model="detailsVisible"
      title="请求详情"
      width="60%"
    >
      <el-descriptions :column="2" border>
        <el-descriptions-item label="请求编号">{{ currentRequest.requestId }}</el-descriptions-item>
        <el-descriptions-item label="数据类型">{{ getDataTypeName(currentRequest.dataType) }}</el-descriptions-item>
        <el-descriptions-item label="提交日期">{{ currentRequest.submitDate }}</el-descriptions-item>
        <el-descriptions-item label="期望交付日期">{{ currentRequest.expectedDate }}</el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="getStatusType(currentRequest.status)">
            {{ getStatusName(currentRequest.status) }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="用途说明" :span="2">{{ currentRequest.purpose }}</el-descriptions-item>
      </el-descriptions>

      <el-table :data="currentRequest.fields || []" style="margin-top: 20px">
        <el-table-column type="index" label="序号" width="80" />
        <el-table-column prop="name" label="字段名称" />
        <el-table-column prop="type" label="字段类型" />
        <el-table-column prop="description" label="字段描述" />
      </el-table>
    </el-dialog>

    <!-- 反馈对话框 -->
    <el-dialog
      v-model="feedbackVisible"
      title="提供反馈"
      width="50%"
    >
      <el-form :model="feedbackForm" label-width="100px">
        <el-form-item label="反馈类型">
          <el-select v-model="feedbackForm.type" placeholder="请选择反馈类型">
            <el-option label="问题反馈" value="issue" />
            <el-option label="建议" value="suggestion" />
            <el-option label="其他" value="other" />
          </el-select>
        </el-form-item>
        <el-form-item label="反馈内容">
          <el-input
            v-model="feedbackForm.content"
            type="textarea"
            :rows="4"
            placeholder="请输入反馈内容"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="feedbackVisible = false">取消</el-button>
          <el-button type="primary" @click="submitFeedback">提交</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 状态变更对话框 -->
    <el-dialog
      v-model="statusChangeVisible"
      title="状态变更"
      width="50%"
    >
      <el-form :model="statusChangeForm" label-width="100px">
        <el-form-item label="当前状态">
          <el-tag :type="getStatusType(currentRequest.status)">
            {{ getStatusName(currentRequest.status) }}
          </el-tag>
        </el-form-item>
        <el-form-item label="变更为">
          <el-tag type="warning">提取中</el-tag>
        </el-form-item>
        <el-form-item label="变更原因" required>
          <el-input
            v-model="statusChangeForm.reason"
            type="textarea"
            :rows="3"
            placeholder="请输入状态变更原因"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="statusChangeVisible = false">取消</el-button>
          <el-button type="primary" @click="submitStatusChange">确认变更</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 反馈记录对话框 -->
    <el-dialog
      v-model="feedbackHistoryVisible"
      title="反馈记录"
      width="60%"
    >
      <div class="feedback-history">
        <el-timeline>
          <el-timeline-item
            v-for="(record, index) in feedbackHistory"
            :key="index"
            :timestamp="record.time"
            :type="getFeedbackTypeIcon(record.type)"
          >
            <el-card class="feedback-card">
              <template #header>
                <div class="feedback-header">
                  <el-tag size="small" :type="getFeedbackTypeStyle(record.type)">
                    {{ record.type }}
                  </el-tag>
                  <span class="feedback-user">{{ record.user }}</span>
                </div>
              </template>
              <div class="feedback-content">{{ record.content }}</div>
              <div v-if="record.statusChange" class="status-change-info">
                <el-tag size="small" type="info">状态变</el-tag>
                <span>{{ getStatusName(record.statusChange.from) }} → {{ getStatusName(record.statusChange.to) }}</span>
              </div>
            </el-card>
          </el-timeline-item>
        </el-timeline>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="feedbackHistoryVisible = false">关闭</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import {download, mydataedit, myreqcount, myreqlist, processrecords} from "../../api/api";

export default {
  name: 'MyRequests',
  data() {
    return {
      filterForm: {
        status: '',
        dateRange: []
      },
      loading: false,
      requestsList: [],
      currentPage: 1,
      pageSize: 10,
      total: 0,
      detailsVisible: false,
      feedbackVisible: false,
      currentRequest: {},
      feedbackForm: {
        type: '',
        content: ''
      },
      statusChangeVisible: false,
      statusChangeForm: {
        reason: ''
      },
      feedbackHistoryVisible: false,
      feedbackHistory: [],
      tableHeight: '500px',
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
  mounted() {
    this.calculateTableHeight()
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

        myreqlist(para).then(res=>{
          if(res.data.code === "200"){
            this.requestsList = res.data.data
          }else{
            this.$message.warning(res.data.msg)
          }
        });
        myreqcount(para).then(res=>{
          if(res.data.code === "200"){
            this.total = res.data.data
          }else{
            this.$message.warning(res.data.msg)
          }
        });
        // 模拟数据
        // this.requestsList = [
        //   {
        //     requestId: 'REQ20231101001',
        //     dataType: 'user_data',
        //     submitDate: '2023-11-01',
        //     expectedDate: '2023-11-10',
        //     handler: "yw",
        //     status: 'completed',
        //     purpose: '用于用户行为分析',
        //     fields: [
        //       { name: '用户ID', type: '文本', description: '用户唯一标识' },
        //       { name: '注册时间', type: '日期', description: '用户注册的时间' }
        //     ]
        //   },
        //   // ... 其他请求数据
        // ]
      } catch (error) {
        this.$message.error('获取数据失败')
      } finally {
        this.loading = false
      }
    },

    // 筛选处理
    handleFilter() {
      this.currentPage = 1
      this.fetchRequests()
    },

    resetFilter() {
      this.filterForm = {
        status: '',
        dateRange: []
      }
      this.handleFilter()
    },

    // 分页处理
    handleSizeChange(val) {
      this.pageSize = val
      this.fetchRequests()
    },

    handleCurrentChange(val) {
      this.currentPage = val
      this.fetchRequests()
    },

    // 状态相关
    getStatusType(status) {
      const typeMap = {
        pending: 'warning',
        processing: 'primary',
        completed: 'success',
        rejected: 'danger'
      }
      return typeMap[status] || 'info'
    },

    getStatusName(status) {
      const nameMap = {
        pending: '待处理',
        processing: '处理中',
        completed: '已完成',
        rejected: '已拒绝'
      }
      return nameMap[status] || status
    },

    getDataTypeName(type) {
      const typeMap = {
        user_data: '用户数据',
        transaction_data: '交易数据',
        system_logs: '系统日志'
      }
      return typeMap[type] || type
    },

    // 操作处理
    viewDetails(row) {
      this.currentRequest = { ...row }
      this.detailsVisible = true
    },

    async downloadData(row) {
      if (row.status !== 'completed') {
        this.$message.warning('只能下载已完成的数据')
        return
      }
      try {
        this.$message.success('开始下载数据')
        let submitData = {"requestno": row.requestId};
        const config = {
          responseType: 'arraybuffer'
        };

        await download( submitData, config).then(res=> {
          if (res.status === 200){
            let fileName = "download.csv";

            if (contentDispositionHeader) {
              // 尝试解析 filename*
              const filenameStarMatch = contentDispositionHeader.match(/filename\*=UTF-8''(.*?)$/);
              if (filenameStarMatch && filenameStarMatch.length > 1) {
                fileName = decodeURIComponent(filenameStarMatch[1]);
              } else {
                // 如果没有 filename*，尝试解析 filename
                const filenameMatch = contentDispositionHeader.match(/filename="(.*?)"/);
                if (filenameMatch && filenameMatch.length > 1) {
                  fileName = filenameMatch[1];
                }
              }
            }

            // 创建一个URL对象
            const fileUrl = window.URL.createObjectURL(new Blob([res.data]));

            // 创建一个<a>标签并触发点击事件进行下载
            const link = document.createElement('a');
            link.href = fileUrl;
            link.setAttribute('download', fileName); // 设置下载的文件名
            document.body.appendChild(link);
            link.click();

            // 清理
            document.body.removeChild(link);
            window.URL.revokeObjectURL(fileUrl);
          }else{
            this.$message.success('下载失败,请变更状态提交反馈')
          }
        }).catch(function (error) {
          console.log(error);
          this.$message.success('下载失败,请变更状态提交反馈')
        });
      } catch (error) {
        this.$message.success('下载失败,请变更状态提交反馈')
      }
    },

    provideFeedback(row) {
      this.currentRequest = row
      this.feedbackVisible = true
    },

    async submitFeedback() {
      if (!this.feedbackForm.type || !this.feedbackForm.content) {
        this.$message.warning('请完整填写反馈信息')
        return
      }
      try {
        this.$message.success('反馈提交成功')
        this.feedbackVisible = false
      } catch (error) {
        this.$message.error('反馈提交失败')
      }
    },

    // 状态变更处理
    showStatusChange(row) {
      this.currentRequest = { ...row }
      this.statusChangeVisible = true
      this.statusChangeForm.reason = ''
    },

    async submitStatusChange() {
      if (!this.statusChangeForm.reason.trim()) {
        this.$message.warning('请输入变更原因')
        return
      }

      try {
        // 模拟 API 调用
        const changeRecord = {
          time: new Date().toLocaleString(),
          type: '状态变更',
          user: '当前用户',
          content: this.statusChangeForm.reason,
          statusChange: {
            from: this.currentRequest.status,
            to: 'processing'
          }
        }
        const para = {
          requestid: localStorage.getItem("usernumber"),
          requestno: this.currentRequest.requestId,
          status: "processing",
          remake: this.statusChangeForm.reason
        }
        mydataedit(para).then(res=>{
          if(res.data.code === "200"){
            this.total = res.data.data
          }else{
            this.$message.warning(res.data.msg)
          }
        });

        // 更新本地数据
        this.currentRequest.status = 'processing'
        this.feedbackHistory.unshift(changeRecord)
        
        this.$message.success('状态变更成功')
        this.statusChangeVisible = false
        this.fetchRequests() // 刷新列表
      } catch (error) {
        this.$message.error('状态变更失败')
      }
    },

    // 反馈记录处理
    async showFeedbackHistory(row) {
      this.currentRequest = { ...row }
      this.feedbackHistoryVisible = true
      
      try {
        const para = {
          "requestno": row.requestId
        }

        processrecords(para).then(res=>{
          if(res.data.code === "200"){
            this.feedbackHistory = res.data.data
          }else{
            this.$message.warning(res.data.msg)
          }
        });
        // this.feedbackHistory = [
        //   {
        //     time: '2024-01-10 14:30:00',
        //     type: '状态变更',
        //     user: '',
        //     content: '数据需要重新提取',
        //     statusChange: {
        //       from: 'completed',
        //       to: 'processing'
        //     }
        //   },
        //   {
        //     time: '2024-01-09 16:20:00',
        //     type: '状态变更',
        //     user: '',
        //     content: '数据格式有误，需要修正'
        //   }
        // ]
      } catch (error) {
        this.$message.error('获取反馈记录失败')
      }
    },

    // 获取反馈类型图标
    getFeedbackTypeIcon(type) {
      const iconMap = {
        '状态变更': 'warning',
        '问题反馈': 'danger',
        '提交请求': 'info',
        "请求处理完成": 'success'
      }
      return iconMap[type] || 'info'
    },

    // 获取反馈类型样式
    getFeedbackTypeStyle(type) {
      const styleMap = {
        '状态变更': 'warning',
        '问题反馈': 'danger',
        '建议': 'info'
      }
      return styleMap[type] || ''
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
          const windowHeight = window.innerHeight
          const tableTop = this.$refs.dataTable.$el.getBoundingClientRect().top
          const paginationHeight = 60
          const padding = 40
          this.tableHeight = `${windowHeight - tableTop - paginationHeight - padding}px`
        } catch (error) {
          console.log('计算表格高度失败:', error)
          this.tableHeight = '500px' // 设置默认高度
        }
      })
    }
  }
}
</script>

<style scoped>
.my-requests {
  padding: 20px;
}

.page-header {
  margin-bottom: 20px;
}

.filter-section {
  margin: 20px 0;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 4px;
}

.pagination-container {
  margin-top: 20px;
  text-align: center;
  display: flex;
  justify-content: center;
  position: relative;
}

:deep(.el-pagination) {
  white-space: normal;
  margin: 0;
  padding: 0;
  display: flex;
  align-items: center;
}

:deep(.el-pagination .el-select .el-input) {
  width: 110px;
}

:deep(.el-select-dropdown) {
  z-index: 2000;
}

:deep(.el-tag) {
  text-align: center;
  min-width: 80px;
}

.dialog-footer {
  text-align: right;
  margin-top: 20px;
}

.feedback-history {
  max-height: 400px;
  overflow-y: auto;
  padding: 20px;
}

.feedback-card {
  margin-bottom: 10px;
}

.feedback-header {
  display: flex;
  align-items: center;
  gap: 10px;
}

.feedback-user {
  color: #606266;
  font-size: 14px;
}

.feedback-content {
  margin: 10px 0;
  color: #303133;
}

.status-change-info {
  margin-top: 10px;
  display: flex;
  align-items: center;
  gap: 10px;
  color: #909399;
  font-size: 13px;
}

:deep(.el-timeline-item__node) {
  background-color: transparent;
}

:deep(.el-timeline-item__content) {
  flex: 1;
}

.operation-buttons {
  display: flex;
  gap: 8px;
  flex-wrap: nowrap;
  justify-content: flex-start;
  align-items: center;
}

:deep(.el-table) {
  --el-table-header-bg-color: #f5f7fa;
  --el-table-header-text-color: #303133;
  --el-table-header-font-weight: bold;
}

:deep(.el-table__header) {
  th {
    background-color: var(--el-table-header-bg-color);
    color: var(--el-table-header-text-color);
    font-weight: var(--el-table-header-font-weight);
  }
}

:deep(.el-table__row) {
  td {
    padding: 8px 0;
  }
}

:deep(.el-button--small) {
  padding: 8px 15px;
}

.table-card {
  margin-bottom: 20px;
}

:deep(.el-table__body-wrapper) {
  overflow-y: auto;
}

:deep(.el-table__header-wrapper) {
  overflow-y: hidden;
}

:deep(.el-card__body) {
  padding: 20px;
}


:deep(.el-select-dropdown__item) {
  padding: 0 20px;
}
</style>
