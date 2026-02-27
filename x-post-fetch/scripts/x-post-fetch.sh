#!/bin/bash
#
# X Post Fetch - Fetch X/Twitter posts using Jina AI Reader
# 
# Usage: x-post-fetch "https://x.com/username/status/1234567890"
#

# Check if URL is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <X/Twitter post URL>"
    echo "Example: $0 https://x.com/username/status/1234567890"
    exit 1
fi

URL="$1"

# Validate URL contains x.com or twitter.com
if ! echo "$URL" | grep -qE "(x\.com|twitter\.com)"; then
    echo "Error: Invalid X/Twitter URL. Please provide a valid X.com or Twitter.com URL"
    exit 1
fi

# Convert twitter.com to x.com for consistency
URL=$(echo "$URL" | sed 's/twitter\.com/x.com/g')

# Try multiple endpoints with fallbacks
endpoints=(
    "https://r.jina.ai/http://"
    "https://r.jina.ai/https://"
)

result=""
for endpoint in "${endpoints[@]}"; do
    full_url="${endpoint}${URL}"
    result=$(curl -sL --max-time 30 "$full_url" 2>/dev/null)
    
    # Check if we got valid content
    if [ -n "$result" ] && ! echo "$result" | grep -qi "error\|not found\|blocked\|login required"; then
        break
    fi
done

# Check final result
if [ -z "$result" ] || echo "$result" | grep -qi "error\|not found\|blocked\|login required"; then
    echo "Error: Failed to fetch post. The post may be private, deleted, or access is blocked."
    exit 1
fi

# Extract author from title line
author=$(echo "$result" | grep "^Title:" | head -1 | sed 's/Title: //' | sed 's/ on X.*//' | sed 's/:.*//')

# Extract post content from Markdown Content section
post_content=$(echo "$result" | sed -n '/^Markdown Content:/,/^===============$/p' | tail -n +2 | head -n -1 | sed 's/  */ /g')

# Get published time
pub_time=$(echo "$result" | grep "^Published Time:" | sed 's/Published Time: //')

# Output with nice formatting
echo "============================================"
echo ""
echo "👤 $author"
echo ""
echo "📝 $post_content"
echo ""
if [ -n "$pub_time" ]; then
    echo "🕐 $pub_time"
fi
echo ""
echo "🔗 $URL"
echo ""
echo "============================================"
