import { defineStore } from 'pinia'
import api from '@/utils/api'

export const useTagsStore = defineStore('tags', {
  state: () => ({
    tags: [],
    loading: false,
  }),
  actions: {
    async getTags() {
      this.loading = true
      try {
        // 根据后端实际路由调整，例如 /api/tags
        const res = await api.get('/tag', { withCredentials: true })
        // 兼容 { code, data } 或直接数组
        this.tags = Array.isArray(res.data) ? res.data : (res.data?.data || [])
        return this.tags
      } finally {
        this.loading = false
      }
    },
  },
})
