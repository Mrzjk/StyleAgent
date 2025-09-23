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

    <el-form-item label="智能体类别" prop="category">
      <el-select v-model="form.category" placeholder="请选择智能体类别" style="width: 100%">
        <el-option
          v-for="category in categories"
          :key="category.id"
          :label="category.name"
          :value="category.id"
        >
          <div class="style-option">
            <span>{{ category.name }}</span>
            <span class="style-desc">{{ category.description }}</span>
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
          v-for="tag in tagList"
          :key="tag.id"
          :label="tag.name"
          :value="tag.name"
        />
      </el-select>
    </el-form-item>


  <el-form-item label="系统提示" prop="systemPrompt" style="position: relative;">
    <el-input
      v-model="form.systemPrompt"
      type="textarea"
      :rows="4"
      placeholder="请输入系统提示词..."
      maxlength="600"
      show-word-limit
    />
    <!-- 绝对定位按钮 -->
  <el-tooltip content="优化提示词" placement="top">
    <el-button
      icon="Star"
      type="text"
      size="small"
      :loading="loadingOptimize"
      @click="optimizeSystemPrompt"
      style="position: absolute; right: 10px; bottom: 10px; z-index: 10;"
    />
  </el-tooltip>

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

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { useAgentsStore } from '@/stores/agent'
import { useTagsStore } from '@/stores/tag'
import { useAgentCategories } from '@/stores/category'

// 接收父组件事件
const emit = defineEmits(['success', 'cancel'])

const agentsStore = useAgentsStore()
const tagsStore = useTagsStore()
const cateStore = useAgentCategories()
const formRef = ref()
const loading = ref(false)

const form = reactive({
  name: '',
  description: '',
  category: '',
  tags: [],
  systemPrompt: '',
  temperature: 0.7
})

const rules = {
  name: [
    { required: true, message: '请输入智能体名称', trigger: 'blur' },
    { min: 2, max: 20, message: '名称长度在2到20个字符', trigger: 'blur' }
  ],
  description: [
    { required: true, message: '请输入智能体描述', trigger: 'blur' },
    { min: 5, max: 200, message: '描述长度在5到200个字符', trigger: 'blur' }
  ],
  category: [
    { required: true, message: '请选择智能体类别', trigger: 'change' }
  ],
  tags: [
    { required: true, message: '请至少选择一个标签', trigger: 'change' }
  ],
  systemPrompt: [
    { required: true, message: '请输入系统提示词', trigger: 'blur' },
    { min: 20, max: 600, message: '提示词长度在20到600个字符', trigger: 'blur' }
  ]
}

const formatTemperature = (value) => {
  if (value <= 0.3) return `保守 (${value})`
  if (value <= 0.7) return `平衡 (${value})`
  return `创新 (${value})`
}

const handleSubmit = async () => {
  if (!formRef.value) return

  try {
    await formRef.value.validate()  // Promise 风格
    loading.value = true

    const payload = {
      name: form.name,
      description: form.description,
      category: form.category,
      tags: form.tags,
      prompt: form.systemPrompt,
      temperature: form.temperature
    }

    console.log('提交 payload:', payload)
    const result = await agentsStore.createAgent(payload)
    loading.value = false

    if (result.success) {
      emit('success')
    } else {
      ElMessage.error(result.message)
    }
  } catch (err) {
    console.log('表单验证未通过', err)
  }
}

const handleCancel = () => {
  emit('cancel')
}

// 使用 store 中的响应式数据
const categories = computed(() => cateStore.categories || [])
const tagList = computed(() => tagsStore.tags || [])

onMounted(async () => {
  try {
    await cateStore.getAgentCategories()
  } catch (error) {
    console.error('获取分类失败:', error)
  }

  try {
    await tagsStore.getTags()
  } catch (error) {
    console.error('获取标签失败:', error)
  }
})
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
