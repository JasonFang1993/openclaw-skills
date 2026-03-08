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

# JSON output (for automation)
node scripts/reader.js --json "https://mp.weixin.qq.com/s/..."

# Quiet mode (suppress fetch logs)
node scripts/reader.js --quiet "https://mp.weixin.qq.com/s/..."

# Custom User-Agent
node scripts/reader.js "https://mp.weixin.qq.com/s/..."
```

## How It Works

1. **Multi-UA Retry (兼容增强)**
   - Tries multiple user-agents (mobile WeChat / mobile Safari / desktop) to improve compatibility
2. **Robust HTML Fetching**
   - Uses Node.js https/http modules
   - Follows redirects and keeps timeout protection
3. **Content Extraction + Fallback**
   - Prefers `#js_content` / rich media content blocks
   - Removes `<script>` / `<style>` / tags and decodes entities
   - Detects WeChat shell pages like `轻触查看原文`
   - On blocked shell pages, falls back to `og:title` / `og:description` extraction
4. **Structured Output**
   - Returns title, paragraphs, and extraction diagnostics

## Parameters

- **URL**: Full WeChat article URL (required)
- Optional env vars:
  - `WEIXIN_READER_UA`: custom user-agent (prepended to retry list)
  - `WEIXIN_READER_REFERER`: custom referer (default `https://mp.weixin.qq.com/`)

## Requirements

- Node.js 18+
- No external dependencies (uses built-in https module)
