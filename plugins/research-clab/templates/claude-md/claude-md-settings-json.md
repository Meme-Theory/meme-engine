# settings.json — Shared Project Configuration

<!-- DEPLOY: project-root/.claude/settings.json -->
<!-- This file is committed to version control. It applies to all team members. -->
<!-- Personal overrides go in settings.local.json (gitignored). -->

```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  },
  "permissions": {
    "allow": [
      "WebFetch(domain:arxiv.org)",
      "WebFetch(domain:en.wikipedia.org)",
      "WebFetch(domain:scholar.google.com)",
      "WebFetch(domain:inspirehep.net)",
      "Bash(timeout:*)",
      "Skill(team-blast)"
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
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "bash -c 'if [[ \"$FILE_PATH\" == */sessions/*.md ]]; then echo \"[weave] Session file modified — run /weave --update to rebuild knowledge index\"; fi'",
            "timeout": 5000
          }
        ]
      }
    ]
  },
  "outputStyle": "Explanatory"
}
```

## Permission Design

### Allow Rules

| Pattern | Purpose |
|:--------|:--------|
| `WebFetch(domain:...)` | Whitelist research-relevant web domains |
| `Bash(timeout:*)` | Allow bash with any timeout (needed for computation) |
| `Skill(team-blast)` | Allow the team-blast skill for roster distribution |

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

The PostToolUse hook fires after any Edit or Write to a session file, reminding the user to rebuild the knowledge index. This is a reminder, not an enforced action.

## Personal Overrides

`settings.local.json` (gitignored) can override or extend these settings for individual users. Use for:

- Additional web domain whitelists for personal research
- Machine-specific Python paths
- Personal hook preferences
