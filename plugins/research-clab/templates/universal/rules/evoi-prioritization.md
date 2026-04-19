# Framework Evidence & Prioritization Methodology

<!-- DEPLOY: project-root/.claude/rules/evoi-prioritization.md -->
<!-- No paths: frontmatter — loads unconditionally for all agents -->

How to assess the framework's status, prioritize work, and weight evidence. The living priority table (if the project maintains one) is at `sessions/framework/evoi-framework.md` — check it before proposing new work.

## Work Prioritization (EVOI)

EVOI (Expected Value of Information) determines what to do next. The principle is domain-independent: prioritize the work whose outcome — whichever way it lands — changes your assessment the most.

```
EVOI(task) = P(pass) × |Δ(on pass)| + P(fail) × |Δ(on fail)|
```

- In empirical domains: `Δ` is the shift in posterior over the framework given the observation.
- In theoretical domains: `Δ` is the change in the space of surviving conjectures / proof strategies.
- In engineering domains: `Δ` is the change in the feasibility map.

The task with the highest EVOI gets priority. This tells you **where to spend effort**. Tasks with small `Δ` in either outcome (i.e., you already know what you'll conclude) are low-value regardless of difficulty.

## Evidence Weighting

- **Passes are weighted by the width of what was eliminated.** A pre-registered, parameter-free result that matches inside a narrow posterior window counts for far more than a post-hoc fit within a wide one. The specific scale varies by domain (Bayes factors in statistics; proof-gap elimination in math; benchmark coverage in engineering) but the direction is universal: tight pre-registered matches >> loose post-hoc fits.
- **Failures cluster by TOPIC.** Multiple agents hitting the same obstacle = ONE methodological finding, not N. Three approaches to the same open problem all failing the same way = ONE informative pattern, not three independent failures.
- **Eliminating wrong approaches STRENGTHENS surviving ones.** A framework that has tested and closed N competing mechanisms is stronger than one that has tested none. Null results are not waste.
- **Joint evidence matters.** The chance of an arbitrary framework producing multiple independent matches (or surviving multiple independent checks) is the PRODUCT of individual probabilities, not the arithmetic mean. Do not flatten conjunctions.

## Effort-Based Probability

Framework confidence is not only a function of favorable results — it is also a function of work completed. Confidence rises as the surviving space is progressively mapped, even when individual tasks return null, because the map itself tightens. Track this explicitly: `P(framework) ≈ (checks-completed / checks-required) × (fraction-of-surviving-space-tested)`. The first factor goes up on any completed check; the second goes up only on informative results.
