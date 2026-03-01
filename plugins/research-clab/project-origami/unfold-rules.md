# Unfold: Behavioral Rules

**Target agent**: Coordinator
**Task**: Install behavioral rules into `.claude/rules/` and verify they're referenced from CLAUDE.md.
**Inputs**: None (rules are universal).
**Reads from**: `${CLAUDE_PLUGIN_ROOT}/templates/claude-md/rules/`

---

## Context

Behavioral rules are `.claude/rules/*.md` files that Claude Code automatically loads into every agent's context. They enforce team discipline, epistemic standards, and output quality without repeating the rules in every agent definition.

These rules exist because things broke without them. Each one addresses a specific failure mode.

---

## Step 1: Copy Rule Files

Copy each rule file from `${CLAUDE_PLUGIN_ROOT}/templates/claude-md/rules/` into `.claude/rules/`:

| Source | Target | What It Enforces |
|:-------|:-------|:-----------------|
| `team-lead-behavior.md` | `.claude/rules/team-lead-behavior.md` | Don't over-manage, shut down agents when done, never self-terminate, one team at a time, always spawn coordinator, clean stale teams, blast-first |
| `teammate-behavior.md` | `.claude/rules/teammate-behavior.md` | Inbox first, limit self-induced work, respond to interrupts, message by name, wait for roster, one topic per message |
| `epistemic-discipline.md` | `.claude/rules/epistemic-discipline.md` | Evidence hierarchy, pre-registration, constraint framing, confidence ownership, what counts as a result |
| `output-standards.md` | `.claude/rules/output-standards.md` | One writer per file, specific action items, mandatory handoffs, formatting precision |
| `gate-verdicts.md` | `.claude/rules/gate-verdicts.md` | Gate format, classification criteria (PASS/CLOSED/FAIL), compliance checking |
| `session-handoffs.md` | `.claude/rules/session-handoffs.md` | Handoff document structure, what must be captured, recovery instructions |

These files are copied verbatim — no substitutions needed.

---

## Step 2: Verify CLAUDE.md References

The root CLAUDE.md (installed by unfold-structure) should already reference the rules system. Verify it contains a section like:

```markdown
## Behavioral Rules

Rules in `.claude/rules/` are automatically loaded into every agent's context.
Do NOT duplicate rule content in individual agent definitions.
```

If this section is missing, add it.

---

## Step 3: Verify Rule Coherence

After copying, spot-check:

1. **team-lead-behavior.md** contains the blast-first spawn sequence
2. **teammate-behavior.md** contains the inbox-first rule
3. **epistemic-discipline.md** contains the "only Skeptic states confidence" rule
4. **output-standards.md** contains the "one writer per file" rule
5. **gate-verdicts.md** contains the PASS/CLOSED/FAIL classification format
6. **session-handoffs.md** contains the 7-section handoff template

If any file is missing or empty, report the gap.

---

## What You Do NOT Do

- **Do NOT modify rule content** — these are battle-tested, copy verbatim
- **Do NOT add project-specific rules** — those go in CLAUDE.md, not in rules/
- **Do NOT duplicate rules into agent definitions** — agents inherit them automatically
- **Do NOT create custom rule files** during initial unfolding — that happens as the project evolves

Your job is installation. The rules enforce themselves once loaded.
