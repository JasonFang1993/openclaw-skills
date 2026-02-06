#!/usr/bin/env node

/**
 * Skill Security Audit Tool v2.1
 * Detects malicious code patterns in agent skills
 */

const fs = require('fs');
const path = require('path');

// ANSI colors
const RED = '\x1b[31m';
const YELLOW = '\x1b[33m';
const GREEN = '\x1b[32m';
const BLUE = '\x1b[34m';
const CYAN = '\x1b[36m';
const RESET = '\x1b[0m';
const BOLD = '\x1b[1m';

/**
 * Preprocess code - remove comments and strings
 * Handles: // comments, /* comments, " strings, ' strings, ` templates, /regex/
 */
function preprocessCode(code) {
  let result = '';
  let i = 0;
  
  while (i < code.length) {
    // Handle multi-line comments
    if (code.substring(i, i + 2) === '/*') {
      const end = code.indexOf('*/', i + 2);
      if (end === -1) break;
      i = end + 2;
      continue;
    }
    
    // Handle single-line comments
    if (code.substring(i, i + 2) === '//') {
      const end = code.indexOf('\n', i);
      if (end === -1) break;
      i = end + 1;
      continue;
    }
    
    // Handle regex literals /.../ (before string handling)
    if (code[i] === '/' && i > 0 && !/[a-zA-Z0-9_]/.test(code[i-1])) {
      let end = i + 1;
      let inClass = false;
      while (end < code.length) {
        if (code[end] === '\\' && code[end + 1]) {
          end += 2;
          continue;
        }
        if (code[end] === '[') inClass = true;
        if (code[end] === ']') inClass = false;
        if (!inClass && code[end] === '/') break;
        end++;
      }
      while (end < code.length && /[gimsuy]/.test(code[end])) end++;
      i = end;
      continue;
    }
    
    // Handle template literals
    if (code[i] === '`') {
      let end = i + 1;
      while (end < code.length) {
        if (code.substring(end, end + 2) === '${') {
          let braceCount = 1;
          let j = end + 2;
          while (j < code.length && braceCount > 0) {
            if (code[j] === '{') braceCount++;
            if (code[j] === '}') braceCount--;
            j++;
          }
          end = j;
        } else if (code[end] === '`') {
          break;
        } else {
          end++;
        }
      }
      i = end + 1 || code.length;
      continue;
    }
    
    // Handle double-quoted strings
    if (code[i] === '"') {
      let end = i + 1;
      while (end < code.length && code[end] !== '"') {
        if (code[end] === '\\' && code[end + 1]) end++;
        end++;
      }
      i = end + 1 || code.length;
      continue;
    }
    
    // Handle single-quoted strings
    if (code[i] === "'") {
      let end = i + 1;
      while (end < code.length && code[end] !== "'") {
        if (code[end] === '\\' && code[end + 1]) end++;
        end++;
      }
      i = end + 1 || code.length;
      continue;
    }
    
    result += code[i];
    i++;
  }
  
  return result;
}

/**
 * Simple line counter
 */
function countLines(code, position) {
  return code.substring(0, position).split('\n').length;
}

