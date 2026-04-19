---
name: rclab-investigate
description: Generate a workshop-schedule campaign by DEEP-INVESTIGATING the prior session's raw results working paper — finds structural patterns (convergences, dissonances, uncovered corridors, elimination-without-explanation, etc.) and designs the parallel solos + paired workshops + closeout that will explore them. The workshops PRODUCE carry-forward computations for the next plan; they do NOT consume them (no bootstrap). Output is a ready-to-dispatch schedule where each entry is a fully-specified /rclab-review invocation. Canonical reference: sessions/session-82/session-82-workshop-schedule.md.
argument-hint: <topic> [--session <N>] [--planner <agent-type>] [--context <file>...] [--dry-run]
---

# Collab-Workshops — Workshop-Schedule Campaign Generator

## --help

If `$ARGUMENTS` contains `--help` or `-h` (or is empty and the user seems confused), read and display `.claude/rclab-help.md`, then stop. Do not proceed with any other phase.

---

Generate a **workshop-schedule campaign** derived from a completed session's findings. The output is a single schedule file containing a ready-to-dispatch list of `/rclab-review` invocations organized into slots (parallel solos → sequential workshops → closeout).

**When to use**: after a session's compute phase closes and you want deep refinement + exploration of the findings BEFORE the next session plans. The workshop-schedule is an artifact of the SOURCE session (it lives in `sessions/session-{SOURCE}/`) and produces the carry-forward computations that the NEXT compute session (S{SOURCE+1}) will consume.

**When NOT to use**: planning a new compute session with pre-registered gates (use `/rclab-plan` instead).

**What's different from `/rclab-plan`**:
- Output is a schedule of `/rclab-review` invocations, NOT a plan of computations.
- No prompter phase — the schedule entries ARE the dispatch specs.
- Planner default is `<domain-generalist>` (cross-domain pattern detection is the natural fit for carry-forward campaign design).

## Usage

```
/rclab-investigate                                       # defaults — mine the latest closed session's working paper; schedule lives in that session's folder
/rclab-investigate "substrate self-determination followup"
/rclab-investigate --session 84
/rclab-investigate --planner <domain-generalist>
/rclab-investigate --context sessions/session-83/session-83-results-workingpaper.md
/rclab-investigate --dry-run                             # show manifest, stop
```

---

## Phase 0: Parse & Validate

### 0a. Extract Arguments

Parse `$ARGUMENTS` for:

| Arg | Required | Default | Description |
|:----|:---------|:--------|:------------|
| `<topic>` | no | `"S{SOURCE_SESSION} workshop campaign"` | Campaign label (first positional arg, may be quoted). **The topic is just a NAME** — the actual scope is the deep-investigation of the source session's working paper (Phase 2.6). Never gate execution on topic presence. |
| `--session <N>` | no | auto-detect | **Source session number** (integer). Campaign lives IN `sessions/session-{N}/` (same folder as the compute session that produced the working paper). Defaults to latest session with a working paper. |
| `--planner <type>` | no | `<domain-generalist>` | Agent type for schedule generation. Cross-domain pattern-detection agent is the canonical choice because campaigns span multiple domains. |
| `--context <file>` | no | none | Extra context files (repeatable — each `--context` takes one path). Typical addition: a specific working paper not automatically picked up. |
| `--dry-run` | no | false | Show context manifest + output paths, then stop. |

### 0b. Resolve Topic (do NOT stop on empty)

The topic is a LABEL, not a scope. The real scope of any `/rclab-investigate` run is the deep-investigation of the source session's working paper (Phase 2.6). **Never stop execution for missing topic.**

- If `<topic>` was provided, use it verbatim.
- If `<topic>` is empty or missing, default to `"S{SOURCE_SESSION} workshop campaign"` where SOURCE_SESSION is resolved in Phase 1a.

### 0c. Validate Agent Type

Check that `--planner` exists in `.claude/agents/`. See `.claude/templates/agent-roster.md` for the canonical list. If invalid, list available types and stop.

### 0d. Validate Context Files

If `--context` files are provided, verify each exists (Read tool, 1 line). If any missing, report which files were not found and stop.

---

## Phase 1: Session ID Resolution

**IMPORTANT FRAMING**: the workshop-schedule campaign LIVES INSIDE the source session's folder. It does NOT consume a new session number. S82's workshop-schedule is at `sessions/session-82/session-82-workshop-schedule.md` — a SESSION-82 artifact, not a separate session. The NEXT compute session (via `/rclab-plan`) is numbered `SOURCE_SESSION + 1`, but that's a later skill invocation, not this one.

