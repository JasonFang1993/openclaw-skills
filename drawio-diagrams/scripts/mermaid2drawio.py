#!/usr/bin/env python3
"""
Draw.io Diagram Generator - Mermaid to Draw.io XML converter

This script converts Mermaid diagrams to Draw.io XML format.
"""

import sys
import re

def parse_mermaid_to_xml(mermaid_code, title="Diagram"):
    """
    Parse Mermaid code and convert to Draw.io XML format
    """
    cells = []
    cell_id = 0
    node_map = {}  # node_id -> cell_id

    lines = mermaid_code.strip().split('\n')
    x_pos = 100
    y_pos = 100

    for line in lines:
        line = line.strip()
        if not line or line.startswith('%%') or line.startswith('graph '):
            continue

        # Extract node ID and label from "A[Label]" or "A{Label}"
        node_def_match = re.match(r'^(\w+)\[(.+)\]\s*$', line)
        if node_def_match:
            node_id = node_def_match.group(1)
            label = node_def_match.group(2)
            cell_id += 1
            cells.append(f'''        <mxCell id="{cell_id}" value="{label}" vertex="1" parent="1">
            <mxGeometry as="geometry" x="{x_pos}" y="{y_pos}" width="120" height="60"/>
        </mxCell>''')
            node_map[node_id] = cell_id
            x_pos += 150
            if x_pos > 800:
                x_pos = 100
                y_pos += 100
            continue

        # Extract decision node "A{Decision}"
        decision_match = re.match(r'^(\w+)\{(.+)\}\s*$', line)
        if decision_match:
            node_id = decision_match.group(1)
            label = decision_match.group(2)
            cell_id += 1
            cells.append(f'''        <mxCell id="{cell_id}" value="{label}" vertex="1" parent="1" style="rhombus;whiteSpace=wrap;html=1;">
            <mxGeometry as="geometry" x="{x_pos}" y="{y_pos}" width="120" height="80"/>
        </mxCell>''')
            node_map[node_id] = cell_id
            x_pos += 150
            if x_pos > 800:
                x_pos = 100
                y_pos += 100
            continue

        # Parse edge: "A --> B" or "A -->|label| B" or "A --> B{Decision}"
        # First, extract node IDs from the line
        edge_match = re.match(r'^(\w+)\s*-->\s*(?:\|([^|]+)\|)?\s*(\w+)', line)
        if edge_match:
            source = edge_match.group(1)
            edge_label = edge_match.group(2) or ''
            target = edge_match.group(3)

            # Create source node if not exists
            if source not in node_map:
                cell_id += 1
                cells.append(f'''        <mxCell id="{cell_id}" value="{source}" vertex="1" parent="1">
            <mxGeometry as="geometry" x="{x_pos}" y="{y_pos}" width="120" height="60"/>
        </mxCell>''')
                node_map[source] = cell_id
                x_pos += 150
                if x_pos > 800:
                    x_pos = 100
                    y_pos += 100

            # Create target node if not exists (could be decision node)
            if target not in node_map:
                if target.startswith('{') and target.endswith('}'):
                    # Decision node
                    label = target[1:-1]
                    cell_id += 1
                    cells.append(f'''        <mxCell id="{cell_id}" value="{label}" vertex="1" parent="1" style="rhombus;whiteSpace=wrap;html=1;">
            <mxGeometry as="geometry" x="{x_pos}" y="{y_pos}" width="120" height="80"/>
        </mxCell>''')
                else:
                    cell_id += 1
                    cells.append(f'''        <mxCell id="{cell_id}" value="{target}" vertex="1" parent="1">
            <mxGeometry as="geometry" x="{x_pos}" y="{y_pos}" width="120" height="60"/>
        </mxCell>''')
                node_map[target] = cell_id
                x_pos += 150
                if x_pos > 800:
                    x_pos = 100
                    y_pos += 100

            # Create edge
            cell_id += 1
            cells.append(f'''        <mxCell id="{cell_id}" value="{edge_label}" edge="1" source="{node_map[source]}" target="{node_map[target]}" parent="1">
            <mxGeometry as="geometry" relative="1"/>
        </mxCell>''')
            continue

    # Build XML
    if cells:
        cells_str = '\n'.join(cells)
        xml = f'''<mxfile host="draw.io" agent="Python" version="1.0">
  <diagram name="{title}">
    <mxGraphModel dx="1422" dy="794" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1169" pageHeight="827">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        <mxCell id="2" value="{title}" vertex="1" parent="1">
          <mxGeometry as="geometry" x="284" y="20" width="600" height="40"/>
        </mxCell>
{cells_str}
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>'''
    else:
        # Fallback: show Mermaid code as text box
        escaped_code = mermaid_code.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')
        xml = f'''<mxfile host="draw.io" agent="Python" version="1.0">
  <diagram name="{title}">
    <mxGraphModel dx="1422" dy="794" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1169" pageHeight="827">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        <mxCell id="2" value="{title}" vertex="1" parent="1">
          <mxGeometry as="geometry" x="284" y="20" width="600" height="40"/>
        </mxCell>
        <mxCell id="3" value="&lt;b&gt;Mermaid Code:&lt;/b&gt;&lt;pre&gt;{escaped_code}&lt;/pre&gt;" vertex="1" parent="1">
          <mxGeometry as="geometry" x="100" y="80" width="900" height="500"/>
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>'''

    return xml

def extract_mermaid_from_input(input_text):
    """Extract Mermaid code from input text"""
    # Check for mermaid code block
    pattern = r'```mermaid\n([\s\S]*?)```'
    matches = re.findall(pattern, input_text)
    if matches:
        return matches[0].strip()
    return input_text.strip()

def main():
    """Main CLI interface"""
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
    xml = parse_mermaid_to_xml(mermaid_code, title)

    # Output XML for manual import
    print(xml)
    print("\n" + "="*60)
    print("Import to Draw.io:")
    print("1. Open https://www.draw.io")
    print("2. File > Import > Paste XML above")
    print("="*60)

if __name__ == "__main__":
    main()
