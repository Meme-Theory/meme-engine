#!/usr/bin/env python3
"""
MathSciNet MCP Server — AMS Mathematical Reviews

Provides two tiers of access:

1. FREE — MRef citation-matcher endpoint (no auth required). Takes a messy
   bibliographic string, returns the matched MR number + clean BibTeX.
   Endpoint: https://mathscinet.ams.org/mathscinet-mref

2. PAID — Full MathSciNet search (requires AMS institutional subscription).
   Activated only when MATHSCINET_API_KEY env var is set. Without the key,
   `search_mathscinet` returns a clear "subscription required" message
   instead of failing silently.

The free MRef tier alone is enormously useful for the project: it canonicalizes
sloppy citations from working papers into stable MR IDs + BibTeX for
cross-referencing against the researcher corpora.
"""

import warnings
import os
warnings.filterwarnings("ignore")
os.environ["PYTHONWARNINGS"] = "ignore"

import asyncio
import logging
import re
from pathlib import Path

import httpx
import mcp.server.stdio
import mcp.types as types
from mcp.server import Server

SERVER_DIR = Path(__file__).resolve().parent
MREF_URL = "https://mathscinet.ams.org/mathscinet-mref"
SEARCH_URL = "https://mathscinet.ams.org/mathscinet/api/publications/search"
USER_AGENT = "Ainulindale-Exflation/MathSciNet-MCP (math-research)"
HTTP_TIMEOUT = 25.0

logging.basicConfig(
    level=logging.INFO,
    filename=str(SERVER_DIR / "mathscinet_mcp.log"),
    filemode="w",
    format="%(asctime)s %(levelname)s %(message)s",
)
logger = logging.getLogger(__name__)

server = Server("mathscinet")

API_KEY = os.environ.get("MATHSCINET_API_KEY", "").strip()


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="lookup_mr_reference",
            description=(
                "FREE TIER. Resolve a messy bibliographic citation string into a "
                "matched MR number + clean BibTeX entry using the public MRef endpoint. "
                "Input can be a full author/title/journal string; MRef does fuzzy matching. "
                "Returns the matched MR number, BibTeX, and confidence signal."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "citation": {
                        "type": "string",
                        "description": "Rough bibliographic reference, e.g. 'Connes, Noncommutative Geometry, 1994'",
                    },
                },
                "required": ["citation"],
            },
        ),
        types.Tool(
            name="get_mr_bibtex",
            description=(
                "FREE TIER. Fetch BibTeX for a known MR number (e.g. 'MR1303779'). "
                "Uses the MRef endpoint with the MR id as the lookup term."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "mr_id": {"type": "string", "description": "MR number, e.g. 'MR1303779' or '1303779'"},
                },
                "required": ["mr_id"],
            },
        ),
        types.Tool(
            name="search_mathscinet",
            description=(
                "PAID TIER. Full-text search of MathSciNet's database. "
                "Requires the MATHSCINET_API_KEY environment variable to be set "
                "(your AMS institutional subscription key). "
                "Without a key, returns a clear 'subscription required' notice — "
                "use `lookup_mr_reference` for free citation resolution instead."
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
            name="mathscinet_status",
            description="Report access tier (free-only vs. with-API-key) for operator visibility.",
            inputSchema={"type": "object", "properties": {}},
        ),
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: dict | None) -> list[types.TextContent]:
    args = arguments or {}
    try:
        if name == "lookup_mr_reference":
            return await _lookup_mref(args["citation"])
        if name == "get_mr_bibtex":
            return await _lookup_mref(args["mr_id"])
        if name == "search_mathscinet":
            return await _search_mathscinet(args)
        if name == "mathscinet_status":
            return [types.TextContent(type="text", text=_status())]
        return [types.TextContent(type="text", text=f"Unknown tool: {name}")]
    except httpx.HTTPStatusError as e:
        return [types.TextContent(type="text", text=f"MathSciNet HTTP error: {e.response.status_code}")]
    except Exception as e:
        logger.exception("MathSciNet tool error")
        return [types.TextContent(type="text", text=f"Error: {e}")]


