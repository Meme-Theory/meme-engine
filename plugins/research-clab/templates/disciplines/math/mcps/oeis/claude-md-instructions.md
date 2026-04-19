### OEIS MCP — Online Encyclopedia of Integer Sequences

Queries the OEIS public JSON / b-file endpoints. Bundled source at `tools/mcp-servers/oeis-mcp/server.py` after install.

**Tools:**

| Tool | Purpose |
|:-----|:--------|
| `search_oeis(query, ...)` | Full-text + keyword + sequence search against OEIS. |
| `get_sequence(A_number)` | Full metadata for one sequence (name, formula, references, cross-references, author). |
| `get_b_file(A_number, limit)` | Bulk terms of a sequence (the "b-file" list). |
| `lookup_by_values(values)` | Find sequences matching a list of initial terms — the canonical use case. |

**Guidance:**

- `lookup_by_values` is the highest-leverage tool. When a computer-algebra experiment produces a regular pattern (first few terms of some counting function), run `lookup_by_values` BEFORE inventing a conjecture. If OEIS finds a match, the conjecture is already stated and cited — cite the A-number in the knowledge index under `references`.
- `get_b_file` is the right tool when you want many terms cheaply (for comparing against your own computation). OEIS caches these as flat text files — fast.
- OEIS rate limits gently; polite use is expected. Batch queries where possible.
- The `observer` agent (math flavoring) is the primary consumer: experimental math workflows map naturally onto OEIS lookups.
