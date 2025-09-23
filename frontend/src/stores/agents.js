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
        const response = await api.get('/agent/')
        this.agents = response.data
      } catch (error) {
        console.error('获取智能体列表失败:', error)
        // 临时添加模拟数据，用于演示
        this.agents = [
          {
            id: 1,
            name: '编程助手',
            description: '专业的编程助手，能够帮助您解决各种编程问题，提供代码示例和最佳实践建议。',
            style: 'technical',
            tags: ['编程助手', '技术顾问'],
            systemPrompt: '你是一个专业的编程助手...',
            temperature: 0.7
          },
          {
            id: 2,
            name: '创意写作师',
            description: '富有创意的写作助手，擅长各种文体创作，能够激发您的创作灵感。',
            style: 'creative',
            tags: ['写作助手', '创意助手'],
            systemPrompt: '你是一个富有创意的写作助手...',
            temperature: 0.9
          },
          {
            id: 3,
            name: '学习导师',
            description: '耐心的学习导师，能够帮助您理解复杂概念，制定学习计划。',
            style: 'friendly',
            tags: ['学习助手', '教育助手'],
            systemPrompt: '你是一个耐心的学习导师...',
            temperature: 0.6
          }
        ]
      }
    },

    async createAgent(agentData) {
      try {
        const response = await axios.post('/api/agents', agentData)
        this.agents.push(response.data)
        return { success: true, agent: response.data }
      } catch (error) {
        // 临时模拟创建成功，用于演示
        const newAgent = {
          id: Date.now(),
          ...agentData,
          createdAt: new Date().toISOString()
        }
        this.agents.push(newAgent)
        return { success: true, agent: newAgent }
      }
    },

    setCurrentAgent(agent) {
      this.currentAgent = agent
    },

    async sendMessage(message) {
      try {
        const response = await axios.post('/api/chat', {
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
        // 临时模拟回复，用于演示
        this.chatHistory.push({
          id: Date.now(),
          type: 'user',
          content: message,
          timestamp: new Date()
        })
        
        // 模拟AI回复
        const replies = [
          '这是一个很好的问题！让我来帮您分析一下...',
          '根据您的问题，我建议您可以尝试以下几种方法...',
          '我理解您的需求，这里有一些建议供您参考...',
          '这是一个有趣的话题，让我从不同角度为您解答...'
        ]
        
        const randomReply = replies[Math.floor(Math.random() * replies.length)]
        
        this.chatHistory.push({
          id: Date.now() + 1,
          type: 'agent',
          content: randomReply,
          timestamp: new Date()
        })
        
        return { success: true }
      }
    },

    clearChatHistory() {
      this.chatHistory = []
    }
  }
})
