# tools/ — Knowledge Index Infrastructure

<!-- DEPLOY: project-root/tools/CLAUDE.md -->

This directory contains the knowledge index pipeline — the scripts, data, and outputs that transform session results into a structured, queryable knowledge graph.

## Structure

```
tools/
├── extract_entities.py         # Entity extractor (sessions → JSON)
├── knowledge_db.py             # SQLite + FTS5 query accelerator
├── visualize_knowledge.py      # PNG/Mermaid visualization generator
├── knowledge-index.json        # Canonical knowledge graph (GENERATED)
├── knowledge.db                # SQLite cache (REBUILT from JSON)
└── viz/                        # Generated visualizations
    ├── knowledge_graph.png
    ├── probability_timeline.png
    ├── data_provenance.png
    ├── gate_verdicts.png
    └── knowledge_graph.mmd     # Mermaid source
```

## The Knowledge Pipeline

```
sessions/*.md              ─┐
{{COMPUTATION_DIR}}/*.py   ─┼─▶ extract_entities.py ─▶ knowledge-index.json
{{COMPUTATION_DIR}}/*.txt  ─┘         │                       │
                                      ├── visualize_knowledge.py ─▶ viz/*.png
                                      └── knowledge_db.py ─▶ knowledge.db
```

## The Single Source of Truth

**`knowledge-index.json` is the canonical knowledge graph.** Everything else is derived from it.

- SQLite (`knowledge.db`) is a **query accelerator** — rebuilt via `/weave --db-sync`
- Visualizations in `viz/` are **generated outputs** — rebuilt via `/weave --viz-all`
- Neither the database nor the visualizations are authoritative

## Entity Types

The index tracks {{ENTITY_TYPE_COUNT}} entity types. Adapt to your domain:

| Entity Type | Purpose | Example |
|:------------|:--------|:--------|
| `theorems` | Proven structural results | "{{EXAMPLE_THEOREM}}" |
| `closed_mechanisms` | Falsified hypotheses | "{{EXAMPLE_CLOSED}}" |
| `gates` | Pre-registered pass/fail tests | "{{EXAMPLE_GATE}}" |
| `probability_trajectory` | Confidence evolution | Skeptic assessments over time |
| `sessions` | Session metadata | Date, format, agents, key results |
| `data_provenance` | Computational lineage | Script → output → gate chain |
| `open_channels` | Surviving hypotheses | Active investigation threads |
| `researchers` | Reference corpus inventory | Paper counts, domains |
| `equations` | Domain-specific structured content | Named equations, formulas |

## Who Writes What

| Actor | Can Do |
|:------|:-------|
| `knowledge-weaver` agent | **Sole writer** of `knowledge-index.json` |
| `/weave --update` command | Triggers the knowledge-weaver to rebuild |
| `extract_entities.py` | Produces the raw extraction (weaver validates) |
| Everyone else | **Read only** — query via `/weave` |

## Source Authority Hierarchy

When sources conflict:

1. **Skeptic verdicts** (highest authority)
2. **Synthesis files**
3. **Gate verdict results**
4. **Session minutes**
5. **Raw computation output** (lowest authority)

## Rules

- **Never hand-edit `knowledge-index.json`** — always use `/weave --update`
- **Never treat `knowledge.db` as source of truth** — it's a cache
- **Run `/weave --update` after editing session files** — the hook in `settings.local.json` reminds you
- **Entity extraction regex is domain-configurable** — adapt patterns in `extract_entities.py` for your domain
- **Visualizations are disposable** — regenerate with `/weave --viz-all`
