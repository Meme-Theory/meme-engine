---
name: document-prep
description: Document preparation toolkit — templates, notation registry, format checking, submission workflows. Backed by the formatter agent's research corpus.
disable-model-invocation: true
argument-hint: --template <format> | --notation | --style <venue> | --check <file> | --submission | --bib | --index
---

# Document Prep — Format-Aware Document Toolkit

Quick access to document preparation expertise for the project. Discovers and uses the formatter agent's research corpus to provide format-specific guidance, notation registries, document checking, and submission workflows.

Unlike other skills, this one **adapts to whatever document formats the project uses** — LaTeX, Typst, markdown, HTML, or any other format. It discovers the project's formatting conventions from the formatter agent's research papers rather than hardcoding them.

## Usage

```
/document-prep --template jhep          # Generate a template/preamble for a target format
/document-prep --notation               # Show the project notation registry
/document-prep --style prd              # Style summary for a target venue
/document-prep --check paper.tex        # Review a document for formatting issues
/document-prep --submission             # Submission checklist for the project's target venue
/document-prep --bib                    # Bibliography setup guide
/document-prep --index                  # Show the formatter's research document index
```

## Parse Arguments

Extract the subcommand flag and its argument from the invocation. The first token is the subcommand flag. Anything after it is the argument.

If no arguments provided or `--help`, show the usage block above and stop.

---

## Discovery: Find the Formatter

Before executing any subcommand, discover the project's formatting resources:

### Step 1: Find the formatter agent

Search `.claude/agents/` for an agent whose description contains "format", "typeset", "document preparation", or "notation". This is the project's formatter agent (may be named `formatter.md`, `latex-typesetting-specialist.md`, `typst-formatter.md`, etc.).

If no formatter agent exists, report:
```
No formatter agent found in .claude/agents/.
Create one with: /new-researcher --archetype formatter <domain>
(e.g., /new-researcher --archetype formatter "LaTeX academic publishing")
```
For `--check` and `--notation`, proceed without the agent (use general knowledge). For other subcommands, stop here.

### Step 2: Find the research corpus

Search `researchers/` for a directory matching the formatter's domain. Common patterns:
- `researchers/LaTeX/`
- `researchers/Technical-Writing/`
- `researchers/Typst/`
- `researchers/Document-Formatting/`

Match by scanning `researchers/*/index.md` for directories whose content relates to document preparation, formatting, or typesetting.

If found, this is `{FORMATTER_CORPUS}`. If not found, the formatter agent has no research papers yet — suggest running `/new-researcher` to populate it.

### Step 3: Read the corpus index

If `{FORMATTER_CORPUS}` exists, read `{FORMATTER_CORPUS}/index.md` to understand what reference documents are available. Cache the document list for use by subcommands.

---

## Subcommand Implementations

### `--template <format>`

Generate a complete, ready-to-use document template/preamble for the specified format or venue.

**Steps:**
1. Search the formatter's research corpus for style guides matching `<format>` (case-insensitive substring match against document titles and filenames).
2. If a matching style guide exists, read it to extract: document class/format, required packages/imports, standard structure, metadata format.
3. Read any notation/macro reference documents in the corpus.
4. Assemble a complete template in a code block with comments explaining each section.

**What the template must include:**
1. The correct document class/format declaration for the venue
2. All required packages, imports, or dependencies
3. The project's notation macros (if a notation registry exists in the formatter's memory)
4. Standard environments/blocks (theorem, definition, proof, etc. — if applicable)
5. Comments explaining each block

If no matching style guide is found:
- List the available formats from the corpus index
- Suggest which one might be closest
- Offer to generate a generic template

### `--notation`

Show the project's notation registry — a quick-reference card of all project-specific symbols, abbreviations, and conventions.

**Steps:**
1. Check the formatter agent's memory (`.claude/agent-memory/{formatter-name}/notation-registry.md` or similar)
2. Check the research corpus for notation/symbol convention documents
3. If notation data exists, format as a markdown table:

| Symbol | Markup | Meaning | First Appears |
|:-------|:-------|:--------|:-------------|

Organized by category (domain-specific groupings).

If no notation registry exists:
```
No notation registry found.
The formatter agent builds this over time as the project develops notation conventions.
To bootstrap: describe your key symbols and run /document-prep --notation again.
```

### `--style <venue>`

Show a concise style summary for the named venue/format.

**Steps:**
1. Search the formatter's research corpus for a matching style guide.
2. Read it and extract a structured summary:

