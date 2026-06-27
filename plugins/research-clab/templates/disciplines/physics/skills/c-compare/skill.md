---
name: c-compare
description: Classify a framework event, observable, or object as PROPAGATION (c-bounded, lives on g_M), SUBSTRATE DYNAMICS (not c-bounded, IS the substrate), MIXED, or CONTRADICTION -- walks a 6-step deterministic algorithm for emergent-metric / analog-gravity frameworks
argument-hint: <description | gate-id | file-path>
---

# c-compare -- Propagation vs Substrate-Dynamics Classifier

Classify any framework event, observable, computation, or hypothesized object along the framework's causal axis. Walks the 6-step deterministic algorithm (produced by the project's transit/causality workshop session), forcing step-by-step reasoning with no shortcuts.

> **Scope note.** This classifier is specialized for EMERGENT / ANALOG-GRAVITY frameworks -- ones where an effective metric (here `g_M`) and its light-speed bound (`c_Gold`) emerge from an underlying substrate, so that some events are *propagation on* the emergent metric while others ARE the substrate reorganizing (and so are not bounded by the emergent `c`). It is NOT a physics-universal tool: where the metric is fundamental rather than emergent, the propagation-vs-substrate axis does not apply. The physics names below (Seeley-DeWitt moments, Goldstone/BCS branches, M_KK, D_K) are concrete examples of how the axis shows up -- substitute your framework's own structures.

## The Four Possible Verdicts

- **PROPAGATION** -- the object moves ACROSS the substrate on the emergent 4D metric g_M. Every step of the algorithm passes; v_g <= c_Gold = 0.915 M_KK. c-bounded.
- **SUBSTRATE DYNAMICS** -- the object IS a reorganization of the substrate itself. Terminates at some step before STEP 5. NOT c-bounded because there is no metric across which it propagates.
- **MIXED** -- the object has separable components that terminate at different steps. One component is propagation (STEPs 0-5 all pass), another is substrate dynamics (terminates earlier). Report both components explicitly.
- **CONTRADICTION** -- STEPs 0-4 all pass but STEP 5 fails (v_g > c_Gold). This is a framework diagnostic: either the object is misclassified at an earlier step, or the framework has a structural bug. NEVER hide this verdict.

## Canonical Source

- Algorithm: derived from the project's transit/causality workshop session (the 6-step algorithm and its section tags, e.g. T5, Re:T4, are that session's internal labels)
- Framework document: the project's causality/framework reference doc under `sessions/framework/` -- the authoritative reference holding the structural theorems
- Project thesis: the project's framing/thesis note (under the project memory or `sessions/framework/`)
- Framework vocabulary: the project's framing rule, if the pack/project defines one

---

## Usage

```
# Classify a description
/c-compare "the fold transit"

# Classify by gate ID (looks up the relevant session working paper)
/c-compare W4-L

# Classify a composite object (expect MIXED verdict)
/c-compare "Bogoliubov pair creation and subsequent propagation to the observer"

# Classify a specific branch at a specific k-scale
/c-compare "Leggett-1 branch at k = 0.043 Mpc^{-1}"

# Classify a hypothesized new observable
/c-compare "instanton-mediated coupling vertex between B2 and B3"
```

---

## Phase 0: Parse the Input

1. **Identify the object**. What is being classified? Extract:
   - A physical description (e.g., "fold transit", "photon propagation")
   - A gate ID (e.g., "W4-L", "W3-N") -- if so, read the relevant session's results working paper under `sessions/` to find the actual computation being tested
   - A file path -- if so, read and identify the principal object

2. **Check for compositeness**. If the input describes multiple distinct events (e.g., "A and B", "creation then propagation", "during transit and after"), flag it as **COMPOSITE** and plan to walk the algorithm separately for each component. Composite objects usually yield a MIXED verdict.

3. **Check for ambiguity**. If the input is underspecified (e.g., "dark matter" without specifying which channel, or "the fabric" without specifying which aspect), HALT and ask the user to sharpen the description before proceeding. Do not guess.

4. **Identify the rate/amplitude being classified**. For non-composite objects: what quantity is actually being measured or bounded? A velocity? An occupation number? A functional derivative? An amplitude? This identification drives STEP 0.

---

## Phase 1: Walk the Algorithm (6 Steps)

