<template>
  <div class="user-management">
    <div class="page-header">
      <div class="header-left">
        <el-button @click="goBack">
          <el-icon><ArrowLeft /></el-icon>返回
        </el-button>
        <h2>用户管理</h2>
      </div>
      
      <div class="header-right">
        <el-button type="primary" @click="showAddUserDialog">
          <el-icon><Plus /></el-icon>添加用户
        </el-button>
      </div>
    </div>

    <el-card class="data-table-section">
      <el-table
        :data="userList"
        style="width: 100%"
        v-loading="loading"
        border
      >
        <el-table-column prop="userId" label="用户号" min-width="120" />
        <el-table-column prop="username" label="用户名" min-width="120" />
        <el-table-column prop="email" label="邮箱" min-width="180" />
        <el-table-column prop="department" label="部门" min-width="120">
          <template #default="scope">
            <el-tag type="info">{{ scope.row.department }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" min-width="120">
          <template #default="scope">
            <el-switch
              v-model="scope.row.status"
              :active-value="1"
              :inactive-value="0"
              @change="handleStatusChange(scope.row)"
              active-text="启用"
              inactive-text="禁用"
            />
          </template>
        </el-table-column>
        <el-table-column prop="role" label="角色" min-width="120">
          <template #default="scope">
            <el-tag :type="getRoleType(scope.row.role)">
              {{ getRoleName(scope.row.role) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="createTime" label="创建时间" min-width="180" />
        <el-table-column label="操作" min-width="200" fixed="right">
          <template #default="scope">
            <div class="operation-buttons">
              <el-button
                size="small"
                type="primary"
                @click="editUser(scope.row)"
              >编辑</el-button>
              <el-button
                size="small"
                type="danger"
                @click="deleteUser(scope.row)"
              >删除</el-button>
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

    <!-- 添加/编辑用户对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑用户' : '添加用户'"
      width="500px"
      :close-on-click-modal="false"
    >
      <el-form
        ref="userForm"
        :model="userForm"
        :rules="rules"
        label-width="100px"
      >
        <el-form-item label="用户号" prop="userId">
          <el-input 
            v-model="userForm.userId"
            :disabled="isEdit"
            placeholder="请输入用户号"
          />
        </el-form-item>
        <el-form-item label="用户名" prop="username">
          <el-input 
            v-model="userForm.username"
            placeholder="请输入用户名"
          />
        </el-form-item>
        
        <!-- 修改密码部分 -->
        <template v-if="isEdit">
          <el-form-item>
            <el-checkbox v-model="changePassword">修改密码</el-checkbox>
          </el-form-item>
          <template v-if="changePassword">
            <el-form-item label="新密码" prop="newPassword">
              <el-input 
                v-model="userForm.newPassword"
                type="password"
                placeholder="请输入新密码"
                show-password
              />
            </el-form-item>
            <el-form-item label="确认新密码" prop="confirmNewPassword">
              <el-input 
                v-model="userForm.confirmNewPassword"
                type="password"
                placeholder="请再次输入新密码"
                show-password
              />
            </el-form-item>
          </template>
        </template>
        
        <!-- 新用户时的密码输入 -->
        <template v-else>
          <el-form-item label="密码" prop="password">
            <el-input 
              v-model="userForm.password"
              type="password"
              placeholder="请输入密码"
              show-password
            />
          </el-form-item>
          <el-form-item label="确认密码" prop="confirmPassword">
            <el-input 
              v-model="userForm.confirmPassword"
              type="password"
              placeholder="请再次输入密码"
              show-password
            />
          </el-form-item>
        </template>

        <el-form-item label="邮箱" prop="email">
          <el-input 
            v-model="userForm.email"
            placeholder="请输入邮箱"
          />
        </el-form-item>
        
        <el-form-item label="部门" prop="department">
          <el-select v-model="userForm.department" placeholder="请选择部门">
            <el-option
              v-for="item in departmentOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>

        <el-form-item label="状态" prop="status">
          <el-switch
            v-model="userForm.status"
            :active-value="1"
            :inactive-value="0"
            active-text="启用"
            inactive-text="禁用"
          />
        </el-form-item>

        <el-form-item label="角色" prop="role">
          <el-select v-model="userForm.role" placeholder="请选择角色">
            <el-option label="普通用户" value="user" />
            <el-option label="管理员" value="admin" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitForm">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ArrowLeft, Plus } from '@element-plus/icons-vue'
import {ElMessage, ElMessageBox} from 'element-plus'
import { userlist, usercreate, userupdate, userdelete} from "@/api/api";

export default {
  name: 'UserManagement',
  components: {
    ArrowLeft,
    Plus
  },
  data() {
    // 密码验证规则
    const validatePass = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请输入密码'))
      } else {
        if (this.userForm.confirmPassword !== '') {
          this.$refs.userForm.validateField('confirmPassword')
        }
        callback()
      }
    };
    const validatePass2 = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请再次输入密码'))
      } else if (value !== this.userForm.password) {
        callback(new Error('两次输入密码不一致!'))
      } else {
        callback()
      }
    };

    // 新密码验证规则
    const validateNewPass = (rule, value, callback) => {
      if (this.changePassword && !value) {
        callback(new Error('请输入新密码'))
      } else {
        if (this.userForm.confirmNewPassword !== '') {
          this.$refs.userForm.validateField('confirmNewPassword')
        }
        callback()
      }
    };
    const validateNewPass2 = (rule, value, callback) => {
      if (this.changePassword && !value) {
        callback(new Error('请再次输入新密码'))
      } else if (value !== this.userForm.newPassword) {
        callback(new Error('两次输入密码不一致!'))
      } else {
        callback()
      }
    };

    return {
      loading: false,
      userList: [],
      currentPage: 1,
      pageSize: 10,
      total: 0,
      dialogVisible: false,
      isEdit: false,
      changePassword: false, // 是否修改密码的标志
      userForm: {
        userId: '',
        username: '',
        password: '',
        confirmPassword: '',
        newPassword: '',
        confirmNewPassword: '',
        role: 'user',
        email: '',
        department: '',
        status: 1
      },
      rules: {
        userId: [
          { required: true, message: '请输入用户号', trigger: 'blur' },
          { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' }
        ],
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' },
          { min: 2, max: 20, message: '长度在 2 到 20 个字符', trigger: 'blur' }
        ],
        password: [
          { validator: validatePass, trigger: 'blur' }
        ],
        confirmPassword: [
          { validator: validatePass2, trigger: 'blur' }
        ],
        newPassword: [
          { validator: validateNewPass, trigger: 'blur' }
        ],
        confirmNewPassword: [
          { validator: validateNewPass2, trigger: 'blur' }
        ],
        role: [
          { required: true, message: '请选择角色', trigger: 'change' }
        ],
        // email: [
        //   { required: true, message: '请输入邮箱', trigger: 'blur' },
        //   { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
        // ],
        department: [
          { required: true, message: '请选择部门', trigger: 'change' }
        ]
      },
      departmentOptions: [] // 部门选项列表
    }
  },
  created() {
    this.fetchUsers()
    this.fetchDepartments() // 获取部门列表
  },
  methods: {
    // 获取用户列表
    async fetchUsers() {
      this.loading = true
      try {
        let data = {
          "pagesize": this.pageSize,
          "pagenumber": this.currentPage
        };
        userlist(data).then(res=>{
          if(res.data.code === "200"){
            console.log(res.data.data);
            this.userList = res.data.data;
            this.total = this.userList.length
          }else{
            ElMessage({
              message: res.data.msg,
              type: 'error'
            });
          }
        });
      } catch (error) {
        this.$message.error('获取用户列表失败')
      } finally {
        this.loading = false
      }
    },

    // 显示添加用户对话框
    showAddUserDialog() {
      this.isEdit = false
      this.changePassword = false // 重置修改密码标志
      this.userForm = {
        userId: '',
        username: '',
        password: '',
        confirmPassword: '',
        newPassword: '',
        confirmNewPassword: '',
        role: 'user',
        email: '',
        department: '',
        status: 1
      };
      this.dialogVisible = true
    },

    // 编辑用户
    editUser(row) {
      this.isEdit = true;
      this.changePassword = false; // 重置修改密码标志
      this.userForm = {
        userId: row.userId,
        username: row.username,
        role: row.role,
        newPassword: '',
        confirmNewPassword: '',
        email: row.email,
        department: row.department,
        status: row.status
      };
      this.dialogVisible = true
    },

    // 删除用户
    deleteUser(row) {
      ElMessageBox.confirm(
        `确定要删除用户 ${row.username} 吗？`,
        '警告',
        {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }
      ).then(async () => {
        try {
          // TODO: 调用后端API删除用户
          this.$message.success('删除成功');
          this.fetchUsers()
        } catch (error) {
          this.$message.error('删除失败')
        }
      })
    },

    // 提交表单
    submitForm() {
      this.$refs.userForm.validate(async (valid) => {
        if (valid) {
          try {
            // 构建提交的数据
            const submitData = {
              usernumber: this.userForm.userId,
              username: this.userForm.username,
              role: this.userForm.role,
              department: this.userForm.department
            };

            // 如果是编辑模式且需要修改密码
            if (this.isEdit && this.changePassword) {
              submitData.password = this.userForm.newPassword
            }
            // 如果是新增模式
            if (!this.isEdit) {
              submitData.password = this.userForm.password
            }

            // TODO: 调用后端API保存用户
            if (this.isEdit){
              userupdate(submitData).then(res=>{
                if(res.data.code === "200"){
                  ElMessage({
                    message: res.data.msg,
                    type: 'success'
                  });
                  this.fetchUsers();
                }
              });
            }else{
              usercreate(submitData).then(res=>{
                if(res.data.code === "200"){
                  ElMessage({
                    message: res.data.msg,
                    type: 'success'
                  });
                  this.fetchUsers();
                }
              });
            }
            ElMessage({
              message: this.isEdit ? '修改成功' : '添加成功',
              type: 'success'
            });
            this.dialogVisible = false;
            this.fetchUsers()
          } catch (error) {
            ElMessage({
              message: this.isEdit ? '修改失败' : '添加失败',
              type: 'error'
            });
          }
        }
      })
    },

    // 返回
    goBack() {
      if (this.$router.options.history.state.back) {
        this.$router.go(-1) // 如果有上一页历史记录，则返回上一页
      } else {
        this.$router.push('/') // 否则返回工作空间
      }
    },

    // 获取角色类型
    getRoleType(role) {
      return role === 'admin' ? 'danger' : 'primary'
    },

    // 获取角色名称
    getRoleName(role) {
      return role === 'admin' ? '管理员' : '普通用户'
    },

    // 分页方法
    handleSizeChange(val) {
      this.pageSize = val
      this.fetchUsers()
    },

    handleCurrentChange(val) {
      this.currentPage = val
      this.fetchUsers()
    },

    // 获取部门列表
    async fetchDepartments() {
      try {
        // TODO: 调用后端API获取部门列表
        // 示例数据
        this.departmentOptions = [
          { value: 'dev', label: '研发部' },
          { value: 'ops', label: '运维部' },
          { value: 'hr', label: '人力资源部' }
        ]
      } catch (error) {
        this.$message.error('获取部门列表失败')
      }
    },

    // 处理用户状态变更
    async handleStatusChange(row) {
      try {
        // TODO: 调用后端API更新用户状态
        this.$message.success('状态更新成功')
      } catch (error) {
        this.$message.error('状态更新失败')
        row.status = !row.status // 恢复原状态
      }
    }
  },
  watch: {
    // 监听修改密码选项的变化
    changePassword(val) {
      if (!val) {
        this.userForm.newPassword = ''
        this.userForm.confirmNewPassword = ''
      }
    }
  }
}
</script>

<style scoped>
.user-management {
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

.data-table-section {
  margin-bottom: 20px;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.operation-buttons {
  display: flex;
  gap: 8px;
}

:deep(.el-tag) {
  min-width: 80px;
  text-align: center;
}

:deep(.el-form-item) {
  margin-bottom: 20px;
}
</style> 