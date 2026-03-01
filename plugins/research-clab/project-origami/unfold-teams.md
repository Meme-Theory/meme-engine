# Unfold: Team Management Protocol

**Target agent**: Coordinator
**Task**: Configure team management defaults, embed operational protocol into coordinator memory.
**Inputs**: None (protocol is universal).
**Reads from**: `${CLAUDE_PLUGIN_ROOT}/TEAM-MANAGEMENT-PROTOCOL.md` (reference)

---

## Context

The team management protocol is already encoded in three places:
1. `.claude/rules/team-lead-behavior.md` — loaded into every agent's context
2. `.claude/rules/teammate-behavior.md` — loaded into every agent's context
3. `/clab-team` skill — enforces blast-first spawn, max 3 agents, hands-off discipline

This unfold doc ensures the coordinator ALSO has the protocol in its memory so it can reference it when orchestrating teams.

---

## Step 1: Write Team Protocol to Coordinator Memory

Append to `.claude/agent-memory/coordinator/MEMORY.md` (after the methodology section installed by unfold-methodology):

```markdown
## Team Operations Protocol

### Spawn Sequence (MANDATORY)
1. Spawn agents with minimal prompts ("Wait for instructions")
2. Wait for ALL agents to idle
3. Roster blast (name-to-type mapping as first inbox message)
4. THEN send real work

### Hard Limits
- MAX 3 agents per team (4+ = notification avalanche)
- ONE team at a time (cross-team inbox contamination is unfixable)
- ALWAYS include a coordinator in every team

### Team Lead Discipline
- Do NOT over-manage — let specialists work
- Do NOT run agents' scripts or duplicate their analysis
- Do NOT mark agents' tasks completed — they mark their own
- Do NOT write agents' designated output files
- Do NOT nudge idle agents — idle notifications are normal
- Do NOT initiate shutdown — ONLY the user decides
- ONE shutdown request per agent, never retry

### Orchestration Patterns
- **Fan-Out**: Independent tasks, parallel work, collect results
- **Pipeline**: Sequential dependencies, each step gates the next
- **Debate**: Agents take positions, critique each other (2-3 rounds max)
- **Coffee Talk**: Paired assessment, joint document
- **Workshop**: Sequential rounds with markdown handoff between teams

### Session Formats → Team Sizes
- First Contact / Debate / Panel: 3 agents
- Computation Sprint: 2-3 agents
- Workshop: 2-3 per round (sequential teams)
- Clab Review: batches of 5-6 (not a team — parallel independent agents)
```

---

## Step 2: Configure Clab-Team Defaults

The `/clab-team` skill is already installed. No additional configuration needed — it discovers agents dynamically from `.claude/agents/` and uses the blast-first workflow.

Verify the skill exists at `.claude/skills/clab-team/SKILL.md`. If missing, report the gap.

---

## Step 3: Clean Runtime State

Ensure no stale team/task state exists:

```
~/.claude/teams/     → should be empty (no active teams)
~/.claude/tasks/     → should be empty (no active task lists)
```

If stale state exists, delete it.

---

## What You Do NOT Do

- **Do NOT modify the team management protocol** — it's battle-tested
- **Do NOT create a team during unfolding** — teams are created when the user runs sessions
- **Do NOT add project-specific team rules** — put those in CLAUDE.md if needed
- **Do NOT modify the clab-team skill** — it's already generalized

Your job is embedding the protocol in coordinator memory. The skills and rules enforce it at runtime.
