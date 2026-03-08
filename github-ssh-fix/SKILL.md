---
name: github-ssh-fix
description: 修复GitHub SSH连接问题
---

# GitHub SSH连接修复

## 问题症状

- SSH连接GitHub失败：`Connection closed by 140.82.116.3 port 22`
- HTTPS方式也不行：需要交互式输入密码

## 诊断步骤

```bash
# 1. 测试22端口
ssh -T git@github.com

# 2. 测试443端口
ssh -T -p 443 git@ssh.github.com
```

## 解决方案

### 方法1：SSH走443端口

```bash
# 配置SSH走443端口
cat >> ~/.ssh/config << 'EOF'

Host github.com
    Hostname ssh.github.com
    Port 443
    User git
EOF

# 添加GitHub的host key
ssh-keyscan -p 443 ssh.github.com >> ~/.ssh/known_hosts
```

### 方法2：测试连接
```bash
ssh -T git@github.com
```

## 验证

成功后显示：
```
Hi [username]! You've successfully authenticated, but GitHub does not provide shell access.
```

## 常见原因

- 22端口被防火墙阻断（机房/GFW）
- 443端口通常可用
