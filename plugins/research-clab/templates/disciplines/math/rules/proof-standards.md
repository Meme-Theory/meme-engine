# Proof Standards

<!-- DEPLOY: project-root/.claude/rules/proof-standards.md -->
<!-- No paths: frontmatter — loads unconditionally for all agents -->

The rigor expected of any stated proof, sketch, or derivation in this project.

## Rigor Levels

Every stated result carries a rigor tag.

| Tag | Meaning | When to use |
|:----|:--------|:------------|
| **SKETCH** | Structure of the argument is clear; steps may be elided but the author claims each elided step is straightforward | Work in progress, intuition-building, exposition for discussion |
| **DETAILED** | Every step is explicit; every lemma cited is in scope and already established | Published results, results the project relies on |
| **FORMALLY-VERIFIED** | A proof artifact in Lean, Coq, Isabelle, or another formal verifier closes the derivation | Results where machine verification is available and the stakes warrant the investment |

A result may move UP this ladder (sketch → detailed → formally-verified) but never down. A DETAILED proof is not demoted to SKETCH because a gap was found — it is marked RETRACTED, and the replacement is re-graded from scratch.

## Citation Discipline

Every non-trivial step in a DETAILED proof must cite:

1. **A prior theorem or lemma** (in the project knowledge base, or in a paper in `researchers/`)
2. **A definition** (from the project's definitions entity type, or standard)
3. **A named inference rule** (modus ponens, induction, contradiction, diagonalization, etc.)

"It can be shown that" / "clearly" / "obviously" / "one can easily verify" are **NEVER** acceptable in a DETAILED proof. Either the step is trivial enough to cite an inference rule alone, or it needs its own proof.

## Proof-Gap Accounting

When a proof is SKETCH, list its **proof obligations** explicitly:

```
Theorem T-12 (SKETCH):
  Proof obligations:
    [O-1] Bound on the spectral radius of M_x as |x| → 0
    [O-2] Monotonicity of F on the interval [0, c)
    [O-3] Closure of the auxiliary sequence under the defined operation
```

When the sketch moves to DETAILED, each obligation becomes either a cited lemma or an explicit derivation. A sketch with unlabeled obligations is a handwave, not a sketch.

## Scope Hygiene

A theorem's scope is the set of objects to which it applies. State scope explicitly. Do not use a theorem in a context broader than its scope without a separate argument that the extension is valid.

- Bad: "By T-12, F is monotonic" (T-12 was proven for compact domains; is F's domain compact?)
- Good: "By T-12 (applicable because our domain is compact by L-3), F is monotonic"

## When Computer Algebra or Formal Verification Enters

- Using Sage/Mathematica for a **numerical example** or **pattern suggestion**: annotate the result as "example-level evidence" — it does not upgrade the proof rigor
- Using formal verification (Lean/Coq) to close a sub-step: upgrades that step to FORMALLY-VERIFIED; the surrounding proof's rigor is still bounded by the weakest step
- Using SAT/SMT solvers for a finite-case decision: verify the encoding is correct; the proof rigor is DETAILED if the encoding is hand-verified, FORMALLY-VERIFIED if the solver output is machine-certified
