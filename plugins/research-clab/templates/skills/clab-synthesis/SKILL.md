---
name: clab-synthesis
description: Generate synthesis or fusion documents from source docs — solo agent, coordinated team, or iterative 2-agent workshop
argument-hint: <doc1> [doc2 ...] --agent <type> | --agents <type1,type2,...> [--writer <name>] [--output <path>] [--type solo|team|master|fusion|workshop] [--session <id>] [--rounds <N>] [--dry-run]
---

# Clab-Synthesis — Synthesis & Fusion Document Generator

Build synthesis documents from existing source documents. Three execution modes: **solo** (one agent reads everything and writes), **team** (2-3 specialists deliberate, designated writer synthesizes), or **workshop** (exactly 2 agents iterate on a single running document for N rounds). Five document types: **solo** (one agent synthesizes raw docs), **team** (multi-agent deliberation), **master** (rollup of sub-sessions within one session — e.g., 30Aa + 30Ab + 30Ba -> Session 30 master), **fusion** (synthesis of syntheses — source docs are themselves synthesis documents, producing cross-synthesis discoveries), **workshop** (iterative 2-agent cross-pollination with labeled sections, forced engagement, convergence/dissent tracking). Detects execution mode from `--agent` (singular) vs `--agents` (plural). Detects document type from context or `--type` override.

## Usage

```
# Solo: one agent writes synthesis from source docs
/clab-synthesis sessions/session-30/session-30Aa-synthesis.md sessions/session-30/session-30Ba-synthesis.md --agent skeptic --output sessions/session-30/session-30-master-synthesis.md

# Solo: verdict on raw computation output
/clab-synthesis sessions/session-31/session-31a-synthesis.md computation/s31a_gate_verdicts.txt --agent skeptic --type solo

# Master: roll up sub-sessions into one session-level document
/clab-synthesis sessions/session-30/session-30Aa-synthesis.md sessions/session-30/session-30Ab-synthesis.md sessions/session-30/session-30Ba-synthesis.md --agent workhorse --type master

# Fusion: synthesis-of-syntheses — source docs are themselves syntheses
/clab-synthesis sessions/session-29/session-29-team-A-synthesis.md sessions/session-29/session-29-team-B-synthesis.md sessions/session-29/session-29-team-C-synthesis.md --agents skeptic,calculator,workhorse --writer calculator --type fusion

# Team: 2 experts + coordinator build team synthesis
/clab-synthesis sessions/session-31/session-31a-synthesis.md sessions/session-31/session-31b-synthesis.md --agents workhorse,dreamer

# Workshop: 2 agents iterate on a shared document (default 2 rounds)
/clab-synthesis sessions/session-34/session-34-synthesis.md --agents workhorse,dreamer --type workshop

# Workshop: 3 rounds with explicit output path
/clab-synthesis sessions/session-34/session-34-collab-A.md sessions/session-34/session-34-collab-B.md --agents skeptic,calculator --type workshop --rounds 3 --output sessions/session-34/session-34-skeptic-calc-workshop.md

# Dry run: show what would happen
/clab-synthesis doc1.md doc2.md --agent skeptic --dry-run
```

---

## Phase 0: Parse & Validate

### 0a. Extract Arguments

Parse `$ARGUMENTS` for:

| Arg | Required | Default | Description |
|:----|:---------|:--------|:------------|
| `<doc1> [doc2 ...]` | YES (at least 1) | — | Source document paths (positional, before any flags) |
| `--agent <type>` | ONE OF | — | Single agent type -> **solo mode** |
| `--agents <t1,t2,...>` | THESE TWO | — | Comma-separated agent types -> **team or workshop mode** |
| `--writer <name>` | no | see defaults | Who writes the final document (not used in workshop) |
| `--output <path>` | no | auto-detect | Output file path |
| `--type <type>` | no | auto-detect | Document format: `solo`, `team`, `master`, `fusion`, `workshop` |
| `--session <id>` | no | auto-detect | Session identifier (e.g., `29`, `30Ba`) |
| `--rounds <N>` | no | 2 | Number of iteration rounds (**workshop only**) |
| `--dry-run` | no | false | Show plan without spawning |

