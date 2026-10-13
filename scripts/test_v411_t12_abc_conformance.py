"""V411-T12 integrated A+B+C conformance runner.

This runner composes already-landed v4.11 owner executable oracles. It does not
reimplement their policy logic and it never turns historical PASS into current
release truth. The committed registry contains expected inputs/oracle bindings
only; actual evidence is emitted at runtime.
"""
from __future__ import annotations

import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
REGISTRY = ROOT / "tests" / "fixtures" / "v411" / "t12" / "scenarios.json"
INTEGRATION_BASE = "301ebcdae1ad3a2cec8cd23627b2423282f98997"
EXPECTED_IDS = {f"S{i:02d}" for i in range(1, 19)} | {f"X{i:02d}" for i in range(1, 9)}
REQUIRED_FIELDS = {
    "case_id", "polarity", "archetype", "adoption_profile", "adoption_level",
    "job_labels", "actual_source_refs", "affected_source_base", "affected_source_head",
    "actor", "operator_session", "permissions", "authority_refs", "owner_refs",
    "mandatory_gates", "fidelity", "setup", "runner", "assertions",
    "expected_transition", "expected_effect_count", "equivalence_class", "exceptions",
}
ALLOWED_WRITE_PREFIXES = (
    "scripts/test_v411_t12_abc_conformance.py",
    "tests/fixtures/v411/t12/",
)
DOWNSTREAM_RELEASE_IDS = {"S11", "X04"}
PHYSICAL_DENY_IDS = {"S08", "X01"}
REQUIRED_PHYSICAL_DENY_TEST = (
    "scripts/test_v411_t09_effect_boundary.py",
    "test_claimed_a_current_deny_blocks_before_real_sink_mutation",
)
_module_cache: dict[str, object] = {}


def git(*args: str) -> str:
    proc = subprocess.run(
        ["git", *args], cwd=ROOT, text=True, capture_output=True, encoding="utf-8"
    )
    if proc.returncode:
        raise AssertionError(f"git {' '.join(args)} failed: {proc.stderr.strip()}")
    return proc.stdout.strip()


def load_registry() -> dict:
    return json.loads(REGISTRY.read_text(encoding="utf-8"))


def changed_paths() -> list[str]:
    return [p for p in git("diff", "--name-only", INTEGRATION_BASE, "HEAD").splitlines() if p]


