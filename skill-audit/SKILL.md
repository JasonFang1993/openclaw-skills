---
name: skill-audit
description: Security audit tool to detect compromised, poisoned, or maliciously modified agent skills. Analyzes code for dangerous patterns, suspicious dependencies, and indicators of compromise.
---

# Skill Security Audit

A comprehensive security scanner for agent skills that detects malicious code, supply chain attacks, and indicators of compromise.

## When to Use This Skill

Use this skill when:

- Installing a new skill from an untrusted source
- Auditing existing skills for security issues
- Before running any skill code from unknown authors
- Checking skills for suspicious patterns after installation
- Responding to security concerns about skill integrity

## Quick Start

```bash
# Audit a specific skill
npx skills audit <skill-name>

# Audit a skill package before installing
npx skills audit --source <owner/repo@skill>

# Full audit with dependency analysis
npx skills audit <skill-name> --deep

# Generate JSON report for automation
npx skills audit <skill-name> --json
```

## What It Checks

### 🔴 Critical Dangers (High Risk)

| Pattern | Description | Risk Score |
|---------|-------------|------------|
| `child_process.exec` | Execute shell commands | 100 |
| `eval()` / `Function()` | Dynamic code execution | 100 |
| `process.setuid()` | Change user ID | 100 |
| `fs.unlink` / `fs.rmSync` | Delete files | 90 |
| `curl` / `wget` to external | Download/execute from internet | 90 |
| `sudo` / `chmod +x` | Privilege escalation | 85 |
| Base64 decode + eval | Obfuscated code execution | 95 |

### 🟠 Suspicious Patterns (Medium Risk)

| Pattern | Description | Risk Score |
|---------|-------------|------------|
| `fetch` / `axios` POST | Send data to external | 50 |
| `process.env` access | Read environment variables | 40 |
| `crypto` usage | Encryption/decryption | 35 |
| Timer-based execution | setInterval/setTimeout loops | 30 |
| Dynamic `require()` | Load modules at runtime | 45 |
| Hidden file operations | Files starting with `.` | 25 |

### 🟡 Indicators of Compromise (IOCs)

- Recently modified dates inconsistent with commit history
- New untrusted contributors with commit access
- Sudden dependency additions
- Code obfuscation or unusual minification
- Base64 strings in unexpected places
- Unexpected network connections to new hosts

## Audit Report Structure

```json
{
  "skill": "example/suspicious-skill",
  "auditTime": "2024-01-15T10:30:00Z",
  "riskLevel": "HIGH",
  "overallScore": 75,
  "findings": [
    {
      "type": "critical",
      "pattern": "child_process.exec",
      "file": "src/index.js",
      "line": 42,
      "description": "Arbitrary command execution detected",
      "severity": "critical"
    }
  ],
  "summary": {
    "critical": 2,
    "warning": 5,
    "info": 3
  },
  "recommendation": "DO NOT INSTALL - Contains arbitrary code execution"
}
```

## Risk Levels

| Level | Score Range | Action |
|-------|-------------|--------|
| 🟢 SAFE | 0-20 | Generally safe to use |
| 🟡 CAUTION | 21-50 | Review warnings before use |
| 🟠 WARNING | 51-79 | Requires manual review |
| 🔴 DANGER | 80-100 | DO NOT INSTALL |

## Technical Analysis

### Static Code Analysis

The auditor performs:
1. **AST Parsing** - Abstract Syntax Tree analysis for accurate pattern matching
2. **String Analysis** - Detection of encoded/obfuscated payloads
3. **Control Flow Analysis** - Understanding code execution paths
4. **Dependency Graph** - Mapping all required modules

### Dependency Checking

- Scans `package.json` for malicious dependencies
- Checks for known vulnerable packages (CVEs)
- Flags dependency confusion attempts
- Identifies out-of-date dependencies with security issues

### Git History Analysis

- Checks for commit author anomalies
- Identifies sudden large code additions
- Flags commits from new/untrusted contributors
- Verifies commit signature validation

## Example Usage Scenarios

### Scenario 1: Before Installing Unknown Skill

```bash
$ npx skills audit --source weird-developer/sketchy-plugin

🔍 Auditing weird-developer/sketchy-plugin...

⚠️  WARNING: Critical pattern detected!
File: index.js:15
Pattern: child_process.exec()
Risk: Arbitrary command execution

🔴 HIGH RISK - 85/100
Recommendation: DO NOT INSTALL

Full report saved to: ./audit-report-2024-01-15.json
```

### Scenario 2: Auditing Already Installed Skill

```bash
$ npx skills audit my-existing-skill

🔍 Auditing my-existing-skill...

✅ No critical issues found
⚠️  3 low-risk warnings detected

🟡 CAUTION - 32/100
Recommendation: Review warnings, generally safe to use

Warnings:
- [INFO] Uses process.env (line 5)
- [INFO] Uses setTimeout (line 23)
- [INFO] HTTP request to api.example.com (line 31)
```

### Scenario 3: CI/CD Integration

```bash
# In CI pipeline
npx skills audit --source $SKILL_TO_INSTALL --json > audit-result.json
if [ $(jq -r '.riskLevel' audit-result.json) == "DANGER" ]; then
  echo "Skill blocked due to security concerns"
  exit 1
fi
```

## Best Practices

### For Skill Users

1. **Always audit before first install**
2. **Re-audit after skill updates**
3. **Trust skills from verified sources**
4. **Keep skills updated** - fixes security issues
5. **Report suspicious skills** to the skills.sh team

### For Skill Developers

1. **Avoid dangerous patterns** when possible
2. **Document necessary dangerous operations**
3. **Use sandboxing** for risky operations
4. **Request minimal permissions**
5. **Maintain clean git history**

## Limitations

This auditor cannot detect:
- Zero-day vulnerabilities in legitimate code
- Sophisticated timing-based attacks
- Social engineering/phishing within skill descriptions
- Logic bugs that don't match known patterns
- Supply chain attacks on npm registry itself

## Reporting Issues

If you find a malicious skill:
1. Save the audit report
2. Report to skills.sh/issues
3. Do NOT install or use the skill
4. Alert the skill maintainer (if legitimate)

---

*Security is everyone's responsibility. Audit, verify, and stay safe.*
