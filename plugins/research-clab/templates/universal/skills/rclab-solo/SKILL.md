---
name: rclab-solo
description: Execute a wave plan sequentially in the main agent session -- no subagent spawning. Task list is the primary driver: two tasks per gate (compute, update wp) in order.
argument-hint: <wave-plan-file> [--wp <working-paper-path>] [--start <gate-number>]
---

# rclab-solo -- Single-agent sequential wave execution

## --help

If `$ARGUMENTS` contains `--help` or `-h` (or is empty and the user seems confused), read and display `.claude/rclab-help.md`, then stop. Do not proceed with any other phase.

---

Like `/rclab-coordinate`, but the main agent does every gate itself, in order. No subagent spawning. The task list is the state machine; tasks are executed in sequence and drive progression from one gate to the next.

Use this when:
- Subagent spawning is crashing or undesirable.
- A single coherent thread through the wave is wanted (one reasoning narrative, not N parallel ones).
- The wave is small or each gate is quick.

Use `/rclab-coordinate` instead when you want per-gate context isolation or parallelism.

## Usage

```
/rclab-solo sessions/session-plan/session-85-plan-w3.md
/rclab-solo sessions/session-plan/session-85-plan-w3.md --start 4     # resume at gate 4
/rclab-solo sessions/session-plan/session-85-plan-w3.md --wp sessions/session-85/session-85-w3-workingpaper.md
```

## Phase 0 -- Resolve paths

- Plan: `PLAN = <arg1>` (path to a wave-plan file like `session-{N}-plan-w{W}.md`).
- Working paper: `WP = <--wp path>` if given, else derive from the plan's session + wave (e.g. `sessions/session-{N}/session-{N}-w{W}-workingpaper.md`).
- Session: parse `{N}` from the plan filename. Verdict file: `{{COMPUTATION_DIR}}/session-{N}/s{N}_gate_verdicts.txt`.
- Both PLAN and WP must exist. Read both end-to-end.
- Don't read other plan / workingpaper documents.
- Count K = gates in the plan (grep `^## §W{W}-[0-9]`).
- If `--start n`: verify §W{W}-1 through §W{W}-(n-1) are already filled (not still in `*(pending ...)*` state). If any earlier gate is still pending, halt and report.

## Phase 1 -- Build the task list (the primary driver)

Call TaskCreate with **2K tasks, in this exact order**:

```
1.    compute §W{W}-1       -- {GATE_ID_1}
2.    update wp §W{W}-1     -- {GATE_ID_1}
3.    compute §W{W}-2       -- {GATE_ID_2}
4.    update wp §W{W}-2     -- {GATE_ID_2}
...
2K-1. compute §W{W}-K       -- {GATE_ID_K}
2K.   update wp §W{W}-K     -- {GATE_ID_K}
```

Task titles must be literal: `compute §W{W}-{n}` and `update wp §W{W}-{n}`. The gate ID goes in the description.

**This step is not optional.** Without the task list the agent loses its place between gates. The two-task-per-gate decomposition is load-bearing: it gives the user an interrupt point between a verdict landing and its write-up -- if a verdict is surprising, the user can inspect before the write-up goes in.

If `--start n`: skip tasks 1 through 2(n-1); begin the list at `compute §W{W}-n`.

## Phase 2 -- Execute in sequence

For each task in the list, in order:

### `compute §W{W}-{n}`

1. TaskUpdate -> in_progress.
2. **Agent-ownership-takeover (no agent tasking).** Read the plan's `Agent:` field for §W{W}-{n}. If a specific agent is designated, the solo runner TAKES OWNERSHIP of the gate -- DO NOT spawn the designated agent via the Agent tool. Agent tasking has known breaking-bug modes (parallel-writer races on a shared WP, stuck Edit-retry loops, transcript-resume edge cases) that solo execution avoids by construction; the user chose solo deliberately. To preserve substantive context, perform the corpus-load BEFORE step 3:
   - Resolve the designated agent's `subagent_type` via `.claude/templates/agent-roster.md`, then read `.claude/agents/<agent-type>.md` to identify its research-corpus pointers (typically `researchers/<Name>/` per the root `CLAUDE.md` Project Structure table, or a `## Key References` / `## Domain Specialties` block in the agent file for agents whose corpus is integrated rather than a folder).
   - Read 1-3 directly-relevant papers / index files from that corpus before proceeding, picking the ones whose abstracts match the gate's hypothesis keywords.
   - The solo runner remains the SOLE EXECUTOR; the corpus is loaded for CONTEXT only, NOT for delegation. No Agent-tool dispatch under any circumstance during this skill's run.
