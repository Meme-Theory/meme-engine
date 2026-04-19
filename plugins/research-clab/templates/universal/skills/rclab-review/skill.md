---
name: rclab-review
description: Generate solo synthesis/review reports from source docs — 1+ independent agents each read the same sources and write their own report. No coordination between agents.
argument-hint: <doc(s)> --agents <type1[,type2,...]> [--session <id>] [--output <path>] [--context <text>]
---

# rclab-review

## --help

If `$ARGUMENTS` contains `--help` or `-h` (or is empty and the user seems confused), read and display `.claude/rclab-help.md`, then stop. Do not proceed with any other phase.

---

Solo synthesis. 1+ agents independently read source documents and write their own report. No coordination between agents — each produces its own file from the same inputs.

For 2-agent iterative workshops on a shared document, use `/rclab-workshop`.

## Usage

```
# One agent synthesizes source docs
/rclab-review session-63-W6*.md --agents <domain-generalist>

# Three agents each independently write a report
/rclab-review session-63*.md --agents hawking,landau,volovik --session 63

# With focus topics
/rclab-review session-74*.md --agents qa,connes --context CC closure, GL stability
```

---

## Phase 0: Parse & Validate

### 0a. Extract Arguments

Parse `$ARGUMENTS`:

| Arg | Required | Default | Notes |
|:----|:---------|:--------|:------|
| `[doc(s)]` | yes (1+) | — | Source doc paths or globs (positional, before flags) |
| `--agents` | yes | — | Comma-separated agent types or short names (1 or more) |
| `--session` | no | auto-detect | Session ID (e.g., `63`) |
| `--output` | no | auto-detect | Output path prefix (per-agent files generated) |
| `--context` | no | — | Focus topics or instructions passed to agents |

### 0b. Validate

1. **Source docs**: Glob-resolve paths. Read 1 line of each to verify existence. Report missing and stop.
2. **Agent types**: Resolve short names via `.claude/templates/agent-roster.md`. If invalid, list available types and stop.

### 0c. Defaults

**Session ID** (if not provided):
- Extract from first source doc filename: regex `session-(\d+)`

**Output path** (if not provided, per agent):
- `sessions/session-{id}/session-{id}-{short-name}-synthesis.md`

If session ID unresolvable, ask the user.

---

## Phase 1: Collision Check

If any output file already exists, ask: "Output file exists at `{path}`. Overwrite / New name / Cancel?"

---

## Phase 2: Execute

For each agent in `--agents`, spawn a **background agent** in parallel:

- `subagent_type`: the agent type
- `run_in_background`: true
- `name`: `review-{short-name}`
- `mode`: `acceptEdits`

**Agent prompt:**

```
You are writing a synthesis report for the {{PROJECT_NAME}} project.

## Source Documents (read ALL of these FIRST)
{numbered list of source doc paths}

Also read your agent memory: `.claude/agent-memory/{your-type}/MEMORY.md`

{If --context provided:}
## Focus
{context text}

## Your Task

Read all source documents, then write your synthesis to: `{output_path}`

## Document Structure

Follow the template in `.claude/templates/synthesis.md`.

## Rules
- Gate verdicts from source docs are authoritative — do not re-adjudicate.
- If sources conflict, flag the conflict explicitly.
- Write ONLY the output file.
- Use the project's framing vocabulary (see the framework-framing rule if one is installed by the selected discipline pack).
- Every equation dimensionally consistent. Every approximation states its regime.
```

If multiple agents: create a TaskCreate per agent for progress tracking.

---

## Phase 3: Verify & Report

```
=== RCLAB-REVIEW COMPLETE ===
Agent(s): {list}
Output: {path(s)} ({lines} lines each)
Source documents: {N}
```

---

## Rules

1. **Never overwrite files** without user confirmation (collision check).
2. **Never execute computations** — review reports only.
3. **Never re-adjudicate gate verdicts** — source doc verdicts are authoritative.
4. **No cross-agent coordination** — each agent writes independently. For iterative 2-agent exchanges, use `/rclab-workshop`.
5. **Never initiate shutdown** — user decides.
6. **Project-specific framing** — if the selected discipline pack installed a framework-framing rule, it applies.

## Error Handling

| Condition | Action |
|:----------|:-------|
| No source docs | Show usage and stop |
| Source doc missing | Report which, stop |
| No `--agents` | Show usage and stop |
| Agent type invalid | List available types, stop |
| Output collision | Ask: overwrite / rename / cancel |
| Agent fails to produce output | Report, suggest different agent |
