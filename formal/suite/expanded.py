"""ADS v1 suite extension: native SMT/TLC execution, no model IR or ADS gate."""
import hashlib
import json
import re
import subprocess
import tempfile
from pathlib import Path
from provenance import model_alignment
from differential import solver_differential

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
        ok = result["code"] == 0 and answers == case["expect"] and "(error" not in result["text"].lower()
        actual = {"answers": answers}
    status = ("COUNTEREXAMPLE" if case["purpose"] == "mutation" else "PASS_MODEL") if ok else (
        "NOT_RUN" if result["kind"] == "UNAVAILABLE" else "INCONCLUSIVE" if (result["kind"] == "TIMEOUT" or (kind in ("z3", "cvc5") and "unknown" in actual.get("answers", []))) else "FAIL")
    return {"id": case["id"], "model_id": case["model_id"], "property_id": case["property_id"],
            "purpose": case["purpose"], "tool": kind, "status": status,
            "expected": case["expect"], "actual": actual, "inputs_sha256": hashes,
            "exit_code": result["code"], "output_tail": result["text"][-800:]}


def affected_properties(properties, changed_sources):
    """Invalidate direct source users AND dependent properties to a fixed point."""
    changed = set(changed_sources)
    invalid = {p["id"] for p in properties if changed.intersection(p.get("sources", []))}
    while True:
        next_invalid = invalid | {p["id"] for p in properties
                                  if invalid.intersection(p.get("depends_on", []))}
        if next_invalid == invalid:
            return sorted(invalid)
        invalid = next_invalid


def audit_traceability(spec, index, trace, source_map):
    """Fail closed on missing/broken bidirectional source-property-case links."""
    sha = spec["candidate_head"]
    if sha != index.get("candidate_head") or sha != source_map.get("candidate_head") or sha != trace.get("subject_head"):
        raise ValueError("traceability candidate SHA mismatch")
    sources = [s["path"] for s in source_map["sources"]]
    props = [p["id"] for p in index["properties"]]
    cases = [c["id"] for c in spec["cases"]]
    tp = [p["property_id"] for p in trace["properties"]]
    ts = [s["path"] for s in trace["sources"]]
    for label, values in (("sources", sources), ("properties", props),
                          ("cases", cases), ("trace properties", tp), ("trace sources", ts)):
        if len(values) != len(set(values)):
            raise ValueError("duplicate " + label)
    if set(props) != set(tp) or set(sources) != set(ts):
        raise ValueError("traceability missing or orphan source/property")
    by_prop = {p["id"]: p for p in index["properties"]}
    by_trace = {p["property_id"]: p for p in trace["properties"]}
    by_source = {s["path"]: s for s in trace["sources"]}
    source_definitions = {s["path"]: s for s in source_map["sources"]}
    by_case = {c["id"]: c for c in spec["cases"]}
    for p in index["properties"]:
        pid = p["id"]
        source_paths = set(p.get("sources", []))
        if not source_paths or not source_paths <= set(sources):
            raise ValueError("missing/unmapped source: " + pid)
        deps = p.get("depends_on", [])
        if pid in deps or any(d not in by_prop for d in deps):
            raise ValueError("invalid dependency: " + pid)
        expected_cases = {c["id"] for c in spec["cases"] if c["property_id"] == pid}
        if not expected_cases or set(by_trace[pid]["case_ids"]) != expected_cases:
            raise ValueError("missing or incorrect case link: " + pid)
        if any(by_case[cid]["model_id"] != p["model_id"] for cid in expected_cases):
            raise ValueError("case model identity mismatch: " + pid)
        if source_paths != set(by_trace[pid]["source_paths"]):
            raise ValueError("forward property-source mismatch: " + pid)
    for src in sources:
        actual = {p["id"] for p in index["properties"] if src in p["sources"]}
        if set(by_source[src]["property_ids"]) != actual:
            raise ValueError("reverse source-property mismatch: " + src)
        if by_source[src].get("blob") != source_definitions[src].get("blob"):
            raise ValueError("source provenance blob mismatch: " + src)
        anchors = by_source[src].get("anchors")
        if not isinstance(anchors, list) or not anchors or any(not isinstance(a, str) or not a for a in anchors):
            raise ValueError("missing/invalid trace source anchors: " + src)
    for c in spec["cases"]:
        if c["property_id"] not in by_prop:
            raise ValueError("unmapped case: " + c["id"])
    visiting, done = set(), set()
    def visit(pid):
        if pid in visiting:
            raise ValueError("cyclic property dependency: " + pid)
        if pid in done:
            return
        visiting.add(pid)
        for dep in by_prop[pid].get("depends_on", []):
            visit(dep)
        visiting.remove(pid)
        done.add(pid)
    for pid in props:
        visit(pid)
    return {"status": "PASS", "property_count": len(props),
            "case_count": len(cases), "source_count": len(sources)}


