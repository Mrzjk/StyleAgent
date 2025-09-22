<template>
  <div class="chat-container">
    <header class="chat-header">
      <div class="header-left">
        <el-button 
          type="text" 
          @click="goBack"
          class="back-btn"
        >
          <el-icon><ArrowLeft /></el-icon>
          返回
        </el-button>
        <div class="agent-info">
          <div class="agent-avatar">
            <el-icon :size="24">
              <component :is="getAgentIcon(agentsStore.currentAgent?.style)" />
            </el-icon>
          </div>
          <div class="agent-details">
            <h3>{{ agentsStore.currentAgent?.name }}</h3>
            <p>{{ agentsStore.currentAgent?.description }}</p>
          </div>
        </div>
      </div>
      <div class="header-right">
        <el-button 
          type="text" 
          @click="clearChat"
          :disabled="agentsStore.chatHistory.length === 0"
        >
          <el-icon><Delete /></el-icon>
          清空对话
        </el-button>
      </div>
    </header>

    <main class="chat-main">
      <div class="chat-messages" ref="messagesContainer">
        <div v-if="agentsStore.chatHistory.length === 0" class="empty-chat">
          <div class="empty-content">
            <el-icon :size="60" color="#ccc"><ChatDotRound /></el-icon>
            <h3>开始对话</h3>
            <p>向 {{ agentsStore.currentAgent?.name }} 发送消息开始聊天</p>
          </div>
        </div>
        
        <div 
          v-for="message in agentsStore.chatHistory" 
          :key="message.id"
          class="message-item"
          :class="{ 'user-message': message.type === 'user', 'agent-message': message.type === 'agent' }"
        >
          <div class="message-avatar">
            <el-icon v-if="message.type === 'user'"><User /></el-icon>
            <el-icon v-else><component :is="getAgentIcon(agentsStore.currentAgent?.style)" /></el-icon>
          </div>
          <div class="message-content">
            <div class="message-bubble">
              <div class="message-text" v-html="formatMessage(message.content)"></div>
              <div class="message-time">{{ formatTime(message.timestamp) }}</div>
            </div>
          </div>
        </div>
        
        <div v-if="loading" class="message-item agent-message">
          <div class="message-avatar">
            <el-icon><component :is="getAgentIcon(agentsStore.currentAgent?.style)" /></el-icon>
          </div>
          <div class="message-content">
            <div class="message-bubble">
              <div class="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>

    <footer class="chat-footer">
      <div class="input-container">
        <el-input
          v-model="inputMessage"
          type="textarea"
          :rows="1"
          :autosize="{ minRows: 1, maxRows: 4 }"
          placeholder="输入消息..."
          @keydown.enter.exact.prevent="handleSendMessage"
          @keydown.enter.shift.exact="inputMessage += '\n'"
          :disabled="loading"
        />
        <el-button 
          type="primary" 
          @click="handleSendMessage"
          :loading="loading"
          :disabled="!inputMessage.trim()"
          class="send-btn"
        >
          <el-icon><Promotion /></el-icon>
        </el-button>
      </div>
    </footer>
  </div>
</template>

