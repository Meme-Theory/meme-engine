# madrigal MCP — Settings Permissions

## settings.json Additions

```json
"WebFetch(domain:cedar.openmadrigal.org)",
"WebFetch(domain:madrigal.haystack.mit.edu)",
"WebFetch(domain:jro.igp.gob.pe)",
"WebFetch(domain:isr.sri.com)"
```

The main public Madrigal mirrors. Add regional mirrors if your project uses them; the `madrigalWeb` client queries whichever server URL you pass.

## settings.local.json Additions

```json
"Bash(\"{{PYTHON_CMD}}\":*)"
```

This allows the MCP server process to execute.
