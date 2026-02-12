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
| **browser-use** | 云端浏览器自动化（需 API Key） | ⭐⭐ |
| **browser-cash** | 匿名浏览器 session，防检测 | ⭐⭐ |
| **kesslerio-stealth-browser** | 反机器人浏览器，绕过验证 | ⭐⭐⭐ |
| **ddg-search** | DuckDuckGo 免费网页搜索 | ⭐ |
| **jina-reader** | 网页内容提取（Jina AI） | ⭐ |
| **research-company** | 公司调研，生成 PDF 报告 | ⭐ |
| **http-client** | HTTP 客户端（配置文件、请求管理、历史追踪） | ⭐ |
| **github-search** | GitHub 仓库搜索（API、Stars、详细信息） | ⭐ |
| **skill-creator** | 创建新技能指南 | ⭐ |
| **drawio-diagrams** | Draw.io 图表生成（Mermaid/CSV/XML） | ⭐ |

---

## 🚀 快速安装

### 方法 1：ClawHub CLI（推荐）

```bash
# 安装单个 skill
npx clawhub@latest install <skill-name>

# 示例：安装浏览器自动化
npx clawhub@latest install browser-use

# 安装所有 skill
for skill in pdf pptx docx xlsx canvas-design webapp-testing weather weixin-reader find-skills systematic-debugging browser-use browser-cash kesslerio-stealth-browser ddg-search jina-reader research-company http-client github-search skill-creator drawio-diagrams; do
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

### 1. 🌍 browser-use（云端浏览器）

**功能**：通过 API 控制云端浏览器，执行自动化任务

**安装**：
```bash
npm install -g clawdbot  # 如果使用 Clawdbot
# 或配置 API Key
clawdbot config set skills.entries.browser-use.apiKey "your_api_key"
```

**使用**：
```bash
# 创建浏览器会话
npx clawhub@latest install browser-use

# 在 OpenClaw 中直接使用
# agent 会自动调用 browser 工具
```

**文档**：
- 官网：https://docs.cloud.browser-use.com
- 定价：$0.06/小时（新用户送 $10）

---

### 2. 🌐 browser-cash（匿名浏览器）

**功能**：提供匿名浏览器 session，绕过 Cloudflare、DataDome 等反爬机制

**安装**：
```bash
npx clawhub@latest install browser-cash
```

**配置**：
```bash
# 获取 API Key
# 访问 https://dash.browser.cash 注册

# 配置
clawdbot config set skills.entries.browser-cash.apiKey "your_key"
```

**使用**：
```bash
# 创建 session
curl -X POST "https://api.browser.cash/v1/browser/session" \
  -H "Authorization: Bearer $API_KEY" \
  -d '{"country": "US", "windowSize": "1920x1080"}'
```

---

### 3. 🥷 kesslerio-stealth-browser（反机器人浏览器）

**功能**：使用 Camoufox + Nodriver 绕过强反爬（Cloudflare Turnstile、Datadome 等）

**安装**：
```bash
npx clawhub@latest install kesslerio-stealth-browser

# 需要先安装 distrobox（Linux）
curl -s https://raw.githubusercontent.com/89luca89/distrobox/main/install | sh
```

**使用**：
```bash
# 进入容器
distrobox-enter pybox

# 使用 Camoufox 抓取
python3.14 scripts/camoufox-fetch.py "https://example.com" --headless

# 或使用 curl_cffi（纯 API）
python3.14 scripts/curl-api.py "https://api.example.com/endpoint"
```

**注意**：
- Airbnb/Yelp 等网站需要 **住宅代理**
- 首次运行会自动下载 Camoufox 浏览器（~700MB）

---

### 4. 🔍 ddg-search（DuckDuckGo 搜索）

**功能**：免费网页搜索，无需 API Key

**安装**：
```bash
npx clawhub@latest install ddg-search
```

**使用**：
```bash
# 搜索脚本
cd skills/ddg-search
bash scripts/search.sh "your search query"
```

---

### 5. 📖 jina-reader（Jina AI 网页提取）

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

### 6. 📊 research-company（公司调研）

**功能**：自动调研公司，生成专业 PDF 报告

**安装**：
```bash
npx clawhub@latest install research-company

