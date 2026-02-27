#!/bin/bash
# link-to-knowledge: 将网页链接转换为 Obsidian 笔记

VAULT_PATH="${OBSIDIAN_VAULT:-$HOME/Obsidian/Vault}"

extract_url() { echo "$1" | grep -oE 'https?://[^[:space:]]+' | head -1; }
fetch_content() { curl -s "https://r.jina.ai/http://${1#http://}" | head -c 20000; }
sanitize() { echo "$1" | tr -cd '[:alnum:][:space:]_-' | tr ' ' '-' | tr '[:upper:]' '[:lower:]' | head -c 50; }

call_ai_summary() {
    opencode run "分析以下内容，提取 title、summary(50-150字)、tags(3个)。以 JSON 返回: {\"title\":\"...\",\"summary\":\"...\",\"tags\":[\"...\"]}

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
    
    TITLE=$(echo "$AI_RESP" | python3 -c "import sys,json; print(json.load(sys.stdin).get('title',''))" 2>/dev/null || echo "untitled")
    SUMMARY=$(echo "$AI_RESP" | python3 -c "import sys,json; print(json.load(sys.stdin).get('summary','无'))" 2>/dev/null || echo "无")
    TAGS=$(echo "$AI_RESP" | python3 -c "import sys,json; print(','.join(json.load(sys.stdin).get('tags',[])))" 2>/dev/null || echo "")
    
    YEAR=$(date +%Y); MONTH=$(date +%m); DATE=$(date +%Y-%m-%d)
    FILE=$(sanitize "$TITLE")
    
    # 写入原文
    mkdir -p "$VAULT_PATH/articles/$YEAR/$MONTH"
    cat > "$VAULT_PATH/articles/$YEAR/$MONTH/$FILE.md" << EOF
---
title: "$TITLE"
source: "$URL"
tags: [$([ -n "$TAGS" ] && echo "\"$(echo "$TAGS" | tr ',' '","')\"" || echo "")]
date: "$DATE"
---

$CONTENT
EOF

    # 写入总结
    mkdir -p "$VAULT_PATH/summaries/$YEAR/$MONTH"
    cat > "$VAULT_PATH/summaries/$YEAR/$MONTH/${FILE}-summary.md" << EOF
---
title: "$TITLE - 总结"
source: "$URL"
tags: [$([ -n "$TAGS" ] && echo "\"$(echo "$TAGS" | tr ',' '","')\"" || echo "")]
date: "$DATE"
---

$SUMMARY
EOF

    echo "✅ 完成!"
    echo "📄 原文: $VAULT_PATH/articles/$YEAR/$MONTH/$FILE.md"
    echo "📄 总结: $VAULT_PATH/summaries/$YEAR/$MONTH/${FILE}-summary.md"
}

main "$@"
