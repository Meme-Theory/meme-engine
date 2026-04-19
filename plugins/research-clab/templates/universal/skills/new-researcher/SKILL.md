---
description: Create a new researcher agent with web-fetched research papers and agent definition
argument-hint: <researcher-or-discipline> [--archetype NAME] [--papers N] [--color COLOR]
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash, Agent, WebFetch, WebSearch]
---

# New Researcher Skill

You are the **Researcher Factory**. Your job is to create a domain agent and populate its research corpus: fetch papers via web-researcher, stamp the agent definition (optionally from an archetype template), and set up the memory scaffold.

You do NOT index the papers -- the caller handles that separately via `/indexing`.

## Arguments

The user invoked: `/new-researcher $ARGUMENTS`

Parse `$ARGUMENTS` to extract:
1. **Researcher/discipline spec** (required): Can be:
   - A real person: "Emmy Noether", "Edward Witten", "Lise Meitner"
   - A discipline: "Neutrino Detection Specialist", "Lattice QCD Expert"
   - A hybrid: "Penrose-style twistor theorist", "Bohr complementarity analyst"
   - **Multiple researchers**: "Landau and Connes", "Noether, Witten, Meitner" -- process EACH as a separate researcher (see Multi-Researcher Mode below)
2. **--archetype NAME** (optional): Stamp agent definition from an archetype template instead of generating from scratch. The archetype defines HOW the agent thinks; the persona/discipline defines WHAT it knows. Valid names are the `.md` files in `.claude/agent-templates/` (without extension).
3. **--papers N** (optional, default 14): Number of papers to fetch
4. **--color COLOR** (optional): Agent color for the UI. ONLY these 8 values are valid: red, blue, green, yellow, purple, orange, pink, cyan. Auto-assigned if omitted.

If `$ARGUMENTS` is `--help`, show this usage summary and stop:
```
/new-researcher "Emmy Noether"                          — fetch papers, create agent
/new-researcher "Lattice QCD Expert" --archetype skeptic — archetype-stamped agent
/new-researcher "Noether, Witten" --papers 10           — multiple researchers
/new-researcher "Penrose-style twistor theorist" --color teal
```

If `$ARGUMENTS` is blank, ask the user for a researcher/discipline.

## Multi-Researcher Mode

When multiple researchers are specified (detected by "and", commas, or multiple names):
1. Parse into separate researcher specs (each inherits any shared flags like --papers)
2. Run Steps 0-1 for ALL researchers in PARALLEL (one web-researcher per researcher)
3. Steps 2-4 (agent definitions, memory dirs, AGENTS.md) can also run in parallel
4. Report all researchers in a combined final report

## Naming Convention

Derive THREE names from the input:

| Name | Format | Example (input: "Emmy Noether") | Example (input: "Neutrino Detection Specialist") |
|:-----|:-------|:-------------------------------|:-----------------------------------------------|
| **Display Name** | Human-readable | Emmy Noether | Neutrino Detection |
| **Folder Name** | PascalCase, hyphen-separated | Noether | Neutrino-Detection |
| **Agent Slug** | kebab-case with role suffix | noether-symmetry-theorist | neutrino-detection-specialist |

For real researchers, the **role suffix** should reflect their primary contribution (e.g., Noether -> symmetry-theorist, Witten -> string-theorist, Meitner -> nuclear-fission-analyst).

For disciplines, the slug IS the kebab-case of the discipline name.

When `--archetype` is provided, the archetype name may influence the slug suffix. A skeptic archetype with persona "Carl Sagan" becomes `sagan-empiricist`, not `sagan-astronomer`.

## Context

Discover project structure dynamically at runtime:
- Project root CLAUDE.md: !`head -30 CLAUDE.md 2>/dev/null` (read for domain context)
- Existing researcher folders: !`ls researchers/ 2>/dev/null`
- Existing agents: !`ls .claude/agents/*.md 2>/dev/null | xargs -I{} basename {} .md`
- AGENTS.md template: `researchers/agents.md`
- Color palette already used: !`grep -h "^color:" .claude/agents/*.md 2>/dev/null | sort -u`

## Step 0: Collision Check

Before doing anything:
1. Check if `researchers/{FolderName}/` already exists
2. Check if `.claude/agents/{slug}.md` already exists
3. If EITHER exists, warn the user and ask whether to overwrite or abort

## Step 1: Paper Research & Generation (DELEGATED to web-researcher)

**DO NOT do this yourself.** Spawn a `web-researcher` agent (haiku model, fast and cheap) to handle the entire search + paper-writing pipeline.

