# Unfold: Project Structure

**Target agent**: Coordinator
**Task**: Create the full directory tree, install CLAUDE.md files, copy skills, configure settings.
**Inputs**: Project name, domain, target output format, hardware specs (optional).
**Reads from**: `${CLAUDE_PLUGIN_ROOT}/templates/universal/claude-md/`, `${CLAUDE_PLUGIN_ROOT}/skills/`

---

## Step 1: Create the Directory Tree

Create this exact structure under the project root. Every directory listed here MUST exist before proceeding to Step 2.

```
{project-root}/
├── .claude/
│   ├── agents/                 # Infrastructure agents (coordinator, indexer, scout)
│   ├── agent-memory/           # Per-agent MEMORY.md stubs
│   ├── skills/                 # All universal/skills/ + any discipline pack skills
│   ├── templates/              # All universal/project-docs/ files + session-templates/ + agent-templates/ + agent-roster.md
│   ├── rules/                  # Universal rules + discipline overlay additions/overrides
│   └── rclab-help.md           # Installed from universal/project-docs/rclab-help.md
├── team-lead-behavior.md       # Project root — NOT in .claude/rules/ (keeps subagents from auto-loading)
├── researchers/                # One folder per domain agent (populated post-scaffold by /new-researcher)
├── sessions/
│   ├── session-plan/
│   ├── framework/              # Cross-session mechanism discussions; discipline-manifest.md lives here
│   └── misc/
├── tools/
│   ├── knowledge-schema.yaml   # Copied from universal (or overridden by discipline pack)
│   └── viz/                    # Generated index visualizations
├── artifacts/
│   ├── source/
│   └── document-templates/     # Installed by unfold-document-prep.md based on output-format selection
├── CLAUDE.md                   # Generated in Phase 3b from universal claude-md-root.md + fragment injection
├── .gitignore
└── agents.md                   # Human-readable agent & skill registry
```

### Conditional directories (create only if the user selected them)

- **`{{COMPUTATION_DIR}}/`** — create only if Q5 computation answer is "Yes — describe hardware" (user supplies the name; default is `computation/`). Skip entirely if Q5 is "No — purely theoretical".
- **`{{SIMULATION_DIR}}/`** — create only if the user explicitly said they need a structured simulation codebase (Q5 answered Yes *and* the hardware spec implied a simulation, or volunteered at Q2/Q3). Skip otherwise.

When either conditional directory is skipped, the coordinator must also:
- Drop the corresponding line from the generated root CLAUDE.md's project-structure block (do not leave `{{COMPUTATION_DIR}}/` as a literal string).
- Leave conditional rule `computation-environment.md` out of `.claude/rules/` if no discipline pack installs one.

**Do NOT create** `document-templates/` subdirectories here — that's handled by `unfold-document-prep.md` based on the user's format selection.

### Empty-directory persistence (`.gitkeep`)

Git does not track empty directories — they disappear on `git clone`. After `mkdir -p`, create a `.gitkeep` file in every directory that would otherwise be empty at end-of-scaffold:

```
researchers/.gitkeep                       # domain agents added later via /new-researcher
artifacts/source/.gitkeep                  # source PDFs/primary docs added as needed
tools/viz/.gitkeep                         # visualizations generated on demand
sessions/misc/.gitkeep                     # rare supporting files
```

**Do NOT** create `.gitkeep` in directories that will definitely have content by end-of-scaffold (e.g., `.claude/agents/` gets infrastructure agents, `.claude/rules/` gets rule files). Those will be tracked automatically by their contents.

**Do NOT** create `.gitkeep` in `artifacts/document-templates/` — `unfold-document-prep.md` populates it (LaTeX templates, Typst/Markdown placeholders, or a minimal README for "Not sure yet"). If document-prep produces only a README, that README already serves the role of `.gitkeep`.

Empty dirs created by conditional rules (e.g., `{{COMPUTATION_DIR}}/` for Q5=Yes) that exist after scaffold also get a `.gitkeep` — pattern applies uniformly: if the dir is created, and no file lands in it this scaffold, it gets `.gitkeep`.

---

## Step 2: Install CLAUDE.md Files

Each directory gets a scoped CLAUDE.md that tells agents what belongs there and how to behave. Read the templates from `${CLAUDE_PLUGIN_ROOT}/templates/universal/claude-md/` and write them into the project, substituting project-specific values.

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

### Templates NOT installed at scaffold (handled elsewhere)

