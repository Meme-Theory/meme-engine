# Unfold: Python Environment Backbone

**Target agent**: Main `/new-research-project` skill (NOT coordinator — this phase is user-interactive)
**Task**: Write the project-level `requirements-mcp.txt` + `requirements-compute.txt`, ask the user whether to install now, and (if yes) run pip against the right interpreter(s).
**Inputs**: `{output-format}`, `{hardware-specs}`, `{discipline}`, the MCP selection result from Phase 7b, and whether `{{COMPUTATION_DIR}}` was created in Phase 2.
**Reads from**: `${CLAUDE_PLUGIN_ROOT}/templates/universal/python-env/`, the selected discipline pack's `python-env/` (if any), `sessions/framework/discipline-manifest.md` (MCP registrations).
**Runs after**: Phase 7b (MCP install — so that `tools/mcp-servers/` is populated and editable installs resolve).
**Runs before**: Phase 10 (final verification).

---

## Context

Research projects need two Python environments:

1. **System Python 3.13** for MCP servers. Claude Code spawns these as stdio subprocesses; they can't use a venv the harness doesn't know about.
2. **Compute venv** (e.g., `{{COMPUTATION_DIR}}/.venv/`) for numerical scripts. Isolated from system Python so heavy deps (torch, camb, cvxpy) don't pollute the MCP interpreter, and so multiple projects on one machine don't conflict.

This unfold writes the two requirements files to the project root, then asks the user whether to run pip immediately or defer.

---

## Step 1: Gate — Ask the User

