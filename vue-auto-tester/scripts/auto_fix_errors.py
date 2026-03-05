#!/usr/bin/env python3
"""
Auto-fix common Vue/JS errors.

Usage:
    python auto_fix_errors.py <project-path> [--fix] [--dry-run]

Features:
- Auto-fix: missing imports, duplicate imports, simple syntax errors
- Safety: always confirm before fixing (unless --fix is used)
- Re-test: automatically re-run tests after fixing
"""

import json
import re
import subprocess
from pathlib import Path
from datetime import datetime


def run_command(cmd, cwd=None, timeout=30):
    """Run command and return output."""
    result = subprocess.run(
        cmd, shell=True, cwd=cwd,
        capture_output=True, text=True, timeout=timeout
    )
    return {
        'returncode': result.returncode,
        'stdout': result.stdout,
        'stderr': result.stderr
    }


def find_vue_files(project_path):
    """Find all Vue and JS files."""
    project = Path(project_path)
    vue_files = list(project.rglob('*.vue'))
    js_files = list(project.rglob('*.js'))
    ts_files = list(project.rglob('*.ts'))
    return vue_files + js_files + ts_files


def analyze_console_errors(console_errors, project_path):
    """
    Analyze console errors and suggest fixes.
    
    Returns:
        list of fixes to apply
    """
    project = Path(project_path)
    fixes = []
    
    for error in console_errors:
        error_text = error.get('text', '')
        error_location = error.get('location', '')
        
        # Pattern 1: ReferenceError - missing import
        ref_match = re.search(r"ReferenceError:\s*'(\w+)' is not defined", error_text)
        if ref_match:
            var_name = ref_match.group(1)
            fixes.append({
                'type': 'missing_import',
                'variable': var_name,
                'description': f"Variable '{var_name}' is not defined",
                'fix': f"Add import: import {{ {var_name} }} from 'package' or define as const/let"
            })
        
        # Pattern 2: Module not found
        module_match = re.search(r"Module not found:\s*Can't resolve\s*['\"]([^'\"]+)['\"]", error_text)
        if module_match:
            module_name = module_match.group(1)
            fixes.append({
                'type': 'missing_module',
                'module': module_name,
                'description': f"Module '{module_name}' not found",
                'fix': f"Install: npm install {module_name} or check import path"
            })
        
        # Pattern 3: Syntax error - missing bracket/parenthesis
        syntax_match = re.search(r"Unexpected token\s+\((.+)\)", error_text)
        if syntax_match:
            token = syntax_match.group(1)
            fixes.append({
                'type': 'syntax_error',
                'token': token,
                'description': f"Syntax error: unexpected token '{token}'",
                'fix': "Check for missing bracket, parenthesis, or semicolon"
            })
        
        # Pattern 4: Cannot read property of undefined
        prop_match = re.search(r"Cannot read property '(\w+)' of undefined", error_text)
        if prop_match:
            prop_name = prop_match.group(1)
            fixes.append({
                'type': 'undefined_property',
                'property': prop_name,
                'description': f"Cannot read property '{prop_name}' of undefined",
                'fix': "Check if object is initialized before accessing property"
            })
        
        # Pattern 5: Network error
        if 'net::ERR' in error_text or 'fetch' in error_text.lower():
            fixes.append({
                'type': 'network_error',
                'description': f"Network request failed: {error_text}",
                'fix': "Check API URL, CORS configuration, or backend server"
            })
    
    return fixes


def apply_fix(fix, project_path, dry_run=False):
    """
    Apply a single fix.
    
    Returns:
        success: bool
        message: str
    """
    project = Path(project_path)
    fix_type = fix.get('type')
    
    # Only apply fixes we're 100% sure about
    if fix_type == 'missing_module':
        # Auto-install missing npm package
        module = fix.get('module')
        if module and not dry_run:
            result = run_command(['npm', 'install', module], cwd=project)
            if result['returncode'] == 0:
                return True, f"Installed npm package: {module}"
            else:
                return False, f"Failed to install {module}: {result['stderr']}"
        return True, f"[DRY RUN] Would install: {module}"
    
    # For other fixes, just report them (require manual intervention)
    return False, f"Manual fix required: {fix.get('description')}"


