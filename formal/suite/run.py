#!/usr/bin/env python3
"""Opt-in ADS formal verification runner. Uses native solvers; no FIR."""
import argparse
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ANSWER = re.compile(r"^(?:sat|unsat|unknown)$", re.M)
STATES = re.compile(r"(\d+) states generated, (\d+) distinct states found")


def tool(argv, cwd=None, seconds=90):
    try:
        p = subprocess.run(argv, cwd=cwd, text=True, errors="replace",
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                           timeout=seconds, check=False)
        return {"code": p.returncode, "text": p.stdout}
    except (subprocess.TimeoutExpired, OSError) as e:
        return {"code": None, "text": str(e)}


def safe_file(root, path, suffix=None):
    if not isinstance(path, str) or not path or Path(path).is_absolute():
        raise ValueError("invalid relative path")
    p = (root / path).resolve()
    if not p.is_relative_to(root.resolve()) or not p.is_file():
        raise ValueError("missing/escaping input file: " + path)
    if suffix and p.suffix != suffix:
        raise ValueError("wrong model extension")
    return p


def hash_file(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_check(checkout, source_map):
    if not checkout:
        return {"status": "NOT_RUN", "reason": "No exact-SHA checkout supplied"}
    root = Path(checkout).resolve()
    head = tool(["git", "rev-parse", "HEAD"], cwd=root)
    if head["code"] != 0 or head["text"].strip() != source_map["candidate_head"]:
        return {"status": "BLOCKED_WRONG_HEAD", "found": head["text"].strip(),
                "expected": source_map["candidate_head"]}
    entries = source_map.get("sources")
    if not isinstance(entries, list) or not entries:
        return {"status": "FAIL", "reason": "SOURCE_BINDINGS_EMPTY_OR_MALFORMED", "checks": []}
    checks = []
    for row in entries:
        anchors = row.get("anchors") if isinstance(row, dict) else None
        if not isinstance(anchors, list) or not anchors or any(
            not isinstance(anchor, str) or not anchor for anchor in anchors
        ):
            checks.append({"path": row.get("path") if isinstance(row, dict) else None,
                           "status": "FAIL", "reason": "SOURCE_ANCHORS_EMPTY_OR_MALFORMED"})
            continue
        try:
            raw = safe_file(root, row["path"]).read_bytes()
            actual = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
            missing = [a for a in row["anchors"] if a not in raw.decode("utf-8", errors="replace")]
            ok = actual == row["blob"] and not missing
            checks.append({"path": row["path"], "status": "PASS" if ok else "FAIL",
                           "actual_blob": actual, "missing_anchors": missing})
        except (OSError, ValueError) as e:
            checks.append({"path": row["path"], "status": "FAIL", "error": str(e)})
    return {"status": "PASS" if all(c["status"] == "PASS" for c in checks) else "FAIL",
            "checks": checks}


def check(case, root, a):
    kind, purpose = case["tool"], case["purpose"]
    if kind not in ("z3", "tlc") or purpose not in ("proof", "mutation"):
        raise ValueError("unsupported tool or purpose: " + case["id"])
    model = safe_file(root, case["model"], ".smt2" if kind == "z3" else ".tla")
    hashes = {model.name: hash_file(model)}
    timeout = min(max(int(case.get("timeout_seconds", 90)), 1), 300)
    if kind == "z3":
        result = tool([a.z3, str(model)], cwd=root, seconds=timeout)
        actual = ANSWER.findall(result["text"])
        expected = case["expect"]
        if not isinstance(expected, list) or not expected or any(x not in ("sat", "unsat") for x in expected):
            raise ValueError("invalid expected SAT answers")
        matched = result["code"] == 0 and actual == expected
        detail = {"queries": actual}
    else:
        config = safe_file(root, case["config"], ".cfg")
        hashes[config.name] = hash_file(config)
        if not Path(a.tlc_jar).is_file():
            return {"id": case["id"], "status": "NOT_RUN", "reason": "TLC JAR missing"}
        with tempfile.TemporaryDirectory(prefix="ads-tlc-") as tmp:
            result = tool([a.java, "-cp", str(Path(a.tlc_jar).resolve()), "tlc2.TLC",
                           "-deadlock", "-metadir", tmp, "-config", str(config), model.name],
                          cwd=root, seconds=timeout)
        invariant_error = "Error: Invariant" in result["text"]
        states = STATES.search(result["text"])
        n = int(states.group(2)) if states else None
        if case["expect"] == "safe":
            matched = result["code"] == 0 and not invariant_error and n is not None and n >= case.get("min_states", 1)
        elif case["expect"] == "counterexample":
            matched = result["code"] not in (None, 0) and invariant_error and n is not None and case.get("invariant", "") in result["text"]
        else:
            raise ValueError("invalid TLC expectation")
        detail = {"invariant_error": invariant_error, "distinct_states": n}
    return {"id": case["id"], "tool": kind, "purpose": purpose, "model_hashes": hashes,
            "status": ("DETECTED" if purpose == "mutation" else "PASS") if matched
                      else ("NOT_RUN" if result["code"] is None else "FAIL"),
            "expected": case["expect"], "actual": detail,
            "exit_code": result["code"], "output_tail": result["text"][-1500:]}


def main():
    p = argparse.ArgumentParser(description="Native ADS formal verification suite (no FIR)")
    p.add_argument("--suite", required=True)
    p.add_argument("--z3", default="z3")
    p.add_argument("--cvc5", default="cvc5")
    p.add_argument("--all", action="store_true")
    p.add_argument("--model")
    p.add_argument("--property")
    p.add_argument("--changed-source", action="append")
    p.add_argument("--java", default="java")
    p.add_argument("--tlc-jar", required=True)
    p.add_argument("--source-checkout")
    p.add_argument("--strict-source", action="store_true")
    p.add_argument("--model-head", help="Exact experiment Git HEAD binding all consumed model/suite/runner bytes")
    p.add_argument("--out", required=True)
    a = p.parse_args()
    suite_path = Path(a.suite).resolve()
    root = suite_path.parent
    spec = json.loads(suite_path.read_text("utf-8"))
    if spec.get("schema") == "ads/formal-suite/v1":
        from expanded import main_v1
        return main_v1(a, suite_path, spec)
    if spec.get("schema") != "ads/formal-suite/v0" or not spec.get("cases"):
        raise ValueError("invalid/empty suite")
    map_path = safe_file(root, spec["source_map"], ".json")
    source_map = json.loads(map_path.read_text("utf-8"))
    if spec["candidate_head"] != source_map["candidate_head"]:
        raise ValueError("candidate SHA mismatch")
    ids = [x["id"] for x in spec["cases"]]
    if len(set(ids)) != len(ids):
        raise ValueError("duplicate case identifiers")
    checks = [check(x, root, a) for x in spec["cases"]]
    alignment = source_check(a.source_checkout, source_map)
    model_ok = all(x["status"] in ("PASS", "DETECTED") for x in checks)
    source_ok = alignment["status"] == "PASS"
    verdict = ("FAIL" if not model_ok or (a.strict_source and not source_ok) else
               "MODEL_AND_SOURCE_PASS" if source_ok else "MODEL_ONLY_PASS")
    report = {
        "kind": "ADS_BOUNDED_FORMAL_SUITE_NOT_FULL_ADS_PROOF",
        "suite_sha256": hash_file(suite_path), "source_map_sha256": hash_file(map_path),
        "candidate_head": spec["candidate_head"], "model_verdict": verdict,
        "tool_versions": {"z3": tool([a.z3, "-version"])["text"].strip(),
                          "java": tool([a.java, "-version"])["text"].splitlines()[:1],
                          "tlc_jar_sha256": hash_file(Path(a.tlc_jar)) if Path(a.tlc_jar).is_file() else None},
        "source_alignment": alignment, "checks": checks,
        "limitations": ["No full natural-language semantic-equivalence proof",
                        "No normative ADS qualification, Freeze or CI gate"]
    }
    output = Path(a.out).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", "utf-8")
    print(json.dumps({"model_verdict": verdict, "cases": len(checks),
                      "source": alignment["status"], "receipt": str(output)}))
    return 0 if verdict != "FAIL" else 1


if __name__ == "__main__":
    sys.exit(main())
