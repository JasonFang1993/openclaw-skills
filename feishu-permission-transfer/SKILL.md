---
name: feishu-permission-transfer
description: 转让飞书云文档所有权
---

# 转让飞书文档所有权

## 快速使用

用户让你转让文档所有权时：

1. **获取用户 open_id**：
   - 直接从会话 metadata 获取 `sender_id`
   - 格式：`ou_xxxxxxxx`

2. **调用转让工具**：
   ```
   文档链接 + 目标用户open_id
   ```

## 获取凭证

### 方法1：从 openclaw.json 获取应用凭证

```bash
grep -A5 "feishu" ~/.openclaw/openclaw.json
```

找到 `appId` 和 `appSecret`。

### 方法2：从会话获取用户 open_id

sender_id 就是用户的 open_id：
```
ou_8f8408612073321f7ed59c1bb085022a
```

## API调用

### 1. 获取 tenant_access_token

```bash
curl -s -X POST "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" \
  -H "Content-Type: application/json" \
  -d "{\"app_id\": \"$APP_ID\", \"app_secret\": \"$APP_SECRET\"}"
```

响应：
```json
{
  "code": 0,
  "msg": "success",
  "tenant_access_token": "xxx",
  "expire": 7200
}
```

### 2. 转让所有权

```bash
curl -s -X POST "https://open.feishu.cn/open-apis/drive/v1/permissions/{doc_token}/members/transfer_owner?type={type}" \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json; charset=utf-8" \
  -d '{"member_type": "openid", "member_id": "ou_xxx"}'
```

**参数说明**：
| 参数 | 说明 | 示例 |
|------|------|------|
| doc_token | 文档 token | NC3kdYkBEo9J9mxWAsHcKp7Mn5o |
| type | 文档类型 | docx, doc, sheet, bitable, wiki, folder |
| member_id | 目标用户 open_id | ou_8f8408612073321f7ed59c1bb085022a |

## 错误处理

| 错误码 | 原因 | 解决 |
|--------|------|------|
| 0 | 成功 | - |
| 99991661 | Missing access token | 需要在 Authorization header 中添加 token |
| 99991663 | token无效 | 重新获取 tenant_access_token |
| 99991664 | 参数解析失败 | 检查请求体格式 |
| 1063002 | 应用非所有者 | 手动转让给应用 |
| 99991705 | 权限不足 | 检查应用是否有 permission.member:transfer 权限 |

## 文档类型

docx | doc | sheet | bitable | wiki | folder

## 完整示例

```bash
# 配置
APP_ID="cli_xxxxx"
APP_SECRET="xxxxx"
DOC_TOKEN="NC3kdYkBEo9J9mxWAsHcKp7Mn5o"
MEMBER_ID="ou_8f8408612073321f7ed59c1bb085022a"

# 1. 获取 token
TOKEN=$(curl -s -X POST "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" \
  -H "Content-Type: application/json" \
  -d "{\"app_id\": \"$APP_ID\", \"app_secret\": \"$APP_SECRET\"}" | grep -o '"tenant_access_token":"[^"]*"' | cut -d'"' -f4)

# 2. 转让所有权
curl -s -X POST "https://open.feishu.cn/open-apis/drive/v1/permissions/$DOC_TOKEN/members/transfer_owner?type=docx" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"member_type\": \"openid\", \"member_id\": \"$MEMBER_ID\"}"
```

## 相关工具

- `feishu_doc` - 读取/创建文档
- `feishu_drive` - 云盘操作
- `feishu_perm` - 权限管理
