<template>
  <div class="app-container">
    <!-- 侧边栏 -->
    <aside class="sidebar" :class="{ 'collapsed': !sidebarOpen && window.innerWidth >= 768, 'hidden': !sidebarOpen && window.innerWidth < 768 }" v-if="isLoggedIn">
      <div class="logo-container">
        <img src="/vite.svg" alt="Logo" class="logo" />
        <h1 class="system-title">物业管理系统</h1>
      </div>
      <el-menu
        default-active="/"
        class="el-menu-vertical-demo"
        router
      >
        <el-menu-item index="/">
          <i class="el-icon-s-home"></i>
          <span>仪表盘</span>
        </el-menu-item>
        <el-sub-menu index="1">
          <template #title>
            <i class="el-icon-user"></i>
            <span>用户管理</span>
          </template>
          <el-menu-item index="/users">用户列表</el-menu-item>
          <el-menu-item index="/owners">业主管理</el-menu-item>
        </el-sub-menu>
        <el-menu-item index="/properties">
          <i class="el-icon-building"></i>
          <span>物业信息</span>
        </el-menu-item>
        <el-menu-item index="/maintenance">
          <i class="el-icon-s-tools"></i>
          <span>维修管理</span>
        </el-menu-item>
        <el-menu-item index="/announcements">
          <i class="el-icon-bell"></i>
          <span>公告管理</span>
        </el-menu-item>
        <el-menu-item index="/payments">
          <i class="el-icon-money"></i>
          <span>支付管理</span>
        </el-menu-item>
        <el-menu-item index="/settings">
          <i class="el-icon-setting"></i>
          <span>系统设置</span>
        </el-menu-item>
      </el-menu>
      <!-- 用户信息区域已移除 -->
    </aside>

    <!-- 主内容区域 -->
    <main class="main-content" :class="{ 
      'logged-in': isLoggedIn, 
      'sidebar-collapsed': isLoggedIn && !sidebarOpen && window.innerWidth >= 768,
      'sidebar-hidden': isLoggedIn && !sidebarOpen && window.innerWidth < 768
    }">
      <!-- 顶部导航栏 -->
      <header class="main-header" v-if="isLoggedIn">
        <div class="header-left">
          <el-button type="text" icon="el-icon-menu" @click="toggleSidebar" class="sidebar-toggle" />
          <h2 class="page-title">{{ pageTitle }}</h2>
        </div>
        <div class="header-right">
          <el-dropdown>
            <span class="el-dropdown-link">
              <el-avatar class="user-avatar" style="cursor: pointer;">{{ userName.charAt(0).toUpperCase() }}</el-avatar>
            </span>
            <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item @click="handleLogout">退出登录</el-dropdown-item>
                </el-dropdown-menu>
              </template>
          </el-dropdown>
        </div>
      </header>

      <!-- 页面内容 -->
      <div class="content-wrapper">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <!-- 使用路由路径作为key，确保每次路由切换时重新创建组件 -->
            <component :is="Component" :key="$route.path" />
          </transition>
        </router-view>
      </div>
    </main>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      isLoggedIn: false,
      userName: '管理员',
      pageTitle: '仪表盘',
      notificationCount: 3,
      sidebarOpen: true
    }
  },
  watch: {
    // 监听路由变化，更新页面标题
    $route: {
      handler(to) {
        // 使用路径而不是组件名称来更新页面标题，确保路由匹配准确性
        this.updatePageTitleByPath(to.path)
        
        // 检查用户是否已登录
        const token = localStorage.getItem('token')
        this.isLoggedIn = !!token
        
        // 如果用户未登录且访问的不是登录页面，则重定向到登录页面
        if (!this.isLoggedIn && to.path !== '/login') {
          this.$router.replace('/login')
        }
        // 如果用户已登录且访问的是登录页面，则重定向到仪表盘
        else if (this.isLoggedIn && to.path === '/login') {
          this.$router.replace('/dashboard')
        }
      },
      immediate: true
    }
  },
  mounted() {
    // 检查用户是否已登录
    const token = localStorage.getItem('token')
    this.isLoggedIn = !!token
    
    // 如果用户已登录且访问的是登录页面，则重定向到仪表盘
    if (this.isLoggedIn && this.$route.path === '/login') {
      this.$router.replace('/dashboard')
    }
    
    // 监听窗口大小变化，在小屏幕上自动折叠侧边栏
    window.addEventListener('resize', this.handleResize)
    this.handleResize()
  },
  beforeUnmount() {
    window.removeEventListener('resize', this.handleResize)
  },
  methods: {
    // 更新页面标题
    updatePageTitle(pageName) {
      switch (pageName) {
        case 'DashboardView':
          this.pageTitle = '仪表盘'
          break
        case 'LoginView':
          this.pageTitle = '登录'
          break
        case 'UserManagementView':
          this.pageTitle = '用户管理'
          break
        case 'OwnerManagementView':
          this.pageTitle = '业主管理'
          break
        case 'PropertyManagementView':
          this.pageTitle = '物业信息'
          break
        case 'MaintenanceRequestView':
          this.pageTitle = '维修管理'
          break
        case 'AnnouncementView':
          this.pageTitle = '公告管理'
          break
        case 'PaymentManagementView':
          this.pageTitle = '支付管理'
          break
        case 'SystemSettingsView':
          this.pageTitle = '系统设置'
          break
        default:
          this.pageTitle = '仪表盘'
      }
    },
      
      // 根据路径更新页面标题
      updatePageTitleByPath(path) {
        switch (path) {
          case '/':
          case '/dashboard':
            this.pageTitle = '仪表盘'
            break
          case '/login':
            this.pageTitle = '登录'
            break
          case '/users':
            this.pageTitle = '用户管理'
            break
          case '/owners':
            this.pageTitle = '业主管理'
            break
          case '/properties':
            this.pageTitle = '物业信息'
            break
          case '/maintenance':
            this.pageTitle = '维修管理'
            break
          case '/announcements':
            this.pageTitle = '公告管理'
            break
          case '/payments':
            this.pageTitle = '支付管理'
            break
          case '/settings':
            this.pageTitle = '系统设置'
            break
          default:
            this.pageTitle = '仪表盘'
        }
      },
      
      // 切换侧边栏显示/隐藏
      toggleSidebar() {
        this.sidebarOpen = !this.sidebarOpen
      },
      
      // 处理窗口大小变化
      handleResize() {
        if (window.innerWidth < 768) {
          this.sidebarOpen = false
        } else {
          this.sidebarOpen = true
        }
      },
      
      // 退出登录
      handleLogout() {
      // 清除本地存储中的token
      localStorage.removeItem('token')
      localStorage.removeItem('userInfo')
      
      // 更新登录状态
      this.isLoggedIn = false
      
      // 重定向到登录页面
      this.$router.replace('/login')
      
      this.$message.success('退出登录成功')
    },
    
    // 跳转到个人资料页面
    gotoProfile() {
      // 在实际应用中，这里应该跳转到个人资料页面
      this.$message.info('个人资料页面暂未实现')
    },
    
    // 跳转到系统设置页面
    gotoSettings() {
      this.$router.push('/settings')
    }
  }
}
</script>

