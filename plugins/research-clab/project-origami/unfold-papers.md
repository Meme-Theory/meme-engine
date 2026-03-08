# Unfold: Populate Research Corpus

**Target agent**: Main orchestrator (`/new-research-project` skill)
**Task**: Create domain agents and fetch their research papers.
**Inputs**: Researcher queue from coordinator (see `sessions/session-plan/researcher-queue.md`).
**Depends on**: `unfold-agents.md` must complete first (coordinator writes the researcher queue).
**Mechanism**: `/new-researcher` skill (which internally delegates to web-researcher for paper fetching).

---

## Context

This is NOT a standalone unfold task that a teammate reads. This is the **main orchestrator's playbook** for the researcher-creation phase of `/new-research-project`.

The coordinator has already:
1. Presented the archetype menu to the user
2. Collected selections (archetypes, persona descriptions, domains, colors)
3. Written the researcher queue at `sessions/session-plan/researcher-queue.md`

The main orchestrator now processes that queue.

---

## Step 1: Read the Researcher Queue

Read `sessions/session-plan/researcher-queue.md` (created by the coordinator during unfold-agents). It contains:

```markdown
# Researcher Queue -- Session 0

| Persona Spec | Archetype | Papers | Color |
|:-------------|:----------|:-------|:------|
| Carl Sagan-style empiricist for {domain} | skeptic | 14 | coral |
| {sub-domain} computation specialist | calculator | 14 | teal |
| {sub-domain} workhorse | workhorse | 14 | amber |
```

---

## Step 2: Invoke `/new-researcher` for Each Entry

For each row in the queue:

```
/new-researcher "{Persona Spec}" --archetype {archetype} --papers {N} --color {color}
```

This creates:
1. Research papers in `researchers/{FolderName}/` (via web-researcher)
2. Agent definition at `.claude/agents/{slug}.md` (stamped from archetype template)
3. Agent memory directory at `.claude/agent-memory/{slug}/`
4. AGENTS.md in the researcher folder

### Sequencing

- Process entries ONE AT A TIME (each `/new-researcher` invocation spawns a web-researcher)
- Wait for each to complete before starting the next
- If one fails, report the failure and continue to the next entry

---

## Step 3: Index Each Researcher Folder

After ALL `/new-researcher` invocations complete, invoke `/librarian` on each researcher folder:

```
/librarian {FolderName-1}
/librarian {FolderName-2}
...
```

This spawns the newly created domain agent to read its own papers and build a structured index.

**Sequential**: `/librarian` creates a team, so only one at a time.

---

## Step 4: Update Cross-Researcher Index

After all indexing is done, create or update `researchers/index.md`:

```markdown
# Researchers -- Cross-Domain Index

| Domain | Papers | Agent | Archetype | Description |
|:-------|:-------|:------|:----------|:------------|
| {folder-1} | {count} | {slug-1} | {archetype} | {one-line} |
| {folder-2} | {count} | {slug-2} | {archetype} | {one-line} |
```

---

## Step 5: Update Agent Registry

Update `agents.md` at project root -- replace the "Queued" placeholders from the coordinator with actual agent entries:

```markdown
### Domain Specialists

| Agent | Archetype / Model | Role |
|:------|:------------------|:-----|
| {slug-1} | {archetype} / opus | {one-line role} |
| {slug-2} | {archetype} / opus | {one-line role} |
```

---

## What You Do NOT Do

- **Do NOT fetch papers yourself** -- `/new-researcher` delegates to web-researcher
- **Do NOT create agent definitions yourself** -- `/new-researcher` handles this
- **Do NOT modify the researcher queue** -- the coordinator wrote it, you execute it
- **Do NOT skip entries** -- process every row, report failures
- **Do NOT create agents for infrastructure roles** -- coordinator, indexer, and scout are already installed
