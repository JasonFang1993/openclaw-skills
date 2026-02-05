#!/bin/bash

# WeChat Article Reader - Bash Wrapper
# Usage: ./reader.sh "https://mp.weixin.qq.com/s/..."

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ -z "$1" ]; then
    echo "Usage: $0 <wechat-article-url>"
    echo "Example: $0 https://mp.weixin.qq.com/s/xxxxx"
    exit 1
fi

node "$SCRIPT_DIR/reader.js" "$1"
