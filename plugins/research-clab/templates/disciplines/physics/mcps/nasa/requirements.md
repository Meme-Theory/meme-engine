# nasa MCP — Requirements

## What this pack ships

Server source bundled at `server/`. The unfold copies it to `{project-root}/tools/mcp-servers/nasa-mcp/`. Entry script is `nasa_server.py` (not `server.py`).

## Runtime Dependencies

- **Python**: 3.10 or later
- **Packages** (covered by `requirements-mcp.txt`):
  - `fastmcp` — MCP framework
  - `httpx` — async HTTPS to api.nasa.gov
  - `python-dotenv` — optional, reads `NASA_API_KEY` from a project `.env` if present

## API Key

Free key from <https://api.nasa.gov>. The `.mcp.json` fragment defaults to `DEMO_KEY` which is rate-limited (30 req/hour/IP) but workable for exploration. Set `NASA_API_KEY` in your shell or in a project `.env` file to lift the limit.

## Installation

```bash
{{PYTHON_CMD}} -m pip install -r requirements-mcp.txt
# or
{{PYTHON_CMD}} -m pip install fastmcp httpx python-dotenv
```

## Python Detection

Standard detection order (see `unfold-mcp.md` Step 2). Requires Python 3.10+.

## Verification

```bash
{{PYTHON_CMD}} -c "import fastmcp, httpx; print('OK')"
# Live API check (uses DEMO_KEY):
{{PYTHON_CMD}} -c "import httpx; print(httpx.get('https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY').status_code)"
```

## Supported Platforms

Cross-platform. All deps are pure Python.
