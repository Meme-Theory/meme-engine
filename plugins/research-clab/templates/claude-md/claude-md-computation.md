# {{COMPUTATION_DIR}}/ — Computation Scripts & Outputs

<!-- DEPLOY: project-root/{{COMPUTATION_DIR}}/CLAUDE.md -->
<!-- In the origin project, this was tier0-computation/. Name is domain-configurable. -->

This directory contains computation scripts and their outputs — the numerical backbone of the research project. Every quantitative claim in the project traces back to a script here.

## Structure

```
{{COMPUTATION_DIR}}/
├── *.py                        # Computation scripts
├── *.npz                       # Numerical output files (NumPy archives)
├── *.png                       # Generated figures
├── *.txt                       # Text output (gate verdicts, logs)
├── {{OUTPUT_SUBDIR}}/          # Organized output subdirectories (optional)
│   └── *.png
└── README.md                   # Script inventory and dependency documentation
```

## What This Directory Is

- **The computation engine** — scripts that produce the numerical results
- **The evidence factory** — gate verdicts are generated here
- **Fully traceable** — every output file links to the script that produced it

## Data Provenance

Every computation must maintain a clear provenance chain:

```
Script (*.py) ──runs──▶ Output (*.npz, *.png, *.txt) ──feeds──▶ Gate verdict ──enters──▶ Knowledge index
```

This chain is tracked in `tools/knowledge-index.json` under the `data_provenance` entity type.

## Gate Verdicts

Pre-registered gates are resolved here. The workflow:

1. **Pre-register** — define pass/fail criteria in `sessions/session-plan/` BEFORE computation
2. **Compute** — run the script, record numerical output
3. **Verdict** — compare output to pre-registered threshold
4. **Record** — write verdict to session file, update knowledge index via `/weave --update`

### Verdict Format

```
Gate {{GATE_ID}}: {{PASSED|FAILED}}
  Threshold: {{CRITERION}}
  Computed:  {{VALUE}}
  Verdict:   {{PASS/FAIL with brief explanation}}
```

## Script Conventions

- **One script per computation** — avoid monolithic scripts that do everything
- **Document inputs and outputs** — header comment or docstring in every script
- **Deterministic where possible** — set random seeds, document non-deterministic steps
- **Output files named descriptively** — `bcs_coupling.png` not `output_3.png`

## Python Execution

```bash
{{PYTHON_EXECUTABLE}} script_name.py
```

Use the project's virtual environment Python, not system Python. The exact path is configured in the root CLAUDE.md under "Simulation Environment."

## Rules

- **Scripts are the source of truth for numerical claims** — if a session document says "X = 3.14," a script here must produce that number
- **Never modify output files by hand** — they are generated artifacts
- **Gate verdicts are permanent** — once a gate is CLOSED or PASSED, the verdict stands
- **Mark preliminary results** — any claim from a script not yet reviewed by the Skeptic is "PRELIMINARY"
- **README.md is the inventory** — keep it updated with script descriptions and dependency info

## Who Works Here

| Role | Access |
|:-----|:-------|
| Calculator agents | Read/write — they produce and run scripts |
| Workhorse agents | Read/write — they implement specific computations |
| Observer agents | Read — they analyze outputs |
| Skeptic agents | Read — they evaluate gate verdicts |
| Infrastructure agents | **Do not touch** — coordinator, indexer, scout stay out |
