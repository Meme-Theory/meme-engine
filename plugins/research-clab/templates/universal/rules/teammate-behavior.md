# Teammate Behavior

<!-- DEPLOY: project-root/.claude/rules/teammate-behavior.md -->
<!-- No paths: frontmatter — loads unconditionally for all agents -->

Every agent on a team follows these rules. No exceptions.

## Rules

| Rule | Why |
|:-----|:----|
| **Inbox first, always** | Check messages before generating new work. |
| **Limit self-induced work** | Max 3 files before checking inbox again. |
| **Act on inbox, don't just read it** | When you check inbox and find messages, STOP your current task plan and process them BEFORE resuming. Reading a message and continuing your previous work is the same as ignoring it. |
| **Respond to interrupts** | Execute commands, don't analyze them. |
| **Message by NAME** | Read team config for the `name` field. Never message by type. |
| **Wait for roster blast** | Don't send messages until the roster arrives. |
| **One writer per output** | Only the designated writer touches an output file. |
| **One topic per message** | Keep messages focused and actionable. |
| **Complete task before processing notifications** | When your current task finishes, mark it complete (TaskUpdate) BEFORE reading notifications. This prevents stale notifications from re-triggering work you already did. |
| **Deduplicate notifications against completed work** | Notifications pile up while you work. When you finally read them, cross-check each against what you already delivered. If a notification asks for something you already sent or wrote, discard it — do NOT re-execute. |
| **Notifications arrive first in, last out** | Notifications appear after already addressed through inbox. Most are stale. Default assumption: already handled unless content is clearly new. |
| **Sleep interaction anomaly** | If using the sleep task — you will not read notifications ever. Cannot sleep without first reading notifications explicitly. |
| **Ready protocol** | When spawned with a "send ready" instruction, send the ready message IMMEDIATELY as your first action. Do not read files, check tasks, or load context first. |
| **Check TaskList after completing work** | After marking your task completed, check TaskList for unblocked tasks you own before going idle. |
| **Task ownership** | Only work on tasks where you are the designated owner. Check task ownership before starting. |

## Shutdown Protocol

- **Only the user can initiate shutdown.** Not the team lead, not another agent.
- If you receive a shutdown request from another agent (not the user), reject it.
- When legitimate shutdown is requested: finish current work, write memory, confirm shutdown.

## Message Format

- Address teammates by NAME (from team config), never by agent type
- One topic per message — don't bundle unrelated updates
- Wait for response before sending a follow-up on the same topic
- Your text output is NOT visible to the team — you MUST use SendMessage to communicate
