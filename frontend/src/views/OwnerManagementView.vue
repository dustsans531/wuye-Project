<template>
  <div class="owner-management-container">
    <!-- 顶部操作栏 -->
    <div class="operation-bar mb-4 d-flex justify-content-between items-center">
      <h1>业主信息管理</h1>
      <el-button type="primary" icon="el-icon-plus" @click="handleAddOwner">
        添加业主
      </el-button>
    </div>

    <!-- 搜索和过滤 -->
    <div class="search-filter mb-4">
      <el-row :gutter="20">
        <el-col :span="6">
          <el-input
            v-model="searchKeyword"
            placeholder="搜索业主姓名或电话"
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
            <el-option label="正常" value="active" />
            <el-option label="欠费" value="overdue" />
            <el-option label="其他" value="other" />
          </el-select>
        </el-col>
        <el-col :span="4">
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="resetFilters">重置</el-button>
        </el-col>
      </el-row>
    </div>

    <!-- 业主表格 -->
    <el-table :data="ownersData" style="width: 100%">
      <el-table-column type="index" width="50" />
      <el-table-column prop="name" label="姓名" width="120" />
      <el-table-column prop="phone" label="联系电话" width="150" />
      <el-table-column prop="id_card" label="身份证号" width="200" />
      <el-table-column prop="property_name" label="所属物业" width="180" />
      <el-table-column prop="unit_number" label="单元号" width="120" />
      <el-table-column prop="house_number" label="房号" width="120" />
      <el-table-column prop="status" label="状态" width="100">
        <template #default="scope">
          <el-tag :type="getStatusType(scope.row.status)">{{ getStatusName(scope.row.status) }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="240" fixed="right">
        <template #default="scope">
          <el-button type="primary" size="small" @click="handleEditOwner(scope.row)">
            编辑
          </el-button>
          <el-button type="info" size="small" @click="handleViewDetails(scope.row)">
            详情
          </el-button>
          <el-popconfirm
            title="确定要删除此业主信息吗？"
            confirm-button-text="确定"
            cancel-button-text="取消"
            @confirm="handleDeleteOwner(scope.row.id)"
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
        :total="totalOwners"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>

    <!-- 添加/编辑业主对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑业主' : '添加业主'"
      width="600px"
    >
      <el-form :model="ownerForm" :rules="ownerRules" ref="ownerFormRef" label-width="100px">
        <el-form-item label="姓名" prop="name">
          <el-input v-model="ownerForm.name" placeholder="请输入业主姓名" />
        </el-form-item>
        <el-form-item label="联系电话" prop="phone">
          <el-input v-model="ownerForm.phone" placeholder="请输入联系电话" />
        </el-form-item>
        <el-form-item label="身份证号" prop="id_card">
          <el-input v-model="ownerForm.id_card" placeholder="请输入身份证号" />
        </el-form-item>
        <el-form-item label="所属物业" prop="property_id">
          <el-select v-model="ownerForm.property_id" placeholder="请选择所属物业">
            <el-option v-for="property in properties" :key="property.id" :label="property.name" :value="property.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="单元号" prop="unit_number">
          <el-input v-model="ownerForm.unit_number" placeholder="请输入单元号" />
        </el-form-item>
        <el-form-item label="房号" prop="house_number">
          <el-input v-model="ownerForm.house_number" placeholder="请输入房号" />
        </el-form-item>
        <el-form-item label="房屋面积" prop="house_area">
          <el-input v-model.number="ownerForm.house_area" type="number" placeholder="请输入房屋面积" />
        </el-form-item>
        <el-form-item label="入住日期" prop="move_in_date">
          <el-date-picker v-model="ownerForm.move_in_date" type="date" placeholder="选择入住日期" />
        </el-form-item>
        <el-form-item label="业主状态" prop="status">
          <el-select v-model="ownerForm.status" placeholder="请选择业主状态">
            <el-option label="正常" value="active" />
            <el-option label="欠费" value="overdue" />
            <el-option label="其他" value="other" />
          </el-select>
        </el-form-item>
        <el-form-item label="备注" prop="remarks">
          <el-input v-model="ownerForm.remarks" type="textarea" placeholder="请输入备注信息" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>

    <!-- 业主详情对话框 -->
    <el-dialog
      v-model="detailDialogVisible"
      title="业主详情"
      width="500px"
    >
      <div v-if="selectedOwner">
        <el-descriptions :column="1" border>
          <el-descriptions-item label="姓名">{{ selectedOwner.name }}</el-descriptions-item>
          <el-descriptions-item label="联系电话">{{ selectedOwner.phone }}</el-descriptions-item>
          <el-descriptions-item label="身份证号">{{ selectedOwner.id_card }}</el-descriptions-item>
          <el-descriptions-item label="所属物业">{{ selectedOwner.property_name }}</el-descriptions-item>
          <el-descriptions-item label="单元号">{{ selectedOwner.unit_number }}</el-descriptions-item>
          <el-descriptions-item label="房号">{{ selectedOwner.house_number }}</el-descriptions-item>
          <el-descriptions-item label="房屋面积">{{ selectedOwner.house_area }} ㎡</el-descriptions-item>
          <el-descriptions-item label="入住日期">{{ selectedOwner.move_in_date ? formatDate(selectedOwner.move_in_date) : '-' }}</el-descriptions-item>
          <el-descriptions-item label="状态"><el-tag :type="getStatusType(selectedOwner.status)">{{ getStatusName(selectedOwner.status) }}</el-tag></el-descriptions-item>
          <el-descriptions-item label="备注" v-if="selectedOwner.remarks">{{ selectedOwner.remarks }}</el-descriptions-item>
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
  name: 'OwnerManagementView',
  data() {
    return {
      ownersData: [],
      properties: [],
      totalOwners: 0,
      currentPage: 1,
      pageSize: 10,
      searchKeyword: '',
      propertyFilter: '',
      statusFilter: '',
      dialogVisible: false,
      detailDialogVisible: false,
      isEdit: false,
      selectedOwner: null,
      ownerForm: {
        id: '',
        name: '',
        phone: '',
        id_card: '',
        property_id: '',
        property_name: '',
        unit_number: '',
        house_number: '',
        house_area: 0,
        move_in_date: '',
        status: 'active',
        remarks: ''
      },
      ownerRules: {
        name: [
          { required: true, message: '请输入业主姓名', trigger: 'blur' },
          { min: 2, max: 20, message: '长度在 2 到 20 个字符', trigger: 'blur' }
        ],
        phone: [
          { required: true, message: '请输入联系电话', trigger: 'blur' },
          { pattern: /^1[3-9]\d{9}$/, message: '请输入有效的手机号码', trigger: 'blur' }
        ],
        id_card: [
          { required: true, message: '请输入身份证号', trigger: 'blur' },
          { pattern: /(^\d{15}$)|(^\d{18}$)|(^\d{17}(\d|X|x)$)/, message: '请输入有效的身份证号', trigger: 'blur' }
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
        house_area: [
          { required: true, message: '请输入房屋面积', trigger: 'blur' },
          { type: 'number', min: 0, message: '房屋面积必须大于等于0', trigger: 'blur' }
        ],
        move_in_date: [
          { required: true, message: '请选择入住日期', trigger: 'change' }
        ],
        status: [
          { required: true, message: '请选择业主状态', trigger: 'change' }
        ]
      }
    }
  },
  mounted() {
    // 加载业主数据
    this.loadOwnersData()
    // 加载物业数据用于下拉选择
    this.loadPropertiesData()
  },
  methods: {
    // 加载业主数据
    loadOwnersData() {
      // 在实际应用中，这里应该发送请求到后端获取业主数据
      // 这里使用模拟数据
      this.ownersData = [
        {
          id: 1,
          name: '张明',
          phone: '13800138001',
          id_card: '110101199001011234',
          property_id: 1,
          property_name: '阳光花园小区',
          unit_number: '1',
          house_number: '101',
          house_area: 95.5,
          move_in_date: '2023-01-15',
          status: 'active',
          remarks: ''
        },
        {
          id: 2,
          name: '李华',
          phone: '13900139002',
          id_card: '310101199202022345',
          property_id: 1,
          property_name: '阳光花园小区',
          unit_number: '2',
          house_number: '202',
          house_area: 120.0,
          move_in_date: '2023-03-20',
          status: 'active',
          remarks: '业主是公司高管，经常出差'
        },
        {
          id: 3,
          name: '王芳',
          phone: '13700137003',
          id_card: '440301199503033456',
          property_id: 2,
          property_name: '商业中心大厦',
          unit_number: 'A',
          house_number: '501',
          house_area: 150.8,
          move_in_date: '2023-05-10',
          status: 'overdue',
          remarks: '物业费已拖欠2个月'
        },
        {
          id: 4,
          name: '赵强',
          phone: '13600136004',
          id_card: '440101198804044567',
          property_id: 3,
          property_name: '科技园区办公楼',
          unit_number: 'C',
          house_number: '1201',
          house_area: 200.0,
          move_in_date: '2023-07-05',
          status: 'active',
          remarks: '租户是科技公司'
        }
      ]
      this.totalOwners = this.ownersData.length
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
    
    // 获取状态对应的标签类型
    getStatusType(status) {
      switch (status) {
        case 'active':
          return 'success'
        case 'overdue':
          return 'danger'
        default:
          return 'warning'
      }
    },
    
    // 获取状态名称
    getStatusName(status) {
      switch (status) {
        case 'active':
          return '正常'
        case 'overdue':
          return '欠费'
        default:
          return '其他'
      }
    },
    
    // 格式化日期
    formatDate(dateString) {
      const date = new Date(dateString)
      return date.toLocaleDateString('zh-CN')
    },
    
    // 搜索业主
    handleSearch() {
      // 在实际应用中，这里应该发送请求到后端搜索业主
      // 这里简单模拟搜索
      let filteredOwners = [...this.ownersData]
      
      if (this.searchKeyword) {
        filteredOwners = filteredOwners.filter(owner => 
          owner.name.includes(this.searchKeyword) || 
          owner.phone.includes(this.searchKeyword)
        )
      }
      
      if (this.propertyFilter) {
        filteredOwners = filteredOwners.filter(owner => owner.property_id.toString() === this.propertyFilter)
      }
      
      if (this.statusFilter) {
        filteredOwners = filteredOwners.filter(owner => owner.status === this.statusFilter)
      }
      
      this.ownersData = filteredOwners
      this.totalOwners = filteredOwners.length
      this.currentPage = 1
    },
    
    // 重置筛选条件
    resetFilters() {
      this.searchKeyword = ''
      this.propertyFilter = ''
      this.statusFilter = ''
      this.loadOwnersData()
    },
    
    // 分页大小变化
    handleSizeChange(size) {
      this.pageSize = size
      this.loadOwnersData()
    },
    
    // 当前页变化
    handleCurrentChange(current) {
      this.currentPage = current
      this.loadOwnersData()
    },
    
    // 添加业主
    handleAddOwner() {
      this.isEdit = false
      this.ownerForm = {
        id: '',
        name: '',
        phone: '',
        id_card: '',
        property_id: '',
        property_name: '',
        unit_number: '',
        house_number: '',
        house_area: 0,
        move_in_date: '',
        status: 'active',
        remarks: ''
      }
      this.dialogVisible = true
    },
    
    // 编辑业主
    handleEditOwner(row) {
      this.isEdit = true
      this.ownerForm = { ...row }
      this.dialogVisible = true
    },
    
    // 查看业主详情
    handleViewDetails(row) {
      this.selectedOwner = { ...row }
      this.detailDialogVisible = true
    },
    
    // 删除业主
    handleDeleteOwner(id) {
      // 在实际应用中，这里应该发送请求到后端删除业主
      this.ownersData = this.ownersData.filter(owner => owner.id !== id)
      this.totalOwners = this.ownersData.length
      this.$message.success('业主信息已删除')
    },
    
    // 提交表单
    handleSubmit() {
      this.$refs.ownerFormRef.validate((valid) => {
        if (valid) {
          // 获取所选物业的名称
          const selectedProperty = this.properties.find(p => p.id === this.ownerForm.property_id)
          if (selectedProperty) {
            this.ownerForm.property_name = selectedProperty.name
          }
          
          // 在实际应用中，这里应该发送请求到后端保存业主数据
          if (this.isEdit) {
            // 编辑业主
            const index = this.ownersData.findIndex(owner => owner.id === this.ownerForm.id)
            if (index !== -1) {
              this.ownersData[index] = { ...this.ownerForm }
            }
            this.$message.success('业主信息已更新')
          } else {
            // 添加业主
            const newOwner = {
              ...this.ownerForm,
              id: Date.now()
            }
            this.ownersData.unshift(newOwner)
            this.totalOwners++
            this.$message.success('业主信息已添加')
          }
          
          this.dialogVisible = false
        }
      })
    }
  }
}
</script>

<style scoped>
.owner-management-container {
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