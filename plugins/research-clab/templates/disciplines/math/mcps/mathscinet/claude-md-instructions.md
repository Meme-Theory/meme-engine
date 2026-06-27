### MathSciNet MCP — AMS MR Reference Lookup

Lookup interface to the American Mathematical Society's MathSciNet / MR (Mathematical Reviews) database. Bundled source at `tools/mcp-servers/mathscinet-mcp/server.py` after install.

**Tools:**

| Tool | Purpose |
|:-----|:--------|
| `lookup_mr_reference(citation)` | Find the MR number + metadata for a free-form citation string. Uses the public `mref` endpoint. |
| `get_mr_bibtex(mr_number)` | Return a BibTeX entry for a given MR number. |
| `search_mathscinet(query, ...)` | Full search (requires institutional subscription; returns a clear error otherwise). |
| `mathscinet_status()` | Report whether the server has working public access and any subscription signals. |

**Guidance:**

- `lookup_mr_reference` and `get_mr_bibtex` use the free public `mref` endpoint — no subscription required.
- `search_mathscinet` requires the user's institution to have a MathSciNet subscription; the server returns a graceful error message when unauthenticated.
- The `bridge` agent (math flavoring) is the primary consumer: use MR numbers as stable citation anchors in the knowledge index under `references`.
- zbMATH is an alternative / complementary database — see `zbmath` MCP for Open Access coverage.
