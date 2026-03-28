#!/usr/bin/env python3
"""
WeChat Article Reader v2 — Camoufox 降级 + Python 精确提取

使用逻辑:
1. 先试 Node.js reader.js (快速路径)
2. 如果拿到壳页，自动切换 Camoufox 浏览器渲染
3. Camoufox 把渲染后的 HTML 存到 debug/ 目录
4. Python 从 debug HTML 用精确正则提取正文（解决官方提取器的 bug）
"""

import re
import os
import sys
import json
import subprocess
import shutil
import argparse
from pathlib import Path


# ============================================================================
# 提取核心
# ============================================================================

def decode_html(text=''):
    if not text:
        return ''
    text = text.replace('&nbsp;', ' ')
    text = text.replace('&lt;', '<').replace('&gt;', '>')
    text = text.replace('&amp;', '&').replace('&quot;', '"')
    text = text.replace('&#39;', "'").replace('&#x27;', "'")
    text = re.sub(r'&#x([0-9a-fA-F]+);',
                   lambda m: chr(int(m.group(1), 16)) if len(m.group(1)) <= 6 else m.group(0), text)
    text = re.sub(r'&#(\d+);',
                   lambda m: chr(int(m.group(1))) if int(m.group(1)) < 65536 else m.group(0), text)
    return text


def html_to_text(html=''):
    text = re.sub(r'<script[^>]*>[\s\S]*?<\/script>', '', html)
    text = re.sub(r'<style[^>]*>[\s\S]*?<\/style>', '', text)
    text = re.sub(r'<!--[\s\S]*?-->', '', text)
    text = re.sub(r'<\s*br\s*\/?>', '\n', text)
    text = re.sub(r'<\/p>', '\n', text)
    text = re.sub(r'<\/div>', '\n', text)
    text = re.sub(r'<\/h[1-6]>', '\n\n', text)
    text = re.sub(r'<h[1-6][^>]*>', '\n\n### ', text)
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'\r', '', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return decode_html(text).strip()


def extract_from_html(html, url):
    """从已渲染 HTML 中精确提取文章内容"""

    # ---- 标题 ----
    title = None
    for pattern in [
        r'<title[^>]*>([^<]+)</title>',
        r'var\s+msg_title\s*=\s*"([^"]+)"',
        r'var\s+msg_title\s*=\s*\'([^\']+)\'',
    ]:
        m = re.search(pattern, html)
        if m:
            raw = m.group(1).strip()
            if raw and raw not in ('微信公众平台', 'javascript'):
                title = decode_html(raw.replace('\\n', '').replace('\\/', '/'))
                break

    if not title:
        og = re.search(r'og:title["\'].*?content="([^"]+)"', html)
        if og:
            title = decode_html(og.group(1).split('\n')[0])

    # ---- js_content 精确提取 ----
    content_html = None
    for pattern in [
        # 精确截断到干扰元素
        r'id="js_content"[^>]*>([\s\S]*?)(?=<div[^>]*id="(?:js_tag|js_read_area3|meta_content|js_toobar3|js_iframetest|js_pc_qr_code|timestamp|source_created_time|profile_type|author|profile_type)["\'])',
        # 备选：到倒数第二个div
        r'id="js_content"[^>]*>([\s\S]*?)<\/div>\s*<\/div>\s*<script',
        # 备选：rich_media_content
        r'class="rich_media_content[^"]*"[^>]*>([\s\S]*?)<div[^>]*id="js_',
    ]:
        m = re.search(pattern, html)
        if m and len(m.group(1)) > 300:
            content_html = m.group(1)
            break

    paragraphs = []
    if content_html:
        text = html_to_text(content_html)
        skip_phrases = {
            '微信扫一扫赞赏作者', 'Like the Author', '写留言', 'Send Message',
            'Name cleared', 'Other Amount', '原文链接', '相关阅读',
        }
        for line in text.split('\n'):
            line = line.strip()
            if (10 < len(line) < 5000
                    and not re.match(r'^\d+$', line)
                    and not re.match(r'^https?://', line)
                    and not any(phrase in line for phrase in skip_phrases)
                    and not re.match(r'^\d+年\d+月\d+日', line)):
                paragraphs.append(line)

        # 去重标题 echo
        if paragraphs and title and paragraphs[0] == title:
            paragraphs = paragraphs[1:]

    return {
        'title': title or 'Unknown',
        'paragraphs': paragraphs[:100],
        'url': url,
        'paragraphCount': len(paragraphs),
        'rawLength': len(html),
    }


# ============================================================================
# 抓取层
# ============================================================================

CAMOUFOX_TOOL_DIR = Path('/root/.agent-reach/tools/wechat-article-for-ai')


