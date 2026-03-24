# paper-search MCP — Requirements

## Runtime Dependencies

- **Python**: 3.10 or later
- **Package**: `paper-search-mcp` (PyPI)
- **Transitive dependencies**: `beautifulsoup4`, `fastmcp`, `feedparser`, `lxml`, `mcp`, `pypdf2`, `requests`

## Installation

```bash
pip install paper-search-mcp
```

Or with a project venv:

```bash
python -m venv .venv
.venv/bin/pip install paper-search-mcp     # Unix
.venv\Scripts\pip install paper-search-mcp  # Windows
```

## Python Detection

The unfold process determines the Python command by checking, in order:

1. Project-local venv: `.venv/bin/python` (Unix) or `.venv\Scripts\python.exe` (Windows)
2. System `python3` on PATH
3. System `python` on PATH (verify version >= 3.10)
4. Windows Python Launcher: `py -3`

If none are found or the version is below 3.10, the MCP cannot be installed. Alert the user and skip.

## Verification

After installation, verify with:

```bash
{{PYTHON_CMD}} -c "import paper_search_mcp; print('OK')"
```

## Supported Platforms

All paper-search tools work cross-platform. Google Scholar scraping may be rate-limited or blocked by CAPTCHA under heavy use.
