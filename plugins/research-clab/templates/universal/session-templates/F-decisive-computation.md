# Format F: Decisive Computation

## When to Use

Single-objective sprint. One computation, pre-registered gates, clear pass/fail. The question is well-defined and the computation is scoped.

## How to Launch

Decisive computations are focused sprints — use `/rclab-team --mode compute`:

```bash
# Launch the computation sprint
/rclab-team sessions/session-plan/session-18-prompt.md --mode compute --team-name s18-veff

# Dry run to verify assignments and gate pre-registration
/rclab-team sessions/session-plan/session-18-prompt.md --mode compute --dry-run

# After sprint completes, run wrap-up review with a small panel
/rclab-team sessions/session-plan/session-18-wrapup-prompt.md --mode panel --team-name s18-wrapup
```

**Why `--mode compute`**: The session exists to run scripts, produce numerical results, and classify them against pre-registered gates. Compute mode is task-driven — agents work through TaskList items, not free-form discussion.

**The wrap-up is a separate invocation**: The sprint produces numbers; the wrap-up interprets them. These are different cognitive modes (compute vs. panel) and different agent teams (builder+validator vs. interpreters). Always separate them.

## Why This Format Exists

When the investigation has funneled down to a single decisive computation, you don't need a workshop — you need focused execution with minimal overhead and maximum rigor.

## Recipe

**Team**: 2-3 agents (1 builder + 1 validator + coordinator).

**Flow**:
```
1. BRIEF — Combined context from prior sessions (what's proven, what's open)
2. COMPUTE — Builder executes the computation against a pre-registered specification
3. VALIDATE — Validator checks results (separate from builder)
4. VERDICT — Gate classified against pre-registered criteria
5. WRAP-UP — Separate 2-3 agent team synthesizes implications
```

**Duration**: 1 session (hours)

## Prompt Template

```markdown
# Session {{N}}: {{Computation Name}} — Decisive Sprint

## Session Type: DECISIVE COMPUTATION (Single-objective sprint)
## Agents: {{builder}} + {{validator}} + coordinator
## Session Goal: {{Compute X and classify against pre-registered gate Y.}}

# I. WHY THIS SESSION EXISTS
  {{Narrative from prior sessions. The one thing that remains.
    Quote wall from prior agents reinforcing urgency.}}

# II. WHAT WE KNOW AND WHAT'S MISSING
  {{Done item 1}}
  {{Done item 2}}
  {{Missing: THE THING THIS SESSION COMPUTES}}

# III. REQUIRED READING
  ## All agents:
  - {{combined handout}}
  ## {{Builder}} additionally:
  - {{specific equations, prior scripts}}

# IV. ASSIGNMENTS

## {{Builder}}: Assignment {{ID}} — {{Build and Execute}}
**Priority: CRITICAL**
{{Background paragraph}}
### Computation Steps
1. {{Step with code snippet}}
2. {{Step with code snippet}}
#### Deliverable
{{Exact output format and precision}}
**Write to**: `{{filename.py}}`

## {{Validator}}: Assignment {{ID}} — {{Validate}}
**Priority: HIGH**
### Validation Checks
1. {{Independent check}}
2. {{Consistency check}}

# V. WORKFLOW
  Phase 1 (parallel): Builder computes, Validator prepares checks
  Phase 2 (sequential): Validator checks Builder's output

# VI. PRE-REGISTERED GATES
  | Gate | Condition | Classification |
  |:-----|:---------|:--------------|
  | {{ID}} | {{threshold}} | PASS / CLOSED |

# VII. OUTPUT
  ## Designated writer: coordinator
  Must contain:
  1. Computation result (exact numbers)
  2. Validation checks (all PASS/FAIL)
  3. Gate verdict (against pre-registered criteria)
  4. Interpretation (2-3 sentences, no more)
  5. What this changes for the next session

# VIII. WHAT THIS SESSION DOES NOT DO
  {{Explicit scope boundary}}
```

## Wrap-Up Document (Separate Team)

```markdown
# Session {{N}} Wrap-Up: {{Implications}}

## I. Result Summary
  | Outcome | What Is NOT Closed | What Survives |

## II. Pre-Registered Decision Tree
  | Scenario | Probability | Outcome |
  **THIS ONE ->** {{highlight the actual outcome}}

## III. Candidate Next Steps
  ### Candidate 1: {{Path}}
  | Sub-route | Status | Verdict |

## IV. Reframing
  {{How the result changes the larger picture}}
```

## Failure Modes This Format Prevents

| Problem | How This Format Handles It |
|:--------|:--------------------------|
| Builder validates their own work | Separate validator agent |
| Goalpost-moving after result | Pre-registered gates with explicit thresholds |
| Scope creep into "let's also check..." | "WHAT THIS SESSION DOES NOT DO" section |
| Over-interpreting numbers | "Interpretation: 2-3 sentences, no more" |
