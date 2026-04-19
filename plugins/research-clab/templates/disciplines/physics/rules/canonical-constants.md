# Canonical Constants & Local Variables

<!-- DEPLOY: project-root/.claude/rules/canonical-constants.md -->
<!-- Path-scoped: loads when working in the computation directory OR on Python sources -->
<!-- Source: extracted from Ainulindale Exflation .claude/rules/math-scripts.md §"Canonical Constants (MANDATORY)" and §"Local Variable Tagging" -->

---
paths:
  - "{{COMPUTATION_DIR}}/**"
  - "*.py"
---

## Canonical Constants (MANDATORY)

Every computation script MUST:

1. **Import from `{{CANONICAL_MODULE}}`**: e.g., `from {{CANONICAL_MODULE}} import *`
2. **Never hardcode framework constants** — use the imported names
3. **Add new constants to `{{CANONICAL_MODULE}}` FIRST** if they do not exist, then import

Framework constants are any numerical values that (a) represent a physical or mathematical input the project treats as fixed, (b) carry provenance (PDG, Planck, DESI, prior gate result, or an audited registry entry), and (c) are used by more than one script.

**Heuristic**: if the same literal value appears in 3+ scripts, it belongs in `{{CANONICAL_MODULE}}`.

## Local Variable Tagging

Variables that are computed intermediate values (NOT framework constants) must be tagged with `# (local)` at the end of the assignment line:

```python
E_kin = 0.5 * m * v**2          # (local)
R_ratio = a_2 / a_4             # (local)
delta_ns = ns_bare - ns_obs     # (local)
```

The `# (local)` tag tells the constants audit to skip this line. Without it, any assignment matching the potential-hardcode regex is flagged.

### When to use `# (local)`

- Computed quantities derived from other variables
- Loop counters and indices that happen to match the naming pattern
- Temporary results specific to one computation
- Estimates, approximations, and scan parameters

### When NOT to use `# (local)`

- Framework constants that should be in `{{CANONICAL_MODULE}}`
- Observational values (PDG, Planck, DESI, or other audited references) used in 2+ scripts
- Gate thresholds and pre-registered criteria

## Audit Pipeline

The knowledge-weaver / constants-audit pipeline reports:

- **Compliant**: scripts with correct imports
- **Violations**: known stale hardcodes (must fix)
- **Potential**: assignments not in `{{CANONICAL_MODULE}}` and not tagged `# (local)`

Target: **Potential = 0**. Every assignment is either imported from canonical or tagged as local.
