# Unfold: Project Structure

**Target agent**: Coordinator
**Task**: Create the full directory tree, install CLAUDE.md files, copy skills, configure settings.
**Inputs**: Project name, domain, target output format, hardware specs (optional).
**Reads from**: `${CLAUDE_PLUGIN_ROOT}/templates/claude-md/`, `${CLAUDE_PLUGIN_ROOT}/skills/`

---

## Step 1: Create the Directory Tree

Create this exact structure under the project root. Every directory listed here MUST exist before proceeding to Step 2.

```
{project-root}/
├── .claude/
│   ├── agents/
│   ├── agent-memory/
│   ├── skills/
│   │   ├── weave/
│   │   ├── shortterm/
│   │   ├── clab-review/
│   │   ├── clab-team/
│   │   ├── clab-plan/
│   │   ├── redact/
│   │   ├── document-prep/
│   │   ├── new-researcher/
│   │   ├── librarian/
│   │   ├── team-blast/
│   │   └── clab-synthesis/
│   ├── templates/
│   │   ├── agent-templates/
│   │   └── session-templates/
│   └── rules/
├── researchers/
├── sessions/
│   ├── session-plan/
│   ├── framework/
│   └── misc/
├── tools/
│   └── viz/
└── artifacts/
    ├── source/
    └── document-templates/    # Installed by unfold-document-prep.md
```

**Do NOT create** a simulation directory yet — that's domain-dependent and happens later if the user needs computation infrastructure.
**Do NOT create** `document-templates/` subdirectories here — that's handled by `unfold-document-prep.md` based on the user's format selection.

---

## Step 2: Install CLAUDE.md Files

Each directory gets a scoped CLAUDE.md that tells agents what belongs there and how to behave. Read the templates from `${CLAUDE_PLUGIN_ROOT}/templates/claude-md/` and write them into the project, substituting project-specific values.

| Template Source | Install To | Substitutions |
|:----------------|:-----------|:-------------|
| `claude-md-root.md` | `{root}/CLAUDE.md` | Project name, domain, project root path |
| `claude-md-dot-claude.md` | `.claude/CLAUDE.md` | None (generic) |
| `claude-md-agents.md` | `.claude/agents/CLAUDE.md` | None (generic) |
| `claude-md-agent-memory.md` | `.claude/agent-memory/CLAUDE.md` | None (generic) |
| `claude-md-skills.md` | `.claude/skills/CLAUDE.md` | None (generic) |
| `claude-md-researchers.md` | `researchers/CLAUDE.md` | None (generic) |
| `agents-md-researchers.md` | `researchers/agents.md` | None (generic) |
| `claude-md-sessions.md` | `sessions/CLAUDE.md` | None (generic) |
| `claude-md-sessions-plan.md` | `sessions/session-plan/CLAUDE.md` | None (generic) |
| `claude-md-sessions-framework.md` | `sessions/framework/CLAUDE.md` | None (generic) |
| `claude-md-tools.md` | `tools/CLAUDE.md` | None (generic) |
| `claude-md-artifacts.md` | `artifacts/CLAUDE.md` | None (generic) |

### Root CLAUDE.md — the most important file

The root CLAUDE.md is the project constitution — LEAN, universal orientation only. Read `claude-md-root.md` as a template, then generate the real file with these sections filled in:

1. **Project Name & Domain** — from user input
2. **Verify Working Directory** — `pwd` check with the actual project path
3. **Project Structure** — the directory tree from Step 1
4. **Computation Environment** — pointer to conditional rule (hardware/python live there, not here)
5. **Knowledge Index** — boilerplate about `/weave` (copy from template)
6. **Behavioral Rules** — pointer to `.claude/rules/` (8 files)
7. **Agent Roster** — pointer to `.claude/templates/agent-roster.md`
8. **Personal Overrides** — `CLAUDE.local.md` guidance

---

## Step 3: Install Behavioral Rules

Copy rule files from `${CLAUDE_PLUGIN_ROOT}/templates/claude-md/rules/` into `.claude/rules/`:

| Source | Install To | Purpose |
|:-------|:-----------|:--------|
| `team-lead-behavior.md` | `.claude/rules/team-lead-behavior.md` | Don't over-manage, shut down agents when done, never self-terminate |
| `teammate-behavior.md` | `.claude/rules/teammate-behavior.md` | Inbox first, message discipline |
| `epistemic-discipline.md` | `.claude/rules/epistemic-discipline.md` | Evidence hierarchy, what counts as a result |
| `output-standards.md` | `.claude/rules/output-standards.md` | Formatting, precision requirements |
| `gate-verdicts.md` | `.claude/rules/gate-verdicts.md` | How to classify constraint gate outcomes |
| `session-handoffs.md` | `.claude/rules/session-handoffs.md` | How to write handoff documents |