# 安装 PDF 生成依赖
pip install reportlab
```

**使用**：
```bash
# 1. 研究阶段
# agent 会自动并行抓取：
# - 公司官网
# - 融资新闻
# - 竞争对手分析
# - 领导层信息

# 2. 生成 JSON 数据
cat > /tmp/research_data.json << 'EOF'
{
  "company_name": "Example Corp",
  "executive_summary": "...",
  "profile": { ... },
  "products": { ... },
  ...
}
EOF

# 3. 生成 PDF
python3 scripts/generate_report.py /tmp/research_data.json report.pdf
```

**输出**：专业格式的 PDF 报告，包含执行摘要、公司简介、产品/服务、目标市场、竞争对手、行业分析等章节。

---

### 7. 🌐 http-client（HTTP 客户端）

**功能**：功能完整的命令行 HTTP 客户端，支持配置文件、请求保存/加载、历史追踪、认证、自动重试、抗爬虫保护

**安装**：
```bash
npx clawhub@latest install http-client

# 或手动安装
cp -r http-client ~/.openclaw/skills/
```

**使用**：
```bash
# 基础 GET 请求
cd http-client
node bin/http-client.js -u https://httpbin.org/get --pretty

# POST 请求
node bin/http-client.js -u https://httpbin.org/post \
  -m POST \
  -d '{"name":"test"}' \
  --pretty

# 保存请求
node bin/http-client.js -u https://api.example.com/users \
  -m POST \
  --save my-api

# 加载已保存的请求
node bin/http-client.js --load my-api --pretty

# 查看历史
node bin/http-client.js --history
```

**功能特性**：
| 功能 | 描述 |
|------|------|
| HTTP 方法 | GET/POST/PUT/PATCH/DELETE |
| 认证 | Bearer、Basic Auth |
| 自动重试 | 指数退避重试 |
| 抗爬虫 | 随机 UA + 延迟 |
| 配置文件 | 保存/加载请求 |
| 历史追踪 | 自动记录历史 |
| 请求脱敏 | 敏感信息自动掩码 |

**文档**：`http-client/SKILL.md`

---

### 8. 🛠️ skill-creator（创建新技能指南）

**功能**：学习如何创建自定义技能

**安装**：
```bash
npx clawhub@latest install skill-creator
```

**使用**：查看 `SKILL.md` 学习技能开发规范。

---

## 📁 目录结构

```
openclaw-skills/
├── pdf/                    # PDF 处理
│   ├── SKILL.md
│   └── scripts/
├── pptx/                   # PPT 制作
│   ├── SKILL.md
│   └── scripts/
├── docx/                   # Word 文档
│   ├── SKILL.md
│   └── scripts/
├── xlsx/                   # Excel 数据
│   ├── SKILL.md
│   └── scripts/
├── canvas-design/          # 视觉设计
│   └── SKILL.md
├── webapp-testing/         # Web 测试
│   ├── SKILL.md
│   └── scripts/
├── weather/                # 天气查询
│   └── SKILL.md
├── weixin-reader/         # 微信文章读取
│   ├── SKILL.md
│   └── scripts/
├── find-skills/           # 搜索 skills
│   └── SKILL.md
├── systematic-debugging/    # 调试方法
│   └── SKILL.md
├── browser-use/           # 云端浏览器
│   ├── SKILL.md
│   └── references/
├── browser-cash/         # 匿名浏览器
│   └── SKILL.md
├── kesslerio-stealth-browser/  # 反机器人
│   ├── SKILL.md
│   ├── scripts/
│   └── references/
├── ddg-search/          # DuckDuckGo 搜索
│   ├── SKILL.md
│   └── scripts/
├── jina-reader/          # 网页内容提取
│   ├── SKILL.md
│   └── scripts/
├── research-company/     # 公司调研
│   ├── SKILL.md
│   ├── scripts/
│   └── references/
├── http-client/         # HTTP 客户端
│   ├── SKILL.md
│   └── bin/
├── skill-creator/       # 技能创建指南
│   └── SKILL.md
├── drawio-diagrams/     # Draw.io 图表生成
│   ├── SKILL.md
│   ├── scripts/
│   └── references/
└── README.md            # 本文件
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
sudo apt install -y python3 python3-pip
pip install --upgrade pip
```

### 浏览器依赖

```bash
# Playwright（如果需要本地浏览器）
npm install -g playwright
playwright install

