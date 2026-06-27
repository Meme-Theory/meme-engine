#!/bin/bash
# SessionStart hook: brief at a session boundary (startup/resume/compact/clear).
# Counters the "skim the resume banner, propose plausible next steps" failure
# mode. A compact/resume starts a FRESH context -- in-memory state from the prior
# turn is gone, so continuing work means reading the actual handoff on disk.
# No paths, no python -- a static brief.

cat << 'EOF'
{
  "suppressOutput": true,
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "SESSION BOUNDARY -- compact/resume starts a fresh context; in-memory state from the prior turn is gone. If continuing prior work, read the latest handoff/plan/session file on disk rather than relying on the resume banner or recall."
  }
}
EOF
