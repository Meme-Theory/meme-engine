---
name: rclab-workshop
description: 2-agent iterative workshop on a shared document. Exactly 2 agents, N rounds (1-5), sequential — no team infrastructure. Each agent reads the running document, fills in their sections, completes before the next spawns.
argument-hint: <doc(s)> --agents <typeA,typeB> [--session <id>] [--rounds <N>] [--output <path>] [--context <text>]
---

# rclab-workshop

## --help

If `$ARGUMENTS` contains `--help` or `-h` (or is empty and the user seems confused), read and display `.claude/rclab-help.md`, then stop. Do not proceed with any other phase.

---

2-agent iterative workshop. Exactly 2 agents, N rounds (default 2, range 1-5), sequential — no team infrastructure. Each agent reads the running document, fills in their sections, and completes before the next spawns.

For solo synthesis (1+ agents independently writing reports from sources), use `/rclab-review`.

## Usage

```
# 2 agents, 2 rounds (default), focus topics
/rclab-workshop session-63*.md --agents hawking,qa --context CC closure, GL stability

# 3 rounds, explicit output
/rclab-workshop session-34*.md --agents kk,connes --rounds 3 --output sessions/session-34/session-34-kk-connes-workshop.md
```

---

## Phase 0: Parse & Validate

### 0a. Extract Arguments

Parse `$ARGUMENTS`:

| Arg | Required | Default | Notes |
|:----|:---------|:--------|:------|
| `[doc(s)]` | yes (1+) | — | Source doc paths or globs (positional, before flags) |
| `--agents` | yes | — | Comma-separated agent types or short names. EXACTLY 2. |
| `--session` | no | auto-detect | Session ID (e.g., `63`) |
| `--rounds` | no | `2` | Range: 1-5 |
| `--output` | no | auto-detect | Full output path |
| `--context` | no | — | Focus topics or instructions passed to agents |

### 0b. Validate

1. **Source docs**: Glob-resolve paths. Read 1 line of each to verify existence. Report missing and stop.
2. **Agent types**: Resolve short names via `.claude/templates/agent-roster.md`. If invalid, list available types and stop.
3. **Agent count**: Exactly 2. Anything else: error and stop.
4. **Rounds**: 1-5. Outside range: error and stop.

### 0c. Defaults

**Session ID** (if not provided):
- Extract from first source doc filename: regex `session-(\d+)`

**Output path** (if not provided):
- `sessions/session-{id}/session-{id}-{agentA-short}-{agentB-short}-workshop.md`

If session ID unresolvable, ask the user.

---

## Phase 1: Collision Check

If the output file already exists, ask: "Output file exists at `{path}`. Overwrite / New name / Cancel?"

---

## Phase 2: Execute

Workshop spawns exactly 2 agents **sequentially** — no team infrastructure. Each agent reads the running document, fills in their sections, and completes before the next spawns.

**Short name mapping**: Read `.claude/templates/agent-roster.md`.

### Step 1: Build Full Document Skeleton

**MANDATORY.** Build the COMPLETE workshop skeleton BEFORE launching any agent. Use `.claude/templates/workshop.md` as the structural reference. The skeleton must include:

- Header (date, format, agents, source docs, focus topics)
- ALL round headings for ALL rounds
- ALL turn sections with `*[NOT STARTED]*` placeholders
- Agent A's labeled topic sections (one per focus topic + cross-cutting)
- Agent B's response sections (Re: each of A's sections + original analysis + questions)
- Round 2+ CONVERGENCE / DISSENT / EMERGENCE / QUESTIONS sections
- Workshop Verdict table shell (final round)
- Remaining Open Questions placeholder

Write this skeleton with the Write tool in a single call. Agents fill placeholders using Edit — they never create structure.

### Step 2: Create Task Tracking

```
For each round r and turn (A, B):
  TaskCreate: "R{r}-A: {agent-a-short} analysis" (blockedBy: previous turn)
  TaskCreate: "R{r}-B: {agent-b-short} response" (blockedBy: R{r}-A)
```

### Step 3: Round Loop

