---
name: skill-manager
description: 管理 GitHub-based Skills 的生命周期。检查更新、列出列表、删除已安装的 skills。
license: MIT
github_url: https://github.com/KKKKhazix/Khazix-Skills
github_hash: fe15fea6cf7ac216027d11c2c64e87b462cc0427
version: 1.0.0
created_at: 2026-02-25
---

# Skill Manager

管理已安装的 GitHub-based Skills 的生命周期。

## 核心功能

1. **审计 (Audit)**: 扫描本地 skills 文件夹
2. **检查 (Check)**: 对比本地与远程 commit hash
3. **报告 (Report)**: 生成状态报告（Stale/Current）
4. **更新 (Update)**: 引导式升级工作流
5. **清单 (Inventory)**: 列出所有 skills，删除不需要的

## 使用方式

**触发指令**: 
- `/skill-manager check` - 检查更新
- `/skill-manager list` - 列出所有 skills
- `/skill-manager delete <name>` - 删除 skill

### 检查更新

```bash
# 扫描 skills 目录
python3 scripts/scan_and_check.py ~/.openclaw/workspace/skills
```

### 列出 Skills

```bash
# 列出所有已安装的 skills
python3 scripts/list_skills.py ~/.openclaw/workspace/skills
```

### 删除 Skill

```bash
# 删除指定的 skill
python3 scripts/delete_skill.py ~/.openclaw/workspace/skills <skill-name>
```

## 状态说明

| 状态 | 说明 |
|------|------|
| **Current** | 与远程仓库同步 |
| **Outdated** | 远程有新提交可用 |
| **Error** | 无法连接远程仓库 |

## 脚本说明

| 脚本 | 功能 |
|------|------|
| `scan_and_check.py` | 扫描目录、解析 frontmatter、检查远程版本 |
| `list_skills.py` | 列出已安装 skills 及元数据 |
| `delete_skill.py` | 永久删除指定 skill |
| `update_helper.py` | 更新前备份文件 |

## 前置依赖

```bash
# 安装 Python 依赖
pip install pyyaml
```

## 工作原理

1. 扫描 skills 目录下的所有子目录
2. 读取每个 SKILL.md 的 YAML frontmatter
3. 检查是否包含 `github_url` 字段（判断是否为 GitHub-based skill）
4. 使用 `git ls-remote` 获取远程最新 commit hash
5. 对比本地 `github_hash` 与远程 hash
6. 输出状态报告
