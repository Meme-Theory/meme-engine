# sessions/session-{{NN}}/ — Session {{NN}} Workspace

<!-- DEPLOY: project-root/sessions/session-{{NN}}/CLAUDE.md -->
<!-- This is a TEMPLATE. One copy per session directory, with {{NN}} replaced. -->

This directory contains all outputs from Session {{NN}}.

## Required Files

Every session directory must contain:

1. **Main output** — Meeting minutes, computation results, or analysis document
2. **Handoff document** — Summary for the next session (see format below)

## Handoff Document Format

Every session produces a handoff with these 7 sections:

1. **Session metadata** — date, format, agents involved, original prompt
2. **Key results** — numbered, specific, citable
3. **Constraint map updates** — new entries, state changes, closed mechanisms
4. **Open questions** — numbered, actionable, assigned to agents or roles
5. **Action items** — using 7-component format (what, who, input, output, format, deadline, depends-on)
6. **Files created or modified** — full paths
7. **Next session recommendations** — format suggestion, agent composition, focus areas

## File Naming

```
session-{{NN}}-descriptor.md          # Main output
session-{{NN}}-handoff.md             # Handoff document
session-{{NN}}x-descriptor.md         # Sub-session (x = a, b, c...)
```

## Rules

- **One writer per file** — designated writer incorporates all agent contributions
- **No cross-session content** — each session directory is self-contained
- **Cite sources precisely** — paper numbers, file paths, line numbers
- **Gate verdicts are permanent** — once recorded, a gate verdict cannot be retroactively changed
- **Mark preliminary results** — label any claim not yet validated by computation as "PRELIMINARY"
