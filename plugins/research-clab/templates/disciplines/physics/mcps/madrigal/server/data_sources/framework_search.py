"""
Framework-specific search helpers for retrospective analysis.

These tools encode the project's search criteria for locating existing data
that might retrospectively contain substrate-level pair production signatures
per the Jensen-resonance framework prediction (see
sessions/framework/Phononic-C-Causality.md and
sessions/session-74/session-74-rf-analysis.md).

The helpers layer framework-specific knowledge on top of the generic
MadrigalClient interface: which instruments are phased-array coherent
emitters, which campaigns match the framework's target frequency band,
which experiments explicitly reported anomalies in published literature.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any

from .madrigal_client import MadrigalClient

logger = logging.getLogger(__name__)


# Framework-specific instrument priority list. Ranked by framework-test value
# per the session-74-rf-analysis.md Section V priority table. Keys are canonical
# short names; values are dicts with instrument code (verified against live
# EISCAT Madrigal query 2026-04-11), Madrigal server short name, and priority
# metadata.
#
# Category layout:
#  (A) Radar instruments — active phased-array or dish emitters
#  (B) Optical coincidence instruments — Fabry-Perots, photometers, all-sky
#      imagers colocated with radars. Critical for framework search because
#      pair-annihilation signatures (511 keV, anomalous spectral lines) would
#      appear in OPTICAL data not in radar returns.
#
# EISCAT Heating facility and EISCAT_3D are NOT in this table because:
#  - EISCAT Heating (Ramfjordmoen) is a facility, not a Madrigal instrument.
#    The 2012 Blagoveshchenskaya X-mode anomaly data lives under whichever ISR
#    observed it — typically EISCAT Tromsø UHF (72) or VHF (74).
#  - EISCAT_3D has NOT achieved first light as of 2026-04. Construction began
#    November 2022; Karesuvanto and Kaiseniemi receiver sites completed
#    September 2023; Skibotn core transmitter status unreported, integrated
#    system not yet producing scientific data, no Madrigal instrument code
#    assigned. (Per Wikipedia EISCAT article, last updated 2026-03-22.) When
#    EISCAT_3D eventually comes online, it will likely be assigned a Madrigal
#    code in the 2000s-8000s range; check periodically with list_instruments.
#
# CRITICAL OPERATIONAL STATUS UPDATE (verified 2026-04-11):
#  - Kiruna UHF antenna (code 71) DEMOLISHED 13 October 2024
#  - Sodankylä UHF antenna (code 73) DEMOLISHED 23 April 2025
#  - Kiruna VHF receiver (code 75) — no new data after Kiruna demolition
#  - Sodankylä VHF receiver (code 76) — no new data after Sodankylä demolition
#  - The legacy EISCAT tristatic UHF system NO LONGER EXISTS as operational
#    hardware. Codes 71, 73, 75, 76 are now purely historical archive targets.
#  - EISCAT Tromsø UHF (72) and Tromsø VHF (74) remain operational at
#    Ramfjordmoen. Tromsø is the sole surviving legacy EISCAT mainland site.
#  - EISCAT Svalbard (95) remains operational at Longyearbyen.
#  - EISCAT Heating facility at Ramfjordmoen remains operational.
FRAMEWORK_INSTRUMENTS: dict[str, dict[str, Any]] = {
    # === (A) Radar instruments ===
    "eiscat_vhf_tromso": {
        "name": "EISCAT Tromsø VHF IS radar (224 MHz) — OPERATIONAL",
        "server": "eiscat",
        "code_hint": 74,  # verified 2026-04-11
        "frequency_hz": 224e6,
        "coherent_elements": 128,
        "operational_since": 1985,
        "priority": 4,  # PROMOTED: closest-frequency AND still operational
        "instrument_type": "radar",
        "framework_note": (
            "OPERATIONAL at Ramfjordmoen. Closest-frequency framework target "
            "with 40 years of operational archive. 128-element phased feed on "
            "120x40 m cylindrical parabolic, ~2 MW peak. Target Jensen resonance "
            "per Tesla T4 is ~160 MHz; this is 40% off — borderline relevance "
            "depending on Q factor. Observation of EISCAT Heating X-mode "
            "anomalies is catalogued under THIS instrument when VHF was the "
            "radar used (2012-2015 campaigns). POST-2024 NOTE: Kiruna VHF "
            "receiver (code 75) and Sodankylä VHF receiver (code 76) no longer "
            "contribute to tristatic measurements following the 2024-2025 "
            "decommissioning of the Kiruna/Sodankylä sites."
        ),
    },
    "eiscat_uhf_tromso": {
        "name": "EISCAT Tromsø UHF IS radar (~930 MHz) — OPERATIONAL",
        "server": "eiscat",
        "code_hint": 72,  # verified 2026-04-11
        "frequency_hz": 931e6,
        "coherent_elements": 1,  # 32-m steerable dish, not phased-array
        "operational_since": 1981,
        "priority": 5,
        "instrument_type": "radar",
        "framework_note": (
            "OPERATIONAL at Ramfjordmoen. Sole surviving legacy EISCAT UHF "
            "ISR on the mainland after Kiruna UHF (71) was demolished 13 Oct "
            "2024 and Sodankylä UHF (73) was demolished 23 Apr 2025. "
            "Mechanically-steered 32-m dish, NOT phased-array. Critical "
            "framework priority because the Blagoveshchenskaya X-mode anomaly "
            "observations use EISCAT UHF as the primary diagnostic radar "
            "during Heating campaigns. Archive search for 2009-2015 X-mode "
            "heating campaigns should query THIS instrument."
        ),
    },
    "eiscat_kiruna_uhf_historical": {
        "name": "EISCAT Kiruna UHF IS Receiver (DEMOLISHED 2024-10-13)",
        "server": "eiscat",
        "code_hint": 71,  # verified 2026-04-11; hardware no longer exists
        "frequency_hz": 931e6,
        "coherent_elements": 1,
        "operational_since": 1981,
        "priority": 14,
        "instrument_type": "radar_historical",
        "framework_note": (
            "HISTORICAL ARCHIVE ONLY. Antenna demolished 13 October 2024 "
            "as part of the transition to EISCAT_3D. No new data after this "
            "date. The 1981-2024 tristatic archive is still accessible via "
            "Madrigal and covers 43 years of UHF ISR observations."
        ),
    },
    "eiscat_sodankyla_uhf_historical": {
        "name": "EISCAT Sodankylä UHF IS Receiver (DEMOLISHED 2025-04-23)",
        "server": "eiscat",
        "code_hint": 73,  # verified 2026-04-11; hardware no longer exists
        "frequency_hz": 931e6,
        "coherent_elements": 1,
        "operational_since": 1981,
        "priority": 14,
        "instrument_type": "radar_historical",
        "framework_note": (
            "HISTORICAL ARCHIVE ONLY. Antenna demolished 23 April 2025 as "
            "part of the transition to EISCAT_3D. No new data after this "
            "date. The 1981-2025 tristatic archive is still accessible via "
            "Madrigal."
        ),
    },
    "eiscat_svalbard": {
        "name": "EISCAT Svalbard IS Radar (ESR, Longyearbyen, 500 MHz) — OPERATIONAL",
        "server": "eiscat",
        "code_hint": 95,  # verified 2026-04-11
        "frequency_hz": 500e6,
        "coherent_elements": 1,  # 32-m steerable + 42-m fixed
        "operational_since": 1996,
        "priority": 9,
        "instrument_type": "radar",
        "framework_note": (
            "OPERATIONAL at Longyearbyen. Dish-based ISR on Svalbard. Lower "
            "framework priority (not phased-array, far from 160 MHz target) "
            "but unique geographic position and 30 years of data. One of only "
            "three surviving EISCAT ISRs after the 2024-2025 mainland "
            "decommissioning (the others being Tromsø UHF and Tromsø VHF). "
            "Colocated with Svalbard all-sky imagers for optical coincidence."
        ),
    },
    "eiscat_combined": {
        "name": "EISCAT combined IS Radars (tristatic)",
        "server": "eiscat",
        "code_hint": 70,  # verified 2026-04-11
        "frequency_hz": 0.0,  # meta-instrument covering multiple facilities
        "coherent_elements": 0,
        "operational_since": 1981,
        "priority": 12,
        "instrument_type": "radar_meta",
        "framework_note": (
            "Meta-instrument for tristatic EISCAT measurements combining "
            "Tromsø UHF + Kiruna + Sodankylä receivers. Use to find datasets "
            "that use all three sites simultaneously."
        ),
    },
    "millstone_hill": {
        "name": "Millstone Hill IS Radar (440 MHz)",
        "server": "millstone",
        "code_hint": 30,  # verified 2026-04-11
        "frequency_hz": 440e6,
        "coherent_elements": 1,
        "operational_since": 1963,
        "priority": 10,
        "instrument_type": "radar",
        "framework_note": (
            "Long-baseline UHF ISR at MIT Haystack. 67-m steerable + 46-m "
            "zenith dishes. Not phased-array. Longest continuous operational "
            "record in the ISR community. Colocated with Millstone Hill "
            "Fabry-Perot (5340, 5360) and BU Millstone All-Sky Imager (7200) "
            "for optical coincidence."
        ),
    },
    "pfisr": {
        "name": "Poker Flat IS Radar (PFISR, AMISR)",
        "server": "eiscat",  # also accessible via SRI Madrigal
        "code_hint": 61,  # verified 2026-04-11
        "frequency_hz": 450e6,
        "coherent_elements": 4096,  # per face
        "operational_since": 2007,
        "priority": 7,
        "instrument_type": "radar",
        "framework_note": (
            "Phased-array ISR with 4,096 panels at 450 MHz. Direct comparison "
            "to Tesla's bell-array geometry at a different frequency. "
            "Colocated with Poker Flat Fabry-Perot (5475), all-sky scanning "
            "Fabry-Perot (5465), 4-channel filter photometer (4470), and lidar "
            "(6380). The optical-coincidence setup at Poker Flat is among the "
            "richest in the ISR community for framework-specific cross-search."
        ),
    },
    "risr_n": {
        "name": "Resolute Bay North IS Radar (RISR-N, AMISR)",
        "server": "eiscat",
        "code_hint": 91,  # verified 2026-04-11
        "frequency_hz": 443e6,
        "coherent_elements": 4096,
        "operational_since": 2009,
        "priority": 7,
        "instrument_type": "radar",
        "framework_note": (
            "Twin of PFISR at Resolute Bay Canada. Same framework relevance. "
            "Colocated with Resolute Bay Fabry-Perot (5535) and Michelson "
            "Interferometer (5950)."
        ),
    },
    "risr_c": {
        "name": "Resolute Bay Canada IS Radar (RISR-C)",
        "server": "eiscat",
        "code_hint": 92,  # verified 2026-04-11
        "frequency_hz": 443e6,
        "coherent_elements": 4096,
        "operational_since": 2015,
        "priority": 8,
        "instrument_type": "radar",
        "framework_note": (
            "Second AMISR face at Resolute Bay, pointed differently from "
            "RISR-N. Newer installation. Same colocated optical instruments."
        ),
    },
    "poker_flat_mst": {
        "name": "Poker Flat MST Radar (~46 MHz)",
        "server": "eiscat",
        "code_hint": 1140,  # verified 2026-04-11
        "frequency_hz": 46e6,
        "coherent_elements": 100,  # approximate
        "operational_since": 1998,
        "priority": 11,
        "instrument_type": "radar",
        "framework_note": (
            "Mesosphere-Stratosphere-Troposphere radar at Poker Flat. VHF, "
            "much lower frequency than Tesla target but phased-array coherent "
            "emitter with decades of operation."
        ),
    },
    "poker_flat_mf": {
        "name": "Poker Flat MF radar",
        "server": "eiscat",
        "code_hint": 1375,  # verified 2026-04-11
        "frequency_hz": 2.5e6,
        "coherent_elements": 4,  # approximate
        "operational_since": 1998,
        "priority": 13,
        "instrument_type": "radar",
        "framework_note": (
            "Medium-frequency radar. Off target, lower priority."
        ),
    },
    # === (B) Optical coincidence instruments (colocated with radars) ===
    "pfisr_fabry_perot": {
        "name": "Poker Flat Fabry-Perot",
        "server": "eiscat",
        "code_hint": 5475,  # verified 2026-04-11
        "frequency_hz": 0.0,  # optical
        "coherent_elements": 0,
        "operational_since": 1990,
        "priority": 2,  # HIGH — spectroscopy colocated with PFISR phased array
        "instrument_type": "optical_fabry_perot",
        "framework_note": (
            "HIGH FRAMEWORK PRIORITY. Fabry-Perot spectrometer colocated with "
            "PFISR. Measures airglow line emissions with high spectral "
            "resolution. Framework-specific search: query for data COINCIDENT "
            "in time with PFISR transmission pulses, looking for anomalous "
            "spectral lines (511 keV is in the X-ray band — NOT captured by "
            "optical Fabry-Perot — but visible-band anomalies consistent with "
            "pair-annihilation secondary products would appear here)."
        ),
    },
    "pfisr_allsky_fabry_perot": {
        "name": "Poker Flat all-sky scanning Fabry-Perot",
        "server": "eiscat",
        "code_hint": 5465,  # verified 2026-04-11
        "frequency_hz": 0.0,
        "coherent_elements": 0,
        "operational_since": 1990,
        "priority": 2,
        "instrument_type": "optical_fabry_perot",
        "framework_note": (
            "HIGH FRAMEWORK PRIORITY. All-sky scanning version covers wider "
            "spatial coverage than fixed Fabry-Perot. Use for framework "
            "coincidence search alongside PFISR."
        ),
    },
    "pfisr_photometer": {
        "name": "Poker Flat 4 Channel Filter Photometer",
        "server": "eiscat",
        "code_hint": 4470,  # verified 2026-04-11
        "frequency_hz": 0.0,
        "coherent_elements": 0,
        "operational_since": 1990,
        "priority": 3,
        "instrument_type": "optical_photometer",
        "framework_note": (
            "Filter photometer at Poker Flat. 4 optical channels. Colocated "
            "with PFISR for coincidence analysis. Lower spectral resolution "
            "than Fabry-Perot but higher time resolution and dynamic range."
        ),
    },
    "pfisr_lidar": {
        "name": "Poker Flat Lidar",
        "server": "eiscat",
        "code_hint": 6380,  # verified 2026-04-11
        "frequency_hz": 0.0,
        "coherent_elements": 0,
        "operational_since": 2000,
        "priority": 6,
        "instrument_type": "optical_lidar",
        "framework_note": (
            "Lidar at Poker Flat, measures atmospheric backscatter. Colocated "
            "with PFISR. Could detect anomalous plasma or particle density "
            "variations coincident with PFISR transmission events."
        ),
    },
    "risr_fabry_perot": {
        "name": "Resolute Bay Fabry-Perot",
        "server": "eiscat",
        "code_hint": 5535,  # verified 2026-04-11
        "frequency_hz": 0.0,
        "coherent_elements": 0,
        "operational_since": 2010,
        "priority": 3,
        "instrument_type": "optical_fabry_perot",
        "framework_note": (
            "Fabry-Perot at Resolute Bay, colocated with RISR-N and RISR-C. "
            "Framework coincidence search target."
        ),
    },
    "risr_michelson": {
        "name": "Resolute Bay Michelson Interferometer",
        "server": "eiscat",
        "code_hint": 5950,  # verified 2026-04-11
        "frequency_hz": 0.0,
        "coherent_elements": 0,
        "operational_since": 2010,
        "priority": 3,
        "instrument_type": "optical_interferometer",
        "framework_note": (
            "Michelson interferometer at Resolute Bay. Imaging + spectral "
            "data. Colocated with RISR-N/C for framework coincidence."
        ),
    },
    "millstone_fabry_perot": {
        "name": "Millstone Hill Fabry-Perot",
        "server": "millstone",
        "code_hint": 5340,  # verified 2026-04-11
        "frequency_hz": 0.0,
        "coherent_elements": 0,
        "operational_since": 1985,
        "priority": 6,
        "instrument_type": "optical_fabry_perot",
        "framework_note": (
            "Fabry-Perot at MIT Haystack, colocated with Millstone Hill ISR. "
            "Long operational record."
        ),
    },
    "millstone_allsky": {
        "name": "BU Millstone All-Sky Imager",
        "server": "millstone",
        "code_hint": 7200,  # verified 2026-04-11
        "frequency_hz": 0.0,
        "coherent_elements": 0,
        "operational_since": 1995,
        "priority": 6,
        "instrument_type": "optical_all_sky",
        "framework_note": (
            "Boston University all-sky imager colocated with Millstone Hill. "
            "Wide-angle optical coverage for coincidence analysis."
        ),
    },
}


# Tesla-Mack workshop pre-registered target frequency band (MHz, low-high)
# per session-74-tesla-mack-bells-workshop.md. The framework's Jensen resonance
# target is approximately 160 MHz with scaling exponent p uncertainty giving
# a search band of roughly 10-1000 MHz. This band is used by
# search_by_frequency() to flag facilities that operate near the target.
FRAMEWORK_FREQUENCY_BAND_HZ = (10e6, 1000e6)
FRAMEWORK_TARGET_HZ = 160e6
FRAMEWORK_TARGET_TOLERANCE = 0.5  # ±50% relative

# Published anomaly campaigns — instrument, approximate date, anomaly type,
# source citation. Use this to seed search_anomaly_campaigns() with known leads
# from session-74-rf-analysis.md Section III.
KNOWN_ANOMALY_CAMPAIGNS: list[dict[str, Any]] = [
    {
        "instrument": "eiscat_heating",
        "date_iso": "2012-10-19",
        "anomaly_type": "x_mode_optical_emission_unexplained",
        "frequency_hz": 7.1e6,
        "erp_mw": 430,
        "source": (
            "Blagoveshchenskaya et al., 'Optical and Ionospheric Phenomena at "
            "EISCAT under Continuous X-mode HF Pumping' (ResearchGate 268989066). "
            "The mechanism responsible for 630 nm and 557.7 nm emission "
            "enhancements during X-mode heating is NOT known. This is the "
            "highest-priority framework-relevant ionospheric-heater anomaly."
        ),
    },
    {
        "instrument": "arecibo_430",
        "date_iso": "2019-06-11",
        "date_iso_end": "2019-06-15",
        "anomaly_type": "anomalous_high_altitude_plasma_cavity",
        "frequency_hz": 5.125e6,
        "erp_mw": 100,  # placeholder, verify
        "source": (
            "Levine et al. 2020 (JGR Space Physics). Anomalous high-altitude "
            "plasma cavity formation during June 2019 Arecibo heating campaign. "
            "Described as 'anomalous' in the published literature."
        ),
    },
    {
        "instrument": "sura",
        "date_iso": "2021-09-05",
        "anomaly_type": "sporadic_E_557_emission_first_recording",
        "frequency_hz": 4.3e6,
        "erp_mw": 80,
        "source": (
            "Sura group (MDPI Atmosphere 2022). First recording of 557.7 nm "
            "emission at sporadic E-layer heights. Mechanism is STANDARD "
            "(O-mode airglow). Lower framework priority."
        ),
    },
]


@dataclass
class FrameworkInstrument:
    """Structured view of a framework-relevant instrument."""

    short_name: str
    name: str
    server: str
    code_hint: int | None
    instrument_type: str
    frequency_hz: float
    frequency_mhz: float
    coherent_elements: int
    operational_since: int
    priority: int
    is_in_framework_band: bool
    detuning_from_target: float
    framework_note: str

    @classmethod
    def from_table(cls, short_name: str, row: dict[str, Any]) -> "FrameworkInstrument":
        freq = float(row.get("frequency_hz") or 0.0)
        lo, hi = FRAMEWORK_FREQUENCY_BAND_HZ
        in_band = (lo <= freq <= hi) if freq > 0 else False
        detuning = (
            abs(freq - FRAMEWORK_TARGET_HZ) / FRAMEWORK_TARGET_HZ
            if freq > 0
            else 999.0
        )
        code_hint = row.get("code_hint")
        return cls(
            short_name=short_name,
            name=str(row.get("name", "")),
            server=str(row.get("server", "")),
            code_hint=int(code_hint) if code_hint is not None else None,
            instrument_type=str(row.get("instrument_type", "unknown")),
            frequency_hz=freq,
            frequency_mhz=freq / 1e6,
            coherent_elements=int(row.get("coherent_elements", 0) or 0),
            operational_since=int(row.get("operational_since", 0) or 0),
            priority=int(row.get("priority", 99) or 99),
            is_in_framework_band=in_band,
            detuning_from_target=detuning,
            framework_note=str(row.get("framework_note", "")),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "short_name": self.short_name,
            "name": self.name,
            "server": self.server,
            "code_hint": self.code_hint,
            "instrument_type": self.instrument_type,
            "frequency_hz": self.frequency_hz,
            "frequency_mhz": self.frequency_mhz,
            "coherent_elements": self.coherent_elements,
            "operational_since": self.operational_since,
            "priority": self.priority,
            "is_in_framework_band": self.is_in_framework_band,
            "detuning_from_target": self.detuning_from_target,
            "framework_note": self.framework_note,
        }


class FrameworkSearch:
    """Framework-specific retrospective-search helpers."""

    def __init__(self, client: MadrigalClient):
        self.client = client

    def list_framework_instruments(self) -> list[dict[str, Any]]:
        """
        List all framework-relevant instruments with their priority and
        detuning from the Tesla-Mack predicted Jensen resonance target.

        Sorted by priority (ascending, 1 = highest).
        """
        rows = [
            FrameworkInstrument.from_table(name, row).to_dict()
            for name, row in FRAMEWORK_INSTRUMENTS.items()
        ]
        rows.sort(key=lambda r: r["priority"])
        return rows

    def search_by_frequency(
        self, freq_min_hz: float, freq_max_hz: float
    ) -> list[dict[str, Any]]:
        """
        Return framework-relevant instruments whose operating frequency falls
        within [freq_min_hz, freq_max_hz]. Useful for finding retrospective
        targets once the Jensen resonance frequency is narrowed.
        """
        rows = []
        for name, row in FRAMEWORK_INSTRUMENTS.items():
            freq = float(row.get("frequency_hz") or 0.0)
            if freq_min_hz <= freq <= freq_max_hz:
                rows.append(FrameworkInstrument.from_table(name, row).to_dict())
        rows.sort(key=lambda r: r["priority"])
        return rows

    def list_anomaly_campaigns(
        self, instrument: str | None = None
    ) -> list[dict[str, Any]]:
        """
        Return the table of published anomaly campaigns that are
        framework-relevant. Optionally filter by instrument short name.
        """
        if instrument is None:
            return list(KNOWN_ANOMALY_CAMPAIGNS)
        return [
            row for row in KNOWN_ANOMALY_CAMPAIGNS
            if row.get("instrument") == instrument
        ]

    def describe_framework_target(self) -> dict[str, Any]:
        """
        Return the framework's current target parameters for reference.
        Useful as a single-call tool that gives the LLM the context it needs
        to decide which historical campaigns are framework-relevant.
        """
        return {
            "target_frequency_hz": FRAMEWORK_TARGET_HZ,
            "target_frequency_mhz": FRAMEWORK_TARGET_HZ / 1e6,
            "frequency_band_hz": list(FRAMEWORK_FREQUENCY_BAND_HZ),
            "frequency_band_mhz": [
                f / 1e6 for f in FRAMEWORK_FREQUENCY_BAND_HZ
            ],
            "target_tolerance_relative": FRAMEWORK_TARGET_TOLERANCE,
            "framework_source": (
                "sessions/session-74/session-74-tesla-mack-bells-workshop.md "
                "Tesla T4 pre-registered frequency; sessions/framework/"
                "Phononic-C-Causality.md §3, §8"
            ),
            "notes": (
                "Target is the Leggett-channel Jensen resonance at approximately "
                "160 MHz in lab-redshifted units, with wide uncertainty (10-1000 "
                "MHz plausible band) pending OQ-TESLA-T1 and OQ-TESLA-T4 gate "
                "computations. Any facility operating within ±50% of 160 MHz is "
                "a Tier-1 retrospective target."
            ),
        }
