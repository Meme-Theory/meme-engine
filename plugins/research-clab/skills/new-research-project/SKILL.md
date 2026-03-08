---
description: "Scaffold a complete multi-agent research collaboration — agents, skills, rules, knowledge tooling, and Session 0 plan — in any domain"
argument-hint: "[--dry-run]"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion, Agent
---

# /new-research-project

Scaffold a complete multi-agent research collaboration in the current working directory. This skill is the single authority — it drives the entire pipeline from user input to project completion. Origami docs (`project-origami/*.md`) are referenced for detailed content specifications but this file controls execution order and flow.

All templates and assets resolve from `${CLAUDE_PLUGIN_ROOT}`.

## AskUserQuestion Constraint

**ONE QUESTION PER CALL. NO EXCEPTIONS.** Every AskUserQuestion invocation must have exactly one entry in the `questions` array. Multi-question calls silently fail in the terminal UI — the user sees nothing, the tool auto-resolves with blank answers, and the agent continues talking to itself. This is a known platform limitation.

Rules:
1. Each AskUserQuestion call: `questions` array length = 1.
2. Each question: 2-4 options with short labels (under 8 words) and short descriptions (under 20 words).
3. Wait for the user's answer before calling AskUserQuestion again.
4. When presenting complex information (menus, spec lists), print it as plain text output FIRST, then ask a simple approval/selection question separately.
5. If you need to collect 5 inputs, that's 5 separate AskUserQuestion calls in sequence — not 1 call with 5 questions.
6. **NO QUESTIONS IN THE FIRST RESPONSE.** After a skill loads, AskUserQuestion is broken for the entire first agent response turn — the UI silently drops every prompt. The SKILL.md injection poisons the rendering pipeline for that turn. **The fix**: in your first response after the skill loads, ONLY output plain text (pre-flight status, Phase 0 results, a "ready to begin" message). Do NOT call AskUserQuestion. End your first response with a prompt like "Ready — press Enter to start." The user's reply creates a turn boundary, and AskUserQuestion works normally from the second response onward.

## Usage

```
/new-research-project
/new-research-project --dry-run
```

## Parse Arguments

1. `--dry-run`: Show what would be created without writing anything.
2. `$ARGUMENTS` contains any user-provided text.

---

## Phase 0: Pre-Flight

### 0a. Locate Plugin Assets

Verify these paths exist under `${CLAUDE_PLUGIN_ROOT}`:

```
templates/agent-templates/
templates/session-templates/
templates/skills/
templates/claude-md/
templates/claude-md/rules/
project-origami/
agents/
```

If any are missing, stop: "Plugin assets incomplete. Reinstall the research-clab plugin."

### 0b. Verify Target Directory

The target is the current working directory.

