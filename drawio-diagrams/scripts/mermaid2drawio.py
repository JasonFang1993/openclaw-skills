#!/usr/bin/env python3
"""
Draw.io Diagram Generator - Mermaid to PlantUML converter
"""

import sys
import re

def mermaid_to_plantuml(mermaid_code, title="Diagram"):
    """Convert Mermaid code to PlantUML format"""
    lines = mermaid_code.strip().split('\n')
    
    # Map: node_id -> label
    node_map = {}  # A -> 用户发送消息, B -> (AI识别意图)
    node_types = {}  # A -> rectangle, B -> decision
    
    # Parse all lines
    all_lines = []
    for line in lines:
        line = line.strip()
        if not line or line.startswith('%%') or line.startswith('graph '):
            continue
        
        # Store original for processing
        all_lines.append(line)
    
    # First pass: extract all node definitions
    for line in all_lines:
        # Check for node definition: A[Label] or A{Decision}
        def_match = re.match(r'^(\w+)\[(.+)\]\s*$', line)
        if def_match:
            node_id = def_match.group(1)
            label = def_match.group(2)
            node_map[node_id] = label
            node_types[node_id] = 'rectangle'
            continue
        
        def_match = re.match(r'^(\w+)\{(.+)\}\s*$', line)
        if def_match:
            node_id = def_match.group(1)
            label = def_match.group(2)
            node_map[node_id] = label
            node_types[node_id] = 'decision'
            continue
        
        # Also check for inline definitions in edges
        if '-->' in line:
            parts = line.split('-->')
            for part in parts:
                part = part.strip()
                # A[Label]
                m = re.search(r'(\w+)\[(.+)\]', part)
                if m:
                    node_id = m.group(1)
                    label = m.group(2)
                    if node_id not in node_map:
                        node_map[node_id] = label
                        node_types[node_id] = 'rectangle'
                # A{Decision}
                m = re.search(r'(\w+)\{(.+)\}', part)
                if m:
                    node_id = m.group(1)
                    label = m.group(2)
                    if node_id not in node_map:
                        node_map[node_id] = label
                        node_types[node_id] = 'decision'
    
    # Build PlantUML
    output = ['@startuml', f'title {title}', '']
    
    # Add nodes
    for node_id, label in node_map.items():
        if node_types.get(node_id) == 'decision':
            output.append(f'({label})')
        else:
            output.append(f'rectangle "{label}"')
    
    output.append('')
    
    # Second pass: process edges
    for line in all_lines:
        if '-->' not in line:
            continue
        
        parts = line.split('-->')
        if len(parts) < 2:
            continue
        
        # Process source
        source_part = parts[0].strip()
        source_id_match = re.match(r'^(\w+)', source_part)
        source_id = source_id_match.group(1) if source_id_match else source_part
        
        # Get source label
        if source_id in node_map:
            if node_types.get(source_id) == 'decision':
                source = f'({node_map[source_id]})'
            else:
                source = node_map[source_id]
        else:
            source = source_id
        
        # Process target
        target_part = parts[1].strip()
        
        # Check for edge label
        label_match = re.search(r'\|(.+)\|', target_part)
        edge_label = label_match.group(1) if label_match else ''
        
        # Extract target ID
        clean_target = re.sub(r'\|.+\|', '', target_part).strip()
        target_id_match = re.match(r'^(\w+)', clean_target)
        target_id = target_id_match.group(1) if target_id_match else clean_target
        
        # Get target label
        if target_id in node_map:
            if node_types.get(target_id) == 'decision':
                target = f'({node_map[target_id]})'
            else:
                target = node_map[target_id]
        else:
            target = target_id
        
        # Build edge line
        if edge_label:
            output.append(f'{source} --> |{edge_label}| {target}')
        else:
            output.append(f'{source} --> {target}')
    
    output.append('@enduml')
    return '\n'.join(output)

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
    plantuml = mermaid_to_plantuml(mermaid_code, title)

    print(plantuml)
    print("\n" + "="*60)
    print("Import to Draw.io:")
    print("1. Arrange > Insert > Advanced > PlantUML (SVG)")
    print("2. Paste the code above")
    print("3. Click 'Insert'")
    print("="*60)

if __name__ == "__main__":
    main()
