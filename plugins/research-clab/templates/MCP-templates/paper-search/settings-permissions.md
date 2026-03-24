# paper-search MCP — Settings Permissions

## settings.json Additions

Add these to the `permissions.allow` array in `.claude/settings.json`:

```json
"WebFetch(domain:api.semanticscholar.org)",
"WebFetch(domain:arxiv.org)",
"WebFetch(domain:export.arxiv.org)",
"WebFetch(domain:pubmed.ncbi.nlm.nih.gov)",
"WebFetch(domain:eutils.ncbi.nlm.nih.gov)",
"WebFetch(domain:api.biorxiv.org)",
"WebFetch(domain:www.biorxiv.org)",
"WebFetch(domain:www.medrxiv.org)",
"WebFetch(domain:scholar.google.com)"
```

These whitelist the academic API endpoints that the paper-search MCP tools call. The MCP server itself handles the network requests, but Claude Code also needs permission to fetch from these domains directly for supplementary searches.

## settings.local.json Additions

Add the MCP Python command permission to the personal settings:

```json
"Bash(\"{{PYTHON_CMD}}\":*)"
```

This allows the MCP server process to execute.
