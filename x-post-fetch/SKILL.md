# X Post Fetch Skill

使用 Jina AI Reader 获取 X (Twitter) 帖子内容。当直接访问 X 被阻止时使用此技能。

## 使用方法

```bash
# 抓取用户主页（获取最近帖子）
x-post-fetch "https://x.com/openclaw"

# 抓取单条帖子（最稳定）
x-post-fetch "https://x.com/openclaw/status/2027173869648216469"

# 带认证 cookie（需要 auth_token + ct0）
x-post-fetch "https://x.com/username/status/1234567890" "your_auth_token" "your_ct0"

# 基本搜索（仅公开内容）
x-post-fetch "https://x.com/hashtag/OpenClaw"
```

## 功能特点

- **多端点 fallback**: 主用 `r.jina.ai/http://`，失败时自动尝试其他端点
- **纯 Bash 实现**: 无外部依赖，只需 curl
- **自动转换**: 自动将 twitter.com 转换为 x.com
- **支持用户 timeline**: 可以抓取用户主页获取最近帖子
- **支持 hashtag**: 可抓取话题标签页
- **支持认证**: 可带 auth_token + ct0 cookie（见下文限制）
- **错误处理**: 失败时给出清晰的错误提示

## 返回内容

- 作者信息
- 发布时间
- 帖子正文
- 原始链接
- 互动数据（Views, Likes, Retweets 等）

## 关于 auth_token 的研究

**重要发现：**
- X 的认证系统通常需要 **两个** cookie：`auth_token` + `ct0`
- 仅提供 `auth_token` 通常不够
- cookie 可能很快过期
- 即使有 cookie，Jina Reader 的 IP 可能仍被 X 阻止

**如何获取 cookie：**
1. 登录 X 后打开开发者工具
2. Network → 任意请求 → Request Headers → Cookie
3. 复制 `auth_token=` 和 `ct0=` 的值

**使用示例：**
```bash
x-post-fetch "https://x.com/search?q=OpenClaw" "your_auth_token_here" "your_ct0_here"
```

## 限制

| 类型 | 状态 | 说明 |
|------|------|------|
| 公开帖子/主页 | ✅ 可用 | 最稳定 |
| 单条帖子链接 | ✅ 可用 | 最推荐 |
| Hashtag 页面 | ⚠️ 部分可用 | 需看具体内容 |
| 搜索结果 | ❌ 需登录 | 暂不支持 |
| 评论区 | ❌ 需登录 | 暂不支持 |
| 带 auth_token | ⚠️ 不稳定 | 需要 ct0 且易过期 |

## 实用技巧

```bash
# 抓取官方账号最新帖子
x-post-fetch "https://x.com/openclaw"

# 抓取单条帖子（最稳定）
x-post-fetch "https://x.com/openclaw/status/2027173869648216469"

# 抓取任意公开帖子
x-post-fetch "https://x.com/username/status/xxx"

# 抓取 hashtag
x-post-fetch "https://x.com/hashtag/OpenClaw"
```

## 备选方案

如果 X 抓取失败，可以尝试：
- **Hacker News**: `curl -sL "https://r.jina.ai/http://news.ycombinator.com"`
- **Discord**: 查看 OpenClaw 官方服务器
- **GitHub**: issues/discussions/releases

## 依赖

- curl
- bash
- sed/grep (基本 Unix 工具)

## 文件结构

```
x-post-fetch/
├── SKILL.md
└── scripts/
    └── x-post-fetch.sh
```

## 示例输出

```
============================================

👤 OpenClaw🦞 (@openclaw)

📝 OpenClaw 2026.2.26 🦞
🔐 External Secrets Management
🤖 ACP thread-bound agents
⚡ Codex WebSocket-first transport
...

🕐 2026-02-27 08:22:32

🔗 https://x.com/openclaw/status/2027173869648216469

============================================

✅ Successfully fetched!
```

---

## 更新日志

- **2026-02-27**: 添加 ct0 参数支持，整合搜索场景，更新限制说明
