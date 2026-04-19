"""
GWOSC MCP Server — Gravitational Wave Open Science Center
Provides access to LIGO/Virgo/KAGRA event catalogs, strain data metadata,
and observation run information via the GWOSC REST API.
"""

import json
from fastmcp import FastMCP
import requests

GWOSC_BASE = "https://gwosc.org"

# Physical parameter keys in jsonfull (underscore format)
PARAM_KEYS = [
    "mass_1_source", "mass_2_source", "total_mass_source", "final_mass_source",
    "chirp_mass_source", "luminosity_distance", "redshift",
    "network_matched_filter_snr", "chi_eff", "far", "p_astro",
]

mcp = FastMCP("GWOSC — Gravitational Wave Open Science Center")


def _format_event(vname: str, info: dict) -> str:
    """Format a single event's parameters into readable text."""
    lines = [f"**{info.get('commonName', vname)}** (v{info.get('version', '?')})"]
    lines.append(f"  Catalog: {info.get('catalog.shortName', '?')}")
    lines.append(f"  GPS: {info.get('GPS', '?')}")
    for key in PARAM_KEYS:
        val = info.get(key)
        if val is not None:
            unit = info.get(f"{key}_unit", "")
            lower = info.get(f"{key}_lower", "")
            upper = info.get(f"{key}_upper", "")
            err = ""
            if lower and upper:
                err = f" (+{upper}/{lower})"
            label = key.replace("_", " ")
            lines.append(f"  {label}: {val}{err} {unit}".rstrip())
    strain = info.get("strain", [])
    lines.append(f"  Strain files: {len(strain)}")
    return "\n".join(lines)


@mcp.tool()
def list_catalogs() -> str:
    """List all available gravitational wave event catalogs (GWTC-1, GWTC-2, GWTC-3, etc.)."""
    r = requests.get(f"{GWOSC_BASE}/eventapi/json/", timeout=30)
    r.raise_for_status()
    data = r.json()
    lines = []
    for cat_name, cat_info in data.items():
        desc = cat_info.get("description", "")
        lines.append(f"- **{cat_name}**: {desc}")
    return "\n".join(lines) if lines else "No catalogs found."


@mcp.tool()
def list_events(catalog: str = "GWTC-3-confident") -> str:
    """List all gravitational wave events in a catalog with key parameters.

    Args:
        catalog: Catalog name (e.g. 'GWTC-1-confident', 'GWTC-2.1-confident', 'GWTC-3-confident'). Default: 'GWTC-3-confident'.
    """
    r = requests.get(f"{GWOSC_BASE}/eventapi/jsonfull/{catalog}/", timeout=60)
    r.raise_for_status()
    data = r.json()
    events = data.get("events", {})
    lines = [f"**{catalog}**: {len(events)} events\n"]
    for name, info in sorted(events.items()):
        m1 = info.get("mass_1_source", "?")
        m2 = info.get("mass_2_source", "?")
        dist = info.get("luminosity_distance", "?")
        snr = info.get("network_matched_filter_snr", "?")
        common = info.get("commonName", name)
        lines.append(f"- {common}: m1={m1}, m2={m2} Msun, d={dist} Mpc, SNR={snr}")
    if len(lines) > 52:
        return "\n".join(lines[:52]) + f"\n... and {len(events) - 50} more"
    return "\n".join(lines)


@mcp.tool()
def get_event(event_name: str) -> str:
    """Get detailed parameters for a single gravitational wave event.

    Args:
        event_name: Event name (e.g. 'GW150914', 'GW170817', 'GW190521').
    """
    # Use the json/event/ alias for basic info + strain URLs
    r = requests.get(
        f"{GWOSC_BASE}/eventapi/json/event/{event_name}/", timeout=30
    )
    r.raise_for_status()
    basic = r.json()
    basic_events = basic.get("events", {})

    # Find which catalog this event belongs to
    catalog = None
    for vname, info in basic_events.items():
        catalog = info.get("catalog.shortName")
        break

    if not catalog:
        return f"Event {event_name} not found."

    # Fetch full parameters from the catalog jsonfull endpoint
    r2 = requests.get(f"{GWOSC_BASE}/eventapi/jsonfull/{catalog}/", timeout=60)
    r2.raise_for_status()
    full_data = r2.json()
    full_events = full_data.get("events", {})

    # Find matching event
    for vname, info in full_events.items():
        if info.get("commonName", "") == event_name or event_name in vname:
            result = _format_event(vname, info)
            # Append strain URLs from basic data
            for bname, binfo in basic_events.items():
                strain = binfo.get("strain", [])
                if strain:
                    result += "\n\n  **Strain data:**"
                    for s in strain[:10]:
                        det = s.get("detector", "?")
                        dur = s.get("duration", "?")
                        url = s.get("url", "?")
                        result += f"\n  - [{det}, {dur}s]: {url}"
                break
            return result

    return f"Event {event_name} found in {catalog} but parameters unavailable."


