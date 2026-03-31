# Framework Evidence & Probability Methodology

<!-- DEPLOY: project-root/.claude/rules/evoi-prioritization.md -->
<!-- No paths: frontmatter — loads unconditionally for all agents -->

How to assess the framework's status, prioritize computations, and weight evidence. The living EVOI priority table is at `sessions/framework/evoi-framework.md` — check it before proposing new computations.

## Computation Priority (EVOI)

EVOI (Expected Value of Information) determines what to compute next:

EVOI = P(pass) × |delta_P(pass)| + P(fail) × |delta_P(fail)|

The computation with the highest EVOI gets priority. This tells you where to SPEND WORK.

## Evidence Weighting

- **Observational passes** are weighted by prior predictive range / posterior width. A Higgs mass within 7% from zero geometric free parameters across a 5-OOM prediction space has BF ~ 1000, not 2.
- **Failures cluster by TOPIC**. Four agents hitting the same truncation wall = ONE methodological finding. Three CC mechanisms failing = ONE open problem with three eliminated approaches.
- **Eliminating wrong mechanisms STRENGTHENS surviving paths.** A framework that has tested and closed 25 wrong mechanisms is stronger than one that has tested none.
- **Joint probability matters.** The chance of one random geometry producing multiple independent observational matches is the PRODUCT of individual probabilities, not the arithmetic mean.

## Effort-Based Probability

The framework probability is tracked as: (mechanism links complete / total) × (fraction approaching observation). This goes UP when work is done, not only when favorable results return.
