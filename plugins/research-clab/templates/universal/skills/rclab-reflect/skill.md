---
name: rclab-reflect
description: Reflect on a just-closed wave, plan, session, or document -- what stood out, what was surprising, what patterns cross tests, what the next session should pursue. Summary plus introspection, not description.
argument-hint: <doc(s)> [--append] [--agent <type>] [--voice <role>] [--scope wave|session|plan|custom]
---

# rclab-reflect

## --help

If `$ARGUMENTS` contains `--help` or `-h` (or is empty and the user seems confused), read and display `.claude/rclab-help.md`, then stop. Do not proceed with any other phase.

---

Reflection skill. Reads the full breadth of a task/plan/wave's outputs and produces a structured introspection: what stood out, what was surprising, what pattern connects the gates, what the next session should prioritize. The output sounds like the researcher who did the work, not a project manager who summarized it.

Use this when:
- A `/rclab-solo` or `/rclab-coordinate` wave just closed and you want the reflective pass before the session handoff.
- You want a second look at a filled working paper weeks later -- what did we actually learn?
- You want to review a plan document before dispatching and ask "what's the structurally weightiest bet here?"
- You want to force an agent to articulate the expectation-vs-outcome delta, not just report outcomes.

Do NOT use this for:
- Generating a new synthesis report from raw source docs (use `/rclab-review`).
- Two agents iterating on a shared document (use `/rclab-workshop`).
- Computing anything (use `/rclab-coordinate` or `/rclab-solo`).

## Usage

```
# Reflect on a just-closed wave, append as "Closing Notes" to the WP
/rclab-reflect sessions/session-85/session-85-w10-workingpaper.md --append

# Reflect on a full session (WP + plan + handoff), inline response only
/rclab-reflect sessions/session-85/*.md

# Have a specific agent do the reflection (fresh session)
/rclab-reflect sessions/session-84/session-84-w1-workingpaper.md --agent <agent-type> --append

# Reflect on a plan BEFORE dispatch -- "what's the weightiest bet?"
/rclab-reflect sessions/session-plan/session-86-plan-w3.md --scope plan

# Adversarial voice for a gut-check review
/rclab-reflect sessions/session-85/session-85-w10-workingpaper.md --voice adversarial-skeptic
```

---

## Phase 0: Parse & Validate

### 0a. Extract arguments

Parse `$ARGUMENTS`:

| Arg | Required | Default | Notes |
|:----|:---------|:--------|:------|
| `[doc(s)]` | yes (1+) | -- | Paths or globs to WP / plan / session files (positional, before flags) |
| `--append` | no | false | If set, append the reflection as a `## Closing Notes` section to the PRIMARY document |
| `--agent` | no | calling agent / orchestrator | Spawn a specific agent type for a fresh reflection pass |
| `--voice` | no | `researcher-who-did-the-work` | Voice role: `researcher`, `adversarial-skeptic`, `cross-domain-theorist`, `methodologist`, `empiricist` |
| `--scope` | no | auto-detect | `wave` / `session` / `plan` / `custom` -- influences the reflection prompt below |

### 0b. Validate

1. **Source docs**: Glob-resolve paths. `wc -c` each to verify existence + size them for reading strategy. Report missing and stop.
2. **Primary doc**: The first positional argument is the PRIMARY document (target of `--append` if set). Secondary docs are context.
3. **Agent type** (if `--agent`): Resolve via `.claude/templates/agent-roster.md`. Invalid -> list available and stop.
4. **Voice role**: One of the 5 listed defaults, or free-form -- do not reject unknown voices, just pass them through.

### 0c. Scope auto-detection

If `--scope` not provided, infer:
- Primary doc matches `session-\d+-w\d+-workingpaper.md` -> `wave`
- Primary doc matches `session-\d+-plan-w\d+.md` or `session-\d+-plan.md` -> `plan`
- Primary doc is in `sessions/session-N/` and is not a WP -> `session`
- Otherwise -> `custom`

### 0d. Append-mode pre-check

If `--append`:
- The primary doc MUST be a working paper (has existing section headers, end-of-wave marker, etc.). If not, warn and default to inline.
- Check the primary doc does NOT already contain a `## Closing Notes` section -- if it does, ask: append-new-section / replace-existing / inline-instead / cancel.

