# sessions/session-plan/ — Planning Documents

<!-- DEPLOY: project-root/sessions/session-plan/CLAUDE.md -->

This directory contains planning material — session prompts, agendas, pre-session analysis, and handoff documents that set up future sessions.

## What Belongs Here

- **Session prompts** — the original prompt or research question for a planned session
- **Agendas** — structured plans for upcoming sessions (agent composition, format, objectives)
- **Pre-session analysis** — background research done before a session begins
- **Handoff documents** — when referenced for planning (originals live in their session directory)
- **Team composition plans** — which agents, which archetypes, cost tier analysis

## What Does NOT Belong Here

- **Session outputs** — those go in `sessions/session-NN/`
- **Framework documents** — those go in `sessions/framework/`
{{if-compute}}
- **Computation scripts** — those go in `{{COMPUTATION_DIR}}/`
{{endif-compute}}

## Planning Workflow

1. **Review previous handoff** — read the most recent session's handoff document
2. **Choose session format** — use the selection guide at `sessions/session-plan/format-selection-guide.md`
3. **Plan agent composition** — select archetypes, estimate cost tier requirements
4. **Write session prompt** — specific research question or objective
5. **Pre-register gates** — if the session involves computation, define pass/fail criteria BEFORE starting

## File Naming

```
plan-session-NN-descriptor.md     # Plan for session NN
agenda-session-NN.md              # Detailed agenda
prompt-session-NN.md              # The research prompt
```

## Rules

- **Plans are inputs, not outputs** — this directory feeds INTO sessions, session directories hold the outputs
- **Pre-register before computing** — gate criteria defined here, verdicts recorded in the session directory
- **Cost-conscious planning** — estimate opus vs. sonnet vs. haiku requirements before spawning
