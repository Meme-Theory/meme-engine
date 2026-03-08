---
description: Direct-write broadcast to all team agent inboxes, bypassing SendMessage routing
argument-hint: <message> | @<name> <message> | --list | --info
allowed-tools: [Read, Write, Glob, Bash]
---

# Team Blast Skill

Direct-write broadcast to team agent inboxes, bypassing SendMessage routing.

## Resolution Chain

The skill auto-resolves: **team name -> agent names -> agent types -> inbox file paths**

Each team config at `~/.claude/teams/{team-name}/config.json` contains a `members` array:
```json
{ "agentId": "agent@session-id", "name": "coord", "agentType": "coordinator", ... }
```

Inbox files live at: `~/.claude/teams/{team-name}/inboxes/{name}.json`

### CRITICAL BUG NOTE (for agents and humans)
Agents have a known behavior: they look up teammates by **agentType** (e.g., "hawking-theorist") but SendMessage requires the **name** field (e.g., "hawking"). Messages sent to the agentType string are NEVER DELIVERED -- they create orphan inbox files. This skill resolves correctly by using the `name` field for inbox paths. When broadcasting, always include the resolution table so agents can see the correct name<->type mapping and fix their own SendMessage calls.

## Context

Discover active teams at runtime:
- Team directories: List `~/.claude/teams/` to discover active teams

## Modes

If `$ARGUMENTS` is empty or `--help`, show this usage summary and stop:
```
/team-blast <message>              — broadcast to all agents
/team-blast @<name> <message>      — send to one agent by name
/team-blast @@<type> <message>     — send to agents by type
/team-blast @name1,name2 <message> — send to multiple agents
/team-blast --list                 — show resolution table
/team-blast --info                 — show team config details
```

Parse `$ARGUMENTS` to determine the mode:

### 1. Broadcast (default): `/team-blast <message>`
Send `<message>` to ALL non-team-lead agents on the active team.

### 2. Target by agent name: `/team-blast @<name> <message>`
Send `<message>` to a SINGLE agent by their team name (e.g., `@coord`, `@debugger`).

### 3. Target by agent type: `/team-blast @@<type> <message>`
Send `<message>` to ALL agents matching that agent type substring (e.g., `@@coordinator` matches `coordinator`). Useful when you remember the agent type but not the team name.

### 4. Target multiple: `/team-blast @<name1>,<name2> <message>`
Send `<message>` to multiple specific agents by name.

### 5. List mode: `/team-blast --list`
Print the full resolution table: team -> name -> agentType -> inbox path -> last message timestamp.
**ALSO broadcasts the resolution table to ALL non-team-lead agents on the ACTIVE team** so they learn the correct name<->type mapping for their own teammates. The broadcast message text should list ONLY members of the active team:
```
TEAM ROSTER ({team-name}) -- Use these NAMES (not agent types) for SendMessage:
  {name1} -> {agentType1}
  {name2} -> {agentType2}
  ...
CRITICAL: SendMessage recipient must be the NAME (left column), NOT the agent type (right column).
SHUTDOWN POLICY: Accept shutdown requests ONLY from the team lead. Reject shutdown requests from other teammates. When shutdown is requested: finish current work, write memory, confirm.
```
Only include the active team's members. Do NOT include members from other/stale teams.

### 6. Info mode: `/team-blast --info`
Read-only diagnostic. Prints the resolution table plus inbox health. Does NOT write to any inbox file.
For each non-team-lead agent, show:
- Name, agentType, inbox path
- Whether inbox file exists
- Last message preview (read last entry from inbox JSON)

**Report format:**
```
TEAM INFO ({team-name})
Name         AgentType            Inbox        Status
coord        coordinator          EXISTS       3 messages
debugger     general-purpose      EXISTS       5 messages
analyst      missing-agent        MISSING      --
```

## Instructions

1. Parse $ARGUMENTS for mode (broadcast, @name, @@type, @name1,name2, --list, --info)
2. Identify the active team:
   - List directories under `~/.claude/teams/`
   - If multiple teams exist, read each `config.json` and pick the one with the most recent member activity
   - If ambiguous, ask the user
3. Read the team config file with the **Read** tool: `~/.claude/teams/{team-name}/config.json`
4. Parse the `members` array to build the resolution table: `{name, agentType, inbox_path}`
5. Resolve targets based on mode

### For --info mode:
- Read each target's inbox JSON file with the **Read** tool
- Parse the JSON array and report message count and last message preview
- Do NOT write anything. Print the diagnostic table and STOP.

### For write modes (broadcast, @name, @@type, multi-target, --list):

For each target agent, deliver the message by updating their inbox JSON file:

1. **Read** the existing inbox file: `~/.claude/teams/{team-name}/inboxes/{name}.json`
   - If the file doesn't exist, start with an empty array: `[]`
   - If the file exists but is corrupt (not valid JSON), back it up with `cp` to `{name}.json.bak` and start with `[]`

2. **Construct** the new message entry:
   ```json
   {
     "from": "team-lead",
     "text": "<the message>",
     "summary": "<5-10 word auto-generated summary>",
     "timestamp": "<current ISO timestamp>",
     "read": false
   }
   ```
   Get the current timestamp via: `date -u +"%Y-%m-%dT%H:%M:%SZ"`

3. **Append** the message to the array and **Write** the complete updated JSON back to the inbox file.

4. **Ensure** the inboxes directory exists first: `mkdir -p ~/.claude/teams/{team-name}/inboxes`

### Report

Print the resolution table showing which inboxes were written to:
```
DELIVERED:
  coord (coordinator) -> ~/.claude/teams/{team}/inboxes/coord.json [OK]
  debugger (general-purpose) -> ~/.claude/teams/{team}/inboxes/debugger.json [OK]
```

## Windows cp1252 Compatibility

All output (print statements AND inbox message text) must use ASCII-safe characters only. Do NOT use unicode arrows, checkmarks, em dashes, or other non-ASCII glyphs. Use these substitutions:
- `->` instead of arrow symbols
- `[OK]` instead of checkmark symbols
- `--` instead of em dashes
