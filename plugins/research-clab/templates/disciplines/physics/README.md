# Physics Pack

Discipline overlay for mathematical physics, cosmology, and quantitative sciences.

## What This Pack Ships

Rule additions + overrides, agent-flavoring, a cosmology-ready knowledge schema, CLAUDE.md fragments, and four bundled MCP servers.

### Rule additions

- `canonical-constants.md` — import-from-canonical pattern for framework constants; `# (local)` tagging for intermediates.
- `substitution-chain.md` — mandatory explicit algebra for sign / direction / threshold claims; no "obviously from structure" shortcuts.
- `computation-environment.md` — hardware specs, GPU preference for large linear algebra, thread caps.
- `knowledge-index-usage.md` — query-before-compute discipline; MCP-first identity claims.

### Rule overrides

- `epistemic-discipline.md` → `epistemic-discipline-physics.md` — physics-flavored evidence hierarchy; framework-probability methodology.
- `gate-verdicts.md` → `gate-verdicts-physics.md` — pre-registration with SHA-256 closure hashes; 4-tuple output format (value/scheme/convention/L_max); machinery pin (PRDR).
- `evoi-prioritization.md` → `evoi-prioritization-physics.md` — EVoI with gate-based framing.

### MCPs Shipped

Four physics MCPs ship bundled, each with server source under `mcps/<name>/server/`:

- `astro/` — DESI + 30+ astroquery services (SIMBAD, VizieR, SDSS, Gaia, MAST, IRSA, NED, etc.); snapshot of `SandyYuan/astro_mcp` plus extensions.
- `gwosc/` — LIGO / Virgo / KAGRA gravitational-wave event catalogs + strain URLs via the `gwosc` client.
- `madrigal/` — CEDAR Madrigal ionospheric / heliophysics database with framework-specific search helpers.
- `nasa/` — NASA Open APIs (APOD, Mars rovers, NEO, EPIC, media library); uses `DEMO_KEY` by default, real key via `NASA_API_KEY`.

All four listed in `discipline.json` under `mcps[]`. The universal `knowledge` MCP (now at `templates/universal/mcps/knowledge/`) is also expected for any project using this pack — it is installed automatically from the universal layer when selected in the MCP menu.

### Knowledge schema

Physics entity types: `theorems`, `closed_mechanisms`, `gates`, `trajectory`, `constants`, `equations`, alongside the five universal types. The schema drives the indexer agent; no Python extractor required.

### CLAUDE.md fragments

- `canonical-constants-block.md` — injected at `{{fragment-slot:reference-data}}`. "All scripts MUST import from canonical_constants.py."
- `knowledge-mcp-block.md` — injected at `{{fragment-slot:knowledge-query-discipline}}`. "Query the knowledge MCP before computing."
- `computation-environment-block.md` — injected at `{{fragment-slot:computation-environment}}`. Hardware / venv narrative.

### Agent flavoring

Per-archetype notes in `agent-flavoring/` — layered onto universal templates by `/new-researcher` when stamping a domain agent.

## Skills

`c-compare`, `penrose-diagram`, `latex` — listed in `discipline.json` under `skills[]`; author them in `skills/` as they stabilize.

## Authoring Workflow

1. Extract content from a living physics project (rule, schema, fragment, MCP server), stripping project-specific anecdotes (session numbers, paper paths, hardcoded constants).
2. Drop it into the appropriate subdirectory here. For MCPs: `mcps/<name>/server/` for source, plus the 4 config fragments at `mcps/<name>/`.
3. Register in `discipline.json` under the appropriate field.
4. Test by scaffolding a new project with `--discipline physics` and verifying the content appears.
