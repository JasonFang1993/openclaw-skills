#!/usr/bin/env python3
"""
Draw.io Diagram Generator - CSV to Draw.io converter

Converts CSV data to Draw.io diagrams using CSV format.
Useful for organizational charts, network topologies, etc.

Usage:
    python csv2drawio.py "csv_data" [--type TYPE]
"""

import sys
import csv
import io

def parse_csv(csv_data):
    """Parse CSV data into a list of dictionaries"""
    reader = csv.DictReader(io.StringIO(csv_data))
    return list(reader)

def generate_csv_diagram(rows, diagram_type="tree"):
    """
    Generate Draw.io CSV format for diagrams
    
    For organizational charts:
    - id: unique identifier
    - label: display text
    - parent: parent node id (empty for root)
    - style: optional styling
    """
    csv_output = io.StringIO()
    writer = csv.writer(csv_output)
    
    # Write header
    writer.writerow(["id", "label", "parent", "style"])
    
    for row in rows:
        row_id = row.get('id', '').strip()
        label = row.get('label', row_id).strip()
        parent = row.get('parent', '').strip()
        style = row.get('style', '').strip()
        
        writer.writerow([row_id, label, parent, style])
    
    return csv_output.getvalue()

def csv_to_drawio_csv(csv_data, diagram_type="tree"):
    """
    Convert CSV to Draw.io CSV format
    
    Args:
        csv_data: CSV string data
        diagram_type: tree (org chart), network, or custom
    
    Returns:
        Draw.io compatible CSV string
    """
    # Parse input CSV
    rows = parse_csv(csv_data)
    
    # Generate output CSV
    csv_output = generate_csv_diagram(rows, diagram_type)
    
    return csv_output

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
    import base64
    compressed = compress_data(data)
    encoded = base64.urlsafe_b64encode(compressed).decode('utf-8')
    return encoded.rstrip('=')

def csv_to_drawio_url(csv_data, title="CSV Diagram", diagram_type="tree"):
    """
    Convert CSV data to Draw.io URL
    
    Args:
        csv_data: CSV string data
        title: Diagram title
        diagram_type: tree, network, etc.
    
    Returns:
        Draw.io URL
    """
    # Convert CSV to Draw.io format
    drawio_csv = csv_to_drawio_csv(csv_data, diagram_type)
    
    # Generate URL with Draw.io CSV import
    # Format: https://www.draw.io/#CSV<csv_data>
    encoded_csv = encode_url(drawio_csv)
    url = f"https://www.draw.io/#CSV{encoded_csv}"
    
    return url

def main():
    """Main CLI interface"""
    if len(sys.argv) < 2:
        print("Usage: python csv2drawio.py <csv_data> [--type TYPE] [--title TITLE]")
        print("\nExample (org chart):")
        print('  python csv2drawio.py "id,label,parent"')
        print('                      "CEO,CEO,"')
        print('                      "VP1,VP Sales,CEO"')
        print('                      "VP2,VP Eng,CEO"')
        sys.exit(1)
    
    csv_data = sys.argv[1]
    
    # Parse flags
    diagram_type = "tree"
    title = "CSV Diagram"
    
    if '--type' in sys.argv:
        idx = sys.argv.index('--type')
        if idx + 1 < len(sys.argv):
            diagram_type = sys.argv[idx + 1]
    
    if '--title' in sys.argv:
        idx = sys.argv.index('--title')
        if idx + 1 < len(sys.argv):
            title = sys.argv[idx + 1]
    
    # Generate URL
    url = csv_to_drawio_url(csv_data, title, diagram_type)
    
    print(f"\n{url}")

if __name__ == "__main__":
    main()
