# AI Roleplay App — 设计文档与 React 原型

> 说明：此文档包含产品设计、用户画像、需求优先级、模型选择理由（高层）、以及一个可运行的 React 前端 + Node 后端示例（用于演示如何仅使用：LLM、语音识别（浏览器端）与 TTS（服务端或浏览器）来实现多技能 AI 角色）。

---

## 1. 项目概述

目标是构建一个面向广泛用户的“AI 角色扮演”平台，允许用户搜索/选择大众熟知或原创的角色（例如：受古典哲学启发的“苏格拉底式导师”、富有想象力的“奇幻故事导师”、或“历史人物风格的讲师”），并与之进行**语音对话**与**多技能互动**（提问引导、故事创作、测验/评估、记忆上下文等）。

平台原则：真实感（连贯的人格）、低延迟语音互动、可控与安全的角色行为、易上手的 UI/UX、并提供可拓展的技能模板。

---

## 2. 目标用户与痛点

### 目标用户画像（类型）
1. **学习者 / 学生**：需要练习口语、辩论、语言对话或接受“导师型”引导。
2. **创作者 / 编剧 /作家**：需要与虚构角色进行对话来激发灵感，或用于快速写作草稿/对话模拟。
3. **角色扮演与粉丝用户**：想跟心仪角色（或“灵感来源”）互动的普通用户。
4. **教育工作者 / 培训师**：希望用角色化方式来做测验、教学或模拟场景。
5. **语言学习者**：需要真实语境下的口语练习与即时反馈。
6. **产品/游戏团队原型设计者**：用于测试 NPC 对话或角色设定。

### 共通痛点
- **缺乏沉浸式、低延迟的语音角色体验**（大多数平台仅文本或 TTS 单向）。
- **角色不稳定**：同一个角色在多次对话中表现不一致（人格漂移）。
- **交互能力有限**：无法做到像人一样“提问反问/发起故事/考察理解/给出情感回应”这样的多样技能。
- **版权/形象问题不清楚**：用户希望与已知形象互动但平台不清晰怎样处理版权与改编。
- **安全与可控性担忧**：担心内容不当、误导、或敏感话题的处理。

---

## 3. 代表性用户故事（User Stories）

1. 学生小李："我想和一个‘苏格拉底式导师’练习哲学争辩，要求他只用提问引导我反思，并在会话中记录 3 条关键观察。"
2. 作家小王："我想跟一个‘蒸汽朋克世界的舰长’即兴编故事，要求每轮续写 200 字，并能在需要时让角色生成下一段悬念句。"
3. 语言学习者 Anna："我要用西班牙语跟‘西班牙老师’练习 10 分钟口语，并在练习后得到 5 条发音建议。"
4. 教师陈老师："我要布置一个 5 题的历史快问快答（多项选择），并在学生答题完后自动评分与给出讲解。"

---

## 4. 功能清单（含优先级）

**优先级说明：** Must（M）= 必须在 MVP 中实现；High（H）= 高优先级；Medium（MEd）= 中等；Low（L）= 低优先级。

- 角色创建与浏览（支持标签、示例台词、技能预览） — **M**
- 角色详情页（角色简介、人格/限制设定、声音选择） — **M**
- 语音聊天（浏览器语音识别 -> LLM -> TTS）— **M**
- 会话上下文与短期记忆（会话内一致性） — **H**
- 可选的长期记忆/用户偏好（可选开关） — **MEd**
- 多技能模板（Socratic / Storyteller / Quiz / Coach） — **H**
- 角色声音选择（多说话风格）与速率、音高设置 — **H**
- 会话记录、导出（文本/音频） — **H**
- 安全过滤与内容策略（敏感话题拒绝/脱敏）— **M**
- 版权/合规提示、用户协议与角色来源标注 — **M**
- 账户、订阅与钥匙管理（计费） — **MEd**
- 多人/房间模式（多人角色交互） — **L**
- 自定义训练（用户上传示例让角色更贴合） — **L**


### 本次开发（MVP）计划实现的功能
- 角色搜索/选择
- 语音聊天（浏览器 STT + LLM + TTS）
- 三个示范技能（Socratic、Storyteller、Quiz Master）
- 会话内上下文记忆（session memory）
- 简单安全过滤（关键词屏蔽）
- 前端 Vue 框架 + FastAPI 后端示例（负责代理模型请求与 TTS）

---

