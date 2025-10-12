<template>
  <div class="login-container">
    <div class="login-box">
      <!-- 品牌区域 -->
      <div class="brand-area">
        <img src="/vite.svg" alt="系统Logo" class="brand-logo" />
        <h1 class="brand-title">物业管理系统</h1>
      </div>
      
      <!-- 登录表单 -->
      <div class="form-area">
        <h2 class="form-title">用户登录</h2>
        <el-form :model="loginForm" :rules="rules" ref="loginFormRef" class="login-form">
          <el-form-item prop="username">
            <el-input v-model="loginForm.username" placeholder="请输入用户名" />
          </el-form-item>
          
          <el-form-item prop="password" class="password-item">
            <div class="password-container">
              <el-input v-model="loginForm.password" type="password" placeholder="请输入密码" />
              <div class="password-options">
                <el-checkbox v-model="rememberPassword" class="remember-password">记住密码</el-checkbox>
                <el-link type="primary" @click="handleForgotPassword" class="forgot-password">忘记密码？</el-link>
              </div>
            </div>
          </el-form-item>
          
          <el-form-item>
            <el-button type="primary" @click="handleLogin" class="login-button">登录</el-button>
          </el-form-item>
        </el-form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LoginView',
  data() {
    return {
      loginForm: {
        username: '',
        password: ''
      },
      rememberPassword: false,
      rules: {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' }
        ]
      }
    }
  },
  mounted() {
    // 检查是否有记住的密码
    this.checkRememberPassword()
  },
  methods: {
    handleLogin() {
      this.$refs.loginFormRef.validate((valid) => {
        if (valid) {
          // 模拟登录验证
          // 在实际应用中，这里应该发送请求到后端进行验证
          if (this.loginForm.username === 'admin' && this.loginForm.password === 'admin123') {
            // 存储模拟的token
            localStorage.setItem('token', 'mock-jwt-token')
            localStorage.setItem('userRole', 'admin')
            
            // 记住密码处理
            if (this.rememberPassword) {
              localStorage.setItem('rememberedUsername', this.loginForm.username)
              // 注意：在实际应用中，密码应该加密存储或不存储
              // 这里仅作为演示，实际项目中不应该明文存储密码
              localStorage.setItem('rememberedPassword', this.loginForm.password)
            } else {
              localStorage.removeItem('rememberedUsername')
              localStorage.removeItem('rememberedPassword')
            }
            
            // 登录成功后跳转到仪表盘
            this.$router.push({ name: 'dashboard' })
          } else {
            this.$message.error('用户名或密码错误')
          }
        }
      })
    },
    
    // 检查是否有记住的密码
    checkRememberPassword() {
      const rememberedUsername = localStorage.getItem('rememberedUsername')
      const rememberedPassword = localStorage.getItem('rememberedPassword')
      
      if (rememberedUsername && rememberedPassword) {
        this.loginForm.username = rememberedUsername
        this.loginForm.password = rememberedPassword
        this.rememberPassword = true
      }
    },
    
    // 处理忘记密码
    handleForgotPassword() {
      this.$message.info('忘记密码功能正在开发中')
      // 在实际应用中，这里应该跳转到忘记密码页面或显示忘记密码对话框
    }
  }
}
</script>

<style scoped>
/* 重置默认样式 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

/* 确保html和body占满整个视口 */
html, body {
  height: 100%;
  overflow: hidden;
  margin: 0;
  padding: 0;
}

/* 登录容器 - 确保完全覆盖整个视口 */
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  width: 100vw;
  background-color: #f0f2f5;
  background-image: 
    radial-gradient(circle at 10% 20%, rgba(64, 158, 255, 0.05) 0%, transparent 20%),
    radial-gradient(circle at 90% 80%, rgba(64, 158, 255, 0.08) 0%, transparent 30%);
  background-size: cover;
  background-attachment: fixed;
  position: fixed;
  top: 0;
  left: 0;
  z-index: 100;
}

/* 登录框 */
.login-box {
  animation: fadeIn 0.5s ease-in-out;
  border-radius: 16px;
  padding: 40px 50px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  background-color: #ffffff;
  max-width: 450px;
  width: 90%;
  min-width: 320px;
}

.login-box:hover {
  box-shadow: 0 15px 50px rgba(0, 0, 0, 0.15);
}

/* 淡入动画 */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 品牌区域 */
.brand-area {
  text-align: center;
  margin-bottom: 30px;
  padding-bottom: 25px;
  border-bottom: 1px solid var(--border-color);
}

.brand-logo {
  width: 64px;
  height: 64px;
  margin-bottom: 15px;
  transition: transform 0.3s ease;
}

.brand-logo:hover {
  transform: scale(1.05);
}

.brand-title {
  color: #333333;
  font-size: 28px;
  font-weight: 700;
  margin: 0;
  letter-spacing: -0.5px;
}

/* 表单区域 */
.form-area {
  width: 100%;
}

.form-title {
  text-align: center;
  color: #333333;
  font-weight: 600;
  margin-bottom: 30px;
  font-size: 22px;
}

/* 登录表单 */
.login-form {
  width: 100%;
  max-width: 400px;
  margin: 0 auto;
}

/* 表单项 */
.el-form-item {
  margin-bottom: 25px;
}

/* 密码项样式 */
.password-item {
  margin-bottom: 15px !important;
}

/* 密码容器样式 */
.password-container {
  position: relative;
  display: flex;
  flex-direction: column;
  width: 100%;
}

/* 密码选项容器 - 用于对齐记住密码和忘记密码 */
.password-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 10px;
}

/* 输入框 */
.el-input {
  width: 100%;
}

.el-input__inner {
  border-radius: 6px;
  border-color: var(--border-color);
  transition: all 0.3s ease;
  height: 40px;
  font-size: 14px;
  padding: 0 15px;
  width: 100%;
}

.el-input__inner:focus {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 2px rgba(64, 158, 255, 0.2);
}

/* 登录按钮 */
.login-button {
  width: 180px;
  height: 44px;
  font-size: 16px;
  font-weight: 600;
  border-radius: 6px;
  padding: 0;
  transition: all 0.3s ease;
  margin-top: 10px;
}

/* 记住密码 */
.remember-password {
  font-size: 14px;
  color: #606266;
  margin-bottom: 10px;
  width: fit-content;
}

/* 忘记密码 */
.forgot-password {
  font-size: 14px;
  color: var(--primary-color);
  cursor: pointer;
  margin-top: 8px;
  margin-bottom: 5px;
  transition: color 0.3s ease;
  align-self: flex-end;
  width: fit-content;
}

.forgot-password:hover {
  color: var(--primary-hover-color);
}

.el-button--primary {
  background-color: var(--primary-color);
  border-color: var(--primary-color);
}

.el-button--primary:hover {
  background-color: var(--primary-hover-color);
  border-color: var(--primary-hover-color);
  transform: translateY(-1px);
}

.el-button--primary:active {
  transform: translateY(0);
  background-color: var(--primary-active-color);
  border-color: var(--primary-active-color);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .login-box {
    margin: 0 20px;
    padding: 30px 25px;
    min-width: auto;
  }
  
  .brand-logo {
    width: 50px;
    height: 50px;
  }
  
  .brand-title {
    font-size: 24px;
  }
  
  .form-title {
    font-size: 20px;
  }
  
  .login-button {
    width: 150px;
    height: 40px;
    font-size: 14px;
  }
}
  </style>