---

## Phase 1: Load material fully

This is not a skim-and-summarize skill. The reflection quality is bounded by reading discipline.

1. For EVERY source document:
   - If `size > 30 KB`: chunk-read in `<30 KB` pieces via the `Read` tool's `limit` param. Do NOT skip interior sections.
   - If the doc is a WP: read the verdict blocks, ALL Result subsections, cross-checks tables, plot references, substitution steps. The subsection-level content IS the source of reflection material; section headings alone are not.
   - If the doc is a plan: read every gate block's method, machinery pin, threshold, substitution steps (if present), expected result.
   - If the doc is a session handoff: read every numbered section and every recommendation.

2. Also load:
   - The verdict file for the session (`{{COMPUTATION_DIR}}/session-{N}/s{N}_gate_verdicts.txt`) -- grep for the specific wave or gate prefix.
   - Any producing scripts referenced in the WP if the WP's numerical claims need verification (optional; prefer the WP if scripts add no new signal).

3. Record what you read: a brief internal list of (doc, sections, lines) pairs. This is the "I actually read it" evidence. Do NOT narrate this to the user -- it is private state.

**Anti-pattern check**: if you find yourself reflecting based only on section headings or verdict-line summaries, STOP and re-read the subsection content. The interesting material lives in the subsections, not in tables of contents.

---

## Phase 2: Reflect

The reflection is structured in 4 sections. Output them in this order, in the voice declared by `--voice`:

### §A. What stood out

Anchor every observation to a specific gate, line, or value. Not narrative, not celebration -- observations. For each:
- What was EXPECTED before the gate ran (prior belief, default assumption, the "obvious" outcome)?
- What ACTUALLY happened (verdict, value, specific numerics)?
- Where is the delta, and why does it matter?

Aim for 3-5 observations. Each one should be specifically anchored; "the result came out right" is not an observation, "W1b-4 returned 188.185 against the 188.34 target at 0.082% residual, below the 0.5% threshold, which anchors the model against numerical drift" is.

Force yourself to classify each observation by TYPE:
- **Empirical/Domain surprise**: a numerical value or direction claim that contradicted prior expectation.
- **Structural-pattern surprise**: a structural pattern that emerged from the computation (e.g. a slope-vs-slope balance) but is not itself a domain prediction.
- **Methodological surprise**: a plan-hygiene, infrastructure, or execution issue that surfaced at runtime.
- **Structural surprise**: a deep, theory-class claim (a new result candidate, an invariant relation, a cross-identity link).

If all 5 observations are the same type, push back on yourself -- you are probably missing the other types' signals.

### §B. Cross-gate patterns

The individual gate reports describe themselves, but the wave produces patterns across gates that no single gate report contains. Identify 1-3 cross-gate patterns. Each must connect at least two distinct gates and articulate the pattern explicitly:

- "Gates X and Y both hit the same wall because Z -- the wall is not gate-specific."
- "Gate X's PASS conditions on Gate Y's FAIL: together they constrain the solution space in a way neither alone does."
- "Gates X, Y, Z are 3 instances of the same structural class -- they want a result that unifies them."

If the wave has only one gate, skip this section.

### §C. Highlights for the next session

3-7 actionable items. Each must be specific enough that a plan author could draft a gate block from it directly. Use this schema for each:

> **(N) Title** -- concrete one-line target. Why it matters (links to the observation / pattern that generated it). Effort class (LIGHT / MODERATE / HEAVY). Expected outcome space (what PASS looks like, what FAIL means).

Avoid vague carry-forwards: "further work on X" is not a highlight, "formalize the stabilization claim from §A-2 as a result candidate with an explicit substitution chain -- MODERATE effort -- PASS lands the result in the registry, FAIL refutes the empirical pattern" is.

Classify each highlight by priority signal (priority / EVOI if the project computes one):
- **EVOI high**: the computation's outcome would meaningfully change the framework's state of knowledge regardless of direction.
- **EVOI medium**: the outcome would sharpen an existing claim.
- **EVOI low / filed**: worth noting but not worth funding this session -- filed for future prioritization.

