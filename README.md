# 🤖 OpenClaw Skills Collection

本仓库包含 OpenClaw AI 助手安装的所有实用技能（Skills），方便团队成员安装使用。

## 📦 技能列表

### 📄 文档处理

| 技能名称 | 功能描述 |
|---------|---------|
| **pdf** | PDF 处理（提取、合并、创建，水印） |
| **pptx** | PPT 制作（幻灯片、模板，设计） |
| **docx** | Word 文档（报告、合同、表格） |
| **xlsx** | Excel 数据（表格、公式、图表） |
| **markdown-to-html** | Markdown转HTML |

### 🔍 搜索与阅读

| 技能名称 | 功能描述 |
|---------|---------|
| **ddg-search** | DuckDuckGo 免费网页搜索 |
| **jina-reader** | 网页内容提取（Jina AI） |
| **weixin-reader** | 微信文章读取（反爬虫破解） |
| **tavily-search** | Tavily AI 搜索（专为 AI 设计） |
| **web-to-markdown** | 网页转Markdown阅读（技术文档转换） |

### 🎨 设计

| 技能名称 | 功能描述 |
|---------|---------|
| **canvas-design** | 视觉设计（海报、艺术创作） |
| **web-design-guidelines** | 网页设计指南与最佳实践 |
| **frontend-design** | 前端设计与开发规范 |
| **ui-ux-pro-max** | UI/UX设计与无障碍指南 |
| **tailwind-design-system** | Tailwind CSS设计系统 |
| **ai-image-generation** | AI图像生成指南（DALL-E、Midjourney、Stable Diffusion） |

### 💻 工程

| 技能名称 | 功能描述 |
|---------|---------|
| **code-review** | 代码审查最佳实践 |
| **webapp-testing** | Web 应用测试（Playwright） |
| **vue-auto-tester** | Vue 3 自动测试（Vitest + Playwright） |
| **http-client** | HTTP 客户端（配置文件、请求管理） |
| **github-search** | GitHub 仓库搜索 |

### 📊 增长与营销

| 技能名称 | 功能描述 |
|---------|---------|
| **seo-audit** | 网站SEO审计与分析 |
| **website-health** | 网站健康检查 |
| **marketing-psychology** | 营销心理学原理与应用 |
| **pricing-strategy** | 定价策略与技巧 |

### ✍️ 写作

| 技能名称 | 功能描述 |
|---------|---------|
| **strategy-writing** | 写作策略与反思 |
| **summarize** | 摘要 URL/文件/YouTube |

### 🔧 飞书集成

| 技能名称 | 功能描述 |
|---------|---------|
| **feishu-permission-transfer** | 飞书文档权限转让 |

### 🛠️ 工具

| 技能名称 | 功能描述 |
|---------|---------|
| **github-ssh-fix** | GitHub SSH连接修复（22端口被墙） |
| **weather** | 天气查询（免费无需API） |
| **drawio-diagrams** | Draw.io 图表生成 |
| **debug-tool-capabilities** | 诊断 OpenClaw 工具能力缺失（exec/read/http） |

### 🧠 AI与研究

| 技能名称 | 功能描述 |
|---------|---------|
| **news-research** | AI行业新闻深度分析 |
| **tech-news-digest** | 技术新闻每日摘要 |
| **research-company** | 公司调研，生成PDF报告 |
| **agent-reach** | AI互联网工具全家桶（Twitter/B站/YouTube） |
| **x-post-fetch** | X (Twitter) 帖子抓取 |

### 📋 项目管理

| 技能名称 | 功能描述 |
|---------|---------|
| **pm-toolkit** | 去中心化项目管理（多AI协作） |
| **cron-tools** | 定时任务（每日简报、每周复盘） |

### 💡 知识管理

| 技能名称 | 功能描述 |
|---------|---------|
| **memory-manager** | 知识记忆管理（Obsidian集成） |
| **link-to-knowledge** | 链接转为知识库条目 |
| **notion** | Notion API（页面、数据库） |
| **obsidian** | Obsidian 笔记 |

### 🔄 自动化

| 技能名称 | 功能描述 |
|---------|---------|
| **init-all** | 一键初始化（换电脑恢复配置） |
| **skill-manager** | 管理Skill生命周期 |
| **skill-evolution-manager** | 基于反馈持续改进 |
| **github-to-skills** | GitHub仓库转AI Skills |

---

## 🚀 快速安装

### 方法 1：ClawHub CLI（推荐）

```bash
# 安装单个 skill
npx clawhub@latest install <skill-name>

# 安装所有 skill
npx clawhub@latest install all
```

### 方法 2：手动安装

```bash
# 克隆仓库
git clone https://github.com/JasonFang1993/openclaw-skills.git

# 复制到本地 skills 目录
cp -r <skill-name> ~/.openclaw/workspace/skills/
```

## 📝 添加新 Skill

1. 在仓库根目录创建 `<skill-name>/` 文件夹
2. 添加 `SKILL.md` 文件
3. 提交并推送到仓库

## 📄 License

MIT
