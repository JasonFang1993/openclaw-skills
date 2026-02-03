# 🤖 OpenClaw Skills Collection

本仓库包含 OpenClaw AI 助手安装的所有实用技能（Skills），方便团队成员安装使用。

## 📦 技能列表

| 技能名称 | 功能描述 | 安装难度 |
|---------|---------|---------|
| **browser-use** | 云端浏览器自动化（需 API Key） | ⭐⭐ |
| **browser-cash** | 匿名浏览器 session，防检测 | ⭐⭐ |
| **kesslerio-stealth-browser** | 反机器人浏览器，绕过验证 | ⭐⭐⭐ |
| **ddg-search** | DuckDuckGo 免费网页搜索 | ⭐ |
| **jina-reader** | 网页内容提取（Jina AI） | ⭐ |
| **research-company** | 公司调研，生成 PDF 报告 | ⭐ |
| **skill-creator** | 创建新技能指南 | ⭐ |

---

## 🚀 快速安装

### 方法 1：ClawHub CLI（推荐）

```bash
# 安装单个 skill
npx clawhub@latest install <skill-name>

# 示例：安装浏览器自动化
npx clawhub@latest install browser-use

# 安装所有 skill
for skill in browser-use browser-cash kesslerio-stealth-browser ddg-search jina-reader research-company skill-creator; do
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

### 7. 🛠️ skill-creator（创建新技能指南）

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
├── skill-creator/       # 技能创建指南
│   └── SKILL.md
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

## 📞 支持

- 遇到问题：查看各技能目录下的 `SKILL.md`
- 贡献代码：欢迎提交 PR
- 建议反馈：联系团队负责人

---

## 📝 更新日志

### v1.0.0 (2026-02-03)
- 初始版本
- 添加 7 个核心技能
- 完成中文文档

---

*本仓库由 OpenClaw AI 助手维护*
