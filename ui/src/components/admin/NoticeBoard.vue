<template>
    <div class="notice-board">
        <div class="notice-header">
            <div class="header-left">
                <h2>通知公告</h2>
                <el-radio-group v-model="currentType" size="small" @change="filterNotices">
                    <el-radio-button label="all">全部</el-radio-button>
                    <el-radio-button label="info">普通</el-radio-button>
                    <el-radio-button label="warning">重要</el-radio-button>
                    <el-radio-button label="danger">紧急</el-radio-button>
                </el-radio-group>
            </div>
            <el-button v-if="isAdmin" type="primary" @click="showAddDialog">
                <el-icon><Plus /></el-icon>发布通知
            </el-button>
        </div>

        <div class="notice-list" v-loading="loading">
            <el-empty v-if="filteredNotices.length === 0" description="暂无通知" />
            <el-timeline v-else>
                <el-timeline-item
                    v-for="notice in filteredNotices"
                    :key="notice.info_no"
                    :timestamp="notice.createTime"
                    :type="notice.type"
                >
                    <el-card class="notice-card" :class="{'is-new': isNewNotice(notice.createTime)}">
                        <template #header>
                            <div class="notice-title">
                                <div class="title-left">
                                    <el-tag :type="notice.type" effect="dark">{{ notice.category }}</el-tag>
                                    <span class="title-text">{{ notice.title }}</span>
                                </div>
                                <div class="notice-actions" v-if="isAdmin">
                                    <el-button type="primary" link @click="editNotice(notice)">
                                        <el-icon><Edit /></el-icon>
                                    </el-button>
                                    <el-button type="danger" link @click="deleteNotice(notice.info_no)">
                                        <el-icon><Delete /></el-icon>
                                    </el-button>
                                </div>
                            </div>
                        </template>
                        <div class="notice-content" v-html="notice.content"></div>
                        <div class="notice-footer">
                            <span class="notice-time">发布时间：{{ formatTime(notice.createTime) }}</span>
                        </div>
                    </el-card>
                </el-timeline-item>
            </el-timeline>
        </div>

        <!-- 管理员的添加/编辑通知对话框 -->
        <el-dialog
            v-if="isAdmin"
            v-model="dialogVisible"
            :title="dialogType === 'add' ? '发布通知' : '编辑通知'"
            width="50%"
        >
            <el-form :model="noticeForm" label-width="80px" :rules="rules" ref="noticeFormRef">
                <el-form-item label="标题" prop="title">
                    <el-input v-model="noticeForm.title" placeholder="请输入通知标题"/>
                </el-form-item>
                <el-form-item label="类型" prop="type">
                    <el-select v-model="noticeForm.type" placeholder="请选择通知类型">
                        <el-option label="普通" value="info"/>
                        <el-option label="重要" value="warning"/>
                        <el-option label="紧急" value="danger"/>
                    </el-select>
                </el-form-item>
                <el-form-item label="分类" prop="category">
<!--                    <el-input v-model="noticeForm.category" placeholder="请输入通知分类"/>-->
                  <el-select v-model="noticeForm.category" placeholder="请输入通知分类">
                    <el-option label="系统通知" value="系统通知"/>
                    <el-option label="重要事件" value="重要事件"/>
                    <el-option label="紧急事件" value="紧急事件"/>
                  </el-select>
                </el-form-item>
                <el-form-item label="内容" prop="content">
                    <el-input
                        v-model="noticeForm.content"
                        type="textarea"
                        :rows="6"
                        placeholder="请输入通知内容"
                    />
                </el-form-item>
            </el-form>
            <template #footer>
                <span class="dialog-footer">
                    <el-button @click="dialogVisible = false">取消</el-button>
                    <el-button type="primary" @click="submitNotice">确定</el-button>
                </span>
            </template>
        </el-dialog>
    </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { Plus, Edit, Delete } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import dayjs from 'dayjs'
import {addnewinformation, delnewinformation, editnewinformation, getnewinformation} from "../../api/api";

