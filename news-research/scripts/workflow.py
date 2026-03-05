#!/usr/bin/env python3
"""
News Research Skill - Agent工作流定义 (深度分析版 v2)
支持中英文源，包含深度分析框架
"""

import json
from datetime import datetime

WORKFLOW = """
# News Research 工作流 (深度分析版 v2)

## 核心理念
- 不做机械化的信息汇总
- 只关注有价值的重点新闻
- 中英文源混合，覆盖更全面
- 每条重点新闻都要有深入分析和思考

## 数据源 (15个)

### 英文源 (10个)
- Reuters (权重5) - 权威财经
- CNBC (权重4) - 商业新闻
- MIT Tech Review (权重5) - AI专业
- VentureBeat (权重5) - AI专业
- Wired (权重4) - 科技
- TechCrunch (权重4) - 科技
- Ars Technica (权重4) - 科技
- The Verge (权重4) - 科技
- Google News AI (权重4) - 聚合
- Google News Funding (权重4) - 融资

### 中文源 (5个)
- 钛媒体 (权重5) - RSS可抓取
- 爱范儿 (权重4) - RSS可抓取
- 36氪 (权重5) - 需browser
- 量子位 (权重5) - 需browser
- 机器之心 (权重5) - 需browser

## 执行步骤

### Step 1: 收集新闻
1. 英文源：使用 web_fetch 抓取 RSS
2. 中文源：
   - 钛媒体/爱范儿：用 web_fetch 抓取 RSS
   - 36氪/量子位/机器之心：用 browser 抓取 HTML
3. 解析并提取新闻条目
4. 按日期过滤（最近1-7天）

### Step 2: 去重处理
1. 跨源去重：相似标题只保留一个
2. 日期过滤：只保留最近N天的新闻

### Step 3: 排序
按权重排序：
- 来源权重：Reuters(5) > 钛媒体(5) > CNBC(4) > 其他(4)
- 内容质量：包含数据 +1分

### Step 4: 筛选重点新闻
根据以下标准判断是否为重点：
- 重大投资/融资（>$1B）
- 行业里程碑事件
- 政策监管动态
- AI安全/伦理问题
- 突破性技术
- 就业影响
- 市场重大变化

### Step 5: 深度分析（可选）
对于非常重要的新闻，可以深入研究：
1. 搜索更多背景信息
2. 找到相关数据
3. 分析对行业的影响

### Step 6: 分类整理
将新闻按以下类别整理：
- 💰 融资动态
- 📈 财报/市场
- 🔧 技术突破
- 🌍 政策/监管
- 💼 就业/职场
- 🔬 研究/学术

### Step 7: 生成报告
报告结构：
1. 今日概览（总数+分类统计）
2. 分类新闻列表（每条有分析思考）
3. 今日总结
4. 明日关注

### Step 8: 发送报告
- 生成Markdown
- 通过Discord发送
- 保存文件备份
"""

def get_collection_prompt(topic: str = "AI") -> str:
    """新闻收集提示词"""
    return f"""
请帮我收集今日关于「{topic}」的新闻。

需要抓取的RSS源：

【英文源】
1. Reuters: https://www.reutersagency.com/feed/?taxonomy=topics&post_type=best&topic=tech
2. Google News AI: https://news.google.com/rss/search?q=AI%20artificial%20intelligence
3. Google News Funding: https://news.google.com/rss/search?q=AI%20funding%20investment

【中文源】(如果有RSS可用)
4. 钛媒体: https://www.tmtpost.com/feed

请使用 web_fetch 抓取每个RSS源，解析XML获取新闻条目。
返回JSON数组格式：
[{{"title": "标题", "url": "链接", "source": "来源", "date": "日期", "lang": "en/zh"}}]
"""

def get_analysis_prompt(news_item: dict) -> str:
    """单条新闻分析提示词"""
    return f"""
请帮我分析这条重点新闻：

标题：{news_item.get('title', 'N/A')}
来源：{news_item.get('source', 'N/A')}
日期：{news_item.get('date', 'N/A')}

请给出：
1. **这新闻讲了什么？**（1句话）
2. **为什么重要？**（2-3句话）
3. **我的思考**：（3-4句话的深度分析，要有个人观点）
4. **后续关注**：（1-2个需要跟踪的点）
"""

def get_report_structure_prompt() -> str:
    """报告结构提示词"""
    return """
请按以下结构生成报告：

# AI行业深度分析 - YYYY年MM月DD日

> 今日共X条重点新闻
> 分类统计：融资X条 | 财报X条 | 技术X条 | 政策X条 | 就业X条

## 💰 融资动态
### 1. [新闻标题]
- 来源：xxx
- 分析：xxx

## 📈 财报/市场
...

## 📈 今日总结
（3-5句话的核心洞察）

## 👀 明日关注
- 关注点1
- 关注点2
"""

def main():
    print("=" * 60)
    print("News Research Workflow v2 loaded")
    print("=" * 60)
    print(f"数据源: 15个 (10英文 + 5中文)")
    print(f"功能: 深度分析 + 分类整理")
    print(f"Created at: {datetime.now().isoformat()}")

if __name__ == "__main__":
    main()
