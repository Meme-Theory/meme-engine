---
paths:
  - "sessions/session-plan/**"
  - "sessions/**"
---

# Gate Verdict Standards (Math)

<!-- DEPLOY: project-root/.claude/rules/gate-verdicts.md (OVERRIDES universal) -->
<!-- Path-scoped: loads when working in session plans / outputs -->

In math, a **gate** is usually a **proof obligation** — a precisely-stated claim that the session commits to discharging. Gates may also be computer-verified example gates (small case, counterexample search) or formal-verification gates (Lean/Coq artifact).

## Gate Kinds

| Kind | Meaning | Pass condition |
|:-----|:--------|:--------------|
| **PROOF** | Prove theorem T from premises P | DETAILED or FORMALLY-VERIFIED proof on disk |
| **REFUTATION** | Construct a counterexample to conjecture C | Concrete object with verified construction |
| **VERIFICATION** | Verify claim on a specific case / instance | Explicit computation or derivation |
| **FORMAL** | Close a proof in a formal verifier | Machine-checkable artifact (Lean `.olean`, Coq `.vo`, etc.) |
| **REDUCTION** | Reduce conjecture C to a simpler conjecture C′ | Written reduction argument, with C′ explicitly stated |

Compute gates (run a script, compare numerical output to a threshold) are allowed but should be rare in math projects. When used, mark as `COMPUTE` (the universal kind) and follow the universal gate-verdict format.

## Pre-Registration Protocol

1. **Before the work**: define the gate in `sessions/session-plan/` with:
   - Gate ID (e.g., `P-3` for proof, `R-1` for refutation, `F-2` for formal verification)
   - Kind
   - Precise statement of what must be shown
   - Required premises (with IDs of prior theorems/lemmas/definitions)
   - What PASS means (a proof closing, a counterexample constructed, a reduction established)
   - What FAIL means (an encountered obstruction that forces a scope narrowing, or a counterexample discovered against the claim)

2. **During the work**: produce the artifact — write the proof, construct the counterexample, run the formal verifier. The artifact is the primary record.

3. **After the work**: verify the artifact meets the criterion. For PROOF gates this means the Skeptic audits rigor level; for FORMAL gates this means the verifier output is clean; for REFUTATION gates this means the counterexample is independently checked.

## Verdict Format

```
Gate {{GATE_ID}}: {{PASSED | FAILED | PARTIAL | INCONCLUSIVE}}
  Kind:      {{PROOF | REFUTATION | VERIFICATION | FORMAL | REDUCTION}}
  Criterion: {{pre-registered criterion verbatim}}
  Artifact:  {{path/to/proof-file.md#section or Lean file path or inline reference}}
  Rigor:     {{SKETCH | DETAILED | FORMALLY-VERIFIED}}  (for PROOF/REDUCTION)
  Verdict:   {{one-line explanation}}
```

- **PASSED** — artifact meets criterion at required rigor
- **FAILED** — artifact shows the claim is false (counterexample found, or an explicit obstruction blocks any proof at the stated scope)
- **PARTIAL** — artifact closes a restricted version of the claim. State the narrower scope that WAS closed; the original gate rolls forward with updated scope.
- **INCONCLUSIVE** — work blocked on a prerequisite (unproven lemma, scope ambiguity, missing definition). Record the blocker; reassign as a new gate.

## Rules

- Gate criteria are defined BEFORE starting work — never after seeing partial results
- Verdicts are permanent — the recorded outcome and criterion cannot be retroactively changed
- A partial result is PARTIAL, not PASSED — do not overclaim
- A SKETCH-level proof PASSES a PROOF gate only if the gate explicitly set its rigor requirement to SKETCH; the default rigor for PROOF gates is DETAILED
- Only the Skeptic adjudicates rigor level (sketch vs. detailed)
- Record verdicts in the session file AND update the knowledge index via `/weave --update`
- When a PROOF gate passes, the proven statement moves to the `theorems` entity type in the knowledge index; the Skeptic is the authority for this transition
