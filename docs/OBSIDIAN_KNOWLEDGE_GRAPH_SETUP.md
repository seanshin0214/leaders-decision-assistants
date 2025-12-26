# Obsidian Knowledge Graph Setup Guide

This document describes how to set up and connect the Persona Knowledge Base in Obsidian for optimal knowledge graph visualization and navigation.

## Overview

The Persona-Vault is an Obsidian vault containing 142 World-Class+ expert personas organized into a connected knowledge graph. This setup enables:

- **Visual navigation** through the knowledge graph
- **Direct connections** between related knowledge files
- **MOC (Map of Contents)** based categorization
- **Cross-domain knowledge discovery**

## Vault Structure

```
Persona-Vault/
├── HOME.md                    # Main entry point
├── Development-MOC.md         # Software Engineering hub
├── AI-MOC.md                  # AI/ML hub
├── Creative-MOC.md            # Design & Creative hub
├── Business-MOC.md            # Business & Marketing hub
├── Education-MOC.md           # Education hub
├── Healthcare-MOC.md          # Healthcare hub
└── Knowledge/
    ├── 101-xxx/               # Development (100s)
    ├── 201-xxx/               # Design & Creative (200s)
    ├── 301-xxx/               # Business & Marketing (300s)
    ├── 401-xxx/               # AI & Data Science (400s)
    ├── 601-xxx/               # Education (600s)
    ├── 701-xxx/               # Healthcare (700s)
    └── 801-xxx/               # Writing (800s)
```

## MOC (Map of Contents) Files

Each category has a dedicated MOC file that serves as a hub:

| MOC File | Category | Persona Range |
|----------|----------|---------------|
| `Development-MOC.md` | Software Engineering, DevOps, QA, Security | 100s |
| `AI-MOC.md` | AI, ML, Data Science, NLP, LLM | 400s |
| `Creative-MOC.md` | Design, Video, Audio, Animation | 200s |
| `Business-MOC.md` | Marketing, Sales, Leadership, Operations | 300s |
| `Education-MOC.md` | Teachers, Professors, Curriculum | 600s |
| `Healthcare-MOC.md` | Medical, Nursing, Therapy, Pharmacy | 700s |

## Knowledge Graph Connections

### Connection Types

1. **MOC → Knowledge Files** (Hub-and-Spoke)
   - Each MOC links to all knowledge files in its category
   - Example: `Development-MOC.md` → `backend-architecture-2025.md`

2. **Knowledge ↔ Knowledge** (Mesh Network)
   - Direct connections between related knowledge files
   - Based on keyword matching and domain relationships
   - Example: `backend-architecture-2025.md` ↔ `database-optimization-2025.md`

### Relationship Mapping

Knowledge files are connected based on these domain relationships:

```
Backend ↔ API, Database, Architecture, DevOps, Security
Frontend ↔ React, Web, UI, UX, Mobile, Performance
DevOps ↔ CI/CD, Infrastructure, Cloud, Automation, GitOps, SRE
AI/ML ↔ MLOps, Data, NLP, LLM, Production
Design ↔ UX, UI, Figma, Visual, Graphic
Marketing ↔ Strategy, Content, Social Media, SEO, Brand
Education ↔ Teaching, Classroom, Curriculum, Learning
Healthcare ↔ Nursing, Therapy, Medical, Clinical
```

## Setup Instructions

### 1. Open Vault in Obsidian

1. Open Obsidian
2. Click "Open folder as vault"
3. Select the `Persona-Vault` folder

### 2. Enable Required Plugins

**Core Plugins:**
- Graph view (enabled by default)
- Backlinks
- Outgoing links

**Optional Community Plugins:**
- Dataview (for advanced queries)
- Local REST API (for MCP integration)

### 3. Configure Graph View

Recommended graph view settings:

```
Filters:
- Show tags: OFF
- Show attachments: OFF
- Show existing files only: ON

Groups:
- MOC files: #ff6b6b (red)
- Knowledge files: #4ecdc4 (teal)

Display:
- Node size: 1.5
- Link thickness: 1.0
- Center force: 0.5
- Repel force: 10
```

## MCP Integration

To use with Claude Desktop MCP:

### 1. Install Obsidian MCP

```bash
npm install -g obsidian-mcp
```

### 2. Configure Claude Desktop

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "obsidian": {
      "command": "node",
      "args": [
        "path/to/obsidian-mcp/build/main.js",
        "path/to/Persona-Vault"
      ],
      "env": {
        "TRIGGER_KEYWORDS": "obsidian,vault,ORAA,persona",
        "SUBMARINE_MODE": "true"
      }
    }
  }
}
```

### 3. Enable Local REST API in Obsidian

1. Settings → Community Plugins → Browse
2. Search "Local REST API"
3. Install and enable
4. Enable "Non-encrypted (HTTP) Server"

## Adding New Knowledge Files

When adding new knowledge files, include a Related section:

```markdown
# Your Knowledge Title

(Content...)

---

## Related
- [[path/to/related-file-1|Display Name 1]]
- [[path/to/related-file-2|Display Name 2]]
- [[path/to/related-file-3|Display Name 3]]
```

## Automated Knowledge Linking

For bulk linking of knowledge files, use the Python script approach:

```python
# Key relationship mappings
RELATIONSHIP_MAP = {
    "backend": ["api", "database", "architecture", "devops"],
    "frontend": ["react", "web", "ui", "ux", "mobile"],
    "devops": ["cicd", "infrastructure", "cloud", "gitops"],
    "ai": ["ml", "nlp", "llm", "data-science"],
    # ... more mappings
}

# Extract keywords from filename
# Find related files based on keyword matching
# Add Related section to each file
```

## Graph Statistics

After full setup:

| Metric | Value |
|--------|-------|
| Total Knowledge Files | 138+ |
| MOC Hub Files | 7 |
| Average Connections per File | 6-8 |
| Graph Density | High (mesh network) |

## Troubleshooting

### Graph Not Showing Connections

1. Check that links use correct relative paths
2. Verify file exists at linked location
3. Refresh graph view (Ctrl+R)

### MCP Not Connecting

1. Ensure Local REST API is enabled
2. Check vault path in MCP config
3. Restart Claude Desktop

### Files Not Appearing in Graph

1. Check file is `.md` extension
2. Verify file is in vault folder
3. Rebuild Obsidian cache

## Version History

| Date | Version | Changes |
|------|---------|---------|
| 2025-12-26 | 1.0.0 | Initial setup with MOC structure and automated knowledge linking |

---

**Related Documentation:**
- [KNOWLEDGE_BASE_STRATEGY.md](../KNOWLEDGE_BASE_STRATEGY.md)
- [KNOWLEDGE_BASE_WORKFLOW.md](../KNOWLEDGE_BASE_WORKFLOW.md)
- [KNOWLEDGE_SETUP.md](../KNOWLEDGE_SETUP.md)
