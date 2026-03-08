#!/usr/bin/env node

/**
 * WeChat Article Reader (hardened)
 * - Multi-UA retries
 * - Better metadata/title extraction
 * - Shell-page detection ("轻触查看原文")
 * - Fallback extraction from og:title / meta content when body is blocked
 */

const https = require('https');
const http = require('http');

const USER_AGENTS = [
  // iPhone Safari
  'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1',
  // WeChat Android WebView-ish
  'Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/120.0.0.0 Mobile Safari/537.36 MicroMessenger/8.0.47.2560(0x28002F37) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN',
  // Desktop Chrome
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
];

function decodeHtmlEntities(text = '') {
  return text
    .replace(/&nbsp;/g, ' ')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&amp;/g, '&')
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/&#x([0-9a-fA-F]+);/g, (_, hex) => {
      try {
        return String.fromCodePoint(parseInt(hex, 16));
      } catch {
        return _;
      }
    })
    .replace(/&#(\d+);/g, (_, dec) => {
      try {
        return String.fromCodePoint(parseInt(dec, 10));
      } catch {
        return _;
      }
    });
}

function htmlToText(html = '') {
  return decodeHtmlEntities(
    html
      .replace(/<script[^>]*>[\s\S]*?<\/script>/gi, '')
      .replace(/<style[^>]*>[\s\S]*?<\/style>/gi, '')
      .replace(/<!--[\s\S]*?-->/g, '')
      .replace(/<\s*br\s*\/?>/gi, '\n')
      .replace(/<\/p>/gi, '\n')
      .replace(/<\/div>/gi, '\n')
      .replace(/<\/h[1-6]>/gi, '\n\n')
      .replace(/<h[1-6][^>]*>/gi, '\n\n### ')
      .replace(/<[^>]+>/g, '')
      .replace(/\u00a0/g, ' ')
      .replace(/\r/g, '')
      .replace(/\n{3,}/g, '\n\n')
  ).trim();
}