3. Read §W{W}-{n} from the plan. Extract: method (the procedure to run), machinery/input pins, expected result + PASS/FAIL/INFO thresholds, and the value-substitution steps for any sign/direction/threshold claim.
4. **Knowledge-index pre-compute query (MANDATORY).** Before writing the script, query the knowledge index (per the project's knowledge-query discipline -- the root `CLAUDE.md` Knowledge Index section, and `.claude/rules/knowledge-index-usage.md` if the discipline pack installs one):
   - `mcp__knowledge__search_knowledge("<gate topic keywords from the plan>")` -- check whether the result is already closed, a prior session computed it, or the approach is eliminated.
   - `mcp__knowledge__get_constant("<constant>")` for every project constant named in the plan's substitution steps -- confirm value + provenance match what the plan asserts.
   - `mcp__knowledge__trace_entity("<mechanism or result>")` if the gate tests a named mechanism or references a prior result.
   (If the project has no knowledge MCP, grep `tools/knowledge-index.json` for the same.) Record the queries executed and the salient returns (one line each) in a scratch block -- these go into the working-paper entry in the `update wp` task (the Knowledge Pre-Compute Audit block in `.claude/templates/workingpaper.md`).
   **Branch on result**:
   - If a closed result covers the gate -> cite the closure, mark the gate PRE-CLOSED in §W{W}-{n}, skip steps 5-8, and move to the `update wp` task.
   - If `get_constant` disagrees with the plan's substitution steps -> halt; report to the user; do NOT proceed until reconciled (the knowledge index IS the canonical state).
   - Otherwise -> proceed to step 5.
5. Write the producing script `{{COMPUTATION_DIR}}/session-{N}/s{N}_w{W}_{slug}.py` per the plan's method block. Reuse if already present and matching.
6. Run it with the project's configured Python: `{{PYTHON_CMD}} {{COMPUTATION_DIR}}/session-{N}/s{N}_w{W}_{slug}.py`.
7. The script PRINTS the verdict payload on its own lines -- `<<<EMIT_VERDICT_PAYLOAD>>>` then one-line JSON then `<<<END_EMIT_VERDICT_PAYLOAD>>>` (keys: `gate_id`, `session`, `value`, `verdict` [PASS|FAIL|INFO|INCONCLUSIVE], `threshold`, `content_sha256`, `script_sha256`, `source_file`, `track` ["session"]). The agent then `ToolSearch select:mcp__knowledge__emit_verdict` and calls `emit_verdict(**payload)` -- the race-safe single writer of `{{COMPUTATION_DIR}}/session-{N}/s{N}_gate_verdicts.txt` (see `.claude/rules/gate-verdicts.md`). The script does NOT open-code a file append -- a raw `open("a")` loses lines under concurrent Windows writers.
8. The script's exit code reflects script health only -- PASS/FAIL/INFO all exit 0. Non-zero exit means the script broke (traceback, missing input, env error).
9. If the script broke: TaskUpdate -> blocked, write a one-paragraph diagnostic into the §W{W}-{n} pending block, stop the skill, report to the user. Do NOT proceed to the update task.
10. Else: TaskUpdate -> completed, move to the next task.

### `update wp §W{W}-{n}`

1. TaskUpdate -> in_progress.
2. In `WP`, find §W{W}-{n} and replace the pending blocks (`*(pending agent execution)*`, `*(pending -- include: ...)*`) with the completed answer-log entry matching the correct Pattern from `.claude/templates/workingpaper.md`:
   - Numerical PASS/FAIL -> Pattern A
   - Registration / META -> Pattern B
   - FAIL with remediation -> Pattern C
   - INFO / INCONCLUSIVE with note -> Pattern D
   - ABORTED (cascade-failure) -> Pattern E (no entry; record the state in the Constraint-Map table)
3. Paste the verdict line VERBATIM from the verdict file -- full 64-char `content_sha256` and `script_sha256`, never truncated.
4. The substitution steps in the WP carry the SUBSTITUTED numbers from this run (not the plan's symbolic form).
5. Domain framing (if the project installs a framing rule) appears inline in the reasoning, not as a separate block.
6. TaskUpdate -> completed, move to the next task.

## Phase 3 -- Wave close

After the 2K-th task:

1. Grep the WP for remaining `*(pending` blocks -- there should be zero.
2. Grep the verdict file for the K gate IDs added this wave -- there should be K distinct verdict lines with unique `content_sha256` (duplicate SHAs indicate a hardcoded-literal / copy-paste bug in the producing script).
3. Report: gates attempted (K), PASS / FAIL / INFO / ABORTED counts, script/data/plot file paths, any diagnostics.
4. **Write the Wave {W} Synthesis section** with the math-vs-non-math split (MANDATORY structural form):

   ### Carry-Forward Computations (MATH ONLY -- propagate to S{N+1})

   **Discriminator (4-field test)**: an item belongs HERE iff it satisfies ALL FOUR fields. If ANY field cannot be filled, the item is NOT a math carry-forward -- move it to "Effected In-Session" below and EXECUTE it NOW.
   - **What**: specific equation / numerical observable / structural result to compute
   - **Inputs**: data files, project constants, upstream gates needed
   - **Gate**: pre-registered PASS / FAIL / INFO threshold with explicit tolerance
   - **Effort**: estimated wave-equivalents

   ### Effected In-Session (NON-MATH -- completed by YOU, the orchestrator, BEFORE declaring wave close)

   **MANDATORY -- NON-NEGOTIABLE.** You ARE the final agent for this wave. You hold full Edit / Write access on the project tree. Use it.

   Plan-vs-reality deviations and audit issues surfaced during gate execution must be FIXED in-session, not deferred. Carry-forwards are reserved for GENUINE FUTURE COMPUTATION -- a new gate, a new measurement, a new derivation with a pre-registered threshold -- items satisfying the 4-field test. Carry-forwards are NEVER for hygiene observations on already-correct artifacts, NEVER for registry-status promotions, NEVER for rule-file extensions, NEVER for registry edits, NEVER for knowledge-index single-value updates, NEVER for cross-link fixes, NEVER for audit-script regex extensions. (This is the project `CLAUDE.md` "No Technical Debt" clause, inlined so it loads regardless of how this session was launched.)

   The wave-synthesis section must DISTINGUISH "process observations (closed in-session, NOT propagating)" from "carry-forward computations (genuine future work, propagating)". Do not merge them -- padding the second with the first inflates the forward queue with non-actionable items that get lost across sessions.

   Therefore: every non-math item surfaced across the wave's K gates MUST be EXECUTED NOW with concrete file edits, BEFORE you mark the wave-synthesis task complete.

   **Non-math classification** (move ANY item matching to this section and EXECUTE):
   - Registry / status edits -- status promotions, slot allocations, re-tags, registry-row additions
   - Rule-file extensions -- new sub-clauses, counter advances, taxonomy additions
   - Knowledge-index registrations / updates -- new entities, constant updates via `update_constant(...)`
   - Documentation hygiene -- provenance fixes, broken cross-links, stale-pin remediation, missing "see also" pointers
   - Framework housekeeping -- registry index updates, cross-link pointer rows
   - Audit-script extensions -- regex pattern additions, single-function-scope diagnostic flags

   **Procedure**: enumerate every non-math item from each gate's WP section + your own observations across the wave; for each, EXECUTE the file edit / Write / registry-write NOW; record the action with a concrete `file:line` reference; check the box ONLY after the edit is on disk.

   **Output format** (one row per non-math item):

   - [x] {item description} -- {action taken} -- `{file/path:line-range}` -- {sha-short or session anchor}

   **FORBIDDEN**: leaving any non-math item UNCHECKED; deferring non-math to "Carry-Forward Computations"; writing "queued for S{N+1}" / "TODO" / "deferred" on a non-math item.

5. **Self-audit before wave close.** Grep the WP's "Effected In-Session" subsection for unchecked `- [ ]` items. If ANY remain unchecked, return to step 4, execute them now, then re-grep. Only after `grep -c '^- \[ \]'` on the section returns 0 may you mark the wave-synthesis task complete and report wave close.

6. **Housekeeping ledger (if the discipline pack ships one).** If the project provides `.claude/templates/session-housekeeping.md`, write/update `sessions/session-{N}/session-{N}-housekeeping.md` per that template: Effected-In-Session items from step 4 mirror to its in-session-fix section; genuine math carry-forwards mirror to its future-work section. You ARE the final agent for this wave and hold full Edit/Write access; the ledger write happens at THIS step.

## Safety rules

1. **Task list discipline.** Never skip, reorder, or collapse the compute+update pair. The two-step structure is the skill's primary mechanism.
2. **Single writer.** The main agent is the sole writer for the WP during this skill's run. No concurrent edits from other sessions.
3. **Verdict semantics.** Exit 0 for PASS/FAIL/INFO; FAIL is a valid scientific result, not an agent failure; no iterate-until-PASS (see `.claude/rules/gate-verdicts.md`).
4. **Verdict file path.** Canonical at `{{COMPUTATION_DIR}}/session-{N}/s{N}_gate_verdicts.txt`. Never a shared/`_shared` path, a `sessions/...` path, or a plan-folder path.
5. **No subagent spawning -- agent-ownership-takeover discipline (Phase 2 step 2).** A plan that designates a specific agent does NOT cause the solo runner to spawn it. The solo runner TAKES OWNERSHIP of every gate; the designated agent's corpus is loaded for context, but the agent itself is NEVER invoked through Agent-tool dispatch during this skill's run. If a gate genuinely requires isolation or context that solo cannot supply even with the corpus loaded, halt with a diagnostic -- switching to coordinate mid-run is not this skill's job.
6. **Effected-In-Session is NON-NEGOTIABLE (Phase 3 steps 4-5).** Every non-math item surfaced in the wave MUST be executed by the orchestrator with concrete file edits before the wave-synthesis task is marked complete. Non-math items deferred to the next session are FORBIDDEN per the project `CLAUDE.md` "No Technical Debt" clause (the full substance is inlined in Phase 3 step 4, so it loads regardless of session-launch form). Only items satisfying the 4-field math test propagate forward. Phase 3 step 5 self-audit ENFORCES this: `grep -c '^- \[ \]'` on the "Effected In-Session" subsection must return 0 before wave close. This session does NOT close until all non-math items are executed with concrete edits and the wave-synthesis task is marked complete -- no housekeeping entries are carried forward; they are taken care of before this task can complete.

## Error handling

| Condition | Action |
|:----------|:-------|
| PLAN file missing | Stop, report path |
| WP file missing | Stop, report path |
| `--start n` but an earlier gate still pending | Stop, report which gates need filling first |
| Python script crash (non-zero exit) | TaskUpdate -> blocked, write diagnostic into pending block, stop |
| Verdict emission fails | Stop, report, do NOT proceed to the update task |
| Update task but §W{W}-{n} pending blocks already gone (gate filled by another process) | TaskUpdate -> completed with a one-line "pre-filled" note, proceed |
| Duplicate `content_sha256` detected in Phase 3 | Report the duplicate, flag the producing script for a hardcoded-SHA bug, do not block wave close |
| User interrupts | Task list persists in TaskList state. Resume via `/rclab-solo <plan> --start <next-pending-n>`. |

## Relationship to other skills

- `/rclab-coordinate` -- parallel-subagent variant of the same role. Pick based on whether you want per-gate context isolation (coordinate) or one reasoning thread (solo).
- `/rclab-plan` -- produces the wave plans and WP shells this skill consumes.
- `/rclab-reflect` -- optional post-execution reflection pass over the filled WP after wave close.
- `/rclab-investigate` -- runs after wave close on the filled WPs to generate the next session's workshop-schedule campaign.
