---
paths:
  - "{{COMPUTATION_DIR}}/**"
  - "sessions/session-plan/**"
  - "sessions/**"
---

# Gate Verdict Standards -- Physics Override

<!-- DEPLOY: project-root/.claude/rules/gate-verdicts.md -->
<!-- Path-scoped: loads when working in the computation directory or session plans -->
<!-- Source: generalized from parent .claude/rules/gate-verdicts.md -->
<!-- Overrides: universal/rules/gate-verdicts.md -->
<!-- NOTE: frontmatter MUST be at byte 0 for path-scoping to parse; heading + provenance comments follow it. -->

A **gate** is a pre-registered, verifiable pass/fail check on a numerical computation. For this pack, every gate block has eight required fields and every verdict carries a cryptographic closure hash over its inputs.

## Canonical Verdict-File Path (MANDATORY)

The ONE canonical location for a session's verdict file is:

```
{{COMPUTATION_DIR}}/session-{N}/s{N}_gate_verdicts.txt
```

where `{N}` is the session number.

- Agents MUST emit their verdict line to this path and no other.
- Variants such as `{{COMPUTATION_DIR}}/_shared/s{N}_gate_verdicts.txt`, `sessions/session-{N}/s{N}_gate_verdicts.txt`, and `sessions/session-plan/s{N}_gate_verdicts.txt` are FORBIDDEN. If a plan document, rule file, or working paper names any of these, treat it as a documentation bug and write to `{{COMPUTATION_DIR}}/session-{N}/` anyway.
- When plan text is ambiguous (a bare `s{N}_gate_verdicts.txt` with no directory prefix), resolve to `{{COMPUTATION_DIR}}/session-{N}/` by this rule.
- **Rationale**: this is the file `/weave --update` and the downstream audit scripts grep. A verdict written elsewhere is an auditing blind spot. The per-session directory keeps each session's verdict log co-located with its scripts and data.

### Investigation-track path (if the investigation track is in use)

A parallel exploratory track carries its own verdict ledger, structurally mirroring the session track:

```
{{COMPUTATION_DIR}}/investigation-{n}/inv{n}_gate_verdicts.txt
```

Emit via `emit_verdict(session={n}, track="investigation", ...)`. The `track` argument is the ONLY difference from a session emission; all other discipline (closure SHA, supersedes correction, verdict permanence, the canonical line grammar) applies identically across tracks. The `s{N}_`/`inv{n}_` prefixes and `session-`/`investigation-` directory names never cross. An investigation result becomes permanent only when it is PROMOTED into a session (lifted as a carry-forward and recomputed under a `session-{N}` gate); the investigation track is exploratory, not a permanent-results ledger.

## Pre-Registration Protocol

1. **Before computation**: define the gate in `sessions/session-plan/` with the full block. Every gate block MUST include:

   - **Gate ID** (e.g., `V-1`, `M-3`, `T3-<SCRIPT>`)
   - **Trigger**: `[SIGN]`, `[VERIFY]`, `[AUDIT]`, `[VERIFY-THEOREM]`, or `[CHAIN]`
   - **Classification**: a domain-specific category tag
     > NOTE: this pack does not ship a canonical classification enum. The living project authors its own (e.g., a cosmology project might use `PHONONIC | GEOMETRIC | PARTICLE | NON-PHONONIC`; a condensed-matter project might use `LATTICE | BAND-STRUCTURE | TRANSPORT | EXOTIC`). Pick the set of categories that partitions your solution space, document it in a project rule, and use it consistently.
   - **Hypothesis being tested** (one sentence)
   - **Pass/fail/INFO threshold** -- quantitative, with RATIO / ABSOLUTE / THEOREM tolerance rule stated explicitly
   - **Machinery pin (PRDR)**: `N_eval`, `L_max`, `scan_range`, `step_size`, `tolerance`, `scheme`, `convention`, `random_seed`, `GPU path`. A gate that leaves any of these unpinned is PRU-vulnerable (Class 8 failure; see `.claude/rules/epistemic-discipline.md` Pre-Registration Completeness).
   - **Input SHA-256 pins** for every file the script reads (static files get precomputed hashes; dynamic inputs are marked `<computed-at-runtime>`).
   - **Expected output 4-tuple**: `(value=<v>, scheme=<s>, convention=<c>, L_max=<L>)`
   - **Substitution chain**: required for any sign / direction / threshold claim, per `.claude/rules/substitution-chain.md`.
   - **What PASSES and what FAILS mean** for the solution space (the boundary the gate maps, not rhetoric)

