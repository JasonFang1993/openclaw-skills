#!/usr/bin/env python3
"""
Draw.io Diagram Generator - Mermaid to PlantUML converter

Outputs PlantUML code for Draw.io PlantUML (SVG) import
"""

import sys
import re

def mermaid_to_plantuml(mermaid_code, title="Diagram"):
    """Convert Mermaid code to PlantUML format"""
    lines = mermaid_code.strip().split('\n')
    
    # First pass: collect all node definitions
    # A[Label] -> A: Label
    # A{Decision} -> A: (Decision)
    node_defs = {}  # A -> "Label" or "(Label)"
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith('%%') or line.startswith('graph '):
            continue
        
        # Find all node definitions
        for match in re.finditer(r'(\w+)\[(.+?)\]', line):
            node_id = match.group(1)
            label = match.group(2)
            node_defs[node_id] = f'"{label}"'
        
        for match in re.finditer(r'(\w+)\{(.+?)\}', line):
            node_id = match.group(1)
            label = match.group(2)
            node_defs[node_id] = f'({label})'
    
    # Second pass: convert to PlantUML
    output = ['@startuml', f'title {title}', 'skinparam shadowing false', '']
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith('%%') or line.startswith('graph '):
            continue
        
        # Check if it's a sequence diagram (has colons)
        if re.search(r':\s*\w', line) and not re.search(r'rectangle|\(|\)', line):
            # Sequence diagram style - just clean up node refs
            for node_id, label in node_defs.items():
                line = re.sub(rf'\b{node_id}\b', label, line)
            output.append(line)
            continue
        
        # Split by arrows
        parts = re.split(r'\s*-->\s*', line)
        
        if len(parts) >= 2:
            # Process chain of nodes
            # A --> |label| B --> |label| C
            
            current_label = ''
            result_parts = []
            
            for i, part in enumerate(parts):
                part = part.strip()
                if not part:
                    continue
                
                # Check for label at start: |label| B
                label_match = re.match(r'^\|(.+)\|\s*(.+)', part)
                if label_match:
                    current_label = label_match.group(1)
                    part = label_match.group(2).strip()
                
                # Replace node ID with actual label
                for node_id, label in node_defs.items():
                    part = re.sub(rf'\b{node_id}\b', label, part)
                
                # Clean up remaining
                part = re.sub(r'\[.*?\]', '', part)
                part = re.sub(r'\{.*?\}', '', part)
                part = part.strip()
                
                if part:
                    result_parts.append(part)
            
            # Build edges
            if len(result_parts) >= 2:
                # First node
                result_parts[0] = re.sub(r'^(\S+)\s*.*', r'\1', result_parts[0])
                
                # Build connections
                for i in range(len(result_parts) - 1):
                    source = result_parts[i]
                    target = result_parts[i + 1]
                    
                    # Extract labels from source/target
                    s_match = re.search(r'^(\S+)(?:\s+(.+))?$', source)
                    t_match = re.search(r'^(\S+)(?:\s+(.+))?$', target)
                    
                    if s_match and t_match:
                        s_label = s_match.group(1)
                        s_msg = s_match.group(2) or ''
                        t_label = t_match.group(1)
                        t_msg = t_match.group(2) or ''
                        
                        # Combine messages
                        msg = t_msg if t_msg else current_label
                        current_label = ''  # reset
                        
                        if msg:
                            output.append(f'{s_label} --> {t_label}: {msg}')
                        else:
                            output.append(f'{s_label} --> {t_label}')
    
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
