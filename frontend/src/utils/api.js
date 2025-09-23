import axios from 'axios'

// 创建axios实例
const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    // 登录和注册接口不需要带 token
    if (config.url === '/api/auth/login' || config.url === '/api/auth/register') return config

    // 不再从 localStorage 取 token，cookie 会自动携带
    // axios 配置了 withCredentials 后，浏览器会自动带上 cookie
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    if (error.response?.status === 401) {
      // 401错误不自动跳转，让组件自己处理
      console.log('API请求返回401，需要重新登录')
    }
    return Promise.reject(error)
  }
)

export default api
