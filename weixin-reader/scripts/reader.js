#!/usr/bin/env node

/**
 * WeChat Article Reader
 * Fetches and extracts readable content from mp.weixin.qq.com articles
 */

const https = require('https');
const http = require('http');

// Default User-Agent (iPhone Safari)
const DEFAULT_UA = 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1';

function fetchWeChatArticle(url, userAgent = DEFAULT_UA) {
  return new Promise((resolve, reject) => {
    // Extract hostname and path from URL
    const urlObj = new URL(url);
    const options = {
      hostname: urlObj.hostname,
      path: urlObj.pathname + urlObj.search,
      method: 'GET',
      headers: {
        'User-Agent': userAgent,
        'Referer': 'https://mp.weixin.qq.com/',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
      }
    };

    const client = urlObj.protocol === 'https:' ? https : http;

    console.log(`Fetching: ${url}`);
    console.log(`User-Agent: ${userAgent}`);

    const req = client.request(options, (res) => {
      let data = '';

      res.on('data', (chunk) => {
        data += chunk;
      });

      res.on('end', () => {
        if (res.statusCode !== 200) {
          reject(new Error(`HTTP ${res.statusCode}: ${res.statusMessage}`));
          return;
        }

        resolve(extractContent(data, url));
      });
    });

    req.on('error', (e) => {
      reject(e);
    });

    req.setTimeout(30000, () => {
      req.destroy();
      reject(new Error('Request timeout'));
    });

    req.end();
  });
}

function extractContent(html, url) {
  // Extract title
  const titleMatch = html.match(/<title[^>]*>([^<]+)<\/title>/i);
  const title = titleMatch ? titleMatch[1].trim() : 'Unknown Title';

  // Extract meta description
  const descMatch = html.match(/<meta[^>]*name=["']description["'][^>]*content=["']([^"']+)["']/i);
  const description = descMatch ? descMatch[1].trim() : '';

  // Clean HTML and extract text
  const cleanText = html
    // Remove scripts
    .replace(/<script[^>]*>[\s\S]*?<\/script>/gi, '')
    // Remove styles
    .replace(/<style[^>]*>[\s\S]*?<\/style>/gi, '')
    // Remove comments
    .replace(/<!--[\s\S]*?-->/g, '')
    // Replace tags with newlines
    .replace(/<\/p>/g, '\n')
    .replace(/<\/div>/g, '\n')
    .replace(/<\/br>/g, '\n')
    .replace(/<br\s*\/?>/g, '\n')
    .replace(/<\/h[1-6]>/g, '\n\n')
    .replace(/<h[1-6][^>]*>/gi, '\n\n### ')
    .replace(/<[^>]+>/g, '')
    // Decode HTML entities
    .replace(/&nbsp;/g, ' ')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&amp;/g, '&')
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    // Clean up whitespace
    .replace(/\n{3,}/g, '\n\n')
    .trim();

  // Extract paragraphs
  const paragraphs = cleanText.split('\n')
    .map(line => line.trim())
    .filter(line => line.length > 10)
    .filter(line => line.length < 500)
    .filter(line => !line.toLowerCase().includes('http'))
    .filter(line => !line.toLowerCase().includes('wx_'))
    .filter(line => !line.match(/^\d+$/))  // Remove pure numbers
    .slice(0, 100);  // Limit to 100 paragraphs

  return {
    title,
    description,
    url,
    paragraphs,
    rawLength: html.length,
    extractedLength: cleanText.length,
    paragraphCount: paragraphs.length
  };
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

  if (options.content !== false) {
    data.paragraphs.forEach((p, i) => {
      output += `${p}\n\n`;
    });
  }

  output += `---\n`;
  output += `共提取 ${data.paragraphCount} 段内容\n`;

  return output;
}

// CLI
async function main() {
  const args = process.argv.slice(2);
  const url = args[0];

  if (!url) {
    console.error('Usage: node reader.js <wechat-article-url>');
    console.error('Example: node reader.js https://mp.weixin.qq.com/s/xxxxx');
    process.exit(1);
  }

  try {
    const data = await fetchWeChatArticle(url);
    const output = formatOutput(data);
    console.log(output);
  } catch (error) {
    console.error('Error:', error.message);
    process.exit(1);
  }
}

// Export for programmatic use
module.exports = { fetchWeChatArticle, extractContent, formatOutput };

// Run if called directly
if (require.main === module) {
  main();
}
