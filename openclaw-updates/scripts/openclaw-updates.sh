#!/bin/bash
#
# OpenClaw Updates Fetcher
# 自动获取 OpenClaw 最新动态
#
# 用法:
#   openclaw-updates.sh [选项]
#
# 选项:
#   --github    只看 GitHub
#   --twitter   只看 Twitter
#   --all       全部（默认）
#   --check     检查版本差异
#

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

MODE="all"

# 解析参数
while [[ $# -gt 0 ]]; do
    case $1 in
        --github)
            MODE="github"
            shift
            ;;
        --twitter)
            MODE="twitter"
            shift
            ;;
        --all)
            MODE="all"
            shift
            ;;
        --check)
            MODE="check"
            shift
            ;;
        *)
            echo "用法: $0 [--github|--twitter|--all|--check]"
            exit 1
            ;;
    esac
done

echo -e "${BLUE}🦞 OpenClaw 最新动态${NC}"
echo "================================"

# 检查版本
check_version() {
    echo -e "\n${YELLOW}📊 版本检查${NC}"
    echo "---"
    
    # 当前版本
    CURRENT=$(openclaw --version 2>/dev/null || echo "未知")
    echo "当前版本: $CURRENT"
    
    # 最新版本
    LATEST=$(curl -sL "https://api.github.com/repos/openclaw/openclaw/releases" | jq -r '.[0].tag_name' 2>/dev/null | sed 's/^v//')
    echo "最新版本: $LATEST"
    
    # 比较（去掉 v 前缀比较）
    CURRENT_CLEAN=$(echo "$CURRENT" | sed 's/^v//')
    if [ "$CURRENT_CLEAN" = "$LATEST" ]; then
        echo -e "${GREEN}✅ 已是最最新${NC}"
    else
        echo -e "${YELLOW}⚠️ 有新版本可用${NC}"
    fi
}

# GitHub Releases
fetch_github() {
    echo -e "\n${YELLOW}🐙 GitHub Releases${NC}"
    echo "---"
    
    # 最新 3 个版本
    curl -sL "https://api.github.com/repos/openclaw/openclaw/releases?per_page=3" | jq -r '.[] | "版本: \(.tag_name)\n日期: \(.published_at[:10])\n"' | head -15
    
    # Breaking Changes
    echo -e "\n${RED}⚠️ Breaking Changes:${NC}"
    curl -sL "https://api.github.com/repos/openclaw/openclaw/releases" | jq -r '.[0].body' | grep -A2 -i "breaking" | head -10
    
    # Issues 热点
    echo -e "\n${BLUE}💬 热门讨论:${NC}"
    curl -sL "https://api.github.com/repos/openclaw/openclaw/discussions?per_page=5&sort=reactions" | jq -r '.[] | "  \(.reactions.total_count)👍 [\(.category.name)] \(.title)"'
}

# Twitter
fetch_twitter() {
    echo -e "\n${BLUE}🐦 Twitter @openclaw${NC}"
    echo "---"
    
    # 抓最新帖子
    curl -sL "https://r.jina.ai/http://x.com/openclaw" 2>/dev/null | grep -E "status|OpenClaw|release|v2026|🦞|star" | head -20
    
    # 如果上面没内容，给提示
    if [ $? -ne 0 ]; then
        echo "（Twitter 抓取可能需要登录）"
        echo "可手动访问: https://x.com/openclaw"
    fi
}

# 运行
case $MODE in
    github)
        check_version
        fetch_github
        ;;
    twitter)
        fetch_twitter
        ;;
    all)
        check_version
        fetch_github
        fetch_twitter
        ;;
    check)
        check_version
        ;;
esac

echo -e "\n================================"
echo -e "${GREEN}完成！${NC}"
