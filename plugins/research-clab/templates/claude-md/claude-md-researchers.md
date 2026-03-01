# researchers/ — Reference Corpora

<!-- DEPLOY: project-root/researchers/CLAUDE.md -->

This directory contains the reference knowledge base for the project. Each subdirectory holds the papers, sources, and summaries that ground a specific research domain.

## Structure

```
researchers/
├── {{DOMAIN_A}}/
│   ├── index.md                    # Paper inventory with tags and dependencies
│   ├── agents.md                   # Reading guidance for agents
│   ├── 01_YYYY_Author_Title.md     # Paper summary (markdown)
│   ├── 02_YYYY_Author_Title.md
│   └── ...                         # 10-14 papers per domain
├── {{DOMAIN_B}}/
│   └── ...
└── ...
```

## What This Directory Is

- **The project's primary knowledge base** — agents read these papers to ground their analysis
- **Curated summaries, not raw PDFs** — each paper is a markdown summary with key results, methodology, and equations
- **Organized by research domain** — one folder per domain, each corresponding to one or more agent specializations

## What This Directory Is NOT

- **Not a dump for session outputs** — those go in `sessions/`
- **Not for computation results** — those go in `{{COMPUTATION_DIR}}/`
- **Not for original source PDFs** — those go in `artifacts/source/`

## Paper Naming Convention

```
NN_YYYY_Author_ShortTitle.md
```

- `NN` — Zero-padded index (01, 02, ... 14)
- `YYYY` — Publication year
- `Author` — Primary author surname
- `ShortTitle` — Descriptive title (underscores for spaces)

**Examples**:
- `01_1921_Kaluza_Unified_Field_Theory.md`
- `07_2006_Connes_Noncommutative_Geometry_SM.md`

## Adding New Domains

Use `/new-researcher` to populate a new domain folder:

1. The skill searches the web for key papers in the domain
2. Generates markdown summaries for each paper
3. Creates `index.md` with inventory and dependency graph
4. Creates `agents.md` with standard reading guidance

After population, create the corresponding agent definition at `.claude/agents/{domain-agent}.md`.

## Rules

- **Every domain folder must have `index.md`** — the paper inventory
- **Every domain folder must have `agents.md`** — reading guidance for agents entering this folder
- **10-14 papers per domain** — enough depth without overwhelming context
- **Papers are reference material** — agents cite them, they don't modify them
- **Source authority**: The papers here are primary sources. Agent analysis is secondary.
