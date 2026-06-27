---
name: weave
description: Query and maintain the project knowledge index
argument-hint: --update | --show <type> | --trace "entity" | --provenance file | --search "keyword" | --stats | --validate | --graph | --mermaid | --viz-all | --db-sync | --db-search "query" | --db-query <table> <id>
---

# Knowledge Weave -- Query the Project Index

Read, query, and maintain the structured knowledge index at `tools/knowledge-index.json`.

The index is schema-driven: the entity types it holds are defined by `tools/knowledge-schema.yaml`. Every project carries the UNIVERSAL types -- `sessions`, `researchers`, `results`, `references`, `open_questions` (plus `data_provenance`). A discipline pack may add more types (the physics pack, for example, adds `theorems`, `closed_mechanisms`, `gates`, `constants`, `trajectory`, `equations`). The `--show <type>` and visualization subcommands work for whatever types your schema defines; see "Discipline Extensions" at the end for subcommands that apply only when the matching types are present.

## Usage

```
/weave --update                    # Rebuild the index from source files
/weave --show sessions             # Sessions table
/weave --show results              # Results table
/weave --show references           # Cited references table
/weave --show open                 # Open questions table
/weave --show researchers          # Researcher cross-map
/weave --trace "entity"            # Evidence chain for an entity
/weave --provenance s12_sweep.npz  # Script->data->result lineage
/weave --search "keyword"          # Search across all entity fields
/weave --stats                     # Summary counts
/weave --validate                  # Consistency checks
/weave --graph                     # Knowledge topology PNG
/weave --mermaid                   # Mermaid diagram to stdout
/weave --viz-all                   # All available visualizations
/weave --db-sync                   # Rebuild SQLite database
/weave --db-search "convergence"   # FTS5 ranked search
/weave --db-query results R-1      # Direct entity lookup
```

Discipline-specific subcommands (`--show theorems`, `--show equations`, `--show trajectory`, `--timeline`, `--gates-graph`, `--audit-constants`, ...) are documented under "Discipline Extensions" -- they appear only when your schema/pack defines the matching types.

## Parse Arguments

Extract the subcommand and argument from `$ARGUMENTS`. The first token after `/weave` is the subcommand flag. Anything after it is the argument.

## Subcommand Implementations

### `--update`

Run the extraction script to rebuild the index:

```
"python" tools/extract_entities.py
```

Report the statistics output to the user.

### `--show <type>`

`--show` formats one entity type from the index as a markdown table. Read `tools/knowledge-index.json`, parse the JSON, select the array for the requested type, and render it. Sort sensibly (by session number ascending, or by the most relevant ranking column). Show all entries. The universal types are below; discipline packs add more (see Discipline Extensions).

**`--show sessions`**

| Session | Date | Type | Focus | Key Outcome |
|:--------|:-----|:-----|:------|:------------|

Sort by session number (ascending).

**`--show results`**

| # | Result | Session | Status | Source |
|:--|:-------|:--------|:-------|:-------|

`Status` is one of PROVEN / PRELIMINARY / FALSIFIED. Sort by session number. Bold PROVEN rows.

**`--show references`**

| Ref | Title | Authors | Year | Cited In |
|:----|:------|:--------|:-----|:---------|

Sort by year (descending), or by citation count if present.

**`--show open`** (open questions)

| Question | Detail | Session |
|:---------|:-------|:--------|

**`--show researchers`**

| Domain | Papers | Citations | Sessions Referenced | Description |
|:-------|:-------|:----------|:-------------------|:------------|

Sort by citation count (descending).

### `--trace "entity"`

1. Read `tools/knowledge-index.json`.
2. Search the entity name (case-insensitive) across ALL entity types present in the schema (sessions, results, references, open_questions, researchers, and any discipline types).
3. For each match:
   - Show the full entity record.
   - Read the `source_file` using the Read tool to get surrounding context (+/-10 lines around the entity mention).
   - List related entities (same session, shared id, or name substring matches in other entities).
