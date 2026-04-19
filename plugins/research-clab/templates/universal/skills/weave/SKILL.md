---
name: weave
description: Query and maintain the project knowledge index
argument-hint: --update | --show <type> | --show equations [type|named] | --trace "entity" | --provenance file | --search "keyword" | --stats | --validate | --audit-constants | --graph | --timeline | --mermaid | --viz-all | --db-sync | --db-search "query"
---

# Knowledge Weave — Query the Project Index

Read, query, and maintain the structured knowledge index at `tools/knowledge-index.json`.

## Usage

```
/weave --update                    # Rebuild the index from source files
/weave --show theorems             # PROVEN theorems table
/weave --show closed                 # Closed mechanisms table
/weave --show gates                # Gate verdicts table
/weave --show trajectory           # Probability timeline
/weave --show open                 # OPEN channels table
/weave --show researchers          # Researcher cross-map
/weave --trace "CPT"               # Evidence chain for an entity
/weave --provenance s24a_vspec.npz # Script→data→gate lineage
/weave --show equations             # Equations by type (display/inline/code/etc)
/weave --search "keyword"          # Search across all entity fields
/weave --stats                     # Summary counts
/weave --validate                  # Consistency checks
/weave --graph                     # Knowledge topology PNG
/weave --timeline                  # Probability trajectory PNG
/weave --mermaid                   # Mermaid diagram to stdout
/weave --viz-all                   # All visualizations (5 PNGs + Mermaid)
/weave --db-sync                   # Rebuild SQLite database
/weave --db-search "BCS gap"       # FTS5 ranked search
/weave --db-query gates V-1        # Direct entity lookup
```

## Parse Arguments

Extract the subcommand and argument from `$ARGUMENTS`. The first token after `/weave` is the subcommand flag. Anything after it is the argument.

## Subcommand Implementations

### `--update`

Run the extraction script to rebuild the index:

```
"python" tools/extract_entities.py
```

Report the statistics output to the user.

### `--show theorems`

1. Read `tools/knowledge-index.json` using the Read tool.
2. Parse the JSON.
3. Format the `theorems` array as a markdown table:

| # | Theorem | Sessions | Precision | Source |
|:--|:--------|:---------|:----------|:-------|

Sort by session number (ascending). Show all entries.

### `--show closed`

1. Read `tools/knowledge-index.json`.
2. Format the `closed_mechanisms` array as a markdown table:

| # | Mechanism | Session | Closed By | Gate ID |
|:--|:----------|:--------|:----------|:--------|

Sort by session number.

### `--show gates`

1. Read `tools/knowledge-index.json`.
2. Format the `gates` array as a markdown table:

| Gate | Session | Condition | Result | Verdict | BF |
|:-----|:--------|:----------|:-------|:--------|:---|

Highlight CLOSED verdicts with bold. Show BF if available.

### `--show trajectory`

1. Read `tools/knowledge-index.json`.
2. Format the `probability_trajectory` array as a timeline:

```
Session  | Panel  | Sagan  | Key Event
---------|--------|--------|-----------
prior    | 2-5%   |        | Theoretical
7-8      | 10-15% |        | KO-dim=6
...
24a/24b  | 5%     | 3%     | V-1 CLOSED
```

Only show entries that have panel or sagan values (skip empty ones).

### `--show open`

1. Read `tools/knowledge-index.json`.
2. Format the `open_channels` array as a markdown table:

| Channel | Detail | Session |
|:--------|:-------|:--------|

### `--show researchers`

1. Read `tools/knowledge-index.json`.
2. Format the `researchers` array as a markdown table:

| Domain | Papers | Citations | Sessions Referenced | Description |
|:-------|:-------|:----------|:-------------------|:------------|

Sort by citation count (descending).

### `--show equations`

1. Read `tools/knowledge-index.json`.
2. Parse the `equations` array (12,000+ entries after dedup).
3. Group by `type` (display, inline, structural, code, comment).
4. For each type, show count, named count, and the first 10 examples:

```
Type: display (111 equations, 111 named)
  eq_42  | Spectral Action          | s24a_vspec.py:15        | $$V_{spec}(\tau) = a_2 R + a_4 R^2$$
  eq_43  | Seeley-DeWitt Coefficients | session-20a-synth.md:88 | $$\text{Tr}(f(D^2/\Lambda^2)) = \sum a_n$$
  ...

Type: code (8,333 equations, 81 named)
  eq_500 | BCS Gap Equation         | s23a_bcs_gap.py:42      | M_evals, M_evecs, M_max, M_matrix = linearized_bcs(...)
  ...
```

