---
paths:
  - "{{COMPUTATION_DIR}}/**"
  - "sessions/session-plan/**"
  - "sessions/**"
---

# Mechanical-Closure Discipline (Orchestrator-Authored Verdict Emission)

<!-- DEPLOY: project-root/.claude/rules/mechanical-closure-discipline.md -->
<!-- Path-scoped: loads in the computation directory and session plans -->
<!-- Source: generalized from parent .claude/rules/mechanical-closure-discipline.md (honest-closure kernel; the project-specific layer-separability carve-out is intentionally omitted) -->
<!-- NOTE: frontmatter MUST be at byte 0 for path-scoping to parse; heading + provenance comments follow it. -->

## Scope

A mechanical-closure script emits verdict lines WITHOUT specialist-agent dispatch and WITHOUT physics computation. It documents that a gate could not be evaluated because at least one upstream prerequisite has a verdict != PASS -- the gate is structurally untestable this session.

This rule distinguishes HONEST mechanical closure from the task-complete-lie failure mode (a verdict line appended while the working-paper section is silently skipped, and the agent reports completion anyway). Cross-link: `.claude/rules/agent-standards.md` Completion Verification.

## When mechanical closure IS acceptable

A mechanical-closure script may be authored ONLY when ALL of the following hold:

1. **Upstream-block topology is the cause**: every gate the script closes has >=1 upstream prerequisite with verdict != PASS, AND the plan's downstream decision-point table specifies the documented outcome for a prereq-block (typically "PRE-REG-INCOMPLETE, deferred to next session"). The plan author MUST have anticipated the prereq-block scenario. If the plan does not address it, the closure script is post-hoc plan editing (a prohibited gate-integrity action) and is FORBIDDEN.

2. **Verdict honesty**: emitted verdicts are FAIL or PRE-REG-INCOMPLETE (INCONCLUSIVE), NEVER PASS. The descriptive value string follows a `value='PRE-REG-INC_blocked_by_<symbol>_<status>'` or `value='upstream_<reason>'` pattern. A PASS verdict from a mechanical-closure script is an ansatz-forced PASS -- prohibited.

3. **Per-gate-distinct closure SHA**: even when multiple gates share a prerequisite set, the pin map feeding each closure SHA MUST embed per-gate identity keys (gate id, working-paper section id, scheme, convention) so the resulting closure SHAs are pairwise distinct across all gates the script closes.

4. **Audit-trail signature**: the verdict line MUST carry a descriptive `value` string naming the blocking prerequisite and its status. A future audit MUST be able to grep the line and verify the named upstream gate exists with the named status in the same verdict file.

5. **Working-paper update is in-script**: the closure script MUST update the corresponding working-paper section (Status, Verdict, Results, framing blocks) IN THE SAME RUN as the verdict-line emission. A closure script that emits the verdict line but skips the working-paper update is the task-complete-lie pattern and is FORBIDDEN.

## When mechanical closure indicates a PLANNING DEFECT

If the number of gates a closure script covers reaches the threshold `N_PLANNING_DEFECT = 4` of the wave's total gates, the wave plan was OVER-OPTIMISTIC about prerequisite landings. This is a plan-authorship PRU vulnerability: the planner should have routed those gates into a later wave conditional on the prerequisites landing, rather than into the current wave with mechanical-closure deferral.

The PLANNING-DEFECT trigger fires on `covered_count >= N_PLANNING_DEFECT = 4` INDEPENDENTLY of item-1 above (the trigger is count-keyed). The closure script remains acceptable AT EXECUTION TIME (it preserves the audit trail honestly), but the next session's planner MUST log this as a plan-authorship lesson and adjust wave-partitioning to avoid recurrence.

## Audit-trail signature

Canonical verdict-line pattern for a mechanical closure (see `.claude/rules/gate-verdicts.md` for the full grammar):

```
{GATE_ID}: FAIL -- value='PRE-REG-INC_blocked_by_<sym1>_<status1>' scheme=<plan-pinned> convention=<plan-pinned> L_max=<plan-pinned> content_sha256=<64-hex> script_sha256=<64-hex>
```

Companion comment row:

```
# {GATE_ID} PRE-REG-INC per session-{N}-plan-w{W}.md; deferred to S{N+1}; required prereqs: [<sym1>, <sym2>, ...]
```

## Audit checks

An audit over the verdict file greps for the `value='PRE-REG-INC_blocked_by_*'` / `value='upstream_*'` patterns and verifies, for each match:

1. the named upstream gate exists in the same file;
2. the named upstream gate's status matches what the closure value string asserts;
3. the closure line's closure SHA is unique across all canonical lines in the file;
4. the corresponding working-paper section has been updated (Status != "NOT STARTED", verdict block populated).

## Cross-references

- `.claude/rules/gate-verdicts.md` -- verdict-line schema, race-safe emission, supersedes correction.
- `.claude/rules/agent-standards.md` -- Completion Verification (the task-complete-lie failure mode this rule prevents).
- `.claude/rules/epistemic-discipline.md` -- Pre-Registration Completeness (mechanical closure is the in-session honest reporting for an upstream-blocked, PRU-clear gate).
