<template>
  <div class="maintenance-request-container">
    <!-- 顶部操作栏 -->
    <div class="operation-bar mb-4 d-flex justify-content-between items-center">
      <h1>维修请求管理</h1>
      <div>
        <el-button type="primary" icon="el-icon-plus" @click="handleAddRequest">
          添加维修请求
        </el-button>
        <el-button type="info" icon="el-icon-refresh-left" @click="exportRequests">
          导出数据
        </el-button>
      </div>
    </div>

    <!-- 搜索和过滤 -->
    <div class="search-filter mb-4">
      <el-row :gutter="20">
        <el-col :span="6">
          <el-input
            v-model="searchKeyword"
            placeholder="搜索业主姓名或请求描述"
            clearable
            suffix-icon="el-icon-search"
            @keyup.enter="handleSearch"
          />
        </el-col>
        <el-col :span="4">
          <el-select v-model="propertyFilter" placeholder="所属物业" clearable>
            <el-option label="所有物业" value="" />
            <el-option v-for="property in properties" :key="property.id" :label="property.name" :value="property.id" />
          </el-select>
        </el-col>
        <el-col :span="4">
          <el-select v-model="statusFilter" placeholder="状态筛选" clearable>
            <el-option label="所有状态" value="" />
            <el-option label="待处理" value="pending" />
            <el-option label="处理中" value="in_progress" />
            <el-option label="已完成" value="completed" />
            <el-option label="已取消" value="cancelled" />
          </el-select>
        </el-col>
        <el-col :span="4">
          <el-date-picker
            v-model="dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            value-format="YYYY-MM-DD"
          />
        </el-col>
        <el-col :span="4">
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="resetFilters">重置</el-button>
        </el-col>
      </el-row>
    </div>

    <!-- 维修请求表格 -->
    <el-table :data="requestsData" style="width: 100%">
      <el-table-column type="index" width="50" />
      <el-table-column prop="owner_name" label="业主姓名" width="120" />
      <el-table-column prop="property_name" label="所属物业" width="180" />
      <el-table-column prop="unit_number" label="单元号" width="100" />
      <el-table-column prop="house_number" label="房号" width="100" />
      <el-table-column prop="request_type" label="维修类型" width="120">
        <template #default="scope">
          <el-tag :type="getTypeTag(scope.row.request_type)">{{ getTypeLabel(scope.row.request_type) }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="description" label="请求描述" />
      <el-table-column prop="status" label="状态" width="120">
        <template #default="scope">
          <el-tag :type="getStatusTag(scope.row.status)">{{ getStatusLabel(scope.row.status) }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="created_at" label="创建时间" width="180" />
      <el-table-column prop="updated_at" label="更新时间" width="180" />
      <el-table-column label="操作" width="220" fixed="right">
        <template #default="scope">
          <el-button type="primary" size="small" @click="handleEditRequest(scope.row)">
            编辑
          </el-button>
          <el-button type="info" size="small" @click="handleViewDetails(scope.row)">
            详情
          </el-button>
          <el-button
            type="success"
            size="small"
            @click="handleCompleteRequest(scope.row)"
            :disabled="scope.row.status !== 'pending' && scope.row.status !== 'in_progress'"
          >
            完成
          </el-button>
          <el-popconfirm
            title="确定要删除此维修请求吗？"
            confirm-button-text="确定"
            cancel-button-text="取消"
            @confirm="handleDeleteRequest(scope.row.id)"
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
        :total="totalRequests"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>

    <!-- 添加/编辑维修请求对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑维修请求' : '添加维修请求'"
      width="700px"
    >
      <el-form :model="requestForm" :rules="requestRules" ref="requestFormRef" label-width="100px">
        <el-form-item label="业主姓名" prop="owner_name">
          <el-input v-model="requestForm.owner_name" placeholder="请输入业主姓名" />
        </el-form-item>
        <el-form-item label="联系电话" prop="phone">
          <el-input v-model="requestForm.phone" placeholder="请输入联系电话" />
        </el-form-item>
        <el-form-item label="所属物业" prop="property_id">
          <el-select v-model="requestForm.property_id" placeholder="请选择所属物业">
            <el-option v-for="property in properties" :key="property.id" :label="property.name" :value="property.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="单元号" prop="unit_number">
          <el-input v-model="requestForm.unit_number" placeholder="请输入单元号" />
        </el-form-item>
        <el-form-item label="房号" prop="house_number">
          <el-input v-model="requestForm.house_number" placeholder="请输入房号" />
        </el-form-item>
        <el-form-item label="维修类型" prop="request_type">
          <el-select v-model="requestForm.request_type" placeholder="请选择维修类型">
            <el-option label="水电维修" value="water_electric" />
            <el-option label="管道维修" value="plumbing" />
            <el-option label="家电维修" value="appliance" />
            <el-option label="门窗维修" value="door_window" />
            <el-option label="其他" value="other" />
          </el-select>
        </el-form-item>
        <el-form-item label="请求描述" prop="description">
          <el-input v-model="requestForm.description" type="textarea" placeholder="请输入维修请求描述" />
        </el-form-item>
        <el-form-item label="紧急程度" prop="priority">
          <el-radio-group v-model="requestForm.priority">
            <el-radio label="low">低</el-radio>
            <el-radio label="medium">中</el-radio>
            <el-radio label="high">高</el-radio>
            <el-radio label="urgent">紧急</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="状态" prop="status" v-if="isEdit">
          <el-select v-model="requestForm.status" placeholder="请选择状态">
            <el-option label="待处理" value="pending" />
            <el-option label="处理中" value="in_progress" />
            <el-option label="已完成" value="completed" />
            <el-option label="已取消" value="cancelled" />
          </el-select>
        </el-form-item>
        <el-form-item label="维修人员" prop="maintenance_staff" v-if="isEdit">
          <el-input v-model="requestForm.maintenance_staff" placeholder="请输入维修人员姓名" />
        </el-form-item>
        <el-form-item label="维修记录" prop="maintenance_notes" v-if="isEdit">
          <el-input v-model="requestForm.maintenance_notes" type="textarea" placeholder="请输入维修记录" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>

    <!-- 维修请求详情对话框 -->
    <el-dialog
      v-model="detailDialogVisible"
      title="维修请求详情"
      width="600px"
    >
      <div v-if="selectedRequest">
        <el-descriptions :column="1" border>
          <el-descriptions-item label="业主姓名">{{ selectedRequest.owner_name }}</el-descriptions-item>
          <el-descriptions-item label="联系电话">{{ selectedRequest.phone }}</el-descriptions-item>
          <el-descriptions-item label="所属物业">{{ selectedRequest.property_name }}</el-descriptions-item>
          <el-descriptions-item label="单元号">{{ selectedRequest.unit_number }}</el-descriptions-item>
          <el-descriptions-item label="房号">{{ selectedRequest.house_number }}</el-descriptions-item>
          <el-descriptions-item label="维修类型"><el-tag :type="getTypeTag(selectedRequest.request_type)">{{ getTypeLabel(selectedRequest.request_type) }}</el-tag></el-descriptions-item>
          <el-descriptions-item label="请求描述">{{ selectedRequest.description }}</el-descriptions-item>
          <el-descriptions-item label="紧急程度">{{ getPriorityLabel(selectedRequest.priority) }}</el-descriptions-item>
          <el-descriptions-item label="状态"><el-tag :type="getStatusTag(selectedRequest.status)">{{ getStatusLabel(selectedRequest.status) }}</el-tag></el-descriptions-item>
          <el-descriptions-item label="维修人员" v-if="selectedRequest.maintenance_staff">{{ selectedRequest.maintenance_staff }}</el-descriptions-item>
          <el-descriptions-item label="维修记录" v-if="selectedRequest.maintenance_notes">{{ selectedRequest.maintenance_notes }}</el-descriptions-item>
          <el-descriptions-item label="创建时间">{{ selectedRequest.created_at }}</el-descriptions-item>
          <el-descriptions-item label="更新时间">{{ selectedRequest.updated_at }}</el-descriptions-item>
        </el-descriptions>
      </div>
      <template #footer>
        <el-button @click="detailDialogVisible = false">关闭</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: 'MaintenanceRequestView',
  data() {
    return {
      requestsData: [],
      properties: [],
      totalRequests: 0,
      currentPage: 1,
      pageSize: 10,
      searchKeyword: '',
      propertyFilter: '',
      statusFilter: '',
      dateRange: [],
      dialogVisible: false,
      detailDialogVisible: false,
      isEdit: false,
      selectedRequest: null,
      requestForm: {
        id: '',
        owner_name: '',
        phone: '',
        property_id: '',
        property_name: '',
        unit_number: '',
        house_number: '',
        request_type: 'water_electric',
        description: '',
        priority: 'medium',
        status: 'pending',
        maintenance_staff: '',
        maintenance_notes: '',
        created_at: '',
        updated_at: ''
      },
      requestRules: {
        owner_name: [
          { required: true, message: '请输入业主姓名', trigger: 'blur' }
        ],
        phone: [
          { required: true, message: '请输入联系电话', trigger: 'blur' },
          { pattern: /^1[3-9]\d{9}$/, message: '请输入有效的手机号码', trigger: 'blur' }
        ],
        property_id: [
          { required: true, message: '请选择所属物业', trigger: 'change' }
        ],
        unit_number: [
          { required: true, message: '请输入单元号', trigger: 'blur' }
        ],
        house_number: [
          { required: true, message: '请输入房号', trigger: 'blur' }
        ],
        request_type: [
          { required: true, message: '请选择维修类型', trigger: 'change' }
        ],
        description: [
          { required: true, message: '请输入维修请求描述', trigger: 'blur' }
        ]
      }
    }
  },
  mounted() {
    // 加载维修请求数据
    this.loadRequestsData()
    // 加载物业数据用于下拉选择
    this.loadPropertiesData()
  },
  methods: {
    // 加载维修请求数据
    loadRequestsData() {
      // 在实际应用中，这里应该发送请求到后端获取维修请求数据
      // 这里使用模拟数据
      this.requestsData = [
        {
          id: 1,
          owner_name: '张明',
          phone: '13800138001',
          property_id: 1,
          property_name: '阳光花园小区',
          unit_number: '1',
          house_number: '101',
          request_type: 'water_electric',
          description: '厨房水龙头漏水，需要维修',
          priority: 'high',
          status: 'pending',
          maintenance_staff: '',
          maintenance_notes: '',
          created_at: '2024-05-01 10:30:00',
          updated_at: '2024-05-01 10:30:00'
        },
        {
          id: 2,
          owner_name: '李华',
          phone: '13900139002',
          property_id: 1,
          property_name: '阳光花园小区',
          unit_number: '2',
          house_number: '202',
          request_type: 'appliance',
          description: '空调不制冷，需要检查',
          priority: 'medium',
          status: 'in_progress',
          maintenance_staff: '王师傅',
          maintenance_notes: '已联系师傅上门检查',
          created_at: '2024-05-02 14:20:00',
          updated_at: '2024-05-03 09:15:00'
        },
        {
          id: 3,
          owner_name: '王芳',
          phone: '13700137003',
          property_id: 2,
          property_name: '商业中心大厦',
          unit_number: 'A',
          house_number: '501',
          request_type: 'plumbing',
          description: '卫生间下水道堵塞',
          priority: 'urgent',
          status: 'completed',
          maintenance_staff: '刘师傅',
          maintenance_notes: '已疏通下水道，问题解决',
          created_at: '2024-05-03 08:45:00',
          updated_at: '2024-05-03 11:30:00'
        },
        {
          id: 4,
          owner_name: '赵强',
          phone: '13600136004',
          property_id: 3,
          property_name: '科技园区办公楼',
          unit_number: 'C',
          house_number: '1201',
          request_type: 'door_window',
          description: '办公室门锁损坏',
          priority: 'low',
          status: 'cancelled',
          maintenance_staff: '',
          maintenance_notes: '业主自行更换了门锁',
          created_at: '2024-05-04 16:00:00',
          updated_at: '2024-05-05 10:00:00'
        }
      ]
      this.totalRequests = this.requestsData.length
    },
    
    // 加载物业数据
    loadPropertiesData() {
      // 在实际应用中，这里应该发送请求到后端获取物业数据
      // 这里使用模拟数据
      this.properties = [
        { id: 1, name: '阳光花园小区' },
        { id: 2, name: '商业中心大厦' },
        { id: 3, name: '科技园区办公楼' },
        { id: 4, name: '城市综合体' }
      ]
    },
    
    // 获取维修类型标签类型
    getTypeTag(type) {
      switch (type) {
        case 'water_electric':
          return 'primary'
        case 'plumbing':
          return 'info'
        case 'appliance':
          return 'success'
        case 'door_window':
          return 'warning'
        default:
          return 'default'
      }
    },
    
    // 获取维修类型标签
    getTypeLabel(type) {
      switch (type) {
        case 'water_electric':
          return '水电维修'
        case 'plumbing':
          return '管道维修'
        case 'appliance':
          return '家电维修'
        case 'door_window':
          return '门窗维修'
        default:
          return '其他'
      }
    },
    
    // 获取状态标签类型
    getStatusTag(status) {
      switch (status) {
        case 'pending':
          return 'warning'
        case 'in_progress':
          return 'primary'
        case 'completed':
          return 'success'
        case 'cancelled':
          return 'danger'
        default:
          return 'default'
      }
    },
    
    // 获取状态标签
    getStatusLabel(status) {
      switch (status) {
        case 'pending':
          return '待处理'
        case 'in_progress':
          return '处理中'
        case 'completed':
          return '已完成'
        case 'cancelled':
          return '已取消'
        default:
          return '未知'
      }
    },
    
    // 获取优先级标签
    getPriorityLabel(priority) {
      switch (priority) {
        case 'low':
          return '低'
        case 'medium':
          return '中'
        case 'high':
          return '高'
        case 'urgent':
          return '紧急'
        default:
          return '未知'
      }
    },
    
    // 搜索维修请求
    handleSearch() {
      // 在实际应用中，这里应该发送请求到后端搜索维修请求
      // 这里简单模拟搜索
      let filteredRequests = [...this.requestsData]
      
      if (this.searchKeyword) {
        filteredRequests = filteredRequests.filter(request => 
          request.owner_name.includes(this.searchKeyword) || 
          request.description.includes(this.searchKeyword)
        )
      }
      
      if (this.propertyFilter) {
        filteredRequests = filteredRequests.filter(request => request.property_id.toString() === this.propertyFilter)
      }
      
      if (this.statusFilter) {
        filteredRequests = filteredRequests.filter(request => request.status === this.statusFilter)
      }
      
      if (this.dateRange && this.dateRange.length === 2) {
        filteredRequests = filteredRequests.filter(request => {
          const requestDate = new Date(request.created_at.split(' ')[0])
          const startDate = new Date(this.dateRange[0])
          const endDate = new Date(this.dateRange[1])
          return requestDate >= startDate && requestDate <= endDate
        })
      }
      
      this.requestsData = filteredRequests
      this.totalRequests = filteredRequests.length
      this.currentPage = 1
    },
    
    // 重置筛选条件
    resetFilters() {
      this.searchKeyword = ''
      this.propertyFilter = ''
      this.statusFilter = ''
      this.dateRange = []
      this.loadRequestsData()
    },
    
    // 分页大小变化
    handleSizeChange(size) {
      this.pageSize = size
      this.loadRequestsData()
    },
    
    // 当前页变化
    handleCurrentChange(current) {
      this.currentPage = current
      this.loadRequestsData()
    },
    
    // 添加维修请求
    handleAddRequest() {
      this.isEdit = false
      const now = new Date()
      this.requestForm = {
        id: '',
        owner_name: '',
        phone: '',
        property_id: '',
        property_name: '',
        unit_number: '',
        house_number: '',
        request_type: 'water_electric',
        description: '',
        priority: 'medium',
        status: 'pending',
        maintenance_staff: '',
        maintenance_notes: '',
        created_at: now.toLocaleString('zh-CN'),
        updated_at: now.toLocaleString('zh-CN')
      }
      this.dialogVisible = true
    },
    
    // 编辑维修请求
    handleEditRequest(row) {
      this.isEdit = true
      this.requestForm = { ...row }
      this.dialogVisible = true
    },
    
    // 查看维修请求详情
    handleViewDetails(row) {
      this.selectedRequest = { ...row }
      this.detailDialogVisible = true
    },
    
    // 完成维修请求
    handleCompleteRequest(row) {
      // 在实际应用中，这里应该发送请求到后端更新维修请求状态
      row.status = 'completed'
      row.updated_at = new Date().toLocaleString('zh-CN')
      this.$message.success('维修请求已标记为完成')
    },
    
    // 删除维修请求
    handleDeleteRequest(id) {
      // 在实际应用中，这里应该发送请求到后端删除维修请求
      this.requestsData = this.requestsData.filter(request => request.id !== id)
      this.totalRequests = this.requestsData.length
      this.$message.success('维修请求已删除')
    },
    
    // 导出数据
    exportRequests() {
      // 在实际应用中，这里应该发送请求到后端导出数据
      this.$message.success('数据导出成功')
    },
    
    // 提交表单
    handleSubmit() {
      this.$refs.requestFormRef.validate((valid) => {
        if (valid) {
          // 获取所选物业的名称
          const selectedProperty = this.properties.find(p => p.id === this.requestForm.property_id)
          if (selectedProperty) {
            this.requestForm.property_name = selectedProperty.name
          }
          
          // 更新时间
          this.requestForm.updated_at = new Date().toLocaleString('zh-CN')
          
          // 在实际应用中，这里应该发送请求到后端保存维修请求数据
          if (this.isEdit) {
            // 编辑维修请求
            const index = this.requestsData.findIndex(request => request.id === this.requestForm.id)
            if (index !== -1) {
              this.requestsData[index] = { ...this.requestForm }
            }
            this.$message.success('维修请求已更新')
          } else {
            // 添加维修请求
            const newRequest = {
              ...this.requestForm,
              id: Date.now()
            }
            this.requestsData.unshift(newRequest)
            this.totalRequests++
            this.$message.success('维修请求已添加')
          }
          
          this.dialogVisible = false
        }
      })
    }
  }
}
</script>

<style scoped>
.maintenance-request-container {
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