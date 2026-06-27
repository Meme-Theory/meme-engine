# Output Standards

<!-- DEPLOY: project-root/.claude/rules/output-standards.md -->
<!-- No paths: frontmatter — loads unconditionally for all agents -->

## Action Items Format

Every action item must include all 7 components:

1. **What** — the specific deliverable
2. **Who** — which agent or role
3. **Input** — what they need to start
4. **Output** — what they produce
5. **Format** — file type and location
6. **Deadline** — session or phase
7. **Depends on** — prerequisite action items

## Handoff Documents

Every session produces a handoff document with these 7 sections:

1. Session metadata (date, format, agents, prompt)
2. Key results (numbered, specific)
3. Constraint map updates (new entries, state changes)
4. Open questions (numbered, actionable)
5. Action items (using 7-component format above)
6. Files created or modified (paths)
7. Next session recommendations

## General Output Rules

- **Mark preliminary results** — label any claim not yet validated by computation as "PRELIMINARY"
- **Cite sources precisely** — paper numbers, file paths, line numbers
- **One writer per file** — designated writer only; others contribute via messages
- **Gate verdicts are permanent** — once recorded, a verdict cannot be retroactively changed
- **No filler** — avoid "as we can see," "it's worth noting," "interestingly"

## Workshop Wrap-Up "What Changed" -- Numerical vs Structural Distinction

A workshop Wrap-Up "What Changed" section (and the analogous handoff "Constraint map updates" section) MUST split its changes into two epistemic categories:

**(a) Numerical revisions** -- quantitative recalibrations: a value, band, ratio, or magnitude tightened or corrected, with the result's TYPE unchanged. Examples:
- a discrimination band re-pinned (`4.25 -> 2.22`)
- an order-of-magnitude estimate sharpened to an exact value (`"~45" -> 47.08`)

**(b) Structural changes** -- reframings that alter the EPISTEMIC TYPE of the result, not merely its number. Examples:
- a single-test falsifier promoted to a two-test outcome matrix (one detector -> a 2x2 outcome grid)
- a "primary + confirmation" pair reclassified as a co-primary double-source
- a one-dimensional ranking re-read as a multi-dimensional partition

**Why the distinction matters**: numerical revisions are SUBORDINATE to structural reframings; structural changes are the more durable output of a workshop. Listing both in one undifferentiated bullet block hides which results are durable reframings versus which are precision-tightening updates. Keep them in separate sub-sections.

**Format**:

```markdown
## What Changed

### (a) Numerical revisions
- discrimination band re-pinned: 4.25 -> 2.22 (recomputed)
- estimate sharpened: "~45" -> 47.08 (exact)

### (b) Structural changes
- single-test falsifier -> two-test outcome matrix (promoted to a 2x2 outcome grid)
- primary+confirmation -> co-primary double-source (anchor structure reclassified)
```

## Carry-Forward Dependency Enumeration (extends Action Items "Depends on")

Carry-forward specs (in a workshop Wrap-Up, or in the "Action items" section of a handoff) SHOULD enumerate their upstream dependencies explicitly in the "Depends on" field -- rather than leave them to be discovered at next-session plan time.

**When a carry-forward has dependencies**:
- cite each upstream by name -- the gate, data file, module, or pinned constant/identifier it consumes;
- for a multi-input dependency, enumerate ALL inputs, not just the most prominent one;
- for a transitive dependency, cite the PROXIMATE upstream (the next-session planner resolves the chain from there).

**Why this matters**: explicit enumeration fixes wave order at plan-freeze. Without it, the planner must walk the carry-forward chain to discover prerequisites -- slow, error-prone, and apt to miss an input that was only implicit. The "Depends on" field is already mandatory in the Action Items format above; this rule makes it a structured enumeration whenever the carry-forward has more than one substantive prerequisite.

**Format**:

```markdown
### Action Item N

1. **What**: {the computation -- equation, method, output variable}
2. **Who**: {agent or role}
3. **Input**: {short description}
4. **Output**: {result + any tag}
5. **Format**: {file path(s)}
6. **Deadline**: {next session, Wave 2}
7. **Depends on**:
   - {upstream gate ID} verdict (UPSTREAM GATE)
   - {spec / module name} from this workshop (REGISTRY ENTRY)
   - {pinned constant / data identifier}: {name = value}
```