### §D. Wave (or session, or document) signature

One paragraph. Distill the whole thing into a single phrase + one paragraph of justification. Examples of good signature phrases:

- "boundary sharpening, not confirmation"
- "a wall confirmed + two corridors narrowed"
- "structural unification via one emergent result"
- "plan-hygiene failure cascade (3 execution-property breaches)"

Bad signature phrases (anti-patterns):
- "successful wave" / "productive wave" (celebration, not signature)
- "4 PASS 1 FAIL" (tally, not signature)
- "much learned" (vague)

The signature is the one sentence someone who wasn't in the session could carry forward. If you cannot distill to one phrase, the wave does not yet have a signature -- say so explicitly rather than inventing one.

---

## Phase 3: Emit or append

### Inline mode (default)

Output §A, §B, §C, §D directly in the conversation response. No other ceremony.

### Append mode (`--append`)

Append the reflection to the PRIMARY document as a new trailing section, using the format below. Use the `Edit` tool to append after the document's existing terminal marker (e.g. "End of Wave W10 Working Paper.", "End of Session N handoff.", or EOF if no marker).

```markdown
---

## Closing Notes -- {voice} reflection ({DATE})

### What stood out

{§A content}

### Cross-gate patterns

{§B content; omit if only one gate}

### Highlights for {next-scope}

{§C content}

### {scope} signature

{§D content}

---
```

Replace `{voice}` with the `--voice` value (default: `researcher-who-did-the-work`), `{DATE}` with today's ISO date, `{next-scope}` with "next session" for wave-scope, "next wave" for plan-scope, etc.

### Fresh-agent mode (`--agent <type>`)

Spawn the specified agent type as a subagent with:
- `subagent_type`: resolved agent type
- `run_in_background`: false (reflection is synchronous and short)
- `mode`: `acceptEdits` if `--append`; else `default`

Subagent prompt template:

```
You are reflecting on a completed wave / plan / session for the {{PROJECT_NAME}} project.

## Documents to read (in full, no skimming)
{numbered list of source docs with size hints}

Also read your agent memory: `.claude/agent-memory/{your-type}/MEMORY.md` and the project claudeMd at `CLAUDE.md`.

## Voice
Adopt the voice of `{voice}`. This is NOT a project-manager summary. You are the researcher who did the work (or a fresh reviewer reading what was done); articulate what stood out, what connected, what to do next.

## Output structure (mandatory -- 4 sections, in order)

§A. What stood out (3-5 observations, anchored to specific gates/lines, classified as Empirical/Domain / Structural-pattern / Methodological / Structural surprise)
§B. Cross-gate patterns (1-3 patterns connecting >=2 gates; skip if single gate)
§C. Highlights for {next-scope} (3-7 actionable items with title / one-line target / why / effort / outcome space / priority)
§D. {scope} signature (one phrase + one paragraph)

{If --append:}
After composing the 4 sections, append them to `{primary_doc}` as a `## Closing Notes -- {voice} reflection ({DATE})` section using the Edit tool. Do NOT modify any other content in the document.

{If inline:}
Print the 4 sections directly. Do not write any files.