These are universal — no substitutions needed.

---

## Step 4: Copy Skills

Copy each skill's `SKILL.md` from `${CLAUDE_PLUGIN_ROOT}/skills/` into `.claude/skills/`. Skills are direct-load assets (not templates) — they ship as-is with the plugin.

```
${CLAUDE_PLUGIN_ROOT}/skills/weave/SKILL.md              → .claude/skills/weave/SKILL.md
${CLAUDE_PLUGIN_ROOT}/skills/shortterm/SKILL.md          → .claude/skills/shortterm/SKILL.md
${CLAUDE_PLUGIN_ROOT}/skills/clab-review/SKILL.md      → .claude/skills/clab-review/SKILL.md
${CLAUDE_PLUGIN_ROOT}/skills/clab-team/SKILL.md        → .claude/skills/clab-team/SKILL.md
${CLAUDE_PLUGIN_ROOT}/skills/clab-plan/SKILL.md        → .claude/skills/clab-plan/SKILL.md
${CLAUDE_PLUGIN_ROOT}/skills/redact/SKILL.md             → .claude/skills/redact/SKILL.md
${CLAUDE_PLUGIN_ROOT}/skills/document-prep/SKILL.md      → .claude/skills/document-prep/SKILL.md
${CLAUDE_PLUGIN_ROOT}/skills/new-researcher/SKILL.md     → .claude/skills/new-researcher/SKILL.md
${CLAUDE_PLUGIN_ROOT}/skills/librarian/SKILL.md          → .claude/skills/librarian/SKILL.md
${CLAUDE_PLUGIN_ROOT}/skills/team-blast/SKILL.md         → .claude/skills/team-blast/SKILL.md
${CLAUDE_PLUGIN_ROOT}/skills/clab-synthesis/SKILL.md     → .claude/skills/clab-synthesis/SKILL.md
```

---

## Step 4b: Copy Session Templates

Copy the session format reference docs from `${CLAUDE_PLUGIN_ROOT}/templates/session-templates/` into `.claude/templates/session-templates/`. These are the format definitions (A through I) that agents consult when planning and running sessions.

```
${CLAUDE_PLUGIN_ROOT}/templates/session-templates/A-first-contact-review.md       → .claude/templates/session-templates/A-first-contact-review.md
${CLAUDE_PLUGIN_ROOT}/templates/session-templates/B-adversarial-debate.md          → .claude/templates/session-templates/B-adversarial-debate.md
${CLAUDE_PLUGIN_ROOT}/templates/session-templates/C-collaborative-deep-dive.md     → .claude/templates/session-templates/C-collaborative-deep-dive.md
${CLAUDE_PLUGIN_ROOT}/templates/session-templates/D-workshop.md                    → .claude/templates/session-templates/D-workshop.md
${CLAUDE_PLUGIN_ROOT}/templates/session-templates/E-investigation-arc.md           → .claude/templates/session-templates/E-investigation-arc.md
${CLAUDE_PLUGIN_ROOT}/templates/session-templates/F-decisive-computation.md        → .claude/templates/session-templates/F-decisive-computation.md
${CLAUDE_PLUGIN_ROOT}/templates/session-templates/G-mass-parallel-assessment.md    → .claude/templates/session-templates/G-mass-parallel-assessment.md
${CLAUDE_PLUGIN_ROOT}/templates/session-templates/H-decision-gate.md              → .claude/templates/session-templates/H-decision-gate.md
${CLAUDE_PLUGIN_ROOT}/templates/session-templates/I-formalization.md               → .claude/templates/session-templates/I-formalization.md
${CLAUDE_PLUGIN_ROOT}/templates/session-templates/00-infrastructure.md             → .claude/templates/session-templates/00-infrastructure.md
${CLAUDE_PLUGIN_ROOT}/templates/session-templates/supporting-documents.md          → .claude/templates/session-templates/supporting-documents.md
```

These are verbatim copies — no substitutions needed. The selection guide is NOT copied here (it goes to `sessions/session-plan/format-selection-guide.md` in unfold-methodology Step 1).

---

## Step 4c: Copy Agent Templates

Copy the agent archetype templates from `${CLAUDE_PLUGIN_ROOT}/templates/agent-templates/` into `.claude/templates/agent-templates/`. These are the cognitive archetype definitions that `/new-researcher` reads when stamping new domain agents.

