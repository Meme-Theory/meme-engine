---
name: clab-plan
description: Generate session plans and prompts from a topic — context assembly, planner agent, user checkpoint, prompter agent
argument-hint: <topic> [--session <N>] [--format compute|workshop|panel] [--sub-sessions <N>] [--planner <agent-type>] [--prompter <agent-type>] [--context <file>...] [--dry-run]
---

# Clab-Plan — Session Plan & Prompt Generator

Automate the session planning pipeline: topic -> context -> plan -> prompts. The skill assembles project context deterministically, spawns a solo planner agent to produce the plan document, checkpoints with the user, then spawns a solo prompter agent to generate self-contained prompt files. No teams — sequential solo agents only.

## Usage

```
/clab-plan "Initial domain survey"
/clab-plan "Initial domain survey" --planner coordinator
/clab-plan "Constraint boundary analysis" --format compute --session 12
/clab-plan "Cross-domain integration test" --format panel --session 5 --sub-sessions 3
/clab-plan "Parallel computation sprint" --format compute --planner workhorse
/clab-plan "test topic" --dry-run
/clab-plan "Literature gap analysis" --context sessions/session-05/session-5-synthesis.md
```

---

## Phase 0: Parse & Validate

### 0a. Extract Arguments

Parse `$ARGUMENTS` for:

| Arg | Required | Default | Description |
|:----|:---------|:--------|:------------|
| `<topic>` | YES | — | The session topic (first positional arg, may be quoted) |
| `--session <N>` | no | auto-detect | Session number (integer) |
| `--format <fmt>` | no | `compute` | Session format — see below |
| `--sub-sessions <N>` | no | planner decides | Number of prompt files to generate (team formats only) |
| `--planner <type>` | no | `coordinator` | Agent type for plan generation |
| `--prompter <type>` | no | `coordinator` | Agent type for prompt generation |
| `--context <file>` | no | none | Extra context files (repeatable — each `--context` takes one path) |
| `--dry-run` | no | false | Show context manifest and output paths, then stop |

#### Format Options

| Format | Description | Plan Structure | Prompt Output |
|:-------|:-----------|:---------------|:-------------|
| `compute` | Wave-based parallel independent agents. Each computation is an independent Agent call. No teams. Shared working paper. Decision points between waves. | Waves + per-computation specs + decision points | ONE plan file + ONE working paper template |
| `workshop` | Sequential paired discussions in rounds. ONE team at a time. Markdown handoff between rounds. | Round definitions + participant pairs + topics | Per-round prompt files |
| `panel` | Interpretive panel with designated writer. 2-3 specialists + writer synthesize. | Thesis + specialist assignments + output structure | Single prompt file |

If `--format` is omitted, default is `compute`.

### 0b. Validate Topic

If `<topic>` is empty or missing, show the Usage block above and stop.

### 0c. Validate Agent Types

Check that `--planner` and `--prompter` agent types exist in `.claude/agents/`. List all `.claude/agents/*.md` files and match against the provided type names (case-insensitive, filename minus `.md`).

If invalid, list available types and stop.

### 0d. Validate Context Files

If `--context` files are provided, verify each exists using the Read tool (read 1 line). If any missing, report which files were not found and stop.

---

## Phase 1: Session ID Resolution

### 1a. Auto-Detect Session Number

If `--session` was NOT provided:

1. Glob for `sessions/session-plan/session-*-plan.md`
2. Extract session numbers from filenames (e.g., `session-12-plan.md` -> 12)
3. Set the next session number = max(found) + 1

If no existing plans found, default to session 1.

If `--session` was provided, use that number.

### 1b. Set Output Paths

```
PLAN_FILE = sessions/session-plan/session-{N}-plan.md
PROMPT_PREFIX = sessions/session-plan/session-{N}
SESSION_FOLDER = sessions/session-{N}/
```

Sub-session labels use lowercase letters: `a`, `b`, `c`, ... Prompt files become:
```
session-{N}a-prompt.md
session-{N}b-prompt.md
session-{N}c-prompt.md
...
```

