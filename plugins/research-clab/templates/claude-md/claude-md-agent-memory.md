# .claude/agent-memory/ — Persistent Agent State

<!-- DEPLOY: project-root/.claude/agent-memory/CLAUDE.md -->

This directory contains one subdirectory per agent. Each subdirectory holds the agent's persistent memory — state that survives across conversations and sessions.

## Structure

```
agent-memory/
├── constraint-map.md           # Project-wide constraint map (coordinator-owned)
├── coordinator/
│   ├── MEMORY.md               # Auto-loaded into context (keep < 200 lines)
│   ├── session-results.md      # Topic file: session metadata
│   └── {topic}.md              # Additional topic files as needed
├── {{AGENT_NAME}}/
│   ├── MEMORY.md               # Auto-loaded (mandatory)
│   └── {topic}.md              # Overflow topic files
└── ...
```

## MEMORY.md Rules

Every agent has a `MEMORY.md` that is **automatically loaded** into the agent's context at the start of every conversation. This is the agent's "working memory."

| Rule | Detail |
|:-----|:-------|
| **200-line limit** | Lines beyond 200 are truncated. Be concise. |
| **Organize by topic** | Use semantic sections, not chronological entries. |
| **Link to topic files** | For detailed notes, create `{topic}.md` and reference it from MEMORY.md. |
| **No session transcripts** | Store conclusions, not conversation logs. |
| **Update, don't append** | Replace outdated entries rather than adding contradicting new ones. |

## What to Save

- Stable patterns confirmed across multiple sessions
- Key results with source references (session number, file path)
- Proven structural results (theorems, closed mechanisms, gate verdicts)
- Debugging lessons and error patterns
- Architectural decisions and their rationale
- Agent-specific methodology refinements

## What NOT to Save

- Session-specific context (current task, in-progress work)
- Speculative or unverified conclusions from a single computation
- Information that duplicates the root CLAUDE.md
- Full derivations (link to session files instead)
- Probability or confidence statements (Skeptic only)

## Topic Files

When MEMORY.md gets too long, factor content into topic files:

- `{topic}.md` — unlimited length, linked from MEMORY.md
- Name descriptively: `key-results.md`, `debugging-lessons.md`, `constraint-updates.md`
- Topic files are NOT auto-loaded — agents must explicitly read them when needed

## The Constraint Map

`constraint-map.md` lives at the root of `agent-memory/` (not inside any agent's folder). It is the project-wide structured reference for solution-space boundaries.

- **Owner**: The coordinator agent maintains this file
- **Format**: See `.claude/agent-memory/coordinator/constraint-map.md` for full schema
- **Entry types**: Constraints, structural theorems, active channels, unvalidated gates, observational benchmarks
- **State machine**: HYPOTHESIS → PRE-REGISTRATION → COMPUTATION → VERDICT → ENTRY
- **Authority**: Coordinator writes, Skeptic challenges, all agents read

## Ownership Rules

| Who | Can Do |
|:----|:-------|
| Each agent | Read/write its OWN memory directory only |
| Coordinator | Read any agent's memory; write constraint-map.md |
| Librarian | Read any agent's memory (for indexing); write nothing |
| Team lead | Read any agent's memory (for orchestration) |

## Memory Collapse

When agent memory grows unwieldy, run `/shortterm` to trigger a three-agent memory collapse:

1. **Reader** — reads and summarizes all memory files
2. **Analyzer** — identifies redundancy, staleness, contradictions
3. **Writer** — produces compressed, deduplicated memory files

This is a maintenance operation, not a content operation. It preserves meaning while reducing volume.
