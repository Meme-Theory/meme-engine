# Unfold: Knowledge Index System

**Target agent**: Librarian
**Task**: Generate the knowledge schema for the domain, create the empty index, seed your own memory with the maintenance protocol.
**Inputs**: Domain and research question (from coordinator or user). Constraint categories (from coordinator).
**Reads from**: `${CLAUDE_PLUGIN_ROOT}/KNOWLEDGE-DATABASE.md` (canonical specification), project `tools/` directory
**No Python required**: The core knowledge system is schema-driven and agent-maintained. Python tools are optional accelerators.

---

## Context

The knowledge index is the project's institutional memory — a structured, queryable graph of everything the project has established. You (the librarian) are the sole writer of this index. You maintain it by reading session artifacts and updating `knowledge-index.json` directly, guided by the knowledge schema.

Architecture:
```
sessions/*.md              ─┐
data/output/*               ─┼─▶  YOU (librarian)  ─▶  knowledge-index.json
constraint-map.md           ─┘   (read schema,           (canonical)
                                   extract entries)
                              knowledge-schema.yaml ──── (defines what to extract)
```

No extraction scripts. No regex. You read structured session artifacts and populate the index according to the schema's entity types and field definitions.

For the full specification, read `${CLAUDE_PLUGIN_ROOT}/KNOWLEDGE-DATABASE.md`.

---

## Step 1: Read the Domain Context

Before generating the schema, understand what you're working with:

1. **Read the domain** — what field is this project investigating? (e.g., "computational biology", "algebraic topology", "climate modeling")
2. **Read the research question** — what specific problem is being studied?
3. **Read the constraint categories** — the coordinator should have configured domain-specific constraint prefixes (beyond the universal S/F/D/O). If they haven't, ask.

These inputs determine which domain-specific entity types and constraint categories to add to the schema.

---

## Step 2: Generate Knowledge Schema

Write `tools/knowledge-schema.yaml`. The schema defines what knowledge types this project tracks.

### Universal Entity Types (always include these 9)

| Type | Purpose | Authority |
|:-----|:--------|:----------|
| `sessions` | Session metadata | coordinator |
| `constraints` | Established boundaries of solution space | coordinator |
| `gates` | Pre-registered pass/fail tests | skeptic |
| `proven_results` | Permanent structural results | workhorse |
| `closed_approaches` | Falsified hypotheses | coordinator |
| `active_channels` | Surviving hypotheses under investigation | coordinator |
| `confidence_trajectory` | Bayesian confidence evolution | skeptic |
| `data_provenance` | Computation lineage (script → output → gate) | librarian |
| `references` | Reference corpus inventory | librarian |

### Domain-Specific Entity Type (add at least one)

Choose the structured content type that matters most in this domain. This replaces `equations` from the origin project. Examples:

| Domain | Type | What It Captures |
|:-------|:-----|:-----------------|
| Theoretical Physics | `equations` | Named mathematical expressions with LaTeX |
| Computational Biology | `protocols` | Experimental procedures with reagents/conditions |
| Machine Learning | `experiments` | Training runs with hyperparams/metrics |
| Drug Discovery | `compounds` | Chemical entities with pharmacological data |
| Software Architecture | `components` | System components with API contracts |
| Mathematics | `conjectures` | Open problems with approach history |

Define the entity type with its fields. Every entity type needs:
- At least one `required: true` field
- A `source_file` field for provenance tracking
- An `authority` designation (which archetype produces this content)

### Constraint Categories

Include the 4 universal prefixes plus domain-specific ones from the coordinator:

| Prefix | Universal? | Example |
|:-------|:-----------|:--------|
| `S` | Yes | Structural — permanent logical constraints |
| `F` | Yes | Framework — axiom/scope constraints |
| `D` | Yes | Dynamical — evolution/stability constraints |
| `O` | Yes | Observational — external data bounds |
| `{domain}` | No | Coordinator-defined domain categories |

### Write the Schema

Use the full schema format from `${CLAUDE_PLUGIN_ROOT}/KNOWLEDGE-DATABASE.md` § 2a. Write to `tools/knowledge-schema.yaml`.

**Verification**: After writing, confirm:
- [ ] All 9 universal types present
- [ ] At least 1 domain-specific type added
- [ ] Every type has `authority` and `source_file` field
- [ ] All 4 universal constraint categories present
- [ ] Domain constraint categories included
- [ ] Source authority hierarchy defined

---

## Step 3: Create Empty Index

Generate `tools/knowledge-index.json` from the schema:

1. Read `tools/knowledge-schema.yaml`
2. Create a JSON object with:
   - `metadata` block: project name, domain, date, entity_types list, counters at 0
   - One empty array `[]` for each entity type in the schema
