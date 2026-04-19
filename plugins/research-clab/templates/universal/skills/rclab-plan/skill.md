---
name: rclab-plan
description: Plan the next compute session — mechanical carry-forward gathering, wave partition, then a SWARM of per-wave planners that each design full-fidelity test cases for their slice of the carry-forward. Consolidate (single plan + single working paper) or fan-out (per-wave plan files + per-wave working papers). For workshop-schedule campaigns derived from the just-closed session, use `/rclab-investigate` instead.
argument-hint: <topic> [--session <N>] [--waves <N>] [--consolidate|--fanout] [--planner <agent-type>] [--prompter <agent-type>] [--context <file>...] [--dry-run]
---

# Collab-Plan — Session Plan & Working-Paper Bootstrap (Swarm Architecture)

## --help

If `$ARGUMENTS` contains `--help` or `-h` (or is empty and the user seems confused), read and display `.claude/rclab-help.md`, then stop. Do not proceed with any other phase.

---

Three-phase pipeline:

1. **Mechanical context gathering** — collect every carry-forward computation produced by the prior session's syntheses + workshops, dedupe, write a single context file. **No interpretation.** No reading of MEMORY, prior gate verdicts, knowledge index, or permanent results — those live in the planner agent's auto-loaded memory or via MCP.
2. **Mechanical wave partition** — orchestrator reads the deduplicated carry-forward table, assigns items to waves by theme, merges semantic duplicates, writes a wave-partition manifest. **No interpretation of the items themselves** — just bucketing.
3. **Swarm plan generation** — spawn N per-wave planner agents (one per wave, or more if a wave is dense) IN PARALLEL. Each reads the context file + its assigned carry-forward items and designs the full-fidelity test case for each entry in its wave. Consolidate into one plan file OR keep as per-wave plan files (user choice / default consolidate).
4. **Working paper generation** — mirror consolidation choice. Single working paper (if consolidated) or per-wave working papers (if fanned out).

**Why a swarm and not a single planner**: Opus 4.7 has real complexity constraints. A single planner trying to hold ~100 carry-forward items in working memory while writing 3000+ lines of structured gate blocks hits the stream watchdog (S84 2026-04-18: two <domain-generalist> planners stalled at 600s with zero writes). Per-wave planners holding 6-15 items each consistently succeed. Stalled per-wave agents get split further into sub-waves (W1 → W1a + W1b) — **never** papered over with a leaner spec.

## Precedent for per-sub-session fan-out

This skill extends a pre-existing project pattern. See `sessions/session-plan/archive/`:
- Sessions 17-22: `session-{N}a-prompt.md` + `session-{N}b-prompt.md` + `session-{N}c-prompt.md` + `session-{N}d-prompt.md`
- Session 28: `session-28-prompt-a.md` + `session-28-prompt-b.md` + `session-28-prompt-c.md`
- Session 29: `session-29Aa-prompt.md` through `session-29Ac-prompt.md` + `session-29Ba-prompt.md` + `session-29Bb-prompt.md`
- Session 30A: `session-30Aa/Ab/Ac-prompt.md`

Those were workshop/panel sub-sessions producing one prompt per group. The swarm architecture generalizes to compute format: one plan/prompt/working-paper per wave.

## Usage

```
# Most common — bootstrap next session from carry-forwards, consolidate to single plan
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

# Optional topic label — does NOT scope the plan
/rclab-plan "BCS gap closure"

# Dry-run — gather + dedupe + write context file + partition, do NOT spawn planners
/rclab-plan --dry-run
```

---

## Phase 0: Parse & Validate

### 0a. Arguments

| Arg | Required | Default | Description |
|:----|:---------|:--------|:------------|
| `<topic>` | no | auto-generated | Cosmetic label only. Scope is the carry-forward mined in Phase 2. |
| `--session <N>` | no | auto-detect (latest plan number + 1) | Session number for the new plan |
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

(S83 close, 2026-04-18: "the topic is just a fucking name — we test the entire carry forward.")

