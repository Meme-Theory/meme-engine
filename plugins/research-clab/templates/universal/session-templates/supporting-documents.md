# Supporting Document Formats

Reusable document templates used across all session formats.

---

## Handoff Document

Written at the end of every session. Designed for a reader with NO session context.

```markdown
# Session {{N}} Handoff — Recovery Document
## Date, Branch, Status

## I. What Happened
  {{Team composition, architecture, result summary}}

## II. Task-by-Task Results
  | ID | Task | Agent | Status | Key Result |

## III. Artifacts Produced
  | File | Agent | Purpose |

## IV. Key Numbers to Carry Forward
  | Quantity | Value | Source |

## V. Architecture Notes
  {{What worked, what broke}}

## VI. What's Next
  - Next session prompt: {{path}}
  - Team: {{agents}}
  - Critical task: {{the one thing that matters most}}
  - Prerequisites: {{status}}

## VII. Recovery Instructions
  {{Step-by-step for a fresh context to resume at full speed}}
```

---

## Primer Document

Co-authored by 2 agents BEFORE a session. Establishes conceptual foundation.

```markdown
# Session {{N}} Primer: {{High-Level Title}}
**Date** | **Authors** | **Predecessor**

## I. The Problem Restated
  {{What's established. What's ruled out. The new question.}}

## II. Proposed Framework / Hypothesis
  {{The core idea being tested this session}}

## III. Cross-Domain Connections
  {{Why other fields are relevant}}

## IV. Assessment (Pre-Session)
  {{Calibrated probability ranges with conditional branches}}

## V. Computation Plan
  {{Numbered assignments mapped to sub-sessions}}

## VI. What Constitutes Confirmation vs. Closure
  {{Pre-registered criteria}}
```

---

## Combined Handout

Single document every agent reads before any round of a Workshop or review.

```markdown
# Session {{N}} Combined Handout: Everything We Know

## Part A: What We've Proven
  | # | Result | Method | Script |

## Part B: Recent Results
  {{Per-test summary with pass/fail}}

## Part C: Corrections to Prior Narrative
  | Issue | Old Frame | New Frame |

## Part D: Priority Stack
  Computational priorities (numbered)
  Theoretical priorities (numbered)
  Decision matrix (If... / Then...)

## Part E: Key References
  | Paper | Content | Why It Matters |
```

---

## Session Index

For multi-phase sessions (Investigation Arcs, Workshops), an index enables parallel planning.

```markdown
# Session {{N}} Index

## Overview
{{Probability baseline, context, what this session attempts}}

## Sessions at a Glance
| Session | File | Type | Agents | Dependency | Duration |

## Per-Session Summaries
### Session {{N}}a: {{title}}
Computations: {{list}}
Constraint gates: {{list}}
Output: {{path}}

## Pre-Registered Constraint Gate Summary (All Sessions)
| Gate ID | Session | Condition | Tier | Status |

## What Session {{N}} Is NOT Doing
| Excluded Item | Reason |

## Agent Reference
| Name | Type | Domain | Primary Session |

## Output Files
| File | Content | Session |
```

---

## Plan Scrub Report

Post-computation audit of the pre-registered plan. Written after the first priority runs.

```markdown
# Session {{N}} Plan Scrub

## Summary
| KEEP | CUT | DEMOTE |

## Section 1: KEEP
| Item | Justification |

## Section 2: CUT
| Item | Falsification Reason |

## Section 3: DEMOTE
| Item | New Status | Condition for Promotion |

## Section 4: Source Audit
| Claimed Source | Actual Provenance | Status |

## Section 5: Revised Plan Skeleton
{{What remains after the scrub}}
```

---

## Permanent Results Registry

Cross-session accumulation of proven results. Updated after every session.

```markdown
# Permanent Results Registry

## I. Publishable Standalone Results
| # | Result | Precision | Session | Script |

## II. Machine-Epsilon Verified Infrastructure
| Check | Count | Precision | Session | Script |

## III. Closed Mechanisms
| # | Mechanism | Session | Reason | Wall |

## IV. Gate Verdicts
### PASS Gates
| Gate | Key Number | Session |
### CLOSED Gates
| Gate | Key Number | Session |

## V. Probability Trajectory
| Session | Panel | Skeptic | Key Event |

## VI. Corrections and Retractions
| Original Claim | Correction | Session |
```

---

## Constraint Chain

For investigations with ordered gate dependencies. Each gate only runs if the previous passed.

```markdown
# Constraint Chain: {{Chain Name}}

## Chain Logic
KC-1 -> KC-2 -> KC-3 -> KC-4 -> KC-5
(Failure at any step terminates downstream)

## Chain Table
| Step | Computation | Session | Condition for CLOSED | Status |
|:-----|:-----------|:--------|:--------------------|:-------|
| KC-1 | {{computation}} | {{N}}a | {{exact threshold}} | PENDING |
| KC-2 | {{computation}} | {{N}}b | {{exact threshold}} | BLOCKED by KC-1 |
| KC-3 | {{computation}} | {{N}}c | {{exact threshold}} | BLOCKED by KC-2 |

## Gate Classification
| Type | Definition | Consequence |
|:-----|:----------|:-----------|
| HARD CLOSE | Any one terminates session | All downstream cancelled |
| SOFT GATE | Constrains but does not terminate | Priority modified, work continues |
| POSITIVE SIGNAL | Increases probability | No structural change |

## Outcome Truth Table
| KC-1 | KC-2 | KC-3 | Framework Verdict |
|:-----|:-----|:-----|:-----------------|
| PASS | PASS | PASS | {{best case}} |
| PASS | PASS | CLOSED | {{partial}} |
| PASS | CLOSED | — | {{reduced scope}} |
| CLOSED | — | — | {{chain terminated}} |
```

---

## Living Reference Document

Shared reference maintained continuously across sessions (e.g., symbol glossary, variable registry).

```markdown
# {{Document Title}} — {{Project Name}}

**Last updated**: {{date}}
**Maintainer**: {{designated agent}}
**Scope**: {{what this document covers}}

## Citation Convention
- S## = Session ##
- P## = Paper ##
- Eq ## = Equation reference

## {{Domain Section 1}}
### {{Subsection 1.1}}
`symbol` -- Description sentence. (Source reference)
`symbol` -- Description sentence. (S## T-#, script.py)

### {{Subsection 1.2}}
`symbol` -- Description sentence. (P## eq ##)

## {{Domain Section 2}}
...
```

Key rules:
- One designated maintainer (domain expert, not coordinator)
- Updated after every session that introduces new terms
- Source citations use the established citation language
- `see also` cross-references for related entries
- Living document — revision date always current

---

## Accommodation Audit

Classification of every mechanism as Prediction (P) or Accommodation (A).

```markdown
# Accommodation Audit

| Mechanism | P or A | Justification |
|:----------|:------:|:-------------|
| {{mechanism 1}} | P | Predicted before data was available |
| {{mechanism 2}} | A | Constructed to match known result |
| {{mechanism 3}} | P | Framework predicts specific value, not just consistency |

**Rule**: Only P-class mechanisms count as evidence for the framework.
A-class mechanisms demonstrate consistency but have zero evidential weight.
```
