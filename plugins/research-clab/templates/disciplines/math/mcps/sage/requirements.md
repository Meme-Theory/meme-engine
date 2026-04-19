# sage MCP — Requirements

## What this pack ships

Server source bundled at `server/server.py`. The unfold copies it to `{project-root}/tools/mcp-servers/sage-mcp/`.

## Runtime Dependencies

- **Python**: 3.10 or later
- **Packages** (covered by `requirements-mcp.txt`):
  - `mcp` — MCP SDK
  - `httpx` — session setup for SageCell
  - `websockets` — SageCell Jupyter `/service` protocol (HTTP is broken for SageCell; WS is the reliable transport)
- **Optional local backend**: a working `sage` binary on PATH. If missing, the MCP still functions via SageCell. If both are missing, the MCP reports "no backend available" and every tool returns a clean error.

## Installation

```bash
{{PYTHON_CMD}} -m pip install -r requirements-mcp.txt
# or
{{PYTHON_CMD}} -m pip install mcp httpx websockets
```

Local SageMath install (optional, separate from pip):
- **macOS**: `brew install --cask sage`
- **Linux**: distribution package or <https://www.sagemath.org/download.html>
- **Windows**: SageMath Windows installer or WSL

## Verification

```bash
{{PYTHON_CMD}} -c "import mcp, httpx, websockets; print('OK')"
# Check SageCell reachability:
{{PYTHON_CMD}} -c "import httpx; print(httpx.get('https://sagecell.sagemath.org').status_code)"
# Check local sage (optional):
sage --version 2>&1 | head -1
```

## Supported Platforms

Cross-platform for the MCP itself. Local SageMath works best on macOS / Linux / WSL; native Windows support has been limited historically.
