---
name: drawio-diagrams
description: "Generate and create diagrams using Draw.io from Mermaid, CSV, or XML inputs. Use when users want to create flowcharts, architecture diagrams, org charts, network topologies, or any visual diagrams. Supports three input formats: Mermaid (mermaid code), CSV (structured data), and XML (native Draw.io format). Automatically opens diagrams in browser editor for further customization and export."
---

# Draw.io Diagrams

Generate professional diagrams using Draw.io from Mermaid, CSV, or XML inputs.

## Quick Start

```bash
# Mermaid flowchart (import XML via File > Import)
python scripts/mermaid2drawio.py """
A[Start] --> B{Decision}
B -->|Yes| C[Continue]
B -->|No| D[Stop]
"""

# CSV org chart
python scripts/csv2drawio.py """
id,label,parent,style
CEO,CEO,,shape=rectangle
VP1,VP Sales,CEO,shape=rectangle
"""

# XML format
python scripts/xml2drawio.py "<mxGraphModel>...</mxGraphModel>"
```

## When to Use

| Format | Script | Best For |
|--------|--------|----------|
| **Mermaid** | `mermaid2drawio.py` | Flowcharts, sequences, architecture, timelines, state machines, mind maps |
| **CSV** | `csv2drawio.py` | Org charts, network topologies, hierarchical data |
| **XML** | `xml2drawio.py` | Fine-grained control, existing Draw.io exports |

## Usage Patterns

### Flowchart (Draw.io XML Import)
```bash
python scripts/mermaid2drawio.py """
A[Start] --> B{Decision}
B -->|Yes| C[Continue]
B -->|No| D[Stop]
"""
```
Output: Draw.io XML - import via **File > Import > Paste XML**

### Organization Chart (CSV)
```bash
python scripts/csv2drawio.py """
id,label,parent,style
CEO,CEO,,shape=rectangle
VP1,VP Sales,CEO,shape=rectangle
VP2,VP Eng,CEO,shape=rectangle
""" --type tree --title "Org Chart"
```
Output: Draw.io URL - import via **Arrange > Insert > Advanced > CSV**

### XML Format
```bash
python scripts/xml2drawio.py "<mxGraphModel>...</mxGraphModel>"
```
Output: Draw.io URL - import via **File > Import**

## Resources

### references/
- **usage_guide.md**: Complete usage documentation and troubleshooting
- **examples.md**: 8 detailed examples (OAuth2, org charts, microservices, etc.)

### scripts/
- `mermaid2drawio.py`: Convert Mermaid code to Draw.io
- `csv2drawio.py`: Convert CSV data to Draw.io
- `xml2drawio.py`: Convert Draw.io XML to URL

## Dependencies

- Python 3.6+
- No external dependencies required
- All formats use Draw.io native import features

## Output

Scripts output:
- **Mermaid**: Draw.io XML (import via File > Import)
- **CSV**: Draw.io URL (import via Arrange > Insert > Advanced > CSV)
- **XML**: Draw.io URL (import via File > Import)

All can be edited and exported to PNG/SVG/PDF in Draw.io.