4. Format as an evidence chain showing how the entity connects to other findings.

Example: `/weave --trace "baseline metric"`.

### `--provenance <filename>`

1. Read `tools/knowledge-index.json`.
2. Search `data_provenance` for entries where:
   - `script` matches the filename, OR
   - any item in `outputs` matches the filename, OR
   - any item in `inputs` matches the filename.
3. For each match, show the full provenance chain:
   ```
   Script: s12_sweep.py
   Session: s12
   Inputs: [list of input files loaded]
   Outputs: [s12_sweep.npz, s12_sweep.png]
   Results informed: [R-3]
   ```
4. If a result (or, in packs that define them, a gate) is listed in the `informed` field, also show that entity's record.

### `--search "keyword"`

1. Read `tools/knowledge-index.json`.
2. Search the keyword (case-insensitive) across ALL fields of ALL entity types.
3. For each match, show:
   - Entity type (session / result / reference / open_question / researcher / provenance, plus any discipline type)
   - Entity name or id
   - The matching field and its value (truncated to 200 chars)
4. Group results by entity type.

### `--stats`

Run the extraction script in stats mode:

```
"python" tools/extract_entities.py --stats
```

Report the output.

### `--validate`

Run the extraction script in validation mode:

```
"python" tools/extract_entities.py --validate
```

Report violations (if any) or confirm consistency.

---

## Tier 2: Visualization Subcommands

These generate PNG graphs and diagrams from the knowledge index.

### `--graph`

Generate the knowledge topology graph (results, sessions, references, and any discipline entities as connected nodes).

```
"python" tools/visualize_knowledge.py --graph
```

Report the output path and file size to the user. Output: `tools/viz/knowledge_graph.png`.

### `--provenance-graph`

Generate the data provenance flow graph (scripts -> outputs -> results).

```
"python" tools/visualize_knowledge.py --provenance
```

Report the output path. Output: `tools/viz/data_provenance.png`.

### `--citations-graph`

Generate the researcher domain citation network.

```
"python" tools/visualize_knowledge.py --citations
```

Report the output path. Output: `tools/viz/researcher_citations.png`.

### `--mermaid`

Generate Mermaid flowchart code showing key results and their connections.

```
"python" tools/visualize_knowledge.py --mermaid
```

Show the Mermaid code to the user (it prints to stdout). Also writes `tools/viz/knowledge_graph.mmd`.

### `--viz-all`

Generate all available visualizations at once.

```
"python" tools/visualize_knowledge.py --all
```

Report the summary table of all output files and sizes.

---

## Tier 3: SQLite Database Subcommands

These use a SQLite database with FTS5 full-text search for fast ranked queries.

### `--db-sync`

Rebuild the SQLite database from the JSON index.

```
"python" tools/knowledge_db.py --sync
```

Report the row counts per table. Output: `tools/knowledge.db`.

### `--db-search "query"`

Run a FTS5 ranked search across all entity types. Extract the search query from `$ARGUMENTS` (everything after `--db-search`).

```
"python" tools/knowledge_db.py --search "QUERY"
```

Show the grouped, ranked results to the user.

### `--db-query TABLE ID`

Look up a specific entity by table name and ID.

```
"python" tools/knowledge_db.py --query TABLE ID
```

Show the full entity record. Example: `/weave --db-query results R-1`.

---

## Discipline Extensions (present when your schema/pack defines these types)

A discipline pack can add entity types to `tools/knowledge-schema.yaml`. When those types exist, the subcommands below become available -- they share the same mechanics as the universal `--show` and visualization commands above, applied to the pack's types. If your schema does not define a type, its subcommand simply reports no entries. The examples here use the physics pack's types (`theorems`, `closed_mechanisms`, `gates`, `trajectory`, `equations`, `constants`); substitute your own pack's types as appropriate.

### `--show theorems`

Format the `theorems` array as a markdown table:

| # | Theorem | Sessions | Precision | Source |
|:--|:--------|:---------|:----------|:-------|

