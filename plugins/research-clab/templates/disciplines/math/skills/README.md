# Math-Specific Skills

Empty at ship. Candidates for future work:

| Skill | Purpose |
|:------|:--------|
| `/proof-check` | Walk a proof, flag unstated lemmas, list case-coverage gaps, check scope of every citation |
| `/conjecture-index` | Catalog the project's open conjectures, their approaches, and their blockers |
| `/sage` | Invoke Sage for a symbolic computation and report the result with the input script |
| `/lean` | Compile a Lean artifact and report pass/fail + first error on fail |
| `/theorem-lookup` | Search the project knowledge base for theorems matching a description |

To author one, mirror the universal skill structure:

```
disciplines/math/skills/<name>/
└── SKILL.md       # YAML frontmatter (name, description, argument-hint, allowed-tools) + body
```

Then register in `disciplines/math/discipline.json` under `skills[]`.
