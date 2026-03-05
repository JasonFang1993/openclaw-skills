---
name: pm-toolkit
description: 去中心化项目管理工具箱。基于 STATE.yaml 的多 AI 协作 + 事件驱动的项目状态追踪。适用于复杂项目的自动化管理。
---

# pm-toolkit

去中心化项目管理工具箱，结合 **STATE.yaml 模式** + **事件驱动追踪**。

---

## 🎯 这是什么？

一个让**多个 AI 员工**能**自行协调**工作的工具。

- 不需要你一直盯着
- AI 自己知道要做什么
- 自动记录进度和决策
- 适合复杂项目

---

## 👥 适用场景

| 场景 | 需要 |
|------|------|
| 多个 AI 同时干活 | ✅ |
| 大项目需要分工 | ✅ |
| 记录每个决策原因 | ✅ |
| 一个人管理多个项目 | ✅ |
| 小任务不需要 | ❌ |

---

## 🏗️ 核心概念

### STATE.yaml - 任务表

就像一个共享的**任务看板**，所有 AI 都能看到：

```yaml
project: my-project
updated: 2026-02-28T10:00:00Z

tasks:
  - id: task-001
    status: in_progress     # todo | in_progress | done | blocked
    owner: opencode-frontend  # 谁负责
    description: 开发首页
    
  - id: task-002
    status: done
    owner: opencode-backend
    output: src/api/auth.ts   # 产出物

next_actions:
  - "opencode-frontend: 首页完成后对接 API"
```

### EVENTS.yaml - 决策日志

记录所有重要决定，方便以后追溯：

```yaml
events:
  - type: decision
    time: 2026-02-28T09:00:00Z
    content: "决定用 React 不用 Vue"
    reason: "团队更熟悉 React，生态更好"
    
  - type: blocker
    time: 2026-02-28T10:00:00Z
    content: "后端 API 文档不完整"
    resolved: false
```

---

## 📦 包含内容

| 文件 | 用途 |
|------|------|
| `pm-init.sh` | 创建新项目 |
| `pm-task.sh` | 添加任务 |
| `pm-update.sh` | 更新任务状态 |
| `pm-status.sh` | 查看项目进度 |
| `pm-event.sh` | 记录事件 |

---

## 🚀 快速开始

### 1. 安装

```bash
# 克隆 skills
git clone git@github.com:JasonFang1993/openclaw-skills.git ~/.openclaw/skills

# 设置环境变量
export PROJECTS_DIR="$HOME/projects"
```

### 2. 创建项目

```bash
cd ~/.openclaw/skills/pm-toolkit/scripts
./pm-init.sh my-app "做一个 AI 助手"
```

输出：
```
📁 创建项目: my-app
✅ 项目已创建: ~/projects/my-app

下一步:
  pm-task.sh my-app --id task-001 --desc '第一个任务'
```

### 3. 添加任务

```bash
./pm-task.sh my-app --id frontend-home --desc "开发首页" --owner opencode-frontend
./pm-task.sh my-app --id backend-api --desc "开发 API" --owner opencode-backend
./pm-task.sh my-app --id test-api --desc "写测试" --owner opencode-qa
```

### 4. 派给 AI 员工

```bash
# 前端员工
tmux new -d -s opencode-frontend "opencode run '读取 ~/projects/my-app/STATE.yaml，找到 owner=opencode-frontend 的任务，完成后用 pm-update.sh 更新状态'"

# 后端员工
tmux new -d -s opencode-backend "opencode run '读取 ~/projects/my-app/STATE.yaml，找到 owner=opencode-backend 的任务，完成后用 pm-update.sh 更新状态'"
```

### 5. 查看进度

```bash
./pm-status.sh my-app
```

输出：
```
📊 my-app 状态
================

📋 总任务: 3
⏳ 待办: 1 | 🔵 进行中: 1 | ✅ 完成: 1 | 🚧 阻塞: 0

✅ 已完成:
  - backend-api: 开发 API → src/api/auth.ts

🔵 进行中:
  - frontend-home: 开发首页

⏳ 待办:
  - test-api: 写测试

最后更新: 2026-02-28T10:30:00Z
```

### 6. 记录决策

```bash
./pm-event.sh my-app --type decision --content "用 React 不用 Vue" --reason "团队更熟悉"
```

---

## 📋 完整命令参考

### pm-init.sh - 初始化项目

```bash
pm-init.sh <项目名> [描述]
```

示例：
```bash
pm-init.sh ai-product "做一个 AI 产品"
```

### pm-task.sh - 添加任务

```bash
pm-task.sh <项目名> --id <任务ID> --desc <描述> [--owner <负责人>]
```

示例：
```bash
pm-task.sh my-app --id task-001 --desc "开发登录页面" --owner opencode-frontend
```

