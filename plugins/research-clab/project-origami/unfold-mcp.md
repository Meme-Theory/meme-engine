# Unfold: MCP Server Installation

**Target agent**: Coordinator (during infrastructure setup)
**Task**: Detect available MCP servers, ask user which to install, verify runtime dependencies, configure `.mcp.json` and settings, append CLAUDE.md instructions.
**Inputs**: User's MCP selections (via AskUserQuestion). Python environment status (detected or from `{hardware}` input).
**Depends on**: `unfold-structure.md` (directories, settings.json, and root CLAUDE.md must exist).
**Reads from**: `${CLAUDE_PLUGIN_ROOT}/templates/MCP-templates/`

---

## Context

MCP (Model Context Protocol) servers extend Claude Code with domain-specific tools. Research projects benefit from MCPs that search academic databases, fetch papers, or connect to specialized APIs. These are **optional** — the core research-clab functionality works without them — but they dramatically improve the paper acquisition and corpus-building workflow.

This unfold is **open-ended**: each MCP is a self-contained template directory under `${CLAUDE_PLUGIN_ROOT}/templates/MCP-templates/{mcp-name}/`. To add a new MCP to the menu, create its template directory and add a menu entry in Step 1 below. No other files need modification.

### MCP Template Directory Structure

Each MCP template contains:

```
MCP-templates/{mcp-name}/
├── mcp-json-fragment.json     # Server entry for .mcp.json (one key = server name)
├── claude-md-instructions.md  # Instructions block appended to root CLAUDE.md
├── settings-permissions.md    # Permission entries for settings.json
└── requirements.md            # Runtime requirements, detection logic, install commands
```

---

## Step 1: Present the MCP Menu

**This step uses AskUserQuestion and MUST NOT run in the first response turn after a skill loads.** The calling skill is responsible for the turn boundary.

Scan `${CLAUDE_PLUGIN_ROOT}/templates/MCP-templates/` for subdirectories. Each subdirectory is an available MCP. Build the menu dynamically:

```
=== OPTIONAL MCP SERVERS ===

MCP servers add specialized tools to your project. These require external
dependencies (typically Python) and are fully optional.

Available:

  1. PAPER-SEARCH    Search & download academic papers
                     Sources: arXiv, PubMed, bioRxiv, medRxiv, Google Scholar
                     Requires: Python 3.10+, pip install paper-search-mcp

  {future MCPs appear here automatically}

  0. NONE            Skip MCP installation (can add later manually)
```

Print the menu as plain text, then ask ONE AskUserQuestion:

- Question: "Which MCP servers would you like to install?"
- Options: One option per discovered MCP (label: MCP name, description: 1-line summary + key requirement), plus "None — skip MCP setup".
- **Wait for the user's answer.**

If user selects "None", skip to Step 6 (report skip and exit).

---

## Step 2: Detect Python Environment

For each selected MCP that requires Python (check its `requirements.md`), determine the Python command. Test in this order:

### 2a. Check Project-Local venv

```bash
# Unix/macOS
if [ -f ".venv/bin/python" ]; then
  PYTHON_CMD=".venv/bin/python"
fi

# Windows
if [ -f ".venv/Scripts/python.exe" ]; then
  PYTHON_CMD=".venv/Scripts/python.exe"
fi
```

### 2b. Check System Python

```bash
# Try python3 first (avoids Python 2 on some systems)
if command -v python3 &>/dev/null; then
  PYTHON_CMD="python3"
elif command -v python &>/dev/null; then
  PYTHON_CMD="python"
elif command -v py &>/dev/null; then
  # Windows Python Launcher
  PYTHON_CMD="py -3"
fi
```

### 2c. Verify Version

```bash
$PYTHON_CMD --version 2>&1
# Must report Python 3.10 or later
```

### 2d. If Python Is Not Available

**Do NOT silently skip.** Alert the user with a clear message:

```
⚠ Python 3.10+ is required for the paper-search MCP but was not found.

The paper-search MCP needs Python to run its server process. Without it,
the search_arxiv, search_google_scholar, and other paper search tools
will not be available.

Options:
  - Install Python 3.10+ and re-run this setup
  - Continue without paper-search (you can add it manually later)
  - If Python IS installed but not on PATH, provide the full path
```

Ask ONE AskUserQuestion:
- Question: "Python not found. How to proceed?"
- Options:
  - "Skip paper-search" (description: "Continue without it, add later")
  - "Provide Python path" (description: "I'll type the path to my Python")
- **Wait for the user's answer.**

If user provides a path, verify it works (`{path} --version`). If it fails, report the error and ask again (same pattern, single question).

If user skips, remove that MCP from the install list and continue.

---

## Step 3: Install MCP Package

For each selected MCP, read its `requirements.md` and run the installation.

### paper-search

```bash
$PYTHON_CMD -m pip install paper-search-mcp
```

**Verify installation**:

```bash
$PYTHON_CMD -c "import paper_search_mcp; print('paper-search-mcp installed successfully')"
```

