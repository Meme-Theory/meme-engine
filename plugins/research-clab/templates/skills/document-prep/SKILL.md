---
name: document-prep
description: "Document preparation toolkit — create documents from templates, draft sections, peer review, citation management, format checking, compilation. Adapts to LaTeX, Typst, or Markdown."
argument-hint: --new <type> [title] | --draft <section> [file] | --review <file> | --cite <doi|query> | --compile [file] | --template <format> | --notation | --style <venue> | --check <file> | --submission | --bib | --index | --templates
metadata:
    building-workflows-from: K-Dense-AI/claude-scientific-skills (MIT License)
    templates-from: delibae/claude-prism (apps/desktop/public/examples)
---

# Document Prep — Format-Aware Document Toolkit

Create, draft, review, and compile scientific documents. Discovers the project's formatting resources from the formatter agent's research corpus AND from shipped templates at `artifacts/document-templates/`.

> Building workflows derived from [K-Dense-AI/claude-scientific-skills](https://github.com/K-Dense-AI/claude-scientific-skills) (MIT). Templates from [claude-prism](https://github.com/delibae/claude-prism).

## Usage

### Building (create and write documents)

```
/document-prep --new <type> [title]       # Create a new document from template
/document-prep --draft <section> [file]   # Write or expand a section (IMRAD-aware)
/document-prep --review <file>            # Structured peer review of a manuscript
/document-prep --cite <doi|arxiv|query>   # Look up and format citations as BibTeX
/document-prep --compile [file]           # Compile document to PDF
/document-prep --templates                # List available document templates
```

### Reference (lookup and checking)

```
/document-prep --template <format>  # Generate a template/preamble for a target format
/document-prep --notation           # Show the project notation registry
/document-prep --style <venue>      # Style summary for a target venue
/document-prep --check <file>       # Review a document for formatting issues
/document-prep --submission         # Submission checklist
/document-prep --bib                # Bibliography setup guide
/document-prep --index              # Show the formatter's research document index
```

## Parse Arguments

Extract the subcommand flag and its argument from the invocation. The first token is the subcommand flag. Anything after it is the argument.

If no arguments provided or `--help`, show the usage block above and stop.

---

## Discovery: Find Resources

Before executing any subcommand, discover the project's formatting resources:

### Step 1: Find document templates

Search for `artifacts/document-templates/` in the project root. This contains format-specific templates installed during project scaffolding (see `unfold-document-prep.md`).

Supported subdirectories: `latex/`, `typst/`, `markdown/`.

### Step 2: Find the formatter agent

Search `.claude/agents/` for an agent whose description contains "format", "typeset", "document preparation", or "notation". This is the project's formatter agent.

If no formatter agent exists, report:
```
No formatter agent found in .claude/agents/.
Create one with: /new-researcher --archetype formatter <domain>
(e.g., /new-researcher --archetype formatter "LaTeX academic publishing")
```
For `--new`, `--draft`, `--review`, `--cite`, `--compile`, `--check`, and `--notation`: proceed without the agent (use templates + general knowledge). For `--template`, `--style`, `--bib`, `--index`: check formatter corpus, use general knowledge if absent.

### Step 3: Find the research corpus

If the formatter agent exists, search `researchers/` for its research corpus. Read the corpus index if found.

---

## Building Subcommands

### `--new <type> [title]`

Create a new document from a shipped template.

**Available template types** (LaTeX):

| Type | Template File | Document Class | Use For |
|:-----|:-------------|:---------------|:--------|
| `paper` | `paper-standard.tex` | `article` | Generic research paper |
| `paper-ieee` | `paper-ieee.tex` | `IEEEtran` | IEEE conference/journal |
| `paper-acm` | `paper-acm.tex` | ACM format | ACM conference/journal |
| `poster` | `poster-academic.tex` | `article` (A0) | Academic conference poster |
| `slides` | `presentation-beamer.tex` | `beamer` | Conference talk, seminar, defense |
| `thesis` | `thesis-standard.tex` | `report` | PhD/Master's thesis |
| `report` | `report-scientific.tex` | `report` | Lab/scientific report |
| `report-tech` | `report-technical.tex` | `report` | Technical report |
| `letter` | `letter-formal.tex` | letter | Formal/cover letter |
| `cv` | `cv-modern.tex` | custom | Academic CV |
| `book` | `book-standard.tex` | `book` | Book/monograph |
| `newsletter` | `newsletter.tex` | custom | Newsletter |
| `blank` | `blank.tex` | `article` | Empty starting point |

**Steps:**

1. Match `<type>` against the template table. If no match, show the table and stop.
2. Read the template file from `artifacts/document-templates/latex/<type>.tex`. If templates directory doesn't exist, report: "No document templates installed. Run project scaffolding with a document format selection, or manually copy templates to `artifacts/document-templates/latex/`."
3. Ask the user for a target directory (default: current directory) and filename.
4. Customize the template:
   - Replace placeholder title with `[title]`, or leave `{Title}` if none given.
   - Replace placeholder author/institution with `{Author Name}` / `{Institution}`.
   - Keep all structural sections intact.
5. If a `references.bib` template exists, copy it alongside the `.tex` file.
6. Write the customized files to the target directory.
7. Report what was created and suggest next steps.

**Type-specific guidance (include as LaTeX comments):**

- **paper / paper-ieee / paper-acm**: IMRAD structure. Abstract 150-300 words.
- **poster**: A0 portrait. Max 800 words total. 5-6 sections. Title 72-120pt, body 28-36pt. Three columns.
- **slides**: ~1 slide per minute. 60-70% visual, 30-40% text. Body 24-28pt.
- **thesis**: Front matter (declaration, abstract, acknowledgements, TOC). Main chapters. Appendices.
- **report**: Highlight boxes for key findings. Summary statistics tables.

### `--draft <section> [file]`

Write or expand a section of an existing document.

**Steps:**

1. If `[file]` provided, read it. Otherwise, search for document files (`.tex`, `.typ`, `.md`) in current directory and ask which one.
2. Identify document type from content/extension.
3. Locate the target `<section>`. Match flexibly:
   - `abstract`, `introduction`, `intro`
   - `methods`, `methodology`, `materials`, `approach`, `proposed`, `framework`
   - `results`, `experiments`, `evaluation`
   - `discussion`, `analysis`
   - `conclusion`, `summary`, `future`
   - `related`, `background`, `literature`, `prior`
   - For slides: frame titles. For thesis: chapter names.
4. Apply the **two-stage writing process**:

   **Stage 1 — Outline**: Generate a structured outline:
   - 3-7 key points with supporting sub-points
   - Mark citations needed as `\cite{needed:topic}` (LaTeX) or `[?topic]` (Markdown)
   - Mark figures/tables needed as comments
   - Present to user for approval

   **Stage 2 — Prose**: Convert approved outline to flowing scientific prose:
   - Write in full paragraphs (NEVER bullet points in the document body)
   - Follow IMRAD conventions for the section type
   - Use precise, field-appropriate terminology
   - Include equation/code environments where needed

5. Edit the section content into the file using the Edit tool.

**Section-specific guidance:**

| Section | Key Requirements |
|:--------|:----------------|
| Abstract | Self-contained. Problem, method, result, implication. 150-300 words. |
| Introduction | Context, gap, contribution, outline. Final paragraph: numbered contributions. |
| Methods | Reproducible detail. Define all variables. State assumptions. |
| Results | Present without interpretation. One message per figure/table. |
| Discussion | Interpret. Compare to prior work. Limitations. Implications. |
| Conclusion | 1-2 paragraphs. Contribution summary (not results). Future directions. |

### `--review <file>`

Structured peer review of a manuscript.

**Steps:**

1. Read the file (`.tex`, `.typ`, `.md`, or `.pdf`).
2. Perform a systematic 7-stage review:

   **Stage 1 — First Impression**: Novelty, significance, scope.

   **Stage 2 — Section-by-Section**: Title/Abstract accuracy, Introduction clarity, Methods rigor, Results validity, Discussion interpretation, References coverage.

   **Stage 3 — Technical Rigor**: Mathematical correctness, statistical methods, experimental design, computational reproducibility.

   **Stage 4 — Figures and Tables**: Quality, readability, accessibility, axis labels, error bars, captions, data integrity.

   **Stage 5 — Writing Quality**: Clarity, conciseness, grammar, logical flow.

3. Output a structured review report:

```markdown
## Summary Statement
[2-3 sentences on contribution and assessment]

## Major Issues (must address before publication)
1. [Issue with location and suggestion]

## Minor Issues (should address)
1. [Issue with line/section reference]

## Line-by-Line Comments
- L42: [specific comment]

## Questions for Authors
1. [Clarification needed]

## Recommendation
[ ] Accept as-is
[ ] Minor revision
[ ] Major revision
[ ] Reject
```

### `--cite <identifier>`

Look up a citation and format as BibTeX.

**Steps:**

1. Determine identifier type:
   - DOI (contains `10.`): fetch from `https://doi.org/<doi>` with Accept: `application/x-bibtex`
   - arXiv ID (e.g., `2103.14030`): fetch from arXiv and construct BibTeX
   - Free text: use WebSearch to find the paper, extract DOI, then fetch

2. Clean and format the BibTeX entry:
   - Citation key: `FirstAuthor2024keyword`
   - Protect capitalization with `{}`
   - Use `--` for page ranges
   - Include DOI field
   - Remove unnecessary fields

3. Output the formatted entry.

4. If a `.bib` file exists in current directory, offer to append.

**Batch mode**: comma-separated or one-per-line identifiers.

### `--compile [file]`

Compile a document to PDF.

**Steps:**

1. If `[file]` not given, find the main document file in current directory.
2. Detect format:
   - `.tex`: check for `pdflatex`, `xelatex`, `lualatex`, or `latexmk`
   - `.typ`: check for `typst`
   - `.md`: check for `pandoc`
3. Compile with the appropriate engine:

   **LaTeX:**
   ```bash
   pdflatex -interaction=nonstopmode <file> && \
   bibtex <basename> 2>/dev/null; \
   pdflatex -interaction=nonstopmode <file> && \
   pdflatex -interaction=nonstopmode <file>
   ```

   **Typst:**
   ```bash
   typst compile <file>
   ```

   **Markdown:**
   ```bash
   pandoc <file> -o <basename>.pdf
   ```

4. Parse log/output for errors and warnings. Report with line numbers.
5. If compiler not found, suggest installation.

### `--templates`

List all available document templates.

Read `artifacts/document-templates/` and show what's installed:
- Template name (the `--new` type argument)
- Format (LaTeX/Typst/Markdown)
- Document class
- Whether a `.bib` template is included

---

## Reference Subcommands

### `--template <format>`

Generate a complete document template/preamble for a target format or venue.

**Steps:**
1. Search formatter's research corpus for style guides matching `<format>`.
2. If found, read and extract: document class, required packages, standard structure.
3. Read notation/macro reference documents if available.
4. Assemble a complete template in a code block with comments.

If no corpus match, check `artifacts/document-templates/` for a shipped template matching the format. If neither exists, list available options.

### `--notation`

Show the project's notation registry from the formatter agent's memory or research corpus.

### `--style <venue>`

Concise style summary for a named venue: document class, page limits, bibliography format, figure requirements, abstract limits, submission portal, review timeline.

### `--check <file>`

Review a document for formatting issues: structural problems, notation consistency, format compliance, common mistakes, reference integrity. Output categorized issues with line numbers.

### `--submission`

Generate a submission checklist (pre-submission, metadata, file package, post-submission). Augment with venue-specific items from the formatter's corpus.

### `--bib`

Bibliography setup guide: format compatibility matrix, reference source workflows, single-source strategy, citation commands.

### `--index`

Show the formatter's research corpus index.

---

## Format-Specific Constraints

### Posters

- **Content**: Max 300-800 words total body text
- **Sections**: 5-6 for A0, 4-5 for A1
- **Fonts**: Title 72-120pt, headers 40-48pt, body 28-36pt, refs 24pt
- **Layout**: 3 columns for A0 portrait
- **Color**: Cohesive theme, colorblind accessible
- **Test**: Readable from 1.5 meters

### Slides

- **Density**: ~1 slide per minute
- **Content**: 60-70% visual, 30-40% text
- **Fonts**: Body 24-28pt, titles 36-44pt
- **Anti-patterns**: No text walls, no full sentences, max 6 bullets/slide
- **Talk types**: Conference 10-15 slides, seminar 30-40, defense 35-45, lightning 5-7

### Grant Proposals

- **NSF**: Intellectual Merit + Broader Impacts. 15-page description.
- **NIH**: Significance, Innovation, Approach. R01 = 12 pages.
- **DOE**: Technical narrative. Mission relevance. Milestones.
- **General**: Objectives in first paragraph. Preliminary data. Timeline figure.

---

## Spawning the Formatter Agent

For heavy lifting (full document drafting, multi-section notation audits, submission package assembly), spawn the formatter agent instead of using this skill inline.

## Error Handling

- If `--new <type>` doesn't match: show template table
- If `--draft <section>` not found in file: list sections present
- If file doesn't exist: report not found
- If no document files found: suggest `--new <type>`
- If compiler not found: provide installation instructions
- If no arguments given: show usage block
- If formatter corpus missing: proceed with shipped templates + general knowledge
