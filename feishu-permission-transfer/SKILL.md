---
name: feishu-permission-transfer
description: 转让飞书云文档所有权
---

# 转让飞书文档所有权

## 快速使用

1. 获取token → 2. 调用转让API

## API调用

```bash
# 1. 获取tenant_access_token
curl -s -X POST "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" \
  -H "Content-Type: application/json" \
  -d "{\"app_id\": \"$APP_ID\", \"app_secret\": \"$APP_SECRET\"}"

# 2. 转让所有权
curl -s -X POST "https://open.feishu.cn/open-apis/drive/v1/permissions/{doc_token}/members/transfer_owner?type={type}" \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json; charset=utf-8" \
  -d "{\"member_type\": \"openid\", \"member_id\": \"{target_open_id}\"}"
```

## 错误处理

| 错误码 | 原因 | 解决 |
|--------|------|------|
| 99991663 | token无效 | 重新获取token |
| 1063002 | 应用非所有者 | 手动转让给应用 |

## 文档类型

docx | doc | sheet | bitable | wiki | folder
