# Session 0 Plan — Operational Script

This is the step-by-step script the main agent follows when `/new-research-project` fires. SKILL.md collects user input (project name, domain, research question, output format, hardware) and then hands control to this plan. Every step here is deterministic — no decisions, no branching, no improvisation.

**Inputs available when this plan starts**:
- `${PROJECT_NAME}` — lowercase, hyphenated
- `${DOMAIN}` — research domain
- `${RESEARCH_QUESTION}` — 1-2 sentences
- `${OUTPUT_FORMAT}` — LaTeX | Typst | Markdown | Not sure yet
- `${HARDWARE}` — specs or "Not configured"
- `${PLUGIN}` — path to plugin root (where origami docs live)

---

## Step 1: Create the directory tree

**DO**: Run a single mkdir command:
```
mkdir -p .claude/agents .claude/agent-memory .claude/rules
mkdir -p .claude/skills/{weave,shortterm,clab-review,clab-team,clab-plan,redact,document-prep,new-researcher,librarian,team-blast}
mkdir -p researchers sessions/session-plan sessions/framework sessions/misc sessions/session-00
mkdir -p .claude/templates/agent-templates .claude/templates/session-templates
mkdir -p tools/viz artifacts/source plans
```

**VERIFY**: Every directory in the tree from `unfold-structure.md` Step 1 exists.

---

## Step 2: Copy infrastructure agents

**DO**: Copy these 3 files verbatim from `${PLUGIN}/agents/` to `.claude/agents/`:
- `coordinator.md`
- `indexer.md`
- `scout.md`

**DO**: Create 3 empty memory stubs:
- `.claude/agent-memory/coordinator/MEMORY.md` → `# Coordinator Memory\n`
- `.claude/agent-memory/indexer/MEMORY.md` → `# Indexer Memory\n`
- `.claude/agent-memory/scout/MEMORY.md` → `# Scout Memory\n`

**VERIFY**: 3 agent files in `.claude/agents/`, 3 MEMORY.md files in agent-memory subdirs.

---

## Step 3: Copy behavioral rules

**DO**: Copy these 6 files verbatim from `${PLUGIN}/templates/claude-md/rules/` to `.claude/rules/`:
- `team-lead-behavior.md`
- `teammate-behavior.md`
- `epistemic-discipline.md`
- `output-standards.md`
- `gate-verdicts.md`
- `session-handoffs.md`

**READ**: `${PLUGIN}/project-origami/unfold-rules.md` for the coherence spot-check list.

**VERIFY**: 6 files in `.claude/rules/`. Spot-check: `team-lead-behavior.md` mentions blast-first, `epistemic-discipline.md` mentions "only Skeptic states confidence."

---

## Step 4: Copy skills

**DO**: Copy 10 SKILL.md files verbatim from `${PLUGIN}/templates/skills/` to `.claude/skills/`:

```
weave/SKILL.md
shortterm/SKILL.md
clab-review/SKILL.md
clab-team/SKILL.md
clab-plan/SKILL.md
redact/SKILL.md
document-prep/SKILL.md
new-researcher/SKILL.md
librarian/SKILL.md
team-blast/SKILL.md
```

**VERIFY**: 10 SKILL.md files, one in each skills subdirectory.

---

## Step 4b: Copy Session Templates

**DO**: Copy 11 session format files verbatim from `${PLUGIN}/templates/session-templates/` to `.claude/templates/session-templates/`:

- `A-first-contact-review.md`
- `B-adversarial-debate.md`
- `C-collaborative-deep-dive.md`
- `D-workshop.md`
- `E-investigation-arc.md`
- `F-decisive-computation.md`
- `G-mass-parallel-assessment.md`
- `H-decision-gate.md`
- `I-formalization.md`
- `00-infrastructure.md`
- `supporting-documents.md`

The selection guide is NOT copied here — it goes to `sessions/session-plan/format-selection-guide.md` in Step 9.

**VERIFY**: 11 files in `.claude/templates/session-templates/`.

---

## Step 4c: Copy Agent Templates

**DO**: Copy 10 agent archetype files verbatim from `${PLUGIN}/templates/agent-templates/` to `.claude/templates/agent-templates/`:

- `skeptic.md`
- `calculator.md`
- `workhorse.md`
- `principalist.md`
- `dreamer.md`
- `boundary-guard.md`
- `observer.md`
- `bridge.md`
- `formatter.md`
- `generalist.md`

