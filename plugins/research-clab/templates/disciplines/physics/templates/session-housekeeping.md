# Session Housekeeping Template

Per-session bookkeeping ledger. Filled in DURING the session's wave-compute (at wave-synthesis time), BEFORE `/rclab-investigate` runs.

This ledger is the CANONICAL list of a session's **bookkeeping items** -- the things that are NOT adversarial physics: status-tag edits, mechanical promotions, provenance hygiene, rule/template diffs, audit-script extensions, gate finalization, and pre-compute escalations. Working-paper `## Carry-Forward Computations` blocks for the future-compute sections (B/C/D) are MIRRORS of the entries here.

## Purpose

Catching bookkeeping items at wave-compute (not at `/rclab-investigate` time) closes two failure modes:

1. **Workshop bloat** -- bookkeeping items dressed as workshops waste dispatch cycles.
2. **Carry-forward invisibility** -- items that exist only in a schedule are invisible to `/rclab-plan`, which reads working-paper carry-forward blocks, not schedules.

Closing both: identify bookkeeping items at wave-close; record FIXES in Section A (effected in-session); record genuine-future-compute items in Sections B/C/D with 4-field specs that mirror to working-paper CF blocks; escalate pre-compute shell waves in Section E.

## Section A vs Sections B-D (load-bearing distinction)

**Section A is the record of what was already effected IN-SESSION.** Hygiene observations on already-correct artifacts are NOT carry-forwards; status-tag edits, mechanical promotions, audit-script regex extensions, and other orchestrator-direct edits MUST happen in the same session that surfaced them. Section A is the audit trail of those fixes, not a queue.

**Sections B/C/D are genuinely future-compute items.** An item belongs in B-D iff its resolution requires compute that an orchestrator-direct edit cannot perform: an independent cross-verify by a second agent; a promotion whose verdict depends on a numerical re-run; a parallel-compute wave with per-axis pre-registered thresholds; a methodology rule extension whose freeze depends on a validator. If an item can be effected by an Edit/Write on a rule/template/registry/canonical-module file with no compute, it belongs in Section A, NOT B-D.

## Canonical instance path

`sessions/session-{N}/session-{N}-housekeeping.md`

## Schema

