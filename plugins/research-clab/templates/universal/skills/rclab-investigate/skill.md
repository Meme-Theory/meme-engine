---
name: rclab-investigate
description: Generate a workshop-schedule campaign from a just-closed session's working paper(s) -- find structural patterns (convergences, dissonances, uncovered corridors, elimination-without-explanation) and design the parallel solos (/rclab-review) + paired workshops (/rclab-workshop) + closeout. Workshop definitions and the workshop-vs-carry-forward discriminator come from `.claude/rules/Investigating-Workshops.md`; the schedule shape from `.claude/templates/workshop-schedule.md`. Small sources are read by one schedule planner; large multi-wave sources fan out to a per-chunk investigator swarm + one consolidator. Also supports an INVESTIGATION MODE (`--investigation n`) that mines an `investigation-{n}` effort's outputs into a synthesis + a forward seed for the next investigation and housekeeps `sessions/investigation/index.md`.
argument-hint: <topic> [--session <N> | --investigation <n>] [--investigator <agent-type>] [--planner <agent-type>] [--context <file>...] [--dry-run]
---

# Collab-Workshops -- Workshop-Schedule Campaign Generator

## --help

If `$ARGUMENTS` contains `--help` or `-h` (or is empty and the user seems confused), read and display `.claude/rclab-help.md`, then stop. Do not proceed with any other phase.

---

Generate a **workshop-schedule campaign** derived from a completed session's findings. The output is a single schedule file containing a ready-to-dispatch list of `/rclab-review` invocations organized into slots (parallel solos -> sequential workshops -> closeout).

**When to use**: after a session's compute phase closes and you want deep refinement + exploration of the findings BEFORE the next session plans. The workshop-schedule is an artifact of the SOURCE session (it lives in `sessions/session-{SOURCE}/`) and produces the carry-forward computations that the NEXT compute session (S{SOURCE+1}) will consume.

**When NOT to use**: planning a new compute session with pre-registered gates (use `/rclab-plan` instead).

**What's different from `/rclab-plan`**:
- Output is a schedule of `/rclab-review` (Slot 1/3) + `/rclab-workshop` (Slot 2) invocations, NOT a plan of computations.
- No prompter phase -- the schedule entries ARE the dispatch specs.
- Planner default is `<domain-generalist>` (cross-domain pattern detection is the natural fit for campaign design).

## Authorities (this skill delegates)

This skill is a **procedure**. It does not define what a workshop is, and it does not define the schedule's output shape.

| File | Role | Authority over |
|:--|:--|:--|
| `.claude/skills/rclab-investigate/skill.md` (this file) | Procedure | Workflow: detect source, size, investigate, consolidate, report. |
| `.claude/rules/Investigating-Workshops.md` | Policy | Workshop definition, Q1/Q2/Q3 discriminator, honest-count discipline, workshop-vs-carry-forward routing. |
| `.claude/templates/workshop-schedule.md` | Structure | Schedule shape, 3-slot organization, skill-slot invocation mapping. |
| `sessions/investigation/index.md` | Register (DATA) | Investigations index -- HOUSEKEPT here in investigation mode; registered by `/rclab-plan`. |

When something feels missing, check the rule (for "what counts") or the template (for "what the output looks like") before adding to the skill.

## Usage

```
/rclab-investigate                                       # defaults -- mine the latest closed session's working paper; schedule lives in that session's folder
/rclab-investigate "open-questions follow-up"            # cosmetic topic label only
/rclab-investigate --session 84                          # pin the source session
/rclab-investigate --investigator <domain-generalist>   # override the per-chunk investigator (swarm path)
/rclab-investigate --planner <domain-generalist>        # override the schedule planner / consolidator
/rclab-investigate --context sessions/<extra-doc>.md
/rclab-investigate --dry-run                             # show manifest + size decision, stop

# Investigation mode (parallel exploratory track; see "Investigation Mode")
/rclab-investigate --investigation 1                     # mine investigation-1's survey -> synthesis + seed investigation-2 + housekeep the index
/rclab-investigate --investigation 2                     # mine investigation-2's outputs -> seed investigation-3 + housekeep the index
```

---

## Investigation Mode (`--investigation n`)

`/rclab-investigate` has two modes. **Session mode** (default; Phases 0-5 below) mines a closed session's working paper(s) into a workshop-SCHEDULE. **Investigation mode** (`--investigation n`) mines an `investigation-{n}` effort's outputs and does two jobs:

1. **Output analysis** -- synthesize the investigation's outputs into `investigation-{n}/_synthesis.md` + a forward-candidate **seed** that drives the NEXT investigation (the seed is the free-form `--from` input to `/rclab-plan --investigation {n+1}`).
2. **Index housekeeping** -- update `sessions/investigation/index.md` (status / outputs / drives). `/rclab-investigate` is the SOLE housekeeper of that index; `/rclab-plan` only registers new rows.

**Key structural difference.** In the session track this skill emits a workshop-SCHEDULE (a list of `/rclab-review` + `/rclab-workshop` invocations the user dispatches by hand). In the investigation track there is NO separate schedule: follow-ups become typed gates in the next investigation's PLAN -- `/rclab-plan --investigation` assigns each candidate a `gate_type` (workshop / review / compute) and `/rclab-coordinate` juggles them. So the seed this mode writes carries the SAME Q1/Q2/Q3 discriminator outcomes (per `.claude/rules/Investigating-Workshops.md`), but as a `suggested gate_type` per candidate, not as schedule slots. Schedule-then-dispatch in the session track collapses into plan-then-coordinate in the investigation track.

### Sources by investigation shape