**RULES before starting**:
- Walk ALL 6 steps even if termination is reached early. Do not shortcut. State the verdict at each step.
- At each step, produce: (a) what you looked for, (b) what you found, (c) pass/fail verdict, (d) short reason.
- Cite workshop sections when invoking authoritative positions (T5, Re:T4, C-R2-1, etc.).

### STEP 0: Spectral-Moment Localization

**What to check**: Does the object's rate or amplitude live in **a_0** (zeroth Seeley-DeWitt moment) or **a_2** (second Seeley-DeWitt moment)?

**Canonical markers**:
- **a_0 signatures** (SUBSTRATE DYNAMICS terminal):
  - Functional derivatives of the spectral action: dS/dtau, dV_eff/dtau, d n_inst/dtau, log det H
  - Instanton nucleation rates, fugacities, 't Hooft vertex amplitudes
  - Jensen deformation parameter evolution
  - Zero-point / vacuum spectral sums (a_0 = Tr 1 before weighting)
  - Units involving M_KK^4 per dimensionless tau
- **a_2 signatures** (proceed to STEP 1a):
  - Metric curvature, Einstein-Hilbert action R*sqrt(g)
  - Dispersion relations omega(k), group velocities v_g
  - Signals traversing g_M, source-to-receiver transport
  - Planck-factor H^2 in amplitude formulas
  - Units of (distance / time) on g_M

**Rationale**: Gilkey's local index theorem + Seeley-DeWitt orthogonality forces a_0 and a_2 into distinct polynomial degrees in the heat-kernel expansion. They cannot mix; a quantity living in a_0 CANNOT be a velocity on g_M. (In an emergent-metric framework this is the "spectral-moment decoupling" structural theorem; see the project's framework reference doc under `sessions/framework/` for the formal statement.)

**Verdict rules**:
- a_0 moment -> **TERMINATE: SUBSTRATE DYNAMICS**
- a_2 moment -> proceed to STEP 1a
- Unclear / mixed -> flag as AMBIGUOUS; if the object is genuinely composite, split it and walk each component separately

---

### STEP 1a: Tensor Existence

**What to check**: Does a rank-2 Lorentzian symmetric tensor g_M exist at the moment of the event?

**Canonical markers**:
- **g_M exists** (pass):
  - The event happens in a regime where the a_2 Seeley-DeWitt coefficient has already been computed and yields an Einstein-Hilbert term
  - The surrounding context is post-fold (tau > tau_exit) or far-pre-fold (tau < tau_entry) -- regions where the spectral triple is stable
  - Photon propagation, CMB observations, BAO features
- **g_M does NOT exist** (fail):
  - The event is PARTICIPATING in the generation of g_M (fold transit, Jensen evolution during the fold, spectral-action gradient at tau_fold)
  - The a_2 coefficient is itself evolving because the spectral triple is being reorganized
  - Pre-fold and post-fold refer to DIFFERENT Lorentzian manifolds (g_M^< vs g_M^>) per the Two-Manifold Non-Embedding Theorem

**Verdict rules**:
- g_M exists -> proceed to STEP 1b
- g_M does not exist -> **TERMINATE: SUBSTRATE DYNAMICS**

---

### STEP 1b: Lorentzian Cone

**What to check**: Does g_M have a well-defined timelike direction INDEPENDENT of tau (Jensen deformation parameter)?

**Canonical markers**:
- **Lorentzian cone exists** (pass):
  - The signature (-, +, +, +) is established and stable across the timescale of the event
  - The timelike direction is a Killing direction of g_M, not a tau-dependent mixing
  - Standard GR observables work: light cones, causal future/past, asymptotic time
- **Lorentzian cone fails** (fail):
  - The event's timelike direction is tau-dependent (a changing spectral triple changes the cone)
  - Near-fold regions where g_M^< and g_M^> have distinct timelike structures
  - Quasi-static approximations that break down at the fold

**Verdict rules**:
- Lorentzian cone with tau-independent timelike direction -> proceed to STEP 2
- tau-dependent cone or no cone -> **TERMINATE: SUBSTRATE DYNAMICS**

---

### STEP 2: Source-Receiver Separability on g_M

**What to check**: Can one identify two g_M-distinct points (source, receiver) between which the object transports information?