```markdown
# Session {N} Housekeeping Ledger

**Date**: {today}
**Session**: {N}

## Bookkeeping marker

A candidate is a bookkeeping item iff its resolution is a status-tag edit / mechanical
promotion / rule-file diff / audit-script extension / mechanical re-run, rather than a
derivation that produces a new structural claim.

---

## A. In-session resolutions (already effected; ledger only)

Items in this section were FIXED during S{N} wave compute. Each row cites the surfacing
wave/gate, the resolution edit (file:lines), and the gate's verdict-line closure SHA short.

| # | Source wave / gate | Item | Resolution (file:lines) | Verified at (closure SHA short) |
|:--|:-------------------|:-----|:------------------------|:--------------------------------|
| A1 | W{w}-{g} | {one-line description} | `path/to/file.md:LL-LL` | `{short16}` |

If no in-session resolutions: write `(none -- no bookkeeping items fixed in-session)`.

---

## B. Promotion-compute carry-forwards (4-field spec; mirrored to WP CF)

Bookkeeping items requiring mechanical compute next session: promotion via an independent
cross-verify (cannot be effected by an orchestrator edit); canonical-module promotions whose
value comes from a re-run; registry-row landings whose anchor binds to a compute output.

Each entry MUST be MIRRORED to the originating wave's working-paper `## Carry-Forward
Computations` section so `/rclab-plan` consumes it via its existing contract.

### CF-S{N+1}-HK-{n} -- {one-line title}

> **Why not Section A**: {one sentence naming the compute step that prevents an
>   orchestrator-direct edit -- e.g. "the canonical value is a re-run output that
>   does not exist yet" or "promotion needs a second-agent independent verify".}

1. **What**: {specific deliverable}
2. **Inputs**: {file paths + canonical references + upstream gate closure SHA if applicable}
3. **Gate**: `S{N+1}-{GATE-ID}` with PASS criterion = {artifact-existence predicate if
   methodology-class, OR a specific numerical predicate if compute-class}
4. **Effort**: {wave-equivalents}

If no Section B items: write `(none)`.

---

## C. Parallel-compute-wave carry-forwards (mirrored to WP CF)

Items with N prerequisite conditions on structurally orthogonal axes + 1 wave-AND closeout.
Each entry uses the 4-field spec + per-axis sub-gate enumeration. Mirrored to WP CF.

### CF-S{N+1}-HK-{n} -- {one-line title}

> **Why not a workshop**: {one sentence naming the structural orthogonality of the N axes
>   that rules out adversarial adjudication -- no cross-axis rebuttal is meaningful.}

1. **What**: N-axis prerequisite validation; logical-AND closeout for the composite verdict
2. **Inputs**: per-axis prerequisites
3. **Gate**: N parallel sub-gates dispatched together:
   - `S{N+1}-{GATE-A}` -- axis A; PASS criterion = {...}
   - `S{N+1}-{GATE-B}` -- axis B; PASS criterion = {...}
   - **Wave-closeout gate**: `S{N+1}-{GATE-AND}` -- PASS = ALL N sub-gates PASS (logical AND)
4. **Effort**: {wave-equivalents}

If no Section C items: write `(none)`.

---

## D. Methodology-rule extensions (mirrored to WP CF)

Bookkeeping items resolving as rule-file diffs (Edit/Write on `.claude/{rules,templates,skills}/**`
only; verbatim sub-diff from a closed workshop/synthesis). If the rule extension content is
contested between two specific agents, it is NOT a bookkeeping item -- re-route it to a workshop.

### CF-S{N+1}-HK-{n} -- {one-line title}

1. **What**: rule-file diff at `.claude/rules/{rule-file}.md` -- state the structural extension
2. **Inputs**: cited source workshop/synthesis; pre-existing rule version SHA
3. **Gate**: `S{N+1}-{GATE-ID}` with an artifact-existence PASS predicate
4. **Effort**: {wave-equivalents}

If no Section D items: write `(none)`.

---

## E. Pre-compute shell waves (upstream escalation; NOT a CF)

A wave is a pre-compute shell iff ALL hold: every gate `Status: NOT STARTED` in the WP AND
no matching artifacts on disk (verify via Glob) AND no matching gate-IDs in the verdict file
(verify via grep). These are upstream-pipeline state for `/rclab-coordinate`, NOT carry-forwards.
Do NOT create wave-execution carry-forward entries for them.

| Wave | State evidence (Glob + grep verified) | Escalation |
|:-----|:--------------------------------------|:-----------|
| W{w} | all gates NOT STARTED; no artifacts; no gate-IDs in verdict file | Re-dispatch `/rclab-coordinate sessions/session-plan/session-{N}-plan-w{w}.md` |

If no Section E items: write `(none -- no pre-compute shell waves detected)`.

---

## F. Structural counts (artifact shape; not length)

| Category | Count |
|:---------|------:|
| A In-session resolutions | {n} |
| B Promotion-compute CFs (mirrored to WP) | {n} |
| C Parallel-wave CFs (mirrored to WP) | {n} |
| D Methodology rule extensions (mirrored to WP) | {n} |
| E Pre-compute shell waves (escalation only) | {n} |
| **Total bookkeeping items surfaced** | {sum} |

---

## Consumption pointers

- **`/rclab-investigate` (S{N})**: read this file BEFORE producing candidates. Every A-E entry
  is a non-workshop. A new bookkeeping candidate not in this file indicates an upstream
  wave-synthesis miss -- route it to the appropriate section here (NOT the schedule), mirror to
  WP CF if it belongs in B/C/D.
- **`/rclab-plan` (S{N+1})**: consume B, C, D via the WP CF blocks they mirror to. Section A is
  ledger-only -- do NOT re-dispatch the fixes. Section E routes to `/rclab-coordinate`.
- **`/rclab-coordinate` (S{N+1})**: dispatch Section E entries as re-runs before opening new waves.

*End of S{N} housekeeping ledger.*
```

## Mirror discipline (WP CF blocks)

For every entry in Sections B / C / D, MIRROR a corresponding CF block into the originating wave's working-paper `## Carry-Forward Computations` section using the same `CF-S{N+1}-HK-{n}` identifier and 4-field structure, with a routing-note pointer back to this ledger so the two views stay synchronized. The housekeeping file is the CANONICAL bookkeeping ledger (filter source for `/rclab-investigate`); the WP CF blocks are MIRRORS (consumption source for `/rclab-plan`). A bare housekeeping entry without a WP CF mirror is invisible to the next-session planner.

## Anti-patterns

- **Section A used as a queue** -- items written to A that were NOT actually effected this session. A is the AUDIT TRAIL of completed fixes, not a TODO list. Uneffected items go in B/C/D with a 4-field spec, or get effected immediately.
- **B-D missing the "Why not Section A" routing note** -- without it, audits cannot distinguish "genuinely requires future compute" from "I deferred a fix I could have made now."
- **B-D entries lacking the WP CF mirror** -- `/rclab-plan` reads working papers, not this file.
- **Section E entries with wave-execution carry-forwards** -- pre-compute shell waves escalate to `/rclab-coordinate` retry, never a manufactured "wave-execution CF".
- **Length targets anywhere** -- content requirements only; no "concise" / "<=N lines" language.
- **Option-asking phrasing in routing notes** -- use directive language ("Mirrored to ...", "Re-dispatch ..."). Never "Should I ...", "Which option ...".

## Cross-references

- `.claude/rules/gate-verdicts.md` -- verdict-line schema (closure SHA the Section A rows cite).
- `.claude/rules/mechanical-closure-discipline.md` -- honest in-session closure for upstream-blocked gates.
- `.claude/rules/epistemic-discipline.md` -- Pre-Registration Completeness.
