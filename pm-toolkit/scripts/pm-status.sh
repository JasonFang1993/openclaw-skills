#!/bin/bash
# pm-status.sh - 查看项目状态

PROJECTS_DIR="${PROJECTS_DIR:-$HOME/projects}"

if [ -z "$1" ]; then
    echo "用法: pm-status.sh <项目名>"
    exit 1
fi

PROJECT="$1"
PROJECT_DIR="$PROJECTS_DIR/$PROJECT"
STATE_FILE="$PROJECT_DIR/STATE.yaml"

if [ ! -f "$STATE_FILE" ]; then
    echo "错误: 项目 $PROJECT 不存在"
    exit 1
fi

echo "📊 $PROJECT 状态"
echo "================"
echo ""

python3 << 'PYEOF'
import yaml
import sys
from datetime import datetime

state_file = "$STATE_FILE"

with open(state_file, 'r') as f:
    state = yaml.safe_load(f)

tasks = state.get('tasks', [])

# 按状态分组
todo = [t for t in tasks if t.get('status') == 'todo']
in_progress = [t for t in tasks if t.get('status') == 'in_progress']
done = [t for t in tasks if t.get('status') == 'done']
blocked = [t for t in tasks if t.get('status') == 'blocked']

print(f"📋 总任务: {len(tasks)}")
print(f"⏳ 待办: {len(todo)} | 🔵 进行中: {len(in_progress)} | ✅ 完成: {len(done)} | 🚧 阻塞: {len(blocked)}")
print("")

if done:
    print("✅ 已完成:")
    for t in done:
        output = f" → {t.get('output', '')}" if t.get('output') else ""
        print(f"  - {t['id']}: {t.get('description', '')}{output}")

if in_progress:
    print("\n🔵 进行中:")
    for t in in_progress:
        notes = f" ({t.get('notes', '')})" if t.get('notes') else ""
        print(f"  - {t['id']}: {t.get('description', '')}{notes}")

if blocked:
    print("\n🚧 阻塞:")
    for t in blocked:
        blocked_by = f" ← {t.get('blocked_by', '')}" if t.get('blocked_by') else ""
        notes = f" ({t.get('notes', '')})" if t.get('notes') else ""
        print(f"  - {t['id']}: {t.get('description', '')}{blocked_by}{notes}")

if todo:
    print("\n⏳ 待办:")
    for t in todo:
        print(f"  - {t['id']}: {t.get('description', '')}")

print(f"\n最后更新: {state.get('updated', 'unknown')}")
PYEOF
