---
name: link-to-knowledge
description: 将网页链接自动转换为 Obsidian 笔记，包含原文和 AI 总结。使用 OpenCode (minimax) 进行 AI 分析。适用于知识收集场景。
---

# link-to-knowledge

将网页链接转换为 Obsidian 笔记的 skill。自动抓取网页内容并用 AI 提取关键信息。

## 功能

| 功能 | 说明 |
|------|------|
| 🔗 URL 识别 | 自动从消息中提取 URL |
| 📥 网页抓取 | 使用 jina-reader 抓取完整内容 |
| 🤖 AI 总结 | 用 OpenCode (minimax) 提取标题、核心观点、标签 |
| 📝 单文件存储 | 原文 + 总结合并在一个文件 |
| 🏷️ 标签分类 | 按第一个 AI 标签自动归类 |
| 📋 索引更新 | 自动更新搜索索引 |

## 输出结构

```
knowledge-base/
├── AI/                         # 按标签分类（AI 生成的第一个标签）
│   └── ai-trends-2026.md      # 合并笔记（原文+总结）
├── 产品/
│   └── product-ideas.md
├── 编程/
│   └── rust-tutorial.md
├── 未分类/                      # 没有标签时
└── .index/
    └── index.md               # 搜索索引
```

## 单文件格式

```markdown
---
title: "AI 趋势 2026"
source: "https://..."
tags: ["AI", "趋势"]
date: "2026-02-28"
---

# AI 趋势 2026

> 来源: https://...

---

## 📥 原文摘要

[抓取的网页内容]

---

## 💡 AI 总结

[AI 提取的核心观点]

---

## 🗣️ 我的想法

[你补充的想法]

---

*保存时间: 2026-02-28*
```

## 使用方法

### 命令行

```bash
# 基本用法
link-to-knowledge.sh "https://example.com/article"

# 指定 vault 路径
link-to-knowledge.sh "https://example.com" --vault ~/Obsidian/knowledge-base
```

### 环境变量

```bash
# 设置默认 vault 路径
export OBSIDIAN_VAULT="/path/to/your/vault"
```

## 依赖

| 依赖 | 说明 |
|------|------|
| curl | 网页抓取 |
| opencode | AI 总结（需要配置 minimax 模型）|
| python3 | JSON 解析 |

---

## 📱 频道使用方式

### 触发方式

| 场景 | 怎么说 |
|------|--------|
| 保存链接 | `保存 https://...` |
| 收藏文章 | `收藏这个 https://...` |
| 记笔记 | `把这个文章保存到知识库` |

### 对话示例

```
你: https://mp.weixin.qq.com/s/AnjwroZWApvWddOienW0Ng

AI: 📥 检测到链接，正在抓取...
    🤖 AI 分析中...
    ✅ 已保存!
    
    📄 笔记: AI/ai-trends-2026.md
    🏷️ 标签: AI, 趋势
```

---

## 💾 存储与检索

### 本地存储 (Obsidian Vault)

```
knowledge-base/
├── AI/                    # 标签目录
│   └── xxx.md           # 笔记文件
├── 产品/
│   └── xxx.md
├── .index/
│   └── index.md          # 索引（Cmd+K 搜索）
└── inbox/                # 待整理
```

### 检索方式

| 方式 | 操作 |
|------|------|
| 按标签 | 打开对应文件夹 |
| 全局搜索 | Cmd+K 搜索关键字 |
| 索引 | 打开 .index/index.md |
| Graph View | Obsidian 右下角 graph 查看关联 |

---

## 🔄 远程备份

### GitHub

```
GitHub: github.com/JasonFang1993/knowledge-base
```

### 自动同步

```bash
# crontab (每 30 分钟)
*/30 * * * * cd ~/Obsidian/knowledge-base && git add -A && git commit -m "chore: sync" && git push
```

---

## 🛠️ 初始化设置

```bash
# 1. 克隆
git clone git@github.com:JasonFang1993/knowledge-base.git ~/Obsidian/knowledge-base

# 2. 设置环境变量
echo 'export OBSIDIAN_VAULT="$HOME/Obsidian/knowledge-base"' >> ~/.bashrc

# 3. 打开 Obsidian → 选 vault → knowledge-base
```

---

## 📋 日常使用

| 操作 | 怎么做 |
|------|--------|
| 保存 | 发链接到 Discord: `保存 https://...` |
| 阅读 | 打开 Obsidian |
| 搜索 | Cmd+K 或按标签找 |
| 补充 | 在 "我的想法" 区域添加笔记 |
| 同步 | 自动 crontab 或手动 git push |
