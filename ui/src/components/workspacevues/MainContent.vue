<!-- src/components/workspacevues/MainContent.vue -->
<template>
  <div class="main-content">
    <div class="card-row" v-for="(row, index) in cardRows" :key="index">
      <Card
        v-for="card in row"
        :key="card.id"
        :title="card.title"
        :icon="card.icon"
        :link="card.link"
        :icon-color="card.type"
      />
    </div>
  </div>
</template>

<script>
import Card from './Card.vue';

export default {
  name: "MainContent",
  components: {
    Card
  },
  data() {
    return {
      userRole: '', // 用户角色
      cards: [] // 卡片列表将根据角色动态生成
    }
  },
  created() {
    // 获取用户角色，这里暂时模拟，实际应从登录状态或后端获取
    this.userRole = localStorage.getItem('userRole') || 'user'
    
    // 如果是普通用户，直接跳转到我的请求页面
    if (this.userRole === 'user') {
      this.$router.push('/myrequests');
      return
    }
    
    this.initializeCards()
  },
  methods: {
    initializeCards() {
      // 基础卡片配置
      const cardConfigs = {
        admin: [
          {
            id: 1,
            title: '用户管理',
            icon: "User",
            link: '/admin/users',
            type: "primary"
          },
          {
            id: 4,
            title: '系统文档',
            icon: "Document",
            link: '/docs'
          },
          {
            id: 7,
            title: '数据请求',
            icon: "DataLine",
            link: '/myrequests'
          },
          {
            id: 8,
            title: '通知',
            icon: "Platform",
            link: '/notice'
          },
          {
            id: 9,
            title: '数据处理',
            icon: "DataLine",
            link: '/requestmanagement'
          }
        ],
        requestProcessor: [
          {
            id: 2,
            title: '数据请求',
            icon: "DataLine",
            link: '/myrequests'
          },
          {
            id: 6,
            title: '通知',
            icon: "Platform",
            link: '/notice'
          },
        ],
        dataProcessor: [
          {
            id: 3,
            title: '数据处理',
            icon: "DataLine",
            link: '/requestmanagement'
          },
          {
            id: 5,
            title: '通知',
            icon: "Platform",
            link: '/notice'
          },
        ]
      }

      // 根据角色分配卡片
      switch (this.userRole) {
        case 'admin':
          // 管理员可以看到所有卡片
          this.cards = [
            ...cardConfigs.admin,
            // ...cardConfigs.dataProcessor,
            // ...cardConfigs.requestProcessor
          ]
          break
        case 'dataProcessor':
          // 数据处理人员只看到数据处理卡片
          this.cards = [...cardConfigs.dataProcessor]
          break
        case 'requestProcessor':
          this.cards = [...cardConfigs.dataProcessor]
        default:
          this.cards = [...cardConfigs.requestProcessor]
      }
    }
  },
  computed: {
    cardRows() {
      const rows = [];
      for (let i = 0; i < this.cards.length; i += 7) { // 每行4个卡片
        rows.push(this.cards.slice(i, i + 7));
      }
      return rows;
    }
  }
}
</script>

<style scoped>
.main-content {
  padding: 20px;
  background-color: #f5f7fa;
  min-height: calc(100vh - 60px);
}

.card-row {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
}
</style>