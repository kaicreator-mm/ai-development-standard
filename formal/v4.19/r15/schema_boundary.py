"""ADS #1366 R15: exact candidate Schema bytes -> syntax-only Dispatch evidence.

No output from this module authorizes a canonical Dispatch, Claim or READY write.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.test_protocol_schemas import assert_supported_schema, validate_subset  # noqa: E402

CANDIDATE_SOURCE_HEAD = "dac263fa4c0ab155406d2f2117459b34322cc988"
PINNED_SCHEMA_BLOB = "5d9233b6b881d9d92f66fc6cd5307a05a0fdbe2f"


def git_blob(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def assess(schema_bytes: bytes, dispatch: object, *, expected_blob: str = PINNED_SCHEMA_BLOB) -> dict:
    """Fail closed on source drift. Shape validity is never publication authority."""
    observed = git_blob(schema_bytes)
    result = {
        "schema": "ads/formal-r15-dispatch-schema-boundary/v1",
        "candidate_source_head": CANDIDATE_SOURCE_HEAD,
        "expected_schema_blob": expected_blob,
        "observed_schema_blob": observed,
        "source_binding": "BLOCK",
        "shape_status": "NOT_RUN",
        "canonical_admission": "NOT_PROVEN",
        "publication_authorized": False,
        "diagnostics": [],
    }
    if observed != expected_blob:
        result["diagnostics"] = ["SCHEMA_BLOB_MISMATCH"]
        return result
    try:
        schema = json.loads(schema_bytes)
        if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
            raise ValueError("unexpected schema dialect")
        assert_supported_schema(schema)
    except (ValueError, UnicodeDecodeError, TypeError) as exc:
        result["diagnostics"] = ["SCHEMA_UNSUPPORTED_OR_INVALID", str(exc)]
        return result
    result["source_binding"] = "EXACT_BLOB_PASS"
    errors = validate_subset(dispatch, schema)
    result["shape_status"] = "SHAPE_VALID_ONLY" if not errors else "INVALID_SCHEMA"
    result["diagnostics"] = errors
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Candidate schema syntax check, never canonical admission")
    parser.add_argument("--schema", type=Path, required=True)
    parser.add_argument("--dispatch", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        schema_bytes = args.schema.read_bytes()
        dispatch = json.loads(args.dispatch.read_text(encoding="utf-8"))
        output = assess(schema_bytes, dispatch)
    except (OSError, UnicodeDecodeError, ValueError) as exc:
        output = {"schema": "ads/formal-r15-dispatch-schema-boundary/v1",
                  "source_binding": "BLOCK", "shape_status": "NOT_RUN",
                  "canonical_admission": "NOT_PROVEN", "publication_authorized": False,
                  "diagnostics": ["INPUT_INVALID_OR_UNREADABLE", str(exc)]}
    print(json.dumps(output, indent=2, sort_keys=True))
    return 0 if output.get("source_binding") == "EXACT_BLOB_PASS" and output.get("shape_status") == "SHAPE_VALID_ONLY" else 2


if __name__ == "__main__":
    raise SystemExit(main())
