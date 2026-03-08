# OpenClaw Updates Skill

自动获取 OpenClaw 最新动态，包括 GitHub Releases、热门讨论和 Twitter 更新。

## 功能

- 📊 版本检查 - 对比当前版本与最新版本
- 🐙 GitHub Releases - 获取最新版本发布说明
- ⚠️ Breaking Changes - 提醒破坏性更新
- 💬 热门讨论 - GitHub Discussions 热点
- 🐦 Twitter 更新 - @openclaw 最新帖子

## 使用方法

```bash
# 全部更新（默认）
openclaw-updates

# 只看 GitHub
openclaw-updates --github

# 只看 Twitter
openclaw-updates --twitter

# 只检查版本
openclaw-updates --check
```

## 输出示例

```
🦞 OpenClaw 最新动态
================================

📊 版本检查
---
当前版本: 2026.3.2
最新版本: v2026.3.2
✅ 已是最最新

🐙 GitHub Releases
---
版本: v2026.3.2
日期: 2026-03-03

⚠️ Breaking Changes:
（显示 Breaking 更新）

💬 热门讨论:
  2👍 [Ideas] Vaultwarden...
  1👍 [Ideas] Subagent...

🐦 Twitter @openclaw
---
（最新帖子内容）
```

## 依赖

- curl
- jq
- openclaw (用于检查当前版本)

## 定时任务

建议添加到 heartbeat 或 cron：

```bash
# 每天早上 9 点检查
0 9 * * * openclaw-updates --check
```

## 文件结构

```
openclaw-updates/
├── SKILL.md
└── scripts/
    └── openclaw-updates.sh
```

## 更新日志

- 2026-03-07: 初始版本
