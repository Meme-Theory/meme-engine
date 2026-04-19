# Format C: Collaborative Deep-Dive

## When to Use

Focused investigation of a specific problem, typically producing a computation specification or research plan. One agent leads; others verify, extend, and challenge.

## How to Launch

Deep-dives are live teams producing a specification — use `/rclab-team --mode panel`:

```bash
# Panel mode — agents discuss and converge on a specification
/rclab-team sessions/session-plan/session-06-deepdive-prompt.md --mode panel

# With explicit team name
/rclab-team sessions/session-plan/session-06-deepdive-prompt.md --mode panel --team-name deepdive-algebra

# If the deep-dive involves actual computation (not just specification)
/rclab-team sessions/session-plan/session-06-compute-prompt.md --mode compute
```

**Why `--mode panel`** (not compute): Deep-dives produce a *specification*, not computed results. Agents discuss, challenge, and converge on a research plan with dependency graphs and pass/fail criteria. If the session involves running scripts and producing `.npz` files, use `--mode compute` instead.

**When to switch to compute**: If the deep-dive prompt contains `## COMPUTATIONS`, script prefixes, or `.npz` references, rclab-team auto-detects compute mode anyway. But if you want a specification session that happens to reference prior scripts, explicitly set `--mode panel`.

## Why This Format Exists

After broad reviews and adversarial debates identify the critical question, you need a focused session to produce an executable plan — not more assessment, but a specification with milestones, dependencies, and pass/fail criteria.

## Recipe

**Team**: 3-5 specialists + coordinator. One specialist is designated LEAD. The lead drives the investigation; others verify from their domain.

**Flow**:
```
1. PRIOR CORRECTION — State what the prior session got wrong (if anything)
2. PARALLEL ANALYSIS — All agents independently identify the flaw/path
3. CONVERGE — Check for agreement on the correction/approach
4. SPECIFY — Build computation roadmap with steps, timelines, deliverables
5. GATE — Define success, partial success, and failure criteria
```

**Duration**: 1 session

## Prompt Template

```markdown
# Session {{N}}: Collaborative Deep-Dive — {{Problem}}

## Session Type: COLLABORATIVE DEEP-DIVE
## Agents: {{3-5 agents}}
## Session Goal: Produce executable specification for {{computation/investigation}}.

# I. THE PROBLEM
{{Prior session's leading claim, the specific flaw or question, the correct framing}}

# II. PRIOR STATE
{{What Sessions N-1 and N-2 established. What's open.}}

# III. ASSIGNMENTS
### {{Lead agent}}: LEAD
  - Drive the investigation
  - Produce the specification draft

### {{Agent-2}}: {{VERIFICATION/LITERATURE/COMPUTATION}}
  - {{Specific verification task}}

### {{Agent-3}}: {{PHYSICAL INTERPRETATION/CROSS-CHECK}}
  - {{Specific cross-check task}}

# IV. DELIVERABLES
1. Computation specification:
   - Step-by-step procedure (numbered)
   - Duration estimate per step
   - Deliverable per step (specific artifact)
   - Dependencies between steps
2. Success/failure criteria:
   - SUCCESS: {{what constitutes a positive result}}
   - PARTIAL: {{what constitutes an ambiguous result}}
   - FAILURE: {{what constitutes a negative result, and its consequences}}
3. Dependency graph (ASCII tree)
4. Convergence table (which finding, how many agents agree, confidence level)
5. Disagreement table (what remains open)
```

## Output Format

```markdown
# Session {{N}} Deep-Dive: {{Problem}}

## CRITICAL PIVOT
{{What changed vs. prior session's understanding}}

## Computation Roadmap
### Step 1: {{Action}}
- Duration: {{time}}
- Deliverable: {{artifact}}
- Dependencies: {{what must exist first}}

### Step 2: ...

## Success Criteria
| Outcome | Definition | Consequence |
|:--------|:-----------|:-----------|
| SUCCESS | {{threshold}} | {{what to do next}} |
| PARTIAL | {{threshold}} | {{what to investigate}} |
| FAILURE | {{threshold}} | {{what's ruled out}} |

## Dependency Graph
```
Step 1 ──→ Step 2
              ├──→ Step 3a (parallel)
              └──→ Step 3b (parallel)
                        ↓
                    Step 4 (requires 3a + 3b)
```

## Key Convergences
| Finding | Agents Agreeing | Confidence |

## Key Disagreements
| Question | Position A | Position B | Status |
```

## Failure Modes This Format Prevents

| Problem | How This Format Handles It |
|:--------|:--------------------------|
| Endless assessment without execution | Forces computation specification with timelines |
| Scope creep | Dependency graph constrains what runs next |
| Ambiguous success criteria | Three-outcome framework (success/partial/failure) |
