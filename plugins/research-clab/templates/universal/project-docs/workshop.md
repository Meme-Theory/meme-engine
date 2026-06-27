# Workshop Document Template

Build the FULL skeleton before launching any agent. Replace variables in braces.
All `*[NOT STARTED]*` placeholders are filled by agents during execution.

```markdown
# Session {session-id} Workshop: {Agent-A-Short} x {Agent-B-Short}

**Date**: {today}
**Format**: Iterative 2-agent workshop ({N} rounds, {N*2} turns)
**Agents**: {agent-a-short} ({agent-a-type}), {agent-b-short} ({agent-b-type})
**Source Documents**:
{bulleted list of source doc paths}

**Focus Topics**:
{numbered list from --context, if provided}

---

## Round 1 — {Agent-A-Short}: Opening Analysis

{For each focus topic, create a labeled subsection:}

### {A-initial}1: {Focus Topic 1}

*[NOT STARTED]*

### {A-initial}2: {Focus Topic 2}

*[NOT STARTED]*

{Continue for all focus topics, then add:}

### {A-initial}N: Cross-Cutting Observations

*[NOT STARTED]*

---

## Round 1 — {Agent-B-Short}: Response & Cross-Synthesis

### Part 1: Response to {Agent-A-Short}'s Sections

{For each of Agent A's sections, create a response subsection:}

#### Re: {A-initial}1 — {Focus Topic 1}

*[NOT STARTED]*

{Continue for all sections.}

### Part 2: Original Analysis

#### {B-initial}1: {Agent B's Perspective Title}

*[NOT STARTED]*

#### {B-initial}2: {Further Analysis}

*[NOT STARTED]*

#### {B-initial}3: Questions for {Agent-A-Short}

*[NOT STARTED]*

---

{For rounds 2+, repeat this pattern per round:}

## Round {r} — {Agent-A-Short}: Follow-up

### CONVERGENCE

*[NOT STARTED]*

### DISSENT

*[NOT STARTED]*

### EMERGENCE

*[NOT STARTED]*

### QUESTIONS

*[NOT STARTED]*

---

## Round {r} — {Agent-B-Short}: Cross-Synthesis

### CONVERGENCE

*[NOT STARTED]*

### DISSENT

*[NOT STARTED]*

### EMERGENCE

*[NOT STARTED]*

{On the FINAL round only, Agent B also fills:}

## Workshop Verdict

| # | Topic | Source | Status | Key Insight |
|:--|:------|:-------|:-------|:------------|
| 1 | {topic} | {A-initial}1, Re:{A-initial}1 | *pending* | |

Status categories: **Converged** | **Dissent** | **Partial** | **Emerged**

## Remaining Open Questions

*[To be filled after final round]*

## Wrap-Up -- Workshop Impact Summary

{MANDATORY -- Agent B fills this in the FINAL round alongside the Verdict table.}

### What Changed
{1-3 bullets: what this workshop CHANGED about the framework's state -- new structural results, resolved tensions, revised estimates. Split numerical revisions from structural changes per the output-standards.md "What Changed" rule.}

### What Holds
{1-3 bullets: what SURVIVED the exchange -- results challenged and defended, or confirmed from both perspectives.}

### What Breaks or Strains
{1-3 bullets: what the workshop THREATENS or leaves unresolved. If nothing, say "Nothing identified."}

### Carry-Forward Computations (DEFERRED WORK ONLY -- propagate to next session)

**Discriminator (4-field test)**: an item belongs HERE iff it satisfies ALL FOUR fields below. If ANY field cannot be filled, it is NOT a carry-forward -- move it to "Effected In-Session" and execute it NOW.

- **What**: the specific computation / derivation / structural result to produce
- **Inputs**: the data files, constants, upstream gates needed
- **Gate**: the pre-registered PASS / FAIL / INFO threshold, with explicit tolerance
- **Effort**: estimated effort (compute time or agent-sessions)

{Numbered list -- only items satisfying ALL FOUR fields. This list is a PRIMARY input to /rclab-plan for the next session.}

### Effected In-Session (IN-SESSION EDITS -- completed by YOU, the final agent, BEFORE TERMINATING)

**MANDATORY -- NON-NEGOTIABLE.** Per the project's "No Technical Debt" discipline and repeated evidence that deferred edit-type items become orphans: every edit-type item this workshop surfaces MUST be EXECUTED by you (the final agent) NOW, with concrete file edits, BEFORE the workshop document is complete.

**In-session edit categories (non-exhaustive)**:
- Registry / status edits -- status promotions (e.g. CANDIDATE -> PERMANENT, SUGGESTION -> MANDATORY), slot allocations, re-tags, classification changes
- Rule-file edits -- new sub-clauses, calibration-corpus entries, taxonomy additions
- Documentation hygiene -- fixing broken cross-links, stale references, anchor mismatches, "see also" pointers
- Knowledge-index updates -- new or updated entities / constants via `/weave --update`

**Procedure**:
1. Enumerate EVERY edit-type item surfaced across all rounds (CONVERGENCE / DISSENT / EMERGENCE / QUESTIONS / Wrap-Up).
2. For each, EXECUTE the edit NOW with your Edit / Write tools.
3. Record what you did with a concrete `file:line` reference.
4. Check the box ONLY after the edit is on disk.

**Output format** (one row per item):

- [x] {item description} -- {action taken} -- `{file/path:line-range}`

**Self-audit before terminating**: run `grep -c '^- \[ \]' {this-workshop-file}` over this section -- the count MUST be 0 (no unchecked boxes remain).

**FORBIDDEN**:
- Leaving any edit-type item UNCHECKED.
- Deferring an edit-type item to "Carry-Forward Computations".
- Listing an edit-type item as "next-session" / "queued" / "TODO" / "deferred".
- Writing placeholder text in lieu of executing the edit.

If you find yourself wanting to write "queued for next session" on an edit-type item: STOP. Execute it now.

### Closing Line
{One sentence. The single most important thing from this workshop.}
```
