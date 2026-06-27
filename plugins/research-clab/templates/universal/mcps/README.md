# MCP Templates (Universal)

This directory contains configuration + bundled-source templates for optional MCP (Model Context Protocol) servers that enhance research-clab projects, regardless of discipline.

Each subdirectory is one MCP server. `unfold-mcp.md` in `project-origami/` reads these templates and installs whichever MCPs the user selects during project scaffolding.

## Available Universal MCPs

| MCP | Directory | Requires | Purpose |
|:----|:----------|:---------|:--------|
| knowledge | `knowledge/` | Python 3.10+, `mcp` | Queries the project's own `knowledge-index.json` + SQLite accelerator. Mandatory for computation-agent identity-claim discipline. |
| paper-search | `paper-search/` | Python 3.10+, `mcp`, `fastmcp`, `httpx`, `requests`, `feedparser`, `PyPDF2` | Search and download academic papers from arXiv, PubMed, bioRxiv, medRxiv, Google Scholar, and Semantic Scholar. |

Discipline-specific MCPs live under `templates/disciplines/<pack>/mcps/` and are merged into the install menu when that pack is selected.

## MCP Template Layout

Each MCP template contains:

```
{mcp-name}/
├── mcp-json-fragment.json     # Server entry for .mcp.json (one key = server name)
├── claude-md-instructions.md  # Instructions block appended to root CLAUDE.md
├── settings-permissions.md    # Permission entries for settings.json
├── requirements.md            # Runtime requirements + verification
└── server/                    # (optional) Bundled server source
```

Every MCP in this plugin ships `server/` — the unfold copies the whole directory to `{project-root}/tools/mcp-servers/{mcp-name}-mcp/` (note the `-mcp` suffix on the target directory). Install is then `pip install -r requirements-mcp.txt` (Phase 7c) plus any editable-install commands documented in the MCP's `requirements.md`.

## Adding a New Universal MCP

1. Create a subdirectory `{mcp-name}/`
2. Write the 4 config fragments
3. Drop the full server source (including any subpackages, data files, tests you want shipped) into `{mcp-name}/server/`
4. Exclude caches, logs, egg-info from source copies — the `__pycache__`, `*.log`, `*.egg-info` patterns are dropped automatically if you use the `cp` + `find -delete` pattern documented in `unfold-mcp.md`
5. If the MCP is pip-installable from PyPI instead of (or in addition to) bundled source, document both paths in `requirements.md` — the `.mcp.json` fragment usually works for either install mode when the entry is `-m {package}.server`
