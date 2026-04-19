#!/usr/bin/env python3
"""
Knowledge MCP Server — Project Knowledge Base Access for Agents

Wraps the knowledge-index.json / knowledge.db and canonical_constants.py
so that every spawned agent can query settled results, gate verdicts,
closed mechanisms, and framework constants without needing the /weave skill.

Tools:
  search_knowledge     — FTS5 ranked search across all entity types
  query_entity         — Direct lookup by table and ID
  list_entities        — Show all entities of a given type
  trace_entity         — Evidence chain for a named entity
  get_constant         — Get a canonical constant with provenance
  list_constants       — List/filter canonical constants
  update_constant      — Add or update a constant in canonical_constants.py
"""

# Suppress warnings before any imports — stderr noise breaks MCP stdio
import warnings
import os
warnings.filterwarnings("ignore")
os.environ["PYTHONWARNINGS"] = "ignore"

import asyncio
import json
import sqlite3
import re
import logging
import sys
from pathlib import Path
from typing import Any, Optional

import mcp.server.stdio
import mcp.types as types
from mcp.server import Server

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

SERVER_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SERVER_DIR.parent.parent.parent  # tools/mcp-servers/knowledge-mcp -> root
INDEX_PATH = PROJECT_ROOT / "tools" / "knowledge-index.json"
DB_PATH = PROJECT_ROOT / "tools" / "knowledge.db"
CONSTANTS_PATH = PROJECT_ROOT / "tier0-computation" / "canonical_constants.py"
USAGE_COUNTER_PATH = SERVER_DIR / "usage_counter.json"

