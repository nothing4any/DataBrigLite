import { createRouter, createWebHistory } from 'vue-router';
import Login from '../components/LoginRegister.vue';
import MyRequests from '../components/datarequests/MyRequests.vue';
import Home from '../components/Home.vue';
import workspacehomeview from '../components/workspacevues/HomeOverview'
import DataRequestForm from '../components/datarequests/DataRequestForm.vue'
import RequestManagement from "../components/datarequests/RequestManagement";
import UserManagement from '../components/admin/UserManagement.vue'
import FileManagement from '../components/FileManagement.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta:{
      title: '首页'
    }
  },
  {
    path: '/home',
    name: 'Home',
    component: Home,
    meta:{
      title: '首页'
    }
  },
  {
    path: '/myrequests',
    name: 'MyRequests',
    component: MyRequests,
    meta: {
      title: '我的申请',
      requiresAdmin: true,
      requestProcessor: true
    }
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta:{
      title: '登录'
    }
  },
  {
    path: '/workspace',
    name: 'Workspace',
    component: workspacehomeview,
    meta:{
      title: '工作空间',
      requiresAdmin: true,
      requiresDataProcessor: true
    }
  },
  {
    path: '/datarequest',
    name: 'DataRequest',
    component: DataRequestForm,
    meta:{
      title: '数据提取申请'
    }
  },
  {
    path: '/requestmanagement',
    name: 'RequestManagement',
    component: RequestManagement,
    meta:{
      title: '申请管理',
      requiresAdmin: true,
      requiresDataProcessor: true
    }
  },
  {
    path: '/admin/users',
    name: 'UserManagement',
    component: UserManagement,
    meta: {
      title: '用户管理',
      requiresAdmin: true,
      requiresDataProcessor: true
    }
  },
  {
    path: '/file-management',
    name: 'FileManagement',
    component: FileManagement,
    meta: {
      title: '文件系统',
      requiresAdmin: true,
      requiresDataProcessor: true
    }
  },
  {
    path: '/notice',
    name: 'Notice',
    component: () => import('@/components/admin/NoticeBoard.vue'),
    meta: {
      title: '通知公告'
    }
  },
  {
    path: '/docs',
    name: 'Docs',
    component: () => import('@/components/admin/docs')
  }
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
});

router.beforeEach((to, from, next) => {
  const userRole = localStorage.getItem('userRole')
  const username = localStorage.getItem("username")



  // 我希望未登录时，跳转到登录页面
  if (to.path !== '/login' && username === null) {
    next('/login')
    return
  }

// 检查路由是否需要权限
  if (to.meta.requiresAdmin && userRole !== 'admin') {
    if (to.meta.requiresDataProcessor && userRole === 'dataProcessor'){
      next();
      return
    }
    if(to.path === '/workspace' && userRole === 'requestProcessor'){
      next('/myrequests');
      return
    }
    if (to.meta.requestProcessor && userRole === 'requestProcessor'){
      next();
      return
    }
    next('/'); // 如果不是管理员，重定向到首页
    return
  }
  if (to.meta.requiresDataProcessor && !['admin', 'dataProcessor'].includes(userRole)) {
    next('/') ;// 如果不是数据处理人员或管理员，重定向到首页
    return
  }

  if (to.meta.title) {
    document.title = to.meta.title
  }
  next()
})

export default router;