### 1a. Resolve Source Session Number

The campaign operates ON the source session. If `--session` was provided, that IS the source session. If not:

1. Glob for `sessions/session-*/session-*-results-workingpaper.md`
2. Extract session numbers from filenames, take the LATEST (highest N with a working paper)
3. `SOURCE_SESSION = max(found)` — the most recently closed compute session

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

The planner's invocation-context strings reference "next compute session" as `S{SOURCE_SESSION + 1}`. For example, if source = 83, next-compute = S84 ("feeds into S84 planning", "pre-register a gate S84-{name}"). This is what goes in the context strings — NOT a session folder or output path.

Set `NEXT_COMPUTE = SOURCE_SESSION + 1` and pass it to the planner so it can reference the correct future session in gate names and deliverable summaries.

---

## Phase 2: Verify Source Documents Exist

The skill does NOT read + aggregate context into a pre-digest file. That's the planner's job — the planner reads the raw working paper directly to find structural patterns (any pre-digest would be a lossy compression of exactly the material the planner needs unfiltered).

The skill's job is to VERIFY the source documents exist + PASS their paths to the planner. Build a manifest of expected sources:

| Source | Path | Required? |
|:-------|:-----|:---------:|
| Source working paper | `sessions/session-{SOURCE_SESSION}/session-{SOURCE_SESSION}-results-workingpaper.md` | YES |
| Source gate verdicts | `tier0-computation/s{SOURCE_SESSION}_gate_verdicts.txt` | YES |
| Source plan | `sessions/session-plan/session-{SOURCE_SESSION}-plan.md` | YES |
| Prior syntheses (if any) | glob `sessions/session-{SOURCE_SESSION}/session-*-{synthesis,synth,workshop,collab}.md` | optional |
| Permanent results registry | `sessions/permanent-results-registry.md` | optional |
| Framework MEMORY | `C:\Users\ryan\.claude\projects\<project-slug>\memory\MEMORY.md` | optional (auto-loaded into agent context regardless) |
| Planner agent memory | `.claude/agent-memory/{planner-agent-type}/MEMORY.md` | optional (auto-loaded) |
| Extra `--context` files | from flag | optional |

If any REQUIRED source is missing, report + stop. Otherwise, proceed to Phase 2.6 directly — no intermediate context file.

### 2a. Dry-Run Checkpoint

If `--dry-run`: display the source manifest + output paths + planner type, then STOP.

```
=== COLLAB-WORKSHOPS DRY RUN ===
Topic: "{topic}"
Source session: {SOURCE_SESSION} (campaign lives IN this folder)
Next compute: S{NEXT_COMPUTE} (referenced in context strings but NOT created)
Schedule file: {SCHEDULE_FILE}
Planner: {planner-type}

Sources verified:
  sessions/session-{SOURCE_SESSION}/session-{SOURCE_SESSION}-results-workingpaper.md  [size]
  tier0-computation/s{SOURCE_SESSION}_gate_verdicts.txt                                [size]
  sessions/session-plan/session-{SOURCE_SESSION}-plan.md                               [size]
  ... (optional sources marked present or missing)

Ready to spawn planner agent. Run without --dry-run to proceed.
```

---

## Phase 2.6: Seed-Extraction Guidance (for the Planner, not the Skill)

The skill does not extract seeds. The planner does that in-process while reading the working paper. What the skill provides is the PATTERN CATALOG the planner will use during its deep-read pass. This catalog goes into the planner's prompt (Phase 3), not into a file.

Reference pattern: the S82 workshop-schedule (9 entries from reading S80 + S82 working papers) — `sessions/session-82/session-82-workshop-schedule.md`. Every entry there came from the planner NOTICING a structural pattern in the working paper, not from a pre-existing list.

### Seed-Extraction Patterns (what to look for in the working paper)

Read the source working paper gate-by-gate. For each of the 9 patterns below, scan for instances. Each instance is a campaign-seed candidate.

**Pattern 1 — Convergence** (candidate: 3-agent solo to produce canonical statement)
Two or more gates prove the SAME thing via DIFFERENT machinery. Each proof is independently correct but scattered across §W{W}-G{G} sections. The canonical statement hasn't been written. Example: S82 W2-3 + W3-3 → Universal Level-2 Cartan Exclusion Theorem.

