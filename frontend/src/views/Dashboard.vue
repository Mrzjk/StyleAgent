<template>
  <div class="dashboard">
    <header class="dashboard-header">
      <div class="header-content">
        <h1>AI智能体平台</h1>
        <div class="user-info">
          <span>欢迎，{{ userStore.userInfo?.username }}</span>
          <el-button type="text" @click="handleLogout">退出登录</el-button>
        </div>
      </div>
    </header>

    <main class="dashboard-main">
      <div class="main-content">
        <div class="section-header">
          <h2>选择智能体</h2>
          <el-button type="primary" @click="showCreateDialog = true">
            <el-icon><Plus /></el-icon>
            创建新智能体
          </el-button>
        </div>

        <div class="agents-grid" v-loading="loading">
          <div 
            v-for="agent in agentsStore.agents" 
            :key="agent.id"
            class="agent-card"
            @click="selectAgent(agent)"
          >
            <div class="agent-avatar">
              <el-icon :size="40">
                <component :is="getAgentIcon(agent.style)" />
              </el-icon>
            </div>
            <div class="agent-info">
              <h3>{{ agent.name }}</h3>
              <p>{{ agent.description }}</p>
              <div class="agent-tags">
                <el-tag 
                  v-for="tag in agent.tags" 
                  :key="tag" 
                  size="small"
                  :type="getTagType(tag)"
                >
                  {{ tag }}
                </el-tag>
              </div>
            </div>
            <div class="agent-actions">
              <el-button type="primary" size="small" @click.stop="startChat(agent)">
                开始对话
              </el-button>
            </div>
          </div>
        </div>

        <div v-if="agentsStore.agents.length === 0 && !loading" class="empty-state">
          <el-icon :size="80" color="#ccc"><Robot /></el-icon>
          <h3>还没有智能体</h3>
          <p>创建您的第一个智能体，开始智能对话体验</p>
          <el-button type="primary" @click="showCreateDialog = true">
            创建智能体
          </el-button>
        </div>
      </div>
    </main>

    <!-- 创建智能体对话框 -->
    <el-dialog
      v-model="showCreateDialog"
      title="创建新智能体"
      width="600px"
      :before-close="handleCloseDialog"
    >
      <CreateAgentForm @success="handleCreateSuccess" @cancel="showCreateDialog = false" />
    </el-dialog>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Robot, User, Star, Setting, ChatDotRound } from '@element-plus/icons-vue'
import { useUserStore } from '../stores/user'
import { useAgentsStore } from '../stores/agents'
import CreateAgentForm from '../components/CreateAgentForm.vue'

export default {
  name: 'Dashboard',
  components: {
    CreateAgentForm
  },
  setup() {
    const router = useRouter()
    const userStore = useUserStore()
    const agentsStore = useAgentsStore()
    const loading = ref(false)
    const showCreateDialog = ref(false)

    const agentIcons = {
      'assistant': User,
      'creative': Star,
      'technical': Setting,
      'friendly': ChatDotRound,
      'default': Robot
    }

    const getAgentIcon = (style) => {
      return agentIcons[style] || agentIcons.default
    }

    const getTagType = (tag) => {
      const types = ['', 'success', 'warning', 'danger', 'info']
      return types[tag.length % types.length]
    }

    const selectAgent = (agent) => {
      agentsStore.setCurrentAgent(agent)
    }

    const startChat = (agent) => {
      agentsStore.setCurrentAgent(agent)
      router.push(`/chat/${agent.id}`)
    }

    const handleLogout = async () => {
      try {
        await ElMessageBox.confirm('确定要退出登录吗？', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        })
        userStore.logout()
        ElMessage.success('已退出登录')
        router.push('/login')
      } catch {
        // 用户取消
      }
    }

    const handleCreateSuccess = () => {
      showCreateDialog.value = false
      ElMessage.success('智能体创建成功')
      agentsStore.fetchAgents()
    }

    const handleCloseDialog = (done) => {
      done()
    }

    onMounted(async () => {
      loading.value = true
      await agentsStore.fetchAgents()
      loading.value = false
    })

    return {
      userStore,
      agentsStore,
      loading,
      showCreateDialog,
      getAgentIcon,
      getTagType,
      selectAgent,
      startChat,
      handleLogout,
      handleCreateSuccess,
      handleCloseDialog
    }
  }
}
</script>

<style scoped>
.dashboard {
  min-height: 100vh;
  background: #f5f7fa;
}

.dashboard-header {
  background: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 0 20px;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 70px;
}

.header-content h1 {
  color: #333;
  font-size: 24px;
  font-weight: 600;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 15px;
}

.user-info span {
  color: #666;
  font-size: 14px;
}

.dashboard-main {
  padding: 30px 20px;
}

.main-content {
  max-width: 1200px;
  margin: 0 auto;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.section-header h2 {
  color: #333;
  font-size: 28px;
  font-weight: 600;
}

.agents-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.agent-card {
  background: white;
  border-radius: 15px;
  padding: 25px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  cursor: pointer;
  border: 2px solid transparent;
}

.agent-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
  border-color: #667eea;
}

.agent-avatar {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
  color: #667eea;
}

.agent-info h3 {
  color: #333;
  font-size: 20px;
  font-weight: 600;
  margin-bottom: 10px;
  text-align: center;
}

.agent-info p {
  color: #666;
  font-size: 14px;
  line-height: 1.5;
  margin-bottom: 15px;
  text-align: center;
}

.agent-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  justify-content: center;
  margin-bottom: 20px;
}

.agent-actions {
  display: flex;
  justify-content: center;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #999;
}

.empty-state h3 {
  margin: 20px 0 10px;
  color: #666;
  font-size: 20px;
}

.empty-state p {
  margin-bottom: 30px;
  color: #999;
}

:deep(.el-dialog) {
  border-radius: 15px;
}

:deep(.el-dialog__header) {
  padding: 20px 20px 10px;
}

:deep(.el-dialog__body) {
  padding: 10px 20px 20px;
}
</style>
