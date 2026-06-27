# Workshop / Synthesis Schedule Template

Use this template when the deliverable is a CAMPAIGN of slash-command invocations across two skills -- multiple solo syntheses via `/rclab-review` plus adversarial workshops via `/rclab-workshop` -- not a single session plan. Produced by `/rclab-investigate`.

This is DISTINCT from `plan-workshop.md` (a workshop/panel *session plan*). A workshop schedule is a ready-to-execute list of invocations; a workshop session plan is a single session's structure.

The output is ready-to-execute: each slot contains the exact slash-command invocation matching the right skill, so the user can dispatch each entry directly.

**Skill-slot mapping (load-bearing invariant)**:

- **Slot 1 entries -> `/rclab-review`** (solo synthesis; 1+ independent agents per entry, default 1 = the primary author of the question; NO `--type` flag, NO `--rounds` flag -- `/rclab-review` is solo-only).
- **Slot 2 entries -> `/rclab-workshop`** (2-agent iterative workshop on a shared document; EXACTLY 2 agents per entry; `--rounds 2` default).
- **Slot 3 entries -> `/rclab-review`** (closeout combined-landscape synthesis; 1 agent typical).

DO NOT emit `/rclab-review --type workshop --rounds N --agents A,B` -- that flag combination is structurally invalid (`/rclab-review` accepts neither `--type` nor `--rounds`). Workshop semantics are encoded by `/rclab-workshop`, not by flags on `/rclab-review`. See `.claude/rules/Investigating-Workshops.md` for the workshop-vs-carry-forward definition this schedule enforces.

