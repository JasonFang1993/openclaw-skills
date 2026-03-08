---
name: website-health
description: 网站健康检查
---

# 网站健康检查

## 快速检查项

### 1. 可访问性
```bash
curl -s -o /dev/null -w "%{http_code}" https://example.com
curl -s -I https://example.com | grep -i "content-type"
```

### 2. SSL证书
```bash
openssl s_client -connect example.com:443 -servername example.com 2>/dev/null | openssl x509 -noout -dates
```

### 3. 性能
```bash
# TTFB
curl -s -o /dev/null -w "%{time_starttransfer}" https://example.com

# 页面大小
curl -s -I https://example.com | grep -i "content-length"
```

### 4. 常见问题
- 死链检查
- 重定向链
- 混合内容(HTTP/HTTPS)
- 缺少的安全头

## 自动化工具

- Google PageSpeed Insights
- GTmetrix
- WebPageTest
- SSL Labs

## 输出模板

```markdown
# 网站健康报告

## 状态
- HTTP状态: 200
- SSL: 有效
- TTFB: Xms

## 问题
1. [高] xxx
2. [中] xxx

## 建议
-
```
