---
description: Build a structured index for a researcher folder or general project folder
argument-hint: <folder-name> [qualifier1] [qualifier2] ...
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash, Agent, TeamCreate, TaskCreate, TaskUpdate, TaskList, TaskGet, SendMessage]
---

# Indexing Skill (Team Orchestration)

Two-agent team: a **specialist** (domain expert who reads and analyzes the files) and a **coordinator** (template enforcer who assembles the index). You are the **team lead** orchestrating them.

## Arguments

The user invoked: `/indexing $ARGUMENTS`

Parse `$ARGUMENTS` as:
- **`--help`**: show this usage summary and stop:
  ```
  /indexing                          — list all indexable folders
  /indexing <folder>                 — index entire folder
  /indexing <folder> <qualifier> ... — index only matching files
  ```
- **Blank**: list all indexable folders and their status, then stop
- **`<folder>`**: index the entire folder with auto-detected groupings
- **`<folder> <qualifier1> [qualifier2] ...`**: index ONLY files matching the given qualifiers
  - Qualifiers match by case-insensitive substring against filenames
  - E.g., `/indexing meeting-minutes session-16 giants` processes only files whose names contain "session-16" or "giants"
  - E.g., `/indexing Noether 13-18` processes only files whose names contain "13-18" (or papers 13 through 18 -- interpret numerically if a range)
  - If `index.md` already exists, MERGE results into it (update/add only the affected sections, leave other entries intact)

## Context

Discover folders and agents dynamically using Glob/Bash at runtime:
- Researcher folders: `researchers/*/` subdirectories
- Top-level folders: `*/` in project root
- Existing researcher indexes: `researchers/*/index.md`
- Available agents: `.claude/agents/*.md`

## Mode Detection

1. If `<folder>` matches a subfolder of `researchers/` -> **Mode A: Researcher Index**
2. If `<folder>` matches a top-level folder (e.g., `meeting-minutes`, `sessions`) -> **Mode B: General Folder Index**
3. If ambiguous, ask the user

---

# Step 1: Discovery (Both Modes)

### 1a. Validate Folder

- Mode A: confirm `researchers/<folder>/` exists
- Mode B: confirm `<folder>/` exists as a directory
- List ALL files (`.md` and `.py` primarily, exclude `index.md` and `AGENTS.md`)

### 1b. Apply Qualifier Filter

If qualifiers were provided:
- Filter the file list to ONLY files whose names contain ANY qualifier (case-insensitive substring)
- For numeric ranges like `13-18`, expand to individual numbers and match files containing any of 13, 14, 15, 16, 17, 18
- Report: "Filtered to N files matching qualifiers: [list]"
- If ZERO files match, report and stop

If no qualifiers: use the full file list.

### 1c. Detect Groupings

Scan the (filtered) filenames to identify **natural groups** of 3-7 files each. The team lead does this BEFORE spawning agents.

**Mode A grouping** (researcher papers):
- Group by natural clusters in filename numbering, topic, or era
- E.g., Group 1 = "Papers 01-06 (foundations)", Group 2 = "Papers 07-12 (advanced topics)", Group 3 = "Papers 13-18 (applications)"
- Target: 2-5 groups of 3-7 papers each

**Mode B grouping** (general folders):
- Group by detected qualifier pattern (session number, date, type prefix)
- E.g., sessions: "Sessions 1-6", "Sessions 7-10", "Sessions 11-15"
- E.g., computation: by prefix pattern (tier1_*, session11_*, etc.)
- Target: 3-8 groups

Format each group as:
```
Group N: "<descriptive name>" -- files: [file1.md, file2.md, ...]
```

### 1d. Resolve Agent (Mode A only)

Match the folder name to an agent in `.claude/agents/` by case-insensitive substring:
1. Scan all `.claude/agents/*.md` filenames
2. Find agents whose filename contains the folder name (case-insensitive)
3. If exactly ONE match: use that agent type
4. If ZERO matches: ask the user which agent to use
5. If MULTIPLE matches: show candidates and ask the user to pick

