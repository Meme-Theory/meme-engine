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
templates/universal/agent-templates/
templates/universal/project-docs/agent-roster.md
templates/universal/session-templates/
templates/universal/mcps/
templates/universal/skills/
templates/universal/claude-md/
templates/universal/rules/
templates/universal/infrastructure-agents/
templates/universal/knowledge-schema.yaml
templates/disciplines/
project-origami/
agents/
```

If any are missing, stop: "Plugin assets incomplete. Reinstall the research-clab plugin."

### 0a-ii. Non-empty spot check

For the following key files, verify they are non-empty (file size > 0):

```
templates/universal/claude-md/claude-md-root.md
templates/universal/claude-md/claude-md-settings-json.md
templates/universal/rules/teammate-behavior.md
templates/universal/rules/team-lead-behavior.md
templates/universal/knowledge-schema.yaml
templates/universal/project-docs/agent-roster.md
```

If any is empty, stop with "Plugin asset is empty or corrupt: {path}."

### 0a-iii. Orphaned template check

List every `.md` file in `templates/universal/claude-md/`. Compare against the two tables in `project-origami/unfold-structure.md` Step 2:
- The unconditional install table (11-12 entries)
- The known-conditional exclusion table (6 entries)

Every file in `templates/universal/claude-md/` must appear in EXACTLY one of those tables. If a file is in neither, stop with "Orphaned template: {path} — add to the install table or the exclusion table before scaffolding."

### 0a-iv. Discipline scan

Also scan `templates/disciplines/` — each subdirectory with a `discipline.json` is a selectable pack. Record the list for Question 6. Read each `discipline.json` to verify `schema-version == "1.0"`; packs with other versions are flagged as "incompatible — exclude from menu."

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

### Question 6 — Discipline Pack

Ask the user: "Which discipline pack should overlay the universal harness?"
- Scan `${CLAUDE_PLUGIN_ROOT}/templates/disciplines/` for subdirectories containing `discipline.json`. Read each `display-name` and `description` to build options.
- Use AskUserQuestion with one question. Options derived from the scan, plus always include **"None — generic research harness"** as a fallback.
  - Example: `[{"label": "Physics / Cosmology", "description": "Gate-based computation, canonical-constants, astro/arxiv MCPs"}, {"label": "None — generic", "description": "Universal harness only, no discipline overlay"}]`
- Store the answer as `{discipline}`. Use the literal directory name (e.g., `"physics"`) or `"none"`.
- **Wait for their answer.**

Store all inputs. These are referenced as `{project-name}`, `{domain}`, `{research-question}`, `{output-format}`, `{hardware}`, `{discipline}` throughout.

---

## Dispatch 1: Infrastructure + Knowledge (SERIAL)

After collecting all user inputs, launch Agent 1 (coordinator) FIRST. When it completes, launch Agent 2 (indexer). **Do not parallelize** — the indexer reads `tools/knowledge-schema.yaml`, which the coordinator writes during its Phase 3a (universal baseline) and merges in Phase 3c (discipline overlay). Running them in parallel creates a race: indexer may read the file before coordinator finishes writing the merged schema.

### Dispatch 1a: Coordinator — Infrastructure Setup (Phases 2-8)

Use the Agent tool:
- `subagent_type`: `"general-purpose"`
- `name`: `"coordinator-scaffold"`
- `prompt`: use this exact template. Substitute the bracketed values with the actual inputs collected in Phase 1:

```
You are the coordinator agent for the research-clab plugin. Read your full agent definition at {plugin-root}/agents/coordinator.md — find the "## /new-research-project — Scaffolding Directives" section and execute the "Infrastructure Setup Task" exactly as specified.

Inputs:
  project-name: <project-name>
  domain: <domain>
  research-question: <research-question>
  output-format: <output-format>
  hardware-specs: <hardware or "none">
  discipline: <discipline pack name or "none">
  plugin-root: <absolute path of ${CLAUDE_PLUGIN_ROOT}>
  target-dir: <absolute path of the current working directory>

Do NOT call AskUserQuestion. All user interaction is handled by the main skill.
Report back: list every phase that completed successfully, every phase that failed (with the exact error), and the final contents of sessions/framework/discipline-manifest.md if a pack was applied.
```

Use plain text key-value lines (one per line, `key: value` format). Do NOT pass JSON or YAML — the coordinator parses line-by-line.

The coordinator executes Phases 2-8 from its scaffolding directives — directory tree, universal install, CLAUDE.md generation, discipline overlay (if any), fragment-slot strip, project-specific files, methodology, team protocol, rules spot-check, infrastructure gate. Coordinator does NOT do MCP install or knowledge-index init — those belong to the main skill and the indexer respectively.

### Wait for coordinator, then verify schema

Before dispatching the indexer, verify the coordinator's output:
- `tools/knowledge-schema.yaml` exists and is non-empty.
- The schema has an `entity_types:` block with at least the 5 universal types.
- If a discipline pack was selected: `sessions/framework/discipline-manifest.md` exists.
- Infrastructure gate (coordinator Phase 8) reports success.

If any check fails: do NOT dispatch the indexer. Report the coordinator's failure to the user and stop.

### Dispatch 1b: Indexer — Knowledge Index Initialization

Only after the coordinator has completed successfully. Use the Agent tool:
- `subagent_type`: `"general-purpose"`
- `name`: `"indexer-knowledge-init"`
- `prompt`: use this exact template:

```
You are the indexer agent for the research-clab plugin. Read your full agent definition at {plugin-root}/agents/indexer.md — find the "## /new-research-project — Scaffolding Directives" section and execute the "Knowledge Index Initialization Task" exactly as specified.

