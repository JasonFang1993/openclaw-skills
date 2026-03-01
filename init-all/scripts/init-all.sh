#!/bin/bash
# init-all.sh - 一键初始化所有配置

set -e

echo "🚀 OpenClaw 全量初始化"
echo "========================"
echo ""

# 1. 克隆所有仓库
echo "📦 第 1 步: 克隆仓库"

REPOS=(
    "git@github.com:JasonFang1993/openclaw-skills.git:$HOME/.openclaw/skills"
    "git@github.com:JasonFang1993/openclaw-memory.git:$HOME/openclaw-memory"
    "git@github.com:JasonFang1993/knowledge-base.git:$HOME/Obsidian/knowledge-base"
)

for repo in "${REPOS[@]}"; do
    IFS=':' read -r url dir <<< "$repo"
    if [ -d "$dir/.git" ]; then
        echo "  ✅ $dir 已存在"
    else
        echo "  📥 克隆 $url → $dir"
        mkdir -p "$(dirname "$dir")"
        git clone "$url" "$dir"
    fi
done

# 2. 创建目录结构
echo ""
echo "📁 第 2 步: 创建目录结构"

mkdir -p "$HOME/projects"          # PM-Toolkit 项目
mkdir -p "$HOME/Obsidian"        # Obsidian
mkdir -p "$HOME/.local/bin"      # 脚本

# 3. 设置环境变量
echo ""
echo "⚙️ 第 3 步: 环境变量"

ENV_VARS=(
    'export OBSIDIAN_VAULT="$HOME/Obsidian/knowledge-base"'
    'export PROJECTS_DIR="$HOME/projects"'
    'export PATH="$HOME/.local/bin:$PATH"'
)

SHELL_RC="$HOME/.bashrc"
[ -n "$ZSH_VERSION" ] && SHELL_RC="$HOME/.zshrc"

for var in "${ENV_VARS[@]}"; do
    if ! grep -q "$var" "$SHELL_RC" 2>/dev/null; then
        echo "$var" >> "$SHELL_RC"
    fi
done
echo "  ✅ 环境变量已添加到 $SHELL_RC"
echo "  ⚠️ 运行: source $SHELL_RC"

# 4. 配置 Cron
echo ""
echo "⏰ 第 4 步: Cron 配置"

# 检查 cron 是否已存在
CRON_TASKS=(
    "0 9 * * 1-5 $HOME/.openclaw/skills/cron-tools/scripts/daily-brief.sh"
    "0 18 * * 5 $HOME/.openclaw/skills/cron-tools/scripts/weekly-review.sh"
)

for task in "${CRON_TASKS[@]}"; do
    if ! crontab -l 2>/dev/null | grep -q "$task"; then
        (crontab -l 2>/dev/null; echo "$task") | crontab -
        echo "  ✅ 添加: $task"
    else
        echo "  ⏭️ 已存在: $task"
    fi
done

# 5. 创建软链接
echo ""
echo "🔗 第 5 步: 软链接"

# link 命令
cat > "$HOME/.local/bin/link" << 'LINKEOF'
#!/bin/bash
# 快速保存网页到知识库
$HOME/.openclaw/skills/link-to-knowledge/scripts/link-to-knowledge.sh "$1"
LINKEOF
chmod +x "$HOME/.local/bin/link"
echo "  ✅ link 命令已创建"

# pm 命令
cat > "$HOME/.local/bin/pm" << 'PMEOF'
#!/bin/bash
# PM-Toolkit 快捷命令
SCRIPT_DIR="$HOME/.openclaw/skills/pm-toolkit/scripts"
case "$1" in
    init) $SCRIPT_DIR/pm-init.sh "${@:2}" ;;
    task) $SCRIPT_DIR/pm-task.sh "${@:2}" ;;
    update) $SCRIPT_DIR/pm-update.sh "${@:2}" ;;
    status) $SCRIPT_DIR/pm-status.sh "${@:2}" ;;
    event) $SCRIPT_DIR/pm-event.sh "${@:2}" ;;
    *) echo "用法: pm <init|task|update|status|event> [参数]" ;;
esac
PMEOF
chmod +x "$HOME/.local/bin/pm"
echo "  ✅ pm 命令已创建"

echo ""
echo "========================"
echo "✅ 初始化完成!"
echo ""
echo "📋 快捷命令:"
echo "   link <url>    - 保存网页到知识库"
echo "   pm init <项目> - 创建项目"
echo "   pm status <项目> - 查看状态"
echo ""
echo "📦 已安装:"
echo "   - openclaw-skills"
echo "   - openclaw-memory"
echo "   - knowledge-base"
echo "   - cron-tools"
echo "   - pm-toolkit"
echo ""
echo "⚠️ 下一步:"
echo "   1. source ~/.bashrc"
echo "   2. 配置通知 (DISCORD_WEBHOOK)"
echo "   3. 开始使用!"
