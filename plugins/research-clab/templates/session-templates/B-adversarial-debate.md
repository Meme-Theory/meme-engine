# Format B: Adversarial Debate

## When to Use

Testing claims, resolving disagreements, surfacing hidden landmines, or when a prior collaborative session smoothed over genuine tensions.

## How to Launch

Adversarial debate is a live panel — use `/clab-team --mode panel`:

```bash
# Launch a debate panel from a prepared prompt
/clab-team sessions/session-plan/session-05-debate-prompt.md --mode panel

# Explicit team name for tracking
/clab-team sessions/session-plan/session-05-debate-prompt.md --mode panel --team-name debate-qm-claims

# Dry run first to verify agent roster and task extraction
/clab-team sessions/session-plan/session-05-debate-prompt.md --mode panel --dry-run
```

**Why `--mode panel`**: Debate requires agents to read each other's positions and respond in real time. Panel mode creates a live team where agents message each other directly, with a designated writer synthesizing the exchanges. The coordinator moderates but does not contribute domain content.

**Prompt tip**: Pre-assign adversarial postures in the prompt's agent roster table. Without explicit opposing positions, agents default to diplomatic agreement — which defeats the purpose.

## Why This Format Exists

Collaborative sessions produce diplomatic consensus that hides real disagreements. Adversarial debate forces agents to state positions, make explicit concessions, catch each other's errors, and identify the single computation that would settle each dispute.

## Recipe

**Team**: 3-5 specialist agents + 1 coordinator (moderator-only). Each specialist is pre-assigned an adversarial posture.

**Flow**:
```
1. FRAME — State the precise question and prior positions
2. POSITION — Each agent states their position
3. DEBATE — 2-3 rounds of critique, concessions, error-catching
4. CLASSIFY — Each topic resolves to CONVERGENCE or SHARPENED DISAGREEMENT
5. SETTLE — For each open question, identify the single settling computation
```

**Duration**: 1 session

## Plan

```markdown
# Session {{N}} Plan: Adversarial Debate

## Objective
Stress-test {{claim/result}} through structured adversarial debate.

## Agent Roster
| Agent | Assigned Posture |
|:------|:----------------|
| {{agent-1}} | {{e.g., "advocate for X"}} |
| {{agent-2}} | {{e.g., "skeptic of X, formalist"}} |
| {{agent-3}} | {{e.g., "realist, demands computation"}} |

## Debate Topics
1. {{Precise question 1}}
2. {{Precise question 2}}
3. {{Precise question 3}}

## Prior Session Being Stress-Tested
{{Session N-1, which produced the claims now being tested}}
```

## Prompt Template

```markdown
# Session {{N}}: Adversarial Debate — {{Topic}}

## Session Type: ADVERSARIAL DEBATE
## Agents: {{3-5 agents}}
## Session Goal: Surface constraints, landmines, and genuine disagreements
    that were diplomatically smoothed in Session {{N-1}}.

# I. DEBATE TOPICS

## Topic 1: {{Precise question}}
### Prior positions (from Session {{N-1}}):
- {{Agent-1}}: {{position}}
- {{Agent-2}}: {{position}}

## Topic 2: ...

# II. RULES
- Agents MUST make explicit moves (concede, challenge, correct)
- "I agree" is not a valid move — state WHAT you agree with and WHY
- Every debate topic must resolve to either:
  - CONVERGENCE: new joint position stated
  - SHARPENED DISAGREEMENT: clearer map of what's contested + settling computation
- Coordinator moderates only — no domain contributions

# III. OUTPUT DOCUMENTS
1. Debate transcript (per-topic)
2. Concessions log (who conceded what, to whom, on what)
3. Landmine registry (failure modes with severity and probability)
4. Settling computations table (question → computation → time estimate)
5. Revised assessment table (feature-by-feature rating changes with direction arrows)
```

## Concessions Log Format

```markdown
## Concessions Log

| Agent | Conceded | To | On What Topic | Impact |
|:------|:---------|:---|:-------------|:-------|
| {{agent}} | {{what they gave up}} | {{who convinced them}} | {{topic}} | {{rating change}} |
```

## Landmine Registry Format

```markdown
## Landmines Identified

| Landmine | Severity | P(triggers) | Identified By | Would Be Caught By |
|:---------|:---------|:------------|:-------------|:------------------|
| {{failure mode}} | {{HIGH/MED/LOW}} | {{%}} | {{agent}} | {{computation/test}} |
```

## Settling Computations Table

```markdown
## Settling Computations

| Open Question | Computation | Duration | What It Settles |
|:-------------|:-----------|:---------|:---------------|
| {{question}} | {{specific computation}} | {{time}} | {{which debate topic}} |
```

## Failure Modes This Format Prevents

| Problem | How This Format Handles It |
|:--------|:--------------------------|
| False consensus from diplomatic smoothing | Pre-assigned adversarial postures |
| Vague disagreements | "SHARPENED DISAGREEMENT" requires settling computation |
| Untracked position changes | Concessions log creates an audit trail |
| Hidden failure modes | Landmine registry with severity ratings |