- **inv-1 (the root survey)**: the N free-form survey files under `investigation-1/` (each typically: gaps / contradictions / assumptions / refinements / bridges / a "highest-leverage next steps" list). Chunk for the investigator swarm.
- **inv-2+ (a planned effort)**: per-wave WPs + review syntheses + workshop docs + compute verdicts (`{{COMPUTATION_DIR}}/investigation-{n}/inv{n}_gate_verdicts.txt`). Read like session-mode WPs.

### Procedure (reuses the size decision + investigators)

- **Partition** the investigation's output files by size (the same logic as Phase 2a), one investigator per natural unit, batched to the concurrency cap.
- **Investigators** each surface (a) cross-output CONVERGENCES (the same gap/bridge raised by 2+ sources -- the highest-signal items), (b) the strongest individual gaps / contradictions / bridges, (c) per candidate the `Investigating-Workshops.md` Q1/Q2/Q3 outcome as a `suggested gate_type` (Q1a -> workshop, Q1b -> review, concrete-numerical -> compute). Seeds land at `investigation-{n}/workshops/_seed-*.md`.
- **Consolidator** writes TWO files (NOT a schedule):
  - `investigation-{n}/_synthesis.md` -- the cross-output synthesis: convergences, settled-vs-open, the highest-leverage clusters.
  - `investigation-{n}/_next-investigation-seed.md` -- the forward seed: candidate efforts clustered by theme, each a "highest-leverage next step"-shaped item (What / pre-registered Gate / Effort / suggested gate_type / source anchor). This IS the `--from` input to `/rclab-plan --investigation {n+1}`. A rich investigation may seed SEVERAL focused next-investigations -- list them as separate clusters.

`.claude/templates/workshop-schedule.md` and its Slot machinery do NOT apply in investigation mode (there is no schedule). The synthesis + seed are free-form, shaped to feed `/rclab-plan`.

### Index housekeeping (MANDATORY; orchestrator-direct edit)

After the consolidator lands, update the `investigation-{n}` row in `sessions/investigation/index.md` per that file's schema (a reviewed orchestrator-direct edit, never a bulk append):

- **Status** -> `ANALYZING` while mining; `CLOSED` once `_synthesis.md` + the seed are on disk.
- **Outputs** -> the deliverables produced (disk is truth -- list what exists, do not invent).
- **Drives** -> the next investigation(s) the seed proposes. When `/rclab-plan --investigation` later registers a spawned row, its Driver/Seed cell points back here -- reciprocal links.

### Output paths + report

```
SYNTH_FILE   = sessions/investigation/investigation-{n}/_synthesis.md
SEED_FILE    = sessions/investigation/investigation-{n}/_next-investigation-seed.md
INDEX        = sessions/investigation/index.md   (housekeeping; orchestrator-direct)
seeds        = sessions/investigation/investigation-{n}/workshops/_seed-*.md   (intermediate investigator outputs)
```

Report: investigation mined, N investigators / 1 consolidator, the synthesis + seed paths, the clusters the seed proposes (with their suggested gate_type mix), and the index row updated. Next step: `/rclab-plan --investigation {n+1} --from {SEED_FILE}`.

---

## Phase 0: Parse & Validate

### 0a. Extract Arguments

Parse `$ARGUMENTS` for:

| Arg | Required | Default | Description |
|:----|:---------|:--------|:------------|
| `<topic>` | no | `"S{SOURCE_SESSION} workshop campaign"` | Campaign label (first positional arg, may be quoted). **The topic is just a NAME** -- the actual scope is the investigation of the source session's working paper (Phase 2.6). Never gate execution on topic presence. |
| `--session <N>` | no | auto-detect | **Source session number** (integer). Campaign lives IN `sessions/session-{N}/` (same folder as the compute session that produced the working paper). Defaults to latest session with a working paper. Mutually exclusive with `--investigation`. |
| `--investigation <n>` | no | -- (presence = investigation mode) | Switches to INVESTIGATION mode (see "Investigation Mode"): mine `investigation-{n}`'s outputs -> synthesis + next-investigation seed + index housekeeping. Mutually exclusive with `--session`. |
| `--investigator <type>` | no | `<domain-generalist>` | Agent type for per-chunk investigators on the swarm path (large sources / investigation mode). |
| `--planner <type>` | no | `<domain-generalist>` | Agent type for the single schedule planner and for the swarm consolidator. Cross-domain pattern-detection is the canonical choice because campaigns span multiple domains. |
| `--context <file>` | no | none | Extra context files (repeatable -- each `--context` takes one path). Typical addition: a specific working paper not automatically picked up. |
| `--dry-run` | no | false | Show context manifest + output paths + size decision, then stop. |

### 0b. Resolve Topic (do NOT stop on empty)

The topic is a LABEL, not a scope. The real scope of any `/rclab-investigate` run is the deep-investigation of the source session's working paper (Phase 2.6). **Never stop execution for missing topic.**

- If `<topic>` was provided, use it verbatim.
- If `<topic>` is empty or missing, default to `"S{SOURCE_SESSION} workshop campaign"` where SOURCE_SESSION is resolved in Phase 1a.

### 0c. Validate Agent Types

Check that `--planner` and (if passed) `--investigator` exist in `.claude/agents/`. See `.claude/templates/agent-roster.md` for the canonical list. If invalid, list available types and stop.

### 0d. Validate Context Files

If `--context` files are provided, verify each exists (Read tool, 1 line). If any missing, report which files were not found and stop.

### 0e. Mode select

