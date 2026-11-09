"""ADS v1 suite extension: native SMT/TLC execution, no model IR or ADS gate."""
import hashlib
import json
import re
import subprocess
import tempfile
from pathlib import Path

ANSWERS = re.compile(r"^(sat|unsat|unknown)$", re.MULTILINE)
STATES = re.compile(r"(\d+) states generated, (\d+) distinct states found")


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def safe_path(root, relative, suffix=None):
    if not isinstance(relative, str) or not relative or Path(relative).is_absolute():
        raise ValueError("relative file path required")
    p = (root / relative).resolve()
    if not p.is_relative_to(root.resolve()) or not p.is_file() or (suffix and p.suffix != suffix):
        raise ValueError("missing, escaping or wrong-extension input: " + relative)
    return p


def execute(args, cwd=None, timeout=90):
    try:
        p = subprocess.run(args, cwd=cwd, text=True, errors="replace",
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                           timeout=min(max(int(timeout), 1), 300), check=False)
        return {"code": p.returncode, "text": p.stdout, "kind": "EXECUTED"}
    except subprocess.TimeoutExpired as exc:
        return {"code": None, "text": str(exc), "kind": "TIMEOUT"}
    except OSError as exc:
        return {"code": None, "text": str(exc), "kind": "UNAVAILABLE"}


def source_alignment(checkout, source_map):
    if not checkout:
        return {"status": "NOT_RUN", "reason": "Exact candidate checkout not provided"}
    root = Path(checkout).resolve()
    r = execute(["git", "rev-parse", "HEAD"], cwd=root)
    if r["code"] != 0 or r["text"].strip() != source_map["candidate_head"]:
        return {"status": "BLOCKED", "reason": "candidate HEAD mismatch", "observed": r["text"].strip()}
    checks = []
    for s in source_map["sources"]:
        try:
            raw = safe_path(root, s["path"]).read_bytes()
            blob = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
            anchors_ok = all(x in raw.decode("utf8", errors="replace") for x in s["anchors"])
            checks.append({"path": s["path"], "blob": blob, "status": "PASS" if blob == s["blob"] and anchors_ok else "FAIL"})
        except (OSError, ValueError) as exc:
            checks.append({"path": s["path"], "status": "FAIL", "error": str(exc)})
    return {"status": "PASS" if all(c["status"] == "PASS" for c in checks) else "FAIL", "checks": checks}


def run_case(case, root, options):
    kind = case["tool"]
    if kind not in ("z3", "cvc5", "tlc") or case.get("purpose") not in ("proof", "mutation"):
        raise ValueError("unsupported tool or purpose: " + case["id"])
    model = safe_path(root, case["model"], ".tla" if kind == "tlc" else ".smt2")
    hashes = {case["model"]: sha256(model)}
    if kind == "tlc":
        cfg = safe_path(root, case["config"], ".cfg")
        hashes[case["config"]] = sha256(cfg)
        jar = Path(options.tlc_jar)
        if not jar.is_file():
            return {"id": case["id"], "status": "NOT_RUN", "tool": kind, "reason": "TLC JAR unavailable", "inputs_sha256": hashes}
        with tempfile.TemporaryDirectory(prefix="ads-tlc-v1-") as scratch:
            result = execute([options.java, "-cp", str(jar.resolve()), "tlc2.TLC", "-deadlock",
                              "-metadir", scratch, "-config", str(cfg), model.name],
                             cwd=model.parent, timeout=case.get("timeout_seconds", 90))
        match = STATES.search(result["text"])
        states = int(match.group(2)) if match else None
        bad = "Error: Invariant" in result["text"]
        if case["expect"] == "safe":
            ok = result["code"] == 0 and not bad and states is not None and states >= case.get("min_states", 1)
        elif case["expect"] == "counterexample":
            ok = result["code"] not in (0, None) and bad and case.get("invariant", "") in result["text"] and states is not None
        else:
            raise ValueError("invalid TLC expected outcome")
        actual = {"distinct_states": states, "invariant_failure": bad}
    else:
        command = [options.z3, "-smt2", str(model)] if kind == "z3" else [options.cvc5, "--lang=smt2", "--incremental", str(model)]
        result = execute(command, cwd=root, timeout=case.get("timeout_seconds", 90))
        answers = ANSWERS.findall(result["text"])
        if not isinstance(case["expect"], list) or not case["expect"] or any(x not in ("sat", "unsat") for x in case["expect"]):
            raise ValueError("invalid SMT expected outcome")
        ok = result["code"] == 0 and answers == case["expect"]
        actual = {"answers": answers}
    status = ("COUNTEREXAMPLE" if case["purpose"] == "mutation" else "PASS_MODEL") if ok else (
        "NOT_RUN" if result["kind"] == "UNAVAILABLE" else "INCONCLUSIVE" if result["kind"] == "TIMEOUT" else "FAIL")
    return {"id": case["id"], "model_id": case["model_id"], "property_id": case["property_id"],
            "purpose": case["purpose"], "tool": kind, "status": status,
            "expected": case["expect"], "actual": actual, "inputs_sha256": hashes,
            "exit_code": result["code"], "output_tail": result["text"][-800:]}