Show the `name` column when an equation has one; show `—` when `name` is null.
If the equation has an `errata` field, append ` [ERRATA]` after the raw text.

If the user specifies a type (e.g., `--show equations display`), filter to that type only and show up to 50 entries.
If the user specifies `--show equations named`, show ONLY equations that have a non-null `name`, across all types, up to 100 entries.

### `--trace "entity"`

1. Read `tools/knowledge-index.json`.
2. Search the entity name (case-insensitive) across ALL entity types: theorems, closed_mechanisms, gates, open_channels.
3. For each match:
   - Show the full entity record.
   - Read the `source_file` using the Read tool to get surrounding context (±10 lines around the entity mention).
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
   Script: s24a_vspec.py
   Session: s24a
   Inputs: [list of .npz files loaded]
   Outputs: [s24a_vspec.npz, s24a_vspec.png]
   Gates informed: [V-1, V-3]
   ```
4. If a gate is listed in `gates_informed`, also show the gate verdict from the gates array.

### `--search "keyword"`

1. Read `tools/knowledge-index.json`.
2. Search the keyword (case-insensitive) across ALL fields of ALL entity types.
3. For each match, show:
   - Entity type (theorem/closed/gate/session/open/provenance/researcher)
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

Generate the knowledge topology graph (theorems, gates, closed mechanisms, sessions as connected nodes).

```
"python" tools/visualize_knowledge.py --graph
```

Report the output path and file size to the user. Output: `tools/viz/knowledge_graph.png`.

### `--timeline`

Generate the probability trajectory chart (panel + Sagan assessments over sessions, with milestone annotations).

```
"python" tools/visualize_knowledge.py --timeline
```

Report the output path. Output: `tools/viz/probability_timeline.png`.

### `--provenance-graph`

Generate the data provenance flow graph (scripts → outputs → gates).

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

### `--gates-graph`

Generate the gate verdict visual summary table.

```
"python" tools/visualize_knowledge.py --gates
```

Report the output path. Output: `tools/viz/gate_verdicts.png`.

### `--mermaid`

Generate Mermaid flowchart code showing key theorems, gates, and closed mechanisms.

```
"python" tools/visualize_knowledge.py --mermaid
```

Show the Mermaid code to the user (it prints to stdout). Also writes `tools/viz/knowledge_graph.mmd`.

### `--viz-all`

Generate all visualizations at once (5 PNGs + 1 Mermaid file).

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

Show the full entity record.

### `--audit-constants`

Run the canonical constants audit on S34+ tier0 scripts. Flags hardcoded values that should import from `tier0-computation/canonical_constants.py`. Scans both `tier0-computation/` (active) and `tier0-archive/` (S7-S51).

```
"python" tools/extract_entities.py --audit-constants
```

Reports compliant scripts (using `from canonical_constants import ...`) and violations (stale hardcoded E_cond, Vol_SU3, M_KK). Scripts from session 33 and lower are exempt (historical). The audit also runs automatically during `--update` and `--validate`.

## Error Handling

- If `tools/knowledge-index.json` does not exist, tell the user to run `/weave --update` first.
- If a `--show` subcommand has no entries, say "No {type} entries found in the index."
- If `--trace` finds no matches, say "No matches found for '{query}'."
- If `--provenance` finds no matches, say "No provenance found for '{filename}'."

## Notes

- The index is the single source of truth. Always read it fresh — never cache.
- For `--trace`, reading the source file provides the human context that the JSON alone cannot capture. Always include the source excerpt.
- The index is generated by `tools/extract_entities.py`. If results look stale, suggest `/weave --update`.
- **Curated equation fields**: Equations may have `name` (human-readable, e.g., "Spectral Action"), `latex` (LaTeX rendering), `audit_status` (ok/typo), and `errata` (correction notes). These are manually curated and preserved across index rebuilds. Use `tools/name_equations.py` to re-apply names after a rebuild.
- **Curated entity fields**: Any entity type may have an `errata` field containing correction notes. These are preserved across rebuilds by `merge_curated_from_existing()` in `extract_entities.py`.
