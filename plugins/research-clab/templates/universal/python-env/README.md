# Python Environment Templates

Source templates for the two requirements files installed at a project root during scaffolding.

## Files

- `requirements-mcp.txt` — System Python 3.13 dependencies for MCP servers spawned by Claude Code.
- `requirements-compute.txt` — Compute-venv dependencies for numerical scripts (shared by math and physics for the most part).

## Install Pipeline

`project-origami/unfold-python-env.md` owns the install flow:

1. Copy these files to the project root, substituting `{{COMPUTATION_DIR}}` and `{{COMPUTE_VENV_PY}}` from the user's Q5 answer.
2. Append discipline-specific additions (physics: astro + gwosc + camb + cvxpy; math: empty for now).
3. Ask the user **install now / defer / skip** via a single `AskUserQuestion`.
4. If install now: detect Python 3.13 + the compute venv, run `pip install -r ...` in each, verify with a smoke import.

## Pin Rationale

Versions pin to what has been tested end-to-end on Windows 11 / Python 3.13 against live MCPs. The MCP SDK and `fastmcp` APIs churn across minor releases — bump at your own risk, and verify with `/mcp` round-trips if you do.

## Discipline Overrides

A discipline pack can provide its own additions by setting `python-env:` in its `discipline.json`:

```json
"python-env": {
  "mcp-additions": "python-env/requirements-mcp.add.txt",
  "compute-additions": "python-env/requirements-compute.add.txt"
}
```

Both paths are relative to the pack root. The unfold step concatenates the pack additions onto the universal baseline before writing the final file.

The universal template already contains commented-out "common additions" blocks showing the physics-style extras — a pack can either ship an explicit additions file or rely on the user uncommenting those lines by hand.
