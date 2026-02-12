#!/usr/bin/env python3
"""
Draw.io Diagram Generator - PlantUML to Draw.io converter

PlantUML is supported natively in Draw.io!
"""

import sys

def mermaid_to_plantuml(mermaid_code, title="Diagram"):
    """
    Convert Mermaid code to PlantUML format (supported by Draw.io)
    """
    lines = mermaid_code.strip().split('\n')
    plantuml_lines = ['@startuml', f'title {title}']

    for line in lines:
        line = line.strip()
        if not line or line.startswith('%%') or line.startswith('graph '):
            continue

        # Convert Mermaid to PlantUML syntax
        # A[Label] -> rectangle "Label"
        line = line.replace('[', ' as "').replace(']', '"')
        # A{Decision} -> if "Decision"
        line = line.replace('{', ' ("').replace('}', '")')
        # --> --> -->
        line = line.replace('-->', '-->')
        # |label| --> |label| -->

        plantuml_lines.append(line)

    plantuml_lines.append('@enduml')
    return '\n'.join(plantuml_lines)

def plantuml_to_drawio(plantuml_code, title="Diagram"):
    """
    Generate PlantUML code for Draw.io import
    """
    return plantuml_code

def extract_mermaid_from_input(input_text):
    """Extract Mermaid code from input text"""
    import re
    # Check for mermaid code block
    pattern = r'```mermaid\n([\s\S]*?)```'
    matches = re.findall(pattern, input_text)
    if matches:
        return matches[0].strip()
    return input_text.strip()

def main():
    if len(sys.argv) < 2:
        print("Usage: python mermaid2drawio.py <mermaid_code> [--title TITLE]")
        print("\nNote: Draw.io supports PlantUML natively!")
        print("\nExample:")
        print('  python mermaid2drawio.py """')
        print('  A[Start] --> B{Decision}')
        print('  B -->|Yes| C[Continue]')
        print('  B -->|No| D[Stop]')
        print('  """ --title "Flowchart"')
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
    print("1. Open https://app.diagrams.net")
    print("2. Arrange > Insert > Advanced > PlantUML")
    print("3. Paste the code above")
    print("="*60)

if __name__ == "__main__":
    main()
