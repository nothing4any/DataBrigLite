<template>
  <div class="data-request-form">
    <h2>数据请求提交</h2>
    
    <el-form :model="formData" :rules="rules" ref="requestForm" label-width="120px">
      <!-- 基本信息 -->
      <el-form-item label="数据类型" prop="datatype">
        <el-select v-model="formData.datatype" placeholder="请选择数据类型">
          <el-option label="用户数据" value="user_data" />
          <el-option label="交易数据" value="transaction_data" />
          <el-option label="系统日志" value="system_logs" />
        </el-select>
      </el-form-item>

      <el-form-item label="用途说明" prop="purpose">
        <el-input
          type="textarea"
          v-model="formData.purpose"
          placeholder="请详细说明数据用途"
          :rows="3"
        />
      </el-form-item>

      <!-- 添加处理人选择 -->
      <el-form-item label="处理人" prop="handler">
        <el-select 
          v-model="formData.handler" 
          placeholder="请选择处理人"
          filterable
        >
          <el-option
            v-for="item in handlers"
            :key="item.id"
            :label="item.name"
            :value="item.id"
          />
        </el-select>
      </el-form-item>

      <el-form-item label="期望交付日期" prop="expectedDate">
        <el-date-picker
          v-model="formData.expectedDate"
          type="date"
          placeholder="选择日期"
          format="YYYY年MM月DD日"
          value-format="YYYY-MM-DD"
          :disabledDate="(time) => time.getTime() < Date.now()"
        />
      </el-form-item>

      <!-- 动态字段列表 -->
      <div class="fields-list">
        <h3>需要的字段</h3>
        <div v-for="(field, index) in formData.fields" :key="index" class="field-item">
          <el-row :gutter="20">
            <el-col :span="7">
              <el-form-item
                :prop="'fields.' + index + '.name'"
                :rules="{ required: true, message: '请输入字段名称', trigger: 'blur' }"
              >
                <el-input v-model="field.name" placeholder="字段名称" />
              </el-form-item>
            </el-col>
            <el-col :span="7">
              <el-form-item
                :prop="'fields.' + index + '.type'"
                :rules="{ required: true, message: '请选择字段类型', trigger: 'change' }"
              >
                <el-select v-model="field.type" placeholder="字段类型">
                  <el-option label="文本" value="string" />
                  <el-option label="数字" value="number" />
                  <el-option label="日期" value="date" />
                  <el-option label="布尔值" value="boolean" />
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item :prop="'fields.' + index + '.description'">
                <el-input v-model="field.description" placeholder="字段描述" />
              </el-form-item>
            </el-col>
            <el-col :span="2">
              <el-button type="danger" icon="el-icon-delete" circle @click="removeField(index)" />
            </el-col>
          </el-row>
        </div>
      </div>

      <div class="field-actions">
        <el-button type="primary" plain @click="addField">手动添加字段</el-button>
        <el-upload
          class="excel-uploader"
          action="#"
          :show-file-list="false"
          :auto-upload="false"
          accept=".xlsx,.xls"
          :on-change="handleExcelUpload"
        >
          <el-button type="success" plain>
            <i class="el-icon-upload2"></i> 从Excel导入
          </el-button>
        </el-upload>
        <el-button type="info" plain @click="downloadTemplate">
          下载模板
        </el-button>
      </div>

      <div class="form-actions">
        <el-button @click="previewRequest">预览</el-button>
        <el-button type="primary" @click="submitRequest">提交</el-button>
      </div>
    </el-form>

    <!-- 预览对话框 -->
    <el-dialog
      v-model="previewVisible"
      title="数据请求预览"
      width="70%"
      class="preview-dialog"
      :append-to-body="true"
      destroy-on-close
    >
      <div class="preview-content">
        <div class="preview-section">
          <h3>基本信息</h3>
          <el-descriptions :column="2" border>
            <el-descriptions-item label="数据类型">
              {{ getDataTypeName(formData.datatype) }}
            </el-descriptions-item>
            <el-descriptions-item label="期望交付日期">
              {{ formatDate(formData.expectedDate) }}
            </el-descriptions-item>
            <el-descriptions-item label="用途说明" :span="2">
              {{ formData.purpose }}
            </el-descriptions-item>
          </el-descriptions>
        </div>

        <div class="preview-section">
          <h3>字段信息</h3>
          <el-table :data="formData.fields" border style="width: 100%">
            <el-table-column type="index" label="序号" width="80" align="center" />
            <el-table-column prop="name" label="字段名称" />
            <el-table-column prop="type" label="字段类型">
              <template #default="scope">
                {{ getFieldTypeName(scope.row.type) }}
              </template>
            </el-table-column>
            <el-table-column prop="description" label="字段描述" show-overflow-tooltip />
          </el-table>
        </div>

        <div class="preview-summary">
          <p>总计: {{ formData.fields.length }} 个字段</p>
        </div>
      </div>
      
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="previewVisible = false">关闭</el-button>
          <el-button type="primary" @click="handleExport">导出预览</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import * as XLSX from 'xlsx'
