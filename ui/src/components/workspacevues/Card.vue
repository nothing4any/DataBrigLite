<!-- src/components/Card.vue -->
<template>
    <div class="card" @click="handleClick">
        <div class="card-content">
            <el-icon class="card-icon" :class="iconColor">
                <component :is="resolveIcon(icon)" />
            </el-icon>
            <div class="card-title">{{ title }}</div>
        </div>
    </div>
</template>

<script>
import { 
    DataLine, 
    Platform, 
    Monitor, 
    Connection,
    Document,
    User,
    Setting,
    List,
    Management,
    Histogram,
    Operation,
    Share,
    Bell
} from '@element-plus/icons-vue'

export default {
    name: 'Card',
    components: {
        DataLine, 
        Platform, 
        Monitor, 
        Connection,
        Document,
        User,
        Setting,
        List,
        Management,
        Histogram,
        Operation,
        Share,
        Bell
    },
    props: {
        title: {
            type: String,
            required: true
        },
        icon: {
            type: String,
            required: true
        },
        link: {
            type: String,
            required: true
        },
        iconColor: {
            type: String,
            default: 'primary'  // primary, success, warning, danger
        }
    },
    methods: {
        handleClick() {
            this.$router.push(this.link)
        },
        resolveIcon(iconName) {
            // 确保图标名称存在
            return this.$options.components[iconName] ? iconName : 'Document'
        }
    }
}
</script>

<style scoped>
.card {
    position: relative;
    width: 200px;
    height: 200px;
    border-radius: 8px;
    background: white;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
    cursor: pointer;
    transition: all 0.3s ease;
}

.card:hover {
    transform: translateY(-5px);
    box-shadow: 0 4px 16px 0 rgba(0, 0, 0, 0.2);
}

.card-content {
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 20px;
}

.card-icon {
    font-size: 64px;
    margin-bottom: 16px;
    transition: transform 0.3s ease;
}

.card:hover .card-icon {
    transform: scale(1.1);
}

.card-title {
    font-size: 18px;
    font-weight: 500;
    color: #303133;
}

/* 图标颜色类 */
.primary {
    color: #409eff;
}

.success {
    color: #67c23a;
}

.warning {
    color: #e6a23c;
}

.danger {
    color: #f56c6c;
}
</style>