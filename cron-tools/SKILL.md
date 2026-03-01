---
name: cron-tools
description: 定时任务工具箱 - 自动生成每日简报、每周复盘。基于文章"OpenClaw进阶"的最佳实践。
---

# cron-tools

定时任务工具箱 - 让 OpenClaw 自动跑起来。

## 🎯 这是什么？

让 OpenClaw 按时产出，不需要你催：

- ⏰ 每日简报 - 每天早上自动生成
- 📊 每周复盘 - 每周五自动生成

## 🚀 快速开始

### 1. 安装

```bash
# 克隆后放到 skills
cp -r cron-tools ~/.openclaw/skills/
```

### 2. 配置 Cron

```bash
# 每天早上 9 点生成简报
crontab -e
0 9 * * 1-5 ~/.openclaw/skills/cron-tools/scripts/daily-brief.sh

# 每周五 6 点生成复盘
crontab -e
0 18 * * 5 ~/.openclaw/skills/cron-tools/scripts/weekly-review.sh
```

## 📦 包含脚本

| 脚本 | 用途 | Cron 示例 |
|------|------|----------|
| `daily-brief.sh` | 每日简报 | 0 9 * * 1-5 |
| `weekly-review.sh` | 每周复盘 | 0 18 * * 5 |

## 📝 输出位置

```
knowledge-base/
└── Journal/
    ├── 2026-02-28.md      # 每日简报
    └── Weekly/
        └── Week09.md     # 每周复盘
```

## ⚙️ 配置

### 环境变量

```bash
# 知识库位置
export KNOWLEDGE_BASE="$HOME/Obsidian/knowledge-base"
```

## 🎯 最佳实践

### 最小可用 Cron（2 条）

```bash
# 🌞 工作日早上 9 点：每日简报
0 9 * * 1-5 /root/.openclaw/skills/cron-tools/scripts/daily-brief.sh

# 🍻 周五下午 6 点：每周复盘
0 18 * * 5 /root/.openclaw/skills/cron-tools/scripts/weekly-review.sh
```

### 常见坑

| 坑 | 解决方案 |
|-----|----------|
| task 太泛 | 给结构、给长度、给角色 |
| 产出没地方放 | 固定沉淀到 Obsidian |

## 📖 相关文章

- [OpenClaw 进阶：从会用到用好](https://mp.weixin.qq.com/s/PCQ_k3sktq7ETnBaSAVwRg)
