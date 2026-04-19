# Math-Specific MCPs

Empty at ship. Candidates for future work:

| MCP | Purpose | Notes |
|:----|:--------|:------|
| **mathscinet** | Query MathSciNet (AMS) bibliography | Requires institutional subscription |
| **zbmath** | Query Zentralblatt für Mathematik | Open-access API available |
| **oeis** | Online Encyclopedia of Integer Sequences lookup | Free API, very useful for pattern recognition |
| **sage-bridge** | Drive a local Sage installation for symbolic computation | Local CLI wrapper; no network dependency |
| **lean-bridge** | Compile and check a Lean 4 artifact | Requires Lean + mathlib installed locally |

To author one, mirror the MCP template structure (see `templates/universal/mcps/README.md` and `templates/universal/mcps/paper-search/` for the shape):

```
disciplines/math/mcps/<name>/
├── mcp-json-fragment.json
├── claude-md-instructions.md
├── settings-permissions.md
└── requirements.md
```

Then register in `disciplines/math/discipline.json` under `mcps[]`.
