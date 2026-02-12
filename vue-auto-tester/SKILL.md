---
name: vue-auto-tester
description: Auto-test and debug Vue 3 projects using Vitest and Playwright. Automatically starts dev server, checks console errors, runs tests, and can capture screenshots. Use when testing Vue components, debugging frontend issues, or validating Vue project changes.
---

# Vue Auto Tester

Automatically test, debug, and validate Vue 3 projects with minimal manual intervention.

## When to Use This Skill

- Testing Vue components after code changes
- Debugging frontend rendering issues
- Running Vitest test suites
- Capturing screenshots of Vue pages
- Checking component structure (props, styles)

## Quick Start

```bash
# Test entire Vue project
python scripts/auto_test_vue_project.py ./my-vue-app

# With screenshot comparison
python scripts/auto_test_vue_project.py ./my-vue-app --screenshot

# Save current as baseline (for future comparisons)
python scripts/auto_test_vue_project.py ./my-vue-app --baseline

# Auto-fix common errors (npm install missing packages)
python scripts/auto_test_vue_project.py ./my-vue-app --fix

# Run Vitest only
python scripts/auto_test_vue_project.py ./my-vue-app --vitest-only

# Check specific component
python scripts/auto_test_vue_project.py ./my-vue-app --check LoginForm
```

## Auto-Fix Errors (P3)

### Safe Auto-Fixes
| Error Type | Auto-Fixable | Example |
|------------|-------------|---------|
| Missing npm package | ✅ Yes | `npm install axios` |
| Duplicate imports | ⚠️ Detect only | Report to user |
| Missing import statement | ⚠️ Detect only | Report to user |
| Syntax errors | ⚠️ Detect only | Report to user |
| Network errors | ❌ No | Manual fix required |

### Usage
```bash
# Auto-fix errors (npm install missing packages)
python auto_test_vue_project.py ./my-vue-app --fix

# Dry run (show fixes without applying)
python auto_fix_errors.py ./my-vue-app --fix --dry-run
```

### How It Works
```
1. Run tests → Detect errors
2. Analyze error patterns
3. Auto-fix safe issues (missing npm packages)
4. Report manual fixes needed
5. Re-run tests
```

## Screenshot Comparison

### Capture and Compare
```bash
# Take screenshot and compare with baseline
python auto_test_vue_project.py ./my-vue-app --screenshot
```

### Save New Baseline
```bash
# After UI changes, save new baseline
python auto_test_vue_project.py ./my-vue-app --baseline
```

### How It Works
1. First run: `--baseline` saves screenshot as baseline
2. Later runs: `--screenshot` compares with baseline
3. Reports: Match ✅ or Different ❌

### Baseline Storage
```
vue-project/
└── .test-baseline/
    ├── baseline_20260212_103000.png
    ├── baseline_20260212_110500.png
    └── ...
```

## Available Functions

### auto_test_vue_project(path, screenshot=False, fix_errors=False)

Complete project test suite:

| Step | Action |
|------|--------|
| 1 | Start dev server (npm run dev) |
| 2 | Wait for server ready (port 5173) |
| 3 | Check console errors |
| 4 | Capture screenshot (optional) |
| 5 | Run Vitest suite |
| 6 | Generate test report |

### run_vitest_tests(path, reporter='json')

Run Vitest tests only:

```bash
python scripts/auto_test_vue_project.py ./my-vue-app --vitest-only
```

### check_component(name, path)

Validate Vue component structure:

```bash
python scripts/auto_test_vue_project.py ./my-vue-app --check ButtonGroup
```

Checks:
- Component file exists
- Has `<script>`, `<template>`, `<style>`
- Extracts props definitions

## Requirements

```json
{
  "devDependencies": {
    "vitest": "^2.0.0",
    "@vue/test-utils": "^2.4.0",
    "@playwright/test": "^1.45.0"
  }
}
```

### Install All Dependencies
```bash
# Vue project dependencies
npm install

# Testing dependencies
npm install -D vitest @vue/test-utils @playwright/test

# Install Playwright browsers
npx playwright install chromium
```

### Verify Installation
```bash
# Check Vitest
npx vitest --version

# Check Playwright
npx playwright --version
```

## Output Format

```json
{
  "project": "/path/to/project",
  "timestamp": "2026-02-12T10:30:00",
  "dev_server": {
    "status": "ready",
    "port": 5173
  },
  "console_errors": [
    {
      "text": "Uncaught ReferenceError: axios is not defined",
      "location": "{\"url\":\"http://localhost:5173/src/api.js\",\"lineNumber\":10}"
    }
  ],
  "console_warnings": [
    {
      "text": "Deprecation warning:...",
      "location": "..."
    }
  ],
  "page_errors": [
    {
      "message": "Cannot read property 'data' of undefined",
      "stack": "at VueComponentmounted..."
    }
  ],
  "network_errors": [
    {
      "url": "http://localhost:3000/api/users",
      "failure": "net::ERR_CONNECTION_REFUSED"
    }
  ],
  "vitest_results": {
    "status": "completed",
    "returncode": 0,
    "tests": 15,
    "passed": 14,
    "failed": 1
  },
  "screenshot": "/path/to/test-screenshot.png",
  "success": true
}
```

### Error Types Explained

| Field | Description | Cause |
|-------|-------------|-------|
| `console_errors` | JavaScript console errors | Syntax errors, undefined variables |
| `page_errors` | Uncaught exceptions | Runtime errors in Vue components |
| `network_errors` | Failed API requests | Backend down, CORS issues, wrong URL |
| `console_warnings` | Console warnings | Deprecated APIs, performance tips |

## Integration with Claude

AI can self-test by calling:

```
call vue-auto-tester.auto_test_vue_project("./vue-project")
call vue-auto-tester.check_component("MyComponent", "./vue-project")
```

## Best Practices

1. **Run tests after code changes**: `call auto_test_vue_project()` before committing
2. **Use screenshots for visual bugs**: Add `--screenshot` flag
3. **Component checks for PRs**: Verify component structure in reviews
4. **CI/CD integration**: Run `--vitest-only` in pipelines

## Troubleshooting

### Dev server won't start
```bash
# Check port 5173 is free
lsof -i :5173

# Kill conflicting processes
kill <PID>
```

### Vitest not found
```bash
# Install dependencies
npm install

# Verify vitest
npx vitest --version
```

### Playwright errors
```bash
# Install browsers
npx playwright install chromium

# Verify installation
npx playwright --version
```

### Common Console Errors

| Error | Solution |
|-------|----------|
| `Uncaught ReferenceError: axios is not defined` | Install missing dependency: `npm install axios` |
| `net::ERR_CONNECTION_REFUSED` | Start backend server or check API URL |
| `CORS policy blocked` | Configure backend CORS headers |
| `Cannot read property 'x' of undefined` | Fix component data/props |
| `Module not found: Can't resolve 'vue'` | Check import paths and aliases |