### 1e. Check Existing Index

- If `index.md` already exists AND no qualifiers: ask user whether to rebuild
- If `index.md` exists AND qualifiers were provided: will merge (no need to ask)
- If no `index.md`: fresh build

---

# Step 2: Create Team and Tasks

### 2a. Create the Team

Use **TeamCreate** to create a team named `indexing-<folder-short-name>` (e.g., `indexing-noether`, `indexing-minutes`).

### 2b. Create Tasks

Use **TaskCreate** to create two tasks:

**Task 1: "Analyze files by domain"**
- Description: Read all files in [group list]. For each file, produce: summary, key results, key equations (Mode A) or one-line summary with outcome (Mode B). Process one group at a time, sending results per group.
- Assigned to: specialist (Mode A) or reader (Mode B)

**Task 2: "Assemble index from reports"**
- Description: Receive per-group reports from the specialist/reader. Assemble into the index template. Enforce template compliance. Detect cross-file patterns (dependency graph, phases, topic map).
- Assigned to: coordinator (Mode A) or assembler (Mode B)

---

# Step 3: Spawn Teammates

Use the **Agent** tool to spawn BOTH agents in parallel (single message, two Agent calls):

## Mode A: Researcher Index

**Specialist teammate**:
- `subagent_type`: the resolved agent type from Step 1d
- `team_name`: the team name from 2a
- `name`: `specialist`
- `mode`: `bypassPermissions`
- Prompt:

```
You are a teammate on team "<team-name>". Your name is "specialist".

Check TaskList for your assigned task. Read the task description, then execute it.

You are indexing researcher papers in `researchers/<folder>/`. Process them in groups, ONE GROUP AT A TIME.

**GROUPS:**
<paste the group list from Step 1c>

**INSTRUCTIONS:**
1. Start with Group 1. Read ALL papers in Group 1.
2. For each paper, produce:
   - **Summary** (2-4 sentences: what the paper does, the main construction, key result)
   - **Key Results** (bullet list of theorems/propositions/computed values that matter)
   - **Key Equations** (table: equation label | description | equation or reference)
   - **Dependencies** (which other papers are upstream/downstream)
   - **Relevance** (CRITICAL / HIGH / MEDIUM / LOW to the project)
   - **Tags** (topic keywords for cross-referencing)
3. Send Group 1 results to "coordinator" via SendMessage.
4. CHECK YOUR INBOX. Process any messages before continuing.
5. Proceed to Group 2. Repeat steps 2-4 for each group.
6. After ALL groups: send a final synthesis to "coordinator" with:
   - Overall dependency graph (text diagram showing paper relationships)
   - Topic map (which papers cover which topics)
   - Quick Reference recommendations (task keyword -> paper numbers -> priority)
7. Mark your task as completed via TaskUpdate.

Use your specialist knowledge to identify which results matter most for the project. Be honest about relevance -- LOW is fine for papers that don't directly apply.
```

**Coordinator teammate**:
- `subagent_type`: `coordinator`
- `team_name`: the team name from 2a
- `name`: `coordinator`
- `mode`: `bypassPermissions`
- Prompt:

```
You are a teammate on team "<team-name>". Your name is "coordinator".

Check TaskList for your assigned task. Read the task description, then execute it.

You are assembling a researcher index for `researchers/<folder>/`. The specialist is reading papers and will send you per-group reports. Your job is STRUCTURAL ASSEMBLY -- enforce the template and build the final index.

**TEMPLATE** (follow this structure exactly):
```markdown
# <Researcher> Paper Index

**Researcher**: <name>
**Papers**: <count> (<year range>)
**Primary domain**: <topics>
**Project relevance**: <1-2 sentences>

---

## Dependency Graph
<text diagram from specialist>

## Topic Map
<grouped topic sections from specialist>

## Quick Reference
| If your task involves... | Read these papers | Priority |
|:---|:---|:---|

## Paper Entries
### Paper NN: <Title>
- **File**: `filename.md`
- **Year**: <year>
- **Relevance**: <CRITICAL/HIGH/MEDIUM/LOW>
- **Tags**: <keywords>