If `--investigation n` is present -> INVESTIGATION mode. Jump to "Investigation Mode"; `--investigation` and `--session` cannot both be set (stop with error if both passed); verify `sessions/investigation/investigation-{n}/` exists -- if not, report and stop. Absent `--investigation` -> SESSION mode (Phases 1-5 below, unchanged).

---

## Phase 1: Session ID Resolution

**IMPORTANT FRAMING**: the workshop-schedule campaign LIVES INSIDE the source session's folder. It does NOT consume a new session number. The schedule for session N is at `sessions/session-{N}/session-{N}-workshop-schedule.md` -- a session-N artifact, not a separate session. The NEXT compute session (via `/rclab-plan`) is numbered `SOURCE_SESSION + 1`, but that is a later skill invocation, not this one.

### 1a. Resolve Source Session Number

The campaign operates ON the source session. If `--session` was provided, that IS the source session. If not:

1. Glob for `sessions/session-*/session-*-results-workingpaper.md`
2. Extract session numbers from filenames, take the LATEST (highest N with a working paper)
3. `SOURCE_SESSION = max(found)` -- the most recently closed compute session

If `SOURCE_SESSION` folder doesn't exist, AskUserQuestion for which source session to mine.

### 1b. Set Output Paths

All outputs land INSIDE the source session's folder:

```
SCHEDULE_FILE = sessions/session-{SOURCE_SESSION}/session-{SOURCE_SESSION}-workshop-schedule.md
SESSION_FOLDER = sessions/session-{SOURCE_SESSION}/
WORKSHOPS_SUBDIR = sessions/session-{SOURCE_SESSION}/workshops/
```

Create `WORKSHOPS_SUBDIR` if missing. `SESSION_FOLDER` MUST already exist (it contains the source working paper).

### 1c. Check for Collisions

If `SCHEDULE_FILE` exists: AskUserQuestion: "Workshop schedule already exists at {path}. Overwrite / Cancel?"

### 1d. Derive the Next-Compute-Session Reference (for context strings)

The planner's invocation-context strings reference "next compute session" as `S{SOURCE_SESSION + 1}`. For example, the context strings read "feeds into S{SOURCE_SESSION+1} planning" and "pre-register a gate S{SOURCE_SESSION+1}-{name}". This is what goes in the context strings -- NOT a session folder or output path.

Set `NEXT_COMPUTE = SOURCE_SESSION + 1` and pass it to the planner so it can reference the correct future session in gate names and deliverable summaries.

---

## Phase 2: Verify Source Documents Exist

The skill does NOT read + aggregate context into a pre-digest file. That's the planner's job -- the planner reads the raw working paper directly to find structural patterns (any pre-digest would be a lossy compression of exactly the material the planner needs unfiltered).

The skill's job is to VERIFY the source documents exist + PASS their paths to the planner. Build a manifest of expected sources:

| Source | Path | Required? |
|:-------|:-----|:---------:|
| Source working paper | `sessions/session-{SOURCE_SESSION}/session-{SOURCE_SESSION}-results-workingpaper.md` | YES |
| Source gate verdicts | `{{COMPUTATION_DIR}}/session-{SOURCE_SESSION}/s{SOURCE_SESSION}_gate_verdicts.txt` | YES |
| Source plan | `sessions/session-plan/session-{SOURCE_SESSION}-plan.md` | YES |
| Prior syntheses (if any) | glob `sessions/session-{SOURCE_SESSION}/session-*-{synthesis,synth,workshop,collab}.md` | optional |
| Permanent results registry | `sessions/permanent-results-registry.md` | optional |
| Framework MEMORY | (auto-loaded into agent context) | optional |
| Investigator/planner agent memory | `.claude/agent-memory/{agent-type}/MEMORY.md` | optional (auto-loaded) |
| Extra `--context` files | from flag | optional |

If any REQUIRED source is missing, report + stop. Otherwise, run the size decision (2a), then proceed to Phase 2.6 -- no intermediate context file.

### 2a. Size Decision (single planner vs investigator swarm)

The source working paper(s) drive how Phase 3 runs. Measure aggregate size:

- **Single-planner path (default)** -- the source is one wave OR small enough for one agent to deep-read (roughly <= 3K aggregate lines). ONE schedule planner reads the working paper directly and writes the schedule (Phase 3). This is the common case.
- **Swarm path** -- the source is multi-wave and large (roughly > 3K aggregate lines, or several per-wave WP files exist). A single planner trying to deep-read a very large working paper hits the stream watchdog (the same failure mode as `/rclab-plan`). Fan out to N per-chunk investigators -- one per wave (per-wave WP shape) or one per ~2K lines (unified WP shape), batched to the concurrency cap -- then ONE consolidator (Phase 3S).

Record the chosen path + chunk plan for the dry-run report and Phase 3.

### 2b. Dry-Run Checkpoint

If `--dry-run`: display the source manifest + output paths + size decision, then STOP.

```
=== COLLAB-WORKSHOPS DRY RUN ===
Topic: "{topic}"
Source session: {SOURCE_SESSION} (campaign lives IN this folder)
Next compute: S{NEXT_COMPUTE} (referenced in context strings but NOT created)
Schedule file: {SCHEDULE_FILE}
Path: {single-planner | swarm (N investigators + 1 consolidator)}
Planner: {planner-type}   Investigator: {investigator-type, swarm path only}

Sources verified:
  sessions/session-{SOURCE_SESSION}/session-{SOURCE_SESSION}-results-workingpaper.md  [size]
  {{COMPUTATION_DIR}}/session-{SOURCE_SESSION}/s{SOURCE_SESSION}_gate_verdicts.txt     [size]
  sessions/session-plan/session-{SOURCE_SESSION}-plan.md                               [size]
  ... (optional sources marked present or missing)

Run without --dry-run to proceed.
```

