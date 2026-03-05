#!/usr/bin/env python3
"""
Memory Manager - 搜索记忆
通过 MCP 适配器调用 obsidian_search_notes
"""

import json
import sys

def search_memory(query):
    """
    搜索记忆
    
    Args:
        query: 搜索关键词
    
    Returns:
        搜索结果
    """
    return {
        "tool": "obsidian_search_notes",
        "args": {
            "path": "/data/vault",
            "query": query
        }
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: search_memory.py <query>")
        sys.exit(1)
    
    query = sys.argv[1]
    result = search_memory(query)
    print(json.dumps(result, indent=2))
