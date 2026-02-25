#!/usr/bin/env python3
"""
RSS 解析模块
用于从 RSS 订阅源获取新闻
"""

import re
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path

class RSSParser:
    """RSS 解析器"""
    
    def __init__(self):
        self.namespaces = {
            'media': 'http://search.yahoo.com/mrss/',
            'content': 'http://purl.org/rss/1.0/modules/content/',
        }
    
    def parse_date(self, date_str: str) -> Optional[datetime]:
        """解析日期字符串"""
        if not date_str:
            return None
        
        formats = [
            "%a, %d %b %Y %H:%M:%S %z",  # RFC 822
            "%Y-%m-%dT%H:%M:%SZ",        # ISO 8601
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d",
        ]
        
        for fmt in formats:
            try:
                # 移除时区部分（如果有）
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
            # 解析 XML
            root = ET.fromstring(rss_content)
            
            # 获取 channel
            channel = root.find('channel')
            if channel is None:
                return news_items
            
            # 遍历所有 item
            for item in channel.findall('item'):
                try:
                    # 提取标题
                    title_elem = item.find('title')
                    title = title_elem.text if title_elem is not None and title_elem.text else ""
                    
                    # 提取链接
                    link_elem = item.find('link')
                    link = link_elem.text if link_elem is not None and link_elem.text else ""
                    
                    # 提取描述
                    desc_elem = item.find('description')
                    description = desc_elem.text if desc_elem is not None and desc_elem.text else ""
                    
                    # 清理 HTML 标签
                    description = re.sub(r'<[^>]+>', '', description)
                    description = description.strip()
                    
                    # 提取日期
                    date_elem = item.find('pubDate')
                    pub_date = None
                    if date_elem is not None and date_elem.text:
                        pub_date = self.parse_date(date_elem.text)
                    
                    # 提取来源
                    source = source_name
                    source_elem = item.find('source')
                    if source_elem is not None and source_elem.text:
                        source = source_elem.text
                    
                    # 跳过空标题
                    if not title or len(title) < 5:
                        continue
                    
                    news_items.append({
                        "title": title.strip(),
                        "url": link.strip() if link else "",
                        "description": description[:500] if description else "",
                        "source": source,
                        "pub_date": pub_date.isoformat() if pub_date else None,
                        "extracted_at": datetime.now().isoformat()
                    })
                    
                except Exception as e:
                    # 跳过解析错误的 item
                    continue
        
        except Exception as e:
            print(f"RSS解析错误 {source_name}: {e}")
        
        return news_items
    
    def is_recent(self, news: Dict, days: int = 1) -> bool:
        """判断新闻是否在最近几天内"""
        if not news.get("pub_date"):
            return True  # 没有日期信息，默认保留
        
        try:
            pub_date = datetime.fromisoformat(news["pub_date"])
            delta = (datetime.now() - pub_date).days
            return delta < days
        except:
            return True
    
    def filter_by_keywords(self, news_items: List[Dict], keywords: List[str]) -> List[Dict]:
        """根据关键词过滤新闻"""
        if not keywords:
            return news_items
        
        filtered = []
        keywords_lower = [kw.lower() for kw in keywords]
        
        for news in news_items:
            title = news.get("title", "").lower()
            desc = news.get("description", "").lower()
            
            # 如果标题或描述包含关键词
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
    
    # 测试 RSS 解析
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
<item>
<title>Machine Learning Update</title>
<link>https://example.com/2</link>
<description>New ML techniques announced</description>
<pubDate>Mon, 23 Feb 2026 12:00:00 GMT</pubDate>
</item>
</channel>
</rss>'''
    
    parser = RSSParser()
    news = parser.process_rss_source(test_rss, "Test Source", ["AI", "ML"], days=1)
    
    print(f"解析到 {len(news)} 条新闻:")
    for n in news:
        print(f"  - {n['title']}")


if __name__ == "__main__":
    main()