Context: the knowledge schema is already installed at tools/knowledge-schema.yaml (by the coordinator, Phase 3a + merged by Phase 3c if a discipline pack was applied). Do NOT rewrite it. Your job is to generate the empty tools/knowledge-index.json from the schema and seed your own memory.

Inputs:
  project-name: <project-name>
  domain: <domain>
  research-question: <research-question>
  plugin-root: <absolute path of ${CLAUDE_PLUGIN_ROOT}>
  target-dir: <absolute path of the current working directory>

Do NOT call AskUserQuestion. Do NOT rewrite tools/knowledge-schema.yaml — the coordinator owns that file.
Report back: whether tools/knowledge-index.json was created successfully, the entity types you observed in the schema, and any gaps between what the schema specifies and what your initialization could establish.
```

The indexer reads `unfold-knowledge.md` starting at Step 3 (skip Step 2 — the schema is already in place), generates `tools/knowledge-index.json` from the schema, seeds its own memory, and verifies the knowledge triad.

### After Both Complete

Wait for both to return. Check their reports:
- If either reports errors, attempt to fix them before proceeding.
- Verify key outputs exist: `.claude/agents/coordinator.md`, `tools/knowledge-schema.yaml`, `tools/knowledge-index.json`, `agents.md`.
- If critical files are missing and unfixable, stop and report to the user.

---

## Phase 7b: MCP Server Installation (Interactive)

**READ**: `${CLAUDE_PLUGIN_ROOT}/project-origami/unfold-mcp.md` — follow its 6 steps.

This phase runs after infrastructure and knowledge setup are complete but before agent selection. It presents the user with optional MCP servers that enhance the project's research capabilities.

**SERIAL QUESTIONS ONLY.** This phase uses AskUserQuestion — one question per call, wait for each answer.

The unfold-mcp doc handles:
1. Scanning `${CLAUDE_PLUGIN_ROOT}/templates/universal/mcps/` for available MCPs
2. Presenting the menu to the user (AskUserQuestion)
3. Detecting Python environment (if an MCP requires it)
4. Alerting the user if Python is not available (with options to skip or provide a path)
5. Installing the MCP package, writing `.mcp.json`, updating settings and CLAUDE.md
6. Verification and reporting

**If the user selects "None"**: skip to Phase 7c. No MCP configuration is written.

**If Python is not found**: the unfold explicitly alerts the user — it does NOT silently skip. The user decides whether to skip or provide a Python path.

---

## Phase 7c: Python Backbone (Interactive, Gated)

**READ**: `${CLAUDE_PLUGIN_ROOT}/project-origami/unfold-python-env.md` — follow its 5 steps.

This phase writes `requirements-mcp.txt` and `requirements-compute.txt` at the project root (universal baseline + discipline additions if the selected pack supplies any) and asks the user whether to run `pip install` now.

**SERIAL QUESTIONS ONLY.** The gate is a single AskUserQuestion (three options: Install now / Defer / Skip entirely). Sub-questions about missing Python or missing venv are each their own single-question AskUserQuestion call.

Rules:
- Runs AFTER Phase 7b so editable MCP installs (e.g., `paper-search-mcp`) resolve against actual on-disk paths.
- Runs BEFORE Phase 8 so the user's first real session doesn't discover a broken import the first time they invoke an MCP.
- If the user selects "Skip entirely", NO files are written. Continue to Phase 8.
- If "Defer install", files ARE written but pip is not run. Continue to Phase 8.
- If "Install now", the unfold runs dry-run resolves, real installs, and smoke imports, reporting per-interpreter status before continuing to Phase 8.
- Never auto-install ROCm/CUDA torch. Print the command for manual execution; the wheel index is SDK-specific and can't be safely pinned in a plain-index requirements file.

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
   - Skeptic + pure math → "Grothendieck" (foundational rewrites, trust only full structural understanding) or "Poincaré" (rigor critic across physics and topology)
   - Calculator + climate modeling → "James Hansen" (quantitative modeling pioneer)
   - Calculator + drug discovery → "Patrick Vallance" (data-driven policy)
   - Calculator + math → "Terence Tao" (computational-experimental number theory) or "Erdős" (prolific explicit constructions and estimates)
   - Dreamer + algebraic topology → "John Conway" (playful cross-domain connections)
   - Dreamer + geometry / analysis → "Gromov" (metric/structural analogies across areas)
   - Principalist + any domain → field-relevant philosopher or axiomatist
   - Principalist + math → "Gödel" (foundational limits) or "Bourbaki" (axiomatic structuralism)
   - Observer + any domain → field-relevant empiricist or survey researcher
   - Workhorse + any domain → field-relevant methodical practitioner
   - Workhorse + math → "Serre" (meticulous exposition, complete proofs) or "Atiyah" (geometric+algebraic synthesis)
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
- [ ] Every file in `templates/universal/rules/` landed in `.claude/rules/` (minus `team-lead-behavior.md`, which goes to project root); plus any additions or overrides supplied by the selected discipline pack. Expect ≥8 files for "none"; more if a pack added rules.
- [ ] Every subdirectory in `templates/universal/skills/` copied into `.claude/skills/` (each with a `SKILL.md` or `skill.md`); plus any discipline pack skills. Expect ≥14 for "none".
- [ ] Every file in `templates/universal/session-templates/` copied into `.claude/templates/session-templates/` (expect ≥11 format letter files plus `00-infrastructure.md` and `supporting-documents.md`; exact count tracks the source directory)
- [ ] Every file in `templates/universal/agent-templates/` copied into `.claude/templates/agent-templates/` (expect ≥10: skeptic, calculator, workhorse, principalist, dreamer, boundary-guard, observer, bridge, formatter, generalist)
- [ ] `.claude/templates/agent-roster.md` exists with agent name-to-type mapping
- [ ] Every entry in `unfold-structure.md` Step 2's unconditional install table produced a CLAUDE.md (or `researchers/agents.md`) at its target path (expect 11 CLAUDE.md targets + 1 `researchers/agents.md`)
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
- [ ] If MCP servers were installed: `.mcp.json` exists at project root and is valid JSON
- [ ] If MCP servers were installed: root CLAUDE.md contains MCP instructions section
- [ ] If LaTeX format selected: `artifacts/document-templates/latex/` has 14 `.tex` files + `references.bib`
- [ ] If a discipline pack declared `directories[]`: each listed path exists under the project root
- [ ] If Phase 7c was not "Skip entirely": `requirements-mcp.txt` and `requirements-compute.txt` exist at project root, with zero surviving `{{...}}` mustache placeholders in either file
- [ ] If Phase 7c was "Install now": `sessions/framework/discipline-manifest.md` records the install status under a `## Python Environment` section

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
    .claude/rules/ ............. 8 behavioral rules
    sessions/ .................. Session 0 prompt ready
    tools/ ..................... Knowledge schema initialized

  Next:
    1. /new-researcher for each entry in researcher-queue.md
    2. Start a NEW SESSION (reload agents and skills)
    3. /rclab-team sessions/session-plan/session-0-prompt.md

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