<script>
import { ref, onMounted, nextTick, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { ArrowLeft, Delete, ChatDotRound, User, Promotion } from '@element-plus/icons-vue'
import { useAgentsStore } from '../stores/agents'

export default {
  name: 'Chat',
  setup() {
    const route = useRoute()
    const router = useRouter()
    const agentsStore = useAgentsStore()
    const inputMessage = ref('')
    const loading = ref(false)
    const messagesContainer = ref()

    const agentIcons = {
      'assistant': User,
      'creative': 'Star',
      'technical': 'Setting',
      'friendly': ChatDotRound,
      'default': 'Robot'
    }

    const getAgentIcon = (style) => {
      return agentIcons[style] || agentIcons.default
    }

    const formatMessage = (content) => {
      // 简单的markdown格式化
      return content
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        .replace(/`(.*?)`/g, '<code>$1</code>')
        .replace(/\n/g, '<br>')
    }

    const formatTime = (timestamp) => {
      return new Date(timestamp).toLocaleTimeString('zh-CN', {
        hour: '2-digit',
        minute: '2-digit'
      })
    }

    const scrollToBottom = () => {
      nextTick(() => {
        if (messagesContainer.value) {
          messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
        }
      })
    }

    const handleSendMessage = async () => {
      if (!inputMessage.value.trim() || loading.value) return

      const message = inputMessage.value.trim()
      inputMessage.value = ''
      loading.value = true

      const result = await agentsStore.sendMessage(message)
      loading.value = false

      if (!result.success) {
        ElMessage.error(result.message)
      }

      scrollToBottom()
    }

    const clearChat = async () => {
      try {
        await ElMessageBox.confirm('确定要清空对话记录吗？', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        })
        agentsStore.clearChatHistory()
        ElMessage.success('对话记录已清空')
      } catch {
        // 用户取消
      }
    }

    const goBack = () => {
      router.push('/dashboard')
    }

    // 监听聊天历史变化，自动滚动到底部
    watch(() => agentsStore.chatHistory, () => {
      scrollToBottom()
    }, { deep: true })

    onMounted(async () => {
      const agentId = route.params.agentId
      if (agentId) {
        const agent = agentsStore.getAgentById(agentId)
        if (agent) {
          agentsStore.setCurrentAgent(agent)
        } else {
          ElMessage.error('智能体不存在')
          router.push('/dashboard')
        }
      }
      scrollToBottom()
    })

    return {
      agentsStore,
      inputMessage,
      loading,
      messagesContainer,
      getAgentIcon,
      formatMessage,
      formatTime,
      handleSendMessage,
      clearChat,
      goBack
    }
  }
}
</script>

<style scoped>
.chat-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: #f5f7fa;
}

.chat-header {
  background: white;
  padding: 15px 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 20px;
}

.back-btn {
  color: #667eea;
  font-weight: 500;
}

.agent-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.agent-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.agent-details h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

.agent-details p {
  margin: 0;
  font-size: 12px;
  color: #666;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 15px;
}

.chat-main {
  flex: 1;
  overflow: hidden;
}

.chat-messages {
  height: 100%;
  overflow-y: auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.empty-chat {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.empty-content {
  text-align: center;
  color: #999;
}

.empty-content h3 {
  margin: 20px 0 10px;
  color: #666;
  font-size: 20px;
}

.empty-content p {
  color: #999;
  font-size: 14px;
}

.message-item {
  display: flex;
  gap: 12px;
  max-width: 80%;
}

.user-message {
  align-self: flex-end;
  flex-direction: row-reverse;
}

.agent-message {
  align-self: flex-start;
}

.message-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.user-message .message-avatar {
  background: #667eea;
  color: white;
}

.agent-message .message-avatar {
  background: #e8f4fd;
  color: #667eea;
}

.message-content {
  flex: 1;
}

.message-bubble {
  background: white;
  border-radius: 18px;
  padding: 12px 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  position: relative;
}

.user-message .message-bubble {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.message-text {
  line-height: 1.5;
  word-wrap: break-word;
}

.message-time {
  font-size: 11px;
  opacity: 0.7;
  margin-top: 4px;
  text-align: right;
}

.user-message .message-time {
  text-align: left;
}

.typing-indicator {
  display: flex;
  gap: 4px;
  align-items: center;
}

.typing-indicator span {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #ccc;
  animation: typing 1.4s infinite ease-in-out;
}

.typing-indicator span:nth-child(1) {
  animation-delay: -0.32s;
}

.typing-indicator span:nth-child(2) {
  animation-delay: -0.16s;
}

@keyframes typing {
  0%, 80%, 100% {
    transform: scale(0.8);
    opacity: 0.5;
  }
  40% {
    transform: scale(1);
    opacity: 1;
  }
}

.chat-footer {
  background: white;
  padding: 15px 20px;
  box-shadow: 0 -2px 8px rgba(0, 0, 0, 0.1);
}

.input-container {
  display: flex;
  gap: 12px;
  align-items: flex-end;
  max-width: 800px;
  margin: 0 auto;
}

.send-btn {
  height: 40px;
  width: 40px;
  border-radius: 50%;
  padding: 0;
}

:deep(.el-textarea__inner) {
  border-radius: 20px;
  border: 1px solid #e4e7ed;
  resize: none;
}

:deep(.el-textarea__inner:focus) {
  border-color: #667eea;
}

:deep(.el-input__count) {
  color: #999;
  font-size: 12px;
}

/* 滚动条样式 */
.chat-messages::-webkit-scrollbar {
  width: 6px;
}

.chat-messages::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.chat-messages::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.chat-messages::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}
</style>
