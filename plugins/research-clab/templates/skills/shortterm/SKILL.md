---
name: shortterm
description: Collapse and optimize agent memory files — deduplicate, compress, archive to docs
argument-hint: [agent-name]
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash, Task, TeamCreate, TaskCreate, TaskUpdate, TaskList, TaskGet, SendMessage]
---

# Memory Collapse Skill (Team Orchestration)

Two-agent team: the **specialist** (whose memory is being collapsed) classifies what matters AND executes all file edits. The **coordinator** handles structural analysis and sends its findings directly to the specialist. You are the **team lead** — your ONLY job is spawning agents, sending the roster blast, and reporting the final result. Do NOT route messages between agents, do NOT cross-reference reports, do NOT present approval plans. The agents talk to each other directly.

## Arguments

The user invoked: `/shortterm $ARGUMENTS`

- If `$ARGUMENTS` is blank or `--help`: show this usage summary and stop:
  ```
  /shortterm --main         — collapse main agent memory
  /shortterm <agent-name>   — collapse a specific agent's memory
  /shortterm all            — collapse ALL agent memories sequentially
  ```
- If `$ARGUMENTS` is `--main` or "main": target the **main agent** memory at the project memory directory. No specialist agent needed — run single-agent mode (coordinator only, no team needed).
- If `$ARGUMENTS` is "all": process ALL agents sequentially, running the team process for each.
- Otherwise: `$ARGUMENTS` is a name to resolve to an agent. Use the discovery rules below.

## Context

- Available agents: !`python -c "import os; [print(f.removesuffix('.md')) for f in sorted(os.listdir('.claude/agents')) if f.endswith('.md')]" 2>/dev/null`
- Agent memory dirs: !`python -c "import os,sys; base='.claude/agent-memory'; [print(f'{d}: {len(mds)} files, {sum(sum(1 for _ in open(os.path.join(base,d,f),encoding=\"utf-8\",errors=\"ignore\")) for f in mds)} lines') for d in sorted(os.listdir(base)) if os.path.isdir(os.path.join(base,d)) for mds in [[f for f in os.listdir(os.path.join(base,d)) if f.endswith('.md')]]]; sys.exit(0)" 2>/dev/null`

## Agent Discovery

Match `$ARGUMENTS` to an agent in `.claude/agents/` by **case-insensitive substring**:

1. Scan all `.claude/agents/*.md` filenames
2. Find agents whose filename contains `$ARGUMENTS` (case-insensitive)
3. If exactly ONE match: that is the specialist agent type
4. If ZERO matches: ask the user which agent to target
5. If MULTIPLE matches: show candidates and ask the user to pick

The specialist's memory dir is `.claude/agent-memory/<agent-type>/`.

## Step 1: Discovery

1. Resolve the specialist agent type from `$ARGUMENTS`
2. List ALL files in the memory directory with line counts
3. Compute totals: file count, total lines, MEMORY.md line count

## Step 2: Create Team and Tasks

### 2a. Create the team

Use **TeamCreate** to create a team named `shortterm-<agent-short-name>` (e.g., `shortterm-skeptic`).

### 2b. Create tasks

Use **TaskCreate** to create two tasks in the team's task list:

**Task 1: "Classify memory by domain importance"**
- Description: Read all memory files in `.claude/agent-memory/<agent-type>/`. For each file and each distinct piece of information, classify as CRITICAL, REFERENCE, or STALE. Flag PROJECT-WIDE items.
- This task is for the specialist.

**Task 2: "Analyze memory for structural problems"**
- Description: Read all memory files in `.claude/agent-memory/<agent-type>/`. Identify duplication, verbosity, supersession chains, and merge candidates.
- This task is for the coordinator.

### 2c. Spawn teammates

Use the **Task** tool to spawn BOTH agents as teammates (in parallel, in a single message):

**Specialist teammate**:
- `subagent_type`: the resolved agent type (e.g., the agent whose memory is being collapsed)
- `team_name`: the team name from 2a
- `name`: `specialist`
- Prompt:

```
You are a teammate on team "<team-name>". Your name is "specialist".

Check TaskList for your assigned task. Read the task description, then execute it.

Your memory directory is `.claude/agent-memory/<agent-type>/`. Read ALL files in it.

For each file and each distinct piece of information, classify it as:
- **CRITICAL**: Equations, constants, proven results, key file paths, debugging solutions — things that would cause errors or wasted work if forgotten. Explain WHY in 1 sentence.
- **REFERENCE**: Detailed session notes, derivation steps, debate context — useful for deep recall but not needed every session.
- **STALE**: Superseded, refuted, completed TODOs, outdated estimates. State what superseded it.

Also flag any information with PROJECT-WIDE value (breakthroughs, validated results, framework synthesis) for promotion to a shared doc.

Be honest — you are helping yourself by cutting dead weight. If something was true in an earlier session but corrected later, mark the earlier version as STALE.

When done, WAIT for the coordinator to send you its structural report. Then combine both analyses and execute all file edits (deletes, merges, compressions, MEMORY.md rewrite) yourself. No approval needed from team-lead. When all edits are done, send a summary to "team-lead" with before/after line counts. Then mark your task as completed via TaskUpdate.
```

**Coordinator teammate**:
- `subagent_type`: `coordinator`
- `team_name`: the team name from 2a
- `name`: `coordinator`
- Prompt:

```
You are a teammate on team "<team-name>". Your name is "coordinator".

Check TaskList for your assigned task. Read the task description, then execute it.

The target memory directory is `.claude/agent-memory/<agent-type>/`. Read ALL files in it.

Analyze for STRUCTURAL problems (you don't need domain expertise):
- **Duplication**: Flag content that appears in multiple files (same facts restated). Quantify overlapping lines.
- **Verbosity**: Flag multi-sentence descriptions that could be bullet points, hedging language, boilerplate. Estimate compression ratio per file.
- **Supersession**: Flag session notes where a later file explicitly updates/corrects an earlier one.
- **Format**: Identify files that could be merged, files that are entirely redundant. Recommend a target file count and total line count.

When done, send your full structural report DIRECTLY to "specialist" via SendMessage (NOT to team-lead). The specialist will use your findings to execute the edits. Then mark your task as completed via TaskUpdate.
```

### 2d. Assign tasks

Use **TaskUpdate** to assign Task 1 to `specialist` and Task 2 to `coordinator`.

## Step 3: Hands Off — Agents Work Directly

The coordinator sends its structural report directly to the specialist. The specialist combines both analyses and executes all file edits autonomously. **Team-lead does NOTHING during this step.** No routing, no cross-referencing, no approval gates. The agents have each other's names from the roster blast — they communicate directly.

The specialist follows these rules when editing:
- NEVER delete information it classified as CRITICAL
- ALWAYS preserve exact numerical values, equation references, and file paths
- Compress narrative to bullets
- When specialist and coordinator DISAGREE, specialist wins (it knows its domain)
- When in doubt, KEEP IT (classify as REFERENCE and archive)

Target MEMORY.md structure (under 100 lines):
```markdown
# [Agent Name] Memory

## Active Context
[Only CRITICAL items — max 50 lines]

## Reference Index
[1-line pointers to detail files — max 20 lines]

## Key Constants & Equations
[Numerical values, file paths, equation references — max 30 lines]

## Debugging Notes
[Solutions to recurring problems — max 10 lines]
```

## Step 4: Report

Wait for the specialist to send its completion summary (before/after line counts, files changed). Do NOT check on it, nudge it, or take over. When it reports, present the result to the user.

## Step 5: Shutdown Team

1. Send shutdown requests to both teammates via **SendMessage** (type: `shutdown_request`)
2. Wait for shutdown confirmations
3. Use **TeamDelete** to clean up the team

## Rules

- NEVER delete information classified as CRITICAL by the specialist
- ALWAYS preserve exact numerical values, equation references, and file paths
- Compress narrative to bullets — e.g., "Session 4 spent 3 hours debating methodology..." becomes "Session 4: methodology RESOLVED (approach X selected)"
- When specialist and coordinator DISAGREE, specialist wins on importance
- When in doubt, KEEP IT (classify as REFERENCE and archive)
- **Team-lead does NOT intermediate between agents.** Coordinator sends to specialist directly. Specialist executes directly. No approval loop through team-lead.
- **Team-lead does NOT nudge, check on, or take over agent work.** Idle notifications are normal. Wait silently.

## Output Format

After completion:

```
=== COLLAPSE COMPLETE ===
Before: XXXX lines across N files
After:  YYYY lines across M files (+ K archived docs)
Savings: ZZ% reduction in active memory footprint
Team:   shortterm-<name> (specialist: <type>, coordinator: coordinator)
```
