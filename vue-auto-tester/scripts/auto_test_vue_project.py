#!/usr/bin/env python3
"""
Auto-test Vue projects using Vitest and Playwright.

Usage:
    python auto_test_vue_project.py <project-path> [--screenshot] [--fix-errors]
"""

import subprocess
import socket
import time
import json
import tempfile
from pathlib import Path
from datetime import datetime


def is_server_ready(port, timeout=30):
    """Wait for dev server to be ready."""
    start = time.time()
    while time.time() - start < timeout:
        try:
            with socket.create_connection(('localhost', port), timeout=1):
                return True
        except (socket.error, ConnectionRefusedError):
            time.sleep(0.5)
    return False


def run_command(cmd, cwd=None, timeout=60):
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


def check_console_errors(project_path, port=5173, timeout=30):
    """Check console errors using Playwright."""
    project = Path(project_path).resolve()
    
    script_content = f'''const {{ chromium }} = require('playwright');

(async () => {{
    const browser = await chromium.launch({{ headless: true }});
    const page = await browser.newPage();
    
    const errors = [], warnings = [], pageErrors = [], networkErrors = [];
    
    page.on('console', msg => {{
        if (msg.type() === 'error') errors.push({{ text: msg.text(), location: JSON.stringify(msg.location()) }});
        else if (msg.type() === 'warning') warnings.push({{ text: msg.text() }});
    }});
    
    page.on('pageerror', err => pageErrors.push({{ message: err.message, stack: err.stack }}));
    page.on('requestfailed', req => networkErrors.push({{ url: req.url(), failure: req.failure()?.errorText }}));
    
    try {{
        await page.goto(`http://localhost:{port}`, {{ waitUntil: 'networkidle', timeout: 30000 }});
        await page.waitForTimeout(2000);
        console.log(JSON.stringify({{ status: 'success', title: await page.title(), errors, warnings, page_errors: pageErrors, network_errors: networkErrors }}));
    }} catch (err) {{
        console.log(JSON.stringify({{ status: 'error', error: err.message, errors, warnings, page_errors: pageErrors, network_errors: networkErrors }}));
    }}
    
    await browser.close();
}})();
'''
    
    script_file = Path(tempfile.gettempdir()) / 'check_console.js'
    with open(script_file, 'w') as f:
        f.write(script_content)
    
    try:
        result = subprocess.run(['node', str(script_file)], cwd=str(project), capture_output=True, text=True, timeout=timeout)
        if result.stdout:
            return json.loads(result.stdout)
    except Exception:
        pass
    finally:
        if script_file.exists():
            script_file.unlink()
    
    return {'status': 'failed', 'error': 'Unable to check console errors'}


def take_screenshot(project_path, output_path, port=5173):
    """Take screenshot using Playwright."""
    project = Path(project_path).resolve()
    
    script = f'''const {{ chromium }} = require('playwright');
(async () => {{
    const browser = await chromium.launch({{ headless: true }});
    const page = await browser.newPage();
    await page.goto('http://localhost:{port}', {{ waitUntil: 'networkidle', timeout: 30000 }});
    await page.waitForTimeout(2000);
    await page.screenshot({{ path: '{output_path}', fullPage: true }});
    console.log(JSON.stringify({{ success: true, path: '{output_path}', title: await page.title() }}));
    await browser.close();
}})();
'''
    
    script_file = Path(tempfile.gettempdir()) / 'screenshot.js'
    with open(script_file, 'w') as f:
        f.write(script)
    
    try:
        result = subprocess.run(['node', str(script_file)], cwd=str(project), capture_output=True, text=True, timeout=45)
        if result.stdout:
            return json.loads(result.stdout)
    except Exception:
        pass
    finally:
        if script_file.exists():
            script_file.unlink()
    
    return {'success': False, 'error': 'Failed to take screenshot'}