These templates exist in `templates/universal/claude-md/` intentionally but are NOT in the unconditional install table above. If you're auditing for orphaned files, these are the known-conditional set:

| Template | Where it lives | When installed |
|:---------|:---------------|:----------------|
| `claude-md-computation.md` | `{{COMPUTATION_DIR}}/CLAUDE.md` | Only if Q5=Yes (computation requested). Installed as part of the conditional-directory creation in Step 1. |
| `claude-md-simulation.md` | `{{SIMULATION_DIR}}/CLAUDE.md` | Only if Q5=Yes AND the user opted into a structured simulation codebase. |
| `claude-md-researcher-domain.md` | `researchers/<folder>/CLAUDE.md` | Installed by `/new-researcher` Step 4a when a new researcher folder is created — `{{DOMAIN}}` is substituted with the display name, and the `{{if-compute}}` block is resolved against the project's Q5 answer. Not copied by the main scaffolder because researcher folders do not exist yet at that point. |
| `claude-md-session-instance.md` | `sessions/session-NN/CLAUDE.md` | **Reference template only** — not auto-installed by any skill. The parent `sessions/CLAUDE.md` already scopes behavior for every session directory under it; per-session CLAUDE.md is optional. Copy manually if a specific session needs different rules. |
| `claude-md-settings-json.md` | (not a CLAUDE.md) | Source template for `.claude/settings.json`. Extracted by coordinator Phase 4a — NOT a CLAUDE.md install target. |
| `claude-md-settings-md.md` | (not a CLAUDE.md) | Source guidance for personal `.claude/settings.local.md`-style overrides — reference documentation only, not installed. |

**Phase 0a asserts every `.md` file in `templates/universal/claude-md/` is either in the unconditional install table OR in this exclusion table.** If a new template is added to the dir without being registered in one of the two tables, pre-flight fails with "orphaned template file: {path}."

### Fragment-Slot Resolution

Universal CLAUDE.md templates contain `{{fragment-slot:NAME}}` markers where discipline packs inject text. The authoritative strip-and-inject logic lives in `unfold-discipline-overlay.md` Step 6 — that doc is canonical; do not duplicate it here.

Coordinator Phase 3b generates the CLAUDE.md files with slot markers intact. Phase 3c (overlay, if a discipline was selected) injects pack fragments at the matching markers. Phase 3d runs the strip pass unconditionally to zero out any marker that neither the universal template nor a pack fragment resolved.

See coordinator Phase 3d for when this runs, and `unfold-discipline-overlay.md` Step 6 for how.

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

Copy rule files from `${CLAUDE_PLUGIN_ROOT}/templates/universal/rules/` into `.claude/rules/`:

| Source | Install To | Purpose |
|:-------|:-----------|:--------|
| `team-lead-behavior.md` | `{root}/team-lead-behavior.md` | Don't over-manage, compute-mode protocol, never self-terminate. **Installed at project root — NOT in `.claude/rules/` — so subagents do not auto-load it.** |
| `teammate-behavior.md` | `.claude/rules/teammate-behavior.md` | Inbox first, message discipline |
| `epistemic-discipline.md` | `.claude/rules/epistemic-discipline.md` | Evidence hierarchy, what counts as a result |
| `output-standards.md` | `.claude/rules/output-standards.md` | Formatting, precision requirements |
| `gate-verdicts.md` | `.claude/rules/gate-verdicts.md` | How to classify constraint gate outcomes |
| `session-handoffs.md` | `.claude/rules/session-handoffs.md` | How to write handoff documents |
| `agent-standards.md` | `.claude/rules/agent-standards.md` | Shared agent behavior baselines (memory discipline, output standards) |
| `evoi-prioritization.md` | `.claude/rules/evoi-prioritization.md` | Expected-value-of-information ranking for next-step selection |

These are universal — no substitutions needed. The coordinator copies the entire `templates/universal/rules/` directory in Phase 3a, so this table reflects whatever is currently in that source directory; add or remove entries here when the universal rule set changes.

---

## Step 4: Copy Skills

Handled by coordinator Phase 3a: the entire directory `${CLAUDE_PLUGIN_ROOT}/templates/universal/skills/` copies into `.claude/skills/` verbatim. The actual skill set ships with the plugin and drifts over time — do not enumerate a hardcoded list here. A discipline pack may add skills on top in Phase 3c (overlay Step 7).

---

## Step 4b: Copy Session Templates

Copy the session format reference docs from `${CLAUDE_PLUGIN_ROOT}/templates/universal/session-templates/` into `.claude/templates/session-templates/`. These are the format definitions (A through I) that agents consult when planning and running sessions.

