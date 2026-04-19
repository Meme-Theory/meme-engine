### GWOSC MCP — Gravitational-Wave Open Science Center

Wraps the `gwosc` Python client for LIGO / Virgo / KAGRA event catalogs and strain data. Ships with the plugin as bundled source at `tools/mcp-servers/gwosc-mcp/server.py` after install.

**Tools exposed:**

| Tool | Purpose |
|:-----|:--------|
| `list_catalogs()` | All GW event catalogs (GWTC-1 through current). |
| `list_events(catalog)` | Events in a catalog with masses, distances, SNR. |
| `get_event(event_name)` | Full parameters for one event (e.g., `GW150914`). |
| `search_events(min_mass, max_snr, ...)` | Filter by physical parameters. |
| `get_strain_urls(event_name, detector)` | Download URLs for strain data per detector. |
| `get_run_info(dataset)` | Observing-run metadata. |
| `get_timeline(dataset, gps_start, duration)` | Data-quality segments. |

**Guidance:**

- Strain URLs are large (~MB per event per detector). Download only what you need; cache under `tools/mcp-servers/gwosc-mcp/cache/` or a project-chosen cache directory.
- Event parameters (masses, spins, distances) can be cited directly as gate inputs — log the query and the retrieved value in the session file, treat the MCP-retrieved value as canonical.
- When an event is re-processed in a newer catalog (GWTC-2 → GWTC-2.1 → GWTC-3), parameters can shift. Cite the catalog version alongside the event name.