```markdown
# Session {N} -- Workshop / Synthesis Schedule

**Date drafted**: {today}
**Scope**: {one-line description of campaign purpose, e.g., "Refinement and exploration of Session {N} results before planning S{N+1}"}
**Rationale**: {2-3 sentences -- why this campaign now? What gaps remain in the source material that warrant dedicated synthesis passes? Cite specific deferrals from the source documents.}

**Source documents (authoritative; do not re-adjudicate)**:
- `{path}` ({size}, {line count})
- `{path}` ({size}, {line count})
- ...

**All workshop + synthesis outputs land inside `sessions/session-{N}/`**. {State explicitly whether the next session plan is open or pending.}

---

## Dispatch Strategy

Ordered by criticality and cross-dependency. Slot 1 `/rclab-review` solos can launch in parallel (no cross-deps; respect the project's concurrency cap). Slot 2 `/rclab-workshop` entries that target distinct output files with no shared inputs are MUTUALLY INDEPENDENT and run as PARALLEL TRACKS up to the concurrency cap; only the TURNS WITHIN a single workshop are sequential (turn B reads turn A's edits to the shared document). The Skill tool loads the `rclab-workshop` procedure once; concurrency is at the Agent-dispatch level, not the Skill-call level. Slot 3 is closeout.

| Slot | ID | Title | Skill | Agents | Rounds | Depends on |
|:----:|:---|:------|:------|:-------|:------:|:-----------|
| 1 | S-1 | {title} | `/rclab-review` | {1; or 2-3 if multi-perspective value} | -- | -- |
| 1 | S-2 | {title} | `/rclab-review` | {1 typical} | -- | -- |
| 2 | W-1 | {title} | `/rclab-workshop` | 2 | 2 | -- |
| 2 | W-2 | {title} | `/rclab-workshop` | 2 | 2 | -- |
| 3 | S-N | {title} | `/rclab-review` | {1 typical} | -- | W-1, W-2 (ideal; graceful degrade) |

---

## Slot 1 -- Independent Solo Syntheses (`/rclab-review`; parallel dispatch up to the concurrency cap)

### S-1 -- {Title}

**Why**: {2-4 sentences -- what specific gap this fills, what's in the source docs that needs this synthesis, what the output feeds into}

**Agents**: `{agent-type-1}` ({domain expertise -- primary author of the question})
*Default: 1 agent (the primary author). Add a second/third agent ONLY when independent multi-perspective value clearly outweighs the additional dispatch cost -- the recommended default is 1 agent per Slot 1 entry.*

**Invocation** (NO `--type`, NO `--rounds` -- `/rclab-review` is solo-only):
```
/rclab-review {source docs space-separated} --agents {agent-type-or-comma-list} --session {N} --context "{FULL context string -- include all specific anchors, numbers, gate IDs, and explicit classification/adjudication demands the synthesis must address}"
```

---

### S-2 -- {Title}

(repeat pattern)

---

## Slot 2 -- Workshops (`/rclab-workshop`; independent workshops run as PARALLEL TRACKS up to the concurrency cap; only the TURNS WITHIN each workshop are sequential)

### W-1 -- {Title}

**Why**: {why this adjudication matters -- what competing claims or unresolved tensions live in the source material that require cross-agent rebuttal, not just independent reading}

**Agents (EXACTLY 2 -- `/rclab-workshop` requires exactly 2 per its Phase 0 validation)**: `{agent-type-A}` ({role in workshop -- e.g., owner of track X}), `{agent-type-B}` ({role -- owner of track Y})

**Invocation** (use `/rclab-workshop`, NOT `/rclab-review` -- workshop semantics are encoded by the workshop skill, not by flags on review):
```
/rclab-workshop {source docs} --agents {A},{B} --rounds 2 --session {N} --context "{full context -- include the competing positions, the stakes, the adjudication rule, and explicit sub-topics (a) (b) (c) etc.}" --output "sessions/session-{N}/workshops/{filename}.md"
```

*Rounds default = 2 (matches `/rclab-workshop`'s skill default). Bump to 3 only if the candidate is genuine ledger-dissonance needing R1 = steelman, R2 = respond to opponent's best case, R3 = converge on gate (rare; document the reason in the Why block).*

---

### W-2 -- {Title}

(repeat pattern)

---

## Slot 3 -- Closeout (`/rclab-review`; depends on Slot 1 + Slot 2 outputs)

(Slot 3 entries are closeout tasks -- usually combined-landscape syntheses that depend on Slot 2 workshop verdicts and/or Slot 1 solo synthesis outputs, or methodology audits.)

### S-M -- {Title}

**Why**: {explicit mention of which Slot 1 solos and Slot 2 workshops this depends on; what combined-landscape view the closeout produces}

**Agents**: 1 typical (closeout is solo synthesis pulling threads together; bump to 2 only if cross-domain composition genuinely needs it)

**Invocation** (NO `--type`, NO `--rounds` -- `/rclab-review` solo):
```
/rclab-review {...} --agents {agent-type} --session {N} --context "{...includes 'if W-X has landed, fold in...' graceful-degrade language so Slot 3 doesn't crash when an upstream Slot 2 workshop is incomplete}"
```

---

## Post-Campaign Deliverable Summary

After all syntheses land, the following files exist in `sessions/session-{N}/` and `sessions/session-{N}/workshops/`:

| File | Produced by | Feeds into next session as |
|:-----|:------------|:----------------------------|
| `sessions/session-{N}/workshops/{w1-file}.md` | W-1 workshop | {what gate, what pre-registration, what structural result} |
| `sessions/session-{N}/session-{N}-{agent-short}-synthesis.md` | S-1 solo ({agent}) | {what it produces} |
| ... | ... | ... |

**Total expected outputs**: {N} workshop MDs + {M} per-agent solo MDs = {N+M} files.

---

## Planning Input Checklist (populated by this campaign)

Items this campaign produces that the next session's planner needs:

- {specific adjudication result expected}
- {pre-registered gate ID expected to be created}
- {registry entry draft expected}
- {watchlist / open-question update expected}
- {combined landscape document expected}
- {methodology diff expected}
- ...

---

## Operational Notes

- **Session ID pinning**: all invocations use `--session {N}` explicitly. Skill auto-detect may pick up a different session from the first source doc; the explicit pin prevents mis-routing.
- **Output paths**: workshop outputs use explicit `--output sessions/session-{N}/workshops/{name}.md`. The `workshops/` subdirectory is created on first Write. Solo outputs use the skill default `sessions/session-{N}/session-{N}-{short-name}-synthesis.md`.
- **Dispatch count**: Slot 1 = {X} agents in parallel (discrete launch, wait all, then next slot). Slot 2 = {Y} workshops x 2 sequential turns x {R} rounds = {2*Y*R} sequential agent turns total. Slot 3 = {Z} mixed.
- **Concurrency cap**: respect the project's max concurrent Agent dispatches. If Slot 1 exceeds the cap, split into sub-slots 1a / 1b.
- **Closeout graceful degrade**: the combined-landscape solo (typical Slot 3 item) should reference Slot 2 outputs "if landed" -- agents must degrade gracefully if dependencies have not completed.
- **Length targets**: do NOT include line-count or page-count targets in invocation contexts. Content requirements only ("include X table", "include Y gate") -- length is determined by content.
- **Structured carry-forward (compute-only)**: every synthesis invocation context must include the 4-field carry-forward mandate (what / inputs / gate / effort). ONLY items satisfying all 4 fields propagate forward as carry-forwards.
- **Non-compute effected in-session**: every workshop invocation context must include the directive that the FINAL agent (last round, last turn) MUST effect every non-compute item with concrete file edits before terminating -- registry edits, rule-file extensions, methodology promotions, hygiene cleanups, anchor re-tags, audit-script extensions. Deferring non-compute items is FORBIDDEN per the project's no-technical-debt discipline (CLAUDE.md). The `/rclab-workshop` skill audits checkbox completion and re-dispatches if items remain unchecked.

---

*End of S{N} workshop schedule. Draft {date}.*
```

