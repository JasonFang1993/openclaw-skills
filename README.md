# 🤖 OpenClaw Skills Collection

本仓库包含 OpenClaw AI 助手安装的所有实用技能（Skills），方便团队成员安装使用。

## 📦 技能列表

| 技能名称 | 功能描述 | 安装难度 |
|---------|---------|---------|
| **pdf** | PDF 处理（提取、合并、创建、水印） | ⭐ |
| **pptx** | PPT 制作（幻灯片、模板、设计） | ⭐ |
| **docx** | Word 文档（报告、合同、表格） | ⭐ |
| **xlsx** | Excel 数据（表格、公式、图表） | ⭐ |
| **canvas-design** | 视觉设计（海报、艺术创作） | ⭐ |
| **webapp-testing** | Web 应用测试（Playwright） | ⭐ |
| **weather** | 天气查询（免费无需 API） | ⭐ |
| **weixin-reader** | 微信文章读取（反爬虫破解） | ⭐ |
| **find-skills** | 搜索 skills 库 | ⭐ |
| **systematic-debugging** | 系统化调试方法 | ⭐ |
| **ddg-search** | DuckDuckGo 免费网页搜索 | ⭐ |
| **jina-reader** | 网页内容提取（Jina AI） | ⭐ |
| **github-search** | GitHub 仓库搜索（API、Stars、详细信息） | ⭐ |
| **http-client** | HTTP 客户端（配置文件、请求管理、历史追踪） | ⭐ |
| **skill-creator** | 创建新技能指南 | ⭐ |
| **drawio-diagrams** | Draw.io 图表生成（Mermaid/CSV/XML） | ⭐ |
| **vue-auto-tester** | Vue 3 自动测试（Vitest + Playwright） | ⭐ |
| **news-research** | AI 行业新闻研究（RSS 聚合 + 深度分析） | ⭐ |
| **x-post-fetch** | X (Twitter) 帖子抓取（支持 auth_token） | ⭐ |
| **github-to-skills** | 将 GitHub 仓库自动转换为 AI Skills | ⭐⭐ |
| **skill-manager** | 管理 Skill 生命周期（检查更新、删除） | ⭐⭐ |
| **skill-evolution-manager** | 基于用户反馈持续改进 Skills | ⭐⭐ |

---

## 🚀 快速安装

### 方法 1：ClawHub CLI（推荐）

```bash
# 安装单个 skill
npx clawhub@latest install <skill-name>

# 示例：安装 PDF 处理
npx clawhub@latest install pdf

# 安装所有 skill
for skill in pdf pptx docx xlsx canvas-design webapp-testing weather weixin-reader find-skills systematic-debugging ddg-search jina-reader github-search http-client skill-creator drawio-diagrams vue-auto-tester news-research x-post-fetch github-to-skills skill-manager skill-evolution-manager; do
  npx clawhub@latest install $skill
done
```

### 方法 2：手动安装

```bash
# 克隆仓库
git clone https://github.com/JasonFang1993/openclaw-skills.git
cd openclaw-skills

# 安装到全局
cp -r <skill-folder> ~/.openclaw/skills/

# 或安装到 workspace
cp -r <skill-folder> <project>/skills/
```

---

## 📖 详细使用说明

### 1. 📄 pdf（PDF 处理）

**功能**：PDF 提取、合并、创建、水印

**使用**：查看 `pdf/SKILL.md`

---

### 2. 📊 pptx（PPT 制作）

**功能**：幻灯片制作、模板、设计

**使用**：查看 `pptx/SKILL.md`

---

### 3. 📝 docx（Word 文档）

**功能**：报告、合同、表格处理

**使用**：查看 `docx/SKILL.md`

---

### 4. 📈 xlsx（Excel 数据）

**功能**：表格、公式、图表处理

**使用**：查看 `xlsx/SKILL.md`

---

### 5. 🎨 canvas-design（视觉设计）

**功能**：海报、艺术创作

**使用**：查看 `canvas-design/SKILL.md`

---

### 6. 🧪 webapp-testing（Web 应用测试）

**功能**：使用 Playwright 进行 Web 测试

**使用**：查看 `webapp-testing/SKILL.md`

---

### 7. 🌤️ weather（天气查询）

**功能**：免费天气查询，无需 API Key

**使用**：查看 `weather/SKILL.md`

---

### 8. 📱 weixin-reader（微信文章读取）

**功能**：解决微信反爬虫，读取微信文章

**使用**：查看 `weixin-reader/SKILL.md`

---

### 9. 🔎 find-skills（搜索 Skills）

**功能**：搜索 skills 库

**使用**：查看 `find-skills/SKILL.md`

---

### 10. 🔧 systematic-debugging（系统化调试）

**功能**：系统化调试方法

**使用**：查看 `systematic-debugging/SKILL.md`

---

### 11. 🔍 ddg-search（DuckDuckGo 搜索）

**功能**：免费网页搜索，无需 API Key

**安装**：
```bash
npx clawhub@latest install ddg-search
```

