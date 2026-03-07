#!/bin/bash
# Check GitHub releases for updates

REPO="${1:-openclaw/openclaw}"

echo "Checking $REPO..."

# Get latest release
DATA=$(curl -s "https://api.github.com/repos/$REPO/releases/latest")

TAG=$(echo "$DATA" | jq -r '.tag_name // "N/A"')
DATE=$(echo "$DATA" | jq -r '.published_at // "N/A"')
TITLE=$(echo "$DATA" | jq -r '.name // "N/A"')
BODY=$(echo "$DATA" | jq -r '.body // ""')

echo "Latest: $TAG ($DATE)"
echo "Title: $TITLE"
echo ""
echo "Body:"
echo "$BODY"

# Check for breaking changes
if echo "$BODY" | grep -qi "breaking\|破坏性"; then
    echo ""
    echo "⚠️ Breaking changes detected!"
fi
