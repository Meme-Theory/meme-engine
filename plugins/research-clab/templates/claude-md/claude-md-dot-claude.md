# .claude/ — Infrastructure Directory

<!-- DEPLOY: project-root/.claude/CLAUDE.md -->

This directory contains all Claude Code infrastructure for the research project. It is the engine room — agents, memory, skills, settings, and hooks all live here.

## Directory Layout

```
.claude/
├── agents/              # Agent definition files (*.md)
├── agent-memory/        # Per-agent persistent memory directories
├── rules/               # Modular behavioral rules (auto-loaded)
├── skills/              # Slash command definitions (SKILL.md per skill)
├── hooks/               # Tool hooks (optional, auto-executed)
├── settings.json        # Shared settings (committed to VCS)
├── settings.local.json  # Personal settings (gitignored)
└── settings.md          # Human-readable hook documentation
```

## Rules

- **Agent definitions and their memory directories must share names** — if you create `agents/foo.md`, its memory lives at `agent-memory/foo/MEMORY.md`
- **Skills follow the `{name}/SKILL.md` convention** — one directory per skill, one `SKILL.md` inside
- **This directory is infrastructure, not content** — no research papers, session outputs, or computation results belong here
- **`settings.json` is shared** (committed); **`settings.local.json` is personal** (gitignored)
- **Rules in `rules/` load automatically** — always-on rules at startup, path-scoped rules when entering matching directories

## What Each Subdirectory Does

| Directory | Purpose | Who Writes |
|:----------|:--------|:-----------|
| `agents/` | Agent identity, methodology, directives | User or `/new-researcher` |
| `agent-memory/` | Persistent cross-session state per agent | Each agent writes its own |
| `rules/` | Modular behavioral rules (team, epistemic, output) | User or coordinator |
| `skills/` | Slash command implementations | User or coordinator |
| `hooks/` | Automated triggers on tool use | User |

## Settings Files

| File | Scope | Committed? | Purpose |
|:-----|:------|:-----------|:--------|
| `settings.json` | All team members | Yes | Shared permissions, hooks, deny rules |
| `settings.local.json` | You only | No (gitignored) | Personal overrides, machine-specific paths |
| `settings.md` | Documentation | Yes | Human-readable explanation of each hook and permission |

## Adding New Components

- **New agent**: Create `agents/{name}.md` + `agent-memory/{name}/MEMORY.md`
- **New skill**: Create `skills/{name}/SKILL.md`
- **New rule**: Create `rules/{name}.md` — add `paths:` frontmatter for directory scoping, or omit for always-on
- **New permission**: Add to `settings.json` under `permissions.allow` (shared) or `settings.local.json` (personal)
- **New hook**: Add to `settings.json` under `hooks` — document it in `settings.md`
