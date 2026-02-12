#!/usr/bin/env python3
"""
Draw.io Diagram Generator - Mermaid to Draw.io URL converter

This script converts Mermaid diagrams to Draw.io format and generates
a URL that opens the diagram in Draw.io editor.

Usage:
    python mermaid2drawio.py "mermaid_code" [--save FILE]
"""

import sys
import json
import base64
import zlib
try:
    import pako
except ImportError:
    print("Warning: pako not installed, using zlib fallback")
    pako = None

def compress_data(data):
    """Compress data using pako (deflate algorithm)"""
    if pako:
        return pako.deflate(data.encode('utf-8'))
    else:
        # Fallback to zlib
        return zlib.compress(data.encode('utf-8'))

def encode_url(data):
    """Encode compressed data to URL-safe base64"""
    compressed = compress_data(data)
    # URL-safe base64 encoding
    encoded = base64.urlsafe_b64encode(compressed).decode('utf-8')
    # Remove padding
    return encoded.rstrip('=')

def mermaid_to_drawio(mermaid_code, title="Diagram"):
    """
    Convert Mermaid code to Draw.io URL
    
    Args:
        mermaid_code: Mermaid diagram code
        title: Optional title for the diagram
    
    Returns:
        Draw.io URL that opens the diagram
    """
    # Create the Draw.io URL format
    # The URL structure: https://www.draw.io/#Uencoded_data
    
    # Encode the Mermaid code
    encoded_data = encode_url(mermaid_code)
    
    # Build the URL
    url = f"https://www.draw.io/#U{encoded_data}"
    
    return url

def extract_mermaid_from_input(input_text):
    """
    Extract Mermaid code from input text
    Supports:
    - Mermaid code blocks (```mermaid)
    - Raw mermaid code
    """
    # Try to find mermaid code block
    import re
    
    # Check for mermaid code block
    pattern = r'```mermaid\n([\s\S]*?)```'
    matches = re.findall(pattern, input_text)
    
    if matches:
        return matches[0].strip()
    
    # If no code block, assume entire input is mermaid code
    return input_text.strip()

def main():
    """Main CLI interface"""
    if len(sys.argv) < 2:
        print("Usage: python mermaid2drawio.py <mermaid_code> [--title TITLE]")
        print("\nExample:")
        print('  python mermaid2drawio.py "graph TD; A-->B; B-->C;"')
        print("\nOr with a code block:")
        print('  python mermaid2drawio.py """')
        print('  graph TD')
        print('      A[Start] --> B{Is it working?}')
        print('      B -->|Yes| C[Great!]')
        print('      B -->|No| D[Debug]')
        print('  """')
        sys.exit(1)
    
    # Get input
    mermaid_code = sys.argv[1]
    
    # Check for title flag
    title = "Diagram"
    if '--title' in sys.argv:
        idx = sys.argv.index('--title')
        if idx + 1 < len(sys.argv):
            title = sys.argv[idx + 1]
    
    # Extract mermaid code if wrapped in code block markers
    mermaid_code = extract_mermaid_from_input(mermaid_code)
    
    # Generate URL
    url = mermaid_to_drawio(mermaid_code, title)
    
    print(f"\n{url}")

if __name__ == "__main__":
    main()