---

## Phase 2.6: Seed-Extraction Guidance (for the planner/investigators, not the Skill)

The skill does not extract seeds. The planner (single-planner path) or the per-chunk investigators (swarm path) do that in-process while reading the working paper. What the skill provides is the PATTERN CATALOG below. It goes into the agent prompt (Phase 3 / Phase 3S), not into a file.

**Authority**: `.claude/rules/Investigating-Workshops.md` is the authoritative source for what COUNTS as a workshop -- the four-condition definition, the "is NOT a workshop" list, the Q1/Q2/Q3 discriminator (Q1a -> workshop, Q1b -> solo review, Q2/Q3 -> carry-forward), and the honest-count discipline ("no workshops" is a valid output; a typical session yields 0-4). The patterns below help an agent FIND candidates; the rule decides how each candidate is CLASSIFIED and ROUTED. Read the rule first.

### Seed-Extraction Patterns (what to look for in the working paper)

Read the source working paper gate-by-gate. For each pattern below, scan for instances. Each instance is a candidate -- then classify it with the rule's discriminator.

**Pattern 1 -- Convergence** (candidate: solo to produce the canonical statement)
Two or more gates establish the SAME result via DIFFERENT methods. Each is independently correct but scattered across sections; the canonical statement has not been written. Example: two waves prove one identity by different routes -> one synthesis stating it once.

**Pattern 2 -- Dissonance** (candidate: 2-agent 3-round workshop, adjudication)
Two tracks compute the same quantity and get materially different answers; both pass their own internal gates. Example: a large gap between two independent estimates of one observable -> a workshop to adjudicate which is right.

**Pattern 3 -- Corridor without characterization** (candidate: 2-agent solo to map the corridor)
Bounds are established (floor + ceiling) but the behavior INSIDE the bounds is not written -- what is permitted vs forbidden, what governs outcomes across the range. Example: a proven feasible band whose interior was never characterized -> a synthesis mapping it.

**Pattern 4 -- Elimination-without-explanation** (candidate: 2-agent solo, constraint-map synthesis)
A FAIL closed a hypothesis but the section does not spell out (a) which hypothesis is now false, (b) what surviving mechanisms must carry the load, (c) the solution-space dimensionality reduction. Example: several FAILs that together narrow the space -> one synthesis stating what survives.

**Pattern 5 -- Recurring pattern across multiple gates** (candidate: 2-agent 2-round workshop, taxonomy)
The same structural behavior shows up in 3+ gates and needs a universal classification into a unifying principle or taxonomy. Example: one effect recurring in three unrelated gates -> a taxonomy that names it.

**Pattern 6 -- Dual-channel ambiguity** (candidate: 2-agent 3-round workshop, consistency audit)
Two channels are CLAIMED independent but never PROVEN independent -- they might be double-counted. Example: a "safe band" asserted from two estimates whose independence was never derived -> a self-consistency workshop.

**Pattern 7 -- Scattered falsifiers** (candidate: 2-agent solo, inventory + roadmap)
Multiple falsifiable predictions are registered in different gates but not consolidated into a coherent campaign with a timeline and a priority ordering. Example: several sign-definite predictions across waves -> one inventory + roadmap.

**Pattern 8 -- Methodology debts** (candidate: 2-agent 2-round workshop, rule-file diff)
Failure modes that recurred in the session (e.g. verdicts emitted without artifacts; under-specified pre-registrations) need an audit proposing a rule-file diff. Example: a recurring process failure -> a methodology audit + proposed rule extension.

**Pattern 9 -- Deferred synthesis** (candidate: multi-perspective closeout)
The working paper explicitly DEFERS a synthesis. Always lands as a Slot 3 closeout depending on earlier slots. Example: a deferred combined-landscape view -> the closeout entry.

### Extraction Procedure

1. Read the source working paper in passes. First pass: skim all §W{W}-G{G} headers + verdict lines for overall shape. Subsequent passes: read full Results blocks when a pattern match is suspected.
2. For each pattern instance, record:
   - **Seed title** (one-line, domain-specific)
   - **Source gates** (which sections provide the evidence)
   - **Pattern type** (from the catalog above)
   - **Why it matters** (2-3 sentences -- what structural hole the workshop/synthesis would fill)
   - **Candidate agents** (from agent-roster.md; pair for complementary tracks)
   - **Candidate classification** (per the rule's Q1/Q2/Q3): Slot 1 solo / Slot 2 workshop / Slot 3 closeout / carry-forward

3. Deduplicate and coalesce: if two seeds cover the same structural territory, merge them or split the scope explicitly.

4. Don't force every pattern to produce a seed -- apply the rule's honest-count discipline ("no workshops" is valid; a typical session yields a handful of solos and 0-4 workshops). Target a realistic count for the session's actual substance, not a quota.

### Seed routing (for the planner / consolidator)

Apply the rule's routing to every seed. No intermediate file in the single-planner path.

- **Q1 seeds (workshop / solo review)** appear in the SCHEDULE as Slot 1 / Slot 2 / Slot 3 entries.
- **Q2 / Q3 seeds (carry-forwards)** do NOT go in the schedule -- they route to the investigated wave's working-paper `## Carry-Forward Computations` section as 4-field blocks (what / inputs / gate / effort), because `/rclab-plan` reads the working paper, not the schedule. (Single-planner path: ensure the WP CF carries them and note them in the schedule's "Planning Input Checklist"; swarm path: the consolidator lifts them -- see Phase 3S.)
- **Nothing gets "DEFERRED" with no home** -- every seed lands either as a schedule entry or as a WP carry-forward.
- **Workshop OUTCOMES feed the next plan** as workshop verdicts; compute carry-forwards feed it via the WP CF. Each workshop invocation context demands the 4-field carry-forward mandate (what / inputs / gate / effort).