# Logging — to file, not stderr
_log_path = SERVER_DIR / "knowledge_mcp.log"
logging.basicConfig(level=logging.INFO, filename=str(_log_path), filemode='w',
                    format='%(asctime)s %(name)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Server
# ---------------------------------------------------------------------------

server = Server("knowledge-base")

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _bump_counter(tool_name: str) -> None:
    """Increment per-tool and total usage counters. Silent on I/O error."""
    import datetime as _dt
    try:
        if USAGE_COUNTER_PATH.exists():
            with open(USAGE_COUNTER_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = {
                "started_at": _dt.datetime.utcnow().isoformat() + "Z",
                "total_calls": 0,
                "by_tool": {},
            }
        now = _dt.datetime.utcnow().isoformat() + "Z"
        data["total_calls"] = int(data.get("total_calls", 0)) + 1
        by_tool = data.setdefault("by_tool", {})
        entry = by_tool.setdefault(tool_name, {"count": 0, "last_called": None})
        entry["count"] = int(entry.get("count", 0)) + 1
        entry["last_called"] = now
        data["last_called"] = now
        tmp = USAGE_COUNTER_PATH.with_suffix(".json.tmp")
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        os.replace(tmp, USAGE_COUNTER_PATH)
    except Exception:
        logger.exception("usage_counter bump failed for %s", tool_name)


def _get_db() -> sqlite3.Connection:
    """Open the knowledge SQLite database."""
    if not DB_PATH.exists():
        raise FileNotFoundError(
            f"Knowledge DB not found at {DB_PATH}. Run /weave --db-sync first."
        )
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def _load_index() -> dict:
    """Load the knowledge-index.json."""
    if not INDEX_PATH.exists():
        raise FileNotFoundError(f"Index not found at {INDEX_PATH}. Run /weave --update.")
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


TABLE_MAP = {
    "theorems": "theorems", "theorem": "theorems",
    "closed": "closed_mechanisms", "closed_mechanisms": "closed_mechanisms",
    "gates": "gates", "gate": "gates",
    "sessions": "sessions", "session": "sessions",
    "provenance": "data_provenance", "data_provenance": "data_provenance",
    "open": "open_channels", "open_channels": "open_channels",
    "researchers": "researchers", "researcher": "researchers",
    "trajectory": "probability_trajectory",
    "equations": "equations", "equation": "equations",
    "edges": "edges", "edge": "edges",  # S81: tagged-link relation edges
}

PK_COLS = {
    "theorems": "id", "closed_mechanisms": "id", "gates": "id",
    "sessions": "id", "researchers": "domain",
    "probability_trajectory": "session",
    "data_provenance": "name", "open_channels": "name",
    "equations": "id",
    "edges": "id",  # S81: edge_N
}


def _parse_constants_module() -> dict:
    """Parse canonical_constants.py via regex — no exec, no hanging."""
    if not CONSTANTS_PATH.exists():
        raise FileNotFoundError(f"canonical_constants.py not found at {CONSTANTS_PATH}")

    with open(CONSTANTS_PATH, "r", encoding="utf-8") as f:
        source = f.read()

    # --- Extract simple assignments: name = value  # comment ---
    # Matches: name = 1.23e-4, name = 0.190, name = 42, name = "string"
    assign_re = re.compile(
        r'^([A-Za-z_]\w*)\s*=\s*'           # name =
        r'(-?[\d]+(?:\.[\d]*)?(?:[eE][+-]?\d+)?)'  # numeric value
        r'\s*(?:#.*)?$',                      # optional comment
        re.MULTILINE
    )
    constants = {}
    for m in assign_re.finditer(source):
        name, val_str = m.group(1), m.group(2)
        if name.startswith("_") or name in ("PI",):
            continue
        try:
            constants[name] = float(val_str)
        except ValueError:
            pass

    # --- Pass 2: Alias assignments (name = other_name) ---
    # Matches: E_cond = E_cond_ED_8mode, M_KK = M_KK_gravity, Delta_BCS = Delta_0_OES
    alias_re = re.compile(
        r'^([A-Za-z_]\w*)\s*=\s*([A-Za-z_]\w*)\s*(?:#.*)?$',
        re.MULTILINE
    )
    aliases = {}  # alias_name -> target_name
    for m in alias_re.finditer(source):
        alias_name, target_name = m.group(1), m.group(2)
        if alias_name.startswith("_") or alias_name in ("PI", "PROVENANCE"):
            continue
        # Skip if it's a known non-constant (imports, builtins, modules)
        if target_name in ("np", "numpy", "sys", "warnings", "True", "False", "None"):
            continue
        aliases[alias_name] = target_name

    # Resolve alias chains: E_cond -> E_cond_ED_8mode -> (numeric value)
    for alias_name, target in aliases.items():
        if target in constants and alias_name not in constants:
            constants[alias_name] = constants[target]
        elif target in aliases and aliases[target] in constants:
            constants[alias_name] = constants[aliases[target]]

    # --- Pass 3: Derived expressions where all operands are already parsed ---
    # Catches: R_protected_fold = a0_fold * a4_fold / a2_fold**2
    #          Omega_DM = Omega_m - Omega_b
    #          T_CMB_GeV = T_CMB * k_B / 1e9
    import math
    expr_re = re.compile(
        r'^([A-Za-z_]\w*)\s*=\s*(.+?)\s*(?:#.*)?$',
        re.MULTILINE
    )
    safe_ns = {**constants, "np": type("np", (), {"pi": math.pi}), "PI": math.pi}
    for m in expr_re.finditer(source):
        name, expr = m.group(1), m.group(2).strip()
        if name in constants or name.startswith("_"):
            continue
        if name in ("PROVENANCE", "Path", "DATA_DIR", "warnings", "sys", "np"):
            continue
        # Only evaluate if the expression contains known constants or numbers
        # and basic operators (no function calls, imports, etc.)
        if any(c in expr for c in ("import", "open(", "exec", "__", "print")):
            continue
        try:
            val = eval(expr, {"__builtins__": {}}, safe_ns)
            if isinstance(val, (int, float)):
                constants[name] = float(val)
        except Exception:
            pass

    # --- Extract PROVENANCE dict ---
    provenance = {}
    prov_start = source.find("PROVENANCE = {")
    if prov_start >= 0:
        # Find matching closing brace
        brace_depth = 0
        prov_text = ""
        for i in range(prov_start, len(source)):
            c = source[i]
            if c == '{':
                brace_depth += 1
            elif c == '}':
                brace_depth -= 1
                if brace_depth == 0:
                    prov_text = source[prov_start:i+1]
                    break

        if prov_text:
            # Clean up for JSON-ish parsing: replace Python dict syntax
            # Extract individual entries via regex
            entry_re = re.compile(
                r'"(\w+)":\s*\{([^}]+)\}',
                re.DOTALL
            )
            for em in entry_re.finditer(prov_text):
                name = em.group(1)
                body = em.group(2)
                entry = {}
                # Extract key-value pairs
                kv_re = re.compile(r'"(\w+)":\s*(?:"([^"]*)"|(None|True|False)|([\d.eE+-]+))')
                for kv in kv_re.finditer(body):
                    key = kv.group(1)
                    if kv.group(2) is not None:
                        entry[key] = kv.group(2)
                    elif kv.group(3) is not None:
                        val = kv.group(3)
                        entry[key] = None if val == "None" else val == "True"
                    elif kv.group(4) is not None:
                        try:
                            entry[key] = float(kv.group(4))
                        except ValueError:
                            entry[key] = kv.group(4)
                # Extract note field (may contain quotes)
                note_re = re.compile(r'"note":\s*"((?:[^"\\]|\\.)*)"')
                nm = note_re.search(body)
                if nm:
                    entry["note"] = nm.group(1)
                provenance[name] = entry

    return constants, provenance


# ---------------------------------------------------------------------------
# Tool definitions
# ---------------------------------------------------------------------------

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="search_knowledge",
            description=(
                "FTS5 ranked search across ALL knowledge entities (theorems, "
                "closed mechanisms, gates, sessions, equations, etc.). "
                "Use this BEFORE computing anything to check if a result is already known."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query (supports FTS5 syntax: AND, OR, NOT, quotes for phrases)"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Max results (default 20)",
                        "default": 20
                    }
                },
                "required": ["query"]
            }
        ),
        types.Tool(
            name="query_entity",
            description=(
                "Look up a specific entity by table and ID. "
                "Tables: theorems, closed, gates, sessions, provenance, open, researchers, equations."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "table": {
                        "type": "string",
                        "description": "Entity table (theorems, closed, gates, sessions, provenance, open, researchers, equations)"
                    },
                    "entity_id": {
                        "type": "string",
                        "description": "Entity ID or name to look up (supports partial match)"
                    }
                },
                "required": ["table", "entity_id"]
            }
        ),
        types.Tool(
            name="list_entities",
            description=(
                "List all entities of a given type. "
                "Types: theorems, closed, gates, trajectory, open, researchers, sessions."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "entity_type": {
                        "type": "string",
                        "description": "Entity type to list"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Max results (default 50)",
                        "default": 50
                    }
                },
                "required": ["entity_type"]
            }
        ),
        types.Tool(
            name="trace_entity",
            description=(
                "Trace an entity across all knowledge types — find every mention "
                "of a name/concept in theorems, gates, closed mechanisms, sessions, etc. "
                "Returns an evidence chain showing how findings connect."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Entity name or concept to trace (e.g. 'BCS', 'monotonic', 'tau stabilization')"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Max results per entity type (default 10)",
                        "default": 10
                    }
                },
                "required": ["name"]
            }
        ),
        types.Tool(
            name="get_constant",
            description=(
                "Get a canonical constant's value and full provenance (session, source, gate, notes). "
                "Use this to check the current authoritative value before hardcoding anything."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Constant name (e.g. 'tau_fold', 'M_KK_gravity', 'Delta_BCS')"
                    }
                },
                "required": ["name"]
            }
        ),
        types.Tool(
            name="list_constants",
            description=(
                "List canonical constants, optionally filtered by a pattern. "
                "Returns name, value, and session provenance for each."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "pattern": {
                        "type": "string",
                        "description": "Filter pattern (regex, case-insensitive). Empty = list all.",
                        "default": ""
                    },
                    "section": {
                        "type": "string",
                        "description": "Filter by section: PDG, geometric, BCS, spectral, transit, cosmological, acoustic, observation",
                        "default": ""
                    }
                }
            }
        ),
        types.Tool(
            name="update_constant",
            description=(
                "Add or update a canonical constant in canonical_constants.py. "
                "Appends to the appropriate section with full provenance comment. "
                "NEVER use this to overwrite existing constants without explicit user approval."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Constant name (Python identifier)"
                    },
                    "value": {
                        "type": "string",
                        "description": "Value as a Python expression (e.g. '7.43e16', '0.190', '2.776e3')"
                    },
                    "session": {
                        "type": "string",
                        "description": "Session where this was established (e.g. 'S77')"
                    },
                    "source": {
                        "type": "string",
                        "description": "Source file or derivation (e.g. 's77_equil_tau_bcs.npz')"
                    },
                    "gate": {
                        "type": "string",
                        "description": "Gate ID if applicable (e.g. 'S77-A1-EQUIL-TAU'). Null if none.",
                        "default": ""
                    },
                    "comment": {
                        "type": "string",
                        "description": "Brief description comment for the assignment line"
                    },
                    "section_label": {
                        "type": "string",
                        "description": "Which section to append to (e.g. 'SECTION B', 'SECTION C', 'SECTION D')",
                        "default": "SECTION E"
                    }
                },
                "required": ["name", "value", "session", "source", "comment"]
            }
        ),
        types.Tool(
            name="usage_stats",
            description=(
                "Return the knowledge MCP usage counter: total calls, per-tool counts, "
                "and last-called timestamps. Counter persists across server restarts "
                "at tools/mcp-servers/knowledge-mcp/usage_counter.json. "
                "Delete that file to reset."
            ),
            inputSchema={
                "type": "object",
                "properties": {},
            }
        ),
    ]


