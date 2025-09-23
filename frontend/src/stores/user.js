// src/stores/user.js
import { defineStore } from "pinia"
import api from '@/utils/api'

export const useUserStore = defineStore("user", {
  state: () => ({
    user: null,        // 用户信息
    isLoggedIn: false, // 登录状态
    loading: false
  }),
  actions: {
    // 登录
    async login(credentials) {
      this.loading = true
      try {
        const res = await api.post("/auth/login", credentials, { withCredentials: true })
        if (res.data.code === 200) {
          this.user = res.data.data
          this.isLoggedIn = true
          return { success: true }
        }
        return { success: false, message: res.data.msg || "登录失败" }
      } catch (err) {
        return { success: false, message: err.response?.data?.msg || "登录失败" }
      } finally {
        this.loading = false
      }
    },

    // 注册
    async register(credentials) {
      this.loading = true
      try {
        const res = await api.post("/auth/register", credentials, { withCredentials: true })
        if (res.data.code === 200) {
          // 你可以决定注册成功是否直接登录
          this.user = res.data.data
          this.isLoggedIn = true
          return { success: true,message: "注册成功" }
        }
        return { success: false, message: res.data.msg || "注册失败" }
      } catch (err) {
        return { success: false, message: err.response?.data?.msg || "注册失败" }
      } finally {
        this.loading = false
      }
    },

    // 初始化用户状态（页面刷新后调用）
    async fetchCurrentUser() {
      this.loading = true
      try {
        const res = await api.get("/auth/me", { withCredentials: true })
        this.user = res.data.user
        this.isLoggedIn = true
      } catch {
        this.user = null
        this.isLoggedIn = false
      } finally {
        this.loading = false
      }
    },

    // 登出
    logout() {
      this.user = null
      this.isLoggedIn = false
      // 可调用后端登出接口清理 cookie
    }
  }
})