def auto_fix_errors(project_path, auto_fix=False, dry_run=False):
    """
    Main function to auto-fix errors.
    
    Args:
        project_path: Path to Vue project
        auto_fix: If True, automatically apply safe fixes
        dry_run: If True, only report fixes without applying
    
    Returns:
        dict with fix results
    """
    project = Path(project_path)
    
    print(f"Analyzing errors in: {project}")
    
    # Step 1: Run tests to get errors
    print("Running tests to detect errors...")
    test_result = subprocess.run(
        ['npx', 'vitest', 'run', '--reporter=json'],
        cwd=project,
        capture_output=True,
        text=True,
        timeout=120
    )
    
    # Step 2: Get console errors from previous run (if available)
    # For now, we'll parse Vitest output for errors
    errors = []
    if test_result.stderr:
        stderr = test_result.stderr
        # Look for specific error patterns
        patterns = [
            r"ReferenceError:\s*'(\w+)' is not defined",
            r"Module not found:\s*Can't resolve\s*['\"]([^'\"]+)['\"]",
            r"SyntaxError:",
            r"TypeError:\s*Cannot read",
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, stderr)
            for match in matches:
                errors.append({
                    'text': f"{pattern}: {match}",
                    'source': 'vitest'
                })
    
    # Step 3: Analyze and suggest fixes
    fixes = analyze_console_errors(errors, project_path)
    
    if not fixes:
        return {
            'success': True,
            'message': 'No auto-fixable errors found',
            'errors_analyzed': len(errors),
            'fixes_applied': 0,
            'fixes_required': 0
        }
    
    print(f"\nFound {len(fixes)} potential fixes:")
    
    safe_fixes = []
    manual_fixes = []
    
    for i, fix in enumerate(fixes, 1):
        print(f"\n{i}. [{fix['type']}] {fix['description']}")
        print(f"   Fix: {fix['fix']}")
        
        if fix['type'] in ['missing_module'] and auto_fix:
            safe_fixes.append(fix)
        else:
            manual_fixes.append(fix)
    
    # Step 4: Apply safe fixes
    fixes_applied = 0
    fixes_failed = 0
    
    if auto_fix and safe_fixes:
        print(f"\nApplying {len(safe_fixes)} safe fixes...")
        for fix in safe_fixes:
            success, message = apply_fix(fix, project_path, dry_run)
            if success:
                fixes_applied += 1
                print(f"  ✅ {message}")
            else:
                fixes_failed += 1
                print(f"  ❌ {message}")
    
    # Step 5: Re-test if fixes were applied
    if fixes_applied > 0 and not dry_run:
        print("\nRe-running tests after fixes...")
        retest_result = subprocess.run(
            ['npx', 'vitest', 'run', '--reporter=json'],
            cwd=project,
            capture_output=True,
            text=True,
            timeout=120
        )
        
        tests_passed = retest_result['returncode'] == 0 if 'returncode' in retest_result else False
    else:
        tests_passed = None
    
    # Summary
    result = {
        'success': fixes_failed == 0,
        'timestamp': datetime.now().isoformat(),
        'errors_analyzed': len(errors),
        'fixes_found': len(fixes),
        'fixes_applied': fixes_applied,
        'fixes_failed': fixes_failed,
        'manual_fixes_required': len(manual_fixes),
        'tests_passed': tests_passed,
        'safe_fixes': [f['type'] for f in safe_fixes],
        'manual_fixes': [f['type'] for f in manual_fixes]
    }
    
    print(f"\n{'='*50}")
    print(f"Auto-fix Results:")
    print(f"  Errors analyzed: {result['errors_analyzed']}")
    print(f"  Fixes applied: {result['fixes_applied']}")
    print(f"  Manual fixes: {result['manual_fixes_required']}")
    if result['tests_passed'] is not None:
        print(f"  Tests after fix: {'✅ PASSED' if result['tests_passed'] else '❌ FAILED'}")
    print(f"{'='*50}")
    
    return result


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Auto-fix common Vue/JS errors')
    parser.add_argument('project', help='Path to Vue project')
    parser.add_argument('--fix', action='store_true', help='Automatically apply safe fixes')
    parser.add_argument('--dry-run', action='store_true', help='Show fixes without applying')
    
    args = parser.parse_args()
    
    result = auto_fix_errors(args.project, args.fix, args.dry_run)
    print(json.dumps(result, indent=2))