---

## Phase 3: Spawn Schedule Planner (single-planner path)

Use this path when Phase 2a chose single-planner. For the swarm path, skip to Phase 3S.

Create a task for tracking:

```
TaskCreate: subject="Generate S{SOURCE_SESSION} workshop schedule: {topic}"
```

Spawn a **solo background agent** using the Agent tool:

- `subagent_type`: from `--planner` flag (default: `<domain-generalist>`)
- `run_in_background`: true
- `name`: `workshop-planner`
- `mode`: `"acceptEdits"` -- planner writes the schedule file only
- `effort`: `"thorough"` -- schedule design spans multiple domains

### Planner Agent Prompt

```
You are generating a **workshop-schedule campaign** for the {{PROJECT_NAME}} project.

## Your Task

Write a campaign schedule to: `{SCHEDULE_FILE}`

**Topic (label)**: {topic}
**Source session**: {SOURCE_SESSION} (campaign lives IN this folder; next compute session will be S{NEXT_COMPUTE})
**Date**: {today}

## Read first (mandatory)

- `.claude/rules/Investigating-Workshops.md` -- the authority for what COUNTS as a workshop (four-condition definition, "is NOT a workshop" list, Q1/Q2/Q3 discriminator, honest-count discipline). Read it before producing any candidate.
- `.claude/templates/workshop-schedule.md` -- the schedule's output shape, the 3-slot organization, and the skill-slot invocation mapping. Follow it exactly.

## What a Workshop Schedule IS

It is a ready-to-dispatch list of invocations organized into slots:
- Slot 1: parallel independent solos via `/rclab-review` (no cross-deps)
- Slot 2: workshops via `/rclab-workshop` (sequential within each; parallel across when non-overlapping)
- Slot 3: closeout via `/rclab-review` (depends on Slot 1/2 outputs)

The deliverable IS the schedule. Slot 1 + Slot 3 entries are fully-specified `/rclab-review` invocations; Slot 2 entries are `/rclab-workshop` invocations. NEVER emit `/rclab-review --type workshop` -- that flag combination is invalid (the load-bearing skill-slot invariant). Each entry must be copy-paste-ready.

## Source Documents (read these directly)

| Source | Path | Role |
|:-------|:-----|:-----|
| Source working paper | `sessions/session-{SOURCE_SESSION}/session-{SOURCE_SESSION}-results-workingpaper.md` | **PRIMARY** -- all wave/gate Results blocks. Large file. Chunk reads at ~30KB to avoid silent Read-tool truncation. Seeds come from here. |
| Source gate verdicts | `{{COMPUTATION_DIR}}/session-{SOURCE_SESSION}/s{SOURCE_SESSION}_gate_verdicts.txt` | Permanent verdict ledger (latest non-superseded line wins per gate ID). |
| Source plan | `sessions/session-plan/session-{SOURCE_SESSION}-plan.md` | Original pre-registrations. Cross-reference what was supposed to happen vs what did. |
| Permanent results registry | `sessions/permanent-results-registry.md` | Results landed at/before S{SOURCE_SESSION}. |
| Optional prior syntheses | glob `sessions/session-{SOURCE_SESSION}/session-*-{synthesis,synth,workshop,collab}.md` | Usually empty for a just-closed session -- this campaign is what produces them. |

**What you're looking for**: STRUCTURAL PATTERNS in the working paper -- not a pre-existing carry-forward list. Carry-forwards will be OUTPUTS of the workshops you schedule, plus the Q2/Q3 items you route to the WP per the rule. See the Seed-Extraction Patterns section below.

## Seed-Extraction Patterns (scan the working paper for these)

**Pattern 1 -- Convergence** (candidate: solo to produce the canonical statement)
Two or more gates establish the SAME result via DIFFERENT methods. The canonical statement is not yet written.

**Pattern 2 -- Dissonance** (candidate: 2-agent 3-round workshop, adjudication)
Two tracks compute the same quantity and get materially different answers; both pass their own internal gates.

**Pattern 3 -- Corridor without characterization** (candidate: 2-agent solo to map the corridor)
Bounds established (floor + ceiling) but the behavior inside the bounds is not written.

**Pattern 4 -- Elimination-without-explanation** (candidate: 2-agent solo, constraint-map synthesis)
A FAIL closed a hypothesis but the section does not spell out (a) which hypothesis is now false, (b) surviving mechanisms, (c) solution-space dimensionality reduction.

**Pattern 5 -- Recurring pattern across multiple gates** (candidate: 2-agent 2-round workshop, taxonomy)
The same structural behavior shows up in 3+ gates -- needs a universal classification.

**Pattern 6 -- Dual-channel ambiguity** (candidate: 2-agent 3-round workshop, consistency audit)
Two channels CLAIMED independent but never PROVEN independent -- might be double-counted.

**Pattern 7 -- Scattered falsifiers** (candidate: 2-agent solo, inventory + roadmap)
Multiple falsifiable predictions registered in different gates but not consolidated into a coherent campaign with a timeline and a priority ordering.

**Pattern 8 -- Methodology debts** (candidate: 2-agent 2-round workshop, rule-file diff)
Failure modes that recurred in the session -- need an audit proposing a rule-file diff.

**Pattern 9 -- Deferred synthesis** (candidate: multi-perspective closeout)
The working paper explicitly DEFERS a synthesis. Always lands as a Slot 3 closeout.

**Extraction procedure**:
1. Skim pass: all wave/gate headers + verdict lines for overall shape.
2. Targeted read pass: full Results blocks when a pattern match is suspected. Chunk at ~30KB.
3. Record per seed: title, source gates, pattern type, why it matters, candidate agents, candidate classification (per the rule's Q1/Q2/Q3).
4. Deduplicate and coalesce overlapping seeds.
5. Apply the rule's honest-count discipline -- target a realistic count for the actual substance, not a quota; "no workshops" is valid.

## Template

Read `.claude/templates/workshop-schedule.md` and follow it EXACTLY. See the "Planner's instructions" section at the bottom of the template for generation rules.

## Rules

1. **Mine the source material**: explicit deferrals, unresolved adjudications, claimed-but-unformalized results, recurring failure modes, watchlists. These are campaign seeds.

2. **Classify each seed** per the rule's Q1/Q2/Q3 (Q1a workshop / Q1b solo / Q2-Q3 carry-forward). NOT every seed is a schedule entry.

3. **Organize schedule entries into slots** by dependency (Slot 1 independent solos, Slot 2 workshops, Slot 3 closeout).

4. **Write exact invocations** -- not narrative descriptions. Slot 1 + Slot 3 -> `/rclab-review`; Slot 2 -> `/rclab-workshop`. NEVER `/rclab-review --type workshop`. Each must be copy-paste-ready with all flags, agent lists, session pins, and full context strings.

5. **Context strings must be full-fidelity**: every specific gate ID, numeric anchor, classification seed, adjudication rule the synthesis needs. NO "see source docs" or "appropriate context" -- be explicit.

6. **Agent selection**: use `.claude/templates/agent-roster.md` canonical short names. For Slot 1 solos, pick the agent whose domain owns the question. For Slot 2 workshops, pair agents covering complementary, genuinely-competing readings of the same claim -- two specialists who would derive the result by different methods and might disagree.

7. **Rounds (Slot 2 only)**: default 2 rounds; use 3 only for genuine dissonance (R1 steelman, R2 respond, R3 converge); use 1 only for informational exchanges (rare).

8. **No length targets** in invocation contexts. Content requirements only ("include X table", "include Y gate").

9. **Carry-forward routing**: Q2/Q3 carry-forwards do NOT go in the schedule -- lift them to the investigated wave's WP `## Carry-Forward Computations` section as 4-field blocks (what / inputs / gate / effort), since `/rclab-plan` reads the WP, not the schedule. Every workshop invocation context demands the same 4-field mandate for the compute items it surfaces.