For each round `r` from 1 to `--rounds`:

#### Turn A: Agent A

Spawn background agent:
- `subagent_type`: first agent from `--agents`
- `run_in_background`: true
- `name`: `workshop-{agent-a-short}-r{r}`
- `mode`: `acceptEdits`

Mark task `in_progress` before spawn. Mark `completed` after.

**R1 Turn A prompt:**

```
You are writing the OPENING ANALYSIS for a 2-agent iterative workshop on the {{PROJECT_NAME}} project.

## Source Documents (read ALL of these FIRST)
{numbered list of source doc paths}

Also read your agent memory: `.claude/agent-memory/{your-type}/MEMORY.md`

{If --context:}
## Focus Topics
{context text}

## Your Task

Read all source documents, then FILL IN your sections in: `{output_path}`

The file has a pre-built skeleton with `*[NOT STARTED]*` placeholders. Use the Edit tool to replace each placeholder in the "Round 1 — {agent-a-short}" section with your analysis. Do NOT overwrite the header, other sections, or the Round 2 skeleton.

For each labeled section ({A-initial}1, {A-initial}2, ...):
- State your key finding clearly
- Connect to your research papers (cite equations, paper numbers)
- Identify structural implications for the framework
- Pose specific questions for {agent-b-short}

## Rules
- REPLACE `*[NOT STARTED]*` placeholders in YOUR sections only.
- Ground in source docs and your research papers. Cite precisely.
- Label sections clearly — load-bearing for cross-reference.
- Use the project's framing vocabulary if a framing rule is installed by the selected discipline pack.
- Write ONLY to the workshop file.
```

**R2+ Turn A prompt:**

```
You are writing ROUND {r} FOLLOW-UP for a 2-agent workshop.

## Workshop Document (read FIRST — contains all prior rounds)
`{output_path}`

## Source Documents (reference)
{numbered list}

## Your Task

Read the full workshop document, then FILL IN the Round {r} — {agent-a-short} placeholders:

### CONVERGENCE — Where you now agree with {agent-b-short}. State what changed.
### DISSENT — Where you still disagree. New evidence only; don't restate.
### EMERGENCE — New insights from cross-pollination.
### QUESTIONS — Sharper follow-ups. Answer {agent-b-short}'s questions to you.

## Rules
- REPLACE placeholders in YOUR Round {r} sections only.
- Reference {agent-b-short}'s sections by label.
- Project-specific framing (if a framing rule is installed by the discipline pack).
- Write ONLY to the workshop file.
```

**Wait for Agent A to complete before Turn B.**

#### Turn B: Agent B

Spawn background agent:
- `subagent_type`: second agent from `--agents`
- `run_in_background`: true
- `name`: `workshop-{agent-b-short}-r{r}`
- `mode`: `acceptEdits`

**R1 Turn B prompt:**

```
You are writing the RESPONSE for a 2-agent iterative workshop.

## Source Documents (read ALL FIRST)
{numbered list}

## Workshop Document (read AFTER sources)
`{output_path}`

This file contains the header and {agent-a-short}'s opening analysis with labeled sections.

Also read your agent memory: `.claude/agent-memory/{your-type}/MEMORY.md`

## Your Task

Read all source documents AND the workshop document, then FILL IN your sections.

### Part 1: Response to {agent-a-short}'s Sections

For EACH "Re:" placeholder, replace `*[NOT STARTED]*` with:
- **AGREE**: Why, plus your domain's supporting evidence
- **DISAGREE**: Why, with counter-evidence from your papers
- **MISSED**: What your domain reveals that theirs doesn't
- **EMERGES**: Cross-domain insights from combining perspectives

### Part 2: Original Analysis

Fill in your labeled sections ({B-initial}1, {B-initial}2, ...) with findings {agent-a-short} did not address.

## Rules
- REPLACE placeholders in YOUR sections only.
- Reference {agent-a-short}'s sections by label.
- Project-specific framing (if a framing rule is installed by the discipline pack).
- Write ONLY to the workshop file.
```

**R2+ Turn B prompt:**