**Pattern 2 — Dissonance** (candidate: 2-agent 3-round workshop, ledger-adjudication)
Two tracks compute the same observable and get materially different answers. Both tracks pass their own internal gates. Example: S82 W1-1 TD H̃=5.91e-3 vs LI H̃=2.46e-5 (2.38 OOM gap).

**Pattern 3 — Corridor without phenomenology** (candidate: 2-agent solo to map corridor)
Bounds are established (floor + ceiling) but the PHENOMENOLOGY inside the bounds is not written — what is structurally permitted vs kinematically forbidden, what response function governs observables across the corridor. Example: S82 W2-4 + W3-6 → Substrate-IC Corridor Phenomenology.

**Pattern 4 — Elimination-without-explanation** (candidate: 2-agent solo, structural-elimination bulletins)
A FAIL verdict closed a hypothesis but the §W{W}-G{G} section doesn't spell out (a) which hypothesis is now false, (b) what surviving mechanisms must now carry the load, (c) the solution-space dimensionality reduction. Example: S82 W2-2, W2-8, W2-9 → Structural-Failure Constraint-Map Synthesis.

**Pattern 5 — Recurring pattern across multiple gates** (candidate: 2-agent 2-round workshop, taxonomy)
The same structural behavior shows up in 3+ gates (e.g., "ratios are observables; absolute moments are regulator-dressed" recurs in H̃_B vs H̃_A, f_0, E_J). Needs universal classification into a theorem or taxonomy. Example: S82 H̃-epoch + W2-13 + W3-7 → Regulator-Dressing Taxonomy Extension (§VII.K).

**Pattern 6 — Dual-channel ambiguity** (candidate: 2-agent 3-round workshop, diagrammatic audit)
Two channels are CLAIMED independent but never PROVEN independent — might be double-counted. Example: S82 F_amp_slot (0.39) vs F_amp^{3PI} (47.92) — "ceiling and floor bracket a safe band" asserted but derivation missing → A_s Ledger Self-Consistency workshop.

**Pattern 7 — Scattered falsifiers** (candidate: 2-agent solo, inventory + roadmap)
Multiple sign-definite falsifiable predictions registered in different gates but not consolidated into a coherent observational campaign with timeline + EVOI ordering. Example: S82 α_f_NL + n_T + C_cons + DR3 + GW γ/α → Falsifier Campaign Inventory.

**Pattern 8 — Methodology debts** (candidate: 2-agent 2-round workshop, rule-file diff)
Failure modes that recurred in the session (e.g., agents emitting verdicts without artifacts; PRU class 8 floatation; SHA collisions) need an audit that proposes a rule-file v2 diff. Example: S82 Section IX.A item 13 → Completion-Verification Methodology Audit.

**Pattern 9 — Deferred synthesis** (candidate: 3-agent multi-perspective closeout)
The working paper explicitly DEFERS a synthesis. Always lands as Slot 3 closeout depending on earlier workshops. Example: S82 §X deferred S80↔S82 combined landscape → S-5 closeout synthesis.

### Extraction Procedure

1. Read the source working paper in passes. First pass: skim all §W{W}-G{G} headers + verdict lines for overall shape. Subsequent passes: read full Results blocks when a pattern match is suspected.
2. For each pattern instance, record:
   - **Seed title** (one-line, domain-specific)
   - **Source gates** (which §W{W}-G{G} sections provide the evidence)
   - **Pattern type** (1–9 above)
   - **Why it matters** (2-3 sentences — what structural hole the workshop/synthesis would fill)
   - **Candidate agents** (from agent-roster.md; pair for complementary tracks)
   - **Candidate classification**: Slot 1 solo / Slot 2 workshop / Slot 3 closeout

3. Deduplicate and coalesce: if two seeds cover the same structural territory, merge them or split the scope explicitly.

4. Don't force all 9 patterns to produce seeds. A session may naturally produce 6-10 seeds total. S82 produced 9 entries (4 solos + 3 workshops + 2 closeout). Target ~6-12 entries for a typical compute session's post-session campaign.

### Seed→Schedule Enforcement (for the planner)

The planner, while reading the working paper, records seeds in-process and then writes them directly into the schedule. No intermediate file. Enforcement rules the planner must follow:

- **Every seed the planner identifies MUST appear in the schedule** as a Slot 1 solo, Slot 2 workshop, or Slot 3 closeout entry.
- **Nothing gets "DEFERRED" status** — if a pattern is noticed but can't fit the campaign, it goes into the schedule's own "Planning Input Checklist" for S{NEXT_COMPUTE} as an explicit hand-off, not a deferral.
- **The workshop OUTPUTS ARE the carry-forward computations** for S{NEXT_COMPUTE}. Each workshop's Wrap-Up must include a 4-field structured carry-forward (what/inputs/gate/effort) per `feedback_carry-forward-mandatory.md`. This is how the next compute session's plan gets its inputs.

