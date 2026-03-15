# Unfold: Document Preparation Infrastructure

**Target agent**: Coordinator (during infrastructure setup)
**Task**: Install format-specific document templates and configure the document-prep skill based on the user's output format selection.
**Inputs**: `{output-format}` from Question 4 (LaTeX, Typst, Markdown, or "Not sure yet").
**Depends on**: `unfold-structure.md` Step 1 (directories must exist).
**Executed during**: Dispatch 1 (coordinator infrastructure setup), after unfold-structure Steps 1-4.

---

## Context

Question 4 of `/new-research-project` asks the user: "What document format will this project produce?" The answer determines which document templates get installed and how the `/document-prep` skill behaves.

Currently three format tracks are supported:

| Format | Templates Shipped | Status |
|:-------|:-----------------|:-------|
| **LaTeX** | 13 templates (paper, poster, slides, thesis, report, etc.) | Complete |
| **Typst** | Placeholder | Stub — formatter agent fills via research corpus |
| **Markdown** | Placeholder | Stub — formatter agent fills via research corpus |

LaTeX templates are derived from [K-Dense-AI/claude-scientific-skills](https://github.com/K-Dense-AI/claude-scientific-skills) (MIT License) and [claude-prism](https://github.com/delibae/claude-prism) examples.

---

## Step 1: Create the Document Templates Directory

Add to the project directory tree:

```
artifacts/
├── document-templates/
│   ├── latex/          # LaTeX .tex templates (if format = LaTeX)
│   ├── typst/          # Typst .typ templates (if format = Typst)
│   └── markdown/       # Markdown templates (if format = Markdown)
```

Create `artifacts/document-templates/` and the subdirectory matching `{output-format}`.

---

## Step 2: Install Format-Specific Templates

### If `{output-format}` = LaTeX

Copy ALL `.tex` files from `${CLAUDE_PLUGIN_ROOT}/templates/document-templates/latex/` into `artifacts/document-templates/latex/`:

```
paper-standard.tex      # Generic article (natbib, amsmath)
paper-ieee.tex          # IEEE conference/journal (IEEEtran)
paper-acm.tex           # ACM conference/journal
poster-academic.tex     # A0 portrait academic poster (multicol, tikz)
presentation-beamer.tex # Beamer presentation (Madrid theme)
thesis-standard.tex     # PhD/Master's thesis (report class)
report-scientific.tex   # Scientific report with highlight boxes
report-technical.tex    # Technical report
letter-formal.tex       # Formal/cover letter
cv-modern.tex           # Academic CV
book-standard.tex       # Book/monograph
newsletter.tex          # Newsletter
blank.tex               # Minimal starting point
references.bib          # Sample bibliography file
```

Also install the `references.bib` template.

### If `{output-format}` = Typst

Copy `${CLAUDE_PLUGIN_ROOT}/templates/document-templates/typst/README.md` into `artifacts/document-templates/typst/`.

Report to the main orchestrator: "Typst templates are stubs. The formatter agent will populate templates from its research corpus. Consider adding a formatter agent with `/new-researcher --archetype formatter 'Typst academic publishing'`."

### If `{output-format}` = Markdown

Copy `${CLAUDE_PLUGIN_ROOT}/templates/document-templates/markdown/README.md` into `artifacts/document-templates/markdown/`.

The `/document-prep --new` command will scaffold markdown documents from general knowledge.

### If `{output-format}` = "Not sure yet"

Create the `artifacts/document-templates/` directory but leave it empty. The user can install templates later by running this unfold manually or by creating a formatter agent.

---

## Step 3: Update Root CLAUDE.md

Append to the project structure section of the root CLAUDE.md:

```
artifacts/
  document-templates/    # Document templates for /document-prep --new
    {format}/            # {Format}-specific templates
```

And add to the skills reference:

```
| `/document-prep` | Document toolkit — create, draft, review, cite, compile | Recommended |
```

---

## Step 4: Update document-prep SKILL.md (Format Binding)

The `document-prep` SKILL.md is already installed by unfold-structure Step 4. It includes format-aware building capabilities. No modification needed — the skill discovers templates at `artifacts/document-templates/` at runtime.

If the skill's `--new` subcommand can't find templates, it reports which format was selected and suggests creating a formatter agent.

---

## Step 5: Recommend Formatter Agent (Conditional)

If `{output-format}` is LaTeX, add a recommendation to `sessions/session-plan/researcher-queue.md` (or report to the main orchestrator for inclusion):

```markdown
| LaTeX academic publishing specialist | formatter | 14 | amber |
```

This is a SUGGESTION, not automatic. The main orchestrator presents it to the user during Phase 8 (agent selection). The formatter archetype is in the "UTILITY" category — optional but recommended for any project that will produce documents.

---

## Verification

- [ ] `artifacts/document-templates/` directory exists
- [ ] Format-specific subdirectory exists and contains templates (or README placeholder)
- [ ] For LaTeX: 13 `.tex` files + 1 `.bib` file present
- [ ] Root CLAUDE.md references the document-templates directory
- [ ] `/document-prep` skill is installed (from unfold-structure Step 4)

---

## What You Do NOT Do

- **Do NOT create the formatter agent** — that's the user's choice via agent selection
- **Do NOT modify the document-prep SKILL.md** — it ships ready-to-use from the plugin
- **Do NOT install templates for formats the user didn't select** — install only the chosen format
- **Do NOT compile any LaTeX** — that's the user's responsibility via `/document-prep --compile`
