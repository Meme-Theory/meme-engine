### Sage MCP — Symbolic Computation Bridge

Two-backend bridge to SageMath for symbolic algebra, eigenvalue problems, LaTeX rendering, and general CAS work. Bundled source at `tools/mcp-servers/sage-mcp/server.py` after install.

**Backends** (auto-detected at server startup, reported by `sage_backend_info`):

1. **Local Sage** — if `sage` is on PATH, runs computations locally. Fastest, highest trust.
2. **SageCell WebSocket** — public Jupyter-style SageCell server. No install required; uses the Jupyter `/service` protocol (HTTP is unreliable; the MCP uses WebSockets).

**Tools:**

| Tool | Purpose |
|:-----|:--------|
| `sage_eval(expression)` | Evaluate a Sage expression in the active backend. |
| `sage_simplify(expression)` | Symbolic simplification. |
| `sage_latex(expression)` | Render to LaTeX. |
| `sage_symbolic_eig(matrix)` | Symbolic eigenvalues / eigenvectors (exact when possible, falls back to approximate over RDF / CDF). |
| `sage_backend_info()` | Report which backend is active and a health check. |

**Guidance:**

- `sage_symbolic_eig` is the canonical use case in math projects: a small symbolic matrix where you want exact eigenvalues + multiplicities rather than numeric scipy output.
- The WebSocket backend has per-cell timeouts (60s default); large symbolic problems should run against local Sage or against the project's compute venv using sympy as a fallback.
- Results are returned as plain text (for `sage_latex`) or structured dicts (`{"result": ..., "backend": "local|sagecell", "timing_s": ...}`). The server refuses to compute if both backends are unreachable.
- Scripted, heavy, reproducible computations belong in `{{COMPUTATION_DIR}}/` with sympy — the MCP is for interactive / small-case work during sessions.
