---
name: web-to-markdown
description: 将网页技术文档转换为Markdown格式再阅读
---

# 网页转Markdown阅读

## 适用场景

- 阅读飞书技术文档
- 阅读GitHub README
- 阅读API文档
- 阅读技术博客

## 使用方法

### 方法1：jina.ai Reader

```bash
curl -s "https://r.jina.ai/https://目标URL" | head -500
```

例如：
```bash
curl -s "https://r.jina.ai/https://open.feishu.cn/document/server-docs/calendar-v4/calendar-event/create"
```

### 方法2：web_fetch工具

使用OpenClaw的web_fetch工具，带maxChars参数：
```
maxChars: 15000
```

### 方法3：浏览器+快照

用browser工具打开网页，然后用snapshot获取内容。

## 工作流程

1. 用户给URL
2. 用jina.ai转Markdown
3. 读取转换后的内容
4. 分析提取关键信息

## 常见文档转换

| 平台 | URL示例 |
|------|--------|
| 飞书文档 | `https://r.jina.ai/https://open.feishu.cn/document/xxx` |
| GitHub | `https://r.jina.ai/https://github.com/user/repo` |
| 普通网页 | `https://r.jina.ai/https://example.com` |

## 优势

- 结构清晰，不漏参数
- 方便搜索
- 减少网络请求失败
