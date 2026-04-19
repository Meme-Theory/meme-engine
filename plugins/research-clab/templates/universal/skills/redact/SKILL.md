---
name: redact
description: Remove all agent-memory references to a session, mechanism, or identifier
argument-hint: <identifier> [--dry-run] [--keep <file>] [--keep-all-detail]
---

# Redact — Purge Agent Memory References

Remove all references to a given identifier (session ID, mechanism name, etc.) from agent memory files. Project files (sessions/, tier0-computation/, constraint-map) are preserved — only `.claude/agent-memory/` is touched.

## Usage

```
/redact 29Ac                          # Remove all memory references to "29Ac"
/redact 29Ac --dry-run                # Show what would be removed, don't edit
/redact "rolling quintessence"        # Remove references to a mechanism name
/redact 21b --keep constraint-map.md  # Skip constraint-map (already default)
/redact 29Ac --keep-all-detail        # Only touch MEMORY.md files, skip detail files
```

## Parse Arguments

1. Extract `<identifier>` — the first argument (or quoted multi-word string).
2. Extract flags:
   - `--dry-run`: Preview only, no edits.
   - `--keep <file>`: Skip files whose basename matches `<file>`. Multiple `--keep` flags allowed.
   - `--keep-all-detail`: Only edit files named `MEMORY.md`. Skip all other `.md` files in agent-memory dirs.
3. If no identifier provided, show the usage block above and stop.

## Implementation Steps

### Step 1: Scan

Use the Grep tool to search for `<identifier>` (case-insensitive) across all files matching the glob `.claude/agent-memory/**/*.md`.

Collect all matching files and their line numbers. Use `output_mode: "content"` with line numbers enabled to see exact matches.

If zero matches found, report:
```
=== REDACT: "<identifier>" ===
Scanned: .claude/agent-memory/**/*.md
Matches: 0

Nothing to redact.
```
Stop here.

### Step 2: Filter files

Remove from the match list:
- Any file whose basename is `constraint-map.md` (default preserve — constraint-map is reference data that survives redaction).
- Any file matching a `--keep <file>` argument (basename comparison).
- If `--keep-all-detail`: any file NOT named `MEMORY.md`.

Track kept files separately — they will appear in the final report as "KEPT".

### Step 3: Classify removals

For each remaining file with matches, read the full file using the Read tool. Classify each match into one of:

**a) Section removal**: If the match falls inside a section (delimited by `##` or `###` headers) where ALL or MOST content is about the identifier, mark the entire section (header through to next header or EOF) for removal.

**b) Line removal**: If the match is a single line within a larger section that covers multiple topics, mark just that line for removal. This includes:
- Bullet points (`- ...`)
- Numbered list items (`1. ...`)
- Standalone sentences

**c) Table row removal**: If the match is inside a markdown table (`| ... |`), mark just that row for removal. Never remove the header row or separator row.

**d) Multi-reference line — FLAG**: If a line contains BOTH the identifier AND other substantive, unrelated content (e.g., mentions both `29Ac` and `29Ab` with distinct information about each), do NOT remove it. Flag it for manual review in the report.

**Key rules:**
- Look for related file path references too: `sessions/session-XX/`, `sXX_*.py`, `sXX_*.npz`, `sXX_*.png`, `sXX_gate_verdicts.txt` where XX maps to the identifier.
- When removing a section, also remove any blank line immediately after the section that would create a double-blank-line.
- When removing a list item, if it was the last item under a header, also remove the now-empty header.
- Never remove the file's top-level `#` title header.

### Step 4: Preview

Build a summary table showing what will be changed:

```
=== REDACT: "<identifier>" ===
Scanned: N agent memory files across M agents
Matches: X references in Y files

  agent/MEMORY.md ................. remove §Section Name (K lines)
  agent/detail-file.md ............ remove 2 lines from §Other Section
  agent2/MEMORY.md ................ remove 1 table row (1 line)
  agent3/MEMORY.md ................ FLAG: line N contains mixed refs (manual review)
  constraint-map.md ............... KEPT (default preserve)
```

If `--dry-run`, display this summary and stop. Do not make any edits.

### Step 5: Execute edits

For each file with removals:

1. Use the Edit tool to remove the identified sections/lines.
2. Work from bottom-to-top within each file (highest line numbers first) to avoid offset drift.
3. After all removals, clean up artifacts:
   - Collapse any resulting triple-or-more blank lines down to a single blank line.
   - Remove any orphaned section headers (headers with no content before the next header).

### Step 6: Verify

Use the Grep tool to re-scan for `<identifier>` across all `.claude/agent-memory/**/*.md` files.

- References in kept files (constraint-map, --keep targets) are expected — report them as "remaining (kept)".
- References in edited files indicate incomplete removal — report them as "WARNING: residual reference".
- Flagged multi-reference lines are expected — report them as "remaining (flagged for manual review)".

### Step 7: Report

Show the final summary:

```
Before: NNNN lines across N files
After:  NNNN lines across N files
Removed: NN lines (N.N%)
Remaining: N references in kept/flagged files
```

If any files were flagged for manual review, list them with line numbers:
```
Manual review needed:
  agent/MEMORY.md:42 — mentions both "29Ac" and "29Ab"
```

## Safety Rules

1. **NEVER touch files outside `.claude/agent-memory/`** — sessions/, tier0-computation/, researchers/, tools/ are untouchable.
2. **NEVER remove a line containing other valuable data** — flag it for manual review instead.
3. **NEVER remove constraint-map.md content by default** — it's reference data. Only remove if the user explicitly passes `--no-preserve-constraint-map` (not a standard flag — they'd need to explicitly ask).
4. **Section-level granularity preferred** — removing a whole section is cleaner than leaving an orphaned header with one remaining bullet.
5. **Table integrity** — never remove a table's header row or separator row. Only remove data rows.
6. **Preserve file structure** — every file should still have its `#` title after redaction. If redaction would empty a file entirely, leave the title and a single line: `<!-- Redacted: all content referenced <identifier> -->`.

## Error Handling

- If `.claude/agent-memory/` directory doesn't exist: report error and stop.
- If identifier is empty: show usage and stop.
- If identifier is too short (1-2 chars): warn that this may match broadly and ask for confirmation before proceeding.
- If `--keep` file doesn't exist in the match list: silently ignore (it just means there were no matches in that file).
