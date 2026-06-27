# .claude/skills/ — Slash Command Definitions

<!-- DEPLOY: project-root/.claude/skills/CLAUDE.md -->

Each subdirectory here defines a slash command. The directory name becomes the command name — `skills/weave/SKILL.md` creates the `/weave` command.

## Structure

Each installed skill is one subdirectory containing a `SKILL.md`:

```
skills/
├── <skill-name>/
│   └── SKILL.md
└── ...
```

The actual set of skills installed depends on the scaffold: the universal harness ships a baseline (weave, shortterm, rclab-*, librarian, new-researcher, redact, paper, pdf, rebuild-library), and the selected discipline pack may add more. To see what's installed, run `ls .claude/skills/` or check the "Skills" section of `agents.md` at the project root.

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

## Installed Skills

The set of installed skills depends on the scaffold (universal baseline + any discipline pack additions). To see the current installed set, inspect `.claude/skills/` directly or read the Skills table in `agents.md` at the project root. Only `/weave` is strictly required; everything else is recommended or optional.

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
