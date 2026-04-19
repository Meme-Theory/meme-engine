# mathscinet MCP — Requirements

## What this pack ships

Server source bundled at `server/server.py`. The unfold copies it to `{project-root}/tools/mcp-servers/mathscinet-mcp/`.

## Runtime Dependencies

- **Python**: 3.10 or later
- **Packages** (covered by `requirements-mcp.txt`):
  - `mcp` — MCP SDK
  - `httpx` — async HTTPS to `mathscinet.ams.org` / `www.ams.org/mathscinet/mref`

## Subscription

- Public `mref` endpoints (used by `lookup_mr_reference` + `get_mr_bibtex`) require no subscription.
- `search_mathscinet` requires the caller's IP to resolve to an institution with an AMS MathSciNet subscription. The server returns a clear "subscription required" error otherwise — it does not crash.

## Installation

```bash
{{PYTHON_CMD}} -m pip install -r requirements-mcp.txt
# or
{{PYTHON_CMD}} -m pip install mcp httpx
```

## Verification

```bash
{{PYTHON_CMD}} -c "import mcp, httpx; print('OK')"
```

## Supported Platforms

Cross-platform. Pure Python deps.
