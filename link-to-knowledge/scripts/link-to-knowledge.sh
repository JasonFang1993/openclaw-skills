#!/bin/bash
# link-to-knowledge: 将网页链接转换为 Obsidian 笔记 (PARA 结构)

VAULT_PATH="${OBSIDIAN_VAULT:-$HOME/Obsidian/knowledge-base}"

extract_url() { echo "$1" | grep -oE 'https?://[^[:space:]]+' | head -1; }

# 根据 URL 类型选择合适的抓取方式
fetch_content() {
    local url="$1"
    local content=""
    
    if echo "$url" | grep -q "mp.weixin.qq.com"; then
        # 微信文章 → 使用 weixin-reader（过滤调试输出）
        content=$(~/.openclaw/workspace/skills/weixin-reader/scripts/reader.sh "$url" 2>/dev/null | tail -n +10)
    elif echo "$url" | grep -q "github.com"; then
        # GitHub → 尝试获取 raw 内容
        local repo_url="${url%.git}"
        local readme_url=""
        if echo "$url" | grep -q "/blob/"; then
            # 已经是文件链接，直接获取
            readme_url="${url/github.com/raw.githubusercontent.com}"
        else
            # 仓库首页，获取 README
            readme_url="$repo_url/raw/main/README.md"
        fi
        [ -n "$readme_url" ] && content=$(curl -s "$readme_url" | head -c 25000)
    else
        # 其他网页 → 使用 jina.ai
        content=$(curl -s "https://r.jina.ai/http://${url#http://}" | head -c 25000)
    fi
    
    echo "$content"
}
sanitize() { echo "$1" | tr -cd '[:alnum:][:space:]_-' | tr ' ' '-' | tr '[:upper:]' '[:lower:]' | head -c 50; }

call_ai_summary() {
    opencode run "分析以下内容，提取:
- title: 文章标题
- summary: 核心观点(50-100字)
- para: 归类到 P(项目)/A(领域)/R(资源)/A(归档)
- tags: 2-4个中文标签

以 JSON 返回: {\"title\":\"...\",\"summary\":\"...\",\"para\":\"P/A/R/A\",\"tags\":[\"...\"]}

内容: $1" 2>/dev/null | grep -oP '\{.*\}' | tail -1
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
    PARA=$(echo "$AI_RESP" | python3 -c "import sys,json; print(json.load(sys.stdin).get('para','R'))" 2>/dev/null || echo "R")
    TAGS=$(echo "$AI_RESP" | python3 -c "import sys,json; print(','.join(json.load(sys.stdin).get('tags',[])))" 2>/dev/null || echo "")
    
    YEAR=$(date +%Y); MONTH=$(date +%m); DATE=$(date +%Y-%m-%d)
    FILE=$(sanitize "$TITLE")
    
    # PARA 目录映射
    case "$PARA" in
        P) DIR="Projects" ;;
        A) DIR="Areas" ;;
        R) DIR="Resources" ;;
        *) DIR="Resources" ;;
    esac
    
    # 如果有标签，用第一个标签作为子目录
    if [ -n "$TAGS" ]; then
        SUB_DIR=$(echo "$TAGS" | cut -d',' -f1)
        SUBDIR_PATH="$DIR/$SUB_DIR"
    else
        SUBDIR_PATH="$DIR"
    fi
    
    # 创建目录
    mkdir -p "$VAULT_PATH/$SUBDIR_PATH"
    mkdir -p "$VAULT_PATH/Inbox"
    mkdir -p "$VAULT_PATH/.index"
    
    # 写入笔记
    cat > "$VAULT_PATH/$SUBDIR_PATH/$FILE.md" << EOF
---
title: "$TITLE"
source: "$URL"
tags: [$([ -n "$TAGS" ] && echo "\"$(echo "$TAGS" | tr ',' '","')\"" || echo "")]
para: $PARA
date: "$DATE"
---

# $TITLE

> 来源: [$URL]($URL)
> 分类: [[$DIR]]

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

## 🔗 相关笔记

[[Inbox/]] [[Areas/]] [[Resources/]] [[Archives/]]

---

*保存时间: $DATE | PARA: $PARA*
EOF

    # 复制到 Inbox（临时）
    cp "$VAULT_PATH/$SUBDIR_PATH/$FILE.md" "$VAULT_PATH/Inbox/$DATE-$FILE.md" 2>/dev/null || true

    # 更新索引
    INDEX_FILE="$VAULT_PATH/index.md"
    {
        echo "---
tags: [$([ -n "$TAGS" ] && echo "\"$(echo "$TAGS" | tr ',' '","')\"" || echo "")]
---

# 知识索引

## 最近保存

| 日期 | 标题 | PARA | 标签 |
|------|------|------|------|
| $DATE | [[$SUBDIR_PATH/$FILE.md|$TITLE]] | $PARA | $TAGS |

" > "$INDEX_FILE.tmp"
        
        if [ -f "$INDEX_FILE" ]; then
            tail -n +8 "$INDEX_FILE" >> "$INDEX_FILE.tmp" 2>/dev/null || true
            mv "$INDEX_FILE.tmp" "$INDEX_FILE"
        else
            mv "$INDEX_FILE.tmp" "$INDEX_FILE"
        fi
    } 2>/dev/null || true

    echo "✅ 完成!"
    echo "📄 笔记: $VAULT_PATH/$SUBDIR_PATH/$FILE.md"
    echo "📋 索引: $VAULT_PATH/index.md"
    echo "🏷️ 分类: $PARA ($DIR)"
}

main "$@"