**Canonical markers**:
- **Separable** (pass):
  - Phonon emitted at (t_s, x_s), absorbed at (t_r, x_r), with (t_r - t_s)^2 - |x_r - x_s|^2 >= 0 in g_M
  - CMB photon at last scattering -> observer today
  - BAO peak feature at sound-horizon distance
  - Any excitation with a clear source-point and receiver-point on g_M
- **Not separable** (fail):
  - The event is a change in the spectral triple itself (tau evolves, D_K eigenvalues reorganize)
  - The event happens AT a single point in the configuration space of the spectral triple
  - Functional-derivative rates (dS/dtau) are not transports between points
  - Instanton tunneling between topological sectors -- no source/receiver pair

**Verdict rules**:
- Separable source-receiver pair exists -> proceed to STEP 3
- No such pair -> **TERMINATE: SUBSTRATE DYNAMICS**

---

### STEP 3: Dispersion Relation

**What to check**: Does the object admit a dispersion relation omega_Q(k) with a group velocity v_g = domega/dk that describes its advance on g_M?

**Canonical markers**:
- **Dispersion relation exists** (pass):
  - Phononic branches B1, B2, B3, Leggett, optical, etc. -- each has an explicit omega(k) from the BCS structure
  - Photon omega = c_photon * k
  - Acoustic modes with group velocity v_g > 0
- **No dispersion relation** (fail):
  - Functional-derivative rates (dS/dtau, d log Z / dtau) have no omega(k)
  - Lefschetz thimble amplitudes at fixed winding
  - Instanton action values S_inst(tau)
  - Coleman-Weinberg potential derivatives

**Verdict rules**:
- omega(k) with well-defined v_g -> proceed to STEP 4
- No omega(k) -> **TERMINATE: SUBSTRATE DYNAMICS**

---

### STEP 4: Units Check

**What to check**: Is v_g in units of (g_M-distance) / (g_M-time)? Does it carry the units of a velocity on the emergent metric?

**Canonical markers**:
- **Correct velocity units** (pass):
  - v_g in M_KK units (natural) or m/s (SI)
  - Dimensionless v_g / c_Gold
  - Mpc / Gyr, cm / s, etc.
- **Wrong units** (fail):
  - M_KK^4 per dimensionless tau (functional derivative, not velocity)
  - Dimensionless amplitude per dimensionless tau (Bogoliubov coefficient rate)
  - Energy per time on a substrate clock that is NOT g_M-time

**Verdict rules**:
- Correct velocity units -> proceed to STEP 5
- Wrong units -> **TERMINATE: the object is not a velocity at all; classify as SUBSTRATE DYNAMICS or re-examine the object**

---

### STEP 5: Bound Check

**What to check**: Is v_g <= c_Gold = 0.915 M_KK?

**Canonical markers**:
- **Pass**: v_g in [0, 0.915 M_KK]. The Goldstone branch saturates the bound; gapped branches have smaller v_g; BAO propagation at ~c_photon is safely below.
- **Fail**: v_g > 0.915 M_KK. Structurally impossible because lambda_max in D_K bounds dispersive slopes. Strong diagnostic signal.