### 0b. Mode Detection

- `--agent` present -> **solo mode**
- `--agents` present + `--type workshop` -> **workshop mode**
- `--agents` present (no workshop type) -> **team mode**
- Both `--agent` AND `--agents` present -> error: "Use --agent (solo) OR --agents (team/workshop), not both."
- Neither present -> error: show usage.

### 0c. Validate Source Documents

Read 1 line of each source document to verify it exists. If any missing, report which and stop.

### 0d. Validate Agent Types

Check that all agent types exist in `.claude/agents/`. See `.claude/templates/agent-roster.md` for the canonical list. If invalid, list available types and stop.

### 0e. Defaults

**Writer defaults:**
- Solo mode: the single agent writes the output (no separate writer needed)
- Team mode: `coordinator` if present in `--agents`, otherwise the FIRST agent listed
- Workshop mode: no designated writer — both agents write to the same document sequentially

**Type defaults:**
- Solo execution + raw docs (gate verdicts, computation output, minutes): `solo`
- Solo execution + sub-session syntheses as input: `master`
- Team execution with 2 agents: `team`
- Team execution with 3+ agents OR source docs are themselves syntheses: `fusion`
- `--type workshop` explicitly set: `workshop`
- Override with `--type` always respected

**Type selection heuristic** (when `--type` not provided):
1. If `--type workshop` is explicitly set -> `workshop`
2. If ALL source docs match `*-synthesis.md` or `*-synth.md` -> default `fusion` (synthesis-of-syntheses)
3. If source docs are from the SAME session number (e.g., all `session-30*`) and execution is solo -> default `master` (sub-session rollup)
4. If team execution -> default `team` (2 agents) or `fusion` (3 agents)
5. Otherwise -> default `solo`

**NOTE**: Workshop mode is NEVER auto-detected — it must be explicitly requested via `--type workshop`. This prevents accidental workshop launches when team mode was intended.

**Output path default** (if `--output` not provided):
1. If `--session` provided: `sessions/session-{N}/session-{session-id}-{type-suffix}.md`
   - `solo` -> `-synthesis.md`
   - `team` -> `-team-synthesis.md`
   - `master` -> `-master-synthesis.md` (rolls up sub-sessions within one session)
   - `fusion` -> `-fusion-synthesis.md` (synthesis of syntheses)
   - `workshop` -> `-{agentA-short}-{agentB-short}-workshop.md`
2. If no `--session`: attempt to extract session from first source doc filename (regex: `session-(\d+\w*)`). If found, use that session folder.
3. If neither works: ask the user for the output path.

**Session ID default** (if `--session` not provided):
- Extract from first source doc filename. If ambiguous or not found, ask.

**Rounds default** (if `--rounds` not provided):
- Workshop mode: 2 rounds
- Non-workshop modes: `--rounds` is ignored with a warning if provided

### 0f. Mode-Specific Constraints

**Team mode:**
- Max 3 agents (project mandate). If more provided, warn and stop.
- If `coordinator` is not in the `--agents` list, add it automatically and inform the user.
- If `--writer` names an agent not in `--agents`, error and stop.

**Workshop mode:**
- EXACTLY 2 agents required. If more or fewer provided, error: "Workshop mode requires exactly 2 agents. Got {N}."
- No coordinator added — workshop is a direct 2-agent exchange with no mediator.
- `--writer` is ignored with a warning if provided (both agents write to the same document).
- `--rounds` must be >= 1 and <= 5. Default: 2.

---

## Phase 1: Collision Check

If the output file already exists, use AskUserQuestion:
- "Output file already exists at {path}. Overwrite / Choose new name / Cancel?"

---

## Phase 2: Dry Run (if `--dry-run`)

Display plan and stop. Format varies by type:

