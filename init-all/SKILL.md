---
name: init-all
description: 一键初始化所有配置。换电脑后一键恢复所有环境。
---

# init-all

换电脑后一键恢复所有配置。

## 一键初始化

```bash
git clone git@github.com:JasonFang1993/openclaw-skills.git /tmp/setup
/tmp/setup/init-all/scripts/init-all.sh
```

## 自动配置

| 配置项 | 自动？ |
|--------|--------|
| 克隆仓库 | ✅ |
| 环境变量 | ✅ |
| Cron 任务 | ✅ |
| 快捷命令 | ✅ |

## 包含脚本

| 脚本 | 用途 |
|------|------|
| `init-all.sh` | 一键初始化 |
| `restore-memory.sh` | 恢复记忆 |

## 快捷命令

| 命令 | 用途 |
|------|------|
| `link <url>` | 保存网页到知识库 |
| `pm init <项目>` | 创建项目 |
| `pm status` | 查看状态 |

## 换电脑恢复

```bash
# 克隆工作区
git clone git@github.com:JasonFang1993/openclaw-memory.git ~/.openclaw/workspace

# 同步 skills
for dir in ~/.openclaw/workspace/openclaw-skills/*/; do
    cp -r "$dir" ~/.openclaw/skills/
done

# 运行初始化
~/.openclaw/skills/init-all/scripts/init-all.sh
```
