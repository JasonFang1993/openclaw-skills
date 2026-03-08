#!/bin/bash
# pm-event.sh - 记录项目事件

PROJECTS_DIR="${PROJECTS_DIR:-$HOME/projects}"

if [ -z "$1" ] || [ -z "$2" ]; then
    echo "用法: pm-event.sh <项目名> --type <decision|blocker|pivot|progress> --content <内容> [--reason <原因>]"
    exit 1
fi

PROJECT="$1"
shift

TYPE=""
CONTENT=""
REASON=""

while [ $# -gt 0 ]; do
    case "$1" in
        --type) TYPE="$2"; shift 2 ;;
        --content) CONTENT="$2"; shift 2 ;;
        --reason) REASON="$2"; shift 2 ;;
        *) shift ;;
    esac
done

if [ -z "$TYPE" ] || [ -z "$CONTENT" ]; then
    echo "错误: 需要 --type 和 --content"
    exit 1
fi

PROJECT_DIR="$PROJECTS_DIR/$PROJECT"
EVENTS_FILE="$PROJECT_DIR/EVENTS.yaml"

if [ ! -f "$EVENTS_FILE" ]; then
    echo "错误: 项目 $PROJECT 不存在"
    exit 1
fi

echo "📝 记录事件: $TYPE - $CONTENT"

python3 << PYEOF
import yaml

events_file = "$EVENTS_FILE"

with open(events_file, 'r') as f:
    events = yaml.safe_load(f)

# 添加新事件
new_event = {
    'type': "$TYPE",
    'time': "$(date -Iseconds)",
    'content': "$CONTENT"
}

if "$REASON":
    new_event['reason'] = "$REASON"

if 'events' not in events:
    events['events'] = []

events['events'].append(new_event)

with open(events_file, 'w') as f:
    yaml.dump(events, f, default_flow_style=False, allow_unicode=True)

print(f"✅ 事件已记录: $TYPE")
PYEOF

# Git 提交
cd "$PROJECT_DIR"
git add EVENTS.yaml 2>/dev/null
git commit -m "feat: add $TYPE event" 2>/dev/null || true
