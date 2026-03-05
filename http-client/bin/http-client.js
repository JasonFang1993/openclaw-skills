#!/usr/bin/env node

/**
 * HTTP Client v2.3
 * Added: Config file support (.http-client.json), saved requests
 */

const https = require('https');
const http = require('http');
const url = require('url');
const querystring = require('querystring');
const zlib = require('zlib');
const fs = require('fs');
const path = require('path');
const stream = require('stream');
const { pipeline } = require('stream/promises');
const os = require('os');

// ANSI colors
const RED = '\x1b[31m';
const YELLOW = '\x1b[33m';
const GREEN = '\x1b[32m';
const BLUE = '\x1b[34m';
const CYAN = '\x1b[36m';
const MAGENTA = '\x1b[35m';
const RESET = '\x1b[0m';
const BOLD = '\x1b[1m';

// Config file path
const CONFIG_FILE = '.http-client.json';
const HISTORY_FILE = '.http-client-history.json';

// User-Agent pool
const USER_AGENTS = [
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0',
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15'
];

function getRandomUserAgent() {
  return USER_AGENTS[Math.floor(Math.random() * USER_AGENTS.length)];
}

// Sensitive data mask
const SENSITIVE_PATTERNS = [
  /Authorization:\s*Bearer\s+[a-zA-Z0-9_\-\.]+/gi,
  /X-API-Key:\s*[a-zA-Z0-9_\-\.]+/gi
];

function sanitize(obj) {
  if (!obj) return obj;
  const cloned = JSON.parse(JSON.stringify(obj));
  if (cloned.headers) {
    for (const key of Object.keys(cloned.headers)) {
      if (key.toLowerCase().includes('authorization') || 
          key.toLowerCase().includes('x-api-key')) {
        cloned.headers[key] = '[MASKED]';
      }
    }
  }
  return cloned;
}

