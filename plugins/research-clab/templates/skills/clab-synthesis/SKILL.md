---
name: clab-synthesis
description: Generate synthesis or fusion documents from source docs — solo agent or coordinated team
argument-hint: <doc1> [doc2 ...] --agent <type> | --agents <type1,type2,...> [--writer <name>] [--output <path>] [--type solo|team|master|fusion] [--session <id>] [--dry-run]
---

# Clab-Synthesis — Synthesis & Fusion Document Generator

Build synthesis documents from existing source documents. Two execution modes: **solo** (one agent reads everything and writes) or **team** (2-3 specialists deliberate, designated writer synthesizes). Four document types: **solo** (one agent synthesizes raw docs), **team** (multi-agent deliberation), **master** (rollup of sub-sessions within one session — e.g., 30Aa + 30Ab + 30Ba → Session 30 master), **fusion** (synthesis of syntheses — source docs are themselves synthesis documents, producing cross-synthesis discoveries). Detects execution mode from `--agent` (singular) vs `--agents` (plural). Detects document type from context or `--type` override.

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
| `--agent <type>` | ONE OF | — | Single agent type → **solo mode** |
| `--agents <t1,t2,...>` | THESE TWO | — | Comma-separated agent types → **team mode** |
| `--writer <name>` | no | see defaults | Who writes the final document |
| `--output <path>` | no | auto-detect | Output file path |
| `--type <type>` | no | auto-detect | Document format: `solo`, `team`, `master`, `fusion` (see descriptions above) |
| `--session <id>` | no | auto-detect | Session identifier (e.g., `29`, `30Ba`) |
| `--dry-run` | no | false | Show plan without spawning |

### 0b. Mode Detection

- `--agent` present → **solo mode**
- `--agents` present → **team mode**
- Both present → error: "Use --agent (solo) OR --agents (team), not both."
- Neither present → error: show usage.

### 0c. Validate Source Documents

Read 1 line of each source document to verify it exists. If any missing, report which and stop.

### 0d. Validate Agent Types

Discover valid agent types dynamically from `.claude/agents/`:

```bash
ls .claude/agents/*.md | sed 's|.claude/agents/||;s|\.md$||'
```

Check that ALL specified agent types (from `--agent` or `--agents`) exist as `.claude/agents/{type}.md`. If invalid, list available types and stop.

### 0e. Defaults

**Writer defaults:**
- Solo mode: the single agent writes the output (no separate writer needed)
- Team mode: `coordinator` if present in `--agents`, otherwise the FIRST agent listed

**Type defaults:**
- Solo execution + raw docs (gate verdicts, computation output, minutes): `solo`
- Solo execution + sub-session syntheses as input: `master`
- Team execution with 2 agents: `team`
- Team execution with 3+ agents OR source docs are themselves syntheses: `fusion`
- Override with `--type` always respected

**Type selection heuristic** (when `--type` not provided):
1. If ALL source docs match `*-synthesis.md` or `*-synth.md` → default `fusion` (synthesis-of-syntheses)
2. If source docs are from the SAME session number (e.g., all `session-30*`) and execution is solo → default `master` (sub-session rollup)
3. If team execution → default `team` (2 agents) or `fusion` (3 agents)
4. Otherwise → default `solo`

**Output path default** (if `--output` not provided):
1. If `--session` provided: `sessions/session-{N}/session-{session-id}-{type-suffix}.md`
   - `solo` → `-synthesis.md`
   - `team` → `-team-synthesis.md`
   - `master` → `-master-synthesis.md` (rolls up sub-sessions within one session)
   - `fusion` → `-fusion-synthesis.md` (synthesis of syntheses)
2. If no `--session`: attempt to extract session from first source doc filename (regex: `session-(\d+\w*)`). If found, use that session folder.
3. If neither works: ask the user for the output path.

**Session ID default** (if `--session` not provided):
- Extract from first source doc filename. If ambiguous or not found, ask.

### 0f. Team Mode Constraints

- Max 3 agents (project mandate). If more provided, warn and stop.
- If `coordinator` is not in the `--agents` list, add it automatically and inform the user.
- If `--writer` names an agent not in `--agents`, error and stop.

---

## Phase 1: Collision Check

If the output file already exists, use AskUserQuestion:
- "Output file already exists at {path}. Overwrite / Choose new name / Cancel?"

---

## Phase 2: Dry Run (if `--dry-run`)

Display plan and stop:

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

---

## Phase 3: Execute (branches by mode)

