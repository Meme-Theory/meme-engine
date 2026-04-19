#!/usr/bin/env python3
"""
Sage MCP Server — SageMath Computer Algebra Access

Two backends, selected automatically:

1. **Local Sage** (preferred if present) — if the environment variable `SAGE_BIN`
   is set and points to a working `sage` executable, code is run via subprocess.
   Faster, no network, supports arbitrary libraries.

2. **SageCell** (fallback, always available) — public hosted Sage at
   https://sagecell.sagemath.org/service. Zero install. POSTs code, parses
   the JSON response. Session isolation; no persistent state between calls.

Tools exposed:
  sage_eval          — run arbitrary Sage code, return stdout + last expression
  sage_simplify      — simplify a symbolic expression
  sage_latex         — render a symbolic expression to LaTeX
  sage_symbolic_eig  — compute exact eigenvalues of a small integer/rational matrix
  sage_backend_info  — report which backend is active

The framework's substrate algebra (SU(3) representation sums, spectral moment
identities, KK zeta-regularized sums) often wants exact rational/algebraic
answers instead of floating point. This server gives agents that option.
"""

import warnings
import os
warnings.filterwarnings("ignore")
os.environ["PYTHONWARNINGS"] = "ignore"

import asyncio
import json
import logging
import shutil
import subprocess
import uuid
from pathlib import Path

import httpx
import websockets
import mcp.server.stdio
import mcp.types as types
from mcp.server import Server

SERVER_DIR = Path(__file__).resolve().parent
SAGECELL_BASE = "https://sagecell.sagemath.org"
SAGECELL_KERNEL_URL = f"{SAGECELL_BASE}/kernel"
USER_AGENT = "Ainulindale-Exflation/Sage-MCP"
HTTP_TIMEOUT = 60.0
SAGE_BIN = os.environ.get("SAGE_BIN", "").strip()

logging.basicConfig(
    level=logging.INFO,
    filename=str(SERVER_DIR / "sage_mcp.log"),
    filemode="w",
    format="%(asctime)s %(levelname)s %(message)s",
)
logger = logging.getLogger(__name__)

server = Server("sage")


def _local_sage_available() -> bool:
    if SAGE_BIN and Path(SAGE_BIN).exists():
        return True
    return shutil.which("sage") is not None


def _active_backend() -> str:
    if _local_sage_available():
        return "local"
    return "sagecell"


async def _run_sagecell(code: str, timeout: float = 60.0) -> dict:
    """Execute code against SageCell via its Jupyter kernel WebSocket.

    Protocol:
      1. POST /kernel → {id, ws_url}
      2. Connect WebSocket at {ws_url}kernel/{id}/channels
      3. Send Jupyter `execute_request` on channel 'shell'
      4. Drain iopub messages until execution_state == 'idle'
      5. Collect stream/execute_result/error into a uniform result dict
    """
    # 1) Kernel handshake
    async with httpx.AsyncClient(timeout=timeout, headers={"User-Agent": USER_AGENT}) as client:
        r = await client.post(SAGECELL_KERNEL_URL, data={"accepted_tos": "true"})
        r.raise_for_status()
        meta = r.json()
    kernel_id = meta["id"]
    ws_url = f"{meta['ws_url']}kernel/{kernel_id}/channels"

    # 2-5) Jupyter execute over WebSocket
    msg_id = str(uuid.uuid4())
    session_id = str(uuid.uuid4())
    exec_msg = {
        "header": {
            "msg_id": msg_id, "username": "mcp", "session": session_id,
            "msg_type": "execute_request", "version": "5.2",
        },
        "parent_header": {},
        "metadata": {},
        "channel": "shell",
        "content": {
            "code": code,
            "silent": False,
            "store_history": False,
            "user_expressions": {},
            "allow_stdin": False,
            "stop_on_error": True,
        },
    }

    stdout_parts: list[str] = []
    stderr_parts: list[str] = []
    success = True

    try:
        async with websockets.connect(ws_url) as ws:
            await ws.send(json.dumps(exec_msg))
            done = False
            while not done:
                raw = await asyncio.wait_for(ws.recv(), timeout=timeout)
                msg = json.loads(raw)
                hdr = msg.get("header", {})
                parent = msg.get("parent_header", {}).get("msg_id")
                if parent != msg_id:
                    continue
                t = hdr.get("msg_type")
                content = msg.get("content", {})
                if t == "stream":
                    if content.get("name") == "stderr":
                        stderr_parts.append(content.get("text", ""))
                    else:
                        stdout_parts.append(content.get("text", ""))
                elif t == "execute_result":
                    data = content.get("data", {})
                    text = data.get("text/plain", "")
                    if text:
                        stdout_parts.append(str(text) + ("\n" if not text.endswith("\n") else ""))
                elif t == "error":
                    success = False
                    stderr_parts.append(f"{content.get('ename', '')}: {content.get('evalue', '')}")
                    for tb in content.get("traceback", []) or []:
                        stderr_parts.append(tb)
                elif t == "status" and content.get("execution_state") == "idle":
                    done = True
    except asyncio.TimeoutError:
        return {
            "stdout": "".join(stdout_parts),
            "stderr": ("".join(stderr_parts) + f"\n[TIMEOUT after {timeout}s]").strip(),
            "success": False,
            "backend": "sagecell",
        }
    except Exception as e:
        return {
            "stdout": "".join(stdout_parts),
            "stderr": f"{''.join(stderr_parts)}\n[WebSocket error: {e}]".strip(),
            "success": False,
            "backend": "sagecell",
        }

    return {
        "stdout": "".join(stdout_parts),
        "stderr": "\n".join(s for s in stderr_parts if s),
        "success": success,
        "backend": "sagecell",
    }


