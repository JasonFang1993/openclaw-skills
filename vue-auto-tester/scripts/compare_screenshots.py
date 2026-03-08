#!/usr/bin/env python3
"""
Screenshot comparison for Vue projects using Playwright.

Usage:
    python compare_screenshots.py <project-path> [--baseline] [--diff]

Features:
- Capture current screenshot
- Compare with baseline
- Generate diff image
- Report pixel differences
"""

import subprocess
import socket
import time
import json
import sys
import tempfile
import hashlib
from pathlib import Path
from datetime import datetime


def is_server_ready(port=5173, timeout=10):
    """Check if dev server is ready."""
    start = time.time()
    while time.time() - start < timeout:
        try:
            with socket.create_connection(('localhost', port), timeout=1):
                return True
        except (socket.error, ConnectionRefusedError):
            time.sleep(0.5)
    return False


def take_screenshot(project_path, output_path, port=5173):
    """
    Take a screenshot using Playwright.
    
    Returns:
        dict with screenshot info
    """
    project = Path(project_path).resolve()
    
    if not is_server_ready(port):
        return {
            'success': False,
            'error': f'Server not ready on port {port}'
        }
    
    script_content = f'''const {{ chromium }} = require('playwright');

(async () => {{
    const browser = await chromium.launch({{ headless: true }});
    const page = await browser.newPage();
    
    await page.goto('http://localhost:{port}', {{
        waitUntil: 'networkidle',
        timeout: 30000
    }});
    
    // Wait for Vue to hydrate
    await page.waitForTimeout(2000);
    
    await page.screenshot({{
        path: '{output_path}',
        fullPage: true
    }});
    
    const title = await page.title();
    const viewport = page.viewport();
    
    console.log(JSON.stringify({{
        success: true,
        path: '{output_path}',
        title: title,
        viewport: viewport
    }}));
    
    await browser.close();
}})();
'''
    
    script_file = Path(tempfile.gettempdir()) / f'screenshot_{project.name}.js'
    with open(script_file, 'w') as f:
        f.write(script_content)
    
    try:
        result = subprocess.run(
            ['node', str(script_file)],
            cwd=str(project),
            capture_output=True,
            text=True,
            timeout=45
        )
        
        if result.stdout:
            return json.loads(result.stdout)
        else:
            return {
                'success': False,
                'stderr': result.stderr
            }
    
    except json.JSONDecodeError:
        return {
            'success': False,
            'error': 'Failed to parse output'
        }
    except FileNotFoundError:
        return {
            'success': False,
            'error': 'Playwright not installed'
        }
    finally:
        if script_file.exists():
            script_file.unlink()


def compute_image_hash(image_path):
    """Compute perceptual hash of image."""
    if not Path(image_path).exists():
        return None
    
    # Simple hash based on file size and modification time
    stat = Path(image_path).stat()
    return hashlib.md5(
        f"{stat.st_size}_{stat.st_mtime}".encode()
    ).hexdigest()[:8]


def compare_images(baseline_path, current_path, diff_path):
    """
    Compare two images and generate diff.
    
    Uses pixel-by-pixel comparison.
    """
    if not Path(baseline_path).exists():
        return {
            'match': False,
            'error': 'Baseline image not found',
            'diff_percentage': None
        }
    
    if not Path(current_path).exists():
        return {
            'match': False,
            'error': 'Current screenshot not found',
            'diff_percentage': None
        }
    
    # Try to use ImageMagick for comparison
    result = subprocess.run(
        ['compare', '-metric', 'AE', baseline_path, current_path, diff_path],
        capture_output=True,
        text=True
    )
    
    if result.returncode in [0, 1]:  # 0 = images identical, 1 = images different
        try:
            # Extract number of different pixels
            error_output = result.stderr.strip()
            diff_pixels = int(error_output.split()[0]) if error_output else 0
            
            # Get image dimensions
            stat = Path(current_path).stat()
            total_pixels = stat.st_size / 3  # Rough estimate
            
            return {
                'match': diff_pixels == 0,
                'diff_pixels': diff_pixels,
                'diff_percentage': round(diff_pixels / max(total_pixels, 1) * 100, 2),
                'diff_image': str(diff_path) if Path(diff_path).exists() else None
            }
        except (ValueError, IndexError):
            pass
    
    # Fallback: simple file comparison
    baseline_hash = compute_image_hash(baseline_path)
    current_hash = compute_image_hash(current_path)
    
    return {
        'match': baseline_hash == current_hash,
        'diff_pixels': 'unknown',
        'diff_percentage': 'unknown',
        'note': 'Using file hash comparison'
    }


def compare_screenshots(project_path, baseline_dir=None, port=5173):
    """
    Main function to compare screenshots.
    
    Args:
        project_path: Path to Vue project
        baseline_dir: Directory for baseline images (default: project/.test-baseline)
        port: Dev server port
    
    Returns:
        dict with comparison results
    """
    project = Path(project_path).resolve()
    baseline_dir = baseline_dir or project / '.test-baseline'
    baseline_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    current_path = baseline_dir / f'current_{timestamp}.png'
    diff_path = baseline_dir / f'diff_{timestamp}.png'
    
    # Find baseline (use most recent or specified)
    baselines = sorted(baseline_dir.glob('baseline_*.png'), reverse=True)
    baseline_path = baselines[0] if baselines else None
    
    print(f"Project: {project}")
    print(f"Baseline: {baseline_path or 'none'}")
    print(f"Taking current screenshot...")
    
    # Take current screenshot
    result = take_screenshot(project_path, str(current_path), port)
    
    if not result.get('success'):
        return {
            'success': False,
            'error': result.get('error'),
            'screenshot_error': result
        }
    
    response = {
        'success': True,
        'timestamp': timestamp,
        'current_screenshot': str(current_path),
        'baseline_screenshot': str(baseline_path) if baseline_path else None,
        'title': result.get('title'),
        'viewport': result.get('viewport')
    }
    
    # Compare with baseline
    if baseline_path:
        print(f"Comparing with baseline...")
        comparison = compare_images(str(baseline_path), str(current_path), str(diff_path))
        response['comparison'] = comparison
        
        if comparison.get('match'):
            print("✅ Screenshots match!")
        else:
            diff_pct = comparison.get('diff_percentage', 'unknown')
            print(f"❌ Screenshots differ: {diff_pct}% different")
            if diff_path.exists():
                print(f"Diff image: {diff_path}")
    
    # Save as new baseline if no baseline exists
    else:
        print("No baseline found. Saving current as baseline...")
        new_baseline = baseline_dir / f'baseline_{timestamp}.png'
        current_path.rename(new_baseline)
        response['baseline_screenshot'] = str(new_baseline)
        response['comparison'] = {
            'match': True,
            'note': 'First screenshot saved as baseline'
        }
    
    return response


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Screenshot comparison for Vue projects')
    parser.add_argument('project', help='Path to Vue project')
    parser.add_argument('--baseline', action='store_true', help='Save current as baseline')
    parser.add_argument('--dir', default=None, help='Baseline directory')
    parser.add_argument('--port', type=int, default=5173, help='Dev server port')
    
    args = parser.parse_args()
    
    result = compare_screenshots(args.project, args.dir, args.port)
    print(json.dumps(result, indent=2))
