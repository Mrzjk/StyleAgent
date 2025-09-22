# AI智能体平台前端

这是一个基于Vue 3的AI智能体平台前端应用，提供用户注册、登录、智能体创建和对话聊天功能。

## 功能特性

- 🔐 用户注册和登录
- 🤖 智能体风格卡片选择
- ✨ 智能体创建和配置
- 💬 实时对话聊天
- 📱 响应式设计
- 🎨 现代化UI界面

## 技术栈

- **Vue 3** - 渐进式JavaScript框架
- **Vite** - 快速的前端构建工具
- **Vue Router** - 官方路由管理器
- **Pinia** - Vue状态管理库
- **Element Plus** - Vue 3组件库
- **Axios** - HTTP客户端

## 项目结构

```
frontend/
├── src/
│   ├── components/          # 可复用组件
│   │   └── CreateAgentForm.vue
│   ├── views/              # 页面组件
│   │   ├── Login.vue
│   │   ├── Register.vue
│   │   ├── Dashboard.vue
│   │   └── Chat.vue
│   ├── stores/             # 状态管理
│   │   ├── user.js
│   │   └── agents.js
│   ├── router/             # 路由配置
│   │   └── index.js
│   ├── utils/              # 工具函数
│   │   ├── api.js
│   │   └── constants.js
│   ├── styles/             # 样式文件
│   │   └── global.css
│   ├── App.vue
│   └── main.js
├── index.html
├── package.json
├── vite.config.js
└── README.md
```

## 安装和运行

### 1. 安装依赖

```bash
cd frontend
npm install
```

### 2. 启动开发服务器

```bash
npm run dev
```

应用将在 `http://localhost:3000` 启动

### 3. 构建生产版本

```bash
npm run build
```

## 页面说明

### 登录页面 (`/login`)
- 用户邮箱和密码登录
- 表单验证
- 自动跳转到仪表板

### 注册页面 (`/register`)
- 用户名、邮箱、密码注册
- 密码确认验证
- 注册成功后自动登录

### 仪表板 (`/dashboard`)
- 显示所有可用的智能体
- 智能体卡片展示
- 创建新智能体功能
- 选择智能体开始对话

### 智能体创建 (`/create-agent`)
- 智能体基本信息配置
- 风格选择（助手型、创意型、技术型、友好型）
- 标签设置
- 系统提示词配置
- 温度参数调节

### 对话页面 (`/chat/:agentId`)
- 实时对话界面
- 消息历史记录
- 打字指示器
- 清空对话功能
- 返回仪表板

## API接口

应用需要后端提供以下API接口：

### 认证接口
- `POST /api/auth/login` - 用户登录
- `POST /api/auth/register` - 用户注册

### 智能体接口
- `GET /api/agents` - 获取智能体列表
- `POST /api/agents` - 创建新智能体

### 聊天接口
- `POST /api/chat` - 发送消息

## 配置说明

### 代理配置
在 `vite.config.js` 中配置了API代理，将 `/api` 请求代理到后端服务器：

```javascript
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:8000',
      changeOrigin: true
    }
  }
}
```

### 环境变量
可以通过环境变量配置API基础URL：

```bash
VITE_API_BASE_URL=http://localhost:8000
```

## 开发说明

### 状态管理
使用Pinia进行状态管理：
- `user.js` - 用户认证状态
- `agents.js` - 智能体和聊天状态

### 路由守卫
配置了路由守卫，自动处理：
- 登录状态检查
- 未登录用户重定向
- 已登录用户访问登录页重定向

### 响应式设计
- 移动端适配
- 弹性布局
- 触摸友好的交互

## 浏览器支持

- Chrome >= 87
- Firefox >= 78
- Safari >= 14
- Edge >= 88

## 许可证

MIT License
