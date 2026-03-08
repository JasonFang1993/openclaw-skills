# Tech News Digest 增强版 - 使用说明

> 本 skill 用于生成每日科技新闻简报，包含 AI 深度分析

## 这是什么？

**基础版**：自动抓取科技新闻，生成简单的新闻列表
**增强版**：抓取 + AI 深度分析 + 人工审核 + 推送到 Discord

## 解决什么问题？

1. **信息过载**：每天科技新闻太多，看不过来
2. **深度不够**：只有标题+链接，没有分析
3. **质量不稳**：容易混入不相关或水内容的新闻

## 核心特点

### 1. 严格筛选
- 只选 AI 相关新闻（LLM、AI Agent、AI编程、AI行业）
- 排除：纯围棋、纯生物、纯政治新闻

### 2. 深度分析
- 每篇新闻 500+ 字
- 包含：核心事件 + 深入分析 + 独立观点
- 必须读取原文，不能只看标题

### 3. 质量保证
- 子 agent 初稿
- 人工审核
- 不符合就退回修正

## 工作流程

### 步骤 1：抓取新闻（自动）
```
每天 9:00 AM，Cron 自动执行
→ 抓取 RSS / Twitter / GitHub / Reddit / Web
→ 生成 JSON 文件
```

### 步骤 2：筛选 + 初稿（子 agent）
```
1. 读取 JSON 文件
2. 筛选 10-15 篇 AI 相关新闻
3. 每篇读取原文
4. 写 500+ 字深度分析
5. 提交审核
```

### 步骤 3：审核（人工）
```
检查清单：
□ 10 篇都是 AI 相关？
□ 每篇 500+ 字？
□ 每篇有独立观点？
□ 没有水文？
□ 格式统一？

❌ 不符合 → 退回修正
✅ 符合 → 发送
```

### 步骤 4：发送
```
→ 发送到 Discord 频道
→ 简报完成
```

## 文件说明

| 文件 | 作用 |
|------|------|
| `SKILL.md` | 原始 skill 定义（抓取脚本） |
| `CUSTOM.md` | 本使用说明 |
| `CHECKLIST.md` | 质量检查清单 |
| `scripts/news-digest.sh` | 每日自动执行脚本 |

## 如何使用

### 手动运行

```bash
# 1. 抓取新闻
/root/.openclaw/workspace/scripts/news-digest.sh

# 2. 分析并发送（后续步骤需要人工介入）
```

### 查看今日新闻

```bash
# 查看抓取的新闻
cat /tmp/td-daily.json | python3 -m json.tool | less

# 查看热点新闻
python3 -c "
import json
data = json.load(open('/tmp/td-daily.json'))
for a in sorted(sum([t['articles'] for t in data['topics'].values()], []), key=lambda x: -x['quality_score'])[:10]:
    print(f\"{a['quality_score']:.0f}分 | {a['source_name']}\")
    print(f\"  {a['title']}\")
"
```

## 常见问题

### Q: 为什么需要人工审核？
A: AI 写的分析可能不够深入，或者会偷懒。人工审核确保质量。

### Q: 可以完全自动化吗？
A: 抓取可以自动化，但深度分析需要读取原文和思考，目前只能半自动化。

### Q: 如何调整筛选标准？
A: 修改 `CHECKLIST.md` 中的筛选标准

## 技术细节

### 数据源
- RSS: 46 个科技博客
- Twitter/X: 44 个 KOL
- GitHub: 19 个热门仓库
- Reddit: 13 个子版块
- Web Search: 4 个主题

### 输出格式
- Discord: Markdown 格式
- Email: HTML 格式（可选）
- PDF: A4 格式（可选）

### 定时任务
- 每天 9:00 AM UTC
- 配置：`crontab -l` 查看
