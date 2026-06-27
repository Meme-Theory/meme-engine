---
paths:
  - "sessions/**"
---

# Gate Verdict Standards

<!-- DEPLOY: project-root/.claude/rules/gate-verdicts.md -->
<!-- Path-scoped: loads when working in sessions/. Disciplines with a computation directory may extend this path scope via their own gate-verdicts rule override. -->

A **gate** is a pre-registered, verifiable pass/fail check. The *form* of verification varies by domain:

- **Computational gates**: run a script, compare numerical output to a threshold
- **Proof obligations**: discharge a lemma, close a subgoal, verify a theorem
- **Empirical gates**: compare observation to prediction within a pre-registered uncertainty
- **Benchmark gates**: meet a performance or correctness threshold on a fixed workload

The *discipline* is identical across forms: define the criterion before doing the work; record the outcome verbatim; treat the verdict as permanent.

## Pre-Registration Protocol

1. **Before the work**: Define the gate in `sessions/session-plan/` with:
   - Gate ID (e.g., `V-1`, `M-3`, `L-7` for a lemma, `B-2` for a benchmark)
   - Kind: `COMPUTE | PROOF | EMPIRICAL | BENCHMARK` (or a discipline-specific tag)
   - Hypothesis / claim being tested
   - Pass/fail criterion (quantitative for compute/empirical; structural for proof — e.g., "a closed derivation from premises P to conclusion C using only scoped lemmas")
   - What PASSES and what FAILS mean for the solution space
   - Required inputs (scripts, data pins, prior lemmas, benchmark artifacts) so the check is reproducible

2. **During the work**: Produce the artifact and record it — script output, proof derivation, observation, benchmark run. Preserve the raw record before interpretation.

3. **After the work**: Compare the artifact to the pre-registered criterion. The verdict is a direct comparison; it is not a reinterpretation.

## Verdict Format

```
Gate {{GATE_ID}}: {{PASSED|FAILED|INCONCLUSIVE}}
  Kind:      {{COMPUTE | PROOF | EMPIRICAL | BENCHMARK}}
  Criterion: {{the pre-registered criterion verbatim}}
  Result:    {{the artifact-level outcome — value, proof reference, observation, benchmark number}}
  Verdict:   {{PASS/FAIL/INCONCLUSIVE with a one-line explanation}}
```

Discipline packs may add fields (e.g., closure SHA for compute-gate reproducibility, Lean artifact hash for proof-gates, significance level for empirical gates) — see the pack's `rules/` for the extended format.

## Rules

- Gate criteria are defined BEFORE the work — never after seeing results
- Verdicts are permanent — no retroactive changes to the criterion or the recorded outcome
- INCONCLUSIVE is a legitimate outcome (script crashed, proof blocked on an unscoped lemma, observation too noisy) — do not flatten it to FAIL
- Only the Skeptic evaluates whether a verdict is *meaningful* for the framework (a PASS against a trivial criterion is not evidence)
- Record verdicts in the session file AND update the knowledge index via `/weave --update`

## Gate Integrity -- Prohibited Actions

A pre-registered gate can be cheated. The following four actions are FORBIDDEN at every stage of a gate's life -- each manufactures a PASS the criterion did not earn, and each corrupts the verdict record for everyone downstream:

1. **Convention-shopping** -- changing a gate's convention, scheme, or threshold to reach PASS. The criterion is fixed at pre-registration; re-running under a different convention is a NEW gate, not a recovery of this one.
2. **Iterate-until-PASS** -- re-running the same gate with different seeds, scan ranges, or tolerances until one run lands above threshold. The first pre-registered run is the verdict; cherry-picking a favorable run from repeated trials is not.
3. **Post-hoc pre-registration editing** -- editing the pass threshold, pass band, or tolerance rule AFTER seeing the computed value. Edits to a plan after a verdict is recorded are documentation-only and MUST be logged with a `post-hoc:` prefix; they never change the verdict.
4. **Ansatz-forced PASS** -- manually editing a verdict line to read PASS without re-running the producing work. The verdict record is write-once per gate; the only way to change an outcome is to redo the work and record a new line.

Items 3 and 4 are absolute for any pre-registered gate (compute, proof, empirical, benchmark). Items 1 and 2 generalize as: do not change the criterion to pass, and do not retry until the answer is favorable. If a proposed remediation would require any of these four, it is not a remediation -- stop and report the gate as it stands.
