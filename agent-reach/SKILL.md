---
name: agent-reach
description: 给 AI Agent 一键装上互联网能力。统一打包 Twitter、X、B站、YouTube、GitHub、小红书、Reddit 等平台读取工具。免费开源，兼容所有 Agent。
homepage: https://github.com/Panniantong/Agent-Reach
---

# Agent Reach

让 AI Agent 能读取全网平台的统一工具包。

## 核心理念

- **脚手架，不是框架** - 每个平台是独立工具，不满意可以换掉
- **全部免费** - 所有工具开源、API 免费
- **兼容所有 Agent** - Claude Code、OpenClaw、Cursor、Windsurf 都能用

## 功能一览

| 平台 | 功能 | 费用 |
|------|------|------|
| 🌐 网页 | 阅读任意网页 | 免费 |
| 📺 YouTube | 字幕提取 + 搜索 | 免费 |
| 📺 B站 | 字幕提取 + 搜索 | 免费 |
| 🐦 Twitter/X | 读推文、搜索、发推 | 免费（Cookie） |
| 📕 小红书 | 阅读、搜索、评论 | 免费（Cookie） |
| 🔍 全网搜索 | 语义搜索 | 免费（Exa MCP） |
| 📦 GitHub | 读仓库、搜项目 | 免费 |
| 📡 RSS | 订阅解析 | 免费 |
| Reddit | 搜索、读帖子 | 免费 |

## 与现有技能的区别

| 场景 | 推荐技能 | 说明 |
|------|---------|------|
| **读网页** | jina-reader | 更轻量，AI 优化 |
| **Twitter** | agent-reach | 功能更全，读+搜+发 |
| **X (帖子)** | x-post-fetch | 轻量快速 |
| **YouTube/B站** | agent-reach | 统一处理 |
| **GitHub** | github-search | 更专注 GitHub |
| **全网搜索** | ddg-search / tavily-search | 各有侧重 |
| **需要全部平台** | agent-reach | 一键全装 |

## 安装

### 方法 1：让 Agent 安装（推荐）

直接把这句话发给 Agent：

```
帮我安装 Agent Reach：https://raw.githubusercontent.com/Panniantong/agent-reach/main/docs/install.md
```

Agent 会自动完成：
- 安装 CLI 工具（pip install agent-reach）
- 安装系统依赖（Node.js、gh CLI 等）
- 配置搜索引擎（MCP 接入 Exa，免费）
- 注册 SKILL.md 到 skills 目录

### 方法 2：手动安装

```bash
# 安装 Python 包
pip install agent-reach

# 检测环境
agent-reach doctor
```

### 安全模式

不想自动改系统？用安全模式：

```
帮我安装 Agent Reach（安全模式）：https://raw.githubusercontent.com/Panniantong/agent-reach/main/docs/install.md
```

安装时使用 `--safe` 参数。

## 使用方法

安装完成后，直接告诉 Agent：

- "帮我看看这个链接" → 读任意网页
- "这个 GitHub 仓库是做什么的" → gh repo view
- "这个视频讲了什么" → yt-dlp 提取字幕
- "帮我看看这条推文" → xreach tweet
- "搜一下 GitHub 上有什么 LLM 框架" → gh search repos
- "帮我配 Twitter" → 配置 Cookie

不需要记命令。Agent 读了 SKILL.md 后自己知道该调什么。

## 配置平台

### Twitter/X
1. 用 Chrome 插件 [Cookie-Editor](https://chromewebstore.google.com/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm) 导出 Cookie
2. 告诉 Agent「帮我配 Twitter」

### 小红书
1. 同样导出 Cookie
2. 告诉 Agent「帮我配小红书」

⚠️ **注意**：建议用专用小号，不要用主账号（有封号风险）。

## 依赖工具

Agent Reach 底层使用的工具：

| 工具 | 用途 | Star |
|------|------|------|
| jina-reader | 网页阅读 | 9.8K |
| xreach | Twitter 读写 | - |
| yt-dlp | 视频字幕 | 148K |
| gh CLI | GitHub | - |
| feedparser | RSS | 2.3K |

## 卸载

```bash
# 预览卸载内容
agent-reach uninstall --dry-run

# 卸载（保留配置）
agent-reach uninstall --keep-config

# 完全卸载
agent-reach uninstall
```

## 参考

- 官网：https://github.com/Panniantong/Agent-Reach
- 安装文档：https://raw.githubusercontent.com/Panniantong/agent-reach/main/docs/install.md

## 使用场景建议

- **需要多个平台**：用 agent-reach，一个命令全搞定
- **只需要一个平台**：用对应的轻量技能（如只需要 Twitter 用 x-post-fetch）
- **追求轻量**：用现有单一技能，按需安装
