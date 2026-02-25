#!/usr/bin/env python3
"""
Jina Reader - 获取新闻完整内容
"""

import requests
import re
from typing import List, Dict
import time


def fetch_news_content(url: str) -> str:
    """获取单条新闻的完整内容"""
    if not url or not url.startswith("http"):
        return ""
    
    try:
        jina_url = f"https://r.jina.ai/{url}"
        resp = requests.get(jina_url, timeout=30, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
        if resp.status_code == 200:
            content = resp.text
            
            # 提取主要内容
            if "Markdown Content:" in content:
                content = content.split("Markdown Content:")[1]
            
            # 清理
            content = re.sub(r'!\[.*?\]', '', content)  # 图片
            content = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', content)  # 链接
            content = re.sub(r'http[^\s]+', '', content)  # URL
            content = re.sub(r'<[^>]+>', '', content)  # HTML
            content = re.sub(r'\*+', '', content)  # 星号
            content = re.sub(r'#+\s*', '', content)  # 标题
            content = re.sub(r'=+\s*', '', content)  # 分隔符
            
            # 移除网站名和导航
            skip_words = ["钛媒体", "量子位", "爱范儿", "36氪", "雷锋网", "虎嗅", "极客公园", 
                         "TechCrunch", "Wired", "CNBC", "MIT", "Ars Technica",
                         "视频", "直播", "登录", "注册", "App下载", "微信公众号",
                         "更多精彩", "热门推荐", "相关阅读", "责任编辑", "作者:",
                         "企服", "创投", "咨询", "活动", "钛空时间", "集团时光", "公众号"]
            for w in skip_words:
                content = content.replace(w, '')
            
            # 提取句子
            sentences = []
            for sent in content.split('。'):
                sent = sent.strip()
                if len(sent) > 15:  # 至少15个字符
                    sentences.append(sent)
            
            # 返回前8句话
            return '。'.join(sentences[:8]) + '。'
            
        return ""
    except Exception as e:
        return ""


def fetch_all_news_details(news_list: List[Dict]) -> List[Dict]:
    """获取所有新闻的完整内容"""
    total = len(news_list)
    print(f"   共{total}条新闻，开始逐条获取完整内容...")
    
    for i, news in enumerate(news_list):
        url = news.get("url", "")
        title = news.get("title", "")[:30]
        
        print(f"   [{i+1}/{total}] 正在获取: {title}...")
        
        if url and url.startswith("http"):
            content = fetch_news_content(url)
            if content:
                news["description"] = content
        
        # 避免请求太频繁
        time.sleep(0.5)
    
    print(f"   内容获取完成！")
    return news_list


if __name__ == "__main__":
    # 测试
    test = [{"url": "https://www.qbitai.com/2026/02/382058.html", "title": "测试", "description": ""}]
    result = fetch_all_news_details(test)
    print(result[0].get("description", "")[:500])
