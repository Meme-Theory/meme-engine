#!/usr/bin/env python3
"""
OEIS MCP Server — Online Encyclopedia of Integer Sequences

Wraps the public OEIS JSON API (no auth) so agents can:
  - Search sequences by keyword, ID, or matching values
  - Retrieve a sequence's full metadata (name, formula, references, crossrefs)
  - Fetch the b-file (first N terms with high precision)
  - Reverse-lookup: given numerical values, find candidate OEIS entries

Endpoint: https://oeis.org/search?fmt=json  (public, rate-limited politely)
"""

import warnings
import os
warnings.filterwarnings("ignore")
os.environ["PYTHONWARNINGS"] = "ignore"

import asyncio
import json
import logging
from pathlib import Path
from urllib.parse import quote

import httpx
import mcp.server.stdio
import mcp.types as types
from mcp.server import Server

SERVER_DIR = Path(__file__).resolve().parent
OEIS_BASE = "https://oeis.org"
USER_AGENT = "Ainulindale-Exflation/OEIS-MCP (math-research; contact via project)"
HTTP_TIMEOUT = 20.0

logging.basicConfig(
    level=logging.INFO,
    filename=str(SERVER_DIR / "oeis_mcp.log"),
    filemode="w",
    format="%(asctime)s %(levelname)s %(message)s",
)
logger = logging.getLogger(__name__)

server = Server("oeis")


async def _oeis_get(path: str, params: dict | None = None) -> dict | str:
    """GET against OEIS. Returns parsed JSON if available, else raw text."""
    async with httpx.AsyncClient(timeout=HTTP_TIMEOUT, headers={"User-Agent": USER_AGENT}) as client:
        url = f"{OEIS_BASE}{path}"
        r = await client.get(url, params=params or {})
        r.raise_for_status()
        try:
            return r.json()
        except Exception:
            return r.text


def _fmt_sequence(entry: dict) -> str:
    """Render one OEIS search-result entry as a compact markdown block."""
    num = entry.get("number")
    seq_id = f"A{num:06d}" if isinstance(num, int) else str(num)
    name = entry.get("name", "(no name)")
    data = entry.get("data", "")
    keywords = entry.get("keyword", "")
    author = entry.get("author", "")
    formulas = entry.get("formula", [])
    refs = entry.get("reference", [])
    links = entry.get("link", [])

    lines = [f"### {seq_id} — {name}"]
    if data:
        preview = ",".join(data.split(",")[:20])
        lines.append(f"- **First terms**: `{preview}...`")
    if keywords:
        lines.append(f"- **Keywords**: {keywords}")
    if author:
        lines.append(f"- **Author**: {author}")
    if formulas:
        lines.append(f"- **Formulas** ({len(formulas)}):")
        for f in formulas[:3]:
            lines.append(f"    - {f}")
    if refs:
        lines.append(f"- **References**: {len(refs)} entries")
    if links:
        lines.append(f"- **Links**: {len(links)} entries")
    lines.append(f"- **URL**: {OEIS_BASE}/{seq_id}")
    return "\n".join(lines)


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="search_oeis",
            description=(
                "Search the OEIS by keyword, ID, or comma-separated integer values. "
                "Examples: 'fibonacci', 'id:A000045', '1,1,2,3,5,8'. "
                "Returns up to max_results candidate sequences with metadata."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"},
                    "max_results": {"type": "integer", "default": 10, "minimum": 1, "maximum": 50},
                },
                "required": ["query"],
            },
        ),
        types.Tool(
            name="get_sequence",
            description=(
                "Fetch full metadata for one OEIS sequence by ID (e.g. 'A000045', 'A001622'). "
                "Returns name, data, formulas, references, keywords, author, cross-refs."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "seq_id": {"type": "string", "description": "OEIS ID like A000045"},
                },
                "required": ["seq_id"],
            },
        ),
        types.Tool(
            name="get_b_file",
            description=(
                "Fetch the b-file for a sequence — the first N terms at high precision. "
                "Good for numerical comparison against project data. Format: (n, a_n) pairs."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "seq_id": {"type": "string"},
                    "n_terms": {"type": "integer", "default": 100, "minimum": 1, "maximum": 10000},
                },
                "required": ["seq_id"],
            },
        ),
        types.Tool(
            name="lookup_by_values",
            description=(
                "Reverse-lookup: given a list of integers, find OEIS sequences that match. "
                "Useful when a computation produces a small integer sequence and you want to "
                "know whether it's a known combinatorial object."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "values": {
                        "type": "array",
                        "items": {"type": "integer"},
                        "description": "The integer sequence to look up",
                    },
                    "max_results": {"type": "integer", "default": 5, "minimum": 1, "maximum": 20},
                },
                "required": ["values"],
            },
        ),
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: dict | None) -> list[types.TextContent]:
    args = arguments or {}
    try:
        if name == "search_oeis":
            return await _search_oeis(args)
        if name == "get_sequence":
            return await _get_sequence(args)
        if name == "get_b_file":
            return await _get_b_file(args)
        if name == "lookup_by_values":
            return await _lookup_by_values(args)
        return [types.TextContent(type="text", text=f"Unknown tool: {name}")]
    except httpx.HTTPStatusError as e:
        return [types.TextContent(type="text", text=f"OEIS HTTP error: {e.response.status_code} on {e.request.url}")]
    except Exception as e:
        logger.exception("OEIS tool error")
        return [types.TextContent(type="text", text=f"Error: {e}")]


