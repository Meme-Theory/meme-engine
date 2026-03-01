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
