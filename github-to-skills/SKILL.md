---
name: github-to-skills
description: 将 GitHub 仓库自动转换为 AI Skills。当用户提供 GitHub URL 并想要"包装"或"创建"一个 skill 时使用此技能。
license: MIT
---

# GitHub to Skills Factory

自动化工具，将 GitHub 仓库转换为可安装的 AI Skills。

## 核心功能

1. **分析**: 抓取仓库元数据（描述、README、最新 commit hash）
2. **脚手架**: 创建标准化的 skill 目录结构
3. **元数据注入**: 生成带扩展 frontmatter 的 SKILL.md，便于后续生命周期管理
4. **包装器生成**: 创建 wrapper 脚本以便调用工具

## 使用方式

**触发指令**: 
- `/github-to-skills <github_url>`
- "Package this repo into a skill: <url>"

### 必需元数据格式

此工具创建的每个 skill 必须在 SKILL.md 中包含以下扩展 YAML frontmatter。这对 skill-manager 后续功能至关重要。

```yaml
---
name: <kebab-case-repo-name>
description: <简短描述-用于触发agent>
# 扩展元数据（必需）
github_url: <原始仓库URL>
github_hash: <创建时的最新commit hash>
version: <标签或0.1.0>
created_at: <ISO-8601日期>
entryrapper.py # 或_point: scripts/w主脚本
dependencies: # 列出主要依赖，例如 ["yt-dlp", "ffmpeg"]
---
```

## 工作流程

1. **抓取信息**: 运行 `scripts/fetch_github_info.py` 获取仓库原始数据
2. **规划**: 分析 README 了解如何调用工具（CLI 参数、Python API 等）
3. **生成**: 使用 skill-creator 模式编写 SKILL.md 和包装脚本，确保**扩展元数据**存在
4. **验证**: 检查 commit hash 是否正确捕获

## 脚本说明

| 脚本 | 功能 |
|------|------|
| `fetch_github_info.py` | 抓取仓库详情（README、Hash、Tags）|
| `create_github_skill.py` | 编排创建目录和初始文件 |

## 生成 Skill 的最佳实践

- **隔离**: 生成的 skill 应自行安装依赖（如 venv 或 uv/pip），或明确声明
- **渐进披露**: 不要把整个仓库塞进 skill。只包含必要的包装代码，需要深入时引用原始仓库
- **幂等性**: `github_hash` 字段允许未来的 skill-manager 检查 `if remote_hash != local_hash` 来触发更新
