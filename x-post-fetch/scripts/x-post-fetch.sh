#!/bin/bash
#
# X Post Fetch - Fetch X/Twitter posts using Jina AI Reader
#
# Usage:
#   x-post-fetch "https://x.com/username/status/1234567890"
#   x-post-fetch "https://x.com/username" [auth_token] [ct0]
#
# Note: auth_token alone may not be sufficient. X often requires both
# auth_token and ct0 cookies for authenticated requests.
#

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if URL is provided
if [ -z "$1" ]; then
    echo -e "${RED}Usage: $0 <X/Twitter post URL> [auth_token] [ct0]${NC}"
    echo -e "${YELLOW}Examples:${NC}"
    echo "  $0 https://x.com/username/status/1234567890"
    echo "  $0 https://x.com/username"
    echo "  $0 https://x.com/username/status/1234567890 your_auth_token your_ct0"
    exit 1
fi

URL="$1"
AUTH_TOKEN="$2"
CT0="$3"

# Validate URL contains x.com or twitter.com
if ! echo "$URL" | grep -qE "(x\.com|twitter\.com)"; then
    echo -e "${RED}Error: Invalid X/Twitter URL. Please provide a valid X.com or Twitter.com URL${NC}"
    exit 1
fi

# Convert twitter.com to x.com for consistency
URL=$(echo "$URL" | sed 's/twitter\.com/x.com/g')

echo -e "${BLUE}🔍 Fetching: $URL${NC}"

# Build cookie header
COOKIE=""
if [ -n "$AUTH_TOKEN" ]; then
    COOKIE="auth_token=$AUTH_TOKEN"
    if [ -n "$CT0" ]; then
        COOKIE="${COOKIE}; ct0=$CT0"
    fi
    echo -e "${YELLOW}🔐 Using auth cookie (may not work for all content)${NC}"
fi

# Try multiple endpoints with fallbacks
endpoints=(
    "https://r.jina.ai/http://"
    "https://r.jina.ai/https://"
    "https://r.jina.ai/http://x.com/"
    "https://r.jina.ai/http://www.x.com/"
)

result=""
success=false

for endpoint in "${endpoints[@]}"; do
    full_url="${endpoint}${URL}"
    
    if [ -n "$COOKIE" ]; then
        result=$(curl -sL --max-time 30 -H "Cookie: $COOKIE" "$full_url" 2>/dev/null)
    else
        result=$(curl -sL --max-time 30 "$full_url" 2>/dev/null)
    fi

    # Check if we got valid content (not an error page)
    if [ -n "$result" ] && \
       ! echo "$result" | grep -qi "error\|not found\|blocked\|login required\|Hmm.*this page doesn't exist" && \
       echo "$result" | grep -q "Title:"; then
        success=true
        break
    fi
done

# Check final result
if [ -z "$result" ] || ! echo "$result" | grep -q "Title:"; then
    echo -e "${RED}Error: Failed to fetch post.${NC}"
    echo -e "${YELLOW}Possible reasons:${NC}"
    echo "  - The post is private or deleted"
    echo "  - The post requires login to view"
    echo "  - X has blocked the Jina IP range"
    echo ""
    echo -e "${YELLOW}Try:${NC}"
    echo "  1. Use auth_token: x-post-fetch \"URL\" \"your_token\""
    echo "  2. Check if the URL is correct"
    echo "  3. Try again later if rate limited"
    exit 1
fi

# Extract author from title line
author=$(echo "$result" | grep "^Title:" | head -1 | sed 's/Title: //' | sed 's/ on X.*//' | sed 's/:.*//')

# Extract post content from Markdown Content section
post_content=$(echo "$result" | sed -n '/^Markdown Content:/,/^===============$/p' | tail -n +2 | head -n -1 | sed 's/  */ /g')

# Get published time
pub_time=$(echo "$result" | grep "^Published Time:" | sed 's/Published Time: //')

# Get URL from result
original_url=$(echo "$result" | grep "^URL Source:" | sed 's/URL Source: //')

# Output with nice formatting
echo ""
echo "============================================"
echo ""
if [ -n "$author" ]; then
    echo -e "${GREEN}👤 $author${NC}"
fi

if [ -n "$post_content" ]; then
    echo -e "${NC}📝 $post_content${NC}"
fi

if [ -n "$pub_time" ]; then
    echo ""
    echo -e "${YELLOW}🕐 $pub_time${NC}"
fi

if [ -n "$original_url" ]; then
    echo ""
    echo -e "${BLUE}🔗 $original_url${NC}"
fi

echo ""
echo "============================================"
echo ""
echo -e "${GREEN}✅ Successfully fetched!${NC}"
