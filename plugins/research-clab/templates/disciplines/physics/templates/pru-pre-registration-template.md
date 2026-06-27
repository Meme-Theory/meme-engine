# PRU Pre-Registration Template

**Purpose**: prevent Pre-Registration Underspecification (PRU, Class 8 plan-property failure). Every gate declared in a session plan fills this block BEFORE the producing script runs.

---

## R3 YAML Gate-Block Scaffold

**Canonical machinery-pin scaffold**: `.claude/templates/r3-yaml-gate-block.yaml`. It declares the **8 required checklist items**:

1. `operator`
2. `strict_PASS_boundary`
3. `boundary_reachable_analytically`
4. `reachable_rationals`
5. `machinery_pin_map`
6. `audit_discriminators`
7. `substitution_chain`
8. `input_files`

**Validation rule**: a gate block is R3-compliant iff every one of the 8 checklist items is populated with non-empty content AND the block declares `schema_version: "R3"`. A gate block that is not R3-compliant does not count toward gate closure. The prose block below remains valid for markdown plan files as long as its field set covers the 8 items; new plans SHOULD prefer the YAML scaffold.

---

## Gate Block (prose form)

Copy this block into the session plan under each gate.

```
Gate {{GATE_ID}} -- {{ONE-LINE HYPOTHESIS}}
==========================================

Trigger:            [SIGN] | [VERIFY] | [AUDIT] | [VERIFY-THEOREM] | [CHAIN]
Classification:     <project classification tag>
Producing script:   {{COMPUTATION_DIR}}/_shared/s{{NN}}_*.py
Dependencies:       {{prior gates or theorems this rests on}}

---- Pre-registered inputs (SHA-256 pins) ----
Input file 1: {{path}}
  expected_sha256 = {{hexdigest or "<computed-at-runtime>"}}
Input file 2: {{path}}
  expected_sha256 = {{hexdigest or "<computed-at-runtime>"}}
Closure hash (canonical module + all imports): {{hexdigest or "<computed-at-runtime>"}}

---- Pre-registered machinery (PRDR pin -- enumerate every free parameter) ----
N_eval        = {{int}}                       # eigenvalue / sample / iteration count
L_max         = {{int or N/A}}                # truncation scale
scan_range    = [{{min}}, {{max}}]            # any swept parameter
step_size     = {{value or "adaptive"}}
tolerance     = {{eps}}                       # convergence / residual tolerance
scheme        = {{project scheme tag}}
convention    = {{ABSOLUTE|RATIO|MIXED|...}}
random_seed   = {{int or "N/A -- deterministic"}}
GPU path      = {{torch.linalg|numpy.linalg|cpu-cap-OMP8}}
regulator_pin = {{a_n^{scheme} or N/A}}       # iff a scheme-dependent quantity is cited

All other free parameters explicitly pinned: {{YES | list-outstanding-here}}

---- Pre-registered pass/fail criterion ----
PASS iff:   {{quantitative condition, e.g.  |value - target| / target <= 0.005}}
FAIL iff:   {{quantitative condition, e.g.  |value - target| / target >  0.05}}
INFO iff:   {{intermediate regime, between PASS and FAIL thresholds}}

Target value:           {{canonical_constant_name or literal}}
Tolerance policy:       RATIO = 0.5%  |  ABSOLUTE = 5%  |  THEOREM = machine-eps
publication_precision:  {{sig figs}}          # iff this value is cited downstream

---- Pre-registered output 4-tuple ----
Expected form:
  (value=<computed>, scheme={{scheme}}, convention={{convention}}, L_max={{L_max}})

Verdict line format (emitted via emit_verdict, per .claude/rules/gate-verdicts.md):
  {{GATE_ID}}: PASS|FAIL|INFO -- value=<v> scheme=<s> convention=<c> L_max=<L> content_sha256=<64-hex> script_sha256=<64-hex>

---- Substitution chain (MANDATORY for sign/direction/threshold claims) ----
Step 1 -- Definitions:
  {{quantity 1}} = {{definition, cite canonical constant or defining equation}}
  {{quantity 2}} = ...

Step 2 -- Substitution (plug definitions into target, no simplification):
  {{target expression with all symbols expanded}}

Step 3 -- Simplification (algebra only, one step per line):
  = {{line 1}}
  = {{canonical form}}

Step 4 -- Direction read-off (from canonical form):
  {{sign/direction/threshold conclusion}}

---- Post-run actions (filled AFTER the script executes) ----
[ ] Verdict line emitted via emit_verdict with full 64-hex closure SHA
[ ] Input SHAs logged in the first 20 lines of script stdout
[ ] 4-tuple output tag printed as the final non-verdict line
[ ] Result promoted to the canonical module (if it is a reusable constant)
[ ] Registry/inventory row landed (if a permanent claim)
```

---

## How to Use

### At plan-write time (PRDR -- Pre-Registration Dry-Run)

1. **Enumerate every free parameter in the producing script** via static (AST) analysis: every `name = <number>` assignment that is NOT imported from the canonical module and NOT tagged `# (local)` is a free parameter. Pin it or declare it diagnostic.
2. **Compute expected input SHAs where possible**. Static input files have fixed SHAs; paste them. Runtime-generated inputs stay `<computed-at-runtime>`.
3. **Write the substitution chain for every sign/direction claim**. Without it the gate's verdict can hinge on a direction the plan never pinned.
4. **Select convention + scheme explicitly**. A gate that says "c > 1" without naming the scheme is underspecified.

### At execution time

1. Script reads inputs, logs the SHA-256 of each, computes the two SHAs.
2. Script runs the computation and evaluates the gate.
3. Script prints the 4-tuple tag and the emit_verdict payload.
4. The dispatching agent calls `emit_verdict` (race-safe single writer).

---

## Class 8 Failure Mode (PRU)

PRU is a *plan-property* failure, structurally distinct from the 7 execution-property failures:

| # | Failure | Type | Prevented by |
|:--|:--------|:-----|:-------------|
| 1 | Convention-shopping | execution | Pre-registered scheme field |
| 2 | Ansatz-forced PASSes | execution | Pre-registered threshold |
| 3 | Vacuous-margin | execution | Pre-registered convention + tolerance |
| 4 | Load-and-compare-to-self | execution | Independent target value |
| 5 | Linear-rescale-as-cross-check | execution | Pre-registered cross-check method |
| 6 | Iterate-until-PASS | execution | One-shot execution + verdict |
| 7 | False cross-checks | execution | Pre-registered cross-check criterion |
| **8** | **PRU (machinery unpinned)** | **plan-property** | **This template + PRDR** |

A scrubbed plan that prevents all 7 execution failures but does not pin every free parameter via PRDR remains PRU-vulnerable and produces multi-iteration verdict-log floatation.

---

## References

- `.claude/rules/epistemic-discipline.md` -- Pre-Registration Completeness + Source Reconciliation (Class 8.1) + the Class-8 sub-class taxonomy.
- `.claude/rules/substitution-chain.md` -- the Double-Check Logic chain.
- `.claude/rules/gate-verdicts.md` -- verdict-line schema, race-safe emission, Option-A correction.
- `.claude/templates/r3-yaml-gate-block.yaml` -- the canonical YAML scaffold.
- `.claude/templates/script-template.py` -- the producing-script scaffold.
