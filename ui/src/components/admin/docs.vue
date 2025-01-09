<template>
    <div class="docs-management">
        <el-card class="docs-card">
            <template #header>
                <div class="card-header">
                    <el-icon><Document /></el-icon>
                    <span>API文档管理</span>
                </div>
            </template>
            
            <div class="docs-content">
                <div class="status-section">
                    <el-switch
                        v-model="isEnabled"
                        @change="handleSwitchChange"
                        :loading="loading"
                        active-color="#409EFF"
                        inline-prompt
                        :active-text="'开启'"
                        :inactive-text="'关闭'"
                    />
                    <span class="status-text" :class="{ 'status-active': isEnabled }">
                        {{ isEnabled ? '文档功能已开启' : '文档功能已关闭' }}
                    </span>
                </div>

                <div v-if="isEnabled" class="docs-link-section">
                    <el-alert
                        title="文档访问链接"
                        type="success"
                        :closable="false"
                        class="docs-alert"
                    >
                        <template #default>
                            <div class="link-container">
                                <el-link 
                                    type="primary" 
                                    :href="docsUrl" 
                                    target="_blank"
                                    class="docs-link"
                                >
                                    {{ docsUrl }}
                                </el-link>
                                <el-button
                                    type="primary"
                                    link
                                    @click="copyLink"
                                    class="copy-btn"
                                >
                                    <el-icon><CopyDocument /></el-icon>
                                    复制链接
                                </el-button>
                            </div>
                        </template>
                    </el-alert>
                </div>

                <div class="docs-info">
                    <el-descriptions :column="1" border>
                        <el-descriptions-item label="更新时间">
                            {{ lastUpdateTime }}
                        </el-descriptions-item>
<!--                        <el-descriptions-item label="访问次数">-->
<!--                            {{ visitCount }}-->
<!--                        </el-descriptions-item>-->
                    </el-descriptions>
                </div>
            </div>
        </el-card>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { ElMessage } from 'element-plus';
import { Document, CopyDocument } from '@element-plus/icons-vue';
import { getDocsStatus, updateDocsStatus } from "@/api/api";

const isEnabled = ref(false);
const loading = ref(true);
const docsUrl = ref(window.location.origin + '/docs');
const lastUpdateTime = ref('2024-03-21 15:30:00');
const visitCount = ref(1234);

// 获取当前文档功能状态
const getStatus = async () => {
    try {
        const res = await getDocsStatus();
        isEnabled.value = res.data.enabled;
    } catch (error) {
        ElMessage.error('获取文档状态失败');
    } finally {
        loading.value = false;
    }
};

// 处理开关变化
const handleSwitchChange = async (checked) => {
    loading.value = true;
    try {
        await updateDocsStatus(checked);
        isEnabled.value = checked;
        ElMessage.success(checked ? '文档功能已开启' : '文档功能已关闭');
    } catch (error) {
        ElMessage.error('更新文档状态失败');
        isEnabled.value = !checked;
    } finally {
        loading.value = false;
    }
};

// 复制链接
const copyLink = async () => {
    try {
        await navigator.clipboard.writeText(docsUrl.value);
        ElMessage.success('链接已复制到剪贴板');
    } catch (err) {
        ElMessage.error('复制失败，请手动复制');
    }
};

onMounted(() => {
    getStatus();
});
</script>

<style scoped>
.docs-management {
    padding: 20px;
    max-width: 800px;
    margin: 0 auto;
}

.docs-card {
    background: #fff;
    border-radius: 8px;
}

.card-header {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 16px;
    font-weight: 600;
    color: #303133;
}

.docs-content {
    display: flex;
    flex-direction: column;
    gap: 24px;
}

.status-section {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 16px 0;
}

.status-text {
    font-size: 14px;
    color: #909399;
    transition: color 0.3s ease;
}

.status-active {
    color: #67c23a;
}

.docs-link-section {
    margin: 16px 0;
}

.docs-alert {
    margin: 0;
}

.link-container {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-top: 8px;
}

.docs-link {
    font-size: 14px;
    word-break: break-all;
}

.copy-btn {
    white-space: nowrap;
    margin-left: 16px;
}

.docs-info {
    margin-top: 16px;
}

:deep(.el-descriptions__label) {
    width: 120px;
    justify-content: flex-end;
}
</style>