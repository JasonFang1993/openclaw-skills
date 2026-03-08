#!/usr/bin/env python3
"""
Ralph Loop 搜索模块
负责从各 RSS 源获取新闻
"""

import requests
from datetime import datetime
from typing import List, Dict
from rss_parser import RSSParser


class RalphLoop:
    """Ralph Loop - RSS 新闻获取"""
    
    # RSS 源配置
    RSS_SOURCES = {
        # 英文源
        "CNBC": {
            "url": "https://www.cnbc.com/id/100003114/device/rss/rss.html",
            "weight": 5,
            "keywords": ["AI", "artificial intelligence", "tech"],
            "max": 15
        },
        "MIT_Tech_Review": {
            "url": "https://www.technologyreview.com/feed/",
            "weight": 5,
            "keywords": ["AI", "artificial intelligence"],
            "max": 15
        },
        "Wired": {
            "url": "https://www.wired.com/feed/tag/ai/latest/rss",
            "weight": 4,
            "keywords": [],  # 放宽过滤
            "max": 15
        },
        "TechCrunch": {
            "url": "https://techcrunch.com/category/artificial-intelligence/feed/",
            "weight": 4,
            "keywords": [],  # 放宽过滤
            "max": 15
        },
        "Ars_Technica": {
            "url": "https://feeds.arstechnica.com/arstechnica/technology-lab",
            "weight": 4,
            "keywords": ["AI", "artificial intelligence"],
            "max": 15
        },
        # 中文源 - 优先使用RSS
        "钛媒体": {
            "url": "https://www.tmtpost.com/feed",
            "weight": 5,
            "keywords": [],  # 放宽过滤
            "max": 15
        },
        "爱范儿": {
            "url": "https://www.ifanr.com/feed",
            "weight": 4,
            "keywords": [],  # 放宽过滤
            "max": 15
        },
        "量子位": {
            "url": "https://www.qbitai.com/feed",
            "weight": 5,
            "keywords": [],  # 放宽过滤
            "max": 15
        },
        
        "36氪": {
            "url": "https://www.36kr.com/feed",
            "weight": 5,
            "keywords": [],  # 36氪是全品类，放宽过滤
            "max": 15
        },

        "雷锋网": {
            "url": "https://www.leiphone.com/feed",
            "weight": 4,
            "keywords": ["AI", "人工智能", "大模型"],
            "max": 15
        },
        "Google新闻中文AI": {
            "url": "https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx1YlY4U0FtVnVHZ0pWVXlnQVAB?hl=zh-CN",
            "weight": 4,
            "keywords": [],  # 放宽
            "max": 15
        },
        
        # 额外英文源
        "The_Verge_Tech": {
            "url": "https://www.theverge.com/rss/index.xml",
            "weight": 3,
            "keywords": [],
            "max": 15
        },
        "TechRadar": {
            "url": "https://www.techradar.com/rss",
            "weight": 3,
            "keywords": [],
            "max": 15
        },
    }
    
    def __init__(self, task: dict = None):
        self.task = task or {}
        self.parser = RSSParser()
        self.keywords = task.get("keywords", ["AI", "artificial intelligence", "人工智能"])
        self.days = task.get("days", 1)
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/rss+xml, application/xml,text/xml,*/*",
            "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8",
        }
    
    def fetch_rss(self, source_name: str, source_config: dict) -> List[Dict]:
        """获取单个 RSS 源"""
        url = source_config["url"]
        keywords = source_config.get("keywords", [])
        max_news = source_config.get("max", 15)  # 每个源最多15条
        
        # 合并关键词 - 如果源有关键词就用源的，否则用默认的
        if keywords:
            all_keywords = list(set(keywords))
        else:
            all_keywords = []  # 空关键词 = 不过滤
        
        try:
            response = requests.get(url, timeout=15, headers=self.headers)
            if response.status_code == 200:
                content = response.text
                news_list = self.parser.process_rss_source(content, source_name, all_keywords, self.days)
                
                # 按权重排序后取前max条
                news_list = sorted(news_list, key=lambda x: x.get("weight", 3), reverse=True)[:max_news]
                
                # 添加权重和来源
                for news in news_list:
                    news["weight"] = source_config.get("weight", 3)
                    news["source_name"] = source_name
                
                print(f"   {source_name}: 获取到 {len(news_list)} 条")
                return news_list
            else:
                print(f"   {source_name}: HTTP {response.status_code}")
                return []
        except Exception as e:
            print(f"   {source_name}: 错误 - {str(e)[:50]}")
            return []
    
    def fetch_all(self) -> List[Dict]:
        """获取所有 RSS 源"""
        all_news = []
        
        for source_name, source_config in self.RSS_SOURCES.items():
            news_list = self.fetch_rss(source_name, source_config)
            all_news.extend(news_list)
        
        return all_news
    
    def run(self) -> dict:
        """运行 Ralph Loop（同步版本）"""
        print(f"\n🔍 开始 RSS 搜索...")
        print(f"   关键词: {self.keywords}")
        print(f"   时间范围: 最近 {self.days} 天")
        print(f"   RSS 源数量: {len(self.RSS_SOURCES)}")
        
        news_list = self.fetch_all()
        
        print(f"\n   总计获取: {len(news_list)} 条新闻")
        
        # 更新 task
        self.task["results"] = news_list
        self.task["sources_count"] = len(self.RSS_SOURCES)
        self.task["fetched_at"] = datetime.now().isoformat()
        
        return self.task


# 同步入口
def run_ralph_loop(task: dict) -> dict:
    """Ralph Loop 主函数"""
    loop = RalphLoop(task)
    return loop.run()


# 异步入口（需要 aiohttp）
async def run_ralph_loop_async(task: dict) -> dict:
    """Ralph Loop 异步主函数"""
    loop = RalphLoop(task)
    return loop.run()


# 测试入口
def main():
    """测试入口"""
    task = {
        "keywords": ["AI", "artificial intelligence", "人工智能"],
        "days": 1
    }
    result = run_ralph_loop(task)
    print(f"\n获取到 {len(result.get('results', []))} 条新闻")


if __name__ == "__main__":
    main()