@mcp.tool()
def search_events(
    min_mass: float = None,
    max_mass: float = None,
    min_snr: float = None,
    max_distance: float = None,
    min_chirp_mass: float = None,
    max_far: float = None,
) -> str:
    """Search gravitational wave events by physical parameters.

    Args:
        min_mass: Minimum primary source mass (solar masses).
        max_mass: Maximum primary source mass (solar masses).
        min_snr: Minimum network matched-filter SNR.
        max_distance: Maximum luminosity distance (Mpc).
        min_chirp_mass: Minimum chirp mass (solar masses).
        max_far: Maximum false alarm rate (Hz).
    """
    params = {}
    if min_mass is not None:
        params["mass-1-source-min"] = min_mass
    if max_mass is not None:
        params["mass-1-source-max"] = max_mass
    if min_snr is not None:
        params["network-matched-filter-snr-min"] = min_snr
    if max_distance is not None:
        params["luminosity-distance-max"] = max_distance
    if min_chirp_mass is not None:
        params["chirp-mass-source-min"] = min_chirp_mass
    if max_far is not None:
        params["far-max"] = max_far

    query = "&".join(f"{k}={v}" for k, v in params.items())
    url = f"{GWOSC_BASE}/eventapi/jsonfull/query/show?{query}"
    r = requests.get(url, timeout=60)
    r.raise_for_status()
    data = r.json()
    events = data.get("events", {})
    lines = [f"Found {len(events)} events matching criteria:\n"]
    for name, info in sorted(events.items()):
        m1 = info.get("mass_1_source", "?")
        m2 = info.get("mass_2_source", "?")
        dist = info.get("luminosity_distance", "?")
        snr = info.get("network_matched_filter_snr", "?")
        common = info.get("commonName", name)
        lines.append(f"- {common}: m1={m1}, m2={m2} Msun, d={dist} Mpc, SNR={snr}")
    return "\n".join(lines)


@mcp.tool()
def get_strain_urls(event_name: str, detector: str = "H1") -> str:
    """Get download URLs for strain data files around a gravitational wave event.

    Args:
        event_name: Event name (e.g. 'GW150914').
        detector: Detector code: 'H1' (LIGO Hanford), 'L1' (LIGO Livingston), 'V1' (Virgo), 'K1' (KAGRA).
    """
    r = requests.get(
        f"{GWOSC_BASE}/eventapi/json/event/{event_name}/", timeout=30
    )
    r.raise_for_status()
    data = r.json()
    events = data.get("events", data)
    for ename, edata in events.items():
        strain = edata.get("strain", [])
        matched = [s for s in strain if s.get("detector", "") == detector]
        if matched:
            lines = [f"Strain files for {event_name} ({detector}):"]
            for s in matched:
                url = s.get("url", "?")
                dur = s.get("duration", "?")
                fmt = s.get("format", "?")
                sampling = s.get("sampling_rate", "?")
                lines.append(f"- [{fmt}, {dur}s, {sampling}Hz]: {url}")
            return "\n".join(lines)
    return f"No strain data found for {event_name} at detector {detector}."


@mcp.tool()
def get_run_info(dataset: str = "O3b_16KHZ_R1") -> str:
    """Get metadata about an observing run dataset.

    Args:
        dataset: Dataset identifier (e.g. 'O1', 'O2_16KHZ_R1', 'O3a_16KHZ_R1', 'O3b_16KHZ_R1', 'O4a_16KHZ_R1').
    """
    r = requests.get(
        f"{GWOSC_BASE}/archive/dataset/{dataset}/json/", timeout=30
    )
    r.raise_for_status()
    data = r.json()
    return json.dumps(data, indent=2, default=str)


@mcp.tool()
def get_timeline(
    dataset: str, gps_start: int, duration: int, timeline: str = "DATA"
) -> str:
    """Get data quality timeline segments for an observing run.

    Args:
        dataset: Dataset name (e.g. 'O3b_16KHZ_R1').
        gps_start: GPS start time (seconds).
        duration: Duration (seconds).
        timeline: Timeline type ('DATA', 'CBC_CAT1', 'CBC_CAT2', 'BURST_CAT1', etc.). Default: 'DATA'.
    """
    r = requests.get(
        f"{GWOSC_BASE}/timeline/segments/json/{dataset}/{timeline}/{gps_start}/{duration}/",
        timeout=30,
    )
    r.raise_for_status()
    data = r.json()
    segments = data.get("segments", [])
    total = sum(s[1] - s[0] for s in segments) if segments else 0
    return (
        f"Timeline '{timeline}' for {dataset}: {len(segments)} segments, "
        f"{total:.0f}s total live time\n"
        f"First 10 segments: {segments[:10]}"
    )


if __name__ == "__main__":
    mcp.run()
