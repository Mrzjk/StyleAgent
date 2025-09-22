// 智能体风格配置
export const AGENT_STYLES = {
  assistant: {
    name: '助手型',
    description: '专业、高效、准确',
    icon: 'User',
    color: '#409EFF',
    systemPrompt: '你是一个专业的AI助手，能够准确、高效地回答用户的问题。请保持专业和友好的态度。'
  },
  creative: {
    name: '创意型',
    description: '富有想象力、创新思维',
    icon: 'Star',
    color: '#F56C6C',
    systemPrompt: '你是一个富有创意的AI助手，善于从不同角度思考问题，能够提供创新性的解决方案和想法。'
  },
  technical: {
    name: '技术型',
    description: '逻辑清晰、技术专业',
    icon: 'Setting',
    color: '#67C23A',
    systemPrompt: '你是一个技术专家AI助手，擅长解决技术问题，能够提供详细的技术分析和解决方案。'
  },
  friendly: {
    name: '友好型',
    description: '亲切、幽默、易沟通',
    icon: 'ChatDotRound',
    color: '#E6A23C',
    systemPrompt: '你是一个友好、幽默的AI助手，善于与人交流，能够用轻松愉快的方式帮助用户解决问题。'
  }
}

// 常用标签
export const COMMON_TAGS = [
  '编程助手',
  '写作助手',
  '学习助手',
  '翻译助手',
  '创意助手',
  '技术顾问',
  '生活助手',
  '商务助手',
  '教育助手',
  '娱乐助手'
]

// 温度设置说明
export const TEMPERATURE_DESCRIPTIONS = {
  0.1: '非常保守，回答一致性强',
  0.3: '保守，回答相对稳定',
  0.5: '平衡，兼顾一致性和创造性',
  0.7: '平衡，适度创造性',
  0.9: '创新，回答多样化',
  1.0: '高度创新，回答变化很大'
}

// 消息类型
export const MESSAGE_TYPES = {
  USER: 'user',
  AGENT: 'agent',
  SYSTEM: 'system'
}

// 路由名称
export const ROUTE_NAMES = {
  LOGIN: 'Login',
  REGISTER: 'Register',
  DASHBOARD: 'Dashboard',
  CHAT: 'Chat',
  CREATE_AGENT: 'CreateAgent'
}