```
${CLAUDE_PLUGIN_ROOT}/templates/universal/session-templates/A-first-contact-review.md       → .claude/templates/session-templates/A-first-contact-review.md
${CLAUDE_PLUGIN_ROOT}/templates/universal/session-templates/B-adversarial-debate.md          → .claude/templates/session-templates/B-adversarial-debate.md
${CLAUDE_PLUGIN_ROOT}/templates/universal/session-templates/C-collaborative-deep-dive.md     → .claude/templates/session-templates/C-collaborative-deep-dive.md
${CLAUDE_PLUGIN_ROOT}/templates/universal/session-templates/D-workshop.md                    → .claude/templates/session-templates/D-workshop.md
${CLAUDE_PLUGIN_ROOT}/templates/universal/session-templates/E-investigation-arc.md           → .claude/templates/session-templates/E-investigation-arc.md
${CLAUDE_PLUGIN_ROOT}/templates/universal/session-templates/F-decisive-computation.md        → .claude/templates/session-templates/F-decisive-computation.md
${CLAUDE_PLUGIN_ROOT}/templates/universal/session-templates/G-mass-parallel-assessment.md    → .claude/templates/session-templates/G-mass-parallel-assessment.md
${CLAUDE_PLUGIN_ROOT}/templates/universal/session-templates/H-decision-gate.md              → .claude/templates/session-templates/H-decision-gate.md
${CLAUDE_PLUGIN_ROOT}/templates/universal/session-templates/I-formalization.md               → .claude/templates/session-templates/I-formalization.md
${CLAUDE_PLUGIN_ROOT}/templates/universal/session-templates/00-infrastructure.md             → .claude/templates/session-templates/00-infrastructure.md
${CLAUDE_PLUGIN_ROOT}/templates/universal/session-templates/supporting-documents.md          → .claude/templates/session-templates/supporting-documents.md
```

These are verbatim copies — no substitutions needed. The selection guide is NOT copied here (it goes to `sessions/session-plan/format-selection-guide.md` in unfold-methodology Step 1).

---

## Step 4c: Copy Agent Templates

Copy the agent archetype templates from `${CLAUDE_PLUGIN_ROOT}/templates/universal/agent-templates/` into `.claude/templates/agent-templates/`. These are the cognitive archetype definitions that `/new-researcher` reads when stamping new domain agents.

```
${CLAUDE_PLUGIN_ROOT}/templates/universal/agent-templates/skeptic.md          → .claude/templates/agent-templates/skeptic.md
${CLAUDE_PLUGIN_ROOT}/templates/universal/agent-templates/calculator.md       → .claude/templates/agent-templates/calculator.md
${CLAUDE_PLUGIN_ROOT}/templates/universal/agent-templates/workhorse.md        → .claude/templates/agent-templates/workhorse.md
${CLAUDE_PLUGIN_ROOT}/templates/universal/agent-templates/principalist.md     → .claude/templates/agent-templates/principalist.md
${CLAUDE_PLUGIN_ROOT}/templates/universal/agent-templates/dreamer.md          → .claude/templates/agent-templates/dreamer.md
${CLAUDE_PLUGIN_ROOT}/templates/universal/agent-templates/boundary-guard.md   → .claude/templates/agent-templates/boundary-guard.md
${CLAUDE_PLUGIN_ROOT}/templates/universal/agent-templates/observer.md         → .claude/templates/agent-templates/observer.md
${CLAUDE_PLUGIN_ROOT}/templates/universal/agent-templates/bridge.md           → .claude/templates/agent-templates/bridge.md
${CLAUDE_PLUGIN_ROOT}/templates/universal/agent-templates/formatter.md        → .claude/templates/agent-templates/formatter.md
${CLAUDE_PLUGIN_ROOT}/templates/universal/agent-templates/generalist.md       → .claude/templates/agent-templates/generalist.md
```

These are verbatim copies — no substitutions needed. `/new-researcher` resolves templates from `.claude/templates/agent-templates/` at runtime, so the project is self-contained after scaffolding.

---

## Step 4c-ii: Copy Agent Roster Template

Copy the agent roster from `${CLAUDE_PLUGIN_ROOT}/templates/universal/project-docs/agent-roster.md` into `.claude/templates/`:

```
${CLAUDE_PLUGIN_ROOT}/templates/universal/project-docs/agent-roster.md → .claude/templates/agent-roster.md
```