**Solo/Master/Fusion/Team:**
```
=== CLAB-SYNTHESIS DRY RUN ===

Mode: {solo|team}
Type: {solo|team|master|fusion}
       solo   = one agent synthesizes raw docs
       team   = multi-agent deliberation
       master = rollup of sub-sessions within one session
       fusion = synthesis of syntheses (source docs are themselves syntheses)
Session: {id}

Source Documents ({N}):
  1. {path} ({lines} lines)
  2. {path} ({lines} lines)
  ...

Agent(s): {list with types}
Writer: {name}
Output: {path}

Ready to {spawn agent | create team}. Run without --dry-run to proceed.
```

**Workshop:**
```
=== CLAB-SYNTHESIS DRY RUN (WORKSHOP) ===

Type: workshop (iterative 2-agent cross-pollination)
Session: {id}
Rounds: {N} ({N*2} total turns)

Source Documents ({N}):
  1. {path} ({lines} lines)
  2. {path} ({lines} lines)
  ...

Agent A: {short-name-A} ({agent-type-A}) — opens each round
Agent B: {short-name-B} ({agent-type-B}) — responds each round

Execution Plan:
  R1-A: {short-name-A} reads sources, writes opening analysis
  R1-B: {short-name-B} reads sources + R1-A, writes response & cross-synthesis
  R2-A: {short-name-A} reads R1-A + R1-B, writes follow-up (convergence/dissent)
  R2-B: {short-name-B} reads all, writes convergence summary + verdict table
  ...

Infrastructure: NONE (no TeamCreate, no inbox, pure sequential Agent calls)
Output: {path}

Ready to begin workshop. Run without --dry-run to proceed.
```

---

## Phase 3: Execute (branches by mode)

### SOLO MODE

Spawn a **single background agent** (NOT a team) using the Agent tool:

- `subagent_type`: from `--agent`
- `run_in_background`: true
- `name`: `synthesis-writer`
- `mode`: `"acceptEdits"` — synthesis agents write output files, should not be permission-blocked
- Effort/depth by type: solo -> `effort: 3`, master -> `effort: 4`

**Solo Agent Prompt** (varies by `--type`):

#### Type: `solo`

```
You are writing a **session synthesis** from raw source documents. Your source documents are computation output, gate verdicts, meeting minutes, or other primary materials — NOT other syntheses.

## Your Task

Read all source documents, then write a synthesis to: `{output_path}`

## Source Documents (read ALL of these FIRST)
{numbered list of all source doc paths}

## Document Structure

Follow the template in `.claude/templates/synthesis.md`.

## Rules
- Gate verdicts from source docs are authoritative — do not re-adjudicate.
- If sources conflict, flag the conflict explicitly.
- Write ONLY the output file. Nothing else.
```

#### Type: `master`