def main_v1(options, suite_path, spec):
    root = suite_path.resolve().parents[2]  # formal/v4.19/r1/suite.json -> formal/
    index_path = safe_path(root, spec["source_index"], ".json")
    index = json.loads(index_path.read_text("utf8"))
    source_map = json.loads(safe_path(root, spec["source_map"], ".json").read_text("utf8"))
    if spec["candidate_head"] != source_map["candidate_head"] or spec["candidate_head"] != index["candidate_head"]:
        raise ValueError("Exact SHA discrepancy among suite, index, source-map")
    props = {p["id"]: p for p in index["properties"]}
    if len(props) != len(index["properties"]):
        raise ValueError("duplicate property IDs")
    case_ids = [c["id"] for c in spec["cases"]]
    if len(case_ids) != len(set(case_ids)):
        raise ValueError("duplicate case IDs")
    for c in spec["cases"]:
        if c["property_id"] not in props or c["model_id"] != props[c["property_id"]]["model_id"]:
            raise ValueError("unbound or mismatched property: " + c["id"])
    selected = list(spec["cases"])
    if options.model:
        selected = [c for c in selected if c["model_id"] == options.model]
    if options.property:
        selected = [c for c in selected if c["property_id"] == options.property]
    invalidated = []
    if options.changed_source:
        changed = set(options.changed_source)
        invalidated = [p["id"] for p in index["properties"] if changed.intersection(p["sources"])]
        selected = [c for c in selected if c["property_id"] in invalidated]
    results = [run_case(c, root, options) for c in selected]
    differential = []
    for key in sorted({c["property_id"] for c in selected}):
        solvers = {r["tool"]: r for r in results if r["property_id"] == key and r["tool"] in ("z3", "cvc5") and r["purpose"] == "proof"}
        if len(solvers) == 2:
            z, c = solvers["z3"], solvers["cvc5"]
            differential.append({"property_id": key, "status": "PASS" if z["actual"] == c["actual"] and z["status"] == c["status"] == "PASS_MODEL" else "INCONCLUSIVE"})
    alignment = source_alignment(options.source_checkout, source_map)
    if options.changed_source:
        alignment = {"status": "STALE", "reason": "Changed-source selection invalidates old source-bound results until new exact source pinned", "baseline_alignment": alignment}
    statuses = {r["status"] for r in results}
    good = bool(results) and statuses.issubset({"PASS_MODEL", "COUNTEREXAMPLE"}) and all(d["status"] == "PASS" for d in differential)
    verdict = ("FAIL" if "FAIL" in statuses else "BLOCKED" if alignment["status"] == "BLOCKED" else
               "INCONCLUSIVE" if not good else "MODEL_AND_SOURCE_PASS" if alignment["status"] == "PASS" else "MODEL_ONLY_PASS")
    if options.strict_source and alignment["status"] != "PASS":
        verdict = "BLOCKED"
    tools = {}
    for k, command in (("z3", options.z3), ("cvc5", options.cvc5), ("java", options.java)):
        r = execute([command, "-version"] if k != "cvc5" else [command, "--version"])
        p = Path(command)
        tools[k] = {"version_output": r["text"].splitlines()[:2], "status": "VERIFIED" if r["code"] == 0 else "NOT_RUN",
                    "binary_sha256": sha256(p) if p.is_file() else None}
    jar = Path(options.tlc_jar)
    tools["tlc_jar"] = {"sha256": sha256(jar) if jar.is_file() else None, "status": "AVAILABLE" if jar.is_file() else "NOT_RUN"}
    evidence = {
        "kind": "ADS_BOUNDED_MODEL_CHECK_NOT_NORMATIVE_PROOF", "schema": "ads/formal-receipt/v1",
        "candidate_head": spec["candidate_head"], "candidate_status": "PROSPECTIVE_UNFROZEN",
        "suite_sha256": sha256(suite_path), "source_index_sha256": sha256(index_path),
        "source_map_sha256": sha256(safe_path(root, spec["source_map"], ".json")),
        "source_alignment": alignment, "tool_versions": tools, "model_verdict": verdict,
        "checks": results, "solver_differential": differential,
        "affected_property_ids": invalidated if options.changed_source else None,
        "coverage": {"modeled_obligations_denominator": len(props),
                     "modeled_obligations_with_selected_cases": len({x["property_id"] for x in results}),
                     "source_bound_verified_obligations": len({x["property_id"] for x in results}) if alignment["status"] == "PASS" and good else 0,
                     "all_ADS_normative_obligations_denominator": None,
                     "note": "Pilot denominator is declared properties; entire ADS rule inventory not enumerated"},
        "semantic_evaluation": "SELF_CHALLENGED_INDEPENDENT_REVIEW_NOT_RUN",
        "limitations": ["Bounded abstract states only; no full ADS natural-language equivalence",
                        "No full real GitHub/CI/Release execution evidence", "Model guards require source-to-model review",
                        "TLC liveness/fairness, claim expiry, multi-Task CAS, and full version inheritance not proved"]}
    out = Path(options.out).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(evidence, indent=2, ensure_ascii=False) + "\n", "utf8")
    print(json.dumps({"verdict": verdict, "cases": len(results), "source": alignment["status"], "receipt": str(out)}))
    return 0 if verdict in ("MODEL_ONLY_PASS", "MODEL_AND_SOURCE_PASS") else 2
