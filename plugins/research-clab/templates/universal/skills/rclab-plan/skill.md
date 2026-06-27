---
name: rclab-plan
description: Plan the next compute session -- mechanical carry-forward gathering, wave partition, then a SWARM of per-wave planners that each design full-fidelity test cases for their slice of the carry-forward. Consolidate (single plan + single working paper) or fan-out (per-wave plan files + per-wave working papers). Also MAINTAINS and CONSUMES the project's forward registers (open-questions / priority / open-channel) from the just-mined session, so plan-time doubles as the session wrap-up. Supports an INVESTIGATION MODE (`--investigation [n] --from <seed>`) that plans an exploratory `investigation-{n}` effort in the parallel `sessions/investigation/` track from a free-form seed, as a MIXED-TYPE wave plan (compute / review / workshop gates). For workshop-schedule campaigns derived from the just-closed session, use `/rclab-investigate` instead.
argument-hint: <topic> [--session <N>] [--investigation [n]] [--from <seed>...] [--waves <N>] [--consolidate|--fanout] [--planner <agent-type>] [--prompter <agent-type>] [--context <file>...] [--dry-run]
---

# Collab-Plan -- Session Plan & Working-Paper Bootstrap (Swarm Architecture)

## --help

If `$ARGUMENTS` contains `--help` or `-h` (or is empty and the user seems confused), read and display `.claude/rclab-help.md`, then stop. Do not proceed with any other phase.

---

Three-phase pipeline:

1. **Mechanical context gathering** -- collect every carry-forward computation produced by the prior session's syntheses + workshops, dedupe, write a single context file. **No interpretation.** No reading of MEMORY, prior gate verdicts, knowledge index, or permanent results -- those live in the planner agent's auto-loaded memory or via MCP.
2. **Mechanical wave partition** -- orchestrator reads the deduplicated carry-forward table, assigns items to waves by theme, merges semantic duplicates, writes a wave-partition manifest. **No interpretation of the items themselves** -- just bucketing.
3. **Swarm plan generation** -- spawn N per-wave planner agents (one per wave, or more if a wave is dense) IN PARALLEL. Each reads the context file + its assigned carry-forward items and designs the full-fidelity test case for each entry in its wave. Consolidate into one plan file OR keep as per-wave plan files (user choice / default consolidate).
4. **Working paper generation** -- mirror consolidation choice. Single working paper (if consolidated) or per-wave working papers (if fanned out).

**Why a swarm and not a single planner**: a single planner trying to hold ~100 carry-forward items in working memory while writing 3000+ lines of structured gate blocks hits the stream watchdog (observed: two <domain-generalist> planners stalled at 600s with zero writes on a ~100-item table). Per-wave planners holding 6-15 items each consistently succeed. Stalled per-wave agents get split further into sub-waves (W1 -> W1a + W1b) -- **never** papered over with a leaner spec.

**Plus two cross-cutting capabilities.** (a) Plan-time MAINTAINS and CONSUMES the project's forward registers (Phase 2.5), so a live open question with no working-paper carry-forward still gets planned and the registers do not silently rot; plan-time doubles as the session wrap-up (there is no separate wrap-up command). (b) INVESTIGATION MODE (`--investigation`) plans an exploratory effort in the parallel `sessions/investigation/` track from a free-form seed instead of prior-session carry-forwards -- see "Investigation Mode" below.

## Precedent for per-sub-session fan-out

This skill extends a pre-existing project pattern. See `sessions/session-plan/archive/`:
- Sessions 17-22: `session-{N}a-prompt.md` + `session-{N}b-prompt.md` + `session-{N}c-prompt.md` + `session-{N}d-prompt.md`
- Session 28: `session-28-prompt-a.md` + `session-28-prompt-b.md` + `session-28-prompt-c.md`
- Session 29: `session-29Aa-prompt.md` through `session-29Ac-prompt.md` + `session-29Ba-prompt.md` + `session-29Bb-prompt.md`
- Session 30A: `session-30Aa/Ab/Ac-prompt.md`

Those were workshop/panel sub-sessions producing one prompt per group. The swarm architecture generalizes to compute format: one plan/prompt/working-paper per wave.

## Usage

```
# Most common -- bootstrap next session from carry-forwards, consolidate to single plan
/rclab-plan

# Pin the session number explicitly
/rclab-plan --session 84

# Fan out: keep per-wave plan files, produce per-wave working papers
/rclab-plan --fanout

# Override planner (default <domain-generalist>; <domain-generalist> common alternative)
/rclab-plan --planner <domain-generalist>

# Override wave count (default: auto-partition by theme)
/rclab-plan --waves 10

# Extra context file folded verbatim into context file
/rclab-plan --context sessions/observational_avenues.md

# Optional topic label -- does NOT scope the plan
/rclab-plan "core-result follow-ups"

# Dry-run -- gather + dedupe + write context file + partition, do NOT spawn planners
/rclab-plan --dry-run

# Investigation mode (parallel exploratory track; see "Investigation Mode")
/rclab-plan --investigation --from sessions/investigation/investigation-1/_synthesis.md   # auto-next n, seed from a synthesis
/rclab-plan --investigation 2 --from "sessions/investigation/investigation-1/*.md"        # pin n=2, seed from a whole survey (glob)
```

---

## Investigation Mode (`--investigation`)

