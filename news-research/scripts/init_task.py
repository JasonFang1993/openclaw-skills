#!/usr/bin/env python3
"""
任务初始化模块
负责解析用户指令，确定搜索策略，创建任务追踪文件
"""

import json
import os
import yaml
from datetime import datetime, timedelta
from pathlib import Path

class TaskInitializer:
    def __init__(self, skill_dir: str = None):
        if skill_dir is None:
            # 获取正确的skill目录路径
            current_file = Path(__file__).resolve()
            skill_dir = current_file.parent.parent
        self.skill_dir = Path(skill_dir)
        self.config_dir = self.skill_dir / "config"
        
    def load_config(self) -> dict:
        """加载配置文件"""
        config_path = self.config_dir / "sources.yaml"
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def parse_instruction(self, instruction: str) -> dict:
        """解析用户指令"""
        instruction = instruction.lower().strip()
        
        # 解析主题
        topic = "AI"
        if "研究" in instruction:
            # 提取研究主题
            parts = instruction.replace("研究", "").strip()
            if parts:
                topic = parts
        
        # 解析时间范围
        days = 1
        if "3天" in instruction or "三天" in instruction:
            days = 3
        elif "7天" in instruction or "一周" in instruction:
            days = 7
        
        # 解析最大新闻数
        max_news = 30
        if "10条" in instruction or "10条" in instruction:
            max_news = 10
        elif "20条" in instruction or "20条" in instruction:
            max_news = 20
        elif "50条" in instruction:
            max_news = 50
            
        return {
            "topic": topic,
            "days": days,
            "max_news": max_news,
            "timestamp": datetime.now().isoformat()
        }
    
    def get_search_keywords(self, topic: str, config: dict) -> list:
        """获取搜索关键词列表"""
        keywords = [topic]
        
        # 添加默认关键词
        default_kw = config.get("search", {}).get("default_keywords", [])
        
        # 如果是AI相关，添加扩展词
        if "ai" in topic.lower() or "人工智能" in topic:
            keywords.extend(default_kw[:5])  # 取前5个
        
        return list(set(keywords))  # 去重
    
    def get_sources_by_priority(self, config: dict) -> list:
        """按优先级排序的新闻源"""
        sources = config.get("sources", [])
        return sorted(sources, key=lambda x: x.get("priority", 10))
    
    def init_task(self, instruction: str) -> dict:
        """初始化任务"""
        # 加载配置
        config = self.load_config()
        
        # 解析指令
        parsed = self.parse_instruction(instruction)
        
        # 获取搜索关键词
        keywords = self.get_search_keywords(parsed["topic"], config)
        
        # 获取新闻源（按优先级排序）
        sources = self.get_sources_by_priority(config)
        
        # 构建任务对象
        task = {
            "id": f"news_research_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "instruction": instruction,
            "topic": parsed["topic"],
            "keywords": keywords,
            "days": parsed["days"],
            "max_news": parsed["max_news"],
            "sources": sources,
            "status": "initialized",
            "created_at": datetime.now().isoformat(),
            "progress": {
                "searched": [],
                "pending": [s["name"] for s in sources],
                "done": [],
                "failed": []
            },
            "results": []
        }
        
        return task
    
    def save_task(self, task: dict, output_dir: str = None) -> str:
        """保存任务到文件"""
        if output_dir is None:
            output_dir = Path.home() / ".openclaw" / "workspace" / "kbase" / "news"
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        task_file = output_path / f"task_{task['id']}.json"
        with open(task_file, 'w', encoding='utf-8') as f:
            json.dump(task, f, ensure_ascii=False, indent=2)
        
        return str(task_file)


def main():
    """测试入口"""
    initializer = TaskInitializer()
    
    # 测试用例
    test_instructions = [
        "研究今天的AI行业新闻",
        "研究一下OpenAI的最新动态",
        "研究过去3天的AI融资新闻"
    ]
    
    for instruction in test_instructions:
        print(f"\n{'='*50}")
        print(f"指令: {instruction}")
        print('='*50)
        
        task = initializer.init_task(instruction)
        print(f"任务ID: {task['id']}")
        print(f"主题: {task['topic']}")
        print(f"关键词: {task['keywords']}")
        print(f"新闻源数量: {len(task['sources'])}")
        print(f"前3个源: {[s['name'] for s in task['sources'][:3]]}")
        
        # 保存任务
        task_file = initializer.save_task(task)
        print(f"任务文件: {task_file}")


if __name__ == "__main__":
    main()
