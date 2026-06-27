---
paths:
  - "{{COMPUTATION_DIR}}/**"
  - "*.py"
---

# Canonical Constants & Compute-Script Discipline

<!-- DEPLOY: project-root/.claude/rules/canonical-constants.md -->
<!-- Path-scoped: loads when working in the computation directory OR on Python sources -->
<!-- Source: generalized from parent .claude/rules/math-scripts.md (Canonical Constants, Local Variable Tagging, Canonical Write-Order, Exit Codes, All Results Are Good Results, Machinery-Feasibility Audit) -->
<!-- NOTE: frontmatter MUST be at byte 0 for path-scoping to parse; heading + provenance comments follow it. -->

## Canonical Constants (MANDATORY)

Every computation script MUST:

1. **Import from `{{CANONICAL_MODULE}}`**: e.g., `from {{CANONICAL_MODULE}} import *`
2. **Never hardcode framework constants** -- use the imported names
3. **Add new constants to `{{CANONICAL_MODULE}}` FIRST** if they do not exist, then import

Framework constants are any numerical values that (a) represent a physical or mathematical input the project treats as fixed, (b) carry provenance (PDG, Planck, DESI, prior gate result, or an audited registry entry), and (c) are used by more than one script.

**Heuristic**: if the same literal value appears in 3+ scripts, it belongs in `{{CANONICAL_MODULE}}`.

## Local Variable Tagging

Variables that are computed intermediate values (NOT framework constants) must be tagged with `# (local)` at the end of the assignment line:

```python
E_kin = 0.5 * m * v**2          # (local)
R_ratio = a_2 / a_4             # (local)
delta_ns = ns_bare - ns_obs     # (local)
```

The `# (local)` tag tells the constants audit to skip this line. Without it, any assignment matching the potential-hardcode regex is flagged.

### When to use `# (local)`

- Computed quantities derived from other variables
- Loop counters and indices that happen to match the naming pattern
- Temporary results specific to one computation
- Estimates, approximations, and scan parameters

### When NOT to use `# (local)`

- Framework constants that should be in `{{CANONICAL_MODULE}}`
- Observational values (PDG, Planck, DESI, or other audited references) used in 2+ scripts
- Gate thresholds and pre-registered criteria

## Audit Pipeline

The constants-audit pipeline (run by the `indexer` agent or `/weave --update`) reports:

- **Compliant**: scripts with correct imports
- **Violations**: known stale hardcodes (must fix)
- **Potential**: assignments not in `{{CANONICAL_MODULE}}` and not tagged `# (local)`

Target: **Potential = 0**. Every assignment is either imported from canonical or tagged as local.

## Exit Codes and Verdict Semantics

A gate verdict is **data the script PRINTS**, not the script's exit code. The verdict travels in the `emit_verdict` payload (see `.claude/rules/gate-verdicts.md` -- the script prints the payload, the dispatching agent calls the race-safe MCP writer). The exit code reports script *health*, nothing about the scientific outcome:

- **Exit 0**: the script ran successfully and produced a valid verdict -- regardless of whether that verdict was PASS, FAIL, or INFO.
- **Exit != 0**: reserved for script breakage -- Python traceback, missing input file, SHA mismatch, environment error, pipeline crash.

```python
# CORRECT: verdict is data; exit code reflects script health
verdict = "FAIL" if measured > threshold else "PASS"
print_verdict_payload(verdict, value, content_sha, script_sha)  # agent then calls emit_verdict (race-safe)
sys.exit(0)  # script succeeded regardless of the scientific verdict

# WRONG: couples verdict to exit code
if verdict == "FAIL":
    sys.exit(1)  # NO -- FAIL is a valid scientific result, not a script error
```

**Rationale**: the intake consolidator, `/weave --update`, CI, and any post-tool validation hook key on exit codes to detect broken scripts. Coupling the verdict to the exit code makes it impossible to tell "gate FAILed at threshold" (a normal constraint-map update) from "script crashed" (needs fixing). The two demand different responses.

