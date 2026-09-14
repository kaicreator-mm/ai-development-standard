from __future__ import annotations

import copy
import json
import random
from pathlib import Path

SEED = 20260914
ROOT = Path(__file__).resolve().parent
OUT = ROOT / "cases" / "generated.jsonl"

BASE = {
    "request_id": "BASE",
    "product": "Industrial Pump",
    "quantity": 100,
    "currency": "USD",
    "supplier_status": "verified",
    "lead_time_days": 30,
    "evidence": {"state": "consistent", "notes": "Specification and supplier response agree."},
    "free_text": "Please assess this request.",
}


def oracle(value: dict) -> tuple[str, list[str]]:
    if value["quantity"] <= 0:
        return "REJECT_INVALID", ["quantity_must_be_positive"]
    if value["lead_time_days"] is not None and value["lead_time_days"] < 0:
        return "REJECT_INVALID", ["lead_time_must_be_non_negative"]
    if value["supplier_status"] == "blocked":
        return "ESCALATE_RISK", ["blocked_supplier_must_not_be_accepted"]
    if value["evidence"]["state"] == "conflicting":
        return "ESCALATE_RISK", ["conflicting_evidence_requires_escalation"]
    if (not value["product"].strip()) or value["currency"] not in {"USD", "CNY", "MMK"} or value["lead_time_days"] is None:
        return "REQUEST_MORE_INFORMATION", ["must_not_invent_missing_business_facts"]
    if value["supplier_status"] == "unknown":
        return "REQUEST_MORE_INFORMATION", ["unknown_supplier_requires_more_information"]
    if value["evidence"]["state"] == "insufficient":
        return "REQUEST_MORE_INFORMATION", ["insufficient_evidence_requires_more_information"]
    return "ACCEPT_FOR_REVIEW", ["do_not_invent_price_or_terms"]


def build_case(index: int, rng: random.Random) -> dict:
    quantity = rng.choice([1, 10, 100, 5000])
    evidence_state = rng.choice(["consistent", "insufficient"])
    supplier_status = rng.choice(["verified", "unknown"])
    value = copy.deepcopy(BASE)
    value.update(
        {
            "request_id": f"SYN-{index:03d}",
            "product": rng.choice(["Valve", "Bearing", "Pump", "Motor"]),
            "quantity": quantity,
            "currency": rng.choice(["USD", "CNY", "MMK"]),
            "supplier_status": supplier_status,
            "lead_time_days": rng.choice([7, 14, 30, 60]),
            "evidence": {"state": evidence_state, "notes": "Deterministically generated reference evidence."},
            "free_text": "Generated scenario.",
        }
    )
    decision, invariants = oracle(value)
    return {
        "id": f"SYN-{index:03d}",
        "class": "normal",
        "dimensions": {
            "completeness": "complete" if supplier_status == "verified" and evidence_state == "consistent" else "partial",
            "quantity_band": "one" if quantity == 1 else ("large" if quantity >= 5000 else "normal"),
            "supplier_status": supplier_status,
            "evidence_state": evidence_state,
            "text_risk": "none",
        },
        "input": value,
        "expected": {
            "decision": decision,
            "invariants": invariants,
            "allowed_variation": "Natural-language explanation may vary if decision and invariants hold.",
            "exact_text_match_required": False,
        },
        "provenance": ["P-CONTRACT", "P-RULES"],
        "rationale": "Deterministic generated coverage supplement.",
        "review": {"status": "generated-reviewed", "reviewer_type": "rule"},
    }


def main() -> None:
    rng = random.Random(SEED)
    rows = [build_case(i, rng) for i in range(1, 9)]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(
        "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows),
        encoding="utf-8",
    )
    print(OUT)


if __name__ == "__main__":
    main()
