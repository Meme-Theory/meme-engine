# astro MCP — Requirements

## What this pack ships

Server source bundled at `server/`. The unfold copies the whole directory to `{project-root}/tools/mcp-servers/astro-mcp/`, including the `data_io/`, `data_sources/`, `tools/`, `tests/`, and `utils/` subpackages. This is a snapshot of `SandyYuan/astro_mcp` plus project-specific extensions.

## Runtime Dependencies

- **Python**: 3.11 or later
- **Packages** (covered by `requirements-mcp.txt`):
  - `fastmcp` — MCP framework
  - `httpx`, `python-dotenv`, `requests` — HTTP + config plumbing
  - `astropy`, `astroquery` — the 30+ catalog backends
  - `sparclclient` — DESI spectrum access
  - `h5py` — HDF5 I/O for `convert_to_fits` and related tools
  - `numpy`, `pandas` — result tables
- **Optional**:
  - `datalab` — NOIRLab Data Lab services (adds ~5 more astroquery-style backends)
  - `gwosc` — if you want GW tools served from this MCP; otherwise use the standalone `gwosc` MCP

## Installation

```bash
# Covered by the Python backbone install (Phase 7c):
{{PYTHON_CMD}} -m pip install -r requirements-mcp.txt

# Optional extras:
{{PYTHON_CMD}} -m pip install datalab gwosc
```

## Python Detection

Standard detection order (see `unfold-mcp.md` Step 2). Requires Python 3.11+ (astroquery pins below 3.11 have been dropped upstream).

## Verification

```bash
{{PYTHON_CMD}} -c "import fastmcp, astroquery, astropy, sparclclient; print('OK')"

# Smoke test (enumerate discovered services):
{{PYTHON_CMD}} - <<'PY'
import asyncio, sys, os
sys.path.insert(0, "tools/mcp-servers/astro-mcp")
from server import astro_server
services = astro_server.list_astroquery_services()
print(f"{len(services)} services discovered")
PY
```

## Maintenance

- The bundled server is a snapshot. To update to a newer upstream version, re-snapshot from `SandyYuan/astro_mcp` into `templates/disciplines/physics/mcps/astro/server/` in the plugin, then re-scaffold.
- Some astroquery backends require native libraries for FITS I/O (`cfitsio`) on Linux: `conda install -c conda-forge cfitsio` is the fast path if a pure-pip install fails.

## Supported Platforms

Cross-platform. Linux and macOS are best-tested. Windows works with the MCP itself but some astroquery backends occasionally have Windows-specific packaging quirks — use a conda env if pip fights you.
