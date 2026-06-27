# Counterexample Before Conjecture

<!-- DEPLOY: project-root/.claude/rules/counterexample-before-conjecture.md -->
<!-- No paths: frontmatter — loads unconditionally for all agents -->

Before asserting a claim holds *in general*, search small / degenerate / boundary cases for a counterexample. This rule exists to prevent the recurring failure mode of stating a conjecture whose small-case counterexample is visible in twenty minutes of work.

## The Rule

When an agent is about to state a claim of the form "for all X in class C, P(X) holds":

1. **Enumerate small cases**. What are the minimal or degenerate members of C? (Often: the zero object, the one-element case, the boundary case, the generic case, the pathological case.)
2. **Check P directly on each**. Write out the check — not "it is clear that P holds for the trivial case."
3. **Only then state the conjecture**. If P passes all checks, state the conjecture with the checked cases listed as corroborating evidence.
4. **If any check fails**, either (a) narrow the scope of the claim to exclude the counterexample's class, or (b) abandon the claim.

## Enumeration Checklist

At minimum, check:

- **Zero / empty case** — does the claim hold when the object is trivial?
- **One-element / one-dimensional case** — does it hold in the smallest non-trivial instance?
- **Degenerate case** — does it hold when a parameter is at the boundary of its range?
- **Known pathological objects** — if the field has a canonical pathological example (Peano curve, Cantor set, Weierstrass function, etc.), does the claim survive it?
- **Random / generic case** — does it hold for an arbitrary example, not a specially-constructed one?

Not every check is relevant to every claim. But document which checks were done. An undocumented claim is an unchecked claim.

## Prior-Art Check

Before stating a conjecture, also check:

1. `/weave --show conjectures` — has the project already recorded this conjecture?
2. `/weave --show counterexamples` — has the project already recorded a counterexample against this or a close variant?
3. The `researchers/` corpus — is this conjecture a known folklore open problem, or has a standard counterexample been published?

A conjecture that has already been refuted in the literature wastes the team's attention.

## Reporting Format

When stating a conjecture after the check:

```
Conjecture C-N (status: OPEN):
  Statement: For all X in class C, P(X).
  Small-case checks performed:
    - Zero case: PASSES (derivation: ...)
    - One-element case: PASSES (derivation: ...)
    - Generic case: PASSES (example: ...)
    - Boundary case: PASSES (argument: ...)
  Prior-art check:
    - No matching conjecture in project knowledge base
    - Related to L-4 (but L-4's scope is strictly narrower)
  Approaches tried: [none yet / list]
```

This format makes it trivial for the next session to pick up the conjecture without re-doing the groundwork.
