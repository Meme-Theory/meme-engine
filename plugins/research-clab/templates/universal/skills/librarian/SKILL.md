---
description: Build a structured index for a researcher folder or general project folder
argument-hint: <folder-name> [qualifier1] [qualifier2] ...
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash, Agent]
---

# Librarian Skill

Single-agent indexer: spawn the **domain specialist** (Mode A) or a **coordinator** (Mode B) to read all files and write the index directly. No team infrastructure.

## Arguments

The user invoked: `/librarian $ARGUMENTS`

Parse `$ARGUMENTS` to extract:
- **Blank**: list all indexable folders and their status, then stop
- **`<folder>`**: index the entire folder with auto-detected groupings
- **`<folder> <qualifier1> [qualifier2] ...`**: index ONLY files matching the given qualifiers
  - Qualifiers match by case-insensitive substring against filenames
  - E.g., `/librarian Baptista 13-18` processes only papers 13 through 18 (interpret numerically if a range)
  - If `index.md` already exists, MERGE results into it (update/add only the affected sections)

If `$ARGUMENTS` is `--help`, show this usage summary and stop:
```
/librarian                              -- list all indexable folders and status
/librarian Baptista                     -- index all papers in researchers/Baptista/
/librarian Baptista 13-18               -- index only papers 13-18 (merge into existing index)
/librarian meeting-minutes session-16   -- index files matching "session-16"
/librarian tier0-computation            -- index tier0 scripts and data
```

## Context

Discover folders and agents dynamically at runtime:
- Project root CLAUDE.md: Read `CLAUDE.md` for domain context
- Researcher folders: `researchers/*/` subdirectories
- Top-level folders: `*/` in project root
- Existing researcher indexes: `researchers/*/index.md`
- Available agents: `.claude/agents/*.md`

## Mode Detection

1. If `<folder>` matches a subfolder of `researchers/` -> **Mode A: Researcher Index**
2. If `<folder>` matches a top-level folder (e.g., `sessions`, `tier0-computation`) -> **Mode B: General Folder Index**
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

Scan the (filtered) filenames to identify **natural groups** of 3-7 files each. You do this BEFORE spawning the agent.

**Mode A grouping** (researcher papers):
- Group by natural clusters in filename numbering, topic, or era
- E.g., Baptista: Group 1 = "Papers 01-06 (vortex foundations)", Group 2 = "Papers 07-12 (advanced vortices)", Group 3 = "Papers 13-18 (KK/SM geometry)"
- Target: 2-5 groups of 3-7 papers each

**Mode B grouping** (general folders):
- Group by detected qualifier pattern (session number, date, type prefix)
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
4. If ZERO matches: use `gen-physicist` as fallback, or ask the user
5. If MULTIPLE matches: show candidates and ask the user to pick

Mode B always uses `coordinator`.

### 1e. Check Existing Index

- If `index.md` already exists AND no qualifiers: ask user whether to rebuild
- If `index.md` exists AND qualifiers were provided: will merge (no need to ask)
- If no `index.md`: fresh build

### 1f. Determine Merge Context

If merging (qualifiers + existing index):
- Read the existing `index.md`
- Extract the list of papers/files already indexed
- Pass this to the agent so it knows what already exists

---

# Step 2: Spawn Agent

Spawn a **single background agent** using the Agent tool. One agent does everything: reads the files, analyzes them, and writes the index.

## Mode A: Researcher Index

- `subagent_type`: the resolved agent type from Step 1d
- `run_in_background`: true
- `name`: `librarian-indexer`
- `mode`: `bypassPermissions`

**Prompt (fresh build):**

```
You are building a researcher paper index for `researchers/<folder>/`.

## Required Reading

Read ALL of the following files (actually read them -- full content, not just filenames):

**Papers to index:**
<numbered list of all files from Step 1b>

**Grouped as:**
<paste the group list from Step 1c>

**Also read for format reference:**
- `researchers/Baptista/index.md` (first 100 lines -- see the structure to follow)
- Your agent memory: `.claude/agent-memory/<agent-slug>/MEMORY.md` (if it exists)

## Your Task

Read every paper, then write the complete index to: `researchers/<folder>/index.md`

Use the Write tool to create the file. Follow this template EXACTLY:

```markdown
# <Researcher> Paper Index

**Researcher**: <name>
**Papers**: <count> (<year range>)
**Primary domain**: <topics>
**Project relevance**: <1-2 sentences connecting to the project>

---

## Dependency Graph

<text diagram showing paper relationships -- which papers build on which>
<use arrows: Paper 01 -> Paper 03 -> Paper 07>
<group by theme, not just chronology>

## Topic Map

### <Topic 1>
Papers: NN, NN, NN
<1-2 sentences on what this topic cluster covers>

### <Topic 2>
Papers: NN, NN
<1-2 sentences>

(repeat for each topic cluster)

## Quick Reference

| If your task involves... | Read these papers | Priority |
|:---|:---|:---|
| <topic keyword> | Paper NN, NN | CRITICAL/HIGH/MEDIUM |

(5-10 rows covering the main use cases)

---

## Paper Entries

### Paper NN: <Title>
- **File**: `filename.md`
- **arXiv**: <id if known, otherwise "N/A">
- **Year**: <year>
- **Relevance**: <CRITICAL / HIGH / MEDIUM / LOW>
- **Tags**: <comma-separated topic keywords>

**Summary**: <2-4 sentences: what the paper does, the main construction, key result>

**Key Results**:
- <bullet list of theorems/propositions/computed values that matter>

**Key Equations**:

| Label | Description | Reference |
|:---|:---|:---|
| eq N.NN | <what it is> | <equation or section reference> |

