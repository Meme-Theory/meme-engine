# Epistemic Discipline

<!-- DEPLOY: project-root/.claude/rules/epistemic-discipline.md -->
<!-- No paths: frontmatter — loads unconditionally for all agents -->

IMPORTANT: These rules govern how ALL agents handle evidence, claims, and confidence. Violations undermine the entire research methodology.

## Constraint Methodology

- **Pre-register gates BEFORE computation** — define pass/fail criteria, then compute
- **Negative results are boundaries, not failures** — they constrain the solution space
- **Never cite constraint counts as arguments** — "we have 12 constraints" proves nothing
- **Separate bookkeeping from reasoning** — reference tables and narrative analysis are distinct
- **Latest synthesis wins** — for deduplication, the most recent synthesis document is canonical

## Confidence & Probability

- **No filler confidence language** — avoid "promising," "encouraging," "likely correct"
- **Pre-registered gates are the evidence** — everything else is commentary
- **Framework probability methodology** lives in the `evoi-prioritization.md` rule — See the framework evidence methodology rule for EVOI prioritization and evidence weighting.

## What Does NOT Count as Evidence

- Restatements of prior claims in new words
- Counts of how many agents agree
- Internal consistency alone (a wrong theory can be internally consistent)
- Analogies without quantitative backing

## Source Authority Hierarchy

When sources conflict, higher authority wins:

1. Skeptic verdicts (highest)
2. Synthesis files
3. Gate verdict results
4. Session minutes
5. Raw computation output (lowest)

## Evidence Hierarchy

1. **Structural constraints** are permanent. A proven monotonicity theorem, an exact block-diagonality, a representation-theoretic identity — these define the walls of the solution space. They survive regardless of the framework's physical fate. Report them as geometry: "The allowed region excludes all single-particle spectral functionals."

2. **Computational gates** are decisive. A pre-registered pass/fail criterion tested against new computation is the only thing that changes the state of knowledge. Report gates as measurements: "KC-3 at tau = 0.50 returned [value] against threshold [value]. Gate status: PASS/FAIL/UNCOMPUTED."

3. **Organizational insights** are useful but not evidential. Recognizing that five results share a common algebraic origin is good science — it simplifies the picture. It does not change what is true. Report syntheses as structure: "These three results trace to a single algebraic identity," not as evidence for or against anything.

## How to Assess a Mechanism

A mechanism lives or dies on its **structural position** within the mapped constraint surface:

- What walls does it respect?
- What gates has it passed?
- What gates remain uncomputed?
- What is the dimensionality and topology of the region it occupies?

A mechanism that occupies the sole surviving region after systematic elimination is **well-motivated by the constraint map**. A mechanism in an unexplored region is **untested**. A mechanism that violates a proven wall is **closed**. These are the three categories. Use them.

## What Counts as a Result

- A new number computed from first principles against a pre-registered criterion.
- A proven structural theorem (exact or to machine epsilon).
- A constraint that eliminates a region of solution space with a specific mathematical reason.

## What Does Not Count as a Result

- Agreement among agents (shared context produces shared outputs, not independent confirmation).
- Narrative coherence (a good story is not evidence; the universe is not obligated to have a plot).
- The number of prior closed mechanisms (constraint mapping is progress, not a failure rate).
- Restatement of existing results under new organizational framing.

## Reporting Format

For each finding, state:

- **What was computed** (equation, method, numerical result)
- **What region of solution space it constrains** (which mechanisms survive, which are excluded, and why)
- **What remains uncomputed** (the next gate, with its pre-registered criterion)

Do not state percentage probabilities. The constraint map IS the assessment.
