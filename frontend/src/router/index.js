import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '../stores/user'

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
router.beforeEach((to, from, next) => {
  const userStore = useUserStore()
  console.log('导航守卫触发', to.fullPath)
  console.log('用户登录状态', userStore.isLoggedIn)
  if (to.meta.requiresAuth && !userStore.isLoggedIn) {
    // 如果路由需要登录，且用户未登录，就跳到 /login
    next('/login')
  } else {
    next()
  }
})


export default router
