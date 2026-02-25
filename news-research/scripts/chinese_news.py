#!/usr/bin/env python3
"""
中文新闻源抓取模块
使用Jina Reader API抓取各种中文科技新闻
"""

import requests
import re
from datetime import datetime
from typing import List, Dict


class ChineseNewsCrawler:
    """中文新闻源抓取 - 使用Jina Reader"""
    
    SOURCES = {
        "36氪": "https://www.36kr.com/information/AI/",
        "虎嗅": "https://www.huxiu.com/channel/103",
        "极客公园": "https://www.geekpark.com/topic/300025",
        "爱范儿": "https://www.ifanr.com/",
        "量子位": "https://www.qbitai.com/",
        "钛媒体": "https://www.tmtpost.com/",
        "雷锋网": "https://www.leiphone.com/",
    }
    
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        }
    
    def parse_content(self, content: str, source: str) -> List[Dict]:
        """解析抓取内容"""
        news_list = []
        
        # 提取链接和标题 [标题](链接) 格式
        pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        matches = re.findall(pattern, content)
        
        seen_titles = set()
        for title, url in matches[:15]:
            title = title.strip()
            if not title or title in seen_titles:
                continue
            seen_titles.add(title)
            
            # 过滤AI相关内容
            if any(kw in title for kw in ["AI", "人工智能", "大模型", "ChatGPT", "GPT", "模型", "智能", "Agent", "Sora", "芯片", "GPU", "英伟达", "OpenAI", "字节", "百度", "阿里", "腾讯", "MCP", "OpenClaw", "Claude", "马斯克", "收购", "融资", "发布", "Open", "Gemini"]):
                news_list.append({
                    "title": title,
                    "url": url.strip() if url.startswith('http') else f"https://{url}",
                    "description": "",
                    "source": source,
                    "pub_date": datetime.now().isoformat(),
                    "extracted_at": datetime.now().isoformat(),
                    "weight": 4,
                    "source_name": source
                })
        
        return news_list
    
    def fetch_source(self, name: str, url: str) -> List[Dict]:
        """抓取单个源"""
        try:
            # 使用Jina Reader
            jina_url = f"https://r.jina.ai/http://{url.replace('https://', '').replace('http://', '')}"
            response = requests.get(jina_url, headers=self.headers, timeout=30)
            if response.status_code == 200:
                return self.parse_content(response.text, name)
            else:
                print(f"   {name}: HTTP {response.status_code}")
                return []
        except Exception as e:
            print(f"   {name}: 错误 - {str(e)[:30]}")
            return []
    
    def fetch_all(self) -> List[Dict]:
        """抓取所有源"""
        all_news = []
        for name, url in self.SOURCES.items():
            news = self.fetch_source(name, url)
            all_news.extend(news)
            if news:
                print(f"   {name}: 获取到 {len(news)} 条")
        return all_news


def fetch_chinese_news() -> List[Dict]:
    """抓取中文新闻"""
    crawler = ChineseNewsCrawler()
    return crawler.fetch_all()


if __name__ == "__main__":
    news = fetch_chinese_news()
    print(f"\n总共获取到 {len(news)} 条中文新闻")
