# Universal Session Infrastructure

These conventions apply to ALL session formats. Every session uses them.

## Prompt Document Skeleton

Every session prompt follows this structure:

```markdown
# Session {{N}}: {{Title}} — {{Subtitle}}

## Session Type: {{FORMAT_LABEL}} (e.g., "Decisive Computation", "Workshop Round 1")
## Agents: {{agent-1}} + {{agent-2}} + ...
## Session Goal: {{One sentence. Verb. Concrete deliverable.}}

---

# 0. OPERATIONAL RULES — READ BEFORE ANYTHING ELSE
  - Computation discipline: "Report the number first. Classify second. Interpret third."
  - Completion signal: "SESSION {{N}} COMPLETE — all agents confirm."
  - Message protocol: "Work step, then inbox. Work step, then inbox."
  - Output directory: {{path}}
  - Script prefix: s{{N}}_

# I. CONTEXT
  {{Prior session state. What happened. What this session picks up.}}

# II. REQUIRED READING
  ## All agents:
  - {{path/to/combined-handout.md}}
  ## {{agent-name}} additionally:
  - {{path/to/specific-file.md}} — sections X, Y

# III. PRIOR RESULTS (if continuing from previous phase)
  | ID | Result | Status | Key Numbers | Source |

# IV. CALCULATION ASSIGNMENTS
  ### Assignment {{ID}}: {{Title}} (Priority: {{CRITICAL|HIGH|MEDIUM}})
  {{1-sentence context — where this fits in the larger chain}}

  **YOUR TASK**:
  1. {{Numbered action step}}
  2. {{Numbered action step}}

  **DELIVERABLE**: {{Exact format, precision, parameter sweeps, binary verdict language}}

  **WHY THIS MATTERS**: {{2-4 sentences on downstream impact}}

# V. COORDINATION
  {{Dependency graph (ASCII). Interaction rules. Blocking conditions.}}

# VI. SUCCESS CRITERIA
  Per agent:
  - [ ] {{Deliverable with exact precision target}}

# VII. OUTPUT FILES
  | File | Content | Format | Producer |
  |:-----|:--------|:-------|:---------|

---
*{{Closing quote framing the session's stakes}}*
```

## Constraint Gate System

Every investigation uses pre-registered gates. State these BEFORE computation.

**Binary gate** (early sessions):
```markdown
## Gate {{ID}}
- **OPEN**: {{criterion for continuing investigation}}
- **CLOSED**: {{criterion for definitively ruling out this path}}
```

**5-tier Bayesian gate** (mature sessions):
```markdown
## Pre-Registered Constraint Gates

| Tier | Criterion | Bayes Factor | Prob Shift |
|:-----|:----------|:-------------|:-----------|
| DECISIVE | {{exact threshold}} | 20 | +12-15 pp |
| COMPELLING | {{exact threshold}} | 8 | +6-10 pp |
| INTERESTING | {{exact threshold}} | 3 | +2-4 pp |
| NEUTRAL | {{exact threshold}} | 1 | 0 pp |
| CLOSED | {{exact threshold}} | 0.3 | -4-8 pp |
```

**Gate verdict format** (written after computation):
```markdown
## Gate {{ID}}
- Pre-registered threshold: {{verbatim from prompt}}
- Result: {{actual finding}}
- Classification: PASS / CLOSED / FAIL
- Compliance: {{did result match pre-registered criteria?}}
```

## Team Launch Protocol

Every session follows this exact team creation sequence:

1. **Spawn agents** with minimal prompts ("Wait for instructions")
2. **Wait** for ALL agents to idle
3. **Roster blast** — send roster to every agent as their FIRST inbox message
4. **THEN** send real work assignments

## Output Discipline

- **One writer per file.** Others contribute via messages to the designated writer.
- **Coordinator never generates primary content.** Coordinator assembles, routes, tracks.
- **Only the Skeptic states confidence.** All other agents are banned from expressing probability estimates as authoritative.
- **Constraints, not failures.** Negative results are documented as constraints on the solution space, not project failures.

## Handoff Protocol

Every session MUST produce a handoff document (see [Supporting Documents](supporting-documents.md)).

## Session Output Document Structure

Every session output (meeting minutes, synthesis) follows this skeleton:

```markdown
# Session {{N}}: {{Title}}
**Date** | **Team** | **Agents** | **Designated Writer**

## Active Agents
| Agent | Role | Assignments | Status |

## Executive Summary
{{2-3 bold-text sentences: conclusion, what closes, what survives}}

## Task Results
### {{Task-ID}}: {{Title}} ({{Agent}}) — {{COMPLETE|INCOMPLETE}}
Script: `{{path/to/script.py}}`
Data: `{{path/to/data.npz}}`
{{Bullet results with key numbers}}

## Convergences
## Disagreements (with Resolution status)

## Framework Probability
| Source | Range | Median | Movement |

## Priority List (Post-Session)
| Tier | Item | Decisiveness | Feasibility | Timeline |

## Scripts Produced
| Script | Agent | Purpose | Lines | Runtime |

## Session in One Paragraph
{{~200 word standalone summary}}

---
*Compiled by {{coordinator}}, ~{{N}} hours. {{N}} scripts, {{N}} deliverables.*
```