function normalizeBackslashEscapes(text = '') {
  return text
    .replace(/\\n/g, '\n')
    .replace(/\\r/g, '')
    .replace(/\\t/g, '\t')
    .replace(/\\\//g, '/');
}

function extractMetaContent(html, attr, value, contentAttr = 'content') {
  const re = new RegExp(
    `<meta[^>]*${attr}=["']${value}["'][^>]*${contentAttr}=["']([^"']+)["'][^>]*>|<meta[^>]*${contentAttr}=["']([^"']+)["'][^>]*${attr}=["']${value}["'][^>]*>`,
    'i'
  );
  const m = html.match(re);
  return normalizeBackslashEscapes(decodeHtmlEntities((m && (m[1] || m[2])) || '')).trim();
}

function extractVarString(html, varName) {
  const reSingle = new RegExp(`var\\s+${varName}\\s*=\\s*'([\\s\\S]*?)';`);
  const reDouble = new RegExp(`var\\s+${varName}\\s*=\\s*"([\\s\\S]*?)";`);
  const m = html.match(reSingle) || html.match(reDouble);
  return normalizeBackslashEscapes(decodeHtmlEntities((m && m[1]) || '')).trim();
}

function normalizeParagraphs(text) {
  return text
    .split('\n')
    .map((line) => line.trim())
    .filter((line) => line.length > 10)
    .filter((line) => line.length < 5000)
    .filter((line) => !/^\d+$/.test(line))
    .filter((line) => !/^https?:\/\//i.test(line))
    .filter((line) => !/^(微信扫一扫可打开此内容|向上滑动看下一个|轻触查看原文)$/i.test(line));
}

function detectShellPage(html, paragraphs) {
  const markers = [
    '轻触查看原文',
    'wx_expand_article_placeholder',
    '微信扫一扫可打开此内容',
  ];
  const hitMarker = markers.some((m) => html.includes(m));
  const tooShort = paragraphs.length <= 2;
  return hitMarker && tooShort;
}

function extractMainContentHtml(html) {
  const patterns = [
    /<div[^>]*id=["']js_content["'][^>]*>([\s\S]*?)<div[^>]*id=["'](?:js_tags|js_read_area3|meta_content|js_toobar3|js_iframetest)["']/i,
    /<div[^>]*id=["']js_content["'][^>]*>([\s\S]*?)<\/div>\s*<\/div>\s*<script/i,
    /<div[^>]*class=["'][^"']*rich_media_content[^"']*["'][^>]*>([\s\S]*?)<\/div>/i,
    /<section[^>]*id=["']js_article["'][^>]*>([\s\S]*?)<\/section>/i,
  ];

  for (const p of patterns) {
    const m = html.match(p);
    if (m && m[1] && m[1].length > 300) return m[1];
  }
  return '';
}

function extractContent(html, url) {
  const titleFromTitleTag = decodeHtmlEntities((html.match(/<title[^>]*>([\s\S]*?)<\/title>/i) || [])[1] || '').trim();
  const titleFromOg = extractMetaContent(html, 'property', 'og:title');
  const titleFromVar = extractVarString(html, 'msg_title');
  let title = [titleFromTitleTag, titleFromOg, titleFromVar].find((x) => x && x.length > 0) || 'Unknown Title';
  // Some shell pages put full article into og:title. Keep title readable.
  if (title.includes('\n') || title.length > 120) {
    title = title.split('\n').map((x) => x.trim()).find(Boolean) || title.slice(0, 120);
  }

  const description =
    extractMetaContent(html, 'name', 'description') ||
    extractMetaContent(html, 'property', 'og:description') ||
    extractVarString(html, 'msg_desc') ||
    '';

  const contentHtml = extractMainContentHtml(html);
  const textFromContent = htmlToText(contentHtml || html);
  let paragraphs = normalizeParagraphs(textFromContent).slice(0, 300);

  const shellPage = detectShellPage(html, paragraphs);
  let fallbackUsed = false;

  if (shellPage) {
    // Fallback: og:title often carries full text for blocked pages
    const ogTitle = extractMetaContent(html, 'property', 'og:title');
    const ogDesc = extractMetaContent(html, 'property', 'og:description');
    const altText = [ogTitle, ogDesc].filter(Boolean).join('\n\n');
    const fallbackParas = normalizeParagraphs(altText);
    if (fallbackParas.length > paragraphs.length) {
      paragraphs = fallbackParas.slice(0, 300);
      fallbackUsed = true;
    }
  }

  // De-duplicate title echoed as first paragraph
  if (paragraphs.length > 0 && paragraphs[0] === title) {
    paragraphs = paragraphs.slice(1);
  }

  return {
    title,
    description,
    url,
    paragraphs,
    rawLength: html.length,
    extractedLength: textFromContent.length,
    paragraphCount: paragraphs.length,
    shellPage,
    fallbackUsed,
  };
}

function fetchOnce(url, userAgent) {
  return new Promise((resolve, reject) => {
    const urlObj = new URL(url);
    const isHttps = urlObj.protocol === 'https:';

    const options = {
      hostname: urlObj.hostname,
      path: urlObj.pathname + urlObj.search,
      method: 'GET',
      headers: {
        'User-Agent': userAgent,
        Referer: process.env.WEIXIN_READER_REFERER || 'https://mp.weixin.qq.com/',
        Accept: 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'no-cache',
      },
    };

    const client = isHttps ? https : http;
    const req = client.request(options, (res) => {
      // Follow redirect
      if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
        const nextUrl = new URL(res.headers.location, url).toString();
        resolve(fetchOnce(nextUrl, userAgent));
        return;
      }

      let data = '';
      res.on('data', (chunk) => {
        data += chunk;
      });
      res.on('end', () => {
        if (res.statusCode !== 200) {
          reject(new Error(`HTTP ${res.statusCode}: ${res.statusMessage}`));
          return;
        }
        resolve({ html: data, finalUrl: url });
      });
    });

    req.on('error', reject);
    req.setTimeout(30000, () => {
      req.destroy();
      reject(new Error('Request timeout'));
    });
    req.end();
  });
}

async function fetchWeChatArticle(url) {
  const customUA = process.env.WEIXIN_READER_UA;
  const uas = customUA ? [customUA, ...USER_AGENTS] : USER_AGENTS;

  console.log(`Fetching: ${url}`);

  let lastError = null;
  let best = null;

  for (const ua of uas) {
    try {
      console.log(`Trying User-Agent: ${ua}`);
      const { html } = await fetchOnce(url, ua);
      const parsed = extractContent(html, url);

      if (!best || parsed.paragraphCount > best.paragraphCount) {
        best = parsed;
      }

      // Good enough -> stop early
      if (!parsed.shellPage && parsed.paragraphCount >= 5) {
        return parsed;
      }
    } catch (err) {
      lastError = err;
    }
  }

  if (best) return best;
  throw lastError || new Error('Failed to fetch article');
}

function formatOutput(data, options = {}) {
  let output = '';

  if (options.title !== false) {
    output += `# ${data.title}\n\n`;
  }

  if (data.description) {
    output += `> ${data.description}\n\n`;
  }

  output += `原文链接: ${data.url}\n\n`;
  output += `---\n\n`;

  if (data.shellPage) {
    output += `⚠️ 检测到微信壳页（可能受平台限制，正文未完全直出）。\n`;
    if (data.fallbackUsed) {
      output += `已启用元信息兜底提取（og:title / og:description）。\n\n`;
    } else {
      output += `未找到足够正文，建议：在微信内“复制全文”或发送正文截图。\n\n`;
    }
  }

  if (options.content !== false) {
    data.paragraphs.forEach((p) => {
      output += `${p}\n\n`;
    });
  }

  output += `---\n`;
  output += `共提取 ${data.paragraphCount} 段内容，原始 HTML ${(data.rawLength / 1024 / 1024).toFixed(2)} MB，提取文本 ${(data.extractedLength / 1024).toFixed(1)} KB\n`;

  return output;
}

// CLI
async function main() {
  const args = process.argv.slice(2);
  const jsonMode = args.includes('--json');
  const quiet = args.includes('--quiet');
  const url = args.find((a) => !a.startsWith('--'));

  if (!url) {
    console.error('Usage: node reader.js [--json] [--quiet] <wechat-article-url>');
    console.error('Example: node reader.js --json https://mp.weixin.qq.com/s/xxxxx');
    process.exit(1);
  }

  const originalLog = console.log;
  if (quiet || jsonMode) {
    console.log = (..._args) => {};
  }

  try {
    const data = await fetchWeChatArticle(url);
    if (jsonMode) {
      process.stdout.write(JSON.stringify(data, null, 2) + '\n');
    } else {
      const output = formatOutput(data);
      process.stdout.write(output + (output.endsWith('\n') ? '' : '\n'));
    }
  } catch (error) {
    console.log = originalLog;
    console.error('Error:', error.message);
    process.exit(1);
  }
}

module.exports = { fetchWeChatArticle, extractContent, formatOutput };

if (require.main === module) {
  main();
}