If `--sub-sessions` was provided, the exact count is known. Otherwise the planner decides and declares it in the plan.

### 1c. Check for Collisions

Check if `PLAN_FILE` already exists. If so, use AskUserQuestion:
- "Session {N} plan already exists at {path}. Overwrite / Pick next number / Cancel?"

---

## Phase 2: Context Assembly

**The skill itself assembles context** — this is deterministic, not agent-dependent. Read the following sources in order, accumulating a context package. Track line counts. Stop accumulating when total exceeds ~6000 lines (truncate oldest-added source first).

### 2a. Project Memory

Read the project's auto-memory MEMORY.md (check `.claude/agent-memory/coordinator/MEMORY.md` or the project memory path). This contains methodology summary, session patterns, active state, and team protocol. (~200 lines)

### 2b. Latest Session Syntheses

1. Glob for `sessions/session-*/session-*-synthesis.md` (and `*-synth.md`)
2. Sort by modification time (newest first)
3. Read the 2 most recent syntheses completely

These establish where the project stands RIGHT NOW. (~300-600 lines total)

### 2c. Latest Gate Verdicts

1. Glob for gate verdict files: `sessions/session-*/*gate_verdicts*` and any `*_gate_verdicts.txt` in output directories
2. Sort by modification time (newest first)
3. Read the 3 most recent verdict files

These establish which gates have fired, which are pending. (~100-300 lines total)

### 2d. Knowledge Index: Open Channels + Gates

Read `tools/knowledge-index.json` and extract:
- The `active_channels` array (all open research avenues)
- The `gates` array (all constraint gates with verdicts)

Format as concise tables. (~200-400 lines)

### 2e. Proven Results

If `tools/knowledge-index.json` contains `proven_results`, extract and format them. Alternatively, check for a standalone results registry file. This lists all established results. (~100-200 lines)

### 2f. Planner Agent Memory

Read `.claude/agent-memory/{planner-agent-type}/MEMORY.md` if it exists. This gives the planner's accumulated context from prior sessions. (~100-200 lines)

### 2g. Extra Context Files

If `--context` files were provided, read each completely and append to the context package.

### 2h. Context Manifest

Build a manifest listing every source read, its line count, and whether it was truncated:

```
=== CONTEXT MANIFEST ===
Source                                          Lines   Truncated
coordinator MEMORY.md                           200     no
session-10b-synthesis.md                        185     no
session-10a-synthesis.md                        220     no
session-10b gate verdicts                       42      no
session-10a gate verdicts                       38      no
session-09c gate verdicts                       55      no
knowledge-index: active_channels                45      no
knowledge-index: gates                          180     no
proven_results                                  150     no
{planner} agent memory                          95      no
---
Total context: 1210 lines (cap: 6000)
```

### 2i. Dry Run Checkpoint

If `--dry-run`:

Display the manifest, output paths, and proposed agent types, then STOP. Do not create files or spawn agents.

```
=== CLAB-PLAN DRY RUN ===

Topic: "{topic}"
Session: {N}
Format: {compute|workshop|panel}
Plan file: {PLAN_FILE}
Prompt prefix: {PROMPT_PREFIX}
Sub-sessions: {count or "planner decides"}
Planner: {planner-type}
Prompter: {prompter-type}

{context manifest from 2h}

Ready to spawn planner agent. Run without --dry-run to proceed.
```

---

## Phase 3: Spawn Planner Agent

Spawn a **solo background agent** (NOT a team) using the Agent tool:

- `subagent_type`: from `--planner` flag (default: `coordinator`)
- `run_in_background`: true
- `name`: `planner`

### Planner Agent Prompt

```
You are generating a **session plan** for this research project.

## Your Task

Write a session plan to: `{PLAN_FILE}`

**Topic**: {topic}
**Session number**: {N}
**Date**: {today's date}

## Context Package

The following is assembled project context — methodology status, recent results, open gates, and active channels. Use this to inform your plan.

---START CONTEXT---
{full context package from Phase 2}
---END CONTEXT---

## Plan Structure

The plan format depends on `--format`. Use EXACTLY ONE of the following structures.
```