export default {
    name: 'NoticeBoard',
    components: {
        Plus,
        Edit,
        Delete
    },
    setup() {
        const loading = ref(false)
        const notices = ref([])
        const currentType = ref('all')
        const dialogVisible = ref(false)
        const dialogType = ref('add')
        const isAdmin = ref(localStorage.getItem('userRole') === 'admin')
        
        const noticeForm = ref({
            id: '',
            info_no: '',
            title: '',
            type: 'info',
            category: '',
            content: '',
            createTime: ''
        })

        const rules = {
            title: [{ required: true, message: '请输入标题', trigger: 'blur' }],
            type: [{ required: true, message: '请选择类型', trigger: 'change' }],
            category: [{ required: true, message: '请输入分类', trigger: 'blur' }],
            content: [{ required: true, message: '请输入内容', trigger: 'blur' }]
        }

        const filteredNotices = computed(() => {
            if (currentType.value === 'all') {
                return notices.value
            }
            return notices.value.filter(notice => notice.type === currentType.value)
        })

        const getNotices = async () => {
            loading.value = true
            try {
                // 模拟数据
                notices.value = [
                    // {
                    //     id: 1,
                    //     title: '系统维护通知',
                    //     type: 'warning',
                    //     category: '系统通知',
                    //     content: '系统将于本周六凌晨2点进行维护升级，预计持续2小时。',
                    //     createTime: '2024-03-20 10:00:00'
                    // }
                ]
                const response = await getnewinformation();
                if (response.data.code === "200") {
                    notices.value = response.data.data;
                }
            } catch (error) {
                ElMessage.error('获取通知数据失败');
            } finally {
                loading.value = false
            }
        }

        const formatTime = (time) => {
            return dayjs(time).format('YYYY-MM-DD HH:mm:ss')
        }

        const isNewNotice = (time) => {
            return dayjs().diff(dayjs(time), 'hour') < 24
        }

        // 管理员功能
        const showAddDialog = () => {
            dialogType.value = 'add'
            noticeForm.value = {
                id: '',
                title: '',
                type: 'info',
                category: '',
                content: '',
                createTime: ''
            }
            dialogVisible.value = true
        }

        const editNotice = (notice) => {
            dialogType.value = 'edit'
            noticeForm.value = { ...notice }
            dialogVisible.value = true
        }

        const deleteNotice = async (id) => {
            try {
                await ElMessageBox.confirm('确定要删除这条通知吗？', '提示', {
                    type: 'warning'
                })
              const para = {"infono": id}
                const response = await delnewinformation(para);
                if (response.data.code === "200") {
                  ElMessage.success('删除成功');
                }
                getNotices()
            } catch (e) {
              ElMessage.success('服务异常')
            }
        }

        const submitNotice = async () => {
          try {
            if (dialogType.value === 'add') {
              noticeForm.value.info_no = '';
              noticeForm.value.createTime = dayjs().format('YYYY-MM-DD HH:mm:ss');
              const response = await addnewinformation(noticeForm.value);
              if (response.data.code === "200") {
                ElMessage.success(dialogType.value === 'add' ? '发布成功' : '更新成功');
              }
            }
            if (dialogType.value === 'edit') {
              const response = await editnewinformation(noticeForm.value);
              if (response.data.code === "200") {
                ElMessage.success(dialogType.value === 'add' ? '发布成功' : '更新成功');
              }
            }
          } catch (error) {
            ElMessage.error('获取通知数据失败');
          }

            dialogVisible.value = false
            getNotices()
        }

        onMounted(() => {
            getNotices();
        })

        return {
            loading,
            notices,
            currentType,
            dialogVisible,
            dialogType,
            noticeForm,
            isAdmin,
            rules,
            filteredNotices,
            showAddDialog,
            editNotice,
            deleteNotice,
            submitNotice,
            formatTime,
            isNewNotice
        }
    }
}
</script>

<style scoped>
.notice-board {
    padding: 20px;
    background-color: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
    min-height: calc(100vh - 120px);
}

.notice-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
}

.header-left {
    display: flex;
    align-items: center;
    gap: 20px;
}

.header-left h2 {
    margin: 0;
    font-size: 20px;
    font-weight: 600;
}

.notice-list {
    margin-top: 20px;
}

.notice-card {
    margin-bottom: 10px;
    transition: all 0.3s;
}

.notice-card.is-new {
    border: 1px solid #409eff;
}

.notice-title {
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.title-left {
    display: flex;
    align-items: center;
    gap: 10px;
    flex: 1;
}

.title-text {
    font-weight: bold;
    color: #303133;
}

.notice-actions {
    display: flex;
    gap: 10px;
}

.notice-content {
    margin-top: 10px;
    color: #666;
    line-height: 1.6;
}

.notice-footer {
    margin-top: 15px;
    padding-top: 10px;
    border-top: 1px solid #ebeef5;
    color: #909399;
    font-size: 13px;
}

:deep(.el-timeline-item__node--normal) {
    left: -2px;
}

:deep(.el-card__header) {
    padding: 10px 20px;
}

:deep(.el-timeline-item__content) {
    margin-left: 25px;
}

@media (max-width: 768px) {
    .notice-board {
        padding: 10px;
    }

    .header-left {
        flex-direction: column;
        align-items: flex-start;
        gap: 10px;
    }

    .notice-title {
        flex-direction: column;
        align-items: flex-start;
        gap: 8px;
    }

    .notice-actions {
        margin-top: 8px;
    }
}
</style> 