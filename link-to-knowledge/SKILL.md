---
name: link-to-knowledge
description: 将网页链接自动转换为 Obsidian 笔记。采用 PARA 方法分类，AI 自动归类到 Projects/Areas/Resources/Archives。
---

# link-to-knowledge

将网页链接转换为 Obsidian 笔记的 skill。采用 **PARA 方法** + **Obsidian 最佳实践**。

## 功能概览

| 功能 | 说明 |
|------|------|
| 🔗 URL 识别 | 自动从消息中提取 URL |
| 📥 网页抓取 | 使用 jina.ai 抓取内容 |
| 🤖 AI 分类 | AI 自动判断 PARA 分类 |
| 🏷️ 标签生成 | AI 自动生成中文标签 |
| 📝 双链 | 自动添加 [[Wiki链接]] |
| 📋 索引更新 | 自动更新总索引 |

## PARA 方法

| 分类 | 说明 | 例子 |
|------|------|------|
| **P**rojects | 正在做的项目 | 产品上线、论文写作 |
| **A**reas | 长期负责领域 | 健康管理、理财 |
| **R**esources | 感兴趣的主题 | AI、编程、摄影 |
| **A**rchives | 已完成/暂停 | 旧项目、已过气 |

## 输出结构

```
knowledge-base/
├── 📥 Inbox/                 # 收集箱（临时）
├── 📁 Projects/              # 项目
│   └── AI/
│       └── xxx.md
├── 📁 Areas/                 # 领域
│   ├── AI/
│   │   └── ai-trends.md
│   ├── 产品/
│   └── 编程/
├── 📁 Resources/             # 资源
│   ├── AI/
│   │   └── xxx.md
│   ├── 趋势/
│   └── 工具/
├── 📁 Archives/              # 归档
└── 🔍 index.md               # 总索引
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

### 方式一：link 命令（推荐）

```bash
# 保存链接
link https://example.com/article

# 或直接运行脚本
~/.openclaw/workspace/openclaw-skills/link-to-knowledge/scripts/link-to-knowledge.sh "https://example.com"
```

### 方式二：发到 Discord

直接发送链接即可：
- `保存 https://...`
- `收藏这个 https://...`

## 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `OBSIDIAN_VAULT` | 知识库路径 | `$HOME/Obsidian/knowledge-base` |

### 配置

```bash
# 临时设置
export OBSIDIAN_VAULT="/path/to/vault"

# 永久设置（已自动配置）
echo 'export OBSIDIAN_VAULT="$HOME/Obsidian/knowledge-base"' >> ~/.bashrc
source ~/.bashrc
```

## 初始化

### 自动初始化

```bash
cd ~/.openclaw/workspace/openclaw-skills/link-to-knowledge/scripts
./init.sh
```

初始化步骤：
1. ✅ 克隆 knowledge-base 仓库
2. ✅ 创建 PARA 目录结构
3. ✅ 配置环境变量
4. ✅ 创建便捷命令 `link`

### 手动初始化

```bash
# 1. 克隆仓库
git clone git@github.com:JasonFang1993/knowledge-base.git ~/Obsidian/knowledge-base

# 2. 配置环境变量
echo 'export OBSIDIAN_VAULT="$HOME/Obsidian/knowledge-base"' >> ~/.bashrc
source ~/.bashrc
```

## 远程同步

### GitHub 仓库

- 仓库地址：github.com/JasonFang1993/knowledge-base

### 自动同步 Cron

```bash
# 每 30 分钟同步
*/30 * * * * cd ~/Obsidian/knowledge-base && git add -A && git commit -m "chore: sync" && git push
```

### 手动同步

```bash
cd ~/Obsidian/knowledge-base
git add -A
git commit -m "feat: 添加新笔记"
git push
```

## 故障排除

### 常见问题

| 问题 | 解决方案 |
|------|----------|
| 语法错误 | 确保 bash 版本 ≥ 4.0 |
| 无法抓取 | 检查网络连接 |
| AI 分析失败 | 检查 opencode 是否可用 |
| 权限错误 | 确保 vault 目录可写 |

### 测试脚本

```bash
# 语法检查
bash -n ~/.openclaw/workspace/openclaw-skills/link-to-knowledge/scripts/link-to-knowledge.sh

# 测试运行
link https://example.com
```

## 目录说明

| 目录 | 用途 |
|------|------|
| `Inbox/` | 收集箱，新保存的笔记会同步复制到这里 |
| `Projects/` | 正在进行的工作项目 |
| `Areas/` | 长期关注的领域 |
| `Resources/` | 感兴趣的主题资源 |
| `Archives/` | 已完成或暂停的内容 |
| `index.md` | 总索引，快速查看所有保存的内容 |

## 依赖

- bash ≥ 4.0
- curl
- python3 (用于 JSON 解析)
- git (用于同步)
- opencode (用于 AI 分析，可选)

---

## 📌 快速开始

```bash
# 1. 初始化（已完成）
source ~/.bashrc

# 2. 保存知识
link https://mp.weixin.qq.com/s/xxx

# 3. 查看知识库
ls ~/Obsidian/knowledge-base/
```
