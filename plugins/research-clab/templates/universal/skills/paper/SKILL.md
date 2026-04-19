---
name: paper
description: Scientific document builder — create papers, posters, slides, theses, reports from templates. Draft sections, peer review manuscripts, manage citations, compile LaTeX.
argument-hint: new <type> [title] | draft <section> [file] | review <file> | cite <doi|query> | compile [file] | templates
allowed-tools: Read Write Edit Bash Grep Glob WebSearch WebFetch
metadata:
    derived-from: K-Dense-AI/claude-scientific-skills (MIT License)
    original-skills: scientific-writing, venue-templates, latex-posters, scientific-slides, peer-review, research-grants
    templates-from: delibae/claude-prism (apps/desktop/public/examples)
---

# Paper — Scientific Document Builder

Create, draft, review, and compile scientific documents. Templates in `artifacts/claude-prism-examples/`.

> Derived from [K-Dense-AI/claude-scientific-skills](https://github.com/K-Dense-AI/claude-scientific-skills) (MIT) and [claude-prism](https://github.com/delibae/claude-prism) templates. Consolidated into a single Claude Code skill.

## Usage

```
/paper new <type> [title]       # Scaffold a new document from template
/paper draft <section> [file]   # Write or expand a section (IMRAD-aware)
/paper review <file>            # Structured peer review of a manuscript
/paper cite <doi|arxiv|query>   # Look up and format citations as BibTeX
/paper compile [file]           # Compile LaTeX to PDF
/paper templates                # List available templates
```

## Parse Arguments

Extract the subcommand (first token) and remaining arguments. If no arguments, show the usage block above and stop.

---

## Available Templates

| Type | Template Source | Document Class | Use For |
|:-----|:--------------|:---------------|:--------|
| `paper` | `paper-standard/` | `article` | Generic research paper |
| `paper-ieee` | `paper-ieee/` | `IEEEtran` | IEEE conference/journal |
| `paper-acm` | `paper-acm/` | ACM format | ACM conference/journal |
| `poster` | `poster-academic/` | `article` (A0) | Academic conference poster |
| `slides` | `presentation-beamer/` | `beamer` | Conference talk, seminar, defense |
| `thesis` | `thesis-standard/` | `report` | PhD/Master's thesis |
| `report` | `report-scientific/` | `report` | Lab/scientific report |
| `report-tech` | `report-technical/` | `report` | Technical report |
| `letter` | `letter-formal/` | letter class | Formal/cover letter |
| `cv` | `cv-modern/` | custom | Academic CV |
| `book` | `book-standard/` | `book` | Book/monograph |
| `newsletter` | `newsletter/` | custom | Newsletter |
| `blank` | `blank/` | `article` | Empty starting point |

---

## Subcommand Implementations

### `new <type> [title]`

Create a new LaTeX document from a template.

**Steps:**

1. Match `<type>` against the template table above. If no match, show the table and stop.
2. Read the template `.tex` file from `artifacts/claude-prism-examples/<template-dir>/main.tex`.
3. If a `references.bib` exists in the template dir, read that too.
4. Ask the user for a target directory (default: current directory) and filename.
5. Customize the template:
   - Replace the placeholder title with the provided `[title]`, or leave `{Title}` if none given.
   - Replace placeholder author/institution with `{Author Name}` / `{Institution}`.
   - Keep all structural sections intact.
   - For `poster`: preserve the color theme, font sizes, and multicol layout.
   - For `slides`: preserve the beamer theme and frame structure.
   - For `thesis`: preserve the declaration, abstract, acknowledgements, chapter structure.
6. Write the customized `.tex` file and `.bib` file (if applicable) to the target directory.
7. Report what was created and suggest next steps (e.g., `/paper draft introduction my_paper.tex`).

**Type-specific guidance to include as LaTeX comments:**

- **paper / paper-ieee / paper-acm**: IMRAD structure. Abstract 150-300 words. Introduction states contribution clearly.
- **poster**: A0 portrait. Max 800 words total. 5-6 sections. Title 72-120pt, headers 40-48pt, body 28-36pt. Three columns.
- **slides**: ~1 slide per minute. 60-70% visual, 30-40% text. Body font 24-28pt, titles 36-44pt.
- **thesis**: Front matter (declaration, abstract, acknowledgements, TOC). Main chapters. Appendices. Bibliography.
- **report**: Highlight boxes for key findings. Summary statistics tables. Note boxes for methodology details.

### `draft <section> [file]`

Write or expand a section of an existing document.

**Steps:**

1. If `[file]` is provided, read it. Otherwise, search for `.tex` files in the current directory and ask which one.
2. Identify the document type from the `\documentclass`.
3. Locate the target `<section>` in the document. Section names are flexible — match against:
   - `abstract`, `introduction`, `intro`
   - `methods`, `methodology`, `materials`, `approach`, `proposed`, `framework`
   - `results`, `experiments`, `evaluation`
   - `discussion`, `analysis`
   - `conclusion`, `summary`, `future`
   - `related`, `background`, `literature`, `prior`
   - For slides: frame titles. For thesis: chapter names.
4. Apply the **two-stage writing process**:

   **Stage 1 — Outline**: Generate a structured outline of key points for the section:
   - 3-7 key points, each with 1-2 supporting sub-points
   - Identify citations needed (mark as `\cite{needed:topic}`)
   - Identify figures/tables needed (mark as `% TODO: Figure — description`)
   - Present outline to user for approval

   **Stage 2 — Prose**: Convert approved outline to flowing scientific prose:
   - Write in full paragraphs (NEVER bullet points in the paper body)
   - Follow IMRAD conventions for the section type
   - Use precise, field-appropriate terminology
   - Maintain logical flow with transition sentences
   - Include equation environments where needed
   - Mark citation placeholders

5. Edit the section content into the `.tex` file using the Edit tool.

**Section-specific writing guidance:**

| Section | Key Requirements |
|:--------|:----------------|
| Abstract | Self-contained. State: problem, method, key result, implication. 150-300 words. |
| Introduction | Context → gap → contribution → outline. Final paragraph states contributions as numbered list. |
| Methods | Reproducible detail. Define all variables. State assumptions. Reference prior methods. |
| Results | Present findings without interpretation. One key message per figure/table. Statistical significance. |
| Discussion | Interpret results. Compare to prior work. Acknowledge limitations. State implications. |
| Conclusion | 1-2 paragraphs. Summarize contribution (not results). Future directions. |

### `review <file>`

Structured peer review of a manuscript.

**Steps:**

1. Read the `.tex` or `.pdf` file.
2. Perform a systematic 7-stage review:

   **Stage 1 — First Impression** (30 seconds):
   - Novelty and significance assessment
   - Scope and fit for target venue
   - Overall quality impression

   **Stage 2 — Section-by-Section**:
   - **Title/Abstract**: Accuracy, completeness, word count
   - **Introduction**: Context, gap, contribution clarity
   - **Methods**: Reproducibility, rigor, completeness
   - **Results**: Presentation quality, statistical validity
   - **Discussion**: Interpretation accuracy, limitations acknowledged
   - **References**: Coverage, recency, self-citation balance

   **Stage 3 — Technical Rigor**:
   - Mathematical correctness (verify key derivations)
   - Statistical methods appropriate for data type
   - Experimental design (controls, replication, blinding)
   - Computational reproducibility (code, data availability)

   **Stage 4 — Figures and Tables**:
   - Quality, readability, colorblind accessibility
   - Axis labels, units, error bars, captions
   - Data integrity (consistent numbers across text/figures/tables)

   **Stage 5 — Writing Quality**:
   - Clarity, conciseness, grammar
   - Logical flow between sections and paragraphs
   - Jargon appropriate for audience

3. Output a structured review report:

```markdown
## Summary Statement
[2-3 sentences on the paper's contribution and overall assessment]

## Major Issues (must address before publication)
1. [Issue with specific location and suggestion]
...

## Minor Issues (should address)
1. [Issue with line/section reference]
...

## Line-by-Line Comments
- L42: [specific comment]
...

## Questions for Authors
1. [Clarification needed]
...

## Recommendation
[ ] Accept as-is
[ ] Minor revision
[ ] Major revision
[ ] Reject
```

### `cite <identifier>`

Look up a citation and format as BibTeX.

**Steps:**

1. Determine identifier type:
   - DOI (contains `10.`): fetch metadata from `https://doi.org/<doi>` with Accept: `application/x-bibtex`
   - arXiv ID (e.g., `2103.14030`): fetch from `https://arxiv.org/abs/<id>` and construct BibTeX
   - PMID (numeric): construct PubMed lookup URL
   - Free text query: use WebSearch to find the paper, extract DOI, then fetch BibTeX

2. For DOI resolution, use WebFetch:
   ```
   WebFetch("https://doi.org/<doi>", headers: {"Accept": "application/x-bibtex"})
   ```

3. Clean and format the BibTeX entry:
   - Generate a meaningful citation key: `FirstAuthor2024keyword`
   - Protect capitalization in titles with `{}`
   - Use `--` for page ranges
   - Include DOI field
   - Remove unnecessary fields (abstract, month, keywords unless useful)

4. Output the formatted BibTeX entry.

5. If a `.bib` file exists in the current directory, offer to append the entry.

**Batch mode**: If multiple identifiers are provided (comma-separated or one per line), process each and combine.

### `compile [file]`

Compile a LaTeX document to PDF.

**Steps:**

1. If `[file]` not given, find `.tex` files in current directory. Use the one that contains `\begin{document}`.
2. Check for LaTeX compiler availability:
   ```bash
   which pdflatex || which xelatex || which lualatex
   ```
3. If no compiler found, suggest installation:
   - Windows: MiKTeX or TeX Live (`winget install MiKTeX.MiKTeX`)
   - Check if `latexmk` is available for automated multi-pass compilation
4. Compile with the appropriate engine:
   ```bash
   # Standard compilation (handles references, TOC, etc.)
   pdflatex -interaction=nonstopmode <file> && \
   bibtex <basename> 2>/dev/null; \
   pdflatex -interaction=nonstopmode <file> && \
   pdflatex -interaction=nonstopmode <file>
   ```
   Or if `latexmk` is available:
   ```bash
   latexmk -pdf -interaction=nonstopmode <file>
   ```
5. Parse the log file for errors and warnings:
   - **Errors**: Report with line numbers and context
   - **Warnings**: Report overfull/underfull boxes, undefined references, missing citations
   - **Success**: Report page count and output PDF path
6. If errors occur, attempt to diagnose and fix common issues:
   - Missing packages: suggest `\usepackage{}` additions
   - Undefined control sequences: identify the command and suggest fixes
   - Missing files: check paths

### `templates`

List all available templates with descriptions.

**Steps:**

1. Read the template directories in `artifacts/claude-prism-examples/`.
2. For each directory, check for `main.tex` and `references.bib`.
3. Display a formatted table showing:
   - Template name (the `/paper new` type argument)
   - Document class
   - Includes bibliography template (yes/no)
   - Brief description

---

## Poster-Specific Guidance

When creating or drafting poster content, enforce these constraints:

- **Content limit**: Max 300-800 words total body text
- **Section limit**: 5-6 sections for A0, 4-5 for A1
- **Font sizes**: Title 72-120pt, section headers 40-48pt, body 28-36pt, references 24pt
- **Layout**: 3 columns for A0 portrait (use `multicol`)
- **Color**: Use a cohesive theme. Ensure colorblind accessibility (avoid red-green only distinctions)
- **Figures**: Large, clear, self-explanatory. Minimum 300 DPI
- **Readability test**: Can someone read it from 1.5 meters away?

## Slides-Specific Guidance

When creating or drafting slides:

- **Density**: ~1 slide per minute of talk time
- **Content split**: 60-70% visual (figures, diagrams, equations), 30-40% text
- **Font**: Body 24-28pt minimum, titles 36-44pt
- **Structure**: Title → Outline → Background → Methods → Results → Conclusion → Questions
- **Anti-patterns**: No walls of text. No full sentences (use key phrases). No more than 6 bullet points per slide.
- **Talk types**:
  - Conference (10-20 min): 10-15 content slides + title/questions
  - Seminar (45-60 min): 30-40 content slides
  - Defense (60 min): 35-45 slides + backup slides
  - Lightning (5 min): 5-7 slides, no outline slide

## Grant-Specific Guidance

When creating grant proposals (use `report` or `blank` template):

- **NSF**: Intellectual Merit + Broader Impacts. 15-page project description. Specific Aims first.
- **NIH**: Significance, Innovation, Approach, Investigators, Environment. R01 = 12 pages.
- **DOE**: Technical narrative. Mission relevance. Milestones and deliverables.
- **General**: State objectives in first paragraph. Use preliminary data. Include timeline figure. Budget justification should be detailed but concise.

## Error Handling

- If `<type>` doesn't match any template: show the template table
- If `<section>` not found in document: list the sections present and ask which one
- If `<file>` doesn't exist: report not found
- If no `.tex` files found: suggest `/paper new <type>`
- If LaTeX compiler not found: provide installation instructions
- If no arguments given: show usage block
