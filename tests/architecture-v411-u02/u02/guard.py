"""Schema guard for U02 event payloads.

Reuses the repository's own event-v2 validator (real source/lineage
association, not a re-implementation): the minimal read-only validator in
``scripts/test_v48_execution_ownership.py`` together with the checked-in
``schemas/agent-event-v2.schema.json``.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def _load_v48_validator():
    target = ROOT / "scripts" / "test_v48_execution_ownership.py"
    spec = importlib.util.spec_from_file_location("ads_v48_oracle", target)
    if spec is None or spec.loader is None:  # pragma: no cover - environment
        raise RuntimeError(f"cannot load validator module: {target}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


_V48 = _load_v48_validator()


def load_schema() -> dict:
    return _V48.load_event_schema()


def validate_event(payload: dict) -> list[str]:
    """Return schema/enum/conditional violations; empty list means valid."""
    return _V48.validate_event_payload(load_schema(), payload)
