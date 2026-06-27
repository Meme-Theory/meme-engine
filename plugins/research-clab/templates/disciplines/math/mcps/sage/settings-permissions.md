# sage MCP — Settings Permissions

## settings.json Additions

```json
"WebFetch(domain:sagecell.sagemath.org)",
"WebFetch(domain:www.sagemath.org)"
```

## settings.local.json Additions

```json
"Bash(\"{{PYTHON_CMD}}\":*)",
"Bash(sage:*)"
```

The `Bash(sage:*)` entry is only needed if local SageMath is installed. Safe to include either way.
