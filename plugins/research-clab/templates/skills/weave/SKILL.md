---
name: weave
description: Query and maintain the project knowledge index
argument-hint: --update | --show <type> | --trace "entity" | --provenance file | --search "keyword" | --stats | --validate | --graph | --timeline | --mermaid | --viz-all | --db-sync | --db-search "query"
---

# Knowledge Weave — Query the Project Index

Read, query, and maintain the structured knowledge index at `tools/knowledge-index.json`.

## Usage

```
/weave --update                    # Rebuild the index from source files
/weave --show theorems             # Show entries of a given type
/weave --show gates                # Gate verdicts table
/weave --show trajectory           # Probability timeline
/weave --show open                 # Open questions/channels table
/weave --show researchers          # Researcher cross-map
/weave --show equations            # Equations by type
/weave --trace "entity name"       # Evidence chain for an entity
/weave --provenance script.py      # Script→data→gate lineage
/weave --search "keyword"          # Search across all entity fields
/weave --stats                     # Summary counts
/weave --validate                  # Consistency checks
/weave --graph                     # Knowledge topology PNG
/weave --timeline                  # Probability trajectory PNG
/weave --mermaid                   # Mermaid diagram to stdout
/weave --viz-all                   # All visualizations
/weave --db-sync                   # Rebuild SQLite database
/weave --db-search "query"         # FTS5 ranked search
/weave --db-query TABLE ID         # Direct entity lookup
```

## Parse Arguments

If `$ARGUMENTS` is empty or `--help`, show the Usage block above and stop.

Extract the subcommand and argument from `$ARGUMENTS`. The first token after `/weave` is the subcommand flag. Anything after it is the argument.

## Python Environment

All Python commands use the project's configured Python environment. Discover it by checking (in order):
1. `{{PYTHON_ENV}}` if set in project CLAUDE.md
2. A `.venv*/Scripts/python.exe` (Windows) or `.venv*/bin/python` (Unix) in the project root or simulation directory
3. System `python3` or `python` as fallback

Store the resolved path as `$PYTHON` for use in all commands below.

## Subcommand Implementations

### `--update`

Run the extraction script to rebuild the index:

```
$PYTHON tools/extract_entities.py
```

Report the statistics output to the user.

### `--show <type>`

1. Read `tools/knowledge-index.json` using the Read tool.
2. Parse the JSON.
3. Find the array matching `<type>` (e.g., `theorems`, `gates`, `closed_mechanisms`, `open_channels`, `probability_trajectory`, `researchers`, `equations`).
4. Format as a markdown table with columns appropriate to the entity type.
5. Sort by session number (ascending) where applicable.

**Common entity types** (projects may define additional types in their `extract_entities.py`):

| Type | Typical Columns |
|:-----|:---------------|
| `theorems` | #, Theorem, Sessions, Precision, Source |
| `gates` | Gate, Session, Condition, Result, Verdict |
| `closed` | Mechanism, Session, Closed By, Gate ID |
| `trajectory` | Session, Panel, Key Event |
| `open` | Channel, Detail, Session |
| `researchers` | Domain, Papers, Citations, Sessions, Description |
| `equations` | ID, Name, Source, Raw Text |

If a type has no entries, say "No {type} entries found in the index."

#### Equations subcommand

`/weave --show equations` groups by `type` field (display, inline, structural, code, comment). For each type, show count, named count, and the first 10 examples.

Show the `name` column when an equation has one; show `—` when `name` is null.
If the equation has an `errata` field, append ` [ERRATA]` after the raw text.

If the user specifies a subtype (e.g., `--show equations display`), filter to that type only and show up to 50 entries.
If the user specifies `--show equations named`, show ONLY equations that have a non-null `name`, across all types, up to 100 entries.

### `--trace "entity"`

1. Read `tools/knowledge-index.json`.
2. Search the entity name (case-insensitive) across ALL entity types.
3. For each match:
   - Show the full entity record.
   - Read the `source_file` using the Read tool to get surrounding context (+/-10 lines around the entity mention).
   - List related entities (same session, same gate_id, or name substring matches in other entities).
4. Format as an evidence chain showing how the entity connects to other findings.

### `--provenance <filename>`

