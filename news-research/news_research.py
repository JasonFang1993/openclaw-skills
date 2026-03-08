#!/usr/bin/env python3
"""
News Research Skill 主入口
整合所有模块，提供完整的新闻研究能力
"""

import sys
import json
import asyncio
import yaml
from pathlib import Path
from datetime import datetime

# 添加脚本目录到路径
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR / "scripts"))

from scripts.init_task import TaskInitializer
from scripts.dedup import DedupEngine
from scripts.ranker import RankingEngine
from scripts.formatter import ReportFormatter


class NewsResearcher:
    """新闻研究员 - 整合所有模块"""
    
    def __init__(self, skill_dir: str = None):
        if skill_dir is None:
            skill_dir = Path(__file__).parent.parent / "news-research"
        
        self.skill_dir = Path(skill_dir)
        self.config = self._load_config()
        
        # 初始化各模块
        self.initializer = TaskInitializer(str(self.skill_dir))
        self.dedup_engine = DedupEngine(self.config.get("dedup", {}))
        self.ranker = RankingEngine(self.config.get("ranking", {}))
        self.formatter = ReportFormatter(self.config.get("output", {}))
    
    def _load_config(self) -> dict:
        """加载配置"""
        config_path = self.skill_dir / "config" / "sources.yaml"
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    async def research(self, instruction: str) -> dict:
        """
        执行新闻研究任务
        
        Args:
            instruction: 用户指令，如 "研究今天的AI行业新闻"
        
        Returns:
            包含报告和统计信息的字典
        """
        print(f"\n{'='*60}")
        print(f"🔍 News Research 开始")
        print(f"   指令: {instruction}")
        print(f"{'='*60}\n")
        
        # Step 1: 初始化任务
        print("📋 Step 1: 初始化任务...")
        task = self.initializer.init_task(instruction)
        task_file = self.initializer.save_task(task)
        print(f"   任务ID: {task['id']}")
        print(f"   关键词: {task['keywords']}")
        print(f"   新闻源: {len(task['sources'])} 个")
        
        # Step 2: Ralph Loop 搜索
        print("\n🔍 Step 2: 执行Ralph Loop搜索...")
        from scripts.ralph_loop import RalphLoop
        
        loop = RalphLoop(task)
        task = loop.run()
        
        # 额外抓取36氪
        print("\n🔍 Step 2.1: 抓取36氪...")
        try:
            from scripts.kr36 import fetch_36kr_news
            kr36_news = fetch_36kr_news()
            if kr36_news:
                task["results"].extend(kr36_news)
                print(f"   36氪: 获取到 {len(kr36_news)} 条")
        except Exception as e:
            print(f"   36氪抓取失败: {e}")
        
        # 额外抓取其他中文源
        print("\n🔍 Step 2.2: 抓取其他中文源...")
        try:
            from scripts.chinese_news import fetch_chinese_news
            chinese_news = fetch_chinese_news()
            if chinese_news:
                task["results"].extend(chinese_news)
        except Exception as e:
            print(f"   中文源抓取失败: {e}")
        news_list = task.get("results", [])
        
        print(f"   抓取到: {len(news_list)} 条新闻")
        
        if not news_list:
            # 没有抓取到任何内容，返回空报告
            print("   ⚠️ 没有抓取到任何新闻")
            return {
                "success": False,
                "report": "# 抱歉，未能找到相关新闻\n\n请尝试其他关键词或时间范围。",
                "news_count": 0,
                "task_id": task["id"]
            }
        
        # Step 3: 去重
        print("\n🔄 Step 3: 去重处理...")
        news_list = self.dedup_engine.process(news_list, days=task.get("days", 1))
        
        # Step 4: 排序
        print("\n📊 Step 4: 排序处理...")
        news_list = self.ranker.process(
            news_list, 
            topic=task.get("topic"),
            max_news=task.get("max_news", 30)
        )
        
        # Step 5: 生成报告
        print("\n📝 Step 5: 生成报告...")
        result = self.formatter.process(
            news_list, 
            topic=task.get("topic", "AI"),
            output=True
        )
        
        print(f"\n{'='*60}")
        print(f"✅ News Research 完成")
        print(f"   新闻数: {result['news_count']}")
        print(f"   报告: {result.get('file_path', 'N/A')}")
        print(f"{'='*60}\n")
        
        return {
            "success": True,
            "report": result.get("report", ""),
            "news_count": result["news_count"],
            "topic": task.get("topic"),
            "task_id": task["id"],
            "file_path": result.get("file_path")
        }


# 导出供外部调用的接口
async def news_research(instruction: str) -> dict:
    """
    新闻研究主函数
    
    Usage:
        result = await news_research("研究今天的AI行业新闻")
        print(result["report"])
    """
    researcher = NewsResearcher()
    return await researcher.research(instruction)


# CLI入口
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        instruction = " ".join(sys.argv[1:])
    else:
        instruction = "研究今天的AI行业新闻"
    
    print(f"执行指令: {instruction}\n")
    
    result = asyncio.run(news_research(instruction))
    
    if result.get("success"):
        print("\n📰 报告预览:")
        print("-" * 40)
        print(result["report"][:1000])
        print("-" * 40)
        print(f"\n完整报告已保存到: {result.get('file_path')}")
    else:
        print(f"\n❌ 研究失败: {result.get('report')}")
