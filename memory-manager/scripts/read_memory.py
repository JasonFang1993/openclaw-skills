#!/usr/bin/env python3
"""
Memory Manager - 读取记忆
通过 MCP 适配器调用 obsidian_read_note
"""

import json
import sys

def read_memory(file_path):
    """
    读取指定文件的内容
    
    Args:
        file_path: 文件路径（相对于 vault 根目录）
    
    Returns:
        文件内容
    """
    # 注意：实际调用通过 OpenClaw 的 MCP 工具执行
    # 这里只是定义接口
    return {
        "tool": "obsidian_read_note",
        "args": {
            "name": file_path
        }
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: read_memory.py <file_path>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    result = read_memory(file_path)
    print(json.dumps(result, indent=2))
