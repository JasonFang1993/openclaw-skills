#!/usr/bin/env python3
"""
集成测试：News Research Skill
"""

import sys
import os

# 添加脚本目录
script_dir = os.path.join(os.path.dirname(__file__), "..", "scripts")
sys.path.insert(0, script_dir)

from init_task import TaskInitializer
from dedup import DedupEngine
from ranker import RankingEngine
from formatter import ReportFormatter

def test_init():
    """测试任务初始化"""
    print("\n=== 测试 1: 任务初始化 ===")
    initializer = TaskInitializer()
    task = initializer.init_task("研究今天的AI行业新闻")
    
    assert task["topic"] == "今天的ai行业新闻", f"主题解析错误: {task['topic']}"
    assert len(task["sources"]) > 0, "没有加载新闻源"
    assert len(task["keywords"]) > 0, "没有生成关键词"
    
    print(f"✅ 主题: {task['topic']}")
    print(f"✅ 关键词: {task['keywords'][:3]}...")
    print(f"✅ 新闻源: {len(task['sources'])} 个")

def test_dedup():
    """测试去重引擎"""
    print("\n=== 测试 2: 去重引擎 ===")
    engine = DedupEngine()
    
    news = [
        {"title": "OpenAI releases GPT-5", "source": "Reuters"},
        {"title": "OpenAI releases GPT-5", "source": "TechCrunch"},
        {"title": "Google announces new AI features", "source": "Wired"},
        {"title": "Old news from 2024", "source": "Test", "url": "https://example.com/2024-01-01"},
    ]
    
    result = engine.process(news, days=1)
    
    assert len(result) >= 2, f"去重后应该>=2条，实际{len(result)}条"
    print(f"✅ 去重测试通过: {len(news)} -> {len(result)} 条")

def test_ranker():
    """测试排序引擎"""
    print("\n=== 测试 3: 排序引擎 ===")
    engine = RankingEngine()
    
    news = [
        {"title": "Tech news", "source": "Reuters"},
        {"title": "Another tech", "source": "Test"},
    ]
    
    result = engine.process(news, topic="AI")
    
    assert len(result) == 2, f"排序后应该有2条"
    assert result[0]["source"] == "Reuters", "Reuters应该排第一"
    print(f"✅ 排序测试通过")

def test_formatter():
    """测试报告生成"""
    print("\n=== 测试 4: 报告生成 ===")
    formatter = ReportFormatter()
    
    news = [
        {"title": "OpenAI releases GPT-5", "source": "Reuters", "url": "https://reuters.com/1"},
        {"title": "Google announces AI features", "source": "Wired", "url": "https://wired.com/2"},
    ]
    
    result = formatter.process(news, topic="AI", output=False)
    
    assert "report" in result, "没有生成报告"
    assert "OpenAI" in result["report"], "报告内容缺失"
    assert len(result["report"]) > 100, "报告内容太短"
    print(f"✅ 报告生成测试通过")
    print(f"   报告长度: {len(result['report'])} 字符")

def test_workflow():
    """测试工作流"""
    print("\n=== 测试 5: 工作流 ===")
    from workflow import get_search_prompt, get_report_prompt
    
    search_prompt = get_search_prompt("AI")
    assert len(search_prompt) > 100, "搜索提示词太短"
    print(f"✅ 搜索提示词: {len(search_prompt)} 字符")
    
    report_prompt = get_report_prompt("[test]", "AI")
    assert len(report_prompt) > 100, "报告提示词太短"
    print(f"✅ 报告提示词: {len(report_prompt)} 字符")

def main():
    print("\n" + "="*50)
    print("News Research Skill 集成测试")
    print("="*50)
    
    try:
        test_init()
        test_dedup()
        test_ranker()
        test_formatter()
        test_workflow()
        
        print("\n" + "="*50)
        print("✅ 所有测试通过!")
        print("="*50)
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