### SOLO MODE

Spawn a **single background agent** (NOT a team) using the Agent tool:

- `subagent_type`: from `--agent`
- `run_in_background`: true
- `name`: `synthesis-writer`

**Solo Agent Prompt** (varies by `--type`):

#### Type: `solo`

```
You are writing a **session synthesis** from raw source documents. Your source documents are computation output, gate verdicts, meeting minutes, or other primary materials — NOT other syntheses.

## Your Task

Read all source documents, then write a synthesis to: `{output_path}`

## Source Documents (read ALL of these FIRST)
{numbered list of all source doc paths}

## Also Read
- Your agent memory: `.claude/agent-memory/{your-type}/MEMORY.md` (if it exists)

## Document Structure (follow this format)

```markdown
# Session {session-id} Synthesis: {Title — derive from source content}

**Date**: {today}
**Session type**: SYNTHESIS
**Agents**: {your agent type} (solo synthesis)
**Source documents**: {list}

---

## I. Session Outcome

{2-3 sentence verdict. Lead with the most consequential result. State whether gates passed or failed.}

---

## II. Gate Verdicts (Summary)

{If source docs contain gate verdicts, tabulate them:}

| Gate | Type | Verdict | Decisive Number |
|:-----|:-----|:--------|:----------------|

{If no gates in source docs, replace with "## II. Key Results" and summarize findings.}

---

## III. Computation Results

{For each computation or major finding in the source docs, one subsection:}

### {Result Title}

**Result**: {the number, then the classification}

{2-3 paragraphs: what was computed, what it means, structural implications}

---

## IV. Structural Implications

{What these results mean for the framework. Update constraint map if applicable. Identify what opened, what closed, what shifted.}

---

## V. Forward Projection

{What should happen next. Specific computations. Which gates are now decisive. What the results enable or block.}
```

## Rules
- Ground in the SOURCE DOCUMENTS. Do not invent results not in the sources.
- Report numbers first. Classify second. Interpret third.
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

## Also Read
- Your agent memory: `.claude/agent-memory/{your-type}/MEMORY.md` (if it exists)

## Document Structure

```markdown
# Session {session-id} Master Synthesis: {Title}

**Date**: {today}
**Sub-sessions rolled up**: {list of sub-sessions, e.g., 30Aa, 30Ab, 30Ba, 30Bb}
**Agents**: {from each sub-session}
**Document type**: Definitive standalone session record — all sub-session results integrated by importance, not chronology

---

## Executive Summary

