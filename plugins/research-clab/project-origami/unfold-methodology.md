# Unfold: Session & Methodology System

**Target agent**: Coordinator
**Task**: Configure the session architecture, handoff protocol, and constraint methodology.
**Inputs**: Project name, domain.
**Reads from**: `${CLAUDE_PLUGIN_ROOT}/templates/universal/session-templates/`, `${CLAUDE_PLUGIN_ROOT}/METHODOLOGY.md` (reference)

---

## Step 1: Create Session-Plan Infrastructure

The `sessions/session-plan/` directory should already exist (created by unfold-structure). Populate it:

### Selection Guide

Copy `${CLAUDE_PLUGIN_ROOT}/templates/universal/session-templates/selection-guide.md` → `sessions/session-plan/format-selection-guide.md`

This is the decision tree users consult when planning a session. It maps research needs to session formats.

### Format Reference

Session format templates (A through I, plus infrastructure and supporting docs) are copied into `.claude/templates/session-templates/` by unfold-structure Step 4b. Agents consult these locally when planning sessions — no need to reference the plugin at runtime.

---

## Step 2: Configure the Constraint Methodology

Write `sessions/framework/constraint-methodology.md` with this content:

```markdown
# Constraint Methodology

## Pre-Registration

Every investigation gets pre-registered gates BEFORE execution:

### Gate Format
- **Gate ID**: [PROJECT]-[NUMBER] (e.g., PF-1, AT-3)
- **Condition**: Exact threshold or criterion
- **PASS**: What constitutes success
- **CLOSED**: What constitutes definitive failure
- **Source**: Where this threshold was defined

### Why Pre-Registration Matters
Without pre-registration, every result gets retroactively interpreted as supportive.
The Skeptic agent enforces this. It is the single most important methodological rule.

## Constraint Mapping

Every negative result is documented as a CONSTRAINT, not a "failure":

> **Constraint [ID]**: [What was demonstrated].
> **Source**: [Session, task ID].
> **Implication**: [What approaches this rules out].
> **Surviving space**: [What remains viable].

The count of constraints tells you exploration coverage, not project viability.

## Confidence Trajectory

One designated agent (Skeptic archetype) maintains the running confidence assessment.
Only one agent produces confidence estimates. Others may NOT state them as authoritative.

## Authority Hierarchy

Skeptic verdicts > synthesis files > gate results > session minutes > raw data
```

---

## Step 3: Configure the Handoff Protocol

Write `sessions/framework/handoff-template.md`:

```markdown
# Session [NN] Handoff

## I. What Happened
[Team composition, architecture, narrative summary]

## II. Results Table
| ID | Task | Agent | Status | Key Result |
|:---|:-----|:------|:-------|:-----------|

## III. Artifacts Produced
| File | Agent | Purpose |
|:-----|:------|:--------|

## IV. Key Findings to Carry Forward
| Quantity | Value | Source |
|:---------|:------|:-------|

## V. Architecture Notes
[What worked, what broke, runtime observations]

## VI. What's Next
[Next session references, critical tasks, prerequisites]

## VII. Recovery Instructions
[Step-by-step for a fresh context to resume at full speed]
```

---

## Step 4: Write Coordinator Memory Seed

Write to `.claude/agent-memory/coordinator/MEMORY.md`:

```markdown
# Coordinator Memory

## Session Patterns Available
- **Format A**: First Contact Review — fan-out to 4-6 agents
- **Format B**: Adversarial Debate — 3-5 agents take positions
- **Format C**: Collaborative Deep Dive — focused investigation
- **Format D**: Workshop — sequential small-group rounds
- **Format E**: Investigation Arc — dependency-ordered work
- **Format F**: Decisive Computation — single-objective sprint with gates
- **Format G**: Mass Parallel Assessment — 8-17 agents review independently
- **Format H**: Decision Gate — binary routing based on outcome
- **Format I**: Formalization — consolidate N sessions into status doc

See `sessions/session-plan/format-selection-guide.md` for decision tree.
See `.claude/templates/session-templates/` for full format definitions.

## Methodology
- Pre-register ALL gates before investigation
- Constraints are progress, not failures
- One Skeptic owns confidence — no one else states odds
- Handoff doc is mandatory at session end

## Active State
(empty — populated during sessions)
```

---

## Step 5: Initialize the Constraint Map

Write `.claude/agent-memory/coordinator/constraint-map.md`:

```markdown
# Constraint Map — {Project Name}

## Active Constraints
(none yet)

## Gate Registry
(none yet — gates are registered per-session in session prompts)

## Confidence Trajectory
| Session | Confidence | Key Event |
|:--------|:-----------|:----------|
| 0       | —          | Project initialized |
```

---

## What You Do NOT Do

- **Do NOT modify session templates** — they are reference documents copied verbatim by unfold-structure
- **Do NOT pre-populate constraints** — they accumulate from actual investigation
- **Do NOT write confidence estimates** — that's the Skeptic's exclusive domain
- **Do NOT create session-01/ yet** — only session-00/ and session-plan/ exist at project birth

Your job is the methodology scaffold. Actual research populates it.