// 引入 Element Plus 的中文语言包
import zhCn from 'element-plus/dist/locale/zh-cn.mjs'
import {datareq, usermap} from "@/api/api";

export default {
  name: 'DataRequestForm',
  data() {
    return {
      formData: {
        datatype: '',
        purpose: '',
        handler: '',
        reqid: localStorage.getItem("usernumber"),
        expectedDate: '',
        fields: []
      },
      rules: {
        datatype: [
          { required: true, message: '请选择数据类型', trigger: 'change' }
        ],
        purpose: [
          { required: true, message: '请填写用途说明', trigger: 'blur' }
        ],
        handler: [
          { required: true, message: '请选择处理人', trigger: 'change' }
        ],
        expectedDate: [
          { required: true, message: '请选择期望交付日期', trigger: 'change' }
        ]
      },
      previewVisible: false,
      tableHeight: '400px',
      handlers: [
        { id: "1", name: '张三' },
        { id: "2", name: '李四' },
        { id: "3", name: '王五' }
      ]
    }
  },
  mounted() {
    this.get_user_map();
  }
  ,
  methods: {
    get_user_map(){
      usermap(null).then(res=>{
        if(res.data.code === "200"){
          this.handlers = res.data.data;
        }else{
          this.$message.warning(res.data.msg)
        }
      })
    },

    addField() {
      this.formData.fields.push({
        name: '',
        type: '',
        description: ''
      })
    },
    removeField(index) {
      this.formData.fields.splice(index, 1)
    },
    previewRequest() {
      this.previewVisible = true
      this.$nextTick(() => {
        const previewContent = document.querySelector('.preview-content')
        if (previewContent) {
          this.tableHeight = `${previewContent.clientHeight - 200}px`
        }
      })
    },
    submitRequest() {
      this.$refs.requestForm.validate(valid => {
        if (valid) {
          datareq(this.formData).then(res=>{
            if(res.data.code === "200"){
              this.$message.success(res.data.msg)
              this.$router.push('/myrequests')
            }else{
              this.$message.warning(res.data.msg)
            }
          })

        } else {
          this.$message.error('请完善表单信息')
          return false
        }
      })
    },
    async handleExcelUpload(file) {
      try {
        const data = await this.readExcel(file.raw)
        // 验证数据格式
        if (this.validateExcelData(data)) {
          // 将Excel据转换为字段格式
          const fields = data.map(row => ({
            name: row['字段名称'] || '',
            type: this.mapExcelTypeToFieldType(row['字段类型'] || ''),
            description: row['字段描述'] || ''
          })).filter(field => field.name && field.type)

          // 添加到现有字段中
          this.formData.fields.push(...fields)
          this.$message.success(`成功导入 ${fields.length} 个字段`)
        }
      } catch (error) {
        this.$message.error('Excel导入失败：' + error.message)
      }
    },
    readExcel(file) {
      return new Promise((resolve, reject) => {
        const reader = new FileReader()
        reader.onload = (e) => {
          try {
            const data = e.target.result
            const workbook = XLSX.read(data, { type: 'array' })
            const firstSheetName = workbook.SheetNames[0]
            const worksheet = workbook.Sheets[firstSheetName]
            const jsonData = XLSX.utils.sheet_to_json(worksheet)
            resolve(jsonData)
          } catch (error) {
            reject(error)
          }
        }
        reader.onerror = reject
        reader.readAsArrayBuffer(file)
      })
    },
    validateExcelData(data) {
      if (!Array.isArray(data) || data.length === 0) {
        this.$message.error('Excel文件格式不正确或为空')
        return false
      }

      const requiredColumns = ['字段名称', '字段类型', '字段描述']
      const firstRow = data[0]
      const hasRequiredColumns = requiredColumns.every(col => 
        Object.keys(firstRow).includes(col)
      )

      if (!hasRequiredColumns) {
        this.$message.error('Excel文件必须包含：字段名称、字段类型、字段描述列')
        return false
      }

      return true
    },
    mapExcelTypeToFieldType(excelType) {
      const typeMap = {
        "文本": 'string',
        '数字': 'number',
        '日期': 'date',
        '布尔值': 'boolean'
      }
      return typeMap[excelType] || 'string'
    },
    downloadTemplate() {
      // 创建模板数据
      const template = [
        {
          '字段名称': '示例字段',
          '字段类型': '文本',
          '字段描述': '这是一个示例字段'
        }
      ]

      // 创建工作簿
      const wb = XLSX.utils.book_new()
      const ws = XLSX.utils.json_to_sheet(template)

      // 设置列宽
      ws['!cols'] = [
        { wch: 15 }, // 字段名称列宽
        { wch: 10 }, // 字段类型列宽
        { wch: 30 }  // 字段描述列宽
      ]

      XLSX.utils.book_append_sheet(wb, ws, '字段模板')

      // 下载文件
      XLSX.writeFile(wb, '字段导入模板.xlsx')
    },
    getDataTypeName(type) {
      const typeMap = {
        'user_data': '用户数据',
        'transaction_data': '交易数据',
        'system_logs': '系统日志'
      }
      return typeMap[type] || type
    },
    getFieldTypeName(type) {
      const typeMap = {
        'string': '文本',
        'number': '数字',
        'date': '日期',
        'boolean': '布尔值'
      }
      return typeMap[type] || type
    },
    formatDate(date) {
      if (!date) return ''
      const d = new Date(date)
      return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
    },
    handleExport() {
      // 创建预览数据
      const previewData = {
        基本信息: {
          数据类型: this.getDataTypeName(this.formData.datatype),
          期望交付日期: this.formatDate(this.formData.expectedDate),
          用途说明: this.formData.purpose
        },
        字段清单: this.formData.fields.map((field, index) => ({
          序号: index + 1,
          字段名称: field.name,
          字段类型: this.getFieldTypeName(field.type),
          字段描述: field.description
        }))
      }

      // 创建工作簿
      const wb = XLSX.utils.book_new()
      
      // 创建基本信息工作表
      const basicInfoWs = XLSX.utils.json_to_sheet([previewData.基本信息])
      XLSX.utils.book_append_sheet(wb, basicInfoWs, '基本信息')
      
      // 创建字段清单工作表
      const fieldsWs = XLSX.utils.json_to_sheet(previewData.字段清单)
      XLSX.utils.book_append_sheet(wb, fieldsWs, '字段清单')

      // 下载文件
      XLSX.writeFile(wb, '数据请求预览.xlsx')
    }
  }
}
</script>

