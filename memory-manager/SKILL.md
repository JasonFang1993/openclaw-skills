# Memory Manager Skill

## 描述

管理 OpenClaw 的长期记忆系统，与 Obsidian vault 集成。通过 MCP 协议操作 Obsidian 笔记。

## 功能

### 读取记忆
读取指定的记忆文件内容

### 写入记忆
创建新的记忆记录

### 搜索记忆
搜索记忆库中的内容

### 关联发现
查找与当前记忆相关的其他记忆

## 使用方式

```
# 读取记忆
调用 read_memory，参数：file

# 写入记忆
调用 write_memory，参数：content, type, tags

# 搜索记忆
调用 search_memory，参数：query

# 关联发现
调用 link_memory，参数：file
```

## 依赖

- MCP 插件：openclaw-mcp-adapter
- MCP 服务器：@mauricio.wolff/mcp-obsidian
- Vault 路径：/data/vault

## 工具列表

通过 MCP 适配器提供以下工具：

- obsidian_read_note - 读取笔记
- obsidian_write_note - 创建笔记
- obsidian_search_notes - 搜索笔记
- obsidian_manage_tags - 管理标签
- obsidian_list_directory - 列出目录
- obsidian_get_vault_stats - 获取 vault 统计