**Summary**: <from specialist>
**Key Results**: <from specialist>
**Key Equations**: <table from specialist>
**Dependencies**: <from specialist>

(repeat for each paper)

---

## Cross-Paper Equation Concordance
<equations referenced across multiple papers>

## Notation Conventions
<common notation used across the paper collection>

## Computational Verification Status
<which papers/equations have been verified computationally>
```

**INSTRUCTIONS:**
1. Wait for the specialist's Group 1 report.
2. As each group report arrives, start drafting those paper entries. Enforce template compliance.
3. After receiving ALL group reports plus the final synthesis, assemble the complete index.
4. Send the COMPLETE assembled index to "team-lead" via SendMessage.
5. Mark your task as completed via TaskUpdate.

If an existing researcher index exists in the project, read its first 100 lines as a format reference.
```

## Mode B: General Folder Index

**Reader teammate**:
- `subagent_type`: `coordinator`
- `team_name`: the team name from 2a
- `name`: `reader`
- `mode`: `bypassPermissions`
- Prompt:

```
You are a teammate on team "<team-name>". Your name is "reader".

Check TaskList for your assigned task. Read the task description, then execute it.

You are indexing files in `<folder>/`. Process them in groups, ONE GROUP AT A TIME.

**GROUPS:**
<paste the group list from Step 1c>

**INSTRUCTIONS:**
1. Start with Group 1. Read ALL files in Group 1 (actually read them -- no guessing from filenames).
2. For each file, produce:
   - **One-line summary** (max 15 words, state the OUTCOME not the process)
   - **Qualifier** (session number, phase, type -- whatever the grouping key is)
   - **Key items** (bullet list: decisions, breakthroughs, results, direction changes)
3. Also write a **group paragraph** (1-3 sentences):
   - 1 sentence for simple groups (single outcome)
   - 2-3 sentences for dense groups (multi-round workshops, debates)
   - State what was attempted, what was achieved, any direction changes
4. Send Group 1 results to "assembler" via SendMessage.
5. CHECK YOUR INBOX. Process any messages before continuing.
6. Proceed to Group 2. Repeat steps 2-5 for each group.
7. After ALL groups: send a final synthesis to "assembler" with:
   - Phase recommendations (which groups form natural project phases)
   - Quick Reference suggestions (topic keyword -> file list)
8. Mark your task as completed via TaskUpdate.

One-line summary rules:
- Max 15 words
- State the OUTCOME ("Hypothesis X CONFIRMED" not "Discussed hypothesis X")
- Include key results where applicable
```

**Assembler teammate**:
- `subagent_type`: `coordinator`
- `team_name`: the team name from 2a
- `name`: `assembler`
- `mode`: `bypassPermissions`
- Prompt:

```
You are a teammate on team "<team-name>". Your name is "assembler".

Check TaskList for your assigned task. Read the task description, then execute it.

You are assembling a general folder index for `<folder>/`. The reader is processing files and will send you per-group reports. Your job is STRUCTURAL ASSEMBLY -- enforce the template and detect phases.

**TEMPLATE** (follow this structure exactly):
```markdown
# <Folder Name> Index

**Files**: <count>
**Date range**: <earliest> to <latest>
**Qualifier**: <what the grouping key is>

---

## Phase Overview

### <Phase Name> (qualifier range)
<1-3 sentence paragraph from reader's group summary>

| File | Qualifier | One-Line Summary |
|:---|:---|:---|
| `filename.md` | Session N | What this file contains in <=15 words |

(repeat for each phase)

---

## Quick Reference

