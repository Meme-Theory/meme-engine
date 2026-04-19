# gwosc MCP — Requirements

## What this pack ships

Server source bundled at `server/server.py`. The unfold copies the whole `server/` directory to `{project-root}/tools/mcp-servers/gwosc-mcp/`. No clone, no fetch.

## Runtime Dependencies

- **Python**: 3.10 or later
- **Packages** (covered by `requirements-mcp.txt`):
  - `mcp` — MCP SDK
  - `gwosc` — LIGO/Virgo Open Science Center client

## Installation

```bash
# Already covered if you ran the Python backbone install (Phase 7c):
{{PYTHON_CMD}} -m pip install -r requirements-mcp.txt

# Or install just this MCP's deps:
{{PYTHON_CMD}} -m pip install mcp gwosc
```

## Python Detection

Standard detection order (see `unfold-mcp.md` Step 2). Requires Python 3.10+.

## Verification

```bash
{{PYTHON_CMD}} -c "import gwosc; print('gwosc', gwosc.__version__)"
{{PYTHON_CMD}} "{{PROJECT_ROOT}}/tools/mcp-servers/gwosc-mcp/server.py" --help 2>&1 | head
```

## Supported Platforms

Cross-platform. `gwosc` is pure Python — no native build requirements.