1. **Document class/format** and options
2. **Page limits** (if any)
3. **Bibliography** format and style
4. **Figure requirements** (format, resolution, color)
5. **Abstract** word limit and format
6. **Key formatting rules** (section numbering, equation numbering, appendices)
7. **Submission portal** URL (if documented)
8. **Typical review timeline** (if documented)

If no matching style guide is found, list available venues from the corpus index.

### `--check <file>`

Review a document file for formatting issues. Works with any format the formatter agent understands.

**Steps:**
1. Read the file using the Read tool.
2. Determine the format from the file extension and content (.tex, .typ, .md, .html, etc.).
3. If a formatter research corpus exists, load relevant style guides for the target format.
4. Check for:
   - **Structural issues**: missing required sections, broken cross-references, unmatched delimiters
   - **Notation consistency**: scan for variant spellings of project terms (if notation registry exists)
   - **Format compliance**: check document class/format against expected venue (if determinable)
   - **Common mistakes**: format-specific antipatterns (e.g., for LaTeX: double subscripts, missing `\,` in integrals; for markdown: broken link syntax, inconsistent heading levels)
   - **Reference integrity**: unresolved cross-references, missing bibliography entries
5. Output a categorized issue list with line numbers and suggested fixes.

### `--submission`

Generate a submission checklist for the project's target venue.

**Steps:**
1. Search the formatter's research corpus for submission workflow documents.
2. If found, read and extract checklist items.
3. Generate a markdown checklist organized by phase:

```markdown
## Submission Checklist

### Pre-submission
- [ ] Document compiles/renders cleanly with no warnings
- [ ] All cross-references resolve
- [ ] All figures present and correctly referenced
- [ ] Bibliography complete (no undefined citations, no unused entries)
- [ ] Notation consistent throughout (check notation registry)

### Metadata
- [ ] Title matches document exactly
- [ ] All authors with correct affiliations
- [ ] Abstract within word limit
- [ ] Keywords/categories selected
- [ ] Acknowledgments complete

### File Package
- [ ] All source files included
- [ ] Figures in correct format and resolution
- [ ] Supplementary materials prepared (if any)
- [ ] Total package size within limits

### Post-submission
- [ ] Verify rendering in submission system
- [ ] Check all cross-references in rendered output
- [ ] Confirm all figures appear correctly
- [ ] Note submission ID/reference number
```

Augment with venue-specific items from the research corpus if available.

### `--bib`

Bibliography setup guide for the project's target format(s).

**Steps:**
1. Search the formatter's research corpus for bibliography/reference management documents.
2. If found, generate:

1. **Format compatibility matrix**: which bibliography engines/styles work with which venues
2. **Reference source workflow**: how to export entries from domain-specific databases
3. **Single-source strategy**: one master bibliography file, venue-specific compilation
4. **Common citation commands**: format-specific citation syntax

If no bibliography guide exists in the corpus, provide a generic best-practices guide based on the detected document format.

### `--index`

Show the full document index of the formatter's research corpus.

**Steps:**
1. Read `{FORMATTER_CORPUS}/index.md`
2. Display it to the user
3. If no corpus exists, report that and suggest creating one

---

## Spawning the Formatter Agent

For complex tasks that exceed what this skill can do inline (writing full documents, multi-file template setup, extensive notation standardization), spawn the formatter agent instead:

```
Use the Agent tool with subagent_type = "{formatter-agent-name}" to handle:
- Full document drafting or restructuring
- Multi-section notation audits
- Template architecture for large multi-file documents
- Submission package assembly
```

This skill handles quick lookups and checks. The formatter agent handles heavy lifting.

## Error Handling

- If `--template` argument doesn't match any known format in the corpus: list available formats and stop
- If `--style` argument doesn't match: list available venues and stop
- If `--check` file doesn't exist: report file not found
- If no subcommand given: show usage block
- If formatter research corpus is missing: report which resources are missing and suggest `/new-researcher --archetype formatter <domain>` to populate
- If formatter agent doesn't exist but corpus does: skill works in degraded mode (read-only from corpus, no agent memory)

## Notes

- This skill reads from the formatter's research corpus — it does NOT require spawning the formatter agent for most operations
- The skill adapts to whatever format the project uses — it is NOT tied to any specific typesetting system
- All format-specific knowledge comes from the research corpus, not from hardcoded rules
- For projects that haven't created a formatter agent yet, `--check` and `--notation` still work using general-purpose formatting knowledge
