#!/usr/bin/env python3
"""
Check console errors using Playwright.

Usage:
    python check_console_errors.py <project-path> [--port PORT]
"""

import subprocess
import socket
import time
import json
import sys
import tempfile
from pathlib import Path


def is_server_ready(port, timeout=10):
    """Check if server is ready."""
    start = time.time()
    while time.time() - start < timeout:
        try:
            with socket.create_connection(('localhost', port), timeout=1):
                return True
        except (socket.error, ConnectionRefusedError):
            time.sleep(0.5)
    return False


def check_console_errors(project_path, port=5173, timeout=30):
    """
    Check for console errors using Playwright.
    
    Returns:
        dict with:
        - errors: list of console errors
        - page_errors: list of page errors
        - warnings: list of console warnings
    """
    project = Path(project_path).resolve()
    
    if not is_server_ready(port):
        return {
            'status': 'failed',
            'error': f'Server not ready on port {port}',
            'errors': [],
            'warnings': []
        }
    
    # Create Playwright script
    script_content = '''const { chromium } = require('playwright');

(async () => {
    const browser = await chromium.launch({ headless: true });
    const context = await browser.newContext();
    const page = await context.newPage();
    
    const errors = [];
    const warnings = [];
    const pageErrors = [];
    const networkErrors = [];
    
    // Capture console messages
    page.on('console', msg => {
        if (msg.type() === 'error') {
            errors.push({
                text: msg.text(),
                location: msg.location() ? JSON.stringify(msg.location()) : 'unknown'
            });
        } else if (msg.type() === 'warning') {
            warnings.push({
                text: msg.text(),
                location: msg.location() ? JSON.stringify(msg.location()) : 'unknown'
            });
        }
    });
    
    // Capture page errors
    page.on('pageerror', err => {
        pageErrors.push({
            message: err.message,
            stack: err.stack || 'no stack'
        });
    });
    
    // Capture failed network requests
    page.on('requestfailed', request => {
        networkErrors.push({
            url: request.url(),
            failure: request.failure() ? request.failure().errorText : 'unknown'
        });
    });
    
    try {
        // Navigate and wait for network to be idle
        await page.goto(`http://localhost:${PORT}`, { 
            waitUntil: 'networkidle',
            timeout: 30000 
        });
        
        // Wait a bit for any delayed errors
        await page.waitForTimeout(2000);
        
        // Check if page has meaningful content
        const title = await page.title();
        const bodyText = await page.evaluate(() => document.body?.innerText?.substring(0, 100) || '');
        
        console.log(JSON.stringify({
            status: 'success',
            title: title,
            body_preview: bodyText,
            errors: errors,
            warnings: warnings,
            page_errors: pageErrors,
            network_errors: networkErrors
        }));
        
    } catch (err) {
        console.log(JSON.stringify({
            status: 'error',
            error: err.message,
            errors: errors,
            warnings: warnings,
            page_errors: pageErrors,
            network_errors: networkErrors
        }));
    }
    
    await browser.close();
})();
'''.replace('${PORT}', str(port))
    
    # Write temporary script
    script_file = Path(tempfile.gettempdir()) / f'check_console_{project.name}.js'
    with open(script_file, 'w') as f:
        f.write(script_content)
    
    try:
        # Run Playwright script
        result = subprocess.run(
            ['node', str(script_file)],
            cwd=str(project),
            capture_output=True,
            text=True,
            timeout=timeout
        )
        
        # Parse output
        if result.stdout:
            try:
                return json.loads(result.stdout)
            except json.JSONDecodeError:
                return {
                    'status': 'parse_error',
                    'raw_output': result.stdout[:500],
                    'errors': [],
                    'warnings': []
                }
        
        return {
            'status': 'no_output',
            'stderr': result.stderr,
            'errors': [],
            'warnings': []
        }
    
    except subprocess.TimeoutExpired:
        return {
            'status': 'timeout',
            'error': 'Playwright script timed out',
            'errors': [],
            'warnings': []
        }
    except FileNotFoundError:
        return {
            'status': 'missing_dependency',
            'error': 'Playwright not installed. Run: npm install -D @playwright/test && npx playwright install chromium',
            'errors': [],
            'warnings': []
        }
    finally:
        # Cleanup
        if script_file.exists():
            script_file.unlink()


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Check console errors with Playwright')
    parser.add_argument('project', help='Path to Vue project')
    parser.add_argument('--port', type=int, default=5173, help='Dev server port')
    parser.add_argument('--timeout', type=int, default=30, help='Timeout in seconds')
    
    args = parser.parse_args()
    
    result = check_console_errors(args.project, args.port, args.timeout)
    print(json.dumps(result, indent=2))
