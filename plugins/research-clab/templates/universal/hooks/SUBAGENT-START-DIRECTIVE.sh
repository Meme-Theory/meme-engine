#!/bin/bash
# SubagentStart hook: brief the spawned subagent at its execution boundary.
# Fires once per spawn (child side). The contract is the spawn prompt; the files
# it cites are the contract's substrate. Verify promised artifacts on disk by
# content, not by line count. No paths, no python -- a static brief.

cat << 'EOF'
{
  "suppressOutput": true,
  "hookSpecificOutput": {
    "hookEventName": "SubagentStart",
    "additionalContext": "SUBAGENT START -- Read your spawn prompt and every file it cites before acting; match any pre-registered threshold and tolerance exactly. Verify your promised artifacts exist on disk (by content, not line count) before reporting done."
  }
}
EOF