// Dangerous patterns
const DANGEROUS_PATTERNS = [
  {
    id: 'EXEC_SYNC',
    pattern: /child_process\.execSync\s*\(/,
    severity: 'critical',
    score: 100,
    name: 'Shell Command (Sync)',
    description: 'Synchronous shell command execution',
    recommendation: 'DO NOT INSTALL - Arbitrary code execution'
  },
  {
    id: 'EXEC_CALLBACK',
    pattern: /child_process\.exec\s*\(/,
    severity: 'critical',
    score: 100,
    name: 'Shell Command (Async)',
    description: 'Asynchronous shell command execution',
    recommendation: 'DO NOT INSTALL - Arbitrary code execution'
  },
  {
    id: 'REQ_EXEC',
    pattern: /require\s*\(\s*['"]child_process['"]\s*\)\s*\.\s*exec\s*\(/,
    severity: 'critical',
    score: 100,
    name: 'Require + exec',
    description: 'child_process.exec via require',
    recommendation: 'DO NOT INSTALL - Arbitrary code execution'
  },
  {
    id: 'REQ_SPAWN',
    pattern: /require\s*\(\s*['"]child_process['"]\s*\)\s*\.\s*spawn\s*\([^)]*\{[^}]*shell\s*:/,
    severity: 'critical',
    score: 85,
    name: 'Require + spawn with Shell',
    description: 'child_process.spawn with shell enabled via require',
    recommendation: 'Shell=true enables command injection'
  },
  {
    id: 'SPAWN_SHELL',
    pattern: /child_process\.spawn\s*\([^)]*shell\s*:/,
    severity: 'critical',
    score: 85,
    name: 'Spawn with Shell',
    description: 'Process spawn with shell enabled',
    recommendation: 'Shell=true enables command injection'
  },
  {
    id: 'EVAL_VAR',
    pattern: /\beval\s*\(\s*(?!['"`\/])/,
    severity: 'critical',
    score: 100,
    name: 'eval with Variable',
    description: 'eval() with variable argument - arbitrary code execution',
    recommendation: 'Avoid skills using eval() with dynamic input'
  },
  {
    id: 'FUNCTION_CTOR',
    pattern: /new\s+Function\s*\(/,
    severity: 'critical',
    score: 100,
    name: 'Function Constructor',
    description: 'Function constructor enables dynamic code execution',
    recommendation: 'DO NOT INSTALL'
  },
  {
    id: 'DELETE_FILES',
    pattern: /\b(fs\s*\.\s*)?(unlink|rmSync|rmdirSync)\s*\(/,
    severity: 'warning',
    score: 60,
    name: 'File Deletion',
    description: 'File deletion operations detected',
    recommendation: 'Review file operations'
  },
  {
    id: 'NETWORK_POST',
    pattern: /(fetch|axios)\s*\(\s*\{[^}]*method\s*:\s*['"]POST['"]/,
    severity: 'warning',
    score: 40,
    name: 'POST Request',
    description: 'HTTP POST request - potential data exfiltration',
    recommendation: 'Review endpoints and data flow'
  }
];

const SUSPICIOUS_PATTERNS = [
  {
    id: 'TIMER_LOOP',
    pattern: /setInterval\s*\(/,
    severity: 'info',
    score: 20,
    name: 'Timer Persistence',
    description: 'setInterval detected - possible persistence'
  },
  {
    id: 'ENV_ACCESS',
    pattern: /process\.env\s*\[\s*['"`]/,
    severity: 'info',
    score: 15,
    name: 'Environment Access',
    description: 'Accessing environment variables'
  },
  {
    id: 'CRYPTO_USAGE',
    pattern: /require\s*\(\s*['"]crypto['"]/,
    severity: 'info',
    score: 15,
    name: 'Cryptography',
    description: 'Encryption/decryption operations'
  },
  {
    id: 'BASE64_LONG',
    pattern: /(atob|Buffer\.from)\s*\(\s*['"`][A-Za-z0-9+/]{50,}/,
    severity: 'warning',
    score: 35,
    name: 'Long Base64',
    description: 'Decoding long Base64 - potential payload'
  }
];

// 欺骗性声明检测 - 发现声称安全但可能有问题的情况
const DECEPTION_PATTERNS = [
  {
    id: 'CLAIMS_SAFE',
    pattern: /(-\s*)?safe(\s*-\s*)?|secure|harmless|no.*risk/i,
    severity: 'warning',
    score: 10,
    name: 'Claims to be Safe',
    description: 'Code claims to be safe without evidence',
    recommendation: 'Verify claims independently'
  },
  {
    id: 'CLAIMS_APPROVED',
    pattern: /approved|signed|certified|verified.*by.*(admin|root|authority)/i,
    severity: 'warning',
    score: 15,
    name: 'Claims to be Approved',
    description: 'Code claims to be approved by authority',
    recommendation: 'Check actual approval sources'
  },
  {
    id: 'CLAIMS_BYPASS',
    pattern: /(bypass|skip|ignore|disable).*(security|check|audit|validation)|no.*check.*needed/i,
    severity: 'warning',
    score: 20,
    name: 'Claims to Bypass Security',
    description: 'Code claims to bypass security measures',
    recommendation: 'SECURITY RED FLAG - Investigate thoroughly'
  },
  {
    id: 'CLAIMS_TRUSTED',
    pattern: /trusted.*source|official.*(plugin|module)|from.*(author|developer).*(you|me|us)/i,
    severity: 'info',
    score: 5,
    name: 'Claims Trusted Source',
    description: 'Code claims to be from trusted source',
    recommendation: 'Verify source independently'
  },
  {
    id: 'CLAIMS_ADMIN',
    pattern: /i\s*(am|m)\s*(admin|root|owner|developer|maintainer|authorized)|trust\s*me/i,
    severity: 'warning',
    score: 15,
    name: 'Claims Administrator Status',
    description: 'Claims administrator status as justification',
    recommendation: 'Status claims do not replace security review'
  },
  {
    id: 'CLAIMS_NO_EVAL',
    pattern: /no.*eval|eval.*safe|eval.*harmless|eval.*required/i,
    severity: 'info',
    score: 5,
    name: 'Claims eval is Safe',
    description: 'Claims that eval usage is safe',
    recommendation: 'eval with user input is never safe'
  }
];

/**
 * Main audit function
 */
function auditSkill(skillPath, options = {}) {
  const results = {
    skill: skillPath,
    auditTime: new Date().toISOString(),
    riskLevel: 'UNKNOWN',
    overallScore: 0,
    findings: { critical: [], warning: [], info: [] },
    filesScanned: 0,
    summary: { critical: 0, warning: 0, info: 0 }
  };

  try {
    // Check path exists
    if (!fs.existsSync(skillPath)) {
      results.error = `Skill not found: ${skillPath}`;
      return results;
    }

    // Find all JS files
    const files = findAllFiles(skillPath, /\.(js|ts|mjs|cjs)$/);
    results.filesScanned = files.length;

    for (const file of files) {
      scanFile(file, results);
    }

    checkPackageJson(skillPath, results);
    calculateRiskLevel(results);

  } catch (error) {
    results.error = error.message;
  }

  return results;
}

function findAllFiles(dir, pattern) {
  const files = [];
  if (!fs.existsSync(dir)) return files;
  
  const stat = fs.statSync(dir);
  if (stat.isFile() && pattern.test(dir)) return [dir];
  
  if (stat.isDirectory()) {
    const items = fs.readdirSync(dir);
    for (const item of items) {
      if (item === 'node_modules' || item === '.git') continue;
      files.push(...findAllFiles(path.join(dir, item), pattern));
    }
  }
  return files;
}

function extractComments(code) {
  const comments = [];
  
  // Single-line comments
  const singleLineRegex = /\/\/(.*)/g;
  let match;
  while ((match = singleLineRegex.exec(code)) !== null) {
    comments.push({
      text: match[1].trim(),
      line: code.substring(0, match.index).split('\n').length
    });
  }
  
  // Multi-line comments
  const multiLineRegex = /\/\*([\s\S]*?)\*\//g;
  while ((match = multiLineRegex.exec(code)) !== null) {
    const lines = match[1].split('\n');
    const startLine = code.substring(0, match.index).split('\n').length;
    lines.forEach((line, i) => {
      comments.push({
        text: line.trim(),
        line: startLine + i
      });
    });
  }
  
  return comments;
}

function scanFile(filePath, results) {
  try {
    const content = fs.readFileSync(filePath, 'utf8');
    const cleanCode = preprocessCode(content);
    const relativePath = path.relative(process.cwd(), filePath);
    
    // Check dangerous patterns
    for (const danger of DANGEROUS_PATTERNS) {
      const matches = cleanCode.match(new RegExp(danger.pattern.source, 'gi')) || [];
      for (const match of matches) {
        const pos = cleanCode.indexOf(match);
        const line = countLines(content, pos);
        
        results.findings[danger.severity].push({
          pattern: danger.id,
          name: danger.name,
          file: relativePath,
          line: line,
          description: danger.description,
          severity: danger.severity,
          recommendation: danger.recommendation
        });
      }
    }

    // Check suspicious patterns
    for (const sus of SUSPICIOUS_PATTERNS) {
      const matches = cleanCode.match(new RegExp(sus.pattern.source, 'gi')) || [];
      for (const match of matches) {
        const pos = cleanCode.indexOf(match);
        const line = countLines(content, pos);
        
        results.findings[sus.severity].push({
          pattern: sus.id,
          name: sus.name,
          file: relativePath,
          line: line,
          description: sus.description,
          severity: sus.severity
        });
      }
    }
    
    // Check for deception patterns in comments
    const comments = extractComments(content);
    for (const deception of DECEPTION_PATTERNS) {
      for (const comment of comments) {
        if (deception.pattern.test(comment.text)) {
          // Only flag if there's also dangerous code nearby
          const nearbyDanger = results.findings.critical.length > 0;
          
          if (nearbyDanger) {
            results.findings[deception.severity].push({
              pattern: deception.id,
              name: deception.name,
              file: relativePath,
              line: comment.line,
              description: `${deception.description} (Found: "${comment.text.substring(0, 50)}")`,
              severity: deception.severity,
              recommendation: `${deception.recommendation} CODE HAS KNOWN DANGEROUS PATTERNS!`
            });
          }
        }
      }
    }
    
  } catch (error) {
    // Skip unreadable files
  }
}

function checkPackageJson(skillPath, results) {
  const pkgPath = path.join(skillPath, 'package.json');
  if (!fs.existsSync(pkgPath)) return;
  
  try {
    const pkg = JSON.parse(fs.readFileSync(pkgPath, 'utf8'));
    
    const maliciousPackages = ['node-ipc', 'flatmap-stream', 'event-stream'];
    const allDeps = { ...(pkg.dependencies || {}), ...(pkg.devDependencies || {}) };
    
    for (const [pkgName, version] of Object.entries(allDeps)) {
      if (maliciousPackages.includes(pkgName.toLowerCase())) {
        results.findings.critical.push({
          pattern: 'MALICIOUS_DEP',
          name: 'Known Malicious Package',
          file: 'package.json',
          description: `Contains ${pkgName}@${version}`,
          severity: 'critical',
          recommendation: 'DO NOT INSTALL'
        });
      }
    }
  } catch (error) {
    // Skip invalid package.json
  }
}

function calculateRiskLevel(results) {
  const c = results.findings.critical.length;
  const w = results.findings.warning.length;
  const i = results.findings.info.length;
  
  let score = c * 25 + w * 8 + i * 2;
  score = Math.min(score, 100);
  
  results.overallScore = score;
  results.summary = { critical: c, warning: w, info: i };
  
  if (c >= 2 || score >= 70) results.riskLevel = 'DANGER';
  else if (c >= 1 || score >= 40) results.riskLevel = 'WARNING';
  else if (w >= 3 || score >= 20) results.riskLevel = 'CAUTION';
  else if (c === 0 && w === 0 && i === 0) results.riskLevel = 'SAFE';
  else results.riskLevel = 'INFO';
}

function printResults(results, options = {}) {
  console.log('\n' + '═'.repeat(60));
  console.log(`${BLUE}🔍 Skill Security Audit v2.2${RESET}`);
  console.log('═'.repeat(60));
  
  console.log(`\n📦 Skill: ${BOLD}${results.skill}${RESET}`);
  console.log(`📅 Audited: ${results.auditTime}`);
  console.log(`📄 Files Scanned: ${results.filesScanned}`);
  
  if (options.verbose) {
    console.log(`🎯 Threshold: ${options.threshold}`);
    if (options.ignorePaths.length > 0) {
      console.log(`⏭️  Ignored: ${options.ignorePaths.join(', ')}`);
    }
  }
  
  if (results.error) {
    console.log(`\n${RED}❌ Error: ${results.error}${RESET}`);
    return;
  }
  
  const riskConfig = {
    'DANGER': { color: RED, emoji: '🔴' },
    'WARNING': { color: YELLOW, emoji: '🟠' },
    'CAUTION': { color: BLUE, emoji: '🟡' },
    'INFO': { color: CYAN, emoji: 'ℹ️' },
    'SAFE': { color: GREEN, emoji: '✅' }
  };
  
  const cfg = riskConfig[results.riskLevel] || riskConfig.SAFE;
  const threshold = options.threshold || 40;
  const exceeds = results.overallScore >= threshold;
  
  console.log(`\n${cfg.emoji} Risk Level: ${cfg.color}${BOLD}${results.riskLevel}${RESET}`);
  console.log(`📊 Overall Score: ${results.overallScore}/${threshold}${exceeds ? ' ⚠️ EXCEEDS THRESHOLD' : ''}`);
  
  console.log(`\n${BOLD}📋 Summary:${RESET}`);
  console.log(`   ${RED}Critical: ${results.summary.critical}${RESET}`);
  console.log(`   ${YELLOW}Warnings: ${results.summary.warning}${RESET}`);
  console.log(`   ${CYAN}Info:     ${results.summary.info}${RESET}`);
  
  // Critical findings
  if (results.findings.critical.length > 0) {
    console.log(`\n${RED}${BOLD}⚠️  CRITICAL ISSUES:${RESET}`);
    const criticalList = options.verbose ? results.findings.critical : results.findings.critical.slice(0, 10);
    for (const f of criticalList) {
      console.log(`  ${RED}•${RESET} [${f.pattern}] ${f.name}`);
      console.log(`    📁 ${f.file}:${f.line}`);
      console.log(`    ${RED}${f.description}${RESET}`);
      if (f.recommendation) console.log(`    ${CYAN}💡 ${f.recommendation}${RESET}`);
    }
    if (!options.verbose && results.findings.critical.length > 10) {
      console.log(`  ... and ${results.findings.critical.length - 10} more critical issues`);
    }
  }
  
  // Warnings
  if (results.findings.warning.length > 0) {
    console.log(`\n${YELLOW}${BOLD}⚠️  WARNINGS:${RESET}`);
    const warningList = options.verbose ? results.findings.warning : results.findings.warning.slice(0, 10);
    for (const f of warningList) {
      console.log(`  ${YELLOW}•${RESET} [${f.pattern}] ${f.name}`);
      console.log(`    📁 ${f.file}:${f.line}`);
    }
    if (!options.verbose && results.findings.warning.length > 10) {
      console.log(`  ... and ${results.findings.warning.length - 10} more warnings`);
    }
  }
  
  // Info
  if (options.verbose && results.findings.info.length > 0) {
    console.log(`\n${CYAN}${BOLD}ℹ️  INFORMATIONAL:${RESET}`);
    for (const f of results.findings.info.slice(0, 10)) {
      console.log(`  ${CYAN}•${RESET} [${f.pattern}] ${f.name}`);
      console.log(`    📁 ${f.file}:${f.line}`);
    }
  }
  
  // Recommendation
  console.log(`\n${BOLD}💡 Recommendation:${RESET}`);
  const recs = {
    'DANGER': `${RED}🚫 DO NOT INSTALL${RESET}`,
    'WARNING': `${YELLOW}⚠️  Manual review required${RESET}`,
    'CAUTION': `${BLUE}✓ Generally safe${RESET}`,
    'INFO': `${CYAN}ℹ️  Likely safe${RESET}`,
    'SAFE': `${GREEN}✅ No issues detected${RESET}`
  };
  console.log(`   ${recs[results.riskLevel]}`);
  
  console.log('\n' + '═'.repeat(60) + '\n');
}

// CLI
function main() {
  const args = process.argv.slice(2);
  const options = { 
    json: false,
    ignorePaths: [],
    threshold: 40,
    verbose: false
  };
  
  let skillPath = null;
  
  // Parse arguments
  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    
    if (arg === '--help' || arg === '-h') {
      showHelp();
      process.exit(0);
    } else if (arg === '--json' || arg === '-j') {
      options.json = true;
    } else if (arg === '--verbose' || arg === '-v') {
      options.verbose = true;
    } else if (arg === '--threshold' || arg === '-t') {
      options.threshold = parseInt(args[++i]) || 40;
    } else if (arg === '--ignore' || arg === '-i') {
      const paths = args[++i];
      if (paths) options.ignorePaths = paths.split(',').map(p => p.trim());
    } else if (!arg.startsWith('-') && !skillPath) {
      skillPath = arg;
    }
  }
  
  if (!skillPath) {
    showHelp();
    process.exit(0);
  }
  
  const results = auditSkill(skillPath, options);
  if (options.json) console.log(JSON.stringify(results, null, 2));
  else printResults(results, options);
  
  // Exit based on threshold
  if (results.overallScore >= options.threshold) {
    process.exit(2);
  }
  process.exit(0);
}

function showHelp() {
  console.log(`
${BLUE}Skill Security Audit v2.2${RESET}
${BOLD}Detects malicious code patterns in agent skills${RESET}

${BOLD}Usage:${RESET}
  npx skill-audit <skill-path> [options]
  npx skill-audit ./my-skill --json
  npx skill-audit ./my-skill --threshold 60
  npx skill-audit ./my-skill --ignore node_modules,dist

${BOLD}Options:${RESET}
  --json, -j           Output results as JSON
  --verbose, -v        Show detailed findings
  --threshold, -t N    Set risk threshold (default: 40)
  --ignore, -i paths   Comma-separated paths to ignore
  --help, -h           Show this help message

${BOLD}Risk Levels:${RESET}
  🔴 DANGER   - Critical issues found, do not use
  🟠 WARNING  - Suspicious patterns, manual review required
  🟡 CAUTION  - Low risk, generally safe
  🟢 SAFE     - No security issues detected
  ℹ️  INFO     - Only informational findings

${BOLD}Exit Codes:${RESET}
  0 - Below threshold (safe to use)
  1 - Error
  2 - Above threshold (risky)

${BOLD}Examples:${RESET}
  npx skill-audit ./my-skill
  npx skill-audit ./my-skill --json --verbose
  npx skill-audit ./my-skill --threshold 70
  npx skill-audit ./my-skill --ignore node_modules,.git,dist

${BOLD}Environment Variables:${RESET}
  SKILL_AUDIT_THRESHOLD    Override default threshold
  SKILL_AUDIT_IGNORE      Comma-separated paths to ignore
`);
}

module.exports = { auditSkill, DANGEROUS_PATTERNS, SUSPICIOUS_PATTERNS, preprocessCode };

if (require.main === module) main();
