# Framework Evidence & Probability Methodology — Physics Override

<!-- DEPLOY: project-root/.claude/rules/evoi-prioritization.md -->
<!-- No paths: loads unconditionally for all agents -->
<!-- Source: extracted from Ainulindale Exflation .claude/rules/evoi-prioritization.md -->
<!-- Overrides: universal/rules/evoi-prioritization.md -->

How to assess the framework's status, prioritize computations, and weight evidence. The living EVOI priority table is at `sessions/framework/evoi-framework.md` — check it before proposing new computations.

## Computation Priority (EVOI)

EVOI (Expected Value of Information) determines what to compute next:

```
EVOI = P(pass) × |Δ_P(pass)| + P(fail) × |Δ_P(fail)|
```

The computation with the highest EVOI gets priority. This tells you **where to spend work**. Computations with small `Δ_P` in either outcome (i.e., you already know what you'll conclude) are low-value regardless of their technical difficulty.

## Evidence Weighting

- **Observational passes are weighted by prior predictive range / posterior width.** A parameter-free prediction that matches an observation within a narrow tolerance across a wide prior space counts for far more than a post-hoc fit within a wide posterior. Example pattern: an {{OBSERVABLE}} predicted within {{TIGHT_TOLERANCE}} from zero geometric free parameters across a {{N}}-OOM prediction space gives a Bayes factor of order 10³, not 10⁰. Record the tolerance and prior width explicitly so the BF calculation is auditable.
- **Failures cluster by TOPIC.** Four agents hitting the same truncation wall = ONE methodological finding. Three candidate mechanisms failing on the same structural constraint = ONE open problem with three eliminated approaches, not three independent data points.
- **Eliminating wrong mechanisms STRENGTHENS surviving paths.** A framework that has tested and closed N candidate mechanisms is stronger than one that has tested none. Null results are not waste; they narrow the solution space.
- **Joint probability matters.** The chance of one random geometry producing multiple independent observational matches is the **product** of individual probabilities, not the arithmetic mean. Do not flatten conjunctions of independent matches into an average.

## Effort-Based Probability

The framework probability is tracked as:

```
P(framework) ≈ (mechanism links complete / total) × (fraction approaching observation)
```

This goes **UP** when work is done, not only when favorable results return. The first factor rises on any completed mechanism link; the second factor rises only on informative (predictive-match) results.

## Trajectory Tracking

This pack's knowledge schema includes a `trajectory` entity type (see `knowledge-schema.yaml`). Each entry is a single evidence-accumulation event — a gate PASS, a closure, a predictive match, a pre-registered parameter-free observable hit. The EVOI assessment draws from the trajectory: a framework whose trajectory shows N parameter-free predictive matches across independent observables carries joint evidence that the individual-match reports do not.
