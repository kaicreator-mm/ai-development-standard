"""Cross-check native SMT answers by exact (property, model, purpose) identity."""


def solver_differential(selected, results, require_pairs=False):
    """Reject silent loss of an independent solver when required by the suite.

    Legacy suites may deliberately contain only Z3. Current strict dual-solver
    suites opt in via require_solver_pairs=true, which is Git-model-pinned.
    """
    ids = [r["id"] for r in results]
    by_id = {r["id"]: r for r in results}
    selected_ids = {c["id"] for c in selected}
    groups = {}
    for case in selected:
        if case["tool"] not in ("z3", "cvc5"):
            continue
        key = (case["property_id"], case["model"], case["purpose"])
        groups.setdefault(key, {}).setdefault(case["tool"], []).append(case["id"])
    comparisons = []
    if len(by_id) != len(ids) or any(i not in selected_ids for i in by_id):
        comparisons.append({"property_id": None, "model": None, "purpose": None,
                            "status": "INCONCLUSIVE", "reason": "DUPLICATE_OR_ORPHAN_RESULT_ID"})
    for (prop, model, purpose), tools in sorted(groups.items()):
        present = all(k in tools for k in ("z3", "cvc5"))
        if not present:
            if require_pairs:
                comparisons.append({"property_id": prop, "model": model,
                                    "purpose": purpose, "status": "INCONCLUSIVE",
                                    "reason": "MISSING_INDEPENDENT_SOLVER_PAIR"})
            continue
        pair_ok = len(tools["z3"]) == 1 and len(tools["cvc5"]) == 1
        a = by_id.get(tools["z3"][0]) if pair_ok else None
        b = by_id.get(tools["cvc5"][0]) if pair_ok else None
        success_status = "PASS_MODEL" if purpose == "proof" else "COUNTEREXAMPLE"
        ok = (pair_ok and a is not None and b is not None
              and a["status"] == b["status"] == success_status
              and a.get("tool") in (None, "z3") and b.get("tool") in (None, "cvc5")
              and a["expected"] == b["expected"]
              and a["actual"] == b["actual"]
              and a.get("inputs_sha256") == b.get("inputs_sha256"))
        comparisons.append({"property_id": prop, "model": model, "purpose": purpose,
                            "status": "PASS" if ok else "INCONCLUSIVE",
                            "reason": None if ok else "MISSING_DUPLICATE_OR_DISAGREEING_RESULT"})
    return comparisons
