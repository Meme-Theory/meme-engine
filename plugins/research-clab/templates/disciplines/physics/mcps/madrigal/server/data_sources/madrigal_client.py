"""
Madrigal Client — thin wrapper around madrigalWeb.

Provides a consistent interface to any Madrigal database instance, with
connection pooling and error handling suitable for an MCP tool server.

Known Madrigal servers:
- CEDAR (primary): http://cedar.openmadrigal.org
- EISCAT: https://madrigal.eiscat.se/madrigal
- Millstone Hill: http://madrigal.haystack.mit.edu/madrigal
- Jicamarca: http://jro1.igp.gob.pe/madrigal
- Arecibo (historical): http://madrigal.naic.edu/madrigal
- SRI (Poker Flat/Resolute Bay): http://isr.sri.com/madrigal
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any

logger = logging.getLogger(__name__)

# Lazy-import madrigalWeb so the module loads even if the package is missing.
try:
    from madrigalWeb.madrigalWeb import MadrigalData  # type: ignore
    _MADRIGAL_AVAILABLE = True
except ImportError:
    MadrigalData = None  # type: ignore
    _MADRIGAL_AVAILABLE = False


# Canonical list of public Madrigal servers relevant to the framework
# retrospective-analysis program. Each entry is (short_name, display_name, url).
KNOWN_SERVERS: dict[str, tuple[str, str]] = {
    "cedar": (
        "CEDAR Madrigal (primary distributed DB)",
        "http://cedar.openmadrigal.org",
    ),
    "eiscat": (
        "EISCAT Madrigal (Tromso, Sodankyla, Kiruna, Svalbard, EISCAT_3D)",
        "https://madrigal.eiscat.se/madrigal",
    ),
    "millstone": (
        "Millstone Hill (MIT Haystack)",
        "http://madrigal.haystack.mit.edu/madrigal",
    ),
    "jicamarca": (
        "Jicamarca Radio Observatory (Peru)",
        "http://jro1.igp.gob.pe/madrigal",
    ),
    "arecibo": (
        "Arecibo (historical, decommissioned 2020)",
        "http://madrigal.naic.edu/madrigal",
    ),
    "sri": (
        "SRI (Poker Flat AMISR, Resolute Bay AMISR)",
        "http://isr.sri.com/madrigal",
    ),
}


def _safe_int(value: Any, default: int = 0) -> int:
    """Convert to int if possible, otherwise return default."""
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _safe_float(value: Any, default: float = 0.0) -> float:
    """Convert to float if possible, otherwise return default."""
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


@dataclass
class Instrument:
    """Simplified view of a Madrigal instrument record."""

    code: int
    name: str
    mnemonic: str
    latitude: float
    longitude: float
    altitude: float
    category: str  # Madrigal returns a textual category name, not an int
    contact_name: str
    contact_email: str

    @classmethod
    def from_madrigal(cls, row: Any) -> "Instrument":
        """Construct from a madrigalWeb MadrigalInstrument object."""
        return cls(
            code=_safe_int(getattr(row, "code", 0)),
            name=str(getattr(row, "name", "") or ""),
            mnemonic=str(getattr(row, "mnemonic", "") or ""),
            latitude=_safe_float(getattr(row, "latitude", 0.0)),
            longitude=_safe_float(getattr(row, "longitude", 0.0)),
            altitude=_safe_float(getattr(row, "altitude", 0.0)),
            category=str(getattr(row, "category", "") or ""),
            contact_name=str(getattr(row, "contactName", "") or ""),
            contact_email=str(getattr(row, "contactEmail", "") or ""),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "code": self.code,
            "name": self.name,
            "mnemonic": self.mnemonic,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "altitude": self.altitude,
            "category": self.category,
            "contact_name": self.contact_name,
            "contact_email": self.contact_email,
        }


@dataclass
class Experiment:
    """Simplified view of a Madrigal experiment record."""

    id: int
    instrument_code: int
    instrument_name: str
    start_iso: str
    end_iso: str
    pi_name: str
    pi_email: str
    site_name: str
    url: str

    @classmethod
    def from_madrigal(cls, row: Any) -> "Experiment":
        # Madrigal exposes a parsed datetime object for start/end in some API
        # versions and a tuple in others. Handle both defensively.
        def _iso(dt: Any) -> str:
            try:
                return dt.isoformat() if hasattr(dt, "isoformat") else str(dt)
            except Exception:
                return str(dt)

        return cls(
            id=_safe_int(getattr(row, "id", 0)),
            instrument_code=_safe_int(getattr(row, "instcode", 0)),
            instrument_name=str(getattr(row, "instname", "") or ""),
            start_iso=_iso(getattr(row, "startdatetime", "")),
            end_iso=_iso(getattr(row, "enddatetime", "")),
            pi_name=str(getattr(row, "pi", "") or ""),
            pi_email=str(getattr(row, "piEmail", "") or ""),
            site_name=str(getattr(row, "sitename", "") or ""),
            url=str(getattr(row, "url", "") or ""),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "instrument_code": self.instrument_code,
            "instrument_name": self.instrument_name,
            "start": self.start_iso,
            "end": self.end_iso,
            "pi_name": self.pi_name,
            "pi_email": self.pi_email,
            "site_name": self.site_name,
            "url": self.url,
        }


class MadrigalClient:
    """Thin wrapper around madrigalWeb.MadrigalData with connection caching."""

    def __init__(
        self,
        user_name: str = "phonon-exflation",
        user_email: str = "phonon-exflation@localhost",
        user_affiliation: str = "Phonon-Exflation Cosmology Project",
    ):
        if not _MADRIGAL_AVAILABLE:
            raise ImportError(
                "madrigalWeb is not installed. "
                "Run: py -3.13 -m pip install madrigalWeb"
            )
        self.user_name = user_name
        self.user_email = user_email
        self.user_affiliation = user_affiliation
        self._connections: dict[str, Any] = {}

    def get_connection(self, server: str) -> Any:
        """Get or create a MadrigalData connection for the given server."""
        if server in self._connections:
            return self._connections[server]

        # Allow either a short name (e.g. "eiscat") or a full URL.
        if server in KNOWN_SERVERS:
            url = KNOWN_SERVERS[server][1]
        else:
            url = server

        try:
            conn = MadrigalData(url)
            self._connections[server] = conn
            logger.info("Connected to Madrigal server: %s (%s)", server, url)
            return conn
        except Exception as exc:
            logger.error("Failed to connect to %s: %s", server, exc)
            raise

    def list_known_servers(self) -> list[dict[str, str]]:
        """Return the canonical KNOWN_SERVERS table as dicts."""
        return [
            {"short_name": short, "display_name": display, "url": url}
            for short, (display, url) in KNOWN_SERVERS.items()
        ]

    def list_instruments(self, server: str) -> list[dict[str, Any]]:
        """List all instruments at the given Madrigal server."""
        conn = self.get_connection(server)
        try:
            rows = conn.getAllInstruments()
        except Exception as exc:
            logger.error("list_instruments failed on %s: %s", server, exc)
            raise
        return [Instrument.from_madrigal(row).to_dict() for row in rows]

    def list_experiments(
        self,
        server: str,
        instrument_code: int,
        start_year: int,
        start_month: int,
        start_day: int,
        end_year: int,
        end_month: int,
        end_day: int,
    ) -> list[dict[str, Any]]:
        """List experiments for an instrument in a date range."""
        conn = self.get_connection(server)
        try:
            rows = conn.getExperiments(
                instrument_code,
                start_year, start_month, start_day, 0, 0, 0,
                end_year, end_month, end_day, 23, 59, 59,
            )
        except Exception as exc:
            logger.error("list_experiments failed: %s", exc)
            raise
        return [Experiment.from_madrigal(row).to_dict() for row in rows]

    def list_experiment_files(
        self, server: str, experiment_id: int
    ) -> list[dict[str, Any]]:
        """List files (data products) for a given experiment."""
        conn = self.get_connection(server)
        try:
            rows = conn.getExperimentFiles(experiment_id)
        except Exception as exc:
            logger.error("list_experiment_files failed: %s", exc)
            raise
        out: list[dict[str, Any]] = []
        for row in rows:
            out.append({
                "name": str(getattr(row, "name", "") or ""),
                "kindat": int(getattr(row, "kindat", 0) or 0),
                "kindat_desc": str(getattr(row, "kindatdesc", "") or ""),
                "category": int(getattr(row, "category", 0) or 0),
                "status": str(getattr(row, "status", "") or ""),
                "permission": int(getattr(row, "permission", 0) or 0),
                "expId": int(getattr(row, "expId", 0) or 0),
            })
        return out

    def list_parameters(
        self, server: str, file_name: str
    ) -> list[dict[str, Any]]:
        """List the parameters (columns) available in a specific Madrigal file."""
        conn = self.get_connection(server)
        try:
            rows = conn.getExperimentFileParameters(file_name)
        except Exception as exc:
            logger.error("list_parameters failed: %s", exc)
            raise
        out: list[dict[str, Any]] = []
        for row in rows:
            out.append({
                "mnemonic": str(getattr(row, "mnemonic", "") or ""),
                "description": str(getattr(row, "description", "") or ""),
                "is_error": bool(getattr(row, "isError", False)),
                "units": str(getattr(row, "units", "") or ""),
                "is_measured": bool(getattr(row, "isMeasured", False)),
                "category": str(getattr(row, "category", "") or ""),
            })
        return out

    def download_file(
        self,
        server: str,
        file_name: str,
        dest_path: str,
        file_format: str = "hdf5",
    ) -> str:
        """
        Download a Madrigal file to local disk.

        file_format: one of "hdf5", "netCDF4", "ascii"
        """
        conn = self.get_connection(server)
        try:
            conn.downloadFile(
                file_name,
                dest_path,
                self.user_name,
                self.user_email,
                self.user_affiliation,
                file_format,
            )
        except Exception as exc:
            logger.error("download_file failed: %s", exc)
            raise
        return dest_path

    def isprint_filter(
        self,
        server: str,
        file_name: str,
        parameters: list[str],
        filters: list[str] | None = None,
        header: str = "t",
    ) -> str:
        """
        Run the Madrigal isprint command with parameter selection and filters.

        parameters: list of parameter mnemonics to extract, e.g. ["ut1_unix", "nel"]
        filters: list of filter strings, e.g. ["gdalt,200,500"] (altitude 200-500 km)
        header: 't' to include header, 'f' to exclude
        """
        conn = self.get_connection(server)
        try:
            result = conn.isprint(
                file_name,
                ",".join(parameters),
                ",".join(filters or []),
                self.user_name,
                self.user_email,
                self.user_affiliation,
                header=header,
            )
        except Exception as exc:
            logger.error("isprint_filter failed: %s", exc)
            raise
        return str(result)