2. **During computation**: run the script, record raw numerical output. The script MUST log the SHA-256 of every input in the first 20 lines of stdout and compute the dual SHAs (below). The 4-tuple output tag is printed as the final non-verdict line. The script PRINTS the verdict payload; it does NOT write the verdict file directly.

3. **After computation**: compare output to the pre-registered threshold and emit the canonical verdict line via `emit_verdict` (see "Race-Safe Emission"):

   ```
   {GATE_ID}: PASS|FAIL|INFO -- value=<v> scheme=<s> convention=<c> L_max=<L> content_sha256=<64-hex> script_sha256=<64-hex>
   ```

   The closure SHA pin is MANDATORY on all verdicts.

## Race-Safe Emission via the `emit_verdict` knowledge-MCP tool

The canonical MECHANISM for appending a verdict line is the knowledge-MCP tool `emit_verdict` -- the race-safe, syntax-forced replacement for open-coded `open("a")` verdict-file writes inside producing scripts.

**Why**: a raw `open(path, "a")` append is NOT atomic across processes on Windows. Under concurrent writers it loses lines -- a later writer's buffered flush can land at a stale end-of-file offset and overwrite lines appended in between. `emit_verdict` serializes every write behind a single lock and enforces the line grammar, so the race cannot arise.

**Division of labor**: the producing script computes the two SHAs (it alone holds the input-pin map and the content target) plus the value payload, then PRINTS a delimited block. The dispatching agent parses that block and calls the tool:

1. Script prints, on their own lines:
   ```
   <<<EMIT_VERDICT_PAYLOAD>>>
   {one-line JSON}
   <<<END_EMIT_VERDICT_PAYLOAD>>>
   ```
2. JSON payload keys: `gate_id`, `session`, `value`, `verdict` (one of `PASS|FAIL|INFO|INCONCLUSIVE`), `threshold`, `content_sha256`, `script_sha256`, `source_file`, `track` (default `"session"`; `"investigation"` for the investigation track), `supersedes` (optional; the 64-hex of a prior line this one corrects). Physics gates additionally carry `scheme`, `convention`, and `L_max` (and a `regulator_pin` when a regularization-scheme-dependent quantity is cited, per `.claude/rules/regulator-pin-discipline.md`); these are rendered into the verdict line.
3. The agent calls `mcp__knowledge__emit_verdict(**payload)` -- the single writer.

**The two SHAs**:

- `script_sha256` = SHA-256 of the producing-script bytes alone. Responds to script edits only; reproducibility of the code.
- `content_sha256` = SHA-256 over the full pinned-input closure (script bytes || canonical-module bytes || the canonical JSON of the input-pin map). Responds to any change in the computational content. This is the "closure SHA" the verdict line pins.

Both MUST be the full 64-character lowercase hexdigest -- never a head-truncated prefix. A 16-char head form is allowed in the prose sections of the verdict file for human scan-readability, but NEVER in the canonical line. A producing script that still open-codes a verdict-file `open("a")` append is non-compliant and MUST be migrated to `print_verdict_payload` (see `.claude/templates/script-template.py`). If a legacy script genuinely cannot be migrated before dispatch, serialize the verdict-emitting gates (one writer at a time) as the interim guard.

## Verdict Format

Legacy verdict blocks in plan / handoff docs remain valid in this form:

```
Gate {{GATE_ID}}: {{PASSED|FAILED}}
  Threshold: {{CRITERION}}
  Computed:  {{VALUE}}
  Verdict:   {{PASS/FAIL with brief explanation}}
```

**Canonical form** (required in `{{COMPUTATION_DIR}}/session-{N}/s{N}_gate_verdicts.txt`):

```
{GATE_ID}: PASS|FAIL|INFO -- value=<v> scheme=<s> convention=<c> L_max=<L> content_sha256=<64-hex> script_sha256=<64-hex>
```

## SIGN / MAGNITUDE / REGIME 3-tuple (for `[SIGN]`-trigger gates)

Any gate whose pre-registration includes a `[SIGN]` trigger -- or whose substitution chain pre-registers a directional prediction -- MUST emit a companion annotation row decomposing the verdict into a 3-tuple:

```
# sign_verdict=PASS|FAIL|N/A magnitude_verdict=PASS|INFO|FAIL regime_verdict=VALID|MARGINAL|BREAKDOWN # {GATE_ID} 3-tuple annotation
```

### Field semantics

