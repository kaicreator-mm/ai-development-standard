from __future__ import annotations

import json
from pathlib import Path
import re
import unittest

from test_protocol_schemas import validate_subset

ROOT = Path(__file__).resolve().parents[1]
STANDARD = ROOT / "standards" / "INCIDENT_RECOVERY_FEEDBACK_STANDARD.md"
REFERENCE = ROOT / "references" / "INCIDENT_RECOVERY_REFERENCE.md"
CONTRACT = ROOT / "schemas" / "incident-event-v1.schema.json"


def durable_routing(case: dict) -> bool:
    """Illustrative conformance oracle, NOT an incident/Task state engine."""
    if not case.get("classification_decision_ref"):
        return False
    disposition = case.get("classification_disposition")
    if disposition == "NO_ENGINEERING_WORK_WITH_RATIONALE":
        return bool(case.get("classification_owner_ref") and case.get("no_engineering_work_rationale_ref"))
    if disposition not in {"REQUIRED_ENGINEERING_WORK", "INVESTIGATION_PENDING"}:
        return False
    if not case.get("reproduction_ref"):
        return False
    if disposition == "REQUIRED_ENGINEERING_WORK" and case.get("classification_owner_ref") and case.get("engineering_work_item_ref"):
        return True
    # The explicit pending path is durable routing, not follow-up completion.
    missing_owner = not case.get("classification_owner_ref")
    missing_work = disposition == "REQUIRED_ENGINEERING_WORK" and not case.get("engineering_work_item_ref")
    if missing_owner and not case.get("unresolved_owner_assignment_obligation_ref"):
        return False
    if missing_work and not case.get("unresolved_work_item_creation_obligation_ref"):
        return False
    return bool(case.get("accountable_assignment_authority_ref") and case.get("next_routing_owner_ref"))


def follow_up_complete(case: dict) -> bool:
    """Completion claim requires owning references; service recovery is irrelevant."""
    if not durable_routing(case):
        return False
    disposition = case["classification_disposition"]
    if disposition == "NO_ENGINEERING_WORK_WITH_RATIONALE":
        return True
    if disposition == "INVESTIGATION_PENDING":
        return False
    return bool(
        case.get("classification_owner_ref")
        and case.get("engineering_work_item_ref")
        and case.get("engineering_work_verified_by_owner")
        and not case.get("unresolved_owner_assignment_obligation_ref")
        and not case.get("unresolved_work_item_creation_obligation_ref")
    )


def ordinary_evidence_safe(reference: str) -> bool:
    """Fixture negative guard; real privacy approval remains with v4.1 owner."""
    unsafe = (r"\bauthorization\s*:\s*bearer\b", r"[?&]token=", r"[?&]X-Amz-Signature=", r"\braw-secret:")
    return not any(re.search(item, reference, re.IGNORECASE) for item in unsafe)


class IncidentRecoveryFeedbackTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.standard = STANDARD.read_text(encoding="utf-8")
        cls.reference = REFERENCE.read_text(encoding="utf-8")
        cls.schema = json.loads(CONTRACT.read_text(encoding="utf-8"))

    def test_incident_history_is_append_oriented(self) -> None:
        self.assertIn("append-oriented incident facts", self.standard)
        self.assertIn("MUST preserve prior facts", self.standard)
        self.assertIn("later recovery event does not erase earlier failure evidence", self.standard)

    def test_incident_facts_are_not_collapsed(self) -> None:
        for token in ("DETECTED != MITIGATED", "RECOVERED != VERIFIED", "VERIFIED != FOLLOW_UP_COMPLETE"):
            self.assertIn(token, self.standard)

    def test_recovery_reuses_owning_authorities(self) -> None:
        for token in ("v4.4 Deployment Governance", "v4.2 Data/Migration Governance", "configuration/credential", "external-system mutation"):
            self.assertIn(token, self.standard)
        self.assertIn("incident does not grant that authority", self.reference)

    def test_recovery_requires_verification(self) -> None:
        self.assertIn("MUST NOT be treated as permanent-fix truth", self.standard)
        self.assertIn("service responds again != root cause fixed", self.standard)
        self.assertIn("rollback completed != corrective change verified", self.standard)

    def test_material_incident_routes_engineering_feedback(self) -> None:
        for token in ("reproducible defect/bug evidence", "regression or test scenario", "product/architecture decision", "standard/process gap"):
            self.assertIn(token, self.standard)
        self.assertIn("MUST preserve a durable reference", self.standard)
        for token in ("responsible classification/follow-up owner reference", "unresolved owner-assignment obligation", "unresolved work-item-creation obligation", "classification_disposition"):
            self.assertIn(token, self.standard + self.reference)

    def test_follow_up_routing_rejects_evidence_only_and_allows_explicit_pending(self) -> None:
        base = {"classification_disposition": "REQUIRED_ENGINEERING_WORK", "classification_decision_ref": "decision:42", "reproduction_ref": "redacted:42"}
        self.assertFalse(durable_routing(base))  # predecessor #382 P1 counterexample
        assigned = dict(base, classification_owner_ref="team:quality", engineering_work_item_ref="issue:42")
        self.assertTrue(durable_routing(assigned))
        self.assertFalse(follow_up_complete(assigned))  # no Task verification
        pending = dict(base, unresolved_owner_assignment_obligation_ref="pending:owner", unresolved_work_item_creation_obligation_ref="pending:task", accountable_assignment_authority_ref="team:triage", next_routing_owner_ref="team:triage")
        self.assertTrue(durable_routing(pending))
        self.assertFalse(follow_up_complete(pending))
        del pending["unresolved_work_item_creation_obligation_ref"]
        self.assertFalse(durable_routing(pending))
        assigned["engineering_work_verified_by_owner"] = True
        self.assertTrue(follow_up_complete(assigned))

    def test_investigation_pending_never_equates_to_no_engineering_work(self) -> None:
        pending = {"classification_disposition": "INVESTIGATION_PENDING", "classification_decision_ref": "decision:42", "reproduction_ref": "redacted:42", "classification_owner_ref": "team:triage", "accountable_assignment_authority_ref": "team:triage", "next_routing_owner_ref": "team:triage"}
        self.assertTrue(durable_routing(pending))
        self.assertFalse(follow_up_complete(pending))
        no_work = {"classification_disposition": "NO_ENGINEERING_WORK_WITH_RATIONALE", "classification_decision_ref": "decision:43", "classification_owner_ref": "team:quality", "no_engineering_work_rationale_ref": "decision:rationale"}
        self.assertTrue(follow_up_complete(no_work))
        del no_work["no_engineering_work_rationale_ref"]
        self.assertFalse(follow_up_complete(no_work))

    def test_existing_t01_incident_event_contract_accepts_example(self) -> None:
        required = {"incident_id", "event_id", "event_kind", "occurred_at", "runtime_subject_refs", "evidence_refs", "actor_or_authority_ref", "schema_version"}
        self.assertEqual(set(self.schema["required"]), required)
        payload = {"schema_version": 1, "incident_id": "incident-42", "event_id": "event-42-1", "event_kind": "DETECTED", "occurred_at": "2026-09-30T08:00:00Z", "runtime_subject_refs": ["artifact:sha256:example/env:staging"], "evidence_refs": ["evidence:redacted/42"], "actor_or_authority_ref": "owner:ops", "engineering_follow_up_refs": ["issue:42"]}
        self.assertEqual(validate_subset(payload, self.schema), [])
        self.assertIn("schemas/incident-event-v1.schema.json", self.standard)
        self.assertIn("schemas/incident-event-v1.schema.json", self.reference)

    def test_secret_bearing_evidence_is_forbidden_independent_of_shape(self) -> None:
        safe = "evidence:redacted/incident-042-summary"
        self.assertTrue(ordinary_evidence_safe(safe))
        self.assertIn("MUST NOT embed raw credentials", self.standard)
        for reference in ("Authorization: Bearer token-example", "https://internal.invalid/path?token=secret", "https://storage.invalid/key?X-Amz-Signature=example", "raw-secret:example"):
            with self.subTest(reference=reference):
                self.assertFalse(ordinary_evidence_safe(reference))
        self.assertIn("v4.1 Configuration/Secrets", self.standard)

    def test_closure_does_not_erase_follow_up_or_rewrite_prior_evidence(self) -> None:
        self.assertIn("Incident closure MUST NOT erase required unresolved follow-up", self.standard)
        self.assertIn("MUST NOT rewrite a prior exact Release/Deployment/Validation result", self.standard)
        self.assertIn("FOLLOW_UP_COMPLETE` MUST NOT be asserted", self.standard)


if __name__ == "__main__":
    unittest.main()
