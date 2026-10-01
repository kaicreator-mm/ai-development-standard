"""T06 fixture-only conformance; no external incident/recovery side effects.

Run: python -m unittest discover -s scripts -p test_v45_incident_feedback_conformance.py -v
The tests consume the merged T01 schema and T03 owner oracle, not a new policy.
"""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import re
import unittest

from test_protocol_schemas import validate_subset
from test_v45_incident_recovery_feedback import durable_routing, follow_up_complete

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "docs/implementation/4.5.0/dogfood/incident-feedback/controlled-incident.json"
SCHEMA = ROOT / "schemas/incident-event-v1.schema.json"
OWNER = ROOT / "standards/INCIDENT_RECOVERY_FEEDBACK_STANDARD.md"

# Only a fixture-level guard. v4.1/project-specific privacy approval remains authoritative.
SENSITIVE = re.compile(
    r"authorization\s*:\s*bearer|(?:[?&](?:token|access_token|x-amz-signature)=)|"
    r"raw-secret:|BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY|"
    r"(?:email|phone|ssn|password|api[_-]?key)\s*[:=]\s*[^\s,}]+",
    re.IGNORECASE,
)


def fixture_errors(case: dict, schema: dict) -> list[str]:
    """Check one bounded exercise; never claim to implement the incident owner."""
    errors: list[str] = []
    if case.get("classification") != "SYNTHETIC_FIXTURE_ONLY":
        errors.append("unrecognized execution classification")
    events = case.get("events", [])
    if not events:
        return errors + ["missing append-only events"]
    immutable = case.get("baseline_evidence", {})
    expected_keys = {"deployment_result_ref", "deployment_result_digest", "release_result_ref", "release_result_digest"}
    if not expected_keys <= immutable.keys() or any(not immutable.get(k) for k in expected_keys):
        errors.append("missing historical immutable reference/digest")
    if "historical_evidence_after" in case and case["historical_evidence_after"] != immutable:
        errors.append("prior release/deployment evidence rewritten")
    subject = case.get("subject")
    authority = {a.get("ref"): a for a in case.get("authorized_simulated_actions", [])}
    seen: set[str] = set()
    previous = ""
    kinds: list[str] = []
    for event in events:
        errors.extend(f"event schema {event.get('event_id', '?')}: {err}" for err in validate_subset(event, schema))
        event_id = event.get("event_id")
        if not event_id or event_id in seen:
            errors.append("missing/duplicate immutable event ID")
        seen.add(event_id)
        if event.get("incident_id") != events[0].get("incident_id"):
            errors.append("incident identity drift")
        if event.get("runtime_subject_refs") != [subject]:
            errors.append("runtime subject drift")
        timestamp = event.get("occurred_at", "")
        if not timestamp or timestamp <= previous:
            errors.append("event order/time invalid")
        previous = timestamp
        kinds.append(event.get("event_kind", ""))
        for ref_field in ("mitigation_action_refs", "recovery_action_refs"):
            for ref in event.get(ref_field, []):
                action = authority.get(ref)
                if (not action or action.get("kind") != "FIXTURE_ONLY"
                        or action.get("authority_ref") != event.get("actor_or_authority_ref")):
                    errors.append("missing or wrong recovery/mitigation authority")
        if SENSITIVE.search(json.dumps(event)):
            errors.append("sensitive incident evidence")
        if set(event) & {"release_result", "deployment_result", "validation_result"}:
            errors.append("incident cannot mutate prior owner result")
    sequence = ["DETECTED", "MITIGATED", "RECOVERED", "VERIFIED", "FOLLOW_UP_CREATED"]
    if kinds != sequence:
        errors.append("missing or out-of-order distinct lifecycle fact")
    if not events[3].get("evidence_refs"):
        errors.append("verification has no evidence")
    follow_up = case.get("follow_up", {})
    if not durable_routing(follow_up):
        errors.append("material follow-up routing unresolved")
    if not follow_up.get("regression_scenario_ref"):
        errors.append("escaped defect lacks durable regression scenario")
    if follow_up.get("engineering_work_item_ref") not in events[-1].get("engineering_follow_up_refs", []):
        errors.append("follow-up event lacks work-item link")
    if follow_up.get("completion_claim") and not follow_up_complete(follow_up):
        errors.append("premature follow-up completion")
    if SENSITIVE.search(json.dumps(follow_up)):
        errors.append("sensitive follow-up evidence")
    request = case.get("validation_request", {})
    if request.get("execution") != "NOT_RUN" or request.get("gate") != "BLOCKED":
        errors.append("fixture improperly asserts real host validation")
    if not request.get("scope") or not request.get("reason"):
        errors.append("required host handoff lacks scope/reason")
    return errors


class IncidentFeedbackConformanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.case = json.loads(FIXTURE.read_text(encoding="utf-8"))
        cls.schema = json.loads(SCHEMA.read_text(encoding="utf-8"))

    def check_rejected(self, change: callable, token: str) -> None:
        case = deepcopy(self.case)
        change(case)
        errors = fixture_errors(case, self.schema)
        self.assertTrue(any(token in error for error in errors), errors)

    def test_positive_fixture_event_sequence_and_durable_follow_up(self) -> None:
        self.assertEqual(fixture_errors(self.case, self.schema), [])
        self.assertTrue(durable_routing(self.case["follow_up"]))
        self.assertFalse(follow_up_complete(self.case["follow_up"]))
        self.assertEqual(self.case["validation_request"]["execution"], "NOT_RUN")

    def test_missing_verification_cannot_infer_verified_from_recovered(self) -> None:
        self.check_rejected(lambda c: c["events"].pop(3), "distinct lifecycle fact")

    def test_verification_without_proof_is_not_verified(self) -> None:
        self.check_rejected(lambda c: c["events"][3].update(evidence_refs=[]), "verification has no evidence")

    def test_missing_classification_or_owner_or_work_item_fails(self) -> None:
        for key in ("classification_decision_ref", "classification_owner_ref", "engineering_work_item_ref"):
            with self.subTest(key=key):
                self.check_rejected(lambda c, k=key: c["follow_up"].pop(k), "follow-up routing")

    def test_unresolved_follow_up_cannot_claim_complete(self) -> None:
        self.check_rejected(lambda c: c["follow_up"].update(completion_claim=True), "premature follow-up")

    def test_wrong_or_unapproved_recovery_authority_fails_closed(self) -> None:
        self.check_rejected(lambda c: c["events"][2].update(actor_or_authority_ref="fixture-actor:intruder"), "wrong recovery")
        self.check_rejected(lambda c: c["authorized_simulated_actions"].clear(), "wrong recovery")

    def test_prior_release_deployment_evidence_is_immutable(self) -> None:
        self.check_rejected(lambda c: c.update(historical_evidence_after={"release_result_ref": "replaced"}), "rewritten")
        self.check_rejected(lambda c: c["events"][2].update(release_result="REVERSED"), "incident cannot mutate")

    def test_secret_pii_references_rejected(self) -> None:
        for value in ("Authorization: Bearer fixture-secret", "https://fixture.invalid/x?token=fake",
                      "email:private@example.invalid", "raw-secret:fake"):
            with self.subTest(value=value):
                self.check_rejected(lambda c, v=value: c["events"][0]["evidence_refs"].append(v), "sensitive")

    def test_no_real_runtime_validation_claim(self) -> None:
        self.check_rejected(lambda c: c["validation_request"].update(execution="PASS", gate="PASS"), "improperly asserts")

    def test_consume_frozen_incident_owner_not_new_policy(self) -> None:
        text = OWNER.read_text(encoding="utf-8")
        for invariant in ("RECOVERED != VERIFIED", "VERIFIED != FOLLOW_UP_COMPLETE",
                          "v4.4 Deployment Governance", "v4.2 Data/Migration Governance"):
            self.assertIn(invariant, text)


if __name__ == "__main__":
    unittest.main()
