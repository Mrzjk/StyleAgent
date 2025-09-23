import { defineStore } from 'pinia'
import api from '@/utils/api'

export const useAgentCategories = defineStore('agentCategories', {
  state: () => ({
    categories: [],
    loading: false,
  }),
  actions: {
    async getAgentCategories() {
      this.loading = true
      try {
        // 根据后端实际路由调整，例如 /api/categories
        const res = await api.get('/category', { withCredentials: true })
        // 兼容 { code, data } 或直接数组
        this.categories = Array.isArray(res.data) ? res.data : (res.data?.data || [])
        return this.categories
      } finally {
        this.loading = false
      }
    },
  },
})
