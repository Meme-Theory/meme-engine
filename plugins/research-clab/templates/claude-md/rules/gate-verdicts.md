---
paths:
  - "{{COMPUTATION_DIR}}/**"
---

# Gate Verdict Standards

<!-- DEPLOY: project-root/.claude/rules/gate-verdicts.md -->
<!-- Path-scoped: loads only when working in the computation directory -->

## Pre-Registration Protocol

1. **Before computation**: Define the gate in `sessions/session-plan/` with:
   - Gate ID (e.g., `V-1`, `M-3`)
   - Hypothesis being tested
   - Pass/fail threshold (quantitative)
   - What PASSES and what FAILS mean for the solution space

2. **During computation**: Run the script, record raw numerical output

3. **After computation**: Compare output to pre-registered threshold

## Verdict Format

```
Gate {{GATE_ID}}: {{PASSED|FAILED}}
  Threshold: {{CRITERION}}
  Computed:  {{VALUE}}
  Verdict:   {{PASS/FAIL with brief explanation}}
```

## Rules

- Gate criteria are defined BEFORE computation — never after seeing results
- Verdicts are permanent — no retroactive changes
- Only the Skeptic evaluates whether a gate verdict is meaningful
- Record verdicts in the session file AND update knowledge index via `/weave --update`
