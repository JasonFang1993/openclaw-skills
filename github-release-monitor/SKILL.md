---
name: github-release-monitor
description: Monitor GitHub releases for specific repos. Detect breaking changes and send notifications.
metadata:
  openclaw:
    emoji: "🔔"
    requires:
      bins: ["curl", "jq"]
---

# GitHub Release Monitor

Monitor GitHub releases for specific repositories. Detect breaking changes.

## When to Use

- Track OpenClaw releases
- Monitor breaking changes
- Stay updated with new features

## Quick Start

### Check Latest Release

```bash
curl -s https://api.github.com/repos/openclaw/openclaw/releases/latest | jq '.tag_name, .body, .published_at'
```

### List Recent Releases

```bash
curl -s https://api.github.com/repos/openclaw/openclaw/releases?per_page=5 | jq '.[].tag_name'
```

### Check for Breaking Changes

```bash
curl -s https://api.github.com/repos/openclaw/openclaw/releases/latest | jq -r '.body' | grep -i "breaking\|破坏\|breaking"
```

## Configuration

Create `repos.txt` with repos to monitor:

```
openclaw/openclaw
anthropic/claude-code
openai/openai
```

## Example Output

```json
{
  "tag_name": "2026.3.3",
  "published_at": "2026-03-07T00:00:00Z",
  "body": "## Breaking Changes\n- tools.profile default changed"
}
```

## Cron Setup

Add to crontab:

```bash
0 9 * * * /path/to/check-releases.sh
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| GITHUB_TOKEN | Optional, for higher rate limits |
| REPOS_FILE | Path to repos list |

## Limitations

- 60 requests/hour without token
- 5000 requests/hour with token
