# Discipline Packs

A discipline pack is a plug-and-play overlay that turns the universal research-clab harness into a domain-specific research environment (physics, biomedical, software, legal, etc.).

## Layering

```
templates/
├── universal/              # cognitive harness (discipline-agnostic)
│   ├── rules/              # teammate, team-lead, output, session-handoffs, agent-standards, ...
│   ├── session-templates/  # formats A-I (cognitive patterns, not domain patterns)
│   ├── agent-templates/    # archetypes: skeptic, calculator, workhorse, ...
│   ├── claude-md/          # root + per-directory CLAUDE.md templates (with {{fragment slots}})
│   ├── mcps/               # cross-discipline MCPs (paper-search, filesystem, ...)
│   ├── skills/             # /weave, /rclab-*, /librarian, ...
│   └── ...
└── disciplines/
    ├── physics/            # one pack per discipline
    │   ├── discipline.json
    │   ├── rules/          # discipline-specific rules (substitution-chain, canonical-constants, ...)
    │   ├── mcps/           # discipline-specific MCPs (astro, gwosc, knowledge-index, ...)
    │   ├── knowledge-schema.yaml
    │   ├── claude-md-fragments/   # insertable text blocks for root CLAUDE.md
    │   └── agent-flavoring/       # optional: per-archetype domain-flavor notes
    └── <future packs>/
```

Universal installs unconditionally. A selected discipline pack overlays on top.

## Pack Manifest (`discipline.json`)

```json
{
  "name": "physics",
  "display-name": "Mathematical Physics / Cosmology",
  "description": "Gate-based pre-registered computation, canonical-constants pattern, astro/arxiv/gwosc data access.",
  "extends": "universal",
  "rules": [
    "gate-verdicts-physics.md",
    "substitution-chain.md",
    "canonical-constants.md",
    "knowledge-index-usage.md",
    "computation-environment.md"
  ],
  "rule-overrides": {
    "epistemic-discipline.md": "epistemic-discipline-physics.md"
  },
  "mcps": ["knowledge", "astro", "arxiv", "gwosc"],
  "knowledge-schema": "knowledge-schema.yaml",
  "claude-md-fragments": {
    "root-reference-data": "canonical-constants.md",
    "root-computation-env": "computation-env.md"
  },
  "agent-flavoring": "agent-flavoring/",
  "vocabulary": {
    "pre-registered-test": "gate",
    "pass-fail-record": "verdict",
    "reproducibility-hash": "closure-hash"
  }
}
```

### Required fields

| Field | Purpose |
|:------|:--------|
| `schema-version` | Must equal `"1.0"` for the current overlay spec. Pre-flight rejects other values. Bump when the overlay contract changes incompatibly. |
| `name` | Directory name; matches `disciplines/<name>/` |
| `display-name` | Shown in the discipline-selection menu |
| `description` | One-liner shown under each menu option |
| `extends` | Currently always `"universal"`; reserved for future base-switching |

### Optional fields (all overlay on universal)

| Field | Behavior |
|:------|:---------|
| `rules` | Rule files ADDED to `.claude/rules/` on top of universal rules |
| `rule-overrides` | Map universal rule filename → pack filename that REPLACES it |
| `mcps` | MCP names to install from `disciplines/<name>/mcps/`; universal MCPs always available |
| `knowledge-schema` | Path (relative to pack root) to discipline-specific `knowledge-schema.yaml` |
| `claude-md-fragments` | Text blocks injected into `{{slot}}` markers in universal CLAUDE.md templates |
| `agent-flavoring` | Directory of per-archetype flavor notes appended during `/new-researcher` |
| `skills` | Discipline-specific skills installed to `.claude/skills/` alongside universal skills |
| `vocabulary` | Concept-name overrides for display/docs (not for enforcement) |

## Authoring a New Pack

Minimum viable pack:

```
disciplines/<name>/
├── discipline.json     # only "name", "display-name", "description", "extends" required
├── rules/              # optional
├── mcps/               # optional
├── knowledge-schema.yaml  # optional
└── claude-md-fragments/   # optional
```

A pack with only a `discipline.json` ships the universal harness with a custom display name — useful for "generic research" or "I'll fill it in later."

## Discipline Selection Flow

`/new-research-project` scans `templates/disciplines/` for packs, reads each `discipline.json`, presents a menu. Selection is frozen at scaffold time; switching disciplines on an existing project is not supported.

## One Discipline Per Project

Packs do not stack. If a project needs cross-disciplinary work (e.g., biomed + statistics), author a combined pack or extend the chosen one with project-specific rules in `.claude/rules/` post-scaffold.