If `--dry-run` is in `$ARGUMENTS`, run in report-only mode:

1. **Execute Phase 0** normally — all pre-flight checks including plugin-asset spot-check, orphaned-template detection, and discipline-pack schema-version validation. Report every gap found. These checks are non-mutating.
2. **Execute Phase 1** normally — all 6 user questions, collect answers.
3. **Execute Phase 8a-8d** (agent menu, persona construction) so the user can see the recommended roster.
4. **Do NOT dispatch** coordinator (Dispatch 1a) or indexer (Dispatch 1b). Do NOT run Phase 7b (MCP), Phase 7c (Python backbone), Phase 8e-f (researcher queue), or Phase 10/11.
5. **Report plan**: print a complete plan-of-record listing (not creating):
   - Directories that would be created (from unfold-structure.md Step 1, with conditional dirs resolved per Q5)
   - CLAUDE.md files that would be installed and their substitution summary
   - Rules that would land in `.claude/rules/` (universal + discipline overlay, with override annotations)
   - Skills that would be copied (universal + any discipline skills)
   - MCP menu that WOULD be presented (scan universal + discipline MCPs dirs)
   - LaTeX template count that would install (13 .tex + 1 .bib if Q4=LaTeX)
   - Agent roster with personas
6. **Exit cleanly** with a message: "Dry run complete. Re-invoke without --dry-run to actually scaffold."

No file writes happen in dry-run mode.

---

## Error Recovery

| Problem | Fix |
|:--------|:----|
| Plugin assets missing | Stop. "Plugin assets incomplete. Reinstall the research-clab plugin." |
| Existing `.claude/agents/` | Warn and confirm overwrite before proceeding. |
| User skips Skeptic | Explain non-negotiable. Ask again. |
| User selects >5 domain agents | Warn. "Start with 5 max, add more via /new-researcher." Let them trim. |
| `/new-researcher` fails for a queue entry | Report failure, continue to next entry. |
| Python not available (knowledge) | Skip accelerator. Core knowledge system works without it. |
| Python not available (MCP) | Alert user explicitly. Offer skip or manual path. Never silently skip. |
| MCP package install fails | Offer retry, skip, or manual install. Write config anyway if manual. |
| No git repo | Run `git init` before Phase 2. |
| Stale team/task state | The scaffold does NOT touch `~/.claude/teams/` or `~/.claude/tasks/`. If the user wants them cleaned, they run that manually. |
| Root CLAUDE.md template has unfilled `{{...}}` variables | Substitute or strip — no mustache variables in final output. |
