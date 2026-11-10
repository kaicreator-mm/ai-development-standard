"""Verify returned native-case identities before a model/source PASS may be emitted.

This checks execution-result correspondence, not model truth or ADS semantics.
The declared suite and exact tool identities are separately checked by the runner.
"""


def audit_execution_results(selected, results):
    """Fail closed if an executed case is missing, substituted, or mislabeled.

    A list comprehension usually preserves identity, but that assumption must
    not become an unverified premise of a formal-verification receipt.
    """
    expected_count = len(selected) if isinstance(selected, list) else None
    observed_count = len(results) if isinstance(results, list) else None
    problems = []
    if not isinstance(selected, list) or not selected:
        problems.append({"reason": "EMPTY_OR_INVALID_SELECTED_CASES"})
    if not isinstance(results, list) or observed_count != expected_count:
        problems.append({"reason": "RESULT_COUNT_MISMATCH"})
    if isinstance(selected, list) and isinstance(results, list):
        seen = set()
        for index, (case, result) in enumerate(zip(selected, results)):
            if not isinstance(case, dict) or not isinstance(result, dict):
                problems.append({"position": index, "reason": "INVALID_CASE_OR_RESULT"})
                continue
            identifier = result.get("id")
            if not isinstance(identifier, str) or not identifier or identifier in seen:
                problems.append({"position": index, "reason": "MISSING_OR_DUPLICATE_RESULT_ID"})
            else:
                seen.add(identifier)
            for field in ("id", "tool", "purpose", "property_id", "model_id"):
                if result.get(field) != case.get(field):
                    problems.append({"position": index, "field": field,
                                     "reason": "RESULT_IDENTITY_MISMATCH"})
            if result.get("status") not in ("PASS_MODEL", "COUNTEREXAMPLE", "FAIL", "INCONCLUSIVE", "NOT_RUN"):
                problems.append({"position": index, "field": "status",
                                 "reason": "INVALID_RESULT_STATUS"})
            if result.get("expected") != case.get("expect"):
                problems.append({"position": index, "field": "expected",
                                 "reason": "RESULT_EXPECTATION_MISMATCH"})
    return {"status": "PASS" if not problems else "FAIL",
            "expected_count": expected_count, "observed_count": observed_count,
            "problems": problems[:12]}
