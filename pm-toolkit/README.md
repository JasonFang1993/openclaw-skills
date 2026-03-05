# pm-toolkit

去中心化项目管理工具箱 - 让多个 AI 员工自行协调工作。

## 🎯 一句话说明

用 **STATE.yaml** 让多个 AI 自己协调任务，自动审查代码，自动测试，自动通知。

## 🚀 快速开始

```bash
# 1. 创建项目
pm-init.sh my-app "做一个 AI 产品"

# 2. 添加任务
pm-task.sh my-app --id task-1 --desc "开发首页" --owner opencode-frontend

# 3. 派给 AI
tmux new -d -s opencode-frontend "opencode run '...'"

# 4. AI 完成后（自动审查+测试）
pm-update.sh my-app --task task-1 --status done
```

## 📦 包含命令

| 命令 | 用途 |
|------|------|
| `pm-init.sh` | 创建项目 |
| `pm-task.sh` | 添加任务 |
| `pm-update.sh` | 更新状态 |
| `pm-status.sh` | 查看进度 |
| `pm-event.sh` | 记录决策 |
| `pm-review.sh` | 审查+测试 |
| `pm-test.sh` | 运行测试 |
| `pm-notify.sh` | 发送通知 |

## 🛡️ 自动化

- **完成时**: 自动 3 AI 代码审查
- **审查通过**: 自动运行测试
- **阻塞时**: 自动发送通知

## 📖 详细文档

见 [SKILL.md](SKILL.md)
