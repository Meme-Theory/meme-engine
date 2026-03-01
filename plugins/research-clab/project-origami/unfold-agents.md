# Unfold: Agent Selection & Design

**Target agent**: Coordinator
**Task**: Present the archetype menu, help user select domain agents, design persona specs, write the researcher queue.
**Inputs**: Domain, user's research question, user's archetype selections.
**Reads from**: `${CLAUDE_PLUGIN_ROOT}/templates/agent-templates/`, `${CLAUDE_PLUGIN_ROOT}/ARCHETYPES.md` (reference)

---

## Step 1: Present the Archetype Menu

Show the user the available cognitive roles. Frame each by HOW THEY THINK, not what they know:

```
=== AGENT ARCHETYPES ===

CORE ROLES (pick at least 1 Skeptic + 1 Calculator + 1-2 Workhorses):

  1. SKEPTIC       "Prove it."
     Demands methodology, controls, pre-registration. Owns confidence assessment.
     Cannot be skipped -- without adversarial review, everything looks promising.

  2. CALCULATOR     "Stop debating. Run it."
     Produces artifacts: code, data, prototypes. Resolves debates by computing.
     Cannot be skipped -- without execution, nothing gets tested.

  3. WORKHORSE      "I'll work through this properly."
     Deep domain expertise. Shows every step. Catches subtle errors.
     You'll want 1-3 of these in different sub-domains.

  4. PRINCIPALIST   "What MUST be true?"
     Finds structural constraints. Uses thought experiments. Eliminates dead ends.

  5. DREAMER        "What if this is actually THAT?"
     Cross-domain pattern finder. Proposes counterintuitive connections.

  6. BOUNDARY GUARD "Here are the limits."
     Derives hard constraints, impossibility results, resource bounds.

CONNECTOR ROLES (add as the project matures):

  7. OBSERVER       "What does the data say?"
     Works with measurements, error bars, systematic biases. Connects theory to data.

  8. BRIDGE         "The original source says..."
     Fidelity guardian for external work the project builds on.

UTILITY ROLES (optional):

  9. GENERALIST     Broad coverage, no specific lens. Gap-filler.
 10. FORMATTER      Domain-specific document preparation. Add when you need to publish.

INFRASTRUCTURE (already installed -- do NOT select these):
  - Coordinator, Librarian, Scout
```

---

## Step 2: Recommend Selections Based on Domain

Analyze the user's domain and research question. Suggest a starting roster:

### Minimum Viable Team (always recommend)
- **1 Skeptic** -- non-negotiable
- **1 Calculator** -- non-negotiable
- **1-2 Workhorses** in the project's primary sub-domains

### Domain-Specific Suggestions
- Identify 2-3 sub-domains within the user's field -> recommend as Workhorse specializations
- If the project bridges fields -> recommend a Dreamer
- If the project builds on specific external work -> recommend a Bridge
- If the project involves data/experiments -> recommend an Observer
- If the project needs hard limits/bounds -> recommend a Boundary Guard

### Suggest a Principalist from an Adjacent Field
The best Principalists come from fields that share STRUCTURAL features with the main domain but use different vocabulary. Suggest one:
- Physics project -> suggest a Principalist grounded in mathematics or information theory
- Biology project -> suggest one grounded in thermodynamics or network theory
- Software project -> suggest one grounded in formal methods or information theory

Present suggestions but let the user decide. Accept their additions/removals.

---

## Step 3: Design Persona Specs for Each Selection

For each agent the user selects, collect enough detail to write a rich persona spec for `/new-researcher`:

1. **Archetype** -- which template role (skeptic, workhorse, etc.)
2. **Sub-domain name** -- the research area (e.g., "protein folding kinetics")
3. **Persona frame** -- optional real researcher model (e.g., "Linus Pauling-style"), or leave as discipline-based. **When a real person is chosen**: briefly investigate their actual intellectual character -- what they were known for methodologically, what positions they held, how they communicated. The persona spec should carry real content from the person, not just their name as a label. `/new-researcher` will do a deeper investigation (Step 1.5), but the spec should already hint at the person's distinctive intellectual DNA.
4. **Key methodology** -- one sentence on HOW this agent thinks differently. **If persona-based**: this should reference the person's ACTUAL methodology (e.g., "Feynman: reduces everything to first principles and distrusts formalism" not just "Feynman-style physicist")
5. **Color** -- UI color (pick from unused colors)

### Building the Persona Spec

The persona spec is the string that `/new-researcher` receives as its argument. It must be rich enough to generate a well-characterized agent. Combine the archetype's thinking style with the domain:

**For persona-based agents (named after a real researcher):**

