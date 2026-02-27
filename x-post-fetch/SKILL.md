# X Post Fetch Skill

使用 Jina AI Reader 获取 X (Twitter) 帖子内容。当直接访问 X 被阻止时使用此技能。

## 使用方法

```bash
# 基本用法 - 抓取单条帖子
x-post-fetch "https://x.com/username/status/1234567890"

# 抓取用户主页（获取最近帖子）
x-post-fetch "https://x.com/username"

# 带 auth_token（抓取需要登录的内容）
x-post-fetch "https://x.com/username/status/1234567890" "your_auth_token"
```

## 功能特点

- **多端点 fallback**: 主用 `r.jina.ai/http://`，失败时自动尝试其他端点
- **纯 Bash 实现**: 无外部依赖，只需 curl
- **自动转换**: 自动将 twitter.com 转换为 x.com
- **支持用户 timeline**: 可以抓取用户主页获取最近帖子
- **支持认证**: 可以带上 auth_token 抓取受限内容
- **错误处理**: 失败时给出清晰的错误提示

## 返回内容

- 作者信息
-- 发布时间
- 帖子正文
 原始链接
- 互动数据（如有）

## 限制

- 如果 X 封锁了 Jina 的 IP 段，可能无法获取
- 媒体（图片/视频）不会被下载，仅提供链接
- 频繁请求可能触发限流

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

👤 Elon Musk (@elonmusk)

📝 Just posted something interesting...

🕐 2026-02-26 10:30:00

🔗 https://x.com/elonmusk/status/1234567890

============================================
```