- If it already contains `.claude/agents/`: note it in the status output (do NOT use AskUserQuestion for confirmation — that's broken in this turn).
- If it is not a git repo: run `git init`.

### 0c. Status Output and Turn Boundary

**This is the ONLY thing your first response should do.** Print a status summary and stop. Example:

```
=== /new-research-project ===

Pre-flight:
  Plugin assets: OK (found at ${CLAUDE_PLUGIN_ROOT}/)
  Git repo: OK
  Existing agents: WARNING — .claude/agents/ exists (will confirm overwrite)
  Mode: --dry-run

Ready to collect project parameters. Type 'go' to start.
```

**STOP HERE.** Do not call AskUserQuestion. Do not proceed to Phase 1. Wait for the user to respond. Their response creates the turn boundary that makes AskUserQuestion work.

---

## Phase 1: Collect User Input

**This phase starts in your SECOND response**, after the user has replied to the Phase 0 status output.

**SERIAL QUESTIONS ONLY.** Ask the user ONE question at a time using a single AskUserQuestion call with exactly one entry in the `questions` array. Wait for the user's answer before asking the next question. Never batch multiple questions into one AskUserQuestion call — the UI silently drops multi-question prompts.

### Question 1 — Project Name

Ask the user: "What is the project name? (lowercase, hyphenated — e.g., protein-folding-dynamics)"
- Use AskUserQuestion with one question, 2-3 short options derived from any user-provided text, plus sensible defaults.
- Validate: lowercase, hyphens only, no spaces.
- **Wait for their answer.**

### Question 2 — Domain

Ask the user: "What research domain? (e.g., computational biology, algebraic topology, climate modeling)"
- Use AskUserQuestion with one question, 2-3 options inferred from context.
- **Wait for their answer.**

### Question 3 — Research Question

Ask the user: "What is the primary research question? (1-2 sentences)"
- Use AskUserQuestion with one question, 2-3 candidate phrasings.
- **Wait for their answer.**

### Question 4 — Output Format

Ask the user: "What document format will this project produce?"
- Use AskUserQuestion with one question. Options: LaTeX, Typst, Markdown, Not sure yet.
- **Wait for their answer.**

### Question 5 — Computation

Ask the user: "Does this project need computation infrastructure?"
- Use AskUserQuestion with one question. Options: "Yes — describe hardware", "No — purely theoretical", "Not sure yet".
- **Wait for their answer.**

Store all inputs. These are referenced as `{project-name}`, `{domain}`, `{research-question}`, `{output-format}`, `{hardware}` throughout.

---

## Dispatch 1: Infrastructure + Knowledge (Parallel)

After collecting all user inputs, launch TWO Agent invocations **in parallel** (both in the same response). These agents execute Phases 2-7 concurrently. You (the main skill) do NOT execute any of these phases directly — the agents own them.

### Agent 1: Coordinator — Infrastructure Setup (Phases 2-6)

Use the Agent tool:
- `subagent_type`: `"general-purpose"`
- `name`: `"coordinator-scaffold"`
- `prompt`: Must include ALL of the following so the agent can work autonomously:
  - Identity directive: `"You are the coordinator agent for the research-clab plugin. Read your full agent definition at {plugin-root}/agents/coordinator.md — find the '## /new-research-project — Scaffolding Directives' section and execute the 'Infrastructure Setup Task' exactly as specified."`
  - All user inputs as key-value pairs:
    - `project-name`: `{project-name}`
    - `domain`: `{domain}`
    - `research-question`: `{research-question}`
    - `output-format`: `{output-format}`
    - `hardware-specs`: `{hardware}` (or `"none"`)
  - `plugin-root`: resolved absolute path of `${CLAUDE_PLUGIN_ROOT}`
  - `target-dir`: current working directory (absolute path)
  - Explicit reminder: `"Do NOT call AskUserQuestion. All user interaction is handled by the main skill."`

The coordinator will read the project-origami docs, create directories, copy all static assets (using `templates/infrastructure-agents/` as the source for infrastructure agents — NOT `agents/`), generate project-specific files, install methodology and team protocol, and run the infrastructure gate verification.

### Agent 2: Indexer — Knowledge System Init (Phase 7)

Use the Agent tool:
- `subagent_type`: `"general-purpose"`
- `name`: `"indexer-knowledge-init"`
- `prompt`: Must include ALL of the following:
  - Identity directive: `"You are the indexer agent for the research-clab plugin. Read your full agent definition at {plugin-root}/agents/indexer.md — find the '## /new-research-project — Scaffolding Directives' section and execute the 'Knowledge System Initialization Task' exactly as specified."`
  - Key inputs:
    - `project-name`: `{project-name}`
    - `domain`: `{domain}`
    - `research-question`: `{research-question}`
  - `plugin-root`: resolved absolute path of `${CLAUDE_PLUGIN_ROOT}`
  - `target-dir`: current working directory (absolute path)
  - Explicit reminder: `"Do NOT call AskUserQuestion. All user interaction is handled by the main skill."`

The indexer will read unfold-knowledge.md, determine domain-specific entity types, write the schema and index, seed its own memory, and verify the knowledge triad.

### After Both Complete

Wait for BOTH agents to return. Check their reports:
- If either reports errors, attempt to fix them before proceeding.
- Verify key outputs exist: `.claude/agents/coordinator.md`, `tools/knowledge-schema.yaml`, `tools/knowledge-index.json`, `agents.md`.
- If critical files are missing and unfixable, stop and report to the user.

---

## Phase 8: Interactive Agent Selection

**READ**: `${CLAUDE_PLUGIN_ROOT}/project-origami/unfold-agents.md` — follow its 5 steps.

**SERIAL QUESTIONS ONLY.** Every user-facing question in this phase uses exactly one AskUserQuestion call with exactly one entry in the `questions` array. Wait for the user's answer before proceeding. Never batch multiple questions.

### 8a. Present Archetype Menu

Print the archetype menu as plain text output (NOT as a question — just show it so the user can see the options):

```
=== AGENT ARCHETYPES ===

CORE (pick 1 Skeptic + 1 Calculator + 1-2 Workhorses):
  1. SKEPTIC        "Prove it."
  2. CALCULATOR      "Stop debating. Run it."
  3. WORKHORSE       "I'll work through this properly."
  4. PRINCIPALIST    "What MUST be true?"
  5. DREAMER         "What if this is actually THAT?"
  6. BOUNDARY GUARD  "Here are the limits."

CONNECTORS (add later):
  7. OBSERVER        "What does the data say?"
  8. BRIDGE          "The original source says..."

UTILITY (optional):
  9. GENERALIST      Broad coverage, gap-filler.
 10. FORMATTER       Domain-specific document preparation.

INFRASTRUCTURE (already installed):
  - Coordinator, Indexer, Scout
```

### 8b. Recommend and Collect Selections

Analyze `{domain}` and `{research-question}`. Recommend a starting roster:
- **Always**: 1 Skeptic + 1 Calculator (non-negotiable)
- **Usually**: 1-2 Workhorses in primary sub-domains
- **If cross-domain**: suggest a Dreamer
- **If building on external work**: suggest a Bridge
- **If data-driven**: suggest an Observer

Then ask the user ONE question: present 2-3 pre-built roster options (e.g., "Recommended 4", "Minimal 3", "Full 5") using a single AskUserQuestion call with one question. Keep option labels short (under 8 words) and descriptions under 15 words. **Wait for their answer.**

If user tries to skip Skeptic: "Skeptic is non-negotiable — without adversarial review, everything looks promising." Ask again (single AskUserQuestion, one question).

If user selects >5: "Start with 5 max, add more later via `/new-researcher`." Ask them to trim (single AskUserQuestion, one question).

### 8c. Collect Persona Overlays

For each selected archetype, ask the user ONE question for a persona overlay. This lets the user inject a real person, personality, or tone modifier (e.g., "Carl Sagan", "Gordon Ramsay", "asshole", "my thesis advisor") that shapes the agent's voice and approach beyond the base archetype.

**For each agent, sequentially:**

1. Print: `"[Archetype] — {brief archetype description}. Add a persona overlay?"`
2. **Pick a domain-relevant suggestion.** Before calling AskUserQuestion, choose a real person whose work intersects BOTH the archetype's cognitive style AND `{domain}`. The suggestion should make the user think "oh, that's a good fit." Examples of the reasoning:
   - Skeptic + computational biology → "Ioannidis" (replication crisis, evidence standards)
   - Skeptic + mathematical gastronomy → "Rebecca Watson" (science communication, debunking)
   - Calculator + climate modeling → "James Hansen" (quantitative modeling pioneer)
   - Calculator + drug discovery → "Patrick Vallance" (data-driven policy)
   - Dreamer + algebraic topology → "John Conway" (playful cross-domain connections)
   - Principalist + any domain → field-relevant philosopher or axiomatist
   - Observer + any domain → field-relevant empiricist or survey researcher
   - Workhorse + any domain → field-relevant methodical practitioner
   Do NOT reuse names across agents in the same project. Pick someone the user is likely to recognize.
3. Use AskUserQuestion with one question:
   - Question: `"Persona overlay for {Archetype}?"`
   - Options: `"No Persona Overlay"` (description: "Use base archetype voice") AND the domain-relevant suggestion from step 2 (description: 3-5 word style note). Minimum 2 options required by the tool — the user can always select "Other" to type a custom persona.
   - **Wait for their answer.**
4. Store the result. If "No Persona Overlay", the `persona:` field in the agent definition stays empty. If custom text, it becomes the `persona:` value and modifies the agent's generated prompt.

This is N questions for N agents — one at a time, serial.

### 8d. Build Persona Specs

After collecting all persona overlays, you (the agent) generate the full persona specs using:
1. **Sub-domain name** — infer from domain and research question
2. **Persona overlay** — the user's input from 8c (or empty)
3. **Key methodology** — one sentence on how this agent thinks differently, inflected by the persona
4. **Color** — assign from: cyan, gold, red, green, pink, slate, amber, teal, coral

Build a 15-30 word persona spec for each, embedding BOTH the archetype's cognitive style AND the persona overlay into the domain. A Skeptic with persona "asshole" gets a combative, dismissive spec. A Skeptic with persona "Carl Sagan" gets a warm-but-rigorous spec. A Skeptic with no overlay gets the default evidence-demanding voice.

**For persona-based specs (real person named)**: include at least ONE concrete intellectual move or signature position from that person. Do NOT write "Sagan-style empiricist" -- write "Sagan-style empiricist -- baloney detection kit, extraordinary claims need extraordinary evidence." The spec is the SEED that `/new-researcher` will expand via its Step 1.5 persona research. A richer seed produces a richer agent.

Follow unfold-agents.md Step 3 for construction rules and examples.

### 8e. GATE — Approve Persona Specs

**Before writing anything**, present the complete spec list as plain text, then ask the user ONE question using a single AskUserQuestion call with one question:

Show specs in your output text:
```
Here are your domain agent specs:

1. [Skeptic / "Sagan"] "Carl Sagan-style empiricist for {domain} — demands evidence, pre-registration, controls" (coral)
2. [Calculator / no overlay] "{sub-domain} computation specialist — produces artifacts, benchmarks everything" (teal)
3. [Workhorse / "Gordon Ramsay"] "Ramsay-intensity {sub-domain} specialist — shows every step, berates sloppy work" (amber)
```

Then ask: "Approve these agent specs, or revise?"
- Use AskUserQuestion with one question. Options: "Approve all", "Revise — I'll provide feedback".
- **Wait for their answer.**

If the user revises, rework specs and re-present. Ask the same single approval question again. Loop until approved.

### 8f-9. Dispatch 2: Researcher Queue + Session 0 Prompt

After persona specs are approved, launch ONE Agent invocation to write the queue, update the registry, and generate the Session 0 prompt.

Use the Agent tool:
- `subagent_type`: `"general-purpose"`
- `name`: `"coordinator-post-selection"`
- `prompt`: Must include ALL of the following:
  - Identity directive: `"You are the coordinator agent for the research-clab plugin. Read your full agent definition at {plugin-root}/agents/coordinator.md — find the '## /new-research-project — Scaffolding Directives' section and execute the 'Post-Selection Task' exactly as specified."`
  - Approved persona specs as a complete table (one row per agent):
    - For each: persona spec text, archetype, persona overlay (or "—"), paper count, color
  - Project metadata:
    - `project-name`: `{project-name}`
    - `domain`: `{domain}`
    - `research-question`: `{research-question}`
    - `date`: `{today}`
  - `plugin-root`: resolved absolute path of `${CLAUDE_PLUGIN_ROOT}`
  - `target-dir`: current working directory (absolute path)
  - Explicit reminder: `"Do NOT call AskUserQuestion. All user interaction is handled by the main skill."`

The coordinator will write `researcher-queue.md`, update `agents.md` with queued agents, and write `session-0-prompt.md`.

**After completion**: Verify `sessions/session-plan/researcher-queue.md` exists with at least 2 rows (Skeptic + Calculator minimum). Verify `agents.md` shows queued agents. Verify `sessions/session-plan/session-0-prompt.md` contains the research question.

---

## Phase 10: Final Verification

Run through this checklist. Every item must pass:

- [ ] All directories from Phase 2 exist
- [ ] 3 infrastructure agents in `.claude/agents/`
- [ ] 3 agent memory directories with MEMORY.md files
- [ ] 6 behavioral rules in `.claude/rules/`
- [ ] 11 skills in `.claude/skills/` (each with SKILL.md)
- [ ] 11 session templates in `.claude/templates/session-templates/`
- [ ] 10 agent templates in `.claude/templates/agent-templates/`
- [ ] 11 CLAUDE.md files (root + 10 subdirectories)
- [ ] `.claude/settings.local.json` is valid JSON
- [ ] `.gitignore` exists
- [ ] `agents.md` exists with infrastructure + queued agents
- [ ] `sessions/session-plan/format-selection-guide.md` exists
- [ ] `sessions/framework/constraint-methodology.md` exists
- [ ] `sessions/framework/handoff-template.md` exists
- [ ] `tools/knowledge-schema.yaml` has 9+ universal entity types + domain type
- [ ] `tools/knowledge-index.json` is valid JSON with empty arrays
- [ ] Coordinator MEMORY.md has methodology section AND team protocol section
- [ ] Indexer MEMORY.md has knowledge maintenance protocol
- [ ] `sessions/session-plan/researcher-queue.md` has at least 2 entries
- [ ] `sessions/session-plan/session-0-prompt.md` has the research question
- [ ] `sessions/session-00/` directory exists

Print completion summary using the insight block format. The content inside must be GENERATED from the actual project — not boilerplate. Describe what makes THIS project's agent team distinctive, how the selected archetypes create productive tension for THIS research question, and what the first session will actually investigate.

```
★ Insight ─────────────────────────────────────

  {project-name} — {domain}

  {2-3 sentences: what this project's agent team is built to do.
   Reference the specific archetypes selected, the adversarial
   pairs they form, and why that team composition fits the
   research question. This should read like a colleague explaining
   "here's why we staffed the project this way."}

  Structure:
    .claude/agents/ ............ 3 infrastructure + {N} domain (queued)
    .claude/skills/ ............ 11 skills installed
    .claude/rules/ ............. 6 behavioral rules
    sessions/ .................. Session 0 prompt ready
    tools/ ..................... Knowledge schema initialized

  Next:
    1. /new-researcher for each entry in researcher-queue.md
    2. Start a NEW SESSION (reload agents and skills)
    3. /clab-team sessions/session-plan/session-0-prompt.md

─────────────────────────────────────────────────
```

The insight block is the LAST thing the user sees before deciding whether to process the researcher queue. Make it count — it should make them feel like the project is coherent and ready, not just that files were copied.

---

## Phase 11: Process Researcher Queue (Optional)

Ask via AskUserQuestion: "Create domain agents now, or defer to later?"

### If now

**READ**: `${CLAUDE_PLUGIN_ROOT}/project-origami/unfold-papers.md` for the full processing protocol.

For each row in `researcher-queue.md`, sequentially invoke:
```
/new-researcher "{Persona Spec}" --archetype {archetype} --papers {N} --color {color}
```

- Process ONE AT A TIME — each `/new-researcher` spawns a web-researcher agent.
- Wait for each to complete before starting the next.
- If one fails, report the failure and continue to the next entry.

After ALL `/new-researcher` invocations complete:
1. Invoke `/librarian {FolderName}` for each created researcher folder (sequential — each creates a team).
2. Create or update `researchers/index.md` with a cross-domain table.
3. **Use Edit (not Write)** on `agents.md` — replace "Queued" status entries with actual agent names and roles.

### If deferred

Report: "Researcher queue saved at `sessions/session-plan/researcher-queue.md`. Run `/new-researcher` for each entry when ready."

---

## Dry Run

If `--dry-run`: run Phases 0-1 and 8a-8d only. Display what WOULD be created (directory tree, file list, recommended agent roster, persona specs). Write nothing.

---

## Error Recovery

| Problem | Fix |
|:--------|:----|
| Plugin assets missing | Stop. "Plugin assets incomplete. Reinstall the research-clab plugin." |
| Existing `.claude/agents/` | Warn and confirm overwrite before proceeding. |
| User skips Skeptic | Explain non-negotiable. Ask again. |
| User selects >5 domain agents | Warn. "Start with 5 max, add more via /new-researcher." Let them trim. |
| `/new-researcher` fails for a queue entry | Report failure, continue to next entry. |
| Python not available | Skip accelerator. Core knowledge system works without it. |
| No git repo | Run `git init` before Phase 2. |
| Stale team/task state | Delete in Phase 6c. |
| Root CLAUDE.md template has unfilled `{{...}}` variables | Substitute or strip — no mustache variables in final output. |