{3-5 paragraphs. The reader should be able to understand the entire session arc from this section alone. State: what was attempted, what was found, what it means, what's next.}

---

## I. Results Hierarchy

{Organize ALL results from ALL sub-sessions by importance, not chronology:}

### Tier 1: Framework-Decisive Results
{Results that change the framework's status, probability, or direction}

### Tier 2: Structural Results
{Permanent mathematical results, theorems, proven identities}

### Tier 3: Diagnostic Results
{Useful numbers that inform future sessions but don't independently change status}

---

## II. Gate Verdicts (Complete)

| Gate | Sub-Session | Type | Verdict | Decisive Number |
|:-----|:-----------|:-----|:--------|:----------------|

---

## III. Constraint Map Update

{What opened, what closed, what shifted. Reference specific gate IDs.}

---

## IV. Cross-Sub-Session Discoveries

{Insights visible ONLY when sub-session results are compared against each other. Emergent patterns, unexpected connections between sub-sessions that no individual sub-session synthesis captures alone.}

---

## V. Forward Projection

{Priority-ordered next steps. Specific computations. Which new gates are now defined.}
```

## Rules
- This is a DEFINITIVE STANDALONE RECORD for one session number. A reader with no prior context should understand the full session arc from sub-session A through the last sub-session.
- Organize by IMPORTANCE, not chronology. A reader should hit the most consequential result first.
- Cross-sub-session discoveries (Section IV) are your highest-value contribution — patterns no individual sub-session synthesis captures.
- Write ONLY the output file. Nothing else.
```

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

Spawn ALL agents with the hard-stop prompt (identical to clab-team):

```
You are a teammate on team "{team-name}". Your name is "{short-name}".

YOUR ONLY ACTION RIGHT NOW: Send a message to "team-lead" saying "ready" using SendMessage. Then STOP. Do absolutely nothing else.

DO NOT:
- Read any files
- Check TaskList
- Read your agent memory
- Read team config
- Start any work

JUST send the ready message and go idle. You will receive a roster blast and your full assignment AFTER all agents have checked in.
```

**Short name derivation**: Use the agent definition filename without `.md`. If the name contains hyphens, use the first segment as the short name unless it's ambiguous (e.g., `boundary-guard` → `boundary-guard`, `coordinator` → `coordinator`). For agents with persona-based names, use the full slug.

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

Also read:
- Your agent memory: `.claude/agent-memory/{your-type}/MEMORY.md`

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

{INCLUDE THE FULL DOCUMENT STRUCTURE TEMPLATE HERE — use the appropriate template based on --type:}

{For `team` type: use Team Synthesis Template (below)}
{For `fusion` type: use Fusion Synthesis Template (below)}

### Rules
- YOU are the only agent who writes the output file.
- Wait for specialist inputs before writing — do not front-run.
- Capture convergent AND divergent views.
- Attribute insights to their source specialist.
- When done: TaskUpdate completed + send summary to team-lead.
```

**Team Synthesis Template** (for `team` type):

```markdown
# {Title} Team Synthesis: {Subtitle}

**Team**: {agent names and types}
**Designated Writer**: {writer name}
**Date**: {today}
**Re**: {session-id} Results
**Source Documents**: {list}

---

## I. Executive Summary
{2-3 paragraphs: what the team found, where they converge, where they diverge}

---

## II. Convergent Themes
{Themes that multiple specialists agree on. State convergence count.}

### Theme 1: {Title} ({N}/{total} {Unanimous/Majority})
- **{Agent1}**: {their perspective}
- **{Agent2}**: {their perspective}
**Synthesis**: {integrated assessment}

---

## III. Divergent Assessments
{Where specialists disagree. State each side's reasoning.}

---

## IV. Cross-Pollination Discoveries
{Ideas that emerged from discussion — present in the exchange but not in any individual source doc.}

---

## V. Forward Projection
{Priority-ordered next steps synthesized from all specialist inputs.}
```

**Fusion Synthesis Template** (for `fusion` type — synthesis of syntheses):

```markdown
# Session {session-id} Fusion Synthesis

## Synthesis of Syntheses: Cross-Document Deliberation

**Date**: {today}
**Fusion Team**: {agent names and types}
**Designated Writer**: {writer name}
**Method**: {N} rounds of structured cross-synthesis deliberation
**Source Syntheses**: {list — these are themselves synthesis documents, not raw data}
**Fusion Purpose**: Extract patterns, connections, and discoveries visible ONLY when comparing source syntheses against each other

---

## I. The Central Structural Insight
{The ONE deepest finding that emerges from cross-synthesis. 2-3 paragraphs.}

---

## II. Cross-Synthesis Discoveries
{Findings visible ONLY when all source docs are compared. Label each:}

### XS-1. {Discovery Title}
{Description. Attribution: which specialists identified which aspects.}

---

## III. Results Hierarchy

### Tier 1: Framework-Decisive
{Results that change status or direction}

### Tier 2: Structural / Permanent
{Mathematical results surviving any future closure}

### Tier 3: Diagnostic / Informational
{Useful context for future sessions}

---

## IV. Constraint Map Update
{What opened, closed, shifted. Full gate verdict table if applicable.}

---

## V. Forward Projection
{Priority-ordered next computations/sessions. Include specific gate definitions.}

---

## VI. Attribution Index
{Who contributed what. Specialist → their key insight.}
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
5. **Solo mode: never spawn teams.** Team mode: max 3 agents.
6. **Always include coordinator in team mode** if not already in `--agents`.
7. **Never initiate shutdown** — user decides. (Exception: none. This is non-negotiable.)
8. **Team mode follows blast-first workflow** — no exceptions.

## Error Handling

| Condition | Action |
|:----------|:-------|
| No source docs provided | Show usage block and stop |
| Source doc missing | Report which file(s) not found and stop |
| Neither `--agent` nor `--agents` | Show usage block and stop |
| Both `--agent` AND `--agents` | Error: "Use one or the other, not both" |
| Agent type invalid | List available types and stop |
| `--agents` has > 3 types | Warn: max 3 agents per project rules. Stop |
| `--writer` not in `--agents` list | Error: writer must be a team member |
| Output collision | AskUserQuestion: overwrite / new name / cancel |
| Agent fails to produce output | Report failure, suggest different agent type |
| Writer doesn't receive specialist input | After 5 min, report stall to user |
| Stale teams found | Report and offer cleanup before proceeding |