# 或 Puppeteer
npm install -g puppeteer
```

---

## ⚠️ 注意事项

1. **API Key 安全**：不要将 API Key 提交到 GitHub，使用环境变量或配置文件
2. **成本控制**：云端浏览器服务可能产生费用，请关注使用量
3. **代理要求**：某些网站（如 Airbnb、Yelp）需要住宅代理
4. **遵守规则**：自动化操作请遵守网站使用条款

---

## 📦 github-search（GitHub 仓库搜索）

### 简介

使用 GitHub API 搜索开源仓库，比较项目质量，收集技术研究数据。支持关键词搜索、语言筛选、排序选项（Stars、Forks、更新时间），以及获取仓库详细信息。

### 特点

- ✅ **免费无需 API Key**：使用 GitHub 公共 API
- ✅ **多功能搜索**：关键词、语言、排序、过滤
- ✅ **详细信息获取**：仓库详情、Topics、统计数据
- ✅ **纯 Python 实现**：无外部依赖
- ✅ **JSON 输出**：方便程序解析

### 使用方式

```bash
# 进入 skill 目录
cd openclaw-skills/github-search

# 搜索仓库
python3 scripts/github_search.py search "whatsapp bot automation"

# 按语言筛选
python3 scripts/github_search.py search "machine learning" --language python

# 获取仓库详情
python3 scripts/github_search.py details aldinokemal go-whatsapp-web-multidevice

# 获取仓库 Topics
python3 scripts/github_search.py topics pedroslopez whatsapp-web.js
```

### 搜索示例

```bash
# 搜索 WhatsApp 相关项目
python3 scripts/github_search.py search "whatsapp bot automation" --per-page 10 --sort stars

# 搜索 Go 语言项目
python3 scripts/github_search.py search "docker orchestration" --language go --per-page 20

