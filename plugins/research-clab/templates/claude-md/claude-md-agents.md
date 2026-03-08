# .claude/agents/ — Agent Definitions

<!-- DEPLOY: project-root/.claude/agents/CLAUDE.md -->

Every file in this directory defines a research agent. The filename (minus `.md`) becomes the `subagent_type` used to spawn it.

## File Format — Canonical 7-Section Structure

Every agent definition follows this exact structure:

```yaml
---
name: agent-name-here          # Lowercase, hyphenated. MUST match filename.
description: "When to use..."  # 3-5 example prompts. Claude reads this to dispatch.
model: opus | sonnet | haiku   # LLM tier (see below)
color: cyan                    # Terminal display color
memory: project                # Always "project" for research agents
---
```

### Body Sections (in order)

1. **Identity** (no header) — 1-2 paragraphs. HOW they think, not WHAT they know. Methodology over knowledge domain.
2. **`## Research Corpus`** — Points to `researchers/{{DOMAIN}}/`. Includes read-at-start instruction.
3. **`## Core Methodology`** — 3-5 numbered principles that define the agent's analytical approach.
4. **`## Primary Directives`** — 3-5 numbered operational rules specific to the archetype.
5. **`## Interaction Patterns`** — Exactly 4 bullets: Solo, Team, Adversarial, Cross-domain.
6. **`## Output Standards`** — Bullet list of formatting, quality, and epistemic requirements.
7. **`## Persistent Memory`** — Boilerplate pointing to `.claude/agent-memory/{name}/`.

## Model Tier Assignment

| Tier | Cost | Use For | Typical Agents |
|:-----|:-----|:--------|:---------------|
| `opus` | Highest | Deep derivation, adversarial debate, nuanced analysis | Specialist theorists, Skeptic |
| `sonnet` | Medium | Structured indexing, synthesis, orchestration | Coordinator, Indexer |
| `haiku` | Lowest | Fast bulk tasks, paper fetching, simple retrieval | Scout, web-researcher |

## Agent Archetypes

Every research agent maps to one cognitive archetype:

| Archetype | Thinking Style | Role |
|:----------|:---------------|:-----|
| **Skeptic** | "Prove it." | Demands methodology + controls |
| **Principalist** | "What MUST be true?" | Finds structural constraints |
| **Calculator** | "Stop debating. Run it." | Produces executable artifacts |
| **Dreamer** | "What if we tried...?" | Cross-domain pattern finder |
| **Workhorse** | "I'll derive it step by step." | Rigorous domain specialist |
| **Bridge** | "Does this match the source?" | Source fidelity guardian |
| **Observer** | "Here's what the data says." | Empirical measurer |
| **Boundary Guard** | "Here are the limits." | Maps exclusion regions |
| **Coordinator** | Orchestrates. Does NOT research. | Infrastructure |
| **Indexer** | Indexes. Does NOT evaluate. | Infrastructure |
| **Scout** | Fetches. Does NOT analyze. | Infrastructure |

## Required Agents

These three must exist in every project:

1. **coordinator.md** — Orchestration, meeting minutes, context keeping
2. **knowledge-weaver.md** — Knowledge index curation (sole writer of `knowledge-index.json`)
3. **web-researcher.md** — Paper fetching and corpus population

## Rules

- **One agent per file** — no multi-agent definitions
- **Filename = identity** — `foo-bar.md` means the agent's name is `foo-bar`
- **No project-wide rules in agent files** — those belong in the root CLAUDE.md
- **Infrastructure agents don't do research** — coordinator orchestrates, indexer indexes, scout fetches. Hard boundary.
- **Every agent needs a memory stub** — create `.claude/agent-memory/{name}/MEMORY.md` when creating the agent

## Anti-Patterns

- **The "Yes Man"** — agrees with everything, has no methodology. Fix: add adversarial directives.
- **The "Kitchen Sink"** — knows everything, thinks about nothing distinctly. Fix: narrow the methodology.
- **The "Personality Without Methodology"** — has a persona but no analytical framework. Fix: define HOW it evaluates claims.
- **The "Stateless"** — never references or updates its memory. Fix: add memory read/write instructions.
- **The "Novelist"** — produces prose instead of structured output. Fix: mandate output format.

## Quality Checklist

Before considering an agent definition complete:

- [ ] YAML frontmatter has all 5 fields
- [ ] Identity section describes methodology, not just knowledge
- [ ] Research corpus points to an actual `researchers/` subdirectory
- [ ] Primary directives are specific and actionable (not "be thorough")
- [ ] Interaction patterns cover all 4 contexts
- [ ] Output standards include epistemic requirements
- [ ] Persistent memory section exists with directory path
- [ ] **Debate test**: Spawn alongside another agent on contested topic — does it hold a DISTINCT position?
- [ ] **Execution test**: Give it a concrete problem — does it produce ACTIONABLE output?
