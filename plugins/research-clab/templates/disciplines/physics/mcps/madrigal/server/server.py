#!/usr/bin/env python3

"""
Madrigal MCP Server — Ionospheric / Heliophysics Data Access

A Model Context Protocol (MCP) server exposing MIT Haystack's Madrigal
database ecosystem to LLM tools, with framework-specific search helpers for
the Phonon-Exflation Cosmology retrospective-analysis program.

Data sources:
- EISCAT Madrigal (Tromsø, Kiruna, Sodankylä, Svalbard, EISCAT_3D)
- CEDAR distributed Madrigal (primary)
- Millstone Hill (MIT Haystack)
- Jicamarca, Arecibo (historical), SRI (AMISR Poker Flat / Resolute Bay)

Framework purpose (see sessions/session-74/session-74-rf-analysis.md):
Locate existing ionospheric-radar / ionospheric-heater data that might
retrospectively contain substrate-level pair production signatures per
the Jensen-resonance framework prediction from the Tesla-Mack workshop.

Usage:
    py -3.13 server.py
"""

# Suppress warnings before any imports — stderr noise breaks MCP stdio handshake.
import warnings
import os
warnings.filterwarnings("ignore")
os.environ["PYTHONWARNINGS"] = "ignore"

import asyncio
import json
import logging
from typing import Any

import mcp.server.stdio
import mcp.types as types
from mcp import Tool
from mcp.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions

from data_sources import MadrigalClient, FrameworkSearch


# Configure logging — send to file, not stderr (stderr noise breaks MCP stdio).
_log_path = os.path.join(os.path.dirname(__file__), "madrigal_mcp.log")
logging.basicConfig(
    level=logging.INFO,
    filename=_log_path,
    filemode="w",
    format="%(asctime)s %(name)s %(levelname)s %(message)s",
)
logger = logging.getLogger(__name__)

# Initialize MCP server
server = Server("madrigal-mcp")

# Lazy initialization of the Madrigal client so import failures don't block
# server startup (the server should still respond to tool-list requests even
# if madrigalWeb is missing).
_client: MadrigalClient | None = None
_framework: FrameworkSearch | None = None


def get_client() -> MadrigalClient:
    global _client
    if _client is None:
        _client = MadrigalClient()
    return _client


def get_framework() -> FrameworkSearch:
    global _framework
    if _framework is None:
        _framework = FrameworkSearch(get_client())
    return _framework


# ---------------------------------------------------------------------------
# Tool definitions
# ---------------------------------------------------------------------------

TOOLS: list[Tool] = [
    Tool(
        name="list_madrigal_servers",
        description=(
            "List the canonical public Madrigal database servers available for "
            "query. Each entry gives the short name (e.g. 'eiscat'), display "
            "name, and base URL. Use the short name in subsequent tool calls."
        ),
        inputSchema={"type": "object", "properties": {}, "required": []},
    ),
    Tool(
        name="list_instruments",
        description=(
            "List all instruments catalogued at a given Madrigal server. "
            "Each entry gives the instrument code (used in list_experiments), "
            "name, mnemonic, location, and contact info."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "server": {
                    "type": "string",
                    "description": (
                        "Madrigal server short name (e.g. 'eiscat', 'cedar', "
                        "'millstone') or a full URL."
                    ),
                },
            },
            "required": ["server"],
        },
    ),
    Tool(
        name="list_experiments",
        description=(
            "List all experiments conducted at a given instrument within a "
            "date range. Returns experiment IDs, start/end timestamps, "
            "principal investigator, and URLs for further drill-down."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "server": {"type": "string"},
                "instrument_code": {
                    "type": "integer",
                    "description": (
                        "Madrigal instrument code from list_instruments()."
                    ),
                },
                "start_year": {"type": "integer"},
                "start_month": {"type": "integer"},
                "start_day": {"type": "integer"},
                "end_year": {"type": "integer"},
                "end_month": {"type": "integer"},
                "end_day": {"type": "integer"},
            },
            "required": [
                "server", "instrument_code",
                "start_year", "start_month", "start_day",
                "end_year", "end_month", "end_day",
            ],
        },
    ),
    Tool(
        name="list_experiment_files",
        description=(
            "List all data files (kindats) available for a given experiment. "
            "Each file contains a different data product from the same "
            "observing run."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "server": {"type": "string"},
                "experiment_id": {"type": "integer"},
            },
            "required": ["server", "experiment_id"],
        },
    ),
    Tool(
        name="list_parameters",
        description=(
            "List the parameters (columns) available in a specific Madrigal "
            "data file. Returns mnemonic, description, units, and measurement "
            "type for each parameter."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "server": {"type": "string"},
                "file_name": {
                    "type": "string",
                    "description": (
                        "Madrigal file name (from list_experiment_files)."
                    ),
                },
            },
            "required": ["server", "file_name"],
        },
    ),
    Tool(
        name="isprint_filter",
        description=(
            "Run the Madrigal isprint command on a data file, extracting a "
            "selection of parameters optionally filtered by value ranges. "
            "Returns the raw result as a text block. For large datasets, "
            "prefer download_file instead."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "server": {"type": "string"},
                "file_name": {"type": "string"},
                "parameters": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": (
                        "List of parameter mnemonics to extract "
                        "(e.g. ['ut1_unix', 'gdalt', 'nel'])."
                    ),
                },
                "filters": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": (
                        "List of isprint filter strings, e.g. "
                        "['gdalt,200,500'] for altitudes 200-500 km. "
                        "Optional — omit for no filtering."
                    ),
                },
                "header": {
                    "type": "string",
                    "enum": ["t", "f"],
                    "description": "'t' to include column headers, 'f' to omit.",
                },
            },
            "required": ["server", "file_name", "parameters"],
        },
    ),
    Tool(
        name="download_file",
        description=(
            "Download a Madrigal data file to local disk in the specified "
            "format. Returns the local path on success. Use for full dataset "
            "extraction; use isprint_filter for quick parameter sampling."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "server": {"type": "string"},
                "file_name": {"type": "string"},
                "dest_path": {
                    "type": "string",
                    "description": "Local destination path for the downloaded file.",
                },
                "file_format": {
                    "type": "string",
                    "enum": ["hdf5", "netCDF4", "ascii"],
                    "description": "Output format.",
                },
            },
            "required": ["server", "file_name", "dest_path"],
        },
    ),
    # ----- Framework-specific tools -----
    Tool(
        name="list_framework_instruments",
        description=(
            "FRAMEWORK TOOL: Return the curated list of instruments relevant "
            "to the Phonon-Exflation substrate-pair-production retrospective "
            "analysis, sorted by priority. Each entry gives the framework "
            "priority, detuning from the Jensen resonance target, and a note "
            "explaining why the instrument matters. Consult this before "
            "running generic Madrigal queries to focus on high-value targets."
        ),
        inputSchema={"type": "object", "properties": {}, "required": []},
    ),
    Tool(
        name="search_by_frequency",
        description=(
            "FRAMEWORK TOOL: Return framework-relevant instruments whose "
            "operating frequency falls within [freq_min_hz, freq_max_hz]. "
            "Use to narrow the retrospective search to facilities close to "
            "a specific target frequency (e.g. once the OQ-TESLA-T1 "
            "computation returns a refined Jensen resonance estimate)."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "freq_min_hz": {
                    "type": "number",
                    "description": "Minimum frequency in Hz.",
                },
                "freq_max_hz": {
                    "type": "number",
                    "description": "Maximum frequency in Hz.",
                },
            },
            "required": ["freq_min_hz", "freq_max_hz"],
        },
    ),
    Tool(
        name="list_anomaly_campaigns",
        description=(
            "FRAMEWORK TOOL: Return the curated list of published anomaly "
            "campaigns that are framework-test targets. Each entry gives the "
            "instrument, date, anomaly type, operating frequency, and a "
            "literature citation. Optionally filter by instrument short name. "
            "Use this to identify known unexplained observations in the "
            "literature that match the framework prediction's signature."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "instrument": {
                    "type": "string",
                    "description": (
                        "Optional instrument short name to filter by "
                        "(e.g. 'eiscat_heating')."
                    ),
                },
            },
            "required": [],
        },
    ),
    Tool(
        name="describe_framework_target",
        description=(
            "FRAMEWORK TOOL: Return the current Tesla-Mack workshop target "
            "parameters — Jensen resonance frequency, acceptable band, "
            "tolerance — in a single call. Use at the start of a retrospective "
            "search session to establish context."
        ),
        inputSchema={"type": "object", "properties": {}, "required": []},
    ),
]