## All Results Are Good Results

PASS, FAIL, and INFO are all **results**. None of them is an agent failure. A FAIL verdict does not mean the agent was inadequate -- it means the math does not work at that gate, which is useful information: it closes a corridor in the constraint map.

Agents MUST NOT:

- Describe a FAIL as a personal failure ("I could not recover PASS...", "I failed to close the gate...")
- Retry under different conditions hoping for PASS -- this is iterate-until-PASS, a prohibited gate-integrity action (see `.claude/rules/gate-verdicts.md`)
- Frame FAIL apologetically, or treat the solution-space interpretation as a concession
- Change convention / scheme / scan range / tolerance mid-run to reach PASS

Agents MUST:

- Report the verdict factually with value + threshold + tolerance rule
- Write the solution-space interpretation: which corridor is closed, what the FAIL tells us about the constraint surface, which downstream gates are now affected
- Move to the next gate

Same for INFO: INFO is a structured, pre-registered outcome (e.g. a band between PASS and FAIL, or PRE-REG-INCOMPLETE for missing pinnable machinery), not an incomplete result. An INFO verdict fired a pre-registered clause; the plan anticipated the scenario.

## Canonical Write-Order for New Predictions

When a computation gate produces a new framework prediction value `P`, the producing script (or its post-run orchestrator step) MUST follow the write-order **(1) verdict file -> (2) canonical module -> (3) registry/inventory row**:

1. **Step 1 -- Verdict-file emission**: emit the canonical verdict line for the gate via `emit_verdict` (per `.claude/rules/gate-verdicts.md`). This happens FIRST so the value is permanently pinned with its closure SHA.

2. **Step 2 -- Canonical-module promotion**: add `P` and its PROVENANCE entry to `{{CANONICAL_MODULE}}` (e.g. via `update_constant(name, value, session=..., source=..., comment=...)`). This MUST precede Step 3, because computation scripts can only `import` from the canonical module -- they cannot read a value out of a registry markdown file.

3. **Step 3 -- Registry/inventory row**: the registry's designated sole-writer appends a row (or audit-pin sub-row) to the project's results/inventory registry, citing BOTH the verdict-line closure SHA (full 64-hex) AND the canonical-module entry name.

### What goes wrong under the inverted order (1) -> (3) -> (2)

If the registry row lands before the canonical-module promotion, downstream scripts cannot consume `P` via `import` until Step 2 completes -- possibly sessions later. That window leaves the value "canonical in the registry but invisible to script import," a pre-registration-underspecification hazard for any gate that consumes `P`.

### In-session promotion vs carry-forward (decision rule)

- If Step 2 is a single `update_constant(...)` call with no derivation ambiguity: **promote in-session** -- add the entry before terminating the gate.
- If Step 2 requires sub-keying decisions (multiple pathways / pivots / branches) OR primary-source recovery: **carry forward with a 4-field spec** (What / Inputs / Gate / Effort). Queue it for next session; do not promote a single-value stub.

## Machinery-Feasibility Audit

Every machinery pin in a computation script must declare its feasibility envelope, checked at plan-freeze:

- **GPU / accelerator pins**: matrix-dimension feasibility against the VRAM cap. Hard-halt if dense storage exceeds roughly half of available VRAM (see `.claude/rules/computation-environment.md` for the project's hardware).
- **Compute-time pins**: wall-time feasibility against the agent timeout. Flag if the estimated runtime exceeds roughly half the timeout, so a long run does not silently die mid-gate.
- **Numerical-precision pins**: declare the working precision (float64 / complex128 default); call out explicitly if arbitrary precision (mpmath or equivalent) is required.

A pin whose value lies far outside the envelope predicted by a structural argument (e.g. a value more than ~2 orders of magnitude away from an algebraic estimate) is flagged at severity-1 regardless of other checks -- this catches plausible-looking pins that mask a structural divergence.
