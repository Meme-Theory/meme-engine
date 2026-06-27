### zbMATH MCP — zbMATH Open

Queries zbMATH Open (the reviewing service formerly known as Zentralblatt MATH) for documents, authors, and MSC subject classifications. Bundled source at `tools/mcp-servers/zbmath-mcp/server.py` after install.

**Tools:**

| Tool | Purpose |
|:-----|:--------|
| `search_zbmath(query, ...)` | Document search. Supports author / title / MSC / year filters. |
| `get_zbmath_document(id)` | Full metadata for one zbMATH document ID. |
| `search_zbmath_authors(query)` | Author search (disambiguates duplicate name entries). |
| `search_msc(query)` | MSC 2020 subject-classification lookup. |

**Guidance:**

- zbMATH Open is free (unlike MathSciNet) — no subscription needed.
- zbMATH IDs (e.g., `Zbl 1234.56789`) are stable citation anchors. Pair with MR numbers from the MathSciNet MCP for maximum bibliographic coverage; some papers have only one.
- `search_msc` is useful when positioning the project's research within the MSC hierarchy — the result can seed the project's `artifacts/manuscript.tex` `\subjclass` line.
- The `bridge` agent (math flavoring) uses zbMATH alongside MathSciNet for primary-source fidelity work.