10. **Deliverable table**: explicitly list every file the campaign will produce, with the agent responsible and the next-session consumption pattern.

11. **Planning Input Checklist**: list what the NEXT session's planner should expect from the campaign (adjudication results, new gate IDs, registry drafts, watchlists / open-question updates, combined-landscape docs, methodology diffs).

12. **Concurrency cap**: respect the project's max concurrent Agent dispatches. If Slot 1 exceeds the cap, split into Slot 1a / Slot 1b sub-slots.

13. **Graceful degrade**: Slot 3 items must reference Slot 2 outputs "if landed" so agents degrade gracefully if dependencies have not completed.

14. **Do NOT execute syntheses** -- only schedule them.
15. **Do NOT modify MEMORY.md, agent memory, rule/template files, or the knowledge index** (the WP CF appends in rule 9 are the only allowed writes besides the schedule).
16. **Write the schedule file** (plus any WP CF appends per rule 9). Nothing else.
```

### Wait for Planner

Wait for the planner agent to complete. Then:

1. Verify `{SCHEDULE_FILE}` exists.
2. Read it, extract line count.
3. Extract slot counts (Slot 1 entries, Slot 2 workshops, Slot 3 closeout items).

If the file doesn't exist or is empty, report failure and suggest trying a different planner type.

---

## Phase 3S: Investigator Swarm + Consolidator (large-source path)

Use this path when Phase 2a chose swarm (large multi-wave source). It mirrors `/rclab-plan`'s swarm: N per-chunk investigators each write a seed; one consolidator merges the seeds into the schedule. Track via TaskCreate/TaskUpdate.

### Output paths

```
SEED_FILE({stem})  = sessions/session-{SOURCE_SESSION}/workshops/_seed-{stem}.md   (intermediate; underscore-prefixed)
SCHEDULE_FILE      = sessions/session-{SOURCE_SESSION}/session-{SOURCE_SESSION}-workshop-schedule.md
```

`{stem}` = wave id (`w0a`, `w12`) for per-wave shape; `unified-{i}` for unified shape.

### 3S-a. Spawn investigators (batched to the concurrency cap)

One investigator per chunk (`--investigator` type, default `<domain-generalist>`), `run_in_background`, `mode="acceptEdits"`, `name="inv-{stem}"`. Wait for each batch before launching the next.

Investigator prompt (short -- it points at the rule + the Phase 2.6 catalog, it does not re-encode them):

```
You are investigating Session {SOURCE_SESSION} for the workshop-schedule campaign.

## Read first (mandatory before producing any candidate)
- `.claude/rules/Investigating-Workshops.md` -- the four-condition workshop definition, the "is NOT a workshop" list, the Q1/Q2/Q3 discriminator, the honest-count discipline ("no candidates" is valid).

## Your chunk
{Per-wave shape: the WP file(s) to read in full + the plan file(s) they reference.}
{Unified shape: (file, start_line, end_line) -- read with offset/limit <= 200 lines per call to avoid silent ~30KB Read-tool truncation.}