```
${CLAUDE_PLUGIN_ROOT}/templates/agent-templates/skeptic.md          → .claude/templates/agent-templates/skeptic.md
${CLAUDE_PLUGIN_ROOT}/templates/agent-templates/calculator.md       → .claude/templates/agent-templates/calculator.md
${CLAUDE_PLUGIN_ROOT}/templates/agent-templates/workhorse.md        → .claude/templates/agent-templates/workhorse.md
${CLAUDE_PLUGIN_ROOT}/templates/agent-templates/principalist.md     → .claude/templates/agent-templates/principalist.md
${CLAUDE_PLUGIN_ROOT}/templates/agent-templates/dreamer.md          → .claude/templates/agent-templates/dreamer.md
${CLAUDE_PLUGIN_ROOT}/templates/agent-templates/boundary-guard.md   → .claude/templates/agent-templates/boundary-guard.md
${CLAUDE_PLUGIN_ROOT}/templates/agent-templates/observer.md         → .claude/templates/agent-templates/observer.md
${CLAUDE_PLUGIN_ROOT}/templates/agent-templates/bridge.md           → .claude/templates/agent-templates/bridge.md
${CLAUDE_PLUGIN_ROOT}/templates/agent-templates/formatter.md        → .claude/templates/agent-templates/formatter.md
${CLAUDE_PLUGIN_ROOT}/templates/agent-templates/generalist.md       → .claude/templates/agent-templates/generalist.md
```

These are verbatim copies — no substitutions needed. `/new-researcher` resolves templates from `.claude/templates/agent-templates/` at runtime, so the project is self-contained after scaffolding.

---

## Step 4c-ii: Copy Agent Roster Template

Copy the agent roster from `${CLAUDE_PLUGIN_ROOT}/templates/agent-roster.md` into `.claude/templates/`:

```
${CLAUDE_PLUGIN_ROOT}/templates/agent-roster.md → .claude/templates/agent-roster.md
```

This is a verbatim copy — no substitutions needed. `/new-researcher` appends new domain agents to this file as they are created. The root CLAUDE.md references this file for name-to-type resolution.

---

## Step 4d: Install Document Templates

**READ**: `${CLAUDE_PLUGIN_ROOT}/project-origami/unfold-document-prep.md` and execute it.

This step installs format-specific document templates into `artifacts/document-templates/` based on the user's `{output-format}` selection (Question 4). For LaTeX projects, this installs 13 `.tex` templates (paper, poster, slides, thesis, report, etc.) and a sample `.bib` file. For Typst and Markdown, it installs placeholder READMEs.

The `/document-prep --new <type>` command discovers these templates at runtime.

---

## Step 5: Install Settings

### 5a: Install `settings.json` (shared, committed)

Read the template from `${CLAUDE_PLUGIN_ROOT}/templates/claude-md/claude-md-settings-json.md` and write the JSON block to `.claude/settings.json`. This file includes:

- `env.CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` — **required** for agent team functionality
- Shared permissions (research domain whitelists, deny rules for credentials)
- PostToolUse hooks for session file tracking

If the user specified additional web domains for research, add `WebFetch(domain:...)` entries to the allow list.

### 5b: Install `settings.local.json` (personal, gitignored)

Generate `.claude/settings.local.json` with:

```json
{
  "permissions": {
    "allow": [
      "Bash(timeout:*)"
    ]
  }
}
```

If a Python environment was identified, add `Bash("{python-path}":*)`.

---

## Step 6: Install Infrastructure Agents

Copy the 3 infrastructure agents from `${CLAUDE_PLUGIN_ROOT}/templates/infrastructure-agents/` into `.claude/agents/`:

```
${CLAUDE_PLUGIN_ROOT}/templates/infrastructure-agents/coordinator.md → .claude/agents/coordinator.md
${CLAUDE_PLUGIN_ROOT}/templates/infrastructure-agents/indexer.md   → .claude/agents/indexer.md
${CLAUDE_PLUGIN_ROOT}/templates/infrastructure-agents/scout.md       → .claude/agents/scout.md
```

**Variable substitution**: After copying, replace `{{PROJECT_NAME}}` with the actual project name in `indexer.md` (2 occurrences: YAML description and agent intro paragraph) and `scout.md` (3 occurrences: Connection section header, generation phase template, cross-domain interaction pattern). `coordinator.md` has no template variables — copy verbatim.

Create agent-memory stubs for each:

