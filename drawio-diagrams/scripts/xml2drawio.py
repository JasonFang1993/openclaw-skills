#!/usr/bin/env python3
"""
Draw.io Diagram Generator - XML to Draw.io converter

Converts Draw.io native XML format to a URL that opens in Draw.io editor.
Useful when you have existing Draw.io XML or want fine-grained control.

Usage:
    python xml2drawio.py "xml_data" [--save FILE]
"""

import sys
import base64
try:
    import pako
except ImportError:
    pako = None
    print("Warning: pako not installed, using zlib fallback")

def compress_data(data):
    """Compress data using raw deflate (compatible with Draw.io)"""
    import zlib
    try:
        compressor = zlib.compressobj(zlib.Z_DEFAULT_COMPRESSION, zlib.DEFLATED, -zlib.MAX_WBITS)
        return compressor.compress(data.encode('utf-8')) + compressor.flush()
    except Exception:
        return zlib.compress(data.encode('utf-8'))

def encode_url(data):
    """Encode compressed data to URL-safe base64"""
    compressed = compress_data(data)
    encoded = base64.urlsafe_b64encode(compressed).decode('utf-8')
    return encoded.rstrip('=')

def xml_to_drawio_url(xml_data, title="XML Diagram"):
    """
    Convert Draw.io XML to URL
    
    Args:
        xml_data: Draw.io XML format string
        title: Optional diagram title
    
    Returns:
        Draw.io URL that opens the diagram
    """
    encoded_data = encode_url(xml_data)
    url = f"https://www.draw.io/#U{encoded_data}"
    return url

def extract_xml_from_input(input_text):
    """Extract XML code from input"""
    import re
    
    # Check for xml code block
    pattern = r'```xml\n([\s\S]*?)```'
    matches = re.findall(pattern, input_text)
    
    if matches:
        return matches[0].strip()
    
    # Check for Draw.io specific format
    pattern = r'<mxGraphModel>([\s\S]*?)</mxGraphModel>'
    matches = re.findall(pattern, input_text)
    
    if matches:
        return f'<mxGraphModel>{matches[0]}</mxGraphModel>'
    
    return input_text.strip()

def main():
    """Main CLI interface"""
    if len(sys.argv) < 2:
        print("Usage: python xml2drawio.py <xml_data> [--title TITLE]")
        print("\nExample:")
        print('  python xml2drawio.py """')
        print('  <mxGraphModel>')
        print('    <root>')
        print('      <mxCell id="0"/>')
        print('      <mxCell id="1" parent="0"/>')
        print('      <mxCell id="2" value="Start" vertex="1" parent="1">')
        print('        <mxGeometry as="geometry" width="80" height="30"/>')
        print('      </mxCell>')
        print('    </root>')
        print('  </mxGraphModel>')
        print('  """')
        sys.exit(1)
    
    xml_data = sys.argv[1]
    xml_data = extract_xml_from_input(xml_data)
    
    # Check for title flag
    title = "XML Diagram"
    if '--title' in sys.argv:
        idx = sys.argv.index('--title')
        if idx + 1 < len(sys.argv):
            title = sys.argv[idx + 1]
    
    url = xml_to_drawio_url(xml_data, title)
    
    print(f"\n{url}")

if __name__ == "__main__":
    main()
