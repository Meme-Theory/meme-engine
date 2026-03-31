---
paths:
  - "sessions/**"
---

# Session File Standards

<!-- DEPLOY: project-root/.claude/rules/session-handoffs.md -->
<!-- Path-scoped: loads only when working in the sessions directory -->

## Session Naming

- **Directories**: `session-NN/` — zero-padded session number
- **Files**: `session-NNx-descriptor.md` — where `x` is optional sub-session letter
- **Examples**: `session-01-first-contact.md`, `session-14b-spectral-action.md`

## Mandatory Handoff

Every session directory must contain a handoff document. No exceptions. See the Output Standards rule for the 7-section format.

## Knowledge Index Integration

After editing any session file, run `/weave --update` to rebuild the knowledge index. The PostToolUse hook will remind you, but the responsibility is yours.

## Chronological Integrity

- Never renumber existing sessions
- Never move outputs between session directories
- Sub-sessions (a, b, c) are for same-day continuations of a session topic

## Recommendation Carry-Forward

Every session produces reviewer recommendations (computations, suggestions, open questions, pre-registerable predictions). These MUST be carried forward into the next session's plan as planned computations — not deferred lists, not "acknowledged but not included."

- The next session's plan is the ONLY carry-forward mechanism. The knowledge index tracks theorems, gates, and closures — not open suggestions.
- If a recommendation is not planned in the next session, it is effectively lost. No future instance will go looking for it.
- All recommendations go in the plan. Core topic items in early waves. Everything else in later waves. Nothing gets a "DEFERRED" label instead of a computation spec.
