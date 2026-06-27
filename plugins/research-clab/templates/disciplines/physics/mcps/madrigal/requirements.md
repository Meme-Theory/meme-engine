# madrigal MCP — Requirements

## What this pack ships

Server source bundled at `server/`. The unfold copies it to `{project-root}/tools/mcp-servers/madrigal-mcp/`. Includes the `data_sources/` subpackage (framework search helpers).

## Runtime Dependencies

- **Python**: 3.10 or later
- **Packages** (covered by `requirements-mcp.txt`):
  - `fastmcp` — MCP framework (wrapper)
  - `madrigalWeb` — CEDAR Madrigal database client
  - `numpy` — result processing

## Installation

```bash
# Covered by the Python backbone install:
{{PYTHON_CMD}} -m pip install -r requirements-mcp.txt

# Or install just this MCP's deps:
{{PYTHON_CMD}} -m pip install fastmcp madrigalWeb numpy
```

## Python Detection

Standard detection order (see `unfold-mcp.md` Step 2). Requires Python 3.10+.

## Verification

```bash
{{PYTHON_CMD}} -c "import madrigalWeb; import fastmcp; print('OK')"
```

## Supported Platforms

Cross-platform. `madrigalWeb` is pure Python.
