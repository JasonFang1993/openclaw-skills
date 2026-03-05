#!/bin/bash
# link-to-knowledge 初始化脚本
# 只需运行一次，之后重复运行会自动跳过已完成的步骤

set -e

echo "🔧 link-to-knowledge 初始化"
echo "=============================="

# 1. 检查是否已在运行目录
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

# 2. 知识库目录
KB_DIR="${OBSIDIAN_VAULT:-$HOME/Obsidian/knowledge-base}"

echo ""
echo "📁 第 1 步: 克隆知识库"

if [ -d "$KB_DIR/.git" ]; then
    echo "✅ 知识库已存在，跳过克隆"
    cd "$KB_DIR"
    echo "📥 拉取最新..."
    git pull origin main 2>/dev/null || echo "⚠️ 拉取失败，可能是离线模式"
else
    echo "📂 克隆知识库到: $KB_DIR"
    mkdir -p "$(dirname "$KB_DIR")"
    git clone git@github.com:JasonFang1993/knowledge-base.git "$KB_DIR"
    cd "$KB_DIR"
    echo "✅ 克隆完成"
fi

# 3. 检查并创建 PARA 目录结构
echo ""
echo "📁 第 2 步: 创建 PARA 目录结构"

mkdir -p "$KB_DIR/Inbox"
mkdir -p "$KB_DIR/Projects"
mkdir -p "$KB_DIR/Areas"
mkdir -p "$KB_DIR/Resources"
mkdir -p "$KB_DIR/Archives"

if [ ! -f "$KB_DIR/index.md" ]; then
    cat > "$KB_DIR/index.md" << 'EOF'
---
---

# 知识索引

## 最近保存

（保存文章后会自动更新）

## 分类

- [[Inbox/]] - 收集箱
- [[Projects/]] - 项目
- [[Areas/]] - 领域
- [[Resources/]] - 资源
- [[Archives/]] - 归档
EOF
    echo "✅ 创建索引文件"
else
    echo "✅ 索引文件已存在"
fi

# 4. 添加环境变量到 shell 配置
echo ""
echo "⚙️ 第 3 步: 配置环境变量"

SHELL_RC="$HOME/.bashrc"
[ -n "$ZSH_VERSION" ] && SHELL_RC="$HOME/.zshrc"

ENV_LINE='export OBSIDIAN_VAULT="$HOME/Obsidian/knowledge-base"'

if grep -q "OBSIDIAN_VAULT" "$SHELL_RC" 2>/dev/null; then
    echo "✅ 环境变量已配置"
else
    echo "$ENV_LINE" >> "$SHELL_RC"
    echo "✅ 已添加到 $SHELL_RC"
    echo ""
    echo "⚠️ 请运行: source $SHELL_RC"
fi

# 5. 创建便捷脚本
echo ""
echo "🔗 第 4 步: 创建便捷命令"

BIN_DIR="$HOME/.local/bin"
mkdir -p "$BIN_DIR"

# 创建 link 命令
cat > "$BIN_DIR/link" << EOF
#!/bin/bash
# 快速保存链接到知识库
\$SKILL_DIR/scripts/link-to-knowledge.sh "\$1"
EOF
chmod +x "$BIN_DIR/link"
echo "✅ 创建命令: link"

# 6. 设置 crontab 自动同步
echo ""
echo "🔄 第 5 步: 配置自动同步 (可选)"

if crontab -l 2>/dev/null | grep -q "knowledge-base.*git push"; then
    echo "✅ 自动同步已配置"
else
    echo "是否配置自动同步？(每 30 分钟)"
    echo "y = 是, n = 否"
    read -r answer
    
    if [ "$answer" = "y" ] || [ "$answer" = "Y" ]; then
        CRON_JOB="*/30 * * * * cd $KB_DIR && git add -A && git commit -m 'chore: sync' && git push"
        (crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -
        echo "✅ 自动同步已配置 (每 30 分钟)"
    else
        echo "⏭️ 跳过自动同步"
    fi
fi

# 完成
echo ""
echo "=============================="
echo "✅ 初始化完成!"
echo ""
echo "📖 使用方法:"
echo ""
echo "1. 重新加载环境变量:"
echo "   source ~/.bashrc"
echo ""
echo "2. 保存知识:"
echo "   link https://example.com/article"
echo ""
echo "   或发链接到 Discord: 保存 https://..."
echo ""
echo "3. 在 Obsidian 中阅读:"
echo "   打开: $KB_DIR"
echo ""
echo "=============================="
