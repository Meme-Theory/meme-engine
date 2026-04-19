#!/usr/bin/env python3
"""
zbMATH Open MCP Server — Open-Access Math Literature Database

Wraps the public zbMATH Open REST API (api.zbmath.org/v1/) — distinct from
the paywalled zbMATH full service. Open-access endpoints cover bibliographic
metadata, authors, MSC 2020 classifications, and cross-references.

Agents use this to locate prior work on spectral geometry, NCG, KK reductions,
and submersion theory without needing arXiv IDs — zbMATH indexes published
journal articles + books, which arXiv does not consistently.
"""

import warnings
import os
warnings.filterwarnings("ignore")
os.environ["PYTHONWARNINGS"] = "ignore"

import asyncio
import json
import logging
from pathlib import Path

import httpx
import mcp.server.stdio
import mcp.types as types
from mcp.server import Server

SERVER_DIR = Path(__file__).resolve().parent
ZBMATH_BASE = "https://api.zbmath.org/v1"
USER_AGENT = "Ainulindale-Exflation/zbMATH-MCP (math-research)"
HTTP_TIMEOUT = 25.0

logging.basicConfig(
    level=logging.INFO,
    filename=str(SERVER_DIR / "zbmath_mcp.log"),
    filemode="w",
    format="%(asctime)s %(levelname)s %(message)s",
)
logger = logging.getLogger(__name__)

server = Server("zbmath")


async def _zb_get(path: str, params: dict | None = None) -> dict:
    async with httpx.AsyncClient(timeout=HTTP_TIMEOUT, headers={"User-Agent": USER_AGENT, "Accept": "application/json"}) as client:
        url = f"{ZBMATH_BASE}{path}"
        r = await client.get(url, params=params or {})
        r.raise_for_status()
        return r.json()


def _fmt_document(doc: dict) -> str:
    zbl = doc.get("id") or doc.get("zbl_id")
    zbmath_url = doc.get("zbmath_url")
    title_block = doc.get("title") or {}
    title = title_block.get("title") if isinstance(title_block, dict) else str(title_block)
    title = title or "(no title)"
    contribs = doc.get("contributors") or {}
    authors = contribs.get("authors") or []
    author_names = [a.get("name", "?") for a in authors if isinstance(a, dict)][:6]
    year = doc.get("year")
    source_block = doc.get("source") or {}
    source_text = source_block.get("source") if isinstance(source_block, dict) else None

    # MSC list: each {code, text, scheme}
    mscs = doc.get("msc") or []
    msc_codes = [m.get("code") for m in mscs if isinstance(m, dict) and m.get("code")][:8]

    # Links: list of {type, identifier, url}
    links = doc.get("links") or []
    doi = next((l.get("url") for l in links if isinstance(l, dict) and l.get("type") == "doi"), None)
    arxiv = next((l.get("identifier") for l in links if isinstance(l, dict) and l.get("type") == "arxiv"), None)

    lines = [f"### Zbl {zbl} — {title}"]
    if author_names:
        lines.append(f"- **Authors**: {'; '.join(author_names)}")
    if year:
        lines.append(f"- **Year**: {year}")
    if source_text:
        lines.append(f"- **Source**: {source_text}")
    if msc_codes:
        lines.append(f"- **MSC**: {', '.join(msc_codes)}")
    if doi:
        lines.append(f"- **DOI**: {doi}")
    if arxiv:
        lines.append(f"- **arXiv**: {arxiv}")
    if zbmath_url:
        lines.append(f"- **URL**: {zbmath_url}")
    elif zbl:
        lines.append(f"- **URL**: https://zbmath.org/?q=an:{zbl}")
    return "\n".join(lines)


def _fmt_author(a: dict) -> str:
    code = a.get("code")
    name = a.get("name") or "(unknown)"
    spellings = a.get("spellings") or []
    pub_count = spellings[0].get("count") if spellings and isinstance(spellings[0], dict) else None
    main_fields = a.get("main_fields") or []
    top_fields = [f"{f.get('field')}: {f.get('count')}" for f in main_fields[:4] if isinstance(f, dict)]
    awards = a.get("awards") or []
    award_titles = [aw.get("title") for aw in awards[:3] if isinstance(aw, dict) and aw.get("title")]
    zb_url = a.get("zbmath_url") or (f"https://zbmath.org/authors/{code}" if code else None)

    lines = [f"### {name} ({code})"]
    if pub_count is not None:
        lines.append(f"- **Publications (primary spelling)**: {pub_count}")
    if top_fields:
        lines.append(f"- **Main MSC fields**: {', '.join(top_fields)}")
    if award_titles:
        lines.append(f"- **Awards**: {'; '.join(award_titles)}")
    if zb_url:
        lines.append(f"- **URL**: {zb_url}")
    return "\n".join(lines)


def _status_total(data: dict) -> int:
    """Extract total result count from zbMATH's status block."""
    status = data.get("status") or {}
    if isinstance(status, dict):
        for key in ("nr_total_results", "total", "count"):
            if key in status:
                try:
                    return int(status[key])
                except (ValueError, TypeError):
                    pass
    return 0


