# Epistemic Discipline -- Physics Override

<!-- DEPLOY: project-root/.claude/rules/epistemic-discipline.md -->
<!-- No paths: loads unconditionally for all agents -->
<!-- Source: extracted from parent .claude/rules/epistemic-discipline.md -->
<!-- Overrides: universal/rules/epistemic-discipline.md -->

IMPORTANT: These rules govern how ALL agents handle evidence, claims, and confidence. Violations undermine the entire research methodology.

## Constraint Methodology

- **Pre-register gates BEFORE computation** -- define pass/fail criteria, then compute
- **Negative results are boundaries, not failures** -- they constrain the solution space
- **Never cite constraint counts as arguments** -- "we have 12 constraints" proves nothing
- **Separate bookkeeping from reasoning** -- reference tables and narrative analysis are distinct
- **Latest synthesis wins** -- for deduplication, the most recent synthesis document is canonical

## Confidence & Probability

- **No filler confidence language** -- avoid "promising," "encouraging," "likely correct"
- **Pre-registered gates are the evidence** -- everything else is commentary
- **Do not state percentage probabilities.** The constraint map IS the assessment.
- **Framework probability methodology** lives in the `evoi-prioritization.md` rule -- EVOI prioritization, evidence weighting, joint probability, effort-based tracking. Read it before assessing the framework's status or proposing new computations.

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

1. **Structural constraints** are permanent. A proven monotonicity theorem, an exact block-diagonality, a representation-theoretic identity -- these define the walls of the solution space. They survive regardless of the framework's physical fate. Report them as geometry: "The allowed region excludes all single-particle spectral functionals."

2. **Computational gates** are decisive. A pre-registered pass/fail criterion tested against new computation is the only thing that changes the state of knowledge. Report gates as measurements: "KC-3 at tau = 0.50 returned [value] against threshold [value]. Gate status: PASS/FAIL/UNCOMPUTED."

3. **Organizational insights** are useful but not evidential. Recognizing that five results share a common algebraic origin is good science -- it simplifies the picture. It does not change what is true. Report syntheses as structure: "These three results trace to a single algebraic identity," not as evidence for or against anything.

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

## Pre-Registration Completeness

Beyond pre-registering gates (Constraint Methodology above), a plan must pre-register the MACHINERY each gate depends on. A gate-relevant machinery parameter left unpinned creates execution-time freedom that manifests as multi-iteration verdict-log floatation.

- **PRU (Pre-Registration Underspecification)**: plan leaves one or more gate-relevant machinery parameters unpinned. Detection: multiple verdict-log entries for the same gate. Prevention: PRDR (Pre-Registration Dry-Run) at plan-write time.

- **PRDR (Pre-Registration Dry-Run)**: before a gate is frozen into the plan, dry-run the producing script, enumerate every free parameter via static analysis, and pin or declare-as-diagnostic each one in the gate block. Output is a structured machinery-enumeration subsection of the plan.

PRU is a plan-property failure (Class 8), structurally distinct from the 7 execution-property failures (convention-shopping, ansatz-forced PASSes, vacuous-margin, load-and-compare-to-self, linear-rescale-as-cross-check, iterate-until-PASS, false cross-checks). A scrubbed plan that prevents all 7 execution failures but does not pre-register machinery via PRDR remains PRU-vulnerable.

PRU applies recursively: any process that produces gated outputs is PRU-susceptible if its plan does not enumerate its free parameters. This includes audit-workshops. Pre-register audit-workshop decision rules, vocabulary, severity grading, WARRANT classes, and remediation format via a standardized template to eliminate PRU at the audit level by construction. The first invocation of a new audit template is itself audited to confirm the template is self-sufficient.

The canonical PRDR scaffold (the R3 YAML gate-block with its 8-item checklist) is at `.claude/templates/r3-yaml-gate-block.yaml`; the prose pre-registration block is at `.claude/templates/pru-pre-registration-template.md`. New gate blocks pull from those templates.

### PRU Class 8 sub-class taxonomy

PRU is the umbrella for plan-property under-specification. Its sub-classes, from most to least mandatory:

| Sub-class | Name | Status |
|:----------|:-----|:-------|
| 8.0 / 8.1 | machinery-pin cardinality failure (a free parameter left unpinned) | MANDATORY |
| 8.2 | verifier-rubric pre-registration failure | MANDATORY |
| 8.3 | output-precision pre-registration failure | MANDATORY |
| 8.4 | representation-/convention-pin failure | advisory (promote with project use) |
| 8.7 | degenerate-observable pre-flight failure | advisory (promote with project use) |

A gate is INCONCLUSIVE (value `PRE-REG-INCOMPLETE`), NOT FAIL, when it cannot be evaluated because of any Class-8 defect. Pin the machinery, then re-run.

### Verifier-Rubric Pre-Registration (Class 8.2; MANDATORY)

When a gate's PASS/FAIL/INFO criterion involves rubric-grading of qualitative content (a reasoning-quality score, a framing-compliance check, a narrative-pattern detector), the gate block MUST pre-register the verifier rubric alongside the threshold:

