---
name: curl-cffi
description: TLS fingerprint spoofing web scraper. Bypass Cloudflare, anti-bot protection. Use when normal requests get blocked.
metadata:
  openclaw:
    emoji: "🥷"
    requires:
      bins: ["distrobox"]
      env: []
---

# curl-cffi

TLS fingerprint spoofing web scraper. Bypasses Cloudflare, Datadome, and other anti-bot protection.

## When to Use

- Normal requests get blocked
- Cloudflare challenge page
- Anti-bot detection
- Need to spoof TLS fingerprint

## Quick Start

### Basic Request

```bash
distrobox-enter pybox -- python3 -c "
from curl_cffi import requests
r = requests.get('https://example.com')
print(r.text)
"
```

### POST Request

```python
from curl_cffi import requests

r = requests.post(
    "https://example.com/api",
    json={"key": "value"},
    headers={"Authorization": "Bearer token"}
)
print(r.json())
```

### Session with Cookies

```python
from curl_cffi import requests

session = requests.Session()
session.get("https://example.com/login")
session.post("https://example.com/login", data={"user": "admin"})
print(session.cookies)
```

## Examples

### Fetch JSON API

```bash
distrobox-enter pybox -- python3 -c "
from curl_cffi import requests
r = requests.get('https://api.example.com/data')
print(r.json())
"
```

### Handle Headers

```python
from curl_cffi import requests

r = requests.get(
    "https://example.com",
    headers={
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json"
    }
)
```

## Performance

- Much faster than Selenium/Playwright
- TLS fingerprint already spoofed
- No browser overhead
- Supports concurrent requests

## Limitations

- No JavaScript rendering
- Can't handle complex CAPTCHAs
- Some sites need additional headers
