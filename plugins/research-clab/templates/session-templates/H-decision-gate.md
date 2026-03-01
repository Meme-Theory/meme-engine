# Format H: Decision Gate

## When to Use

Binary routing session. The purpose is to determine which of two (or more) sessions runs next. The session produces a verdict, not a synthesis.

## How to Launch

Decision gates are minimal compute sprints — use `/clab-team --mode compute`:

```bash
# Run the gating computation
/clab-team sessions/session-plan/session-20a-prompt.md --mode compute --team-name s20a-gate

# After the gate verdict, launch the appropriate branch:
# If OPEN:
/clab-team sessions/session-plan/session-20b-prompt.md --mode compute --team-name s20b-open
# If CLOSED:
/clab-team sessions/session-plan/session-20b-alt-prompt.md --mode compute --team-name s20b-closed

# Post-gate mass review (optional — have all agents assess the gate outcome)
/clab-review sessions/session-20/session-20a-decision-gate.md
```

**Why `--mode compute`**: Decision gates produce numbers and classify them — that's compute mode. The team is small (2 agents + coordinator) and the session is short. The verdict file (`gate_verdicts.txt`) is the primary output, not a synthesis document.

**The branching happens between invocations**: The human reads the gate verdict and decides which prompt to run next. This is intentional — binary routing decisions should not be automated. The human is the circuit breaker.

**Chaining with conditional sub-sessions** (Sessions 28-29 pattern):

```bash
# Sub-session A: run gating computations
/clab-team sessions/session-plan/session-28-prompt-a.md --mode compute --team-name s28a

# Check gate verdicts before launching B
# (Read s28a_gate_verdicts.txt — if HARD CLOSE, stop)

# Sub-session B: conditional computations (reads A's verdicts)
/clab-team sessions/session-plan/session-28-prompt-b.md --mode compute --team-name s28b

# Sub-session C: constraint chain completion (reads B's verdicts)
/clab-team sessions/session-plan/session-28-prompt-c.md --mode compute --team-name s28c

# Post-chain synthesis: mass review of all results
/clab-review sessions/session-28/session-28c-results.md
```

## Why This Format Exists

When the next session's entire scope depends on the outcome of a single computation, you need a session format optimized for clean decision-making — no interpretation creep, no hedging, just "OPEN or CLOSED."

## Recipe

**Team**: 2 agents (1 builder + 1 analyst) + coordinator.

**Flow**:
```
1. COMPUTE — Execute the gating computation(s)
2. CLASSIFY — Binary verdict against pre-registered criteria
3. ROUTE — Assign the next session based on the verdict
```

**Duration**: Short (hours)

## Prompt Template

```markdown
# Session {{N}}a: Decision Gate

## Session Type: DECISION GATE
## Agents: {{builder}} + {{analyst}} + coordinator
## Session Goal: Determine whether Path A or Path B for Session {{N}}b.

# IV. DECISION GATE
| Result | Interpretation | Impact on Session {{N}}b |
|:-------|:--------------|:------------------------|
| {{ID}} OPEN + {{ID}} validated | {{meaning}} | {{session scope}} |
| {{ID}} CLOSED + {{ID}} validated | {{meaning}} | {{different scope}} |
| {{ID}} OPEN + {{ID}} fails | {{meaning}} | {{different scope}} |

# V. DELIVERABLES
1. Gate verdicts file: `s{{N}}a_gate_verdicts.txt`
2. Decision gate outcome document
3. Session {{N}}b scope assignment
```

## Decision Gate Output Format

```markdown
# Session {{N}}a: Decision Gate Outcome

## I. Deliverables
| Task | Agent | Status | Output |

## II. Per-Task Results
### {{Task ID}}: {{Result with numbers}}

## III. Gate Outcome
{{The exact decision table from the prompt, filled in with actual results}}

## IV. Implications for Session {{N}}b
{{Which branch fires. What the next session's scope is.}}

## V. Stabilization Status Ledger
| Mechanism | Status | Session | Evidence |

## VI. Framework Probability
{{No update / Updated to X, with reason}}
```

## Conditional Sub-Session Routing (Advanced)

For sessions with conditional branching between sub-sessions:

```markdown
# 0. OPERATIONAL RULES — GATE CHECK
Before ANY computation in this sub-session:
1. Read `s{{N}}a_gate_verdicts.txt`
2. If HARD CLOSE fired: do NOT proceed. Report to coordinator.
3. If all gates passed: proceed normally.
4. If SOFT GATE triggered: proceed with modified priority.
```

## Failure Modes This Format Prevents

| Problem | How This Format Handles It |
|:--------|:--------------------------|
| Hedging on binary decisions | Pre-registered decision table with exact thresholds |
| Interpretation creep (turning CLOSED into "maybe") | Verdict file is a flat text file, not a narrative |
| Downstream sessions running on stale assumptions | Gate check protocol reads verdict file before proceeding |
