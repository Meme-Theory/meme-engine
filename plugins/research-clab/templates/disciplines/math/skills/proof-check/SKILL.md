---
name: proof-check
description: Structural review of a proof or derivation -- checks step justification, variable definitions, limiting cases, dimensional consistency, and canonical-source traceability
argument-hint: <path-to-proof-file> | --section <file>:<section-heading> | --inline
allowed-tools: [Read, Grep, Glob, mcp__knowledge__get_constant]
---

# /proof-check -- Structural Proof Review

This skill performs a **structural** audit of a proof or derivation. It does not prove new theorems, and it does not fix the proof. It flags weaknesses in an existing proof so you can remediate them before the result is registered as canonical.

## Usage

```
/proof-check sessions/session-12/session-12-w1-workingpaper.md
/proof-check --section sessions/session-7/session-7-workshop.md:III.B
/proof-check --inline
```

- `<path>`: read the whole file and extract every claimed proof/derivation block.
- `--section <path>:<heading>`: audit one section only (heading matched case-insensitive, prefix OK).
- `--inline`: the proof text is included later in the same user prompt.

## What this skill checks

For every step of the proof (numbered lines, bullet points, or equation-labeled blocks):

| Check | Pass condition | Fail message |
|:------|:---------------|:-------------|
| **S1. Step justification** | Each step cites (a) a prior step number, (b) a named theorem/lemma, or (c) a definition/axiom. | `"Step N has no justification"` |
| **S2. Variable scope** | Every symbol is introduced before first use, with a declaration or a citation to the canonical reference. | `"Symbol X used before definition"` |
| **S3. Limiting cases** | For any inequality, monotonicity, or bound: degenerate limits (zero, infinity, boundary) are checked or explicitly excluded. | `"Limiting case not verified: X -> 0/inf"` |
| **S4. Dimensional / type consistency** | Every equation's LHS and RHS carry the same units (or, for pure math, the same type/object class). | `"Dimension/type mismatch at step N"` |
| **S5. Canonical-source traceability** | Every named constant or cited value is pulled from the project's canonical module via the knowledge MCP, not hardcoded. | `"Constant X not in the canonical module"` |
| **S6. Substitution chain** | Any sign/direction/threshold claim has an explicit substitution chain (definition -> substitution -> simplification -> direction) per `.claude/rules/substitution-chain.md`. | `"Sign claim at step N lacks substitution chain"` |
| **S7. Sole-source avoidance** | The proof does not rest on agent memory or a single unpublished working paper; if it does, flag PROVISIONAL. | `"Evidence chain rests solely on agent memory"` |

## How to execute this skill

1. **Read the target file**. If `--section` was given, locate the heading with Grep and read that slice only.

2. **Locate proof blocks**. Look for these markers:
   - Explicit `Proof.` / `Q.E.D.` delimiters
   - `Lemma`, `Theorem`, `Proposition`, `Claim` headings followed by a derivation
   - Equation chains where successive lines derive from predecessors
   - Gate-verdict `Substitution chain:` blocks

3. **Enumerate steps**. Split each block into ordered steps. Each equation, sentence, or bullet is a step.

4. **Run the 7 checks**. For each step, emit one row per FAILING check. PASS steps need no row.

5. **Cross-check constants**. For every named constant you find, call the knowledge MCP:
   ```
   mcp__knowledge__get_constant(name=<constant>)
   ```
   If the constant does not exist in the canonical module, flag S5. **If the project has no canonical-constants module** (the knowledge MCP's `get_constant` is disabled — common for purely theoretical projects), S5 is N/A: skip it and note "no constants module — S5 not applicable" rather than flagging every constant.

6. **Produce the report**. Single markdown output with this structure:

   ```
   # Proof check: <file/section>

   ## Summary
   - Steps audited: N
   - Issues found: K  (by severity: BLOCKER=x, MAJOR=y, MINOR=z)
   - Overall verdict: CLEAN | MINOR | MAJOR | BLOCKER

   ## Step-by-step

   | # | Step (first 80 chars) | Check | Severity | Finding |
   |--:|:----------------------|:------|:---------|:--------|
   | 3 | "By monotonicity of f..." | S1 | MINOR | No citation for "monotonicity of f" |
   | 7 | "x -> 0 gives Delta = 0"   | S3 | BLOCKER | Limit x -> 0 not verified -- proof needs finite bound |

   ## Recommended actions
   1. <specific remediation for each BLOCKER/MAJOR>
   2. ...
   ```

## Severity rubric

- **BLOCKER**: the step is wrong OR the proof fails without it. The proof cannot be registered.
- **MAJOR**: the step is plausibly wrong, the justification is circular, or a case is missing. The proof is PROVISIONAL pending rework.
- **MINOR**: cosmetic -- a missing citation for a standard result, unclear notation, a "clearly" that is not clear. The proof stands but should be tightened.

## Do NOT do

- Do NOT try to fix the proof. Only report.
- Do NOT re-derive the substantive math yourself. The check is structural.
- Do NOT run numerical computations unless needed for S3 (limiting cases).
- Do NOT defer a finding with "probably fine". Either call it PASS or flag it with a severity.