```
You are writing a **master synthesis** — a rollup of all sub-sessions within a single session number. Your source documents are sub-session syntheses (e.g., 30Aa, 30Ab, 30Ba) and you integrate them into one definitive session-level document (e.g., "Session 30 Master Synthesis"). This is a synthesis of sub-sessions, organized by importance not chronology.

## Your Task

Read all source documents, then write a master synthesis to: `{output_path}`

## Source Documents (read ALL of these FIRST)
{numbered list of all source doc paths}

## Document Structure

Follow the template in `.claude/templates/synthesis-master.md`. Key structural note: organize by IMPORTANCE not chronology. The Executive Summary should let a reader understand the full session arc standalone.

---

### WORKSHOP MODE (Iterative 2-Agent Cross-Pollination)

Workshop mode spawns exactly 2 agents **sequentially** — NO team infrastructure. Each agent runs as a background Agent call, reads the running document, appends their contribution, and completes before the next agent spawns. This loops for `--rounds` rounds (default: 2), producing `rounds * 2` total turns.

**Why no team infrastructure**: The 2-Agent Workshop Pattern eliminates every team management bug: no inbox routing, no notification avalanche, no shutdown resistance, no stale teams. Pure sequential Agent calls with placeholder-replacement writes to a single document.

**Short name mapping**: Read `.claude/templates/agent-roster.md` for the canonical name-to-type mapping.

#### Phase 3W-1: Build Full Document Skeleton

**MANDATORY.** Build the COMPLETE workshop skeleton BEFORE launching any agent. Use `.claude/templates/workshop.md` as the structural reference. The skeleton must include:

- Header (date, format, agents, source docs, focus topics)
- ALL round headings for ALL rounds
- ALL turn sections with `*[NOT STARTED]*` placeholders
- Agent A's labeled topic sections (one per focus topic + cross-cutting)
- Agent B's response sections (Re: each of A's sections + original analysis + questions)
- Round 2+ CONVERGENCE / DISSENT / EMERGENCE / QUESTIONS sections
- Workshop Verdict table shell (final round)
- Remaining Open Questions placeholder

Write this skeleton with the Write tool in a single call. Agents fill placeholders using Edit -- they never create structure.

#### Phase 3W-1.5: Create Task Tracking

Even though workshop mode uses no team infrastructure, create tasks for progress visibility:

```
For each round r and turn (A, B):
  TaskCreate: "R{r}-A: {agent-a-short} analysis" (blockedBy: previous turn's task ID)
  TaskCreate: "R{r}-B: {agent-b-short} response" (blockedBy: R{r}-A task ID)
```

This gives the user a dashboard of workshop progress and ensures proper sequencing.

#### Phase 3W-2: Round Loop

For each round `r` from 1 to `--rounds`:

##### Turn A: Agent A Opens / Follows Up

Spawn Agent A as a background agent using the Agent tool:
- `subagent_type`: first agent from `--agents`
- `run_in_background`: true
- `name`: `workshop-{agent-a-short}-r{r}`
- `mode`: `"acceptEdits"` — workshop agents only append to the shared document
- `effort`: `"thorough"` for workshop depth
- `maxTurns`: R1 Turn A -> 15, R2+ Turn A -> 12

Mark the corresponding task as `in_progress` via TaskUpdate before spawning. Mark it `completed` after the agent finishes.

**Round 1 Turn A Prompt:**

```
You are writing the OPENING ANALYSIS for a 2-agent iterative workshop.

## Source Documents (read ALL of these FIRST)
{numbered list of all source doc paths}

Also read your agent memory: `.claude/agent-memory/{your-type}/MEMORY.md`

{If --context provided:}
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
- Write ONLY to the workshop file.
```

**Round 2+ Turn A Prompt:**

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
- Write ONLY to the workshop file.
```

**Wait for Agent A to complete before proceeding to Turn B.**

##### Turn B: Agent B Responds / Synthesizes

Spawn Agent B as a background agent:
- `subagent_type`: second agent from `--agents`
- `run_in_background`: true
- `name`: `workshop-{agent-b-short}-r{r}`
- `mode`: `"acceptEdits"`
- `effort`: `"thorough"`
- `maxTurns`: R1 Turn B -> 20, R2+ Turn B -> 15

**Round 1 Turn B Prompt:**

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
- Write ONLY to the workshop file.
```

**Round 2+ Turn B Prompt:**

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

## Rules
- REPLACE placeholders in YOUR sections only.
- Write ONLY to the workshop file.
```

**Wait for Agent B. Proceed to next round automatically (pre-committed via `--rounds`).**

#### Phase 3W-3: Inter-Round Status

After each complete round, report:

```
=== WORKSHOP ROUND {r}/{N} COMPLETE ===
{agent-a-short}: {line count}
{agent-b-short}: {line count}
Document: {output_path} ({total lines} lines)
```

Before launching Round 2+, **audit Round 1 for methodology violations**. Include specific corrections in the Round 2 agent prompts. Common violations:
- Using deprecated or incorrect framing from other paradigms
- Explaining domain results through an external rather than native framework
- "Analog of" language when the domain framework is fundamental
- Non-domain vocabulary for domain-specific concepts

---

### TEAM MODE

Team mode uses the blast-first workflow from project rules. The procedure mirrors `/clab-team` panel mode with synthesis-specific templates.

#### Phase 3T-0: Pre-Flight

1. Check `~/.claude/teams/` for stale teams. Report and clean up if found.
2. Verify no active team in this session.

#### Phase 3T-1: Create Team

**TeamCreate** with name: `synthesis-{session-id}` (or `synthesis-{timestamp}` if no session ID).

#### Phase 3T-2: Create Tasks

**For `team` type** (2-3 agents):
- One task per specialist: "Analyze source documents from {domain} perspective, send key findings and assessment to {writer-name}."
- One writer task: "Synthesize specialist perspectives into {output_path}."

**For `fusion` type** (3 agents, multi-round — source docs are themselves syntheses):
- One task per specialist: "Read all source syntheses. Round 1: Identify cross-synthesis patterns your domain uniquely reveals. Round 2: Respond to other specialists' cross-synthesis insights. Round 3: Send final assessment to {writer-name}."
- One writer task: "Collect all specialist inputs across rounds. Write fusion synthesis (synthesis-of-syntheses) to {output_path}. Focus on XS-N cross-synthesis discoveries — findings visible ONLY when comparing source syntheses."

#### Phase 3T-3: Spawn Agents (Blast-First)

Execute the blast-first protocol from team-lead-behavior.md. Spawn all agents with the minimal hard-stop prompt:

```
You are a teammate on team "{team-name}". Your name is "{short-name}".
Send a ready message to "team-lead" using SendMessage, then wait for instructions.
```

**Short name mapping**: Read `.claude/templates/agent-roster.md` for the canonical name-to-type mapping.

Spawn ALL in parallel. Wait for ALL to send "ready". Max 3 agents.

#### Phase 3T-4: Roster Blast

Execute `/team-blast --list`. Fallback: manual roster via SendMessage to each agent.

#### Phase 3T-5: Assign Work

After roster blast, send each agent their full assignment via SendMessage.

**Specialist agents** (non-writers):

```
## Your Assignment: {session-id} Synthesis

### Required Reading (MANDATORY, FULL — do these FIRST)
{numbered list of ALL source documents}

### Your Role
Analyze the source documents through YOUR specialist lens. Identify:
- What your domain reveals that generalists miss
- Connections to your research papers (cite specific equations/results)
- Where you agree/disagree with other specialists
- Structural implications for the framework

### Communication
- Send your analysis to {writer-name} via SendMessage.
- Message other specialists for cross-pollination (use NAMES: {name list}).
- {For fusion type: "This is a multi-round deliberation. Round 1: send initial insights. Round 2: respond to others' insights. Round 3: send final assessment."}

### Rules
- Ground in YOUR research papers and the SOURCE DOCUMENTS. Do not invent.
- Be specific: cite equation numbers, gate IDs, computation results.
- Check inbox between sections of analysis.
- When done: TaskUpdate completed + final assessment to {writer-name}.
```

**Designated writer**:

```
## Your Assignment: {session-id} Synthesis Writer

### Required Reading
{numbered list of ALL source documents}

### Your Role: Synthesis Writer
Collect specialist perspectives. Write the synthesis document.

### Output
Write to: `{output_path}`

For `team` type: read and follow `.claude/templates/synthesis-team.md`
For `fusion` type: read and follow `.claude/templates/synthesis-fusion.md`

### Rules
- YOU are the only agent who writes the output file.
- Wait for specialist inputs before writing — do not front-run.
- Capture convergent AND divergent views.
- Attribute insights to their source specialist.
- When done: TaskUpdate completed + send summary to team-lead.
```

Use **TaskUpdate** to set `owner` on each task.

#### Phase 3T-6: Hands Off

Same rules as `/clab-team`:

1. Do NOT send follow-up messages unless an agent explicitly asks for help.
2. Do NOT write the output file — the writer agent does.
3. Do NOT mark agent tasks completed — they mark their own.
4. Do NOT nudge idle agents.
5. Do NOT initiate shutdown — only the USER decides.

**What you MAY do:**
- Respond to agent questions.
- Relay completion summaries to the user.
- If agents disagree on a factual matter in the source docs, send ONE resolution to BOTH.

---

## Phase 4: Verify & Report

### Solo Mode

When the agent completes:

1. Verify output file exists
2. Read it, extract line count
3. Check it contains the mandatory sections for its type

```
=== CLAB-SYNTHESIS COMPLETE ===

Mode: solo
Type: {type}
Agent: {agent-type}

Output: {path} ({lines} lines)
Source documents: {N}
```

### Workshop Mode

When all rounds complete:

1. Read the final document
2. Count total lines and per-agent contributions
3. Verify the document contains all expected round headings
4. If final round: verify Workshop Verdict table exists

```
=== CLAB-SYNTHESIS COMPLETE (WORKSHOP) ===

Type: workshop
Rounds: {N} ({N*2} turns)
Agent A: {agent-a-short} ({agent-a-type})
Agent B: {agent-b-short} ({agent-b-type})

Per-Agent Contributions:
  {agent-a-short}: {N} sections across {N} rounds
  {agent-b-short}: {N} sections across {N} rounds

Convergence Summary:
  Converged: {count from verdict table}
  Dissent:   {count}
  Partial:   {count}
  Emerged:   {count}

Output: {path} ({lines} lines)
Source documents: {N}
```

### Team Mode

When the writer reports synthesis complete:

```
=== CLAB-SYNTHESIS COMPLETE ===

Mode: team
Type: {type}
Team: {team-name} ({N} agents)

Agents:
  {name} .... analysis delivered
  {writer} .. synthesis written

Output: {path} ({lines} lines)
Source documents: {N}
```

**Do NOT initiate shutdown after reporting.** The user decides.

---

## Safety Rules

1. **Never overwrite existing files** without user confirmation (Phase 1 collision check).
2. **Never execute computations** — synthesis documents only.
3. **Never modify MEMORY.md**, agent memory, or the knowledge index. Read only.
4. **Never re-adjudicate gate verdicts** — source doc verdicts are authoritative.
5. **Solo mode: never spawn teams.** Team mode: max 3 agents. **Workshop mode: exactly 2 agents, no team infrastructure.**
6. **Workshop skeleton is MANDATORY** -- build ALL sections before ANY agent launches.
7. **Always include coordinator in team mode** if not already in `--agents`. **Do NOT add coordinator in workshop mode.**
8. **Never initiate shutdown** — user decides. (Exception: none. This is non-negotiable.)
9. **Team mode follows blast-first workflow** — no exceptions.
10. **Workshop mode is purely sequential** — never spawn Agent B before Agent A completes within a turn. Never spawn the next round before the current round completes.
11. **Workshop skeleton is written by team lead** — agents only REPLACE placeholders via Edit. If an agent overwrites the file structure, the workshop is corrupted.

## Error Handling

| Condition | Action |
|:----------|:-------|
| No source docs provided | Show usage block and stop |
| Source doc missing | Report which file(s) not found and stop |
| Neither `--agent` nor `--agents` | Show usage block and stop |
| Both `--agent` AND `--agents` | Error: "Use one or the other, not both" |
| Agent type invalid | List available types and stop |
| `--agents` has > 3 types (non-workshop) | Warn: max 3 agents per project rules. Stop |
| `--agents` != 2 types (workshop) | Error: "Workshop requires exactly 2 agents. Got {N}." |
| `--writer` not in `--agents` list | Error: writer must be a team member |
| `--writer` used with workshop | Warn: "--writer ignored in workshop mode (both agents write)" |
| `--rounds` used without workshop | Warn: "--rounds only applies to workshop mode. Ignored." |
| `--rounds` < 1 or > 5 | Error: "Rounds must be 1-5. Got {N}." |
| Output collision | AskUserQuestion: overwrite / new name / cancel |
| Agent fails to produce output | Report failure, suggest different agent type |
| Workshop agent overwrites file | Report corruption, offer to restart from last good round |
| Writer doesn't receive specialist input | After 5 min, report stall to user |
| Stale teams found | Report and offer cleanup before proceeding |