3. Write to `tools/knowledge-index.json`

Template:

```json
{
  "metadata": {
    "schema_version": "1.0",
    "project": "{project-name}",
    "domain": "{domain}",
    "created": "{today}",
    "last_updated": "{today}",
    "entity_types": ["sessions", "constraints", "gates", "proven_results", "closed_approaches", "active_channels", "confidence_trajectory", "data_provenance", "references"],
    "total_entities": 0,
    "sessions_indexed": 0
  },
  "sessions": [],
  "constraints": [],
  "gates": [],
  "proven_results": [],
  "closed_approaches": [],
  "active_channels": [],
  "confidence_trajectory": [],
  "data_provenance": [],
  "references": []
}
```

Add arrays for any domain-specific entity types. Ensure the `entity_types` list in metadata matches the arrays.

Create the visualization output directory: `tools/viz/`

---

## Step 4: Seed Librarian Memory

Write to `.claude/agent-memory/librarian/MEMORY.md`:

```markdown
# Librarian Memory

## Knowledge System
- Schema: `tools/knowledge-schema.yaml` (defines entity types and fields)
- Index: `tools/knowledge-index.json` (single source of truth)
- Rebuild: `/weave --update` (I read session artifacts and update the index)
- Specification: `${CLAUDE_PLUGIN_ROOT}/KNOWLEDGE-DATABASE.md` (full protocol reference)

## Entity Types
{list each entity type from the schema with a one-line description}

## Domain-Specific Types
{list any domain-specific entity types added}

## Constraint Categories
{list all constraint category prefixes with names}

## Source Authority Hierarchy
Skeptic verdicts > synthesis files > gate results > session minutes > raw data

## Maintenance Protocol
After each session:
1. Read synthesis file + gate verdicts (highest priority sources)
2. For each entity type in schema: scan for matching content
3. Populate required fields per schema
4. Update knowledge-index.json (append new, update existing by id)
5. Update metadata counters

## Rules
- I am the sole writer of knowledge-index.json
- I index what files say — I never interpret or evaluate
- I do NOT classify gate verdicts (skeptic's authority)
- I do NOT write constraint map entries (coordinator's authority)
- I preserve curated fields across rebuilds (names, notes, errata)
- When conflicts exist between sources, I follow the authority hierarchy

## Active State
- Sessions indexed: 0
- Entities: 0
- Last update: {today} (initial empty index)
```

---

## Step 5: Verify /weave Skill

The `/weave` skill should already be installed at `.claude/skills/weave/SKILL.md` (by unfold-structure). Verify:

1. The skill file exists
2. `tools/knowledge-schema.yaml` exists (just created in Step 2)
3. `tools/knowledge-index.json` exists (just created in Step 3)

The `/weave` skill reads the schema to know what entity types and fields are available. No additional configuration needed — new entity types in the schema are automatically queryable via `/weave --show {type}`.

### Optional: Install Python Accelerator

If the project expects heavy computation or will exceed ~10 sessions:

1. Check if Python is available in the project environment
2. If yes, copy the generalized accelerator tools:
   - `knowledge_db.py` — SQLite + FTS5 ranked search (reads schema for table creation)
   - `visualize_knowledge.py` — PNG/Mermaid generation (reads schema for entity types)
3. Verify with: `$PYTHON tools/knowledge_db.py --help`

If Python is not available or the project is small, skip this. The core knowledge system works without it.

---

## Step 6: Report Completion

Send a message to the coordinator confirming:

```
Knowledge index scaffold complete:
- Schema: tools/knowledge-schema.yaml ({N} entity types, {M} constraint categories)
- Index: tools/knowledge-index.json (empty, ready for first session)
- Memory: .claude/agent-memory/librarian/MEMORY.md (seeded with maintenance protocol)
- /weave skill: verified
- Python accelerator: {installed | not needed | not available}

Entity types configured:
  Universal: sessions, constraints, gates, proven_results, closed_approaches,
             active_channels, confidence_trajectory, data_provenance, references
  Domain:    {list domain-specific types}

Constraint categories: S, F, D, O, {domain categories}

Ready for first session. I will update the index after each session
by reading synthesis files and gate verdicts.
```

---

## What You Do NOT Do

- **Do NOT extract entities** — there are no session files to extract from yet
- **Do NOT interpret content** — you index, you do NOT evaluate
- **Do NOT build visualizations** — nothing to visualize yet
- **Do NOT modify the /weave skill** — it reads the schema dynamically
- **Do NOT create the SQLite database** — it's rebuilt from JSON when needed
- **Do NOT run Python scripts** — the core system doesn't need them

Your job is the knowledge scaffold: schema + empty index + seeded memory. Actual extraction happens after sessions produce content.
