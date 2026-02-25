#!/usr/bin/env python3
"""
36氪新闻抓取模块
使用Jina Reader API抓取36氪AI新闻
"""

import requests
import re
from datetime import datetime
from typing import List, Dict


class Kr36Crawler:
    """36氪新闻抓取"""
    
    JINA_API = "https://r.jina.ai/http://www.36kr.com/information/AI/"
    
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        }
    
    def parse_36kr(self, content: str) -> List[Dict]:
        """解析36氪内容"""
        news_list = []
        
        # 匹配文章标题和链接
        # 格式: [标题](链接)
        pattern = r'\[([^\]]+)\]\(http://www\.36kr\.com/p/\d+\)'
        matches = re.findall(pattern, content)
        
        for title in matches[:10]:  # 最多10条
            # 过滤AI相关内容
            if any(kw in title for kw in ["AI", "人工智能", "大模型", "ChatGPT", "GPT", "模型", "智能", "Agent", "Sora", "芯片", "GPU", "英伟达", "OpenAI"]):
                news_list.append({
                    "title": title.strip(),
                    "url": f"http://www.36kr.com/p/",
                    "description": "",
                    "source": "36氪",
                    "pub_date": datetime.now().isoformat(),
                    "extracted_at": datetime.now().isoformat(),
                    "weight": 5,
                    "source_name": "36氪"
                })
        
        return news_list
    
    def fetch_36kr(self) -> List[Dict]:
        """抓取36氪AI新闻 - 使用Jina Reader"""
        try:
            # 使用Jina Reader抓取
            response = requests.get(self.JINA_API, headers=self.headers, timeout=30)
            if response.status_code == 200:
                return self.parse_36kr(response.text)
            else:
                print(f"   36氪: HTTP {response.status_code}")
                return []
        except Exception as e:
            print(f"   36氪: 错误 - {str(e)[:50]}")
            return []


def fetch_36kr_news() -> List[Dict]:
    """抓取36氪新闻"""
    crawler = Kr36Crawler()
    return crawler.fetch_36kr()


if __name__ == "__main__":
    news = fetch_36kr_news()
    print(f"获取到 {len(news)} 条36氪新闻")
    for n in news[:5]:
        print(f"  - {n['title']}")
