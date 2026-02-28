---
name: link-to-knowledge
description: 将网页链接自动转换为 Obsidian 笔记。采用 PARA 方法分类，AI 自动归类到 Projects/Areas/Resources/Archives。
---

# link-to-knowledge

将网页链接转换为 Obsidian 笔记的 skill。采用 **PARA 方法** + **Obsidian 最佳实践**。

## PARA 方法

| 分类 | 说明 | 例子 |
|------|------|------|
| **P**rojects | 正在做的项目 | 产品上线、论文写作 |
| **A**reas | 长期负责领域 | 健康管理、理财 |
| **R**esources | 感兴趣的主题 | AI、编程、摄影 |
| **A**rchives | 已完成/暂停 | 旧项目、已过气 |

## 功能

| 功能 | 说明 |
|------|------|
| 🔗 URL 识别 | 自动从消息中提取 URL |
| 📥 网页抓取 | 使用 jina-reader 抓取内容 |
| 🤖 AI 分类 | AI 自动判断 PARA 分类 |
| 🏷️ 标签生成 | AI 自动生成中文标签 |
| 📝 双链 | 自动添加 [[Wiki链接]] |
| 📋 索引更新 | 自动更新总索引 |

## 输出结构 (PARA)

```
knowledge-base/
├── 📥 Inbox/                 # 收集箱（临时）
├── 📁 Projects/              # 项目
│   └── AI/
│       └── xxx.md
├── 📁 Areas/               # 领域
│   ├── AI/
│   │   └── ai-trends.md
│   ├── 产品/
│   └── 编程/
├── 📁 Resources/            # 资源
│   ├── 趋势/
│   └── 工具/
├── 📁 Archives/            # 归档
└── 🔍 index.md            # 总索引
```

## 笔记格式

```markdown
---
title: "AI 趋势 2026"
source: "https://..."
tags: ["AI", "趋势"]
para: R
date: 2026-02-28
---

# AI 趋势 2026

> 来源: [https://...](https://...)
> 分类: [[Resources]]

---

## 📥 原文摘要

[抓取的内容]

---

## 💡 AI 总结

[核心观点]

---

## 🗣️ 我的想法

[你的笔记]

---

## 🔗 相关笔记

[[Inbox/]] [[Areas/]] [[Resources/]] [[Archives/]]

---

*保存时间: 2026-02-28 | PARA: R*
```

## 使用方法

```bash
# 基本用法
link-to-knowledge.sh "https://example.com/article"

# 指定 vault
link-to-knowledge.sh "https://example.com" --vault ~/Obsidian/knowledge-base
```

## 环境变量

```bash
export OBSIDIAN_VAULT="/path/to/your/vault"
```

---

## 📱 频道使用

### 触发方式

| 场景 | 怎么说 |
|------|--------|
| 保存链接 | `保存 https://...` |
| 收藏 | `收藏这个 https://...` |

### 对话示例

```
你: https://mp.weixin.qq.com/s/xxx

AI: 📥 检测到链接...
    🤖 AI 分析中...
    ✅ 已保存!
    
    📄 笔记: Resources/AI/ai-trends.md
    🏷️ PARA: R (Resources)
    🏷️ 标签: AI, 趋势
```

---

## 🔍 Obsidian 检索方式

| 方式 | 操作 |
|------|------|
| 按 PARA | 打开对应文件夹 |
| 按标签 | 点击 tag 或搜索 #标签 |
| 全局搜索 | Cmd+K 搜索 |
| 索引 | 打开 index.md |
| 双链 | 点击 [[笔记名]] 跳转 |
| Graph View | 右下角查看关联 |

---

## 🔄 远程同步

```bash
# GitHub
github.com/JasonFang1993/knowledge-base

# 自动同步
*/30 * * * * cd ~/Obsidian/knowledge-base && git add -A && git commit -m "chore: sync" && git push
```

---

## 🛠️ 初始化

```bash
# 1. 克隆
git clone git@github.com:JasonFang1993/knowledge-base.git ~/Obsidian/knowledge-base

# 2. 环境变量
echo 'export OBSIDIAN_VAULT="$HOME/Obsidian/knowledge-base"' >> ~/.bashrc

# 3. 打开 Obsidian
```

---

## 📋 日常使用

| 操作 | 怎么做 |
|------|--------|
| 保存 | 发链接到 Discord |
| 阅读 | Obsidian 打开 |
| 搜索 | Cmd+K / 按 PARA 找 |
| 补充 | 在 "我的想法" 区域写 |
| 归档 | 移动到 Archives 文件夹 |
