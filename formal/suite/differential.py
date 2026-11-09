"""Compare every matching native SMT input independently, including mutations."""

def solver_differential(selected, results):
    by_id = {r["id"]: r for r in results}
    groups = {}
    for c in selected:
        if c["tool"] not in ("z3", "cvc5"):
            continue
        key = (c["property_id"], c["model"], c["purpose"])
        groups.setdefault(key, {}).setdefault(c["tool"], []).append(c["id"])
    comparisons = []
    for (prop, model, purpose), tools in sorted(groups.items()):
        if not all(k in tools for k in ("z3", "cvc5")):
            continue
        pair_ok = len(tools["z3"]) == 1 and len(tools["cvc5"]) == 1
        a = by_id.get(tools["z3"][0]) if pair_ok else None
        b = by_id.get(tools["cvc5"][0]) if pair_ok else None
        success_status = "PASS_MODEL" if purpose == "proof" else "COUNTEREXAMPLE"
        ok = (pair_ok and a is not None and b is not None
              and a["status"] == b["status"] == success_status
              and a["expected"] == b["expected"]
              and a["actual"] == b["actual"]
              and a.get("inputs_sha256") == b.get("inputs_sha256"))
        comparisons.append({"property_id": prop, "model": model, "purpose": purpose,
                            "status": "PASS" if ok else "INCONCLUSIVE"})
    return comparisons
