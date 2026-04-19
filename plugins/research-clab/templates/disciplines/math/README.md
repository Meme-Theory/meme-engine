# Math Pack

Discipline overlay for pure and applied mathematics.

## What This Pack Changes

Math differs from empirical sciences in what counts as evidence. The universal harness is written with empirical research as one valid mode; this pack shifts the defaults so proof is first-class and compute is supplementary.

### Rule additions

- `proof-standards.md` — rigor levels (sketch, detailed, formally-verified), citation discipline for lemmas, "it can be shown" is never an acceptable proof step
- `counterexample-before-conjecture.md` — before asserting generality, search small cases and low-dimensional examples for a counterexample

### Rule overrides

- `epistemic-discipline.md` — evidence hierarchy rewritten: proof > computer-verified case > heuristic argument > conjecture > analogy. Drops the empirical-science framing.
- `gate-verdicts.md` — gates are **proof obligations**. A gate passes when a valid derivation from premises to conclusion is on disk (informal LaTeX, or Lean/Coq artifact). Compute gates are allowed but rare.

### Knowledge schema

Entity types: `theorems`, `conjectures`, `definitions`, `lemmas`, `counterexamples`, `open_problems`. Plus the five universal types (`sessions`, `researchers`, `results`, `references`, `open_questions`). `results` is narrowed to empirical/observational results; math-specific results go in `theorems` and `lemmas`.

### Agent flavoring

- `skeptic.md` — reframed as proof-critic: demands complete case analysis, hunts counterexamples, flags unstated lemmas, questions the scope of every theorem.
- `calculator.md` — reframed as symbolic/constructive verifier: computer algebra for examples, formal proof assistants for critical theorems.
- `dreamer.md` — cross-area structural analogies (topology ↔ number theory, representation theory ↔ combinatorics); less about cross-scale physical patterns.
- `workhorse.md` — "work through the proof in full" not "run the simulation."
- `principalist.md` — axioms-and-foundations agent: reads axiomatic systems, prefers universal-property characterizations, classifies structural failure modes.
- `boundary-guard.md` — impossibility-theorem agent: proves lower bounds, catalogues no-go theorems, flags when a method is structurally blocked.
- `observer.md` — experimental mathematician: runs and documents computer-algebra / enumeration experiments, matches against OEIS, produces heuristic models — never confuses numerical regularity with proof.
- `bridge.md` — faithful reader of primary sources: tracks down original theorem statements, flags scope / notation drift across eras and languages.
- `formatter.md` — LaTeX typesetter for mathematical manuscripts: `amsthm`/`amsmath`/`amssymb` conventions, theorem environments, MR/zbMATH/arXiv-tagged bibliography.
- `generalist.md` — bookkeeper and gap-filler: maintains theorem/lemma/definition inventory, spots duplication, translates notation across sub-areas.

### CLAUDE.md fragments

- `proof-standards-block.md` — injected at `{{fragment-slot:reference-data}}`. Defines what counts as a rigorous proof in this project, and where proofs are stored.
- `prior-results-query.md` — injected at `{{fragment-slot:knowledge-query-discipline}}`. "Query `/weave --show theorems` before re-proving; reference existing lemmas rather than re-deriving."

## MCPs Shipped

Four math-native MCPs ship bundled with this pack, each with server source under `mcps/<name>/server/`:

- `mathscinet/` — AMS MR reference lookup (public `mref` endpoints; full `search_mathscinet` requires institutional subscription).
- `oeis/` — Online Encyclopedia of Integer Sequences. `lookup_by_values` is the highest-leverage tool.
- `sage/` — Two-backend symbolic-computation bridge (local Sage if installed; SageCell WebSocket otherwise).
- `zbmath/` — zbMATH Open (free alternative / complement to MathSciNet).

Listed in `discipline.json` under `mcps[]`. Install via the MCP menu during scaffold (`unfold-mcp.md`).

## Skills

Intentionally empty at ship. Math-specific skills (`/proof-check`, `/conjecture-index`, `/sage-compute`) are candidates for future work — author them in `skills/` and add them to `discipline.json`.

## Authoring New Content

Mirror the physics pack structure:
- New rule → drop in `rules/<name>.md`, add to `discipline.json` under `rules[]`
- New MCP → drop in `mcps/<name>/` with the 4-file MCP template (mcp-json-fragment.json, claude-md-instructions.md, settings-permissions.md, requirements.md), add to `discipline.json` under `mcps[]`
- New skill → drop in `skills/<name>/SKILL.md`, add to `discipline.json` under `skills[]`
- New archetype flavor → drop in `agent-flavoring/<archetype>.md`; loaded automatically by `/new-researcher` when stamping an agent of that archetype