def combine_source_anchors(source_map, trace):
    """Require both source-map anchors and supplementary trace-rule anchors."""
    trace_by_path = {s["path"]: s for s in trace["sources"]}
    merged = dict(source_map)
    merged["sources"] = [
        dict(s, anchors=list(dict.fromkeys(s["anchors"] + trace_by_path[s["path"]]["anchors"])))
        for s in source_map["sources"]
    ]
    return merged


def main_v1(options, suite_path, spec):
    root = suite_path.resolve().parents[2]  # formal/v4.19/r1/suite.json -> formal/
    index_path = safe_path(root, spec["source_index"], ".json")
    index = json.loads(index_path.read_text("utf8"))
    source_map = json.loads(safe_path(root, spec["source_map"], ".json").read_text("utf8"))
    traceability = {"status": "NOT_RUN"}
    effective_source_map = source_map
    if spec.get("traceability"):
        trace = json.loads(safe_path(root, spec["traceability"], ".json").read_text("utf8"))
        traceability = audit_traceability(spec, index, trace, source_map)
        effective_source_map = combine_source_anchors(source_map, trace)
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
        invalidated = affected_properties(index["properties"], options.changed_source)
        selected = [c for c in selected if c["property_id"] in invalidated]
    model_inputs = {str(suite_path.resolve().relative_to(root)),
                    spec["source_index"], spec["source_map"],
                    "suite/run.py", "suite/expanded.py",
                    "suite/provenance.py", "suite/differential.py"}
    if spec.get("traceability"):
        model_inputs.add(spec["traceability"])
    for case in selected:
        model_inputs.add(case["model"])
        if case.get("config"):
            model_inputs.add(case["config"])
    model_before = model_alignment(root, model_inputs, getattr(options, "model_head", None))
    # A caller-provided but invalid model pin must not execute or be treated as PASS.
    blocked_model = model_before["status"] in ("FAIL", "BLOCKED") or (
        options.strict_source and model_before["status"] != "PASS")
    results = [] if blocked_model else [run_case(c, root, options) for c in selected]
    model_after = (model_alignment(root, model_inputs, getattr(options, "model_head", None))
                   if model_before["status"] == "PASS" else model_before)
    differential = solver_differential(selected, results)
    alignment = source_alignment(options.source_checkout, effective_source_map)
    if options.changed_source:
        alignment = {"status": "STALE", "reason": "Changed-source selection invalidates old source-bound results until new exact source pinned", "baseline_alignment": alignment}
    statuses = {r["status"] for r in results}
    good = bool(results) and statuses.issubset({"PASS_MODEL", "COUNTEREXAMPLE"}) and all(d["status"] == "PASS" for d in differential)
    verdict = ("FAIL" if "FAIL" in statuses else "BLOCKED" if alignment["status"] in ("BLOCKED", "FAIL", "STALE") else
               "INCONCLUSIVE" if not good else "MODEL_AND_SOURCE_PASS" if alignment["status"] == "PASS" else "MODEL_ONLY_PASS")
    if verdict == "MODEL_AND_SOURCE_PASS" and model_after["status"] != "PASS":
        verdict = "MODEL_ONLY_PASS"
    if (model_before["status"] in ("FAIL", "BLOCKED") or model_after["status"] in ("FAIL", "BLOCKED")) and verdict != "FAIL":
        verdict = "BLOCKED"
    if options.strict_source and (alignment["status"] != "PASS" or model_after["status"] != "PASS") and verdict != "FAIL":
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
        "traceability_sha256": (sha256(safe_path(root, spec["traceability"], ".json"))
                                 if spec.get("traceability") else None),
        "source_alignment": alignment, "tool_versions": tools, "model_verdict": verdict,
        "traceability_audit": traceability,
        "model_input_alignment_before": model_before,
        "model_input_alignment_after": model_after,
        "checks": results, "solver_differential": differential,
        "selection": {
            "all_declared_cases_selected": (len(selected) == len(spec["cases"])
                                           and not options.model and not options.property
                                           and not options.changed_source),
            "requested_model": options.model,
            "requested_property": options.property,
            "requested_changed_sources": options.changed_source,
            "selected_case_ids": [c["id"] for c in selected],
            "selected_case_count": len(selected),
            "declared_case_count": len(spec["cases"]),
            "qualification": "SELECTED_CASES_ONLY_NOT_FULL_ADS_PROOF"
        },
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
