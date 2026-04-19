# Madrigal MCP Server

MCP (Model Context Protocol) server wrapping the Madrigal ionospheric /
heliophysics database ecosystem, with framework-specific search helpers
for the Phonon-Exflation Cosmology retrospective-analysis program.

## What It Does

Exposes 11 tools to the Claude Code harness:

### Generic Madrigal access
1. **list_madrigal_servers** — canonical list of public Madrigal servers
2. **list_instruments** — instruments catalogued at a given server
3. **list_experiments** — experiments for an instrument in a date range
4. **list_experiment_files** — data files available for an experiment
5. **list_parameters** — parameters (columns) available in a file
6. **isprint_filter** — extract a parameter subset with optional filtering
7. **download_file** — download a data file in HDF5/netCDF4/ASCII

### Framework-specific retrospective search
8. **list_framework_instruments** — curated list ranked by framework priority
9. **search_by_frequency** — find instruments in a target frequency band
10. **list_anomaly_campaigns** — published anomaly campaigns with citations
11. **describe_framework_target** — current Tesla-Mack Jensen-resonance target

## Why It Exists

Per `sessions/session-74/session-74-rf-analysis.md`, the Phonon-Exflation
Cosmology framework predicts substrate-level pair production via coherent
RF stimulation of the Leggett-channel Jensen mode. Retrospective analysis
of existing ionospheric-radar and ionospheric-heater operational archives
is the cheapest framework-test pathway — orders of magnitude cheaper than
building a new experiment.

The Madrigal database at MIT Haystack is the primary public archive for
EISCAT, Millstone Hill, AMISR, Jicamarca, Arecibo (historical), and others.
No MCP wrapper existed for it as of 2026-04-11 (verified against
[MITHaystack GitHub](https://github.com/MITHaystack)); this server fills
that gap.

## Known Framework-Relevant Targets

Ranked by priority per `session-74-rf-analysis.md` §V:

| Priority | Instrument | Why |
|:--------:|:-----------|:----|
| 3 | EISCAT Heating (Ramfjordmoen) | Blagoveshchenskaya 2012 X-mode anomaly — published unexplained mechanism |
| 4 | EISCAT_3D (Skibotn/Kiruna/Karesuvanto) | 9,919-element phased array at 233 MHz; structurally-identical to Tesla bell-array design; open-data policy |
| 5 | EISCAT VHF 224 MHz | Closest-frequency long-archive target; 128-element phased feed |
| 7 | AMISR PFISR/RISR-N | Phased-array with coordinated optical instrumentation |
| 8 | Arecibo historical | 2019 anomalous plasma cavity (Levine 2020) |
| 9 | Jicamarca | 50 MHz equatorial long-baseline |
| 10 | Millstone Hill | UHF ISR, excellent data access |

## Installation

```bash
cd tools/mcp-servers/madrigal-mcp
py -3.13 -m pip install -r requirements.txt
```

Dependencies:
- `madrigalWeb` (MIT Haystack's pure-Python Madrigal client)
- `mcp` (official Model Context Protocol Python SDK)

## Configuration

Register in the project's `.mcp.json`:

```json
{
  "mcpServers": {
    "madrigal": {
      "type": "stdio",
      "command": "C:\\Users\\ryan\\AppData\\Local\\Programs\\Python\\Launcher\\py.exe",
      "args": ["-3.13", "tools/mcp-servers/madrigal-mcp/server.py"],
      "cwd": "C:\\sandbox\\Ainulindale Exflation\\tools\\mcp-servers\\madrigal-mcp",
      "env": {}
    }
  }
}
```

(Add alongside the existing `astro` and `paper-search` entries.)

## Testing

Quick smoke test of the client:

```python
from data_sources import MadrigalClient, FrameworkSearch

client = MadrigalClient()
print(client.list_known_servers())
# Should return ~6 servers (cedar, eiscat, millstone, jicamarca, arecibo, sri)

fw = FrameworkSearch(client)
print(fw.describe_framework_target())
# Should return Jensen-resonance target parameters

print(fw.list_framework_instruments())
# Should return 9 framework-relevant instruments with priority ranking
```

Full Madrigal-server connectivity test (requires network):

```python
# This will actually connect to EISCAT's public Madrigal server
instruments = client.list_instruments("eiscat")
for inst in instruments[:5]:
    print(inst["code"], inst["name"])
```

## Framework Integration

The framework-specific tools encode:

- The Tesla-Mack workshop target Jensen resonance frequency (~160 MHz, ±50%)
- The curated instrument priority ranking from `session-74-rf-analysis.md` §V
- The published anomaly campaigns (EISCAT X-mode 2012, Arecibo 2019, Sura 2021)

When the OQ-TESLA-T1 / OQ-TESLA-T4 pre-computations return refined frequency
estimates, update `data_sources/framework_search.py` constants:

- `FRAMEWORK_TARGET_HZ`
- `FRAMEWORK_FREQUENCY_BAND_HZ`
- `FRAMEWORK_TARGET_TOLERANCE`
- `FRAMEWORK_INSTRUMENTS` priority field
- `KNOWN_ANOMALY_CAMPAIGNS` (new leads as they're identified)

## Logging

Server logs go to `madrigal_mcp.log` in the server directory. stderr is
suppressed (required for MCP stdio handshake compatibility).

## Sources

- [MIT Haystack Observatory GitHub](https://github.com/MITHaystack)
- [madrigalWeb client](https://github.com/MITHaystack/madrigalWeb)
- [Madrigal at MIT Haystack](http://madrigal.haystack.mit.edu/)
- [EISCAT Madrigal](https://madrigal.eiscat.se/madrigal/)
- [Model Context Protocol Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- `sessions/session-74/session-74-rf-analysis.md` — framework retrospective-analysis program
- `sessions/session-74/session-74-tesla-mack-bells-workshop.md` — Jensen-resonance target parameters
- `sessions/framework/Phononic-C-Causality.md` — framework theorems
