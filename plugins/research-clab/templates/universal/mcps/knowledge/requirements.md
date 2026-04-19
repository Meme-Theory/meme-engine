# knowledge MCP — Requirements

## What this pack ships

Server source bundled at `server/server.py`. The unfold copies it to `{project-root}/tools/mcp-servers/knowledge-mcp/`. The server reads the project's `tools/knowledge-index.json` + `tools/knowledge.db` and optionally a canonical constants module — no external services.

## Runtime Dependencies

- **Python**: 3.10 or later
- **Packages** (covered by `requirements-mcp.txt`):
  - `mcp` — MCP SDK (the server uses `mcp.server.stdio`)
  - `sqlite3` — stdlib, no install needed

## Installation

```bash
{{PYTHON_CMD}} -m pip install -r requirements-mcp.txt
# or
{{PYTHON_CMD}} -m pip install mcp
```

## Verification

```bash
{{PYTHON_CMD}} -c "import mcp; print('OK')"
# Sanity check the server can enumerate entity types:
{{PYTHON_CMD}} "{{PROJECT_ROOT}}/tools/mcp-servers/knowledge-mcp/server.py" --help 2>&1 | head
```

## Logs and counters

The server writes:
- `tools/mcp-servers/knowledge-mcp/knowledge_mcp.log` — diagnostic log
- `tools/mcp-servers/knowledge-mcp/usage_counter.json` — per-tool invocation counter

Both are gitignored by the default `.gitignore` template (`*.log`) plus the explicit ignore line you can add for the counter if your project's audit trail doesn't want it tracked.

## Supported Platforms

Cross-platform. Pure Python + stdlib.
