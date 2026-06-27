---
name: conjecture-index
description: Index the project's open conjectures/propositions -- scans sessions + open-question registers, tabulates with priority (EVOI), origin, related tests, and status
argument-hint: [--status open|closed|all] [--since <session-N>] [--top <N>] [--update]
---

# /conjecture-index -- Open-Conjecture Ledger

Scans the project for stated-but-unproven conjectures, propositions, and hypotheses. Groups them by topic, attaches metadata (origin session, priority/EVOI if computed, related test IDs, current status), and emits a single ledger table.

The point: any research project of size accumulates dozens of informally stated conjectures across session minutes, working papers, and framework docs. Without a periodic sweep they stay scattered. This skill produces a canonical ledger so a planner (or `/rclab-plan`) can prioritize them.

## Usage

```
/conjecture-index                    # all open conjectures, default view
/conjecture-index --status all       # include closed + withdrawn
/conjecture-index --since 80         # only conjectures stated or touched from S80 onward
/conjecture-index --top 15           # top 15 by priority (descending)
/conjecture-index --update           # rebuild the cached ledger at sessions/framework/conjecture-ledger.md
```

## Where conjectures live

| Source | What to scan for |
|:-------|:-----------------|
| `sessions/session-N/*.md` | Headings matching `Conjecture`, `Claim`, `Hypothesis`, `Open Question`, `Open Problem`; bullets under `Open questions`, `Carry-forward`, `OPEN` |
| `sessions/framework/*.md` | Any statement marked `OPEN`, `UNCOMPUTED`, `PROVISIONAL` |
| Project results / permanent registry (if present) | Status-field transitions; watch for `PROVISIONAL` or `pending` |
| Priority register (if present, e.g. `sessions/framework/priority-register.md` or an EVOI table) | The authoritative source for priority/EVOI scores |
| Knowledge index `open_questions` entities | Canonical open-question ledger: `mcp__knowledge__list_entities(type="open_questions")` (if no knowledge MCP, grep `tools/knowledge-index.json` for `"type": "open_questions"`) |
| Knowledge index search | `mcp__knowledge__search_knowledge("conjecture OR hypothesis OR open")` -- full-text across everything (else grep the JSON index) |

## Execution steps

1. **Parse arguments**. Extract `--status`, `--since`, `--top`, `--update` from `$ARGUMENTS`.

2. **Pull authoritative lists first** (these are canonical; everything else is supplementary):
   - `mcp__knowledge__list_entities(type="open_questions")` -- returns all open questions with full metadata (or grep `tools/knowledge-index.json`).
   - Read the project's priority register / EVOI table, if one exists.

3. **Scan session-minute files** (widen the net). Use Grep:
   ```
   Grep pattern="^##+\s*(Conjecture|Claim|Hypothesis|Open\s+Question|Open\s+Problem)" glob="sessions/**/*.md" output_mode="content" -n=true
   ```
   Also scan for bullet-level markers: `- **OPEN**`, `- **UNCOMPUTED**`, `- **CONJECTURE:**`.

4. **Deduplicate**. Many conjectures are restated across sessions; collapse by topic (look for shared test IDs, shared mechanism names, or >70% token overlap in the statement).

5. **Enrich each entry** with the 7-column ledger schema:
   | Column | Source |
   |:-------|:-------|
   | `id` | Open-question ID if present; else a slug derived from the first statement |
   | `statement` | One-sentence summary (<=180 chars) |
   | `origin_session` | Earliest session where stated |
   | `last_touched` | Most recent session that referenced it |
   | `related_tests` | Test / gate IDs (from the knowledge index cross-ref) |
   | `priority` | Priority/EVOI value from the priority register if present; otherwise `--` |
   | `status` | `OPEN` / `IN-PROGRESS` / `CLOSED` / `WITHDRAWN` / `PROVISIONAL` |

6. **Apply filters** (`--status`, `--since`, `--top`).

7. **Emit the ledger** as a single markdown table, sorted by:
   - Primary: priority descending (empty priority last)
   - Secondary: last_touched descending

8. **If `--update`**, write the ledger to `sessions/framework/conjecture-ledger.md` with a timestamp + regeneration command at the top. Otherwise print to stdout.

## Output format

```
# Open-conjecture ledger
- Generated: <ISO date>
- Status filter: open
- Since session: (none)
- Total conjectures: 23
- Authoritative sources: knowledge index open_questions (N=15), priority register (N=18), grep-only hits (N=8)

| # | ID | Statement | Origin | Last | Tests | Priority | Status |
|--:|:---|:----------|:------:|:----:|:------|---------:|:-------|
| 1 | OQ-A-43 | ... | S43 | S80 | ... | 0.81 | OPEN |
| 2 | OQ-B-38 | ... | S38 | S83 | ... | 0.62 | OPEN |
| ... |

## Conjectures with no priority score (N=8)
These have been stated but not yet prioritized. Consider adding to the priority register if any are decision-relevant.
- `<statement>` (S74, no test link)
- ...

## Regeneration
- Cached at: `sessions/framework/conjecture-ledger.md`
- Rebuild: `/conjecture-index --update`
- Sole authority for status transitions: see `.claude/rules/gate-verdicts.md`
```

## Guard rails

- **Do NOT** invent conjectures. If a bullet says "could this be X?", that is a question, not a conjecture -- skip unless the session explicitly labels it.
- **Do NOT** copy long statements verbatim. Summarize to <=180 chars.
- **Do NOT** promote a conjecture to CLOSED based on agent-memory claims. Per `.claude/rules/epistemic-discipline.md` + `.claude/rules/gate-verdicts.md`, only the canonical sources (the knowledge index's closed/results entities, gate-verdict files, synthesis docs) can close a conjecture.
- **Do** flag provisional/withdrawn entries distinctly -- they're useful for the "why we gave up on X" history.
- **Do** preserve priority/EVOI scores exactly from the priority register -- never recompute.
