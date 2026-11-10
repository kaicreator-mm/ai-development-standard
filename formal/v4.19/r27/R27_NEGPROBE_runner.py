#!/usr/bin/env python3
"""R27 negative probe executor: one scenario per process (subprocess isolation).

Loads the REAL expanded.py from <formal-root>/suite (exact Git worktree) and the
REAL r10 suite (35 cases) from the same tree, patches ONLY the native result
seam (run_case) and the three binding aligners (model/toolchain/source), then
calls the real main_v1 and writes its receipt.

  --formal-root <path>   exact Git worktree formal/ dir of the runner under test
  --forge none|tlc_model_id
                         tlc_model_id: keep every id legal but return a foreign
                         model_id on TLC results (the R27 counterexample)
  --out <receipt.json>   where main_v1 writes the full receipt

Prints one JSON summary line; exits with the runner's own exit code.
"""
import argparse
import importlib.util
import json
import sys
import tempfile
import types
from pathlib import Path
from unittest import mock


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--formal-root", required=True)
    ap.add_argument("--forge", choices=["none", "tlc_model_id"], required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    root = Path(args.formal_root).resolve()
    suite_path = root / "v4.19" / "r10" / "suite.json"
    sys.path.insert(0, str(root / "suite"))
    spec = importlib.util.spec_from_file_location(
        "ads_r27_probe_runner", root / "suite" / "expanded.py")
    runner = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(runner)

    declared = json.loads(suite_path.read_text("utf8"))
    assert len(declared["cases"]) == 35, "real r10 suite must have 35 cases"
    assert declared["require_solver_pairs"], "real r10 suite must require solver pairs"

    def native_result(case, r, o):
        status = "COUNTEREXAMPLE" if case["purpose"] == "mutation" else "PASS_MODEL"
        model_id = ("FORGED-TLC-MODEL"
                    if (case["tool"] == "tlc" and args.forge == "tlc_model_id")
                    else case["model_id"])
        return {"id": case["id"], "model_id": model_id,
                "property_id": case["property_id"], "tool": case["tool"],
                "purpose": case["purpose"], "status": status,
                "expected": case["expect"],
                "actual": ({"answers": case["expect"]} if case["tool"] != "tlc"
                           else {"distinct_states": 27}),
                "inputs_sha256": {case["model"]: "a" * 64}}

    with tempfile.TemporaryDirectory() as tmp:
        options = types.SimpleNamespace(
            model=None, property=None, changed_source=None, model_head=None,
            source_checkout=tmp, strict_source=True,
            out=str(Path(args.out).resolve()))
        with (mock.patch.object(runner, "run_case", side_effect=native_result),
              mock.patch.object(runner, "model_alignment",
                                return_value={"status": "PASS"}),
              mock.patch.object(runner, "toolchain_alignment",
                                return_value={"status": "PASS", "checks": []}),
              mock.patch.object(runner, "source_alignment",
                                return_value={"status": "PASS", "checks": []})):
            code = runner.main_v1(options, suite_path, declared)
    report = json.loads(Path(args.out).read_text("utf8"))
    audit = report.get("execution_inventory_audit") or {}
    print(json.dumps({"formal_root": str(root), "forge": args.forge,
                      "verdict": report["model_verdict"],
                      "audit_status": audit.get("status"),
                      "audit_expected": audit.get("expected_count"),
                      "audit_observed": audit.get("observed_count"),
                      "model_id_problem": any(p.get("field") == "model_id"
                                              for p in audit.get("problems", [])),
                      "source_bound_verified":
                          report["coverage"]["source_bound_verified_obligations"],
                      "exit_code": code}))
    sys.exit(code)


if __name__ == "__main__":
    main()
