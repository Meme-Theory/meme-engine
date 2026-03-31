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
3. `/clab-team` skill — enforces blast-first spawn (workshop/panel) or parallel independent agents (compute), hands-off discipline

This unfold doc ensures the coordinator ALSO has the protocol in its memory so it can reference it when orchestrating teams.

---

## Step 1: Write Team Protocol to Coordinator Memory

Append to `.claude/agent-memory/coordinator/MEMORY.md` (after the methodology section installed by unfold-methodology):

```markdown
## Team Operations Protocol

### Blast-First Spawn Sequence (Workshop/Panel — MANDATORY)
1. Spawn agents with minimal prompt: `"Send a ready message to team-lead using SendMessage, then wait for instructions."`
2. Wait for ALL agents to send their "ready" message (verify with `/team-blast --ready-check`)
3. Execute `/team-blast --list` (roster lands as each agent's FIRST inbox message)
4. THEN send real work via SendMessage

### Hard Limits
- MAX 4 agents per team in workshop/panel modes (more = notification avalanche)
- Compute mode: NO team -- unlimited parallel independent Agent calls per wave
- ONE team at a time (cross-team inbox contamination is unfixable)
- ALWAYS include a coordinator in every team (workshop/panel)

### Compute Mode Protocol (Parallel Independent Agents)
Compute mode does NOT use TeamCreate or blast-first. Each computation is a standalone Agent call.
1. TaskCreate for all computations across ALL waves (with wave dependencies via `blockedBy`)
2. Spawn current wave's agents as independent Agent calls (no `team_name`) -- ALL in parallel
3. Monitor via TaskList -- do NOT intervene unless agent explicitly errors
4. When all wave tasks complete: read working paper sections, evaluate decision points
5. Report wave results to user with decision-point recommendation
6. On user go-ahead, spawn next wave (loop back to step 2)
7. After all waves: read complete working paper, write gate verdicts, write synthesis

### Team Lead Discipline
- Do NOT over-manage -- let specialists work
- Do NOT run agents' scripts or duplicate their analysis
- Do NOT mark agents' tasks completed -- they mark their own
- Do NOT write agents' designated output files
- Do NOT nudge idle agents -- idle notifications are normal
- Monitor via TaskList -- do NOT intervene unless agent explicitly errors
- Shut down agents when work is complete -- one request per agent, move on if rejected
- Only the USER terminates the team lead session

### Task Metadata
TaskCreate should include structured metadata for tracking:
`metadata: { wave: N, gate_id: "...", agent_type: "..." }`

### Permission Mode
Compute agents that write scripts and working paper sections should be spawned with:
`mode: "acceptEdits"` -- prevents permission prompts from blocking autonomous computation

### Orchestration Patterns
- **Fan-Out**: Independent tasks, parallel work, collect results
- **Pipeline**: Sequential dependencies, each step gates the next
- **Debate**: Agents take positions, critique each other (2-3 rounds max)
- **Coffee Talk**: Paired assessment, joint document
- **Workshop**: Sequential rounds with markdown handoff between teams

### Ready Verification
Use `/team-blast --ready-check` after spawning to verify all agents have sent their ready messages before proceeding with the roster blast.

### Session Formats → Team Sizes
- First Contact / Debate / Panel: 3-4 agents (team-based)
- Computation Sprint: unlimited per wave (parallel independent Agent calls, NO team)
- Workshop: 2-3 per round (sequential teams, markdown handoff)
- Clab Review: batches of 5-6 (parallel independent agents)
- Clab Synthesis Workshop: exactly 2 agents (sequential Agent calls, NO team)
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
