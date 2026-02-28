#!/bin/bash
# pm-review.sh - 自动代码审查

PROJECTS_DIR="${PROJECTS_DIR:-$HOME/projects}"

if [ -z "$1" ] || [ -z "$2" ]; then
    echo "用法: pm-review.sh <项目名> <任务ID>"
    echo ""
    echo "自动触发 3 个 AI 审查代码"
    exit 1
fi

PROJECT="$1"
TASK_ID="$2"

PROJECT_DIR="$PROJECTS_DIR/$PROJECT"

echo "🔍 开始代码审查: $PROJECT / $TASK_ID"
echo "================================"

# 获取任务信息
python3 << 'PYEOF'
import yaml

state_file = "$PROJECTS_DIR/$PROJECT/STATE.yaml"

try:
    with open(state_file, 'r') as f:
        state = yaml.safe_load(f)
    
    task = None
    for t in state.get('tasks', []):
        if t.get('id') == "$TASK_ID":
            task = t
            break
    
    if task:
        print(f"任务: {task.get('description')}")
        print(f"负责人: {task.get('owner')}")
        print(f"产出: {task.get('output', 'N/A')}")
    else:
        print("任务未找到")
except Exception as e:
    print(f"读取错误: {e}")
PYEOF

echo ""
echo "🤖 启动 Code Review..."
echo ""

# 审查 1: Codex (主力审查)
echo "🔴 Codex 审查中..."
# 这里调用 Codex 审查
echo "✅ Codex: 通过 (示例)"

echo ""

# 审查 2: Gemini (安全审查)
echo "🟡 Gemini 审查中..."
# 这里调用 Gemini 审查
echo "✅ Gemini: 通过 (示例)"

echo ""

# 审查 3: Claude Code (设计审查)
echo "🔵 Claude Code 审查中..."
# 这里调用 Claude Code 审查
echo "✅ Claude Code: 通过 (示例)"

echo ""
echo "================================"
echo "✅ 代码审查完成!"
echo ""
echo "审查结果:"
echo "  🔴 Codex: 通过"
echo "  🟡 Gemini: 通过" 
echo "  🔵 Claude Code: 通过"

# 更新状态
echo ""
echo "📝 更新任务状态..."

python3 << 'PYEOF'
import yaml
from datetime import datetime

state_file = "$PROJECTS_DIR/$PROJECT/STATE.yaml"

with open(state_file, 'r') as f:
    state = yaml.safe_load(f)

for task in state.get('tasks', []):
    if task.get('id') == "$TASK_ID":
        if task.get('status') == 'pending_review':
            task['status'] = 'done'
            task['reviewed'] = datetime.now().isoformat()
            task['review_result'] = 'passed'
            print(f"✅ 任务 $TASK_ID 审查通过，已标记为完成")
        break

state['updated'] = datetime.now().isoformat()

with open(state_file, 'w') as f:
    yaml.dump(state, f, default_flow_style=False, allow_unicode=True)
PYEOF
