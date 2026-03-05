---
name: markdown-to-html
description: Markdown转HTML工具
---

# Markdown转HTML

## 常用工具

### 1. 命令行
```bash
# marked
npm install -g marked
marked input.md > output.html

# pandoc
pandoc input.md -o output.html
```

### 2. 在线工具
- Dillinger
- Markdown Live Preview
- StackEdit

### 3. VS Code插件
- Markdown All in One
- Markdown Preview Enhanced

## 常用转换

```bash
# 基础转换
pandoc README.md -o README.html

# 自定义模板
pandoc README.md --template=template.html -o README.html

# 带样式的HTML
pandoc README.md -c style.css -o README.html
```

## 常用参数

| 参数 | 说明 |
|-----|------|
| -o | 输出文件 |
| -c | 样式文件 |
| --template | 自定义模板 |
| -t | 输出格式 |

## 输出格式

支持：HTML, PDF, DOCX, EPUB, LaTeX
