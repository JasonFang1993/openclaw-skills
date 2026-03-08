---
name: debug-tool-capabilities
description: |
  诊断和修复 OpenClaw 运行时缺少工具能力（exec/read/http）的问题。
  当 Claude 报告"没有 xx 能力"、"工具箱里没有"、"无法执行命令"时使用。
  适用于 Linux / macOS / Windows 用户。
---

# OpenClaw 工具能力缺失诊断

## 症状表现

Claude 说类似这样的话：
- "我没有 exec 工具"
- "工具箱里没有文件读取能力"  
- "无法执行 shell 命令"
- "权限不够"

---

## 一键修复（推荐）

### 步骤 1：找到配置文件

| 系统 | 配置文件位置 |
|------|-------------|
| Linux/macOS | `~/.openclaw/openclaw.json` |
| Windows | `C:\Users\你的用户名\.openclaw\openclaw.json` |

### 步骤 2：修改配置

用记事本/VS Code/Nano 打开文件，找到这一段：

```json
"tools": {
  "profile": "messaging"
}
```

改成：

```json
"tools": {
  "profile": "full"
}
```

### 步骤 3：重启服务

打开终端（命令提示符/PowerShell/Terminal），运行：

```bash
openclaw gateway restart
```

### 步骤 4：验证

重启后，让 Claude 再说一次话，测试是否有 exec/read 等能力。

---

## 常见系统命令对照

| 操作 | Linux/macOS | Windows |
|------|-------------|---------|
| 打开配置 | `nano ~/.openclaw/openclaw.json` | `notepad %USERPROFILE%\.openclaw\openclaw.json` |
| 重启服务 | `openclaw gateway restart` | 同样 |
| 查看状态 | `openclaw gateway status` | 同样 |

---

## 技术细节（可选）

### 为什么会出现这个问题？

OpenClaw 的 `tools.profile` 有几种模式：
- `messaging` - 仅聊天，限制最严
- `full` - 全部功能

配置文件默认可能是 `messaging`，导致 AI 没有文件/命令执行能力。

### 手动验证

修复后可以让 Claude 跑：
```bash
# 测试 exec
echo "test"

# 测试 gh 登录
gh auth status
```

---

## 常见问题

| 问题 | 原因 | 解决 |
|------|------|------|
| 没有 exec | profile=messaging | 改成 "full" |
| 没有 read | 同上 | 同上 |
| 没有 http/web | 同上 | 同上 |
| skill 装了不能用 | 运行环境权限未开 | 检查配置文件 |
