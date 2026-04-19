# Double-Check Logic Before Compute — Substitution Chain

<!-- DEPLOY: project-root/.claude/rules/substitution-chain.md -->
<!-- No paths: loads unconditionally for all agents -->
<!-- Source: extracted from Ainulindale Exflation .claude/rules/math-scripts.md §"Double-Check Logic Before Compute" -->

Applies to orchestrators and agents alike.

Before running any compute OR stating any claim involving a **sign, direction, threshold, or ratio**, write the **substitution chain** explicitly. No "obviously from structure" shortcuts.

## Required structure for sign/direction/threshold claims

1. **State the definition of each quantity** involved (what is `x`? what is `F`? what is `c`?). Cite the canonical-constants source or the defining equation.
2. **Write the substitution step** — plug definitions into the target expression, no simplification yet. Every symbol explicit.
3. **Simplify to canonical form** — algebra, not narrative. One step per line.
4. **Read off the direction from the canonical form** — only then state the sign/direction/threshold.

## Example

```
Claim: "c = 2.23 suppresses F under hypothesis H."

Required substitution chain:
  Step 1: z(N, k) = a(N) · sqrt(2·ε) · M_eff(k)     [definition of z]
  Step 2: F(k)   = |v_k|² / z(N, k)²                [definition of F]
  Step 3: c       = M_eff(k_pivot)² / M_eff(0)²     [definition of c]
  Step 4: Substitute:
          F(k_pivot) / F(0)
        = [|v|² / z(k_pivot)²] / [|v|² / z(0)²]
        = z(0)² / z(k_pivot)²
        = 1 / c                                       [simplified]
  Step 5: c > 1  ⇒  F(k_pivot) < F(0)                [direction from canonical form]
  Conclusion: c = 2.23  SUPPRESSES F.                 [only now valid]
```

## When the chain is MANDATORY

- Any assertion containing: "increases", "decreases", "suppresses", "amplifies", "widens", "narrows", "dominates", "larger than", "smaller than"
- Any sign, direction, or threshold claim in a workshop Wrap-Up or synthesis section
- Any claim about whether a parameter being `> 1` (or `< threshold`, etc.) changes an observable in a specific direction
- Any factor-counting or order-of-magnitude estimate used to decide a PASS/FAIL

## When the chain is NOT required

- Definitions-only statements (no direction claim)
- Citing prior results from the canonical registry verbatim (no new derivation)
- Running pre-registered pipelines where the direction is an OUTPUT, not a claim

## Enforcement

- A pre-tool hook may inject a reminder before every `Bash | Edit | Write` tool call. The chain requirement applies regardless of adaptive reasoning routing.
- An orchestrator who states a direction claim without a visible substitution chain in the same response is violating this rule — the user may call this out as a trigger pattern.
- Agents generating plan documents must include `[SIGN]`, `[VERIFY]`, or `[AUDIT]` trigger-phrase prefixes on pre-registered gates that require the chain.
