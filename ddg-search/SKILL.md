---
name: ddg-search
description: 使用 DuckDuckGo 进行免费网页搜索，无需 API Key。适合快速查找公开信息。
---

# DuckDuckGo Search

免费网页搜索工具，无需 API Key，快速获取公开信息。

## 特点

- ✅ **免费无需 API Key**：直接使用 DuckDuckGo
- ✅ **隐私友好**：不跟踪用户
- ✅ **快速响应**：适合简单查询
- ✅ **无请求限制**

## 与其他搜索工具的区别

| 工具 | 特点 | 适用场景 |
|------|------|---------|
| **ddg-search** | 免费、简单、无需配置 | 快速查找公开信息 |
| **jina-reader** | 内容提取 + 摘要 | 需要抓取网页内容 |
| **tavily-search** | AI 优化、语义搜索 | 复杂研究问题 |
| **github-search** | GitHub 仓库搜索 | 找代码项目 |

## 安装

```bash
npx clawhub@latest install ddg-search
```

或手动：
```bash
cd openclaw-skills/ddg-search
```

## 使用方法

### 基本搜索

```bash
# 进入目录
cd ddg-search

# 运行搜索
python3 scripts/search.py "your search query"
```

### 搜索示例

```bash
# 搜索 Python 教程
python3 scripts/search.py "python tutorial for beginners"

# 搜索最新新闻
python3 scripts/search.py "AI news 2026"

# 搜索特定主题
python3 scripts/search.py "open source alternatives to photoshop"
```

### 输出格式

返回 JSON 格式结果：
```json
{
  "results": [
    {
      "title": "Result Title",
      "url": "https://example.com",
      "snippet": "Brief description of the result..."
    }
  ]
}
```

## 脚本说明

| 脚本 | 功能 |
|------|------|
| `search.py` | 执行 DuckDuckGo 搜索 |

## 注意事项

1. **免费使用**：无需任何 API Key
2. **适合简单查询**：日常信息搜索
3. **复杂研究**：建议使用 tavily-search
4. **内容提取**：需要配合 jina-reader

## 使用场景

- 快速查找公开文档
- 搜索开源项目替代品
- 查找教程和指南
- 日常信息查询

## 依赖

- Python 3
- 无需外部库
