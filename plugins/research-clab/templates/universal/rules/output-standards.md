# Output Standards

<!-- DEPLOY: project-root/.claude/rules/output-standards.md -->
<!-- No paths: frontmatter — loads unconditionally for all agents -->

## Action Items Format

Every action item must include all 7 components:

1. **What** — the specific deliverable
2. **Who** — which agent or role
3. **Input** — what they need to start
4. **Output** — what they produce
5. **Format** — file type and location
6. **Deadline** — session or phase
7. **Depends on** — prerequisite action items

## Handoff Documents

Every session produces a handoff document with these 7 sections:

1. Session metadata (date, format, agents, prompt)
2. Key results (numbered, specific)
3. Constraint map updates (new entries, state changes)
4. Open questions (numbered, actionable)
5. Action items (using 7-component format above)
6. Files created or modified (paths)
7. Next session recommendations

## General Output Rules

- **Mark preliminary results** — label any claim not yet validated by computation as "PRELIMINARY"
- **Cite sources precisely** — paper numbers, file paths, line numbers
- **One writer per file** — designated writer only; others contribute via messages
- **Gate verdicts are permanent** — once recorded, a verdict cannot be retroactively changed
- **No filler** — avoid "as we can see," "it's worth noting," "interestingly"
