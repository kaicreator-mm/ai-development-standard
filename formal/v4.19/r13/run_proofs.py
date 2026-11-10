"""Bounded solver-paired proof fixture for ADS #1366; source review, not production CAS."""
from __future__ import annotations
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EXPECTED = {
    "weak-admission-gap.smt2": ["sat"] * 4,
    "publish-safety.smt2": ["sat"] + ["unsat"] * 9 + ["sat"],
}
PINNED_MODEL_GIT_BLOBS = {
    "weak-admission-gap.smt2": "04f85b71b60eea1382b3044d459702d5ba0978e7",
    "publish-safety.smt2": "df743519bf2e7f9ed3aa356b5f0175e7e3fb360c",
}
PINNED_SHA256 = {
    "z3": "fcd0ca765d1c0b4eac776f442ec0f10294b9a6416be91fad4e52fa19012c8d01",
    "cvc5": "6aecddf466552b83bb5883756c7955e0c9d5ddcc6d7f45b48c2f6e06a741b102",
}
COMMANDS = {
    "z3": [os.environ.get("ADS_Z3", "z3"), "-smt2"],
    "cvc5": [os.environ.get("ADS_CVC5", "cvc5"), "--lang=smt2", "--incremental"],
}


def run_solver(tool: str, path: Path) -> dict:
    exe = COMMANDS[tool][0]
    binary_sha = hashlib.sha256(Path(exe).read_bytes()).hexdigest()
    if binary_sha != PINNED_SHA256[tool]:
        return {"tool": tool, "exit_code": None, "statuses": [],
                "expected": EXPECTED[path.name], "matched": False,
                "stderr": "REJECTED_UNPINNED_BINARY_SHA256", "stdout_sha256": None,
                "binary_sha256": binary_sha}
    command = [*COMMANDS[tool], str(path)]
    process = subprocess.run(command, capture_output=True, text=True, timeout=25)
    statuses = re.findall(r"^(sat|unsat|unknown)$", process.stdout, flags=re.MULTILINE)
    expected = EXPECTED[path.name]
    ok = process.returncode == 0 and statuses == expected
    return {"tool": tool, "exit_code": process.returncode, "statuses": statuses,
            "expected": expected, "matched": ok, "stderr": process.stderr[:400],
            "stdout_sha256": hashlib.sha256(process.stdout.encode()).hexdigest(),
            "binary_sha256": binary_sha}


class InputBindingError(RuntimeError):
    """A model or executable does not match the reviewed exact bytes."""


def assert_model_hashes(stage: str) -> list[dict]:
    """Reject any missing/changed model before native execution and after it."""
    checks = []
    for name, expected in PINNED_MODEL_GIT_BLOBS.items():
        path = ROOT / name
        try:
            current = git_blob(path.read_bytes())
        except OSError as exc:
            raise InputBindingError(f"{stage}: missing/unreadable model {name}: {exc}") from exc
        if current != expected:
            raise InputBindingError(f"{stage}: model {name} blob {current} != {expected}")
        checks.append({"path": name, "expected_git_blob": expected,
                       "observed_git_blob": current, "status": "PASS"})
    return checks


def assert_tool_hashes() -> list[dict]:
    """Preflight all selected binaries before running any query."""
    checks = []
    for name, expected in PINNED_SHA256.items():
        location = Path(COMMANDS[name][0])
        try:
            actual = hashlib.sha256(location.read_bytes()).hexdigest()
        except OSError as exc:
            raise InputBindingError(f"tool preflight: unreadable {name}: {exc}") from exc
        if actual != expected:
            raise InputBindingError(f"tool preflight: {name} SHA256 {actual} != pinned {expected}")
        checks.append({"tool": name, "sha256": actual, "status": "PASS"})
    return checks


def verify():
    model_before = assert_model_hashes("preflight")
    tool_before = assert_tool_hashes()
    details = []
    for filename in EXPECTED:
        path = ROOT / filename
        results = [run_solver(tool, path) for tool in COMMANDS]
        details.append({"file": filename, "git_blob": git_blob(path.read_bytes()),
                        "file_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                        "results": results,
                        "solver_pair_pass": all(r["matched"] for r in results) and
                            results[0]["statuses"] == results[1]["statuses"]})
    model_after = assert_model_hashes("postflight")
    tool_after = assert_tool_hashes()
    return {"schema": "ads/formal-r13-bound-dispatch-publication/v2",
            "scope": "ONE_NEW_DISPATCH_ABSTRACT_SOURCE_HYPOTHESIS_AND_OLD_RESERVATION_PROXY",
            "input_binding": {"model_before": model_before,
                              "model_after": model_after,
                              "tool_before": tool_before, "tool_after": tool_after},
            "models": details,
            "total_checks_per_solver": sum(len(x) for x in EXPECTED.values()),
            "pair_status": "PASS" if all(x["solver_pair_pass"] for x in details) else "FAIL",
            "not_proven": ["No real accepted GitHub Claim/Dispatch CAS was executed",
                "No source-to-model equivalence theorem or cryptographic schema identity proof",
                "Model is an asserted necessary-conditions hypothesis; UNSAT follows this hypothesis",
                "Old R8 reservation is not equivalent to an accepted dispatch event",
                "Full ADS rule denominator unknown"]}


def git_blob(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()


if __name__ == "__main__":
    try:
        doc = verify()
    except InputBindingError as exc:
        print(json.dumps({"schema": "ads/formal-r13-input-binding-failure/v1",
                          "pair_status": "BLOCK", "reason": str(exc)}, indent=2))
        sys.exit(2)
    print(json.dumps(doc, indent=2))
    sys.exit(0 if doc["pair_status"] == "PASS" else 1)
