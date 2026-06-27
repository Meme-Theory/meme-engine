# Unfold: Discipline Pack Overlay

**Target agent**: Coordinator
**Task**: Overlay a selected discipline pack on top of the universal harness.
**Inputs**: `{discipline-root}` (absolute path to `templates/disciplines/{name}/`), the universal harness already installed by Phase 3a.
**Reads from**: `{discipline-root}/discipline.json` and the pack's subdirectories.
**Skipped if**: the user selected "None — generic research harness" (`discipline == "none"`).

---

## Context

A discipline pack is a plug-and-play overlay. The universal harness installs first (Phase 3a in the coordinator's scaffolding directives); this overlay step layers domain-specific rules, MCPs, knowledge-schema, CLAUDE.md fragments, and agent-flavoring on top.

See `templates/disciplines/README.md` for the pack format.

---

## Step 1: Read and Validate the Manifest

### 1a. Parse

Read `{discipline-root}/discipline.json`. Parse these fields (all optional except `name` and `schema-version`):

- `schema-version` — must equal `"1.0"` for the current overlay spec. If higher, abort with "pack requires newer plugin." If lower or missing, abort with "pack manifest predates discipline.json v1.0 — update the pack."
- `name` — must match the directory name
- `rules[]` — additional rule files to copy to `.claude/rules/`
- `rule-overrides{}` — map of universal-rule-filename → pack-filename that REPLACES the universal version
- `mcps[]` — MCP names to add to the selectable menu in unfold-mcp.md
- `skills[]` — discipline-specific skill directories to copy to `.claude/skills/`
- `knowledge-schema` — path (relative to pack root) to discipline-specific `knowledge-schema.yaml`; merged into universal schema
- `claude-md-fragments{}` — map of slot-name → pack-filename for text blocks injected into universal CLAUDE.md templates
- `agent-flavoring` — directory of per-archetype flavor notes; installed to project-local `.claude/templates/agent-flavoring/`
- `directories[]` — additional project-relative directories the pack expects to exist (e.g., `sessions/framework/theorems`, `artifacts/formal`). Created in Step 2b with `.gitkeep` files.
- `python-env{}` — paths (relative to pack root) to additions files that extend the universal `requirements-mcp.txt` / `requirements-compute.txt`. Consumed by `unfold-python-env.md` Step 2c; this overlay doc only validates that the referenced files exist.
- `vocabulary{}` — concept-name overrides for display/docs (not enforcement)

### 1b. Pre-flight all file references (do this BEFORE any mutation)

Before Steps 2-10 touch any file, resolve every reference in `discipline.json` against the filesystem:

```
For each filename in rules[]:             verify `{discipline-root}/rules/{filename}` exists and is non-empty
For each (target, source) in rule-overrides{}:  verify `{discipline-root}/rules/{source}` exists and is non-empty
For each mcp in mcps[]:                   verify `{discipline-root}/mcps/{mcp}/` exists and contains mcp-json-fragment.json
For each skill in skills[]:               verify `{discipline-root}/skills/{skill}/` exists and contains SKILL.md or skill.md
If knowledge-schema is set:               verify `{discipline-root}/{knowledge-schema}` exists and is non-empty
For each (slot, source) in claude-md-fragments{}:  verify `{discipline-root}/claude-md-fragments/{source}` exists and is non-empty
If agent-flavoring is set:                verify `{discipline-root}/{agent-flavoring}/` exists and contains at least one .md file
For each path in directories[]:           verify the path is project-relative (no `..`, no absolute prefix, no leading `/`)
For each (key, source) in python-env{}:  verify `{discipline-root}/{source}` exists and is non-empty (keys must be in {"mcp-additions", "compute-additions"})
```

Collect ALL missing references. If any are missing, abort with a single error listing every gap. Do NOT proceed to Step 2 with partial state — the overlay's mutations are not individually reversible, so a mid-execution failure leaves the project in a broken-but-partially-applied state.

Only if every reference resolves does the overlay continue to Step 2.

---

## Step 2: Install Additional Rules

For each file in `rules[]`:

```
{discipline-root}/rules/{filename}.md  →  .claude/rules/{filename}.md
```

These are ADDITIVE — they do not replace universal rules.

---

## Step 2b: Create Pack Directories

If `directories[]` is set, create each listed path (relative to `{target-dir}`) with `mkdir -p`, then write an empty `.gitkeep` into each so the directory survives `git clone` until real content lands. This is how a pack declares "my fragments will reference these paths; ensure they exist."

```
For path in directories[]:
  mkdir -p {target-dir}/{path}
  touch {target-dir}/{path}/.gitkeep
```

Skip any path that already exists with content (another pack, or an earlier scaffold step, may have created it). Do NOT fail if the directory already exists — idempotent create.

Example (math pack):
- `sessions/framework/theorems/` — referenced by `proof-standards-block.md` as the consolidated theorem archive.
- `artifacts/formal/` — referenced by `proof-standards-block.md` and `computation-environment-block.md` as the home for Lean/Coq artifacts.

---

## Step 3: Apply Rule Overrides

For each entry in `rule-overrides{}`:

```
# If universal rule already installed at .claude/rules/{universal-filename},
# OVERWRITE it with the pack's replacement.
{discipline-root}/rules/{pack-filename}  →  .claude/rules/{universal-filename}
```

Rule overrides replace the universal file at the target path; the target filename stays the same (so rule-loading paths don't change).

---

## Step 4: Register Discipline MCPs

The MCP menu is presented by `unfold-mcp.md` (Phase 7b typically). This step does NOT install MCPs directly — it registers the discipline's MCP directory so `unfold-mcp.md` scans both:

- `{plugin-root}/templates/universal/mcps/` (always scanned)
- `{discipline-root}/mcps/` (scanned when discipline is selected)

If the coordinator is executing overlay BEFORE unfold-mcp runs, record the discipline-mcps path in `sessions/framework/discipline-manifest.md` (Step 8 below) so unfold-mcp can find it.

---

## Step 5: Merge Knowledge Schema

By the time this step runs, the universal baseline schema is already at `tools/knowledge-schema.yaml` (coordinator Phase 3a installs it).

If `knowledge-schema` is set in the pack manifest, MERGE — do not replace.

### Concrete Merge Algorithm (no yq required)

Both universal and pack schemas follow a fixed top-level shape: `version`, `description`, `entity_types`, optional `authority_order`. The merge is a line-oriented splice, not a general YAML operation. Execute these steps exactly:

**Step 5.1 — Read both files**

```
A = contents of tools/knowledge-schema.yaml           (universal baseline, already installed)
B = contents of {discipline-root}/{knowledge-schema}  (pack's schema)
```

Use the Read tool for each.

**Step 5.2 — Extract pack sections**

Parse B line-by-line to extract four regions. A section begins at a line matching `^<key>:` (at column 0) and ends at the next column-0 key or EOF.

```
B.version_line       = the single line "version: ..." (empty if absent)
B.description_block  = lines from "description:" through end of its multi-line block (YAML `>` folded or direct string)
B.entity_types_body  = all lines INSIDE the `entity_types:` block (indented under it), WITHOUT the "entity_types:" header line itself
B.authority_body     = all lines INSIDE "authority_order:" block, WITHOUT the header (empty if absent)
```

**Step 5.3 — Build merged output as a new string M**

Start from A, mutate region-by-region:

1. **Replace version line**. If `B.version_line` is non-empty: find A's `^version:` line and replace it with `B.version_line`. If A has no version line, insert `B.version_line` at the top of M.

2. **Replace description**. If `B.description_block` is non-empty: find A's `^description:` block (header + body) and replace the entire block with `B.description_block`. Append a trailing comment line: `# (merged from universal + pack description)` so the concatenation is visible.

3. **Append pack entity_types**. Find A's `entity_types:` section. Locate the LAST line of A's `entity_types:` body (the last indented line before the next column-0 key or EOF). Insert `B.entity_types_body` immediately AFTER that line, preserving exact indentation (both files must use 2-space indent; verify this before inserting).

4. **Replace authority_order**. If `B.authority_body` is non-empty: find A's `^authority_order:` block and replace its body with `B.authority_body`. If A has no `authority_order:` section, append the whole `authority_order:` header + `B.authority_body` at the end of M.

**Step 5.4 — Write the merged result**

```
Write(path="tools/knowledge-schema.yaml", content=M)
```

**Step 5.5 — Verify**

Three checks:

1. **Exactly one `entity_types:` header**:
   ```
   grep -c "^entity_types:" tools/knowledge-schema.yaml   # must return 1
   ```

2. **Exactly one `version:` line**:
   ```
   grep -c "^version:" tools/knowledge-schema.yaml        # must return 1
   ```

3. **Entity-type count matches expectation**. Naïve `grep "^  [a-zA-Z_]*:"` counts ALL 2-space-indented keys, which includes nested `authority:`, `fields:`, `description:` etc. — wrong. Instead, extract the `entity_types:` block and count only its direct children:

   ```bash
   # Extract lines between "^entity_types:" and the next column-0 key (or EOF)
   awk '/^entity_types:/{flag=1; next} /^[a-zA-Z]/{flag=0} flag' tools/knowledge-schema.yaml \
     | grep -c "^  [a-zA-Z_][a-zA-Z0-9_]*:"
   # must equal (universal_entity_count) + (pack_entity_count) - (overrides_count)
   ```

   For the universal (5 types) + math (6 types, 0 overrides) case, expect 11. For universal + physics (6 types, 0 overrides) expect 11.

If any check fails, abort and report — the merge went wrong. Leave `tools/knowledge-schema.yaml` in place for debugging (don't revert to universal-only) but do not proceed to Step 6.

### Handling same-name type collisions (override semantics)

If the pack's `entity_types` contains a key that universal also has (e.g., pack redefines `results`):

1. Before Step 5.3.3, detect the collision by scanning the keys in `B.entity_types_body` (column-2 keys) against the keys already present in A's `entity_types:` block.
2. For each colliding key: in A's entity_types section, remove universal's definition of that key (the column-2 key line + all its indented children). Log the removal in the manifest at Step 9 under "Rules/schema overridden by pack."
3. Then proceed with Step 5.3.3 — the append adds the pack's definition cleanly.

### Why merge not replace

Earlier revisions replaced the universal schema entirely, which silently dropped the 5 universal types — breaking `/weave --show sessions`, `/weave --show researchers`, etc. Merge keeps the universal spine intact while letting packs specialize.

### Pack authoring constraint

Pack schemas MUST use the same top-level shape (`version`, `description`, `entity_types`, optional `authority_order`) and the same 2-space indent as the universal schema. The line-oriented merge depends on this. Don't get creative with YAML features (aliases, anchors, flow-style dicts) — they break the splice.

---

## Step 6: Inject CLAUDE.md Fragments (authoritative strip-and-inject)

This step is the single authoritative definition of the fragment-slot resolution pass. Coordinator Phase 3d and `unfold-structure.md` Step 2 defer to this section.

### Context

Universal CLAUDE.md templates contain `{{fragment-slot:NAME}}` markers where discipline packs can inject text. The markers currently defined on universal templates:

- `{{fragment-slot:reference-data}}` — for "canonical constants" or equivalent domain reference data
- `{{fragment-slot:computation-environment}}` — for hardware/venv/compute-stack specifics
- `{{fragment-slot:knowledge-query-discipline}}` — for "query X before computing" blocks

Packs may reference any subset of these slots via `claude-md-fragments{}` in their manifest.

### Algorithm (runs unconditionally at coordinator Phase 3c+3d)

For every CLAUDE.md installed in Phase 3b (root plus any subdirectory CLAUDE.md with slot markers):

1. **Inject** — for each entry `slot-name → pack-filename` in `claude-md-fragments{}`:
   a. Read `{discipline-root}/claude-md-fragments/{pack-filename}`
   b. Find the literal string `{{fragment-slot:{slot-name}}}` in the target CLAUDE.md
   c. If found: replace the marker (entire line if the marker is alone on a line, otherwise just the marker token) with the fragment content. Preserve indentation and surrounding whitespace.
   d. If not found: log a warning in the discipline manifest (Step 9) — the pack declared a fragment for a slot that doesn't exist in any installed CLAUDE.md. The fragment is dropped.

2. **Strip unresolved** — after all pack injections complete, scan every installed CLAUDE.md for remaining `{{fragment-slot:*}}` markers. Replace each unresolved marker with an empty string (delete the whole line if the marker was the only content on that line; trim the marker inline otherwise).

3. **Verify** — run `grep -rn "{{fragment-slot:" {target-dir}/CLAUDE.md {target-dir}/.claude/` across the installed tree. Zero matches is the gate; any non-zero result means Step 2 missed an instance. Abort with the matching path and line.

### When this runs

- With a selected discipline pack: injection runs for each pack fragment, then strip runs for anything unresolved.
- With `discipline == "none"`: injection is a no-op (no `claude-md-fragments{}` map exists), and strip is the whole pass. Every slot marker resolves to empty string.

Either way, the post-scaffold CLAUDE.md files contain no literal `{{fragment-slot:*}}` text.

### Fragment slots inside conditional blocks

A fragment slot MAY appear inside a `{{if-compute}}...{{endif-compute}}` conditional block (the universal `claude-md-root.md` has `{{fragment-slot:computation-environment}}` inside the compute conditional). Interaction rules:

- **Q5=Yes (conditional block survives)**: the slot is preserved through Phase 3b, and overlay Step 6 injects normally. Works as expected.
- **Q5=No (conditional block stripped)**: the slot is deleted along with its enclosing block during Phase 3b — BEFORE overlay runs. Step 6's injection step for this slot finds no marker in the file. Per the missing-slot rule above: log a warning in the manifest ("pack declared `{slot}` fragment but the slot was stripped by Q5=No — fragment dropped") and move on. This is not a bug; it's graceful degradation.

**Pack-authoring implication**: if your pack targets slots inside conditional blocks, document which Q5 answer makes them active. If Q5=No and the user picked your pack, the compute-bound fragments are silently dropped — the pack's other fragments (for unconditional slots) still apply.

---

## Step 7: Install Discipline Skills

For each entry in `skills[]`:

```
{discipline-root}/skills/{skill-name}/  →  .claude/skills/{skill-name}/
```

Copy the entire skill directory. These install alongside the universal skills already in place; no conflicts expected because discipline-specific skill names should not collide with universal skill names.

If a collision occurs (same skill name in both universal and discipline), the discipline version wins. Log the override in the manifest (Step 9).

---

## Step 8: Install Agent Flavoring

If `agent-flavoring` is set, COPY the pack's flavoring directory into the project. Do NOT leave it as an external path reference — if the plugin gets uninstalled or the project moves machines, lazy-path references would break `/new-researcher`. Self-containment matters.

### Algorithm

1. Resolve source: `{discipline-root}/{agent-flavoring}` (e.g., `{discipline-root}/agent-flavoring/`).
2. Create target: `.claude/templates/agent-flavoring/` (project-local).
3. Copy each file:
   ```
   {discipline-root}/agent-flavoring/*.md  →  .claude/templates/agent-flavoring/
   ```
4. Record the LOCAL path (`.claude/templates/agent-flavoring/`) in the discipline manifest at Step 9. `/new-researcher` reads the local copy, not the plugin path.

### Composition at agent-creation time

When `/new-researcher --archetype <archetype>` runs post-scaffold:
1. Reads universal archetype from `.claude/templates/agent-templates/{archetype}.md`
2. Reads discipline flavor from `.claude/templates/agent-flavoring/{archetype}.md` (if present)
3. Layers flavor on top of archetype
4. Applies persona/domain overlay

Missing flavor files are skipped silently — an archetype with no pack flavoring uses the universal template unchanged.

---

## Step 9: Write Discipline Manifest

Write `sessions/framework/discipline-manifest.md`:

```markdown
# Discipline Pack Applied

- **Pack**: {discipline-name} ({display-name})
- **Applied on**: {scaffold-date}
- **Source**: `{discipline-root}`

## Rules Added
- {list from rules[]}

## Rules Overridden
- {list from rule-overrides{}}

## MCPs Available (in addition to universal)
- Scan path: `{discipline-root}/mcps/`
- {list from mcps[]}

## Knowledge Schema
- Source: `{discipline-root}/{knowledge-schema}`
- Installed to: `tools/knowledge-schema.yaml`

## CLAUDE.md Fragments Injected
- {list of slot→fragment pairings}

## Agent Flavoring
- Source: `{discipline-root}/{agent-flavoring}`
- Installed to: `.claude/templates/agent-flavoring/` (project-local copy — scaffold is self-contained)
- Applied by: `/new-researcher` at agent-creation time, reading from the project-local copy

## Vocabulary
- {list from vocabulary{}}
```

This file is the canonical record of what was applied. If a future audit asks "which pack did this project use?", this is the answer.

---

## Step 10: Verification

Verify:

- [ ] Each file in `rules[]` exists at `.claude/rules/`
- [ ] Each override target in `rule-overrides{}` exists at `.claude/rules/` with pack content (check a unique marker)
- [ ] `tools/knowledge-schema.yaml` exists if `knowledge-schema` was set
- [ ] Root CLAUDE.md contains NO unresolved `{{fragment-slot:...}}` markers
- [ ] `sessions/framework/discipline-manifest.md` exists
- [ ] Each path in `directories[]` exists and contains a `.gitkeep` (or real content)

Report any gaps. Missing optional files are warnings, not errors.

---

## What You Do NOT Do

- **Do NOT merge the pack into `templates/universal/`** — packs stay in their own directory so they can be updated independently.
- **Do NOT install discipline MCPs directly** — leave that to `unfold-mcp.md` which presents a unified menu.
- **Agent-flavoring files are copied into the project at scaffold time**, but the flavoring CONTENT is applied lazily by `/new-researcher` at agent-creation. Do not try to pre-stamp agents here — only the copy happens.
- **Do NOT mutate `discipline.json`** — it is read-only pack metadata.
