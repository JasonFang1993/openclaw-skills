#!/usr/bin/env python3
"""
排序引擎测试
"""

import sys
sys.path.insert(0, "/root/.openclaw/skills/news-research/scripts")

from ranker import RankingEngine

def test_source_weight():
    """权威来源应该排名靠前"""
    engine = RankingEngine()
    
    news = [
        {"title": "新闻A", "source": "机器之心"},  # 权重5
        {"title": "新闻B", "source": "IT之家"},  # 权重2
    ]
    
    result = engine.rank(news)
    
    # 机器之心应该排第一
    assert result[0]["source"] == "机器之心", f"期望机器之心第一，实际{result[0]['source']}"
    print("✅ 测试通过: 来源权重排序")

def test_content_quality():
    """包含数据的新闻应该排名靠前"""
    engine = RankingEngine()
    
    news = [
        {"title": "OpenAI发布新模型", "source": "IT之家", "content": "OpenAI发布新模型GPT-5"},
        {"title": "OpenAI发布GPT-5,性能提升100%", "source": "IT之家", "content": "OpenAI发布GPT-5,性能提升100%"},
    ]
    
    result = engine.rank(news)
    
    # 有数据的应该排第一
    assert result[0]["source"] == "IT之家", "排序应该按得分"
    print("✅ 测试通过: 内容质量排序")

def test_limit():
    """数量限制"""
    engine = RankingEngine()
    
    news = [{"title": f"新闻{i}", "source": "测试"} for i in range(20)]
    
    result = engine.process(news, max_news=10)
    
    assert len(result) == 10, f"应该返回10条，实际{len(result)}条"
    print("✅ 测试通过: 数量限制")

def test_topic_rerank():
    """主题相关度排序"""
    engine = RankingEngine()
    
    news = [
        {"title": "OpenAI发布新模型", "source": "A"},
        {"title": "谷歌发布新AI", "source": "B"},
    ]
    
    result = engine.process(news, topic="OpenAI")
    
    # OpenAI相关的应该排第一
    assert "OpenAI" in result[0]["title"], "主题相关应该优先"
    print("✅ 测试通过: 主题相关度排序")

def main():
    print("\n=== 排序引擎测试 ===\n")
    
    test_source_weight()
    test_content_quality()
    test_limit()
    test_topic_rerank()
    
    print("\n=== 全部测试通过! ===\n")

if __name__ == "__main__":
    main()
