from __future__ import annotations

import copy
import json
from pathlib import Path
import unittest

from test_protocol_schemas import load_schema, validate_subset
from test_v40_operation_contracts import (
    SHA_A,
    SHA_B,
    aggregation_example,
    assurance_example,
    finding_example,
)
from v40_semantics import (
    canonical_semantic_action_key,
    validate_review_aggregation,
    validate_subject_identity,
)

ROOT = Path(__file__).resolve().parents[1]
GOLDEN = ROOT / "templates" / "golden" / "V4_OPERATION_ASSURANCE_EXAMPLES.json"


def base_findings() -> list[dict]:
    return [
        finding_example("F-P2-1", "P2", "covered"),
        finding_example("F-P3-1", "P3", "recorded"),
    ]


def resolved_blocker(finding_id: str, *, subject: str = SHA_A) -> dict:
    return {
        "protocol_version": "ai-dev/review-finding-v1",
        "finding_id": finding_id,
        "assurance_id": "review-a",
        "subject_identity_ref": f"sha:{subject}",
        "severity": "P1",
        "summary": "resolved replacement finding",
        "blocking": True,
        "status": "DISPOSITIONED",
        "disposition": "authorized resolution",
        "resolution_code": "FIXED",
        "evidence_refs": ["issue:#123"],
    }


def superseded_blocker(finding_id: str, target_id: str | None, *, subject: str = SHA_A) -> dict:
    finding = {
        "protocol_version": "ai-dev/review-finding-v1",
        "finding_id": finding_id,
        "assurance_id": "review-a",
        "subject_identity_ref": f"sha:{subject}",
        "severity": "P1",
        "summary": "superseded blocker",
        "blocking": True,
        "status": "SUPERSEDED",
        "disposition": "replaced by newer durable finding",
        "resolution_code": "SUPERSEDED",
        "evidence_refs": ["issue:#123"],
    }
    if target_id is not None:
        finding["superseded_by"] = target_id
    return finding


class V40FinalHardeningTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.examples = json.loads(GOLDEN.read_text(encoding="utf-8"))

    def test_duplicate_finding_identity_shadow_is_rejected(self) -> None:
        shadow = copy.deepcopy(self.examples["forbidden"]["duplicate_finding_identity_shadow"])
        aggregate = aggregation_example()
        aggregate["finding_refs"].append("F-SHADOW")
        errors = validate_review_aggregation(aggregate, base_findings() + shadow, plan=assurance_example())
        self.assertTrue(any("duplicate finding identities are forbidden: F-SHADOW" in e for e in errors), errors)

    def test_valid_supersession_can_resolve_old_blocker(self) -> None:
        replacement = resolved_blocker("F-NEW")
        old = superseded_blocker("F-OLD", "F-NEW")
        aggregate = aggregation_example()
        aggregate["finding_refs"] += ["F-OLD", "F-NEW"]
        self.assertEqual(validate_review_aggregation(aggregate, base_findings() + [old, replacement], plan=assurance_example()), [])

    def test_superseded_missing_linkage_and_target_fail_closed(self) -> None:
        for old in (superseded_blocker("F-OLD", None), superseded_blocker("F-OLD", "F-NOT-THERE")):
            aggregate = aggregation_example()
            aggregate["finding_refs"].append("F-OLD")
            errors = validate_review_aggregation(aggregate, base_findings() + [old], plan=assurance_example())
            self.assertTrue(errors)
            self.assertTrue(any("PASS forbidden" in e for e in errors), errors)

    def test_superseded_self_cross_subject_and_cycle_fail_closed(self) -> None:
        self_link = superseded_blocker("F-OLD", "F-OLD")
        aggregate = aggregation_example(); aggregate["finding_refs"].append("F-OLD")
        self.assertTrue(validate_review_aggregation(aggregate, base_findings() + [self_link], plan=assurance_example()))
        replacement = resolved_blocker("F-NEW", subject=SHA_B)
        old = superseded_blocker("F-OLD", "F-NEW")
        aggregate = aggregation_example(); aggregate["finding_refs"] += ["F-OLD", "F-NEW"]
        self.assertTrue(any("crosses subject identity" in e for e in validate_review_aggregation(aggregate, base_findings() + [old, replacement], plan=assurance_example())))
        a = superseded_blocker("F-A", "F-B"); b = superseded_blocker("F-B", "F-A")
        aggregate = aggregation_example(); aggregate["finding_refs"] += ["F-A", "F-B"]
        self.assertTrue(any("cycle" in e for e in validate_review_aggregation(aggregate, base_findings() + [a, b], plan=assurance_example())))

    def test_unresolved_supersession_replacement_remains_visible_blocker(self) -> None:
        replacement = resolved_blocker("F-NEW"); replacement["status"] = "OPEN"; replacement.pop("disposition")
        old = superseded_blocker("F-OLD", "F-NEW")
        aggregate = aggregation_example(); aggregate["finding_refs"] += ["F-OLD", "F-NEW"]
        errors = validate_review_aggregation(aggregate, base_findings() + [old, replacement], plan=assurance_example())
        self.assertTrue(any("PASS forbidden" in e for e in errors), errors)

    def test_event_v2_handoff_accepts_additive_correlation_fields(self) -> None:
        schema = load_schema("agent-event-v2.schema.json")
        event = {"schema":"ai-dev/event-v2","event":"HANDOFF_READY","actor_role":"reviewer","operator_kind":"chatgpt-web","operator_id":"web:reviewer","issue":"#123","sha":SHA_A,"evidence":"issue:#123","operation_id":"op:T009:hardening","exchange_id":"ex:T009:hardening","assurance_id":"review:T009:hardening","caused_by":"dispatch:T009:hardening"}
        self.assertEqual(validate_subset(event, schema), [])

    def test_semantic_action_key_changes_when_precondition_changes(self) -> None:
        base = copy.deepcopy(self.examples["valid"]["semantic_action"])
        changed = copy.deepcopy(base); changed["expected_precondition"] = {"candidate_state": "THAWED"}
        self.assertNotEqual(canonical_semantic_action_key(base), canonical_semantic_action_key(changed))

    def test_project_defined_identity_error_explains_nonweakening_failure(self) -> None:
        errors = validate_subject_identity(self.examples["forbidden"]["project_defined_weakens_exact_subject"])
        self.assertTrue(errors)
        self.assertTrue(any("weakens" in e or "missing sha" in e for e in errors), errors)


if __name__ == "__main__":
    unittest.main()