#### FORMAT: `compute` (MANDATORY structure for compute plans)

```markdown
# Session {N} Plan: {Topic Title}

**Date**: {date}
**Author**: Team-lead (generated by /clab-plan, planner: {planner-type})
**Format**: Parallel single-agent computations across {W} waves
**Source**: {which sessions/syntheses informed this plan}
**Motivation**: {1-2 sentences: why this session, why now}
**Results file**: `sessions/session-{N}/session-{N}-results-workingpaper.md`

---

## I. Session Objective

{1-2 paragraphs: what this session resolves, what the pre-registered master gate is}

**Pre-registered master gate**:
- **{GATE-ID}**: {description}
- **PASS**: {condition}
- **FAIL**: {condition}
- **Null hypothesis**: {what the default expectation is}

## II. Wave Structure

### Dependency Graph

{ASCII diagram showing waves and which can run in parallel. Example:}
```
Wave 1 (parallel, no dependencies):
  W1-A  W1-B  W1-C  W1-D

Wave 2 (parallel, can co-run with W1):
  W2-A  W2-B  W2-C

Wave 3 (depends on Wave 1 results):
  W3-A  W3-B  W3-C
```

## III. Wave {M}: {Wave Title}

{Repeat this section for each wave. Within a wave, all tasks are independent.}

### W{M}-{L}: {Computation Title}

**Agent**: `{agent-type}`
**Model**: {sonnet or opus}
**Cost**: {ZERO / LOW / MEDIUM / HIGH}

**Prompt**:

{The COMPLETE self-contained prompt for this agent. Include:}
- Context paragraph (what prior sessions established)
- Computation steps (numbered, specific)
- Input data files (full paths)
- Pre-registered gate (ID, PASS/FAIL criteria)
- Output files (script, data, plot paths)
- Working paper section to write to

---

## IV. Constraint Gates Summary

| ID | Type | Condition | Fires If | Consequence |
|:---|:-----|:----------|:---------|:------------|

{CRITICAL: Gate IDs must NOT collide with existing IDs in the knowledge index.}

## V. Decision Points

{Between-wave decision logic. For each decision point:}

**After Wave {M}**:
- If {condition A} -> {action A}
- If {condition B} -> {action B}
- If {condition C} -> {action C}

## VI. Execution Notes

- Python: {project's configured Python environment}
- Output directory: {project's configured output directory}
- Script prefix: `s{N}_`
- Each agent writes results ONLY to their designated section in the working paper
- No TeamCreate — all agents are independent Agent tool calls
```

#### FORMAT: `workshop` or `panel` (MANDATORY structure for these formats)

```markdown
# Session {N} Plan: {Topic Title}

**Date**: {date}
**Author**: Team-lead (generated by /clab-plan, planner: {planner-type})
**Phase**: {A/B/C or standalone}
**Source**: {which sessions/syntheses informed this plan}
**Motivation**: {1-2 sentences: why this session, why now}

---

## I. Relation to Prior Sessions

| Prior Output | Data File | This Session's Use |
|:-------------|:----------|:-------------------|

## II. Conditional Architecture

| Prior Outcome | This Session Scope |
|:-------------|:-------------------|

## III. Computation Plan

### {N}-{sub}: {Computation Title} [{COST ESTIMATE}, {SIGNIFICANCE}]

**Priority**: {number and source}
**Dependency**: {what must complete first, or "None"}
**What**: {1-2 paragraphs}
**Method**: {numbered steps}
**Gate condition**: {PASS criteria}
**Constraint Condition**: {FAIL consequence}
**Inputs**: {file list}
**Script**: {description}
**Computational cost**: {time estimate}
**Agent**: {agent type}
**Output**: {file list}

## IV. Constraint Gates Summary

| ID | Type | Condition | Fires If | Consequence |
|:---|:-----|:----------|:---------|:------------|

## V. Agent Assignments

| Agent | Type | Role | Computations |
|:------|:-----|:-----|:------------|

{Always include a coordinator agent.}

## VI. Sub-Session Structure

| Sub-Session | Computations | Agents | Dependencies |
|:-----------|:-------------|:-------|:-------------|

{Max 3 agents per sub-session, max 4 computations per sub-session.}

## VII. Required Reading

### All Agents
{files every agent must read}

### Agent-Specific
| Agent | Additional Reading |
|:------|:-------------------|
```

