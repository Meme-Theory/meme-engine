---
paths:
  - "sessions/**"
---

# Investigating Workshops

<!-- DEPLOY: project-root/.claude/rules/Investigating-Workshops.md -->
<!-- Path-scoped: loads when working in sessions/. Governs how /rclab-investigate distinguishes WORKSHOPS from CARRY-FORWARDS. Skill names (/rclab-investigate, /rclab-plan, /rclab-workshop, /rclab-review) are the rclab suite defaults; adjust if a project renames them. -->

## Scope

This rule governs how `/rclab-investigate` -- and any agent identifying follow-up work from a closed session's substance -- distinguishes WORKSHOPS from CARRY-FORWARDS. It applies at investigator-prompt level, consolidator-prompt level, and at any session-end synthesis where the question is "what should be reviewed multi-agent next."

A permissive "workshops, solo syntheses, or follow-up work" framing is the structural cause of the carry-forward-listing failure mode -- padding queued computations as if they were workshops. **This rule overrides that permissiveness.** Workshop-schedule deliverables are workshops, period; solo reviews and follow-up computations are categorized differently and routed differently (see "Cross-references").

## Definition: A WORKSHOP IS

A workshop is a structurally-specific kind of follow-up dispatch. ALL FOUR conditions must hold:

1. **TWO+ agents with COMPETING perspectives on a SPECIFIC TENSION** -- not one agent narrating a result, not two agents agreeing in parallel; two or more agents who *disagree* about how to read a claim, a verdict, or a structural pattern.
2. **Genuine DISSONANCE** -- a competing-claim adjudication. The perspectives MUST diverge on something concrete (a number, a sign, a structural reading, a methodology choice, a convention).
3. **Multi-round structure** -- R1 steelman / R2 respond to opponent's best case / R3 converge on verdict. Three rounds for genuine adversarial review; two rounds for routine adjudication; one round only for informational exchanges (rare).
4. **Output: STRUCTURAL VERDICT** that resolves the competing claims -- a NEW pinned position (a verdict, a registry entry, a rule diff, a pre-registered gate), NOT a queued computation to run later.

## Definition: A WORKSHOP is NOT

The following are NOT workshops, even when narrative-inflated to look like ones:

1. **Solo compute follow-ups** -- "compute X next session" with a pre-registered threshold and inputs. -> carry-forward computation; belongs in the next session's plan via `/rclab-plan`.
2. **Verification gates** -- cross-check, plan-freeze audit, independent-verify dispatches. Pre-specified protocol; nothing to adjudicate. -> queued computation gate.
3. **Re-listings of carry-forwards already enumerated** -- a wave-synthesis "Carry-Forward Computations" list re-formatted as "candidates." They already exist in the session's working paper; the next planner picks them up directly. Renaming them "workshops" adds zero structural content.
4. **Single-agent "synthesis" of one wave's results** -- a per-wave digest, useful as background but not a workshop.
5. **Single-agent "exploration" of a registry slot** -- even with "2-agent workshop" framing, with no genuine adversarial tension between the two named agents it is a solo dispatch in disguise.
6. **Rule / methodology extensions where both agents would agree on the content** -- a workshop requires DISAGREEMENT, not parallel-agreement implementation.
7. **Registry-state classification / hygiene / framework-housekeeping** -- choosing status markers for already-landed records, promoting landed-but-not-promoted records, fixing provenance hygiene, addressing gate-finalization gaps. Even when the choice has structural import, the resolution is a registry-state decision, not an adversarial tension between competing readings. -> in-session fix or carry-forward per the routing table. NOT a workshop.
8. **Parallel-compute structures dressed as N-agent panels** -- when N prerequisite conditions can each be tested by an independent compute gate on its own axis, and the N verdicts combine via logical AND for the final outcome, the structure is a parallel-compute wave (N independent gates + 1 AND closeout), NOT an N-agent workshop. The per-axis agent is a derivation-author tag (who owns the math for axis X), not a workshop-participant tag. No adversarial round protocol is needed because the axes are structurally orthogonal. -> carry-forward, marked "wave-together."
9. **Not-yet-executed wave / pre-compute shell** -- a wave with all gates not started, no result artifacts on disk, and no matching verdict entries. Investigator: emit `## Not investigated -- wave {id} is pre-compute shell` (one sentence) and skip the wave in subsequent steps. Do NOT create an "execute this wave next session" carry-forward. Consolidator: do NOT lift any wave-execution carry-forward for a shell wave. -> escalation to a `/rclab-coordinate` retry, NOT a carry-forward.

## How to identify a real workshop in session substance

Look for these signals when reading a session's gates and verdicts:

- **FAILs that admit MULTIPLE structural readings** -- agent A reads the FAIL as evidence of X; agent B reads it as evidence of Y. The reading divergence is the workshop seed.
- **Borderline INFOs** -- marginal-evidence values where domain agents will disagree about signal vs noise.
- **CROSS-WAVE tensions** -- one wave's PASS conflicts with another wave's INFO/FAIL. The ledger has an internal contradiction needing adjudication.
- **Methodology-vs-substance blurs** -- a rule-extension proposal where the right shape is contested; two agents give different rationales.
- **Convention questions where TWO PERSPECTIVES GENUINELY DIVERGE** -- scheme choice, observable definition, registry-anchor structure.
- **EXISTING claims that need ADVERSARIAL TESTING** -- not "compute next" but "audit what we already claimed." A registered result may need adversarial review of its sufficiency conditions.

If the session's substance contains NONE of the above, the session produced NO workshops. That is a valid output.

## "No workshops" is a valid output

A session with clean PASSes, unambiguous verdicts, no cross-wave conflicts, and settled methodology produces ZERO workshops. The investigator MUST emit "## No workshops" with one paragraph explaining why. This is HONEST.

