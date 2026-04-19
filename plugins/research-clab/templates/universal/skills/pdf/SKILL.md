---
name: pdf
description: Read and process PDF files that exceed the Read tool's 10-page limit on Windows
argument-hint: <pdf_path> [prompt]
---

# /pdf — PDF Workaround Skill

Process PDF files by splitting into 10-page chunks, reading each, and synthesizing results. Works around the Read tool's broken `pages` parameter on Windows (claude-code#30819).

## Usage

```
/pdf path/to/paper.pdf
/pdf path/to/paper.pdf "Extract all equations involving the core operator"
/pdf path/to/paper.pdf "Summarize sections 3-5"
/pdf path/to/paper.pdf "Find all references to <topic>"
```

## Arguments

- **First argument** (required): Path to the PDF file
- **Second argument** (optional): A prompt describing what to extract, summarize, or review. If omitted, produces a structured summary of the entire document.

## Execution Steps

### Step 1: Validate and Split

Run the splitter script to create 10-page chunks:

```bash
"<project-venv>/Scripts/python.exe" tools/pdf-extract-pages.py "<pdf_path>" --batch
```

This creates a directory `<pdf_stem>_chunks/` with files like `<pdf_stem>_p001-010.pdf`, `<pdf_stem>_p011-020.pdf`, etc.

If the PDF is ≤10 pages, skip splitting — just read it directly.

### Step 2: Read ALL Chunks

**READ THE ENTIRE DOCUMENT.** Read every chunk file sequentially using the Read tool **WITHOUT the `pages` parameter**. Do NOT skip chunks. Do NOT read only a subset and call it done.

The ONLY exception to reading all chunks is when the user's prompt is a **narrow targeted search** — something like "find equation 3.7" or "what does page 45 say about X." In that case you may read selectively. But if the prompt is a summary, review, synthesis, or any open-ended analysis: **read every page**.

As you read each chunk, extract and note:
- Key content relevant to the user's prompt (if provided)
- Section headings, theorem numbers, equation numbers
- Important definitions, results, or claims
- Page numbers from the original document (chunk filename tells you the range)

### Step 3: Synthesize

After reading ALL chunks:

**If a prompt was provided:** Answer the user's question or perform the requested analysis using the accumulated content from all chunks. Cite page numbers from the original document.

**If no prompt was provided:** Produce a structured summary:
```
## Document Overview
- Title, authors, year, arXiv ID (if available)
- Total pages, sections

## Key Content
- Main results/theorems with page references
- Important equations (with equation numbers)
- Methodology overview

## Relevance to Framework
- Connections to this project's framework (if any)
- Key concepts that map to the project's terminology
```

### Step 4: Cleanup

After synthesis is complete, delete the chunks directory:

```bash
rm -rf "<chunks_directory>"
```

## Rules

- **READ THE WHOLE DOCUMENT** unless the prompt is a narrow targeted search for a specific item.
- **NEVER use the `pages` parameter** on the Read tool. It is broken on Windows.
- Read chunks sequentially, not in parallel (context accumulation matters).
- If a chunk fails to read, note it and continue with the remaining chunks.
- Always cite original page numbers (derived from chunk filenames), not chunk-internal page numbers.
- Do NOT ask "should I read the rest?" — just read it. The user invoked /pdf because they want the whole thing processed.
