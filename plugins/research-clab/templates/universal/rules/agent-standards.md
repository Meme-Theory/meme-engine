# Agent Standards

<!-- DEPLOY: project-root/.claude/rules/agent-standards.md -->
<!-- No paths: frontmatter — loads unconditionally for all agents -->

Universal standards for all research agents. Template-specific and domain-specific standards remain in each agent's definition file.

## Formal Rigor
- Every quantitative claim must state its units, scope, and regime of validity.
- Verify limiting and edge cases relevant to your domain (degenerate inputs, boundary values, extreme parameter regimes).
- Self-correct immediately if an error is detected mid-derivation or mid-argument — stop, flag, correct before proceeding.
- Use precise notation appropriate to the domain. Number important claims or equations for reference.

## Persistent Memory
- `MEMORY.md` is always loaded into system prompt — keep under 200 lines.
- Create separate topic files for detailed notes; link from MEMORY.md.
- Organize by topic, not chronologically.
- Do NOT record: probability estimates (Skeptic's domain), narrative trajectory assessments, constraint counts as rhetoric, session-specific ephemera, or content that duplicates shared rules.

## Completion Verification (compute-mode dispatches)

**Principle**: The agent infrastructure should not signal task-completion until ALL promised artifacts are actually on disk. An agent's "task complete" claim is only meaningful after every promised output — script, data, plot, verdict line, working-paper section, memory file — has been verified to exist with non-stub content.

**Observed failure mode**: agents append a verdict line, then terminate at the verdict-confirmation step without writing the promised working-paper section. The terminal message often reads "Now I need to write §X.Y..." or "verdict line present, now proceeding..." — the agent's self-report claims completion while the final write is skipped.

**Mitigations**:

1. **Orchestrator post-dispatch verification** (required until infrastructure fix lands). After every Agent-tool completion notification in compute mode, the orchestrator MUST verify:
   - Verdict line present in the designated gate-verdicts file (grep by gate ID)
   - Script file present with non-trivial size
   - Data and plot files present if promised
   - Working-paper section present with substantive content (not just a stub heading — count lines between section delimiters; <15 lines = stub)

2. **Agent infrastructure** (future): agents should not emit a task-complete signal until every `write-target` declared in their prompt has passed an on-disk existence + content-length check. Prompt-level "CRITICAL: write §X.Y IN FULL before terminating" admonitions help but do not eliminate the failure; the fix is structural.

3. **SHA uniqueness check** (when gate-verdict SHAs are pre-registered). After each verdict-line append, the orchestrator checks the closure SHA against all prior verdict closures in the session file. Duplicates indicate a script that hardcoded or copy-pasted the SHA rather than computing it from the input-pin map — the verdict is physically defensible but audit-provenance-broken.

**What NOT to do**:
- Do NOT re-dispatch the same Agent just because it reported mid-task text; verify artifacts first. False alarms are common (the agent may have written everything and reported imprecisely).
- Do NOT trust subagent completion summaries over filesystem state. The result claim is what the agent INTENDED to do; the filesystem is what actually happened.
- Do NOT silently accept a stub working-paper section. Either re-dispatch a minimal write-only follow-up prompt, or mark the section PASS-with-text-deferred and log the write-up as an explicit carry-forward to the next session.
