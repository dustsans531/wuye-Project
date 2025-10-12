// 导入Vue核心
import { createApp } from 'vue'
import './style.css'
import App from './App.vue'

// 导入Element Plus及其样式
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

// 导入Bootstrap CSS
import 'bootstrap/dist/css/bootstrap.min.css'

// 导入Bootstrap JS (需要Popper.js)
import 'bootstrap/dist/js/bootstrap.bundle.min.js'

// 导入Axios
import axios from 'axios'

// 导入路由配置
import router from './router'

// 创建应用
const app = createApp(App)

// 使用Element Plus
app.use(ElementPlus)

// 使用路由
app.use(router)

// 配置Axios全局属性
app.config.globalProperties.$axios = axios

// 配置Axios基础URL
axios.defaults.baseURL = 'http://localhost:5000/api' // Flask默认端口

// 添加请求拦截器
axios.interceptors.request.use(
  function (config) {
    // 在发送请求之前做些什么，例如添加token
    const token = localStorage.getItem('token')
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`
    }
    return config
  },
  function (error) {
    // 对请求错误做些什么
    return Promise.reject(error)
  }
)

// 添加响应拦截器
axios.interceptors.response.use(
  function (response) {
    // 对响应数据做点什么
    return response
  },
  function (error) {
    // 对响应错误做点什么
    if (error.response && error.response.status === 401) {
      // 未授权，跳转到登录页面
      localStorage.removeItem('token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// 挂载应用
app.mount('#app')