**VERIFY**: 10 files in `.claude/templates/agent-templates/`.

---

## Step 5: Install CLAUDE.md files

**DO**: Read each template from `${PLUGIN}/templates/claude-md/` and write to the target location:

| Template | Target | Substitutions |
|:---------|:-------|:-------------|
| `claude-md-root.md` | `./CLAUDE.md` | Project name, domain, hardware, python env, date |
| `claude-md-dot-claude.md` | `.claude/CLAUDE.md` | None |
| `claude-md-agents.md` | `.claude/agents/CLAUDE.md` | None |
| `claude-md-agent-memory.md` | `.claude/agent-memory/CLAUDE.md` | None |
| `claude-md-skills.md` | `.claude/skills/CLAUDE.md` | None |
| `claude-md-researchers.md` | `researchers/CLAUDE.md` | None |
| `claude-md-sessions.md` | `sessions/CLAUDE.md` | None |
| `claude-md-sessions-plan.md` | `sessions/session-plan/CLAUDE.md` | None |
| `claude-md-sessions-framework.md` | `sessions/framework/CLAUDE.md` | None |
| `claude-md-tools.md` | `tools/CLAUDE.md` | None |
| `claude-md-artifacts.md` | `artifacts/CLAUDE.md` | None |

**READ**: `${PLUGIN}/project-origami/unfold-structure.md` Step 2 for the root CLAUDE.md required sections (project name, verify working directory, hardware, python env, project structure, knowledge index, team lead behavior, teammate behavior).

**VERIFY**: Root CLAUDE.md contains `${PROJECT_NAME}` and `${DOMAIN}`. All 11 CLAUDE.md files exist.

---

## Step 6: Generate settings

**DO**: Write `.claude/settings.local.json`:
```json
{
  "permissions": {
    "allow": [
      "Bash(timeout:*)"
    ]
  }
}
```

If user specified web domains → add `WebFetch(domain:...)` entries.
If python env discovered → add `Bash("{python-path}":*)`.

**VERIFY**: File is valid JSON. `Bash(timeout:*)` is in the allow list.

---

## Step 7: Generate .gitignore

**DO**: Write `.gitignore` at project root.