<style>
/* 全局样式 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background-color: #f5f5f5;
  margin: 0;
  padding: 0;
}

/* 应用容器 */
.app-container {
  display: flex;
  height: 100vh;
  overflow: hidden;
}

/* 侧边栏样式 */
.sidebar {
  width: 240px;
  background-color: #ffffff;
  color: #333333;
  height: 100vh;
  position: fixed;
  left: 0;
  top: 0;
  z-index: 1000;
  transition: width 0.3s ease, transform 0.3s ease;
  overflow-y: auto;
  border-right: 1px solid var(--border-color);
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
}

.sidebar.collapsed {
  width: 56px;
}

.sidebar.hidden {
  transform: translateX(-100%);
}

.logo-container {
  padding: 20px;
  text-align: center;
  border-bottom: 1px solid var(--border-color);
  background-color: #ffffff;
}

.logo {
  width: 48px;
  height: 48px;
  margin-bottom: 10px;
}

.system-title {
  font-size: 18px;
  font-weight: 600;
  color: #333333;
}

.el-menu-vertical-demo {
  background-color: #ffffff;
  border-right: none;
}

.el-menu-vertical-demo .el-menu-item,
.el-menu-vertical-demo .el-submenu__title {
  color: #606266;
  height: 50px;
  line-height: 50px;
  border-bottom: 1px solid var(--border-color);
}

.el-menu-vertical-demo .el-menu-item:hover,
.el-menu-vertical-demo .el-submenu__title:hover {
  background-color: #ecf5ff;
  color: var(--primary-color);
}

.el-menu-vertical-demo .el-menu-item.is-active {
  background-color: var(--primary-color);
  color: #fff;
}

.el-menu-vertical-demo .el-submenu {
  background-color: #ffffff;
}

.el-menu-vertical-demo .el-submenu .el-menu {
  background-color: #ffffff;
  border-left: 3px solid var(--primary-color);
}

.user-info {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 15px;
  border-top: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  gap: 10px;
  background-color: #ffffff;
}

.user-name {
  flex: 1;
  font-size: 14px;
}

.logout-btn {
  color: #ecf0f1;
  font-size: 12px;
}

/* 主内容区域样式 */
.main-content {
  flex: 1;
  transition: all 0.3s ease;
  overflow-y: auto;
  height: 100vh;
}

.main-content.logged-in {
  margin-left: 240px;
}

.main-content.sidebar-collapsed {
  margin-left: 56px;
}

.main-content.sidebar-hidden {
  margin-left: 0;
}

/* 顶部导航栏样式 */
.main-header {
  height: 60px;
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  position: fixed;
  top: 0;
  right: 0;
  left: 240px;
  z-index: 999;
  transition: left 0.3s ease;
}

.sidebar-collapsed .main-header {
  left: 56px;
}

.sidebar-hidden .main-header {
  left: 0;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 15px;
}

.sidebar-toggle {
  display: none;
}

.page-title {
  font-size: 20px;
  font-weight: 500;
  color: #333;
  margin: 0;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 15px;
}

.notification-badge {
  position: relative;
}

.user-avatar {
  cursor: pointer;
}

/* 内容包装器 */
.content-wrapper {
  padding: 80px 20px 20px;
  min-height: 100vh;
  background-color: #f5f5f5;
}

/* 过渡动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .sidebar {
    width: 0;
    overflow: hidden;
  }
  
  .main-content.logged-in {
    margin-left: 0;
  }
  
  .main-header {
    left: 0;
  }
  
  .sidebar-toggle {
    display: block;
  }
}
</style>
