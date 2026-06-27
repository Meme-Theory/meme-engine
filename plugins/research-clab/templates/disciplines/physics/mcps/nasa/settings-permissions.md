# nasa MCP — Settings Permissions

## settings.json Additions

```json
"WebFetch(domain:api.nasa.gov)",
"WebFetch(domain:apod.nasa.gov)",
"WebFetch(domain:images-api.nasa.gov)",
"WebFetch(domain:mars.nasa.gov)",
"WebFetch(domain:epic.gsfc.nasa.gov)"
```

Domains the MCP itself queries via `httpx`. The `WebFetch` permissions cover any supplementary lookups Claude Code does (e.g., reading an APOD image's landing page).

## settings.local.json Additions

```json
"Bash(\"{{PYTHON_CMD}}\":*)"
```

## Environment Variable

The `.mcp.json` fragment sets `NASA_API_KEY` from your shell environment (or defaults to `DEMO_KEY`). If you export the variable in a `.env` file at the project root, the MCP picks it up via `python-dotenv`.
