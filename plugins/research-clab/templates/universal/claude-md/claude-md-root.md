# {{PROJECT_NAME}} — Project Instructions

<!-- DEPLOY: project-root/CLAUDE.md -->
<!-- LEAN: universal orientation only. Project structure, team pointers, output discipline. -->
<!-- Hardware specs → .claude/rules/computation-environment.md (conditional) -->
<!-- MCP configs → .claude/rules/ (conditional) -->
<!-- Behavioral rules → .claude/rules/ (8 files, auto-loaded) -->
<!-- Agent roster → .claude/templates/agent-roster.md -->

## READ TOOL BYTE LIMIT — SILENT FAILURES

The Read tool silently fails when a requested byte range exceeds ~30KB. When it fails, the tool returns nothing and you get no error message.

- **Small files (<30KB)**: Read without a `limit` parameter — the default (2000 lines) is fine. Don't chunk what fits in one read.
- **Large files (>30KB)**: Use `limit` to stay under ~30KB per read. Estimate from file size: a 90KB file needs ~3 reads.
- **If a Read returns nothing**: The range was too large in bytes. Halve the `limit` and retry. Do NOT skip the section.
- **Don't guess line counts for density** — check file size first if unsure (`wc -c` or `du -b`).

## PATH CAVEATS — SPACES IN PROJECT ROOT

If `{{PROJECT_ROOT}}` contains a space, shell commands break without careful quoting:

- **Write tool**: Use the full path — the JSON parameter handles spaces fine.
- **Bash tool**: ALWAYS double-quote any path containing the project root. Unquoted paths split on the space and silently fail.
- **NEVER** fall back to Bash `echo > path` or `cat > path` for file writing — use the Write tool. The space in the path will eat your output.

(Ignore this section if your project root has no spaces.)

## Verify Working Directory

Before any operation, confirm you are in the project root:

```
pwd
# Expected: {{PROJECT_ROOT}}
```

If not, navigate there first. All paths in this project are relative to this root.

## Project Structure

```
{{PROJECT_NAME}}/
├── .claude/                    # Claude Code infrastructure
│   ├── agents/                 # Agent definitions (*.md)
│   ├── agent-memory/           # Per-agent persistent memory
│   ├── skills/                 # Slash command definitions
│   ├── rules/                  # Modular behavioral rules (auto-loaded)
│   ├── hooks/                  # Tool hooks (optional)
│   ├── settings.json           # Shared settings (committed)
│   └── settings.local.json     # Personal settings (gitignored)
├── researchers/                # Reference corpora — one folder per domain
│   └── {{DOMAIN}}/             # 10-14 markdown papers per domain
├── sessions/                   # All session outputs, chronological
│   ├── session-NN/             # Per-session subdirectories
│   ├── session-plan/           # Prompts, plans, agendas, handoffs
│   └── framework/              # Cross-session mechanism discussions
├── tools/                      # Knowledge index infrastructure
│   ├── knowledge-index.json    # Canonical knowledge graph (generated)
│   ├── knowledge.db            # SQLite accelerator (rebuilt from JSON)
│   └── viz/                    # Generated visualizations
├── {{COMPUTATION_DIR}}/        # Computation scripts + outputs (remove if not needed)
├── {{SIMULATION_DIR}}/         # Simulation codebase + venv (remove if not needed)
├── artifacts/                  # Source materials (PDFs, primary docs)
├── CLAUDE.md                   # This file
├── CLAUDE.local.md             # Personal overrides (gitignored)
└── agents.md                   # Agent & skill registry (human-readable)
```

{{if-compute}}
## Computation Environment

Hardware specs and Python environment details are in a conditional rule at `.claude/rules/computation-environment.md` — loaded only when touching computation files.

{{fragment-slot:computation-environment}}
{{endif-compute}}

## Reference Data

{{fragment-slot:reference-data}}

## Knowledge Index

The knowledge index is the project's institutional memory.

- **Single source of truth**: `tools/knowledge-index.json`
- **Query interface**: `/weave` slash command
- **Rebuild**: `/weave --update` (only the `indexer` agent writes the index)
- **SQLite accelerator**: `tools/knowledge.db` — rebuilt via `/weave --db-sync`

{{fragment-slot:knowledge-query-discipline}}

## Behavioral Rules

Rules live in `.claude/rules/` (plus `team-lead-behavior.md` at the project root, kept outside `rules/` so subagents do not auto-load it). The universal harness ships a baseline set; the selected discipline pack may add or override specific rules.

These rules load automatically — always-on rules at session start, path-scoped rules when entering the relevant directory. Do not enumerate them here; the set drifts as the project evolves. Browse `.claude/rules/` directly to see what is currently installed.

## Agent Roster

See `.claude/templates/agent-roster.md` for the canonical agent name-to-type mapping.

Three infrastructure agents ship with every project (coordinator, indexer, scout). Domain agents are added via `/new-researcher`.

## Personal Overrides

`CLAUDE.local.md` (gitignored) is for personal preferences that don't affect the team:

- Editor quirks, shell preferences, display settings
- Personal workflow shortcuts
- Machine-specific paths or environment variables

Never put shared project rules in `CLAUDE.local.md`.

## Team Management

- Follow `team-lead-behavior.md` (project root — NOT in `.claude/rules/` so subagents don't auto-load it).
- Follow `.claude/skills/rclab-*` skill directions when invoked.
- Be shutdown-adverse: the user decides when the team stops.

## Output File Discipline

- Only ONE agent writes the output file per round (designated in the prompt).
- Other agents contribute via SendMessage to the designated writer.
- Do NOT write to the output file unless you are the designated writer.
