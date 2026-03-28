---
name: weixin-reader
description: Read and extract readable content from WeChat Official Account articles (mp.weixin.qq.com). Use when user wants to fetch and parse WeChat articles that have anti-crawler protection. Handles JS-rendered pages via Camoufox browser fallback and precise content extraction.
---

# WeChat Article Reader

> v2 — Node.js + Camoufox 浏览器三层降级方案

## 快速使用

```bash
# ✅ 推荐：自动三层降级（Node → Camoufox → Python 精确提取）
python3 scripts/reader_v2.py "https://mp.weixin.qq.com/s/xxxxx"

# 保存到文件
python3 scripts/reader_v2.py "https://mp.weixin.qq.com/s/xxxxx" > article.txt

# JSON 输出（自动化场景）
python3 scripts/reader_v2.py "https://mp.weixin.qq.com/s/xxxxx" --json

# 指定输出目录（Camoufox 缓存）
python3 scripts/reader_v2.py "https://mp.weixin.qq.com/s/xxxxx" -o /tmp/my_articles

# 绕过 Node.js，直接用 Camoufox（调试用）
python3 scripts/reader_v2.py "https://mp.weixin.qq.com/s/xxxxx" --camoufox-only
```

## 工作原理（三层降级）

```
第1层：Node.js 快速路径
  └→ 多 UA 重试，抓取静态 HTML
  └→ 成功 + 非壳页 → 直接返回 ✅
  └→ 失败 / 壳页 → 进入第2层

第2层：Camoufox 浏览器渲染
  └→ 启动 headless 浏览器（绕过 JS 渲染）
  └→ 等待页面完全加载
  └→ 保存渲染后 HTML 到 debug/ 目录
  └→ 进入第3层

第3层：Python 精确提取
  └→ 正则匹配 js_content，截断到干扰元素之前
  └→ HTML entity 解码 + 标签清理
  └→ 去除赞赏/留言等干扰段落
  └→ 返回结构化结果 ✅
```

## 适用场景

| 场景 | 方案 | 说明 |
|------|------|------|
| 普通文章（静态 HTML）| Node.js | 毫秒级，不需要额外工具 |
| JS 渲染壳页（"轻触查看原文"）| Camoufox + Python | 约 30-60 秒 |
| 验证码拦截 | Camoufox `--no-headless` | 手动在浏览器窗口解决 |
| 批量抓取 | Camoufox（缓存 debug HTML）| 避免重复渲染 |

## 核心能力

- **多 UA 轮换**：iPhone Safari → Android WeChat → Desktop Chrome
- **JS 渲染绕过**：Camoufox headless 浏览器（不基于 Chromium，自带反检测）
- **精确截断**：正则到 `js_content` div 截止到干扰元素之前（赞赏/留言/二维码）
- **自动降级**：Node.js 失败自动切 Camoufox，不需要手动干预
- **调试支持**：`--camoufox-only` 跳过 Node.js，`-o` 指定输出目录保留 debug HTML

## 示例输出

```
# AI可以做梦了！！

原文链接: https://mp.weixin.qq.com/s/bBKCq88Hrqsz4qGjRQLJUw

---

小时候我一直觉得做梦是浪费时间。

长大后才知道，做梦是大脑最重要的后台任务——清理垃圾信息，把短期记忆整合进长期记忆...

---

提取方法: camoufox | 共 21 段
```

## 安装依赖

```bash
# Camoufox（可选，但强烈推荐）
cd /root/.agent-reach/tools/wechat-article-for-ai
pip3 install -r requirements.txt

# 确保 Python 版本
python3 --version  # 需要 3.10+
```

> **注意**：Camoufox 渲染需要约 30-60 秒，比 Node.js 慢很多。只有在 Node.js 拿到壳页时才自动降级，不需要手动选择。

## 故障排除

| 问题 | 原因 | 解决 |
|------|------|------|
| "⚠️ 检测到微信壳页" | JS 渲染内容拿不到 | 正常，v2 会自动切 Camoufox |
| Camoufox 超时 | 网络慢 / 页面复杂 | 增加 timeout 或重试 |
| 渲染后仍提取失败 | 正则未匹配到 js_content | 用 `--camoufox-only` 保留 debug HTML 分析 |
| 验证码拦截 | 短时间内访问太频繁 | 等几分钟再试 |

## 技术栈

- **Node.js**：快速静态抓取，多 UA 兼容
- **Camoufox**：Python headless 浏览器，专为反爬设计
- **Python 正则**：精确 js_content 提取，解决官方提取器 bug
- **无外部 API 依赖**：完全本地运行