### pm-update.sh - 更新状态

```bash
pm-update.sh <项目名> --task <任务ID> --status <状态> [--output <产出>] [--notes <备注>]
```

状态选项：`todo` | `in_progress` | `done` | `blocked`

示例：
```bash
# 开始做
pm-update.sh my-app --task task-001 --status in_progress

# 做完了
pm-update.sh my-app --task task-001 --status done --output "src/index.ts"

# 遇到问题
pm-update.sh my-app --task task-002 --status blocked --notes "等待后端 API"
```

### pm-status.sh - 查看状态

```bash
pm-status.sh <项目名>
```

### pm-event.sh - 记录事件

```bash
pm-event.sh <项目名> --type <类型> --content <内容> [--reason <原因>]
```

类型选项：`decision` | `blocker` | `pivot` | `progress`

示例：
```bash
# 记录决策
pm-event.sh my-app --type decision --content "用 React 不用 Vue" --reason "团队熟悉"

# 记录阻塞
pm-event.sh my-app --type blocker --content "API 文档不完整"

# 记录方向调整
pm-event.sh my-app --type pivot --content "从付费改免费" --reason "市场调研显示"
```

---

## 🧠 AI 员工如何使用

### 给 AI 的指令模板

```
你是一个项目经理 AI。

1. 读取 ~/projects/<项目名>/STATE.yaml
2. 找到 owner=你的名字 的任务
3. 完成开发
4. 用 pm-update.sh 更新状态
5. 用 pm-event.sh 记录重要决策
6. 提交 git

示例指令：
pm-update.sh my-app --task task-001 --status done --output "src/index.ts"
```

### AI 自主工作流程

```
AI 员工:
1. 读取 STATE.yaml
2. 找到自己的任务 (owner=自己)
3. 开始开发
4. 更新状态为 in_progress
5. 开发完成
6. 更新状态为 done，填写 output
7. 记录 event (如果有决策)
8. 提交 git
```

---

## 📊 项目结构

```
projects/
├── my-app/
│   ├── STATE.yaml      # 任务状态
│   ├── EVENTS.yaml    # 事件日志
│   ├── README.md      # 项目说明
│   └── src/           # 代码
│
├── another-project/
│   ├── STATE.yaml
│   └── EVENTS.yaml
│
└── PROJECT_REGISTRY.yaml  # 项目索引
```

---

## 🔄 完整项目流程示例

### Step 1: 规划 (监工)

```bash
# 创建项目
pm-init.sh ai-assistant "AI 助手产品"

# 添加任务
pm-task.sh ai-assistant --id ui-home --desc "首页 UI" --owner opencode-ui
pm-task.sh ai-assistant --id ui-login --desc "登录页" --owner opencode-ui
pm-task.sh ai-assistant --id api-auth --desc "认证 API" --owner opencode-backend
pm-task.sh ai-assistant --id api-chat --desc "对话 API" --owner opencode-backend
pm-task.sh ai-assistant --id test-api --desc "API 测试" --owner opencode-qa
```

### Step 2: 派活 (监工)

```bash
# 前端团队
tmux new -d -s opencode-ui "opencode run '...'

# 后端团队  
tmux new -d -s opencode-backend "opencode run '...'

# 测试团队
tmux new -d -s opencode-qa "opencode run '...'
```

### Step 3: 执行 (AI 员工)

AI 们自行：
- 读取 STATE.yaml
- pick 自己的任务
- 开发
- 更新状态

### Step 4: 监控 (监工)

```bash
pm-status.sh ai-assistant
```

### Step 5: 验收 (监工)

- 代码审查
- 测试
- 合并发布

---

## ⚙️ 配置选项

### 环境变量

```bash
# 项目目录 (默认: ~/projects)
export PROJECTS_DIR="$HOME/projects"
```

---

## ❓ 常见问题

### Q: 一个人还需要用这个吗？

A: 小项目不需要。多个 AI 协作、复杂项目、大任务分工时才需要。

### Q: 一定要用 tmux 吗？

A: 可以用其他方式启动 AI，只要让 AI 能访问 STATE.yaml 就行。

### Q: Git 集成是必须的吗？

A: 推荐使用，能记录所有变更历史。

### Q: 怎么让 AI 知道自己的任务？

A: 在派活时告诉 AI："你的 owner 是 opencode-frontend，读取 STATE.yaml 找到你的任务"。

---

## 🔗 相关技能

