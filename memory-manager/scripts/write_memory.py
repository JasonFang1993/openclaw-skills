#!/usr/bin/env python3
"""
Memory Manager - 写入记忆
通过 MCP 适配器调用 obsidian_write_note
"""

import json
import sys

def write_memory(content, file_type="daily", tags=None):
    """
    写入新的记忆
    
    Args:
        content: 记忆内容
        file_type: 类型 (daily/project/knowledge)
        tags: 标签列表
    
    Returns:
        创建结果
    """
    # 根据类型确定文件路径
    file_map = {
        "daily": f"01-Memory/100-每日/{get_date()}.md",
        "project": "01-Memory/200-项目/",
        "knowledge": "01-Memory/300-知识/"
    }
    
    file_path = file_map.get(file_type, "01-Memory/100-每日/")
    
    return {
        "tool": "obsidian_write_note",
        "args": {
            "name": file_path,
            "content": content,
            "tags": tags or []
        }
    }

def get_date():
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: write_memory.py <content> [--type daily|project|knowledge] [--tags tag1,tag2]")
        sys.exit(1)
    
    content = sys.argv[1]
    file_type = "daily"
    tags = []
    
    # 简单解析参数
    for i, arg in enumerate(sys.argv):
        if arg == "--type" and i + 1 < len(sys.argv):
            file_type = sys.argv[i + 1]
        if arg == "--tags" and i + 1 < len(sys.argv):
            tags = sys.argv[i + 1].split(",")
    
    result = write_memory(content, file_type, tags)
    print(json.dumps(result, indent=2))
