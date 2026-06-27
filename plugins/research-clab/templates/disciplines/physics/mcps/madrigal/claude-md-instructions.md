### Madrigal MCP — Ionospheric / Heliophysics Database

Wraps the CEDAR Madrigal database ecosystem (ionospheric radar, incoherent-scatter, magnetometer, GPS-TEC networks). Bundled source at `tools/mcp-servers/madrigal-mcp/server.py` after install.

**Generic Madrigal access:**

| Tool | Purpose |
|:-----|:--------|
| `list_madrigal_servers()` | Canonical list of public Madrigal servers |
| `list_instruments(server)` | Instruments catalogued at a server |
| `list_experiments(server, instrument, start, end)` | Experiments for an instrument in a date range |
| `list_experiment_files(experiment_id)` | Data files for an experiment |
| `list_parameters(file_id)` | Parameters (columns) in a file |
| `isprint_filter(file_id, params, filter)` | Extract a parameter subset with filtering |
| `download_file(file_id, format)` | Download in HDF5 / netCDF4 / ASCII |

**Framework-specific helpers** (the shipped server includes project-oriented search helpers; they are harmless for projects outside the original research focus and can be ignored, renamed, or deleted by editing `data_sources/framework_search.py`):

| Tool | Purpose |
|:-----|:--------|
| `list_framework_instruments()` | Curated list ranked by project priority |
| `search_by_frequency(hz_low, hz_high)` | Instruments in a frequency band |
| `list_anomaly_campaigns()` | Published anomaly campaigns with citations |
| `describe_framework_target()` | Current framework target description |

**Guidance:**

- Madrigal APIs can rate-limit. Prefer `list_*` then targeted `download_file` over wide scans.
- Cache downloaded files under `tools/mcp-servers/madrigal-mcp/cache/` or a project-chosen cache directory.
- The framework-specific helpers are opinionated about one research program; editing `data_sources/framework_search.py` to reflect your project's targets is expected.
