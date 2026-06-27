---
name: shortterm
description: Collapse and optimize agent memory files — deduplicate, compress, archive to docs
argument-hint: "<agent-name>"
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash, Agent]
---

# Memory Collapse Skill (Single Agent)

Spawn ONE agent (the specialist whose memory is being collapsed) to classify, analyze, and edit its own memory files. No team, no coordinator, no orchestration overhead.

## Arguments

The user invoked: `/shortterm $ARGUMENTS`

- If `$ARGUMENTS` is blank or "main": target the **main agent** memory at the project memory directory. No agent spawn needed — you (the main agent) do the work directly.
- If `$ARGUMENTS` is "all": process ALL agents sequentially, spawning agents in parallel.
- Otherwise: `$ARGUMENTS` is a name to resolve to an agent. Use the discovery rules below.

## Context

- Available agents: !`python -c "import os; [print(f.removesuffix('.md')) for f in sorted(os.listdir('.claude/agents')) if f.endswith('.md')]" 2>/dev/null`
- Agent memory dirs: !`python -c "import os,sys; base='.claude/agent-memory'; [print(f'{d}: {len(mds)} files, {sum(sum(1 for _ in open(os.path.join(base,d,f),encoding=\"utf-8\",errors=\"ignore\")) for f in mds)} lines') for d in sorted(os.listdir(base)) if os.path.isdir(os.path.join(base,d)) for mds in [[f for f in os.listdir(os.path.join(base,d)) if f.endswith('.md')]]]; sys.exit(0)" 2>/dev/null`

## Agent Discovery

Match `$ARGUMENTS` to an agent in `.claude/agents/` by **case-insensitive substring**:

1. Scan all `.claude/agents/*.md` filenames
2. Find agents whose filename contains `$ARGUMENTS` (case-insensitive)
3. If exactly ONE match: that is the agent type
4. If ZERO matches: ask the user which agent to target
5. If MULTIPLE matches: show candidates and ask the user to pick

The agent's memory dir is `.claude/agent-memory/<agent-type>/`.

## Step 1: Discovery

1. Resolve the agent type from `$ARGUMENTS`
2. List ALL files in the memory directory with line counts
3. Compute totals: file count, total lines, MEMORY.md line count
4. Report the discovery to the user before spawning

## Step 2: Spawn Agent

Use the **Agent** tool to spawn a SINGLE agent:

- `subagent_type`: the resolved agent type (e.g., `calculator`)
- `description`: `Collapse <agent-name> memory`
- Prompt:

```
You are collapsing your own agent memory. Your memory directory is `.claude/agent-memory/<agent-type>/`.

## Phase 1: Read Everything
Read ALL files in your memory directory completely.

## Phase 2: Classify
For each file and each distinct piece of information, classify it as:
- **CRITICAL**: Equations, constants, proven results, key file paths, debugging solutions — things that would cause errors or wasted work if forgotten.
- **REFERENCE**: Detailed session notes, derivation steps, debate context — useful for deep recall but not needed every session.
- **STALE**: Superseded, refuted, completed TODOs, outdated probability estimates. State what superseded it.
- **AMRI-PROMOTE** (Agent-Memory Registry Inversion): project-level registries mistakenly stored in this memory -- watchlists, rosters, cross-item correlation tables, pinned predictions, closed-approach lists, constant tables, gate/test verdict tables. Detect via three tests (if the discipline pack documents an AMRI section in `.claude/rules/agent-standards.md`, follow it; otherwise these are the tests):
  - **input-pin**: another agent or a session plan reads this block as a pinned input (it is consumed elsewhere, not just by you).
  - **output-target**: the content is a registry/table that should have a single canonical home, not a per-agent copy.
  - **cross-agent overlap**: the same content appears in more than one agent's memory (it is project-wide, not agent-private).

  For each **AMRI-PROMOTE** item, your Phase 5 report MUST include:
  - `content`: the full text block, preserved verbatim
  - `target_framework_path`: proposed path `sessions/framework/<slug>.md`
  - `consumer_tests`: gate/test IDs in session plans that reference this memory as a pinned input (search `sessions/session-plan/*.md` and `sessions/session-*/` for your agent-memory path); else NONE_FOUND
  - `migration_note`: one-line justification naming which AMRI test fired

Be honest -- you are helping yourself by cutting dead weight. If something was true in an earlier session but corrected later, mark the earlier version as STALE.

## Phase 3: Structural Analysis
Analyze your own files for:
- **Duplication**: Same facts restated across files. Quantify overlapping lines.
- **Verbosity**: Multi-sentence descriptions that could be bullets. Estimate compression ratio per file.
- **Supersession**: Later files that explicitly update/correct earlier ones.
- **Format**: Files that could be merged, files that are entirely redundant.

## Phase 4: Execute Edits
Combine your classification and structural analysis, then execute ALL file edits:
- Delete STALE-only files
- Merge related detail files where possible
- Compress narrative to bullets
- Rewrite MEMORY.md to the target structure (under 100 lines)
- For **AMRI-PROMOTE** items: do NOT delete the content. Replace it in-place with a pointer line of the form `> See sessions/framework/<slug>.md (AMRI-promoted <YYYY-MM-DD>; was <one-line reason>)`. The orchestrator reads your Phase 5 promotion report, writes the framework file, and reindexes via `/weave --update`. Your job is to (a) remove the AMRI content from your memory and (b) install the pointer so your future self knows where the migrated content lives.

Rules:
- NEVER delete information you classified as CRITICAL
- ALWAYS preserve exact numerical values, equation references, and file paths
- Compress narrative to bullets -- "Session 11 spent 3 hours debating approach X..." becomes "Session 11: approach X RESOLVED (chose method Y)"
- When in doubt, KEEP IT (classify as REFERENCE and archive)

Target MEMORY.md structure (under 100 lines):
```
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

## Phase 5: Report
When all edits are done, output a summary with:
- Before/after line counts per file
- Files deleted, merged, or created
- Total lines before and after
- **AMRI-PROMOTE inventory** -- for each promoted item, emit a structured block the orchestrator parses verbatim:

      ### AMRI-PROMOTE: <slug>
      Target: sessions/framework/<slug>.md
      Migration note: <one-line justification; name which AMRI test fired>
      Consumer tests: <comma-separated gate/test IDs, or NONE_FOUND>
      Content (verbatim): <the exact content block to be promoted>

  If no AMRI-PROMOTE items were found, state "AMRI-PROMOTE inventory: none" explicitly.
```

## Step 3: Report

When the agent returns its summary, present the result to the user:

```
=== COLLAPSE COMPLETE ===
Before: XXXX lines across N files
After:  YYYY lines across M files
Savings: ZZ% reduction in active memory footprint
Agent:  <agent-type>
```

## Rules

- NEVER delete information classified as CRITICAL
- ALWAYS preserve exact numerical values, equation references, and file paths
- When in doubt, KEEP IT
- No teams, no coordinators, no roster blasts — one agent, one job
