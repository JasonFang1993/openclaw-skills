#!/bin/bash
# link-to-knowledge: 将网页链接转换为 Obsidian 笔记

VAULT_PATH="${OBSIDIAN_VAULT:-$HOME/Obsidian/knowledge-base}"

extract_url() { echo "$1" | grep -oE 'https?://[^[:space:]]+' | head -1; }
fetch_content() { curl -s "https://r.jina.ai/http://${1#http://}" | head -c 25000; }
sanitize() { echo "$1" | tr -cd '[:alnum:][:space:]_-' | tr ' ' '-' | tr '[:upper:]' '[:lower:]' | head -c 50; }

call_ai_summary() {
    opencode run "分析以下内容，提取 title、summary(100字内)、tags(2-4个中文标签)。以 JSON 返回: {\"title\":\"...\",\"summary\":\"...\",\"tags\":[\"...\"]}

$1" 2>/dev/null | grep -oP '\{.*\}' | tail -1
}

main() {
    URL=$(extract_url "$1")
    [ -z "$URL" ] && echo "错误: 未检测到 URL" && exit 1
    
    echo "📥 抓取: $URL"
    CONTENT=$(fetch_content "$URL")
    [ -z "$CONTENT" ] && echo "错误: 无法获取内容" && exit 1
    
    echo "🤖 AI 分析中..."
    AI_RESP=$(call_ai_summary "$CONTENT")
    
    TITLE=$(echo "$AI_RESP" | python3 -c "import sys,json; print(json.load(sys.stdin).get('title','untitled'))" 2>/dev/null || echo "untitled")
    SUMMARY=$(echo "$AI_RESP" | python3 -c "import sys,json; print(json.load(sys.stdin).get('summary','无'))" 2>/dev/null || echo "无")
    TAGS=$(echo "$AI_RESP" | python3 -c "import sys,json; print(','.join(json.load(sys.stdin).get('tags',[])))" 2>/dev/null || echo "")
    
    YEAR=$(date +%Y); MONTH=$(date +%m); DATE=$(date +%Y-%m-%d)
    FILE=$(sanitize "$TITLE")
    
    # 确定目录：如果有标签，用第一个标签作为目录
    if [ -n "$TAGS" ]; then
        TAG_DIR=$(echo "$TAGS" | cut -d',' -f1)
    else
        TAG_DIR="未分类"
    fi
    
    # 创建目录
    mkdir -p "$VAULT_PATH/$TAG_DIR"
    mkdir -p "$VAULT_PATH/.index"
    
    # 写入合并的笔记（原文 + 总结）
    cat > "$VAULT_PATH/$TAG_DIR/$FILE.md" << EOF
---
title: "$TITLE"
source: "$URL"
tags: [$([ -n "$TAGS" ] && echo "\"$(echo "$TAGS" | tr ',' '","')\"" || echo "")]
date: "$DATE"
---

# $TITLE

> 来源: $URL

---

## 📥 原文摘要

$CONTENT

---

## 💡 AI 总结

$SUMMARY

---

## 🗣️ 我的想法

[在这里添加你的想法]

---

*保存时间: $DATE*
EOF

    # 更新索引
    INDEX_FILE="$VAULT_PATH/.index/index.md"
    {
        echo "---
date: $DATE
tags: [$([ -n "$TAGS" ] && echo "\"$(echo "$TAGS" | tr ',' '","')\"" || echo "")]
---

# 知识索引

## 最近保存
| 日期 | 标题 | 标签 |
|------|------|------|
| $DATE | [[../$TAG_DIR/$FILE.md|$TITLE]] | $TAGS |

" > "$INDEX_FILE.tmp"
        
        # 如果索引已存在，追加
        if [ -f "$INDEX_FILE" ]; then
            # 跳过前 6 行（frontmatter），追加内容
            tail -n +7 "$INDEX_FILE" >> "$INDEX_FILE.tmp"
            mv "$INDEX_FILE.tmp" "$INDEX_FILE"
        else
            mv "$INDEX_FILE.tmp" "$INDEX_FILE"
        fi
    } 2>/dev/null || true

    echo "✅ 完成!"
    echo "📄 笔记: $VAULT_PATH/$TAG_DIR/$FILE.md"
    echo "📋 索引: $VAULT_PATH/.index/index.md"
}

main "$@"