# ---------------------------------------------------------------------------
# Tool implementations
# ---------------------------------------------------------------------------

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict | None) -> list[types.TextContent]:
    args = arguments or {}
    _bump_counter(name)
    try:
        if name == "search_knowledge":
            return await _search_knowledge(args)
        elif name == "query_entity":
            return await _query_entity(args)
        elif name == "list_entities":
            return await _list_entities(args)
        elif name == "trace_entity":
            return await _trace_entity(args)
        elif name == "get_constant":
            return await _get_constant(args)
        elif name == "list_constants":
            return await _list_constants(args)
        elif name == "update_constant":
            return await _update_constant(args)
        elif name == "usage_stats":
            return await _usage_stats(args)
        else:
            return [types.TextContent(type="text", text=f"Unknown tool: {name}")]
    except Exception as e:
        logger.exception(f"Error in tool {name}")
        return [types.TextContent(type="text", text=f"Error: {e}")]


async def _search_knowledge(args: dict) -> list[types.TextContent]:
    query = args["query"]
    limit = args.get("limit", 20)

    conn = _get_db()
    cur = conn.cursor()

    # FTS5: spaces = implicit AND (very strict). If no explicit operators,
    # convert to OR for broader matching. Users can still use AND/OR/NOT explicitly.
    fts_query = query
    has_operators = any(op in query.upper() for op in (" AND ", " OR ", " NOT ", '"'))
    if not has_operators and " " in query:
        fts_query = " OR ".join(query.split())

    try:
        cur.execute(
            """
            SELECT entity_type, entity_id, name, content, source_file,
                   bm25(knowledge_fts) AS rank
            FROM knowledge_fts
            WHERE knowledge_fts MATCH ?
            ORDER BY rank
            LIMIT ?
            """,
            (fts_query, limit),
        )
        rows = cur.fetchall()
    except Exception:
        # Fallback: quote each term
        terms = query.split()
        fts_query = " OR ".join(f'"{t}"' for t in terms)
        cur.execute(
            """
            SELECT entity_type, entity_id, name, content, source_file,
                   bm25(knowledge_fts) AS rank
            FROM knowledge_fts
            WHERE knowledge_fts MATCH ?
            ORDER BY rank
            LIMIT ?
            """,
            (fts_query, limit),
        )
        rows = cur.fetchall()

    conn.close()

    if not rows:
        return [types.TextContent(type="text", text=f"No results for '{query}'")]

    lines = [f"## Search: '{query}' — {len(rows)} results\n"]
    grouped = {}
    for row in rows:
        etype = row["entity_type"]
        if etype not in grouped:
            grouped[etype] = []
        grouped[etype].append(row)

    for etype, entries in grouped.items():
        lines.append(f"### [{etype}] ({len(entries)} hits)\n")
        for entry in entries:
            name_display = entry["name"] or entry["entity_id"] or "(unnamed)"
            content_short = (entry["content"] or "")[:300].replace("\n", " ")
            lines.append(f"**{name_display}**")
            lines.append(f"  {content_short}")
            if entry["source_file"]:
                lines.append(f"  _src: {Path(entry['source_file']).name}_")
            lines.append("")

    return [types.TextContent(type="text", text="\n".join(lines))]


