#!/usr/bin/env python3
"""
去重引擎模块
负责跨源去重、跨天去重、日期校验
"""

import json
import os
import re
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Set

class DedupEngine:
    def __init__(self, config: dict = None):
        if config is None:
            config = {}
        
        self.title_threshold = config.get("title_similarity_threshold", 0.7)
        self.check_cross_day = config.get("check_cross_day", True)
    
    def normalize_title(self, title: str) -> str:
        """标准化标题：去除标点、转小写、去除空格"""
        if not title:
            return ""
        
        # 转小写
        title = title.lower()
        
        # 去除标点和特殊字符
        title = re.sub(r'[^\w\s]', '', title)
        
        # 去除多余空格
        title = ' '.join(title.split())
        
        return title
    
    def calculate_similarity(self, title1: str, title2: str) -> float:
        """计算两个标题的相似度（简单版：字符集交集）"""
        if not title1 or not title2:
            return 0.0
        
        set1 = set(self.normalize_title(title1))
        set2 = set(self.normalize_title(title2))
        
        if not set1 or not set2:
            return 0.0
        
        # Jaccard相似度
        intersection = len(set1 & set2)
        union = len(set1 | set2)
        
        return intersection / union if union > 0 else 0.0
    
    def is_duplicate(self, title1: str, title2: str) -> bool:
        """判断两个标题是否重复"""
        # 完全相同
        if self.normalize_title(title1) == self.normalize_title(title2):
            return True
        
        # 相似度超过阈值
        similarity = self.calculate_similarity(title1, title2)
        return similarity >= self.title_threshold
    
    def dedup_by_title(self, news_list: List[dict]) -> List[dict]:
        """跨源去重"""
        if not news_list:
            return []
        
        unique_news = []
        seen_titles = []
        
        for news in news_list:
            title = news.get("title", "")
            is_dup = False
            
            for seen_title in seen_titles:
                if self.is_duplicate(title, seen_title):
                    is_dup = True
                    break
            
            if not is_dup:
                unique_news.append(news)
                seen_titles.append(title)
        
        return unique_news
    
    def extract_date_from_content(self, content: str) -> datetime:
        """从内容中提取日期"""
        if not content:
            return None
        
        # 常见的日期格式
        date_patterns = [
            r'(\d{4})[年/-](\d{1,2})[月/-](\d{1,2})',
            r'(\d{1,2})[月/-](\d{1,2})',
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, content)
            if match:
                groups = match.groups()
                if len(groups) == 3:
                    year, month, day = int(groups[0]), int(groups[1]), int(groups[2])
                    if year < 100:
                        year += 2000
                    return datetime(year, month, day)
                elif len(groups) == 2:
                    month, day = int(groups[0]), int(groups[1])
                    return datetime(datetime.now().year, month, day)
        
        return None
    
    def extract_date_from_title(self, title: str) -> datetime:
        """从标题中提取日期"""
        return self.extract_date_from_content(title)
    
    def is_today(self, news: dict, days: int = 1) -> bool:
        """判断新闻是否是最近几天的"""
        # 优先从标题提取
        date = self.extract_date_from_title(news.get("title", ""))
        if date:
            delta = (datetime.now() - date).days
            return delta < days
        
        # 从URL提取
        url = news.get("url", "")
        date_patterns = [
            r'/(\d{4})(\d{2})(\d{2})/',
            r'/(\d{4})-(\d{2})-(\d{2})/',
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, url)
            if match:
                year, month, day = int(match.group(1)), int(match.group(2)), int(match.group(3))
                date = datetime(year, month, day)
                delta = (datetime.now() - date).days
                return delta < days
        
        # 提取不到日期，默认认为是最近的
        return True
    
    def filter_by_date(self, news_list: List[dict], days: int = 1) -> List[dict]:
        """按日期过滤"""
        filtered = []
        
        for news in news_list:
            if self.is_today(news, days):
                filtered.append(news)
        
        return filtered
    
    def load_previous_news(self, days: int = 1) -> List[dict]:
        """加载前几天的新闻（用于跨天去重）"""
        previous_news = []
        
        # 查找之前的报告
        base_dir = Path.home() / ".openclaw" / "workspace" / "kbase" / "news"
        
        if not base_dir.exists():
            return []
        
        for i in range(1, days + 1):
            date = datetime.now() - timedelta(days=i)
            date_str = date.strftime("%Y-%m-%d")
            
            # 查找对应日期的文件
            for f in base_dir.glob(f"*/{date_str}.md"):
                try:
                    with open(f, 'r', encoding='utf-8') as file:
                        content = file.read()
                        # 简单提取标题（实际应该解析更准确）
                        lines = content.split('\n')
                        for line in lines:
                            if line.startswith('## '):
                                previous_news.append({"title": line[3:]})
                except Exception as e:
                    print(f"读取失败 {f}: {e}")
        
        return previous_news
    
    def dedup_cross_day(self, news_list: List[dict], previous_news: List[dict]) -> List[dict]:
        """跨天去重"""
        if not previous_news:
            return news_list
        
        unique_news = []
        
        for news in news_list:
            title = news.get("title", "")
            is_dup = False
            
            for prev in previous_news:
                prev_title = prev.get("title", "")
                if self.is_duplicate(title, prev_title):
                    is_dup = True
                    break
            
            if not is_dup:
                unique_news.append(news)
        
        return unique_news
    
    def process(self, news_list: List[dict], days: int = 1) -> List[dict]:
        """完整的去重流程"""
        if not news_list:
            return []
        
        print(f"\n去重处理:")
        print(f"  输入: {len(news_list)} 条新闻")
        
        # 1. 跨源去重
        news_list = self.dedup_by_title(news_list)
        print(f"  跨源去重后: {len(news_list)} 条")
        
        # 2. 日期过滤
        news_list = self.filter_by_date(news_list, days)
        print(f"  日期过滤后: {len(news_list)} 条")
        
        # 3. 跨天去重
        if self.check_cross_day:
            previous_news = self.load_previous_news(days)
            if previous_news:
                news_list = self.dedup_cross_day(news_list, previous_news)
                print(f"  跨天去重后: {len(news_list)} 条")
        
        print(f"  最终: {len(news_list)} 条\n")
        
        return news_list


def main():
    """测试入口"""
    engine = DedupEngine()
    
    # 测试数据
    test_news = [
        {"title": "OpenAI发布新模型GPT-5", "source": "36kr"},
        {"title": "OpenAI发布新模型GPT-5", "source": "机器之心"},
        {"title": "谷歌推出新AI功能", "source": "IT之家"},
        {"title": "2024年的旧新闻", "source": "测试"},
        {"title": "Meta发布开源大模型", "source": "AIBase"},
    ]
    
    print("测试去重引擎:")
    result = engine.process(test_news)
    
    print(f"\n结果: {len(result)} 条")
    for news in result:
        print(f"  - {news['title']} ({news['source']})")


if __name__ == "__main__":
    main()