# 搜索最近更新的项目
python3 scripts/github_search.py search "api server" --sort updated --order desc
```

### 输出格式

所有命令返回 JSON 格式输出：

```json
{
  "success": true,
  "total_count": 27731,
  "items": [
    {
      "full_name": "owner/repo",
      "description": "项目描述",
      "stars": 1000,
      "forks": 100,
      "language": "JavaScript",
      "updated_at": "2026-02-09T12:00:00Z",
      "html_url": "https://github.com/owner/repo",
      "open_issues": 10,
      "license": "MIT"
    }
  ]
}
```

### 命令参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `search` | 搜索仓库 | `search "whatsapp bot"` |
| `--language` | 按语言筛选 | `--language python` |
| `--sort` | 排序方式 | `--sort stars\|forks\|updated` |
| `--order` | 排序顺序 | `--order desc\|asc` |
| `--per-page` | 结果数量 | `--per-page 20` |
| `details` | 仓库详情 | `details owner repo` |
| `topics` | 仓库标签 | `topics owner repo` |

### 速率限制

GitHub API 公共请求限制为 60 次/小时。如需更高限制：
- 使用认证请求（添加 `--token` header）
- 设置环境变量：`GITHUB_TOKEN`

---

## 📞 支持

- 遇到问题：查看各技能目录下的 `SKILL.md`
- 贡献代码：欢迎提交 PR
- 建议反馈：联系团队负责人

---

## 📝 更新日志

### v1.6.0 (2026-02-12)
- 新增 drawio-diagrams (Draw.io 图表生成工具)
  - Mermaid → Draw.io 流程图、架构图、时序图
  - CSV → Draw.io 组织架构图、网络拓扑图
  - XML → Draw.io 精细控制格式
  - 纯 Python 实现，无外部依赖
  - 本地压缩，保护隐私
  - 自动浏览器打开 Draw.io 编辑器
  - 完整使用指南 + 8个示例

### v1.5.0 (2026-02-09)
- 新增 github-search (GitHub 仓库搜索工具)
  - 使用 GitHub API 搜索开源项目
  - 支持关键词、语言筛选、排序
  - 获取仓库详细信息和 Topics
  - 纯 Python 实现，无外部依赖
  - 成功测试 WhatsApp 项目搜索（21k+ stars）

### v1.4.0 (2026-02-06)
- 新增 http-client (HTTP 客户端工具)
  - 支持配置文件 (.http-client.json)
  - 支持保存/加载/管理请求
  - 自动追踪请求历史
  - 请求脱敏，保护敏感数据
  - 支持 Bearer/Basic 认证
  - 自动重试 + 指数退避
  - 抗爬虫模式 (随机 UA)
  - 彩色输出 + JSON 格式化
  - 零依赖，原生 Node.js

### v1.3.0 (2026-02-05)
- 新增 weixin-reader (微信文章读取)

### v1.2.0 (2026-02-05)
- 新增 weixin-reader (微信文章读取)
  - 解决微信反爬虫保护
  - iPhone User-Agent 伪装
  - HTML 文本提取

### v1.1.0 (2026-02-05)
- 新增 9 个免费实用技能
  - pdf (PDF 处理)
  - pptx (PPT 制作)
  - docx (Word 文档)
  - xlsx (Excel 数据)
  - canvas-design (视觉设计)
  - webapp-testing (Web 测试)
  - weather (天气查询)
  - find-skills (搜索 skills)
  - systematic-debugging (调试方法)

### v1.0.0 (2026-02-03)
- 初始版本
- 添加 7 个核心技能
- 完成中文文档

---

## 📦 drawio-diagrams（Draw.io 图表生成）

### 简介

使用 Draw.io 从 Mermaid、CSV 或 XML 输入生成专业图表。支持三种格式：Mermaid（流程图、时序图）、CSV（组织架构图、网络拓扑图）、XML（精细控制）。

### 特点

- ✅ **三种格式**：Mermaid/CSV/XML 全面支持
- ✅ **纯 Python**：无外部依赖
- ✅ **PlantUML 输出**：Draw.io 原生支持
- ✅ **完整文档**：使用指南 + 示例

### 使用方式

```bash
# 克隆项目
git clone https://github.com/JasonFang1993/openclaw-skills.git
cd openclaw-skills/drawio-diagrams
```

### 脚本说明

| 脚本 | 功能 | 示例 |
|------|------|------|
| `mermaid2drawio.py` | Mermaid → PlantUML | `python scripts/mermaid2drawio.py "A[Start] --> B{Decision}"` |
| `csv2drawio.py` | CSV → Draw.io URL | `python scripts/csv2drawio.py "id,label,parent\nCEO,CEO,"` |
| `xml2drawio.py` | XML → Draw.io URL | `python scripts/xml2drawio.py "<mxGraphModel>..."` |

### 示例

**Mermaid 流程图：**
```bash
python scripts/mermaid2drawio.py """
A[Start] --> B{Decision}
B -->|Yes| C[Continue]
B -->|No| D[Stop]
"""
```

输出 PlantUML 格式，导入 Draw.io：**Arrange > Insert > Advanced > PlantUML (SVG)**

**CSV 组织架构图：**
```bash
python scripts/csv2drawio.py """
id,label,parent,style
CEO,CEO,,shape=rectangle
VP1,VP Sales,CEO,shape=rectangle
VP2,VP Eng,CEO,shape=rectangle
""" --type tree --title "Org Chart"
```

### 文档

- `SKILL.md` - 技能说明
- `references/usage_guide.md` - 完整使用指南
- `references/examples.md` - 示例集合

---

*本仓库由 OpenClaw AI 助手维护*