```
.claude/agent-memory/coordinator/MEMORY.md  (empty — "# Coordinator Memory\n")
.claude/agent-memory/indexer/MEMORY.md    (empty — "# Indexer Memory\n")
.claude/agent-memory/scout/MEMORY.md        (empty — "# Scout Memory\n")
```

---

## Step 7: Create Root Registry

Generate `agents.md` at project root — a human-readable quick-reference:

```markdown
# {Project Name} — Agent & Skill Registry

## Agents

### Infrastructure

| Agent | Type | Role |
|:------|:-----|:-----|
| coordinator | sonnet | Orchestrates teams, writes minutes, maintains constraints |
| indexer | sonnet | Indexes knowledge, serves queries |
| scout | haiku | Fetches papers, archives sources |

### Domain Specialists

(None yet — use `/new-researcher` to add domain agents)

## Skills

| Skill | Description |
|:------|:------------|
| `/weave` | Query and maintain the knowledge index |
| `/shortterm` | Collapse and optimize agent memory files |
| `/clab-review` | Multi-agent collaborative document review |
| `/clab-team` | Launch coordinated research team from session prompt |
| `/clab-plan` | Generate session plans and prompts from a topic |
| `/redact` | Remove agent-memory references to a session or identifier |
| `/document-prep` | Format-aware document toolkit |
| `/new-researcher` | Create a new domain agent with web-fetched papers |
| `/librarian` | Build structured index for researcher or general folder |
| `/team-blast` | Direct-write broadcast to team agent inboxes |
| `/clab-synthesis` | Generate synthesis or fusion documents from source docs |
```

---

## Step 8: Create .gitignore

Generate `.gitignore` at project root:

```
# Python
__pycache__/
*.pyc
.venv*/

# Generated data
tools/knowledge.db
tools/viz/
*.npz

# IDE
.vscode/
.idea/

# Claude Code runtime
.claude/teams/
.claude/tasks/

# OS
.DS_Store
Thumbs.db

# Artifacts (large downloads)
artifacts/source/*.pdf
```

---

## Step 9: Create Session-0 Prompt

Generate the first session prompt at `sessions/session-plan/session-0-prompt.md`:

```markdown
# Session 0: Initial Domain Assessment

**Date**: {today}
**Project**: {project-name}
**Domain**: {domain}
**Format**: First Contact Review (Format A)

## Research Question

{user's initial research question}

## Objectives

1. Survey the current state of knowledge in {domain}
2. Identify 3-5 key open questions or controversies
3. Map the landscape of existing approaches
4. Identify which agent archetypes would be most valuable
5. Propose a 3-session investigation plan

## Agent Assignments

- **coordinator**: Orchestrate the review, write synthesis
- **scout**: Fetch 5-10 foundational papers for the domain

## Required Reading

(None yet — this is the first session)

## Output

- `sessions/session-00/session-0-domain-survey.md` — Initial domain map
- `sessions/session-00/session-0-investigation-plan.md` — Proposed next steps
```

Create the `sessions/session-00/` directory.

---

## Verification Checklist

Before reporting completion, verify:

- [ ] All directories from Step 1 exist
- [ ] Root CLAUDE.md has all required sections filled in
- [ ] All 8 rule files exist in `.claude/rules/`
- [ ] All 11 skills exist in `.claude/skills/`
- [ ] `settings.json` exists, is valid JSON, and contains `env.CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS`
- [ ] `settings.local.json` exists and is valid JSON
- [ ] 3 infrastructure agents exist in `.claude/agents/`
- [ ] 3 agent-memory stubs exist with MEMORY.md files
- [ ] 11 session templates exist in `.claude/templates/session-templates/`
- [ ] 10 agent templates exist in `.claude/templates/agent-templates/`
- [ ] `agent-roster.md` exists in `.claude/templates/`
- [ ] `agents.md` exists at root
- [ ] `.gitignore` exists at root
- [ ] Session-0 prompt exists in `sessions/session-plan/`
- [ ] `sessions/session-00/` directory exists
- [ ] `artifacts/document-templates/` exists with format-specific subdirectory
- [ ] For LaTeX: 13 `.tex` + 1 `.bib` templates present

---

## What You Do NOT Do

- **Do NOT create domain-specific agents** — that's the user's choice via `/new-researcher` (see `unfold-agents.md`)
- **Do NOT fetch papers** — that's Scout's job (see `unfold-papers.md`)
- **Do NOT set up knowledge tools** — that's Indexer's job (see `unfold-knowledge.md`)
- **Do NOT create a simulation directory** — only if user explicitly needs computation infrastructure
- **Do NOT run any Python scripts** — just install the files

Your job is the skeleton. Other agents fill it with life.