async def _query_entity(args: dict) -> list[types.TextContent]:
    table = args["table"]
    entity_id = args["entity_id"]

    tbl = TABLE_MAP.get(table.lower())
    if not tbl:
        return [types.TextContent(type="text",
                text=f"Unknown table: {table}. Available: {', '.join(sorted(set(TABLE_MAP.values())))}")]

    pk = PK_COLS.get(tbl, "id")
    conn = _get_db()
    cur = conn.cursor()

    # Exact match first, then LIKE on PK, then LIKE on name column
    cur.execute(f"SELECT * FROM {tbl} WHERE {pk} = ?", (entity_id,))
    rows = cur.fetchall()
    if not rows:
        cur.execute(f"SELECT * FROM {tbl} WHERE {pk} LIKE ?", (f"%{entity_id}%",))
        rows = cur.fetchall()
    if not rows:
        # Try name column if it exists (most tables have one)
        name_col = "name" if tbl not in ("researchers", "probability_trajectory", "equations") else None
        if name_col:
            try:
                cur.execute(f"SELECT * FROM {tbl} WHERE {name_col} LIKE ?", (f"%{entity_id}%",))
                rows = cur.fetchall()
            except sqlite3.OperationalError:
                pass  # table doesn't have a name column
    conn.close()

    if not rows:
        return [types.TextContent(type="text",
                text=f"No entity found in {tbl} matching '{entity_id}'")]

    lines = [f"## {tbl} / {entity_id} — {len(rows)} result(s)\n"]
    for row in rows:
        for key in row.keys():
            val = row[key]
            if val is not None and str(val).strip():
                lines.append(f"**{key}**: {val}")
        lines.append("---")

    return [types.TextContent(type="text", text="\n".join(lines))]