- [link-to-knowledge](/link-to-knowledge) - 网页知识保存
- [OpenClaw Subagents](https://github.com/openclaw/openclaw) - 多 AI 协作

---

## ✅ 总结

| 特性 | 说明 |
|------|------|
| 多 AI 协作 | 多个 AI 通过文件自行协调 |
| 状态追踪 | 任务状态实时更新 |
| 决策记录 | 所有重要决定都有记录 |
| Git 集成 | 变更历史可追溯 |
| 简单易用 | 命令行工具，上手快 |

---

## 🚀 下一步

1. 运行 `pm-init.sh` 创建第一个项目
2. 添加任务
3. 启动 AI 员工
4. 查看进度

---

## 🔍 代码审查整合

### 完整工作流

```
AI 完成开发 → pm-update --status pending_review → 自动审查 → 通过 → done
                                                      ↓
                                                 失败 → 打回
```

### 审查流程

| 步骤 | AI | 说明 |
|------|-----|------|
| 1 | 完成开发 | - |
| 2 | 更新状态 | `pm-update.sh --status pending_review --review` |
| 3 | 自动触发 | 3 个 AI 同时审查 |
| 4 | 审查通过 | 自动标记 done |
| 5 | 审查失败 | 打回重做 |

### 3 个 AI 审查

| AI | 职责 |
|-----|------|
| Codex | 主力审查，抓逻辑错误 |
| Gemini | 安全审查，发现漏洞 |
| Claude Code | 设计审查，防止过度设计 |

### 使用方法

```bash
# AI 完成后，触发代码审查
pm-update.sh my-app --task task-001 --status pending_review --review

# 或者直接完成（跳过审查）
pm-update.sh my-app --task task-001 --status done --output "src/index.ts"
```

### 手动触发审查

```bash
pm-review.sh my-app task-001
```

### 审查输出示例

```
🔍 开始代码审查: my-app / task-001
================================
任务: 开发首页
负责人: opencode-frontend
产出: src/index.ts

🤖 启动 Code Review...

🔴 Codex 审查中...
✅ Codex: 通过 - 代码逻辑正确，无明显错误

🟡 Gemini 审查中...
✅ Gemini: 通过 - 无安全漏洞

🔵 Claude Code 审查中...
✅ Claude Code: 通过 - 设计合理

================================
✅ 代码审查完成!

📝 任务 task-001 审查通过，已标记为完成
```

### 状态流转

```
todo → in_progress → pending_review → done
                              ↓
                           blocked (审查失败)
```


---

## 🔔 阻塞通知

### 自动通知

当任务标记为 `blocked` 时，自动发送通知：

```bash
# 阻塞时自动通知
pm-update.sh my-app --task task-001 --status blocked --notes "等后端 API"

# 输出:
# 🚧 任务阻塞，将发送通知...
# 📢 发送阻塞通知...
# ✅ Discord/Telegram 通知已发送
```

### 通知渠道

| 渠道 | 环境变量 |
|------|----------|
| Discord | `DISCORD_WEBHOOK` |
| Telegram | `TELEGRAM_BOT_TOKEN` + `TELEGRAM_CHAT_ID` |

### 配置示例

```bash
# Discord
export DISCORD_WEBHOOK="https://discord.com/api/webhooks/xxx"

# Telegram
export TELEGRAM_BOT_TOKEN="123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
export TELEGRAM_CHAT_ID="123456789"
```

### 通知类型

| 类型 | 触发 | 颜色 |
|------|------|------|
| blocked | 任务阻塞 | 🔴 红色 |
| done | 任务完成 | 🟢 绿色 |
| failed | 任务失败 | 🔴 红色 |
| review | 需要审查 | 🟡 黄色 |

---

## ⚙️ 完整流程

```
AI 执行任务
    ↓
状态更新 pm-update.sh --status done/blocked
    ↓
    ├── done → 自动触发代码审查
    │           ├── 通过 → 真正完成
    │           └── 失败 → 打回
    │
    └── blocked → 自动发送通知
                    └── Discord/Telegram
```


---

## 🧪 测试整合

### 自动测试流程

```
代码审查通过 → 自动运行测试 → 通过 → 完成
                              ↓
                           失败 → 打回
```

### 支持的测试框架

| 语言 | 测试命令 |
|------|----------|
| Node.js | `npm test` |
| Rust | `cargo test` |
| Go | `go test ./...` |
| Python | `pytest` |

### 完整流程

```
AI 完成开发
    ↓
pm-update.sh --status done
    ↓
🔍 3 个 AI 审查
    ↓
🧪 自动运行测试
    ↓
✅ 通过 → 真正完成
❌ 失败 → 打回重做
```

### 状态流转

```
todo → in_progress → done → testing → done
                              ↓
                         testing_failed → 打回
```

### 测试输出示例

```
🧪 开始测试: my-app / task-001
================================
📦 检测到 Node.js 项目
🚀 运行测试: npm test

  PASS  test/app.test.js
  PASS  test/api.test.js

================================
✅ 测试通过!

📝 任务 task-001 测试通过，已完成
```

