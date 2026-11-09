#!/usr/bin/env python3
"""ADS v4.19 R0 bounded proof runner (stdlib only + external z3/TLC)."""
import argparse
import hashlib
import json
import re
import subprocess
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROLE_EXPECTED = ["unsat"] * 7 + ["sat"] * 3 + ["unsat"] * 2
GATE_EXPECTED = ["unsat"] * 4 + ["sat"]


def execute(args, cwd=HERE, timeout=90):
    return subprocess.run(args, cwd=cwd, text=True, stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT, timeout=timeout, check=False)


def query(z3, file, expected):
    res = execute([z3, str(HERE / file)])
    values = re.findall(r"^(?:unsat|sat|unknown)$", res.stdout, re.M)
    return {"file": file, "expected": expected, "actual": values,
            "exit_code": res.returncode,
            "pass": res.returncode == 0 and values == expected,
            "output": res.stdout[-1000:]}


def tlc(java, jar, config, expected_error, pattern=None):
    with tempfile.TemporaryDirectory(prefix="ads-tlc-") as scratch:
        res = execute([java, "-cp", jar, "tlc2.TLC", "-deadlock",
                       "-metadir", scratch, "-config", config, "ADSWorkflow.tla"])
    err = "Error: Invariant" in res.stdout
    matched = pattern in res.stdout if pattern else True
    states = re.search(r"(\d+) states generated, (\d+) distinct states found", res.stdout)
    return {"config": config, "expected_invariant_error": expected_error,
            "observed_invariant_error": err,
            "counterexample_expected_marker": pattern,
            "counterexample_marker_found": matched,
            "states_generated": int(states.group(1)) if states else None,
            "distinct_states": int(states.group(2)) if states else None,
            "exit_code": res.returncode,
            "pass": err == expected_error and matched and
                    (res.returncode != 0 if expected_error else res.returncode == 0),
            "output_tail": res.stdout[-3500:]}


def git_blob_sha(payload):
    return hashlib.sha1(b"blob " + str(len(payload)).encode() + b"\0" + payload).hexdigest()


def source_check(checkout, source_map):
    if not checkout:
        return {"status": "NOT_RUN", "reason": "Exact candidate Git checkout not supplied"}
    checkout = Path(checkout).resolve()
    rev = execute(["git", "rev-parse", "HEAD"], cwd=checkout)
    if rev.returncode != 0 or rev.stdout.strip() != source_map["candidate_head"]:
        return {"status": "BLOCKED_WRONG_HEAD", "found": rev.stdout.strip(),
                "expected": source_map["candidate_head"]}
    checks = []
    for row in source_map["sources"]:
        path = checkout / row["path"]
        data = path.read_bytes() if path.is_file() else b""
        actual_sha = git_blob_sha(data) if data else None
        snippet = data.decode("utf-8", errors="replace")
        checks.append({"path": row["path"], "expected_blob": row["blob"],
                       "actual_blob": actual_sha,
                       "missing_anchors": [a for a in row["anchors"] if a not in snippet],
                       "pass": actual_sha == row["blob"] and
                               all(a in snippet for a in row["anchors"])})
    return {"status": "PASS" if all(r["pass"] for r in checks) else "FAIL",
            "checks": checks}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--z3", default="z3")
    ap.add_argument("--java", default="java")
    ap.add_argument("--tlc-jar", required=True)
    ap.add_argument("--source-checkout", help="Git checkout at candidate exact HEAD")
    ap.add_argument("--out", default=str(HERE / "receipt.json"))
    a = ap.parse_args()
    source_map = json.loads((HERE / "source-map.json").read_text(encoding="utf-8"))
    z3_version = execute([a.z3, "-version"]).stdout.strip()
    z3_checks = [query(a.z3, "roles.smt2", ROLE_EXPECTED),
                 query(a.z3, "gates.smt2", GATE_EXPECTED),
                 query(a.z3, "roles-mutant.smt2", ["sat"])]
    tlc_checks = [tlc(a.java, a.tlc_jar, "ADSWorkflow.cfg", False),
                  tlc(a.java, a.tlc_jar, "ADSWorkflow.bad-release.cfg", True, "LifecycleSafe"),
                  tlc(a.java, a.tlc_jar, "ADSWorkflow.bad-claim.cfg", True, "SingleWriter")]
    proof_pass = all(x["pass"] for x in z3_checks + tlc_checks)
    report = {"kind": "BOUNDED_FORMAL_MODEL_CHECK_NOT_FULL_ADS_PROOF",
              "source_binding": source_map["candidate_head"],
              "repo": source_map["repository"], "z3_version": z3_version,
              "z3": z3_checks, "tlc": tlc_checks,
              "exact_source_checkout": source_check(a.source_checkout, source_map),
              "model_verdict": "PASS" if proof_pass else "FAIL",
              "qualification": "MODEL_ONLY_NOT_NORMATIVE_ADOPTION"}
    Path(a.out).write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"model_verdict": report["model_verdict"],
                      "z3_query_count": sum(len(x["actual"]) for x in z3_checks),
                      "tlc_runs": len(tlc_checks),
                      "safe_distinct_states": tlc_checks[0]["distinct_states"],
                      "source_check": report["exact_source_checkout"]["status"]}, ensure_ascii=False))
    raise SystemExit(0 if proof_pass else 1)

if __name__ == "__main__":
    main()