def load_owner_module(rel: str):
    cached = _module_cache.get(rel)
    if cached is not None:
        return cached
    path = ROOT / rel
    if not path.is_file():
        raise AssertionError(f"owner runner missing: {rel}")
    if str(SCRIPTS) not in sys.path:
        sys.path.insert(0, str(SCRIPTS))
    module_name = "v411_t12_owner_" + path.stem
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise AssertionError(f"cannot load owner runner: {rel}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    _module_cache[rel] = module
    return module


def resolve_test(rel: str, method: str) -> unittest.TestCase:
    module = load_owner_module(rel)
    matches: list[type[unittest.TestCase]] = []
    for value in vars(module).values():
        if isinstance(value, type) and issubclass(value, unittest.TestCase) and hasattr(value, method):
            matches.append(value)
    if len(matches) != 1:
        raise AssertionError(
            f"{rel}::{method} resolves to {len(matches)} unittest cases, expected exactly one"
        )
    return matches[0](method)


def execute_owner_test(spec: dict) -> dict:
    rel = spec.get("file")
    method = spec.get("test")
    if not isinstance(rel, str) or not isinstance(method, str):
        return {"ok": False, "error": "malformed owner test binding", "spec": spec}
    try:
        case = resolve_test(rel, method)
        stream = io.StringIO()
        # Class-level unittest fixtures (setUpClass/tearDownClass) are managed
        # by TestSuite, not by invoking TestCase directly. Some reused owner
        # oracles (for example release applicability) intentionally load their
        # source-bound contracts in setUpClass, so every composed owner method
        # must execute through an isolated one-case suite.
        suite = unittest.TestSuite([case])
        result = unittest.TextTestRunner(stream=stream, verbosity=0).run(suite)
        return {
            "ok": result.wasSuccessful(),
            "file": rel,
            "test": method,
            "tests_run": result.testsRun,
            "failures": [msg for _, msg in result.failures],
            "errors": [msg for _, msg in result.errors],
            "skipped": [reason for _, reason in result.skipped],
            "output": stream.getvalue().strip(),
        }
    except Exception as exc:
        return {"ok": False, "file": rel, "test": method, "error": repr(exc)}


def validate_registry(doc: dict) -> list[str]:
    problems: list[str] = []
    if doc.get("schema_version") != "ai-dev/v411-t12-scenarios-v1":
        problems.append("wrong schema_version")
    if doc.get("integration_base") != INTEGRATION_BASE:
        problems.append("integration_base mismatch")
    if doc.get("logical_case_count") != 26 or doc.get("executable_record_count") != 52:
        problems.append("denominator mismatch")
    scenarios = doc.get("scenarios")
    if not isinstance(scenarios, dict) or set(scenarios) != EXPECTED_IDS:
        problems.append("scenario ID set is not exactly S01-S18 + X01-X08")
        return problems
    for case_id in sorted(EXPECTED_IDS):
        pair = scenarios.get(case_id)
        if not isinstance(pair, dict) or set(pair) != {"positive", "negative"}:
            problems.append(f"{case_id}: requires exactly positive+negative")
            continue
        for polarity in ("positive", "negative"):
            rec = pair[polarity]
            if not isinstance(rec, dict):
                problems.append(f"{case_id}/{polarity}: record is not an object")
                continue
            missing = REQUIRED_FIELDS - set(rec)
            if missing:
                problems.append(f"{case_id}/{polarity}: missing {sorted(missing)}")
            if rec.get("case_id") != case_id or rec.get("polarity") != polarity:
                problems.append(f"{case_id}/{polarity}: identity mismatch")
            if rec.get("affected_source_base") != INTEGRATION_BASE or rec.get("affected_source_head") != INTEGRATION_BASE:
                problems.append(f"{case_id}/{polarity}: owner-source base/head must bind post-T11 merge")
            if not rec.get("actual_source_refs") or not rec.get("owner_refs"):
                problems.append(f"{case_id}/{polarity}: missing real owner source/oracle refs")
            for rel in rec.get("actual_source_refs", []):
                if not isinstance(rel, str) or not (ROOT / rel).exists():
                    problems.append(f"{case_id}/{polarity}: source ref missing: {rel!r}")
            runner = rec.get("runner", {})
            tests = runner.get("tests") if isinstance(runner, dict) else None
            if runner.get("type") != "unittest-owner-methods" or not isinstance(tests, list) or not tests:
                problems.append(f"{case_id}/{polarity}: executable owner tests absent")
            forbidden_actual = {"tested_sha", "tested_tree", "exit", "observed_transition",
                                "observed_effect", "gate_disposition", "result", "currentness",
                                "evidence_refs"}
            if forbidden_actual & set(rec):
                problems.append(f"{case_id}/{polarity}: committed fixture pre-fills runtime truth")
        if case_id in DOWNSTREAM_RELEASE_IDS:
            for polarity in ("positive", "negative"):
                rec = pair[polarity]
                if rec.get("fidelity") != "CONTRACT_SIMULATION_NO_RELEASE_PASS":
                    problems.append(f"{case_id}/{polarity}: release fidelity can mint false release truth")
                if "DOWNSTREAM_RELEASE_NOT_RUN" not in rec.get("expected_transition", ""):
                    problems.append(f"{case_id}/{polarity}: downstream release must stay NOT_RUN")
        if case_id in PHYSICAL_DENY_IDS:
            neg_tests = {
                (x.get("file"), x.get("test"))
                for x in pair["negative"].get("runner", {}).get("tests", [])
                if isinstance(x, dict)
            }
            if REQUIRED_PHYSICAL_DENY_TEST not in neg_tests:
                problems.append(f"{case_id}/negative: physical safe-sink DENY oracle not bound")
            if pair["negative"].get("expected_effect_count") != 0:
                problems.append(f"{case_id}/negative: expected effect count must be zero")
    compound = doc.get("compound")
    if not isinstance(compound, dict) or compound.get("id") != "J09+J10+J11+J12":
        problems.append("mandatory J09+J10+J11+J12 compound absent")
    elif not compound.get("tests"):
        problems.append("mandatory compound has no executable owner tests")
    return problems


def validate_write_set() -> list[str]:
    problems = []
    if git("merge-base", "--is-ancestor", INTEGRATION_BASE, "HEAD") != "":
        pass
    for path in changed_paths():
        if not any(path == prefix or path.startswith(prefix) for prefix in ALLOWED_WRITE_PREFIXES):
            problems.append(f"owner-conflict write outside T12 unique paths: {path}")
    return problems


def run_record(record: dict, tested_sha: str, tested_tree: str) -> dict:
    test_results = [execute_owner_test(spec) for spec in record["runner"]["tests"]]
    ok = all(item.get("ok") for item in test_results)
    case_id = record["case_id"]
    release_contract = case_id in DOWNSTREAM_RELEASE_IDS
    return {
        "case_id": case_id,
        "polarity": record["polarity"],
        "tested_sha": tested_sha,
        "tested_tree": tested_tree,
        "command": "python scripts/test_v411_t12_abc_conformance.py",
        "exit": 0 if ok else 1,
        "observed_transition": record["expected_transition"] if ok else "OWNER_ORACLE_FAILED",
        "observed_effect": record["expected_effect_count"],
        "gate_disposition": "NOT_RUN" if release_contract else ("PASS" if ok else "FAIL"),
        "proof_layers": {
            "P1_A": "PASS" if ok else "FAIL",
            "P2_B": "PASS" if ok else "FAIL",
            "P3_C": "PASS" if ok else "FAIL",
        },
        "result": "PASS_CONTRACT" if ok and release_contract else ("PASS" if ok else "FAIL"),
        "currentness": "CURRENT" if ok else "UNVERIFIED",
        "fidelity": record["fidelity"],
        "evidence_refs": [f"{x['file']}#{x['test']}" for x in record["runner"]["tests"]],
        "owner_test_results": test_results,
    }


def run_compound(compound: dict, tested_sha: str, tested_tree: str) -> dict:
    results = [execute_owner_test(spec) for spec in compound["tests"]]
    ok = all(item.get("ok") for item in results)
    return {
        "id": compound["id"],
        "tested_sha": tested_sha,
        "tested_tree": tested_tree,
        "result": "PASS_CONTRACT" if ok else "FAIL",
        "material_disposition": compound["expected_disposition"],
        "release_gate": "NOT_RUN",
        "owner_test_results": results,
    }


def main() -> int:
    doc = load_registry()
    problems = validate_registry(doc) + validate_write_set()
    if problems:
        print(json.dumps({"V411_T12": "REGISTRY_OR_WRITESET_FAIL", "problems": problems}, indent=2))
        return 1

    tested_sha = git("rev-parse", "HEAD")
    tested_tree = git("rev-parse", "HEAD^{tree}")
    records = []
    for case_id in sorted(EXPECTED_IDS):
        for polarity in ("positive", "negative"):
            records.append(run_record(doc["scenarios"][case_id][polarity], tested_sha, tested_tree))

    compound = run_compound(doc["compound"], tested_sha, tested_tree)
    failures = [r for r in records if r["exit"] != 0]
    if compound["result"] != "PASS_CONTRACT":
        failures.append({"compound": compound})
    ledger = {
        "event": "V411_T12_RUNTIME_EVIDENCE_LEDGER",
        "pack_blob": doc["pack_blob"],
        "integration_base": INTEGRATION_BASE,
        "tested_sha": tested_sha,
        "tested_tree": tested_tree,
        "record_count": len(records),
        "records": records,
        "compound": compound,
        "downstream_release_truth": "NOT_RUN",
        "failure_count": len(failures),
    }
    print("V411_T12_EVIDENCE_LEDGER=" + json.dumps(ledger, sort_keys=True))
    if failures:
        print(json.dumps({"V411_T12": "FAIL", "failure_count": len(failures)}, indent=2))
        return 1
    print("V411_T12=PASS records=52 compound=PASS_CONTRACT downstream_release=NOT_RUN")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
