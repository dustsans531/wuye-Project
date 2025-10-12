// 导入Vue Router
import { createRouter, createWebHistory } from 'vue-router'

// 导入组件
import LoginView from '../views/LoginView.vue'
import DashboardView from '../views/DashboardView.vue'
import UserManagementView from '../views/UserManagementView.vue'
import PropertyManagementView from '../views/PropertyManagementView.vue'
import OwnerManagementView from '../views/OwnerManagementView.vue'
import MaintenanceRequestView from '../views/MaintenanceRequestView.vue'
import PaymentManagementView from '../views/PaymentManagementView.vue'
import AnnouncementView from '../views/AnnouncementView.vue'
import SystemSettingsView from '../views/SystemSettingsView.vue'

// 路由配置
const routes = [
  {
    path: '/login',
    name: 'login',
    component: LoginView,
    meta: { requiresAuth: false }
  },
  {
    path: '/',
    name: 'dashboard',
    component: DashboardView,
    meta: { requiresAuth: true }
  },
  {
    path: '/users',
    name: 'users',
    component: UserManagementView,
    meta: { requiresAuth: true }
  },
  {
    path: '/properties',
    name: 'properties',
    component: PropertyManagementView,
    meta: { requiresAuth: true }
  },
  {
    path: '/owners',
    name: 'owners',
    component: OwnerManagementView,
    meta: { requiresAuth: true }
  },
  {    path: '/maintenance',    name: 'maintenance',    component: MaintenanceRequestView,    meta: { requiresAuth: true }  },
  {    path: '/payments',    name: 'payments',    component: PaymentManagementView,    meta: { requiresAuth: true }  },
  {    path: '/announcements',    name: 'announcements',    component: AnnouncementView,    meta: { requiresAuth: true }  },
  {    path: '/settings',    name: 'settings',    component: SystemSettingsView,    meta: { requiresAuth: true }  }
]

// 创建路由实例
const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem('token')
  
  if (to.meta.requiresAuth && !isAuthenticated) {
    // 需要认证但未登录，跳转到登录页
    next({ name: 'login' })
  } else if (to.name === 'login' && isAuthenticated) {
    // 已登录但尝试访问登录页，跳转到首页
    next({ name: 'dashboard' })
  } else {
    // 其他情况正常通过
    next()
  }
})

export default router