## Rules for the Planner

1. **Ground in data**: Every computation must reference specific input files that EXIST (check the context package for file paths).
2. **Non-colliding gate IDs**: Check the gates table in context. Use fresh IDs only.
3. **Realistic cost estimates**: Reference existing computation times from recent sessions if available.
4. **Format-specific agent rules**:
   - `compute`: No agent count limit per wave. Each task is independent. No coordinator needed (team-lead handles synthesis). Write COMPLETE self-contained prompts for each agent inside the plan.
   - `workshop`/`panel`: Max 3 agents per sub-session. Coordinator always included.
5. **Script prefix**: `s{N}_` for compute format, `s{N}{sub}_` for workshop/panel.
6. **Output directory**: Use the project's configured output directory (check CLAUDE.md or default to `sessions/session-{N}/`).
7. **Python**: Use the project's configured Python environment if applicable.
8. **Do NOT execute computations** — only plan them.
9. **Do NOT modify MEMORY.md, agent memory, or the knowledge index.**
10. **Write ONLY the plan file** — nothing else.
11. **Compute format**: Include decision points between waves. Each agent prompt must be fully self-contained (context, method, inputs, outputs, gate criteria) — agents cannot communicate with each other.
```

### Wait for Planner

Wait for the planner agent to complete. Then:

1. Verify the plan file exists at `{PLAN_FILE}`
2. Read it and extract the line count
3. Extract the declared sub-session count from Section VI

If the file doesn't exist or is empty, report failure and suggest trying a different planner agent type.

---

## Phase 4: User Checkpoint

Report to the user:

```
=== PLAN GENERATED ===

File: {PLAN_FILE}
Lines: {count}
Format: {compute|workshop|panel}
Planner: {planner-type}
Sub-sessions: {N_sub} ({list labels})
Computations: {count}
Gates: {count}

Next: Generate {N_sub} prompt files?
```

Use AskUserQuestion with options:
- **Continue to prompts** — proceed to Phase 5
- **Edit plan first** — user will edit manually, re-run `/clab-plan` afterward
- **Stop here** — plan is sufficient

If user provides feedback text (via "Other"), re-spawn the planner agent with the original prompt PLUS the feedback appended under a `## User Feedback` section. Then return to the checkpoint.

---

## Phase 5: Spawn Prompter Agent

Spawn a **solo background agent** (NOT a team):

- `subagent_type`: from `--prompter` flag (default: `coordinator`)
- `run_in_background`: true
- `name`: `prompter`

### Compute Format — Working Paper Generator

For `--format compute`, the prompter generates a **working paper template** (not per-sub-session prompts). The plan file itself IS the prompt — it contains the full self-contained prompts for each agent in each wave.

```
You are generating a **results working paper template** from an approved session plan.

## Your Task

Read the plan at `{PLAN_FILE}` and generate ONE file:
  `sessions/session-{N}/session-{N}-results-workingpaper.md`

## Structure

The working paper has:
1. A header with session metadata and instructions for contributing agents
2. One section per computation (matching the wave/task IDs from the plan)
3. Each section contains: Status, Gate ID + criteria, and a "Results" placeholder
4. A synthesis section at the end (for team-lead to fill after all waves)
5. A constraint map updates table
6. A files produced table

## Section Template (repeat for each W{M}-{L} in the plan)

```markdown
### W{M}-{L}: {Computation Title} ({agent-type})

