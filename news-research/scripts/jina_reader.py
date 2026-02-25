#!/usr/bin/env python3
"""
Jina Reader - 获取新闻详细内容
"""

import requests
import re
from typing import Dict


def fetch_news_detail(url: str) -> str:
    """获取单条新闻详细内容"""
    if not url or not url.startswith("http"):
        return ""
    
    try:
        jina_url = f"https://r.jina.ai/{url}"
        resp = requests.get(jina_url, timeout=20, headers={
            "User-Agent": "Mozilla/5.0"
        })
        if resp.status_code == 200:
            content = resp.text
            
            # 只提取Markdown Content部分
            if "Markdown Content:" in content:
                content = content.split("Markdown Content:")[1]
            
            # 移除所有图片、链接、HTML标签
            content = re.sub(r'!\[.*?\]', '', content)  # 图片
            content = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', content)  # 链接变文本
            content = re.sub(r'http[^\s]+', '', content)  # URL
            content = re.sub(r'<[^>]+>', '', content)  # HTML
            content = re.sub(r'\*+', '', content)  # 星号
            content = re.sub(r'#+\s*', '', content)  # 标题标记
            content = re.sub(r'=+\s*', '', content)  # 分隔符
            content = re.sub(r'\|.*?\|', '', content)  # 表格
            
            # 移除网站名和导航
            skip_words = ["钛媒体", "量子位", "爱范儿", "36氪", "雷锋网", "虎嗅", "极客公园", 
                         "TechCrunch", "Wired", "CNBC", "MIT", "Ars Technica",
                         "视频", "直播", "登录", "注册", "App下载", "微信公众号",
                         "更多精彩", "热门推荐", "相关阅读", "责任编辑", "作者:"]
            for w in skip_words:
                content = content.replace(w, '')
            
            # 提取段落（找有标点的句子）
            sentences = []
            for sent in content.split('。'):
                sent = sent.strip()
                if len(sent) > 20:  # 至少20个字符
                    sentences.append(sent)
            
            if sentences:
                return (sentences[0] + '。').strip()[:400]
            
            # 如果没有句子，取纯文字
            text = ' '.join(content.split())
            return text.strip()[:400]
            
        return ""
    except:
        return ""


def enrich_top_news(news_list: list, top_n: int = 10) -> list:
    """为前N条新闻补充详细内容"""
    print(f"\n📥 正在获取前{top_n}条新闻的详细内容...")
    
    for i, news in enumerate(news_list[:top_n]):
        url = news.get("url", "")
        if url and url.startswith("http"):
            print(f"   [{i+1}] 获取: {news.get('title', '')[:40]}...")
            detail = fetch_news_detail(url)
            if detail:
                news["description"] = detail
            else:
                # 如果抓取失败，用标题生成
                news["description"] = _generate_from_title(news.get("title", ""))
        else:
            news["description"] = _generate_from_title(news.get("title", ""))
    
    # 剩余的新闻也生成描述
    for news in news_list[top_n:]:
        if not news.get("description"):
            news["description"] = _generate_from_title(news.get("title", ""))
    
    return news_list


def _generate_from_title(title: str) -> str:
    """从标题生成描述"""
    companies = ["谷歌", "OpenAI", "阿里", "百度", "字节", "腾讯", "Meta", "微软", "英伟达", "Anthropic", "特斯拉", "苹果", "华为", "IBM", "英伟达"]
    company = next((c for c in companies if c in title), "")
    nums = re.findall(r'(\d+[亿万亿%]?)', title)
    data = "，涉及" + "、".join(nums[:2]) if nums else ""
    
    if "融资" in title:
        return f"AI领域重要融资事件，{company}相关{data}"
    elif "发布" in title or "上线" in title:
        return f"AI领域新产品发布，{company}{data}"
    elif "开源" in title:
        return f"开源AI重要进展，{company}{data}"
    elif "芯片" in title or "GPU" in title:
        return f"AI硬件/算力领域动态，{company}{data}"
    elif "大跌" in title or "暴涨" in title:
        return f"AI行业重大市场变化，{company}{data}"
    else:
        return f"AI行业重要新闻{company}{data}"


if __name__ == "__main__":
    # 测试
    test = [{"url": "https://www.qbitai.com/2026/02/382058.html", "title": "测试", "description": ""}]
    result = enrich_top_news(test, 1)
    print(result[0].get("description", "")[:200])
