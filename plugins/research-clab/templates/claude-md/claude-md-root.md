# {{PROJECT_NAME}} — Project Instructions

<!-- DEPLOY: project-root/CLAUDE.md -->
<!-- This is the constitution. Every agent inherits these rules. -->
<!-- Behavioral rules are factored into .claude/rules/ for modularity. -->
<!-- Target: under 200 lines. Detailed rules live in .claude/rules/*.md -->

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

## Simulation Environment

### Hardware

{{HARDWARE_SPECS}}

### Python Environment

{{PYTHON_ENV_INSTRUCTIONS}}

## Knowledge Index

The knowledge index is the project's institutional memory.

- **Single source of truth**: `tools/knowledge-index.json`
- **Query interface**: `/weave` slash command
- **Rebuild**: `/weave --update` (only the `librarian` agent writes the index)
- **SQLite accelerator**: `tools/knowledge.db` — rebuilt via `/weave --db-sync`

## Behavioral Rules

Team behavior, epistemic discipline, and output standards are defined in `.claude/rules/`:

| Rule File | Scope | What It Covers |
|:----------|:------|:---------------|
| `team-lead-behavior.md` | Always | Orchestration rules, blast-first spawn, what leads don't do |
| `teammate-behavior.md` | Always | Inbox discipline, message routing, team lead shutdown compliance |
| `epistemic-discipline.md` | Always | Pre-registration, constraint methodology, source authority, confidence rules |
| `output-standards.md` | Always | Action item format, handoff document structure, output rules |
| `gate-verdicts.md` | Always | Pre-registration protocol, verdict format, permanence |
| `session-handoffs.md` | `sessions/**` | Session naming, mandatory handoffs, chronological integrity |

These rules load automatically — always-on rules at session start, path-scoped rules when entering the relevant directory.

## Infrastructure Agents

Three agents are required in every project. They do NOT do research.

| Agent | Role | Hard Boundary |
|:------|:-----|:-------------|
| `coordinator` | Orchestrates, writes minutes, maintains constraint map | Does NOT do domain analysis |
| `librarian` | Indexes, queries, serves knowledge graph | Does NOT evaluate content |
| `scout` | Fetches papers, populates researcher folders | Does NOT analyze or interpret |

## Personal Overrides

`CLAUDE.local.md` (gitignored) is for personal preferences that don't affect the team:

- Editor quirks, shell preferences, display settings
- Personal workflow shortcuts
- Machine-specific paths or environment variables

Never put shared project rules in `CLAUDE.local.md`.
