# MCP Templates

This directory contains configuration templates for optional MCP (Model Context Protocol) servers that enhance research-clab projects.

Each subdirectory is one MCP server. The `unfold-mcp.md` doc in `project-origami/` reads these templates and installs whichever MCPs the user selects during project scaffolding.

## Available MCPs

| MCP | Directory | Requires | Purpose |
|:----|:----------|:---------|:--------|
| paper-search | `paper-search/` | Python 3.10+ + pip | Search and download academic papers from arXiv, PubMed, bioRxiv, medRxiv, Google Scholar |

## Adding a New MCP

Create a subdirectory with these files:

```
MCP-templates/{mcp-name}/
├── mcp-json-fragment.json     # .mcp.json server entry (JSON object, one key)
├── claude-md-instructions.md  # CLAUDE.md instructions block to append to root CLAUDE.md
├── settings-permissions.md    # Permission entries to add to settings.json
└── requirements.md            # Runtime requirements + installation commands
```

Then add a menu entry in `project-origami/unfold-mcp.md` Step 1.
