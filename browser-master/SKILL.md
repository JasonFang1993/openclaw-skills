---
name: browser-master
description: 超级浏览器搜索技能 - 整合免费工具的智能选择决策树，支持基础抓取、反检测、垂直平台
metadata:
  openclaw:
    emoji: "🕷️"
    requires:
      bins: ["node", "python3", "pip", "npm"]
      env: []
  version: "1.0.0"
  author: "Clawd"
  license: "MIT"
---

# 🕷️ Browser Master Skill

> 版本: 1.0.0  
> 只做免费的，付费的不考虑

## 概述

这是一个整合了多种免费浏览器自动化工具的超级 Skill，能够根据不同场景自动选择最合适的工具。

## 工具选择决策树

```
用户请求
    │
    ▼
┌─────────────────────────────────────┐
│  判断：需要 JS 渲染吗？              │
└─────────────────────────────────────┘
    │
    ├── 是 ──→ Playwright / Puppeteer
    │              │
    │              ▼
    │         ┌─────────────────────────────────────┐
    │         │  判断：反爬检测吗？                   │
    │         └─────────────────────────────────────┘
    │              │
    │              ├── 是 ──→ Camoufox → 成功
    │              │              │
    │              │              ▼
    │              │         失败 → 升级反检测 → 成功
    │              │
    │              └── 否 ──→ Playwright → 返回内容
    │
    └── 否 ──→ curl-cffi
                 │
                 ▼
            ┌─────────────────────────────────────┐
            │  判断：成功获取？                      │
            └─────────────────────────────────────┘
                 │
                 ├── 是 ──→ 返回内容
                 │
                 └── 否 ──→ Playwright → 返回内容
```

## 垂直平台支持

| 平台 | 工具 | 调用方式 |
|------|------|----------|
| Twitter | twitter-scraper | `node scripts/twitter.js <关键词>` |
| Reddit | reddit-scraper | `python scripts/reddit.py <关键词>` |
| 微信 | weixin-reader | `node scripts/weixin.js <链接>` |
| 小红书 | xiaohongshu-mcp | MCP 调用 |

## 工具注册表

### 1. curl-cffi（快速 HTTP）

```bash
# 使用方式
python3 -c "
from curl_cffi import requests
r = requests.get('https://example.com')
print(r.text)
"
```

**适用场景**：
- 简单静态页面
- API 接口
- 无 JS 渲染需求

**优点**：
- 速度快
- 资源占用低
- TLS 指纹伪造

### 2. Playwright（浏览器自动化）

```bash
# 使用方式
npx playwright screenshot --full-page https://example.com example.png
```

**适用场景**：
- 复杂 JS 页面
- 需要交互（点击、滚动）
- 动态内容

**优点**：
- 官方维护
- 跨浏览器支持
- 活跃社区

### 3. Camoufox（反检测浏览器）

```bash
# 使用方式
distrobox-enter pybox -- python3.14 scripts/camoufox-fetch.py <URL>
```

**适用场景**：
- Cloudflare 站点
- DataDome 保护
- Airbnb/Yelp

**优点**：
- 绕过 Turnstile
- 浏览器指纹隐藏
- 自动处理验证码

## 反检测升级路径

```
Level 1: curl-cffi
    ↓ 失败
Level 2: Playwright + stealth
    ↓ 失败
Level 3: Camoufox
    ↓ 失败
Level 4: 返回错误，建议手动处理
```

## 使用示例

### 示例 1：抓取普通网页

```
用户：帮我抓取百度首页
→ 判断：静态页面
→ curl-cffi
→ 成功 → 返回内容
```

### 示例 2：抓取 Cloudflare 站点

```
用户：抓取某 Cloudflare 保护站点
→ curl-cffi → 失败
→ Playwright → 失败
→ Camoufox → 成功 → 返回内容
```

### 示例 3：抓取 Twitter

```
用户：搜索 OpenClaw 相关推文
→ 判断：Twitter 平台
→ twitter-scraper
→ 返回结果
```

## 前置依赖

| 依赖 | 安装命令 |
|------|----------|
| Node.js | `apt install nodejs` |
| Python | `apt install python3` |
| pip | `python3 -m pip install --upgrade pip` |
| Playwright | `npm install -g playwright && playwright install` |
| curl-cffi | `pip install curl-cffi` |
| Camoufox | `python3 -m pip install camoufox` |

## 测试验证

### 基础功能测试

| # | 测试 | 命令 | 预期 |
|---|------|------|------|
| 1 | 抓取百度 | curl-cffi | 返回 HTML |
| 2 | 抓取知乎 | Playwright | 返回内容 |
| 3 | 抓取 GitHub | curl-cffi | 返回 HTML |
| 4 | Cloudflare | Camoufox | 返回内容 |
| 5 | Twitter | twitter-scraper | 返回推文 |
| 6 | Reddit | reddit-scraper | 返回帖子 |
| 7 | 微信 | weixin-reader | 返回文章 |
| 8 | 小红书 | xiaohongshu | 返回内容 |

### 性能测试

| # | 测试 | 目标 |
|---|------|------|
| 1 | 并发请求 | 5/5 成功 |
| 2 | 响应时间 | ≤5秒 |
| 3 | 内存占用 | ≤500MB |

## 错误处理

| 错误码 | 说明 | 处理方式 |
|--------|------|----------|
| E001 | curl-cffi 失败 | 升级 Playwright |
| E002 | Playwright 失败 | 升级 Camoufox |
| E003 | Camoufox 失败 | 返回错误，建议手动 |
| E004 | 平台不支持 | 提示不支持 |
| E005 | 网络超时 | 重试 3 次 |

## 维护计划

- **每周**：检查依赖更新
- **每月**：运行测试用例
- **每季度**：评估新工具

## 更新日志

| 版本 | 日期 | 内容 |
|------|------|------|
| 1.0.0 | 2026-03-09 | 初始版本 |
