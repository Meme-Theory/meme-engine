# artifacts/ — Source Materials

<!-- DEPLOY: project-root/artifacts/CLAUDE.md -->

This directory contains primary source materials — the original PDFs, documents, and references that the project draws from. These are the raw inputs that get processed into the markdown summaries in `researchers/`.

## Structure

```
artifacts/
├── papers/                     # Markdown paper summaries (legacy/overflow)
│   └── NN_Author_Title_YYYY.md
├── source/                     # Primary source files organized by domain
│   ├── <domain-A>/             # PDFs and documents for domain A
│   ├── <domain-B>/             # PDFs and documents for domain B
│   └── papers_pdfs/            # Unsorted PDF collection
└── <other-artifacts>/          # Domain-specific materials (optional)
```

## What Belongs Here

- **Original PDFs** — the actual papers, not summaries
- **Primary source documents** — raw reference materials in any format
- **Archival copies** — materials that might disappear from the web
- **Domain-organized collections** — one subdirectory per research domain under `source/`

## What Does NOT Belong Here

- **Markdown paper summaries** → `researchers/<domain>/` (the curated, agent-readable versions)
- **Session outputs** → `sessions/`
{{if-compute}}
- **Computation results** → `{{COMPUTATION_DIR}}/`
{{endif-compute}}
- **Agent definitions or memory** → `.claude/`

## Relationship to researchers/

```
artifacts/source/<domain>/paper.pdf  ──(summarized by /new-researcher)──▶  researchers/<domain>/NN_YYYY_Author_Title.md
```

The `artifacts/` directory holds the RAW sources. The `researchers/` directory holds the PROCESSED, agent-readable summaries. Agents read from `researchers/`, not from `artifacts/`.

## Rules

- **Read-only for agents** — agents do not write to this directory
- **Organize by domain** — mirror the `researchers/` domain structure under `source/`
- **No processing here** — this is storage, not a workspace
- **Large files are expected** — PDFs, datasets, and documents can be large; this is their home
