#!/usr/bin/env python3
"""
报告生成模块
负责将新闻列表转换为结构化Markdown报告
支持中英文翻译
"""

import json
import re
from pathlib import Path
from datetime import datetime
from typing import List, Dict

# 常用AI术语中英文对照表（按优先级排序）
TRANSLATIONS = [
    # 公司/品牌 (优先匹配)
    ("OpenAI", "OpenAI"),
    ("Google", "谷歌"),
    ("Meta", "Meta"),
    ("Microsoft", "微软"),
    ("Apple", "苹果"),
    ("Nvidia", "英伟达"),
    ("NVIDIA", "英伟达"),
    ("Amazon", "亚马逊"),
    ("Anthropic", "Anthropic"),
    ("字节跳动", "字节跳动"),
    ("字节", "字节跳动"),
    ("腾讯", "腾讯"),
    ("阿里巴巴", "阿里巴巴"),
    ("阿里", "阿里巴巴"),
    ("百度", "百度"),
    ("苹果", "苹果"),
    
    # 术语
    ("Artificial Intelligence", "人工智能"),
    ("artificial intelligence", "人工智能"),
    ("AI", "人工智能"),
    ("machine learning", "机器学习"),
    ("deep learning", "深度学习"),
    ("large language model", "大语言模型"),
    ("LLM", "大语言模型"),
    ("GPT-5", "GPT-5"),
    ("GPT-4", "GPT-4"),
    ("GPT", "GPT"),
    ("Claude", "Claude"),
    ("Gemini", "Gemini"),
    ("LLaMA", "LLaMA"),
    ("Agent", "智能体"),
    ("agents", "智能体"),
    ("neural network", "神经网络"),
    ("multimodal", "多模态"),
    
    # 动词/名词
    ("launches", "发布"),
    ("launch", "发布"),
    ("releases", "发布"),
    ("release", "发布"),
    ("announces", "发布"),
    ("announce", "发布"),
    ("announcement", "发布"),
    ("breakthrough", "突破"),
    ("invests", "投资"),
    ("invest", "投资"),
    ("investment", "投资"),
    ("funding", "融资"),
    ("raises", "融资"),
    ("acquire", "收购"),
    ("acquisition", "收购"),
    ("partnership", "合作"),
    ("spreading", "扩散"),
    ("companions", "伴侣"),
    
    # 技术
    ("chip", "芯片"),
    ("GPU", "GPU"),
    ("TPU", "TPU"),
    ("transformer", "Transformer"),
    ("model", "模型"),
    ("models", "模型"),
    ("training", "训练"),
    ("inference", "推理"),
    
    # 其他
    ("startup", "初创公司"),
    ("tech giant", "科技巨头"),
    ("report", "报告"),
    ("study", "研究"),
    ("research", "研究"),
    ("safety", "安全"),
    ("security", "安全"),
    ("regulation", "监管"),
    ("jobs", "就业"),
    ("workforce", "劳动力"),
    ("workers", "工人"),
    ("obsolete", "淘汰"),
    ("promotions", "晋升"),
    ("staff", "员工"),
    ("deepfakes", "深度伪造"),
    ("says", "表示"),
    ("admits", "承认"),
]

def translate_to_chinese(text: str) -> str:
    """翻译文本为中文"""
    if not text:
        return text
    
    result = text
    
    # 按长度降序排序，先匹配长的
    for eng, chi in TRANSLATIONS:
        result = result.replace(eng, chi)
    
    # 处理 $XX billion -> XX十亿美元
    result = re.sub(r'\$(\d+(?:\.\d+)?)\s*billion', r'\1十亿美元', result)
    result = re.sub(r'\$(\d+(?:\.\d+)?)\s*million', r'\1百万美元', result)
    
    return result

def translate_news_title(title: str) -> str:
    """翻译新闻标题"""
    return translate_to_chinese(title)

def translate_source(source: str) -> str:
    """翻译来源名称"""
    source_translations = {
        "Reuters": "路透社",
        "The Guardian": "卫报",
        "The Motley Fool": "The Motley Fool",
        "TechCrunch": "TechCrunch",
        "Wired": "Wired",
        "MIT Technology Review": "MIT科技评论",
        "VentureBeat": "VentureBeat",
        "The Verge": "The Verge",
        "Yahoo": "Yahoo",
        "Johns Hopkins University": "约翰霍普金斯大学",
        "Google News": "谷歌新闻",
    }
    return source_translations.get(source, source)


