<template>
  <div class="payment-management-container">
    <!-- 顶部操作栏 -->
    <div class="operation-bar mb-4 d-flex justify-content-between items-center">
      <h1>支付管理</h1>
      <div>
        <el-button type="primary" icon="el-icon-plus" @click="handleAddPayment">
          添加支付记录
        </el-button>
        <el-button type="info" icon="el-icon-refresh-left" @click="exportPayments">
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
            placeholder="搜索业主姓名或交易号"
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
          <el-select v-model="statusFilter" placeholder="支付状态" clearable>
            <el-option label="所有状态" value="" />
            <el-option label="已支付" value="paid" />
            <el-option label="待支付" value="pending" />
            <el-option label="已退款" value="refunded" />
            <el-option label="失败" value="failed" />
          </el-select>
        </el-col>
        <el-col :span="4">
          <el-select v-model="typeFilter" placeholder="支付类型" clearable>
            <el-option label="所有类型" value="" />
            <el-option label="物业费" value="property_fee" />
            <el-option label="维修费" value="maintenance_fee" />
            <el-option label="停车费" value="parking_fee" />
            <el-option label="其他" value="other" />
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
        <el-col :span="6">
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="resetFilters">重置</el-button>
        </el-col>
      </el-row>
    </div>

    <!-- 支付记录表格 -->
    <el-table :data="paymentsData" style="width: 100%">
      <el-table-column type="index" width="50" />
      <el-table-column prop="owner_name" label="业主姓名" width="120" />
      <el-table-column prop="property_name" label="所属物业" width="180" />
      <el-table-column prop="transaction_id" label="交易号" width="220" />
      <el-table-column prop="type" label="支付类型" width="120">
        <template #default="scope">
          <el-tag :type="getTypeTag(scope.row.type)">{{ getTypeLabel(scope.row.type) }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="amount" label="金额（元）" width="120" />
      <el-table-column prop="status" label="支付状态" width="100">
        <template #default="scope">
          <el-tag :type="getStatusTag(scope.row.status)">{{ getStatusLabel(scope.row.status) }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="payment_method" label="支付方式" width="120" />
      <el-table-column prop="payment_date" label="支付日期" width="180" />
      <el-table-column label="操作" width="220" fixed="right">
        <template #default="scope">
          <el-button type="primary" size="small" @click="handleEditPayment(scope.row)">
            编辑
          </el-button>
          <el-button type="info" size="small" @click="handleViewDetails(scope.row)">
            详情
          </el-button>
          <el-button
            type="success"
            size="small"
            @click="handleMarkAsPaid(scope.row)"
            :disabled="scope.row.status === 'paid' || scope.row.status === 'refunded'"
          >
            标记为支付
          </el-button>
          <el-popconfirm
            title="确定要删除此支付记录吗？"
            confirm-button-text="确定"
            cancel-button-text="取消"
            @confirm="handleDeletePayment(scope.row.id)"
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
        :total="totalPayments"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>

    <!-- 添加/编辑支付记录对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑支付记录' : '添加支付记录'"
      width="700px"
    >
      <el-form :model="paymentForm" :rules="paymentRules" ref="paymentFormRef" label-width="100px">
        <el-form-item label="业主姓名" prop="owner_name">
          <el-input v-model="paymentForm.owner_name" placeholder="请输入业主姓名" />
        </el-form-item>
        <el-form-item label="所属物业" prop="property_id">
          <el-select v-model="paymentForm.property_id" placeholder="请选择所属物业">
            <el-option v-for="property in properties" :key="property.id" :label="property.name" :value="property.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="单元号" prop="unit_number">
          <el-input v-model="paymentForm.unit_number" placeholder="请输入单元号" />
        </el-form-item>
        <el-form-item label="房号" prop="house_number">
          <el-input v-model="paymentForm.house_number" placeholder="请输入房号" />
        </el-form-item>
        <el-form-item label="支付类型" prop="type">
          <el-select v-model="paymentForm.type" placeholder="请选择支付类型">
            <el-option label="物业费" value="property_fee" />
            <el-option label="维修费" value="maintenance_fee" />
            <el-option label="停车费" value="parking_fee" />
            <el-option label="其他" value="other" />
          </el-select>
        </el-form-item>
        <el-form-item label="金额（元）" prop="amount">
          <el-input v-model.number="paymentForm.amount" type="number" placeholder="请输入金额" />
        </el-form-item>
        <el-form-item label="支付状态" prop="status" v-if="isEdit">
          <el-select v-model="paymentForm.status" placeholder="请选择支付状态">
            <el-option label="已支付" value="paid" />
            <el-option label="待支付" value="pending" />
            <el-option label="已退款" value="refunded" />
            <el-option label="失败" value="failed" />
          </el-select>
        </el-form-item>
        <el-form-item label="支付方式" prop="payment_method">
          <el-select v-model="paymentForm.payment_method" placeholder="请选择支付方式">
            <el-option label="微信支付" value="wechat" />
            <el-option label="支付宝" value="alipay" />
            <el-option label="银行转账" value="bank_transfer" />
            <el-option label="现金" value="cash" />
            <el-option label="其他" value="other" />
          </el-select>
        </el-form-item>
        <el-form-item label="交易号" prop="transaction_id">
          <el-input v-model="paymentForm.transaction_id" placeholder="请输入交易号" />
        </el-form-item>
        <el-form-item label="支付日期" prop="payment_date">
          <el-date-picker
            v-model="paymentForm.payment_date"
            type="datetime"
            placeholder="选择支付日期"
            value-format="YYYY-MM-DD HH:mm:ss"
          />
        </el-form-item>
        <el-form-item label="备注" prop="notes">
          <el-input v-model="paymentForm.notes" type="textarea" placeholder="请输入备注信息" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>

    <!-- 支付记录详情对话框 -->
    <el-dialog
      v-model="detailDialogVisible"
      title="支付记录详情"
      width="600px"
    >
      <div v-if="selectedPayment" class="payment-detail">
        <el-descriptions :column="1" border>
          <el-descriptions-item label="业主姓名">{{ selectedPayment.owner_name }}</el-descriptions-item>
          <el-descriptions-item label="所属物业">{{ selectedPayment.property_name }}</el-descriptions-item>
          <el-descriptions-item label="单元号">{{ selectedPayment.unit_number }}</el-descriptions-item>
          <el-descriptions-item label="房号">{{ selectedPayment.house_number }}</el-descriptions-item>
          <el-descriptions-item label="支付类型"><el-tag :type="getTypeTag(selectedPayment.type)">{{ getTypeLabel(selectedPayment.type) }}</el-tag></el-descriptions-item>
          <el-descriptions-item label="金额（元）"><strong style="color: #f56c6c;">{{ selectedPayment.amount }}</strong></el-descriptions-item>
          <el-descriptions-item label="支付状态"><el-tag :type="getStatusTag(selectedPayment.status)">{{ getStatusLabel(selectedPayment.status) }}</el-tag></el-descriptions-item>
          <el-descriptions-item label="支付方式">{{ getPaymentMethodLabel(selectedPayment.payment_method) }}</el-descriptions-item>
          <el-descriptions-item label="交易号">{{ selectedPayment.transaction_id }}</el-descriptions-item>
          <el-descriptions-item label="支付日期">{{ selectedPayment.payment_date }}</el-descriptions-item>
          <el-descriptions-item label="备注" v-if="selectedPayment.notes">{{ selectedPayment.notes }}</el-descriptions-item>
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
  name: 'PaymentManagementView',
  data() {
    return {
      paymentsData: [],
      properties: [],
      totalPayments: 0,
      currentPage: 1,
      pageSize: 10,
      searchKeyword: '',
      propertyFilter: '',
      statusFilter: '',
      typeFilter: '',
      dateRange: [],
      dialogVisible: false,
      detailDialogVisible: false,
      isEdit: false,
      selectedPayment: null,
      paymentForm: {
        id: '',
        owner_name: '',
        property_id: '',
        property_name: '',
        unit_number: '',
        house_number: '',
        type: 'property_fee',
        amount: 0,
        status: 'pending',
        payment_method: 'wechat',
        transaction_id: '',
        payment_date: '',
        notes: ''
      },
      paymentRules: {
        owner_name: [
          { required: true, message: '请输入业主姓名', trigger: 'blur' }
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
        type: [
          { required: true, message: '请选择支付类型', trigger: 'change' }
        ],
        amount: [
          { required: true, message: '请输入金额', trigger: 'blur' },
          { type: 'number', min: 0.01, message: '金额必须大于0', trigger: 'blur' }
        ],
        payment_method: [
          { required: true, message: '请选择支付方式', trigger: 'change' }
        ],
        transaction_id: [
          { required: true, message: '请输入交易号', trigger: 'blur' }
        ],
        payment_date: [
          { required: true, message: '请选择支付日期', trigger: 'change' }
        ]
      }
    }
  },
  mounted() {
    // 加载支付记录数据
    this.loadPaymentsData()
    // 加载物业数据用于下拉选择
    this.loadPropertiesData()
  },
  methods: {
    // 加载支付记录数据
    loadPaymentsData() {
      // 在实际应用中，这里应该发送请求到后端获取支付记录数据
      // 这里使用模拟数据
      this.paymentsData = [
        {
          id: 1,
          owner_name: '张明',
          property_id: 1,
          property_name: '阳光花园小区',
          unit_number: '1',
          house_number: '101',
          type: 'property_fee',
          amount: 1200.00,
          status: 'paid',
          payment_method: 'wechat',
          transaction_id: 'WEP20240501101123456',
          payment_date: '2024-05-01 10:30:00',
          notes: '2024年第二季度物业费'
        },
        {
          id: 2,
          owner_name: '李华',
          property_id: 1,
          property_name: '阳光花园小区',
          unit_number: '2',
          house_number: '202',
          type: 'maintenance_fee',
          amount: 580.00,
          status: 'paid',
          payment_method: 'alipay',
          transaction_id: 'ALP20240502142098765',
          payment_date: '2024-05-02 14:20:00',
          notes: '空调维修费用'
        },
        {
          id: 3,
          owner_name: '王芳',
          property_id: 2,
          property_name: '商业中心大厦',
          unit_number: 'A',
          house_number: '501',
          type: 'property_fee',
          amount: 3500.00,
          status: 'pending',
          payment_method: 'bank_transfer',
          transaction_id: 'BT20240503084543210',
          payment_date: '',
          notes: '2024年第二季度物业费（待支付）'
        },
        {
          id: 4,
          owner_name: '赵强',
          property_id: 3,
          property_name: '科技园区办公楼',
          unit_number: 'C',
          house_number: '1201',
          type: 'parking_fee',
          amount: 800.00,
          status: 'paid',
          payment_method: 'cash',
          transaction_id: 'CP20240504160087654',
          payment_date: '2024-05-04 16:00:00',
          notes: '2024年5月停车费'
        },
        {
          id: 5,
          owner_name: '陈静',
          property_id: 1,
          property_name: '阳光花园小区',
          unit_number: '3',
          house_number: '303',
          type: 'property_fee',
          amount: 1200.00,
          status: 'refunded',
          payment_method: 'wechat',
          transaction_id: 'WEP20240428113012345',
          payment_date: '2024-04-28 11:30:00',
          notes: '重复支付，已退款'
        },
        {
          id: 6,
          owner_name: '刘洋',
          property_id: 2,
          property_name: '商业中心大厦',
          unit_number: 'B',
          house_number: '802',
          type: 'other',
          amount: 200.00,
          status: 'failed',
          payment_method: 'alipay',
          transaction_id: 'ALP20240501154567890',
          payment_date: '',
          notes: '快递代收服务费（支付失败）'
        }
      ]
      this.totalPayments = this.paymentsData.length
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
    
    // 获取支付类型标签类型
    getTypeTag(type) {
      switch (type) {
        case 'property_fee':
          return 'primary'
        case 'maintenance_fee':
          return 'success'
        case 'parking_fee':
          return 'warning'
        default:
          return 'info'
      }
    },
    
    // 获取支付类型标签
    getTypeLabel(type) {
      switch (type) {
        case 'property_fee':
          return '物业费'
        case 'maintenance_fee':
          return '维修费'
        case 'parking_fee':
          return '停车费'
        default:
          return '其他'
      }
    },
    
    // 获取支付状态标签类型
    getStatusTag(status) {
      switch (status) {
        case 'paid':
          return 'success'
        case 'pending':
          return 'warning'
        case 'refunded':
          return 'info'
        case 'failed':
          return 'danger'
        default:
          return 'default'
      }
    },
    
    // 获取支付状态标签
    getStatusLabel(status) {
      switch (status) {
        case 'paid':
          return '已支付'
        case 'pending':
          return '待支付'
        case 'refunded':
          return '已退款'
        case 'failed':
          return '失败'
        default:
          return '未知'
      }
    },
    
    // 获取支付方式标签
    getPaymentMethodLabel(method) {
      switch (method) {
        case 'wechat':
          return '微信支付'
        case 'alipay':
          return '支付宝'
        case 'bank_transfer':
          return '银行转账'
        case 'cash':
          return '现金'
        default:
          return '其他'
      }
    },
    
    // 搜索支付记录
    handleSearch() {
      // 在实际应用中，这里应该发送请求到后端搜索支付记录
      // 这里简单模拟搜索
      let filteredPayments = [...this.paymentsData]
      
      if (this.searchKeyword) {
        filteredPayments = filteredPayments.filter(payment => 
          payment.owner_name.includes(this.searchKeyword) || 
          payment.transaction_id.includes(this.searchKeyword)
        )
      }
      
      if (this.propertyFilter) {
        filteredPayments = filteredPayments.filter(payment => payment.property_id.toString() === this.propertyFilter)
      }
      
      if (this.statusFilter) {
        filteredPayments = filteredPayments.filter(payment => payment.status === this.statusFilter)
      }
      
      if (this.typeFilter) {
        filteredPayments = filteredPayments.filter(payment => payment.type === this.typeFilter)
      }
      
      if (this.dateRange && this.dateRange.length === 2) {
        filteredPayments = filteredPayments.filter(payment => {
          if (!payment.payment_date) return false
          const paymentDate = new Date(payment.payment_date.split(' ')[0])
          const startDate = new Date(this.dateRange[0])
          const endDate = new Date(this.dateRange[1])
          return paymentDate >= startDate && paymentDate <= endDate
        })
      }
      
      this.paymentsData = filteredPayments
      this.totalPayments = filteredPayments.length
      this.currentPage = 1
    },
    
    // 重置筛选条件
    resetFilters() {
      this.searchKeyword = ''
      this.propertyFilter = ''
      this.statusFilter = ''
      this.typeFilter = ''
      this.dateRange = []
      this.loadPaymentsData()
    },
    
    // 分页大小变化
    handleSizeChange(size) {
      this.pageSize = size
      this.loadPaymentsData()
    },
    
    // 当前页变化
    handleCurrentChange(current) {
      this.currentPage = current
      this.loadPaymentsData()
    },
    
    // 添加支付记录
    handleAddPayment() {
      this.isEdit = false
      this.paymentForm = {
        id: '',
        owner_name: '',
        property_id: '',
        property_name: '',
        unit_number: '',
        house_number: '',
        type: 'property_fee',
        amount: 0,
        status: 'pending',
        payment_method: 'wechat',
        transaction_id: '',
        payment_date: new Date().toLocaleString('zh-CN'),
        notes: ''
      }
      this.dialogVisible = true
    },
    
    // 编辑支付记录
    handleEditPayment(row) {
      this.isEdit = true
      this.paymentForm = { ...row }
      this.dialogVisible = true
    },
    
    // 查看支付记录详情
    handleViewDetails(row) {
      this.selectedPayment = { ...row }
      this.detailDialogVisible = true
    },
    
    // 标记为支付
    handleMarkAsPaid(row) {
      // 在实际应用中，这里应该发送请求到后端更新支付状态
      row.status = 'paid'
      if (!row.payment_date) {
        row.payment_date = new Date().toLocaleString('zh-CN')
      }
      this.$message.success('支付记录已标记为已支付')
    },
    
    // 删除支付记录
    handleDeletePayment(id) {
      // 在实际应用中，这里应该发送请求到后端删除支付记录
      this.paymentsData = this.paymentsData.filter(payment => payment.id !== id)
      this.totalPayments = this.paymentsData.length
      this.$message.success('支付记录已删除')
    },
    
    // 导出数据
    exportPayments() {
      // 在实际应用中，这里应该发送请求到后端导出数据
      this.$message.success('数据导出成功')
    },
    
    // 提交表单
    handleSubmit() {
      this.$refs.paymentFormRef.validate((valid) => {
        if (valid) {
          // 获取所选物业的名称
          const selectedProperty = this.properties.find(p => p.id === this.paymentForm.property_id)
          if (selectedProperty) {
            this.paymentForm.property_name = selectedProperty.name
          }
          
          // 在实际应用中，这里应该发送请求到后端保存支付记录数据
          if (this.isEdit) {
            // 编辑支付记录
            const index = this.paymentsData.findIndex(payment => payment.id === this.paymentForm.id)
            if (index !== -1) {
              this.paymentsData[index] = { ...this.paymentForm }
            }
            this.$message.success('支付记录已更新')
          } else {
            // 添加支付记录
            const newPayment = {
              ...this.paymentForm,
              id: Date.now()
            }
            this.paymentsData.unshift(newPayment)
            this.totalPayments++
            this.$message.success('支付记录已添加')
          }
          
          this.dialogVisible = false
        }
      })
    }
  }
}
</script>

<style scoped>
.payment-management-container {
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

.payment-detail {
  padding: 10px;
}
</style>