<style scoped>
.data-request-form {
  max-width: 1200px;
  margin: 20px auto;
  padding: 20px;
}

.fields-list {
  margin: 20px 0;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 4px;
}

.field-item {
  margin-bottom: 10px;
}

.form-actions {
  margin-top: 30px;
  text-align: center;
}

.field-actions {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.excel-uploader {
  display: inline-block;
}

.preview-dialog {
  display: flex;
  flex-direction: column;
}

.preview-content {
  flex: 1;
  overflow: hidden;
  padding: 20px;
}

.preview-section {
  margin-bottom: 24px;
}

.preview-section h3 {
  margin-bottom: 16px;
  padding-left: 8px;
  border-left: 4px solid #409EFF;
}

.preview-summary {
  margin-top: 16px;
  text-align: right;
  color: #606266;
}

:deep(.el-descriptions) {
  margin-bottom: 20px;
}

:deep(.el-descriptions__label) {
  width: 120px;
  font-weight: bold;
}

.dialog-footer {
  text-align: right;
  margin-top: 20px;
}

.preview-section :deep(.el-table) {
  height: v-bind(tableHeight);
}

:deep(.el-dialog__body) {
  overflow: hidden;
  padding: 0;
}

:deep(.el-descriptions__body) {
  width: 100%;
}
</style> 