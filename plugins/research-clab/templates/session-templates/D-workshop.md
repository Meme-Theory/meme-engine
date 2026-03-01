# Format D: Workshop

## When to Use

Major decision points requiring structured group deliberation. Multiple topics need simultaneous deep assessment. You have 6+ agents available and need to produce executable specifications.

## How to Launch

Workshops run as sequential rounds — use `/clab-team --mode workshop`:

```bash
# Launch a workshop from the agenda/prompt document
/clab-team sessions/session-plan/session-16-workshop-agenda.md --mode workshop

# With explicit team name (recommended for multi-round tracking)
/clab-team sessions/session-plan/session-16-workshop-agenda.md --mode workshop --team-name workshop-s16

# Dry run to verify round structure and agent pairings
/clab-team sessions/session-plan/session-16-workshop-agenda.md --mode workshop --dry-run
```

**How workshop mode works**: The skill creates a new team per round with a `-r{N}` suffix. Round 1 teams are created, run, and dissolved before Round 2 begins. Each round's output markdown file IS the input for the next round. The skill loops back to team creation for each subsequent round.

**Multi-step workshop execution** (when rounds are in separate prompt files):

```bash
# Round 1: Coffee Talks (paired assessments)
/clab-team sessions/session-plan/session-16-round-1.md --mode workshop --team-name s16-r1

# Round 2: Deep Dives (after Round 1 output exists)
/clab-team sessions/session-plan/session-16-round-2.md --mode workshop --team-name s16-r2

# Round 3: Action Items (after Round 2 output exists)
/clab-team sessions/session-plan/session-16-round-3.md --mode workshop --team-name s16-r3

# Final synthesis: switch to clab-review for mass parallel review of Round 3 output
/clab-review sessions/session-16/session-16-round-3c-priorities.md --agents workhorse-1,skeptic,calculator,principalist
```

**Combining with `/clab-review`**: After the workshop's structured rounds, use `/clab-review` on the final synthesis document to get independent evaluations from agents who didn't participate in the workshop — this catches gaps the workshop team missed.

## Why This Format Exists

Large-group sessions degenerate without structure. The Workshop solves this by breaking deliberation into rounds with different cognitive modes: assess (Round 1) → specify (Round 2) → action-item (Round 3). Each round's output IS the deliverable — markdown handoff between rounds keeps context controlled.

## Recipe

**Team**: 6-10 agents across two groups (domain specialists + evaluators).

**Flow**:
```
1. HANDOUT — Distribute combined handout to all agents (everything known so far)
2. ROUND 1: COFFEE TALKS — 2-person pairs assess topics from their perspective
3. ROUND 2: DEEP DIVES — 3-4 person teams produce specifications
4. ROUND 3: ACTION ITEMS — 2-3 person teams produce executable specs with pass/fail
5. FINAL SYNTHESIS — 4-person cross-section reads all Round 3 output
6. CLOSING REVIEW — 2-person evaluator pair identifies gaps the synthesis missed
```

**Duration**: 1 extended session or 2 sessions

## Plan