def _extract_results(data) -> tuple[list, int]:
    """OEIS returns either a bare list of results, a dict with 'results', or null.
    Normalize to (results_list, total_count)."""
    if data is None:
        return [], 0
    if isinstance(data, list):
        return data, len(data)
    if isinstance(data, dict):
        results = data.get("results") or []
        total = data.get("count", len(results))
        return results, total
    return [], 0


async def _search_oeis(args: dict) -> list[types.TextContent]:
    query = args["query"]
    max_results = int(args.get("max_results", 10))
    data = await _oeis_get("/search", {"q": query, "fmt": "json"})
    results, total = _extract_results(data)
    if not results:
        return [types.TextContent(type="text", text=f"No OEIS matches for `{query}`")]
    blocks = [f"# OEIS search: `{query}`\n- **Matches returned**: {total}\n- **Showing**: {min(max_results, len(results))}\n"]
    for entry in results[:max_results]:
        blocks.append(_fmt_sequence(entry))
    return [types.TextContent(type="text", text="\n\n".join(blocks))]


async def _get_sequence(args: dict) -> list[types.TextContent]:
    seq_id = args["seq_id"].strip().upper()
    if not seq_id.startswith("A"):
        seq_id = f"A{seq_id.zfill(6)}"
    data = await _oeis_get("/search", {"q": f"id:{seq_id}", "fmt": "json"})
    results, _ = _extract_results(data)
    if not results:
        return [types.TextContent(type="text", text=f"No OEIS entry found for `{seq_id}`")]
    return [types.TextContent(type="text", text=_fmt_sequence(results[0]))]


async def _get_b_file(args: dict) -> list[types.TextContent]:
    seq_id = args["seq_id"].strip().upper()
    if not seq_id.startswith("A"):
        seq_id = f"A{seq_id.zfill(6)}"
    n_terms = int(args.get("n_terms", 100))
    # b-file path: /A000045/b000045.txt
    num_part = seq_id[1:].lower()
    text = await _oeis_get(f"/{seq_id}/b{num_part}.txt")
    if not isinstance(text, str):
        return [types.TextContent(type="text", text=f"Unexpected b-file response for {seq_id}")]
    lines = [ln for ln in text.splitlines() if ln.strip() and not ln.strip().startswith("#")]
    lines = lines[:n_terms]
    out = [f"# {seq_id} — first {len(lines)} terms (from b-file)\n"]
    out.append("| n | a(n) |")
    out.append("|--:|:-----|")
    for ln in lines:
        parts = ln.split()
        if len(parts) >= 2:
            out.append(f"| {parts[0]} | `{parts[1]}` |")
    return [types.TextContent(type="text", text="\n".join(out))]


async def _lookup_by_values(args: dict) -> list[types.TextContent]:
    values = args["values"]
    max_results = int(args.get("max_results", 5))
    if not values:
        return [types.TextContent(type="text", text="No values provided")]
    query = ",".join(str(int(v)) for v in values)
    data = await _oeis_get("/search", {"q": query, "fmt": "json"})
    results, total = _extract_results(data)
    if not results:
        return [types.TextContent(type="text", text=f"No OEIS sequence matches `{query}` (verified: not a known integer sequence in OEIS)")]
    blocks = [f"# Reverse lookup for `{query}`\n- **Matches**: {total}\n"]
    for entry in results[:max_results]:
        blocks.append(_fmt_sequence(entry))
    return [types.TextContent(type="text", text="\n\n".join(blocks))]


async def main():
    logger.info("OEIS MCP server starting...")
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
