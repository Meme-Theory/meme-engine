# Constraint Map — Generic Specification

The constraint map is the logic backbone of a multi-agent research project. It is a structured, queryable reference document that defines the boundaries of the solution space — what is proven, what is excluded, what survives, and what remains untested.

This document specifies the system: entry schema, state machine, category taxonomy, authority model, agent interaction rules, knowledge index integration, and bootstrap template. Projects instantiate this specification with domain-specific categories and entries.

**What this document is NOT**: a narrative, a confidence estimate, a progress report, or a rhetorical device. The constraint map is a reference table. Query it by ID. Never recite constraint counts as arguments.

---

## 1. Entry Schema

Every entry in the constraint map follows a universal format. No exceptions.

### 1a. Constraint Entry

```markdown
### {CATEGORY}-{NN}: {Short descriptive title} ({Session source})
- **Constraint**: {What has been established. Precise statement of the boundary.}
- **Implication**: {What class of approaches/solutions this rules out.}
- **Surviving space**: {What remains viable after this constraint. Points to next investigation.}
```

**Required fields**:

| Field | Purpose | Rules |
|:------|:--------|:------|
| `ID` | Unique identifier | `{CATEGORY_PREFIX}-{NN}` — e.g., `S-01`, `M-03`, `O-PHI-02` |
| `Title` | Human-scannable label | Descriptive, factual, no judgment words |
| `Source` | Provenance | Session number, computation ID, or external reference |
| `Constraint` | The boundary itself | Precise, quantitative where possible. What IS established. |
| `Implication` | What it rules out | Classes of solutions/approaches/mechanisms closed |
| `Surviving space` | What remains | What the constraint does NOT close. Next investigation targets. |

**Optional fields** (append when relevant):

| Field | When to include |
|:------|:----------------|
| `Method` | How the constraint was established (computation, proof, experiment) |
| `Precision` | Numerical precision of the boundary (e.g., "machine epsilon", "5 ppm") |
| `Assumptions` | What must hold for the constraint to apply |
| `Tightness` | Whether the bound is achievable or there is a gap |
| `Hardness` | `HARD WALL` (provably uncrossable) or `SOFT BOUNDARY` (crossable if assumptions relax) |

### 1b. Structural Theorem Entry

Permanent positive results — established facts that do not constrain mechanisms but characterize the system.

```markdown
| ID | Statement | Session | Method |
|----|-----------|---------|--------|
| ST-{NN} | {Precise statement of what is proven} | {Source} | {How it was proven} |
```

### 1c. Active Channel Entry

Surviving mechanisms/approaches that have passed all constraints thrown at them so far.

```markdown
| ID | Mechanism/Approach | Status | Key Constraint Survived |
|----|-------------------|--------|------------------------|
| AC-{NN} | {What it is} | {Current state} | {Most relevant constraint it survived} |
```

### 1d. Unvalidated Gate Entry

Pre-registered tests that have been defined but not yet executed.

```markdown
| Gate | What It Tests | PASS condition | FAIL implication |
|------|--------------|----------------|------------------|
| {ID} | {What computation/experiment} | {Exact threshold for PASS} | {What FAIL means for the project} |
```

### 1e. Observational Benchmark Entry

External reference data. Not arguments — calibration values.

```markdown
| Observable | Value | Source | Last Updated |
|:-----------|:------|:-------|:-------------|
| {What is measured} | {Value with uncertainty} | {Who measured it} | {Date} |
```

---

## 2. State Machine — The Gate Lifecycle

Every constraint in the map arrived through a lifecycle. Understanding this lifecycle is essential for maintaining map integrity.

```
                    ┌──────────────────────────────────────────────────┐
                    │                                                  │
                    ▼                                                  │
  HYPOTHESIS ──▶ PRE-REGISTRATION ──▶ COMPUTATION ──▶ VERDICT ──▶ ENTRY
                    │                                    │
                    │                                    ├──▶ CONSTRAINT (boundary mapped)
                    │                                    ├──▶ THEOREM (positive result established)
                    │                                    ├──▶ SURVIVING SPACE (approach lives)
                    │                                    └──▶ INCONCLUSIVE (needs refinement)
                    │
                    └── Unvalidated Gate (parked until resources available)
```