function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }
function randomDelay(min = 100, max = 500) { 
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

function formatBytes(bytes) {
  if (bytes === 0) return '0 B';
  const k = 1024, sizes = ['B', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

function prettyPrint(result) {
  let out = '';
  out += `${CYAN}HTTP/1.1${RESET} ${result.status} OK\n`;
  out += `${BLUE}Size:${RESET} ${formatBytes(result.raw?.length || 0)}\n`;
  out += `${BLUE}Time:${RESET} ${result.duration}ms\n`;
  
  if (result.isJSON) {
    out += `\n${MAGENTA}Response (JSON):${RESET}\n`;
    out += JSON.stringify(result.data, null, 2);
  } else {
    out += `\n${MAGENTA}Response:${RESET}\n`;
    out += (result.raw || '').substring(0, 500);
    if (result.raw?.length > 500) out += '\n... (truncated)';
  }
  return out;
}

function detectBot(status, headers, body) {
  const issues = [];
  if (status === 403) issues.push('403 Forbidden');
  if (status === 429) issues.push('Rate limited');
  if (headers['server']?.includes('cloudflare') || 
      body?.includes('Cloudflare') || body?.includes('challenge')) {
    issues.push('Cloudflare');
  }
  return issues.length > 0 ? issues : null;
}

// Config Manager
class ConfigManager {
  constructor() {
    this.configPath = CONFIG_FILE;
    this.historyPath = HISTORY_FILE;
    this.config = this.loadConfig();
    this.history = this.loadHistory();
  }

  loadConfig() {
    try {
      if (fs.existsSync(this.configPath)) {
        const config = JSON.parse(fs.readFileSync(this.configPath, 'utf8'));
        console.log(`${GREEN}✅ Loaded config: ${this.configPath}${RESET}`);
        return config;
      }
    } catch (e) {
      console.log(`${YELLOW}⚠️  Config load failed: ${e.message}${RESET}`);
    }
    return { saved: {}, defaults: {} };
  }

  loadHistory() {
    try {
      if (fs.existsSync(this.historyPath)) {
        return JSON.parse(fs.readFileSync(this.historyPath, 'utf8'));
      }
    } catch (e) {}
    return [];
  }

  saveHistory() {
    try {
      fs.writeFileSync(this.historyPath, JSON.stringify(this.history.slice(-50), null, 2));
    } catch (e) {}
  }

  addToHistory(request, result) {
    this.history.push({
      timestamp: new Date().toISOString(),
      url: request.url,
      method: request.method,
      status: result?.status,
      duration: result?.duration
    });
    this.saveHistory();
  }

  getSaved(name) {
    return this.config.saved?.[name] || this.config.defaults?.[name];
  }

  async saveRequest(name, request) {
    this.config.saved = this.config.saved || {};
    this.config.saved[name] = request;
    try {
      fs.writeFileSync(this.configPath, JSON.stringify(this.config, null, 2));
      console.log(`${GREEN}✅ Saved request: ${name}${RESET}`);
    } catch (e) {
      console.log(`${RED}❌ Save failed: ${e.message}${RESET}`);
    }
  }

  async deleteRequest(name) {
    if (this.config.saved?.[name]) {
      delete this.config.saved[name];
      fs.writeFileSync(this.configPath, JSON.stringify(this.config, null, 2));
      console.log(`${GREEN}✅ Deleted: ${name}${RESET}`);
    } else {
      console.log(`${YELLOW}⚠️  Not found: ${name}${RESET}`);
    }
  }

  listSaved() {
    console.log(`\n${CYAN}Saved Requests:${RESET}`);
    console.log('='.repeat(40));
    const saved = this.config.saved || {};
    if (Object.keys(saved).length === 0) {
      console.log('No saved requests. Use: http-client --save <name>');
    } else {
      for (const [name, req] of Object.entries(saved)) {
        console.log(`${GREEN}📌 ${name}${RESET}`);
        console.log(`   ${req.method || 'GET'} ${req.url}`);
      }
    }
    console.log('');
  }

  showHistory() {
    console.log(`\n${CYAN}Recent History:${RESET}`);
    console.log('='.repeat(40));
    const recent = this.history.slice(-20);
    if (recent.length === 0) {
      console.log('No history yet.');
    } else {
      for (const h of recent.reverse()) {
        const status = h.status ? `${GREEN}${h.status}${RESET}` : `${RED}❌${RESET}`;
        console.log(`${status} [${h.method}] ${h.url} (${h.duration || '?'}ms)`);
      }
    }
    console.log('');
  }
}

const configManager = new ConfigManager();

// Make HTTP request
function makeRequest(targetUrl, options = {}) {
  return new Promise((resolve, reject) => {
    const parsedUrl = new url.URL(targetUrl);
    const isHttps = parsedUrl.protocol === 'https:';
    const httpModule = isHttps ? https : http;

    const headers = {
      'User-Agent': options.userAgent || getRandomUserAgent(),
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
      'Accept-Language': 'en-US,en;q=0.9',
      'Accept-Encoding': 'gzip, deflate',
      'Connection': 'keep-alive',
      ...options.headers
    };

    if (options.auth) {
      headers['Authorization'] = `Basic ${Buffer.from(`${options.auth.username}:${options.auth.password}`).toString('base64')}`;
    }

    let path = parsedUrl.pathname + (parsedUrl.search || '');
    if (options.queryParams) {
      const qs = querystring.stringify(options.queryParams);
      path += (parsedUrl.search ? '&' : '?') + qs;
    }

    const reqOptions = {
      hostname: parsedUrl.hostname,
      port: parsedUrl.port || (isHttps ? 443 : 80),
      path: path,
      method: options.method || 'GET',
      headers: headers,
      timeout: options.timeout || 30000
    };

    const startTime = Date.now();

    const req = httpModule.request(reqOptions, (res) => {
      // Handle redirects
      if ([301, 302, 303, 307, 308].includes(res.statusCode) && res.headers.location) {
        const redirectUrl = new url.URL(res.headers.location, targetUrl);
        console.log(`${CYAN}→ Redirect: ${redirectUrl.href}${RESET}`);
        makeRequest(redirectUrl.href, { ...options, method: 'GET' })
          .then(resolve).catch(reject);
        return;
      }

      const chunks = [];
      res.on('data', chunk => chunks.push(chunk));
      res.on('end', () => {
        const duration = Date.now() - startTime;
        let body = Buffer.concat(chunks);

        if (res.headers['content-encoding'] === 'gzip') {
          try { body = zlib.gunzipSync(body); } catch (e) {}
        } else if (res.headers['content-encoding'] === 'deflate') {
          try { body = zlib.inflateSync(body); } catch (e) {}
        }

        const bodyStr = body.toString('utf8');
        const ct = res.headers['content-type'] || '';

        let data = bodyStr;
        let isJSON = false;
        if (ct.includes('application/json')) {
          try { data = JSON.parse(bodyStr); isJSON = true; } catch (e) {}
        }

        const result = {
          status: res.statusCode,
          headers: res.headers,
          raw: bodyStr,
          data: data,
          isJSON: isJSON,
          isHTML: ct.includes('text/html'),
          isBinary: ct.includes('image/') || ct.includes('video/'),
          url: targetUrl,
          duration: duration,
          redirected: !!res.headers.location
        };

        const botIssues = detectBot(res.statusCode, res.headers, bodyStr);
        if (botIssues) result.botIssues = botIssues;

        resolve(result);
      });
    });

    req.on('error', (e) => reject({
      message: e.message,
      code: e.code,
      url: targetUrl,
      retryable: ['ECONNRESET', 'ETIMEDOUT', 'ENOTFOUND'].includes(e.code)
    }));

    req.on('timeout', () => {
      req.destroy();
      reject({ message: 'Timeout', timeout: options.timeout, url: targetUrl, retryable: true });
    });

    if (options.body) {
      const bodyData = typeof options.body === 'object' ? JSON.stringify(options.body) : options.body;
      req.write(bodyData);
    }
    req.end();
  });
}

async function httpRequest(options) {
  const maxRetries = options.maxRetries || 3;
  const retryDelay = options.retryDelay || 1000;

  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      const result = await makeRequest(options.url, {
        method: options.method,
        headers: options.headers,
        body: options.body,
        auth: options.auth,
        queryParams: options.queryParams,
        userAgent: options.userAgent,
        timeout: options.timeout
      });

      // Bot detection with retry
      if (options.antiBot && result.botIssues && attempt < maxRetries) {
        console.log(`${YELLOW}⚠️  Bot: ${result.botIssues.join(', ')}${RESET}`);
        await sleep(randomDelay(1000, 3000));
        continue;
      }

      // Add to history
      configManager.addToHistory(options, result);

      return result;

    } catch (error) {
      if (error.retryable && attempt < maxRetries) {
        const delay = retryDelay * Math.pow(2, attempt - 1);
        console.log(`${YELLOW}🔄 Retry ${attempt}/${maxRetries} in ${delay}ms...${RESET}`);
        await sleep(delay);
      } else {
        throw error;
      }
    }
  }
}

async function downloadFile(options) {
  const { url, outputPath, headers = {} } = options;
  console.log(`${CYAN}📥 Downloading: ${url}${RESET}`);
  
  const result = await makeRequest(url, { headers, timeout: 60000 });
  
  await pipeline(
    stream.Readable.from(result.raw),
    fs.createWriteStream(outputPath)
  );
  
  console.log(`${GREEN}✅ Saved: ${outputPath} (${formatBytes(result.raw.length)})${RESET}`);
  return { path: outputPath, size: result.raw.length };
}

// CLI
async function main() {
  const args = process.argv.slice(2);
  
  const options = {
    url: null,
    method: 'GET',
    headers: {},
    body: null,
    pretty: false,
    antiBot: false,
    userAgent: 'default',
    maxRetries: 3,
    timeout: 30000,
    output: null,
    save: null,
    load: null,
    list: false,
    history: false,
    delete: null,
    help: false
  };

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    
    if (arg === '--help' || arg === '-h') options.help = true;
    else if (arg === '--url' || arg === '-u') options.url = args[++i];
    else if (arg === '--method' || arg === '-m') options.method = args[++i].toUpperCase();
    else if (arg === '--header' || arg === '-H') {
      const [key, ...val] = args[++i].split(':');
      options.headers[key.trim()] = val.join(':').trim();
    } else if (arg === '--data' || arg === '-d') options.body = args[++i];
    else if (arg === '--json') options.pretty = true;
    else if (arg === '--pretty' || arg === '-p') options.pretty = true;
    else if (arg === '--anti-bot' || arg === '-a') options.antiBot = true;
    else if (arg === '--user-agent' || arg === '-U') options.userAgent = args[++i];
    else if (arg === '--bearer') options.headers['Authorization'] = `Bearer ${args[++i]}`;
    else if (arg === '--output' || arg === '-o') options.output = args[++i];
    else if (arg === '--save' || arg === '-s') options.save = args[++i];
    else if (arg === '--load' || arg === '-l') options.load = args[++i];
    else if (arg === '--list') options.list = true;
    else if (arg === '--history') options.history = true;
    else if (arg === '--delete' || arg === '-D') options.delete = args[++i];
    else if (arg === '--max-retries') options.maxRetries = parseInt(args[++i]) || 3;
    else if (arg === '--timeout') options.timeout = parseInt(args[++i]) || 30000;
  }

  // Show saved requests
  if (options.list) {
    configManager.listSaved();
    return;
  }

  // Show history
  if (options.history) {
    configManager.showHistory();
    return;
  }

  // Delete saved request
  if (options.delete) {
    await configManager.deleteRequest(options.delete);
    return;
  }

  // Load saved request
  if (options.load) {
    const saved = configManager.getSaved(options.load);
    if (saved) {
      options.url = saved.url || options.url;
      options.method = saved.method || options.method;
      options.headers = { ...saved.headers, ...options.headers };
      options.body = saved.body || options.body;
      console.log(`${GREEN}✅ Loaded: ${options.load}${RESET}`);
    } else {
      console.log(`${RED}❌ Not found: ${options.load}${RESET}`);
      return;
    }
  }

  if (options.help || !options.url) {
    console.log(`
${BLUE}${BOLD}HTTP Client v2.3 - with Config & History${RESET}

${BOLD}Config Commands:${RESET}
  --save <name>      Save current request as <name>
  --load <name>      Load saved request
  --list             List saved requests
  --history          Show request history
  --delete <name>    Delete saved request

${BOLD}Features:${RESET}
  ✅ GET/POST/PUT/PATCH/DELETE
  ✅ Authentication (Bearer, Basic)
  ✅ Auto-retry with backoff
  ✅ Anti-bot protection
  ✅ Request sanitization
  ✅ Pretty print
  ✅ File download
  ✅ History tracking

${BOLD}Options:${RESET}
  --url, -u           URL
  --method, -m        Method (default: GET)
  --header, -H        Custom header
  --data, -d          Request body
  --pretty, -p        Pretty print
  --anti-bot, -a     Anti-bot mode
  --user-agent, -U   User-Agent
  --bearer            Bearer token
  --output, -o        Download file
  --max-retries       Retry count
  --timeout           Timeout (ms)

${BOLD}Examples:${RESET}
  # Basic
  http-client -u https://httpbin.org/uuid --pretty
  
  # Save request
  http-client -u https://api.example.com/users -m POST \\
    --save my-api
  
  # Load saved
  http-client --load my-api --pretty
  
  # Show history
  http-client --history
`);
    return;
  }

  try {
    if (options.output) {
      await downloadFile({ url: options.url, outputPath: options.output, headers: options.headers });
    } else {
      const result = await httpRequest(options);
      console.log(options.pretty || result.isJSON ? prettyPrint(result) : result.raw);
    }
  } catch (error) {
    console.error(`${RED}Error:${RESET}`, error.message);
    if (error.status) console.error(`${RED}Status:${RESET}`, error.status);
    process.exit(1);
  }

  // Auto-save if --save provided
  if (options.save) {
    await configManager.saveRequest(options.save, {
      url: options.url,
      method: options.method,
      headers: options.headers,
      body: options.body
    });
  }
}

module.exports = {
  httpRequest,
  downloadFile,
  configManager,
  sanitize,
  makeRequest
};

if (require.main === module) {
  main();
}
