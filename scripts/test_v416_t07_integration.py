#!/usr/bin/env python3
"""ADS v4.16 T07: real local source-suite composition, not a release authority.

Run at a detached exact SHA. A green run is SOURCE_CONFORMANCE_PASS_ONLY.
No provider invoice, native GitHub ACL, full Host E2E or Release Gate is inferred.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "tests/fixtures/v416/t07/integration_manifest.json"
GROUPS = {*(f"C{i:02}" for i in range(1, 17)), "A03",
          *(f"G{i:02}" for i in range(9, 13))}
REQUIRED_TASK_SUITES = {f"T{i:02}" for i in range(1, 7)}
LEGACY_SUITES = {"LEGACY_INTERACTION", "LEGACY_REPORT",
                 "LEGACY_CONSUMER", "LEGACY_INTEGRATION", "PROTO_SCHEMAS"}
SOURCE_ONLY_RESULT = "SOURCE_CONFORMANCE_PASS_ONLY"



# Frozen owner identities independently checked, never adopted from editable manifest.
EXPECTED_SUITES = {"T01":["scripts/test_v416_t01_report_schema.py","tests/fixtures/v416/t01/scenarios.json"],"T02":["scripts/test_v416_t02_measurement.py","tests/fixtures/v416/t02/scenarios.json"],"T03":["scripts/test_v416_t03_reader.py","tests/fixtures/v416/t03/compatibility_matrix.json"],"T04":["scripts/test_v416_t04_evolution.py","tests/fixtures/v416/t04/scenarios.json"],"T05":["scripts/test_v416_t05_writeback.py","tests/fixtures/v416/t05/scenarios.json"],"T06":["scripts/test_v416_t06_agent_governance.py","tests/fixtures/v416/t06/scenarios.json"],"LEGACY_INTERACTION":["scripts/test_github_structured_interaction.py",None],"LEGACY_REPORT":["tests/test_v415_report.py",None],"LEGACY_CONSUMER":["tests/test_v415_consumer.py",None],"LEGACY_INTEGRATION":["tests/test_v415_contract_integration.py",None],"PROTO_SCHEMAS":["scripts/test_protocol_schemas.py",None]}
EXPECTED_GROUPS = {"C01":["T01","T03"],"C02":["T02"],"C03":["T02"],"C04":["T02"],"C05":["T02"],"C06":["T01","T03"],"C07":["T01","T03"],"C08":["T01","T03"],"C09":["T01","T03"],"C10":["T01"],"C11":["T04"],"C12":["T02"],"C13":["T04"],"C14":["T04"],"C15":["T05"],"C16":["T05"],"A03":["T06"],"G09":["T06"],"G10":["T06"],"G11":["T06"],"G12":["T06"]}
EXPECTED_SCHEMA_PINS = {"schemas/github/v4.14/structured-interaction.schema.json":"a8c5d852c239f69850e7d856af75ca8179aff1dd","schemas/github/v4.15/report.schema.json":"88c96dda7f8bcaabe1766a807599ed15bbeae2de","schemas/github/v4.16/report.schema.json":"7478313cc006162432649d734e59c5cd77db5106"}

class QualificationError(Exception):
    pass


def git(*args: str) -> str:
    proc = subprocess.run(["git", *args], cwd=ROOT, text=True,
                          encoding="utf-8", errors="replace", capture_output=True,
                          check=False)
    if proc.returncode:
        raise QualificationError(f"git {args[0]} failed ({proc.returncode}): {proc.stderr[:400]}")
    return proc.stdout.strip()


def load_and_check_manifest(candidate: dict | None = None) -> dict:
    m = candidate if candidate is not None else json.loads(MANIFEST.read_text(encoding="utf-8"))
    if m.get("schema") != "ads/v416-t07-integrated-source-closure/v1":
        raise QualificationError("Unknown closure manifest format")
    if m.get("scope") != "standards-source-only" or m.get("owned_task") != "#1271":
        raise QualificationError("Manifest scope or owner changed")
    groups = m.get("groups")
    if not isinstance(groups, dict) or set(groups) != GROUPS:
        raise QualificationError("C01-C16/A03/G09-G12 groups missing or unexpected")
    suites = m.get("suites")
    if not isinstance(suites, list):
        raise QualificationError("Suite list missing")
    ids = [s.get("id") for s in suites]
    if len(ids) != len(set(ids)) or set(ids) != REQUIRED_TASK_SUITES | LEGACY_SUITES:
        raise QualificationError("All six sources and five historical suites required")
    for suite in suites:
        if [suite.get("command"), suite.get("artifact")] != EXPECTED_SUITES[suite["id"]]:
            raise QualificationError(f"Suite ID/command/fixture mismatch: {suite['id']}")
        command = suite.get("command")
        if not isinstance(command, str) or not command.endswith(".py") or command.startswith("/"):
            raise QualificationError("Unsafe suite path")
        if ".." in Path(command).parts or not command.startswith(("scripts/", "tests/")):
            raise QualificationError("Out-of-scope suite path")
        if not (ROOT / command).is_file():
            raise QualificationError(f"Missing executable {command}")
        if "artifact" in suite and not (ROOT / suite["artifact"]).is_file():
            raise QualificationError(f"Missing fixture {suite['artifact']}")
    if groups != EXPECTED_GROUPS:
        raise QualificationError("Canonical 21 group ownership map mismatch")
    pinned = m.get("schema_pins")
    if not isinstance(pinned, dict) or pinned != EXPECTED_SCHEMA_PINS:
        raise QualificationError("Frozen v3/v4/v5 schema pins missing")
    for file, want in pinned.items():
        path = ROOT / file
        if not path.is_file() or not re.fullmatch(r"[0-9a-f]{40}", want):
            raise QualificationError(f"Invalid schema path/pin {file}")
        got = git("hash-object", str(path))
        if got != want:
            raise QualificationError(f"SCHEMA_BLOB_DRIFT {file}: {got} != {want}")
    required_gates = {"FULL_REGRESSION", "HIDDEN_VALIDATION",
                      "CRITICAL_JOURNEYS", "PACKAGING", "INDEPENDENT_REVIEW",
                      "RELEASE_QUALIFICATION", "MAIN_MERGE", "TAG"}
    if set(m.get("release_gates", [])) != required_gates:
        raise QualificationError("Release gate inventory incomplete")
    required_external = {"#1210", "#1231", "REAL_TASKMETA_GITHUB_TALLY_E2E",
                         "REAL_CONTROLLER_HOST_DEMO", "AUTHENTICATED_PROVIDER_CLOCK_AND_BILLING",
                         "GITHUB_NATIVE_PUBLISHER_ACL"}
    if set(m.get("external_not_run", [])) != required_external:
        raise QualificationError("External NOT_RUN inventory incomplete")
    return m


def git_clean() -> bool:
    return not git("status", "--porcelain")


def run_all(m: dict, *, expected_sha: str, timeout: int) -> dict:
    if not re.fullmatch(r"[0-9a-f]{40}", expected_sha):
        raise QualificationError("--expected-sha must be immutable 40-digit SHA")
    actual = git("rev-parse", "HEAD")
    if actual != expected_sha:
        raise QualificationError(f"HEAD_DRIFT: {actual} != {expected_sha}")
    if not git_clean():
        raise QualificationError("Dirty source checkout: cannot qualify")
    details = []
    for suite in m["suites"]:
        cmd = [sys.executable, suite["command"]]
        try:
            proc = subprocess.run(cmd, cwd=ROOT, capture_output=True,
                                  encoding="utf-8", errors="replace",
                                  check=False, timeout=timeout)
            combined = proc.stdout + "\n" + proc.stderr
            counts = re.findall(r"Ran\s+(\d+)\s+tests?\s+in", combined)
            count = int(counts[-1]) if counts else None
            passed = proc.returncode == 0 and count is not None and count > 0
            row = {"id": suite["id"], "command": cmd[1],
                   "exit": proc.returncode, "unittest_count": count,
                   "result": "PASS" if passed else "FAIL",
                   "log_sha256": hashlib.sha256(combined.encode("utf-8")).hexdigest(),
                   "timeout": False}
            if not passed:
                print(f"FAILED {suite['id']}: exit={proc.returncode}; "
                      f"count={count}\n{combined[-2000:]}", file=sys.stderr)
        except subprocess.TimeoutExpired:
            row = {"id": suite["id"], "command": cmd[1], "exit": None,
                   "unittest_count": None, "result": "BLOCK",
                   "log_sha256": None, "timeout": True}
        details.append(row)
        print(f"{suite['id']}: {row['result']} exit={row['exit']} tests={row['unittest_count']}", flush=True)
    after = git("rev-parse", "HEAD")
    clean_after = git_clean()
    all_ok = (all(x["result"] == "PASS" for x in details)
              and after == expected_sha and clean_after)
    return {"schema": "ads/v416-t07-local-run-result/v1",
            "task": "#1271", "source_sha": expected_sha,
            "observed_head_after": after,
            "python": sys.version.split()[0],
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "source_suites": details,
            "total_unittest_methods": sum(x["unittest_count"] or 0 for x in details),
            "all_sources_executed": len(details) == len(m["suites"]),
            "source_checkout_clean_after": clean_after,
            "release_gates": {gate: "NOT_RUN" for gate in m["release_gates"]},
            "external_not_run": m["external_not_run"],
            "source_conformance": SOURCE_ONLY_RESULT if all_ok else "BLOCK",
            "native_end_to_end": "NOT_RUN", "release_qualification": "NOT_RUN"}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--run", action="store_true",
                    help="Execute all source test suites (not only their file existence)")
    ap.add_argument("--expected-sha", help="Exact commit hash (mandatory with --run)")
    ap.add_argument("--timeout", type=int, default=420, help="Per-suite seconds")
    ap.add_argument("--json-out", type=Path,
                    help="Write local receipt (outside repository recommended)")
    opts = ap.parse_args()
    try:
        m = load_and_check_manifest()
        if not opts.run:
            print(json.dumps({"manifest": "SOURCE_MAPPING_VALID_ONLY",
                              "groups": len(m["groups"]), "suites": len(m["suites"]),
                              "source_sha": git("rev-parse", "HEAD"),
                              "test_execution": "NOT_RUN", "release_qualification": "NOT_RUN"},
                             sort_keys=True))
            return 0
        if not opts.expected_sha or opts.timeout < 30:
            raise QualificationError("--run needs --expected-sha and timeout >=30")
        receipt = run_all(m, expected_sha=opts.expected_sha, timeout=opts.timeout)
        if opts.json_out:
            if ROOT in opts.json_out.resolve().parents:
                raise QualificationError("Receipt must be outside working source tree")
            opts.json_out.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({k: receipt[k] for k in (
            "source_sha", "total_unittest_methods", "all_sources_executed",
            "source_checkout_clean_after", "source_conformance",
            "release_qualification")}, sort_keys=True))
        return 0 if receipt["source_conformance"] == SOURCE_ONLY_RESULT else 1
    except (QualificationError, OSError, ValueError) as exc:
        print(f"T07 BLOCK: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