### 2a. States

| State | Definition | Who Owns It |
|:------|:-----------|:------------|
| **HYPOTHESIS** | Proposed mechanism, approach, or claim | Any agent |
| **PRE-REGISTERED** | Gate defined with PASS/FAIL criteria BEFORE execution | Skeptic (mandatory review) |
| **COMPUTED** | Computation/experiment executed, raw result available | Calculator / Observer |
| **CLASSIFIED** | Result compared against pre-registered criteria | Skeptic (sole authority) |
| **CONSTRAINT** | Boundary mapped — entry written to constraint map | Coordinator (writes), Skeptic (approves) |
| **THEOREM** | Permanent positive result — structural truth established | Coordinator (writes), Workhorse (verifies) |
| **ACTIVE CHANNEL** | Approach survived classification — still viable | Coordinator (tracks) |
| **UNVALIDATED** | Gate defined but not yet executed — parked | Coordinator (tracks) |

### 2b. Transitions

| From | To | Trigger | Guard |
|:-----|:---|:--------|:------|
| HYPOTHESIS | PRE-REGISTERED | Session planning | Skeptic must review criteria |
| PRE-REGISTERED | COMPUTED | Computation/experiment complete | Calculator/Observer delivers result |
| COMPUTED | CLASSIFIED | Skeptic compares result to criteria | Pre-registered criteria exist |
| CLASSIFIED | CONSTRAINT | Result is CLOSED or FAIL | Entry written with surviving space |
| CLASSIFIED | THEOREM | Result is PASS and structurally permanent | Entry verified by Workhorse |
| CLASSIFIED | ACTIVE CHANNEL | Result is PASS but conditional | Listed with conditions |
| CLASSIFIED | INCONCLUSIVE | Result is ambiguous or computation failed | Returned to PRE-REGISTERED with refined criteria |
| PRE-REGISTERED | UNVALIDATED | Resources not available this session | Parked with conditions for activation |

### 2c. Illegal Transitions

These transitions are **prohibited**. They represent the failure modes this system prevents.

| Illegal Transition | What It Means | Why It's Blocked |
|:-------------------|:-------------|:-----------------|
| HYPOTHESIS → CONSTRAINT | Writing a constraint without pre-registration | Post-hoc rationalization; no criteria existed beforehand |
| COMPUTED → CONSTRAINT (bypassing CLASSIFIED) | Self-classifying results | Builder validates their own work; no adversarial review |
| CLASSIFIED → THEOREM (without Workhorse verification) | Promoting a result to permanent without domain check | Misapplied method, numerical error, or scope overstatement |
| Any → CONSTRAINT (by anyone other than Coordinator) | Uncoordinated map writes | Version conflicts, inconsistent formatting, missing provenance |
| CONSTRAINT → deleted | Removing a constraint entry | Constraints are permanent record. They can be SUPERSEDED (with reference to the superseding entry) but never deleted. |

---

## 3. Category Taxonomy

### 3a. Structural Categories (every project gets these)

These categories exist in every constraint map regardless of domain. They capture universal types of boundaries.

| Prefix | Category | What It Captures | Permanence |
|:-------|:---------|:----------------|:-----------|
| `S` | **Structural** | Proven results that follow from the mathematical/logical structure of the framework. Cannot be evaded by changing parameters. | Permanent |
| `F` | **Framework** | Constraints on the theoretical framework itself — axiom failures, internal inconsistencies, scope limits. | Permanent unless framework changes |
| `D` | **Dynamical** | Constraints on how the system evolves — timescales, stability, transitions. | Permanent within stated regime |
| `O` | **Observational** | External data that bounds the solution space — measurements, benchmarks, empirical facts. | Updated when new data arrives |

### 3b. Domain-Specific Categories (configured per project)

Projects define their own prefixes for domain-specific constraint families. Guidelines:

| Guideline | Rationale |
|:----------|:----------|
| Use 1-3 letter prefixes | Scannable in tables and inline references |
| Group by mechanism or approach, not by session | Semantic organization, not chronological |
| Create sub-prefixes with hyphen for observational subcategories | `O-EXP` for experimental, `O-SIM` for simulation, etc. |
| Document prefix definitions at the top of the map | Self-documenting; agents can parse |

**Example domain configurations**:

| Domain | Custom Categories |
|:-------|:-----------------|
| Theoretical Physics | `P` (Perturbative), `B` (BCS/Condensate), `T` (Topological), `TH` (Thermodynamic), `N` (NCG Axiom) |
| Machine Learning | `A` (Architectural), `C` (Convergence), `G` (Generalization), `E` (Efficiency) |
| Drug Discovery | `B` (Binding), `T` (Toxicity), `P` (Pharmacokinetic), `SY` (Synthesis) |
| Software Architecture | `P` (Performance), `SC` (Scalability), `SE` (Security), `C` (Compatibility) |
| Climate Modeling | `R` (Resolution), `P` (Parameterization), `V` (Validation), `SC` (Scenario) |

### 3c. Compound Sections (every project gets these)

These sections appear at the end of every constraint map. They are derived from the constraint entries, not independent of them.

| Section | What It Contains | Updated When |
|:--------|:----------------|:-------------|
| **Structural Theorems** | Permanent positive results (ST-NN table) | New theorem established |
| **Active Channels** | Surviving approaches (AC-NN table) | Constraint closes or opens a channel |
| **Unvalidated Gates** | Pending tests (Gate table) | Session planning or gate execution |
| **Observational Benchmarks** | External reference data (Observable table) | New data published or measurement updated |

---

## 4. Authority Model

### 4a. Who Writes

| Action | Authority | Rationale |
|:-------|:----------|:----------|
| Write new constraint entry | **Coordinator** | Single writer prevents version conflicts |
| Classify gate verdict | **Skeptic** | Adversarial review prevents self-validation |
| Verify structural theorem | **Workhorse** | Domain depth catches subtle errors |
| Define pre-registered gate | **Any agent** (Skeptic reviews) | Hypotheses come from anywhere; criteria quality-checked |
| Update observational benchmarks | **Observer** | Domain-specific data awareness |
| Propose new active channel | **Any agent** | Discovery is distributed |

### 4b. Who Reads (and How)

Every agent reads the constraint map, but each archetype interacts with it differently.

| Archetype | How They Use the Map |
|:----------|:---------------------|
| **Skeptic** | Queries by gate ID. Updates confidence based on verdicts. Enforces pre-registration. Never recites counts. |
| **Calculator** | Reads surviving space to identify what to compute next. Checks constraints before running expensive computation. |
| **Principalist** | Reads structural constraints to find deeper patterns. Identifies when multiple constraints share a root cause. |
| **Boundary Guard** | Reads ALL constraints to map the feasible region topology. Identifies hard walls vs. soft boundaries. Determines what single test most narrows the surviving space. |
| **Dreamer** | Reads surviving space fields for cross-domain analogies. Proposes new active channels that survive existing constraints. |
| **Workhorse** | Verifies constraint derivations. Checks whether a constraint's assumptions actually hold. |
| **Observer** | Updates observational benchmarks. Checks whether theoretical constraints are consistent with measurements. |
| **Bridge** | Verifies constraints against primary sources. Catches when a constraint overstates what a source actually proves. |
| **Coordinator** | Writes entries. Cites by ID. Links to file path. Never summarizes counts or trends in prose. |
| **Librarian** | Extracts constraint entries into knowledge index entities. Does not evaluate content. |

### 4c. Who Challenges

Constraints can be **challenged** but not deleted. The challenge protocol:

1. **Any agent** identifies a potential issue with an existing constraint
2. The challenge is stated precisely: which assumption may be wrong, what new evidence contradicts the constraint, or why the constraint's scope was overstated
3. **Skeptic** evaluates the challenge against the original pre-registered criteria
4. If the challenge is valid, the constraint is **SUPERSEDED** — the original entry remains with an added `Superseded by: {NEW-ID}` field, and a new entry replaces it
5. **Coordinator** writes both the supersession annotation and the new entry