async def _run_local_sage(code: str, timeout: float = 60.0) -> dict:
    """Run code via local sage subprocess."""
    sage = SAGE_BIN or shutil.which("sage")
    if not sage:
        raise RuntimeError("Local Sage not available")
    loop = asyncio.get_event_loop()

    def _run():
        proc = subprocess.run(
            [sage, "-c", code],
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
        return proc.returncode, proc.stdout, proc.stderr

    rc, out, err = await loop.run_in_executor(None, _run)
    return {"stdout": out, "stderr": err, "success": rc == 0, "backend": "local"}


async def _run_sage(code: str, timeout: float = 60.0) -> dict:
    if _local_sage_available():
        return await _run_local_sage(code, timeout)
    return await _run_sagecell(code, timeout)


def _fmt_result(result: dict, header: str | None = None) -> str:
    lines = []
    if header:
        lines.append(header)
    lines.append(f"- **Backend**: `{result.get('backend', '?')}`")
    lines.append(f"- **Success**: {result.get('success')}")
    if result.get("stdout"):
        lines.append("- **stdout**:")
        lines.append("```")
        lines.append(result["stdout"].strip())
        lines.append("```")
    if result.get("stderr"):
        lines.append("- **stderr**:")
        lines.append("```")
        lines.append(result["stderr"].strip())
        lines.append("```")
    return "\n".join(lines)


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="sage_eval",
            description=(
                "Execute arbitrary Sage code. The last expression is printed automatically. "
                "Multi-line OK. Use this for exact symbolic computation: rationals, "
                "algebraic numbers, polynomial factorisation, group theory, number theory, "
                "symbolic integrals. Timeout default 60s (max 120s)."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "code": {"type": "string", "description": "Sage source code"},
                    "timeout": {"type": "number", "default": 60, "minimum": 1, "maximum": 120},
                },
                "required": ["code"],
            },
        ),
        types.Tool(
            name="sage_simplify",
            description="Simplify one symbolic expression (applies simplify_full()).",
            inputSchema={
                "type": "object",
                "properties": {
                    "expr": {"type": "string", "description": "A Sage symbolic expression (e.g. 'sin(x)^2+cos(x)^2')"},
                },
                "required": ["expr"],
            },
        ),
        types.Tool(
            name="sage_latex",
            description="Render a Sage expression to LaTeX via latex().",
            inputSchema={
                "type": "object",
                "properties": {"expr": {"type": "string"}},
                "required": ["expr"],
            },
        ),
        types.Tool(
            name="sage_symbolic_eig",
            description=(
                "Compute EXACT eigenvalues of a small rational/integer matrix via Sage. "
                "Input: a Python nested-list literal like '[[1,2],[3,4]]' or '[[1/2,0],[0,3]]'. "
                "Returns characteristic polynomial + factored roots. Use this when the "
                "matrix is small (dim ≤ 8) and you need algebraic (not float) spectra."
            ),
            inputSchema={
                "type": "object",
                "properties": {"matrix": {"type": "string", "description": "Nested-list literal"}},
                "required": ["matrix"],
            },
        ),
        types.Tool(
            name="sage_backend_info",
            description="Report which Sage backend is active (local vs. SageCell).",
            inputSchema={"type": "object", "properties": {}},
        ),
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: dict | None) -> list[types.TextContent]:
    args = arguments or {}
    try:
        if name == "sage_eval":
            return await _tool_eval(args)
        if name == "sage_simplify":
            return await _tool_simplify(args)
        if name == "sage_latex":
            return await _tool_latex(args)
        if name == "sage_symbolic_eig":
            return await _tool_eig(args)
        if name == "sage_backend_info":
            return [types.TextContent(type="text", text=_backend_info_text())]
        return [types.TextContent(type="text", text=f"Unknown tool: {name}")]
    except Exception as e:
        logger.exception("Sage tool error")
        return [types.TextContent(type="text", text=f"Error: {e}")]