**Dependencies**: <which other papers in this folder are upstream/downstream>

(repeat for each paper)

---

## Cross-Paper Equation Concordance

<equations or quantities referenced across multiple papers>
<e.g., "The primary operator X appears in Papers 03, 07, 12 with different conventions...">

## Notation Conventions

<common notation used across the paper collection>
<e.g., "τ = deformation parameter", "X = key operator defined in Paper 03">

## Computational Verification Status

| Paper | Equation/Result | Verified? | Where |
|:---|:---|:---|:---|
| NN | <result> | Yes/No/Partial | <tier0 script if applicable> |
```

## Rules
- Read EVERY paper fully before writing. Do not guess from filenames.
- Use your specialist knowledge to assess relevance honestly -- LOW is fine.
- The Dependency Graph and Cross-Paper Equation Concordance are your highest-value contributions.
- Write ONLY the index file. Do not create any other files.
- Target length: 300-800 lines.
```

**Prompt (merge -- qualifiers provided, existing index):**

```
You are UPDATING an existing researcher paper index for `researchers/<folder>/`.

## Existing Index
Read the current index: `researchers/<folder>/index.md`

## New Papers to Add/Update
Read ALL of the following files:
<numbered list of qualifier-filtered files>

## Your Task

1. Read the existing index completely.
2. Read all new/updated papers completely.
3. For each new paper, produce the same entry format as existing entries (Summary, Key Results, Key Equations, Dependencies, Relevance, Tags).
4. Use the Edit tool to:
   - ADD new paper entries in the correct numerical position
   - UPDATE the Dependency Graph to include new papers
   - UPDATE the Topic Map if new topics emerge
   - UPDATE the Quick Reference table
   - UPDATE the Cross-Paper Equation Concordance
   - PRESERVE all existing entries that are not being updated
5. Do NOT rewrite the entire file -- use targeted edits.

## Rules
- PRESERVE all existing entries not covered by the qualifier filter.
- Insert new entries in numerical order among existing entries.
- Update aggregate sections (Dependency Graph, Topic Map, Quick Reference) to reflect the additions.
- Write ONLY to the index file. Do not create any other files.
```

## Mode B: General Folder Index

- `subagent_type`: `coordinator`
- `run_in_background`: true
- `name`: `librarian-indexer`
- `mode`: `bypassPermissions`

**Prompt (fresh build):**

```
You are building a general folder index for `<folder>/`.

## Required Reading

Read ALL of the following files (actually read them -- full content, not just filenames):

**Files to index:**
<numbered list of all files from Step 1b>

**Grouped as:**
<paste the group list from Step 1c>

## Your Task

Read every file, then write the complete index to: `<folder>/index.md`

Use the Write tool to create the file. Follow this template EXACTLY:

```markdown
# <Folder Name> Index

**Files**: <count>
**Date range**: <earliest> to <latest>
**Qualifier**: <what the grouping key is -- e.g., session number, script prefix>

---

## Phase Overview

### <Phase Name> (qualifier range)

<1-3 sentence paragraph: what was attempted, what was achieved, any direction changes>

| File | Qualifier | One-Line Summary |
|:---|:---|:---|
| `filename.md` | Session N | <=15 words stating the OUTCOME |

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
- Name each phase by its objective ("Foundation Review", "Tier 0 Computation", "Two-Team Workshop")
- Some sessions span multiple files -- keep them in one phase group

**ONE-LINE SUMMARY RULES:**
- Max 15 words
- State the OUTCOME ("Chirality catch-22 RESOLVED" not "Discussed chirality issues")
- Include key results where applicable ("KO-dim=6 computed", "phi found at s=1.14")

## Rules
- Read EVERY file fully. Do not guess from filenames.
- Write ONLY the index file. Do not create any other files.
- Target length: 100-400 lines.
```

**Prompt (merge):** Same pattern as Mode A merge -- read existing index, read new files, use Edit to insert/update entries while preserving existing content.

---

# Step 3: Post-Processing

After the agent completes:

### 3a. Verify Output

- Confirm index file exists at the expected path
- Read it and check:
  - Template compliance (all required sections present)
  - No placeholder text or TODO markers
  - Reasonable length (researcher: 300-800 lines, general: 100-400 lines)

### 3b. Place AGENTS.md

Copy `researchers/agents.md` into the target folder as `AGENTS.md` if not already present (Mode A only).

### 3c. Report

**Mode A:**
```
=== LIBRARIAN COMPLETE (Researcher) ===
Folder:    researchers/<name>/
Papers:    <N> indexed
Groups:    <N> processed (<group names>)
Index:     researchers/<name>/index.md (<line count> lines)
AGENTS.md: <placed / already present>
Agent:     <agent type used>
```

**Mode B:**
```
=== LIBRARIAN COMPLETE (General) ===
Folder:    <name>/
Files:     <N> indexed
Groups:    <N> processed (<group names>)
Phases:    <N> identified
Index:     <name>/index.md (<line count> lines)
```

---

# Rules

- The agent reads the files, NOT you. Your job is discovery (Step 1) and verification (Step 3).
- Never overwrite an existing index.md without user confirmation (unless merging with qualifiers).
- If zero agents match in Mode A, use `gen-physicist` or ask the user. Mode B always uses `coordinator`.
- The AGENTS.md file is generic and identical across all researcher folders.
- The agent must ACTUALLY READ every file -- no guessing from filenames.
- When merging into an existing index, preserve all unaffected entries.
- Target group sizes: 3-7 files per group. Smaller groups are fine for qualifiers.
- If the total file count is <= 5, use a SINGLE group (no batching needed).