---

## 5. Constraint Interactions

### 5a. Constraint Chains

When constraints have dependencies, they form chains. A chain is a sequence of gates where failure at any step terminates downstream work.

```
GATE-1 ──PASS──▶ GATE-2 ──PASS──▶ GATE-3 ──PASS──▶ {Mechanism viable}
   │                │                │
   CLOSED           CLOSED           CLOSED
   │                │                │
   ▼                ▼                ▼
 {Chain            {Chain          {Chain
  terminated}       terminated}     terminated}
```

**Chain entry format**:

```markdown
## Constraint Chain: {CHAIN-NAME}

### Chain Logic
{ID-1} -> {ID-2} -> {ID-3} -> {ID-4}
(Failure at any step terminates downstream)

### Chain Table
| Step | Computation | Session | Condition for CLOSED | Status |
|:-----|:-----------|:--------|:--------------------|:-------|
| {ID-1} | {what} | {source} | {threshold} | {PASS/CLOSED/PENDING} |
| {ID-2} | {what} | {source} | {threshold} | BLOCKED by {ID-1} |

### Gate Classification
| Type | Definition | Consequence |
|:-----|:----------|:-----------|
| HARD CLOSE | Terminates chain | All downstream cancelled |
| SOFT GATE | Constrains but continues | Priority modified |
| POSITIVE SIGNAL | Increases confidence | No structural change |
```

### 5b. Constraint Convergence

When multiple independent constraints close the same mechanism, this is **convergence** — stronger than any single constraint. Document convergence explicitly:

```markdown
### Convergence: {Mechanism Name} — CLOSED by independent routes
- Route 1: {CONSTRAINT-ID} — {method}
- Route 2: {CONSTRAINT-ID} — {method}
- Route 3: {CONSTRAINT-ID} — {method}
- **Convergence strength**: {N} independent methods, {M} different agent archetypes
```

### 5c. Constraint Escalation

Constraints have hierarchy levels that determine how they interact:

| Level | Name | Scope | Example |
|:------|:-----|:------|:--------|
| **L0** | Structural/Algebraic | Cannot be evaded by any parameter choice | "The ratio F/B = 4/11 for any positive spectral functional" |
| **L1** | Regime-Dependent | Applies within stated assumptions | "Tree-level potential monotone for all parameter values" |
| **L2** | Computational | Holds for tested range, may not hold outside | "Tested 8 cutoff shapes, all monotone" |
| **L3** | Observational | External data bound, may update | "Current measurement constrains X < Y" |

Higher-level constraints supersede lower-level ones when they conflict. An L0 constraint that closes a mechanism cannot be overridden by an L2 computation that appears to open it — the computation has an error or an unstated assumption.

---

## 6. Framing Rules

These rules govern how agents talk about constraints. Violation of any rule is a flag for the Coordinator to intervene.

### 6a. Language Rules

| Use | Do NOT Use | Why |
|:----|:----------|:----|
| "Constraint" | "Failure" | Constraints map boundaries; "failures" imply decline |
| "Boundary" | "Dead end" | Boundaries define shape; "dead ends" imply finality |
| "Ruled out" | "Killed" / "Destroyed" | Neutral mapping language vs. emotional rhetoric |
| "Surviving space" | "Last hope" | Remaining viable region vs. desperation narrative |
| "Closed mechanism" | "Failed approach" | Mechanism classification vs. quality judgment |
| "20 ruled-out approaches" | "20 failures" | Exploration progress vs. decline narrative |

### 6b. Counting Rules

| Rule | Rationale |
|:-----|:----------|
| NEVER cite constraint counts as arguments | "21 constraints" says nothing about viability — it says 21 boundaries are mapped |
| NEVER use constraint accumulation as evidence of decline | The count measures EXPLORATION COVERAGE, not project health |
| NEVER compare constraint counts between categories | Categories have different granularities |
| DO cite individual constraints by ID when relevant | "S-01 closes this mechanism because..." |
| DO reference the surviving space when proposing work | "Per S-01, the surviving space includes..." |

### 6c. Evidence Rules