# ---------------------------------------------------------------------------
# MCP protocol handlers
# ---------------------------------------------------------------------------


@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    """Return the list of tools this server exposes."""
    return TOOLS


@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict[str, Any] | None
) -> list[types.TextContent]:
    """Dispatch a tool call to the appropriate handler."""
    args = arguments or {}
    logger.info("call_tool: %s %s", name, json.dumps(args))

    try:
        result = await _dispatch(name, args)
    except Exception as exc:
        logger.exception("Tool call failed: %s", name)
        result = {"error": str(exc), "tool": name}

    return [types.TextContent(type="text", text=json.dumps(result, indent=2))]


async def _dispatch(name: str, args: dict[str, Any]) -> Any:
    """Route a named tool call to the right client/framework method."""
    if name == "list_madrigal_servers":
        return get_client().list_known_servers()

    if name == "list_instruments":
        return get_client().list_instruments(args["server"])

    if name == "list_experiments":
        return get_client().list_experiments(
            args["server"],
            int(args["instrument_code"]),
            int(args["start_year"]),
            int(args["start_month"]),
            int(args["start_day"]),
            int(args["end_year"]),
            int(args["end_month"]),
            int(args["end_day"]),
        )

    if name == "list_experiment_files":
        return get_client().list_experiment_files(
            args["server"], int(args["experiment_id"])
        )

    if name == "list_parameters":
        return get_client().list_parameters(args["server"], args["file_name"])

    if name == "isprint_filter":
        return {
            "output": get_client().isprint_filter(
                args["server"],
                args["file_name"],
                list(args.get("parameters") or []),
                list(args.get("filters") or []),
                args.get("header", "t"),
            )
        }

    if name == "download_file":
        path = get_client().download_file(
            args["server"],
            args["file_name"],
            args["dest_path"],
            args.get("file_format", "hdf5"),
        )
        return {"path": path}

    if name == "list_framework_instruments":
        return get_framework().list_framework_instruments()

    if name == "search_by_frequency":
        return get_framework().search_by_frequency(
            float(args["freq_min_hz"]),
            float(args["freq_max_hz"]),
        )

    if name == "list_anomaly_campaigns":
        return get_framework().list_anomaly_campaigns(args.get("instrument"))

    if name == "describe_framework_target":
        return get_framework().describe_framework_target()

    raise ValueError(f"Unknown tool: {name}")


# ---------------------------------------------------------------------------
# Server entry point
# ---------------------------------------------------------------------------


async def main() -> None:
    logger.info("Starting Madrigal MCP server")
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="madrigal-mcp",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())
