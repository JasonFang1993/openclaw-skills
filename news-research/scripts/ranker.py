#!/usr/bin/env python3
"""
排序引擎模块
负责基于来源权威性和内容质量对新闻排序
"""

import re
from typing import List, Dict
from datetime import datetime

class RankingEngine:
    def __init__(self, config: dict = None):
        if config is None:
            config = {}
        
        self.source_weights = config.get("source_weights", {
            "reuters": 5,
            "机器之心": 5,
            "36kr": 4,
            "量子位": 4,
            "the_verge": 3,
            "techcrunch": 3,
            "ithome": 2,
            "aibase": 3,
        })
        
        self.content_factors = config.get("content_factors", {
            "has_numbers": 1,
            "has_quote": 1,
            "has_analysis": 2,
        })
    
    def get_source_weight(self, source_name: str) -> float:
        """获取来源权重"""
        source_lower = source_name.lower()
        
        # 精确匹配
        if source_lower in self.source_weights:
            return self.source_weights[source_lower]
        
        # 模糊匹配
        for key, weight in self.source_weights.items():
            if key in source_lower or source_lower in key:
                return weight
        
        return 3  # 默认权重
    
    def analyze_content(self, title: str, content: str = "") -> float:
        """分析内容质量"""
        score = 0.0
        
        if not content:
            return 0.0
        
        # 包含数字（数据、指标）
        if any(c.isdigit() for c in title):
            score += self.content_factors.get("has_numbers", 1)
        
        # 包含引号（引用）
        if '"' in title or "'" in title:
            score += self.content_factors.get("has_quote", 1)
        
        # 包含分析性词汇
        analysis_words = ["分析", "观点", "趋势", "解读", "预测", "报告", "研究"]
        if any(word in content for word in analysis_words):
            score += self.content_factors.get("has_analysis", 2)
        
        # 标题长度适中（不太短不太长）
        title_len = len(title)
        if 15 <= title_len <= 50:
            score += 1
        
        return score
    
    def calculate_news_score(self, news: dict) -> float:
        """计算单条新闻的综合得分"""
        source = news.get("source", "")
        title = news.get("title", "")
        content = news.get("content", title)  # 如果没有content，用title
        
        # 来源权重
        source_score = self.get_source_weight(source)
        
        # 内容质量
        content_score = self.analyze_content(title, content)
        
        # 综合得分
        total_score = source_score * 0.7 + content_score * 0.3
        
        return total_score
    
    def rank(self, news_list: List[dict]) -> List[dict]:
        """排序新闻列表"""
        if not news_list:
            return []
        
        # 计算每条新闻的得分
        scored_news = []
        for news in news_list:
            score = self.calculate_news_score(news)
            news["score"] = score
            scored_news.append(news)
        
        # 按得分排序
        scored_news.sort(key=lambda x: x["score"], reverse=True)
        
        # 去除score字段
        for news in scored_news:
            news.pop("score", None)
        
        return scored_news
    
    def rerank_by_topic(self, news_list: List[dict], topic: str) -> List[dict]:
        """根据主题重新排序（主题相关度高的排前面）"""
        if not topic or not news_list:
            return news_list
        
        topic_keywords = topic.lower().split()
        
        def topic_relevance(news: dict) -> float:
            title = news.get("title", "").lower()
            
            # 主题关键词匹配
            matches = sum(1 for kw in topic_keywords if kw in title)
            
            return matches * 0.5  # 主题相关度权重
        
        # 先按主题相关度排序
        news_with_relevance = []
        for news in news_list:
            relevance = topic_relevance(news)
            news["_relevance"] = relevance
            news_with_relevance.append(news)
        
        news_with_relevance.sort(key=lambda x: x["_relevance"], reverse=True)
        
        # 去除临时字段
        for news in news_with_relevance:
            news.pop("_relevance", None)
        
        return news_with_relevance
    
    def process(self, news_list: List[dict], topic: str = None, max_news: int = 15) -> List[dict]:
        """完整的排序流程"""
        if not news_list:
            return []
        
        print(f"\n排序处理:")
        print(f"  输入: {len(news_list)} 条新闻")
        
        # 1. 计算得分并排序
        news_list = self.rank(news_list)
        
        # 2. 如果有主题，按主题相关度调整
        if topic:
            news_list = self.rerank_by_topic(news_list, topic)
        
        # 3. 限制数量
        original_count = len(news_list)
        news_list = news_list[:max_news]
        
        print(f"  排序后: {len(news_list)} 条 (取前{max_news})")
        
        # 显示前几条
        if news_list:
            print(f"  Top 5:")
            for i, news in enumerate(news_list[:5]):
                print(f"    {i+1}. {news.get('title', '')[:40]}... ({news.get('source', '')})")
        
        print()
        
        return news_list


def main():
    """测试入口"""
    engine = RankingEngine()
    
    # 测试数据
    test_news = [
        {"title": "OpenAI发布GPT-5，性能提升100%", "source": "机器之心", "content": "OpenAI发布新模型..."},
        {"title": "谷歌发布新AI功能", "source": "36kr", "content": "谷歌宣布..."},
        {"title": "Meta开源新模型LLaMA 4", "source": "IT之家", "content": "Meta发布..."},
        {"title": "苹果AI功能全球上线", "source": "TechCrunch", "content": "苹果公司..."},
        {"title": "英伟达发布新芯片", "source": "机器之心", "content": "英伟达黄仁勋..."},
    ]
    
    print("测试排序引擎:")
    result = engine.process(test_news, topic="OpenAI")
    
    print(f"\n最终结果:")
    for i, news in enumerate(result):
        print(f"  {i+1}. {news['title']} ({news['source']})")


if __name__ == "__main__":
    main()
