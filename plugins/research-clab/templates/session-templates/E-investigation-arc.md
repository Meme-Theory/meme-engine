# Format E: Investigation Arc

## When to Use

Executing a structured series of investigations where results gate each other. Multi-day work with explicit dependency ordering, cost tiers, and phase transitions.

## How to Launch

Investigation Arcs are multi-phase — run `/clab-team` once per phase, gated by prior results:

```bash
# Phase 1: Foundation (fan-out computation)
/clab-team sessions/session-plan/session-17a-prompt.md --mode compute --team-name s17-phase-a

# Phase 2: Verification gate (after Phase 1 completes)
/clab-team sessions/session-plan/session-17b-prompt.md --mode compute --team-name s17-phase-b

# Phase 3: Execution (only if Phase 2 gates CLEARED)
/clab-team sessions/session-plan/session-17c-prompt.md --mode compute --team-name s17-phase-c

# Phase 4: Interpretation (synthesis of all prior phases)
/clab-team sessions/session-plan/session-17d-prompt.md --mode panel --team-name s17-phase-d

# Post-arc mass review: all agents review the final synthesis
/clab-review sessions/session-17/session-17-final.md
```

**Why one invocation per phase**: Each phase depends on the prior phase's results. You must verify gate verdicts between invocations — if Phase 2 returns HARD CLOSE, Phase 3 does not run. The human orchestrator (or the session prompt's gate check protocol) makes this decision.

**Phase 4 uses `--mode panel`**: The final interpretation phase is synthesis, not computation. Agents interpret and converge rather than run scripts. Switch from `compute` to `panel` for this cognitive mode shift.

**Full arc pattern** (with review):

```bash
# Compute phases (sequential, gated)
/clab-team session-17a-prompt.md --mode compute    # Foundation
/clab-team session-17b-prompt.md --mode compute    # Verification gate
/clab-team session-17c-prompt.md --mode compute    # Gated execution
/clab-team session-17d-prompt.md --mode panel      # Interpretation

# Review phase (parallel fan-out)
/clab-review session-17-final.md                   # All 17 agents review
```

## Why This Format Exists

Complex investigations have dependencies — you can't run Phase C until Phase A validates the data. The Investigation Arc makes these dependencies explicit, prevents premature execution of expensive computations, and ensures quality gates are checked before proceeding.

## Recipe

**Team**: 3-5 agents, with team composition changing per phase.

**Flow**:
```
Phase 1: FOUNDATION (Fan-Out)
    Maximum parallelism, zero dependencies, compute-only
         |
Phase 2: VERIFICATION GATE (Sequential)
    Reduced team, explicit PASS/FAIL on Phase 1 results
         |  (only if gates CLEARED)
Phase 3: EXECUTION (Partially Parallel)
    High-stakes gated work that depends on Phase 2
         |
Phase 4: INTERPRETATION (Synthesis)
    Different cognitive mode, synthesizes across all phases
```

**Duration**: Multiple sessions (1 session per phase, or 2-4 phases in one session)

## Plan

```markdown
# Session {{N}} Plan: Investigation Arc

## Phase Map
Phase {{N}}a — {{Title}} ({{MODE: COMPUTE|VERIFY|SYNTHESIZE}})
  Agents: {{list}}
  Tasks: {{count}} (all parallel / sequential / mixed)
       |
       v
Phase {{N}}b — {{Title}} ({{MODE}})
  Agents: {{list}}
  Blocked by: {{N}}a completion
  Tasks: {{count}}

## Task ID Convention
{{AGENT_INITIAL}}-{{NUMBER}}, globally unique across ALL phases.
IDs are NOT reset per phase — they accumulate.

## Dependency Graph
```
B-1 (foundation) ──→ B-2 (verification) ──→ B-5 (execution)
H-1 (foundation) ──→ ─────────────────────→ H-3 (interpretation)
SP-1 (foundation) → SP-2 (blocked by B-2) → SP-3 (execution)
D-1 (foundation) ──→ ─────────────────────→ D-2 (gated by B-3)
```

## Gate Structure
| Gate | Phase | Condition | Blocks |
|:-----|:------|:----------|:-------|
| B-2 CLEARS SP-2 | {{N}}b | All 24 checks PASS | SP-2 in Phase {{N}}b |
| B-3 CLEARS D-2 | {{N}}b | Audit PASS | D-2 in Phase {{N}}c |

## Cost Tiers
| Phase | Cost | Duration | Gate Required |
|:------|:-----|:---------|:-------------|
| {{N}}a | Low | Hours | None |
| {{N}}b | Low | Hours | {{N}}a complete |
| {{N}}c | Moderate | 1 day | {{N}}b gates cleared |
| {{N}}d | Low | Hours | {{N}}c complete |
```

