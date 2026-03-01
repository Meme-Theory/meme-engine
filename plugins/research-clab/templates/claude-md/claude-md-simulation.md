# {{SIMULATION_DIR}}/ — Simulation Codebase

<!-- DEPLOY: project-root/{{SIMULATION_DIR}}/CLAUDE.md -->
<!-- This directory is OPTIONAL. Not all research projects have a simulation component. -->
<!-- In the origin project, this was phonon-exflation-sim/. Name is domain-configurable. -->

This directory contains a structured simulation codebase — a proper software project with source code, scripts, data, and its own virtual environment. This is distinct from the computation directory (which holds standalone scripts); this is an engineered simulation.

## Structure

```
{{SIMULATION_DIR}}/
├── src/                        # Source code (modules, classes, core logic)
│   └── *.py
├── scripts/                    # Runnable scripts that use src/ modules
│   └── *.py
├── data/                       # Input data, configuration files
├── figures/                    # Generated output figures
├── .venv*/                     # Python virtual environment
├── requirements.txt            # Python dependencies (or pyproject.toml)
└── README.md                   # Setup and usage instructions
```

## What This Directory Is

- **A software project** — structured code with separation of concerns (src/ vs scripts/)
- **Self-contained** — has its own virtual environment and dependencies
- **The simulation engine** — runs domain-specific models and produces data

## What This Directory Is NOT

- **Not a scratch pad** — use `{{COMPUTATION_DIR}}/` for one-off scripts
- **Not a notebook collection** — if you need Jupyter, put notebooks in `scripts/`
- **Not shared infrastructure** — this is domain-specific simulation code

## Virtual Environment

```bash
# Activate
source {{SIMULATION_DIR}}/.venv*/bin/activate    # Unix
{{SIMULATION_DIR}}/.venv*/Scripts/activate        # Windows

# Run scripts
python scripts/run_simulation.py
```

The virtual environment is project-local. Never install packages globally.

## Relationship to Other Directories

```
researchers/          ──(theory)──▶  {{SIMULATION_DIR}}/src/    ──(implements)──▶  models
{{COMPUTATION_DIR}}/  ──(validates)──▶  {{SIMULATION_DIR}}/     ──(produces)──▶    data/figures
sessions/             ──(directs)──▶   {{SIMULATION_DIR}}/     ──(reports to)──▶  sessions/
```

## Rules

- **Treat this as a software project** — use proper imports, avoid copy-paste, write docstrings
- **Don't modify src/ without understanding the architecture** — read before writing
- **Virtual environment is sacred** — don't install random packages; update requirements.txt
- **Output goes to designated directories** — `data/` for data, `figures/` for plots
- **Coordinate with computation directory** — if a standalone script in `{{COMPUTATION_DIR}}/` grows complex enough, migrate it here

## Who Works Here

| Role | Access |
|:-----|:-------|
| Calculator agents | Read/write — primary developers of simulation code |
| Workhorse agents | Read/write — implement specific features |
| Observer agents | Read — analyze simulation outputs |
| Skeptic agents | Read — evaluate simulation validity |
| Infrastructure agents | **Do not touch** — no coordinator, librarian, or scout access |
