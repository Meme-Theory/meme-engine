# researchers/{{DOMAIN}}/ — Domain Reference Corpus

<!-- DEPLOY: project-root/researchers/{{DOMAIN}}/CLAUDE.md -->
<!-- This is a TEMPLATE. One copy per domain folder, with {{DOMAIN}} replaced. -->

This folder contains the reference papers for the **{{DOMAIN}}** research domain. These papers are the primary knowledge base for agents specializing in this area.

## How to Read This Folder

### Start with `index.md`

The index file contains:
- Complete paper inventory with numbering
- Tags for each paper (methodology, topic, era)
- Dependency graph showing which papers build on others
- Recommended reading order

### Reading Levels

| Level | What | When |
|:------|:-----|:-----|
| **L0 — Skim** | Read title, abstract equivalent, key results only | First pass; building mental map |
| **L1 — Study** | Read methodology, main arguments, key equations | Preparing for a session involving this domain |
| **L2 — Internalize** | Read everything, cross-reference with other papers | Deep investigation or adversarial debate |

### Navigation Rules

1. **Always start with `index.md`** — it tells you what's here and how it connects
2. **Use paper tags** to find relevant sources for your current task
3. **Follow dependency links** to understand prerequisite knowledge
4. **Cite by paper number** (e.g., "Paper 03") when referencing in session outputs
5. **Do not modify papers** — they are reference material, not working documents

## Source Authority

These papers represent **primary sources** in the project's authority hierarchy:

```
Skeptic verdicts > synthesis files > gate results > session minutes > THESE PAPERS > general training data
```

Papers here outrank general LLM knowledge but are subordinate to project-specific computational results and Skeptic assessments.

## What Belongs Here

- Markdown summaries of key papers in the domain
- Each summary should include: authors, year, key results, methodology, relevant equations
- Papers should cover foundational works, recent advances, and methodological references

## What Does NOT Belong Here

- Session outputs or meeting minutes → `sessions/`
{{if-compute}}
- Computation results → `{{COMPUTATION_DIR}}/`
{{endif-compute}}
- Raw PDF files → `artifacts/source/{{DOMAIN}}/`
- Agent analysis or opinions → agent memory or session files

## Indexer

- The Indexer agent has directives to index the [Domain] folders into a Claude accesibly information heirarchy - focusing agent context on pertinent data.