- `sign_verdict`:
  - PASS = the direction predicted by the substitution chain matches the computed direction (sign of `value - threshold` matches the predicted sign, or sign of `value` for absolute thresholds).
  - FAIL = direction mismatch.
  - N/A = the gate has no directional pre-registration.
- `magnitude_verdict`:
  - PASS = `|value - target| <= pass_band`.
  - INFO = `pass_band < |value - target| <= info_band`.
  - FAIL = `|value - target| > info_band`.
- `regime_verdict`:
  - VALID = the gate's expansion / numerical method stays within its pre-registered regime of validity throughout the scan window.
  - MARGINAL = the regime boundary is crossed within the window, but the breach is `<= 50%` of the intended window.
  - BREAKDOWN = the regime boundary is crossed and the breach is `> 50%` of the intended window. The value is still a well-defined number, but its physical interpretation is not what the pre-registration intended.

### Composite-collapse rule (PRE-REGISTERED -- post-hoc edits are gate-integrity violations)

The composite top-line verdict collapses the 3-tuple deterministically, applied at emit time:

```
if regime_verdict == BREAKDOWN:
    composite = FAIL
elif sign_verdict == FAIL:
    composite = FAIL
elif magnitude_verdict == FAIL and regime_verdict == VALID:
    composite = FAIL
elif magnitude_verdict == FAIL and regime_verdict == MARGINAL:
    composite = INFO   # sign-correct, magnitude-wrong-but-out-of-regime
elif magnitude_verdict == INFO:
    composite = INFO
else:
    composite = PASS
```

Modifying this collapse rule after seeing a verdict is post-hoc pre-registration editing -- a prohibited gate-integrity action.

### Auto-shortening clause (runtime-pinned scan domains)

A cross-check is **auto-shortening** if its tested domain is computed as `min(D_intended, D_runtime)` where `D_runtime` depends on a runtime-pinned quantity (a breakdown threshold, a stability bound, etc.). For every auto-shortening cross-check, the producing script MUST compute `domain_used_frac = D_actual / D_intended`, emit it in the verdict line, and set `regime_verdict` from it:

| `domain_used_frac` | `regime_verdict` | Composite effect |
|:--|:--|:--|
| `>= 0.95` (<=5% shortened) | VALID | unaffected |
| `0.50 <= f < 0.95` (5-50% shortened) | MARGINAL | `magnitude=PASS + regime=MARGINAL => composite INFO` |
| `f < 0.50` (>50% shortened) | BREAKDOWN | `regime=BREAKDOWN => composite FAIL` regardless of other fields |

## Rules

- Gate criteria are defined BEFORE computation -- never after seeing results.
- Verdicts are permanent -- no retroactive in-place changes (see "Option A" below for the correction pathway).
- Only the Skeptic evaluates whether a gate verdict is *meaningful* (a PASS against a trivial criterion is not evidence).
- Record verdicts in the session file AND update the knowledge index via `/weave --update`.
- Canonical-form verdict lines MUST carry the full 64-character closure SHA. The intake consolidator rejects verdict lines with SHAs shorter than 40 hex chars.
- A gate that cannot be evaluated because its producing machinery is unpinned (PRU Class 8) is NOT a FAIL -- it is `INCONCLUSIVE` with value `PRE-REG-INCOMPLETE`. Pin the machinery via PRDR before marking PASS/FAIL.

## Option A -- absolute verdict permanence + `supersedes=` correction

When a producing script emits a corrective verdict line after a prior FAIL/INFO emission (rubric calibration fix, script-bug fix, SHA-hardcoding fix, or any in-script correction within the same dispatch), the policy under absolute verdict permanence is:

1. **The original verdict line is RETAINED on disk.** It is never overwritten, deleted, or edited in place. Permanence is absolute at the byte level.
2. **The corrective line is APPENDED with a `supersedes=<old-64-hex-content_sha256>` tag** naming the original line it replaces.
3. **Downstream consumers cite the LATEST NON-SUPERSEDED line as canonical.** A consumer resolving a gate's verdict scans all lines for the gate ID, excludes every line named in another line's `supersedes=` token, and treats the latest remaining line as authoritative.
4. **The audit trail is preserved by construction.** The chain `original FAIL/INFO -> corrective PASS (with supersedes tag)` is queryable by grep; the `supersedes` tag is the authoritative pointer.
5. **Forward emission discipline.** Every corrective line MUST carry the `supersedes` tag at emission time. Adding the tag later is itself a post-hoc audit-trail edit and is prohibited.