---

## Phase 3: Spawn Schedule Planner

Create a task for tracking:

```
TaskCreate: subject="Generate S{SOURCE_SESSION} workshop schedule: {topic}"
```

Spawn a **solo background agent** using the Agent tool:

- `subagent_type`: from `--planner` flag (default: `<domain-generalist>`)
- `run_in_background`: true
- `name`: `workshop-planner`
- `mode`: `"acceptEdits"` — planner writes schedule file only
- `effort`: `"thorough"` — schedule design spans multiple domains

### Planner Agent Prompt

```
You are generating a **workshop-schedule campaign** for the {{PROJECT_NAME}} project.

## Your Task

Write a campaign schedule to: `{SCHEDULE_FILE}`

**Topic (label)**: {topic}
**Source session**: {SOURCE_SESSION} (campaign lives IN this folder; next compute session will be S{NEXT_COMPUTE})
**Source session**: {SOURCE_SESSION}
**Date**: {today}

## What a Workshop Schedule IS

It is a ready-to-dispatch list of `/rclab-review` invocations organized into slots:
- Slot 1: parallel independent solos (no cross-deps)
- Slot 2: workshops (sequential within each; parallel across when non-overlapping)
- Slot 3: closeout (depends on Slot 1/2 outputs)

The deliverable IS the schedule. Each entry must be a fully-specified `/rclab-review` invocation that the user can copy-paste and dispatch directly.

## Source Documents (read these directly)

| Source | Path | Role |
|:-------|:-----|:-----|
| Source working paper | `sessions/session-{SOURCE_SESSION}/session-{SOURCE_SESSION}-results-workingpaper.md` | **PRIMARY** — all §W{W}-G{G} Results blocks. Large file (~1000-8000 lines typical). Chunk reads at ~30KB to avoid silent Read-tool failures. Seeds come from here. |
| Source gate verdicts | `tier0-computation/s{SOURCE_SESSION}_gate_verdicts.txt` | Permanent verdict file with 64-char SHAs. Dual-entry permanence applies (latest wins per gate ID). |
| Source plan | `sessions/session-plan/session-{SOURCE_SESSION}-plan.md` | Original pre-registrations + substitution chains. Cross-reference what was supposed to happen vs what did. |
| Permanent results registry | `sessions/permanent-results-registry.md` | Theorems landed at/before S{SOURCE_SESSION}. |
| Optional prior syntheses | glob `sessions/session-{SOURCE_SESSION}/session-*-{synthesis,synth,workshop,collab}.md` | Usually empty for a just-closed session — this campaign is what produces them. |

**What you're looking for**: STRUCTURAL PATTERNS in the working paper — not a pre-existing carry-forward list. Carry-forwards will be OUTPUTS of the workshops you're scheduling. See the Seed-Extraction Patterns section below.

Reference: the S82 workshop-schedule at `sessions/session-82/session-82-workshop-schedule.md` is the gold-standard example of the structure and context-string fidelity expected. Study it before writing the S{SOURCE_SESSION} schedule.

## Seed-Extraction Patterns (scan the working paper for these)

**Pattern 1 — Convergence** (candidate: 3-agent solo to produce canonical statement)
Two or more gates prove the SAME thing via DIFFERENT machinery. Canonical statement not yet written.

**Pattern 2 — Dissonance** (candidate: 2-agent 3-round workshop, ledger-adjudication)
Two tracks compute the same observable and get materially different answers. Both pass their own internal gates.

**Pattern 3 — Corridor without phenomenology** (candidate: 2-agent solo to map corridor)
Bounds established (floor + ceiling) but phenomenology inside bounds not written.

**Pattern 4 — Elimination-without-explanation** (candidate: 2-agent solo, structural-elimination bulletins)
FAIL verdict closed a hypothesis but doesn't spell out (a) which hypothesis is now false, (b) surviving mechanisms, (c) solution-space dimensionality reduction.

**Pattern 5 — Recurring pattern across multiple gates** (candidate: 2-agent 2-round workshop, taxonomy)
Same structural behavior shows up in 3+ gates — needs universal classification.

**Pattern 6 — Dual-channel ambiguity** (candidate: 2-agent 3-round workshop, diagrammatic audit)
Two channels CLAIMED independent but never PROVEN independent — might be double-counted.

**Pattern 7 — Scattered falsifiers** (candidate: 2-agent solo, inventory + roadmap)
Multiple sign-definite falsifiable predictions registered in different gates but not consolidated into a coherent observational campaign with timeline + EVOI ordering.

**Pattern 8 — Methodology debts** (candidate: 2-agent 2-round workshop, rule-file diff)
Failure modes that recurred in the session — need audit proposing rule-file v2 diff.

**Pattern 9 — Deferred synthesis** (candidate: 3-agent multi-perspective closeout)
Working paper explicitly DEFERS a synthesis. Always lands as Slot 3 closeout.

**Extraction procedure**:
1. Skim pass: all §W{W}-G{G} headers + verdict lines for overall shape.
2. Targeted read pass: full Results blocks when a pattern match is suspected. Chunk at ~30KB.
3. Record per seed: title, source gates, pattern type, why it matters, candidate agents, candidate slot classification.
4. Deduplicate and coalesce overlapping seeds.
5. Target: 6-12 entries. S82 produced 9.

## Template

Read `.claude/templates/workshop-schedule.md` and follow it EXACTLY. See the "Planner's instructions" section at the bottom of the template for generation rules.

## Rules

1. **Mine the source material**: explicit deferrals, unresolved adjudications, claimed-but-unformalized theorems, honest-admission debts, observational watchlists. These are campaign seeds.

2. **Classify each seed** as solo / workshop / closeout (per Phase 2.6 classification).

3. **Organize into slots** by dependency (Slot 1 independent, Slot 2 workshops, Slot 3 closeout).

4. **Write exact `/rclab-review` invocations** — not narrative descriptions. Each must be copy-paste-ready with all flags, agent lists, session pins, and full context strings.

5. **Context strings must be full-fidelity**: every specific gate ID, numeric anchor, classification seed, adjudication rule the synthesis needs. NO "see source docs" or "appropriate context" — be explicit.

6. **Agent selection**: use `.claude/templates/agent-roster.md` canonical short names. Pair agents whose domains intersect on the target question. For workshops, pair agents covering COMPLEMENTARY TRACKS of the same claim (e.g., TD vs LI for mode-equation vs spectral-functional; connes vs van-den-dungen for K-theory vs KK).

7. **Rounds**:
   - Workshop defaults to 2 rounds.
   - Use 3 rounds when the adjudication is genuine ledger-dissonance (R1 steelman, R2 respond, R3 converge).
   - Use 1 round only for informational exchanges (rare).

8. **No length targets** in invocation contexts. Content requirements only ("include X table", "include Y gate").

9. **Carry-forward mandate**: every invocation context must demand the 4-field structured carry-forward (what/inputs/gate/effort) per `feedback_carry-forward-mandatory.md`.

10. **Deliverable table**: explicitly list every file the campaign will produce, with agent responsible and next-session consumption pattern.

11. **Planning Input Checklist**: list what the NEXT session's planner should expect from the campaign (adjudication results, new gate IDs, registry drafts, observational watchlists, combined-landscape docs, methodology diffs).

12. **Concurrency cap**: max 7-8 concurrent Agent dispatches per project rule. If Slot 1 exceeds 8, split into Slot 1a / Slot 1b sub-slots.

13. **Graceful degrade**: Slot 3 items must reference Slot 2 outputs "if landed" so agents degrade gracefully if dependencies haven't completed.

14. **Do NOT execute syntheses** — only schedule them.
15. **Do NOT modify MEMORY.md, agent memory, or the knowledge index.**
16. **Write ONLY the schedule file.**
```

