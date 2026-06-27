<!-- DEPLOY: project-root/.claude/hooks/ (the *.sh scripts; this README stays template-side) -->

# Universal Hooks

Battle-tested, project-agnostic Claude Code hooks. The unfold step copies the
`*.sh` scripts in this directory to `project-root/.claude/hooks/` and wires
matching entries into `project-root/.claude/settings.json` (see
`claude-md/claude-md-settings-json.md` for the exact `hooks` block).

All scripts are **bare `python` / stdlib only** -- no virtualenv, no project
Python, no discipline-specific audit scripts. They read the PreToolUse /
SessionStart / SubagentStart JSON on stdin and emit the documented hook output
JSON on stdout. Briefs and deny reasons are written generically; nothing here
references a specific domain, gate ID, or corpus filename.

## The hooks

| Script | Event / matcher | What it does |
|:--|:--|:--|
| `rules-folder-subagent-block.sh` | PreToolUse `Edit\|Write\|MultiEdit` | HARD-denies (permissionDecision deny) when a **subagent** (`agent_id` non-empty) tries to edit any file under `.claude/rules/`. The orchestrator is unaffected. Closes the recursion gap where subagents bloat directive-only rule files with corpus content. Highest-value structural guard. |
| `SESSION-START-DIRECTIVE.sh` | SessionStart | Static brief: a compact/resume starts a fresh context; read the latest handoff/plan/session file on disk instead of trusting the resume banner or recall. |
| `SUBAGENT-START-DIRECTIVE.sh` | SubagentStart | Static brief to the spawned subagent: read the spawn prompt and every file it cites, match pre-registered thresholds exactly, and verify promised artifacts on disk by content (not line count) before reporting done. |
| `mcp-pre-check.sh` | PreToolUse `mcp__.*` | `case` dispatcher that injects a per-server just-in-time brief. Ships generic arms for the universal servers (`knowledge` query-first; `paper-search` arXiv API syntax) and a marked extension point where discipline packs add their own server arms. Unknown servers pass through silently. |

## Wiring

The settings block invokes each script via bash with a project-relative path,
e.g. `bash ".claude/hooks/SESSION-START-DIRECTIVE.sh"`. Hooks run with the
project root as the working directory, so no absolute paths are baked in --
the deployed project is portable across machines.

## Extending (discipline packs)

A discipline pack (e.g. `disciplines/physics/hooks/`) can:

- add server arms to `mcp-pre-check.sh` at the marked extension point (keep each
  brief generic to the server's tools), and
- ship additional hooks (e.g. a generalized python lint or an
  epistemic-discipline edit guard) and append their settings entries.

Keep discipline-specific paths, venvs, and audit scripts OUT of these universal
hooks.