## Procedure
1. Read the rule in full FIRST.
2. Read your assigned chunk + its referenced plan file(s). Grep `{{COMPUTATION_DIR}}/session-{SOURCE_SESSION}/s{SOURCE_SESSION}_gate_verdicts.txt` for gate IDs in your range.
3. SHELL check: if a wave has all gates not-started, no result artifacts, and no verdict entries, emit `## Not investigated -- wave {id} is pre-compute shell` and skip it (rule "is NOT" item 9). Do NOT create a wave-execution carry-forward.
4. Scan for the Seed-Extraction Patterns (the catalog in this skill's Phase 2.6). Surface (do not resolve) any candidate depending on / conflicting with another wave under `## Cross-wave flags`, citing both -- the consolidator adjudicates cross-wave tensions.
5. Apply the rule's Q1/Q2/Q3 to EVERY candidate; first YES wins. Q1a -> Slot 2 workshop; Q1b -> Slot 1 solo; Q2/Q3 -> carry-forward (NOT the schedule).

## Write your seed
Output: `sessions/session-{SOURCE_SESSION}/workshops/_seed-{stem}.md`. Use the rule-aligned headings: `## Workshops` (Q1a), `## Solo reviews` (Q1b), `## Cross-wave flags`, `## Carry-forwards (route to /rclab-plan, NOT this schedule)`, and `## No candidates` (with a one-paragraph reason) if the chunk yields none. Modify only your seed file; do not read other chunks.
```

Verify each seed exists with >=1 candidate or a `## No candidates` paragraph; re-dispatch a stub seed once, then pause for user direction if it still fails.

### 3S-b. Spawn the consolidator

One consolidator (`--planner` type), `run_in_background`, `mode="acceptEdits"`, `name="consolidator"`.

Consolidator prompt (short -- points at the template + the rule):

```
You are consolidating per-chunk seeds into the unified workshop schedule for Session {SOURCE_SESSION}.

## Read first
1. `.claude/templates/workshop-schedule.md` -- the schedule's structure, 3-slot organization, and skill-slot invocation mapping (Slot 1/3 -> /rclab-review; Slot 2 -> /rclab-workshop). Follow it exactly.
2. `.claude/rules/Investigating-Workshops.md` -- re-apply the Q1/Q2/Q3 discriminator to every candidate; trust your discriminator over a seed's tag when they conflict (investigators sometimes mis-classify).
3. All seeds at `sessions/session-{SOURCE_SESSION}/workshops/_seed-*.md` -- read every one in full.

## Procedure
1. Aggregate every candidate, retaining source-seed attribution. A `## Cross-wave flags` entry naming a genuine cross-wave CONTRADICTION is itself a workshop candidate -- run it through the discriminator.
2. Re-apply Q1/Q2/Q3; re-tag where an investigator was wrong.
3. Partition: Q1 -> schedule (Slot 1 / 2 / 3); Q2/Q3 -> carry-forward; `## Not investigated` shells -> drop any wave-execution CF (verify SHELL state first).
4. Deduplicate + coalesce overlapping Slot 1 / Slot 2 entries; the merged entry cites all source seeds.
5. Lift every Q2/Q3 item to the investigated wave's WP `## Carry-Forward Computations` as a 4-field block. These do NOT appear in the schedule (`/rclab-plan` reads the WP, not the schedule).
6. Write the schedule strictly per the template -- Slot 1/3 entries `/rclab-review`, Slot 2 entries `/rclab-workshop` (NEVER `/rclab-review --type workshop`), full-fidelity context strings, the Deliverable Table, and the Planning Input Checklist.

Do not modify seed files. Append-only on WP CF blocks.
```

### Phase 3S close

Verify: `SCHEDULE_FILE` exists with Slot 1/2/3 sections + Deliverable Table + Planning Input Checklist; every Slot 1/3 invocation is `/rclab-review`; every Slot 2 invocation is `/rclab-workshop` with exactly two agents and an explicit `--rounds`; no `/rclab-review --type workshop` anywhere; and for each `## Not investigated` shell declaration no wave-execution CF was appended. Then proceed to Phase 4.

---

## Phase 4: User Checkpoint

Report to the user:

```
=== WORKSHOP SCHEDULE GENERATED ===

File: {SCHEDULE_FILE}
Lines: {count}
Topic: "{topic}"
Source session: {SOURCE_SESSION} (campaign lives IN this folder; next compute = S{NEXT_COMPUTE})
Path: {single-planner | swarm}
Planner: {planner-type}

Slot 1 (parallel solos via /rclab-review): {count} entries
Slot 2 (workshops via /rclab-workshop): {count} entries
Slot 3 (closeout via /rclab-review): {count} entries
Total campaign entries: {total}

Next: Dispatch Slot 1?
```

Use AskUserQuestion with options:
- **Dispatch Slot 1 now** -- you (the orchestrator) invoke each Slot 1 `/rclab-review` entry.
- **Edit schedule first** -- user will edit manually, then dispatch later.
- **Stop here** -- schedule is sufficient; user handles dispatch.

If user provides feedback text (via "Other"), re-spawn the planner/consolidator with the original prompt PLUS the feedback appended under `## User Feedback`. Return to the checkpoint.

---

## Phase 5: Report

```
=== COLLAB-WORKSHOPS COMPLETE ===

Topic: "{topic}"
Source session: {SOURCE_SESSION} (campaign lives IN this folder; next compute = S{NEXT_COMPUTE})
Path: {single-planner | swarm (N investigators + 1 consolidator)}

Generated File:
  {SCHEDULE_FILE}                                      {lines} lines
  {swarm path also: workshops/_seed-*.md intermediates + WP CF appends}

Planner: {planner-type}
Slots: 3 (Slot 1 parallel solos via /rclab-review, Slot 2 workshops via /rclab-workshop, Slot 3 closeout via /rclab-review)
Total campaign entries: {count} ({N_solo} solo syntheses + {N_workshop} workshops + {N_closeout} closeout)
Context sources: {count} files ({total_lines} lines)

Next step:
  Dispatch Slot 1 entries in parallel (copy each /rclab-review invocation from the schedule).
  Wait for all Slot 1 to land, then dispatch Slot 2 (each /rclab-workshop).
  Finally dispatch Slot 3 closeout items (/rclab-review).
  Each invocation is already fully specified -- no further editing needed.
```

---

## Safety Rules

1. **Never overwrite existing files** without user confirmation (Phase 1c collision check).
2. **Never spawn teams** -- solo / independent agents only. No TeamCreate, no SendMessage.
3. **Never execute the syntheses the schedule describes** -- schedule-only deliverable. Dispatch is a separate step.
4. **Never modify MEMORY.md, agent memory, rule/template files, or the knowledge index.** The allowed writes are: the schedule file; the per-chunk seed files + the WP `## Carry-Forward Computations` appends (swarm path); and, in INVESTIGATION mode, `investigation-{n}/_synthesis.md` + `_next-investigation-seed.md` plus a reviewed orchestrator-direct row update in `sessions/investigation/index.md` (a DATA register -- append-only on rows, never a bulk dump). Otherwise read-only.
5. **Concurrency cap**: respect the project's max concurrent Agent dispatches (investigator swarm, and later Slot 1 dispatch). If Slot 1 has more solos than the cap, the schedule MUST split into 1a/1b sub-slots.
6. **Routing is mandatory, not "every seed is an entry"** -- per `.claude/rules/Investigating-Workshops.md`, Q1 seeds become schedule entries and Q2/Q3 seeds become WP carry-forwards. Every seed lands somewhere; nothing is silently deferred.

## Error Handling

| Condition | Action |
|:----------|:-------|
| Empty topic | Auto-generate per Phase 0b (no stop). Topic is a label; the working paper is the scope. |
| Agent type not found | List available types from `.claude/agents/` and stop. |
| Context file missing | Report which file(s) not found and stop. |
| Schedule file collision | AskUserQuestion: overwrite / cancel. |
| Source session folder missing | AskUserQuestion: which session to mine (suggest latest-with-working-paper, or earlier user-specified). |
| Schedule file empty after planner/consolidator | Report failure, suggest a different planner type. |
| Investigator returns empty or stalls | One retry on that chunk; if still empty, pause for user direction. |
| Seed file stub-shaped | Same as stall -- one retry, then pause. |
| Consolidator stalls | Report; suggest a different `--planner` type or manual consolidation from seeds. |
| Context very large (>10000 lines) | Take the swarm path (Phase 2a); report total size, proceed unless the user stops. |
| Both `--session` and `--investigation` set | Stop with error (mutually exclusive modes). |
| `--investigation n` but `investigation-{n}/` missing | Report, stop. |
| Investigation has no outputs yet | Report what is on disk; proceed on what exists if a survey is mid-flight (note the partial count); if empty, stop. |
| `_synthesis.md` / seed collision (investigation mode) | AskUserQuestion: overwrite / cancel. |

---

## Relationship to Other Skills

- **`/rclab-plan`** -- for planning a NEW compute session with pre-registered gates. Use AFTER a campaign closes to plan S{N+1}. In INVESTIGATION mode, `/rclab-plan --investigation` consumes the seed THIS skill produces.
- **`/rclab-review`** and **`/rclab-workshop`** -- the TARGET skills each schedule entry invokes (Slot 1/3 -> `/rclab-review`; Slot 2 -> `/rclab-workshop`). This skill GENERATES the invocations; it does not invoke them.
- **`/rclab-coordinate`** -- in SESSION mode, unrelated. In INVESTIGATION mode it dispatches the next investigation's mixed-type plan (seed -> `/rclab-plan --investigation` -> `/rclab-coordinate`).

The full pipeline: compute session S{N} (via `/rclab-plan` then `/rclab-coordinate`) -> **workshop campaign IN S{N}'s folder (via `/rclab-investigate`)** -> next compute session S{N+1} (via `/rclab-plan`). The workshop campaign does NOT consume a session number; it is a post-compute phase of the source session. The investigation track is the parallel exploratory pipeline: `/rclab-plan --investigation` -> `/rclab-coordinate` -> `/rclab-investigate --investigation` -> (seed) -> repeat, with results promoted into a numbered session to become permanent.

---

## Notes

- Default planner/investigator is `<domain-generalist>` because cross-domain pattern detection is the natural fit for campaign design (campaigns span multiple domains). Override `--investigator` for single-domain source material; override `--planner` for a different consolidator/planner style.
- Seeds are intermediate (swarm path), not deliverables -- the `_seed-*.md` underscore prefix marks that. They live in `sessions/session-{SOURCE_SESSION}/workshops/` alongside the actual workshop output files (no underscore) that downstream `/rclab-workshop` dispatches create.
- The workshops subdirectory `sessions/session-{SOURCE_SESSION}/workshops/` is created on first Write. Solo outputs land in `sessions/session-{SOURCE_SESSION}/session-{SOURCE_SESSION}-{short-name}-synthesis.md` per `/rclab-review` defaults.
- Auto-detection default takes the LATEST session with a working paper as SOURCE_SESSION. Override with `--session <N>` to run a campaign on an earlier session.
