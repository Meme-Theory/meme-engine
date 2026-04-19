---
description: Rebuild a researcher paper library from source PDFs -- download via MCP, delete old folder, transcribe all PDFs to markdown, rebuild index
argument-hint: <researcher-folder> [--download-only] [--transcribe-only] [--index-only] [--batch-size N]
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash, Agent, mcp__paper-search__search_arxiv, mcp__paper-search__search_google_scholar, mcp__paper-search__download_arxiv]
---

# Rebuild Library Skill

You are the **Library Rebuilder**. Your job is to take an existing researcher paper folder, download all papers as PDFs from arXiv (and other sources via MCP), delete the old markdown files, transcribe every PDF into structured markdown sourced exclusively from PDF content, and rebuild the index.

This skill exists because agent-generated paper transcriptions frequently contain training-knowledge contamination, duplicate entries, and synthesis docs with no backing paper. A rebuild from source PDFs guarantees every markdown file traces to an actual publication.

## Arguments

The user invoked: `/rebuild-library $ARGUMENTS`

Parse `$ARGUMENTS` to extract:
1. **Researcher folder** (required): The folder name under `researchers/` (e.g., `Baptista`, `Volovik`, `Einstein`)
2. **--download-only** (optional): Only run Phase 1 (download PDFs), skip transcription
3. **--transcribe-only** (optional): Only run Phase 2 (transcribe existing PDFs), skip download
4. **--index-only** (optional): Only run Phase 3 (rebuild index from existing markdown files)
5. **--batch-size N** (optional, default 3): Max parallel transcription agents per round

If `$ARGUMENTS` is `--help`, show usage and stop:
```
/rebuild-library Baptista                     -- full rebuild (download + transcribe + index)
/rebuild-library Volovik --download-only      -- just download PDFs to downloads/{folder}/
/rebuild-library Baptista --transcribe-only   -- transcribe existing PDFs, skip download
/rebuild-library Einstein --index-only        -- rebuild index from existing markdown
/rebuild-library Baptista --batch-size 4      -- use 4 parallel agents per round
```

If `$ARGUMENTS` is blank, ask the user for a researcher folder.

## Context Discovery

After parsing the folder name from `$ARGUMENTS`, run these commands via Bash (substituting the actual folder name):

```bash
# Existing papers
ls "researchers/$FOLDER/" 2>/dev/null | head -20
# Existing index header
head -10 "researchers/$FOLDER/index.md" 2>/dev/null
# Already-downloaded PDFs
ls "downloads/$FOLDER/" 2>/dev/null | head -20
# Paper count
ls "researchers/$FOLDER/"*.md 2>/dev/null | wc -l
```

All four can run in parallel since they are independent reads.

## Phase 1: Download PDFs

### Step 1.1: Extract arXiv IDs from existing index

Read `researchers/{folder}/index.md` and extract all arXiv IDs. Build a mapping:

```
paper_number -> arXiv_ID -> title -> authors -> year
```

Use Grep to find all lines matching `arXiv` in the index. If no index exists, scan all markdown files for arXiv IDs in their headers.

### Step 1.2: Also scan markdown file headers

For papers without arXiv IDs in the index, read the first 10 lines of each markdown file to find:
- `**arXiv:**` fields (some IDs are in the files but missing from the index)
- `**DOI:**` fields (for journal-only papers)
- `**Authors:**` and `**Year:**` fields (for arXiv search)

### Step 1.3: Search for missing papers

For papers without arXiv IDs, search using the MCP tools:

**arXiv search** (CRITICAL SYNTAX -- field prefixes bind to ONE token only):
```
WRONG: ti:dark matter annihilation        (only "dark" hits title field)
WRONG: "Katherine Mack dark matter"       (natural language, returns garbage)
RIGHT: au:Mack_Katherine AND ti:dark AND ti:matter
RIGHT: au:Baptista AND ti:higher AND ti:dimensional AND ti:Standard AND ti:Model
```

