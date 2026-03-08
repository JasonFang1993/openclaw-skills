#!/bin/bash
# weekly-review.sh - 每周复盘

KNOWLEDGE_BASE="${KNOWLEDGE_BASE:-$HOME/Obsidian/knowledge-base}"
DATE=$(date +%Y-%m-%d)
WEEK=$(date +%W)

echo "📊 生成每周复盘: 第${WEEK}周"
echo "=================="

# 创建周报目录
mkdir -p "$KNOWLEDGE_BASE/Journal/Weekly"

# 生成复盘内容
cat > "$KNOWLEDGE_BASE/Journal/Weekly/Week${WEEK}.md" << EOF
---
title: 第${WEEK}周复盘
date: $DATE
tags: [周报, 复盘]
---

# 📊 第${WEEK}周复盘 $DATE

## 📈 本周产出

（自动汇总）

### 项目进展
| 项目 | 状态 | 产出 |
|------|------|------|
|      |      |      |

## 🤔 问题复盘

### 遇到的问题
- 

### 解决方式
- 

## 🎯 下周计划

### 优先级
1. 
2. 
3. 

## 💡 AI 建议

（基于本周数据生成）

---

*由 OpenClaw 自动生成*
EOF

echo "✅ 周报已生成: Journal/Weekly/Week${WEEK}.md"