```
You are writing ROUND {r} RESPONSE for a 2-agent workshop.
{If final round: "This is the FINAL TURN — you must also fill the Workshop Verdict table."}

## Workshop Document (read FIRST)
`{output_path}`

## Source Documents (reference)
{numbered list}

## Your Task

Read the full workshop document, then FILL IN the Round {r} — {agent-b-short} placeholders:

### CONVERGENCE — Where you accept {agent-a-short}'s corrections.
### DISSENT — Sharpen, don't repeat.
### EMERGENCE — New cross-domain insights.

{FINAL ROUND ONLY — also fill:}

## Workshop Verdict — Replace the placeholder table. For each topic assign:
- **Converged**: Both agree after exchange
- **Dissent**: Disagreement persists
- **Partial**: Structure agreed, specifics disputed
- **Emerged**: New finding from exchange

## Remaining Open Questions — Numbered list. Each specific enough to become a computation or session topic. Include pre-registered gates.

## Wrap-Up — Workshop Impact Summary (MANDATORY)

Fill this section — it is the PRIMARY output for session planning:

### What Changed
{1-3 bullets: what this workshop CHANGED about the framework's state.}

### What Holds
{1-3 bullets: what SURVIVED the workshop exchange.}

### What Breaks or Strains
{1-3 bullets: what the workshop THREATENS or leaves unresolved. If nothing, "Nothing identified."}

### Carry-Forward Computations
{Numbered list — EVERY computation suggested across all rounds, deduplicated, with: what to compute, what data it needs, what gate it feeds, estimated effort.}

### Closing Line
{One sentence — the single most important thing from this workshop.}

## Rules
- REPLACE placeholders in YOUR sections only.
- Project-specific framing (if a framing rule is installed by the discipline pack).
- The Wrap-Up section is NON-NEGOTIABLE. Do not skip it.
- Write ONLY to the workshop file.
```

**Wait for Agent B. Proceed to next round automatically (pre-committed via `--rounds`).**

### Step 4: Inter-Round Status

After each complete round, report:

```
=== WORKSHOP ROUND {r}/{N} COMPLETE ===
{agent-a-short}: {line count}
{agent-b-short}: {line count}
Document: {output_path} ({total lines} lines)
```

Before launching Round 2+, **audit Round 1 for project-framing violations** if the discipline pack installed a framing rule. Include specific corrections in the Round 2 agent prompts. The canonical violations are defined by the framing rule itself; examples are typically: inverted causal directions, mis-attribution of cause to effect, imported vocabulary from a rejected paradigm, "analog of" language where the framework treats the object as fundamental rather than derived.

---

## Phase 3: Verify & Report

```
=== RCLAB-WORKSHOP COMPLETE ===
Rounds: {N} ({N*2} turns)
Agent A: {agent-a-short} ({type})
Agent B: {agent-b-short} ({type})
Convergence: {count} | Partial: {count} | Dissent: {count} | Emerged: {count}
Output: {path} ({lines} lines)
```

---

## Rules

1. **Never overwrite files** without user confirmation (collision check).
2. **Never execute computations** — this skill produces a workshop document only.
3. **Never re-adjudicate gate verdicts** — source doc verdicts are authoritative.
4. **Workshop skeleton is MANDATORY** — build ALL sections before ANY agent launches.
5. **Purely sequential** — never spawn B before A completes within a turn.
6. **Never initiate shutdown** — user decides.
7. **Project-specific framing** — audit and correct between rounds if a framing rule is installed.

## Error Handling

| Condition | Action |
|:----------|:-------|
| No source docs | Show usage and stop |
| Source doc missing | Report which, stop |
| No `--agents` | Show usage and stop |
| Agent type invalid | List available types, stop |
| Agents != 2 | Error: "rclab-workshop requires exactly 2 agents" |
| `--rounds` outside 1-5 | Error: "Rounds must be 1-5" |
| Output collision | Ask: overwrite / rename / cancel |
| Agent fails to produce output | Report, suggest different agent |
| Agent overwrites workshop file | Report corruption, offer restart from last good round |
