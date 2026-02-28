# pm-toolkit

去中心化项目管理工具箱 - 让多个 AI 员工自行协调工作。

## 🎯 一句话说明

用 **STATE.yaml** 让多个 AI 自己协调任务，自动记录进度和决策。

## 👥 适合谁

- 需要多个 AI 同时干活
- 复杂项目需要分工
- 想记录每个决策原因

## 🚀 快速开始

```bash
# 1. 创建项目
pm-init.sh my-app "做一个 AI 产品"

# 2. 添加任务
pm-task.sh my-app --id task-1 --desc "开发首页" --owner opencode-frontend
pm-task.sh my-app --id task-2 --desc "开发 API" --owner opencode-backend

# 3. 派给 AI
tmux new -d -s opencode-frontend "opencode run '...'

# 4. 查看进度
pm-status.sh my-app
```

## 📦 包含命令

| 命令 | 用途 |
|------|------|
| `pm-init.sh` | 创建项目 |
| `pm-task.sh` | 添加任务 |
| `pm-update.sh` | 更新状态 |
| `pm-status.sh` | 查看进度 |
| `pm-event.sh` | 记录决策 |

## 📖 详细文档

见 [SKILL.md](SKILL.md)

## 🔗 相关技能

- [link-to-knowledge](/link-to-knowledge) - 网页知识保存