```markdown
# Session {{N}} Plan: Workshop

## Combined Handout
Prepare a single document containing ALL relevant prior results.
Every agent reads this before any round begins. No progressive reveals.

## Round 1: Coffee Talks (2-person pairs)
| Round | Pair | Topic | Output File |
|:------|:-----|:------|:-----------|
| 1a | {{agent-1}} + {{agent-2}} | {{topic}} | session-{{N}}-round-1a.md |
| 1b | {{agent-3}} + {{agent-4}} | {{topic}} | session-{{N}}-round-1b.md |
| 1c | {{agent-5}} + {{agent-6}} | {{topic}} | session-{{N}}-round-1c.md |

## Round 2: Deep Dives (3-4 person teams)
| Round | Team | Reads From | Topic | Output File |
|:------|:-----|:-----------|:------|:-----------|
| 2a | {{agents}} | Round 1a, 1c | {{topic}} | session-{{N}}-round-2a.md |
| 2b | {{agents}} | Round 1a, 1b | {{topic}} | session-{{N}}-round-2b.md |

## Round 3: Action Items (2-3 person teams)
| Round | Team | Reads From | Produces | Output File |
|:------|:-----|:-----------|:---------|:-----------|
| 3a | {{agents}} | All Round 2 | Computational specs | session-{{N}}-round-3a.md |
| 3b | {{agents}} | All Round 2 | Theoretical specs | session-{{N}}-round-3b.md |
| 3c | {{agents}} | Round 3a + 3b | Master ranked list | session-{{N}}-round-3c.md |

## Agent Rotation Rules
- Each agent appears in exactly 1 Coffee Talk, 1 Deep Dive, 1 Action Item
- Pair by domain affinity in Round 1, cross-pollinate in Rounds 2-3
- Evaluator agents appear in Round 1 (as critics), Round 2 (as rankers), and Closing Review
- Evaluators never write specifications — they evaluate and critique
- No agent appears in Round 3c who also wrote a Round 3a/3b spec
```

## Round 1 Output Format (Coffee Talk)

```markdown
# Session {{N}}, Round 1X: {{Topic}} Coffee
## {{Agent-1}} + {{Agent-2}} Joint Assessment

## Top-N Results/Claims (Ranked)
| Rank | Claim | Evidence | Why It Ranks Here |

## Priority Computations
| Computation | Timeline | Dependencies | Pass/Fail |

## Convergences
## Disagreements (with Resolution status for each)
## Key Technical Insights
```

## Round 2 Output Format (Deep Dive)

```markdown
# Session {{N}}, Round 2X: {{Topic}} Deep Dive
## {{Agent list}}

## Executive Summary
{{Key finding + architectural decision + total code estimate}}

## I. Full Specification
- Complete formula/algorithm
- Pseudocode for core functions
- Pass/fail criteria (tiered: BLOCKING / ROBUSTNESS / SIGNIFICANCE)
- Hardware requirements
- Line count and runtime estimates

## Convergences and Disagreements
| # | Topic | Agent A | Agent B | Status |
```

## Round 3 Output Format (Action Item)

Each action item uses this exact structure:

```markdown
## {{N}}. {{ITEM NAME}}
- **Type**: Formula / Computation / Test / Theoretical
- **Specification**: {{full description with formulas, pseudocode}}
- **Pass/Fail**: {{structured: BLOCKING / ROBUSTNESS / SIGNIFICANCE}}
- **Feasibility**: GREEN / YELLOW / RED
- **Timeline**: {{days + breakdown}}
- **Owner**: {{agent name(s)}}
- **Decisiveness**: {{N/10}}
- **Dependencies**: {{prerequisites}}
- **Code**:
  | File | Function | Lines | Runtime | Status |
  {{Pseudocode block}}
```

## Orchestration State Document

Maintain a living document tracking workshop progress:

```markdown
# Session {{N}} Orchestration State

## Metadata
Session type, total rounds planned, start date, coordinator

## Round-by-Round Completion Log
### Round {{X}}: {{Name}}
- File: {{path}}
- Participants: {{list}}
- Key Findings: {{4-8 bullets}}
- Convergences / Divergences / New Threads

## Currently Running
## Remaining Rounds (with trigger conditions)

## Key Process Discoveries
{{Numbered list of what broke and how it was fixed}}

## Framework Probability Tracker
| Agent | Estimate | Round | Reasoning |

## Restoration Instructions
{{Step-by-step for recovering after context compaction}}
```

## Failure Modes This Format Prevents

| Problem | How This Format Handles It |
|:--------|:--------------------------|
| Agents drift into unproductive discussion | Each round has a named output file — no file = failed round |
| Cross-talk between teams | Sequential rounds, one team at a time |
| Context explosion | Markdown handoff — each round reads ONLY its inputs |
| Premature shutdown before output written | Orchestration state tracks completion; redo if output missing |
| Evaluators defending their own specs | Evaluators banned from writing Round 3a/3b specs |
