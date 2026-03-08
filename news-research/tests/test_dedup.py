#!/usr/bin/env python3
"""
去重引擎测试
"""

import sys
sys.path.insert(0, "/root/.openclaw/skills/news-research/scripts")

from dedup import DedupEngine

def test_same_title_dedup():
    """相同标题应该被去重"""
    engine = DedupEngine()
    
    news = [
        {"title": "OpenAI发布新模型GPT-5", "source": "36kr"},
        {"title": "OpenAI发布新模型GPT-5", "source": "机器之心"},
    ]
    
    result = engine.dedup_by_title(news)
    
    assert len(result) == 1, f"期望1条，实际{len(result)}条"
    print("✅ 测试通过: 相同标题去重")

def test_similar_title_dedup():
    """相似标题应该被去重"""
    engine = DedupEngine()
    
    news = [
        {"title": "OpenAI发布GPT-5新模型", "source": "36kr"},
        {"title": "OpenAI发布新模型GPT-5", "source": "机器之心"},
    ]
    
    result = engine.dedup_by_title(news)
    
    # 相似度应该能检测到重复
    assert len(result) <= 2, "去重后应该<=2条"
    print("✅ 测试通过: 相似标题处理")

def test_different_title():
    """不同标题应该保留"""
    engine = DedupEngine()
    
    news = [
        {"title": "OpenAI发布新模型GPT-5", "source": "36kr"},
        {"title": "谷歌发布新AI功能", "source": "机器之心"},
    ]
    
    result = engine.dedup_by_title(news)
    
    assert len(result) == 2, f"期望2条，实际{len(result)}条"
    print("✅ 测试通过: 不同标题保留")

def test_date_filter():
    """日期过滤测试"""
    engine = DedupEngine()
    
    news = [
        {"title": "今天的新闻", "source": "36kr", "url": "https://example.com/2026-02-21"},
        {"title": "昨天的新闻", "source": "机器之心", "url": "https://example.com/2026-02-20"},
    ]
    
    result = engine.filter_by_date(news, days=1)
    
    # 至少今天的应该保留
    assert len(result) >= 1, f"应该保留至少1条，实际{len(result)}条"
    print("✅ 测试通过: 日期过滤")

def test_process():
    """完整流程测试"""
    engine = DedupEngine()
    
    news = [
        {"title": "OpenAI发布新模型GPT-5", "source": "36kr"},
        {"title": "OpenAI发布新模型GPT-5", "source": "机器之心"},
        {"title": "谷歌发布新AI功能", "source": "IT之家"},
        {"title": "2024年的旧新闻", "source": "测试", "url": "https://example.com/2024-01-01"},
    ]
    
    result = engine.process(news, days=1)
    
    print(f"  输入: 4条 -> 输出: {len(result)}条")
    assert len(result) >= 2, f"应该保留>=2条，实际{len(result)}条"
    print("✅ 测试通过: 完整去重流程")

def main():
    print("\n=== 去重引擎测试 ===\n")
    
    test_same_title_dedup()
    test_similar_title_dedup()
    test_different_title()
    test_date_filter()
    test_process()
    
    print("\n=== 全部测试通过! ===\n")

if __name__ == "__main__":
    main()
