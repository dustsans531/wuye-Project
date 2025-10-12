<template>
  <div class="announcement-container">
    <!-- 顶部操作栏 -->
    <div class="operation-bar mb-4 d-flex justify-content-between items-center">
      <h1>公告管理</h1>
      <div>
        <el-button type="primary" icon="el-icon-plus" @click="handleAddAnnouncement">
          添加公告
        </el-button>
        <el-button type="info" icon="el-icon-refresh-left" @click="refreshAnnouncements">
          刷新
        </el-button>
      </div>
    </div>

    <!-- 搜索和过滤 -->
    <div class="search-filter mb-4">
      <el-row :gutter="20">
        <el-col :span="6">
          <el-input
            v-model="searchKeyword"
            placeholder="搜索公告标题"
            clearable
            suffix-icon="el-icon-search"
            @keyup.enter="handleSearch"
          />
        </el-col>
        <el-col :span="4">
          <el-select v-model="statusFilter" placeholder="状态筛选" clearable>
            <el-option label="所有状态" value="" />
            <el-option label="发布中" value="published" />
            <el-option label="草稿" value="draft" />
            <el-option label="已过期" value="expired" />
          </el-select>
        </el-col>
        <el-col :span="4">
          <el-select v-model="typeFilter" placeholder="类型筛选" clearable>
            <el-option label="所有类型" value="" />
            <el-option label="通知" value="notice" />
            <el-option label="活动" value="activity" />
            <el-option label="通知" value="alert" />
          </el-select>
        </el-col>
        <el-col :span="4">
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="resetFilters">重置</el-button>
        </el-col>
      </el-row>
    </div>

    <!-- 公告表格 -->
    <el-table :data="announcementsData" style="width: 100%">
      <el-table-column type="index" width="50" />
      <el-table-column prop="title" label="公告标题" />
      <el-table-column prop="type" label="公告类型" width="120">
        <template #default="scope">
          <el-tag :type="getTypeTag(scope.row.type)">{{ getTypeLabel(scope.row.type) }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="status" label="状态" width="100">
        <template #default="scope">
          <el-tag :type="getStatusTag(scope.row.status)">{{ getStatusLabel(scope.row.status) }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="created_by" label="创建人" width="120" />
      <el-table-column prop="created_at" label="创建时间" width="180" />
      <el-table-column prop="publish_date" label="发布时间" width="180" />
      <el-table-column prop="expiry_date" label="过期时间" width="180" />
      <el-table-column label="操作" width="240" fixed="right">
        <template #default="scope">
          <el-button type="primary" size="small" @click="handleEditAnnouncement(scope.row)">
            编辑
          </el-button>
          <el-button type="info" size="small" @click="handleViewDetails(scope.row)">
            查看
          </el-button>
          <el-button
            type="success"
            size="small"
            @click="handlePublishAnnouncement(scope.row)"
            :disabled="scope.row.status === 'published'"
          >
            发布
          </el-button>
          <el-popconfirm
            title="确定要删除此公告吗？"
            confirm-button-text="确定"
            cancel-button-text="取消"
            @confirm="handleDeleteAnnouncement(scope.row.id)"
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
        :total="totalAnnouncements"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>

    <!-- 添加/编辑公告对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑公告' : '添加公告'"
      width="800px"
    >
      <el-form :model="announcementForm" :rules="announcementRules" ref="announcementFormRef" label-width="100px">
        <el-form-item label="公告标题" prop="title">
          <el-input v-model="announcementForm.title" placeholder="请输入公告标题" />
        </el-form-item>
        <el-form-item label="公告类型" prop="type">
          <el-select v-model="announcementForm.type" placeholder="请选择公告类型">
            <el-option label="通知" value="notice" />
            <el-option label="活动" value="activity" />
            <el-option label="提醒" value="alert" />
          </el-select>
        </el-form-item>
        <el-form-item label="公告内容" prop="content">
          <el-input v-model="announcementForm.content" type="textarea" :rows="8" placeholder="请输入公告内容" />
        </el-form-item>
        <el-form-item label="发布时间" prop="publish_date">
          <el-date-picker
            v-model="announcementForm.publish_date"
            type="datetime"
            placeholder="选择发布时间"
            value-format="YYYY-MM-DD HH:mm:ss"
          />
        </el-form-item>
        <el-form-item label="过期时间" prop="expiry_date">
          <el-date-picker
            v-model="announcementForm.expiry_date"
            type="datetime"
            placeholder="选择过期时间"
            value-format="YYYY-MM-DD HH:mm:ss"
          />
        </el-form-item>
        <el-form-item label="创建人" prop="created_by" v-if="isEdit">
          <el-input v-model="announcementForm.created_by" disabled />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>

    <!-- 公告详情对话框 -->
    <el-dialog
      v-model="detailDialogVisible"
      title="公告详情"
      width="700px"
    >
      <div v-if="selectedAnnouncement" class="announcement-detail">
        <div class="detail-header">
          <h2>{{ selectedAnnouncement.title }}</h2>
          <div class="detail-meta">
            <el-tag :type="getTypeTag(selectedAnnouncement.type)">{{ getTypeLabel(selectedAnnouncement.type) }}</el-tag>
            <span>创建人: {{ selectedAnnouncement.created_by }}</span>
            <span>创建时间: {{ selectedAnnouncement.created_at }}</span>
            <span>发布时间: {{ selectedAnnouncement.publish_date }}</span>
            <span v-if="selectedAnnouncement.expiry_date">过期时间: {{ selectedAnnouncement.expiry_date }}</span>
          </div>
        </div>
        <div class="detail-content">
          {{ selectedAnnouncement.content }}
        </div>
      </div>
      <template #footer>
        <el-button @click="detailDialogVisible = false">关闭</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: 'AnnouncementView',
  data() {
    return {
      announcementsData: [],
      totalAnnouncements: 0,
      currentPage: 1,
      pageSize: 10,
      searchKeyword: '',
      statusFilter: '',
      typeFilter: '',
      dialogVisible: false,
      detailDialogVisible: false,
      isEdit: false,
      selectedAnnouncement: null,
      announcementForm: {
        id: '',
        title: '',
        content: '',
        type: 'notice',
        status: 'draft',
        created_by: '',
        created_at: '',
        publish_date: '',
        expiry_date: ''
      },
      announcementRules: {
        title: [
          { required: true, message: '请输入公告标题', trigger: 'blur' },
          { min: 2, max: 100, message: '标题长度在 2 到 100 个字符之间', trigger: 'blur' }
        ],
        content: [
          { required: true, message: '请输入公告内容', trigger: 'blur' },
          { min: 10, message: '内容长度不能少于10个字符', trigger: 'blur' }
        ],
        type: [
          { required: true, message: '请选择公告类型', trigger: 'change' }
        ],
        publish_date: [
          { required: true, message: '请选择发布时间', trigger: 'change' }
        ]
      }
    }
  },
  mounted() {
    // 加载公告数据
    this.loadAnnouncementsData()
  },
  methods: {
    // 加载公告数据
    loadAnnouncementsData() {
      // 在实际应用中，这里应该发送请求到后端获取公告数据
      // 这里使用模拟数据
      this.announcementsData = [
        {
          id: 1,
          title: '关于小区电梯维护的通知',
          content: '尊敬的业主：\n为保障小区电梯安全运行，物业公司将于5月10日至5月12日对小区所有电梯进行全面维护保养。维护期间可能会短暂影响电梯正常使用，请各位业主提前做好准备，不便之处敬请谅解。\n如有疑问，请联系物业客服热线：400-123-4567。\n\n阳光花园物业管理处\n2024年5月5日',
          type: 'notice',
          status: 'published',
          created_by: '管理员',
          created_at: '2024-05-05 14:30:00',
          publish_date: '2024-05-05 15:00:00',
          expiry_date: '2024-05-15 00:00:00'
        },
        {
          id: 2,
          title: '五一劳动节社区活动通知',
          content: '亲爱的业主朋友们：\n为庆祝五一国际劳动节，丰富小区居民文化生活，物业将于5月1日上午9点在小区中心广场举办"劳动最光荣"主题活动，包括文艺表演、趣味游戏、免费义诊等环节，欢迎广大业主积极参与！\n\n活动安排：\n9:00-10:00 开幕仪式\n10:00-11:30 文艺表演\n11:30-14:00 趣味游戏\n14:00-16:00 免费义诊\n\n阳光花园物业管理处\n2024年4月20日',
          type: 'activity',
          status: 'expired',
          created_by: '活动策划组',
          created_at: '2024-04-20 10:00:00',
          publish_date: '2024-04-20 10:30:00',
          expiry_date: '2024-05-02 00:00:00'
        },
        {
          id: 3,
          title: '消防安全提醒',
          content: '消防安全温馨提示：\n近期天气干燥，容易发生火灾，请各位业主注意以下事项：\n1. 不要在楼道内堆放杂物，保持消防通道畅通；\n2. 不要在小区内随意焚烧物品；\n3. 外出时请关闭电源和燃气阀门；\n4. 家中常备灭火器，并掌握正确使用方法。\n\n让我们共同维护小区的消防安全环境！\n\n阳光花园物业管理处\n2024年5月8日',
          type: 'alert',
          status: 'published',
          created_by: '安全主管',
          created_at: '2024-05-08 09:00:00',
          publish_date: '2024-05-08 09:30:00',
          expiry_date: '2024-06-08 00:00:00'
        },
        {
          id: 4,
          title: '物业费缴纳通知草稿',
          content: '尊敬的业主：\n2024年第二季度物业费缴纳工作即将开始，请各位业主按时缴纳。缴费方式：\n1. 线上缴费：通过物业管理APP或微信公众号缴费；\n2. 线下缴费：到物业管理处前台现金或刷卡缴费。\n\n缴费时间：2024年5月15日至2024年5月31日\n\n感谢您对物业工作的支持与配合！\n\n阳光花园物业管理处\n2024年5月10日',
          type: 'notice',
          status: 'draft',
          created_by: '财务部门',
          created_at: '2024-05-09 16:30:00',
          publish_date: '',
          expiry_date: '2024-06-10 00:00:00'
        }
      ]
      this.totalAnnouncements = this.announcementsData.length
    },
    
    // 获取类型标签类型
    getTypeTag(type) {
      switch (type) {
        case 'notice':
          return 'primary'
        case 'activity':
          return 'success'
        case 'alert':
          return 'warning'
        default:
          return 'default'
      }
    },
    
    // 获取类型标签
    getTypeLabel(type) {
      switch (type) {
        case 'notice':
          return '通知'
        case 'activity':
          return '活动'
        case 'alert':
          return '提醒'
        default:
          return '未知'
      }
    },
    
    // 获取状态标签类型
    getStatusTag(status) {
      switch (status) {
        case 'published':
          return 'success'
        case 'draft':
          return 'default'
        case 'expired':
          return 'danger'
        default:
          return 'default'
      }
    },
    
    // 获取状态标签
    getStatusLabel(status) {
      switch (status) {
        case 'published':
          return '发布中'
        case 'draft':
          return '草稿'
        case 'expired':
          return '已过期'
        default:
          return '未知'
      }
    },
    
    // 搜索公告
    handleSearch() {
      // 在实际应用中，这里应该发送请求到后端搜索公告
      // 这里简单模拟搜索
      let filteredAnnouncements = [...this.announcementsData]
      
      if (this.searchKeyword) {
        filteredAnnouncements = filteredAnnouncements.filter(announcement => 
          announcement.title.includes(this.searchKeyword)
        )
      }
      
      if (this.statusFilter) {
        filteredAnnouncements = filteredAnnouncements.filter(announcement => announcement.status === this.statusFilter)
      }
      
      if (this.typeFilter) {
        filteredAnnouncements = filteredAnnouncements.filter(announcement => announcement.type === this.typeFilter)
      }
      
      this.announcementsData = filteredAnnouncements
      this.totalAnnouncements = filteredAnnouncements.length
      this.currentPage = 1
    },
    
    // 重置筛选条件
    resetFilters() {
      this.searchKeyword = ''
      this.statusFilter = ''
      this.typeFilter = ''
      this.loadAnnouncementsData()
    },
    
    // 分页大小变化
    handleSizeChange(size) {
      this.pageSize = size
      this.loadAnnouncementsData()
    },
    
    // 当前页变化
    handleCurrentChange(current) {
      this.currentPage = current
      this.loadAnnouncementsData()
    },
    
    // 添加公告
    handleAddAnnouncement() {
      this.isEdit = false
      const now = new Date()
      this.announcementForm = {
        id: '',
        title: '',
        content: '',
        type: 'notice',
        status: 'draft',
        created_by: '当前用户', // 实际应用中应该从登录信息中获取
        created_at: now.toLocaleString('zh-CN'),
        publish_date: '',
        expiry_date: ''
      }
      this.dialogVisible = true
    },
    
    // 编辑公告
    handleEditAnnouncement(row) {
      this.isEdit = true
      this.announcementForm = { ...row }
      this.dialogVisible = true
    },
    
    // 查看公告详情
    handleViewDetails(row) {
      this.selectedAnnouncement = { ...row }
      this.detailDialogVisible = true
    },
    
    // 发布公告
    handlePublishAnnouncement(row) {
      // 在实际应用中，这里应该发送请求到后端发布公告
      row.status = 'published'
      if (!row.publish_date) {
        row.publish_date = new Date().toLocaleString('zh-CN')
      }
      row.updated_at = new Date().toLocaleString('zh-CN')
      this.$message.success('公告已发布')
    },
    
    // 删除公告
    handleDeleteAnnouncement(id) {
      // 在实际应用中，这里应该发送请求到后端删除公告
      this.announcementsData = this.announcementsData.filter(announcement => announcement.id !== id)
      this.totalAnnouncements = this.announcementsData.length
      this.$message.success('公告已删除')
    },
    
    // 刷新公告列表
    refreshAnnouncements() {
      this.loadAnnouncementsData()
      this.$message.success('公告列表已刷新')
    },
    
    // 提交表单
    handleSubmit() {
      this.$refs.announcementFormRef.validate((valid) => {
        if (valid) {
          // 在实际应用中，这里应该发送请求到后端保存公告数据
          if (this.isEdit) {
            // 编辑公告
            const index = this.announcementsData.findIndex(announcement => announcement.id === this.announcementForm.id)
            if (index !== -1) {
              this.announcementsData[index] = { ...this.announcementForm }
            }
            this.$message.success('公告已更新')
          } else {
            // 添加公告
            const newAnnouncement = {
              ...this.announcementForm,
              id: Date.now()
            }
            this.announcementsData.unshift(newAnnouncement)
            this.totalAnnouncements++
            this.$message.success('公告已添加')
          }
          
          this.dialogVisible = false
        }
      })
    }
  }
}
</script>

<style scoped>
.announcement-container {
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

.announcement-detail {
  padding: 20px;
}

.detail-header {
  margin-bottom: 20px;
}

.detail-header h2 {
  font-size: 20px;
  margin-bottom: 10px;
}

.detail-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  font-size: 14px;
  color: #666;
}

.detail-content {
  line-height: 1.8;
  white-space: pre-wrap;
  word-break: break-word;
}
</style>