# knowledge MCP — Settings Permissions

## settings.json Additions

The knowledge MCP is local (stdio) and does not call out to external services. No `WebFetch` domains are needed.

## settings.local.json Additions

Add the MCP Python command permission to the personal settings:

```json
"Bash(\"{{PYTHON_CMD}}\":*)"
```

This allows the MCP server process to execute. The server reads the project's knowledge index / SQLite database / canonical constants module, all of which live under the project root — no separate filesystem permission grants are required beyond the usual project-root scoping.

## Notes

- Because the server reads and (via `update_constant`) writes to the canonical constants module, the runtime user needs write access to the project tree.
- The server logs to `tools/mcp-servers/knowledge-mcp/knowledge_mcp.log` and a usage counter at `tools/mcp-servers/knowledge-mcp/usage_counter.json`. Both are gitignored in the reference implementation.
