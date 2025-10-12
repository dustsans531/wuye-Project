<template>
  <div class="user-management-container">
    <!-- 顶部操作栏 -->
    <div class="operation-bar mb-4 d-flex justify-content-between items-center">
      <h1>用户管理</h1>
      <el-button type="primary" icon="el-icon-plus" @click="handleAddUser">
        添加用户
      </el-button>
    </div>

    <!-- 搜索和过滤 -->
    <div class="search-filter mb-4">
      <el-row :gutter="20">
        <el-col :span="6">
          <el-input
            v-model="searchKeyword"
            placeholder="搜索用户名或邮箱"
            clearable
            suffix-icon="el-icon-search"
            @keyup.enter="handleSearch"
          />
        </el-col>
        <el-col :span="4">
          <el-select v-model="roleFilter" placeholder="角色筛选" clearable>
            <el-option label="所有角色" value="" />
            <el-option label="管理员" value="admin" />
            <el-option label="经理" value="manager" />
            <el-option label="员工" value="staff" />
            <el-option label="普通用户" value="user" />
          </el-select>
        </el-col>
        <el-col :span="4">
          <el-select v-model="statusFilter" placeholder="状态筛选" clearable>
            <el-option label="所有状态" value="" />
            <el-option label="启用" value="true" />
            <el-option label="禁用" value="false" />
          </el-select>
        </el-col>
        <el-col :span="4">
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="resetFilters">重置</el-button>
        </el-col>
      </el-row>
    </div>

    <!-- 用户表格 -->
    <el-table :data="usersData" style="width: 100%">
      <el-table-column type="index" width="50" />
      <el-table-column prop="username" label="用户名" width="180" />
      <el-table-column prop="email" label="邮箱" width="240" />
      <el-table-column prop="role" label="角色" width="120">
        <template #default="scope">
          <el-tag :type="getRoleType(scope.row.role)">{{ scope.row.role }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="created_at" label="创建时间" width="180">
        <template #default="scope">
          {{ formatDate(scope.row.created_at) }}
        </template>
      </el-table-column>
      <el-table-column prop="active" label="状态" width="100">
        <template #default="scope">
          <el-switch v-model="scope.row.active" @change="handleStatusChange(scope.row)" />
        </template>
      </el-table-column>
      <el-table-column label="操作" width="180" fixed="right">
        <template #default="scope">
          <el-button type="primary" size="small" @click="handleEditUser(scope.row)">
            编辑
          </el-button>
          <el-popconfirm
            title="确定要删除此用户吗？"
            confirm-button-text="确定"
            cancel-button-text="取消"
            @confirm="handleDeleteUser(scope.row.id)"
          >
            <template #reference>
              <el-button type="danger" size="small">
                删除
              </el-button>
            </template>
          </el-popconfirm>
        </template>
      </el-table-column>
    </el-table>

    <!-- 分页 -->
    <div class="pagination mt-4 d-flex justify-content-center">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :page-sizes="[10, 20, 50, 100]"
        layout="total, sizes, prev, pager, next, jumper"
        :total="totalUsers"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>

    <!-- 添加/编辑用户对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑用户' : '添加用户'"
      width="500px"
    >
      <el-form :model="userForm" :rules="userRules" ref="userFormRef" label-width="80px">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="userForm.username" placeholder="请输入用户名" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="userForm.email" placeholder="请输入邮箱" />
        </el-form-item>
        <el-form-item v-if="!isEdit" label="密码" prop="password">
          <el-input v-model="userForm.password" type="password" placeholder="请输入密码" />
        </el-form-item>
        <el-form-item label="角色" prop="role">
          <el-select v-model="userForm.role" placeholder="请选择角色">
            <el-option label="管理员" value="admin" />
            <el-option label="经理" value="manager" />
            <el-option label="员工" value="staff" />
            <el-option label="普通用户" value="user" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: 'UserManagementView',
  data() {
    return {
      usersData: [],
      totalUsers: 0,
      currentPage: 1,
      pageSize: 10,
      searchKeyword: '',
      roleFilter: '',
      statusFilter: '',
      dialogVisible: false,
      isEdit: false,
      userForm: {
        id: '',
        username: '',
        email: '',
        password: '',
        role: 'user',
        active: true
      },
      userRules: {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' },
          { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' }
        ],
        email: [
          { required: true, message: '请输入邮箱', trigger: 'blur' },
          { type: 'email', message: '请输入有效的邮箱地址', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          { min: 6, message: '密码长度不能少于6位', trigger: 'blur' }
        ],
        role: [
          { required: true, message: '请选择角色', trigger: 'change' }
        ]
      }
    }
  },
  mounted() {
    // 加载用户数据
    this.loadUsersData()
  },
  methods: {
    // 加载用户数据
    loadUsersData() {
      // 在实际应用中，这里应该发送请求到后端获取用户数据
      // 这里使用模拟数据
      this.usersData = [
        {
          id: 1,
          username: 'admin',
          email: 'admin@example.com',
          role: 'admin',
          created_at: '2024-05-01T10:00:00',
          active: true
        },
        {
          id: 2,
          username: 'manager1',
          email: 'manager1@example.com',
          role: 'manager',
          created_at: '2024-05-02T11:30:00',
          active: true
        },
        {
          id: 3,
          username: 'staff1',
          email: 'staff1@example.com',
          role: 'staff',
          created_at: '2024-05-03T09:15:00',
          active: true
        },
        {
          id: 4,
          username: 'user1',
          email: 'user1@example.com',
          role: 'user',
          created_at: '2024-05-04T14:45:00',
          active: true
        }
      ]
      this.totalUsers = this.usersData.length
    },
    
    // 根据角色获取标签类型
    getRoleType(role) {
      switch (role) {
        case 'admin':
          return 'danger'
        case 'manager':
          return 'warning'
        case 'staff':
          return 'info'
        default:
          return 'primary'
      }
    },
    
    // 格式化日期
    formatDate(dateString) {
      const date = new Date(dateString)
      return date.toLocaleString('zh-CN')
    },
    
    // 搜索用户
    handleSearch() {
      // 在实际应用中，这里应该发送请求到后端搜索用户
      // 这里简单模拟搜索
      let filteredUsers = [...this.usersData]
      
      if (this.searchKeyword) {
        filteredUsers = filteredUsers.filter(user => 
          user.username.includes(this.searchKeyword) || 
          user.email.includes(this.searchKeyword)
        )
      }
      
      if (this.roleFilter) {
        filteredUsers = filteredUsers.filter(user => user.role === this.roleFilter)
      }
      
      if (this.statusFilter !== '') {
        filteredUsers = filteredUsers.filter(user => 
          user.active.toString() === this.statusFilter
        )
      }
      
      this.usersData = filteredUsers
      this.totalUsers = filteredUsers.length
      this.currentPage = 1
    },
    
    // 重置筛选条件
    resetFilters() {
      this.searchKeyword = ''
      this.roleFilter = ''
      this.statusFilter = ''
      this.loadUsersData()
    },
    
    // 分页大小变化
    handleSizeChange(size) {
      this.pageSize = size
      this.loadUsersData()
    },
    
    // 当前页变化
    handleCurrentChange(current) {
      this.currentPage = current
      this.loadUsersData()
    },
    
    // 更改用户状态
    handleStatusChange(row) {
      // 在实际应用中，这里应该发送请求到后端更新用户状态
      this.$message.success('用户状态已更新')
    },
    
    // 添加用户
    handleAddUser() {
      this.isEdit = false
      this.userForm = {
        id: '',
        username: '',
        email: '',
        password: '',
        role: 'user',
        active: true
      }
      this.dialogVisible = true
    },
    
    // 编辑用户
    handleEditUser(row) {
      this.isEdit = true
      this.userForm = { ...row }
      this.dialogVisible = true
    },
    
    // 删除用户
    handleDeleteUser(id) {
      // 在实际应用中，这里应该发送请求到后端删除用户
      this.usersData = this.usersData.filter(user => user.id !== id)
      this.totalUsers = this.usersData.length
      this.$message.success('用户已删除')
    },
    
    // 提交表单
    handleSubmit() {
      this.$refs.userFormRef.validate((valid) => {
        if (valid) {
          // 在实际应用中，这里应该发送请求到后端保存用户数据
          if (this.isEdit) {
            // 编辑用户
            const index = this.usersData.findIndex(user => user.id === this.userForm.id)
            if (index !== -1) {
              this.usersData[index] = { ...this.userForm }
            }
            this.$message.success('用户信息已更新')
          } else {
            // 添加用户
            const newUser = {
              ...this.userForm,
              id: Date.now(),
              created_at: new Date().toISOString()
            }
            this.usersData.unshift(newUser)
            this.totalUsers++
            this.$message.success('用户添加成功')
          }
          
          this.dialogVisible = false
        }
      })
    }
  }
}
</script>

<style scoped>
.user-management-container {
  padding: 20px;
}

.operation-bar {
  margin-bottom: 20px;
}

.search-filter {
  margin-bottom: 20px;
}

.pagination {
  margin-top: 20px;
}
</style>