**Status**: NOT STARTED
**Gate**: {GATE-ID}. {PASS/FAIL criteria from plan.}

**Results**:

*(Agent writes here)*

---
```

## Rules
1. Extract ALL computation IDs, titles, agents, and gate criteria from the plan
2. Group sections by wave (Wave 1, Wave 2, etc.)
3. Include the agent instructions block at the top (what to include in results: verdict, key numbers, cross-checks, data files, assessment)
4. Write ONLY the working paper file — nothing else
5. Do NOT modify the plan file
```

### Workshop & Panel Formats — Prompt File Generator

For `--format workshop` or `--format panel`, the prompter generates per-sub-session prompt files.

```
You are generating **session prompt files** from an approved plan for this research project.

## Your Task

Read the plan at `{PLAN_FILE}` and generate {N_sub} prompt files:
{list of prompt file paths}

## Context

Read the plan file first. It contains the full computation plan, agent assignments, gate conditions, and sub-session structure.

Also read for format reference (if they exist):
- The 2 most recent prompt files in `sessions/session-plan/` — use as gold-standard format examples

## Prompt Structure (MANDATORY — follow this format exactly for EACH prompt file)

```markdown
# Session {N}{sub}: {Sub-Session Title}

**Date**: TBD
**Author**: Team-lead (generated by /clab-plan, prompter: {prompter-type})
**Depends on**: {prior sub-session or "None"}
**Prerequisite**: {what must be true before this sub-session runs}
**Input data**:
{list of input files with descriptions}

## Motivation

{2-3 sentences: what this sub-session accomplishes and why}

---

# SESSION DASHBOARD

## Prerequisites

| ID | Requirement | Source | Status |
|:---|:-----------|:-------|:-------|

## Computation Steps (this sub-session)

| Step | Description | ~Scope | ~Cost | Status |
|:-----|:-----------|:-------|:------|:-------|

## Gate Verdicts (this sub-session)

| ID | Type | Short Description | Status |
|:---|:-----|:-----------------|:-------|

## Deliverables

| Output | Description | Status |
|:-------|:-----------|:-------|

---

# 0. OPERATIONAL RULES

## COMPUTATION DISCIPLINE

Every result classified against its pre-registered gate BEFORE any interpretation. Report the number first. Classify second. Interpret third.

