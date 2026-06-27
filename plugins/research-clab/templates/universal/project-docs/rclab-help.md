# rclab -- Skill Suite Help

The rclab-* skills cover the full research-lab pipeline (plan -> execute -> investigate -> review/workshop/reflect). Pick one:

## Decision guide

| I want to... | Use |
|:--|:--|
| Plan the next compute session (gather carry-forwards, partition into waves, design test cases) | `/rclab-plan` |
| Execute a planned session by dispatching independent parallel agents per wave, collecting gate verdicts | `/rclab-coordinate` |
| Execute a planned session sequentially in the main agent, with NO subagent spawning (the no-spawn sibling of `/rclab-coordinate`) | `/rclab-solo` |
| Investigate the just-closed session's working paper to design a workshop-schedule campaign (structural patterns, convergences, dissonances) | `/rclab-investigate` |
| Have 1+ agents independently write their own synthesis from the same source docs (no coordination between agents) | `/rclab-review` |
| Have 2 agents iteratively co-author a single shared document over N rounds (sequential, Edit-based, no team infrastructure) | `/rclab-workshop` |
| Run a 2-3 agent team that coordinates via inbox -- panel/debate or multi-round collaborate sessions | `/rclab-team` |
| Reflect on a just-closed wave/session/document -- what stood out, what was surprising, cross-test patterns, next-session highlights | `/rclab-reflect` |
| Run planning/execution/mining against a parallel EXPLORATORY track instead of the canonical session track | add `--investigation` (see below) |

## Pipeline sequence

```
/rclab-plan (S{N})
  -> /rclab-coordinate (S{N})    <- execute the plan (parallel agents)
     or /rclab-solo (S{N})       <- execute the plan sequentially, no subagents
    -> /rclab-investigate (S{N}) <- mine results for a follow-up campaign
      -> /rclab-workshop | /rclab-review | /rclab-team (S{N} campaign)
        -> /rclab-reflect (S{N}) <- introspect on what was learned
          -> /rclab-plan (S{N+1}) <- carry forward into the next session
```

## Investigation track (parallel exploratory pipeline)

A second pipeline that runs alongside the main compute track for open-ended exploration. Invoke planning/execution/mining with `--investigation`:

```
/rclab-plan --investigation         -> sessions/investigation/investigation-{n}/ plan
  -> /rclab-coordinate (or /rclab-solo) on that plan
    -> /rclab-investigate --investigation
```

- Plans, dispatches, and analyses live under `sessions/investigation/investigation-{n}/`.
- Verdicts are track-local: emitted with `emit_verdict(track="investigation")` and written under `{{COMPUTATION_DIR}}/investigation-{n}/`.
- Investigation results are PROVISIONAL until PROMOTED into a numbered session -- promotion is what makes them permanent. An investigations `index.md` tracks the open threads.

## Coordination medium at a glance

| Skill | Medium | Max agents |
|:--|:--|:--|
| `/rclab-coordinate` | Independent Agent calls, no cross-talk | unlimited per wave |
| `/rclab-solo` | Main agent, sequential, no subagents | 0 (no spawn) |
| `/rclab-review` | Independent, each writes own file | any |
| `/rclab-workshop` | Shared document, sequential Edit-based turns | exactly 2 |
| `/rclab-team` (`collaborate` mode) | Team + inbox, multi-round | 2-3 |
| `/rclab-team` (`panel` mode) | Team + inbox, specialists + writer | 2-3 |
| `/rclab-reflect` | Inline, or one fresh agent (`--agent`) | 0-1 |

## Common disambiguations

- **"Workshop"** in legacy session files usually meant a team-based multi-round pattern -- that's now `/rclab-team --mode collaborate`. The skill `/rclab-workshop` is the 2-agent shared-document pattern.
- **"Compute session"** = `/rclab-coordinate` (parallel) or `/rclab-solo` (sequential) executing an `/rclab-plan` output. Not `/rclab-team`.
- **`/rclab-solo` vs "solo"**: `/rclab-solo` runs a whole wave plan in the main agent with no spawning. (There is no `solo` gate type.)
- **"Workshop-schedule"** (as a document) = the output of `/rclab-investigate`: a campaign of `/rclab-review` solos and `/rclab-workshop` pairs to dispatch.
- **"Synthesis"** is generated either by `/rclab-review` (solo, independent) or inside a `/rclab-workshop` / `/rclab-team --mode panel` run.

## Usage -- each skill's own help

Every rclab skill accepts `--help` and prints this document's relevant section. For full argument lists and phase-by-phase behavior, read the skill file directly: `.claude/skills/rclab-{name}/SKILL.md` (or `skill.md`).