This is a verbatim copy — no substitutions needed. `/new-researcher` appends new domain agents to this file as they are created. The root CLAUDE.md references this file for name-to-type resolution.

---

## Step 4c-iii: Copy rclab-help Reference

Copy the rclab help document into the project's `.claude/` root. Every `/rclab-*` skill resolves this path (`.claude/rclab-help.md`) when invoked with `--help` or `-h`:

```
${CLAUDE_PLUGIN_ROOT}/templates/universal/project-docs/rclab-help.md → .claude/rclab-help.md
```

Verbatim copy — no substitutions.

---

## Step 4c-iv: Copy Document Templates

Copy the skill-referenced document templates from `${CLAUDE_PLUGIN_ROOT}/templates/universal/` into `.claude/templates/`. These templates are used by `/rclab-plan`, `/rclab-review`, and `/rclab-team` to generate session plans, prompts, synthesis reports, and workshop documents.

```
${CLAUDE_PLUGIN_ROOT}/templates/universal/project-docs/plan-compute.md      → .claude/templates/plan-compute.md
${CLAUDE_PLUGIN_ROOT}/templates/universal/project-docs/plan-workshop.md      → .claude/templates/plan-workshop.md
${CLAUDE_PLUGIN_ROOT}/templates/universal/project-docs/prompt-session.md     → .claude/templates/prompt-session.md
${CLAUDE_PLUGIN_ROOT}/templates/universal/project-docs/synthesis.md          → .claude/templates/synthesis.md
${CLAUDE_PLUGIN_ROOT}/templates/universal/project-docs/workshop.md           → .claude/templates/workshop.md
```

These are verbatim copies — no substitutions needed. Skills resolve these templates at runtime from `.claude/templates/`.

---

## Step 4d: Install Document Templates

**READ**: `${CLAUDE_PLUGIN_ROOT}/project-origami/unfold-document-prep.md` and execute it.

This step installs format-specific document templates into `artifacts/document-templates/` based on the user's `{output-format}` selection (Question 4). For LaTeX projects, this installs 13 `.tex` templates (paper, poster, slides, thesis, report, etc.) and a sample `.bib` file. For Typst and Markdown, it installs placeholder READMEs.

The `/paper new <type>` command discovers these templates at runtime.

---

## Step 5: Install Settings

### 5a: Install `settings.json` (shared, committed)

Read the template from `${CLAUDE_PLUGIN_ROOT}/templates/universal/claude-md/claude-md-settings-json.md` and write the JSON block to `.claude/settings.json`. This file includes:

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

Copy the 3 infrastructure agents from `${CLAUDE_PLUGIN_ROOT}/templates/universal/infrastructure-agents/` into `.claude/agents/`:

```
${CLAUDE_PLUGIN_ROOT}/templates/universal/infrastructure-agents/coordinator.md → .claude/agents/coordinator.md
${CLAUDE_PLUGIN_ROOT}/templates/universal/infrastructure-agents/indexer.md   → .claude/agents/indexer.md
${CLAUDE_PLUGIN_ROOT}/templates/universal/infrastructure-agents/scout.md       → .claude/agents/scout.md
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

Generate `agents.md` at project root — a human-readable quick-reference. **Generate the skill list dynamically from `.claude/skills/` rather than hard-coding it** — the installed skill set varies with the selected discipline pack and drifts as the project evolves.

### Agents section

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
```

### Skills section

For each subdirectory in `.claude/skills/`, read its `SKILL.md` (or `skill.md`) YAML frontmatter and extract `name` + `description`. Format one row per skill, sorted alphabetically:

```markdown
## Skills

| Skill | Description |
|:------|:------------|
| `/{name}` | {description truncated to ~80 chars at word boundary} |
| ... one row per installed skill ... |
```

Never hard-code the list — the skill set depends on which discipline pack was selected. A math project gets different skills than a physics project, and both differ from a generic scaffold.

### Discipline pack attribution

If a discipline pack was selected, append a final section noting which skills came from the pack:

```markdown
## Discipline Pack

This project was scaffolded with the **{pack-display-name}** discipline pack.
Skills installed from the pack: {list of discipline-contributed skills}
Rules overridden by the pack: {list from discipline-manifest.md}

See `sessions/framework/discipline-manifest.md` for the full manifest.
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
- [ ] 5 document templates exist in `.claude/templates/` (plan-compute, plan-workshop, prompt-session, synthesis, workshop)
- [ ] `rclab-help.md` exists at `.claude/rclab-help.md`
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
