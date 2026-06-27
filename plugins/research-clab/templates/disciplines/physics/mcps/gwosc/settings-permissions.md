# gwosc MCP — Settings Permissions

## settings.json Additions

```json
"WebFetch(domain:gwosc.org)",
"WebFetch(domain:www.gw-openscience.org)",
"WebFetch(domain:losc.ligo.org)"
```

The MCP itself uses the `gwosc` Python client, which issues its own HTTPS. `WebFetch` permissions cover any supplementary Claude Code lookups (e.g., reading the GWOSC documentation pages directly).

## settings.local.json Additions

```json
"Bash(\"{{PYTHON_CMD}}\":*)"
```

This allows the MCP server process to execute.
