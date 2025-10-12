<template>
  <div class="dashboard-content">
    <div class="mb-4">
      <h1>欢迎回来，{{ currentUser }}</h1>
      <p>今天是 {{ currentDate }}</p>
    </div>

        <!-- 数据卡片 -->
        <div class="row mb-4">
          <div class="col-md-3">
            <el-card class="h-100 bg-primary text-white">
              <div class="card-content">
                <h3 class="card-title">业主总数</h3>
                <p class="card-value">{{ ownerCount }}</p>
              </div>
            </el-card>
          </div>
          <div class="col-md-3">
            <el-card class="h-100 bg-success text-white">
              <div class="card-content">
                <h3 class="card-title">待处理维修</h3>
                <p class="card-value">{{ pendingMaintenanceCount }}</p>
              </div>
            </el-card>
          </div>
          <div class="col-md-3">
            <el-card class="h-100 bg-warning text-white">
              <div class="card-content">
                <h3 class="card-title">未支付费用</h3>
                <p class="card-value">{{ unpaidPaymentCount }}</p>
              </div>
            </el-card>
          </div>
          <div class="col-md-3">
            <el-card class="h-100 bg-info text-white">
              <div class="card-content">
                <h3 class="card-title">最新公告</h3>
                <p class="card-value">{{ latestAnnouncementCount }}</p>
              </div>
            </el-card>
          </div>
        </div>

        <!-- 最近活动 -->
        <div class="mb-4">
          <h2>最近活动</h2>
          <el-table :data="recentActivities" style="width: 100%">
            <el-table-column prop="time" label="时间" width="180" />
            <el-table-column prop="activity" label="活动" />
            <el-table-column prop="user" label="操作用户" width="120" />
            <el-table-column prop="status" label="状态" width="100">
              <template #default="scope">
                <el-tag :type="getStatusType(scope.row.status)">{{ scope.row.status }}</el-tag>
              </template>
            </el-table-column>
          </el-table>
        </div>

        <!-- 快捷操作 -->
        <div>
          <h2>快捷操作</h2>
          <div class="row">
            <div class="col-md-2">
              <el-button type="primary" icon="el-icon-plus" class="w-100" @click="$router.push({ name: 'owners' })" >
                添加业主
              </el-button>
            </div>
            <div class="col-md-2">
              <el-button type="success" icon="el-icon-plus" class="w-100" @click="$router.push({ name: 'announcements' })" >
                发布公告
              </el-button>
            </div>
            <div class="col-md-2">
              <el-button type="warning" icon="el-icon-search" class="w-100" @click="$router.push({ name: 'maintenance' })" >
                查看维修
              </el-button>
            </div>
            <div class="col-md-2">
              <el-button type="info" icon="el-icon-search" class="w-100" @click="$router.push({ name: 'payments' })" >
                查看费用
              </el-button>
            </div>
          </div>
        </div>
  </div>
</template>

<script>
export default {
  name: 'DashboardView',
  components: {
  },
  data() {
    return {
      currentUser: '管理员',
      userAvatar: 'https://randomuser.me/api/portraits/men/32.jpg',
      ownerCount: 0,
      pendingMaintenanceCount: 0,
      unpaidPaymentCount: 0,
      latestAnnouncementCount: 0,
      recentActivities: [],
      currentDate: ''
    }
  },
  // 监听路由变化，确保在进入页面时重新加载数据
  watch: {
    $route: {
      handler() {
        // 强制重新加载数据
        this.setCurrentDate()
        this.loadMockData()
        
        // 确保DOM更新后内容可见
        this.$nextTick(() => {
          // 可选：添加一些日志或调试信息
          console.log('Dashboard data reloaded')
        })
      },
      immediate: true
    }
  },
  mounted() {
    // 设置当前日期
    this.setCurrentDate()
    
    // 加载模拟数据
    this.loadMockData()
  },
  
  // 当组件被keep-alive缓存后再次激活时触发
  activated() {
    // 重新加载数据，确保在路由切换回来时内容正确显示
    this.setCurrentDate()
    this.loadMockData()
  },
  methods: {
    setCurrentDate() {
      const now = new Date()
      this.currentDate = now.toLocaleDateString('zh-CN', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        weekday: 'long'
      })
    },
    
    loadMockData() {
      // 模拟统计数据
      this.ownerCount = 156
      this.pendingMaintenanceCount = 8
      this.unpaidPaymentCount = 12
      this.latestAnnouncementCount = 3
      
      // 模拟最近活动数据
      this.recentActivities = [
        {
          time: '2024-05-20 10:30',
          activity: '添加新业主',
          user: '管理员',
          status: '完成'
        },
        {
          time: '2024-05-20 09:15',
          activity: '处理维修请求 #123',
          user: '维修员',
          status: '进行中'
        },
        {
          time: '2024-05-19 16:45',
          activity: '发布公告',
          user: '管理员',
          status: '完成'
        },
        {
          time: '2024-05-19 14:20',
          activity: '收取物业费',
          user: '财务',
          status: '完成'
        }
      ]
    },
    
    getStatusType(status) {
      switch (status) {
        case '完成':
          return 'success'
        case '进行中':
          return 'warning'
        case '待处理':
          return 'info'
        default:
          return 'default'
      }
    }
  }
}
</script>

<style scoped>
.dashboard-content {
  padding: 20px 0;
}

/* 欢迎信息样式 */
.dashboard-content h1 {
  font-size: 28px;
  color: #333333;
  margin-bottom: 8px;
}

.dashboard-content p {
  color: #606266;
  font-size: 16px;
}

.card-content {
  text-align: center;
  padding: 20px;
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
}

.card-content:hover {
  box-shadow: 0 4px 16px 0 rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.card-title {
  font-size: 16px;
  margin-bottom: 10px;
  color: #606266;
}

.card-value {
  font-size: 32px;
  font-weight: bold;
  color: var(--primary-color);
  margin: 10px 0;
}

/* 按钮样式 */
.el-button {
  border-radius: 4px;
}

.el-button--primary {
  background-color: var(--primary-color);
  border-color: var(--primary-color);
}

.el-button--primary:hover {
  background-color: var(--primary-hover-color);
  border-color: var(--primary-hover-color);
}

/* 表格样式 */
.el-table {
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
}

/* 菜单项激活状态 */
.el-menu-item.is-active {
  background-color: var(--primary-color) !important;
  color: #fff !important;
}
</style>