Sort by session number (ascending).

### `--show closed`

Format the `closed_mechanisms` array:

| # | Mechanism | Session | Closed By | Gate ID |
|:--|:----------|:--------|:----------|:--------|

Sort by session number.

### `--show gates`

Format the `gates` array:

| Gate | Session | Condition | Result | Verdict | BF |
|:-----|:--------|:----------|:-------|:--------|:---|

Highlight CLOSED verdicts in bold. Show the Bayes Factor (BF) if available.

### `--show trajectory`

If your schema defines a `trajectory` type (a confidence/probability timeline), format it:

```
Session  | Panel  | Skeptic | Key Event
---------|--------|---------|-----------
prior    | 2-5%   |         | Initial estimate
7-8      | 10-15% |         | First positive result
...
19       | 5%     | 3%      | R-1 resolved
```

Only show entries that have at least one assessor value (skip empty ones). The columns are the assessors your pack tracks (e.g., a collective "Panel" estimate plus the Skeptic's).

### `--show equations`

If your schema defines an `equations` type, parse the `equations` array, group by `type` (display, inline, structural, code, comment), and for each type show count, named count, and the first 10 examples:

```
Type: display (N equations, N named)
  eq_42  | <named identity>    | <source>:15  | $$ ... $$
  ...

Type: code (N equations, N named)
  eq_500 | <named expression>  | <source>:42  | <code line>
  ...
```

Show the `name` column when an equation has one; show `--` when `name` is null. If the equation has an `errata` field, append ` [ERRATA]` after the raw text.

If the user specifies a type (e.g., `--show equations display`), filter to that type only and show up to 50 entries. If the user specifies `--show equations named`, show ONLY equations that have a non-null `name`, across all types, up to 100 entries.

### `--timeline` (visualization)

Generate the confidence/probability trajectory chart (per-assessor estimates over sessions, with milestone annotations). Requires a `trajectory` type.

```
"python" tools/visualize_knowledge.py --timeline
```

Report the output path. Output: `tools/viz/probability_timeline.png`.

### `--gates-graph` (visualization)

Generate the gate verdict visual summary table. Requires a `gates` type.

```
"python" tools/visualize_knowledge.py --gates
```

Report the output path. Output: `tools/viz/gate_verdicts.png`.

### `--audit-constants`

If your discipline pack defines a constants module (e.g., `{{COMPUTATION_DIR}}/constants.py`), audit computation scripts for hardcoded values that should import from it instead.

```
"python" tools/extract_entities.py --audit-constants
```

Reports compliant scripts (those importing from the constants module) and violations (stale hardcoded constants). Scripts below a configured baseline session can be marked exempt (historical). The audit also runs automatically during `--update` and `--validate` when a constants module is configured.

`--trace`, `--search`, and `--db-query` already scan every type in the schema, so pack-specific types are included in their results with no extra flags.

## Error Handling

- If `tools/knowledge-index.json` does not exist, tell the user to run `/weave --update` first.
- If a `--show` subcommand has no entries (including when the type is not defined in the schema), say "No {type} entries found in the index."
- If `--trace` finds no matches, say "No matches found for '{query}'."
- If `--provenance` finds no matches, say "No provenance found for '{filename}'."

## Notes

- The index is the single source of truth. Always read it fresh -- never cache.
- For `--trace`, reading the source file provides the human context that the JSON alone cannot capture. Always include the source excerpt.
- The index is generated by `tools/extract_entities.py`. If results look stale, suggest `/weave --update`.
- **Curated entity fields**: Any entity type may have an `errata` field containing correction notes. These are preserved across rebuilds by `merge_curated_from_existing()` in `extract_entities.py`.
- **Discipline-pack curated fields**: packs that define richer types may add their own curated fields (for example, the physics pack's equations carry `name`, `latex`, `audit_status`, and `errata`, re-applied after a rebuild via `tools/name_equations.py`). These live with the pack, not the universal core.
