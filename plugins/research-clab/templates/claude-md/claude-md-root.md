# {{PROJECT_NAME}} — Project Instructions

<!-- DEPLOY: project-root/CLAUDE.md -->
<!-- LEAN: universal orientation only. Project structure, team pointers, output discipline. -->
<!-- Hardware specs → .claude/rules/computation-environment.md (conditional) -->
<!-- MCP configs → .claude/rules/ (conditional) -->
<!-- Behavioral rules → .claude/rules/ (8 files, auto-loaded) -->
<!-- Agent roster → .claude/templates/agent-roster.md -->

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

## Computation Environment

Hardware specs and Python environment details are in a conditional rule at `.claude/rules/computation-environment.md` — loaded only when touching computation files. If this project has no computation directory, that rule will not exist.

## Knowledge Index

The knowledge index is the project's institutional memory.

- **Single source of truth**: `tools/knowledge-index.json`
- **Query interface**: `/weave` slash command
- **Rebuild**: `/weave --update` (only the `indexer` agent writes the index)
- **SQLite accelerator**: `tools/knowledge.db` — rebuilt via `/weave --db-sync`

## Behavioral Rules

See `.claude/rules/` for behavioral rules (8 files: epistemic-discipline, output-standards, gate-verdicts, session-handoffs, teammate-behavior, agent-standards, evoi-prioritization, and team-lead-behavior outside rules/ to avoid subagent auto-loading).

These rules load automatically — always-on rules at session start, path-scoped rules when entering the relevant directory.

## Agent Roster

See `.claude/templates/agent-roster.md` for the canonical agent name-to-type mapping.

Three infrastructure agents ship with every project (coordinator, indexer, scout). Domain agents are added via `/new-researcher`.

## Personal Overrides

`CLAUDE.local.md` (gitignored) is for personal preferences that don't affect the team:

- Editor quirks, shell preferences, display settings
- Personal workflow shortcuts
- Machine-specific paths or environment variables

Never put shared project rules in `CLAUDE.local.md`.
