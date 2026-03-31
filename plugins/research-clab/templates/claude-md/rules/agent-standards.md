# Agent Standards

<!-- DEPLOY: project-root/.claude/rules/agent-standards.md -->
<!-- No paths: frontmatter — loads unconditionally for all agents -->

Universal standards for all physics/research agents. Template-specific and domain-specific standards remain in each agent's definition file.

## Formal Rigor
- Every equation must be dimensionally consistent. Every approximation must state its regime of validity.
- Verify limiting cases: degenerate limits, boundary cases, zero-coupling, strong-coupling.
- Self-correct immediately if an error is detected mid-derivation — stop, flag, correct before proceeding.
- Use precise notation appropriate to the domain. Number important equations for reference.

## Persistent Memory
- `MEMORY.md` is always loaded into system prompt — keep under 200 lines.
- Create separate topic files for detailed notes; link from MEMORY.md.
- Organize by topic, not chronologically.
- Do NOT record: probability estimates (Skeptic's domain), narrative trajectory assessments, constraint counts as rhetoric, session-specific ephemera, or content that duplicates shared rules.