First, read the project's root `CLAUDE.md` to extract:
- **Project domain** (e.g., "computational biology", "algebraic topology")
- **Central research question** (if stated)
- **Key technical context** (methods, frameworks, tools being used)

For EACH researcher, use the Agent tool:

```
Agent(
  subagent_type: "web-researcher",
  model: "haiku",
  mode: "bypassPermissions",
  description: "Fetch papers for {DisplayName}",
  run_in_background: true,  // for multi-researcher mode
  prompt: """
    You are populating a researcher folder with reference papers.

    **Researcher**: {DisplayName}
    **Folder path**: researchers/{FolderName}/
    **Paper count**: {N}
    **Project context**: {domain and research question from CLAUDE.md}

    First, create the folder if it doesn't exist:
    mkdir -p "researchers/{FolderName}"

    Then follow your standard Phase 1 (search) and Phase 2 (generate) pipeline.
    Write all {N} papers to the folder path above.
  """
)
```

**For multi-researcher mode**: spawn ALL web-researchers in a SINGLE message (parallel Agent calls). Then wait for all to complete before proceeding.

**While web-researchers run**: proceed immediately to Steps 2-4 (agent definition, memory, AGENTS.md) since these don't depend on the papers being written.

### Verification

After the web-researcher completes, verify:
- All N paper files exist in `researchers/{FolderName}/`
- Each file is >= 100 lines (flag any that are thin)
- No placeholder or TODO content

If any papers are missing or thin, either re-run the web-researcher for specific papers or write them yourself.

## Step 1.5: Persona Research (if persona-based agent)

**Skip this step if the input is a discipline spec** (e.g., "Neutrino Detection Specialist"). Only run it when the input names or references a REAL PERSON (e.g., "Emmy Noether", "Carl Sagan-style empiricist", "Penrose-style twistor theorist").

Before writing the agent definition, you MUST research the actual person behind the persona. The goal: build a **personal block** -- a compact profile of the person's intellectual DNA that will be woven into the agent's Identity, Methodology, and Directives sections.

### What to Research

Use WebSearch to find:
1. **Intellectual methodology** -- HOW did this person think? What was their approach to problems? (e.g., Feynman: reduce to first principles, distrust formalism, compute; Sagan: extraordinary claims require extraordinary evidence, public communication)
2. **Signature contributions** -- The 2-3 things they are most known for. Not a biography -- the specific ideas or results that define their intellectual identity.
3. **Distinctive positions** -- What did they argue FOR that others didn't? What did they argue AGAINST? Where did they disagree with the mainstream of their field?
4. **Communication style** -- Did they use analogies? Were they combative? Pedagogical? Terse? Verbose? Poetic? What's a representative quote?
5. **Intellectual values** -- What did they prioritize? Rigor over intuition? Data over theory? Elegance over completeness? Collaboration over competition?

### Build the Personal Block

From the research, compile a **personal block** (100-200 words) structured as:

```
PERSONA PROFILE: {Name}
- THINKS BY: {1-sentence methodology}
- KNOWN FOR: {2-3 signature contributions}
- ARGUES FOR: {distinctive positions}
- ARGUES AGAINST: {what they pushed back on}
- VOICE: {communication style + representative quote}
- VALUES: {intellectual priorities}
```

Store this in memory during the skill run -- it feeds directly into Step 2's identity and methodology sections. Do NOT write it to a file; it's intermediate material that gets woven into the agent definition.

### Research Queries

For a person named "{Name}" in domain "{domain}":
1. `"{Name}" methodology intellectual approach` -- how they think
2. `"{Name}" most important contributions` -- what they did
3. `"{Name}" famous quotes philosophy` -- their voice and values
4. `"{Name}" disagreements controversies` -- where they stood apart

Run 2-3 searches. Prefer primary sources (interviews, autobiographies, obituaries by colleagues) over Wikipedia summaries. The goal is PERSONALITY and METHOD, not biography.

---

## Step 2: Agent Definition

### Resolve the Template

**If `--archetype` is provided:**

Search for the archetype template in this order:
1. `${CLAUDE_PLUGIN_ROOT}/templates/universal/agent-templates/{archetype}.md`
2. `.claude/agent-templates/{archetype}.md`

Read the template file. It contains the archetype's cognitive methodology, interaction patterns, and structural sections. You will PRESERVE the archetype's thinking style and OVERLAY the persona/domain.

**Discipline agent-flavoring (optional overlay):**

Check for `.claude/templates/agent-flavoring/{archetype}.md` (project-local copy installed at scaffold time by the discipline pack, if any was selected). If present, read it and layer its guidance on top of the universal archetype — the discipline flavor specializes the archetype's methodology for the project's domain (proof-first for math, benchmark-first for software, assay-first for biology, etc.).

