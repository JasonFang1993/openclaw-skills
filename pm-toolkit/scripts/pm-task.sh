#!/bin/bash
# pm-task.sh - 添加新任务

PROJECTS_DIR="${PROJECTS_DIR:-$HOME/projects}"

if [ -z "$1" ] || [ -z "$2" ]; then
    echo "用法: pm-task.sh <项目名> --id <任务ID> --desc <描述> [--owner <负责人>]"
    exit 1
fi

PROJECT="$1"
shift

TASK_ID=""
DESCRIPTION=""
OWNER="unassigned"

# 解析参数
while [ $# -gt 0 ]; do
    case "$1" in
        --id) TASK_ID="$2"; shift 2 ;;
        --desc) DESCRIPTION="$2"; shift 2 ;;
        --owner) OWNER="$2"; shift 2 ;;
        *) shift ;;
    esac
done

if [ -z "$TASK_ID" ] || [ -z "$DESCRIPTION" ]; then
    echo "错误: 需要 --id 和 --desc"
    exit 1
fi

PROJECT_DIR="$PROJECTS_DIR/$PROJECT"
STATE_FILE="$PROJECT_DIR/STATE.yaml"

if [ ! -f "$STATE_FILE" ]; then
    echo "错误: 项目 $PROJECT 不存在"
    echo "先运行: pm-init.sh $PROJECT"
    exit 1
fi

echo "📝 添加任务: $TASK_ID"

# 使用 python3 更新 YAML
python3 << PYEOF
import yaml
import sys

state_file = "$STATE_FILE"

with open(state_file, 'r') as f:
    state = yaml.safe_load(f)

# 添加新任务
new_task = {
    'id': "$TASK_ID",
    'status': 'todo',
    'description': "$DESCRIPTION",
    'owner': "$OWNER",
    'created': "$(date -Iseconds)"
}

if 'tasks' not in state:
    state['tasks'] = []

state['tasks'].append(new_task)
state['updated'] = "$(date -Iseconds)"

with open(state_file, 'w') as f:
    yaml.dump(state, f, default_flow_style=False, allow_unicode=True)

print(f"✅ 任务已添加: $TASK_ID")
PYEOF

# Git 提交
cd "$PROJECT_DIR"
git add STATE.yaml 2>/dev/null
git commit -m "feat: add task $TASK_ID" 2>/dev/null || true
