#!/bin/bash
# pm-update.sh - 更新任务状态

PROJECTS_DIR="${PROJECTS_DIR:-$HOME/projects}"

if [ -z "$1" ] || [ -z "$2" ]; then
    echo "用法: pm-update.sh <项目名> --task <任务ID> --status <todo|in_progress|done|blocked> [--output <产出>] [--notes <备注>]"
    exit 1
fi

PROJECT="$1"
shift

TASK_ID=""
STATUS=""
OUTPUT=""
NOTES=""

while [ $# -gt 0 ]; do
    case "$1" in
        --task) TASK_ID="$2"; shift 2 ;;
        --status) STATUS="$2"; shift 2 ;;
        --output) OUTPUT="$2"; shift 2 ;;
        --notes) NOTES="$2"; shift 2 ;;
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
        task['updated'] = "$(date -Iseconds)"
        
        if "$STATUS" == "in_progress" and 'started' not in task:
            task['started'] = "$(date -Iseconds)"
            
        if "$STATUS" == "done" and 'completed' not in task:
            task['completed'] = "$(date -Iseconds)"
            
        if "$OUTPUT":
            task['output'] = "$OUTPUT"
            
        if "$NOTES":
            task['notes'] = "$NOTES"
            
        updated = True
        print(f"✅ 任务更新: $TASK_ID ({old_status} → $STATUS)")
        break

if not updated:
    print(f"⚠️ 任务 $TASK_ID 不存在")
    sys.exit(1)

state['updated'] = "$(date -Iseconds)"

with open(state_file, 'w') as f:
    yaml.dump(state, f, default_flow_style=False, allow_unicode=True)
PYEOF

# Git 提交
cd "$PROJECT_DIR"
git add STATE.yaml 2>/dev/null
git commit -m "chore: update $TASK_ID to $STATUS" 2>/dev/null || true
