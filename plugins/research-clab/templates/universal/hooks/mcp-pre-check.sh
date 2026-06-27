#!/usr/bin/env bash
# ----------------------------------------------------------------------------
# MCP Pre-Check Hook (PreToolUse, matcher "mcp__.*")
# ----------------------------------------------------------------------------
# Injects a per-MCP-server just-in-time brief before the MCP tool call runs.
# Reads tool_name from PreToolUse JSON stdin and dispatches via `case` on the
# `mcp__<server>__` prefix. Silent passthrough for unknown / future servers.
#
# This is the UNIVERSAL skeleton: it ships generic arms for the two universal
# MCP servers (knowledge, paper-search). Discipline packs extend it by adding
# their own case arms at the marked extension point (e.g. physics: astro,
# madrigal; math: sage, oeis, mathscinet, zbmath). Keep each brief generic to
# the server's TOOLS -- do not hardcode one project's results or rule names.
#
# Bare `python` (stdlib json only) -- no venv, no project Python.
# ----------------------------------------------------------------------------

set -u

INPUT=$(cat)
TOOL_NAME=$(printf '%s' "$INPUT" | python -c \
  "import sys,json; print(json.loads(sys.stdin.read() or '{}').get('tool_name',''))" \
  2>/dev/null || echo "")

case "$TOOL_NAME" in
  mcp__knowledge__*)
    BRIEF="KNOWLEDGE-MCP -- query-first discipline. This is the canonical project knowledge graph. Before computing or deriving anything, verify the result is not already known/settled/canonical. Order: search_knowledge -> trace_entity -> get_constant -> list_constants. Do not recompute what is already closed. Emit gate outcomes with emit_verdict (single race-safe writer), never by hand-appending to the verdict file."
    ;;
  mcp__paper-search__*)
    BRIEF="PAPER-SEARCH-MCP -- download-before-cite. Order: search -> download -> read; never cite a paper from training memory. For arXiv use the API field syntax (au: author, ti: title, abs: abstract, cat: category, AND/OR/ANDNOT) -- a natural-language query returns the LATEST papers, not the most relevant. Mark a gap explicitly when a citation cannot be fetched."
    ;;
  # --- DISCIPLINE-PACK EXTENSION POINT --------------------------------------
  # Discipline packs append server arms here, e.g.:
  #   mcp__astro__*)   BRIEF="ASTRO-MCP -- ..." ;;
  #   mcp__sage__*)    BRIEF="SAGE-MCP -- ..." ;;
  #   mcp__oeis__*)    BRIEF="OEIS-MCP -- ..." ;;
  # Keep briefs generic to the server's tools; do not hardcode project results.
  # --------------------------------------------------------------------------
  *)
    # Unknown / future MCP server -- silent passthrough rather than blocking.
    exit 0
    ;;
esac

# Emit additionalContext for the model's next turn. Build the JSON with python
# so brief text round-trips cleanly regardless of punctuation.
python -c "
import json, sys
print(json.dumps({
  'hookSpecificOutput': {
    'hookEventName': 'PreToolUse',
    'additionalContext': sys.argv[1]
  }
}))
" "$BRIEF"

exit 0
