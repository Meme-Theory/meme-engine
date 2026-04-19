# Gate Verdict Standards — Physics Override

<!-- DEPLOY: project-root/.claude/rules/gate-verdicts.md -->
<!-- Path-scoped: loads when working in the computation directory or session plans -->
<!-- Source: extracted from Ainulindale Exflation .claude/rules/gate-verdicts.md -->
<!-- Overrides: universal/rules/gate-verdicts.md -->

---
paths:
  - "{{COMPUTATION_DIR}}/**"
  - "sessions/session-plan/**"
  - "sessions/**"
---

A **gate** is a pre-registered, verifiable pass/fail check on a numerical computation. For this pack, every gate block has eight required fields and every verdict carries a cryptographic closure hash over its inputs.

## Pre-Registration Protocol

1. **Before computation**: define the gate in `sessions/session-plan/` with the full block. Every gate block MUST include:

   - **Gate ID** (e.g., `V-1`, `M-3`, `T3-<SCRIPT>`)
   - **Trigger**: `[SIGN]`, `[VERIFY]`, `[AUDIT]`, `[VERIFY-THEOREM]`, or `[CHAIN]`
   - **Classification**: a domain-specific category tag
     > NOTE: this pack does not ship a canonical classification enum. The living project authors its own (e.g., a cosmology project might use `PHONONIC | GEOMETRIC | PARTICLE | NON-PHONONIC`; a condensed-matter project might use `LATTICE | BAND-STRUCTURE | TRANSPORT | EXOTIC`). Pick the set of categories that partitions your solution space, document it in a project rule, and use it consistently.
   - **Hypothesis being tested** (one sentence)
   - **Pass/fail/INFO threshold** — quantitative, with RATIO / ABSOLUTE / THEOREM tolerance rule stated explicitly
   - **Machinery pin (PRDR)**: `N_eval`, `L_max`, `scan_range`, `step_size`, `tolerance`, `scheme`, `convention`, `random_seed`, `GPU path`. A gate that leaves any of these unpinned is PRU-vulnerable (Class 8 failure; see `.claude/rules/epistemic-discipline.md` §Pre-Registration Completeness).
   - **Input SHA-256 pins** for every file the script reads (static files get precomputed hashes; dynamic inputs are marked `<computed-at-runtime>`).
   - **Expected output 4-tuple**: `(value=<v>, scheme=<s>, convention=<c>, L_max=<L>)`
   - **Substitution chain**: required for any sign / direction / threshold claim, per `.claude/rules/substitution-chain.md`.
   - **What PASSES and what FAILS mean** for the solution space (the boundary the gate maps, not rhetoric)

2. **During computation**: run the script, record raw numerical output. The script MUST log the SHA-256 of every input in the first 20 lines of stdout and emit the closure hash. The 4-tuple output tag is printed as the final non-verdict line.

3. **After computation**: compare output to pre-registered threshold. Append a single verdict line to `s{N}_gate_verdicts.txt`:

   ```
   {GATE_ID}: PASS|FAIL|INFO -- value=<v> scheme=<s> convention=<c> L_max=<L> sha256=<closure>
   ```

   The SHA-256 pin is MANDATORY on all verdicts using this canonical form.

## Verdict Format

Legacy verdict blocks in plan / handoff docs remain valid in this form:

```
Gate {{GATE_ID}}: {{PASSED|FAILED}}
  Threshold: {{CRITERION}}
  Computed:  {{VALUE}}
  Verdict:   {{PASS/FAIL with brief explanation}}
```

**Canonical form** (required in `s{N}_gate_verdicts.txt`):

```
{GATE_ID}: PASS|FAIL|INFO -- value=<v> scheme=<s> convention=<c> L_max=<L> sha256=<closure>
```

The closure SHA is the SHA-256 of the ordered input-pin map (see the new-script template the project ships for wiring this up).

## Rules

- Gate criteria are defined BEFORE computation — never after seeing results.
- Verdicts are permanent — no retroactive changes.
- Only the Skeptic evaluates whether a gate verdict is *meaningful* (a PASS against a trivial criterion is not evidence).
- Record verdicts in the session file AND update the knowledge index via `/weave --update`.
- Canonical-form verdict lines MUST carry the `sha256=<closure>` pin. **The closure SHA MUST be the full 64-character hexdigest** — never a head-truncated prefix. The intake consolidator rejects verdict lines with SHAs shorter than 40 hex chars. The 16-char head form is allowed in the prose sections of the verdict file for human scan-readability, but NEVER in the first canonical line.
- A gate that cannot be evaluated because its producing machinery is unpinned (PRU Class 8) is NOT a FAIL — it is `PRE-REG-INCOMPLETE`. Pin the machinery via PRDR before marking PASS/FAIL.