## Rules
- Every observation anchored to a gate, line, value, or artifact.
- No celebration language ("impressive", "great", "successful").
- No restatement of PASS/FAIL counts without structural interpretation.
- Domain framing per the project's framing rule, if one is installed.
- The reflection sounds like the researcher who did the work (or an honest reviewer), not a project manager who summarized it.
```

---

## Rules

1. **Never overwrite existing content** without user confirmation (collision check in Phase 0d).
2. **Read the subsection content, not just headings.** Reflection quality is bounded by reading discipline (Phase 1).
3. **Anchor every observation.** Generic prose is the primary anti-pattern; specific-gate anchoring is the correction.
4. **Never re-adjudicate gate verdicts.** Source doc verdicts are authoritative; reflection interprets, does not relitigate.
5. **Domain framing.** Per the project's framing rule, if one is installed by the discipline pack.
6. **Voice discipline.** If `--voice researcher`, sound like the researcher. If `--voice adversarial-skeptic`, sound like the skeptic. Do not average voices into generic prose.
7. **No celebration language.** "Impressive wave", "productive session", "great result" are banned. The wave is what the wave is; reflection interprets it, does not celebrate it.
8. **No PASS/FAIL tally as signature.** The signature is the ONE SENTENCE interpretation; verdict tallies go in the wave-close report that precedes the reflection, not in the signature.
9. **If the wave has no coherent signature, say so.** Not every wave distills. Inventing a signature where there is none is the fail mode to avoid.

## Anti-patterns (the important part)

These are the failure modes. Watch for them in your own output before finalizing.

| Anti-pattern | Why it fails | Correction |
|:-------------|:-------------|:-----------|
| "Key outcomes: 4 PASS, 1 FAIL" as observation | Tally is summary, not reflection | Anchor to specific gate + numeric + structural interpretation |
| "This was a productive wave" | Celebration, not evaluation | Replace with signature phrase + justification |
| "Further work is needed on X" | Vague; not actionable | Concrete gate block: title / target / why / effort / outcome |
| "Both gates PASSed, consistent with expectations" | No expectation-vs-outcome delta; the observation is vacuous | Either articulate the specific expectation that was confirmed, or drop it |
| Observations all of one type (all empirical, all methodological) | Missing other signal classes | Force classification and push back on yourself |
| Signature = "N PASS M FAIL" | Tally, not interpretation | "Boundary sharpening", "wall confirmed", etc. -- one phrase that's not a count |
| Reflection includes re-verification of gate math | That is proof-check territory, not reflection | Delete; trust the wave's verdicts, interpret them |
| Generic narrative prose ("the session progressed through several gates, each of which addressed...") | Description, not reflection | Replace with anchored observations |
| Missing §C (no carry-forwards) | Reflection without actionable next-step forecloses the sharpening loop | Every reflection produces >=3 highlights with full schema |

## Error Handling

| Condition | Action |
|:----------|:-------|
| No source doc paths | Show usage and stop |
| Source doc missing | Report which, stop |
| Primary doc is not a WP but `--append` set | Warn, default to inline unless user confirms append anyway |
| `## Closing Notes` section already exists in primary doc | Ask: append-new / replace / inline / cancel |
| Agent type invalid (if `--agent`) | List available types, stop |
| Fewer than 1 completed gate in source doc | Warn: reflection is degenerate with no completed work; offer to proceed or cancel |
| Source docs sum > 300 KB | Warn the user; reading will be slow; offer scope-narrowing (wave / session / single-gate) |

## Relationship to other skills

- `/rclab-solo` / `/rclab-coordinate` -- execute the plan. `/rclab-reflect` is the optional post-execution pass.
- `/rclab-review` -- synthesizes source docs into reports (fresh outputs, N agents independently). `/rclab-reflect` interprets a completed body of work (observations, patterns, next-steps), 1 agent.
- `/rclab-investigate` -- generates the next workshop-schedule campaign from a just-closed session. `/rclab-reflect` feeds into `/rclab-investigate` by surfacing the highlights-for-next-session that become the campaign's seed items.
- `/rclab-plan` -- authors the next session's plan. Reflection output in §C maps to plan items: each highlight is a gate-block seed.
- `/weave` -- updates the knowledge index. `/rclab-reflect` does not touch the index; the reflection's structural observations may point at result candidates that `/weave` later registers, but that registration is a separate `/weave` pass.

## Why this skill exists

The compute flow (`/rclab-solo`, `/rclab-coordinate`) produces a structured wave-close report: verdict tallies, constraint-map updates, files-produced tables. That is COMPLETE as bookkeeping and INCOMPLETE as reflection.

The researcher's question -- "what was actually interesting here, and what should I do next?" -- requires stepping out of bookkeeping and into pattern recognition. Most runs of the compute flow will not benefit from this extra pass (the findings are self-describing). But waves that surface structural surprises produce MORE value from a deliberate reflection than from the standard wave-close report alone.

Keeping `/rclab-reflect` separate from `/rclab-solo` lets the user call it judiciously -- only when the wave's content deserves the extra pass -- rather than forcing reflection overhead on every compute dispatch.
