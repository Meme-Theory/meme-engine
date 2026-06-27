Math projects compute symbolically, not numerically. Replace the generic Python narrative with the tool stack this project actually uses:

- **Computer algebra** — Sage, Mathematica, SymPy for explicit examples, symbolic manipulation, pattern suggestion. Results at this level are "example-level evidence," not proofs.
- **Proof assistants** — Lean 4 (preferred for new work), Coq, Isabelle for machine-verified proofs. Artifacts live in `artifacts/formal/`. A `.olean` / `.vo` file that compiles cleanly + a statement matching a theorem verbatim is what FORMALLY-VERIFIED means in this project.
- **SAT/SMT solvers** — Z3, CVC5 for finite-case decisions. Hand-verify the encoding; solver output alone is machine-certified only if the encoding layer is also proved correct.

Python still appears for orchestration (batch-running Sage scripts, processing Lean output), but is NOT the primary compute stack. See `.claude/rules/proof-standards.md` for how compute-based evidence feeds rigor levels.