async def _list_entities(args: dict) -> list[types.TextContent]:
    entity_type = args["entity_type"]
    limit = args.get("limit", 50)

    tbl = TABLE_MAP.get(entity_type.lower())
    if not tbl:
        return [types.TextContent(type="text",
                text=f"Unknown type: {entity_type}. Available: theorems, closed, gates, sessions, trajectory, open, researchers, equations, edges")]

    conn = _get_db()
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {tbl} LIMIT ?", (limit,))
    rows = cur.fetchall()
    conn.close()

    if not rows:
        return [types.TextContent(type="text", text=f"No entities in {tbl}")]

    # Build a compact table
    keys = rows[0].keys()
    lines = [f"## {tbl} — {len(rows)} entries\n"]
    lines.append("| " + " | ".join(keys) + " |")
    lines.append("| " + " | ".join(["---"] * len(keys)) + " |")
    for row in rows:
        vals = []
        for k in keys:
            v = str(row[k] or "")[:80]
            v = v.replace("|", "/").replace("\n", " ")
            vals.append(v)
        lines.append("| " + " | ".join(vals) + " |")

    return [types.TextContent(type="text", text="\n".join(lines))]


async def _trace_entity(args: dict) -> list[types.TextContent]:
    name = args["name"]
    limit = args.get("limit", 10)

    conn = _get_db()
    cur = conn.cursor()

    # Search across all FTS content
    try:
        cur.execute(
            """
            SELECT entity_type, entity_id, name, content, source_file,
                   bm25(knowledge_fts) AS rank
            FROM knowledge_fts
            WHERE knowledge_fts MATCH ?
            ORDER BY rank
            LIMIT ?
            """,
            (name, limit * 5),
        )
        rows = cur.fetchall()
    except sqlite3.OperationalError:
        # FTS query syntax error — try quoting
        cur.execute(
            """
            SELECT entity_type, entity_id, name, content, source_file,
                   bm25(knowledge_fts) AS rank
            FROM knowledge_fts
            WHERE knowledge_fts MATCH ?
            ORDER BY rank
            LIMIT ?
            """,
            (f'"{name}"', limit * 5),
        )
        rows = cur.fetchall()
    conn.close()

    if not rows:
        return [types.TextContent(type="text", text=f"No trace found for '{name}'")]

    lines = [f"## Evidence Chain: '{name}'\n"]

    # Group by type, show most relevant per type
    grouped = {}
    for row in rows:
        etype = row["entity_type"]
        if etype not in grouped:
            grouped[etype] = []
        if len(grouped[etype]) < limit:
            grouped[etype].append(row)

    for etype in ["theorem", "gate", "closed_mechanism", "session", "provenance",
                  "open_channel", "trajectory", "researcher", "equation"]:
        entries = grouped.get(etype, [])
        if not entries:
            continue
        lines.append(f"### {etype} ({len(entries)} hits)")
        for entry in entries:
            eid = entry["entity_id"] or ""
            ename = entry["name"] or ""
            content = (entry["content"] or "")[:200].replace("\n", " ")
            lines.append(f"- **{ename}** [{eid}]: {content}")
        lines.append("")

    return [types.TextContent(type="text", text="\n".join(lines))]


