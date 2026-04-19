<!-- Slot: knowledge-query-discipline -->
<!-- Source: extracted from Ainulindale Exflation CLAUDE.md §"Knowledge MCP — MANDATORY for Computation Agents" -->
<!-- This fragment is inserted into the project root CLAUDE.md by the unfold process. -->

## Knowledge MCP — MANDATORY for Computation Agents

The `knowledge` MCP server provides direct access to the project's knowledge base and canonical constants. **Every computation agent MUST query the knowledge base before starting work** to check whether a result is already known, a mechanism is closed, or a gate has already been evaluated.

### Before computing ANYTHING, run:

```
search_knowledge("your topic keywords")     # Check if already known/closed
get_constant("constant_name")               # Get value + provenance before using
trace_entity("mechanism or concept name")   # Find the full evidence chain
```

### Available tools (MCP server: `knowledge`):

| Tool | Use |
|:-----|:----|
| `search_knowledge(query)` | FTS5 search across ALL entities. Multi-word uses OR by default. |
| `query_entity(table, id)` | Direct lookup. Tables: theorems, closed, gates, sessions, open, researchers |
| `list_entities(type)` | Show all entities of a type |
| `trace_entity(name)` | Evidence chain across all entity types |
| `get_constant(name)` | Constant value + session / source / gate provenance |
| `list_constants(pattern)` | Filter constants by regex pattern |
| `update_constant(name, value, session, source, comment)` | Add NEW constant with provenance |

### Why this exists

Agents repeatedly rediscover settled results — a structural theorem from an early session gets re-derived in a later one because the new agent never queried the knowledge base. The knowledge base contains many sessions of theorems, closed mechanisms, and canonical constants. **Query first, compute second.**
