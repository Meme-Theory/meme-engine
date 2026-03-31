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
| `team-lead-behavior.md` | `.claude/rules/team-lead-behavior.md` | Don't over-manage, task-based monitoring, blast-first protocol, compute mode protocol, never self-initiate shutdown |
| `teammate-behavior.md` | `.claude/rules/teammate-behavior.md` | Inbox first, limit self-induced work, respond to interrupts, message by name, wait for roster, ready protocol, task ownership |
| `epistemic-discipline.md` | `.claude/rules/epistemic-discipline.md` | Evidence hierarchy, pre-registration, constraint framing, mechanism assessment, what counts as a result, reporting format |
| `output-standards.md` | `.claude/rules/output-standards.md` | One writer per file, specific action items, mandatory handoffs, formatting precision |
| `gate-verdicts.md` | `.claude/rules/gate-verdicts.md` | Gate format, pre-registration protocol, verdict permanence, compliance checking |
| `session-handoffs.md` | `.claude/rules/session-handoffs.md` | Handoff document structure, chronological integrity, recommendation carry-forward |
| `agent-standards.md` | `.claude/rules/agent-standards.md` | Formal rigor, dimensional consistency, persistent memory guidelines |
| `evoi-prioritization.md` | `.claude/rules/evoi-prioritization.md` | EVOI computation priority, evidence weighting, effort-based probability tracking |

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

1. **team-lead-behavior.md** contains the blast-first protocol and compute mode protocol
2. **teammate-behavior.md** contains the inbox-first rule, ready protocol, and task ownership
3. **epistemic-discipline.md** contains the evidence hierarchy and mechanism assessment sections
4. **output-standards.md** contains the "one writer per file" rule
5. **gate-verdicts.md** contains the pre-registration protocol and verdict format
6. **session-handoffs.md** contains the recommendation carry-forward section
7. **agent-standards.md** contains formal rigor and persistent memory guidelines
8. **evoi-prioritization.md** contains the EVOI formula and evidence weighting rules

If any file is missing or empty, report the gap.

---

## What You Do NOT Do

- **Do NOT modify rule content** — these are battle-tested, copy verbatim
- **Do NOT add project-specific rules** — those go in CLAUDE.md, not in rules/
- **Do NOT duplicate rules into agent definitions** — agents inherit them automatically
- **Do NOT create custom rule files** during initial unfolding — that happens as the project evolves

Your job is installation. The rules enforce themselves once loaded.
