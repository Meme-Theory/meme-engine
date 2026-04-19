# Unfold: Team Management Protocol

**Target agent**: Coordinator
**Task**: Configure team management defaults, embed operational protocol into coordinator memory.
**Inputs**: None (protocol is universal).
**Reads from**: `${CLAUDE_PLUGIN_ROOT}/TEAM-MANAGEMENT-PROTOCOL.md` (reference)

---

## Context

The team management protocol is already encoded in three places:
1. `{root}/team-lead-behavior.md` — at project root so subagents do NOT auto-load it; read by the orchestrator only
2. `.claude/rules/teammate-behavior.md` — loaded into every agent's context
3. `/rclab-team` skill — enforces blast-first spawn (workshop/panel) or parallel independent agents (compute), hands-off discipline

This unfold doc ensures the coordinator ALSO has the protocol in its memory so it can reference it when orchestrating teams.

---

## Step 1: Write Team Protocol to Coordinator Memory

Append to `.claude/agent-memory/coordinator/MEMORY.md` (after the methodology section installed by unfold-methodology):

```markdown
## Team Operations Protocol

The active pipeline is **compute mode** — each piece of work is a standalone Agent call with no inboxes, no SendMessage routing, no TeamCreate. For concrete procedure see `team-lead-behavior.md` at project root and the `/rclab-coordinate`, `/rclab-review`, `/rclab-workshop` skills.

### Compute Mode Protocol
1. `TaskCreate` for all computations across ALL waves (with wave dependencies via `blockedBy`)
2. Spawn current wave's agents as independent Agent calls — ALL in a single message (parallel)
3. Monitor via `TaskList` — do NOT intervene unless an agent explicitly errors
4. When all wave tasks complete: read working-paper sections, verify on-disk artifacts, evaluate decision points
5. Report wave results to user with decision-point recommendation
6. On user go-ahead, spawn next wave (loop back to step 2)
7. After all waves: read the complete working paper, write gate verdicts, write team-lead synthesis

### Team Lead Discipline
- Do NOT over-manage — let specialists work
- Do NOT run agents' scripts or duplicate their analysis
- Do NOT mark agents' tasks completed — they mark their own
- Do NOT write agents' designated output files
- Do NOT nudge idle agents — idle notifications are normal
- Shut down agents when work is complete; move on if they reject the shutdown
- Only the USER terminates the team lead session

### Hard Limits
- Concurrency cap: 8 agents per wave — split larger waves into sub-waves dispatched sequentially
- Compute mode: no TeamCreate, no SendMessage, no inboxes

### Task Metadata
`TaskCreate` should include structured metadata for tracking:
`metadata: { wave: N, gate_id: "...", agent_type: "..." }`

### Permission Mode
Compute agents that write scripts and working paper sections should be spawned with:
`mode: "acceptEdits"` — prevents permission prompts from blocking autonomous computation

### Session Formats → Dispatch Patterns
- First Contact / Review: independent Agent calls per reviewer (no team)
- Computation Sprint (`/rclab-coordinate`): unlimited per wave, parallel independent Agent calls
- Workshop (`/rclab-workshop`): exactly 2 agents, sequential Agent calls (Edit-based on shared doc)
- Investigate → Review (`/rclab-investigate` → `/rclab-review` campaign): parallel per slot
```

---

## Step 2: Configure Clab-Team Defaults

The `/rclab-team` skill is already installed. No additional configuration needed — it discovers agents dynamically from `.claude/agents/` and uses the blast-first workflow.

Verify the skill exists at `.claude/skills/rclab-team/SKILL.md`. If missing, report the gap.

---

## Step 3: Runtime State Note

`~/.claude/teams/` and `~/.claude/tasks/` hold Claude Code's runtime state for active teams and task lists. The scaffold does NOT delete this state — it may contain the user's in-flight work on other projects.

If the user wants stale team/task state cleaned before starting a new session, they can do so manually outside the scaffold flow. The `/rclab-team` and `/rclab-coordinate` skills also handle stale-state cases at invocation time.

---

## What You Do NOT Do

- **Do NOT modify the team management protocol** — it's battle-tested
- **Do NOT create a team during unfolding** — teams are created when the user runs sessions
- **Do NOT add project-specific team rules** — put those in CLAUDE.md if needed
- **Do NOT modify the rclab-team skill** — it's already generalized

Your job is embedding the protocol in coordinator memory. The skills and rules enforce it at runtime.
