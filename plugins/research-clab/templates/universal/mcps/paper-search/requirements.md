# paper-search MCP — Requirements

## What this pack ships

Server source bundled at `server/` — the full `paper_search_mcp` Python package plus its `pyproject.toml`. The unfold copies the directory to `{project-root}/tools/mcp-servers/paper-search-mcp/` and `pip install -e`'s it so the `-m paper_search_mcp.server` invocation resolves.

## Runtime Dependencies

- **Python**: 3.10 or later
- **Package**: `paper-search-mcp` (installed editable from the bundled source)
- **Transitive dependencies** (covered by `requirements-mcp.txt`):
  - `mcp`, `fastmcp`, `pydantic` — framework
  - `httpx`, `requests` — HTTP clients
  - `feedparser` — arXiv Atom feed parser
  - `PyPDF2` — PDF text extraction
  - `python-dotenv` — optional `SEMANTIC_SCHOLAR_API_KEY` loader

## Installation

```bash
# Install the MCP framework deps (if not already via Phase 7c):
{{PYTHON_CMD}} -m pip install -r requirements-mcp.txt

# Install the bundled paper-search-mcp package editable:
{{PYTHON_CMD}} -m pip install -e "{{PROJECT_ROOT}}/tools/mcp-servers/paper-search-mcp"
```

The editable install makes `{{PYTHON_CMD}} -m paper_search_mcp.server` resolve to the bundled copy — the one the project can edit and version-control alongside everything else.

## Alternative: install from PyPI

If you prefer the published version and don't need to modify the server:

```bash
{{PYTHON_CMD}} -m pip install paper-search-mcp
```

Then you can delete the bundled `tools/mcp-servers/paper-search-mcp/` directory — `-m paper_search_mcp.server` picks up the PyPI install automatically. The `.mcp.json` fragment works either way.

## Python Detection

Standard detection order (see `unfold-mcp.md` Step 2). Requires Python 3.10+.

## Verification

```bash
{{PYTHON_CMD}} -c "import paper_search_mcp; print('paper_search_mcp', paper_search_mcp.__version__ if hasattr(paper_search_mcp, '__version__') else 'bundled')"
```

## Supported Platforms

All paper-search tools work cross-platform. Google Scholar scraping may be rate-limited or blocked by CAPTCHA under heavy use — expected behavior, not a bug.
