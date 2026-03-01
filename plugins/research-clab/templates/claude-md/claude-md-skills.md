# .claude/skills/ — Slash Command Definitions

<!-- DEPLOY: project-root/.claude/skills/CLAUDE.md -->

Each subdirectory here defines a slash command. The directory name becomes the command name — `skills/weave/SKILL.md` creates the `/weave` command.

## Structure

```
skills/
├── weave/
│   └── SKILL.md        # /weave — Knowledge index queries and maintenance
├── shortterm/
│   └── SKILL.md        # /shortterm — Memory collapse and optimization
├── clab-review/
│   └── SKILL.md        # /clab-review — Multi-agent document review
├── clab-team/
│   └── SKILL.md        # /clab-team — Full team orchestration launcher
├── clab-plan/
│   └── SKILL.md        # /clab-plan — Session plan & prompt generator
├── redact/
│   └── SKILL.md        # /redact — Memory purge for stale references
├── document-prep/
│   └── SKILL.md        # /document-prep — Format-aware document toolkit
├── new-researcher/
│   └── SKILL.md        # /new-researcher — Create new agent with web-fetched papers
├── indexing/
│   └── SKILL.md        # /indexing — Build structured index for any folder
├── team-blast/
│   └── SKILL.md        # /team-blast — Direct-write broadcast to team inboxes
└── {{DOMAIN_SKILL}}/
    └── SKILL.md        # Domain-specific skills (optional)
```

## SKILL.md Format

```yaml
---
name: skill-name
description: One-line description shown in skill list
argument-hint: --flag1 | --flag2 <arg> | --flag3
---
```

The body contains the complete instruction set Claude follows when the user invokes the command:

1. **Argument parsing rules** — how to interpret flags and arguments
2. **Subcommand implementations** — exact tool sequences for each subcommand
3. **Output formatting** — how to present results
4. **Error handling** — what to do when things fail

## Required Skills

| Skill | Purpose | Priority |
|:------|:--------|:---------|
| `/weave` | Query and maintain the knowledge index | **Required** |
| `/shortterm` | Collapse and optimize agent memory | Recommended |
| `/clab-review` | Multi-agent document review (fan-out + synthesis) | Recommended |
| `/clab-team` | Full team launcher from session prompt | Recommended |
| `/clab-plan` | Session plan & prompt generator from topic | Recommended |
| `/redact` | Purge stale memory references | Optional |
| `/document-prep` | Format-aware document toolkit (templates, notation, checking) | Recommended |
| `/new-researcher` | Create new agent with web-fetched papers | Recommended |
| `/indexing` | Build structured index for researcher or general folder | Recommended |
| `/team-blast` | Direct-write broadcast to team agent inboxes | Optional |

## Rules

- **One SKILL.md per directory** — no multi-skill files
- **Directory name = command name** — `foo/SKILL.md` creates `/foo`
- **Skills are instructions, not agents** — a skill tells Claude what to DO, an agent tells Claude what to BE
- **Domain-specific skills are optional** — only `/weave` is strictly required
- **Skills should not duplicate agent capabilities** — if an agent already does something, don't also make a skill for it

## Progressive Disclosure — 3-Tier Token Management

Skills use a progressive disclosure model to minimize token consumption:

| Tier | What Loads | When | Token Budget |
|:-----|:-----------|:-----|:-------------|
| **Tier 1 — Metadata** | `name` + `description` from YAML frontmatter | Always, at session start | ~100 tokens per skill |
| **Tier 2 — Instructions** | Full `SKILL.md` body | When Claude determines the skill is relevant | Target < 5,000 tokens |
| **Tier 3 — Resources** | Additional files in the skill directory | When explicitly referenced from SKILL.md | Unlimited |

### Implications for Skill Authors

- **Invest heavily in `name` and `description`** — these are the only things Claude sees when deciding whether to load your skill
- **Keep `SKILL.md` under 5K tokens** — if it's longer, factor detailed reference material into separate files in the same directory
- **Use `@path/to/resource` imports** for Tier 3 content — Claude loads these on demand, not upfront
- **Set `disable-model-invocation: true`** for skills with side effects — forces manual `/skill-name` invocation instead of auto-activation

## Adding a New Skill

1. Create directory: `.claude/skills/{name}/`
2. Write `SKILL.md` with YAML frontmatter + implementation body
3. For large skills, split into `SKILL.md` (< 5K tokens) + resource files (Tier 3)
4. Test by invoking `/{name}` in a conversation
5. Add to `agents.md` registry at project root