### 0c. Validate agent types

Check `--planner` and `--prompter` exist in `.claude/agents/`. See `.claude/templates/agent-roster.md`. If invalid, list available types and stop.

### 0d. Validate context files

If `--context <file>` was provided, verify each file exists (Read 1 line). If any missing, report and stop.

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
- Reviewer origin (which agent's synthesis it came from — drives wave-owner selection in §3a)

### 2e. Write the context file

```markdown
# Session {N} — Context File

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

## Phase 2.7: Mechanical Wave Partition

**New phase (S84 learning).** Between context file and planner dispatch, the orchestrator assigns carry-forward items to waves. This is mechanical, not interpretive — a pure bucketing step.

### 2.7a. Partition algorithm

1. **Group by natural theme**. Cluster items by subject area:
   - Primary live gates (rate-limiters, pre-registrations, theorem registrations, DR3-like commitments)
   - Structural theorems to land (registry entries)
   - Propagation / scaling atlases
   - Observational + detector forecasts
   - Corridor / scaling studies (e.g., K-corridor)
   - Field-theory dressing / counterterm work
   - String-theory / M-theory / matrix-model comparisons
   - Variational / foundational work
   - Causal / geometric audits
   - Methodology closure (rule-file edits, tool implementations)
   - Audit integrity (SHA regens, header repairs, missing write-ups)

2. **Detect semantic duplicates.** Items with slashes in the gate ID (e.g., `S84-VII-M-LANDING / S84-THREE-LAYER-REG-LANDING`) are dual-ID single gates. Merge.

3. **Assign reviewer-origin as the default wave-owner subagent_type.** If a wave's items all originated from one reviewer's §V, that reviewer's agent type owns the wave:
   - `CC-5 propagation` items from lizzi-cc5-synthesis → lizzi-spectral-functional-theorist
   - `K-corridor` items from volovik-synthesis → volovik-superfluid-universe-theorist
   - `Observational` items from mack-synthesis → mack-cosmic-bridge
   - `Three-layer` items from connes/lizzi/vdd triple-solo → partition across those three owners
   - `String/M-theory` items from kaku/kk → split between them
   - `Variational` items from einstein-synthesis → einstein-theorist
   - `Causal/geometric` items from sp-synthesis → schwarzschild-penrose-geometer
   - Cross-reviewer waves (e.g., primary-live-gates) → `<domain-generalist>` (breadth owner)

4. **Size target**: 6-15 items per wave. Waves >15 items should be pre-split into sub-waves by owner (e.g., W2a + W2b + W2c if the three-layer work touches three reviewers).

5. **Respect concurrent-dispatch cap**. With ≤~8 concurrent agents, 10 waves → two batches of 5. Sub-wave splits count separately.

### 2.7b. Write the partition manifest

```markdown
# Session {N} — Wave Partition Manifest

**Total carry-forward items**: {N_items}
**Wave count**: {W}
**Semantic merges applied**: {M}
**Dispatch plan**: Batch 1: {waves}; Batch 2: {waves}; ...

## Wave Assignments

### Wave 1 — {theme}
**Owner**: {subagent_type}
**Output**: `session-{N}-plan-w1.md`
**Items** ({count}):
- {#1} {gate ID}: {one-line scope}
- {#2} {gate ID}: {one-line scope}
- ...
**Natural split candidates** (if this wave stalls): W1a = items 1-3 under {owner}; W1b = items 4-7 under {owner}.

### Wave 2 — {theme}
...
```

Write to `PARTITION_FILE`.

### 2.7c. Dry-run late exit

If `--dry-run`, stop here. Report context path + partition path + wave table.

---

## Phase 3: Spawn Per-Wave Planner Swarm

### 3a. Dispatch batches

Launch all wave-planner agents in parallel, respecting the ≤~8 concurrent cap. For 10 waves: dispatch W1-W5 in batch 1; when ≥3 have completed, dispatch W6-W10. Track via TaskCreate/TaskUpdate.

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

`sessions/session-plan/session-{N}-context.md` — complete spec, S82/S83 gate verdicts (collision check), canonical constants, trigger-phrase rules, verdict format.

Do NOT read session-{N-1}-plan.md (too large, watchdog stall risk). Do NOT read individual S{N-1} synthesis files — the context file is self-sufficient.

## Key scientific anchors

{Cherry-picked facts from reviewer's own synthesis that the agent's memory may not auto-load — specific numerical values, SHAs, theorem statements that need to be available verbatim}

## Per-Gate Block Requirements (13-field spec)

1. Gate ID (no S{N-1} collision)
2. Trigger: [SIGN] / [VERIFY] / [AUDIT] / [VERIFY-THEOREM] / [CHAIN]
3. Classification: <domain-class-A> | <domain-class-B> | <domain-class-C> | <domain-class-out-of-scope> | META
4. Agent type (from .claude/agents/) - GenPhysicicst is blacklisted from test-case design; assign a specialist researcher agent
5. Hypothesis (one sentence)
6. Method — COMPLETE self-contained dispatch prompt: equations + numerical procedure (`from canonical_constants import *`, `torch.linalg` for ≥100×100, OMP_NUM_THREADS=8 cap for CPU) + input SHA pins + canonical constants + cross-checks + output files (`s{N}_w{i}_<slug>.py/.npz/.png`)
7. Machinery pin (PRDR): every free parameter pinned. PRU Class 8 = plan rejected.
8. Expected output 4-tuple: (value, scheme, convention, L_max)
9. PASS/FAIL/INFO thresholds with tolerance rule
10. Substitution chain (mandatory for trigger-prefixed gates): definition → substitution → simplification → direction. Python verification.
11. What PASSES/FAILS MEAN for solution space
12. Effort estimate (hours/sessions, GPU vs CPU)
13. Substrate-framing reminder in the agent dispatch prompt

## Output file structure

```markdown
# Session {N} Plan — Wave {i}: {theme}

## Wave {i} Summary
## Wave {i} Decision Point Prerequisites
## §W{i}-{item-number}. {Gate ID}
(full gate block × each assigned item)
## Wave {i} → Wave {i+1} Decision Point
## Wave {i} Machinery-Enumeration Pin (§0.11)
## Wave {i} Input-SHA Ledger
```

## Script prefix

`s{N}_w{i}_<gate-slug>.py` in `tier0-computation/`.

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

1. **Do NOT re-dispatch with a leaner spec**. A stall is an infrastructure event, not a signal to degrade the specification. (S84 2026-04-18: "stalled agents don't mean do it again, but shittier.")
2. **Split the wave** into sub-waves along natural reviewer or theme boundaries per the partition manifest's "Natural split candidates" line.
3. **Re-dispatch each sub-wave** with the SAME full-fidelity per-gate-block spec but narrower item list and reviewer-specific subagent_type.

Example (S84 W1 stall): W1 (7 items, <domain-generalist>) → W1a (3 items: BASELINE + DYNAMICS + W0, transit-dynamics-theorist) + W1b (4 items: MU-BC + ALPHA-S + DR3 + THEOREM-REG, <domain-generalist>).

### 3d. Verify wave files

When all wave planners complete:
1. Verify each `session-{N}-plan-w{i}.md` exists
2. Read line count for each
3. Grep each file for the expected gate IDs (one per assigned item) — missing gate = re-dispatch that sub-wave only

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
- **Continue** — proceed to Phase 4.5 (consolidate) or Phase 5b (fanout working papers)
- **Re-spawn a specific wave** — user names a wave; re-dispatch with feedback
- **Edit wave files manually** — user edits, re-run `/rclab-plan` afterward
- **Stop here** — wave plans are sufficient

---

## Phase 4.5: Mechanical Consolidation (consolidate mode only)

Orchestrator stitches wave files into the master plan:

```markdown
# Session {N} — Compute Plan

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
(aggregated from per-wave `→ Wave {i+1} Decision Point` sections)

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

Consolidation is mechanical — no new writing, no interpretation. Each wave's content is copy-pasted into §II under its wave heading.

Delete per-wave plan files after successful consolidation, OR keep them as appendices (user choice, default delete for cleanliness).

---

## Phase 5: Spawn Prompter(s)

### Phase 5a: Consolidate mode

Spawn ONE prompter agent writing ONE working paper covering all waves. See `plan-compute.md` template for working-paper structure.

### Phase 5b: Fanout mode

Spawn N prompter agents IN PARALLEL (batched per concurrency cap), one per wave. Each writes `session-{N}/session-{N}-w{i}-workingpaper.md` covering only its wave's gates.

In fanout mode, also write a thin `session-{N}/session-{N}-results-index.md` that lists the per-wave working papers:

```markdown
# Session {N} — Results Index (fanout)

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
2. **Never spawn teams** — solo agents only.
3. **Never execute computations** — documents only.
4. **Never modify MEMORY.md, agent memory, or knowledge index.** Read only.
5. **Gate IDs in generated plans must not collide** with existing IDs.
6. **Phase 2 is mechanical only** — no interpretive content in the context file.
7. **Phase 2.7 partition is mechanical** — bucketing by theme, not re-scoping items.
8. **No grep fallback** in carry-forward gathering.
9. **Stalls do not justify degrading the spec.** Split the wave further, keep the rigor.
10. **Planners must not read `session-{N-1}-plan.md`.** Too large; watchdog-stall risk. Context file is self-sufficient.
11. **Full-fidelity per-gate blocks are mandatory.** No abbreviation, even in late waves (`feedback_full-fidelity-prompts.md`).

---

## Error Handling

| Condition | Action |
|:----------|:-------|
| Empty topic | Auto-generate per §0b — never stop |
| Agent type not found | List available, stop |
| `--context` file missing | Report which, stop |
| Session ID collision | AskUserQuestion: overwrite / next / cancel |
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

- **`/rclab-coordinate`** — consumes the plan + working paper(s) this skill produces. Compute-mode dispatcher.
- **`/rclab-investigate`** — runs AFTER a compute session closes, on the same session's working paper(s), to produce a workshop-schedule whose entries (executed via `/rclab-review`) feed THIS skill the carry-forwards for the next session.
- **`/rclab-review`** — workshop and solo agents whose Wrap-Up / §V Carry-Forward sections are the SOLE input to Phase 2.

Pipeline position: **`/rclab-plan` (S{N+1})** ← `/rclab-review` (S{N} schedule entries) ← `/rclab-investigate` (S{N}) ← `/rclab-coordinate` (S{N}) ← `/rclab-plan` (S{N}).

---

## S84 Implementation Notes (added 2026-04-18 post-refactor)

The swarm architecture was introduced mid-S84 after two single-planner attempts stalled on the 124-item carry-forward table (both at 600s watchdog, both <domain-generalist>). The successful pattern:

1. **Initial partition**: 10 waves by theme (primary-live / three-layer / CC-5 / observational / K-corridor / field-theory / strings / Einstein-SP / μ_BC+methodology / audit-integrity).
2. **Per-wave ownership**: W3 → lizzi, W4 → mack, W5 → volovik (reviewer-origin), W1/W2 → <domain-generalist> (cross-reviewer) — but <domain-generalist> waves both stalled.
3. **W1 and W2 split**: W1 (7 items) → W1a (transit-dynamics, 3 items) + W1b (<domain-generalist>, 4 items); W2 (10 items) → W2a (connes, 4) + W2b (lizzi, 3) + W2c (van-den-dungen, 3). Split-by-reviewer-ownership succeeded where consolidated <domain-generalist> failed.
4. **No spec degradation**: all sub-waves carried the same 13-field spec; narrower item list, same rigor.

Takeaway: <domain-generalist> is breadth-owner but struggles on dense, heterogeneous waves. Reviewer-specific agents consistently succeed because they are writing about the material their own memory was trained on.
