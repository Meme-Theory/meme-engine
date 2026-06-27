# zbmath MCP — Requirements

## What this pack ships

Server source bundled at `server/server.py`. The unfold copies it to `{project-root}/tools/mcp-servers/zbmath-mcp/`.

## Runtime Dependencies

- **Python**: 3.10 or later
- **Packages** (covered by `requirements-mcp.txt`):
  - `mcp` — MCP SDK
  - `httpx` — async HTTPS to zbmath.org

## Installation

```bash
{{PYTHON_CMD}} -m pip install -r requirements-mcp.txt
# or
{{PYTHON_CMD}} -m pip install mcp httpx
```

## Verification

```bash
{{PYTHON_CMD}} -c "import mcp, httpx; print('OK')"
# Live zbMATH check:
{{PYTHON_CMD}} -c "import httpx; print(httpx.get('https://zbmath.org/api/v1/document?search=primes').status_code)"
```

## Supported Platforms

Cross-platform. Pure Python deps.
