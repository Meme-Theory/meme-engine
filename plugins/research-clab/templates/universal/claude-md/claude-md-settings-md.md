# settings.md — Hook Documentation

<!-- DEPLOY: project-root/.claude/settings.md -->
<!-- Human-readable companion to settings.json explaining each hook and permission. -->

## Hooks

### PostToolUse: Session File Reminder

**Trigger**: Any `Edit` or `Write` operation on files matching `sessions/*.md`

**What it does**: Prints a reminder to run `/weave --update` after modifying session files. The knowledge index is built from session content — edits should be reflected in the index.

**Why**: Session files are the primary input to the knowledge extraction pipeline. Without this reminder, agents frequently forget to rebuild the index after making changes, leading to stale knowledge graph entries.

**Not blocking**: This hook prints a message but does not prevent the edit. The agent must choose to act on the reminder.

## Permissions

### Allowed

| Permission | Rationale |
|:-----------|:----------|
| `WebFetch` on research domains | Agents need access to academic papers and references |
| `Bash(timeout:*)` | Computation scripts may run for extended periods |

### Denied

| Permission | Rationale |
|:-----------|:----------|
| Credential file reads | Prevents accidental exposure of SSH keys, API tokens, secrets |
| `rm -rf`, `git push --force` | Prevents destructive operations that could lose work |
| Direct push to main/master | Enforces branch-based workflow |

## Adding New Hooks

Hooks are defined in `settings.json` under the `hooks` key. Available hook events:

| Event | When It Fires | Common Use |
|:------|:-------------|:-----------|
| `SessionStart` | Session begins or resumes | Load context, check state |
| `UserPromptSubmit` | User submits a prompt | Skill auto-activation |
| `PreToolUse` | Before a tool executes | Block dangerous operations |
| `PostToolUse` | After a tool succeeds | Lint, format, remind |
| `PostToolUseFailure` | After a tool fails | Error logging |
| `Stop` | Claude finishes responding | Final checks |
| `SubagentStart` | Subagent spawned | Logging, tracking |
| `SubagentStop` | Subagent finishes | Cleanup |
| `PreCompact` | Before context compaction | Save critical state |
| `SessionEnd` | Session terminates | Persist memory |

### Hook Types

- **`command`**: Run a shell command. Exit code 0 = proceed, exit code 2 = block.
- **`http`**: POST event data to a URL.
- **`prompt`**: Single-turn LLM evaluation (returns `{ok: true/false, reason: "..."}`).
- **`agent`**: Multi-turn verification with tool access.
