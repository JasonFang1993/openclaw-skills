#!/bin/bash
# pm-notify.sh - 项目通知

# 通知配置
DISCORD_WEBHOOK="${DISCORD_WEBHOOK:-}"
TELEGRAM_BOT_TOKEN="${TELEGRAM_BOT_TOKEN:-}"
TELEGRAM_CHAT_ID="${TELEGRAM_CHAT_ID:-}"

send_notification() {
    local title="$1"
    local message="$2"
    local color="${3:-"16711680"}"  # 红色
    
    echo "📢 发送通知: $title - $message"
    
    # Discord 通知
    if [ -n "$DISCORD_WEBHOOK" ]; then
        curl -s -X POST "$DISCORD_WEBHOOK" \
            -H "Content-Type: application/json" \
            -d "{
                \"embeds\": [{
                    \"title\": \"$title\",
                    \"description\": \"$message\",
                    \"color\": $color
                }]
            }" 2>/dev/null
        echo "✅ Discord 通知已发送"
    fi
    
    # Telegram 通知
    if [ -n "$TELEGRAM_BOT_TOKEN" ] && [ -n "$TELEGRAM_CHAT_ID" ]; then
        curl -s -X POST "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendMessage" \
            -d "chat_id=$TELEGRAM_CHAT_ID&text=$title%0A$message" 2>/dev/null
        echo "✅ Telegram 通知已发送"
    fi
    
    # 没有配置则输出到 stdout
    if [ -z "$DISCORD_WEBHOOK" ] && [ -z "$TELEGRAM_BOT_TOKEN" ]; then
        echo "⚠️ 未配置通知渠道，请在环境变量中设置:"
        echo "   DISCORD_WEBHOOK 或 TELEGRAM_BOT_TOKEN"
    fi
}

# 解析参数
if [ -z "$1" ]; then
    echo "用法: pm-notify.sh <类型> <项目> <消息>"
    echo ""
    echo "类型:"
    echo "  blocked   - 任务阻塞"
    echo "  done     - 任务完成"
    echo "  failed   - 任务失败"
    echo "  review   - 需要审查"
    echo ""
    echo "示例:"
    echo "  pm-notify.sh blocked my-app 'task-001 遇到问题'"
    echo "  pm-notify.sh done my-app 'task-001 已完成'"
    exit 1
fi

TYPE="$1"
PROJECT="$2"
MESSAGE="$3"

case "$TYPE" in
    blocked)
        send_notification "🚧 任务阻塞 - $PROJECT" "$MESSAGE" "16711680"  # 红色
        ;;
    done)
        send_notification "✅ 任务完成 - $PROJECT" "$MESSAGE" "65280"  # 绿色
        ;;
    failed)
        send_notification "❌ 任务失败 - $PROJECT" "$MESSAGE" "16711680"  # 红色
        ;;
    review)
        send_notification "🔍 需要审查 - $PROJECT" "$MESSAGE" "16776960"  # 黄色
        ;;
    *)
        send_notification "📢 $PROJECT" "$MESSAGE" "16776960"
        ;;
esac
