#!/usr/bin/env python3
"""
Draw.io Diagram Generator - Mermaid to Draw.io XML converter

Generates Draw.io XML format that can be imported directly.
"""

import sys
import re

def mermaid_to_drawio_xml(mermaid_code, title="Diagram"):
    """
    Parse Mermaid code and convert to Draw.io XML format
    """
    cells = []
    cell_id = 0
    node_map = {}  # node_id -> cell_id
    node_positions = {}  # node_id -> (x, y)
    edges = []  # (source_id, target_id, edge_label)
    
    x_pos = 100
    y_pos = 50

    lines = mermaid_code.strip().split('\n')

    for line in lines:
        line = line.strip()
        if not line or line.startswith('%%') or line.startswith('graph '):
            continue

        # Split by arrow
        if '-->' in line:
            parts = line.split('-->')
            if len(parts) == 2:
                source = parts[0].strip()
                rest = parts[1].strip()
                
                # Extract source node ID and label
                source_match = re.match(r'^(\w+)\[(.+)\]', source)
                if source_match:
                    source_id = source_match.group(1)
                    source_label = source_match.group(2)
                else:
                    source_match = re.match(r'^(\w+)', source)
                    source_id = source_match.group(1) if source_match else source
                    source_label = source_id
                
                # Register source
                if source_id not in node_positions:
                    node_positions[source_id] = (x_pos, y_pos, source_label)
                    x_pos += 150
                    if x_pos > 700:
                        x_pos = 100
                        y_pos += 100
                
                # Check for label: |label|
                label_match = re.match(r'\|(.+)\|\s*(.+)', rest)
                if label_match:
                    edge_label = label_match.group(1)
                    target = label_match.group(2).strip()
                else:
                    edge_label = ''
                    target = rest.strip()
                
                # Extract target node ID and label
                target_match = re.match(r'^(\w+)\[(.+)\]', target)
                if target_match:
                    target_id = target_match.group(1)
                    target_label = target_match.group(2)
                # Decision node: B{Decision}
                elif re.match(r'^(\w+)\{.+\}', target):
                    target_match = re.match(r'^(\w+)\{(.+)\}', target)
                    if target_match:
                        target_id = target_match.group(1)
                        target_label = target_match.group(2)
                    else:
                        target_id = target
                        target_label = target
                else:
                    target_match = re.match(r'^(\w+)', target)
                    target_id = target_match.group(1) if target_match else target
                    target_label = target_id
                
                # Register target
                if target_id not in node_positions:
                    node_positions[target_id] = (x_pos, y_pos, target_label)
                    x_pos += 150
                    if x_pos > 700:
                        x_pos = 100
                        y_pos += 100
                
                edges.append((source_id, target_id, edge_label))

        # Check for standalone node: "A[Label]"
        elif '[' in line and ']' in line:
            node_match = re.match(r'^(\w+)\[(.+)\]\s*$', line)
            if node_match:
                node_id = node_match.group(1)
                if node_id not in node_map:
                    node_positions[node_id] = (x_pos, y_pos)
                    x_pos += 150
                    if x_pos > 700:
                        x_pos = 100
                        y_pos += 100

    # Create cells for nodes (with unique IDs)
    for label, (x, y, display) in node_positions.items():
        cell_id += 1
        node_map[label] = cell_id
        
        cells.append(f'''        <mxCell id="{cell_id}" value="{display}" vertex="1" parent="1">
          <mxGeometry as="geometry" x="{x}" y="{y}" width="120" height="60"/>
        </mxCell>''')

    # Create edges
    for source, target, edge_label in edges:
        source_id = node_map.get(source)
        target_id = node_map.get(target)
        
        if source_id and target_id:
            cell_id += 1
            cells.append(f'''        <mxCell id="{cell_id}" value="{edge_label}" edge="1" source="{source_id}" target="{target_id}" parent="1">
          <mxGeometry as="geometry" relative="1"/>
        </mxCell>''')

    # Build XML
    cells_str = '\n'.join(cells)
    xml = f'''<mxfile host="draw.io" version="1.0">
  <diagram name="{title}">
    <mxGraphModel dx="1422" dy="794" grid="1" gridSize="10">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        <mxCell id="2" value="{title}" vertex="1" parent="1">
          <mxGeometry as="geometry" x="200" y="10" width="400" height="30"/>
        </mxCell>
{cells_str}
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>'''

    return xml

def extract_mermaid_from_input(input_text):
    """Extract Mermaid code from input text"""
    pattern = r'```mermaid\n([\s\S]*?)```'
    matches = re.findall(pattern, input_text)
    if matches:
        return matches[0].strip()
    return input_text.strip()

def main():
    if len(sys.argv) < 2:
        print("Usage: python mermaid2drawio.py <mermaid_code> [--title TITLE]")
        sys.exit(1)

    mermaid_code = sys.argv[1]
    title = "Diagram"

    if '--title' in sys.argv:
        idx = sys.argv.index('--title')
        if idx + 1 < len(sys.argv):
            title = sys.argv[idx + 1]

    mermaid_code = extract_mermaid_from_input(mermaid_code)
    xml = mermaid_to_drawio_xml(mermaid_code, title)

    print(xml)
    print("\n" + "="*60)
    print("Import to Draw.io:")
    print("1. File > Import")
    print("2. Paste XML above")
    print("3. Click 'Open'")
    print("="*60)

if __name__ == "__main__":
    main()
