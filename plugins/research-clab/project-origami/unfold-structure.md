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
│   │   ├── indexing/
│   │   ├── team-blast/
│   │   └── clab-synthesis/
│   └── rules/
├── researchers/
├── sessions/
│   ├── session-plan/
│   ├── templates/
│   ├── framework/
│   └── misc/
├── tools/
│   └── viz/
└── artifacts/
    └── source/
```

**Do NOT create** a simulation directory yet — that's domain-dependent and happens later if the user needs computation infrastructure.

---

## Step 2: Install CLAUDE.md Files

Each directory gets a scoped CLAUDE.md that tells agents what belongs there and how to behave. Read the templates from `${CLAUDE_PLUGIN_ROOT}/templates/claude-md/` and write them into the project, substituting project-specific values.

| Template Source | Install To | Substitutions |
|:----------------|:-----------|:-------------|
| `claude-md-root.md` | `{root}/CLAUDE.md` | Project name, domain, hardware specs, python env |
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

The root CLAUDE.md is the project constitution. Read `claude-md-root.md` as a template, then generate the real file with these sections filled in:

1. **Project Name & Domain** — from user input
2. **Verify Working Directory** — `pwd` check with the actual project path
3. **Hardware** — from user input (or "Not configured" if omitted)
4. **Python Environment** — discover or ask: `.venv/bin/python`, system python, or none
5. **Project Structure** — the directory tree from Step 1
6. **Knowledge Index** — boilerplate about `/weave` (copy from template)
7. **Team Lead Behavior** — copy from template (these are universal rules)
8. **Teammate Behavior** — copy from template (universal rules)

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
${CLAUDE_PLUGIN_ROOT}/skills/indexing/SKILL.md           → .claude/skills/indexing/SKILL.md
${CLAUDE_PLUGIN_ROOT}/skills/team-blast/SKILL.md         → .claude/skills/team-blast/SKILL.md
${CLAUDE_PLUGIN_ROOT}/skills/clab-synthesis/SKILL.md     → .claude/skills/clab-synthesis/SKILL.md
```

---

## Step 4b: Copy Session Templates

Copy the session format reference docs from `${CLAUDE_PLUGIN_ROOT}/templates/session-templates/` into `sessions/templates/`. These are the format definitions (A through I) that agents consult when planning and running sessions.

```
${CLAUDE_PLUGIN_ROOT}/templates/session-templates/A-first-contact-review.md       → sessions/templates/A-first-contact-review.md
${CLAUDE_PLUGIN_ROOT}/templates/session-templates/B-adversarial-debate.md          → sessions/templates/B-adversarial-debate.md
${CLAUDE_PLUGIN_ROOT}/templates/session-templates/C-collaborative-deep-dive.md     → sessions/templates/C-collaborative-deep-dive.md
${CLAUDE_PLUGIN_ROOT}/templates/session-templates/D-workshop.md                    → sessions/templates/D-workshop.md
${CLAUDE_PLUGIN_ROOT}/templates/session-templates/E-investigation-arc.md           → sessions/templates/E-investigation-arc.md
${CLAUDE_PLUGIN_ROOT}/templates/session-templates/F-decisive-computation.md        → sessions/templates/F-decisive-computation.md
${CLAUDE_PLUGIN_ROOT}/templates/session-templates/G-mass-parallel-assessment.md    → sessions/templates/G-mass-parallel-assessment.md
${CLAUDE_PLUGIN_ROOT}/templates/session-templates/H-decision-gate.md               → sessions/templates/H-decision-gate.md
${CLAUDE_PLUGIN_ROOT}/templates/session-templates/I-formalization.md               → sessions/templates/I-formalization.md
${CLAUDE_PLUGIN_ROOT}/templates/session-templates/00-infrastructure.md             → sessions/templates/00-infrastructure.md
${CLAUDE_PLUGIN_ROOT}/templates/session-templates/supporting-documents.md          → sessions/templates/supporting-documents.md
```

These are verbatim copies — no substitutions needed. The selection guide is NOT copied here (it goes to `sessions/session-plan/format-selection-guide.md` in unfold-methodology Step 1).

---

## Step 5: Install Settings

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

If the user specified web domains for research (e.g., arxiv.org, pubmed.ncbi.nlm.nih.gov), add `WebFetch(domain:...)` entries to the allow list.

If a Python environment was identified, add `Bash("{python-path}":*)`.

---

## Step 6: Install Infrastructure Agents

Copy the 3 infrastructure agents from `${CLAUDE_PLUGIN_ROOT}/templates/infrastructure-agents/` into `.claude/agents/`:

```
${CLAUDE_PLUGIN_ROOT}/templates/infrastructure-agents/coordinator.md → .claude/agents/coordinator.md
${CLAUDE_PLUGIN_ROOT}/templates/infrastructure-agents/librarian.md   → .claude/agents/librarian.md
${CLAUDE_PLUGIN_ROOT}/templates/infrastructure-agents/scout.md       → .claude/agents/scout.md
```

**Variable substitution**: After copying, replace `{{PROJECT_NAME}}` with the actual project name in `librarian.md` (2 occurrences: YAML description and agent intro paragraph) and `scout.md` (3 occurrences: Connection section header, generation phase template, cross-domain interaction pattern). `coordinator.md` has no template variables — copy verbatim.

Create agent-memory stubs for each:

```
.claude/agent-memory/coordinator/MEMORY.md  (empty — "# Coordinator Memory\n")
.claude/agent-memory/librarian/MEMORY.md    (empty — "# Librarian Memory\n")
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
| librarian | sonnet | Indexes knowledge, serves queries |
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
| `/indexing` | Build structured index for researcher or general folder |
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
- [ ] All 6 rule files exist in `.claude/rules/`
- [ ] All 11 skills exist in `.claude/skills/`
- [ ] `settings.local.json` exists and is valid JSON
- [ ] 3 infrastructure agents exist in `.claude/agents/`
- [ ] 3 agent-memory stubs exist with MEMORY.md files
- [ ] 11 session templates exist in `sessions/templates/`
- [ ] `agents.md` exists at root
- [ ] `.gitignore` exists at root
- [ ] Session-0 prompt exists in `sessions/session-plan/`
- [ ] `sessions/session-00/` directory exists

---

## What You Do NOT Do

- **Do NOT create domain-specific agents** — that's the user's choice via `/new-researcher` (see `unfold-agents.md`)
- **Do NOT fetch papers** — that's Scout's job (see `unfold-papers.md`)
- **Do NOT set up knowledge tools** — that's Librarian's job (see `unfold-knowledge.md`)
- **Do NOT create a simulation directory** — only if user explicitly needs computation infrastructure
- **Do NOT run any Python scripts** — just install the files

Your job is the skeleton. Other agents fill it with life.
