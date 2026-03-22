# Meme Engine

A Claude Code plugin marketplace by [Meme-Engine Megacrop Enterprises](https://meme-engine.com).

## Install

```
/install-plugin Meme-Theory/meme-engine
```

## research-clab

Scaffold a complete multi-agent research collaboration in any domain. One command generates the full project architecture: agents, skills, behavioral rules, knowledge tooling, session infrastructure, and a Session 0 plan.

```
/new-research-project
```

### What it builds

```
your-project/
  .claude/
    agents/          3 infrastructure + N domain specialists
    skills/          11 skills (team launch, synthesis, indexing, ...)
    rules/           6 behavioral rules (epistemic discipline, team conduct, ...)
    agent-memory/    Per-agent persistent memory
  researchers/       Domain reference corpora (14 papers per agent)
  sessions/          Session plans, templates (Formats A-I), framework docs
  tools/             Knowledge schema + index (librarian-maintained)
  CLAUDE.md          Project constitution
  agents.md          Agent & skill registry
```

### How it works

1. `/new-research-project` collects your domain and research question
2. Dispatches **coordinator** and **librarian** agents in parallel to scaffold infrastructure and knowledge system
3. Presents 10 agent archetypes — you pick a team (Skeptic + Calculator mandatory, Workhorses/Dreamers/etc. optional)
4. You assign persona overlays (real researchers whose intellectual DNA shapes each agent)
5. `/new-researcher` stamps each agent definition and deploys **scout** to fetch papers
6. Session 0 prompt is ready — run `/clab-team` to launch your first research session

### Agent archetypes

| Archetype | Cognitive style |
|:----------|:----------------|
| **Skeptic** | "Prove it." Demands methodology, controls, pre-registration. Owns confidence assessment. |
| **Calculator** | "Stop debating. Run it." Produces artifacts, code, data. Resolves debates by computing. |
| **Workhorse** | "I'll work through this properly." Deep domain expertise, shows every step. |
| **Principalist** | "What MUST be true?" Structural constraints, thought experiments. |
| **Dreamer** | "What if this is actually THAT?" Cross-domain pattern finder. |
| **Boundary Guard** | "Here are the limits." Hard constraints, impossibility results. |
| **Observer** | "What does the data say?" Data-driven analysis, error bars. |
| **Bridge** | "The original source says..." Source fidelity, preserves external work. |

### Skills installed in generated projects

| Skill | What it does |
|:------|:-------------|
| `/clab-team` | Launch a coordinated multi-agent session from a prompt file |
| `/clab-synthesis` | Generate synthesis/fusion documents (solo or team mode) |
| `/clab-plan` | Generate session plans and prompts from a topic |
| `/clab-review` | Multi-agent collaborative document review |
| `/new-researcher` | Create a new domain agent with web-fetched papers |
| `/weave` | Query and maintain the knowledge index |
| `/indexing` | Build structured index for a researcher folder |
| `/shortterm` | Collapse and optimize agent memory files |
| `/document-prep` | Format-aware document toolkit |
| `/team-blast` | Direct-write broadcast to team agent inboxes |
| `/redact` | Remove agent-memory references to a session or identifier |

### Session formats

Nine predefined formats with prescribed team sizes and workflows:

| Format | Type | Team |
|:-------|:-----|:-----|
| A | First Contact Review | 2-3 agents |
| B | Adversarial Debate | 2-3 agents |
| C | Collaborative Deep Dive | 2-3 agents |
| D | Workshop | 2-3 agents per round |
| E | Investigation Arc | 2-3 agents |
| F | Decisive Computation | 2-3 agents |
| G | Mass Parallel Assessment | 3 agents |
| H | Decision Gate | 2-3 agents |
| I | Formalization | 2-3 agents |

### Knowledge system

Every generated project includes a schema-driven knowledge graph:

- `tools/knowledge-schema.yaml` — Entity types (universal + domain-specific)
- `tools/knowledge-index.json` — Structured index (librarian is sole writer)
- `/weave` skill for querying and maintaining the index

The librarian agent indexes session outputs, tracks constraints, gates, proven results, data provenance, and cross-references — all without Python.

---

## Also included

**graceful-handoff** — `/grace` generates a detailed conversation summary so a new session can pick up where you left off.

**skeptic-validator** — `/validate` demands concrete evidence (test results, logs, benchmarks) that code changes are correct before accepting them.

## License

MIT