def _backend_info_text() -> str:
    backend = _active_backend()
    lines = [f"# Sage MCP backend\n- **Active**: `{backend}`"]
    if backend == "local":
        lines.append(f"- **SAGE_BIN**: `{SAGE_BIN or shutil.which('sage')}`")
        lines.append("- Subprocess mode; full library access; no network required.")
    else:
        lines.append(f"- **Endpoint**: `{SAGECELL_URL}`")
        lines.append("- Network required. Session-isolated (no persistent state).")
        lines.append("- Set `SAGE_BIN=/path/to/sage` to switch to local subprocess mode.")
    return "\n".join(lines)


async def _tool_eval(args: dict) -> list[types.TextContent]:
    code = args["code"]
    timeout = float(args.get("timeout", 60))
    result = await _run_sage(code, timeout=timeout)
    return [types.TextContent(type="text", text=_fmt_result(result, header=f"# sage_eval\n"))]


async def _tool_simplify(args: dict) -> list[types.TextContent]:
    expr = args["expr"]
    # Declare common symbolic variables so arbitrary input works.
    code = (
        "var('x y z t a b c d n m k p q r s u v w alpha beta gamma theta phi tau omega')\n"
        f"_e = {expr}\n"
        "print(_e.simplify_full())\n"
    )
    result = await _run_sage(code)
    return [types.TextContent(type="text", text=_fmt_result(result, header=f"# sage_simplify(`{expr}`)\n"))]


async def _tool_latex(args: dict) -> list[types.TextContent]:
    expr = args["expr"]
    code = (
        "var('x y z t a b c d n m k p q r s u v w alpha beta gamma theta phi tau omega')\n"
        f"_e = {expr}\n"
        "print(latex(_e))\n"
    )
    result = await _run_sage(code)
    return [types.TextContent(type="text", text=_fmt_result(result, header=f"# sage_latex(`{expr}`)\n"))]


async def _tool_eig(args: dict) -> list[types.TextContent]:
    mat = args["matrix"]
    code = (
        "from sage.all import Matrix, QQ\n"
        f"_M = Matrix(QQ, {mat})\n"
        "print('dim =', _M.nrows(), 'x', _M.ncols())\n"
        "print('charpoly =', _M.charpoly().factor())\n"
        "print('eigenvalues (with multiplicity):')\n"
        "for ev, mult in _M.eigenvalues(extend=True).items() if isinstance(_M.eigenvalues(extend=True), dict) else [(ev, 1) for ev in _M.eigenvalues(extend=True)]:\n"
        "    print(f'  {ev}  (mult {mult})')\n"
    )
    result = await _run_sage(code)
    return [types.TextContent(type="text", text=_fmt_result(result, header=f"# sage_symbolic_eig\n"))]


async def main():
    backend = _active_backend()
    logger.info("Sage MCP server starting... backend=%s", backend)
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
