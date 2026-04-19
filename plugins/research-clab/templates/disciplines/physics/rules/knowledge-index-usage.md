# Knowledge Index (Knowledge MCP + `/weave` skill)

<!-- DEPLOY: project-root/.claude/rules/knowledge-index-usage.md -->
<!-- Path-scoped: loads when working in the tools directory -->
<!-- Source: extracted from Ainulindale Exflation .claude/rules/knowledge-index-usage.md -->

---
paths:
  - "tools/**"
---

The project maintains a structured knowledge graph at `tools/knowledge-index.json` tracking theorems, closed mechanisms, gate verdicts, evidence trajectory, data provenance, open channels, researchers, and equations across all sessions.

## Quick Queries (use `/weave` skill directly)

- `/weave --show theorems|closed|gates|trajectory|open|researchers|equations` — formatted tables
- `/weave --trace "<entity>"` — evidence chain for a named entity
- `/weave --provenance <filename>` — script → data → gate lineage
- `/weave --search "<keyword>"` or `/weave --db-search "<keyword>"` — cross-entity search
- `/weave --update` — rebuild index after adding new session files

## Agent Spawn (use `knowledge-weaver` agent)

- **Solo**: spawn alone for full index rebuilds.
- **Teammate**: spawn on a team to answer live structured queries.
- Intended model: small/cost-efficient. The knowledge-weaver never evaluates physics — it only indexes and serves.

## Rules

- `knowledge-index.json` is the single source of truth. The SQLite database (if present) is a query accelerator rebuilt from the JSON.
- Source authority: Skeptic verdicts > synthesis files > gate verdict `.txt` > other minutes > raw filesystem outputs.
- Deduplication: **latest synthesis wins**. Only the knowledge-weaver agent (or `/weave --update`) should write to the index.

## MCP as first-class identity-claim surface

**Agents MUST query the Knowledge MCP before stating any identity claim** — a constant value, a gate verdict, a theorem statement, a closed-mechanism status.

File-system reads (`{{CANONICAL_MODULE}}`, session markdown, registry files) are the **fallback** when the MCP is known-stale. Cross-check direction is ALWAYS script ⇄ MCP — never trust one without the other.

### Required query patterns

| Question | MCP tool | Authority |
|:---------|:---------|:----------|
| "What is constant X's canonical value + provenance?" | `get_constant(X)` | Canonical; prefer over reading `{{CANONICAL_MODULE}}` |
| "Has gate G been evaluated?" | `query_entity("gates", G)` | Canonical verdict ledger |
| "Is mechanism M closed?" | `query_entity("closed", M)` | Canonical; prevents re-derivation of settled results |
| "What sessions touched this topic?" | `search_knowledge(query)` | FTS5 across all entity types |
| "What is the evidence chain for concept C?" | `trace_entity(C)` | Cross-type traversal |
| "What constants match a pattern?" | `list_constants(regex)` | Canonical enumeration |
| "What theorems exist?" | `list_entities("theorems")` | Canonical enumeration |
| "Add / update a constant after rerun" | `update_constant(...)` | Write-back path (audited tier only, on verified match) |

### Enforcement

- A review, audit, or synthesis that states an identity claim without a demonstrated MCP query is **incomplete** and must be re-run.
- Review-tier agents MUST show MCP query usage for every CLEAN / MINOR / MAJOR / BLOCKER grade that turns on an identity claim.
- Re-run anchor agents MUST fetch the MCP baseline BEFORE modifying a script; compare the reproduced value to the MCP value; only call `update_constant` on match.

### When the MCP is wrong

If `get_constant(X)` returns a value that disagrees with an authoritative source (registry, `{{CANONICAL_MODULE}}` with a `PROVENANCE` comment), that is a data-ingestion bug in the extractor, not a framework fact. Flag via `/weave --update` + a note in the relevant session file. Do NOT silently trust the MCP over an audited source — but also do not silently trust the file over the MCP. Reconcile.
