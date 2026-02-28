# pm-toolkit

去中心化项目管理工具箱 - 让多个 AI 员工自行协调工作。

## 🎯 一句话说明

用 **STATE.yaml** 让多个 AI 自己协调任务，自动审查代码，自动通知。

## 👥 适合谁

- 需要多个 AI 同时干活
- 复杂项目需要分工
- 需要代码审查保证质量
- 需要自动通知

## 🚀 快速开始

```bash
# 1. 创建项目
pm-init.sh my-app "做一个 AI 产品"

# 2. 添加任务
pm-task.sh my-app --id task-1 --desc "开发首页" --owner opencode-frontend

# 3. 派给 AI
tmux new -d -s opencode-frontend "opencode run '...'"

# 4. AI 完成后（自动审查）
pm-update.sh my-app --task task-1 --status done

# 5. AI 遇到阻塞（自动通知）
pm-update.sh my-app --task task-2 --status blocked --notes "等后端 API"
```

## 📦 包含命令

| 命令 | 用途 |
|------|------|
| `pm-init.sh` | 创建项目 |
| `pm-task.sh` | 添加任务 |
| `pm-update.sh` | 更新状态，自动审查+通知 |
| `pm-status.sh` | 查看进度 |
| `pm-event.sh` | 记录决策 |
| `pm-review.sh` | 手动审查 |
| `pm-notify.sh` | 手动通知 |

## 🛡️ 自动化

- **完成时**: 自动触发 3 AI 代码审查
- **阻塞时**: 自动发送 Discord/Telegram 通知

## 📖 详细文档

见 [SKILL.md](SKILL.md)
