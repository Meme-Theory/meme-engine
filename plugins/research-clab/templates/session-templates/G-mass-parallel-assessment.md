# Format G: Mass Parallel Assessment

## When to Use

Extracting maximum insight from completed work. You have results and want 8-17 agents to independently review them before synthesis.

## How to Launch

Mass parallel assessment IS what `/clab-review` was built for:

```bash
# Full roster — all 17 agents review independently, then auto-synthesize
/clab-review sessions/session-19/session-19d-casimir-energy.md

# Targeted review — 6 agents most relevant to the topic
/clab-review sessions/session-19/session-19d-casimir-energy.md --agents principalist,boundary-guard,dreamer,workhorse-1,workhorse-2,skeptic

# Skip synthesis to inspect individual reviews before combining
/clab-review sessions/session-19/session-19d-casimir-energy.md --skip-synthesis

# After inspecting reviews, run synthesis manually with a smaller panel
/clab-team sessions/session-plan/session-19d-synthesis-prompt.md --mode panel --team-name s19d-synthesis

# Cross-evaluation: have specific agents review other agents' collabs
/clab-review sessions/session-19/session-19d-calculator-collab.md --agents dreamer,observer
```

**Scaling the fan-out**: `/clab-review` launches agents in batches of 5-6 (three batches). The full 17-agent roster produces 150-400 lines per agent = 2,500-6,800 lines of independent analysis, then auto-synthesizes into a master collab.

**The cross-evaluation pattern**: After the first fan-out, select 2-3 agents to review other agents' collab files. This catches overclaims and produces the "New Ideas From the Collaboration" section — insights that emerge only from the collision of perspectives.

**Full pipeline** (as used in Session 19d):

```bash
# Step 1: Mass review (all 17 agents)
/clab-review sessions/session-19/session-19d-casimir-energy.md

# Step 2: Cross-evaluations (targeted)
/clab-review sessions/session-19/session-19d-calculator-collab.md --agents dreamer,observer
/clab-review sessions/session-19/session-19d-dreamer-collab.md --agents calculator,observer

# Step 3: Master synthesis (panel assembles the master collab from all reviews)
/clab-team sessions/session-plan/session-19d-master-prompt.md --mode panel --team-name s19d-master
```

## Why This Format Exists

Many specialists reading the same results independently produces connections that no individual would generate. The synthesis step is where cross-pollination happens — ideas emerge from the collision of perspectives that weren't in any single review.

## Recipe

**Team**: 8-17 specialist agents + 1 synthesis writer. Optionally: 2-3 cross-evaluation agents.

**Flow**:
```
1. PRE-COLLAB DIRECTIVE — Brief all agents with the same document
2. FAN-OUT — Each agent writes an independent collab review (150-400 lines)
3. CROSS-EVALUATION (optional) — Select agents review other agents' collabs
4. SYNTHESIS — Synthesis agent reads ALL reviews, produces master document
5. MASTER COLLAB — Theme-organized document with emergent cross-pollination insights
```

**Duration**: 1-2 sessions

## Pre-Collab Directive Format

```markdown
# Session {{N}} Pre-Collab: {{Topic}}

## I. Context
{{What happened. The 4 walls / constraints / key results.}}

## II. What You're Reviewing
{{Specific document(s) to read. Path(s).}}

## III. Your Task
Produce a session-{{N}}-{{your-name}}-collab.md containing:
1. Key observations (3-5, narrative paragraphs, not bullets)
2. The central discovery/question (deep dive with equations)
3. Collaborative suggestions: what YOU would compute next (prioritized)
4. Connections to YOUR domain
5. Open questions (things to compute, not debate)
6. Summary assessment with framework probability estimate

## IV. Operating Principles
{{Methodological rules for this review}}
```

## Individual Collab File Format

```markdown
# {{Agent Name}} Collaborative Review: Session {{N}}
**Date**: {{date}}
**Reviewer**: {{agent-name}}
**Reviewing**: {{file path}}

## 1. Key Observations: {{Thematic Title}}
{{3-5 narrative observations, each labeled and titled}}

## 2. The Central Discovery
{{Deep dive — equations, tables, code blocks}}

## 3. Collaborative Suggestions: What I Would Compute Next
### 3a. Priority 1: {{Task name}}
  Background | Steps | Validation | Output

## 4. Connections to {{My Domain}}
{{How this maps to the agent's expertise}}

## 5. Open Questions
Q1: {{Question with computation steps}}

## Summary Assessment
{{1-3 paragraphs. Framework probability from this agent's perspective.}}
```

## Cross-Evaluation Format (Agent reviewing another agent's collab)

```markdown
# {{Agent}}: Evaluation of {{Other Agent}}'s Review

## 1. Overall Assessment
## 2. Where {{Other Agent}} Is Right (Genuine Overclaims)
## 3. Where {{Other Agent}} Misses (Things They Didn't See)
## 4. Synthesis: The Dialogue Between Both Perspectives
```

## Synthesis Document Format

```markdown
# Session {{N}} Synthesis: {{Topic}}
## {{Memorable subtitle}}
### {{N}} Agent Reviews Synthesized

## THE ONE-PARAGRAPH VERSION
{{Single dense paragraph. Written to stand alone.}}

## I. What Happened
### The Result
| Key Number | Value | Closure Threshold |
### The Discovery Inside the Closure
{{Unexpected finding}}

## II. Agent Consensus and Divergences
### Universal Agreement ({{N/N}} agents)
{{Numbered list}}
### Key Agent-Specific Contributions
**{{Agent}}**: {{unique contribution paragraph}}
{{One paragraph per agent — their distinct contribution}}

## III. Paths Forward
### Track A: {{Fast path}} ({{time}})
### Track B: {{Comprehensive path}} ({{time}})

## IV. Structural Insights
{{Ideas that emerged from cross-pollination, not in any single review}}

## V. Framework Probability
Range: {{X-Y%}}

## VI. Session {{N+1}} Priorities (Ranked)
```

## Master Collab Format (Theme-Organized Cross-Pollination)

```markdown
# Master Collaborative Synthesis: Session {{N}}
## {{N}} Researchers, {{M}} Cross-Evaluations

## I. Executive Summary
## II. Major Theme 1
  *Anchored by: {{collab file link}}*
  *Cross-evaluated by: {{cross-eval link}}*
  ### The Computation Pipeline
  ### PRE-REGISTERED CONSTRAINT Criteria
  ### The {{A}}-{{B}}-{{C}} Dialogue
  | Question | Agent A | Agent B | Resolution |

## III. Convergent Themes Across All Reviews
### A. {{Theme}} ({{N/N}} unanimous)
### B. {{Theme}}

## IV. New Ideas From the Collaboration
{{Ideas that emerged from cross-pollination, not in any single review}}
### IV-A. {{Emergent idea}} ({{contributing agent}})

## V. Probability Assessments
| Reviewer | Probability |
**Consensus range**: {{X-Y%}}

## VI. Priority-Ordered Next Session Agenda
```

## Failure Modes This Format Prevents

| Problem | How This Format Handles It |
|:--------|:--------------------------|
| Echo chamber (agents reinforcing each other) | Independent reviews — no agent sees others' work before writing |
| Missing cross-domain connections | Cross-evaluation step + "New Ideas" section in master collab |
| Losing individual contributions in synthesis | Per-agent paragraph in synthesis preserves unique credit |
| Consensus without substance | "One-paragraph version" forces distillation to a testable claim |