class ReportFormatter:
    def __init__(self, config: dict = None):
        if config is None:
            config = {}
        
        self.format = config.get("format", "markdown")
        self.max_news = config.get("max_news", 15)
        self.include_summary = config.get("include_summary", True)
        self.include_highlights = config.get("include_highlights", True)
        self.translate = config.get("translate", True)
    
    def translate_news(self, news: dict) -> dict:
        """翻译单条新闻"""
        if not self.translate:
            return news
        
        translated = news.copy()
        translated["title"] = translate_news_title(news.get("title", ""))
        translated["source"] = translate_source(news.get("source", ""))
        return translated
    
    def generate_summary(self, news_list: List[dict], topic: str) -> str:
        """生成摘要"""
        if not news_list:
            return "暂无新闻"
        
        sources = {}
        for news in news_list:
            source = news.get("source", "未知")
            sources[source] = sources.get(source, 0) + 1
        
        summary_parts = []
        summary_parts.append(f"今日共收录 **{len(news_list)}** 条{topic}相关新闻")
        
        if sources:
            top_sources = sorted(sources.items(), key=lambda x: x[1], reverse=True)[:3]
            source_str = "、".join([f"{s}({c}条)" for s, c in top_sources])
            summary_parts.append(f"主要来源：{source_str}")
        
        return "，".join(summary_parts)
    
    def extract_highlights(self, title: str) -> str:
        """从标题提取划重点"""
        highlights = []
        
        if any(c.isdigit() for c in title):
            numbers = re.findall(r'(\d+(?:\.\d+)?[亿万亿%个]?)', title)
            if numbers:
                highlights.append(f"数据：{', '.join(numbers)}")
        
        companies = ["OpenAI", "谷歌", "Meta", "微软", "苹果", "英伟达", "阿里", "字节跳动", "腾讯", "百度"]
        for company in companies:
            if company in title:
                highlights.append(f"涉及：{company}")
                break
        
        return " | ".join(highlights) if highlights else "暂无"
    
    def generate_trends(self, news_list: List[dict]) -> str:
        """生成趋势分析"""
        if not news_list:
            return "暂无趋势分析"
        
        keywords = {
            "大模型": 0,
            "智能体": 0,
            "融资": 0,
            "发布": 0,
            "开源": 0,
            "芯片": 0,
            "安全": 0,
            "监管": 0,
            "投资": 0,
        }
        
        for news in news_list:
            title = news.get("title", "")
            for kw in keywords:
                if kw in title:
                    keywords[kw] += 1
        
        trends = sorted(keywords.items(), key=lambda x: x[1], reverse=True)
        trends = [(k, v) for k, v in trends if v > 0]
        
        if not trends:
            return "暂无明显趋势"
        
        trend_str = "、".join([f"{k}({v})" for k, v in trends[:5]])
        
        return f"热点关键词：{trend_str}"
    
    def format_news_item(self, news: dict, index: int) -> str:
        """格式化单条新闻"""
        news = self.translate_news(news)
        
        title = news.get("title", "无标题")
        source = news.get("source", "未知来源")
        
        highlights = self.extract_highlights(title)
        
        lines = []
        lines.append(f"### {index+1}. {title}")
        lines.append(f"")
        lines.append(f"- **来源**：{source}")
        
        if highlights and highlights != "暂无":
            lines.append(f"- **划重点**：{highlights}")
        
        if news.get("url"):
            lines.append(f"- **链接**：{news['url']}")
        
        lines.append("")
        
        return "\n".join(lines)
    
    def format_report(self, news_list: List[dict], topic: str = "AI") -> str:
        """生成完整报告"""
        if self.translate:
            news_list = [self.translate_news(n) for n in news_list]
        
        date_str = datetime.now().strftime("%Y年%m月%d日")
        
        lines = []
        lines.append(f"# {topic}行业新闻日报 - {date_str}")
        lines.append("")
        lines.append("---")
        lines.append("")
        
        if self.include_summary:
            summary = self.generate_summary(news_list, topic)
            lines.append(f"> {summary}")
            lines.append("")
        
        lines.append("## 今日要闻")
        lines.append("")
        
        if news_list:
            for i, news in enumerate(news_list):
                lines.append(self.format_news_item(news, i))
        else:
            lines.append("暂无新闻")
            lines.append("")
        
        if self.include_highlights:
            lines.append("---")
            lines.append("")
            lines.append("## 趋势总结")
            lines.append("")
            trends = self.generate_trends(news_list)
            lines.append(f"- {trends}")
            lines.append("")
        
        lines.append("---")
        lines.append(f"*由 OpenClaw News Research 自动生成 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
        
        return "\n".join(lines)
    
    def save_report(self, report: str, output_dir: str = None, filename: str = None) -> str:
        """保存报告到文件"""
        if output_dir is None:
            output_dir = Path.home() / ".openclaw" / "workspace" / "kbase" / "dailynews" / datetime.now().strftime("%Y-%m-%d")
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        if filename is None:
            filename = f"{datetime.now().strftime('%Y-%m-%d')}.md"
        
        file_path = output_path / filename
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        return str(file_path)
    
    def process(self, news_list: List[dict], topic: str = "AI", output: bool = True) -> dict:
        """完整的报告生成流程"""
        if not news_list:
            news_list = []
        
        print(f"\n报告生成:")
        print(f"  主题: {topic}")
        print(f"  新闻数: {len(news_list)}")
        print(f"  翻译: {'开启' if self.translate else '关闭'}")
        
        news_list = news_list[:self.max_news]
        
        report = self.format_report(news_list, topic)
        
        result = {
            "report": report,
            "news_count": len(news_list),
            "topic": topic,
            "date": datetime.now().strftime("%Y-%m-%d"),
        }
        
        if output:
            file_path = self.save_report(report)
            result["file_path"] = file_path
            print(f"  报告已保存: {file_path}")
        
        return result


def main():
    """测试入口"""
    formatter = ReportFormatter()
    
    test_news = [
        {"title": "Big Tech to invest $650 billion in AI in 2026", "source": "Reuters", "url": "https://reuters.com/1"},
        {"title": "Deepfakes spreading and more AI companions: AI safety report", "source": "The Guardian", "url": "https://guardian.com/2"},
        {"title": "Accenture links staff promotions to use of AI tools", "source": "The Guardian", "url": "https://guardian.com/3"},
    ]
    
    print("测试报告生成（翻译后）:")
    result = formatter.process(test_news, topic="AI")
    print(result["report"])


if __name__ == "__main__":
    main()