def _status() -> str:
    tier = "FREE (MRef only)" if not API_KEY else "FULL (MathSciNet search enabled)"
    return f"# MathSciNet MCP status\n- **Tier**: {tier}\n- **MRef endpoint**: {MREF_URL}\n- **API key set**: {'yes' if API_KEY else 'no — set MATHSCINET_API_KEY to enable full search'}\n"


async def _lookup_mref(citation: str) -> list[types.TextContent]:
    """Use the free MRef endpoint. It returns HTML with an embedded BibTeX pre-block."""
    async with httpx.AsyncClient(timeout=HTTP_TIMEOUT, headers={"User-Agent": USER_AGENT}) as client:
        r = await client.get(MREF_URL, params={"ref": citation, "dataType": "bibtex"})
        r.raise_for_status()
        text = r.text

    # MRef returns HTML with <pre>...</pre> containing BibTeX and an MR number.
    bib_match = re.search(r"<pre[^>]*>(.*?)</pre>", text, re.DOTALL | re.IGNORECASE)
    bibtex = bib_match.group(1).strip() if bib_match else None

    mr_match = re.search(r"(MR\d{5,8})", text)
    mr_id = mr_match.group(1) if mr_match else None

    # MRef signals no-match with phrases like "No Unique Match" or "0 matches"
    no_match = any(kw in text for kw in ("No Unique Match", "0 matches", "No matching records", "did not find any"))

    lines = [f"# MRef lookup: `{citation[:80]}{'...' if len(citation) > 80 else ''}`"]
    if no_match and not mr_id:
        lines.append("- **Result**: no unique match")
        lines.append("- MRef's fuzzy matcher couldn't resolve this citation. Try providing more of the title, author surname, or year.")
    else:
        if mr_id:
            lines.append(f"- **MR Number**: {mr_id}")
        if bibtex:
            lines.append("- **BibTeX**:")
            lines.append("```bibtex")
            # de-HTML common escapes
            clean = bibtex.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
            lines.append(clean)
            lines.append("```")
        if not bibtex and not mr_id:
            lines.append("- **Raw response** (no BibTeX extracted):")
            lines.append(text[:1500])
    return [types.TextContent(type="text", text="\n".join(lines))]


async def _search_mathscinet(args: dict) -> list[types.TextContent]:
    if not API_KEY:
        return [types.TextContent(type="text", text=(
            "# MathSciNet full search unavailable\n"
            "- The `search_mathscinet` tool requires an AMS MathSciNet subscription.\n"
            "- Set the `MATHSCINET_API_KEY` environment variable with your institutional API key.\n"
            "- For free citation resolution, use `lookup_mr_reference` instead — it uses the public MRef endpoint.\n"
            "- Alternative free math-literature search: use the `zbmath` MCP server."
        ))]

    query = args["query"]
    max_results = int(args.get("max_results", 10))
    async with httpx.AsyncClient(timeout=HTTP_TIMEOUT, headers={"User-Agent": USER_AGENT, "x-api-key": API_KEY}) as client:
        r = await client.get(SEARCH_URL, params={"q": query, "size": max_results})
        r.raise_for_status()
        data = r.json()
    hits = data.get("results") or data.get("hits") or []
    if not hits:
        return [types.TextContent(type="text", text=f"No MathSciNet results for `{query}`")]
    lines = [f"# MathSciNet search: `{query}`\n- **Total**: {data.get('total', len(hits))}\n"]
    for h in hits[:max_results]:
        mr = h.get("paperId") or h.get("mr") or "?"
        title = h.get("title", "(no title)")
        authors = h.get("authors", [])
        year = h.get("year", "")
        lines.append(f"### MR{mr} — {title}")
        if authors:
            lines.append(f"- **Authors**: {'; '.join(a.get('name', a) if isinstance(a, dict) else str(a) for a in authors[:6])}")
        if year:
            lines.append(f"- **Year**: {year}")
    return [types.TextContent(type="text", text="\n".join(lines))]


async def main():
    logger.info("MathSciNet MCP server starting... (tier=%s)", "FULL" if API_KEY else "FREE")
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
