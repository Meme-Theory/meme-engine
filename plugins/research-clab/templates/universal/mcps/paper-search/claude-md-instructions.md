### Paper-Search MCP

Tools for searching and downloading academic papers. **CRITICAL**: `search_arxiv` passes queries directly to the arXiv API -- use arXiv API query syntax, NOT natural language.

**arXiv API Query Syntax** (required for `search_arxiv`):

**CRITICAL**: The `ti:`, `au:`, `abs:` prefixes bind to ONE token only. Multi-word after a prefix silently drops to all-fields search and returns garbage (latest papers). Every keyword needs its own prefix, joined by AND.

- Author search: `au:LastName_FirstName` (e.g., `au:Mack_Katherine`, `au:Volovik_G`)
- Title search: **one `ti:` per word**, joined with AND (e.g., `ti:dark AND ti:matter AND ti:annihilation`)
- Abstract search: `abs:keyword` (one per word, join with AND)
- All fields: `all:keyword`
- Category: `cat:astro-ph.CO`, `cat:hep-th`, etc.
- Combine fields: `au:Mack_Katherine AND ti:dark AND ti:matter`
- **WRONG**: `ti:dark matter annihilation` (only `dark` hits title; rest is orphaned, returns garbage)
- **WRONG**: `"Katherine Mack dark matter"` (natural language, returns latest papers, ignores query)
- **RIGHT**: `au:Mack_Katherine AND ti:dark AND ti:matter`
- **RIGHT**: `au:Baptista AND ti:higher AND ti:dimensional AND ti:Standard AND ti:Model`

**Search tools** (all take `query: str, max_results: int`):
- `search_arxiv(query, max_results)` -- arXiv preprints (use API syntax above)
- `search_google_scholar(query, max_results)` -- broad academic search (natural language OK)
- `search_pubmed(query, max_results)` -- biomedical literature
- `search_biorxiv(query, max_results)` -- biology preprints
- `search_medrxiv(query, max_results)` -- medical preprints

**Download/Read tools**:
- `download_arxiv(paper_id, save_path)` -- download PDF (e.g., `paper_id="1309.7783"`, `save_path="./downloads"`)
- `read_arxiv_paper(paper_id, save_path)` -- extract text from PDF (downloads first if needed)
- `download_biorxiv(paper_id, save_path)` -- download bioRxiv PDF by DOI
- `download_medrxiv(paper_id, save_path)` -- download medRxiv PDF by DOI
- `read_biorxiv_paper(paper_id, save_path)` -- extract text from bioRxiv PDF
- `read_medrxiv_paper(paper_id, save_path)` -- extract text from medRxiv PDF

**Workflow for researcher corpus building**:
1. `search_arxiv` with `au:` syntax to find paper IDs
2. `download_arxiv` each paper to `./downloads/`
3. `read_arxiv_paper` or Read tool on the PDFs to extract content
4. Spawn synthesis agents to write markdown reference docs from the downloaded content

**Limitations**:
- Google Scholar: no direct PDF download (scrapes metadata only, may be rate-limited)
- PubMed: metadata and abstracts only (no PDF download)
- bioRxiv/medRxiv: category-based search within a date range (default 30 days)
- arXiv: query syntax is strict -- malformed queries silently return garbage, not errors
