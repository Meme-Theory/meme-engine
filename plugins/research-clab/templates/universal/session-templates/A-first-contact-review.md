# Format A: First Contact Review

## When to Use

Opening investigation of a new topic or body of work. You want diverse independent assessments before any investigation begins.

## How to Launch

This is a fan-out of independent reviews — use `/rclab-review`:

```bash
# Full roster (all 17 agents review the document independently)
/rclab-review sessions/session-01/source-material.md

# Targeted subset (4-6 agents relevant to the new topic)
/rclab-review sessions/session-01/source-material.md --agents principalist,calculator,workhorse-1,workhorse-2,skeptic,bridge

# First pass only (skip synthesis to see raw assessments before reframing)
/rclab-review sessions/session-01/source-material.md --skip-synthesis

# Reframing pass (after reviewing first-pass results, run a second review)
/rclab-review sessions/session-02/reframing-directive.md --agents principalist,calculator,workhorse-1,workhorse-2,skeptic,bridge
```

**Why `/rclab-review`**: First Contact is pure fan-out — agents work independently, no inter-agent communication needed. `/rclab-review` launches agents in background batches and auto-synthesizes. No live team coordination required.

## Why This Format Exists

Without it, the first agent to assess a topic frames all subsequent thinking. Multiple independent lenses catch framing biases that no single perspective reveals. The reframing step (Session 2's innovation) was invented because the first-pass assessment carried hidden assumptions that materially changed 5 of 18 conclusions.

## Recipe

**Team**: 4-6 specialist agents + 1 coordinator. Each specialist covers a different domain or methodology.

**Flow**:
```
1. DISTRIBUTE — Combined handout of source material to all agents
2. FAN-OUT — Each specialist produces independent assessment (no inter-agent communication)
3. GATHER — Coordinator collects all assessments
4. SYNTHESIZE — Coordinator extracts convergences, divergences, cross-cutting themes
5. REFRAME — Second pass questioning assumptions of the first pass
```

**Duration**: 1-2 sessions (first pass + reframing pass)

## Plan

```markdown
# Session {{N}} Plan: First Contact Review

## Objective
Produce a multi-lens assessment of {{topic/document}} from {{N}} independent perspectives.

## Agent Roster
| Agent | Domain | Assigned Angle |
|:------|:-------|:---------------|
| {{agent-1}} | {{domain}} | {{what to look for}} |
| ...

## Source Material
{{List of documents/papers being reviewed}}

## Deliverables
1. Per-agent assessment (150-400 lines each)
2. Cross-team synthesis with convergences/divergences
3. Tiered priority list for next investigation
4. Component credibility ranking

## Reframing Pass (Session N+1)
After initial assessments, run a second session asking:
- Which criticisms survive under a different epistemic frame?
- Which are artifacts of the assessors' assumptions?
- What changes when you separate observation from interpretation?
```

## Prompt Template

```markdown
# Session {{N}}: First Contact Review — {{Topic}}

## Session Type: FAN-OUT REVIEW
## Agents: {{4-6 agents}}
## Session Goal: Produce independent multi-lens assessment of {{topic}}.

# I. CONTEXT
{{Brief description of the topic and why it matters}}

# II. DOCUMENTS UNDER REVIEW
{{Numbered list of source documents with paths}}

# III. YOUR ASSIGNMENT
Read all documents. Produce an independent assessment from your domain's perspective.

Your report MUST include:
1. Component-by-component credibility ranking (table)
2. Strongest claims (with evidence)
3. Weakest claims (with specific objections)
4. What computation would settle the open questions
5. Your framework probability estimate (range, not point)

DO NOT read other agents' assessments before writing yours.

# IV. OUTPUT
Write your assessment to: `sessions/session-{{N}}/session-{{N}}-{{your-name}}-review.md`

# V. SUCCESS CRITERIA
- [ ] All source documents read
- [ ] Component ranking produced
- [ ] Specific objections stated (not vague concerns)
- [ ] At least one computation identified that would be decisive
```

## Synthesis Step

After all agents report, the coordinator produces:

```markdown
# Session {{N}} Synthesis

## Cross-Cutting Agreements
{{What all agents independently converged on}}

## Cross-Cutting Disagreements
{{Where assessments diverge, with each agent's position}}

## Synthesis Questions
Q1: {{Question bridging two disagreeing assessments}}
A1: {{Resolution or explicit "OPEN"}}

## Component Credibility Ranking (Combined)
| Component | Agent 1 | Agent 2 | ... | Consensus |

## Priority List
### Tier 0: Critical Path
### Tier 1: Important
### Tier 2: Worth investigating
### Tier 3: Deferred
```

## Failure Modes This Format Prevents

| Problem | How This Format Handles It |
|:--------|:--------------------------|
| Framing bias from first assessor | Independent parallel review — no agent sees others' work |
| Hidden assumptions in critique | Reframing pass explicitly questions the critique's premises |
| Vague objections | "Specific objections" and "decisive computation" requirements |