1. **Pattern set**: enumerate the specific lexical / structural patterns the verifier accepts.
2. **Disjunction-vs-conjunction declaration**: state whether the verifier requires ALL patterns (conjunction) or ANY (disjunction) per content unit.
3. **Negative-marker set** (optional): patterns that auto-fail.
4. **Pre-registered calibration corpus**: 1+ exemplar passing snippet, pinned by SHA, so the rubric can be re-validated without re-deriving the qualitative judgment.

Without (1)-(4), execution-time iteration to "calibrate the rubric" is structurally indistinguishable from iterate-until-PASS -- even when the underlying content is unchanged across runs.

### Publication-Precision Pre-Registration (Class 8.3; MANDATORY)

When a gate's output VALUE will be cited downstream (in a follow-up gate's verifier, a canonical-module entry, a registry row), the producing gate MUST pre-register the publication precision alongside the value:

1. **Publication-precision pin**: state the number of significant figures the value is published at.
2. **Verifier-tolerance match**: any downstream verifier MUST set `rel_tol >= 10^(-publication_sig_figs)`. A verifier with tolerance tighter than the published precision is structurally guaranteed to FAIL on a precision-floor mismatch, not on a physics boundary.
3. **Round-trip cross-check**: the producing gate emits full float64 to a data file AND a rounded value to its working-paper section. The downstream verifier loads from the data file (full precision), not from the prose.
4. **Metric-match**: when a threshold compares against a canonical-anchor value from a prior verdict, the threshold formula MUST express the SAME metric the canonical reports (e.g. compare `|ratio - 2|`, not `|b2 - 2*b3|/|b2|`, if the canonical reported the ratio). A metric mismatch produces a float-cancellation-floor false FAIL.

### Source Reconciliation (Class 8.1 -- pinned-but-drifted values)

PRU (cardinality) detects MISSING pins. SOURCE-RECONCILIATION detects PINNED-BUT-DRIFTED pins (a value test). Run them sequentially: PRU first (must clear), SOURCE-RECON second, gate execution third.

For every plan pin (`name = value`), the SOURCE-RECON sub-audit at plan-freeze:

1. queries `get_constant(name)` for the canonical value.
2. computes the drift `D = |log10(pin) - log10(source)|`.
3. classifies the drift per the 6-class taxonomy:
   - **(a) PIN-TIGHT-SOURCE-LOOSE** -- pin band tighter than the canonical band.
   - **(b) PIN-LOOSE-SOURCE-TIGHT** -- pin band wider than canonical (highest-leverage; the FALSE-PASS direction).
   - **(c) PIN-DRIFT-FROM-STALE-SOURCE** -- pin computed against a since-superseded canonical.
   - **(d) PIN-DERIVATIVE-VS-SOURCE-PRIMARY** -- pin is a derived form of a primary canonical.
   - **(e) PIN-PROMOTES-TO-CANONICAL-ON-PASS** -- pin will become canonical on PASS (no canonical exists yet at plan-freeze).
   - **(f) PIN-PLACEHOLDER-PENDING-CANONICAL** -- pin given as a textual approximation / OOM estimate / placeholder while a canonical exists. Detection patterns: `~10^...`, `approx`, `placeholder`, `TBD`, `pending`.
4. assigns severity per the band calibration:

| Drift band | Severity |
|:--|:--|
| `D < 0.1` | no action |
| `0.1 <= D < 1.0` | SOURCE-RECON advisory (S2) |
| `1.0 <= D < 3.0` | SOURCE-RECON MANDATORY (S1); halts plan-freeze |
| `D >= 3.0` | hard plan-freeze halt; manual review (the value is order-of-magnitude wrong) |

**Class-to-remediation table**:

| Class | Remediation |
|:--|:--|
| (a) | loosen the pin to the source band |
| (b) | tighten the pin, or invoke a source-structural bound (FALSE-PASS direction; highest leverage) |
| (c) | re-pin to the current canonical; log the drift in the plan-revision history |
| (d) | verify the derivation chain; ratio-check against the source primitives |
| (e) | log the promotion event in `{{CANONICAL_MODULE}}` provenance with `promoted_from = "S{N}-{gate}"` on PASS |
| (f) | query `get_constant(name)` for the canonical, substitute into the plan pin, re-run the audit |

### Registry-Write Hygiene under Parallel-Writer Race

Registry-write helpers (next-N allocators, slot allocators, append-only writers) MUST:

1. **Scan ALL header levels** before allocation -- `## H #N` AND `### H #N` AND `#### H #N`. A scan limited to one hash level under-counts existing slots and collides under parallel writers.
2. **Use append-only writers, not Edit-tool round-trips**, for shared-write registries. The Edit tool is mtime-conditional: when two agents both Read then Edit, the second Edit fails on an mtime conflict. For the VERDICT FILE specifically, the canonical writer is the race-safe `emit_verdict` tool (single, lock-serialized; see `.claude/rules/gate-verdicts.md`) -- never a raw `open("a")` append, which is NOT atomic across processes on Windows.
3. **Detect and document slot-rerouting in the verdict line.** When a planned slot is occupied at runtime, rerouting to the next free slot is permitted, but the verdict line MUST emit FAIL-with-remediation (not PASS) so the rerouting is visible in the audit trail.

Failure to follow (1)-(2) produces collisions / mtime races; failure to follow (3) hides slot drift from downstream consumers and breaks audit provenance.
