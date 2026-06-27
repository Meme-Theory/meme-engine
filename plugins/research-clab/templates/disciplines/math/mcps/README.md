# Math-Specific MCPs

Four MCP servers ship with the math pack. Each is registered in `disciplines/math/discipline.json` under `mcps[]` and is installed when the math discipline is selected. Each server lives in its own directory with bundled source plus four standard config docs:

```
disciplines/math/mcps/<name>/
|-- server/server.py          # bundled server source (copied to {project}/tools/mcp-servers/<name>-mcp/ at unfold)
|-- mcp-json-fragment.json    # the .mcp.json stanza (uses {{PYTHON_CMD}} / {{PROJECT_ROOT}})
|-- claude-md-instructions.md # the tool table + usage guidance injected into the project CLAUDE.md
|-- requirements.md           # runtime deps + install + verification
|-- settings-permissions.md   # settings.json / settings.local.json permission additions
```

## Shipped servers

| MCP | Purpose | Access | Primary consumer |
|:----|:--------|:-------|:-----------------|
| **mathscinet** | AMS MathSciNet / MR reference lookup -- `lookup_mr_reference`, `get_mr_bibtex`, `search_mathscinet`, `mathscinet_status`. | `mref` endpoint is free; full search needs an institutional subscription (graceful error otherwise). | `bridge` agent (MR numbers as citation anchors) |
| **oeis** | Online Encyclopedia of Integer Sequences -- `search_oeis`, `get_sequence`, `get_b_file`, `lookup_by_values`. | Free public JSON / b-file endpoints. | `observer` agent (run `lookup_by_values` BEFORE inventing a conjecture) |
| **sage** | SageMath computer-algebra bridge -- `sage_eval`, `sage_simplify`, `sage_latex`, `sage_symbolic_eig`, `sage_backend_info`. Two backends: local Sage if on PATH, else the SageCell WebSocket. | Free (SageCell needs no install). | `calculator` agent + the `/sage-compute` skill |
| **zbmath** | zbMATH Open document / author / MSC lookup -- `search_zbmath`, `get_zbmath_document`, `search_zbmath_authors`, `search_msc`. | Free (no subscription). | `bridge` agent (zbMATH IDs as citation anchors; pair with MR numbers) |

The same `sage` MCP is also shipped by the physics pack (`disciplines/physics/mcps/sage/`) so the `/sage-compute` skill works under either discipline.

## Authoring an additional pack MCP

Mirror the structure above (see `templates/universal/mcps/README.md` and `templates/universal/mcps/paper-search/` for the canonical shape):

```
disciplines/math/mcps/<name>/
|-- server/server.py
|-- mcp-json-fragment.json
|-- claude-md-instructions.md
|-- requirements.md
|-- settings-permissions.md
```

Then register `<name>` in `disciplines/math/discipline.json` under `mcps[]`.

A frequently-requested candidate not yet shipped: a **Lean/mathlib bridge** (compile and check a Lean 4 artifact). It needs Lean + mathlib installed locally, so it is left to project-level authoring rather than shipped in the pack.
