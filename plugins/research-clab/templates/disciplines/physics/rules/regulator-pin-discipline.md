---
paths:
  - "{{COMPUTATION_DIR}}/**"
  - "sessions/session-plan/**"
  - "sessions/**"
---

# Regulator-Pin Discipline (Scheme Tagging for Regularized Quantities)

<!-- DEPLOY: project-root/.claude/rules/regulator-pin-discipline.md -->
<!-- Path-scoped: loads in the computation directory and session plans -->
<!-- Source: generalized from parent .claude/rules/regulator-pin-discipline.md (scheme-tag kernel only; the Mellin pole-set / Omega_GW / beta_shell / multi-axis-orthogonality specifics are intentionally omitted) -->
<!-- NOTE: frontmatter MUST be at byte 0 for path-scoping to parse; heading + provenance comments follow it. -->

## Rule

Every NEW citation of a regularization-scheme-dependent quantity -- in a computation script, working-paper section, or plan block -- MUST carry an explicit scheme tag. A bare, untagged value is FORBIDDEN going forward.

The canonical example is a Seeley-DeWitt heat-kernel coefficient `a_n`: its numerical value depends on the regulator, so a bare `a_n` silently inherits the calling context's scheme, which may differ from the producing script's scheme. The rule generalizes to any quantity whose value is scheme-dependent (a regularized determinant, a renormalized coupling at a stated scheme, a cutoff-dependent vacuum energy, etc.).

## Tag format

Write `a_n^{<scheme>}` (or, for a general quantity, append the scheme to the name / pin) where `<scheme>` is one of:

- `zeta` -- zeta-function regularization
- `Pauli-Villars` -- Pauli-Villars regularization
- `Mellin` -- Mellin-Barnes regularization
- `lattice` -- lattice-spacing regularization
- `cutoff` -- sharp UV cutoff

### Example

```
Bare (FORBIDDEN):  a_2                  (regulator unspecified)
Tagged (OK):       a_2^{zeta}           (zeta-regulated)
Tagged (OK):       a_2^{Pauli-Villars}  (PV-regulated)
Tagged (OK):       a_2^{Mellin}         (Mellin-regulated)
```

In a gate block, carry the scheme as a machinery pin (`regulator_pin: a_n^{zeta}`) and render it into the verdict line's provenance (alongside `scheme=` / `convention=`, per `.claude/rules/gate-verdicts.md`).

## Rationale

The numerical value depends on the regulator. A bare value in a downstream script silently consumes the calling-context regulator, which may differ from the producing-script regulator -- a silent class-conflation hazard. This is a Class-8 pre-registration vulnerability (see `.claude/rules/epistemic-discipline.md`): the regulator is a gate-relevant machinery parameter, and leaving it unpinned creates execution-time freedom.

## Audit

A plan-freeze / `/weave --update` audit greps for bare scheme-dependent quantities (e.g. the regex `\ba_(\d+)\b(?!\^)` for untagged Seeley-DeWitt coefficients) and flags violations. NEW files MUST comply; pre-existing files are carry-forward triage (mechanical regex inference over-matches non-regularized uses of the same symbol, so retrofit is a manual semantic review, not an automated rewrite).
