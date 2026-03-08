---
name: seo-audit
description: 网站SEO审计与分析
---

# SEO审计

## 工具

- Google PageSpeed Insights
- Google Lighthouse
- GTmetrix
- Ahrefs / SEMrush

## 检查项

1. **技术SEO**
   - 页面加载速度
   - 移动端适配
   - XML sitemap
   - robots.txt
   - 结构化数据

2. **内容SEO**
   - Meta标题/描述
   - H1-H6层级
   - 图片alt文本
   - 关键词密度
   - 内链结构

3. **外链**
   - 反链数量
   - 域名权重
   - 垃圾链接

## 常用命令

```bash
# Lighthouse CLI
lighthouse https://example.com --output=json --output-path=report.json

# 检查sitemap
curl -s https://example.com/sitemap.xml | head -20
```

## 输出格式

```markdown
# SEO审计报告

## 分数
- 性能: X/100
- 可访问性: X/100  
- 最佳实践: X/100
- SEO: X/100

## 问题清单
1. [高] xxx
2. [中] xxx
3. [低] xxx

## 建议
-
```