1. Read `tools/knowledge-index.json`.
2. Search `data_provenance` for entries where:
   - `script` matches the filename, OR
   - any item in `outputs` matches the filename, OR
   - any item in `inputs` matches the filename.
3. For each match, show the full provenance chain:
   ```
   Script: compute_result.py
   Session: session-5
   Inputs: [list of data files loaded]
   Outputs: [result.npz, result.png]
   Gates informed: [G-1, G-3]
   ```
4. If a gate is listed in `gates_informed`, also show the gate verdict from the gates array.

### `--search "keyword"`

1. Read `tools/knowledge-index.json`.
2. Search the keyword (case-insensitive) across ALL fields of ALL entity types.
3. For each match, show:
   - Entity type
   - Entity name or id
   - The matching field and its value (truncated to 200 chars)
4. Group results by entity type.

### `--stats`

Run the extraction script in stats mode:

```
$PYTHON tools/extract_entities.py --stats
```

Report the output.

### `--validate`

Run the extraction script in validation mode:

```
$PYTHON tools/extract_entities.py --validate
```

Report violations (if any) or confirm consistency.

---

## Tier 2: Visualization Subcommands

These generate PNG graphs and diagrams from the knowledge index.

### `--graph`

Generate the knowledge topology graph.

```
$PYTHON tools/visualize_knowledge.py --graph
```

Report the output path and file size. Output: `tools/viz/knowledge_graph.png`.

### `--timeline`

Generate the probability trajectory chart.

```
$PYTHON tools/visualize_knowledge.py --timeline
```

Output: `tools/viz/probability_timeline.png`.

### `--provenance-graph`

Generate the data provenance flow graph (scripts -> outputs -> gates).

```
$PYTHON tools/visualize_knowledge.py --provenance
```

Output: `tools/viz/data_provenance.png`.

### `--citations-graph`

Generate the researcher domain citation network.

```
$PYTHON tools/visualize_knowledge.py --citations
```

Output: `tools/viz/researcher_citations.png`.

### `--gates-graph`

Generate the gate verdict visual summary table.

```
$PYTHON tools/visualize_knowledge.py --gates
```

Output: `tools/viz/gate_verdicts.png`.

### `--mermaid`

Generate Mermaid flowchart code showing key entities and their relationships.

```
$PYTHON tools/visualize_knowledge.py --mermaid
```

Show the Mermaid code to the user (prints to stdout). Also writes `tools/viz/knowledge_graph.mmd`.

### `--viz-all`

Generate all visualizations at once.

```
$PYTHON tools/visualize_knowledge.py --all
```

Report the summary table of all output files and sizes.

---

## Tier 3: SQLite Database Subcommands

These use a SQLite database with FTS5 full-text search for fast ranked queries.

### `--db-sync`

Rebuild the SQLite database from the JSON index.

```
$PYTHON tools/knowledge_db.py --sync
```

Report the row counts per table. Output: `tools/knowledge.db`.

### `--db-search "query"`

Run a FTS5 ranked search across all entity types.

```
$PYTHON tools/knowledge_db.py --search "QUERY"
```

Show the grouped, ranked results to the user.

### `--db-query TABLE ID`

Look up a specific entity by table name and ID.

```
$PYTHON tools/knowledge_db.py --query TABLE ID
```

Show the full entity record.

## Error Handling

- If `tools/knowledge-index.json` does not exist, tell the user to run `/weave --update` first.
- If a `--show` subcommand has no entries, say "No {type} entries found in the index."
- If `--trace` finds no matches, say "No matches found for '{query}'."
- If `--provenance` finds no matches, say "No provenance found for '{filename}'."

## Notes

- The index is the single source of truth. Always read it fresh — never cache.
- For `--trace`, reading the source file provides the human context that the JSON alone cannot capture. Always include the source excerpt.
- The index is generated by `tools/extract_entities.py`. If results look stale, suggest `/weave --update`.
- **Curated fields**: Entities may have `name`, `errata`, `audit_status`, or `latex` fields that are manually curated and preserved across index rebuilds. These are merged back by the extraction script's `merge_curated_from_existing()` function.
- **Entity types are project-configured**: The types listed above (theorems, gates, etc.) are defaults. Projects may define additional entity types in their `extract_entities.py` configuration. The `--show` command should handle any type present in the JSON, not just the ones listed here.