async def _get_constant(args: dict) -> list[types.TextContent]:
    name = args["name"]
    constants, provenance = _parse_constants_module()

    def _format_constant(cname, val, prov):
        lines = [f"## Constant: {cname}\n"]
        lines.append(f"**Value**: {val}")
        if prov:
            lines.append(f"**Session**: {prov.get('session', 'unknown')}")
            lines.append(f"**Source**: {prov.get('source', 'unknown')}")
            lines.append(f"**Gate**: {prov.get('gate', 'None')}")
            lines.append(f"**Superseded**: {prov.get('superseded', False)}")
            if prov.get("R_protected"):
                lines.append("**R-Protected**: YES")
            if prov.get("note"):
                lines.append(f"**Note**: {prov['note']}")
        else:
            lines.append("_No PROVENANCE entry (PDG/CODATA or needs to be added)_")
        return lines

    # Exact match in constants dict
    if name in constants:
        prov = provenance.get(name, {})
        return [types.TextContent(type="text",
                text="\n".join(_format_constant(name, constants[name], prov)))]

    # Has provenance but value not parsed (complex alias or expression)
    if name in provenance:
        prov = provenance[name]
        # Try to resolve via source hint (e.g., "alias for E_cond_ED_8mode")
        alias_target = None
        src = prov.get("source", "")
        if "alias for " in src:
            target_name = src.split("alias for ")[1].strip()
            if target_name in constants:
                alias_target = target_name
        lines = [f"## Constant: {name}\n"]
        if alias_target:
            lines.append(f"**Value**: {constants[alias_target]} (alias for {alias_target})")
        else:
            lines.append("**Value**: _(not directly parsed — check canonical_constants.py)_")
        lines.append(f"**Session**: {prov.get('session', 'unknown')}")
        lines.append(f"**Source**: {prov.get('source', 'unknown')}")
        lines.append(f"**Gate**: {prov.get('gate', 'None')}")
        lines.append(f"**Superseded**: {prov.get('superseded', False)}")
        if prov.get("R_protected"):
            lines.append("**R-Protected**: YES")
        if prov.get("note"):
            lines.append(f"**Note**: {prov['note']}")
        return [types.TextContent(type="text", text="\n".join(lines))]

    # Fuzzy search across both constants and provenance
    matches_c = [k for k in constants if name.lower() in k.lower()]
    matches_p = [k for k in provenance if name.lower() in k.lower() and k not in matches_c]
    if matches_c or matches_p:
        lines = [f"No exact match for '{name}'. Did you mean:\n"]
        for m in matches_c[:10]:
            lines.append(f"- **{m}** = {constants[m]}")
        for m in matches_p[:5]:
            prov = provenance[m]
            lines.append(f"- **{m}** (provenance only: {prov.get('source', '?')})")
        return [types.TextContent(type="text", text="\n".join(lines))]

    return [types.TextContent(type="text", text=f"Constant '{name}' not found")]