Good -- embeds the person's ACTUAL intellectual moves:
```
"Carl Sagan-style empiricist for astrobiology -- baloney detection kit, extraordinary claims require extraordinary evidence, makes the invisible visible through analogy"
"Linus Pauling-style structural chemist -- reasons from bond angles and electronegativity, trusts physical models over computation, relentless about structural constraints"
"Feynman-style calculator for quantum computing -- reduces to first principles, distrusts formalism that can't compute, explains by teaching"
```

Bad -- name-drop without content (DO NOT write specs like these):
```
"Carl Sagan-style empiricist for astrobiology -- demands evidence"
"Linus Pauling-style structural chemist -- thinks about chemistry"
```

**For discipline-based agents (no specific persona):**
```
"protein folding kinetics specialist -- approaches through free energy landscapes and transition state theory"
"lattice QCD computation expert -- trusts numerical integration, benchmarks everything"
```

**Encoding the archetype's methodology:**
The persona spec should naturally embed the archetype's cognitive style:
- Skeptic: include "demands evidence", "adversarial review", "pre-registration"
- Calculator: include "runs it", "produces artifacts", "computational verification"
- Workhorse: include "shows every step", "deep expertise", "catches subtle errors"
- Principalist: include "what must be true", "structural constraints", "thought experiments"
- Dreamer: include "cross-domain", "pattern finder", "what if"
- Boundary Guard: include "hard limits", "impossibility results", "resource bounds"
- Observer: include "measurements", "error bars", "data-driven"
- Bridge: include "original source", "fidelity", "cross-reference"

Example interaction:
```
You selected 2 Workhorses. Let's design them:

Workhorse 1:
  Sub-domain: protein folding kinetics
  Persona: (none -- discipline-based)
  Methodology: Approaches through free energy landscapes and transition state theory
  Color: teal
  -> Persona spec: "protein folding kinetics specialist -- approaches through free energy landscapes and transition state theory, shows every step"

Workhorse 2:
  Sub-domain: molecular dynamics simulation
  Persona: (none -- discipline-based)
  Methodology: Trusts numerical integration over analytical approximation. Benchmarks everything.
  Color: amber
  -> Persona spec: "molecular dynamics simulation specialist -- trusts numerical integration, benchmarks everything, catches subtle numerical errors"
```

---

## Step 4: Write the Researcher Queue

Write `sessions/session-plan/researcher-queue.md` with the information the main orchestrator needs to invoke `/new-researcher`:

```markdown
# Researcher Queue -- Session 0

**Domain**: {project domain}
**Research Question**: {user's research question}
**Date**: {today}

| Persona Spec | Archetype | Papers | Color |
|:-------------|:----------|:-------|:------|
| {persona spec 1} | {archetype} | 14 | {color} |
| {persona spec 2} | {archetype} | 14 | {color} |
| ... | | | |
```

Each row maps directly to a `/new-researcher` invocation:
```
/new-researcher "{Persona Spec}" --archetype {archetype} --papers {N} --color {color}
```

### Quality Check the Persona Specs

Before writing the queue, verify each persona spec:
1. Is it specific enough that `/new-researcher` can generate a distinctive agent? (Not just "skeptic" -- needs domain context)
2. Does it naturally carry the archetype's cognitive flavor? (A skeptic persona should evoke evidence demands even before `--archetype` is applied)
3. Will two different specs produce agents that DISAGREE on methodology? (If they'd always agree, one is redundant)
4. Is it 15-30 words? (Too short = vague agent, too long = noisy)
5. **If persona-based**: does the spec contain at least ONE concrete intellectual move from the actual person? "Sagan-style empiricist" is a name-drop. "Sagan-style empiricist -- baloney detection kit, extraordinary claims require extraordinary evidence" carries real content. The reader should learn something about the person FROM the spec.

---

## Step 5: Update the Registry Placeholder

Update `agents.md` under the "Domain Specialists" section with a preview:

```markdown
### Domain Specialists

(Queued for creation -- {N} agents)

| Archetype | Sub-domain | Status |
|:----------|:-----------|:-------|
| {archetype} | {sub-domain} | Queued |
| ... | ... | ... |
```

The main orchestrator will update this with actual agent names after running `/new-researcher`.

---

## What You Do NOT Do

- **Do NOT create agent definitions** -- `/new-researcher` stamps them from archetype templates
- **Do NOT create agent memory directories** -- `/new-researcher` handles this
- **Do NOT fetch papers** -- `/new-researcher` delegates to web-researcher
- **Do NOT invoke `/new-researcher` yourself** -- you write the queue, the main orchestrator processes it
- **Do NOT force archetype selections** -- user decides (you suggest)
- **Do NOT queue more than 5 domain agents at launch** -- start small, add via `/new-researcher` later
- **Do NOT modify infrastructure agents** -- coordinator, librarian, scout are already installed
- **Do NOT skip the Skeptic** -- if user tries to skip it, explain why it's non-negotiable and ask again

Your job is the agent DESIGN and the researcher queue. The main orchestrator feeds the queue to `/new-researcher`, which does the building.
