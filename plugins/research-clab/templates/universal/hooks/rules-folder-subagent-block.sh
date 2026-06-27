#!/bin/bash
# PreToolUse hook (Edit|Write|MultiEdit): HARD-BLOCK subagent edits to
# `.claude/rules/`. The orchestrator (main agent) is unaffected.
#
# Why
# ---
# Rule files at `.claude/rules/*.md` are DIRECTIVE-only documents. Subagents have
# a recurring pattern of bloating them with corpus-shaped content -- calibration
# entries, ledgers, audit-SHA hex strings, dated session-event records, and
# per-instance promotion narratives. That content belongs in the project's
# knowledge corpus, not in a rule. This hook closes the gap at the harness level
# by emitting a `permissionDecision: "deny"` per the documented Claude Code
# PreToolUse JSON output protocol (see https://code.claude.com/docs/en/hooks).
#
# Discriminator
# -------------
# Per the documented hook input schema, `agent_id` is "Present only when the hook
# fires inside a subagent call." The orchestrator's hook input does not carry
# this field. Subagent-vs-orchestrator detection is therefore the non-emptiness
# of `agent_id`.
#
# Match
# -----
# Subagent (agent_id non-empty) AND normalized `tool_input.file_path` contains
# `.claude/rules/` -> emit deny. Otherwise -> exit 0 silently (no-op).
#
# Bare `python` (stdlib json only) -- no venv. `chr(92)` is used for the literal
# backslash so the script is independent of bash quote/escape semantics; Windows
# absolute paths (`C:\...\.claude\rules\`) and POSIX-relative paths
# (`.claude/rules/...`) both normalize correctly.

INPUT=$(cat)

RESULT=$(printf '%s' "$INPUT" | python -c "
import json, sys
try:
    d = json.load(sys.stdin)
    agent_id = (d.get('agent_id') or '').strip()
    fp = (d.get('tool_input', {}).get('file_path') or '')
    fp_norm = fp.replace(chr(92), '/').lower()
    if agent_id and '.claude/rules/' in fp_norm:
        print('block')
    else:
        print('')
except Exception:
    print('')
" 2>/dev/null)

if [ "$RESULT" != "block" ]; then
  exit 0
fi

cat << 'EOF'
{
  "suppressOutput": true,
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "NO. Subagents do not edit `.claude/rules/`. Rule files are directive-only. Calibration entries, ledgers, audit-SHA hex strings, dated session-event records, and per-instance narratives belong in the project knowledge corpus (e.g. a results/notes file or a registry corpus under `sessions/framework/`), not in a rule. If a rule genuinely needs to change, report the proposed change to the orchestrator -- the orchestrator owns rule edits. Do not route this edit back as a rule-file diff for the orchestrator to apply blindly; put corpus content in the corpus."
  }
}
EOF
exit 0