**READ**: `${PLUGIN}/project-origami/unfold-structure.md` Step 8 for the exact contents (__pycache__, .venv*, knowledge.db, viz/, .claude/teams/, .claude/tasks/, .DS_Store, Thumbs.db, artifacts/source/*.pdf).

**VERIFY**: File exists. Contains `.claude/teams/` and `.claude/tasks/`.

---

## Step 8: Generate agents.md registry

**DO**: Write `agents.md` at project root listing the 3 infrastructure agents and 10 skills.

**READ**: `${PLUGIN}/project-origami/unfold-structure.md` Step 7 for the exact format.

**VERIFY**: File exists. Lists coordinator, indexer, scout. Lists all 10 skills. Domain Specialists section says "(None yet)".

---

## Step 9: Install methodology and session framework

**READ**: `${PLUGIN}/project-origami/unfold-methodology.md` — follow all 5 steps:

1. **DO**: Copy `${PLUGIN}/templates/session-templates/selection-guide.md` → `sessions/session-plan/format-selection-guide.md`

2. **DO**: Write `sessions/framework/constraint-methodology.md` with pre-registration protocol, constraint mapping rules, confidence trajectory ownership, authority hierarchy. Content is specified verbatim in unfold-methodology.md Step 2.

3. **DO**: Write `sessions/framework/handoff-template.md` with the 7-section handoff structure. Content is specified verbatim in unfold-methodology.md Step 3.

4. **DO**: Write `.claude/agent-memory/coordinator/MEMORY.md` with session patterns (Formats A-I), methodology summary, and empty active state. Content is specified verbatim in unfold-methodology.md Step 4. This OVERWRITES the stub from Step 2.

5. **DO**: Write `.claude/agent-memory/coordinator/constraint-map.md` with empty constraint map scaffold (active constraints: none, gate registry: none, confidence trajectory table with Session 0 row). Content is specified verbatim in unfold-methodology.md Step 5.

**VERIFY**: `format-selection-guide.md` exists. `constraint-methodology.md` mentions pre-registration. `handoff-template.md` has 7 sections (I through VII). Coordinator MEMORY.md lists Formats A-I. `constraint-map.md` has Session 0 row.

---

## Step 10: Install team protocol

**READ**: `${PLUGIN}/project-origami/unfold-teams.md` — follow all 3 steps:

1. **DO**: Append the Team Operations Protocol section to `.claude/agent-memory/coordinator/MEMORY.md` (spawn sequence, hard limits, team lead discipline, orchestration patterns, session format → team size mapping). Content is specified verbatim in unfold-teams.md Step 1.

2. **DO**: Verify `.claude/skills/clab-team/SKILL.md` exists (already copied in Step 4).

3. **DO**: Clean stale state — delete contents of `~/.claude/teams/` and `~/.claude/tasks/` if they exist.

**VERIFY**: Coordinator MEMORY.md contains "Spawn Sequence (MANDATORY)" and "MAX 4 agents per team in workshop/panel modes". No stale team/task directories.

---

## Step 11: Generate knowledge system

**READ**: `${PLUGIN}/project-origami/unfold-knowledge.md` — follow all 6 steps:

1. **DO**: Use `${DOMAIN}` and `${RESEARCH_QUESTION}` to determine domain-specific entity types and constraint categories.

2. **DO**: Write `tools/knowledge-schema.yaml` with:
   - 9 universal entity types (sessions, constraints, gates, proven_results, closed_approaches, active_channels, confidence_trajectory, data_provenance, references)
   - At least 1 domain-specific entity type (chosen based on domain — e.g., `equations` for physics, `experiments` for ML, `protocols` for biology)
   - 4 universal constraint categories (S, F, D, O) plus domain-specific categories
   - Authority designations for each entity type
   - Full field definitions per the schema format in `${PLUGIN}/KNOWLEDGE-DATABASE.md` § 2a

3. **DO**: Write `tools/knowledge-index.json` — empty index with metadata block (schema_version, project, domain, dates, entity_types list, counters at 0) and one empty array per entity type.

4. **DO**: Write `.claude/agent-memory/indexer/MEMORY.md` with knowledge system config, entity type list, constraint categories, source authority hierarchy, maintenance protocol, and rules. Content structure is specified in unfold-knowledge.md Step 4. This OVERWRITES the stub from Step 2.

5. **DO**: Verify `.claude/skills/weave/SKILL.md` exists (already copied in Step 4). Verify `tools/knowledge-schema.yaml` and `tools/knowledge-index.json` both exist.

6. **DO**: Check if Python is available. If yes and project expects heavy computation, optionally copy accelerator tools. Otherwise skip.

**VERIFY**: `knowledge-schema.yaml` has all 9 universal types + at least 1 domain type. `knowledge-index.json` is valid JSON with matching entity_types in metadata. Indexer MEMORY.md mentions "sole writer of knowledge-index.json".

---

## Step 12: Interactive agent selection

**READ**: `${PLUGIN}/project-origami/unfold-agents.md` — follow all 5 steps:

1. **DO**: Present the archetype menu to the user via AskUserQuestion. Show all 10 archetypes grouped as CORE (1-6), CONNECTORS (7-8), UTILITY (9-10), with INFRASTRUCTURE noted as already installed. The full menu text is in unfold-agents.md Step 1.

2. **DO**: Analyze `${DOMAIN}` and `${RESEARCH_QUESTION}`. Recommend a starting roster: always Skeptic + Calculator + 1-2 Workhorses. Suggest domain-appropriate additions. Present via AskUserQuestion. Max 5 domain agents.

3. **DO**: For each selected archetype, collect sub-domain, optional persona frame, methodology, and color via AskUserQuestion. Build 15-30 word persona specs embedding the archetype's cognitive style. Follow unfold-agents.md Step 3 for spec construction rules.

4. **DO**: Write `sessions/session-plan/researcher-queue.md` with one row per selected agent (persona spec, archetype, paper count = 14, color). Format is specified in unfold-agents.md Step 4.

5. **DO**: Update `agents.md` — replace "(None yet)" under Domain Specialists with a "Queued for creation" table listing each archetype and sub-domain.

**VERIFY**: `researcher-queue.md` exists with at least 2 rows (Skeptic + Calculator minimum). Each persona spec is 15-30 words. `agents.md` shows queued agents.

---

## Step 13: Generate Session 0 prompt

**DO**: Write `sessions/session-plan/session-0-prompt.md`:

```markdown
# Session 0: Initial Domain Assessment

**Date**: {today}
**Project**: ${PROJECT_NAME}
**Domain**: ${DOMAIN}
**Format**: First Contact Review (Format A)

## Research Question
${RESEARCH_QUESTION}

## Objectives
1. Survey the current state of knowledge in ${DOMAIN}
2. Identify 3-5 key open questions or controversies
3. Map the landscape of existing approaches
4. Propose a 3-session investigation plan

## Agent Assignments
- **coordinator**: Orchestrate the review, write synthesis
- **scout**: Fetch 5-10 foundational papers

## Required Reading
(None — first session)

## Output
- sessions/session-00/session-0-domain-survey.md
- sessions/session-00/session-0-investigation-plan.md
```

**VERIFY**: File exists. Contains `${RESEARCH_QUESTION}`. Format says "First Contact Review".

---

## Step 14: Final verification

**DO**: Run through this checklist. Every item must pass:

- [ ] All directories from Step 1 exist
- [ ] 3 infrastructure agents in `.claude/agents/`
- [ ] 3 agent memory stubs with MEMORY.md files
- [ ] 6 behavioral rules in `.claude/rules/`
- [ ] 10 skills in `.claude/skills/` (each with SKILL.md)
- [ ] 11 session templates in `.claude/templates/session-templates/`
- [ ] 10 agent templates in `.claude/templates/agent-templates/`
- [ ] 11 CLAUDE.md files (root + 10 subdirectories)
- [ ] `.claude/settings.local.json` is valid JSON
- [ ] `.gitignore` exists
- [ ] `agents.md` exists at root
- [ ] `sessions/session-plan/format-selection-guide.md` exists
- [ ] `sessions/framework/constraint-methodology.md` exists
- [ ] `sessions/framework/handoff-template.md` exists
- [ ] `tools/knowledge-schema.yaml` exists with 9+ entity types
- [ ] `tools/knowledge-index.json` is valid JSON with empty arrays
- [ ] Coordinator MEMORY.md has methodology + team protocol sections
- [ ] Indexer MEMORY.md has knowledge maintenance protocol
- [ ] `sessions/session-plan/researcher-queue.md` has at least 2 entries
- [ ] `sessions/session-plan/session-0-prompt.md` has the research question
- [ ] `sessions/session-00/` directory exists

**REPORT**: Print the completion summary:
```
=== PROJECT SCAFFOLDED ===

Project: ${PROJECT_NAME}
Domain: ${DOMAIN}

Structure:
  .claude/agents/ ............ 3 infrastructure agents
  .claude/skills/ ............ 10 skills installed
  .claude/rules/ ............. 6 behavioral rules
  .claude/agent-memory/ ...... 3 agent memory directories
  sessions/ .................. Session 0 prompt + format guide
  tools/ ..................... Knowledge schema + empty index
  plans/ ..................... This plan

Domain Agents: {N} queued in researcher-queue.md

Next Steps:
  1. Process researcher queue: /new-researcher for each entry
  2. First session: /clab-team sessions/session-plan/session-0-prompt.md
```

---

## Step 15: Process researcher queue (OPTIONAL)

**DO**: Ask the user: "Create domain agents now, or defer to later?"

**If now**: For each row in `researcher-queue.md`, sequentially invoke:
```
/new-researcher "{Persona Spec}" --archetype {archetype} --papers {N} --color {color}
```
Then `/librarian {FolderName}` for each created folder. Update `agents.md` and `researchers/index.md`.

**READ**: `${PLUGIN}/project-origami/unfold-papers.md` for the full processing protocol (sequential invocation, failure handling, cross-index update, registry update).

**If deferred**: Report the queue location and tell the user to run `/new-researcher` manually for each entry when ready.

---

## Error Recovery

| Problem | Fix |
|:--------|:----|
| Plugin assets missing at `${PLUGIN}` | Stop. "Plugin assets incomplete. Reinstall the research-clab plugin." |
| Target directory already has `.claude/agents/` | Warn: "This directory already has agent definitions. Overwrite?" Proceed only on confirmation. |
| User skips Skeptic selection | Explain: "Skeptic is non-negotiable — without adversarial review, everything looks promising." Ask again. |
| User selects >5 domain agents | Warn: "Start with 5 max, add more later via /new-researcher." Let them trim. |
| `/new-researcher` fails for a queue entry | Report the failure, continue to next entry. |
| Knowledge tools (Python) not available | Skip Python accelerator. Core system works without it. |
| No git repo | Run `git init` before Step 1. |
| Stale team/task state in `~/.claude/` | Delete it in Step 10. |
