#!/bin/bash
# Check Twitter/X for updates

ACCOUNT="${1:-openclawai}"

echo "Checking @$ACCOUNT on Twitter..."

# Try v2xt API first
DATA=$(curl -s --max-time 10 "https://v2xt.com/api/user/$ACCOUNT" 2>/dev/null)

if [ -n "$DATA" ] && echo "$DATA" | jq -e '.tweets' >/dev/null 2>&1; then
    echo "=== Latest tweets from @$ACCOUNT ==="
    echo "$DATA" | jq -r '.tweets[:5] | .[] | "\(.time) \(.content)"' 2>/dev/null | head -20
else
    echo "v2xt failed, trying nitter RSS..."
    
    # Try nitter RSS
    RSS=$(curl -s --max-time 10 "https://nitter.net/$ACCOUNT/rss" 2>/dev/null)
    
    if [ -n "$RSS" ]; then
        echo "=== RSS Feed ==="
        echo "$RSS" | head -30
    else
        echo "Failed to fetch from both v2xt and nitter"
        echo "Try: agent-reach search 'OpenClaw' --platform twitter"
    fi
fi