Every keyword needs its own `ti:` prefix joined by AND. Author format: `au:LastName_FirstName`.

**Google Scholar search** (natural language OK):
```
search_google_scholar("Bourguignon Gauduchon spinors Dirac operators 1992")
```

### Step 1.4: Download all PDFs

Create download directory: `downloads/{folder}/`

For old-style arXiv IDs with slashes (e.g., `hep-th/0208001`), create subdirectories first:
```bash
mkdir -p downloads/{folder}/hep-th downloads/{folder}/math-ph downloads/{folder}/math downloads/{folder}/gr-qc
```

Then download in parallel batches of ~12:
```
download_arxiv(paper_id="2105.02899", save_path="./downloads/{folder}")
```

### Step 1.5: Triage results

Categorize all papers into:
1. **Downloaded** -- PDF available in `downloads/{folder}/`
2. **Not on arXiv** -- journal-only, pre-arXiv, or book (note DOI/journal for reference)
3. **Synthesis docs** -- marked `[Synthesis]` in author field, no backing external paper
4. **Duplicates** -- multiple old paper numbers sharing one arXiv ID

Report the triage to the user before proceeding.

## Phase 2: Transcribe PDFs to Markdown

### Step 2.1: Build the paper mapping

Create a clean sequential numbering for all downloaded PDFs. Rules:
- One entry per unique PDF (collapse old duplicates)
- Drop synthesis docs with no backing paper
- Drop papers that couldn't be downloaded (note in index as "not available")
- Group thematically (author's core work first, then related papers)

### Step 2.2: Delete old folder and recreate

```bash
# Preserve non-paper files
cp "researchers/{folder}/agents.md" /tmp/{folder}_agents.md 2>/dev/null
rm -rf "researchers/{folder}"
mkdir -p "researchers/{folder}"
cp /tmp/{folder}_agents.md "researchers/{folder}/agents.md" 2>/dev/null
```

### Step 2.3: Spawn transcription agents

Divide papers into batches of 6-10 papers each, grouped by theme. Spawn up to `--batch-size` agents in parallel per round.

Each agent receives:
1. The PDF-to-filename mapping for its batch
2. The markdown template (below)
3. Strict instruction: **ALL content from PDFs only, NEVER training knowledge**

**Agent spawn pattern:**
```
Agent(
  description: "Transcribe {theme} papers {N}-{M}",
  mode: "bypassPermissions",
  run_in_background: true,
  prompt: """
    You are transcribing arXiv papers into structured markdown for
    researchers/{folder}/ in "<project-root>".

    CRITICAL: Generate ALL content from the PDFs only. NEVER use training
    knowledge. If unclear from PDF, write [INCOMPLETE - not extractable from PDF].

    PATH WARNING: Project root has a space. Use Write tool, not Bash echo/cat.

    [paper mapping table]
    [markdown template]

    Process all papers. Read each PDF thoroughly.
  """
)
```

### Step 2.4: Markdown template

Every paper file follows this structure:

```markdown
# [Exact title from PDF]

**Author(s):** [from PDF]
**Year:** [publication year]
**Journal:** [if stated in PDF]
**arXiv:** [ID]
**Relevance:** [CRITICAL / HIGH / MEDIUM / LOW]

---

## Abstract

[Verbatim from PDF]

---

## Key Arguments and Derivations

[Section-by-section summary of theoretical content.
For CRITICAL papers: detailed, 1-2 pages minimum.
For LOW papers: brief summary, ~0.5 pages.]

## Key Results

[Numbered list of main theorems/results]

## Key Equations

| Label | Equation | Reference |
|:------|:---------|:----------|
| [name] | [equation in LaTeX] | [eq number or section] |

[CRITICAL papers: 10-20 equations. Others: 5-15.]

## Relevance to {{PROJECT_NAME}}

[1-5 sentences connecting to the M4 x SU(3) framework.
Be specific about which project results depend on this paper.]
```

### Step 2.5: Verify transcriptions

After all agents complete:
```bash
ls -1 "researchers/{folder}/"*.md | wc -l    # count files
wc -l "researchers/{folder}/"[0-9]*.md | sort -n | head -5  # find thin files
```

Flag any file under 40 lines as potentially incomplete.

## Phase 3: Rebuild Index

### Step 3.1: Extract metadata from all papers

```bash
for f in researchers/{folder}/[0-9]*.md; do
  head -8 "$f" | grep -E "^(#|.*Author|.*Year|.*arXiv|.*Relevance)"
  echo "---"
done
```

### Step 3.2: Write index.md

The index must contain these sections in order:

1. **Header**: Researcher name, paper count, date range, primary domain, project relevance
2. **Dependency Graph**: ASCII art showing paper relationships (upstream/downstream)
3. **Topic Map**: Papers grouped by theme (A, B, C...) with 2-3 sentence descriptions
4. **Quick Reference Table**: "If your task involves X, read papers Y" with priority levels
5. **Paper Entries**: One entry per paper with File, arXiv, Year, Authors, Relevance, Tags

### Step 3.3: Template for paper entries in index

```markdown
### Paper NN: [Short title] [PRIORITY if CRITICAL/HIGH]
- **File**: `{filename}.md`
- **arXiv**: {ID}
- **Year**: {year}
- **Authors**: {authors}
- **Relevance**: {CRITICAL/HIGH/MEDIUM/LOW}
- **Tags**: {comma-separated keywords}
```

## Phase 4: Report

```
=== LIBRARY REBUILD COMPLETE ===
Folder:        researchers/{folder}/
Papers:        {N} transcribed from PDFs
Index:         researchers/{folder}/index.md
Downloads:     downloads/{folder}/ ({M} PDFs)

Changes from previous version:
- Duplicates collapsed: {list}
- Synthesis docs removed: {list}
- Papers not downloadable: {list with reasons}
- New papers added: {list}

Paper count: {old} -> {new}
```

## Rules

1. **PDF content only.** Every sentence in every markdown file must trace to the actual PDF. This is the entire point of the rebuild. Mark gaps with [INCOMPLETE] rather than filling from training knowledge.

2. **arXiv search syntax is critical.** The `ti:` prefix binds to ONE token. Multi-word title searches MUST use `ti:word1 AND ti:word2 AND ti:word3`. See Step 1.3. Getting this wrong returns garbage (latest papers instead of targeted results).

3. **Old-style arXiv IDs have slashes.** IDs like `hep-th/0208001` create subdirectories when downloaded. Pre-create the subdirs (`hep-th/`, `math-ph/`, `math/`, `gr-qc/`, etc.) before downloading.

4. **Max 3-4 agents per parallel batch.** More causes notification avalanche. Each agent handles 6-10 papers.

5. **Preserve non-paper files.** Before deleting the old folder, copy out `agents.md`, any `.json` configs, or other non-paper files. Restore them after recreating the folder.

6. **One markdown per unique PDF.** If the old library had duplicate entries (e.g., preprint + published version sharing one arXiv ID), collapse to one entry.

7. **Relevance tiers follow project convention:**
   - CRITICAL: Directly used in framework computations or gates a mechanism
   - HIGH: Provides methods, data, or context actively referenced
   - MEDIUM: Related but not directly used yet
   - LOW: Background/foundational, may never be directly referenced

8. **CRITICAL papers get detailed treatment.** 10-20 equations, 1-2 pages of derivation summary, specific framework connections. LOW papers get abbreviated treatment.

9. **Report to user at phase boundaries.** After download triage (Phase 1.5), after transcription verification (Phase 2.5), and at completion (Phase 4). Don't run the entire pipeline silently.

10. **The index dependency graph matters.** It's the primary navigation tool for agents reading the library. Get the upstream/downstream relationships right by reading how papers cite each other.