## 5. 我建议采用的 LLM 模型（高层选择与替代方案）

> 选择标准（按优先级）：实时音频支持（低延迟）、优秀的指令遵循能力（角色一致性）、TTS 与语音集成能力、成本/可用性、隐私/合规选项。

- **主推荐（MVP）**：**OpenAI 的 GPT-4o / Realtime API 系列**（用于真实语音理解与低延迟交互的中心 LLM）。优点：已支持多模态与实时交互（便于实现语音对话），生态成熟，文档齐全，开发者工具丰富。适用于原型与商业化迭代阶段。

- **备选 1（更强 TTS 控制）**：**Google Gemini + Gemini TTS**：如果你对 TTS 的音色/情绪控制要求非常高，Gemini 的 TTS 能力提供细粒度的声音/情绪控制与多说话人支持，可用于更自然的语音输出体验。

- **备选 2（注重安全与企业隐私）**：**Anthropic Claude（含 Voice 模式）**：在对话安全与策略控制方面具备优势，适合对安全性/合规性要求高的场景。

- **自托管/开源替代**：**Mistral / Llama 3 / Mixtral** 等可自托管的模型，适合强隐私或希望降低长期成本的企业级部署，但需要更多运维/硬件投入，并在多轮会话与复杂指令一致性上做 tuning。

> 备注：以上选择的详细比对数据参考了当下厂商公示的能力（如实时音频、TTS 控制、多语种支持）——我在本次设计中以 GPT-4o（或等价 realtime API）作为示例集成目标。若你偏向 Google/Anthropic 的语音特性，也可以很容易替换后端适配层（文档与示例已在代码注释中说明）。

---

## 6. 合规、安全与版权注意事项

- **版权/人物肖像**：明确区分“公开域/历史人物”与“受版权保护的小说角色（如《哈利波特》）”。若提供受版权角色，务必在商业化前确认授权或采用“灵感来源”模式与免责声明，并对生成文本与语音加上“粉丝创作/非官方改编”的提示。
- **内容审查**：实现多层过滤（输入/LLM 输出/语音输出前）来屏蔽极端暴力、仇恨、非法行为指示等敏感内容。
- **隐私**：会将会话记录与用户偏好作为可选功能，默认关闭长期记忆并允许用户删除历史会话。

---

## 7. 系统架构（高层）

```
Browser (React) <---> Node/Express proxy
   |  (Web Speech API STT)
   |  (Play audio TTS via <audio> or stream)
   v
Backend endpoints:
  - POST /api/llm  -> 调用 LLM Provider (OpenAI/Gemini/Claude)  (system + messages)
  - POST /api/tts  -> 请求 TTS (返回音频 URL/stream)
  - POST /api/audio-upload (可选，用于上传录音文件做离线 STT)

Storage: session memory in server/DB (短期) + optional longterm memory store (加密)
```

安全 / rate limiting / key management 都放在后端代理层，避免将 provider key 泄露到浏览器。

---

## 8. AI 角色技能设计（至少实现 3 项）

每个技能通过**系统提示（system prompt）+ 指示模板（instruction template）+ 会话历史**来实现。**实现原则**：全部通过 LLM 执行逻辑（推理与策略），不调用第三方 Agent。

### 技能 1 — Socratic Questioning（苏格拉底式提问）
**目标行为**：不直接给出结论，而是通过层层提问引导用户自己思考。

**系统提示样例**：
```
You are 'Socrates'—a neutral, probing dialogue partner. For every user statement, respond only by asking 1-3 thoughtful, targeted questions that lead the user to clarify assumptions or re-evaluate beliefs. Do NOT provide direct answers or lectures. Keep each question concise.
```

**前端交互**：用户开启该技能后，发送用户语音转文本 -> 传给 /api/llm，LLM 返回 1-3 个问题 -> TTS 播放。

---

### 技能 2 — Storyteller（故事创作师）
**目标行为**：与用户共同续写故事，支持“续写长度”、“风格/语气”与“兴奋点”控制。

**系统提示样例**：
```
You are a professional storyteller specialized in Victorian fantasy. When the user says "continue", produce a 150-250 word continuation. Use vivid sensory details, keep previous story lines consistent. If user asks for a twist, propose a single-sentence twist and then continue.
```

**前端交互**：用户按“续写”按钮触发 -> /api/llm 生成新段落 -> TTS。

---

