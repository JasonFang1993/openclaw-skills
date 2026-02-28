---
name: pm-toolkit
description: 去中心化项目管理工具箱。基于 STATE.yaml 的多 AI 协作 + 事件驱动的项目状态追踪。适用于复杂项目的自动化管理。
---

# pm-toolkit

去中心化项目管理工具箱，结合 **STATE.yaml 模式** + **事件驱动追踪**。

## 两种模式

### 模式 1: STATE.yaml (多 AI 协作)
- 多个 AI 通过共享文件协调
- 无中央指挥，AI 自行 pick 任务
- 适合：多 subagent 并行工作

### 模式 2: Event-Driven (事件驱动)
- 自然语言更新项目状态
- 自动记录决策、阻塞、进展
- 适合：单人项目管理

---

## 核心概念

### STATE.yaml - 任务协调文件

```yaml
# 项目状态文件
project: my-project
updated: 2026-02-28T10:00:00Z

tasks:
  - id: task-001
    status: in_progress    # todo | in_progress | done | blocked
    owner: ai-frontend
    started: 2026-02-28T09:00:00Z
    notes: "正在开发首页"
    
  - id: task-002
    status: done
    owner: ai-backend
    completed: 2026-02-28T08:00:00Z
    output: src/api/auth.ts
    
  - id: task-003
    status: blocked
    owner: ai-frontend
    blocked_by: task-002
    notes: "等待 API 完成"

next_actions:
  - "ai-backend: 继续开发 API"
  - "ai-frontend: API 完成后开始前端对接"
```

---

### 事件日志 - 记录所有决策

```yaml
events:
  - type: decision
    time: 2026-02-28T09:00:00Z
    content: "决定使用 React 替代 Vue"
    context: "因为团队更熟悉 React"
    
  - type: blocker
    time: 2026-02-28T10:00:00Z
    content: "API 文档不完整"
    resolved: false
    
  - type: pivot
    time: 2026-02-28T11:00:00Z
    content: "从付费订阅改为免费增值模式"
    reason: "市场调研显示用户对付费敏感"
```

---

## 功能

| 功能 | 说明 |
|------|------|
| 📝 STATE.yaml 管理 | AI 自行更新任务状态 |
| 🔄 事件记录 | 记录决策、阻塞、进展 |
| 🤖 多 AI 协调 | Subagent 通过文件协作 |
| 📊 每日汇总 | 自动生成 standup 报告 |
| 🔍 自然语言查询 | "项目进度怎么样？" |
| 🔗 Git 集成 | 代码提交关联项目 |

---

## 目录结构

```
projects/
├── my-app/
│   ├── STATE.yaml           # 任务状态
│   ├── EVENTS.yaml         # 事件日志
│   └── SPEC.md             # 项目规格
├── website-redesign/
│   ├── STATE.yaml
│   └── EVENTS.yaml
└── PROJECT_REGISTRY.yaml    # 项目索引
```

---

## 使用方法

### 1. 创建新项目

```bash
pm-init.sh my-project "做一个 AI 助手"
```

### 2. 更新任务状态

```bash
# AI 完成一个任务
pm-update.sh my-project --task task-001 --status done --output "src/index.ts"

# 遇到阻塞
pm-update.sh my-project --task task-002 --status blocked --blocked-by task-001
```

### 3. 记录事件

```bash
# 记录决策
pm-event.sh my-project --type decision --content "决定用 TypeScript"

# 记录阻塞
pm-event.sh my-project --type blocker --content "后端 API 延迟"
```

### 4. 查询状态

```bash
# 查看项目进度
pm-status.sh my-project

# 查看所有阻塞
pm-blockers.sh

# 每日汇总
pm-standup.sh
```

---

## 自然语言交互

### AI Agent 指令

```
你是一个项目经理 AI。

当用户说：
- "完成了 XXX" → 更新 STATE.yaml，标记任务为 done
- "遇到 XXX 问题" → 记录 blocker 事件
- "决定 XXX" → 记录 decision 事件
- "开始做 XXX" → 创建新任务，标记为 in_progress

当用户问：
- "项目进度怎么样？" → 读取 STATE.yaml，生成进度报告
- "有什么阻塞？" → 列出所有 blocker
- "为什么当时决定 XXX？" → 搜索 EVENTS.yaml 中的 decision

每个任务完成后要：
1. 更新 STATE.yaml
2. 提交 git
3. 报告给主 AI
```

---

## 输出示例

### 项目状态查询

```
📊 my-project 进度

✅ 已完成 (2):
- task-002: API 认证 (output: src/api/auth.ts)
- task-003: 数据库设计

⏳ 进行中 (1):
- task-001: 前端页面 (started: 09:00)

🚧 阻塞 (1):
- task-004: 等待 API 完成

📝 下一步:
- task-004: 后端完成后对接
```

### 每日 Standup

```
📅 每日汇总 (2026-02-28)

昨天完成:
- task-002: API 认证
- task-003: 数据库设计

今天计划:
- task-001: 前端页面
- task-004: API 对接

阻塞:
- task-004 等待后端 API

决策记录:
- 10:00 决定使用 TypeScript
- 11:00 决定用 React 生态
```

---

## Git 集成

每次状态更新自动提交：

```bash
git add STATE.yaml EVENTS.yaml
git commit -m "chore: update project state"
git push
```

---

## 与 Subagent 协作

```
主 AI:
1. 用户给了一个大任务
2. 创建 STATE.yaml
3. spawn 多个 subagent，每个分配任务

Subagent:
1. 读取 STATE.yaml 找到自己的任务
2. 完成后更新 STATE.yaml
3. 报告给主 AI

主 AI:
1. 定期检查 STATE.yaml
2. 生成进度报告给用户
```

---

## 对比传统 Kanban

| 特性 | 传统 Kanban | PM-Toolkit |
|------|-------------|-------------|
| 更新方式 | 手动拖卡片 | 自然语言/自动 |
| 上下文 | 丢失 | 完整保留 |
| 多 AI 协作 | 不支持 | 去中心化 |
| 决策追溯 | 困难 | 完整记录 |
| 自动化 | 低 | 高 |

---

## 依赖

- bash
- git
- yaml 解析 (python3)
- 可选: gh CLI (Git 集成)

---

## 快速开始

```bash
# 1. 初始化项目
pm-init.sh my-project "项目描述"

# 2. 添加任务
pm-task.sh my-project --id task-001 --desc "开发首页"

# 3. 更新状态
pm-update.sh my-project --task task-001 --status in_progress

# 4. 查看状态
pm-status.sh my-project
```
