<template>
  <div class="system-settings-container">
    <!-- 顶部操作栏 -->
    <div class="operation-bar mb-4 d-flex justify-content-between items-center">
      <h1>系统设置</h1>
      <div>
        <el-button type="primary" icon="el-icon-save" @click="saveSettings">
          保存设置
        </el-button>
        <el-button type="warning" icon="el-icon-refresh-left" @click="resetSettings">
          重置为默认值
        </el-button>
      </div>
    </div>

    <!-- 设置导航 -->
    <el-tabs v-model="activeTab" type="card" class="mb-4">
      <el-tab-pane label="基本设置" name="basicSettings" />
      <el-tab-pane label="安全设置" name="securitySettings" />
      <el-tab-pane label="通知设置" name="notificationSettings" />
      <el-tab-pane label="外观设置" name="appearanceSettings" />
    </el-tabs>

    <!-- 基本设置 -->
    <div v-if="activeTab === 'basicSettings'" class="settings-content">
      <el-card title="系统基本信息">
        <el-form :model="systemInfo" label-width="120px">
          <el-form-item label="系统名称" prop="systemName">
            <el-input v-model="systemInfo.systemName" placeholder="请输入系统名称" />
          </el-form-item>
          <el-form-item label="系统版本" prop="systemVersion" disabled>
            <el-input v-model="systemInfo.systemVersion" />
          </el-form-item>
          <el-form-item label="系统描述" prop="systemDescription">
            <el-input v-model="systemInfo.systemDescription" type="textarea" placeholder="请输入系统描述" />
          </el-form-item>
          <el-form-item label="系统Logo">
            <el-upload
              class="avatar-uploader"
              action="#"
              :show-file-list="false"
              :on-success="handleLogoSuccess"
              :before-upload="beforeLogoUpload"
            >
              <img v-if="systemInfo.systemLogo" :src="systemInfo.systemLogo" class="avatar" />
              <i v-else class="el-icon-plus avatar-uploader-icon"></i>
            </el-upload>
            <div class="el-upload__tip">请上传图片文件，大小不超过2MB</div>
          </el-form-item>
        </el-form>
      </el-card>

      <el-card title="联系信息" class="mt-4">
        <el-form :model="contactInfo" label-width="120px">
          <el-form-item label="客服电话" prop="supportPhone">
            <el-input v-model="contactInfo.supportPhone" placeholder="请输入客服电话" />
          </el-form-item>
          <el-form-item label="客服邮箱" prop="supportEmail">
            <el-input v-model="contactInfo.supportEmail" placeholder="请输入客服邮箱" />
          </el-form-item>
          <el-form-item label="工作时间" prop="workHours">
            <el-input v-model="contactInfo.workHours" placeholder="请输入工作时间" />
          </el-form-item>
          <el-form-item label="地址" prop="address">
            <el-input v-model="contactInfo.address" type="textarea" placeholder="请输入地址" />
          </el-form-item>
        </el-form>
      </el-card>

      <el-card title="支付配置" class="mt-4">
        <el-form :model="paymentConfig" label-width="120px">
          <el-form-item label="默认支付方式" prop="defaultPaymentMethod">
            <el-select v-model="paymentConfig.defaultPaymentMethod" placeholder="请选择默认支付方式">
              <el-option label="微信支付" value="wechat" />
              <el-option label="支付宝" value="alipay" />
              <el-option label="银行转账" value="bank_transfer" />
              <el-option label="现金" value="cash" />
            </el-select>
          </el-form-item>
          <el-form-item label="是否启用在线支付" prop="enableOnlinePayment">
            <el-switch v-model="paymentConfig.enableOnlinePayment" />
          </el-form-item>
          <el-form-item label="支付过期时间（天）" prop="paymentExpiryDays">
            <el-input-number v-model="paymentConfig.paymentExpiryDays" :min="1" :max="30" />
          </el-form-item>
        </el-form>
      </el-card>
    </div>

    <!-- 安全设置 -->
    <div v-if="activeTab === 'securitySettings'" class="settings-content">
      <el-card title="账户安全">
        <el-form :model="securitySettings" label-width="120px">
          <el-form-item label="密码策略" prop="passwordPolicy">
            <el-radio-group v-model="securitySettings.passwordPolicy">
              <el-radio :label="'simple'">简单（至少6位字符）</el-radio>
              <el-radio :label="'medium'">中等（至少8位，包含字母和数字）</el-radio>
              <el-radio :label="'strong'">强（至少10位，包含大小写字母、数字和特殊字符）</el-radio>
            </el-radio-group>
          </el-form-item>
          <el-form-item label="密码过期时间（天）" prop="passwordExpiryDays">
            <el-input-number v-model="securitySettings.passwordExpiryDays" :min="0" :max="365" />
            <div class="el-form-item__error">0表示永不过期</div>
          </el-form-item>
          <el-form-item label="登录失败次数限制" prop="loginAttemptsLimit">
            <el-input-number v-model="securitySettings.loginAttemptsLimit" :min="0" :max="10" />
            <div class="el-form-item__error">0表示无限制</div>
          </el-form-item>
          <el-form-item label="自动锁定时间（分钟）" prop="autoLockoutTime">
            <el-input-number v-model="securitySettings.autoLockoutTime" :min="5" :max="120" />
          </el-form-item>
          <el-form-item label="启用双因素认证" prop="enableTwoFactorAuth">
            <el-switch v-model="securitySettings.enableTwoFactorAuth" />
          </el-form-item>
        </el-form>
      </el-card>

      <el-card title="数据备份" class="mt-4">
        <el-form :model="backupSettings" label-width="120px">
          <el-form-item label="自动备份频率" prop="backupFrequency">
            <el-select v-model="backupSettings.backupFrequency" placeholder="请选择自动备份频率">
              <el-option label="不自动备份" value="never" />
              <el-option label="每天" value="daily" />
              <el-option label="每周" value="weekly" />
              <el-option label="每月" value="monthly" />
            </el-select>
          </el-form-item>
          <el-form-item label="备份保留数量" prop="backupRetention">
            <el-input-number v-model="backupSettings.backupRetention" :min="1" :max="30" />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="createBackup">立即备份</el-button>
            <el-button type="danger" @click="restoreFromBackup">从备份恢复</el-button>
          </el-form-item>
        </el-form>
      </el-card>

      <el-card title="日志记录" class="mt-4">
        <el-form :model="logSettings" label-width="120px">
          <el-form-item label="日志级别" prop="logLevel">
            <el-select v-model="logSettings.logLevel" placeholder="请选择日志级别">
              <el-option label="错误" value="error" />
              <el-option label="警告" value="warn" />
              <el-option label="信息" value="info" />
              <el-option label="调试" value="debug" />
            </el-select>
          </el-form-item>
          <el-form-item label="日志保留时间（天）" prop="logRetentionDays">
            <el-input-number v-model="logSettings.logRetentionDays" :min="1" :max="365" />
          </el-form-item>
          <el-form-item>
            <el-button @click="viewSystemLogs">查看系统日志</el-button>
          </el-form-item>
        </el-form>
      </el-card>
    </div>

    <!-- 通知设置 -->
    <div v-if="activeTab === 'notificationSettings'" class="settings-content">
      <el-card title="通知方式">
        <el-form :model="notificationMethods" label-width="120px">
          <el-form-item label="启用邮件通知" prop="enableEmail">
            <el-switch v-model="notificationMethods.enableEmail" />
          </el-form-item>
          <el-form-item label="启用短信通知" prop="enableSms">
            <el-switch v-model="notificationMethods.enableSms" />
          </el-form-item>
          <el-form-item label="启用微信通知" prop="enableWechat">
            <el-switch v-model="notificationMethods.enableWechat" />
          </el-form-item>
          <el-form-item label="启用站内通知" prop="enableInApp">
            <el-switch v-model="notificationMethods.enableInApp" />
          </el-form-item>
        </el-form>
      </el-card>

      <el-card title="通知内容设置" class="mt-4">
        <el-form :model="notificationContents" label-width="120px">
          <el-form-item label="支付提醒" prop="paymentReminder">
            <el-switch v-model="notificationContents.paymentReminder" />
          </el-form-item>
          <el-form-item label="维修进度通知" prop="maintenanceStatus">
            <el-switch v-model="notificationContents.maintenanceStatus" />
          </el-form-item>
          <el-form-item label="公告通知" prop="announcement">
            <el-switch v-model="notificationContents.announcement" />
          </el-form-item>
          <el-form-item label="系统更新通知" prop="systemUpdate">
            <el-switch v-model="notificationContents.systemUpdate" />
          </el-form-item>
          <el-form-item label="安全提醒" prop="securityAlert">
            <el-switch v-model="notificationContents.securityAlert" />
          </el-form-item>
        </el-form>
      </el-card>

      <el-card title="邮件服务器配置" class="mt-4">
        <el-form :model="emailServerConfig" label-width="120px">
          <el-form-item label="SMTP服务器" prop="smtpServer">
            <el-input v-model="emailServerConfig.smtpServer" placeholder="请输入SMTP服务器地址" />
          </el-form-item>
          <el-form-item label="SMTP端口" prop="smtpPort">
            <el-input-number v-model="emailServerConfig.smtpPort" :min="1" :max="65535" />
          </el-form-item>
          <el-form-item label="发件人邮箱" prop="senderEmail">
            <el-input v-model="emailServerConfig.senderEmail" placeholder="请输入发件人邮箱" />
          </el-form-item>
          <el-form-item label="邮箱密码" prop="emailPassword">
            <el-input v-model="emailServerConfig.emailPassword" type="password" placeholder="请输入邮箱密码" />
          </el-form-item>
          <el-form-item label="启用SSL/TLS" prop="enableSsl">
            <el-switch v-model="emailServerConfig.enableSsl" />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="testEmailConfig">测试配置</el-button>
          </el-form-item>
        </el-form>
      </el-card>
    </div>

    <!-- 外观设置 -->
    <div v-if="activeTab === 'appearanceSettings'" class="settings-content">
      <el-card title="主题设置">
        <el-form :model="themeSettings" label-width="120px">
          <el-form-item label="系统主题" prop="theme">
            <el-select v-model="themeSettings.theme" placeholder="请选择系统主题">
              <el-option label="默认主题" value="default" />
              <el-option label="暗黑主题" value="dark" />
              <el-option label="自定义主题" value="custom" />
            </el-select>
          </el-form-item>
          <el-form-item label="主题颜色" prop="themeColor" v-if="themeSettings.theme === 'custom'">
            <el-color-picker v-model="themeSettings.themeColor" />
          </el-form-item>
          <el-form-item label="菜单布局" prop="menuLayout">
            <el-radio-group v-model="themeSettings.menuLayout">
              <el-radio :label="'side'">侧边栏</el-radio>
              <el-radio :label="'top'">顶部导航</el-radio>
              <el-radio :label="'mix'">混合布局</el-radio>
            </el-radio-group>
          </el-form-item>
        </el-form>
      </el-card>

      <el-card title="显示设置" class="mt-4">
        <el-form :model="displaySettings" label-width="120px">
          <el-form-item label="语言" prop="language">
            <el-select v-model="displaySettings.language" placeholder="请选择语言">
              <el-option label="简体中文" value="zh-CN" />
              <el-option label="English" value="en-US" />
            </el-select>
          </el-form-item>
          <el-form-item label="时区" prop="timezone">
            <el-select v-model="displaySettings.timezone" placeholder="请选择时区">
              <el-option label="中国标准时间 (UTC+8)" value="Asia/Shanghai" />
              <el-option label="UTC" value="UTC" />
            </el-select>
          </el-form-item>
          <el-form-item label="日期格式" prop="dateFormat">
            <el-select v-model="displaySettings.dateFormat" placeholder="请选择日期格式">
              <el-option label="YYYY-MM-DD" value="yyyy-MM-dd" />
              <el-option label="DD/MM/YYYY" value="dd/MM/yyyy" />
              <el-option label="MM/DD/YYYY" value="MM/dd/yyyy" />
            </el-select>
          </el-form-item>
          <el-form-item label="时间格式" prop="timeFormat">
            <el-radio-group v-model="displaySettings.timeFormat">
              <el-radio :label="'24h'">24小时制</el-radio>
              <el-radio :label="'12h'">12小时制</el-radio>
            </el-radio-group>
          </el-form-item>
        </el-form>
      </el-card>

      <el-card title="首页设置" class="mt-4">
        <el-form :model="homepageSettings" label-width="120px">
          <el-form-item label="默认首页" prop="defaultHomepage">
            <el-select v-model="homepageSettings.defaultHomepage" placeholder="请选择默认首页">
              <el-option label="仪表盘" value="/dashboard" />
              <el-option label="用户管理" value="/users" />
              <el-option label="物业信息" value="/properties" />
              <el-option label="业主管理" value="/owners" />
            </el-select>
          </el-form-item>
          <el-form-item label="显示快捷入口" prop="showQuickAccess">
            <el-switch v-model="homepageSettings.showQuickAccess" />
          </el-form-item>
          <el-form-item label="显示最近活动" prop="showRecentActivities">
            <el-switch v-model="homepageSettings.showRecentActivities" />
          </el-form-item>
        </el-form>
      </el-card>
    </div>

    <!-- 确认对话框 -->
    <el-dialog
      v-model="confirmDialogVisible"
      title="确认操作"
      width="400px"
    >
      <p>{{ confirmMessage }}</p>
      <template #footer>
        <el-button @click="confirmDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleConfirm">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: 'SystemSettingsView',
  data() {
    return {
      activeTab: 'basicSettings',
      confirmDialogVisible: false,
      confirmMessage: '',
      confirmAction: null,
      
      // 系统基本信息
      systemInfo: {
        systemName: '物业管理系统',
        systemVersion: '1.0.0',
        systemDescription: '物业管理系统后台管理界面',
        systemLogo: ''
      },
      
      // 联系信息
      contactInfo: {
        supportPhone: '400-123-4567',
        supportEmail: 'support@example.com',
        workHours: '周一至周五 9:00-18:00',
        address: '北京市朝阳区建国路88号'
      },
      
      // 支付配置
      paymentConfig: {
        defaultPaymentMethod: 'wechat',
        enableOnlinePayment: true,
        paymentExpiryDays: 7
      },
      
      // 安全设置
      securitySettings: {
        passwordPolicy: 'medium',
        passwordExpiryDays: 90,
        loginAttemptsLimit: 5,
        autoLockoutTime: 30,
        enableTwoFactorAuth: false
      },
      
      // 备份设置
      backupSettings: {
        backupFrequency: 'weekly',
        backupRetention: 5
      },
      
      // 日志设置
      logSettings: {
        logLevel: 'info',
        logRetentionDays: 30
      },
      
      // 通知方式
      notificationMethods: {
        enableEmail: true,
        enableSms: false,
        enableWechat: true,
        enableInApp: true
      },
      
      // 通知内容设置
      notificationContents: {
        paymentReminder: true,
        maintenanceStatus: true,
        announcement: true,
        systemUpdate: true,
        securityAlert: true
      },
      
      // 邮件服务器配置
      emailServerConfig: {
        smtpServer: 'smtp.example.com',
        smtpPort: 465,
        senderEmail: 'notifications@example.com',
        emailPassword: '',
        enableSsl: true
      },
      
      // 主题设置
      themeSettings: {
        theme: 'default',
        themeColor: '#409EFF',
        menuLayout: 'side'
      },
      
      // 显示设置
      displaySettings: {
        language: 'zh-CN',
        timezone: 'Asia/Shanghai',
        dateFormat: 'yyyy-MM-dd',
        timeFormat: '24h'
      },
      
      // 首页设置
      homepageSettings: {
        defaultHomepage: '/dashboard',
        showQuickAccess: true,
        showRecentActivities: true
      },
      
      // 原始设置备份，用于重置
      originalSettings: null
    }
  },
  mounted() {
    // 保存原始设置，用于重置
    this.backupOriginalSettings()
    
    // 尝试从本地存储加载设置
    this.loadSettingsFromStorage()
  },
  methods: {
    // 备份原始设置
    backupOriginalSettings() {
      this.originalSettings = {
        systemInfo: { ...this.systemInfo },
        contactInfo: { ...this.contactInfo },
        paymentConfig: { ...this.paymentConfig },
        securitySettings: { ...this.securitySettings },
        backupSettings: { ...this.backupSettings },
        logSettings: { ...this.logSettings },
        notificationMethods: { ...this.notificationMethods },
        notificationContents: { ...this.notificationContents },
        emailServerConfig: { ...this.emailServerConfig },
        themeSettings: { ...this.themeSettings },
        displaySettings: { ...this.displaySettings },
        homepageSettings: { ...this.homepageSettings }
      }
    },
    
    // 从本地存储加载设置
    loadSettingsFromStorage() {
      try {
        const savedSettings = localStorage.getItem('systemSettings')
        if (savedSettings) {
          const parsedSettings = JSON.parse(savedSettings)
          
          // 合并保存的设置
          this.systemInfo = { ...this.systemInfo, ...parsedSettings.systemInfo }
          this.contactInfo = { ...this.contactInfo, ...parsedSettings.contactInfo }
          this.paymentConfig = { ...this.paymentConfig, ...parsedSettings.paymentConfig }
          this.securitySettings = { ...this.securitySettings, ...parsedSettings.securitySettings }
          this.backupSettings = { ...this.backupSettings, ...parsedSettings.backupSettings }
          this.logSettings = { ...this.logSettings, ...parsedSettings.logSettings }
          this.notificationMethods = { ...this.notificationMethods, ...parsedSettings.notificationMethods }
          this.notificationContents = { ...this.notificationContents, ...parsedSettings.notificationContents }
          this.emailServerConfig = { ...this.emailServerConfig, ...parsedSettings.emailServerConfig }
          this.themeSettings = { ...this.themeSettings, ...parsedSettings.themeSettings }
          this.displaySettings = { ...this.displaySettings, ...parsedSettings.displaySettings }
          this.homepageSettings = { ...this.homepageSettings, ...parsedSettings.homepageSettings }
          
          // 应用主题设置
          this.applyThemeSettings()
        }
      } catch (error) {
        console.error('加载设置失败:', error)
        this.$message.error('加载设置失败')
      }
    },
    
    // 保存设置
    saveSettings() {
      try {
        const settingsToSave = {
          systemInfo: { ...this.systemInfo },
          contactInfo: { ...this.contactInfo },
          paymentConfig: { ...this.paymentConfig },
          securitySettings: { ...this.securitySettings },
          backupSettings: { ...this.backupSettings },
          logSettings: { ...this.logSettings },
          notificationMethods: { ...this.notificationMethods },
          notificationContents: { ...this.notificationContents },
          emailServerConfig: { ...this.emailServerConfig },
          themeSettings: { ...this.themeSettings },
          displaySettings: { ...this.displaySettings },
          homepageSettings: { ...this.homepageSettings }
        }
        
        // 在实际应用中，这里应该发送请求到后端保存设置
        // 这里简单模拟保存到本地存储
        localStorage.setItem('systemSettings', JSON.stringify(settingsToSave))
        
        // 应用主题设置
        this.applyThemeSettings()
        
        this.$message.success('设置保存成功')
      } catch (error) {
        console.error('保存设置失败:', error)
        this.$message.error('保存设置失败')
      }
    },
    
    // 重置为默认设置
    resetSettings() {
      this.confirmDialogVisible = true
      this.confirmMessage = '确定要重置所有设置为默认值吗？这将丢失您当前的所有设置。'
      this.confirmAction = () => {
        if (this.originalSettings) {
          this.systemInfo = { ...this.originalSettings.systemInfo }
          this.contactInfo = { ...this.originalSettings.contactInfo }
          this.paymentConfig = { ...this.originalSettings.paymentConfig }
          this.securitySettings = { ...this.originalSettings.securitySettings }
          this.backupSettings = { ...this.originalSettings.backupSettings }
          this.logSettings = { ...this.originalSettings.logSettings }
          this.notificationMethods = { ...this.originalSettings.notificationMethods }
          this.notificationContents = { ...this.originalSettings.notificationContents }
          this.emailServerConfig = { ...this.originalSettings.emailServerConfig }
          this.themeSettings = { ...this.originalSettings.themeSettings }
          this.displaySettings = { ...this.originalSettings.displaySettings }
          this.homepageSettings = { ...this.originalSettings.homepageSettings }
          
          // 应用主题设置
          this.applyThemeSettings()
          
          this.$message.success('设置已重置为默认值')
        }
      }
    },
    
    // 应用主题设置
    applyThemeSettings() {
      // 这里简单模拟主题应用
      if (this.themeSettings.theme === 'dark') {
        document.body.classList.add('dark-theme')
      } else {
        document.body.classList.remove('dark-theme')
      }
      
      if (this.themeSettings.theme === 'custom' && this.themeSettings.themeColor) {
        // 设置主题颜色
        document.documentElement.style.setProperty('--theme-color', this.themeSettings.themeColor)
      }
      
      // 这里可以根据menuLayout设置调整菜单布局
      console.log('应用菜单布局:', this.themeSettings.menuLayout)
    },
    
    // 处理Logo上传成功
    handleLogoSuccess(response, file, fileList) {
      // 在实际应用中，这里应该处理上传成功后的逻辑
      // 这里简单模拟
      this.systemInfo.systemLogo = URL.createObjectURL(file.raw)
    },
    
    // 上传Logo前的验证
    beforeLogoUpload(file) {
      const isImage = file.type.startsWith('image/')
      const isLt2M = file.size / 1024 / 1024 < 2
      
      if (!isImage) {
        this.$message.error('上传的文件必须是图片')
      }
      if (!isLt2M) {
        this.$message.error('上传的图片大小不能超过2MB')
      }
      
      return isImage && isLt2M
    },
    
    // 立即备份
    createBackup() {
      this.confirmDialogVisible = true
      this.confirmMessage = '确定要立即创建数据备份吗？备份过程可能需要一些时间。'
      this.confirmAction = () => {
        // 在实际应用中，这里应该发送请求到后端创建备份
        this.$message.success('数据备份已开始创建')
      }
    },
    
    // 从备份恢复
    restoreFromBackup() {
      this.confirmDialogVisible = true
      this.confirmMessage = '确定要从备份恢复数据吗？这将覆盖当前所有数据。'
      this.confirmAction = () => {
        // 在实际应用中，这里应该打开文件选择对话框让用户选择备份文件
        this.$message.success('数据恢复功能暂未实现')
      }
    },
    
    // 查看系统日志
    viewSystemLogs() {
      // 在实际应用中，这里应该打开系统日志页面
      this.$message.info('系统日志查看功能暂未实现')
    },
    
    // 测试邮件配置
    testEmailConfig() {
      // 在实际应用中，这里应该发送测试邮件
      this.$message.success('测试邮件已发送，请检查邮箱')
    },
    
    // 处理确认操作
    handleConfirm() {
      if (typeof this.confirmAction === 'function') {
        this.confirmAction()
      }
      this.confirmDialogVisible = false
    }
  }
}
</script>

<style scoped>
.system-settings-container {
  padding: 20px;
}

.operation-bar {
  margin-bottom: 20px;
}

.settings-content {
  margin-bottom: 20px;
}

.el-form-item__error {
  color: #606266;
  font-size: 12px;
  margin-top: 5px;
}

.avatar-uploader .el-upload {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  width: 150px;
  height: 150px;
}

.avatar-uploader .el-upload:hover {
  border-color: #409EFF;
}

.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 150px;
  height: 150px;
  line-height: 150px;
  text-align: center;
}

.avatar {
  width: 150px;
  height: 150px;
  display: block;
}
</style>