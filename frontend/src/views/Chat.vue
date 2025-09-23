<template>
  <div class="chat-page">
    <!-- Top Navbar -->
    <header class="top-navbar">
      <div class="navbar-inner">
        <div class="brand" @click="goDashboard">
          <span class="brand-logo">🤖</span>
          <span class="brand-name">AI 智能体对话</span>
        </div>
        <div class="nav-actions">
          <div class="user-box" v-if="userStore.isLoggedIn && userStore.user">
            <div class="user-avatar">{{ (userStore.user.username || '用户').slice(0,1).toUpperCase() }}</div>
            <div class="user-meta">
              <div class="user-name">{{ userStore.user.username }}</div>
              <div class="user-email" v-if="userStore.user.email">{{ userStore.user.email }}</div>
            </div>
          </div>
          <el-button type="primary" text @click="goDashboard">
            返回仪表板
          </el-button>
        </div>
      </div>
    </header>

    <div class="chat-layout">
      <!-- Sidebar -->
      <aside class="chat-sidebar">
        <div class="sidebar-header">
          <el-button type="primary" class="new-chat-btn" @click="newConversation">
            <el-icon><ChatLineRound /></el-icon>
            新对话
          </el-button>
        </div>
        <div class="sidebar-section">
          <div class="section-title">我的智能体</div>
          <div class="agent-list" v-loading="sidebarLoading">
            <div 
              v-for="agent in agentsStore.agents" 
              :key="agent.id"
              class="agent-item"
              :class="{ active: agentsStore.currentAgent && agentsStore.currentAgent.id === agent.id }"
              @click="switchAgent(agent)"
            >
              <div class="agent-icon">
                <el-icon><component :is="getAgentIcon(agent.style)" /></el-icon>
              </div>
              <div class="agent-meta">
                <div class="agent-name">{{ agent.name }}</div>
                <div class="agent-desc">{{ agent.description }}</div>
              </div>
            </div>
          </div>
        </div>
      </aside>

      <!-- Main Chat Area -->
      <section class="chat-main">
        <!-- Header -->
        <header class="chat-header">
          <div class="agent-header" v-if="agentsStore.currentAgent">
            <div class="agent-avatar">
              <el-icon :size="22"><component :is="getAgentIcon(agentsStore.currentAgent.style)" /></el-icon>
            </div>
            <div class="agent-title">
              <h3>{{ agentsStore.currentAgent.name }}</h3>
              <p>{{ agentsStore.currentAgent.description }}</p>
            </div>
          </div>
          <div class="header-actions">
            <el-button text :disabled="agentsStore.chatHistory.length === 0" @click="clearChat">
              <el-icon><Delete /></el-icon>
              清空对话
            </el-button>
          </div>
        </header>

        <!-- Messages -->
        <main class="messages" ref="messagesContainer">
          <div v-if="agentsStore.chatHistory.length === 0" class="empty-state">
            <div class="empty-logo">
              <el-icon :size="56"><ChatDotRound /></el-icon>
            </div>
            <h2>开始与 {{ agentsStore.currentAgent?.name || '智能体' }} 对话</h2>
            <p>提出问题或描述任务，按 Enter 发送。Shift+Enter 换行。</p>
          </div>

          <div 
            v-for="message in agentsStore.chatHistory" 
            :key="message.id"
            class="message-row"
            :class="{ 'is-user': message.type === 'user', 'is-agent': message.type === 'agent' }"
          >
            <div class="message-avatar" :class="message.type">
              <el-icon v-if="message.type === 'user'"><User /></el-icon>
              <el-icon v-else><component :is="getAgentIcon(agentsStore.currentAgent?.style)" /></el-icon>
            </div>
            <div class="message-bubble">
              <div class="markdown-body" v-html="renderMarkdown(message.content)"></div>
              <div class="message-time">{{ formatTime(message.timestamp) }}</div>
            </div>
          </div>

          <div v-if="loading" class="message-row is-agent">
            <div class="message-avatar agent">
              <el-icon><component :is="getAgentIcon(agentsStore.currentAgent?.style)" /></el-icon>
            </div>
            <div class="message-bubble">
              <div class="typing-indicator">
                <span></span><span></span><span></span>
              </div>
            </div>
          </div>
        </main>

        <!-- Composer -->
        <footer class="composer">
          <div class="composer-inner">
            <el-input
              v-model="inputMessage"
              type="textarea"
              :rows="1"
              :autosize="{ minRows: 1, maxRows: 8 }"
              placeholder="给智能体发送一条消息..."
              @keydown.enter.exact.prevent="handleSendMessage"
              @keydown.enter.shift.exact="inputMessage += '\n'"
              :disabled="loading || !agentsStore.currentAgent"
            />
            <el-button 
              type="primary" 
              class="send-btn"
              :disabled="!inputMessage.trim() || !agentsStore.currentAgent"
              :loading="loading"
              @click="handleSendMessage"
              circle
            >
              <el-icon><Promotion /></el-icon>
            </el-button>
          </div>
          <div class="composer-hint">Enter 发送 · Shift + Enter 换行</div>
        </footer>
      </section>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, nextTick, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { ArrowLeft, Delete, ChatDotRound, User, Promotion, ChatLineRound, Star, Setting } from '@element-plus/icons-vue'