`/rclab-plan` has two modes. **Session mode** (default; everything outside this section) plans `S{N+1}` from `S{N}` working-paper carry-forwards + forward registers. **Investigation mode** (`--investigation [n] --from <seed>`) plans `investigation-{n}` for the parallel exploratory track at `sessions/investigation/`, seeded from a **free-form input** instead of prior-session carry-forwards. The pipeline shape is identical (gather -> partition -> swarm -> validate -> prompt -> report); the deltas are concentrated here. Output shape per `.claude/templates/plan-investigation.md`. The track and its index live at `sessions/investigation/index.md`.

Investigation results are EXPLORATORY: to become permanent framework results they must be PROMOTED into a numbered session (carried forward as a session-mode gate and re-established on the canonical track). The investigation track explores; the session track canonizes.

> Cross-skill note: investigation plans carry MIXED gate types (compute / review / workshop). `/rclab-coordinate` branches dispatch on each gate's `gate_type`. A project whose `/rclab-coordinate` is compute-only must extend it to dispatch review/workshop gates before running an investigation plan end-to-end.

### Trigger + number resolution

- `--investigation` (bare) -> auto-next: glob `sessions/investigation/investigation-*/`, pick the highest existing `n`, new `n = max + 1`. (By convention `investigation-1` is the free-form root survey that seeds the track, so planned efforts start at `investigation-2`.)
- `--investigation n` -> pin `n`. If `investigation-{n}/` already has a plan, AskUserQuestion overwrite / next / cancel (same collision protocol as session mode, Phase 1c).
- `--investigation` and `--session` are mutually exclusive. `--from` is REQUIRED in investigation mode -- the seed IS the scope.

### Paths (override Phase 1b)

```
INV_DIR            = sessions/investigation/investigation-{n}/
SEED_FILE          = sessions/investigation/investigation-{n}/investigation-{n}-seed.md      (the CONTEXT_FILE analog)
PARTITION_FILE     = sessions/investigation/investigation-{n}/investigation-{n}-partition.md
PLAN_FILE          = sessions/investigation/investigation-{n}/investigation-{n}-plan.md       (consolidate)
PLAN_INDEX         = sessions/investigation/investigation-{n}/investigation-{n}-plan-index.md (fanout)
WAVE_PLAN_FILE(i)  = sessions/investigation/investigation-{n}/investigation-{n}-plan-w{i}.md
WAVE_WP_FILE(i)    = sessions/investigation/investigation-{n}/investigation-{n}-w{i}-workingpaper.md
VERDICT_FILE       = {{COMPUTATION_DIR}}/investigation-{n}/inv{n}_gate_verdicts.txt           (compute gates only)
```

### Phase-2-delta -- gather from the seed, not carry-forwards

Instead of mining a prior session's working-paper carry-forwards (Phase 2), READ the `--from` seed(s) in full and translate them into candidate gate items. A survey-style seed typically offers:

| Seed section | Becomes |
|:--|:--|
| A "highest-leverage next steps" list | The PRIMARY source -- each item usually already states a gate + effort; lift it near-verbatim into a candidate. |
| Untraveled questions / open bridges | Candidate gates: a question needing adjudication between two competing readings -> workshop; one needing a synthesis/characterization -> review; one with a concrete numerical test -> compute. |
| Gaps / contradictions / assumptions / refinements | Context + candidate items wherever a concrete gate is stated; a contradiction with two genuinely-competing readings is a strong workshop seed. |

Each candidate records: the 4-field-equivalent (What / Inputs / Gate / Effort), its **gate_type** (see Phase-2.7-delta), and its **seed anchor** (which source doc + which item). No invented items -- the seed is the scope, exactly as carry-forwards are the scope in session mode. Deduplicate convergent items across seed files. Write `SEED_FILE` (the `CONTEXT_FILE` analog): deduped candidate table + per-item seed-anchor + source manifest + any `--context` files folded verbatim.

### Phase-2.5-delta -- forward-register maintenance is SKIPPED

Investigation mode does NOT close a session, so the session-mode forward-register maintenance (Phase 2.5) is **SKIPPED entirely**. In its place, the index-registration step fires: append (or update) the `investigation-{n}` row in `sessions/investigation/index.md` per that file's schema -- **topic** (from the seed; never invented), **driver/seed** (the `--from` source + what produced it), **plan** path, status `PLANNED`. Append-only; do not reorder or delete rows. This is the "plan touches the index" half of the maintained-by contract; `/rclab-investigate --investigation n` housekeeps the other half. The index is a DATA register (append-only), not a rule file.

### Phase-2.7-delta -- partition + assign gate_type

