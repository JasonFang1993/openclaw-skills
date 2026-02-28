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
| 🤖 AI 总结 | 用 OpenCode (minimax) 提取标题、核心观点、结论、标签 |
| 📝 双文件输出 | 原文 + 总结分开存储 |
| 🏷️ 自动标签 | AI 自动生成标签 |

## 输出结构

```
Obsidian Vault/
├── articles/
│   └── {年份}/
│       └── {月份}/
│           └── {标题}.md      # 原文
└── summaries/
    └── {年份}/
        └── {月份}/
            └── {标题}-summary.md  # AI 总结
```

## Frontmatter 格式

```yaml
---
title: "文章标题"
source: "原始URL"
tags: ["标签1", "标签2"]
date: "2026-02-28"
---
```

## 使用方法

### 命令行

```bash
# 基本用法
link-to-knowledge.sh "https://example.com/article"

# 指定 vault 路径
link-to-knowledge.sh "https://example.com" --vault ~/Obsidian/MyVault
```

### 环境变量

```bash
# 设置默认 vault 路径
export OBSIDIAN_VAULT="/path/to/your/vault"

# 然后直接运行
link-to-knowledge.sh "https://example.com"
```

## 依赖

| 依赖 | 说明 |
|------|------|
| curl | 网页抓取 |
| opencode | AI 总结（需要配置 minimax 模型）|
| python3 | JSON 解析 |

## 注意事项

1. **API 配置**: 确保 opencode 已配置 minimax 或其他模型
2. **vault 路径**: 首次使用需设置 `OBSIDIAN_VAULT` 环境变量
3. **内容长度**: 原文限制 20000 字符
4. **文件名**: 自动 sanitized，确保兼容文件系统

## 示例输出

### 原文笔记 (articles/2026/02/example.md)
```markdown
---
title: "Example Article"
source: "https://example.com/article"
tags: ["科技", "AI"]
date: "2026-02-28"
---

# Example Article

...原文内容...
```

### 总结笔记 (summaries/2026/02/example-summary.md)
```markdown
---
title: "Example Article - 总结"
source: "https://example.com/article"
tags: ["科技", "AI"]
date: "2026-02-28"
---

本文主要讨论了 AI 的发展趋势和未来影响。核心观点包括...
```

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
    
    📄 原文: articles/2026/02/xxx.md
    📄 总结: summaries/2026/02/xxx-summary.md
```

### 自动处理流程

```
收到 URL → jina-reader 抓取 → OpenCode 总结 → 写入 knowledge-base
```
