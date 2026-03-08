#!/bin/bash
# restore-memory.sh - 恢复记忆配置

set -e

echo "🧠 恢复 OpenClaw 记忆配置"
echo "==========================="
echo ""

# 克隆记忆仓库
MEMORY_REPO="git@github.com:JasonFang1993/openclaw-memory.git"
WORKSPACE="$HOME/.openclaw/workspace"

if [ -d "$WORKSPACE/.git" ]; then
    echo "  ✅ 工作区已存在"
else
    echo "  📥 克隆记忆仓库..."
    git clone "$MEMORY_REPO" "$WORKSPACE"
fi

# 需要的关键文件
KEY_FILES=(
    "SOUL.md"
    "AGENTS.md"
    "MEMORY.md"
    "USER.md"
    "IDENTITY.md"
    "TOOLS.md"
    "HEARTBEAT.md"
)

echo ""
echo "📋 恢复关键文件:"

for file in "${KEY_FILES[@]}"; do
    if [ -f "$WORKSPACE/$file" ]; then
        echo "  ✅ $file"
    else
        echo "  ⚠️ $file 不存在"
    fi
done

# 检查 skills
echo ""
echo "📦 检查 Skills:"

SKILLS_DIR="$WORKSPACE/openclaw-skills"
if [ -d "$SKILLS_DIR" ]; then
    echo "  ✅ openclaw-skills 已存在"
    cd "$SKILLS_DIR"
    git pull origin master 2>/dev/null || echo "  ⚠️ 拉取失败"
else
    echo "  📥 克隆 skills..."
    git clone git@github.com:JasonFang1993/openclaw-skills.git "$SKILLS_DIR"
fi

# 复制到 ~/.openclaw/skills
echo ""
echo "🔗 同步 Skills 到 ~/.openclaw/skills"

for skill in "$SKILLS_DIR"/*; do
    if [ -d "$skill" ]; then
        skill_name=$(basename "$skill")
        cp -r "$skill" "$HOME/.openclaw/skills/"
        echo "  ✅ $skill_name"
    fi
done

echo ""
echo "==========================="
echo "✅ 记忆恢复完成!"
echo ""
echo "📁 配置位置: $WORKSPACE"
echo "📦 Skills: ~/.openclaw/skills"