**Output the file preview as plain text first** (so the user can see what they'd be installing), then call a single `AskUserQuestion`.

```
=== PYTHON BACKBONE ===

I can set up the Python dependencies for this project:

  requirements-mcp.txt         → system Python 3.13 (for MCP servers)
  requirements-compute.txt     → {{COMPUTATION_DIR}}/.venv/ (for numerical scripts)

Core pins: mcp==1.26.0, fastmcp==3.0.2, numpy==2.4.2, scipy==1.17.0, sympy==1.14.0, matplotlib==3.10.8
Discipline additions (if any) are appended based on the selected pack.
ROCm/CUDA torch is documented but installed manually — the wheel must match your GPU SDK.
```

Then AskUserQuestion, one question, three options:

- **Label**: `"Install now"` — Description: `"Write files + run pip in both interpreters"`
- **Label**: `"Defer install"` — Description: `"Write files; I'll run pip myself later"`
- **Label**: `"Skip entirely"` — Description: `"No Python env for this project; don't write files"`

Wait for the user's answer. Branches below.

### If "Skip entirely"

Report: `"Skipped Python backbone. Re-run unfold-python-env.md manually to add later."`. Proceed to Phase 10. No files written.

---

## Step 2: Compose the Requirements Files

This step runs for both "Install now" and "Defer install".

### 2a. Read the universal baselines

```
${CLAUDE_PLUGIN_ROOT}/templates/universal/python-env/requirements-mcp.txt      → MCP_BASE
${CLAUDE_PLUGIN_ROOT}/templates/universal/python-env/requirements-compute.txt  → COMPUTE_BASE
```

### 2b. Resolve substitutions

Compute the following substitutions and apply to both files:

- `{{COMPUTATION_DIR}}` — the Q5 directory name if Q5=Yes; if Q5=No, replace with the literal string `(compute dir not configured)` so the file reads as documentation-only.
- `{{COMPUTE_VENV_PY}}` — if Q5=Yes, resolve to `{{COMPUTATION_DIR}}/.venv/Scripts/python.exe` on Windows, `{{COMPUTATION_DIR}}/.venv/bin/python` on Unix. If Q5=No, replace with the literal string `(compute venv not configured)` and prepend a `# ` to any install command line that referenced it so those lines are commented out.
- `{{PROJECT_NAME}}` — from user input (rarely used in these files but available).

After substitution, NO `{{...}}` mustache placeholder may remain in either file.

### 2c. Append discipline additions

If the selected discipline pack sets `python-env` in its `discipline.json`:

```json
"python-env": {
  "mcp-additions": "python-env/requirements-mcp.add.txt",
  "compute-additions": "python-env/requirements-compute.add.txt"
}
```

Read each referenced file (relative to the pack root) and APPEND to the corresponding base file under a clearly-marked section:

```
# ==============================================================================
#  Discipline-pack additions ({discipline-display-name})
# ==============================================================================
<contents of the pack additions file>
```

If the pack has no `python-env` field, skip this step and keep the universal baseline's commented "common additions" blocks as-is.

### 2d. Write to project root

```
{target-dir}/requirements-mcp.txt
{target-dir}/requirements-compute.txt
```

### 2e. Verify no surviving placeholder leaks

```bash
grep -nE "\{\{[A-Z_]+\}\}" {target-dir}/requirements-mcp.txt {target-dir}/requirements-compute.txt
```

This must return zero matches. Any `{{...}}` placeholder that survives Step 2b is a bug in the substitution logic — abort and report the path + line number.

---

## Step 3: Install Pipeline (only if "Install now")

If the user chose "Defer install", skip to Step 5.

### 3a. Detect system Python 3.13

Try in order, take the first that succeeds:

```bash
# Windows
py -3.13 --version

# Unix
python3.13 --version
command -v python3.13

# Last-resort fallback (ambiguous — warn user)
python --version   # accept only if output contains "Python 3.13"
```

Record the invocation prefix as `$PY_MCP` (e.g., `py -3.13` or `python3.13`).

If no Python 3.13 is found: alert the user explicitly. Offer:
- **"Skip MCP install"** — leave requirements-mcp.txt on disk, continue
- **"Provide path"** — accept a user-supplied Python 3.13 absolute path (single AskUserQuestion, one question)

Do NOT silently fall back to `python` — the version matters; the MCP SDK pins we use are tested on 3.13.

### 3b. Detect compute venv

If Q5=Yes with an explicit `{{COMPUTATION_DIR}}`:

```bash
ls "{target-dir}/{{COMPUTATION_DIR}}/.venv*/Scripts/python.exe"     # Windows
ls "{target-dir}/{{COMPUTATION_DIR}}/.venv*/bin/python"             # Unix
```

If multiple matches exist, prefer `.venv312`, else the lexicographically last match. Record as `$PY_COMPUTE`.

If no venv exists: offer to create one using the same Python 3.13 discovered in 3a. Single AskUserQuestion, one question:
- **"Create venv now"** — `$PY_MCP -m venv "{target-dir}/{{COMPUTATION_DIR}}/.venv"` then use it
- **"Skip compute install"** — leave requirements-compute.txt on disk, continue without installing

If Q5=No: `requirements-compute.txt` is documentation-only; skip 3b entirely.

### 3c. Dry-run resolve

Before any real install, run pip in dry-run mode to catch version conflicts early:

```bash
$PY_MCP -m pip install --dry-run -r "{target-dir}/requirements-mcp.txt"
```

```bash
"$PY_COMPUTE" -m pip install --dry-run -r "{target-dir}/requirements-compute.txt"
```

If either fails: capture stderr, report to the user, and ask whether to proceed with `--no-deps` (dangerous — skip resolver), retry after manual edit, or abort. Single AskUserQuestion, one question.

### 3d. Real install

Only if dry-run passed:

```bash
$PY_MCP -m pip install -r "{target-dir}/requirements-mcp.txt"
"$PY_COMPUTE" -m pip install -r "{target-dir}/requirements-compute.txt"
```

Allow up to 5 minutes per install (10 minutes if this is a fresh venv). Stream stdout to the user.

### 3e. Editable MCPs

For each MCP registered in `sessions/framework/discipline-manifest.md` (or anywhere under `tools/mcp-servers/`) that has a `pyproject.toml` or `setup.py`:

```bash
$PY_MCP -m pip install -e "{target-dir}/tools/mcp-servers/<mcp-name>"
```

`paper-search-mcp` is the canonical example. Skip any that aren't present on disk yet (the MCP unfold may have skipped them if the user declined the MCP menu).

### 3f. GPU torch (opt-in, printed, not auto-run)

Do NOT auto-install ROCm/CUDA torch — the wheel index depends on the user's GPU SDK. Print the install command from `requirements-compute.txt`'s GPU block and note it for the user to run manually when they're ready:

```
-- GPU torch not auto-installed. --
Run when your GPU SDK is ready. Example (ROCm 7.2):
  "$PY_COMPUTE" -m pip install torch==2.9.1+rocmsdk20260116 --index-url https://download.pytorch.org/whl/rocm7.2
See requirements-compute.txt for CUDA and CPU-only variants.
```

---

## Step 4: Smoke Test

Only for installed interpreters (skip for deferred / skipped installs):

```bash
# MCP
$PY_MCP -c "import mcp, fastmcp, httpx; print('mcp OK', mcp.__version__)"

# Compute
"$PY_COMPUTE" -c "import numpy, scipy, sympy, matplotlib; print('compute OK', numpy.__version__)"
```

Capture failures and report per-line. A smoke failure is not automatically fatal — some deps may need network or credentials to fully import. Record the failure and continue to Step 5.

---

## Step 5: Report

Print a summary the user can scan:

```
=== PYTHON BACKBONE ===

Files written:
  requirements-mcp.txt      OK ({N} pinned deps)
  requirements-compute.txt  OK ({M} pinned deps; venv={venv-path or "not configured"})

Install status:
  MCP (system Python 3.13): {INSTALLED | DRY-RUN-ONLY | DEFERRED | SKIPPED | FAILED <reason>}
  Compute ({venv}):         {INSTALLED | DRY-RUN-ONLY | DEFERRED | SKIPPED | FAILED <reason>}

Editable MCPs installed:
  - paper-search-mcp        {OK | SKIPPED (not on disk) | FAILED <reason>}

Next steps:
  - GPU torch is NOT auto-installed. See requirements-compute.txt.
  - If deferred, install commands:
      py -3.13 -m pip install -r requirements-mcp.txt
      "{venv-path}" -m pip install -r requirements-compute.txt
```

Append one line to `sessions/framework/discipline-manifest.md` under a new `## Python Environment` section with the install status, so future audits can see what was done.

---

## Verification

- [ ] `requirements-mcp.txt` exists at project root (if not "Skip entirely")
- [ ] `requirements-compute.txt` exists at project root (if not "Skip entirely")
- [ ] If "Install now": smoke import for `mcp` succeeds under `$PY_MCP`
- [ ] If "Install now" and Q5=Yes: smoke import for `numpy` succeeds under `$PY_COMPUTE`
- [ ] No unresolved `{{COMPUTE_VENV_PY}}` or `{{PROJECT_NAME}}` placeholders in the written files
- [ ] Manifest updated if a pack added `python-env` extras

---

## What You Do NOT Do

- **Do NOT auto-install ROCm/CUDA torch** — the wheel is SDK-specific and the user's machine may not even have a GPU. Print the command for manual execution.
- **Do NOT create the compute venv silently** — always ask the user if no venv exists. Users may prefer their system Python, Conda, poetry, uv, etc.
- **Do NOT run `pip install --upgrade ...`** — pins are pins. Upgrading against them defeats reproducibility.
- **Do NOT silently fall back to a non-3.13 Python** — MCP SDK pins are 3.13-tested. Ambiguous falls go through an explicit AskUserQuestion.
- **Do NOT skip the dry-run** — a failed resolve on the real install can leave pip in a half-installed state that's harder to debug than a clean failure.