| Rule | Rationale |
|:-----|:----------|
| Only results against pre-registered gates count as evidence | Prevents post-hoc rationalization |
| Non-pre-registered insights are recorded as OBSERVATIONS | They inform future gate design but don't move confidence |
| The constraint map is a reference document, not a narrative | Cite by ID, don't weave into prose |
| Narrative coherence is NOT evidence | A beautiful story that fits all constraints is still just a story |
| Constraint counts are NOT evidence | Exploration breadth says nothing about framework viability |

---

## 7. Knowledge Index Integration

Constraint map entries feed into the knowledge index through the entity extractor. The mapping:

| Constraint Map Section | Knowledge Index Entity Type |
|:-----------------------|:---------------------------|
| Constraint entries (all categories) | `closed_mechanisms` + `constraints` |
| Structural Theorems | `theorems` |
| Active Channels | `open_channels` |
| Unvalidated Gates | `gates` |
| Gate verdicts (PASS/CLOSED) | `gates` (status updated) |
| Observational Benchmarks | `data_provenance` |

### Entity Extraction Pattern

The knowledge extractor should parse constraint entries using these patterns:

```
Entry ID:           /^### ([A-Z]+-\d+):/
Constraint field:   /^- \*\*Constraint\*\*: (.+)/
Implication field:  /^- \*\*Implication\*\*: (.+)/
Surviving field:    /^- \*\*Surviving space\*\*: (.+)/
Source field:        /\(Session[s]? ([\d,\s]+[a-z]?)\)/
Gate verdict:       /Classification: (PASS|CLOSED|FAIL)/
Theorem entry:      /^\| ST-(\d+) \|/
Active channel:     /^\| AC-(\d+) \|/
```

### Authority Hierarchy for Index Conflicts

When the knowledge index has conflicting entries from different sources, resolve by:

```
Skeptic verdicts  >  Synthesis files  >  Gate results  >  Session minutes  >  Raw computation
```

---

## 8. Maintenance Protocol

### 8a. When to Update

| Event | Required Update |
|:------|:----------------|
| Gate verdict delivered | New constraint entry OR active channel updated |
| New structural result proven | New theorem entry |
| Computation closes a mechanism | New constraint entry with surviving space |
| External data published | Observational benchmark updated |
| Prior constraint superseded | Original annotated, new entry written |
| Session ends | Coordinator reviews all new entries for completeness |

### 8b. Periodic Audit

Every 5-10 sessions (or at project milestones), the Boundary Guard performs a constraint map audit:

1. **Completeness**: Every classified gate has a corresponding entry
2. **Consistency**: No two constraints contradict each other
3. **Surviving space coherence**: Active channels actually survive all constraints in the map
4. **Staleness**: Observational benchmarks use current data
5. **Convergence detection**: Identify mechanisms closed by multiple independent routes
6. **Chain integrity**: Constraint chains have correct dependency structure

### 8c. Size Management

The constraint map grows monotonically (entries are never deleted). To manage size:

| Technique | When |
|:----------|:-----|
| **Category-level summary headers** | When a category exceeds 10 entries — add a 2-line summary at the top of the category |
| **Archival** | When a category is fully explored (all surviving space closed) — move to `constraint-map-archive.md` with a cross-reference |
| **Convergence compression** | When 3+ constraints close the same mechanism — create a convergence entry and mark individuals as "see convergence" |

---

## 9. Anti-Patterns

What goes wrong when projects don't use this system, and what goes wrong when they use it incorrectly.

### 9a. Without a Constraint Map

| Failure Mode | Symptom | Consequence |
|:-------------|:--------|:------------|
| **Groundhog Day** | New sessions re-investigate approaches already ruled out | Wasted computation, no compound progress |
| **Echo chamber** | Every session ends with "this is promising" | No adversarial memory; confirmation bias dominates |
| **Invisible progress** | Team can't articulate what they've learned | Demoralization; inability to plan effectively |
| **Goalpost shifting** | Success criteria change after results come in | Unfalsifiable framework; no genuine tests |
| **Context loss** | Prior session's key results forgotten | Each session starts from scratch |

