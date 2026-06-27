#!/usr/bin/env python3
"""
S{{SESSION}} {{WAVE}}-{{GATE_ID}} -- {{SHORT_DESCRIPTION}}
========================================================

Gate: {{GATE_ID}} ({{TRIGGER}})
  Trigger options: [SIGN] | [VERIFY] | [AUDIT] | [VERIFY-THEOREM] | [CHAIN]

Pre-registered threshold:
  {{PASS_CRITERION}}
  PASS iff {{CONDITION}}, FAIL iff {{CONDITION_NEG}}, INFO otherwise.

Inputs (SHA-256 dual-pinned at runtime -- see Section 4):
  - {{INPUT_FILE_1}}
  - {{INPUT_FILE_2}}
  - canonical_constants.py (feeds the closure SHA only)
  - script bytes (feeds BOTH the closure SHA and the script-only SHA)

Output 4-tuple:
  (value=<computed>, scheme={{SCHEME}}, convention={{CONVENTION}}, L_max={{L_MAX}})

Classification: {{PROJECT CLASSIFICATION TAG}}

METHODOLOGY
-----------
{{ONE-PARAGRAPH DESCRIPTION OF METHOD; cite prior sessions/gates/theorems.}}

DISCIPLINE
----------
- `from canonical_constants import *`  (the project's canonical-constants module)
- Every local/intermediate tagged `# (local)`
- GPU path via `torch.linalg` for matrices >= 100x100 (see computation-environment.md)
- SHA-256 of all input files logged in the first 20 lines of stdout
- content_sha256 (closure) + script_sha256 (script-only) emitted
- 4-tuple printed as the final non-verdict line
- Gate verdict emitted via the `emit_verdict` knowledge-MCP tool (race-safe;
  per .claude/rules/gate-verdicts.md): the script PRINTS the payload
  (print_verdict_payload); the dispatching AGENT reads it and calls
  mcp__knowledge__emit_verdict(**payload). The script does NOT write the verdict
  file directly -- a raw open("a") append is NOT atomic across processes on
  Windows (concurrent appenders lose lines).
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Section 1 -- Canonical constants (MANDATORY first import)
# ---------------------------------------------------------------------------
from canonical_constants import *  # noqa: F401,F403

# ---------------------------------------------------------------------------
# Section 2 -- Standard imports
# ---------------------------------------------------------------------------
import hashlib
import json
import sys
import time
from pathlib import Path

# Numerical -- uncomment as needed. torch.linalg PREFERRED for N >= 100.
# import numpy as np
# import torch

# ---------------------------------------------------------------------------
# Section 3 -- Paths + pre-registration
# ---------------------------------------------------------------------------
# Scripts live at {{COMPUTATION_DIR}}/session-N/. SESSION_DIR is this script's
# parent; COMPUTATIONS_DIR is its parent; SHARED_DIR holds canonical_constants.py.
SESSION_DIR = Path(__file__).resolve().parent
COMPUTATIONS_DIR = SESSION_DIR.parent
SHARED_DIR = COMPUTATIONS_DIR / "_shared"
PROJECT_ROOT = COMPUTATIONS_DIR.parent

SESSION = "S{{SESSION}}"                                           # (local)
GATE_ID = "{{GATE_ID}}"                                            # (local)
SCHEME = "{{SCHEME}}"                                              # (local)
CONVENTION = "{{CONVENTION}}"                                      # (local)
L_MAX = {{L_MAX}}                                                  # (local)

# Pre-registered pass/fail threshold (define BEFORE running)
PASS_THRESHOLD = {{THRESHOLD_VALUE}}                               # (local)
N_EVAL = {{N_EVAL}}                                                # (local)
SCAN_MIN = {{SCAN_MIN}}                                            # (local)
SCAN_MAX = {{SCAN_MAX}}                                            # (local)

# Output destinations (per-session)
OUT_NPZ = SESSION_DIR / f"s{{SESSION}}_{{GATE_ID_LOWER}}_results.npz"
OUT_PNG = SESSION_DIR / f"s{{SESSION}}_{{GATE_ID_LOWER}}.png"
# The verdict file is written by the emit_verdict MCP tool -- NOT this script.

INPUT_FILES = [
    SHARED_DIR / "canonical_constants.py",
    # SESSION_DIR / "{{OTHER_INPUT_NPZ}}",
]


# ---------------------------------------------------------------------------
# Section 4 -- SHA-256 input-pin block (MANDATORY; first 20 lines of stdout)
#
# DUAL-SHA SCHEMA:
#   content_sha256 = sha256( bytes(script) || bytes(canonical) || bytes(pinmap_json) )
#                    -- the full pinned-input closure; the SHA the verdict line pins.
#   script_sha256  = sha256( bytes(script) )
#                    -- script-only; responds to code edits, invariant under
#                       canonical / pinmap change.
#
# Canonical verdict line:
#   {GATE}: PASS|FAIL|INFO -- value=<v> scheme=<s> convention=<c> L_max=<L>
#     content_sha256=<64> script_sha256=<64>
# ---------------------------------------------------------------------------

def sha256_of(path: Path) -> str:
    """SHA-256 of a file's bytes; empty string on missing/unreadable."""
    h = hashlib.sha256()  # (local)
    try:
        h.update(path.read_bytes())
    except OSError:
        return ""
    return h.hexdigest()


