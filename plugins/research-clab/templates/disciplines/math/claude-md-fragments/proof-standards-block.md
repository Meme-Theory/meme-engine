## Proof Artifacts

Proofs are the primary artifact of this project. Every non-trivial stated result carries a rigor tag:

- **SKETCH** — structure clear, elided steps claimed straightforward
- **DETAILED** — every step explicit, every cited lemma in scope
- **FORMALLY-VERIFIED** — machine-checked in Lean / Coq / Isabelle

See `.claude/rules/proof-standards.md` for the full specification.

Proofs live in:

- `sessions/session-NN/*.md` — per-session working proofs and sketches
- `sessions/framework/theorems/` — consolidated statements of proven theorems (one file per theorem, with a canonical proof reference)
- `artifacts/formal/` — formal verification artifacts (if the project uses Lean/Coq)

Query established theorems via `/weave --show theorems` before re-deriving. Cite by theorem ID (e.g., "by T-12"); do not paste the proof inline unless the session's work depends on the proof's internal structure.
