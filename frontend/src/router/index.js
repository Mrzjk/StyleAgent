import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'

const routes = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue')
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/Register.vue')
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('@/views/Dashboard.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/chat/:agentId',
    name: 'Chat',
    component: () => import('@/views/Chat.vue'),
    meta: { requiresAuth: true }
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

//路由守卫
router.beforeEach(async (to, from, next) => {
  const userStore = useUserStore()
  
  // 如果访问需要认证的页面，先检查登录状态
  if (to.meta.requiresAuth) {
    // 如果store中还没有登录状态，尝试从后端获取
    if (!userStore.isLoggedIn) {
      try {
        await userStore.fetchCurrentUser()
      } catch (error) {
        // 获取用户信息失败，跳转到登录页
        console.log('未登录，跳转到登录页')
        console.log(error)
        next('/login')
        return
      }
    }
    
    // 检查登录状态
    if (!userStore.isLoggedIn) {
      console.log('用户未登录，跳转到登录页')
      next('/login')
      return
    }
  }
  
  // 如果已登录用户访问登录页，跳转到仪表板
  if ((to.name === 'Login' || to.name === 'Register') && userStore.isLoggedIn) {
    next('/dashboard')
    return
  }
  
  next()
})


export default router
