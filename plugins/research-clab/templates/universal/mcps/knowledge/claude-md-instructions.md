### Knowledge MCP — Project Knowledge Index Bridge

Project-local MCP that wraps `tools/knowledge-index.json` + the SQLite accelerator + the canonical-constants module (if present). Bundled server source at `tools/mcp-servers/knowledge-mcp/server.py` after install. Built on `mcp.server.stdio`.

**Every computation agent MUST query the knowledge MCP before starting work** to check whether a result is already known, a mechanism is closed, or a gate has already been evaluated.

**Query patterns before computing anything:**

```
search_knowledge("your topic keywords")     # FTS5 across all entities
get_constant("constant_name")               # Canonical value + provenance (if your project has a constants module)
trace_entity("mechanism or concept name")   # Cross-type evidence chain
```

**Tool reference:**

| Tool | Use |
|:-----|:----|
| `search_knowledge(query)` | FTS5 search across ALL entity types. Multi-word uses OR by default. |
| `query_entity(table, id)` | Direct lookup. Tables depend on the project's `knowledge-schema.yaml`. |
| `list_entities(type)` | Enumerate all entities of a type. |
| `trace_entity(name)` | Cross-type evidence chain for a concept. |
| `get_constant(name)` | Constant value + provenance (when a canonical constants module is configured). |
| `list_constants(pattern)` | Filter constants by regex pattern. |
| `update_constant(name, value, session, source, comment)` | Append a new constant with provenance. Audited-tier only. |

**Identity-claim discipline.** A review, audit, or synthesis that states an identity claim (a constant value, a gate verdict, a theorem statement, a closed-mechanism status) without a demonstrated MCP query is **incomplete** and must be re-run. Cross-check direction is ALWAYS script ⇄ MCP — never trust one without the other.

**When the MCP is wrong.** If `get_constant(X)` disagrees with an authoritative source (the canonical constants module with a `PROVENANCE` comment, or a registry entry), that is a data-ingestion bug in the extractor, not a framework fact. Flag via `/weave --update` + a session-file note. Do NOT silently trust either source over the other; reconcile.

**Configuring the canonical-constants bridge.** The shipped server auto-detects a module at `{{CANONICAL_MODULE}}` (resolve per project — usually `tools/canonical_constants.py` or similar). If the project has no constants module, `get_constant` / `list_constants` / `update_constant` are disabled cleanly; search and entity tools still work.
