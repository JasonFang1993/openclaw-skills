---
name: obsidian
description: 使用 obsidian-cli 自动化管理 Obsidian 保险库（纯 Markdown 笔记）。
homepage: https://help.obsidian.md
metadata: {"clawdbot":{"emoji":"💎","requires":{"bins":["obsidian-cli"]},"install":[{"id":"brew","kind":"brew","formula":"yakitrak/yakitrak/obsidian-cli","bins":["obsidian-cli"],"label":"安装 obsidian-cli (brew)"}]}}
---

# Obsidian

Obsidian 保险库 = 磁盘上的普通文件夹。

## 保险库结构（典型）

- 笔记：`*.md`（纯文本 Markdown，可用任何编辑器编辑）
- 配置：`.obsidian/`（工作区 + 插件设置，通常不从脚本触碰）
- 画布：`*.canvas`（JSON）
- 附件：你选择的文件夹（图片/PDF 等）

## 查找活动的保险库

Obsidian 桌面版在此处跟踪保险库（权威来源）：
- `~/Library/Application Support/obsidian/obsidian.json`

`obsidian-cli` 从该文件解析保险库；保险库名称通常是**文件夹名称**（路径后缀）。

快速查看"哪个保险库是活动的/笔记在哪里？"
- 如果已设置默认值：`obsidian-cli print-default --path-only`
- 否则，读取 `~/Library/Application Support/obsidian/obsidian.json` 并使用 `"open": true` 的条目

注意：
- 多个保险库很常见（iCloud vs `~/Documents`，工作/个人等）。不要猜测，请读取配置。
- 避免将硬编码的保险库路径写入脚本；优先读取配置或使用 `print-default`。

## obsidian-cli 快速开始

设置默认保险库（一次）：
- `obsidian-cli set-default "<vault-folder-name>"`
- `obsidian-cli print-default` / `obsidian-cli print-default --path-only`

搜索
- `obsidian-cli search "query"`（笔记名称）
- `obsidian-cli search-content "query"`（笔记内容，显示片段 + 行号）

创建
- `obsidian-cli create "Folder/New note" --content "..." --open`
- 需要 Obsidian URI 处理程序（`obsidian://…`）正常工作（已安装 Obsidian）。

移动/重命名（安全重构）
- `obsidian-cli move "old/path/note" "new/path/note"`
- 更新整个保险库中的 `[[wikilinks]]` 和常见 Markdown 链接（这是相对于 `mv` 的主要优势）

删除
- `obsidian-cli delete "path/note"`

适当时候直接编辑：打开 `.md` 文件并更改它；Obsidian 会自动识别。