**Verdict rules**:
- v_g <= c_Gold -> **CLASSIFICATION: PROPAGATION** (valid, c-bounded)
- v_g > c_Gold -> **CONTRADICTION**: report prominently. Either (a) the object was misclassified at STEP 3 or STEP 4 (likely it's really substrate dynamics and a velocity was spuriously assigned), or (b) the framework has a real structural violation. Do NOT silently reclassify. Flag this for user investigation.

---

## Phase 2: Report

### If PROPAGATION:

```
=== C-COMPARE VERDICT: PROPAGATION ===
Object: {description}
STEP 0: PASS (a_2 moment)
STEP 1a: PASS (g_M exists)
STEP 1b: PASS (Lorentzian cone stable)
STEP 2: PASS (source-receiver pair: {s}, {r})
STEP 3: PASS (dispersion omega(k) = {form}; v_g = {value})
STEP 4: PASS (units: {units})
STEP 5: PASS (v_g = {value} <= c_Gold = 0.915 M_KK)

Classification: PROPAGATION on g_M. c-bounded.
Framework notes: {relevant framing-rule interpretation, if the project defines a framing rule}
```

### If SUBSTRATE DYNAMICS:

```
=== C-COMPARE VERDICT: SUBSTRATE DYNAMICS ===
Object: {description}
Terminated at STEP {N}.
Reason: {specific reason}
STEPs 0 through {N-1}: {each with pass/fail and reason}
STEP {N}: FAIL -- {reason}
STEPs {N+1} through 5: NOT REACHED (unnecessary -- terminal verdict at STEP {N})

Classification: SUBSTRATE DYNAMICS. NOT c-bounded.
Framework notes: this object IS the substrate reorganizing; it is the film being edited, not something playing on the film. Rates may be bounded by M_KK throughput, spectral-action gradients, or D_K eigenvalue structure -- but NOT by c in the GR sense. See the project's framework reference doc under `sessions/framework/`.
```

### If MIXED:

```
=== C-COMPARE VERDICT: MIXED ===
Object: {composite description}
Component A: {description}
  -> walked as {PROPAGATION or SUBSTRATE DYNAMICS}
  -> {step-by-step summary}
Component B: {description}
  -> walked as {PROPAGATION or SUBSTRATE DYNAMICS}
  -> {step-by-step summary}
{... more components as needed ...}

Classification: MIXED.
Framework notes: this composite spans both regimes. Any statement about "the speed of X" must specify WHICH component.
```

### If CONTRADICTION:

```
=== C-COMPARE VERDICT: CONTRADICTION -- FLAG FOR INVESTIGATION ===
Object: {description}
STEP 0-4: PASS
STEP 5: FAIL -- v_g = {value} > c_Gold = 0.915 M_KK

This should not happen. Two possibilities:
  (a) Misclassification at STEP 3 or STEP 4: the object is probably SUBSTRATE DYNAMICS with a spurious velocity assignment. Re-examine whether the "v_g" is genuinely a dispersive group velocity on g_M or whether it is a functional-derivative rate wearing velocity clothing.
  (b) Structural framework violation: if the object truly is a propagating mode with a dispersion relation and correct units and v_g > c_Gold, the framework has a bug that should be reported.

Do NOT silently reclassify. Report to user.
```

---

## Rules

1. **Force step-by-step reasoning**. Never shortcut to a verdict. Walk all 6 steps, even when termination is reached early. Document each step's pass/fail and reason.
2. **Do not modify the 6 steps**. The algorithm is authoritative from the project's workshop session. Individual STEP descriptions may be elaborated but the terminal conditions and ordering are fixed.
3. **Cite workshop sections** when invoking authoritative positions (T1, T5, Re:T4, C-R2-1, etc.).
4. **Reference the framework document**. Use the project's causality/framework reference doc under `sessions/framework/` for formal theorem statements rather than re-deriving them. In an emergent-metric framework it typically collects the structural theorems (decoupling, non-embedding, etc.).
5. **Handle MIXED explicitly**. Many real framework objects span both regimes. Split the input and walk each component separately. Report as MIXED with per-component verdicts.
6. **Handle CONTRADICTION prominently**. Never silently reclassify STEP 5 failures. Flag them for user investigation.
7. **No computation**. This skill is a CLASSIFIER, not a compute tool. It walks the algorithm using reasoning over the input, not by running scripts.
8. **Substrate-first framing**. Apply the project's framing rule (if the pack/project defines one) throughout. The fabric is primary; GR is emergent. The film analogy is load-bearing.
9. **Halt on ambiguity**. If the input is underspecified, ask the user to sharpen the description. Do not guess the object's category.
10. **Respect canonical constants**. c_Gold = 0.915 M_KK. Do not use alternative values. If a different sound speed is relevant (c_Leggett = 0.025 M_KK, c_B1 = 0.0798 M_KK, etc.), name it explicitly and note its relationship to c_Gold.

---

## Worked Examples

### Example 1: "The fold transit itself"

- **STEP 0**: a_0 moment (dS/dtau = +58,673 M_KK at tau_fold is a spectral-action functional derivative, not a dispersive quantity). **TERMINATE: SUBSTRATE DYNAMICS**. Steps 1-5 NOT REACHED.
- **Verdict**: SUBSTRATE DYNAMICS. The fold IS the film being edited. Mach 13.75 is a ratio of the substrate reorganization rate to the internal acoustic speed c_BLV = 0.4849 M_KK; it is NOT a velocity on g_M. (Workshop T2, R2 C-R2-3.)

### Example 2: "CMB photon propagating from last scattering to the observer"

- **STEP 0**: a_2 moment (photon kinetic term comes from a_2 Seeley-DeWitt). PASS, proceed.
- **STEP 1a**: g_M exists (post-fold, stable Lorentzian). PASS, proceed.
- **STEP 1b**: Lorentzian cone stable with tau-independent timelike direction. PASS, proceed.
- **STEP 2**: Source (last scattering surface) and receiver (observer) are g_M-distinct. PASS, proceed.
- **STEP 3**: Photon omega(k) = c * k, v_g = c = c_Gold to leading order. PASS, proceed.
- **STEP 4**: v_g in Mpc/Gyr or natural units. Velocity units on g_M. PASS, proceed.
- **STEP 5**: v_g = c_Gold <= c_Gold (saturates the bound exactly). PASS.
- **Verdict**: PROPAGATION. Standard GR optics on the emergent metric.

### Example 3: "Goldstone acoustic phonon at CMB k"

- **STEP 0**: a_2 moment (dispersive branch, propagates on g_M). PASS.
- **STEP 1a**: g_M exists (post-fold). PASS.
- **STEP 1b**: Lorentzian cone stable. PASS.
- **STEP 2**: Source (GGE relic mode at fold exit) and receiver (BAO feature at k=0.043 Mpc^{-1}) are g_M-distinct. PASS.
- **STEP 3**: omega(k) = c_B1 * k initially, disperses into c_Gold * k at high k. v_g = 0.0798 to 0.915 M_KK. PASS.
- **STEP 4**: v_g in M_KK (natural). Velocity units. PASS.
- **STEP 5**: v_g <= c_Gold = 0.915 M_KK. PASS (saturates at high k).
- **Verdict**: PROPAGATION. The Goldstone is the only gapless branch reaching observable k, per W4-L.

### Example 4: "Leggett-1 branch at k = 0.043 Mpc^{-1}"

- **STEP 0**: a_2 moment (dispersive branch). PASS.
- **STEP 1a**: g_M exists. PASS.
- **STEP 1b**: Lorentzian cone stable. PASS.
- **STEP 2**: Source-receiver separable if the mode propagates. PASS pending STEP 3.
- **STEP 3**: omega^2(k) ~= m_gap^2 = (0.0492 M_KK)^2 (gap-dominated regime); v_g = domega/dk ~= 0 for k << m_gap. **The group velocity vanishes** because the branch is gap-dominated at cosmological k. Strictly, the branch exists but carries ZERO propagation at CMB scales. TERMINATE: this is the W4-L FAIL scenario -- the branch has a dispersion relation but does not propagate to observable scales.
- **Verdict**: SUBSTRATE DYNAMICS (effectively). The Leggett-1 branch does not carry observable information at CMB k; its v_g -> 0 in the gap-dominated regime. The 56-OOM W4-L FAIL is the quantitative statement of this non-propagation.

### Example 5: "Instanton nucleation vertex"

- **STEP 0**: a_0 moment (instanton fugacity y(tau) = C * S_inst^6 * exp(-S_inst) is a spectral-action quantity; d n_inst/dtau is a functional derivative). **TERMINATE: SUBSTRATE DYNAMICS**. Steps 1-5 NOT REACHED.
- **Verdict**: SUBSTRATE DYNAMICS. Instantons don't move; they tunnel between topological sectors of the gauge bundle. There is no velocity.

### Example 6: "Jensen tau evolution from tau_entry to tau_exit"

- **STEP 0**: a_0 moment (tau is the modulus of the spectral triple; its rate is set by dS/dtau, not by any dispersion). **TERMINATE: SUBSTRATE DYNAMICS**. Steps 1-5 NOT REACHED.
- **Verdict**: SUBSTRATE DYNAMICS. tau evolution IS the spectral triple reorganizing. The rate carries units of M_KK^4 per dimensionless tau -- not a velocity. This is canonical "film editing".

### Example 7: "Bogoliubov pair creation and subsequent propagation"

- **COMPOSITE** input -- split and walk each.
- **Component A: Pair creation during transit** (59.8 pairs from tau-chirp of omega_k(tau)):
  - STEP 0: a_0 moment (the pair-creation rate is driven by domega_k/dtau, a functional derivative). TERMINATE: SUBSTRATE DYNAMICS.
- **Component B: Post-transit propagation of the 59.8 pairs on g_M**:
  - STEP 0: a_2 moment. PASS.
  - STEP 1a-1b: g_M exists, stable cone. PASS.
  - STEP 2: Source-receiver separable. PASS.
  - STEP 3: omega(k) from branch structure. PASS.
  - STEP 4-5: v_g in correct units, <= c_Gold. PASS.
  - Verdict: PROPAGATION.
- **Overall verdict**: MIXED. Pair CREATION is substrate dynamics; pair PROPAGATION is propagation. The same 59.8 pairs change their classification between during and after the transit.

### Example 8: "c_Gold itself (its emergence)"

- **STEP 0**: a_2 moment? The a_2 Seeley-DeWitt coefficient DETERMINES c_Gold via the kinetic term for photons. But "c_Gold emerging" is a change in the a_2 coefficient, not a quantity lying IN a_2. This is participating in the generation of g_M. a_0-like. **TERMINATE: SUBSTRATE DYNAMICS**.
- **Verdict**: SUBSTRATE DYNAMICS. The emergence of c_Gold is itself a substrate-level event. Once c_Gold exists, it IS the bound on propagation; but the emergence of the bound is not itself a propagation.

### Example 9: "Leggett DM occupation imprint on CMB"

- **COMPOSITE** -- split.
- **Component A: Leggett DM occupation** (n_Leggett ~= 59.8):
  - STEP 0: a_0 moment (vacuum occupation, zero-point ZPE energy). TERMINATE: SUBSTRATE DYNAMICS.
- **Component B: Gravitational imprint of Leggett DM on the CMB**:
  - STEP 0: a_2 moment (gravitational effect via g_M curvature). PASS.
  - STEP 1a-5: PASS (the gravitational signal propagates on g_M at c_photon).
  - Verdict: PROPAGATION.
- **Overall verdict**: MIXED. The OCCUPATION is substrate-dynamics (static, no propagation); the IMPRINT is propagation via gravitational coupling. The observable signal propagates at c_Gold; the reservoir it signals does not.

---

## Error Handling

| Condition | Action |
|:----------|:-------|
| Ambiguous input (unclear what the object is) | HALT. Ask user to sharpen description. |
| Missing data (can't read gate file) | Report which file, stop. Ask user for clarification or alternative input. |
| Composite object | Split into components, walk each separately, report as MIXED. |
| Terminal at STEP 0 (a_0 moment) | Report SUBSTRATE DYNAMICS immediately with STEP 0 reasoning; note STEPs 1-5 not reached. |
| STEP 5 fails with earlier passes | Report CONTRADICTION prominently. Do NOT silently reclassify. |
| Object is "c itself" or "c_Gold" | SUBSTRATE DYNAMICS -- c_Gold is the bound on propagation, not a propagation. Its emergence is substrate-level. |
| Object is a static configuration (winding number, vacuum condensate) | SUBSTRATE DYNAMICS via STEP 3 (no dispersion) or STEP 0 (a_0 moment). |
| User disagrees with verdict | Do not override. Report your reasoning step-by-step and ask user which step is disputed. |

---

## References

- **Primary**: the project's transit/causality workshop session under `sessions/` -- the workshop that produced the algorithm. Its internal sections (e.g. T1, T5, Re:T4) are the canonical sources for the step definitions.
- **Framework document**: the project's causality/framework reference doc under `sessions/framework/` -- the distilled load-bearing reference. In an emergent-metric framework it typically contains the algorithm plus the structural theorems (e.g. spectral-moment decoupling, two-manifold non-embedding, Goldstone masslessness, heat-kernel polynomial orthogonality).
- **Project thesis (the framing this algorithm implements)**: the project's framing/thesis note, under the project memory or `sessions/framework/`.
- **Framework vocabulary rule**: the project's framing rule, if the pack/project defines one.
- **Canonical constants**: `{{COMPUTATION_DIR}}/canonical_constants.py` (M_KK, c_Gold, c_fabric, etc.)
- **Mathematical anchor**: Gilkey, P. -- *Invariance Theory, the Heat Equation, and the Atiyah-Singer Index Theorem* (heat-kernel Seeley-DeWitt orthogonality); Chamseddine & Connes -- *The Spectral Action Principle* (a_k moments of the spectral action).
