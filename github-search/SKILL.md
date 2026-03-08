---
name: github-search
description: Search GitHub repositories using the GitHub API. Use when you need to find open source projects, compare alternatives, analyze repository quality, or gather technical research data. Supports search by keywords, programming language filtering, sorting options (stars, forks, updated), and detailed repository information retrieval.
---

# GitHub Repository Search

Use this skill to search GitHub repositories, analyze project quality, and gather technical research data.

## Usage

### Search Repositories

```bash
# Basic search
python3 scripts/github_search.py search "whatsapp bot automation"

# Filter by language
python3 scripts/github_search.py search "machine learning" --language python

# Sort by different criteria
python3 scripts/github_search.py search "docker" --sort stars --order desc

# Get more results (max 100)
python3 scripts/github_search.py search "react" --per-page 20
```

### Get Repository Details

```bash
# Get detailed info for a specific repository
python3 scripts/github_search.py details aldinokemal go-whatsapp-web-multidevice
```

### List Repository Topics

```bash
# List topics/tags for a repository
python3 scripts/github_search.py topics pedroslopez whatsapp-web.js
```

## Search Query Tips

| Goal | Example Query |
|------|--------------|
| Find WhatsApp bots | `whatsapp bot automation` |
| Filter by language | `whatsapp bot --language typescript` |
| Find trending projects | `chatbot --sort stars` |
| Recently updated | `api server --sort updated` |
| Most forked | `docker --sort forks` |

## Output Format

All commands return JSON output:

```json
{
  "success": true,
  "total_count": 12345,
  "items": [
    {
      "full_name": "owner/repo",
      "description": "Repository description",
      "stars": 1000,
      "forks": 100,
      "language": "JavaScript",
      "updated_at": "2026-02-09T12:00:00Z",
      "html_url": "https://github.com/owner/repo",
      "open_issues": 10,
      "license": "MIT"
    }
  ]
}
```

## Examples

### Compare WhatsApp Bot Libraries

```bash
# Search for WhatsApp automation projects
python3 scripts/github_search.py search "whatsapp bot automation" --per-page 10

# Check specific projects
python3 scripts/github_search.py details pedroslopez whatsapp-web.js
python3 scripts/github_search.py details aldinokemal go-whatsapp-web-multidevice
python3 scripts/github_search.py details WhiskeySockets Baileys
```

### Research Technology Options

```bash
# Find Python ML projects
python3 scripts/github_search.py search "machine learning api" --language python --sort stars

# Find Docker tools
python3 scripts/github_search.py search "docker orchestration" --language go --per-page 20
```

## Rate Limits

GitHub API has rate limits (60 requests/hour for unauthenticated). For higher limits:
- Use authenticated requests (add `--token` header in script)
- GitHub tokens can be set in environment: `GITHUB_TOKEN`
