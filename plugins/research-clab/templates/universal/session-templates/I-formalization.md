# Format I: Formalization

## When to Use

No new computation. The purpose is to consolidate N prior sessions into a single status document — a workshop-ready artifact that any agent can read cold.

## How to Launch

Formalization combines a panel session (for cataloging) with a mass review (for validation):

```bash
# Step 1: Panel session — specialists catalog their domains into a unified document
/rclab-team sessions/session-plan/session-15-formalization-prompt.md --mode panel --team-name s15-formalize

# Step 2: Mass review — all agents independently validate the status document
/rclab-review sessions/session-15/session-15-formalization.md

# Step 3 (optional): Targeted review if specific domains need deeper scrutiny
/rclab-review sessions/session-15/session-15-formalization.md --agents workhorse-1,bridge,workhorse-2 --skip-synthesis
```

**Why `--mode panel`** for Step 1: Formalization is a coordination task — agents discuss domain boundaries, reconcile conflicting classifications (is this result "proven" or "suggestive"?), and produce a unified document. Panel mode's discussion-driven approach fits this better than compute mode's task-driven approach.

**Why `/rclab-review`** for Step 2: After the panel produces the status document, independent review catches misclassifications. An agent whose work was summarized by someone else in Step 1 may disagree with the classification — this surfaces those disagreements.

**The formalization-to-workshop pipeline**:

```bash
# Formalize (produces the combined handout for the workshop)
/rclab-team session-15-formalization-prompt.md --mode panel --team-name formalize

# Workshop (uses the formalization output as its combined handout)
/rclab-team session-16-workshop-agenda.md --mode workshop --team-name workshop
```

## Why This Format Exists

After 5-15 sessions of investigation, the accumulated knowledge is scattered across dozens of files. A Formalization session catalogues everything using a consistent taxonomy, producing a single document that makes the next session productive from turn one.

## Recipe

**Team**: 4-6 specialists (each assigned a domain scope) + coordinator.

**Flow**:
```
1. ASSIGN DOMAINS — Each agent catalogs their domain's status
2. CATALOG — Apply consistent taxonomy: proven / suggestive / open / refuted / gaps
3. MERGE — Coordinator merges sections into unified document
4. RECOMMENDATIONS — Synthesize next steps from the catalog
```

**Duration**: 1 session

## Prompt Template

```markdown
# Session {{N}}: Formalization

## Session Type: PARALLEL FORMALIZATION → TEAM-LEAD SYNTHESIS
## Agents: {{4-6 agents}}
## Session Goal: Produce rigorous status document consolidating Sessions {{1-N}}.

# I. CONTEXT
All results from Sessions {{range}} need consolidation before the next phase.

# II. ASSIGNMENTS
### {{Agent-1}}: {{Domain scope 1}}
  Catalog status of all results in your domain:
  - PROVEN (machine epsilon or exact)
  - SUGGESTIVE (positive but not definitive)
  - OPEN (needs computation)
  - REFUTED (disproven)
  - STRUCTURAL GAPS (missing pieces)

### {{Agent-2}}: {{Domain scope 2}}
  (same taxonomy)

# III. OUTPUT STRUCTURE
  I. Proven Results (table)
  II. Suggestive Results (table)
  III. Null Results (table)
  IV. Refuted Claims (list)
  V. Open Computations (ranked)
  VI. Structural Gaps (severity table)
  VII. Framework Probability (with "what would change this")
  VIII. Recommendations (team structure for next phase)
```

## Output Format

```markdown
# Session {{N}}: Formalization — Status Document

## I. Proven Results
| # | Result | Method | Script | Precision |

## II. Suggestive Results
| # | Result | Value | Caveat |

## III. Null Results
| # | Test | Result | Verdict |

## IV. Refuted Claims
{{Numbered list with session and evidence}}

## V. Open Computations (Ranked)
| Rank | Computation | Decisiveness | Feasibility | Timeline |

## VI. Structural Gaps
| Gap | Severity | Status | What Would Close It |

## VII. Framework Probability
| Assessor | Range | Median | What Would Change This |

## VIII. Recommendations
### Team A: {{Computational}}
1. {{task}}
2. {{task}}

### Team B: {{Theoretical}}
1. {{task}}
2. {{task}}

### Key Debate Questions for Next Session
1. {{question}}
2. {{question}}
```

## Failure Modes This Format Prevents

| Problem | How This Format Handles It |
|:--------|:--------------------------|
| Scattered knowledge across too many files | Single status document with consistent taxonomy |
| Retroactive interpretation of results | Fixed taxonomy forces honest classification |
| Losing track of what's proven vs. suggestive | Separate tables for each category |
| Next session re-discovering known results | Status document is the required reading for all future sessions |