def try_node_js(url, timeout=20):
    """快速路径：Node.js"""
    try:
        script = Path(__file__).parent / 'reader.js'
        result = subprocess.run(
            ['node', str(script), '--quiet', url],
            capture_output=True, text=True, timeout=timeout,
            env={**os.environ, 'NODE_PATH': str(Path(__file__).parent / '..' / '..' / '..' / '..' / '.nvm' / 'versions' / 'node' / 'v22.22.0' / 'lib' / 'node_modules')}
        )
        if result.returncode == 0 and '⚠️ 检测到微信壳页' not in result.stdout:
            return result.stdout, 'node'
    except Exception:
        pass
    return None, None


def try_node_js_direct(url, timeout=20):
    """直接用node调reader.js"""
    try:
        script = Path(__file__).parent / 'reader.js'
        result = subprocess.run(
            ['node', str(script), '--quiet', url],
            capture_output=True, text=True, timeout=timeout
        )
        if result.returncode == 0 and '⚠️ 检测到微信壳页' not in result.stdout:
            return result.stdout, 'node'
        if result.returncode == 0:
            # 仍然拿到了内容，只是带警告
            return result.stdout, 'node-warn'
    except Exception:
        pass
    return None, None


def fetch_with_camoufox(url, output_dir):
    """Camoufox 降级：调用外部工具 + 解析 debug HTML"""
    if not CAMOUFOX_TOOL_DIR.exists():
        raise RuntimeError(
            f"Camoufox tool not found at {CAMOUFOX_TOOL_DIR}. "
            "请先安装: cd /root/.agent-reach/tools/wechat-article-for-ai && pip install -r requirements.txt"
        )

    # 清理旧debug
    debug_dir = Path(output_dir) / 'debug'
    debug_dir.mkdir(parents=True, exist_ok=True)

    result = subprocess.run(
        ['python3', str(CAMOUFOX_TOOL_DIR / 'main.py'),
         url, '-o', output_dir, '--no-images', '-v'],
        capture_output=True, text=True, timeout=90
    )

    # 查找 debug HTML
    debug_files = list(debug_dir.glob('*.html'))
    if debug_files:
        with open(debug_files[0], encoding='utf-8') as f:
            return f.read(), 'camoufox'

    raise RuntimeError(f"Camoufox failed: {result.stderr[:500]}")


def fetch_with_requests(url, timeout=15):
    """最后兜底：用 requests 拿原始 HTML"""
    import requests
    ua = 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1'
    r = requests.get(url, headers={'User-Agent': ua}, timeout=timeout)
    r.encoding = 'utf-8'
    return r.text, 'requests'


# ============================================================================
# 主流程
# ============================================================================

def main():
    parser = argparse.ArgumentParser(description='WeChat Article Reader v2')
    parser.add_argument('url', help='WeChat article URL')
    parser.add_argument('--output', '-o', default='/tmp/wechat_v2', help='Camoufox output dir')
    parser.add_argument('--json', action='store_true')
    parser.add_argument('--camoufox-only', action='store_true', help='Skip Node.js, use Camoufox directly')
    args = parser.parse_args()

    url = args.url
    html = None
    method = None

    if not args.camoufox_only:
        # 1. 快速路径：Node.js
        content, method = try_node_js_direct(url)
        if method == 'node' and content:
            html = content
        elif method == 'node-warn' and content:
            # Node拿到了但带警告，尝试从内容重建
            # 这个路径Node无法直接返回结构化HTML，继续用Camoufox
            pass

        # 2. Camoufox 降级
        if not html or method == 'node-warn':
            print("Node.js 拿到壳页，切换 Camoufox 渲染...", file=sys.stderr)
            try:
                html, method = fetch_with_camoufox(url, args.output)
            except Exception as e:
                print(f"Camoufox 失败: {e}", file=sys.stderr)
                # 3. 最后兜底
                print("尝试 requests 兜底...", file=sys.stderr)
                html, method = fetch_with_requests(url)
    else:
        try:
            html, method = fetch_with_camoufox(url, args.output)
        except Exception as e:
            print(f"Camoufox 失败: {e}", file=sys.stderr)
            sys.exit(1)

    # 用 Python 提取
    result = extract_from_html(html, url)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    if result['paragraphCount'] == 0:
        print(f"⚠️ 提取失败，HTML 长度 {len(html)} 字节但无法解析正文", file=sys.stderr)
        sys.exit(1)

    output = f"# {result['title']}\n\n"
    output += f"原文链接: {url}\n\n"
    output += "---\n\n"
    for p in result['paragraphs']:
        output += p + "\n\n"
    output += f"---\n提取方法: {method} | 共 {result['paragraphCount']} 段\n"
    print(output)


if __name__ == '__main__':
    main()