Padding with carry-forward listings dressed as workshops violates this rule (the workshop definition), the project's no-technical-debt / fix-in-session discipline (carry-forwards belong in the next session's plan), and the principle that length is not quality.

## Honest count discipline

A typical session produces 0-4 genuine workshops. Even a content-heavy multi-wave session may produce only 2-5; the rest of the substance feeds carry-forwards (next session's plan) or is settled in place. An investigator reporting 5-10 "workshops" per wave is almost certainly carrying-forward bloviation. Sanity-check the count against the four-condition definition.

## Discriminating decision: workshop vs carry-forward

When evaluating any candidate from a closed session's substance, apply this 3-question procedure BEFORE adding it to the workshop schedule. The first YES wins.

### Q1 -- Is the tension a substantive adjudication?

Does the candidate's resolution require deciding between TWO+ competing readings of a result, structural identity, or convention, with first-principles arguments on both sides? If YES -> workshop. If NO -> continue to Q2.

Markers of a real adjudication: (i) the disagreement is about WHAT the result MEANS, not what status to tag it with; (ii) the two readings invoke different machinery / methods; (iii) the two readings cannot both be right -- the workshop's job is to derive which is correct, producing a STRUCTURAL VERDICT.

Sub-classification once Q1 is YES:

- **Q1a -- cross-rebuttal essential to converge** (the agents must respond to each other's arguments) -> Slot 2 workshop (`/rclab-workshop`, EXACTLY 2 agents).
- **Q1b -- independent reading suffices** ("synthesize / characterize / survey X") -> Slot 1 solo review (`/rclab-review`, 1+ agents, default 1 = the question owner).
- Default to Slot 1 when uncertain -- workshops are expensive.

### Q2 -- Is the candidate registry-state, hygiene, gate finalization, or a framework issue?

A candidate is Q2 if its resolution is one of: a status-tag edit; a mechanical promotion (pre-conditions met, only the bookkeeping move remains); provenance / canonical-value hygiene; a rule / methodology extension both agents would agree on; an audit-script extension any methodology-aware agent would derive the same way; a registry-write hygiene fix; a gate-finalization gap (verdict backfill, working-paper section finalization the completion check missed).

**One-line marker test**: would the resolution be a status-tag edit / mechanical promotion / rule-file diff / audit-script extension / mechanical re-run, rather than a derivation that produces a new structural claim? If YES, it is Q2 -- the "tension" is bookkeeping, not adversarial substance. -> carry-forward (route per the table below), NOT a workshop.

### Q3 -- Is the candidate a parallel-compute structure (N conditions x N axes)?

Does the candidate involve N prerequisite conditions, each on a different axis, each with its own pre-registered PASS criterion, where the N verdicts combine via logical AND for the final outcome? If YES -> carry-forward to the working paper as a parallel-wave-together structure (N pre-registered sub-gates + 1 AND closeout), NOT a workshop -- regardless of how many agents would be involved. The per-axis agent attribution is a derivation-author tag, not a workshop-participant tag (no cross-agent rebuttal, because the axes are orthogonal).

### Routing summary

| Decision | Route to | Lands in |
|:--|:--|:--|
| Q1a YES (cross-rebuttal adjudication) | Workshop schedule, Slot 2 (`/rclab-workshop`) | `sessions/session-{N}/session-{N}-workshop-schedule.md` |
| Q1b YES (independent reading) | Workshop schedule, Slot 1 (`/rclab-review`) | same schedule |
| Q2 YES -- in-session fix | Fix it now (the edit lives in the relevant rule / template / registry file) | -- |
| Q2 YES -- needs future compute | Carry-forward (4-field spec) | the investigated wave's WP `## Carry-Forward Computations` section |
| Q3 YES (parallel-compute wave) | Carry-forward, marked "wave-together" | same WP CF section |
| Pre-compute shell wave ("is NOT" item 9) | Escalation (`/rclab-coordinate` retry, NOT a CF) | -- |
| Multiple YES | Q1 wins; else Q2; else Q3 | -- |

**Canonical-vs-mirror split**: carry-forwards (Q2-compute / Q3) are lifted to the investigated wave's working paper `## Carry-Forward Computations` section as 4-field blocks (what / inputs / gate / effort). `/rclab-plan` consumes the working paper, NOT the workshop schedule -- a compute carry-forward that lives ONLY in the schedule is invisible to the next-session planner. Workshop OUTCOMES (the verdicts `/rclab-review` and `/rclab-workshop` produce) feed the next plan separately.

## Cross-references

- **Carry-forwards go to `/rclab-plan`** -- every wave-synthesis produces 4-field structured carry-forwards (what / inputs / gate / effort); those are inputs to the NEXT session's plan, not to a workshop schedule. The workshop schedule and the carry-forward queue are SEPARATE outputs.
- **`/rclab-investigate` skill** -- investigator and consolidator prompts MUST cite this rule as authoritative and read it BEFORE producing candidates. The seed file uses `## Workshops` (not `## Candidates`) to enforce the categorical distinction; non-workshop computes go under a separate `## Carry-forwards (route to /rclab-plan, NOT this schedule)` section.
- **`.claude/templates/workshop-schedule.md`** -- the schedule's output shape (Slot 1 `/rclab-review` solos / Slot 2 `/rclab-workshop` pairs / Slot 3 closeout) and the load-bearing skill-slot invariant: never emit `/rclab-review --type workshop` (workshop semantics live in `/rclab-workshop`, not in flags on `/rclab-review`).
- **Large working papers** -- for very large sources the investigator partition is size-driven (`/rclab-investigate` Phase 1); each chunk should cover enough cross-wave substance that cross-wave tensions are visible to at least one investigator.
