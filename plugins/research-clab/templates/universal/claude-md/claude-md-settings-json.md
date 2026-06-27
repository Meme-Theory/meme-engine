# settings.json — Shared Project Configuration

<!-- DEPLOY: project-root/.claude/settings.json -->
<!-- This file is committed to version control. It applies to all team members. -->
<!-- Personal overrides go in settings.local.json (gitignored). -->

```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1",
    "BASH_DEFAULT_TIMEOUT_MS": "180000",
    "BASH_MAX_TIMEOUT_MS": "300000"
  },
  "effortLevel": "xhigh",
  "permissions": {
    "allow": [
      "WebFetch(domain:arxiv.org)",
      "WebFetch(domain:en.wikipedia.org)",
      "WebFetch(domain:scholar.google.com)",
      "WebFetch(domain:inspirehep.net)",
      "Bash(timeout:*)"
    ],
    "deny": [
      "Bash(rm -rf *)",
      "Bash(git push --force *)",
      "Bash(git push * main)",
      "Bash(git push * master)",
      "Read(~/.ssh/*)",
      "Read(~/.aws/*)",
      "Read(~/.gnupg/*)",
      "Read(~/.config/gh/*)",
      "Read(**/.env)",
      "Read(**/.env.local)",
      "Read(**/credentials.json)",
      "Read(**/.npmrc)",
      "Read(**/.pypirc)",
      "Read(**/secrets.*)",
      "Read(**/*.pem)",
      "Read(**/*.key)"
    ]
  },
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup|resume|clear|compact",
        "hooks": [
          {
            "type": "command",
            "command": "echo '{\"systemMessage\":\"effort: MAX (session-start hook)\",\"hookSpecificOutput\":{\"hookEventName\":\"SessionStart\",\"additionalContext\":\"EFFORT LEVEL: MAX. Every task in this session is non-trivial. Do not self-limit thinking. Research/audit/orchestration work = MAX reasoning.\"}}'",
            "timeout": 5000
          },
          {
            "type": "command",
            "command": "bash \".claude/hooks/SESSION-START-DIRECTIVE.sh\"",
            "timeout": 5000
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Edit|Write|MultiEdit",
        "hooks": [
          {
            "type": "command",
            "command": "bash \".claude/hooks/rules-folder-subagent-block.sh\"",
            "timeout": 5000
          }
        ]
      },
      {
        "matcher": "mcp__.*",
        "hooks": [
          {
            "type": "command",
            "command": "bash \".claude/hooks/mcp-pre-check.sh\"",
            "timeout": 5000
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "bash -c 'if [[ \"$FILE_PATH\" == */sessions/*.md ]]; then echo \"[weave] Session file modified -- run /weave --update to rebuild knowledge index\"; fi'",
            "timeout": 5000
          }
        ]
      }
    ],
    "SubagentStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash \".claude/hooks/SUBAGENT-START-DIRECTIVE.sh\"",
            "timeout": 5000
          }
        ]
      }
    ]
  },
  "outputStyle": "Explanatory"
}
```

## Environment

| Key | Value | Purpose |
|:--|:--|:--|
| `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` | `"1"` | Enables the multi-agent team features the framework is built on. |
| `BASH_DEFAULT_TIMEOUT_MS` | `"180000"` | Default Bash timeout (3 min) -- long-compute default for research runs. |
| `BASH_MAX_TIMEOUT_MS` | `"300000"` | Max Bash timeout (5 min) the model may request for a single command. |
| `effortLevel` (top-level) | `"xhigh"` | Maximum reasoning budget for inherently non-trivial orchestration/audit work. |

## Permission Design

### Allow Rules

| Pattern | Purpose |
|:--------|:--------|
| `WebFetch(domain:...)` | Whitelist research-relevant web domains |
| `Bash(timeout:*)` | Allow bash with any timeout (needed for computation) |

Add domain-specific web domains as needed (e.g., `WebFetch(domain:pubmed.ncbi.nlm.nih.gov)` for biomedical research).

### Deny Rules — Security Defaults

IMPORTANT: These deny rules protect against accidental credential exposure. They block reads to common credential paths and destructive git operations.

| Pattern | Protects |
|:--------|:---------|
| `~/.ssh/*`, `~/.aws/*`, `~/.gnupg/*` | SSH keys, AWS credentials, GPG keys |
| `~/.config/gh/*` | GitHub CLI tokens |
| `**/.env`, `**/.env.local` | Environment variable files |
| `**/credentials.json` | Service account credentials |
| `**/.npmrc`, `**/.pypirc` | Package registry tokens |
| `**/secrets.*`, `**/*.pem`, `**/*.key` | Secrets, certificates, private keys |
| `rm -rf *`, `git push --force *` | Destructive operations |
| `git push * main/master` | Direct pushes to protected branches |

### Hooks

The unfold step deploys the scripts in `templates/universal/hooks/` to
`project-root/.claude/hooks/` and wires them here. All run on bare `python`
(stdlib only) -- no virtualenv required. Each is invoked via a project-relative
path (`bash ".claude/hooks/<name>.sh"`), so the deployed project stays portable.

- **`SessionStart`** (matcher `startup|resume|clear|compact`) -- two hooks: an inline "effort: MAX" directive (belt-and-suspenders with `effortLevel: "xhigh"`), and `SESSION-START-DIRECTIVE.sh`, which reminds that a compact/resume starts a fresh context -- read the latest handoff on disk rather than trusting recall.
- **`PreToolUse`** (matcher `Edit|Write|MultiEdit`) -- `rules-folder-subagent-block.sh` HARD-denies subagent edits to `.claude/rules/` (rule files are directive-only; corpus content belongs in the knowledge corpus). The orchestrator is unaffected.
- **`PreToolUse`** (matcher `mcp__.*`) -- `mcp-pre-check.sh` injects a per-server just-in-time brief (knowledge: query-first; paper-search: arXiv API syntax). Discipline packs add their own server arms at the marked extension point.
- **`PostToolUse`** (matcher `Edit|Write`) -- reminds you to run `/weave --update` after editing a session file. A reminder, not an enforced action.
- **`SubagentStart`** -- `SUBAGENT-START-DIRECTIVE.sh` briefs each spawned subagent to read its spawn prompt + cited files and to verify promised artifacts on disk by content (not line count) before reporting done.

## Personal Overrides

`settings.local.json` (gitignored) can override or extend these settings for individual users. Use for:

- Additional web domain whitelists for personal research
- Machine-specific Python paths
- Personal hook preferences