### 9b. With a Misused Constraint Map

| Misuse | Symptom | Fix |
|:-------|:--------|:----|
| **Counting as argument** | "We have 25 constraints, so the project is failing" | Counting is rhetoric. Ban it. Cite by ID only. |
| **Post-hoc entries** | Constraints written after results, with no pre-registration | Enforce the state machine. No HYPOTHESIS → CONSTRAINT shortcut. |
| **Self-validation** | Calculator classifies their own gate | Skeptic classifies. Always. |
| **Narrative embedding** | Constraint map woven into synthesis prose | Cite by ID. Link to file. Map is a reference document. |
| **Deletion of inconvenient entries** | "This one doesn't apply anymore" | Constraints are SUPERSEDED, never deleted. Trail must be preserved. |
| **Enthusiasm inflation** | Active Channels described with excitement language | Neutral descriptions only. "Survives" not "is promising." |
| **Constraint inflation** | Minor observations elevated to constraint status | Constraints must pass through the full state machine. Observations are observations. |
| **Missing surviving space** | Entries that say what's closed but not what remains | Every constraint entry MUST have a surviving space field, even if "None within this framework." |

---

## 10. Bootstrap Template

When a new project creates its constraint map, start with this scaffold:

```markdown
# Unified Constraint Map — {{PROJECT_NAME}}

This is a structured reference table. Query by ID for specific facts.
Do NOT recite constraint counts. Do NOT use the number of entries as an argument.
Each entry defines a boundary of the allowed region: what is proven, what is excluded, what survives.

Last updated: Session {{N}} ({{DATE}}). Maintained by Coordinator.

---

## Category Definitions

| Prefix | Category | Scope |
|:-------|:---------|:------|
| S | Structural | Permanent mathematical/logical constraints |
| F | Framework | Constraints on the framework's axioms or assumptions |
| D | Dynamical | Constraints on system evolution and stability |
| O | Observational | External data bounds |
| {{DOMAIN-PREFIX}} | {{DOMAIN-CATEGORY}} | {{SCOPE}} |

---

## S: Structural Constraints

(No entries yet. First entry will be S-01.)

---

## F: Framework Constraints

(No entries yet.)

---

## D: Dynamical Constraints

(No entries yet.)

---

## O: Observational Constraints

(No entries yet.)

---

## Structural Theorems (permanent, established results)

| ID | Statement | Session | Method |
|----|-----------|---------|--------|
| (No entries yet.) | | | |

---

## Active Channels (surviving solution space)

| ID | Mechanism/Approach | Status | Key Constraint Survived |
|----|-------------------|--------|------------------------|
| (No entries yet.) | | | |

---

## Unvalidated Gates (pre-registered, awaiting computation)

| Gate | What It Tests | PASS condition | FAIL implication |
|------|--------------|----------------|------------------|
| (No entries yet.) | | | |

---

## Observational Benchmarks (reference values, not arguments)

| Observable | Value | Source | Last Updated |
|:-----------|:------|:-------|:-------------|
| (No entries yet.) | | | |
```

---

## 11. Cross-References

This specification is used by and references:

| Document | Relationship |
|:---------|:-------------|
| `METHODOLOGY.md` § 3 | Defines the constraint methodology this specification implements |
| `BEHAVIORAL-PATTERNS.md` § 3 | Coordinator rules (Constraint Framing, Evidence Discipline) that enforce this system |
| `ARCHETYPES.md` | Defines which archetypes have which authority over the map |
| `ARCHITECTURE.md` § 5 | Knowledge index entity types that constraint entries map to |
| `agent-templates/skeptic.md` | Skeptic's pre-registration and classification authority |
| `agent-templates/coordinator.md` | Coordinator's write authority and framing rules |
| `agent-templates/boundary-guard.md` | Boundary Guard's constraint mapping methodology |
| `session-templates/H-decision-gate.md` | Decision Gate format that produces PASS/CLOSED verdicts |
| `session-templates/F-decisive-computation.md` | Decisive Computation format with pre-registered gates |
| `session-templates/supporting-documents.md` | Constraint Chain and Permanent Results Registry templates |
