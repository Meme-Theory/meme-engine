# oeis MCP — Requirements

## What this pack ships

Server source bundled at `server/server.py`. The unfold copies it to `{project-root}/tools/mcp-servers/oeis-mcp/`.

## Runtime Dependencies

- **Python**: 3.10 or later
- **Packages** (covered by `requirements-mcp.txt`):
  - `mcp` — MCP SDK
  - `httpx` — async HTTPS to oeis.org

## Installation

```bash
{{PYTHON_CMD}} -m pip install -r requirements-mcp.txt
# or
{{PYTHON_CMD}} -m pip install mcp httpx
```

## Verification

```bash
{{PYTHON_CMD}} -c "import mcp, httpx; print('OK')"
# Live OEIS check:
{{PYTHON_CMD}} -c "import httpx; print(httpx.get('https://oeis.org/search?q=1,1,2,3,5,8&fmt=json').status_code)"
```

## Supported Platforms

Cross-platform. Pure Python deps.