### Wait for Planner

Wait for the planner agent to complete. Then:

1. Verify `{SCHEDULE_FILE}` exists.
2. Read it, extract line count.
3. Extract slot counts (Slot 1 entries, Slot 2 workshops, Slot 3 closeout items).

If the file doesn't exist or is empty, report failure and suggest trying a different planner type.

---

## Phase 4: User Checkpoint

Report to the user:

```
=== WORKSHOP SCHEDULE GENERATED ===

File: {SCHEDULE_FILE}
Lines: {count}
Topic: "{topic}"
Source session: {SOURCE_SESSION} (campaign lives IN this folder; next compute = S{NEXT_COMPUTE})
Source session: {SOURCE_SESSION}
Planner: {planner-type}

Slot 1 (parallel solos): {count} entries
Slot 2 (workshops): {count} entries
Slot 3 (closeout): {count} entries
Total campaign entries: {total}

Next: Dispatch Slot 1?
```

Use AskUserQuestion with options:
- **Dispatch Slot 1 now** — you (the orchestrator) invoke each Slot 1 `/rclab-review` entry.
- **Edit schedule first** — user will edit manually, then dispatch later.
- **Stop here** — schedule is sufficient; user handles dispatch.

If user provides feedback text (via "Other"), re-spawn the planner with the original prompt PLUS the feedback appended under `## User Feedback`. Return to the checkpoint.

