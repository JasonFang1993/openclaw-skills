---
name: weixin-reader
description: Read and extract readable content from WeChat Official Account articles (mp.weixin.qq.com). Use when user wants to fetch and parse WeChat articles that have anti-crawler protection. Handles mobile User-Agent spoofing, HTML parsing, and text extraction.
---

# WeChat Article Reader

## Usage

```bash
# Basic usage
./scripts/reader.sh "https://mp.weixin.qq.com/s/..."

# Save to file
./scripts/reader.sh "https://mp.weixin.qq.com/s/..." > output.txt

# Custom User-Agent
node scripts/reader.js "https://mp.weixin.qq.com/s/..."
```

## How It Works

1. **User-Agent Spoofing**: Uses iPhone Safari user-agent to bypass WeChat's mobile detection
2. **HTML Fetching**: Uses Node.js https module for reliable requests
3. **Text Extraction**: 
   - Removes `<script>` and `<style>` tags
   - Strips all HTML tags
   - Decodes HTML entities (&nbsp;, &lt;, &gt;, &amp;)
   - Filters out short lines and URLs
   - Returns clean paragraphs

## Parameters

- **URL**: Full WeChat article URL (required)
- Optional: Add custom headers via environment variables

## Requirements

- Node.js 18+
- No external dependencies (uses built-in https module)
