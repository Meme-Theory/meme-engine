# Session Format Selection Guide

## Decision Tree

Use this decision tree to pick the right format:

```
Is this the FIRST session on a new topic?
  YES → Format A: First Contact Review
  NO ↓

Do you need to STRESS-TEST claims from a prior session?
  YES → Format B: Adversarial Debate
  NO ↓

Do you need a COMPUTATION SPECIFICATION for a single problem?
  YES → Format C: Collaborative Deep-Dive
  NO ↓

Do you need STRUCTURED DELIBERATION across multiple topics?
  YES → Format D: Workshop
  NO ↓

Is this a MULTI-DAY investigation with dependency ordering?
  YES → Format E: Investigation Arc
  NO ↓

Is there a SINGLE DECISIVE computation to execute?
  YES → Format F: Decisive Computation
  NO ↓

Do you have RESULTS that need review by many agents?
  YES → Format G: Mass Parallel Assessment
  NO ↓

Does the NEXT SESSION depend on a binary outcome?
  YES → Format H: Decision Gate
  NO ↓

Do you need to CONSOLIDATE prior sessions into a status document?
  YES → Format I: Formalization
```

## Skill Quick Reference

| Format | Primary Skill | Mode/Args | Notes |
|:-------|:-------------|:----------|:------|
| A. First Contact | `/clab-review` | `--agents` subset or full roster | Fan-out, no live team needed |
| B. Adversarial Debate | `/clab-team` | `--mode panel` | Pre-assign adversarial postures in prompt |
| C. Deep-Dive | `/clab-team` | `--mode panel` (spec) or `--mode compute` (code) | Panel for specification, compute for execution |
| D. Workshop | `/clab-team` | `--mode workshop` | One invocation per round, or single prompt with all rounds |
| E. Investigation Arc | `/clab-team` | `--mode compute` per phase, `--mode panel` for final | Gate check between invocations |
| F. Decisive Computation | `/clab-team` | `--mode compute` | Wrap-up as separate `--mode panel` invocation |
| G. Mass Parallel Assessment | `/clab-review` | Full roster, then cross-evals | Master collab via `--mode panel` |
| H. Decision Gate | `/clab-team` | `--mode compute` | Human reads verdict, picks next branch |
| I. Formalization | `/clab-team` + `/clab-review` | `--mode panel` → mass review | Panel catalogs, review validates |

**Rule of thumb**:
- **Need independent reviews?** → `/clab-review`
- **Need live coordination?** → `/clab-team`
- **Need scripts to run?** → `--mode compute`
- **Need discussion to converge?** → `--mode panel`
- **Need sequential rounds?** → `--mode workshop`

## Format Combinations

Sessions often combine formats within a single session or across sub-sessions:

| Combination | Example | Skill Sequence |
|:-----------|:--------|:--------------|
| Decision Gate → Decisive Computation | Sessions 20a → 20b | `clab-team --mode compute` → check verdict → `clab-team --mode compute` |
| Decisive Computation → Mass Parallel Assessment | Sessions 18 → 19d | `clab-team --mode compute` → `clab-review` (full roster) |
| Investigation Arc with Workshop sub-session | Session 25 | `clab-team --mode compute` (phases) → `clab-team --mode workshop` (one phase) |
| Formalization → Workshop | Sessions 15 → 16 | `clab-team --mode panel` → `clab-team --mode workshop` |
| First Contact → Adversarial Debate → Deep-Dive | Sessions 1 → 5 → 6 | `clab-review` → `clab-team --mode panel` → `clab-team --mode panel` |
| Compute → Review → Synthesize | Sessions 28a → 28-review → 28-fusion | `clab-team --mode compute` → `clab-review` → `clab-team --mode panel` |

## Format Evolution Timeline

Formats emerged in this order, each solving a failure mode of the previous:

| Session | Innovation | Failure Mode Solved |
|:--------|:----------|:-------------------|
| 1 | Fan-out parallel review | Single-assessor framing bias |
| 2 | Epistemological reframing | Hidden assumptions in first-pass critique |
| 5 | Adversarial debate with concessions log | Diplomatic smoothing hiding real disagreements |
| 6 | Computation specification with dependency graph | Assessment without executable next steps |
| 8 | Format declaration in opening header | Ambiguous session structure |
| 11 | Unanimous verdict with per-agent thumbs-up | Unclear group consensus mechanism |
| 13 | Convergence map tracking cross-session evolution | Losing track of how conclusions changed |
| 15 | Formalization with fixed taxonomy | Scattered knowledge, retroactive interpretation |
| 16 | Multi-round Workshop with orchestration state | Context explosion, unproductive large-group discussion |
| 17 | Investigation Arc with phased gating | Premature execution of expensive computation |
| 18 | Decisive Computation sprint | Overhead on simple computations |
| 19 | Mass Parallel Assessment with cross-evaluation | Missing cross-domain connections |
| 20 | Decision Gate with binary routing | Ambiguous session scope when outcome is uncertain |
| 21 | Bifurcated teams (interpret vs. compute) | Single-team conflating interpretation and execution |
| 22 | Session index for arc-level planning | Inability to plan parallel sub-sessions |
| 24 | Real-time gate classification during computation | Post-hoc interpretation of numbers |
| 25 | Pre-collab directive before workshop | Workshop starting without sufficient preparation |
| 26 | Plan scrub report | Plans not updated after first results invalidate premises |
| 28 | Constraint chains with conditional branching | Flat gate lists missing dependency structure |
| 29 | Pre-session gate checkpoint protocol | Sub-sessions running despite upstream hard closes |

---

## Quick Reference: Session Format Cheat Sheet

| Format | Skill | Mode | Team | Duration | Key Output |
|:-------|:------|:-----|:-----|:---------|:-----------|
| A. First Contact | `/clab-review` | — | 4-17 | 1-2 sessions | Multi-lens assessment |
| B. Adversarial Debate | `/clab-team` | `panel` | 3-5 | 1 session | Concessions + settling computations |
| C. Deep-Dive | `/clab-team` | `panel`/`compute` | 3-5 | 1 session | Computation specification |
| D. Workshop | `/clab-team` | `workshop` | 6-10 | 1-2 sessions | Ranked action items with specs |
| E. Investigation Arc | `/clab-team` | `compute`×N | 3-5/phase | Multi-session | Phased deliverables with gates |
| F. Decisive Computation | `/clab-team` | `compute` | 2-3 | Hours | Gate verdict |
| G. Mass Parallel Assessment | `/clab-review` | — | 8-17 | 1-2 sessions | Synthesis + master collab |
| H. Decision Gate | `/clab-team` | `compute` | 2-3 | Hours | Binary routing verdict |
| I. Formalization | both | `panel` → review | 4-6 | 1 session | Status document |