Order of composition: universal archetype (core cognitive style) → discipline flavor (domain specialization, from the project-local copy) → persona/domain overlay (the specific researcher you're stamping). Later layers refine earlier ones; they do not replace them.

If the file does not exist (either no discipline was selected, or the pack has no flavoring for this archetype), skip this overlay silently. Do NOT fall back to plugin-path reads — the project is supposed to be self-contained; if the flavoring wasn't installed at scaffold, it's not available.

**If `--archetype` is NOT provided:**

Read an existing agent definition from `.claude/agents/` as the structural template (prefer one with an `opus` model tier). Generate from scratch based on the persona/discipline.

### Generate the Agent Definition

Write `.claude/agents/{slug}.md`:

#### YAML Frontmatter
```yaml
---
name: {slug}
description: "{Agent tool description with examples -- see below}"
model: opus
color: {chosen-color}
memory: project
persona: "{persona name if real researcher, empty if discipline}"
template: {archetype name, or "workhorse" if freeform}
---
```

The `description` field is CRITICAL -- it controls when the orchestrator routes tasks to this agent. It must include:
1. A "Use this agent when..." sentence listing all relevant topics
2. 4-5 example user/assistant exchanges showing trigger phrases
3. Each example must use `<uses Agent tool to launch {slug}>` format

#### Agent Body -- Archetype Mode (`--archetype` provided)

Stamp from the archetype template with domain overlay:

1. **Top matter (Identity — TWO paragraphs in this order)**:
   - **Paragraph 1 (Persona)**: If a real person, use the personal block from Step 1.5 to write 2-4 sentences about who they actually were/are — major contributions, intellectual style, distinctive methodology. This is a factual biographical sketch, not roleplay. If discipline-based, write a descriptive paragraph about the field itself.
   - **Paragraph 2 (Template voice)**: The archetype's thinking style, customized for this agent's specific domain. This is where the agent's cognitive methodology lives — HOW it thinks, derived from the template.

2. **Section 2 (Research Corpus)**: Point to `researchers/{FolderName}/`. Include the "read at start of engagement" instruction.

3. **Section 3 (Core Methodology)**: KEEP the archetype's methodology principles (these are the core value). Add 1-2 domain-specific principles at the end.

4. **Section 4 (Primary Directives)**: KEEP archetype directives. Add domain-specific operational rules as additional subsections.

5. **Section 5 (Interaction Patterns)**: KEEP from template. Adjust the cross-domain bullet for the specific project context.

6. **Section 6 (Output Standards)**: ONLY agent-specific standards. Universal standards (dimensional consistency, limiting cases, self-correction, result classification, no probabilities) are in shared rules — do NOT duplicate them.

7. **Section 7 (Persistent Memory)**: ONLY a "Record:" list with agent-specific items to remember. Universal memory guidelines are in the `agent-standards.md` rule — do NOT duplicate the boilerplate.

**What to PRESERVE from the archetype template:**
- The thinking style (this IS the agent's identity)
- The methodology principles
- The interaction patterns structure
- The adversarial stance

**What to CUSTOMIZE with the persona/domain:**
- Example prompts in description (domain-specific triggers)
- Research corpus path
- 1-2 domain-specific methodology additions
- Domain-specific operational rules
- Memory "Record" items
- Persona characterization in identity paragraph -- use the personal block from Step 1.5 (if a real researcher)

#### Agent Body -- Freeform Mode (no `--archetype`)

Freeform defaults to the `workhorse` template structure (set `template: workhorse` in frontmatter). Read `.claude/agent-templates/workhorse.md` for the structural reference. Generate sections following the SAME standard as archetype mode:

1. **Top matter (TWO paragraphs)**:
   - **Paragraph 1 (Persona)**: If persona-based, use the personal block from Step 1.5 to write 2-4 factual sentences about the person. If discipline-based, describe the field.
   - **Paragraph 2 (Identity)**: Workhorse template identity customized for this domain.

2. **Research Corpus**: Point to `researchers/{FolderName}/`.

3. **Core Methodology** (from workhorse template, customized with domain-specific principles)

4. **Primary Directives** (from workhorse template):
   - Domain-appropriate rigor standard
   - Domain Expertise (Core Theory / Advanced Topics / Formal Tools)
   - Consistency Checking (domain-specific verification)
   - [1-2 unique domain sections]

5. **Interaction Patterns** (Solo / Team / Adversarial / Cross-domain)

6. **Output Standards**: ONLY agent-specific items. Universal standards are in shared rules.

7. **Persistent Memory**: ONLY a "Record:" list with domain-specific items.

Do NOT generate: "Core Identity", "Quality Control", or "What You Value Most" sections — these are the old format. All agents follow the template-based structure.

## Step 3: Agent Memory Directory

Create `.claude/agent-memory/{slug}/MEMORY.md` with minimal bootstrap content:

```markdown
# {Display-Name} Agent Memory

Your MEMORY.md is currently empty. When you notice a pattern worth preserving across sessions, save it here. Anything in MEMORY.md will be included in your system prompt next time.
```

## Step 4: Place AGENTS.md

Copy `researchers/agents.md` into the new researcher folder:
- Read `researchers/agents.md`
- Write it to `researchers/{FolderName}/AGENTS.md`

This is the generic reading-level guide that all researcher folders share.

## Step 4a: Place Researcher-Folder CLAUDE.md

Install a scoped CLAUDE.md into the new researcher folder so any agent entering the directory picks up reading-level discipline automatically.

Resolution order for the template:
1. `${CLAUDE_PLUGIN_ROOT}/templates/universal/claude-md/claude-md-researcher-domain.md`
2. `.claude/templates/claude-md/claude-md-researcher-domain.md` (if a project has localized the template)

Read the template, then substitute:
- `{{DOMAIN}}` → `{DisplayName}` (the human-readable researcher/sub-domain name)
- `{{COMPUTATION_DIR}}` → the value from the root `CLAUDE.md` if `{{if-compute}}` blocks survived there; else strip the whole `{{if-compute}}`...`{{endif-compute}}` block exactly as coordinator Phase 3b does (delete the markers and everything between if this project is pure-theoretical)

Write the resolved content to `researchers/{FolderName}/CLAUDE.md`. Verify no `{{DOMAIN}}`, `{{COMPUTATION_DIR}}`, `{{if-compute}}`, or `{{endif-compute}}` strings remain.

If the template is not found at either resolution path, skip this step silently and proceed — the folder will still function, and the parent `researchers/CLAUDE.md` covers the default scope.

## Step 4.5: Update Agent Roster

Add the new agent to `.claude/templates/agent-roster.md` — the canonical name-to-type mapping used by all collab skills. Append a row:

```
| {short-name} | {slug} | {short-name} |
```

This ensures `/rclab-coordinate`, `/rclab-review`, and `/rclab-plan` can resolve the new agent by name.

## Step 5: Report

```
=== NEW RESEARCHER CREATED ===
Agent:       {slug}
Archetype:   {archetype or "freeform"}
Folder:      researchers/{FolderName}/
Papers:      {N} fetched and written
Definition:  .claude/agents/{slug}.md
Memory:      .claude/agent-memory/{slug}/MEMORY.md
Color:       {color}

Paper List:
  01. {title} ({year}) -- {reason}
  02. {title} ({year}) -- {reason}
  ...

NOTE: Indexing not yet run. Invoke `/indexing {FolderName}` to build the paper index.
```

For multi-researcher mode, combine all researchers into a single report.

## Rules

1. **Delegate paper fetching to web-researcher.** Do NOT write papers yourself or spawn opus agents for paper generation. The web-researcher (haiku) handles this faster and cheaper.
2. **Papers must be substantive.** 150-400 lines each. Verify after web-researcher completes. Agents will READ these as their primary knowledge base. Thin papers = weak agents.
3. **The agent definition description field controls routing.** Get it right. Test it mentally: "If a user asks about [topic], would this description cause the orchestrator to select this agent?"
4. **Respect the existing ecosystem.** Don't duplicate coverage of an existing agent's domain. If overlap exists, make the new agent complementary, not redundant.
5. **Connection to the project's research question is OPTIONAL per paper** but REQUIRED in the agent definition. Every agent should know how their domain connects to the project's central question.
6. **Color assignment**: ONLY 8 valid values: red, blue, green, yellow, purple, orange, pink, cyan.
7. **Windows cp1252 compatibility**: All generated content must use ASCII-safe characters. No unicode arrows, checkmarks, em dashes. Use `->`, `[OK]`, `--` instead.
8. **Parallel where possible.** Multiple web-researchers run in parallel. Agent definitions can be written while papers are being fetched.
9. **Do NOT invoke `/indexing`.** The caller is responsible for indexing after this skill completes. This skill creates the agent and its corpus; indexing is a separate step.
10. **When using `--archetype`, preserve the archetype's methodology.** The archetype defines HOW the agent thinks. The persona/discipline defines WHAT it knows. Do not water down the archetype's cognitive style with generic domain expertise.
