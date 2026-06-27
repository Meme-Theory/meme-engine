# Working Paper Template

The working paper is the answer log for a wave. `/rclab-coordinate` (or `/rclab-solo`) writes each gate's completed entry into this file. It is NOT a plan-echo: at dispatch it carries pending placeholders; at completion each placeholder is REPLACED with the real answer.

## At dispatch (orchestrator)

Write `sessions/session-{N}/session-{N}-w{W}-workingpaper.md` with one section per gate, each holding pending blocks:

```markdown
# Session {N} Wave {W} -- {WAVE_TITLE} (Results Working Paper)

**Session**: {N} | **Wave**: {W} | **Plan**: session-{N}-plan-w{W}.md | **Theme**: {THEME}

## Gate Sections

### §W{W}-1. {GATE_ID_1} ({agent-type})

**Status**: NOT STARTED
**Gate ID**: `{GATE_ID_1}`
**Trigger**: `{TRIGGER}`
**Classification**: **{CLASS}**
**Agent**: `{agent-type}`
**Hypothesis**: {one-line paraphrase from the plan}

**Output Artifacts** (closure-verification checklist):
*(pending -- for each entry in the plan's output-artifacts list: confirm the file exists (`ls <path>`) AND paste `grep -E '<must_contain>' <path>` output for every content pattern the plan requires. This block IS the per-gate completion checklist the agent verifies before TaskUpdate; an entry with the file missing OR any required pattern returning empty means the gate did not properly close. Detection is by content presence only -- never by line/byte count.)*

**Knowledge Pre-Compute Audit**:
*(pending -- list the knowledge-index queries run before writing the script, with one-line salient return each; mark PRE-CLOSED if a closure covers the gate. Per the project's knowledge-query discipline.)*

**Verdict**:
*(pending agent execution)*

**Results**:
*(pending -- include: {comma-separated list of plan deliverables})*

### §W{W}-2. ...
(Repeat per gate.)

## Wave {W} Synthesis (team-lead)

## Carry-Forward Computations

## Constraint-Map Updates

## Files Produced
```

## At gate completion (runtime agent)

Replace your gate's `*(pending ...)*` blocks with the completed answer-log entry. Pick the Pattern that fits your gate type:

| Pattern | Gate type | What the entry contains |
|:--------|:----------|:------------------------|
| **A** | Numerical PASS / FAIL | Verdict line (verbatim from the verdict file), computed numbers, cross-checks, the explicit value-substitution steps, and a short assessment |
| **B** | Registration / META | The registration record -- what was registered, the canonical home/path, and the identifiers assigned |
| **C** | FAIL with remediation | The FAIL verdict + the remediation path (what would have to change for a future PASS) |
| **D** | INFO / INCONCLUSIVE with note | The inconclusive outcome, why it is inconclusive, and what it nonetheless informs |
| **E** | ABORTED (cascade-failure) | No gate entry; record the state change in the Constraint-Map table instead |

Every completed entry keeps the **Knowledge Pre-Compute Audit** block filled (the queries you ran before computing and their salient returns). The verdict line is pasted VERBATIM -- full 64-char `content_sha256` and `script_sha256`, never truncated.

## At wave close (team-lead)

Write the **Wave {W} Synthesis** section: what the wave changed, what holds, what breaks or strains.

Write the **Carry-Forward Computations** section: one `### {CF-ID} -- {one-line title}` sub-heading per genuine future-work item, each with a 4-field spec (What / Inputs / Gate / Effort). This section is the canonical carry-forward source `/rclab-plan` consumes for next-session planning, so it MUST be a top-level `## ` heading (not buried in synthesis prose), and it is MATH ONLY -- process observations and in-session hygiene do NOT belong here (they were executed in-session per the "Effected In-Session" discipline; see the project `CLAUDE.md` "No Technical Debt" clause). An empty CF section is acceptable IFF the wave produced zero genuine future-work items; in that case write a single line "No carry-forwards: all wave outcomes closed in-session" so the absence is intentional.

Append the session-level **Constraint-Map Updates** and **Files Produced** tables.

If the discipline pack ships `.claude/templates/session-housekeeping.md`, also write/update `sessions/session-{N}/session-{N}-housekeeping.md` per that template (in-session fixes in its §A; genuine math carry-forwards mirrored to its future-work section).

## Rules

1. The verdict line is canonical at `{{COMPUTATION_DIR}}/session-{N}/s{N}_gate_verdicts.txt` per `.claude/rules/gate-verdicts.md`; the working paper mirrors it (it does not replace it).
2. One writer per gate. The team-lead writes only the Synthesis + Carry-Forward Computations + Constraint-Map + Files-Produced sections.
3. Every completed gate entry includes the **Knowledge Pre-Compute Audit** block listing the knowledge-index queries run before compute and their salient returns. An entry without this block is incomplete -- the knowledge query is the compute procedure's first action (see `rclab-solo` Phase 2), not a post-hoc citation.
4. **Every wave-close MUST produce a `## Carry-Forward Computations` section** with one 4-field spec (What / Inputs / Gate / Effort) per genuine future-work item, per the project `CLAUDE.md` "No Technical Debt" clause. It MUST be a top-level `## ` heading so `/rclab-plan` can grep for it as a distinct block. Process observations and in-session hygiene do NOT belong here.

## Anti-pattern

Do not use `<!-- Runtime agent fills: ... -->` stubs -- they survive into the final document and turn the paper into a plan-echo instead of an answer log. The observed failure mode: stub comments survive runtime dispatch because agents read them as permanent scaffolding rather than placeholders. The pending-block pattern (`*(pending -- include: ...)*`) replaces the WHOLE block on completion; stub comments ask the agent to fill in-place around them, which consistently fails.