---

## Phase 5: Report

```
=== COLLAB-WORKSHOPS COMPLETE ===

Topic: "{topic}"
Source session: {SOURCE_SESSION} (campaign lives IN this folder; next compute = S{NEXT_COMPUTE})
Source session: {SOURCE_SESSION}

Generated File:
  {SCHEDULE_FILE}                                      {lines} lines

Planner: {planner-type}
Slots: 3 (Slot 1 parallel solos, Slot 2 sequential workshops, Slot 3 closeout)
Total campaign entries: {count} ({N_solo} solo syntheses + {N_workshop} workshops + {N_closeout} closeout)
Context sources: {count} files ({total_lines} lines)

Next step:
  Dispatch Slot 1 entries in parallel (copy each /rclab-review invocation from the schedule).
  Wait for all Slot 1 to land, then dispatch Slot 2 sequentially.
  Finally dispatch Slot 3 closeout items.
  Each invocation is already fully specified — no further editing needed.
```

---

## Safety Rules

1. **Never overwrite existing files** without user confirmation (Phase 1c collision check).
2. **Never spawn teams** — solo agents only. No TeamCreate, no SendMessage, no blast.
3. **Never execute syntheses** — schedule-file only. The schedule is the deliverable; dispatch is a separate step.
4. **Never modify MEMORY.md**, agent memory files, or the knowledge index. Read only.
5. **Concurrency cap**: max 7-8 concurrent Agent dispatches when the user later dispatches Slot 1. If the schedule's Slot 1 has >8 solos, the schedule MUST split into 1a/1b sub-slots.
6. **Carry-forward enforcement is mandatory** — Phase 2.6 runs before every planner spawn. Every seed becomes an entry. No deferrals.

## Error Handling

| Condition | Action |
|:----------|:-------|
| Empty topic | Auto-generate per Phase 0b (no stop). Topic is a label; carry-forward mining is the scope. |
| Agent type not found | List available types from `.claude/agents/` and stop. |
| Context file missing | Report which file(s) not found and stop. |
| Session ID collision | AskUserQuestion: overwrite / next number / cancel. |
| Source session folder missing | AskUserQuestion: which session to mine (suggest latest-with-working-paper, or earlier user-specified). |
| Schedule file empty after planner | Report failure, suggest different planner type. |
| Context very large (>10000 lines) | Report total size to user, proceed unless user stops. |
| Planner agent errors out | Report error, show agent output, suggest retry. |

---

## Relationship to Other Skills

- **`/rclab-plan`** — for planning a NEW compute session with pre-registered gates. Use AFTER a campaign closes to plan S{N+1}. (This skill is for a different phase of the pipeline.)
- **`/rclab-review`** — the TARGET skill that each schedule entry invokes. This skill GENERATES `/rclab-review` invocations; it does not invoke them.
- **`/rclab-coordinate`** — unrelated. Used for compute-mode dispatch of a session plan, not for workshop campaigns.

The full pipeline: compute session S{N} (via `/rclab-plan` then `/rclab-coordinate`) → **workshop campaign IN S{N}'s folder (via `/rclab-investigate`)** → next compute session S{N+1} (via `/rclab-plan`). Note: the workshop campaign does NOT consume a session number; it's a post-compute phase of the source session.

---

## Notes

- Default planner is `<domain-generalist>` because cross-domain pattern detection is the natural fit for campaign design (workshops span K-theory, spectral functionals, observational bridges, etc.).
- The workshops subdirectory `sessions/session-{SOURCE_SESSION}/workshops/` is created on first Write. Solo outputs land in `sessions/session-{SOURCE_SESSION}/session-{SOURCE_SESSION}-{short-name}-synthesis.md` per `/rclab-review` defaults.
- Auto-detection default takes the LATEST session with a working paper as SOURCE_SESSION. Override with `--session <N>` to run a workshop campaign on an earlier session (e.g., if S{N}'s campaign never landed and you're rebuilding it retroactively).