def _fmt_msc(c: dict) -> str:
    code = c.get("code") or c.get("id")
    title = c.get("long_title") or c.get("short_title") or c.get("title") or c.get("text") or ""
    parent = c.get("parent")
    suffix = f" (parent: {parent})" if parent else ""
    return f"- **{code}** — {title}{suffix}"


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="search_zbmath",
            description=(
                "Search zbMATH Open documents (published journal articles, books). "
                "Query syntax supports fielded search: 'au:Connes' (author), 'ti:spectral triple' (title), "
                "'cc:58' (MSC class 58 = global analysis), free text, and AND/OR. "
                "Returns up to max_results with bibliographic metadata."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "max_results": {"type": "integer", "default": 10, "minimum": 1, "maximum": 50},
                },
                "required": ["query"],
            },
        ),
        types.Tool(
            name="get_zbmath_document",
            description="Fetch one zbMATH document by its Zbl ID (e.g. '1234.58008' or just the number).",
            inputSchema={
                "type": "object",
                "properties": {"doc_id": {"type": "string"}},
                "required": ["doc_id"],
            },
        ),
        types.Tool(
            name="search_zbmath_authors",
            description=(
                "Search zbMATH authors by name. Useful for disambiguating (zbMATH maintains "
                "stable author codes across name variants, unlike arXiv)."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "max_results": {"type": "integer", "default": 10, "minimum": 1, "maximum": 30},
                },
                "required": ["query"],
            },
        ),
        types.Tool(
            name="search_msc",
            description=(
                "Search the MSC 2020 classification tree. Takes either a code prefix "
                "('58J40' for spectral geometry on manifolds, '46L87' for NCG differential geometry) "
                "or a keyword ('noncommutative', 'Kaluza-Klein')."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "max_results": {"type": "integer", "default": 15, "minimum": 1, "maximum": 50},
                },
                "required": ["query"],
            },
        ),
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: dict | None) -> list[types.TextContent]:
    args = arguments or {}
    try:
        if name == "search_zbmath":
            return await _search_docs(args)
        if name == "get_zbmath_document":
            return await _get_doc(args)
        if name == "search_zbmath_authors":
            return await _search_authors(args)
        if name == "search_msc":
            return await _search_msc(args)
        return [types.TextContent(type="text", text=f"Unknown tool: {name}")]
    except httpx.HTTPStatusError as e:
        return [types.TextContent(type="text", text=f"zbMATH HTTP error: {e.response.status_code} on {e.request.url}")]
    except Exception as e:
        logger.exception("zbMATH tool error")
        return [types.TextContent(type="text", text=f"Error: {e}")]


async def _search_docs(args: dict) -> list[types.TextContent]:
    query = args["query"]
    max_results = int(args.get("max_results", 10))
    data = await _zb_get("/document/_search", {"search_string": query, "results_per_request": max_results})
    results = data.get("result") or []
    if not results:
        return [types.TextContent(type="text", text=f"No zbMATH matches for `{query}`")]
    total = _status_total(data) or len(results)
    blocks = [f"# zbMATH search: `{query}`\n- **Total**: {total}\n- **Showing**: {min(max_results, len(results))}\n"]
    for doc in results[:max_results]:
        blocks.append(_fmt_document(doc))
    return [types.TextContent(type="text", text="\n\n".join(blocks))]


async def _get_doc(args: dict) -> list[types.TextContent]:
    doc_id = args["doc_id"].strip()
    data = await _zb_get(f"/document/{doc_id}")
    doc = data.get("result") or data
    if not doc:
        return [types.TextContent(type="text", text=f"No zbMATH entry for `{doc_id}`")]
    return [types.TextContent(type="text", text=_fmt_document(doc))]


async def _search_authors(args: dict) -> list[types.TextContent]:
    query = args["query"]
    max_results = int(args.get("max_results", 10))
    data = await _zb_get("/author/_search", {"search_string": query, "results_per_request": max_results})
    results = data.get("result") or []
    if not results:
        return [types.TextContent(type="text", text=f"No zbMATH author matches for `{query}`")]
    total = _status_total(data) or len(results)
    blocks = [f"# zbMATH authors: `{query}`\n- **Total**: {total}\n"]
    for a in results[:max_results]:
        blocks.append(_fmt_author(a))
    return [types.TextContent(type="text", text="\n\n".join(blocks))]


async def _search_msc(args: dict) -> list[types.TextContent]:
    query = args["query"]
    max_results = int(args.get("max_results", 15))
    data = await _zb_get("/classification/_search", {"search_string": query, "results_per_request": max_results})
    results = data.get("result") or []
    if not results:
        return [types.TextContent(type="text", text=f"No MSC codes matched `{query}`")]
    total = _status_total(data) or len(results)
    lines = [f"# MSC 2020 matches: `{query}`\n- **Total**: {total}\n"]
    for c in results[:max_results]:
        lines.append(_fmt_msc(c))
    return [types.TextContent(type="text", text="\n".join(lines))]


async def main():
    logger.info("zbMATH MCP server starting...")
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