If installation fails (network error, permission issue, build failure):

```
⚠ Failed to install paper-search-mcp.

Error: {error message}

This usually means:
  - No internet connection
  - pip needs updating: $PYTHON_CMD -m pip install --upgrade pip
  - Missing build tools (C compiler) for native dependencies
```

Ask ONE AskUserQuestion:
- Question: "paper-search-mcp installation failed. How to proceed?"
- Options: "Retry", "Skip paper-search", "I'll install manually"
- **Wait for the user's answer.**

If "I'll install manually": write the `.mcp.json` config anyway (the server will fail at runtime but the config is ready for when the package is installed). Note this in the completion report.

---

## Step 4: Write Configuration Files

### 4a. Create or Update `.mcp.json`

The `.mcp.json` file lives at **project root** (not inside `.claude/`).

Read `${CLAUDE_PLUGIN_ROOT}/templates/MCP-templates/{mcp-name}/mcp-json-fragment.json` for each selected MCP. Each fragment contains one JSON key-value pair representing a server entry.

**If `.mcp.json` does not exist**: create it with the standard wrapper:

```json
{
  "mcpServers": {
    // ... server entries from selected MCPs
  }
}
```

**If `.mcp.json` already exists**: read it, parse the JSON, merge the new server entries into `mcpServers`, and write back. Do NOT overwrite existing server entries with the same key.

**Variable substitution in fragments**: Replace `{{PYTHON_CMD}}` with the resolved Python command from Step 2 (use the absolute path if a venv was found, or the command name if it's on PATH).

### 4b. Update `.claude/settings.json` Permissions

Read `${CLAUDE_PLUGIN_ROOT}/templates/MCP-templates/{mcp-name}/settings-permissions.md` for each selected MCP. It lists permission entries to add to `settings.json`.

**Use Edit, not Write.** Read `.claude/settings.json`, add the new permission entries to `permissions.allow` (skip duplicates), and write back. Preserve all existing entries.

### 4c. Append to Root CLAUDE.md

Read `${CLAUDE_PLUGIN_ROOT}/templates/MCP-templates/{mcp-name}/claude-md-instructions.md` for each selected MCP.

**Use Edit, not Write.** Append the instructions block to the root CLAUDE.md. Place it after the existing "Tools" or "Knowledge" section. If neither exists, append at the end.

Add a section header if one is not already present:

```markdown
## MCP Servers

{instructions block from template}
```

### 4d. Create Downloads Directory

If any selected MCP involves paper downloading (paper-search does):

```bash
mkdir -p downloads
```

Add `downloads/*.pdf` to `.gitignore` if not already present.

---

## Step 5: Verify Installation

For each installed MCP, run its verification check.

### paper-search Verification

1. **Package import**: `$PYTHON_CMD -c "import paper_search_mcp; print('OK')"`
2. **Config present**: `.mcp.json` exists and contains the `paper-search` server entry
3. **Permissions**: `.claude/settings.json` contains the academic domain whitelist entries
4. **CLAUDE.md**: Root CLAUDE.md contains the "Paper-Search MCP" instructions section

Report results per MCP:

```
MCP Installation Results:
  paper-search:
    ✓ Package installed ($PYTHON_CMD -m paper_search_mcp.server)
    ✓ .mcp.json configured
    ✓ Settings permissions added (8 academic domains)
    ✓ CLAUDE.md instructions appended
    ✓ downloads/ directory created

  {future MCPs here}
```

---

## Step 6: Report Completion

### If MCPs were installed:

```
MCP setup complete:
  Installed: {list of installed MCP names}
  Config: .mcp.json ({N} server entries)
  Python: {PYTHON_CMD} ({version})

  Tools now available:
    - search_arxiv, search_google_scholar, search_pubmed,
      search_biorxiv, search_medrxiv
    - download_arxiv, download_biorxiv, download_medrxiv
    - read_arxiv_paper, read_biorxiv_paper, read_medrxiv_paper

  NOTE: MCP servers activate on next Claude Code session start.
  If you are in an active session, restart to pick up the new tools.
```

### If skipped:

```
MCP setup skipped. No MCP servers installed.
Paper search tools are not available. Papers can still be fetched
manually via WebFetch or by the scout agent using web search.

To add MCP servers later, see:
  ${CLAUDE_PLUGIN_ROOT}/templates/MCP-templates/README.md
```

---

## What You Do NOT Do

- **Do NOT install MCPs without asking the user** — always gate behind AskUserQuestion
- **Do NOT silently skip when Python is missing** — always alert the user with options
- **Do NOT overwrite existing `.mcp.json` entries** — merge, don't replace
- **Do NOT modify MCP template files** — they are read-only source material
- **Do NOT install Python** — only detect and use what's already available
- **Do NOT run the MCP server** — just install the package and write config; the server starts automatically when Claude Code loads `.mcp.json`
- **Do NOT assume Python is available** — always detect and verify before proceeding

Your job is detection, user consent, installation, and configuration. The MCP server runs itself at session start.
