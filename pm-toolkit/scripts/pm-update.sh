#!/bin/bash
# pm-update.sh - 更新任务状态（自动触发代码审查 + 阻塞通知）

PROJECTS_DIR="${PROJECTS_DIR:-$HOME/projects}"

if [ -z "$1" ] || [ -z "$2" ]; then
    echo "用法: pm-update.sh <项目名> --task <任务ID> --status <状态> [--output <产出>] [--notes <备注>] [--no-review] [--no-notify]"
    echo ""
    echo "状态选项:"
    echo "  todo           - 待办"
    echo "  in_progress    - 进行中"
    echo "  done           - 已完成 (自动触发代码审查)"
    echo "  blocked        - 阻塞 (自动通知)"
    echo ""
    echo "示例:"
    echo "  # 完成后自动审查（默认）"
    echo "  pm-update.sh my-app --task task-001 --status done --output src/index.ts"
    echo ""
    echo "  # 阻塞时自动通知"
    echo "  pm-update.sh my-app --task task-001 --status blocked --notes '等后端 API'"
    exit 1
fi

PROJECT="$1"
shift

TASK_ID=""
STATUS=""
OUTPUT=""
NOTES=""
SKIP_REVIEW=false
SKIP_NOTIFY=false

while [ $# -gt 0 ]; do
    case "$1" in
        --task) TASK_ID="$2"; shift 2 ;;
        --status) STATUS="$2"; shift 2 ;;
        --output) OUTPUT="$2"; shift 2 ;;
        --notes) NOTES="$2"; shift 2 ;;
        --no-review) SKIP_REVIEW=true; shift ;;
        --no-notify) SKIP_NOTIFY=true; shift ;;
        *) shift ;;
    esac
done

if [ -z "$TASK_ID" ] || [ -z "$STATUS" ]; then
    echo "错误: 需要 --task 和 --status"
    exit 1
fi

PROJECT_DIR="$PROJECTS_DIR/$PROJECT"
STATE_FILE="$PROJECT_DIR/STATE.yaml"

if [ ! -f "$STATE_FILE" ]; then
    echo "错误: 项目 $PROJECT 不存在"
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "🔄 更新任务: $TASK_ID → $STATUS"

python3 << PYEOF
import yaml
from datetime import datetime

state_file = "$STATE_FILE"

with open(state_file, 'r') as f:
    state = yaml.safe_load(f)

# 找到并更新任务
updated = False
for task in state.get('tasks', []):
    if task.get('id') == "$TASK_ID":
        old_status = task.get('status')
        task['status'] = "$STATUS"
        task['updated'] = datetime.now().isoformat()
        
        if "$STATUS" == "in_progress" and 'started' not in task:
            task['started'] = datetime.now().isoformat()
            
        if "$STATUS" == "done" and 'completed' not in task:
            task['completed'] = datetime.now().isoformat()
            
        if "$OUTPUT":
            task['output'] = "$OUTPUT"
            
        if "$NOTES":
            task['notes'] = "$NOTES"
            
        updated = True
        
        # 完成后自动审查（除非明确跳过）
        if "$STATUS" == "done" and "$SKIP_REVIEW" != "true":
            task['needs_review'] = True
            print(f"✅ 任务更新: $TASK_ID ({old_status} → $STATUS)")
            print(f"⏳ 将自动触发代码审查...")
        else:
            print(f"✅ 任务更新: $TASK_ID ({old_status} → $STATUS)")
            
        # 阻塞时通知
        if "$STATUS" == "blocked" and "$SKIP_NOTIFY" != "true":
            task['needs_notify'] = True
            print(f"🚧 任务阻塞，将发送通知...")
        break

if not updated:
    print(f"⚠️ 任务 $TASK_ID 不存在")
    exit(1)

state['updated'] = datetime.now().isoformat()

with open(state_file, 'w') as f:
    yaml.dump(state, f, default_flow_style=False, allow_unicode=True)
PYEOF

# Git 提交
cd "$PROJECT_DIR"
git add STATE.yaml 2>/dev/null
git commit -m "chore: update $TASK_ID to $STATUS" 2>/dev/null || true

# 完成后自动审查
if [ "$STATUS" = "done" ] && [ "$SKIP_REVIEW" != "true" ]; then
    echo ""
    echo "🚀 自动触发代码审查..."
    cd "$SCRIPT_DIR"
    ./pm-review.sh "$PROJECT" "$TASK_ID"
elif [ "$STATUS" = "done" ] && [ "$SKIP_REVIEW" = "true" ]; then
    echo "⏭️ 已跳过代码审查"
fi

# 阻塞时通知
if [ "$STATUS" = "blocked" ] && [ "$SKIP_NOTIFY" != "true" ]; then
    echo ""
    echo "📢 发送阻塞通知..."
    cd "$SCRIPT_DIR"
    ./pm-notify.sh blocked "$PROJECT" "任务 $TASK_ID 被阻塞: $NOTES"
elif [ "$STATUS" = "blocked" ] && [ "$SKIP_NOTIFY" = "true" ]; then
    echo "⏭️ 已跳过通知"
fi