## Phase Prompt Template

Each phase gets its own prompt with this structure:

```markdown
# Session {{N}}{{X}}: {{Title}} — Phase {{M}} of {{Total}}

## Session Type: {{COMPUTE|VERIFY|SYNTHESIZE}}
## Agents: {{phase-specific agent list}}
## Session Goal: {{One sentence}}

# 0. OPERATIONAL RULES
  {{Standard rules + phase-specific additions}}

# I. CONTEXT
  {{Phase-specific context. What prior phases delivered.}}

# II. REQUIRED READING
  {{Per-agent reading lists, phase-specific}}

# III. PRIOR RESULTS (phases 2+ only)
  | ID | Result | Status | Key Numbers | Source |

# IV. CALCULATION ASSIGNMENTS
  ### Assignment {{ID}}: {{Title}} (Priority: {{LEVEL}})
  {{Context sentence}}
  **YOUR TASK**: {{numbered steps}}
  **DELIVERABLE**: {{exact spec}}
  **WHY THIS MATTERS**: {{downstream consumer named}}

# V. COORDINATION
  {{ASCII dependency graph for this phase}}

# VI. SUCCESS CRITERIA
  - [ ] {{per-agent deliverable checklist}}

# VII. INFRASTRUCTURE
  | Script | Lines | What It Does | Who Needs It |
```

## Handoff Between Phases

```markdown
# Session {{N}}a+{{N}}b Handoff — Recovery Document

## I. WHAT HAPPENED
  Per-phase narrative:
  - Team composition
  - Architecture (fan-out / sequential)
  - Result: {{N/N}} deliverables complete

## II. TASK-BY-TASK RESULTS
  | ID | Task | Agent | Status | Key Result |

## III. SCRIPTS PRODUCED
  | Script | Agent | Phase | Purpose |

## IV. KEY NUMBERS TO CARRY FORWARD
  | Quantity | Value | Source |
  {{Only the data the next phase ACTUALLY NEEDS}}

## V. ARCHITECTURE NOTES
  {{What worked, what broke, agent behavior observations}}

## VI. WHAT'S NEXT: Phase {{N}}c
  - Prompt file: {{path}}
  - Team: {{agents}}
  - Critical task: {{which task is the critical path}}
  - Prerequisites: {{status of each}}
  - Critical numbers for next agents: {{specific values to pass in}}
```

## Final Synthesis Document

Written by a SEPARATE synthesis team, not the working agents:

```markdown
# Session {{N}}: Complete Synthesis

## I. Executive Summary
## II. Complete Deliverable Table
  | # | ID | Phase | Deliverable | Agent | Key Result |

## III. PROVEN (Machine Epsilon or Exact)
## IV. FOUND (New Discoveries)
## V. FALSIFIED (Disproven Hypotheses)
## VI. INCONCLUSIVE (Unresolved)

## VII. Framework Probability Assessment
  Per assessor (named): Range, Median, Movement, Reasoning

## VIII. Priority List (Post-Session)
  Tiered: DECISIVE / HIGH / MEDIUM / DEFERRED

## IX. Closing Remarks
  Per-assessor paragraph in their characteristic voice
```

## Failure Modes This Format Prevents

| Problem | How This Format Handles It |
|:--------|:--------------------------|
| Running expensive computation before validating inputs | Phase 2 is always a quality gate |
| Losing state between phases | Handoff document written for recovery (no session context assumed) |
| Working agents marking their own homework | Final synthesis written by a separate team |
| Task IDs colliding across phases | Global task ID scheme (never reset per phase) |
