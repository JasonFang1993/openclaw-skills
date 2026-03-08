#!/bin/bash
# pm-init.sh - 初始化新项目

PROJECTS_DIR="${PROJECTS_DIR:-$HOME/projects}"

if [ -z "$1" ]; then
    echo "用法: pm-init.sh <项目名> [描述]"
    exit 1
fi

PROJECT="$1"
DESCRIPTION="${2:-新项目}"

PROJECT_DIR="$PROJECTS_DIR/$PROJECT"

echo "📁 创建项目: $PROJECT"

# 创建目录
mkdir -p "$PROJECT_DIR"

# 创建 STATE.yaml
cat > "$PROJECT_DIR/STATE.yaml" << EOF
# STATE.yaml - 项目状态文件
# 由 pm-toolkit 自动生成

project: $PROJECT
description: "$DESCRIPTION"
created: $(date -Iseconds)
updated: $(date -Iseconds)

tasks: []

next_actions: []

EOF

# 创建 EVENTS.yaml
cat > "$PROJECT_DIR/EVENTS.yaml" << EOF
# EVENTS.yaml - 事件日志
# 由 pm-toolkit 自动生成

project: $PROJECT
created: $(date -Iseconds)

events: []

EOF

# 创建 README.md
cat > "$PROJECT_DIR/README.md" << EOF
# $PROJECT

$DESCRIPTION

## 状态

查看 [STATE.yaml](STATE.yaml) 了解任务进度

## 事件

查看 [EVENTS.yaml](EVENTS.yaml) 了解所有决策和变更

## 命令

\`\`\`bash
# 更新任务状态
pm-update.sh $PROJECT --task <task-id> --status <todo|in_progress|done|blocked>

# 添加任务
pm-task.sh $PROJECT --id <task-id> --desc <描述>

# 查看状态
pm-status.sh $PROJECT
\`\`\`
EOF

# 初始化 git
cd "$PROJECT_DIR"
git init -q 2>/dev/null || true
git add -A
git commit -m "chore: init project" 2>/dev/null || true

echo "✅ 项目已创建: $PROJECT_DIR"
echo ""
echo "下一步:"
echo "  pm-task.sh $PROJECT --id task-001 --desc '第一个任务'"
