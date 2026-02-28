#!/bin/bash
# pm-update.sh - 更新任务状态

PROJECTS_DIR="${PROJECTS_DIR:-$HOME/projects}"

if [ -z "$1" ] || [ -z "$2" ]; then
    echo "用法: pm-update.sh <项目名> --task <任务ID> --status <状态> [--output <产出>] [--notes <备注>] [--review]"
    echo ""
    echo "状态选项:"
    echo "  todo           - 待办"
    echo "  in_progress    - 进行中"
    echo "  pending_review - 待审查 (自动触发代码审查)"
    echo "  done           - 已完成"
    echo "  blocked        - 阻塞"
    echo ""
    echo "示例:"
    echo "  # 完成后自动审查"
    echo "  pm-update.sh my-app --task task-001 --status done --output src/index.ts --review"
    echo ""
    echo "  # 直接完成（不审查）"
    echo "  pm-update.sh my-app --task task-001 --status done --output src/index.ts"
    exit 1
fi

PROJECT="$1"
shift

TASK_ID=""
STATUS=""
OUTPUT=""
NOTES=""
AUTO_REVIEW=false

while [ $# -gt 0 ]; do
    case "$1" in
        --task) TASK_ID="$2"; shift 2 ;;
        --status) STATUS="$2"; shift 2 ;;
        --output) OUTPUT="$2"; shift 2 ;;
        --notes) NOTES="$2"; shift 2 ;;
        --review) AUTO_REVIEW=true; shift ;;
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
import subprocess
import os

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
        print(f"✅ 任务更新: $TASK_ID ({old_status} → $STATUS)")
        
        # 如果是待审查状态，需要触发代码审查
        if "$STATUS" == "pending_review":
            print(f"⏳ 等待代码审查...")
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

# 如果开启自动审查且状态为待审查
if [ "$AUTO_REVIEW" = true ]; then
    echo ""
    echo "🚀 自动触发代码审查..."
    cd "$(dirname "$0")"
    ./pm-review.sh "$PROJECT" "$TASK_ID"
fi
