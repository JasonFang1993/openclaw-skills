#!/bin/bash
# pm-test.sh - 自动测试

PROJECTS_DIR="${PROJECTS_DIR:-$HOME/projects}"

if [ -z "$1" ] || [ -z "$2" ]; then
    echo "用法: pm-test.sh <项目名> <任务ID>"
    echo ""
    echo "自动运行项目测试"
    exit 1
fi

PROJECT="$1"
TASK_ID="$2"

PROJECT_DIR="$PROJECTS_DIR/$PROJECT"

echo "🧪 开始测试: $PROJECT / $TASK_ID"
echo "================================"

# 检测项目类型
if [ -f "$PROJECT_DIR/package.json" ]; then
    echo "📦 检测到 Node.js 项目"
    TEST_CMD="npm test"
elif [ -f "$PROJECT_DIR/Cargo.toml" ]; then
    echo "📦 检测到 Rust 项目"
    TEST_CMD="cargo test"
elif [ -f "$PROJECT_DIR/go.mod" ]; then
    echo "📦 检测到 Go 项目"
    TEST_CMD="go test ./..."
elif [ -f "$PROJECT_DIR/pytest.ini" ] || [ -f "$PROJECT_DIR/pyproject.toml" ]; then
    echo "📦 检测到 Python 项目"
    TEST_CMD="pytest"
else
    echo "⚠️ 未检测到测试框架，跳过测试"
    exit 0
fi

echo ""
echo "🚀 运行测试: $TEST_CMD"
echo ""

# 运行测试
cd "$PROJECT_DIR"
if $TEST_CMD; then
    echo ""
    echo "================================"
    echo "✅ 测试通过!"
    
    # 更新状态
    python3 << PYEOF
import yaml

state_file = "$PROJECTS_DIR/$PROJECT/STATE.yaml"

try:
    with open(state_file, 'r') as f:
        state = yaml.safe_load(f)
    
    for task in state.get('tasks', []):
        if task.get('id') == "$TASK_ID":
            if task.get('status') == 'testing':
                task['status'] = 'done'
                task['test_result'] = 'passed'
                print(f"✅ 任务 $TASK_ID 测试通过，已完成")
                break
    
    with open(state_file, 'w') as f:
        yaml.dump(state, f, default_flow_style=False, allow_unicode=True)
except Exception as e:
    print(f"更新状态失败: {e}")
PYEOF
    
    echo ""
    # 发送通知
    cd "$(dirname "$0")"
    ./pm-notify.sh done "$PROJECT" "任务 $TASK_ID 测试通过"
    
else
    echo ""
    echo "================================"
    echo "❌ 测试失败!"
    
    # 更新状态
    python3 << PYEOF
import yaml

state_file = "$PROJECTS_DIR/$PROJECT/STATE.yaml"

try:
    with open(state_file, 'r') as f:
        state = yaml.safe_load(f)
    
    for task in state.get('tasks', []):
        if task.get('id') == "$TASK_ID":
            task['status'] = 'testing_failed'
            task['test_result'] = 'failed'
            print(f"❌ 任务 $TASK_ID 测试失败")
            break
    
    with open(state_file, 'w') as f:
        yaml.dump(state, f, default_flow_style=False, allow_unicode=True)
except Exception as e:
    print(f"更新状态失败: {e}")
PYEOF
    
    echo ""
    # 发送通知
    cd "$(dirname "$0")"
    ./pm-notify.sh failed "$PROJECT" "任务 $TASK_ID 测试失败"
    
    exit 1
fi
