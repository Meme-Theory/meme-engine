### Astro MCP

Unified access to astronomical datasets — DESI spectra, 30+ astroquery services (SIMBAD, VizieR, SDSS, Gaia, MAST, IRSA, NED, etc.), and gravitational-wave catalog data. Server source bundled at `tools/mcp-servers/astro-mcp/` after install (snapshot of `SandyYuan/astro_mcp` plus project extensions).

**Framework relevance**: DESI BAO gives a direct `w(z)` measurement and is a Tier-1 observable for cosmology projects. Astroquery services are the workhorse for cross-matching surveys when corroborating a predicted signal.

**Key tools** (names as exposed by the server):

- `list_astroquery_services()` — enumerate the 30+ survey services discovered on server startup.
- `astroquery_<service>_<method>(...)` — auto-generated per service (e.g., `astroquery_simbad_query_object(name)`, `astroquery_gaia_query_region(...)`). Check `list_astroquery_services()` output for the exact names your installation registers.
- `desi_spectrum(target_id)` — fetch DESI spectra directly via sparclclient.
- `get_global_statistics()` — server-level stats (file registry size, services count).

### GWOSC Tools (gravitational-wave events)

If the project also installs the GWOSC MCP (`gwosc-mcp`, a separate clone or the astro-mcp's GW submodule), these tools expose:

- `list_catalogs()` — all GW event catalogs (GWTC-1 through GWTC-4 at time of writing).
- `list_events(catalog)` — events with masses, distances, SNR.
- `get_event(event_name)` — full parameters for one event (e.g., `GW150914`).
- `search_events(min_mass, max_snr, ...)` — filter by physical parameters.
- `get_strain_urls(event_name, detector)` — download URLs for strain data.
- `get_run_info(dataset)` — observing run metadata.
- `get_timeline(dataset, gps_start, duration)` — data quality segments.

### Guidance

- Astroquery calls hit external APIs — batch where possible; respect rate limits.
- DESI spectrum fetches can be large — cache results under `tools/mcp-servers/astro-mcp/data_io/` or a project-chosen cache directory.
- When a prediction depends on a catalog value, query via MCP, log the query + retrieved value in the session file, and treat the MCP-retrieved value as the gate input for SHA-256 pinning purposes.
