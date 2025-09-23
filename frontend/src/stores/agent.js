import { defineStore } from 'pinia'
import api from '@/utils/api'

export const useAgentsStore = defineStore('agents', {
  state: () => ({
    agents: [],
    currentAgent: null,
    chatHistory: []
  }),

  getters: {
    getAgentById: (state) => (id) => state.agents.find(agent => agent.id === id)
  },

  actions: {
    async fetchAgents() {
      try {
        const response = await api.get('/agent')
        console.log('获取智能体列表成功:', )
        this.agents = response.data.data
      } catch (error) {
        console.error('获取智能体列表失败:', error)
        return { success: false, message: error.message }
      }
    },

    async createAgent(agentData) {
      try {
        console.log('创建智能体:', agentData)
        const response = await api.post('/agent', agentData)
        this.agents.push(response.data)
        return { success: true, agent: response.data }
      } catch (error) {
        return { success: false, message: error.message }
      }
    },

    setCurrentAgent(agent) {
      this.currentAgent = agent
    },

    async sendMessage(message) {
      try {
        const response = await api.post('/chat', {
          agentId: this.currentAgent.id,
          message: message
        })
        
        this.chatHistory.push({
          id: Date.now(),
          type: 'user',
          content: message,
          timestamp: new Date()
        })
        
        this.chatHistory.push({
          id: Date.now() + 1,
          type: 'agent',
          content: response.data.reply,
          timestamp: new Date()
        })
        
        return { success: true }
      } catch (error) {
        return { success: false, message: error.message }
      }
    },

    clearChatHistory() {
      this.chatHistory = []
    },
    optimizeSystemPrompt(agent_info){
      return api.post('/optimize_system_prompt', agent_info)

    }
  }
})
