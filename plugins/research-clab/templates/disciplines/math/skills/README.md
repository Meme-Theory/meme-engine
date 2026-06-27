# Math-Specific Skills

Two skills ship with the math pack; both are registered in `disciplines/math/discipline.json` under `skills[]` and installed when the math discipline is selected.

## Shipped skills

| Skill | Purpose |
|:------|:--------|
| `/proof-check` | Structural audit of an existing proof/derivation -- the 7-check pass (step justification, variable scope, limiting cases, dimensional/type consistency, canonical-source traceability, substitution chain, sole-source avoidance). Reports findings; does not fix the proof. Cross-listed with the physics pack. |
| `/sage-compute` | Thin front-end to the `sage` MCP for exact/symbolic computation (factor, simplify, symbolic eigenvalues, exact integrals, LaTeX). Requires the `sage` MCP. Cross-listed with the physics pack. |

## Candidates for future work

| Skill | Purpose |
|:------|:--------|
| `/conjecture-index` | Catalog the project's open conjectures, their approaches, and their blockers. (A universal version is the better home -- see `templates/universal/skills/`.) |
| `/lean` | Compile a Lean artifact and report pass/fail + first error on fail. (Needs Lean + mathlib installed locally.) |
| `/theorem-lookup` | Search the project knowledge base for theorems matching a description. |

## Authoring a new skill

Mirror the universal skill structure:

```
disciplines/math/skills/<name>/
|-- SKILL.md       # YAML frontmatter (name, description, argument-hint, allowed-tools) + body
```

Then register `<name>` in `disciplines/math/discipline.json` under `skills[]`.
