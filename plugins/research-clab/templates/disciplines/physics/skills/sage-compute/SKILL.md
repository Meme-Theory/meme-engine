---
name: sage-compute
description: Quick symbolic/exact computation via the Sage MCP -- factor, simplify, symbolic eigenvalues, exact integrals. Use when float answers are not good enough
argument-hint: <expression> | --code "<multiline sage>" | --eig "<matrix>" | --latex "<expr>" | --factor "<integer>" | --simplify "<expr>"
allowed-tools: [Read, mcp__sage__sage_eval, mcp__sage__sage_simplify, mcp__sage__sage_latex, mcp__sage__sage_symbolic_eig, mcp__sage__sage_backend_info]
---

# /sage-compute -- Exact Symbolic Computation via Sage

> **Requires**: the `sage` MCP server (this discipline pack ships it at `mcps/sage/`). If the server is not configured, every tool below returns a clean "no backend available" error -- install/enable it first.

Front-end to the `sage` MCP server. Routes common patterns to the right tool with the right preamble, so you do not need to remember Sage syntax for one-off queries.

## When to use this skill vs. raw Python

Use `/sage-compute` when the answer **must be exact or symbolic**:

- Factor a large integer into primes
- Eigenvalues of a small rational/integer matrix, returned as algebraic roots (not floats)
- Closed-form integral or sum
- Simplify a trigonometric/algebraic expression
- Render a symbolic expression to LaTeX

Use plain Python (numpy/torch) when a numerical answer is fine. Sage is slower and the round-trip to the remote backend adds latency.

## Usage

```
/sage-compute factor(2^64 - 1)
/sage-compute --factor 18446744073709551615
/sage-compute --eig "[[1,2,3],[4,5,6],[7,8,0]]"
/sage-compute --latex "integrate(sin(x)^2, x)"
/sage-compute --simplify "sin(x)^2 + cos(x)^2"
/sage-compute --code "
    R.<x> = QQ[]
    p = x^4 - 10*x^2 + 1
    print(p.factor())
    print(p.roots(AA))
"
```

The first form (bare expression) is treated as a Sage expression and evaluated with a `print(...)` wrapper.

## Execution steps

1. **Parse `$ARGUMENTS`**. Branch on flags:
   - `--factor N` -> `sage_eval(code="print(factor(N))")`
   - `--eig "<matrix>"` -> `sage_symbolic_eig(matrix="<matrix>")`
   - `--latex "<expr>"` -> `sage_latex(expr="<expr>")`
   - `--simplify "<expr>"` -> `sage_simplify(expr="<expr>")`
   - `--code "<block>"` -> `sage_eval(code="<block>")`
   - No flag (bare expression) -> `sage_eval(code="print(<expression>)")`

2. **Call the right MCP tool**. All tools are on the `sage` server:

   | Skill route | MCP tool | Required arg |
   |:------------|:---------|:-------------|
   | `--factor`, bare expr, `--code` | `mcp__sage__sage_eval` | `code` |
   | `--simplify` | `mcp__sage__sage_simplify` | `expr` |
   | `--latex` | `mcp__sage__sage_latex` | `expr` |
   | `--eig` | `mcp__sage__sage_symbolic_eig` | `matrix` (nested-list literal) |
   | (health check) | `mcp__sage__sage_backend_info` | (none) |

3. **Relay the result**. The MCP tool already formats `backend / success / stdout / stderr`. Pass it through unchanged. If `success` is false, surface the stderr prominently; do not silently hide errors.

4. **Verify the result** if the caller will act on it. Substitution-chain discipline applies: a Sage output is **an oracle, not a proof**. Before citing a Sage answer in a working paper, run a cross-check in Python with `sympy` (or `torch`) on a small instance to confirm.

## Backend transparency

The Sage MCP auto-selects a backend (report it with `mcp__sage__sage_backend_info`):

- **Local Sage** -- if a `sage` binary is on PATH (or `SAGE_BIN` is set). Fastest, no network, highest trust.
- **SageCell (remote)** -- default fallback over the SageCell Jupyter WebSocket. No install required. Session-isolated: no state between calls.

## Guard rails

- **No persistent state in SageCell mode**: each call starts a fresh kernel. If you need state (e.g. define a ring, then manipulate polynomials in it), put everything in ONE `--code` block.
- **Do not use Sage for floating-point throughput**. `numpy.linalg` / `torch.linalg` are faster and more appropriate -- Sage's value is symbolic correctness, not numerical speed.
- **Bare expressions are wrapped in `print(...)`**. If your expression already prints, use `--code` instead to avoid double-printing.
- **Heavy, reproducible computations belong in `{{COMPUTATION_DIR}}/`** with a pinned script (sympy/torch) -- the MCP is for interactive, small-case work during a session.