Bucket by theme/domain (owner = the seed author's domain). Then assign **gate_type** to each item by applying the `.claude/rules/Investigating-Workshops.md` Q1/Q2/Q3 discriminator (the SAME decision the session pipeline makes at `/rclab-investigate` time -- here it is made at plan time, because the investigation plan IS the schedule):

- concrete compute with a pre-registered numerical gate + effort -> **compute** (whether large or small; "one reasoning thread vs many" is NOT a gate_type axis).
- a tension with two genuinely-competing readings where cross-rebuttal is essential to converge (Q1a) -> **workshop** (EXACTLY 2 agents).
- independent reading + write-up -- "synthesize / characterize / survey X" (Q1b) -> **review** (1+ agents, default 1 = the question owner).

**There is NO `solo` gate_type.** Every gate is dispatched to a positioned specialist agent. The reason is load-bearing: a research agent's system prompt + memory + corpus pointers position the model in the region of its domain expertise; the orchestrator has no such positioning and is not trusted to compute. `/rclab-solo` is the legitimate no-spawn path, but it is a SEPARATE session launched AS a research agent running its whole plan itself -- the executor is still a positioned specialist. Stamping `solo` onto individual gates routes work to the one agent not positioned to do it.

Write `PARTITION_FILE` with a **gate_type column** (`compute` | `review` | `workshop`) per item -- the manifest `/rclab-coordinate` reads to branch dispatch. Mixed-type waves are normal and expected.

### Phase-3-delta -- mixed-type gate blocks

Per-wave planners read `.claude/templates/plan-investigation.md` (instead of `plan-compute.md`) and set each gate's `gate_type`, filling the type-appropriate fields:

- **compute** -> full gate block + verdict rubric + output artifacts WITH a verdict line pinned to `{{COMPUTATION_DIR}}/investigation-{n}/inv{n}_gate_verdicts.txt` (NEVER a `session-{N}` path).
- **review** -> the review block (agents / sources / output paths / context); no numeric gate; output = one synthesis per agent, NO verdict line.
- **workshop** -> the workshop block (EXACTLY 2 agents / rounds / sources / output path / adjudication question / context); no numeric gate; output = the workshop md, NO verdict line.

Per-wave planner prompt: same as session mode (Phase 3b) but swap the "READ ONLY this one file" target so it also reads `.claude/templates/plan-investigation.md`, and instruct the planner to set `gate_type` per its assigned `PARTITION_FILE` rows. Owner-agent / stall-handling / verify-grep all unchanged.

### Validation + working-paper deltas

Any plan validation (completeness / upstream-pin checks, Phase 3d) runs on the **compute gates only**. For **review/workshop** gates, readiness = artifact-existence: the `review:`/`workshop:` block is complete (agents present; workshop has EXACTLY 2; sources + output paths set) and output artifacts list the deliverable with its content markers. A review/workshop gate is NOT pin-validated and is NOT pre-registration-vulnerable for lacking a numeric threshold. WP prompters (Phase 5) write per-wave WP shells under `INV_DIR`: compute sections use the normal pending-block + verdict-line closure; review/workshop sections carry a pending block pointing at the deliverable + an artifact-existence checklist, NOT a verdict-line block.

### Report + next step

Report per Phase 6 with the investigation paths. Next step: `/rclab-coordinate sessions/investigation/investigation-{n}/investigation-{n}-plan-index.md` (it branches on the three gate types directly).

---

## Phase 0: Parse & Validate

### 0a. Arguments

| Arg | Required | Default | Description |
|:----|:---------|:--------|:------------|
| `<topic>` | no | auto-generated | Cosmetic label only. Scope is the carry-forward mined in Phase 2 (or the seed in investigation mode). |
| `--session <N>` | no | auto-detect (latest plan number + 1) | Session number for the new plan (SESSION mode). Mutually exclusive with `--investigation`. |
| `--investigation [n]` | no | -- (presence = investigation mode; `n` auto-next) | Switches to INVESTIGATION mode (see "Investigation Mode"). Bare -> auto-next `investigation-{n}`; `n` pins. Mutually exclusive with `--session`. |
| `--from <seed>` | no | -- (REQUIRED in investigation mode) | Free-form seed input: a survey output, a synthesis, or a file/glob/dir of exploratory docs. Repeatable. The seed IS the scope. |
| `--waves <N>` | no | auto-partition by theme | Wave count (the orchestrator's partition can still split a wave if it stalls) |
| `--consolidate` | no | true (default) | Produce single `session-{N}-plan.md` + single working paper |
| `--fanout` | no | false | Produce per-wave plan files + per-wave working papers; write thin `session-{N}-plan-index.md` referencing them |
| `--planner <type>` | no | `<domain-generalist>` | Default per-wave planner agent type. Per-wave overrides in §3a map. |
| `--prompter <type>` | no | `<domain-generalist>` | Prompter agent type |
| `--context <file>` | no | none | Extra context file(s) folded verbatim. Repeatable. |
| `--dry-run` | no | false | Phase 1 + 2 + 2.7 only; do not spawn planners |

`--consolidate` and `--fanout` are mutually exclusive. `--consolidate` is the default.

### 0b. Topic is a label, not a scope

The topic does NOT gate execution. The scope of every `/rclab-plan` run is the full carry-forward mined in Phase 2.

- If `<topic>` was provided, use it verbatim in the context-file header.
- If `<topic>` is empty, default to `"S{N} carry-forward plan"`.

(Design note: the topic is just a label -- a run tests the entire carry-forward, not the topic.)

### 0c. Validate agent types

Check `--planner` and `--prompter` exist in `.claude/agents/`. See `.claude/templates/agent-roster.md`. If invalid, list available types and stop.

### 0d. Validate context files

If `--context <file>` was provided, verify each file exists (Read 1 line). If any missing, report and stop.

### 0e. Mode select

If `--investigation` is present -> INVESTIGATION mode. Jump to "Investigation Mode" for the Phase-1/2 deltas; the swarm/validate/prompt/report phases run as written with the investigation paths. `--investigation` and `--session` cannot both be set (stop with error if both passed). In investigation mode `--from` is REQUIRED -- verify each `--from` glob/dir/file resolves to >=1 existing file (Read 1 line of one); missing -> report and stop. Absent `--investigation` -> SESSION mode (everything below, unchanged).

---

## Phase 1: Session ID Resolution

### 1a. Auto-detect session number

If `--session` was NOT provided:
1. Glob `sessions/session-plan/session-*-plan.md`
2. Extract highest N from filenames
3. New session = N + 1

### 1b. Set output paths

```
CONTEXT_FILE    = sessions/session-plan/session-{N}-context.md
PARTITION_FILE  = sessions/session-plan/session-{N}-partition.md
PLAN_FILE       = sessions/session-plan/session-{N}-plan.md          (consolidate mode)
PLAN_INDEX      = sessions/session-plan/session-{N}-plan-index.md    (fanout mode)
WAVE_PLAN_FILE  = sessions/session-plan/session-{N}-plan-w{i}.md     (one per wave)
WORKING_PAPER   = sessions/session-{N}/session-{N}-results-workingpaper.md                 (consolidate mode)
WAVE_WP_FILE    = sessions/session-{N}/session-{N}-w{i}-workingpaper.md                    (one per wave, fanout mode)
```

### 1c. Collision check

If `PLAN_FILE` or `PLAN_INDEX` already exists, AskUserQuestion: "Session {N} plan already exists. Overwrite / Pick next number / Cancel?"

---

## Phase 2: Mechanical Context Gathering

**Purely mechanical.** No interpretation, no synthesis, no judgment about what matters. The carry-forward sections of the prior session's syntheses + workshops are the SOURCE OF TRUTH for what the next session must compute. Gather, dedupe, write, stop.

### 2a. Identify the prior session

`PRIOR = N - 1`. If `sessions/session-{PRIOR}/` missing, fall back to the latest session folder that exists; AskUserQuestion if ambiguous.

### 2b. Glob the wrap-up sources

```
sessions/session-{PRIOR}/session-*-workshop.md      # workshop wrap-ups (## Wrap-Up)
sessions/session-{PRIOR}/session-*-synthesis.md     # solo synthesis wrap-ups (## V. Carry-Forward Computations)
sessions/session-{PRIOR}/workshops/*.md             # workshop outputs in subdirectory
```

Optional (only if they exist):
```
sessions/session-{PRIOR}/session-*-<topic>-plan.md
```

### 2c. Extract carry-forward entries

- **Workshop wrap-up**: find `## Wrap-Up` near end; extract `### Carry-Forward Computations` numbered list (4 fields: what / inputs / gate / effort).
- **Solo synthesis**: find `## V. Carry-Forward Computations`; extract numbered list (4 fields).
- **Closeout solo** (e.g., `session-{PRIOR}-{agent}-s6-synthesis.md`): may contain an Appendix B consolidated §IX Carry-Forward. If present, prefer it (the closeout solo deduplicated already).

If a source file lacks a structured Wrap-Up / §V section, **report which file is missing** and skip it. Do not grep-fall-back.

### 2d. Deduplicate

Merge by computation title (case-insensitive) OR explicit gate ID match. For each unique entry record:
- Computation title
- 4 fields
- Source file list (convergence count = `len(sources)`)
- Reviewer origin (which agent's synthesis it came from -- drives wave-owner selection in §3a)

### 2e. Write the context file

```markdown
# Session {N} -- Context File

**Generated**: {today}
**Topic label**: {topic}

## Source Wrap-Ups
| File | Lines | Origin (agent or workshop) |

## Deduplicated Carry-Forward Computations
| # | Gate ID | Computation | What | Inputs | Gate criteria | Effort | Convergence | Origin |

## Extra Context (from --context flags)
```

The context file contains ONLY the carry-forward table and source manifest. No MEMORY.md dump. No prior verdicts. No knowledge-index snapshot. Planners query MCP directly.

### 2f. Dry-run early exit

If `--dry-run` AND `--waves` unset, stop after Phase 2. Report source manifest + entry count + context path.

---

## Phase 2.5: Maintain & Consume the Forward Registers

The framework's forward direction lives in a small set of **curated registers**, not in the working-paper carry-forwards alone. These registers rot silently whenever nothing consumes them. This phase closes that gap by making `/rclab-plan` the single place that BOTH **maintains** the registers from the just-mined session AND **consumes** them as a planning source. Plan-time IS the de-facto session wrap-up (the framework has no separate wrap-up command); register maintenance rides on the Phase-2 session mining already done.

If a project keeps no forward registers, this phase is a no-op -- proceed to Phase 2.7. Under `--dry-run`, Step 1 (MAINTAIN, which writes) is SKIPPED; Step 2 (CONSUME) runs read-only to inform the partition preview.

### The forward-register set (generic)

| Register (example path) | Holds | Maintained here | Consumed here |
|:--|:--|:--|:--|
| Open-questions register (`sessions/framework/open-questions.md`) | the standing open-question ledger | yes (fold in S{PRIOR} resolutions) | yes (still-open questions = candidates) |
| Priority register (`sessions/framework/priority-register.md`) | value-of-information / priority tiers + an actionable queue | yes (currency audit + rebuild) | yes (the queue orders Wave 1; tiers order the rest) |
| Open-channel ledger (`sessions/framework/open-channel-ledger.md`) | curated live channels / threads | yes (refresh + mark closed) | yes (live channels = candidates) |
| Status register (`sessions/framework/assumptions.md`) | assumption / claim status (proven / conditional / broken) | yes (status down-tags only) | yes (broken/conditional with a tractable gate = candidate) |

A project names these per its domain; the discipline is identical. An owner-routed register (a domain register one agent is the sole writer of) is NOT direct-edited here -- emit a dispatch for that agent instead.

### Step 1 -- MAINTAIN: reconcile the just-closed session into the registers

Every update MUST be **traceable** to S{PRIOR}'s verdict file + session handoff + working-paper closures -- **no invented closures**. Updates are append-only over verbatim originals (record closures as updates; do not overwrite the original wording).

1. **Priority register** -- run the currency audit; if it lags, REBUILD before ordering (do not re-note-and-defer -- that loop is exactly what lets a priority table content-freeze for many sessions). Fold S{PRIOR} closures in; refresh the tiers + actionable queue from the gathered carry-forwards + the open-questions register; bump the register's content-currency marker; re-check to PASS. See `.claude/rules/evoi-prioritization.md`.
2. **Open-questions register** -- for each S{PRIOR} verdict/closure that resolves or advances a listed question, append a freshness update (preserve the verbatim original).
3. **Status register** -- down-tag any assumption/claim whose status S{PRIOR} changed (status cell only; never invert the explanation direction; the prose tag MUST equal the register status).
4. **Open-channel ledger** -- refresh live channels; mark any S{PRIOR}-closed channel.
5. **Routing** -- a value an owner agent is the sole writer of is ROUTED to that agent (emit a dispatch), not direct-edited. A genuinely-unreconciled tension routes to a workshop/carry-forward per `.claude/rules/Investigating-Workshops.md`, NOT a fabricated status edit.

### Step 2 -- CONSUME: use the registers as a planning source

With the registers current, the planning corpus is **WP carry-forwards (Phase 2) UNION register-sourced candidates** -- not WP carry-forwards alone. The blind spot this closes: a live channel can sit in the registers with NO WP carry-forward surfacing it (no session happened to route it), so a WP-only planner never plans it.

1. **Gather register candidates**: the priority queue + tiers; still-open questions; live channels; broken/conditional status entries that have a tractable pre-registrable gate.
2. **Dedupe vs WP carry-forwards (Phase 2)**: a register item already covered by a carry-forward -> merge (record convergence). A register item with NO carry-forward -> a genuine candidate the WPs missed -> add it to the corpus, tagged `register-sourced`.
3. **Order by priority tier** (the priority queue is authoritative for Wave 1). Priority values are **ordinal leverage proxies, not probabilities** -- ordering only.
4. **Fold** the register-sourced candidates into the Phase 2.7 partition (re-bucket by theme/owner). A high-leverage candidate with NO tractable gate is recorded as a **standing gap**, not a wave gate -- leverage is not tractability.

---

## Phase 2.7: Mechanical Wave Partition

**New phase.** Between context file and planner dispatch, the orchestrator assigns items to waves. This is mechanical, not interpretive -- a pure bucketing step. The item set is the Phase-2 carry-forwards PLUS any `register-sourced` candidates from Phase 2.5; bucket both.

### 2.7a. Partition algorithm

1. **Group by natural theme**. Cluster items by subject area. Typical buckets (domain-dependent):
   - Primary live gates (rate-limiters, pre-registrations, key result registrations, headline commitments)
   - Structural results to land (registry entries)
   - Scaling / parameter-sweep atlases
   - Empirical / external-validation forecasts
   - Corridor / bound-characterization studies
   - Secondary-method refinement work
   - Cross-framework / alternative-model comparisons
   - Foundational / first-principles work
   - Internal-consistency / structural audits
   - Methodology closure (rule-file edits, tool implementations)
   - Audit integrity (SHA regens, header repairs, missing write-ups)

2. **Detect semantic duplicates.** Items with slashes in the gate ID (e.g., `<GATE-ID-A> / <GATE-ID-B>`) are dual-ID single gates. Merge.

3. **Assign reviewer-origin as the default wave-owner subagent_type.** If a wave's items all originated from one reviewer's §V, that reviewer's agent type owns the wave:
   - items from `<reviewer>-synthesis` -> `<reviewer>`'s agent type (a single-theme wave -> that theme's specialist)
   - a multi-reviewer item (drawn from several reviewers' syntheses) -> partition across the involved owners
   - Cross-reviewer waves (e.g., the primary-live-gates wave) -> `<domain-generalist>` (breadth owner)

4. **Size target**: 6-15 items per wave. Waves >15 items should be pre-split into sub-waves by owner (e.g., W2a + W2b + W2c if a wave's items span three reviewers' work).

5. **Respect concurrent-dispatch cap**. With <=~8 concurrent agents, 10 waves -> two batches of 5. Sub-wave splits count separately.

### 2.7b. Write the partition manifest

```markdown
# Session {N} -- Wave Partition Manifest

**Total carry-forward items**: {N_items}
**Wave count**: {W}
**Semantic merges applied**: {M}
**Dispatch plan**: Batch 1: {waves}; Batch 2: {waves}; ...

## Wave Assignments

### Wave 1 -- {theme}
**Owner**: {subagent_type}
**Output**: `session-{N}-plan-w1.md`
**Items** ({count}):
- {#1} {gate ID}: {one-line scope}
- {#2} {gate ID}: {one-line scope}
- ...
**Natural split candidates** (if this wave stalls): W1a = items 1-3 under {owner}; W1b = items 4-7 under {owner}.

### Wave 2 -- {theme}
...
```

Write to `PARTITION_FILE`.

### 2.7c. Dry-run late exit

If `--dry-run`, stop here. Report context path + partition path + wave table.

---

## Phase 3: Spawn Per-Wave Planner Swarm

### 3a. Dispatch batches

Launch all wave-planner agents in parallel, respecting the <=~8 concurrent cap. For 10 waves: dispatch W1-W5 in batch 1; when >=3 have completed, dispatch W6-W10. Track via TaskCreate/TaskUpdate.

Each per-wave planner:
- `subagent_type`: per the wave's owner (see §2.7a step 3)
- `run_in_background`: true
- `name`: `planner-w{i}` (or `planner-w{i}{letter}` for sub-waves)
- `mode`: `"acceptEdits"`
- `effort`: `"thorough"`
- `maxTurns`: 20-25

### 3b. Per-Wave Planner Prompt Template

Each planner receives a focused, narrow-scope prompt:

```
You are writing ONE wave of the Session {N} plan for {{PROJECT_NAME}}.

## Your Task

Write **Wave {i} only** to: `sessions/session-plan/session-{N}-plan-w{i}.md`

**Wave {i} theme**: {theme from partition manifest}

## Your assigned items ({count} items)

| # | Gate ID | Scope summary |
|:--|:--------|:-------------|
{items from partition manifest, with scope copy-pasted from context file row}

## READ ONLY this one file

`sessions/session-plan/session-{N}-context.md` -- complete spec, prior-session gate verdicts (collision check), canonical constants, trigger-phrase rules, verdict format.

Do NOT read session-{N-1}-plan.md (too large, watchdog stall risk). Do NOT read individual S{N-1} synthesis files -- the context file is self-sufficient.

## Key scientific anchors

{Cherry-picked facts from reviewer's own synthesis that the agent's memory may not auto-load -- specific numerical values, SHAs, key result/claim statements that need to be available verbatim}

## Per-Gate Block Requirements (13-field spec)

1. Gate ID (no S{N-1} collision)
2. Trigger: [SIGN] / [VERIFY] / [AUDIT] / [VERIFY-RESULT] / [CHAIN]
3. Classification: <domain-class-A> | <domain-class-B> | <domain-class-C> | <domain-class-out-of-scope> | META
4. Agent type (from .claude/agents/) - the breadth `<domain-generalist>` is blacklisted from test-case design; assign a positioned specialist researcher agent
5. Hypothesis (one sentence)
6. Method -- COMPLETE self-contained dispatch prompt: equations + numerical procedure (`from canonical_constants import *`, `torch.linalg` for >=100x100, OMP_NUM_THREADS=8 cap for CPU) + input SHA pins + canonical constants + cross-checks + output files (`s{N}_w{i}_<slug>.py/.npz/.png`)
7. Machinery pin (PRDR): every free parameter pinned. PRU Class 8 = plan rejected.
8. Expected output 4-tuple: (value, scheme, convention, precision/cutoff bound)
9. PASS/FAIL/INFO thresholds with tolerance rule
10. Substitution chain (mandatory for trigger-prefixed gates): definition -> substitution -> simplification -> direction. Python verification.
11. What PASSES/FAILS MEAN for solution space
12. Effort estimate (hours/sessions, GPU vs CPU)
13. Domain-framing reminder in the agent dispatch prompt

## Output file structure

```markdown
# Session {N} Plan -- Wave {i}: {theme}

## Wave {i} Summary
## Wave {i} Decision Point Prerequisites
## §W{i}-{item-number}. {Gate ID}
(full gate block x each assigned item)
## Wave {i} -> Wave {i+1} Decision Point
## Wave {i} Machinery-Enumeration Pin (§0.11)
## Wave {i} Input-SHA Ledger
```

## Script prefix

`s{N}_w{i}_<gate-slug>.py` in `{{COMPUTATION_DIR}}/`.

## What NOT to do

- Do NOT execute computations
- Do NOT write to any file besides `session-{N}-plan-w{i}.md`
- Do NOT re-list items from other waves
- Do NOT read session-{N-1}-plan.md or individual synthesis files
- Do NOT abbreviate gate blocks
- Do NOT collide with S{N-1} gate IDs

## Final deliverable

`session-{N}-plan-w{i}.md` on disk with all {count} full gate blocks + structural sections. Do not terminate until the file exists with non-stub content for every gate.

Write the plan. Write nothing else. Start immediately with the Write tool.
```

### 3c. Stall handling

If a per-wave agent reports `killed` or `stalled` without writing its file:

1. **Do NOT re-dispatch with a leaner spec**. A stall is an infrastructure event, not a signal to degrade the specification. (A stall is a reason to split the wave, never to weaken its spec.)
2. **Split the wave** into sub-waves along natural reviewer or theme boundaries per the partition manifest's "Natural split candidates" line.
3. **Re-dispatch each sub-wave** with the SAME full-fidelity per-gate-block spec but narrower item list and reviewer-specific subagent_type.

Example: a stalled W1 (7 items, <domain-generalist>) -> W1a (3 items under a positioned specialist) + W1b (4 items under <domain-generalist>) -- same full-fidelity spec, narrower item lists.

### 3d. Verify wave files

When all wave planners complete:
1. Verify each `session-{N}-plan-w{i}.md` exists
2. Read line count for each
3. Grep each file for the expected gate IDs (one per assigned item) -- missing gate = re-dispatch that sub-wave only

---

## Phase 4: User Checkpoint

Report:

```
=== WAVE PLANS GENERATED ===

Session: {N}
Partition: {PARTITION_FILE}
Wave files:
  {WAVE_PLAN_FILE 1}    {lines} lines, {item_count} gates
  {WAVE_PLAN_FILE 2}    {lines} lines, {item_count} gates
  ...

Total computations: {count}
Total gates: {count}

Consolidation mode: {consolidate|fanout}

Next: {if consolidate} Stitch wave files into {PLAN_FILE}? | {if fanout} Generate {count} per-wave working papers?
```

AskUserQuestion:
- **Continue** -- proceed to Phase 4.5 (consolidate) or Phase 5b (fanout working papers)
- **Re-spawn a specific wave** -- user names a wave; re-dispatch with feedback
- **Edit wave files manually** -- user edits, re-run `/rclab-plan` afterward
- **Stop here** -- wave plans are sufficient

---

## Phase 4.5: Mechanical Consolidation (consolidate mode only)

Orchestrator stitches wave files into the master plan:

```markdown
# Session {N} -- Compute Plan

## §0. Session Metadata
Session: {N} | Date: {today} | Format: compute | Waves: {W}

## §0.5 Plan Dependencies
(canonical_constants state, upstream SHAs required)

## §0.10 PRU Pre-Registration
(aggregate from per-wave §0.11 machinery pins)

## §I. Theme + Structural Position
(one-paragraph orchestrator-written theme synthesizing the partition manifest)

## §II. Wave-by-Wave Breakdown

### Wave 1
{verbatim content of session-{N}-plan-w1.md body}

### Wave 2
{verbatim content of session-{N}-plan-w2.md body}

...

## §III. Decision Points
(aggregated from per-wave `-> Wave {i+1} Decision Point` sections)

## §IV. Working-Paper Shell Spec
(pointers to which wave produces which working-paper section)

## §V. Constraint-Map Updates Expected
(aggregated from per-wave "what PASSES/FAILS MEAN" blocks)

## §VI. Session Summary
Total wave count: {W} | Total gate count: {count} | Total computations: {count} | Effort estimate: {sum}

## §VII. Master Index
| Wave | Theme | Owner | Gates | File |
|:----:|:------|:------|:-----:|:-----|
```

Consolidation is mechanical -- no new writing, no interpretation. Each wave's content is copy-pasted into §II under its wave heading.

Delete per-wave plan files after successful consolidation, OR keep them as appendices (user choice, default delete for cleanliness).

---

## Phase 5: Spawn Prompter(s)

### Phase 5a: Consolidate mode

Spawn ONE prompter agent writing ONE working paper covering all waves. See `plan-compute.md` template for working-paper structure.

### Phase 5b: Fanout mode

Spawn N prompter agents IN PARALLEL (batched per concurrency cap), one per wave. Each writes `session-{N}/session-{N}-w{i}-workingpaper.md` covering only its wave's gates.

In fanout mode, also write a thin `session-{N}/session-{N}-results-index.md` that lists the per-wave working papers:

```markdown
# Session {N} -- Results Index (fanout)

| Wave | Theme | Working Paper |
|:----:|:------|:-------------|
| 1 | {theme} | session-{N}-w1-workingpaper.md |
| 2 | {theme} | session-{N}-w2-workingpaper.md |
...

Each per-wave working paper is self-contained and consumable by `/rclab-coordinate`.
```

### 5c. Prompter Agent Prompt (both modes)

```
You are generating a results working paper template from an approved session plan.

## Your Task

{Consolidate mode}: Read the plan at `{PLAN_FILE}` and write to `{WORKING_PAPER}`.
{Fanout mode}: Read `session-{N}-plan-w{i}.md` and write to `session-{N}/session-{N}-w{i}-workingpaper.md`.

## Structure

The working paper has:
1. Header: session metadata + instructions for contributing agents (verdict, key numbers, cross-checks, data files, assessment)
2. One section per computation (W{M}-{L} IDs from plan)
3. Each section: Status (NOT STARTED), Gate ID + criteria, "Results" placeholder
4. Synthesis section at end (team-lead fills)
5. Constraint-map updates table
6. Files-produced table

## Section Template (one per W{M}-{L})

```markdown
### W{M}-{L}: {Title} ({agent-type})
**Status**: NOT STARTED
**Gate**: {GATE-ID}. {PASS/FAIL criteria}
**Results**:
*(Agent writes here)*
---
```

## Rules

1. Extract ALL computation IDs, titles, agents, gate criteria from the plan.
2. Group sections by wave.
3. Include agent-instructions block at top.
4. Write ONLY the working paper file.
5. Do NOT modify the plan file.
```

### Wait for prompters

When done:
1. Verify each working-paper file exists
2. Read each; extract line count
3. Verify section coverage (one section per W{M}-{L} in the plan)

If missing sections, report which ones and ask whether to re-spawn.

---

## Phase 6: Report

### Consolidate mode

```
=== COLLAB-PLAN COMPLETE (consolidate) ===

Session: {N}
Generated files:
  {CONTEXT_FILE}        {lines} lines
  {PARTITION_FILE}      {lines} lines
  {PLAN_FILE}           {lines} lines  ({W} waves, {count} gates)
  {WORKING_PAPER}       {lines} lines

Next step:
  /rclab-coordinate {PLAN_FILE}
```

### Fanout mode

```
=== COLLAB-PLAN COMPLETE (fanout) ===

Session: {N}
Generated files:
  {CONTEXT_FILE}            {lines} lines
  {PARTITION_FILE}          {lines} lines
  {PLAN_INDEX}              {lines} lines
  session-{N}-plan-w1.md    {lines} lines
  session-{N}-plan-w2.md    {lines} lines
  ...
  session-{N}-w1-workingpaper.md    {lines} lines
  session-{N}-w2-workingpaper.md    {lines} lines
  ...

Each wave is independently dispatchable:
  /rclab-coordinate session-{N}-plan-w1.md
  /rclab-coordinate session-{N}-plan-w2.md
  ...

OR run the full session via the plan index:
  /rclab-coordinate {PLAN_INDEX}
```

---

## Safety Rules

1. **Never overwrite existing files** without user confirmation (§1c).
2. **Never spawn teams** -- solo agents only.
3. **Never execute computations** -- documents only.
4. **Never modify MEMORY.md, agent memory, rule files, or the knowledge index.** (Phase 2.5 MAINTAIN DOES edit the forward registers -- open-questions / priority / open-channel / status -- as reviewed freshness/status patches, each traceable to S{PRIOR}'s verdict file + handoff with NO invented closures, append-only over verbatim originals; these are *registers*, not rule files, and an owner-routed register is dispatched to its owner, never direct-edited. In investigation mode the Phase-2.5-delta instead registers the new `investigation-{n}` row in `sessions/investigation/index.md` -- a DATA register, append-only -- and SKIPS forward-register maintenance entirely.) Otherwise read-only.
5. **Gate IDs in generated plans must not collide** with existing IDs.
6. **Phase 2 is mechanical only** -- no interpretive content in the context file.
7. **Phase 2.7 partition is mechanical** -- bucketing by theme, not re-scoping items.
8. **No grep fallback** in carry-forward gathering.
9. **Stalls do not justify degrading the spec.** Split the wave further, keep the rigor.
10. **Planners must not read `session-{N-1}-plan.md`.** Too large; watchdog-stall risk. Context file is self-sufficient.
11. **Full-fidelity per-gate blocks are mandatory.** No abbreviation, even in late waves.

---

## Error Handling

| Condition | Action |
|:----------|:-------|
| Empty topic | Auto-generate per §0b -- never stop |
| Agent type not found | List available, stop |
| `--context` file missing | Report which, stop |
| Session ID collision | AskUserQuestion: overwrite / next / cancel |
| Both `--session` and `--investigation` set | Stop with error (mutually exclusive modes) |
| `--investigation` without `--from` | Stop with error -- the seed IS the scope |
| `--from` glob/dir resolves to zero files | Report the glob, stop |
| Investigation collision (`investigation-{n}` plan exists) | AskUserQuestion: overwrite / next / cancel |
| Prior session folder missing | Fall back to latest existing; AskUserQuestion if ambiguous |
| Source wrap-up missing structured section | Report which file, skip; no grep fallback |
| Partition ambiguous (item fits 2+ themes) | Assign to the wave with the stronger reviewer-origin signal; flag in manifest |
| Wave planner stalls (>600s no write) | Split wave into sub-waves per §3c; re-dispatch with same rigor |
| Wave file missing gates | Re-dispatch that sub-wave only with a targeted gate list |
| Consolidation collides (duplicate gate IDs across wave files) | Stop; report collision; ask user to rename gates |
| Prompter stalls | Split prompter similarly (one prompter per 3-5 gates) |
| Working paper missing sections | Report, re-spawn prompter for missing subset |

---

## Relationship to Other Skills

- **`/rclab-coordinate`** -- consumes the plan + working paper(s) this skill produces. Compute-mode dispatcher (and, for an investigation plan, the dispatcher that branches on each gate's `gate_type`).
- **`/rclab-investigate`** -- runs AFTER a compute session closes, on the same session's working paper(s), to produce a workshop-schedule whose entries (executed via `/rclab-review` and `/rclab-workshop`) feed THIS skill the carry-forwards for the next session. In investigation mode, `/rclab-investigate --investigation n` mines an investigation's outputs and seeds the next one.
- **`/rclab-review`** -- workshop and solo agents whose Wrap-Up / §V Carry-Forward sections are the SOLE input to Phase 2.
- **Investigation track** -- `/rclab-plan --investigation` plans an exploratory `investigation-{n}` effort (mixed compute/review/workshop gates) in `sessions/investigation/`, seeded from a free-form input rather than prior-session carry-forwards. Promote an investigation's results into a numbered session to make them permanent. See "Investigation Mode".

Pipeline position: **`/rclab-plan` (S{N+1})** <- `/rclab-review` (S{N} schedule entries) <- `/rclab-investigate` (S{N}) <- `/rclab-coordinate` (S{N}) <- `/rclab-plan` (S{N}).

---

## Why the per-wave swarm (design rationale)

The swarm architecture exists because a single planner stalls on a large carry-forward table: one agent trying to hold ~100+ heterogeneous items in working memory while writing thousands of lines of structured gate blocks hits the stream watchdog (observed: two <domain-generalist> planners stalled at the 600s watchdog with zero writes on a ~100-item table). Per-wave planners holding ~6-15 items each consistently succeed. The pattern that works:

1. **Initial partition**: cluster the carry-forward into waves by theme/sub-domain -- one wave per coherent subject area.
2. **Per-wave ownership**: a wave whose items all came from one reviewer's synthesis is owned by that reviewer's agent type (reviewer-origin); a cross-reviewer wave goes to <domain-generalist> (the breadth owner).
3. **Split dense or stalled waves**: a wave that is too large, or that stalls, is split into sub-waves along natural owner/theme boundaries (W1 -> W1a + W1b), each re-dispatched with the SAME full-fidelity spec but a narrower item list. Owner-specific specialists tend to succeed where a consolidated <domain-generalist> wave stalled.
4. **No spec degradation**: every sub-wave carries the same per-gate-block spec; narrower item list, same rigor.

Takeaway: <domain-generalist> is the breadth owner but struggles on dense, heterogeneous waves; per-domain specialists are the reliable owners for thematically-focused waves, because each is writing about the material its own memory was trained on.
