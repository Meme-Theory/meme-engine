<!-- Slot: reference-data -->
<!-- Source: extracted from Ainulindale Exflation CLAUDE.md §"Canonical Constants" -->
<!-- This fragment is inserted into the project root CLAUDE.md by the unfold process. -->

## Canonical Constants (`{{CANONICAL_MODULE}}`)

All computation scripts MUST import framework constants from `{{CANONICAL_MODULE}}` — never hardcode them. The `/weave --update` pipeline audits compliance automatically. Read the module for available constants and provenance. See `.claude/rules/canonical-constants.md` for the full discipline (import pattern, `# (local)` tagging for intermediates, audit categories).
