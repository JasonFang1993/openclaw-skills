---
name: summarize
description: 使用 summarize CLI 摘要 URL、文件和 YouTube（网页、PDF、图片、音频）。
homepage: https://summarize.sh
metadata: {"clawdbot":{"emoji":"🧾","requires":{"bins":["summarize"]},"install":[{"id":"brew","kind":"brew","formula":"steipete/tap/summarize","bins":["summarize"],"label":"安装 summarize (brew)"}]}}
---

# Summarize

快速 CLI 工具，用于摘要 URL、本地文件和 YouTube 链接。

## 快速开始

```bash
summarize "https://example.com" --model google/gemini-3-flash-preview
summarize "/path/to/file.pdf" --model google/gemini-3-flash-preview
summarize "https://youtu.be/dQw4w9WgXcQ" --youtube auto
```

## 模型 + 密钥

为所选提供商设置 API 密钥：
- OpenAI: `OPENAI_API_KEY`
- Anthropic: `ANTHROPIC_API_KEY`
- xAI: `XAI_API_KEY`
- Google: `GEMINI_API_KEY`（别名：`GOOGLE_GENERATIVE_AI_API_KEY`、`GOOGLE_API_KEY`）

默认模型是 `google/gemini-3-flash-preview`（如果未设置）。

## 常用选项

- `--length short|medium|long|xl|xxl|<chars>` - 摘要长度
- `--max-output-tokens <count>` - 最大输出 token
- `--extract-only` - 仅提取 URL
- `--json` - 机器可读格式
- `--firecrawl auto|off|always` - 备用提取
- `--youtube auto` - Apify 备用（如果设置了 `APIFY_API_TOKEN`）

## 配置

可选配置文件：`~/.summarize/config.json`

```json
{ "model": "openai/gpt-5.2" }
```

可选服务：
- `FIRECRAWL_API_KEY` - 用于被阻止的网站
- `APIFY_API_TOKEN` - YouTube 备用