**使用**：
```bash
cd skills/ddg-search
bash scripts/search.sh "your search query"
```

---

### 12. 📖 jina-reader（Jina AI 网页提取）

**功能**：提取网页内容，支持三种模式

**安装**：
```bash
npx clawhub@latest install jina-reader
```

**环境变量**：
```bash
export JINA_API_KEY="jina_..."
# 可选，免费额度 10M tokens
```

**使用**：
```bash
cd skills/jina-reader/scripts

# 读取 URL
./reader.sh "https://example.com/article"

# 搜索模式（返回前5条结果）
./reader.sh --mode search "AI news 2025"

# 事实核查
./reader.sh --mode ground "OpenAI founded in 2015"
```

**选项**：
| 选项 | 说明 | 默认 |
|------|------|------|
| `--mode` | read/search/ground | read |
| `--selector` | CSS 选择器提取特定区域 | - |
| `--remove` | 要移除的元素（逗号分隔） | - |
| `--format` | markdown/html/text/screenshot | markdown |

---

### 13. 🐙 github-search（GitHub 仓库搜索）

**功能**：使用 GitHub API 搜索开源仓库，比较项目质量

**安装**：
```bash
npx clawhub@latest install github-search
```

**使用**：
```bash
cd openclaw-skills/github-search

# 搜索仓库
python3 scripts/github_search.py search "whatsapp bot automation"

# 按语言筛选
python3 scripts/github_search.py search "machine learning" --language python

# 获取仓库详情
python3 scripts/github_search.py details aldinokemal go-whatsapp-web-multidevice
```

**特点**：
- ✅ 免费无需 API Key（60次/小时）
- ✅ 支持关键词、语言、排序筛选
- ✅ 纯 Python 实现，无外部依赖

---

### 14. 🌐 http-client（HTTP 客户端）

**功能**：命令行 HTTP 客户端，支持配置文件、请求保存/加载、历史追踪

**安装**：
```bash
npx clawhub@latest install http-client
```

**使用**：
```bash
cd http-client
node bin/http-client.js -u https://httpbin.org/get --pretty

# 保存请求
node bin/http-client.js -u https://api.example.com/users -m POST --save my-api

# 加载请求
node bin/http-client.js --load my-api --pretty
```

**功能特性**：
- HTTP 方法：GET/POST/PUT/PATCH/DELETE
- 认证：Bearer、Basic Auth
- 自动重试 + 指数退避
- 抗爬虫：随机 UA + 延迟

---

### 15. 🛠️ skill-creator（创建新技能指南）

**功能**：学习如何创建自定义技能

**安装**：
```bash
npx clawhub@latest install skill-creator
```

**使用**：查看 `skill-creator/SKILL.md`

---

### 16. 📐 drawio-diagrams（Draw.io 图表生成）

**功能**：从 Mermaid、CSV、XML 生成 Draw.io 图表

**安装**：
```bash
npx clawhub@latest install drawio-diagrams
```

**使用**：
```bash
cd openclaw-skills/drawio-diagrams

# Mermaid → PlantUML
python scripts/mermaid2drawio.py "A[Start] --> B[End]"

# CSV → 组织架构图
python scripts/csv2drawio.py "id,label,parent\nCEO,CEO,\nVP1,VP Sales,CEO"
```

**特点**：
- ✅ 三种格式：Mermaid/CSV/XML
- ✅ 纯 Python，无外部依赖
- ✅ 自动打开 Draw.io 编辑器

---

### 17. 🧬 vue-auto-tester（Vue 3 自动测试）

**功能**：自动测试和调试 Vue 3 项目

**安装**：
```bash
npx clawhub@latest install vue-auto-tester
```

**使用**：
```bash
cd openclaw-skills/vue-auto-tester

# 完整测试
python scripts/auto_test_vue_project.py ./my-vue-app

# 带截图对比
python scripts/auto_test_vue_project.py ./my-vue-app --screenshot
```

**依赖**：
```bash
npm install -D vitest @vue/test-utils @playwright/test
npx playwright install chromium
```

---

### 18. 📰 news-research（行业新闻研究）

**功能**：AI 行业新闻 RSS 聚合 + 深度分析

**使用**：查看 `news-research/SKILL.md`

---

### 19. 🐦 x-post-fetch（X 帖子抓取）

**功能**：X (Twitter) 帖子抓取，支持 auth_token

**使用**：查看 `x-post-fetch/SKILL.md`

---

### 20. 📦 github-to-skills（GitHub 仓库转 AI Skills）

**功能**：将 GitHub 仓库自动转换为可安装的 AI Skills

**安装**：
```bash
npx clawhub@latest install github-to-skills
```

**使用**：
```bash
# 在 OpenClaw 中直接使用
/github-to-skills https://github.com/yt-dlp/yt-dlp
```

**或手动**：
```bash
cd openclaw-skills/github-to-skills
python3 scripts/fetch_github_info.py "https://github.com/yt-dlp/yt-dlp"
```