async def _list_constants(args: dict) -> list[types.TextContent]:
    pattern = args.get("pattern", "")
    section = args.get("section", "")
    constants, provenance = _parse_constants_module()

    filtered = {}
    for k, v in constants.items():
        if pattern:
            try:
                if not re.search(pattern, k, re.IGNORECASE):
                    continue
            except re.error:
                if pattern.lower() not in k.lower():
                    continue
        if section:
            prov = provenance.get(k, {})
            src = prov.get("source", "")
            sess = prov.get("session", "")
            # Rough section matching by keyword
            if not any(s.lower() in f"{k} {src} {sess}".lower() for s in section.split()):
                continue
        filtered[k] = v

    if not filtered:
        return [types.TextContent(type="text",
                text=f"No constants matching pattern='{pattern}' section='{section}'")]

    lines = [f"## Canonical Constants ({len(filtered)} matches)\n"]
    lines.append("| Name | Value | Session | Gate |")
    lines.append("|:-----|:------|:--------|:-----|")
    for k in sorted(filtered.keys()):
        v = filtered[k]
        prov = provenance.get(k, {})
        sess = prov.get("session", "")
        gate = prov.get("gate", "") or ""
        val_str = f"{v:.6g}" if isinstance(v, float) else str(v)
        lines.append(f"| {k} | {val_str} | {sess} | {gate} |")

    return [types.TextContent(type="text", text="\n".join(lines))]