def compare_images(baseline_path, current_path):
    """Simple image comparison using file hash."""
    if not Path(baseline_path).exists() or not Path(current_path).exists():
        return {'match': False, 'error': 'Missing images'}
    
    import hashlib
    def file_hash(p):
        with open(p, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    
    bh, ch = file_hash(baseline_path), file_hash(current_path)
    return {'match': bh == ch, 'baseline_hash': bh, 'current_hash': ch}


def auto_test_vue_project(project_path, take_screenshot=False, fix_errors=False, baseline_screenshot=False):
    """
    Main function to auto-test Vue project.
    """
    project = Path(project_path).resolve()
    port = 5173
    
    if not project.exists():
        return {'success': False, 'error': f'Project not found: {project}'}
    
    print(f"Testing Vue project: {project}")
    
    # Check package.json
    package_json = project / 'package.json'
    if not package_json.exists():
        return {'success': False, 'error': 'No package.json found'}
    
    with open(package_json) as f:
        pkg = json.load(f)
    
    has_vitest = 'vitest' in pkg.get('devDependencies', {})
    print(f"Vitest configured: {has_vitest}")
    
    results = {
        'project': str(project),
        'timestamp': datetime.now().isoformat(),
        'dev_server': {'status': 'pending'},
        'console_errors': [],
        'console_warnings': [],
        'page_errors': [],
        'network_errors': [],
        'vitest_results': {'status': 'pending'},
        'screenshot': None,
        'screenshot_comparison': None
    }
    
    # Start dev server
    print("Starting dev server...")
    dev_process = subprocess.Popen(
        ['npm', 'run', 'dev'],
        cwd=project,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    try:
        if is_server_ready(port):
            results['dev_server'] = {'status': 'ready', 'port': port}
            print("Dev server ready on port", port)
            
            # Step 3: Check console errors
            print("Checking console errors...")
            console_result = check_console_errors(project_path, port)
            results['console_errors'] = console_result.get('errors', [])
            results['console_warnings'] = console_result.get('warnings', [])
            results['page_errors'] = console_result.get('page_errors', [])
            results['network_errors'] = console_result.get('network_errors', [])
            
            if console_result.get('status') == 'success':
                print(f"Console: {len(results['console_errors'])} errors, {len(results['console_warnings'])} warnings")
            else:
                print(f"Console check: {console_result.get('status')}")
            
            # Step 4: Screenshot comparison
            if take_screenshot or baseline_screenshot:
                print("Taking screenshot...")
                baseline_dir = project / '.test-baseline'
                baseline_dir.mkdir(exist_ok=True)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                current_path = baseline_dir / f'current_{timestamp}.png'
                
                screenshot_result = take_screenshot(project_path, str(current_path), port)
                
                if screenshot_result.get('success'):
                    results['screenshot'] = str(current_path)
                    
                    # Find existing baseline
                    baselines = sorted(baseline_dir.glob('baseline_*.png'), reverse=True)
                    
                    if baseline_screenshot:
                        # Save as new baseline
                        new_baseline = baseline_dir / f'baseline_{timestamp}.png'
                        current_path.rename(new_baseline)
                        results['screenshot_comparison'] = {'match': True, 'note': 'Saved as new baseline'}
                        print("Saved as new baseline")
                    
                    elif baselines:
                        # Compare with latest baseline
                        baseline_path = baselines[0]
                        comparison = compare_images(str(baseline_path), str(current_path))
                        results['screenshot_comparison'] = {
                            'baseline': str(baseline_path),
                            **comparison
                        }
                        
                        if comparison.get('match'):
                            print("Screenshot: ✅ Match!")
                        else:
                            print("Screenshot: ❌ Different from baseline")
                    
                    else:
                        # First screenshot - save as baseline
                        new_baseline = baseline_dir / f'baseline_{timestamp}.png'
                        current_path.rename(new_baseline)
                        results['screenshot_comparison'] = {'match': True, 'note': 'First screenshot saved as baseline'}
                        print("First screenshot saved as baseline")
            
            # Step 5: Run Vitest
            if has_vitest:
                print("Running Vitest...")
                vitest_result = run_command(
                    ['npx', 'vitest', 'run', '--reporter=json'],
                    cwd=project,
                    timeout=120
                )
                results['vitest_results'] = {
                    'status': 'completed',
                    'returncode': vitest_result['returncode'],
                    'output': (vitest_result['stdout'][:3000] + vitest_result['stderr'][:1000]) if vitest_result['stderr'] else vitest_result['stdout'][:3000]
                }
                print(f"Vitest: returncode={vitest_result['returncode']}")
                if vitest_result['returncode'] == 0:
                    print("All tests passed!")
                else:
                    print("Some tests failed")
        
        else:
            results['dev_server'] = {'status': 'failed', 'error': 'Server failed to start'}
            print("Dev server failed to start")
    
    finally:
        dev_process.terminate()
        try:
            dev_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            dev_process.kill()
        print("Server stopped")
    
    # Step 6: Auto-fix errors if enabled
    if fix_errors and results.get('console_errors'):
        print("\nAttempting auto-fix for errors...")
        fix_script = Path(__file__).parent / 'auto_fix_errors.py'
        
        if fix_script.exists():
            fix_result = subprocess.run(
                ['python3', str(fix_script), str(project), '--fix'],
                capture_output=True,
                text=True,
                timeout=180
            )
            
            if fix_result.stdout:
                try:
                    fix_data = json.loads(fix_result.stdout)
                    results['auto_fix'] = fix_data
                    
                    fixes_applied = fix_data.get('fixes_applied', 0)
                    manual_fixes = fix_data.get('manual_fixes_required', 0)
                    
                    if fixes_applied > 0:
                        print(f"Auto-fixed {fixes_applied} errors")
                    if manual_fixes > 0:
                        print(f"{manual_fixes} errors require manual intervention")
                    
                    # Update success based on fix result
                    if fix_data.get('tests_passed') is False:
                        results['success'] = False
                        print("Tests still failing after auto-fix")
                except json.JSONDecodeError:
                    print("Auto-fix: failed to parse output")
        else:
            print("Auto-fix script not found")
    
    # Determine success
    results['success'] = (
        results['dev_server']['status'] == 'ready' and
        results['vitest_results'].get('returncode', 1) == 0 and
        not results.get('visual_regression') and
        (results.get('auto_fix', {}).get('tests_passed', True) or not results.get('auto_fix'))
    )
    
    print(f"\n{'TEST PASSED' if results['success'] else 'TEST FAILED'}")
    return results


def run_vitest_tests(project_path, reporter='json'):
    """Run Vitest tests only."""
    project = Path(project_path).resolve()
    print(f"Running Vitest: {project}")
    
    result = subprocess.run(
        ['npx', 'vitest', 'run', f'--reporter={reporter}'],
        cwd=project,
        capture_output=True,
        text=True,
        timeout=120
    )
    
    return {
        'returncode': result.returncode,
        'stdout': result.stdout,
        'stderr': result.stderr
    }


def check_component(component_name, project_path):
    """Check Vue component structure."""
    project = Path(project_path).resolve()
    components_dir = project / 'src' / 'components'
    
    if not components_dir.exists():
        return {'error': 'Components directory not found'}
    
    component_files = list(components_dir.glob(f'{component_name}.vue')) + \
                     list(components_dir.glob(f'{component_name}.{jsx,tsx}'))
    
    if not component_files:
        return {'error': f'Component not found: {component_name}'}
    
    component = component_files[0]
    print(f"Checking component: {component}")
    
    with open(component) as f:
        content = f.read()
    
    import re
    results = {
        'component': str(component),
        'exists': True,
        'has_script': '<script' in content,
        'has_template': '<template>' in content,
        'has_style': '<style' in content,
        'props': [],
        'issues': []
    }
    
    if '<script' in content:
        props_match = re.search(r'props:\s*\{([^}]+)\}', content)
        if props_match:
            props_str = props_match.group(1)
            results['props'] = [p.strip().split(':')[0].strip().strip("'\"") 
                              for p in props_str.split(',')]
    
    if not results['has_script']:
        results['issues'].append('Missing <script> tag')
    if not results['has_template']:
        results['issues'].append('Missing <template> tag')
    if not results['has_style']:
        results['issues'].append('Missing <style> tag')
    
    print(f"Props: {results['props']}")
    print(f"Issues: {results['issues']}")
    
    return results


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Auto-test Vue projects')
    parser.add_argument('project', help='Path to Vue project')
    parser.add_argument('--screenshot', action='store_true', help='Take screenshot and compare')
    parser.add_argument('--baseline', action='store_true', help='Save current as baseline')
    parser.add_argument('--fix', action='store_true', help='Auto-fix errors')
    parser.add_argument('--check', metavar='COMPONENT', help='Check component')
    parser.add_argument('--vitest-only', action='store_true', help='Run Vitest only')
    
    args = parser.parse_args()
    
    if args.check:
        result = check_component(args.check, args.project)
        print(json.dumps(result, indent=2))
    elif args.vitest_only:
        result = run_vitest_tests(args.project)
        print(json.dumps(result, indent=2))
    else:
        result = auto_test_vue_project(args.project, args.screenshot, args.fix, args.baseline)
        print(json.dumps(result, indent=2))