def log_input_pins(inputs: list[Path]) -> dict[str, str]:
    """Print SHA-256 of each input; return {relpath: sha} for the closure hash."""
    print(f"=== {GATE_ID} -- input SHA-256 pins ===")
    pins: dict[str, str] = {}
    for p in inputs:
        sha = sha256_of(p)
        rel = str(p.relative_to(PROJECT_ROOT)).replace("\\", "/")
        print(f"  {rel}: {sha[:16]}...")
        pins[rel] = sha
    return pins


def compute_dual_sha(
    script_path: Path,
    canonical_path: Path,
    pins: dict[str, str],
) -> tuple[str, str]:
    """Compute (content_sha256, script_sha256).

    content_sha256:
        sha256( bytes(script) || bytes(canonical_constants.py) || pinmap_json )
        where pinmap_json is the canonical (sorted, compact) JSON serialization
        of `pins` (the {relpath: sha256} map). This is the closure SHA.

    script_sha256:
        sha256( bytes(script) ) -- responds to script edits only.
    """
    script_bytes = b""  # (local)
    try:
        script_bytes = script_path.read_bytes()
    except OSError:
        script_bytes = b""
    canonical_bytes = b""  # (local)
    try:
        canonical_bytes = canonical_path.read_bytes()
    except OSError:
        canonical_bytes = b""
    pinmap_json = json.dumps(
        dict(sorted(pins.items())),
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")  # (local)

    h_content = hashlib.sha256()
    h_content.update(script_bytes)
    h_content.update(canonical_bytes)
    h_content.update(pinmap_json)
    content = h_content.hexdigest()  # (local)

    h_script = hashlib.sha256()
    h_script.update(script_bytes)
    script = h_script.hexdigest()  # (local)

    return content, script


# ---------------------------------------------------------------------------
# Section 5 -- Compute
# ---------------------------------------------------------------------------

def compute() -> dict:
    """Main computation. Return a dict with 'value' and any cross-check fields.

    All internal intermediates MUST be tagged `# (local)`.
    """
    # Example:
    #     result = some_canonical * some_other_canonical   # framework-valid
    #     ratio = result / SOME_CANONICAL                  # (local)
    raise NotImplementedError("Replace this body with the computation.")


# ---------------------------------------------------------------------------
# Section 6 -- Gate verdict + 4-tuple output
# ---------------------------------------------------------------------------

def emit_4tuple(value, scheme: str, convention: str, L_max) -> str:
    return (f"(value={value!r}, scheme={scheme}, "
            f"convention={convention}, L_max={L_max})")


def print_verdict_payload(
    verdict: str,
    value,
    content_sha: str,
    script_sha: str,
    threshold="{{THRESHOLD_VALUE}}",
    track: str = "session",
    sign_verdict: str | None = None,
    magnitude_verdict: str | None = None,
    regime_verdict: str | None = None,
    supersedes: str | None = None,
    extra_rows: list[str] | None = None,
) -> dict:
    """Print the verdict PAYLOAD for the dispatching AGENT to pass to the
    knowledge-MCP `emit_verdict` tool.

    The script does NOT write the verdict file -- that single, lock-serialized
    write is owned by `emit_verdict` (per .claude/rules/gate-verdicts.md). The
    script still computes the two SHAs (it alone holds the input-pin map); the
    agent reads the delimited JSON block below from stdout and calls
    mcp__knowledge__emit_verdict(**payload).

    For [SIGN]-trigger gates, pass ALL THREE of sign/magnitude/regime_verdict.
    `value` is the RAW payload string (no surrounding quotes). `supersedes` is
    the 64-hex of a prior line this one corrects (Option-A; see gate-verdicts.md).
    """
    payload: dict = {
        "gate_id": GATE_ID,
        "session": int(SESSION.lstrip("Ss")),
        "value": str(value),
        "verdict": verdict,
        "threshold": str(threshold),
        "content_sha256": content_sha,
        "script_sha256": script_sha,
        "source_file": str(Path(__file__).name),
        "track": track,
        # physics provenance carried into the verdict line:
        "scheme": SCHEME,
        "convention": CONVENTION,
        "l_max": str(L_MAX),
    }
    if supersedes:
        payload["supersedes"] = supersedes
    if not (sign_verdict is None and magnitude_verdict is None and regime_verdict is None):
        payload["sign_verdict"] = sign_verdict
        payload["magnitude_verdict"] = magnitude_verdict
        payload["regime_verdict"] = regime_verdict
    if extra_rows:
        payload["extra_rows"] = list(extra_rows)
    # Delimited so the agent can extract it deterministically from stdout.
    print("<<<EMIT_VERDICT_PAYLOAD>>>")
    print(json.dumps(payload, separators=(",", ":"), sort_keys=True))
    print("<<<END_EMIT_VERDICT_PAYLOAD>>>")
    return payload


def evaluate_gate(value) -> str:
    """Compare computed value to the pre-registered threshold; return PASS/FAIL/INFO."""
    # Replace this with the actual gate rule. Example for |value| <= PASS_THRESHOLD:
    #     if value <= PASS_THRESHOLD:
    #         return "PASS"
    #     if value > PASS_THRESHOLD * 10:
    #         return "FAIL"
    #     return "INFO"
    raise NotImplementedError("Define the gate rule before running.")


# ---------------------------------------------------------------------------
# Section 7 -- Main
# ---------------------------------------------------------------------------

def main() -> int:
    t0 = time.time()  # (local)

    # 1. Log input pins (first 20 lines of stdout)
    pins = log_input_pins(INPUT_FILES)

    # 1b. Compute the two SHAs
    script_path = Path(__file__).resolve()  # (local)
    canonical_path = SHARED_DIR / "canonical_constants.py"  # (local)
    content_sha, script_sha = compute_dual_sha(script_path, canonical_path, pins)
    print(f"  content_sha256: {content_sha[:16]}... (closure: script+canonical+pinmap)")
    print(f"  script_sha256:  {script_sha[:16]}... (script only)")
    print()

    # 2. Compute
    result = compute()
    value = result["value"]

    # 3. Evaluate gate
    verdict = evaluate_gate(value)

    # 4. Emit 4-tuple + PRINT the emit_verdict payload. The dispatching agent
    #    reads the delimited JSON block and calls mcp__knowledge__emit_verdict.
    #    For [SIGN] gates, also pass sign_verdict/magnitude_verdict/regime_verdict.
    tag = emit_4tuple(value, SCHEME, CONVENTION, L_MAX)
    print(tag)
    print_verdict_payload(verdict, value, content_sha, script_sha)

    # 5. Final summary
    wall = time.time() - t0  # (local)
    print(f"\n=== {GATE_ID}: {verdict} (wall {wall:.1f}s) ===")
    # Exit 0 regardless of PASS/FAIL/INFO; non-zero is reserved for breakage.
    return 0


if __name__ == "__main__":
    sys.exit(main())
