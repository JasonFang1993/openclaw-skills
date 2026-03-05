#!/bin/bash
# daily-brief.sh - 每日简报

# 配置
KNOWLEDGE_BASE="${KNOWLEDGE_BASE:-$HOME/Obsidian/knowledge-base}"
DATE=$(date +%Y-%m-%d)
TIME=$(date +%H:%M)

echo "📰 生成每日简报: $DATE"
echo "=================="

# 获取昨天的任务完成情况
cd "$KNOWLEDGE_BASE"

# 扫描 Projects 目录的任务
echo ""
echo "📋 昨日产出:"

# 生成简报内容
cat > "$KNOWLEDGE_BASE/Journal/$DATE.md" << EOF
---
title: 每日简报 $DATE
date: $DATE
tags: [日报, 日记]
---

# 📰 每日简报 $DATE

## ⏰ 时间
$TIME

## 📋 昨日产出
（自动生成）

## 🎯 今日计划
（自动生成）

## ⚠️ 风险与阻塞
（自动生成）

## 💡 AI 建议
（基于上下文生成）

---

*由 OpenClaw 自动生成*
EOF

echo "✅ 每日简报已生成: Journal/$DATE.md"
echo ""
echo "下一步: 编辑内容，添加你的实际产出和计划"
