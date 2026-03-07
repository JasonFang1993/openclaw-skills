---
name: twitter-monitor
description: Monitor Twitter/X for specific accounts. Use browser or RSS as fallback.
metadata:
  openclaw:
    emoji: "🐦"
    requires:
      bins: ["curl"]
---

# Twitter Monitor

Monitor Twitter/X for specific accounts.

## When to Use

- Track OpenClaw official announcements
- Monitor specific keywords or hashtags

## Methods

### Method 1: OpenClaw Browser

Use OpenClaw's browser tool to open Twitter/X directly.

### Method 2: RSS Feed (Nitter)

```bash
# Get RSS for specific user
curl -s "https://nitter.net/openclawai/rss"
```

### Method 3: Use Agent-Reach (Recommended)

Since agent-reach is installed, use it to search Twitter:

```bash
# Check if Twitter is available
agent-reach doctor
```

If Twitter shows ✅, you can use browser automation.

### Method 4: Web Fetch via Jina

```bash
curl -s "https://r.jina.ai/http://twitter.com/openclawai"
```

## Quick Start

### Check Latest from OpenClaw

1. Use OpenClaw browser: `browser open https://twitter.com/openclawai`
2. Or use the web fetching skill

## Configuration

No additional config needed. Use existing tools.

## Notes

- Twitter/X may block automated access
- Use browser tool for reliable access
- Consider using RSS alternatives like Nitter
