---
name: drawio-diagrams
description: "Generate and create diagrams using Draw.io from Mermaid, CSV, or XML inputs. Use when users want to create flowcharts, architecture diagrams, org charts, network topologies, or any visual diagrams. Supports three input formats: Mermaid (mermaid code), CSV (structured data), and XML (native Draw.io format). Automatically opens diagrams in browser editor for further customization and export."
---

# Draw.io Diagrams

Generate professional diagrams using Draw.io from Mermaid, CSV, or XML inputs.

## Quick Start

```bash
# Mermaid to diagram
python scripts/mermaid2drawio.py "graph TD; A-->B; B-->C;"

# CSV to org chart
python scripts/csv2drawio.py "id,label,parent\nCEO,CEO,\nVP1,VP Sales,CEO"

# XML to diagram
python scripts/xml2drawio.py "<mxGraphModel>...</mxGraphModel>"
```

## When to Use

| Format | Script | Best For |
|--------|--------|----------|
| **Mermaid** | `mermaid2drawio.py` | Flowcharts, sequences, architecture, timelines, state machines, mind maps |
| **CSV** | `csv2drawio.py` | Org charts, network topologies, hierarchical data |
| **XML** | `xml2drawio.py` | Fine-grained control, existing Draw.io exports |

## Usage Patterns

### Flowchart
```bash
python scripts/mermaid2drawio.py """
graph TD
    A[Start] --> B{Decision}
    B -->|Yes| C[Continue]
    B -->|No| D[Stop]
"""
```

### Architecture Diagram
```bash
python scripts/mermaid2drawio.py """
graph TB
    subgraph Frontend
        UI[React UI]
    end
    subgraph Backend
        API[API Gateway]
        Auth[Auth Service]
    end
    UI --> API
    API --> Auth
"""
```

### Organization Chart
```bash
python scripts/csv2drawio.py """
id,label,parent,style
CEO,CEO,,shape=rectangle
VP1,VP Sales,CEO,shape=rectangle
VP2,VP Eng,CEO,shape=rectangle
""" --type tree --title "Org Chart"
```

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
- Optional: `pako` for better compression (`pip install pako`)
- Falls back to zlib if pako not available

## Output

Scripts output a Draw.io URL that:
- Is displayed directly in the response
- Can be clicked to open in browser
- Loads the diagram in Draw.io editor
- Enables export to PNG, SVG, PDF
- Keeps data local (no server upload)
