<template>
  <el-form 
    ref="formRef" 
    :model="form" 
    :rules="rules" 
    label-width="100px"
    @submit.prevent="handleSubmit"
  >
    <el-form-item label="智能体名称" prop="name">
      <el-input 
        v-model="form.name" 
        placeholder="请输入智能体名称"
        maxlength="20"
        show-word-limit
      />
    </el-form-item>

    <el-form-item label="智能体描述" prop="description">
      <el-input 
        v-model="form.description" 
        type="textarea" 
        :rows="3"
        placeholder="请描述智能体的功能和特点"
        maxlength="200"
        show-word-limit
      />
    </el-form-item>

    <el-form-item label="智能体风格" prop="style">
      <el-select v-model="form.style" placeholder="请选择智能体风格" style="width: 100%">
        <el-option
          v-for="style in agentStyles"
          :key="style.value"
          :label="style.label"
          :value="style.value"
        >
          <div class="style-option">
            <el-icon><component :is="style.icon" /></el-icon>
            <span>{{ style.label }}</span>
            <span class="style-desc">{{ style.description }}</span>
          </div>
        </el-option>
      </el-select>
    </el-form-item>

    <el-form-item label="标签" prop="tags">
      <el-select
        v-model="form.tags"
        multiple
        filterable
        allow-create
        placeholder="请选择或输入标签"
        style="width: 100%"
      >
        <el-option
          v-for="tag in commonTags"
          :key="tag"
          :label="tag"
          :value="tag"
        />
      </el-select>
    </el-form-item>

    <el-form-item label="系统提示" prop="systemPrompt">
      <el-input 
        v-model="form.systemPrompt" 
        type="textarea" 
        :rows="4"
        placeholder="请输入系统提示词，定义智能体的行为模式"
        maxlength="500"
        show-word-limit
      />
    </el-form-item>

    <el-form-item label="温度设置" prop="temperature">
      <el-slider
        v-model="form.temperature"
        :min="0"
        :max="1"
        :step="0.1"
        show-stops
        show-input
        :format-tooltip="formatTemperature"
      />
    </el-form-item>

    <el-form-item>
      <div class="form-actions">
        <el-button @click="handleCancel">取消</el-button>
        <el-button type="primary" :loading="loading" @click="handleSubmit">
          创建智能体
        </el-button>
      </div>
    </el-form-item>
  </el-form>
</template>

<script>
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import { User, Star, Setting, ChatDotRound } from '@element-plus/icons-vue'
import { useAgentsStore } from '../stores/agents'

export default {
  name: 'CreateAgentForm',
  emits: ['success', 'cancel'],
  setup(props, { emit }) {
    const agentsStore = useAgentsStore()
    const formRef = ref()
    const loading = ref(false)

    const form = reactive({
      name: '',
      description: '',
      style: '',
      tags: [],
      systemPrompt: '',
      temperature: 0.7
    })

    const agentStyles = [
      {
        value: 'assistant',
        label: '助手型',
        description: '专业、高效、准确',
        icon: User
      },
      {
        value: 'creative',
        label: '创意型',
        description: '富有想象力、创新思维',
        icon: Star
      },
      {
        value: 'technical',
        label: '技术型',
        description: '逻辑清晰、技术专业',
        icon: Setting
      },
      {
        value: 'friendly',
        label: '友好型',
        description: '亲切、幽默、易沟通',
        icon: ChatDotRound
      }
    ]

    const commonTags = [
      '编程助手', '写作助手', '学习助手', '翻译助手', 
      '创意助手', '技术顾问', '生活助手', '商务助手'
    ]

    const rules = {
      name: [
        { required: true, message: '请输入智能体名称', trigger: 'blur' },
        { min: 2, max: 20, message: '名称长度在2到20个字符', trigger: 'blur' }
      ],
      description: [
        { required: true, message: '请输入智能体描述', trigger: 'blur' },
        { min: 10, max: 200, message: '描述长度在10到200个字符', trigger: 'blur' }
      ],
      style: [
        { required: true, message: '请选择智能体风格', trigger: 'change' }
      ],
      tags: [
        { required: true, message: '请至少选择一个标签', trigger: 'change' }
      ],
      systemPrompt: [
        { required: true, message: '请输入系统提示词', trigger: 'blur' },
        { min: 20, max: 500, message: '提示词长度在20到500个字符', trigger: 'blur' }
      ]
    }

    const formatTemperature = (value) => {
      if (value <= 0.3) return '保守 (0.3)'
      if (value <= 0.7) return '平衡 (0.7)'
      return '创新 (1.0)'
    }

    const handleSubmit = async () => {
      if (!formRef.value) return

      await formRef.value.validate(async (valid) => {
        if (valid) {
          loading.value = true
          const result = await agentsStore.createAgent(form)
          loading.value = false

          if (result.success) {
            emit('success')
          } else {
            ElMessage.error(result.message)
          }
        }
      })
    }

    const handleCancel = () => {
      emit('cancel')
    }

    return {
      formRef,
      form,
      rules,
      loading,
      agentStyles,
      commonTags,
      formatTemperature,
      handleSubmit,
      handleCancel
    }
  }
}
</script>

<style scoped>
.style-option {
  display: flex;
  align-items: center;
  gap: 10px;
}

.style-desc {
  color: #999;
  font-size: 12px;
  margin-left: auto;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 15px;
  width: 100%;
}

:deep(.el-form-item__label) {
  font-weight: 500;
  color: #333;
}

:deep(.el-input__wrapper) {
  border-radius: 8px;
}

:deep(.el-select .el-input__wrapper) {
  border-radius: 8px;
}

:deep(.el-textarea__inner) {
  border-radius: 8px;
}
</style>
