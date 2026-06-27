# Double-Check Logic Before Compute -- Substitution Chain

<!-- DEPLOY: project-root/.claude/rules/substitution-chain.md -->
<!-- No paths: loads unconditionally for all agents -->
<!-- Source: extracted from parent .claude/rules/math-scripts.md §"Double-Check Logic Before Compute" -->

Applies to orchestrators and agents alike.

Before running any compute OR stating any claim involving a **sign, direction, threshold, or ratio**, write the **substitution chain** explicitly. No "obviously from structure" shortcuts.

## Required structure for sign/direction/threshold claims

1. **State the definition of each quantity** involved (what is `x`? what is `F`? what is `c`?). Cite the canonical-constants source or the defining equation.
2. **Write the substitution step** -- plug definitions into the target expression, no simplification yet. Every symbol explicit.
3. **Simplify to canonical form** -- algebra, not narrative. One step per line.
4. **Read off the direction from the canonical form** -- only then state the sign/direction/threshold.

## Example

```
Claim: "c = 2.23 suppresses F under hypothesis H."

Required substitution chain:
  Step 1: z(N, k) = a(N) * sqrt(2*epsilon) * M_eff(k)     [definition of z]
  Step 2: F(k)   = |v_k|^2 / z(N, k)^2                [definition of F]
  Step 3: c       = M_eff(k_pivot)^2 / M_eff(0)^2     [definition of c]
  Step 4: Substitute:
          F(k_pivot) / F(0)
        = [|v|^2 / z(k_pivot)^2] / [|v|^2 / z(0)^2]
        = z(0)^2 / z(k_pivot)^2
        = 1 / c                                       [simplified]
  Step 5: c > 1  =>  F(k_pivot) < F(0)                [direction from canonical form]
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

## Mnemonic-vs-exact ratio discipline

When citing a reduction factor, band-narrowing, or any ratio derived from a general identity, do NOT use a convenient mnemonic-form shortcut (e.g. `1/c_X`, `c_X^{-2}`) without an explicit cross-check against the structurally-exact form. Mnemonics propagate downstream; a misused mnemonic mis-publishes downstream observables.

**Structural reason**: a mnemonic of the form `1/c_X` implicitly assumes BOTH numerator and denominator scale by `1/c_X` under the relevant hypothesis switch. When only ONE side shifts (the test quantity) while the other (the reference quantity) is INVARIANT, the true ratio is bounded BELOW `1/c_X`. The mnemonic and the exact form diverge in proportion to that asymmetry.

**Discipline**:

1. When a ratio "looks like" a known convenient form, derive the structurally-exact form by writing out the substitution chain (the 4-step structure above).
2. Cross-check the mnemonic against the exact form symbolically (e.g. via the `sage` MCP / `/sage-compute`) when float arithmetic loses precision.
3. If mnemonic and exact form disagree by `>= 1%` relative deviation, USE THE EXACT FORM in registry text and the canonical module. Relegate the mnemonic to a "first-order approximation" footnote.
4. Document the structural reason for the asymmetry in the registry text (e.g. "reference quantity INVARIANT under the hypothesis switch; only the test quantity shifts; ratio bounded below `1/c_X`").

## Selection-rule pre-flight (center-character / quantum-number admissibility)

Any substitution chain claiming that a matrix element `<a| O |b>` between named symmetry sectors is "generically nonzero" (or asserting it "connects" the sectors) MUST carry a selection-rule admissibility check at plan-freeze, BEFORE the gate is pinned:

1. **State the conserved quantum numbers / center characters** of the bra `a`, the ket `b`, and the operator `O`. (For an SU(3) example, the relevant label is the triality/center character `t(p,q) = (p - q) mod 3`; a squared modulus `|f|^2` is always center-character 0 regardless of the content of `f`.)
2. **Verify admissibility** -- the trivial representation must occur in `conj(a) (x) O (x) b` (for the SU(3) center-character form: `t(a) == t(b) + t(O) (mod 3)`). The check is NECESSARY only: a passed check does NOT certify the element nonzero; a FAILED check proves it EXACTLY zero.
3. **Mismatch routing** -- a failed check means the "generically nonzero" claim is group-theoretically inadmissible. Revise the gate block at plan-freeze: re-anchor to the admissible operator, or declare the derived form with its derivation cited. Never carry a selection-rule-forbidden matrix element into a pinned gate.

This generalizes to any project with a conserved charge / quantum number / center character: confirm admissibility before claiming a nonzero coupling, transition, or overlap.

## Enforcement

- A pre-tool hook may inject a reminder before every `Bash | Edit | Write` tool call. The chain requirement applies regardless of adaptive reasoning routing.
- An orchestrator who states a direction claim without a visible substitution chain in the same response is violating this rule -- the user may call this out as a trigger pattern.
- Agents generating plan documents must include `[SIGN]`, `[VERIFY]`, or `[AUDIT]` trigger-phrase prefixes on pre-registered gates that require the chain.
