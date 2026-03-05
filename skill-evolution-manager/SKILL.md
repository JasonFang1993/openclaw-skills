---
name: skill-evolution-manager
description: 基于用户反馈和会话经验持续改进 Skills。分析 skill 表现，提取经验，将最佳实践写入 SKILL.md。
license: MIT
github_url: https://github.com/KKKKhazix/Khazix-Skills
github_hash: fe15fea6cf7ac216027d11c2c64e87b462cc0427
version: 1.0.0
created_at: 2026-02-25
---

# Skill Evolution Manager

基于用户反馈和会话经验持续改进 Skills。

## 核心功能

1. **会话回顾 (Session Review)**: 分析 skill 在对话中的表现
2. **经验提取 (Experience Extraction)**: 将反馈转换为结构化 JSON
3. **智能整合 (Smart Stitching)**: 将最佳实践持久化到 SKILL.md
4. **批量重整 (Align All)**: 批量更新所有 skills

## 使用方式

**触发指令**: 
- `/evolve`
- "Save this experience to the skill"

### 保存经验

在对话中，如果某个 skill 的使用效果很好或有问题，可以告诉 agent 保存经验：

```
"Save this experience to the skill: 当用户要求生成 PDF 时，使用 reportlab 比 weasyprint 更稳定"
```

### 手动使用脚本

```bash
# 合并经验数据
python3 scripts/merge_evolution.py <skill-dir> <feedback-json>

# 智能整合到 SKILL.md
python3 scripts.py <skill-dir/smart_stitch>

# 批量重整所有 skills
python3 scripts/align_all.py ~/.openclaw/workspace/skills
```

## 经验数据格式

```json
{
  "skill_name": "example-skill",
  "experiences": [
    {
      "situation": "用户要求生成 PDF 报告",
      "action": "使用 reportlab 生成",
      "result": "成功生成专业格式报告",
      "preference": "优先使用 reportlab 而非 weasyprint"
    }
  ],
  "best_practices": [
    "始终检查依赖是否安装",
    "使用 JSON 输出便于解析"
  ],
  "custom_prompts": [
    "当用户要求生成报告时，先询问格式偏好"
  ]
}
```

## 工作流程

1. **Review (回顾)**: Agent 分析对话中什么有效/无效
2. **Extract (提取)**: 创建结构化 JSON（偏好、修复、自定义提示）
3. **Persist (持久化)**: 合并到 evolution.json
4. **Stitch (整合)**: 更新 SKILL.md 中的最佳实践

## 脚本说明

| 脚本 | 功能 |
|------|------|
| `merge_evolution.py` | 增量合并新经验数据到 evolution.json |
| `smart_stitch.py` | 生成/更新 SKILL.md 中的最佳实践部分 |
| `align_all.py` | 批量重整所有 skills 的最佳实践 |

## 前置依赖

```bash
# 安装 Python 依赖
pip install pyyaml
```

## 使用场景

- **优化 prompt**: 根据用户偏好调整 skill 行为
- **记录技巧**: 保存成功的使用模式
- **避免错误**: 记录失败的尝试和解决方案
- **知识传承**: 让后续会话也能受益于经验积累