async def _update_constant(args: dict) -> list[types.TextContent]:
    name = args["name"]
    value = args["value"]
    session = args["session"]
    source = args["source"]
    gate = args.get("gate", "")
    comment = args["comment"]
    section_label = args.get("section_label", "SECTION E")

    # Validate name is a valid Python identifier
    if not name.isidentifier():
        return [types.TextContent(type="text",
                text=f"Error: '{name}' is not a valid Python identifier")]

    # Check if constant already exists
    constants, provenance = _parse_constants_module()
    if name in constants:
        return [types.TextContent(type="text",
                text=f"Error: Constant '{name}' already exists with value {constants[name]}. "
                     f"To update an existing constant, manually edit canonical_constants.py "
                     f"(safety measure to prevent accidental overwrites).")]

    # Build the assignment line
    assignment = f"{name} = {value}  # {comment} ({session})"

    # Build the PROVENANCE entry
    gate_str = f'"{gate}"' if gate else "None"
    prov_entry = (
        f'    "{name}": {{"session": "{session}", "source": "{source}", '
        f'"gate": {gate_str}, "superseded": False}},'
    )

    # Read the file to find insertion points
    with open(CONSTANTS_PATH, "r", encoding="utf-8") as f:
        content = f.read()
        lines = content.split("\n")

    # Find the section to insert the constant
    section_line = None
    for i, line in enumerate(lines):
        if section_label in line and line.strip().startswith("#"):
            section_line = i
            break

    if section_line is None:
        # Append before PROVENANCE dict
        for i, line in enumerate(lines):
            if line.startswith("PROVENANCE"):
                section_line = i - 2
                break

    if section_line is None:
        return [types.TextContent(type="text",
                text=f"Error: Could not find '{section_label}' or PROVENANCE in canonical_constants.py")]

    # Find end of section (next blank line or next section header)
    insert_at = section_line + 1
    for i in range(section_line + 1, len(lines)):
        if lines[i].strip().startswith("# ==") or lines[i].strip().startswith("PROVENANCE"):
            insert_at = i - 1
            break
        if lines[i].strip() == "" and i > section_line + 2:
            insert_at = i
            break
    else:
        insert_at = len(lines) - 1

    # Insert the constant
    lines.insert(insert_at, assignment)

    # Find PROVENANCE dict end and insert entry
    prov_insert = None
    for i, line in enumerate(lines):
        if line.strip().startswith(f'"session": "{session}"') or \
           (line.strip().startswith("}") and i > 0 and "PROVENANCE" in "\n".join(lines[max(0,i-200):i])):
            # Find the closing brace of PROVENANCE
            pass

    # Simpler approach: find the last entry before the closing }
    in_prov = False
    last_entry_line = None
    for i, line in enumerate(lines):
        if line.startswith("PROVENANCE"):
            in_prov = True
        if in_prov and line.strip() == "}":
            last_entry_line = i
            break

    if last_entry_line:
        lines.insert(last_entry_line, prov_entry)
        lines.insert(last_entry_line, f"\n    # {section_label} — {session}")

    # Write back
    with open(CONSTANTS_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    return [types.TextContent(type="text",
            text=f"Added constant **{name}** = {value}\n"
                 f"Session: {session}\n"
                 f"Source: {source}\n"
                 f"Gate: {gate or 'None'}\n"
                 f"Inserted into {section_label} of canonical_constants.py\n"
                 f"PROVENANCE entry added.\n\n"
                 f"**Run `/weave --update` to rebuild the knowledge index.**")]


async def _usage_stats(args: dict) -> list[types.TextContent]:
    """Return the usage counter state. Note: this call itself is counted (pre-bumped in dispatch)."""
    if not USAGE_COUNTER_PATH.exists():
        return [types.TextContent(
            type="text",
            text="Usage counter file not found yet. It will be created on the next tool call."
        )]
    try:
        with open(USAGE_COUNTER_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        return [types.TextContent(type="text", text=f"Error reading usage counter: {e}")]

    lines = []
    lines.append("# Knowledge MCP Usage Counter\n")
    lines.append(f"- Started: {data.get('started_at', 'unknown')}")
    lines.append(f"- Last call: {data.get('last_called', 'never')}")
    lines.append(f"- Total calls: {data.get('total_calls', 0)}")
    lines.append(f"- Counter file: `{USAGE_COUNTER_PATH}`")
    lines.append("")
    lines.append("## By tool")
    lines.append("| Tool | Count | Last called |")
    lines.append("|:-----|------:|:------------|")
    by_tool = data.get("by_tool", {}) or {}
    # Sort by count desc
    for tool_name, entry in sorted(by_tool.items(), key=lambda kv: -int(kv[1].get("count", 0))):
        lines.append(f"| {tool_name} | {entry.get('count', 0)} | {entry.get('last_called', 'never')} |")
    lines.append("")
    lines.append("To reset: delete the counter file and restart the server.")
    return [types.TextContent(type="text", text="\n".join(lines))]


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

async def main():
    logger.info("Knowledge MCP server starting...")
    logger.info(f"Project root: {PROJECT_ROOT}")
    logger.info(f"DB path: {DB_PATH} (exists: {DB_PATH.exists()})")
    logger.info(f"Index path: {INDEX_PATH} (exists: {INDEX_PATH.exists()})")
    logger.info(f"Constants path: {CONSTANTS_PATH} (exists: {CONSTANTS_PATH.exists()})")

    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options(),
        )


if __name__ == "__main__":
    asyncio.run(main())