**生成的 SKILL.md 格式**：
```yaml
---
name: yt-dlp
description: Download videos from YouTube
github_url: https://github.com/yt-dlp/yt-dlp
github_hash: a1b2c3d4e5f6...
version: 2023.12.30
created_at: 2026-02-25
---
```

---

### 23. ⚙️ skill-manager（Skill 生命周期管理）

**功能**：管理已安装的 GitHub-based Skills

**安装**：
```bash
npx clawhub@latest install skill-manager
```

**使用**：
```bash
# 检查更新
/skill-manager check

# 列出所有 skills
/skill-manager list

# 删除 skill
/skill-manager delete <name>
```

**或手动**：
```bash
cd openclaw-skills/skill-manager
python3 scripts/scan_and_check.py ~/.openclaw/workspace/skills
```

**状态说明**：
| 状态 | 说明 |
|------|------|
| Current | 与远程仓库同步 |
| Outdated | 远程有新提交 |
| Error | 无法连接远程仓库 |

---

### 24. 🔄 skill-evolution-manager（Skill 持续改进）

**功能**：基于用户反馈持续改进 Skills

**安装**：
```bash
npx clawhub@latest install skill-evolution-manager
```

**使用**：
```bash
# 保存经验到 skill
/evolve
```

**或手动**：
```bash
cd openclaw-skills/skill-evolution-manager
python3 scripts/merge_evolution.py <skill-dir> '<json-data>'
python3 scripts/smart_stitch.py <skill-dir>
```

**经验数据格式**：
```json
{
  "skill_name": "example-skill",
  "experiences": [{"situation": "...", "action": "...", "result": "..."}],
  "best_practices": ["始终检查依赖是否安装"],
  "custom_prompts": ["当用户要求生成报告时，先询问格式偏好"]
}
```

---

## 📁 目录结构

```
openclaw-skills/
├── pdf/                    # PDF 处理
├── pptx/                   # PPT 制作
├── docx/                   # Word 文档
├── xlsx/                   # Excel 数据
├── canvas-design/          # 视觉设计
├── webapp-testing/         # Web 测试
├── weather/                # 天气查询
├── weixin-reader/          # 微信文章读取
├── find-skills/            # 搜索 skills
├── systematic-debugging/   # 调试方法
├── ddg-search/             # DuckDuckGo 搜索
├── jina-reader/            # 网页内容提取
├── github-search/          # GitHub 仓库搜索
├── http-client/            # HTTP 客户端
├── skill-creator/          # 技能创建指南
├── drawio-diagrams/        # Draw.io 图表
├── vue-auto-tester/        # Vue 3 自动测试
├── news-research/           # 新闻研究
├── x-post-fetch/           # X 帖子抓取
├── github-to-skills/       # GitHub 转 Skills
├── skill-manager/          # 生命周期管理
├── skill-evolution-manager/ # 持续改进
└── README.md               # 本文件
```

---

## 🔧 依赖安装

### 通用依赖

```bash
# Linux
sudo apt update
sudo apt install -y curl jq git

# Node.js（推荐使用 nvm）
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install --lts

# Python 3.10+
sudo apt install -y python3 python3-pip python3-yaml
pip install --upgrade pip
```

### 浏览器依赖

```bash
# Playwright
npm install -g playwright
playwright install
```

---

## ⚠️ 注意事项

1. **API Key 安全**：不要将 API Key 提交到 GitHub，使用环境变量或配置文件
2. **成本控制**：云端浏览器服务可能产生费用，请关注使用量
3. **代理要求**：某些网站（如 Airbnb、Yelp）需要住宅代理
4. **遵守规则**：自动化操作请遵守网站使用条款

---

## 📞 支持

- 遇到问题：查看各技能目录下的 `SKILL.md`
- 贡献代码：欢迎提交 PR
- 建议反馈：联系团队负责人

---

## 📝 更新日志

### v1.7.0 (2026-02-25)
- 新增三个 GitHub Skills 管理工具
  - **github-to-skills**: 将 GitHub 仓库自动转换为 AI Skills
  - **skill-manager**: 管理 Skill 生命周期
  - **skill-evolution-manager**: 基于反馈持续改进 Skills
- 新增 x-post-fetch (X 帖子抓取)
- 新增 news-research (行业新闻研究)
- 整理 README 顺序

### v1.6.0 (2026-02-12)
- 新增 drawio-diagrams (Draw.io 图表生成)
- 新增 vue-auto-tester (Vue 3 自动测试)

### v1.5.0 (2026-02-09)
- 新增 github-search (GitHub 仓库搜索)

### v1.4.0 (2026-02-06)
- 新增 http-client (HTTP 客户端)

### v1.3.0 (2026-02-05)
- 新增 weixin-reader (微信文章读取)

### v1.1.0 (2026-02-05)
- 新增 9 个免费实用技能
  - pdf, pptx, docx, xlsx, canvas-design
  - webapp-testing, weather, find-skills
  - systematic-debugging

### v1.0.0 (2026-02-03)
- 初始版本，添加 7 个核心技能

---

*本仓库由 OpenClaw AI 助手维护*
