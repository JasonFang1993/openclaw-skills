#!/usr/bin/env python3
"""
新闻详细概要抓取模块
使用Jina Reader获取每条新闻的详细内容
"""

import requests
import re
from datetime import datetime
from typing import List, Dict


class NewsDetailFetcher:
    """获取新闻详细内容"""
    
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        }
    
    def fetch_detail(self, url: str) -> str:
        """获取单条新闻的详细内容"""
        if not url or url == "http://www.36kr.com/p/" or not url.startswith("http"):
            return ""
        
        try:
            # 使用Jina Reader
            jina_url = f"https://r.jina.ai/{url}"
            response = requests.get(jina_url, headers=self.headers, timeout=15)
            if response.status_code == 200:
                content = response.text
                # 提取前500字作为概要
                lines = content.split('\n')
                text = ' '.join([l for l in lines if l.strip() and not l.startswith('#')])
                # 清理
                text = re.sub(r'!\[.*?\]', '', text)
                text = re.sub(r'\[.*?\]\(.*?\)', '', text)
                return text[:500] if text else ""
            return ""
        except:
            return ""
    
    def enrich_news(self, news_list: List[Dict]) -> List[Dict]:
        """为新闻列表添加详细内容"""
        enriched = []
        for news in news_list:
            url = news.get("url", "")
            desc = news.get("description", "")
            
            # 如果没有描述或者描述太短，获取详细内容
            if not desc or len(desc) < 50:
                detail = self.fetch_detail(url)
                if detail:
                    news["description"] = detail
            
            enriched.append(news)
        
        return enriched


def enrich_news_details(news_list: List[Dict]) -> List[Dict]:
    """为新闻添加详细内容"""
    fetcher = NewsDetailFetcher()
    return fetcher.enrich_news_details(news_list)


if __name__ == "__main__":
    # 测试
    test_news = [{"url": "https://www.qbitai.com/2026/02/382058.html", "description": ""}]
    fetcher = NewsDetailFetcher()
    result = fetcher.enrich_news(test_news)
    print(result[0].get("description", "")[:300])
