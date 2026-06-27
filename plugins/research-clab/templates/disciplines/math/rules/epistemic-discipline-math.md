# Epistemic Discipline (Math)

<!-- DEPLOY: project-root/.claude/rules/epistemic-discipline.md (OVERRIDES universal) -->
<!-- No paths: frontmatter — loads unconditionally for all agents -->

How to reason about the project's framework: what counts as a result, what does not, how to weight evidence, how to report progress.

## Source Authority Hierarchy

1. Formally-verified proof artifacts (Lean, Coq, Isabelle output)
2. DETAILED proofs in the project's session files or published papers
3. Skeptic verdicts in the project knowledge base
4. SKETCH proofs (noted as such)
5. Computer-algebra or numerical examples
6. Heuristic arguments / physical intuition / analogy
7. Conjectures awaiting proof

A lower item does not override a higher item. A heuristic that matches a detailed proof is corroborating, not primary.

## Evidence Hierarchy

1. **Proven theorems** are permanent. A DETAILED or FORMALLY-VERIFIED proof closes the question at its stated scope. Report them as geometry: "Under hypotheses H, X is impossible." They survive regardless of framework fate.

2. **Verified cases and constructed counterexamples** are decisive within their scope. A concrete counterexample falsifies a conjecture definitively. A verified small case establishes that the conjecture at least holds on that case.

3. **Heuristic arguments and analogies** are useful for direction but NOT evidential. "This should follow from the analogy with X" is a PROPOSED LEMMA, not a theorem. Report as: "Heuristic: ..., formal verification pending."

## How to Assess a Conjecture

A conjecture lives or dies on its **structural position** in the mapped proof landscape:

- What prior theorems entail it?
- What small-case and boundary checks has it survived?
- What counterexamples have been tried and failed?
- What proof strategies have been attempted, and where did each block?

A conjecture with many failed counterexample attempts, survival of all small cases, and multiple partial proofs from independent angles is strongly supported — but is not a theorem. Report it as OPEN with the supporting evidence attached.

## Pre-Registration

Before beginning a proof attempt:

- State the conjecture precisely (scope, premises, conclusion)
- State the proof strategy (induction, contradiction, construction, reduction to known theorem X)
- State the proof obligations the strategy will generate
- State what a SUCCESSFUL proof closes and what it leaves open

Post-attempt, compare to the pre-registered structure. A proof that "worked but via a different strategy" is still a valid result — but note the divergence. Unpre-registered proofs are accepted, but the surprise is recorded (it may signal a more general pattern).

## Reporting Format

Do not state subjective probabilities of open problems. Report:

- What is proven, with rigor level
- What is conjectured, with supporting and refuting evidence
- What is open, with priority and related results
- What was ruled out, with the counterexample or impossibility argument

The constraint map IS the assessment.

## Do Not

- Do not state a theorem without a cited proof
- Do not use "it can be shown" in a DETAILED result
- Do not promote a SKETCH to DETAILED without writing out the steps
- Do not cite a theorem outside its scope without a scope-extension argument
- Do not treat heuristic / physical / analogical reasoning as a proof
- Do not state percentage probabilities of a conjecture being true — the evidence map IS the assessment