---

## Planner's instructions (for agents generating this schedule)

When generating a workshop-schedule document:

1. **Mine the source documents** for explicit deferrals, unresolved adjudications, claimed-but-unformalized results, failure-mode summaries, and watchlists. These are your campaign seeds. Apply the `.claude/rules/Investigating-Workshops.md` discriminator to classify each.

2. **Classify each seed** by its required interaction shape:
   - **Solo synthesis (Slot 1)** -- independent reading + write-up. 1 agent default (the primary author of the question), 2-3 agents only when independent multi-perspective value is essential. NO cross-agent rebuttal. **Skill: `/rclab-review`**.
   - **Workshop (Slot 2)** -- adjudication of GENUINELY COMPETING positions between two specific domains where cross-rebuttal is essential (the agents must respond to each other's arguments to converge). EXACTLY 2 agents, 2 rounds default. **Skill: `/rclab-workshop`**.
   - **Closeout (Slot 3)** -- depends on Slot 1/Slot 2 outputs; usually combined-landscape solo synthesis or methodology audit. 1 agent typical. **Skill: `/rclab-review`**.

3. **Organize into slots** by dependency AND interaction-shape:
   - **Slot 1 (`/rclab-review`)**: independent solo syntheses that can launch in parallel (no cross-deps). Respect the concurrency cap (split into 1a/1b sub-slots if more entries than the cap).
   - **Slot 2 (`/rclab-workshop`)**: 2-agent adversarial workshops; turns WITHIN a workshop are sequential (turn B reads turn A), but INDEPENDENT workshops (distinct output files, no shared inputs) run as PARALLEL TRACKS up to the cap. The Skill tool loads the procedure once; concurrency is at the Agent-dispatch level, not the Skill-call level.
   - **Slot 3 (`/rclab-review`)**: closeout depending on Slot 1/2 outputs.

4. **Skill-slot mapping is a load-bearing invariant**: write the EXACT slash-command matching the slot's skill. Slot 1 + Slot 3 use `/rclab-review`. Slot 2 uses `/rclab-workshop`. NEVER emit `/rclab-review --type workshop --rounds N --agents A,B` -- the `--type` flag does not exist on `/rclab-review` and `--rounds` is a `/rclab-workshop` flag, not a `/rclab-review` flag (see each skill's argument-hint). The user should be able to copy-paste each invocation and dispatch it directly without runtime arg-validation errors. (This invariant exists because a schedule that emitted dozens of entries under the invalid form once had to be halted before dispatch.)

5. **Context strings must be full-fidelity** -- include every specific gate ID, numeric anchor, classification seed, adjudication rule the synthesis needs. No "see source docs" or "appropriate context" -- be explicit.

6. **Agent selection**: use the `agent-roster.md` canonical short names. For Slot 1 solos, pick the agent whose domain owns the question (default: 1 agent, the primary author). For Slot 2 workshops, pair agents whose domains cover complementary, genuinely-competing readings of the same claim -- two specialists who would derive the result via different methods and might disagree on the outcome. The Slot-2 pairing is the workshop's adversarial axis; the Slot-1 single-agent pick is the question's primary owner.

7. **Rounds (Slot 2 only -- Slot 1 and Slot 3 are solo and have no rounds field)**:
   - Slot 2 default: **2 rounds** (matches `/rclab-workshop`'s skill default).
   - Use 3 rounds only when the adjudication is genuine ledger-dissonance (R1 = steelman, R2 = respond to opponent's best case, R3 = converge on gate). Document the bump in the Why block.
   - Use 1 round only for informational exchanges (rare; document why).

8. **No length targets** in invocation contexts. Content requirements only.

9. **Carry-forward mandate (compute-vs-non-compute split)** -- every invocation context must demand BOTH (a) the 4-field structured carry-forward (what / inputs / gate / effort) for COMPUTE-only items propagating to S{N+1}, AND (b) the in-session execution directive for every NON-COMPUTE item the workshop surfaces. Non-compute items (registry edits, rule-file extensions, methodology status promotions, hygiene cleanups, anchor re-tags, constant/parameter promotions, knowledge-index registrations, audit-script extensions) MUST be effected by the final agent (last round, last turn) with concrete file edits BEFORE the workshop terminates. Deferring non-compute items is FORBIDDEN per the project's no-technical-debt discipline (CLAUDE.md). The `/rclab-workshop` skill audits checkbox completion in the workshop document's "Effected In-Session" section and re-dispatches the final agent until all non-compute boxes are ticked.

10. **Deliverable table** -- explicitly list every file the campaign will produce, with the agent responsible and the next-session consumption pattern.