**Python environment**: {project's configured Python environment, or "N/A — no computation"}
**Output directory**: {project's configured output directory}
**Script prefix**: `s{N}{sub}_`

## PRE-SESSION GATE CHECK (MANDATORY FIRST ACTION)

{What to verify before any computation. Check prior sub-session verdicts if applicable.}

## COMPLETION SIGNAL

Session ends ONLY when user approves shutdown explicitly. Idle agents are not finished agents.

---

# I. REQUIRED READING

## ALL agents (MANDATORY):

{numbered list of files every agent must read}

## Agent-specific required reading:

| Agent | Additional Reading |
|:------|:-------------------|

---

# II. AGENT ASSIGNMENTS

| Agent | Type | Role |
|:------|:-----|:-----|

{Always include coordinator. Max 3 agents total.}

---

# III. COMPUTATIONS

{For each computation assigned to this sub-session:}

## Step {M}: {Computation Title}

**Agent**: {agent name}

**What**: {description}

**Method**:
1. {step}
2. {step}

**Inputs**: {files}

**Output**: {expected output files}

**Gate**: {gate ID} — {condition}

---

# IV. CONSTRAINT GATES

| ID | Type | Condition | Fires If | Consequence |
|:---|:-----|:----------|:---------|:------------|

{Include ONLY gates relevant to THIS sub-session.}

---

# V. SYNTHESIS & OUTPUT

**Designated writer**: coordinator

**Synthesis file**: `sessions/session-{N}/session-{N}{sub}-synthesis.md`

**Gate verdicts file**: `sessions/session-{N}/s{N}{sub}_gate_verdicts.txt`

{Structure for synthesis document — sections, what to include.}
```

## Rules for the Prompter

1. **Each prompt must be self-contained**: A user running `/clab-team {prompt-file}` should need NO other context. Include all operational rules, environment config, file paths, gate conditions, and agent assignments in every prompt.
2. **Computation details from the plan**: Copy the full method, inputs, outputs, gate conditions, and constraint conditions from the plan into the corresponding prompt. Do not summarize — include the full specification.
3. **Agent count**: Max 3 per prompt (coordinator always included). If the plan assigns more, split across sub-sessions.
4. **Gate IDs**: Use EXACTLY the IDs from the plan. Do not rename or renumber.
5. **Script prefix**: `s{N}{sub}_` (e.g., `s12a_`, `s12b_`).
6. **Required reading**: Include both the ALL-agents list from the plan AND the agent-specific list. Add the plan file itself to the ALL-agents list.
7. **Dependencies**: If sub-session B depends on sub-session A, state this explicitly in the Prerequisites section and the PRE-SESSION GATE CHECK.
8. **Do NOT execute computations** — only write prompt documents.
9. **Do NOT modify MEMORY.md, agent memory, or the knowledge index.**
10. **Write ONLY the prompt files** — nothing else.
```

### Wait for Prompter

Wait for the prompter agent to complete. Then:

1. Verify each expected prompt file exists
2. Read each and extract line counts
3. Check each contains the mandatory sections (SESSION DASHBOARD, OPERATIONAL RULES, REQUIRED READING, AGENT ASSIGNMENTS, COMPUTATIONS, CONSTRAINT GATES)

If any files are missing, report which ones failed.

---

## Phase 6: Report

### Compute Format
```
=== CLAB-PLAN COMPLETE ===

Topic: "{topic}"
Session: {N}
Format: compute (parallel independent)

Generated Files:
  {PLAN_FILE}                                          {lines} lines
  sessions/session-{N}/session-{N}-results-workingpaper.md   {lines} lines

Planner: {planner-type}
Prompter: {prompter-type}
Waves: {W}
Total computations: {count}
Gates: {count}
Context sources: {count} files ({total_lines} lines)

Next step:
  /clab-team sessions/session-plan/session-{N}-plan.md --mode compute
```

### Workshop & Panel Formats
```
=== CLAB-PLAN COMPLETE ===

Topic: "{topic}"
Session: {N}
Format: {workshop|panel}

Generated Files:
  {PLAN_FILE}                              {lines} lines
  {prompt-file-1}                          {lines} lines
  {prompt-file-2}                          {lines} lines
  ...

Planner: {planner-type}
Prompter: {prompter-type}
Context sources: {count} files ({total_lines} lines)

Next step:
  /clab-team sessions/session-plan/session-{N}a-prompt.md --mode {workshop|panel}
```

---

## Safety Rules

1. **Never overwrite existing files** without user confirmation (Phase 1c collision check).
2. **Never spawn teams** — solo agents only. No TeamCreate, no SendMessage, no blast.
3. **Never execute computations** — documents only. No running scripts.
4. **Never modify MEMORY.md**, agent memory files, or the knowledge index. Read only.
5. **Context reads capped at ~6000 lines total**. Truncate oldest-added source first.
6. **Gate IDs in generated plans must not collide** with existing IDs in the knowledge index.
7. **Always include a coordinator** in agent assignments (except compute format where team-lead handles synthesis).

## Error Handling

| Condition | Action |
|:----------|:-------|
| Empty topic | Show usage block and stop |
| Agent type not found | List available types from `.claude/agents/` and stop |
| Context file missing | Report which file(s) not found and stop |
| Session ID collision | AskUserQuestion: overwrite / next number / cancel |
| Plan file empty after planner | Report failure, suggest different planner type |
| Prompt file(s) missing after prompter | Report which are missing, suggest re-running prompter |
| Context exceeds 6000 lines | Truncate oldest sources, report which were truncated |
| Planner agent errors out | Report error, show agent output, suggest retry |
| Prompter agent errors out | Report error, show agent output, suggest retry |