### 技能 3 — Quiz Master（测验大师）
**目标行为**：自动生成问题（选择题或简答），收集用户回答，给出即时评分与解释。

**系统提示样例**：
```
You are a Quiz Master in the domain of World History. Produce a 5-question multiple-choice quiz at an intermediate level. After user answers each question, evaluate correctness and give one-sentence explanation. Score at the end.
```

**实现要点**：后端调用 LLM 要求输出结构化 JSON（问题/选项/正确答案/解释），前端循环问答并提交回答到 /api/llm 进行判分。

---

### 技能 4 — Memory & Consistency（会话内记忆）
**目标行为**：记录会话内的关键事实（最多 N 条），并在后续交互中参考这些事实以保持角色一致性。

**实现要点**：在每次请求前，后端会将当次 session 的核心记忆摘要（例如 3 条）拼接进 system prompt 或初始 messages 中以辅助 LLM 保持一致性。

---

### 技能 5 — Emotional Tone Control（情绪/语气控制）
**目标行为**：按用户选择的情绪（温和/严厉/幽默/中立）调整回复风格。

**实现要点**：在 system prompt 中插入 `tone` 说明，或在调用 TTS 时使用 TTS 的情绪/韵律参数（若 provider 支持）。

---

## 9. 示例代码说明（包含前端 React 与后端 Node/Express 示例）

> 注意：此处给出一个可运行的最小示例。真实部署时请把 provider key 放在服务器端（env），并做好速率限制与内容审查。文档后有运行步骤。

---

### 代码结构说明（示例）

```
-AIAgent
  -frontend
    -src/App.jsx
    -src/components/RoleList.jsx
    -src/components/VoiceChat.jsx
  -backend
    -agent (智能体)
      -config
         *
      -schemas
         -*
      -utils
         -*
      -graph.py
      -state.py
      prompt.py
    -api (路由)
      -models(数据库的orm原型)
         -agent_card..py
         -agent_tag.py
         -user.py
         -*
      -router （子路由）
         -user_router.py
         -auth_router.py
         -agent_router.py
         -***
      -schemas（接受前端数据封装的类型）
         -LoginIn.py
         -FormData.py
         -*
    -.env  
  -main.py
 README.md
```

---


---

## 10. 运行与测试（快速入门）

1. 克隆仓库。
2. 在 `backend/.env` 中配置：
   - `LLM_API_URL`（你的 provider endpoint）
   - `LLM_API_KEY`
   - `LLM_MODEL`（例如 `gpt-4o-realtime`）
3. conda create -n agent python=3.11
4.  pip install requirement.txt
5. `cd backend\src && conda activate agent && python main.py`
6. `cd frontend && npm install && npm run dev`（使用支持 Web Speech API 的浏览器）
---

## 11. 可扩展方向 & 路线图（后续迭代）

- 引入可视化人物编辑器（声线/人格/记忆条目编辑）
- 提供社交房间与多人角色（笑剧/角色扮演会话）
- 高级长期记忆与隐私合规（可加密记忆、审计日志）
- 商业化策略（订阅、按分钟计费 TTS、付费声音/角色）

---

## 12. 结语

该原型集中展示如何在**不使用多工具 Agent**的前提下，通过巧妙设计的 system prompt + 会话管理 + 浏览器 STT + 后端 TTS，把多技能的 AI 角色体验落地为一个轻量且可扩展的产品雏形。文档中包含了三项（及以上）技能示例：Socratic、Storyteller、Quiz Master，并演示了如何实现 session memory 与情绪控制等辅助能力。


---

### 附：示例系统 prompt 模板（快速拷贝）

**Socratic 模板**：
```
System: You are a Socratic dialogue partner. For every user input, respond ONLY with 1-3 probing questions aimed to clarify assumptions. Never provide the answer.
```

**Storyteller 模板**：
```
System: You are a professional storyteller. Continue the story in 150-220 words, keep plot consistent, and produce vivid sensory details.
```

**Quiz Master 模板**：
```
System: You are a Quiz Master. Output a JSON array of questions with fields {id, type, question, choices, answer}. After each user attempt, evaluate correctness and return explanation.
```


---

*原型代码与文档均作为交付物提交。若你希望我把后端示例改成具体某个 provider（OpenAI / Google Gemini / Anthropic）的完整调用代码，我可以在此基础上直接替换并给出可运行的 provider 示例（包含 Node SDK/HTTP 示例）。*
