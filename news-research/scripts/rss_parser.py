#!/usr/bin/env python3
"""
RSS 解析模块
用于从 RSS 订阅源获取新闻
"""

import re
from datetime import datetime
from typing import List, Dict, Optional


class RSSParser:
    """RSS 解析器"""
    
    def __init__(self):
        pass
    
    def parse_date(self, date_str: str) -> Optional[datetime]:
        """解析日期字符串"""
        if not date_str:
            return None
        
        formats = [
            "%a, %d %b %Y %H:%M:%S %z",
            "%Y-%m-%dT%H:%M:%SZ",
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d",
        ]
        
        for fmt in formats:
            try:
                if '+' in date_str:
                    date_str = date_str.split('+')[0].strip()
                return datetime.strptime(date_str.strip(), fmt)
            except:
                continue
        
        return None
    
    def extract_news_from_rss(self, rss_content: str, source_name: str) -> List[Dict]:
        """从 RSS 内容中提取新闻"""
        news_items = []
        
        try:
            # 替换 CDATA 标记
            rss_content = re.sub(r'<!\[CDATA\[', '<![CDATA[', rss_content)
            rss_content = re.sub(r'\]\]>', ']]>', rss_content)
            
            # 提取每个 item
            item_pattern = r'<item>(.*?)</item>'
            items = re.findall(item_pattern, rss_content, re.DOTALL)
            
            for item_content in items:
                # 提取完整内容（如果有）
                full_content = ""
                content_match = re.search(r'<content:encoded><!\[CDATA\[(.*?)\]\]></content:encoded>', item_content, re.DOTALL)
                if not content_match:
                    content_match = re.search(r'<content:encoded>(.*?)</content:encoded>', item_content, re.DOTALL)
                if content_match:
                    full_content = content_match.group(1)
                    # 清理HTML
                    full_content = re.sub(r'<[^>]+>', '', full_content)
                    full_content = re.sub(r'\s+', ' ', full_content).strip()[:800]
                
                # 提取标题
                title_match = re.search(r'<title><!\[CDATA\[(.*?)\]\]></title>', item_content)
                if not title_match:
                    title_match = re.search(r'<title>(.*?)</title>', item_content)
                title = title_match.group(1).strip() if title_match else ""
                
                if not title or len(title) < 5:
                    continue
                
                # 提取链接
                link_match = re.search(r'<link>(.*?)</link>', item_content)
                link = link_match.group(1).strip() if link_match else ""
                
                # 提取描述
                desc_match = re.search(r'<description><!\[CDATA\[(.*?)\]\]></description>', item_content)
                if not desc_match:
                    desc_match = re.search(r'<description>(.*?)</description>', item_content)
                description = desc_match.group(1).strip() if desc_match else ""
                description = re.sub(r'<[^>]+>', '', description)[:500]
                
                # 提取日期
                date_match = re.search(r'<pubDate>(.*?)</pubDate>', item_content)
                pub_date = None
                if date_match:
                    pub_date = self.parse_date(date_match.group(1))
                
                news_items.append({
                    "title": title,
                    "url": link,
                    "description": description,
                    "full_content": full_content,  # 完整内容
                    "source": source_name,
                    "pub_date": pub_date.isoformat() if pub_date else None,
                    "extracted_at": datetime.now().isoformat()
                })
        
        except Exception as e:
            print(f"RSS解析错误 {source_name}: {e}")
        
        return news_items
    
    def is_recent(self, news: Dict, days: int = 1) -> bool:
        """判断新闻是否在最近几天内"""
        if not news.get("pub_date"):
            return True
        
        try:
            pub_date = datetime.fromisoformat(news["pub_date"])
            delta = (datetime.now() - pub_date).days
            return delta < days
        except:
            return True
    
    def filter_by_keywords(self, news_items: List[Dict], keywords: List[str]) -> List[Dict]:
        """根据关键词过滤新闻"""
        # 非AI关键词需要过滤
        non_ai_keywords = ["游艇", "汽车", "新车", "车型", "股价", "房地产", "房价", "宠物", "食品", "饮料", "酒店", "旅游", "航空", "足球", "篮球", "电影", "电视剧", "综艺", "明星", "八卦", "万科", "万达", "地产"]
        
        # 如果没有设置关键词，返回所有（但要过滤非AI）
        if not keywords:
            filtered = []
            for news in news_items:
                title = news.get("title", "")
                if not any(kw in title for kw in non_ai_keywords):
                    filtered.append(news)
            return filtered
        
        filtered = []
        keywords_lower = [kw.lower() for kw in keywords]
        
        for news in news_items:
            title = news.get("title", "").lower()
            desc = news.get("description", "").lower()
            
            if any(kw in title or kw in desc for kw in keywords_lower):
                filtered.append(news)
        
        return filtered
    
    def process_rss_source(self, rss_content: str, source_name: str, keywords: List[str] = None, days: int = 1) -> List[Dict]:
        """处理单个 RSS 源"""
        # 解析 RSS
        news_items = self.extract_news_from_rss(rss_content, source_name)
        
        # 按日期过滤
        news_items = [n for n in news_items if self.is_recent(n, days)]
        
        # 按关键词过滤
        if keywords:
            news_items = self.filter_by_keywords(news_items, keywords)
        
        return news_items


def main():
    """测试入口"""
    import sys
    
    test_rss = '''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
<channel>
<title>Test News</title>
<link>https://example.com</link>
<item>
<title>AI Breakthrough in 2026</title>
<link>https://example.com/1</link>
<description>A major breakthrough in AI research</description>
<pubDate>Tue, 24 Feb 2026 03:00:00 GMT</pubDate>
</item>
</channel>
</rss>'''
    
    parser = RSSParser()
    news = parser.process_rss_source(test_rss, "Test Source", ["AI"], days=1)
    
    print(f"解析到 {len(news)} 条新闻:")
    for n in news:
        print(f"  - {n['title']}")


if __name__ == "__main__":
    main()
