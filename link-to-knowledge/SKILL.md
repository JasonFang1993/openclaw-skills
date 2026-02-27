---
name: link-to-knowledge
description: 将网页链接转换为 Obsidian 笔记，自动提取 AI 总结。使用 OpenCode (minimax) 进行 AI 分析。
---

# link-to-knowledge

将网页链接转换为 Obsidian 笔记的 skill。

## 功能

1. 检测用户消息中的 URL
2. 使用 jina-reader 抓取网页内容
3. 使用 OpenCode (minimax) 提取关键信息（标题、核心观点、结论、标签）
4. 写入 Obsidian vault：
   - 原文 → `articles/年份/月份/标题.md`
   - 总结 → `summaries/年份/月份/标题-summary.md`

## 前置要求

- `curl` 命令
- `opencode` (用于 AI 总结)
- Obsidian vault 目录

## 使用方法

```bash
# 基本用法
./scripts/link-to-knowledge.sh <URL>

# 指定 vault 路径
./scripts/link-to-knowledge.sh <URL> --vault ~/MyNotes
```

## 环境变量

```bash
export OBSIDIAN_VAULT="/path/to/your/vault"
```
