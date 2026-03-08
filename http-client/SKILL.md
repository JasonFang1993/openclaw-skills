---
name: http-client
description: Advanced HTTP client with config file support, saved requests, history tracking, authentication, auto-retry, anti-bot protection, and request sanitization. Works with native Node.js modules.
---

# HTTP Client Skill v2.3

一个功能完整的命令行 HTTP 客户端，支持配置文件、请求保存/加载、历史追踪、认证、自动重试、抗爬虫保护等功能。

## 目录

- [功能特性](#功能特性)
- [快速开始](#快速开始)
- [配置文件](#配置文件)
- [CLI 命令](#cli-命令)
- [编程使用](#编程使用)
- [安全特性](#安全特性)
- [错误处理](#错误处理)
- [API 参考](#api-参考)
- [示例](#示例)
- [常见问题](#常见问题)

---

## 功能特性

### 核心功能

| 功能 | 描述 | 状态 |
|------|------|------|
| HTTP 方法 | 支持 GET、POST、PUT、PATCH、DELETE | ✅ |
| 自定义 Headers | Authorization、API Key、Content-Type 等 | ✅ |
| 认证支持 | Bearer Token、Basic Auth | ✅ |
| 请求体 | 支持 JSON、Form Data、纯文本 | ✅ |
| 查询参数 | 自动拼接 URL 参数 | ✅ |
| 超时控制 | 可配置请求超时时间 | ✅ |
| 自动重试 | 指数退避重试机制 | ✅ |
| 重定向处理 | 自动跟随 301/302/307/308 | ✅ |
| 压缩支持 | gzip、deflate 自动解压 | ✅ |

### 配置文件

| 功能 | 描述 | 状态 |
|------|------|------|
| 保存请求 | 将常用请求保存为命名配置 | ✅ |
| 加载请求 | 快速加载已保存的请求 | ✅ |
| 历史追踪 | 自动记录所有请求历史 | ✅ |
| 列表管理 | 查看/删除已保存的请求 | ✅ |

### 安全特性

| 功能 | 描述 | 状态 |
|------|------|------|
| 请求脱敏 | 自动屏蔽敏感信息 | ✅ |
| Token 隐藏 | Authorization、Bearer 自动掩码 | ✅ |
| API Key 保护 | X-API-Key 等自动隐藏 | ✅ |

### 高级特性

| 功能 | 描述 | 状态 |
|------|------|------|
| 抗爬虫模式 | 随机 UA + 延迟重试 | ✅ |
| 文件下载 | 简单文件下载功能 | ✅ |
| 彩色输出 | 终端颜色高亮 | ✅ |
| JSON 格式化 | 自动美化 JSON 输出 | ✅ |

---

## 快速开始

### 安装

```bash
# 克隆项目
git clone https://github.com/JasonFang1993/openclaw-skills.git
cd openclaw-skills/http-client

# 无需安装依赖，原生 Node.js 即可运行
node bin/http-client.js --help
```

### 基本用法

```bash
# GET 请求
node bin/http-client.js -u https://httpbin.org/get --pretty

# POST 请求 (JSON)
node bin/http-client.js -u https://httpbin.org/post \
  -m POST \
  -d '{"name":"test","version":"2.3"}' \
  --pretty

# 带 Headers
node bin/http-client.js -u https://api.github.com/user \
  -H "Authorization: Bearer ghp_token" \
  --pretty
```

### 保存和加载

```bash
# 保存请求
node bin/http-client.js -u https://api.example.com/users \
  -m POST \
  -d '{"name":"John"}' \
  --save create-user

# 加载并执行
node bin/http-client.js --load create-user --pretty

# 查看所有已保存
node bin/http-client.js --list

# 查看请求历史
node bin/http-client.js --history

# 删除已保存
node bin/http-client.js --delete create-user
```

---

## 配置文件

### 配置文件位置

```
.http-client.json          # 保存的请求配置
.http-client-history.json # 请求历史记录
```

### 配置文件格式

```json
{
  "saved": {
    "github-user": {
      "url": "https://api.github.com/user",
      "method": "GET",
      "headers": {
        "Authorization": "Bearer ghp_xxxxx"
      }
    },
    "create-post": {
      "url": "https://api.example.com/posts",
      "method": "POST",
      "headers": {
        "Content-Type": "application/json"
      },
      "body": "{\"title\":\"Hello\",\"content\":\"World\"}"
    }
  },
  "defaults": {
    "timeout": 30000,
    "maxRetries": 3
  }
}
```

### 历史记录格式

```json
[
  {
    "timestamp": "2026-02-06T12:00:00.000Z",
    "url": "https://httpbin.org/uuid",
    "method": "GET",
    "status": 200,
    "duration": 267
  },
  {
    "timestamp": "2026-02-06T12:01:00.000Z",
    "url": "https://httpbin.org/post",
    "method": "POST",
    "status": 200,
    "duration": 312
  }
]
```

---

## CLI 命令

### 基础命令

| 命令 | 短格式 | 描述 |
|------|--------|------|
| `--url <url>` | `-u` | 请求 URL (必需) |
| `--method <method>` | `-m` | HTTP 方法 (默认: GET) |
| `--header <key:value>` | `-H` | 自定义请求头 |
| `--data <body>` | `-d` | 请求体 |
| `--json` | | 自动设置 Content-Type: application/json |
| `--pretty` | `-p` | 格式化输出 |
| `--output <path>` | `-o` | 下载文件到指定路径 |
| `--help` | `-h` | 显示帮助信息 |

### 认证命令

| 命令 | 描述 |
|------|------|
| `--bearer <token>` | 设置 Bearer Token Authorization |
| `--user-agent <ua>` | `-U` 设置 User-Agent |

### 高级命令

| 命令 | 描述 |
|------|------|
| `--timeout <ms>` | 设置超时时间 (默认: 30000) |
| `--max-retries <n>` | 设置最大重试次数 (默认: 3) |
| `--anti-bot` | `-a` 启用抗爬虫模式 |

### 配置管理命令

| 命令 | 描述 |
|------|------|
| `--save <name>` | 保存当前请求为 `<name>` |
| `--load <name>` | 加载已保存的 `<name>` 请求 |
| `--list` | 列出所有已保存的请求 |
| `--history` | 显示请求历史记录 |
| `--delete <name>` | 删除已保存的 `<name>` 请求 |

---

## 编程使用

### 引入模块

```javascript
const { httpRequest, downloadFile, configManager, sanitize } = require('./bin/http-client.js');
```

### 基础请求

```javascript
// GET 请求
const result = await httpRequest({
  url: 'https://httpbin.org/get',
  method: 'GET',
  timeout: 5000
});

console.log(result.status);      // 200
console.log(result.data);       // { args: {}, headers: {...}, ... }
console.log(result.raw);        // 原始响应文本
console.log(result.duration);   // 267 (ms)
```

### POST 请求

```javascript
// POST JSON
const postResult = await httpRequest({
  url: 'https://httpbin.org/post',
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: {
    name: 'John',
    email: 'john@example.com'
  }
});

console.log(postResult.data.json);
// { name: 'John', email: 'john@example.com' }
```

### 认证

```javascript
// Bearer Token
const gh = await httpRequest({
  url: 'https://api.github.com/user',
  headers: {
    'Authorization': 'Bearer ghp_your_token_here'
  }
});

// Basic Auth
const basic = await httpRequest({
  url: 'https://api.example.com/protected',
  auth: {
    username: 'user',
    password: 'pass'
  }
});

// API Key
const weather = await httpRequest({
  url: 'https://api.weather.com/v1/forecast',
  headers: {
    'X-API-Key': 'your_api_key'
  }
});
```

### 查询参数

```javascript
const result = await httpRequest({
  url: 'https://api.example.com/search',
  queryParams: {
    q: 'javascript',
    page: 1,
    limit: 10
  }
});
// 实际请求: https://api.example.com/search?q=javascript&page=1&limit=10
```

### 文件下载

```javascript
await downloadFile({
  url: 'https://example.com/file.zip',
  outputPath: './downloads/file.zip',
  headers: {
    'Authorization': 'Bearer token'
  }
});
// 输出:
// 📥 Downloading: https://example.com/file.zip
// ✅ Saved: ./downloads/file.zip (45.2 MB)
```

### 配置管理

```javascript
// 保存请求
await configManager.saveRequest('my-api', {
  url: 'https://api.example.com/data',
  method: 'POST',
  headers: {
    'Authorization': 'Bearer token'
  },
  body: {
    key: 'value'
  }
});

// 获取已保存的请求
const saved = configManager.getSaved('my-api');
// { url, method, headers, body }

// 删除已保存的请求
await configManager.deleteRequest('my-api');

// 列出所有已保存
configManager.listSaved();

// 显示历史
configManager.showHistory();
```

---

## 安全特性

### 请求脱敏

```javascript
const { sanitize } = require('./bin/http-client.js');

const sensitiveRequest = {
  url: 'https://api.github.com/user',
  headers: {
    'Authorization': 'Bearer ghp_secret_token_12345',
    'X-API-Key': 'sk-abcdefghijk'
  },
  body: '{"password":"supersecret"}'
};

console.log(sanitize(sensitiveRequest));
// 输出:
// {
//   "url": "https://api.github.com/user",
//   "headers": {
//     "Authorization": "[MASKED]",
//     "X-API-Key": "[MASKED]"
//   },
//   "body": "{\"password\":\"supersecret\"}"
// }
```

### 敏感数据检测

```javascript
const SENSITIVE_PATTERNS = [
  /Authorization:\s*Bearer\s+[a-zA-Z0-9_\-\.]+/gi,
  /X-API-Key:\s*[a-zA-Z0-9_\-\.]+/gi,
  /api[_-]?key[s]?["']?\s*[:=]\s*["']?[a-zA-Z0-9_\-\.]+/gi,
  /password["']?\s*[:=]\s*["']?[^\s&"']+/gi
];
```

---

## 错误处理

### 基本错误处理

```javascript
try {
  const result = await httpRequest({
    url: 'https://api.example.com/data',
    timeout: 5000,
    maxRetries: 3
  });
  console.log(result.data);
} catch (error) {
  console.error('请求失败:', error.message);
}
```

### 详细错误处理

```javascript
try {
  const result = await httpRequest({
    url: 'https://api.example.com/data',
    maxRetries: 3
  });
} catch (error) {
  // 网络错误
  if (error.code) {
    console.log('错误代码:', error.code);
    // ECONNRESET - 连接被重置
    // ETIMEDOUT - 连接超时
    // ENOTFOUND - DNS 解析失败
  }

  // 超时错误
  if (error.timeout) {
    console.log('请求超时:', error.timeout, 'ms');
  }

  // 可重试错误
  if (error.retryable) {
    console.log('错误可重试');
  }

  // HTTP 状态码 (在 result 中)
  if (result.status === 401) {
    console.log('未授权 - 检查 API Key');
  } else if (result.status === 403) {
    console.log('禁止访问 - 可能被反爬虫机制拦截');
    console.log('Bot Issues:', result.botIssues);
  } else if (result.status === 429) {
    console.log('请求过于频繁 - 请稍后再试');
    console.log('Retry-After:', result.headers?.['retry-after']);
  } else if (result.status >= 500) {
    console.log('服务器错误');
  }
}
```

### 抗爬虫错误

```javascript
const result = await httpRequest({
  url: 'https://example.com',
  antiBot: true  // 启用抗爬虫模式
});

// 检测到爬虫保护
if (result.botIssues) {
  console.log('被反爬虫机制拦截:', result.botIssues);
  // 可能的原因:
  // - Cloudflare
  // - 403 Forbidden
  // - 429 Rate Limited
}
```

---

## API 参考

### httpRequest(options)

发起 HTTP 请求。

**参数:**

| 属性 | 类型 | 必需 | 默认值 | 描述 |
|------|------|------|--------|------|
| `url` | string | ✅ | - | 请求 URL |
| `method` | string | ❌ | 'GET' | HTTP 方法 |
| `headers` | object | ❌ | {} | 请求头 |
| `body` | object/string | ❌ | - | 请求体 |
| `auth` | object | ❌ | - | Basic 认证 `{username, password}` |
| `queryParams` | object | ❌ | - | 查询参数 |
| `timeout` | number | ❌ | 30000 | 超时时间 (ms) |
| `maxRetries` | number | ❌ | 3 | 最大重试次数 |
| `retryDelay` | number | ❌ | 1000 | 重试间隔 (ms) |
| `antiBot` | boolean | ❌ | false | 启用抗爬虫模式 |
| `userAgent` | string | ❌ | 'default' | User-Agent |

**返回值:**

```javascript
{
  status: 200,           // HTTP 状态码
  statusMessage: 'OK',   // 状态消息
  headers: {...},        // 响应头
  raw: '{...}',         // 原始响应文本
  data: {...},           // 解析后的数据 (JSON 或 文本)
  isJSON: true,          // 是否为 JSON
  isHTML: false,         // 是否为 HTML
  isBinary: false,       // 是否为二进制
  contentLength: 1234,   // 内容长度
  url: 'https://...',    // 请求 URL
  redirected: false,     // 是否重定向
  duration: 267,         // 请求耗时 (ms)
  botIssues: null        // 反爬虫问题 (如果有)
}
```

### downloadFile(options)

下载文件。

**参数:**

| 属性 | 类型 | 必需 | 描述 |
|------|------|------|------|
| `url` | string | ✅ | 下载 URL |
| `outputPath` | string | ✅ | 保存路径 |
| `headers` | object | ❌ | 请求头 |

### configManager

配置管理器。

**方法:**

| 方法 | 描述 |
|------|------|
| `saveRequest(name, request)` | 保存请求配置 |
| `getSaved(name)` | 获取已保存的请求 |
| `deleteRequest(name)` | 删除已保存的请求 |
| `listSaved()` | 列出所有已保存 |
| `showHistory()` | 显示请求历史 |

### sanitize(obj)

脱敏处理。

**参数:**

| 属性 | 类型 | 描述 |
|------|------|------|
| `obj` | object | 请求对象 |

**返回值:** 脱敏后的对象

---

## 示例

### 完整工作流示例

```bash
# 1. 创建 API 请求并保存
node bin/http-client.js \
  -u https://api.github.com/user \
  --bearer ghp_your_token \
  --save github-me

# 2. 使用已保存的请求
node bin/http-client.js --load github-me --pretty

# 3. 查看历史
node bin/http-client.js --history

# 4. 列表管理
node bin/http-client.js --list

# 5. 删除不需要的
node bin/http-client.js --delete old-api
```

### GitHub API

```bash
# 获取用户信息
node bin/http-client.js \
  -u https://api.github.com/users/octocat \
  --pretty

# 获取仓库信息
node bin/http-client.js \
  -u https://api.github.com/repos/microsoft/vscode \
  --pretty

# 创建 Gist
node bin/http-client.js \
  -u https://api.github.com/gists \
  -m POST \
  -H "Authorization: Bearer ghp_token" \
  -H "Content-Type: application/json" \
  -d '{"description":"Test Gist","public":false,"files":{"test.txt":{"content":"Hello"}}}'
```

### Slack Webhook

```bash
node bin/http-client.js \
  -u https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXX \
  -m POST \
  -H "Content-Type: application/json" \
  -d '{"text":"Hello from HTTP Client!","channel":"#general"}'
```

### OpenAI API

```bash
node bin/http-client.js \
  -u https://api.openai.com/v1/chat/completions \
  -m POST \
  -H "Authorization: Bearer sk-your-key" \
  -H "Content-Type: application/json" \
  -d '{"model":"gpt-3.5-turbo","messages":[{"role":"user","content":"Hello!"}],"max_tokens":100}' \
  --pretty
```

### 下载文件

```bash
node bin/http-client.js \
  -u https://example.com/large-file.zip \
  -o ./downloads/file.zip
```

### 抗爬虫访问

```bash
# 使用随机 User-Agent + 自动延迟
node bin/http-client.js \
  -u https://example.com/page \
  --anti-bot \
  -U random \
  --pretty
```

---

## 常见问题

### Q: 如何设置请求超时?

```bash
node bin/http-client.js -u https://api.example.com --timeout 10000
```

### Q: 如何处理 SSL 证书错误?

该工具使用原生 Node.js `https` 模块，不支持禁用 SSL 验证。如需处理自签名证书，请使用代理或额外工具。

### Q: 如何支持代理?

可以通过环境变量设置:

```bash
export HTTP_PROXY=http://proxy.example.com:8080
export HTTPS_PROXY=http://proxy.example.com:8080
node bin/http-client.js -u https://api.example.com
```

### Q: 为什么请求被拒绝 (403)?

可能原因:
1. 缺少必要的请求头 (User-Agent, Referer 等)
2. 被反爬虫机制拦截
3. IP 被封禁

解决方案:
```bash
node bin/http-client.js -u https://example.com \
  --anti-bot \
  -U random
```

### Q: 如何查看请求详情?

```bash
node bin/http-client.js -u https://httpbin.org/headers \
  -H "X-Custom-Header: value" \
  --pretty
```

### Q: 配置文件保存在哪里?

- 保存的请求: `.http-client.json`
- 历史记录: `.http-client-history.json`

这两个文件位于执行命令的当前目录。

### Q: 如何完全重置配置?

```bash
rm -f .http-client.json .http-client-history.json
```

---

## 技术细节

### 依赖

```
Node.js >= 14 (使用原生 http/https 模块)
无外部 npm 依赖
```

### User-Agent 池

```javascript
const USER_AGENTS = [
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0',
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15'
];
```

### 自动重试策略

```
重试次数: maxRetries (默认 3)
重试间隔: retryDelay * 2^(attempt-1)
示例:
  第1次重试: 1000ms 后
  第2次重试: 2000ms 后
  第3次重试: 4000ms 后
```

---

## 贡献

欢迎提交 Issue 和 Pull Request！

- Repository: https://github.com/JasonFang1993/openclaw-skills
- Issues: https://github.com/JasonFang1993/openclaw-skills/issues

---

## 许可证

MIT License

---

**版本:** 2.3.0  
**更新日期:** 2026-02-06  
**作者:** Jason Fang