| If you need... | Read these files |
|:---|:---|
| <topic keyword> | <file list> |
```

**PHASE GROUPING RULES:**
- Group files by natural project phases, NOT by date or session number alone
- A phase = a contiguous span of sessions/files that share a common objective
- Name each phase by its objective ("Foundation Review", "Computation Sprint", "Two-Team Workshop")
- Some sessions span multiple files -- keep them in one phase group

**INSTRUCTIONS:**
1. Wait for the reader's Group 1 report.
2. As each group report arrives, start drafting those phase sections. Enforce template compliance.
3. After receiving ALL group reports plus the final synthesis, assemble the complete index.
4. Detect phases across groups -- the reader will suggest phase boundaries but you make the final call.
5. Build the Quick Reference table from the reader's suggestions.
6. Send the COMPLETE assembled index to "team-lead" via SendMessage.
7. Mark your task as completed via TaskUpdate.
```

---

# Step 4: Assign Tasks and Wait

### 4a. Assign Tasks

Use **TaskUpdate** to assign Task 1 to `specialist`/`reader` and Task 2 to `coordinator`/`assembler`.

### 4b. Wait for Reports

Wait for both teammates to complete their work. The coordinator/assembler will send the final assembled index to you via SendMessage.

---

# Step 5: Merge and Write

### 5a. Review the Index

Read the coordinator/assembler's submitted index. Check for:
- Template compliance (all required sections present)
- No placeholder text or TODO markers
- Reasonable length (researcher: 300-800 lines, general: 100-400 lines)

### 5b. Write or Merge the Index

**Fresh build** (no existing index, or user approved rebuild):
- Write the index directly to `<folder>/index.md`

**Merge** (qualifiers specified, existing index present):
- Read the existing `index.md`
- Identify which sections correspond to the qualifier-filtered files
- Replace/add ONLY those sections (paper entries, phase sections)
- Update aggregate sections (Quick Reference, Topic Map, dependency graph) to include new entries
- Preserve all unaffected entries

### 5c. Place AGENTS.md

Copy `researchers/agents.md` into the target folder as `AGENTS.md` if not already present.

---

# Step 6: Shutdown Team

1. Send shutdown requests to both teammates via **SendMessage** (type: `shutdown_request`)
2. Wait for shutdown confirmations
3. **DO NOT call TeamDelete.** Leave the team intact. The user will clean up teams manually or in a later session. Multiple indexing instances may be running in parallel -- deleting teams from one instance DESTROYS the others.

---

# Step 7: Report

**Mode A:**
```
=== INDEXING COMPLETE (Researcher) ===
Folder:    researchers/<name>/
Papers:    <N> indexed
Groups:    <N> processed (<group names>)
Index:     researchers/<name>/index.md (<line count> lines)
AGENTS.md: <placed / already present>
Agent:     <specialist agent type>
Team:      indexing-<name> (specialist: <type>, coordinator: coordinator)
```

**Mode B:**
```
=== INDEXING COMPLETE (General) ===
Folder:    <name>/
Files:     <N> indexed
Groups:    <N> processed (<group names>)
Phases:    <N> identified
Index:     <name>/index.md (<line count> lines)
AGENTS.md: <placed / already present>
Team:      indexing-<name> (reader: coordinator, assembler: coordinator)
```

---

# Rules

- **NEVER DELETE TEAMS. NEVER CALL TeamDelete.** Multiple indexing instances may run in parallel. Deleting teams from one instance destroys active work in others. Teams are cheap; lost work is not. The user manages team cleanup.
- **NEVER delete other teams' directories** (e.g., `rm -rf ~/.claude/teams/*`). Only your own team exists from your perspective.
- **Do NOT "clean up stale teams"** as part of indexing startup. Skip the stale-team-cleanup step from CLAUDE.md when running as indexing. Other indexing instances may be active.
- The agents read the files, NOT you. Your job is orchestration and final assembly.
- Never overwrite an existing index.md without user confirmation (unless merging with qualifiers).
- If zero agents match in Mode A, ask the user. Mode B always uses `coordinator`.
- The AGENTS.md file is generic and identical across all folders.
- For Mode B, the reader must ACTUALLY READ every file -- no guessing from filenames.
- Agents process ONE GROUP AT A TIME, checking inbox between groups.
- When merging into an existing index, preserve all unaffected entries.
- Target group sizes: 3-7 files per group. Smaller groups are fine for qualifiers.
- If the total file count is <= 5, use a SINGLE group (no batching needed).
