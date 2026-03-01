# Unfold: Agent Definition Format Spec

**Target agent**: Coordinator (reference doc — not a task, used during agent stamping)
**Task**: Reference specification for the exact format of agent definition files.
**Reads from**: `${CLAUDE_PLUGIN_ROOT}/AGENT-DEFINITION-PATTERNS.md`, `${CLAUDE_PLUGIN_ROOT}/CANONICAL-AGENT-FORMAT.md` (originals)

---

## When to Use This Doc

This is a REFERENCE document, not a task. The `/new-researcher` skill reads it when generating agent definitions. The coordinator may also reference it when designing persona specs during `unfold-agents.md`. It specifies the exact format every agent definition must follow.

---

## File Location & Naming

- Path: `.claude/agents/{agent-name}.md`
- Naming: lowercase, hyphenated (e.g., `folding-kinetics-specialist.md`)
- The filename minus `.md` becomes the `subagent_type` used to spawn the agent

---

## YAML Frontmatter

```yaml
---
name: {agent-name}
description: "When to use this agent. 3-5 example user/assistant prompt pairs."
model: opus | sonnet | haiku
color: {color}
memory: project
persona: ""
---
```

| Field | Required | Notes |
|:------|:---------|:------|
| `name` | Yes | Must match filename. Lowercase, hyphenated. |
| `description` | Yes | Dispatch guide — Claude Code reads this to decide which agent to spawn. Include 3-5 concrete example prompts with assistant responses. |
| `model` | Yes | `opus` for deep analysis/debate. `sonnet` for structured/admin work. `haiku` for fast bulk tasks. |
| `color` | Yes | Terminal differentiation: cyan, gold, red, green, pink, slate, amber, etc. |
| `memory` | Yes | Always `project`. |
| `persona` | Yes | Empty `""` by default. When set (e.g., `"Marie Curie"`), agent adopts communication style of that figure while preserving archetype methodology. Persona is flavor, not function. |

### Model Tier Assignment

| Tier | Use For | Archetypes |
|:-----|:--------|:-----------|
| `opus` | Deep analysis, adversarial debate, first-principles reasoning | skeptic, principalist, calculator, dreamer, boundary-guard, workhorse, observer, bridge, generalist |
| `sonnet` | Structured orchestration, indexing, formatting | coordinator, librarian, formatter |
| `haiku` | Fast bulk tasks, web fetching | scout |

---

## Body: 7 Sections in This Exact Order

### Section 1: Identity (NO header)

Opening prose immediately after frontmatter. 1-2 paragraphs.
- WHO this agent is (archetype role)
- HOW they think (methodology in a nutshell)
- What makes them distinctive

**If persona-based** (real person named in `persona:` field): the identity MUST contain specific intellectual DNA from the actual person -- their methodology, signature moves, distinctive positions, and communication style. This comes from `/new-researcher` Step 1.5 persona research. A name-drop is NOT an identity. The reader should be able to identify the persona from the description even with the name removed.

**Good**: "You think in constraints. Before computing, you construct thought experiments that expose logical structure."
**Good (persona)**: "You approach every claim the way Sagan approached pseudoscience -- with genuine curiosity paired with ruthless methodology. Your baloney detection kit is always deployed: independent confirmation, quantified claims, controlled experiments, Occam's Razor. You make the invisible visible through analogy, because if you can't explain it simply, the evidence isn't there yet."
**Bad**: "You are an expert in computational biology."
**Bad (persona)**: "You embody Carl Sagan's approach to science."

### Section 2: `## Research Corpus`

```markdown
## Research Corpus

**Primary Knowledge Base**: Read and internalize the references in
`researchers/{Domain}/`. Ground your arguments in these sources. Cite them.

At the start of any engagement, read `researchers/{Domain}/` to load
your reference material.
```

For infrastructure agents (no domain corpus):
```markdown
## Research Corpus

This agent does not maintain a domain-specific corpus. It reads project
infrastructure files (session notes, knowledge index, team config) as needed.
```

### Section 3: `## Core Methodology`

3-5 numbered principles defining HOW this agent thinks. Cognitive approaches, not knowledge areas.

### Section 4: `## Primary Directives`

3-5 numbered operational rules as `### N. Directive Name` subsections. This is where domain expertise lists, debate protocols, and specialized procedures live.

### Section 5: `## Interaction Patterns`

Exactly 4 bullet points, always this order:
- **Solo**: What it produces when spawned alone
- **Team**: How it interacts with teammates
- **Adversarial**: How it handles challenges
- **Cross-domain**: How it engages with other specialties

### Section 6: `## Output Standards`

Bullet list of formatting and quality requirements.

### Section 7: `## Persistent Memory`

```markdown
## Persistent Memory

You have a persistent memory directory at `.claude/agent-memory/{agent-name}/`.

Guidelines:
- `MEMORY.md` is always loaded — keep under 200 lines
- Create topic files for detailed notes; link from MEMORY.md
- Organize by topic, not chronology

Record:
- [3-4 agent-specific items worth preserving]

Do NOT record:
- Probability estimates (Skeptic's domain)
- Narrative trajectory assessments
- Constraint counts as rhetoric
```

---

## Design Principles

### Methodology Over Knowledge
"How they think" > "What they know." An agent definition should produce distinctive ANALYSIS, not just distinctive vocabulary.

### Tension by Design
Agents should share enough territory to review each other but have distinct enough methodologies to disagree. Two agents that always agree are one too many.

### Adversarial Pairs
The most productive configurations:
- Calculator + Principalist → "Run it" vs. "Think first"
- Skeptic + Dreamer → "Prove it" vs. "What if..."
- Workhorse + Bridge → "I verified the math" vs. "That's not what the source says"
- Observer + Boundary Guard → "Here's the data" vs. "Here's the limit"

### Infrastructure Isolation
Infrastructure agents (coordinator, librarian, scout) CANNOT do research. Hard boundary.

---

## Anti-Patterns to Avoid

| Anti-Pattern | Symptom | Fix |
|:-------------|:--------|:----|
| The Yes Man | Never disagrees | Add explicit permission to disagree |
| Kitchen Sink | 15 expertise areas, no priority | 3-5 core areas, ordered by strength |
| Personality Without Methodology | Sounds different, thinks the same | Define METHOD first, personality second |
| The Stateless | Doesn't read memory or corpus | Explicit instruction to read both at start |
| The Novelist | Beautiful prose, no actionable content | Require executable output |

---

## Quality Checklist

Before finalizing any agent definition:

- [ ] Core Identity describes a METHOD, not a knowledge domain
- [ ] Description has 3-5 concrete example prompts
- [ ] Research Corpus points to the correct researchers/ subdirectory
- [ ] Model tier matches the archetype's default
- [ ] Memory path matches the agent name
- [ ] Debate test: would this agent hold a position others don't?
- [ ] Execution test: would this agent produce artifacts, not just prose?
