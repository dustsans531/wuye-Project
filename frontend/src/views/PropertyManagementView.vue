<template>
  <div class="property-management-container">
    <!-- 顶部操作栏 -->
    <div class="operation-bar mb-4 d-flex justify-content-between items-center">
      <h1>物业信息管理</h1>
      <el-button type="primary" icon="el-icon-plus" @click="handleAddProperty">
        添加物业
      </el-button>
    </div>

    <!-- 搜索和过滤 -->
    <div class="search-filter mb-4">
      <el-row :gutter="20">
        <el-col :span="6">
          <el-input
            v-model="searchKeyword"
            placeholder="搜索物业名称或地址"
            clearable
            suffix-icon="el-icon-search"
            @keyup.enter="handleSearch"
          />
        </el-col>
        <el-col :span="4">
          <el-select v-model="typeFilter" placeholder="类型筛选" clearable>
            <el-option label="所有类型" value="" />
            <el-option label="住宅" value="residential" />
            <el-option label="商业" value="commercial" />
            <el-option label="办公" value="office" />
            <el-option label="其他" value="other" />
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

    <!-- 物业表格 -->
    <el-table :data="propertiesData" style="width: 100%">
      <el-table-column type="index" width="50" />
      <el-table-column prop="name" label="物业名称" width="200" />
      <el-table-column prop="address" label="地址" />
      <el-table-column prop="type" label="物业类型" width="120">
        <template #default="scope">
          <el-tag :type="getPropertyType(scope.row.type)">{{ getPropertyTypeName(scope.row.type) }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="units_count" label="单元数量" width="120" />
      <el-table-column prop="floors_count" label="楼层数量" width="120" />
      <el-table-column prop="manager_name" label="物业经理" width="120" />
      <el-table-column prop="status" label="状态" width="100">
        <template #default="scope">
          <el-switch v-model="scope.row.status" @change="handleStatusChange(scope.row)" />
        </template>
      </el-table-column>
      <el-table-column label="操作" width="180" fixed="right">
        <template #default="scope">
          <el-button type="primary" size="small" @click="handleEditProperty(scope.row)">
            编辑
          </el-button>
          <el-popconfirm
            title="确定要删除此物业吗？"
            confirm-button-text="确定"
            cancel-button-text="取消"
            @confirm="handleDeleteProperty(scope.row.id)"
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
        :total="totalProperties"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>

    <!-- 添加/编辑物业对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑物业' : '添加物业'"
      width="600px"
    >
      <el-form :model="propertyForm" :rules="propertyRules" ref="propertyFormRef" label-width="100px">
        <el-form-item label="物业名称" prop="name">
          <el-input v-model="propertyForm.name" placeholder="请输入物业名称" />
        </el-form-item>
        <el-form-item label="地址" prop="address">
          <el-input v-model="propertyForm.address" type="textarea" placeholder="请输入物业地址" />
        </el-form-item>
        <el-form-item label="物业类型" prop="type">
          <el-select v-model="propertyForm.type" placeholder="请选择物业类型">
            <el-option label="住宅" value="residential" />
            <el-option label="商业" value="commercial" />
            <el-option label="办公" value="office" />
            <el-option label="其他" value="other" />
          </el-select>
        </el-form-item>
        <el-form-item label="单元数量" prop="units_count">
          <el-input v-model.number="propertyForm.units_count" type="number" placeholder="请输入单元数量" />
        </el-form-item>
        <el-form-item label="楼层数量" prop="floors_count">
          <el-input v-model.number="propertyForm.floors_count" type="number" placeholder="请输入楼层数量" />
        </el-form-item>
        <el-form-item label="物业经理" prop="manager_name">
          <el-input v-model="propertyForm.manager_name" placeholder="请输入物业经理姓名" />
        </el-form-item>
        <el-form-item label="经理电话" prop="manager_phone">
          <el-input v-model="propertyForm.manager_phone" placeholder="请输入物业经理电话" />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input v-model="propertyForm.description" type="textarea" placeholder="请输入物业描述" />
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
  name: 'PropertyManagementView',
  data() {
    return {
      propertiesData: [],
      totalProperties: 0,
      currentPage: 1,
      pageSize: 10,
      searchKeyword: '',
      typeFilter: '',
      statusFilter: '',
      dialogVisible: false,
      isEdit: false,
      propertyForm: {
        id: '',
        name: '',
        address: '',
        type: 'residential',
        units_count: 0,
        floors_count: 0,
        manager_name: '',
        manager_phone: '',
        description: '',
        status: true
      },
      propertyRules: {
        name: [
          { required: true, message: '请输入物业名称', trigger: 'blur' },
          { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
        ],
        address: [
          { required: true, message: '请输入物业地址', trigger: 'blur' },
          { min: 5, message: '地址不能为空', trigger: 'blur' }
        ],
        type: [
          { required: true, message: '请选择物业类型', trigger: 'change' }
        ],
        units_count: [
          { required: true, message: '请输入单元数量', trigger: 'blur' },
          { type: 'number', min: 0, message: '单元数量必须大于等于0', trigger: 'blur' }
        ],
        floors_count: [
          { required: true, message: '请输入楼层数量', trigger: 'blur' },
          { type: 'number', min: 1, message: '楼层数量必须大于等于1', trigger: 'blur' }
        ],
        manager_name: [
          { required: true, message: '请输入物业经理姓名', trigger: 'blur' }
        ],
        manager_phone: [
          { required: true, message: '请输入物业经理电话', trigger: 'blur' },
          { pattern: /^1[3-9]\d{9}$/, message: '请输入有效的手机号码', trigger: 'blur' }
        ]
      }
    }
  },
  mounted() {
    // 加载物业数据
    this.loadPropertiesData()
  },
  methods: {
    // 加载物业数据
    loadPropertiesData() {
      // 在实际应用中，这里应该发送请求到后端获取物业数据
      // 这里使用模拟数据
      this.propertiesData = [
        {
          id: 1,
          name: '阳光花园小区',
          address: '北京市朝阳区阳光路88号',
          type: 'residential',
          units_count: 250,
          floors_count: 18,
          manager_name: '张三',
          manager_phone: '13800138001',
          description: '高品质住宅小区，配套设施齐全',
          status: true
        },
        {
          id: 2,
          name: '商业中心大厦',
          address: '上海市浦东新区商业大道100号',
          type: 'commercial',
          units_count: 120,
          floors_count: 30,
          manager_name: '李四',
          manager_phone: '13900139002',
          description: '现代化商业中心，集购物、餐饮、娱乐于一体',
          status: true
        },
        {
          id: 3,
          name: '科技园区办公楼',
          address: '深圳市南山区科技园路55号',
          type: 'office',
          units_count: 80,
          floors_count: 25,
          manager_name: '王五',
          manager_phone: '13700137003',
          description: '专为科技企业打造的现代化办公空间',
          status: true
        },
        {
          id: 4,
          name: '城市综合体',
          address: '广州市天河区天河路385号',
          type: 'other',
          units_count: 300,
          floors_count: 45,
          manager_name: '赵六',
          manager_phone: '13600136004',
          description: '集住宅、商业、办公于一体的城市综合体',
          status: true
        }
      ]
      this.totalProperties = this.propertiesData.length
    },
    
    // 获取物业类型对应的标签类型
    getPropertyType(type) {
      switch (type) {
        case 'residential':
          return 'primary'
        case 'commercial':
          return 'success'
        case 'office':
          return 'warning'
        default:
          return 'info'
      }
    },
    
    // 获取物业类型名称
    getPropertyTypeName(type) {
      switch (type) {
        case 'residential':
          return '住宅'
        case 'commercial':
          return '商业'
        case 'office':
          return '办公'
        default:
          return '其他'
      }
    },
    
    // 搜索物业
    handleSearch() {
      // 在实际应用中，这里应该发送请求到后端搜索物业
      // 这里简单模拟搜索
      let filteredProperties = [...this.propertiesData]
      
      if (this.searchKeyword) {
        filteredProperties = filteredProperties.filter(property => 
          property.name.includes(this.searchKeyword) || 
          property.address.includes(this.searchKeyword)
        )
      }
      
      if (this.typeFilter) {
        filteredProperties = filteredProperties.filter(property => property.type === this.typeFilter)
      }
      
      if (this.statusFilter !== '') {
        filteredProperties = filteredProperties.filter(property => 
          property.status.toString() === this.statusFilter
        )
      }
      
      this.propertiesData = filteredProperties
      this.totalProperties = filteredProperties.length
      this.currentPage = 1
    },
    
    // 重置筛选条件
    resetFilters() {
      this.searchKeyword = ''
      this.typeFilter = ''
      this.statusFilter = ''
      this.loadPropertiesData()
    },
    
    // 分页大小变化
    handleSizeChange(size) {
      this.pageSize = size
      this.loadPropertiesData()
    },
    
    // 当前页变化
    handleCurrentChange(current) {
      this.currentPage = current
      this.loadPropertiesData()
    },
    
    // 更改物业状态
    handleStatusChange(row) {
      // 在实际应用中，这里应该发送请求到后端更新物业状态
      this.$message.success('物业状态已更新')
    },
    
    // 添加物业
    handleAddProperty() {
      this.isEdit = false
      this.propertyForm = {
        id: '',
        name: '',
        address: '',
        type: 'residential',
        units_count: 0,
        floors_count: 0,
        manager_name: '',
        manager_phone: '',
        description: '',
        status: true
      }
      this.dialogVisible = true
    },
    
    // 编辑物业
    handleEditProperty(row) {
      this.isEdit = true
      this.propertyForm = { ...row }
      this.dialogVisible = true
    },
    
    // 删除物业
    handleDeleteProperty(id) {
      // 在实际应用中，这里应该发送请求到后端删除物业
      this.propertiesData = this.propertiesData.filter(property => property.id !== id)
      this.totalProperties = this.propertiesData.length
      this.$message.success('物业信息已删除')
    },
    
    // 提交表单
    handleSubmit() {
      this.$refs.propertyFormRef.validate((valid) => {
        if (valid) {
          // 在实际应用中，这里应该发送请求到后端保存物业数据
          if (this.isEdit) {
            // 编辑物业
            const index = this.propertiesData.findIndex(property => property.id === this.propertyForm.id)
            if (index !== -1) {
              this.propertiesData[index] = { ...this.propertyForm }
            }
            this.$message.success('物业信息已更新')
          } else {
            // 添加物业
            const newProperty = {
              ...this.propertyForm,
              id: Date.now()
            }
            this.propertiesData.unshift(newProperty)
            this.totalProperties++
            this.$message.success('物业信息已添加')
          }
          
          this.dialogVisible = false
        }
      })
    }
  }
}
</script>

<style scoped>
.property-management-container {
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