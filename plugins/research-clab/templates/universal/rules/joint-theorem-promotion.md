---
paths:
  - "sessions/**"
---

# Joint Result Promotion Pathway

<!-- DEPLOY: project-root/.claude/rules/joint-theorem-promotion.md -->
<!-- Path-scoped: loads when working in sessions/ (workshops, cross-reviews, registry writes). -->

This rule defines the 4-stage upgrade pathway for promoting a **joint cross-axis result** (a theorem, claim, or finding) into the project's permanent results registry under `sessions/framework/`. A joint result is one whose statement contains clauses requiring evidence from MORE THAN ONE methodological axis -- for example an analytical derivation plus an empirical observation, two independent proof strategies, or a theoretical prediction plus an independent computational verification. No single axis can establish it alone.

This rule is the **constructive complement** to `epistemic-discipline.md` ("What Does Not Count as a Result" -> "Agreement among agents (shared context produces shared outputs, not independent confirmation)"). That exclusion forbids shared-context agreement from counting as evidence. The 4-stage pathway specifies HOW genuinely joint-axis evidence becomes registry-eligible WITHOUT falling into the agreement-as-evidence trap.

## Why a constructive complement is needed

The "agreement among agents" exclusion prevents shared-context-produced agreement from being mistaken for independent confirmation. But that exclusion alone gives no pathway for a genuine joint-axis result -- one whose statement is intrinsically cross-axis and cannot be derived from a single axis.

The resolution: joint clauses are authored ONCE (Stage 0), registered as a CANDIDATE (Stage 1), then independently verified by TWO agents on DIFFERENT axes who operate WITHOUT prior workshop context (Stage 2), before the result becomes permanent (Stage 3). The agreement that emerges from Stage 2 is structurally NOT shared-context agreement -- the two cross-reviewers have never seen the workshop output.

## The 4 stages

### Stage 0 -- Workshop-Internal Candidate

- **Where**: within a workshop's closure or wrap-up section.
- **Form**: candidate text drafted by the workshop's authoring agents (typically two agents on different axes); contains all clauses with per-clause cross-axis attribution (which axis authored each clause, and which clauses are JOINT).
- **PASS criterion**: every clause is stated with explicit author-side attribution; the workshop verdict freezes the text.
- **Status**: workshop-internal artifact only; NOT yet in the registry.

### Stage 1 -- Registration as Candidate (next session)

- **Where**: the permanent results registry under `sessions/framework/`.
- **Form**: full text from Stage 0 + a `STAGE-1-CANDIDATE` tag + identification of the JOINT clauses (those requiring Stage-2 cross-axis verification) + any corrigenda from the originating workshop.
- **PASS criterion**: registry entry written with all clauses, all corrigenda, joint-clause flags, and authorship attribution; `STAGE-1-CANDIDATE` tag present.
- **Status**: registered as a CANDIDATE only -- not permanent. Downstream work may CITE it but MUST carry the `STAGE-1-CANDIDATE` qualifier.

### Stage 2 -- Two-Agent Parallel Cross-Check (mandatory upgrade gate)

- **Where**: one dedicated independent-verification gate.
- **Form**: TWO independent cross-reviewers, ONE per axis, dispatched IN PARALLEL:
  - the Axis-A cross-reviewer audits the Axis-A clauses + the JOINT clauses;
  - the Axis-B cross-reviewer audits the Axis-B clauses + the JOINT clauses;
  - both operate WITHOUT prior workshop context -- they read ONLY the registered Stage-1 entry, never the workshop transcript;
  - JOINT clauses are PASS-AND'd across the two verdicts (BOTH reviewers must independently PASS each joint clause -- logical AND, not OR).
- **PASS**: both cross-reviewers PASS their single-axis clauses AND both independently PASS every JOINT clause. This is independent verification per `epistemic-discipline.md`.
- **FAIL**: either reviewer FAILs any clause -> promotion blocked; the result stays at Stage 1; the failing clauses route to next-session remediation.
- **INFO**: either reviewer returns INFO on a clause -> the result stays at Stage 1; the clause is documented as a deferred item.

### Stage 3 -- Permanent Registration

- **Where**: the registry -- replace `STAGE-1-CANDIDATE` with `STAGE-3-PERMANENT`.
- **Form**: the result joins the permanent results table alongside the project's other structural results.
- **PASS criterion**: a Stage-2 PASS verdict landed; the session-end synthesis updates the registry tag.
- **Status**: permanent -- citable as a structural result without the candidate qualifier.

## Two-agent independent-verify (Stage 2 details)

Stage 2 requires TWO independent agents on DIFFERENT axes, dispatched IN PARALLEL, BOTH operating WITHOUT prior workshop context. Single-agent verification of joint clauses is structurally INSUFFICIENT.

The "without prior workshop context" condition is what makes the agreement count:

- the cross-reviewers receive ONLY the registered Stage-1 entry text + the relevant input files;
- they do NOT receive the workshop transcript;
- they cannot be the original workshop authoring agents;
- they are dispatched with explicit instruction to verify the registered result from first principles, NOT to re-derive it along the workshop's path.

If both reviewers independently PASS a joint clause without having read the workshop, the agreement is structurally independent -- it is evidence under the standard "What Counts as a Result" criterion. If they shared the workshop context, it is not (per the epistemic-discipline exclusion).

### Axis-B selection protocol

When dispatching the Stage-2 Axis-B cross-reviewer, satisfy ALL THREE conditions:

1. **Axis-distinctness**: the Axis-B reviewer's primary methodology is on a DIFFERENT axis from Axis-A. Two reviewers who differ only in narrow specialty but share the same axis FAIL this condition.
2. **Original-author exclusion (with downstream-inheritance reach)**: neither cross-reviewer may be (a) an original workshop authoring agent, or (b) a successor agent whose memory inherits the workshop's reading-path -- e.g. an agent whose own memory or notes cite the workshop transcript as canonical reference. Such an agent is pre-loaded with the workshop's view and fails the "without prior workshop context" requirement.
3. **Audit-coverage adequacy**: the Axis-B reviewer's expertise MUST cover ALL joint clauses + ALL Axis-B single-axis clauses. Partial coverage creates gaps where a joint clause passes formally but is never substantively examined cross-axis.

## Independence audit at gate dispatch

Before a Stage-2 gate is dispatched, verify:

1. two cross-reviewers are dispatched in parallel (not sequentially);
2. the reviewers are on DIFFERENT axes;
3. neither reviewer is an original workshop authoring agent (apply the downstream-inheritance reach);
4. the dispatch prompts do NOT include the workshop transcript;
5. JOINT clauses are PASS-AND'd across both verdicts in the gate logic.

Missing any of these -> the verification is not independent -> Stage 2 -> 3 promotion is blocked.

## Optional hardening -- input orthogonality

For a Stage-2 verification over N >= 2 observables, you MAY additionally require **input orthogonality**: at least one observable's input data is loaded by exactly ONE cross-reviewer, not both. Without it, PASS-AND establishes that two distinct decision pipelines agree on the SAME data (output-type independence) but not that the inputs themselves were independent. When the predicate fails, tag the promotion with an explicit "shared-input caveat." This is optional hardening, not a floor.

## Forward-looking convention

This pathway is the only recognized route for a joint cross-axis result to enter the permanent results table. A result registered without the 4-stage progression is NOT eligible.