import { useAgentsStore } from '@/stores/agent'
import { useUserStore } from '@/stores/user'

export default {
  name: 'Chat',
  setup() {
    const route = useRoute()
    const router = useRouter()
    const agentsStore = useAgentsStore()
    const userStore = useUserStore()
    const inputMessage = ref('')
    const loading = ref(false)
    const messagesContainer = ref()
    const sidebarLoading = ref(false)

    const agentIcons = {
      'assistant': User,
      'creative': Star,
      'technical': Setting,
      'friendly': ChatDotRound,
      'default': ChatDotRound
    }

    const getAgentIcon = (style) => {
      return agentIcons[style] || agentIcons.default
    }

    const renderMarkdown = (text) => {
      if (!text) return ''
      let html = text
        .replace(/```([\s\S]*?)```/g, (match, p1) => {
          const escaped = p1.replace(/</g, '&lt;').replace(/>/g, '&gt;')
          return `<pre class=\"code-block\"><code>${escaped}</code></pre>`
        })
        .replace(/`([^`]+)`/g, '<code class=\"inline-code\">$1</code>')
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        .replace(/\n/g, '<br>')
      return html
    }

    const formatTime = (timestamp) => {
      try {
        return new Date(timestamp).toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
      } catch { return '' }
    }

    const scrollToBottom = () => {
      nextTick(() => {
        if (messagesContainer.value) {
          messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
        }
      })
    }

    const handleSendMessage = async () => {
      if (!inputMessage.value.trim() || loading.value || !agentsStore.currentAgent) return
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
      } catch {}
    }

    const switchAgent = (agent) => {
      if (!agent) return
      agentsStore.setCurrentAgent(agent)
      agentsStore.clearChatHistory()
      router.push(`/chat/${agent.id}`)
    }

    const newConversation = () => {
      agentsStore.clearChatHistory()
      scrollToBottom()
    }

    const goDashboard = () => {
      router.push('/dashboard')
    }

    watch(() => agentsStore.chatHistory, () => scrollToBottom(), { deep: true })

    onMounted(async () => {
      if (!agentsStore.agents || agentsStore.agents.length === 0) {
        sidebarLoading.value = true
        try { await agentsStore.fetchAgents() } finally { sidebarLoading.value = false }
      }
      const agentId = route.params.agentId
      if (agentId) {
        const agent = agentsStore.getAgentById(Number(agentId))
        if (agent) {
          agentsStore.setCurrentAgent(agent)
        }
      }
      scrollToBottom()
    })

    return {
      agentsStore,
      userStore,
      inputMessage,
      loading,
      messagesContainer,
      sidebarLoading,
      getAgentIcon,
      renderMarkdown,
      formatTime,
      handleSendMessage,
      clearChat,
      switchAgent,
      newConversation,
      goDashboard
    }
  }
}
</script>

<style scoped>
.chat-page { display: flex; flex-direction: column; height: 100vh; }

.top-navbar {
  background: #ffffff;
  border-bottom: 1px solid #eceff5;
}
.navbar-inner {
  max-width: 1200px; margin: 0 auto; height: 56px; display: flex; align-items: center; justify-content: space-between; padding: 0 16px;
}
.brand { display: flex; align-items: center; gap: 10px; cursor: pointer; }
.brand-logo { font-size: 18px; }
.brand-name { font-weight: 600; color: #111827; }

.nav-actions { display: flex; align-items: center; gap: 12px; }
.user-box { display: flex; align-items: center; gap: 10px; padding-right: 8px; }
.user-avatar { width: 32px; height: 32px; border-radius: 50%; background: #4f46e5; color: #fff; display: flex; align-items: center; justify-content: center; font-weight: 600; }
.user-meta { line-height: 1.2; }
.user-name { font-size: 14px; color: #111827; font-weight: 600; }
.user-email { font-size: 12px; color: #6b7280; }

.chat-layout {
  display: grid;
  grid-template-columns: 280px 1fr;
  height: calc(100vh - 56px);
  background: #f5f7fa;
}

.chat-sidebar {
  background: #0f172a;
  color: #e5e7eb;
  display: flex;
  flex-direction: column;
  border-right: 1px solid rgba(255,255,255,0.06);
}

.sidebar-header { padding: 16px; border-bottom: 1px solid rgba(255,255,255,0.06); }
.new-chat-btn { width: 100%; }

.sidebar-section { padding: 12px 8px; overflow: hidden auto; }
.section-title { font-size: 12px; color: #94a3b8; padding: 8px 8px; }

.agent-list { display: flex; flex-direction: column; gap: 6px; }
.agent-item { display: flex; gap: 10px; align-items: center; padding: 10px; border-radius: 8px; cursor: pointer; transition: background 0.2s ease; }
.agent-item:hover { background: rgba(255,255,255,0.06); }
.agent-item.active { background: rgba(255,255,255,0.12); }
.agent-icon { width: 28px; height: 28px; display: flex; align-items: center; justify-content: center; color: #a5b4fc; }
.agent-meta { overflow: hidden; }
.agent-name { color: #e5e7eb; font-size: 14px; white-space: nowrap; text-overflow: ellipsis; overflow: hidden; }
.agent-desc { color: #94a3b8; font-size: 12px; white-space: nowrap; text-overflow: ellipsis; overflow: hidden; }

.chat-main { display: flex; flex-direction: column; height: 100%; }

.chat-header { background: #ffffff; border-bottom: 1px solid #eceff5; padding: 10px 16px; display: flex; align-items: center; justify-content: space-between; }
.agent-header { display: flex; align-items: center; gap: 10px; }
.agent-avatar { width: 36px; height: 36px; border-radius: 8px; background: #eef2ff; display: flex; align-items: center; justify-content: center; color: #667eea; }
.agent-title h3 { margin: 0; font-size: 16px; color: #111827; font-weight: 600; }
.agent-title p { margin: 0; font-size: 12px; color: #6b7280; }

.messages { flex: 1; overflow-y: auto; padding: 24px; display: flex; flex-direction: column; gap: 16px; }

.empty-state { text-align: center; color: #9ca3af; margin-top: 10vh; }
.empty-state h2 { margin: 14px 0 8px; color: #374151; font-weight: 600; }

.message-row { display: flex; gap: 12px; }
.message-row.is-user { flex-direction: row-reverse; }

.message-avatar { width: 32px; height: 32px; border-radius: 6px; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.message-avatar.user { background: #4f46e5; color: #fff; }
.message-avatar.agent { background: #eef2ff; color: #4f46e5; }

.message-bubble { background: #ffffff; border-radius: 10px; padding: 12px 14px; box-shadow: 0 1px 3px rgba(0,0,0,0.06); max-width: 70%; }
.message-row.is-user .message-bubble { background: #4f46e5; color: #fff; }

.message-time { font-size: 11px; opacity: 0.6; margin-top: 6px; text-align: right; }
.message-row.is-user .message-time { color: rgba(255,255,255,0.8); }

.typing-indicator { display: flex; gap: 4px; }
.typing-indicator span { width: 8px; height: 8px; border-radius: 50%; background: #cbd5e1; animation: typing 1.4s infinite ease-in-out; }
.typing-indicator span:nth-child(1) { animation-delay: -0.32s; }
.typing-indicator span:nth-child(2) { animation-delay: -0.16s; }
@keyframes typing { 0%, 80%, 100% { transform: scale(0.8); opacity: 0.5; } 40% { transform: scale(1); opacity: 1; } }

.composer { background: #ffffff; border-top: 1px solid #eceff5; padding: 12px 16px; }
.composer-inner { max-width: 900px; margin: 0 auto; display: flex; gap: 10px; align-items: flex-end; }
.composer-hint { text-align: center; font-size: 12px; color: #9ca3af; margin-top: 6px; }

.send-btn { width: 40px; height: 40px; }

/* Markdown styles */
.markdown-body { font-size: 14px; line-height: 1.7; color: inherit; }
.markdown-body p { margin: 0 0 8px; }
.markdown-body code.inline-code { background: rgba(15, 23, 42, 0.06); padding: 2px 6px; border-radius: 4px; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace; }
.markdown-body pre.code-block { background: #0b1020; color: #e5e7eb; padding: 12px; border-radius: 8px; overflow: auto; }
.markdown-body pre.code-block code { font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace; }

/* Scrollbar */
.messages::-webkit-scrollbar { width: 8px; }
.messages::-webkit-scrollbar-thumb { background: #d1d5db; border-radius: 4px; }

@media (max-width: 1024px) {
  .chat-layout { grid-template-columns: 240px 1fr; }
}

@media (max-width: 768px) {
  .chat-layout { grid-template-columns: 1fr; }
  .chat-sidebar { display: none; }
  .message-bubble { max-width: 85%; }
}
</style>
