from __future__ import annotations

import json
from pathlib import Path
import re
import unittest

from test_protocol_schemas import validate_subset

ROOT = Path(__file__).resolve().parents[1]
STANDARD = ROOT / "standards" / "INTENT_ASSUMPTION_GOVERNANCE_STANDARD.md"
REFERENCE = ROOT / "references" / "INTENT_ASSUMPTION_REFERENCE.md"
SCHEMA = ROOT / "schemas" / "intent-assumption-record-v1.schema.json"
DISPATCH = ROOT / "schemas" / "dispatch.schema.json"
EXECUTION = ROOT / "schemas" / "execution-pack-manifest.schema.json"


def sample_record(**changes: object) -> dict:
    record = {
        "schema_version": 1,
        "record_id": "intent-sample",
        "repository": "example/project",
        "subject_ref": "issue:42",
        "classification": "INTERPRETATION",
        "content_ref": "evidence:approved-summary",
        "source_ref": "issue:42#comment-1",
        "evidence_refs": ["evidence:approved-summary"],
        "materiality": "MATERIAL",
        "currentness_ref": "issue:42@observed-sha",
        "disposition": {"action": "CLARIFY", "target_ref": "issue:product-decision-47"},
        "created_by_ref": "agent:analyst",
        "created_at": "2026-09-30T08:00:00Z",
    }
    record.update(changes)
    return record


def promotion_proven(record: dict, *, actual_owner_issued: bool, current_target: bool, contradictions_resolved: bool) -> bool:
    """Test-only evidence gate; cannot perform or issue Product/Task promotions."""
    return all((
        record.get("classification") == "DURABLE_REQUIREMENT_REF",
        bool(record.get("promotion_authority_ref")),
        bool(record.get("promoted_requirement_ref")),
        bool(record.get("source_ref")),
        bool(record.get("currentness_ref")),
        actual_owner_issued,
        current_target,
        contradictions_resolved,
    ))


def user_statement_proven(record: dict, *, original_user_source_verified: bool) -> bool:
    return (record.get("classification") == "USER_INTENT"
            and bool(record.get("source_ref")) and original_user_source_verified)


def material_routing_admissible(record: dict) -> bool:
    """Test-only syntactic routing check; DOES NOT prove owner/currentness truth."""
    action = record["disposition"]["action"]
    if record["materiality"] == "UNKNOWN":
        return action == "BLOCK"
    if action in {"CLARIFY", "PROMOTE_BY_OWNER", "SUPERSEDE"}:
        if not record["disposition"].get("target_ref"):
            return False
        if action == "SUPERSEDE" and not record.get("supersedes_refs"):
            return False
    if record.get("contradiction_refs") and action not in {"BLOCK", "CLARIFY", "SUPERSEDE"}:
        return False
    return True


def supersession_proven(record: dict, *, actual_owner_issued: bool,
                        current_replacement: bool, contradictions_resolved: bool) -> bool:
    """Test-only independent evidence gate, never a real owner-issued decision.

    A syntactically present target_ref and supersedes_refs cannot prove a
    real, current owner-issued replacement or resolve material contradiction.
    """
    return all((
        record.get("disposition", {}).get("action") == "SUPERSEDE",
        material_routing_admissible(record),
        bool(record.get("source_ref")),
        bool(record.get("currentness_ref")),
        actual_owner_issued,
        current_replacement,
        contradictions_resolved,
    ))


class IntentAssumptionGovernanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.standard = STANDARD.read_text(encoding="utf-8")
        cls.reference = REFERENCE.read_text(encoding="utf-8")
        cls.schema = json.loads(SCHEMA.read_text(encoding="utf-8"))

    def test_only_existing_six_truth_classes_and_six_wire_actions(self) -> None:
        classes = self.schema["properties"]["classification"]["enum"]
        self.assertEqual(classes, ["USER_INTENT", "INTERPRETATION", "ASSUMPTION", "UNKNOWN", "DECISION_REQUIRED", "DURABLE_REQUIREMENT_REF"])
        actions = self.schema["properties"]["disposition"]["properties"]["action"]["enum"]
        self.assertEqual(actions, ["RETAIN", "CLARIFY", "PROMOTE_BY_OWNER", "REJECT", "SUPERSEDE", "BLOCK"])
        self.assertNotIn("ROUTE", actions)
        self.assertNotIn("PROMOTE_REF", actions)
        self.assertIn("not extra machine enum values", self.standard)

    def test_material_routing_needs_real_destination_and_prior_fact(self) -> None:
        clarify = sample_record()
        self.assertEqual(validate_subset(clarify, self.schema), [])
        self.assertTrue(material_routing_admissible(clarify))
        self.assertFalse(material_routing_admissible(sample_record(disposition={"action": "CLARIFY"})))
        promote_request = sample_record(classification="ASSUMPTION", disposition={"action": "PROMOTE_BY_OWNER", "target_ref": "issue:owner"})
        self.assertTrue(material_routing_admissible(promote_request))
        self.assertFalse(promotion_proven(promote_request, actual_owner_issued=False, current_target=False, contradictions_resolved=True))
        self.assertFalse(material_routing_admissible(sample_record(disposition={"action": "SUPERSEDE", "target_ref": "record:new"})))
        syntactic_successor = sample_record(disposition={"action": "SUPERSEDE", "target_ref": "record:new"}, supersedes_refs=["record:old"])
        self.assertTrue(material_routing_admissible(syntactic_successor))
        self.assertFalse(supersession_proven(syntactic_successor, actual_owner_issued=False,
                                             current_replacement=False, contradictions_resolved=True))
        self.assertTrue(material_routing_admissible(sample_record(classification="UNKNOWN", materiality="UNKNOWN", disposition={"action": "BLOCK"})))
        self.assertFalse(material_routing_admissible(sample_record(classification="UNKNOWN", materiality="UNKNOWN")))

    def test_real_user_statement_is_not_agent_interpretation_or_product_freeze(self) -> None:
        interpretation = sample_record()
        self.assertFalse(user_statement_proven(interpretation, original_user_source_verified=True))
        user = sample_record(classification="USER_INTENT")
        self.assertFalse(user_statement_proven(user, original_user_source_verified=False))
        self.assertTrue(user_statement_proven(user, original_user_source_verified=True))
        self.assertIn("is not automatically Frozen Product", self.standard)
        self.assertIn("not the user's actual sentence", self.reference)

    def test_missing_either_promotion_ref_is_rejected_by_actual_schema(self) -> None:
        accepted_shape = sample_record(classification="DURABLE_REQUIREMENT_REF", disposition={"action": "RETAIN"},
                                       promotion_authority_ref="owner:product-47", promoted_requirement_ref="product:req-47")
        self.assertEqual(validate_subset(accepted_shape, self.schema), [])
        for missing in ("promotion_authority_ref", "promoted_requirement_ref"):
            with self.subTest(missing=missing):
                candidate = dict(accepted_shape)
                del candidate[missing]
                self.assertTrue(validate_subset(candidate, self.schema))
                self.assertFalse(promotion_proven(candidate, actual_owner_issued=True, current_target=True, contradictions_resolved=True))

    def test_reject_invented_authority_fields_through_real_schema(self) -> None:
        accepted = sample_record(classification="DURABLE_REQUIREMENT_REF", disposition={"action": "RETAIN"},
                                 promotion_authority_ref="owner:product-47", promoted_requirement_ref="product:req-47")
        self.assertEqual(validate_subset(accepted, self.schema), [])
        for forbidden in ("product_authority_granted", "may_mutate_frozen_product"):
            with self.subTest(forbidden=forbidden):
                invented = dict(accepted)
                invented[forbidden] = True
                self.assertTrue(validate_subset(invented, self.schema))
        self.assertFalse(self.schema["additionalProperties"])

    def test_reference_shaped_promotions_do_not_create_authority(self) -> None:
        ref = sample_record(classification="DURABLE_REQUIREMENT_REF", disposition={"action": "RETAIN"},
                            promotion_authority_ref="example:owner", promoted_requirement_ref="example:req")
        self.assertEqual(validate_subset(ref, self.schema), [])
        cases = (
            (False, True, True),  # agent-invented owner refs
            (True, False, True),  # stale target requirement
            (True, True, False), # unresolved material contradiction
        )
        for issued, current, resolved in cases:
            with self.subTest(issued=issued, current=current, resolved=resolved):
                self.assertFalse(promotion_proven(ref, actual_owner_issued=issued, current_target=current, contradictions_resolved=resolved))
        self.assertTrue(promotion_proven(ref, actual_owner_issued=True, current_target=True, contradictions_resolved=True))
        self.assertIn("Structurally valid references alone do not prove", self.standard)

    def test_assumption_and_unknown_never_self_promote(self) -> None:
        for truth_class in ("ASSUMPTION", "UNKNOWN", "INTERPRETATION", "USER_INTENT", "DECISION_REQUIRED"):
            with self.subTest(truth_class=truth_class):
                candidate = sample_record(classification=truth_class, disposition={"action": "PROMOTE_BY_OWNER", "target_ref": "issue:owner"},
                                          promotion_authority_ref="agent:invented", promoted_requirement_ref="agent:invented")
                self.assertEqual(validate_subset(candidate, self.schema), [])
                self.assertFalse(promotion_proven(candidate, actual_owner_issued=False, current_target=False, contradictions_resolved=True))
        self.assertIn("MUST NOT self-promote", self.standard)

    def test_conflict_cannot_be_guessed_or_erased(self) -> None:
        unresolved = sample_record(contradiction_refs=["record:conflict"], disposition={"action": "RETAIN"})
        self.assertFalse(material_routing_admissible(unresolved))
        self.assertTrue(material_routing_admissible(sample_record(contradiction_refs=["record:conflict"], disposition={"action": "BLOCK"})))
        self.assertIn("preserve `contradiction_refs`", self.standard)
        self.assertIn("not silent promotion", self.reference)

    def test_guessed_or_stale_supersession_cannot_resolve_contradiction(self) -> None:
        guessed = sample_record(contradiction_refs=["record:conflict"], supersedes_refs=["record:old"],
                                disposition={"action": "SUPERSEDE", "target_ref": "agent:guessed"})
        self.assertEqual(validate_subset(guessed, self.schema), [])
        self.assertTrue(material_routing_admissible(guessed))  # only shape, NOT authority
        for issued, current, resolved in ((False, True, True), (True, False, True), (True, True, False)):
            with self.subTest(issued=issued, current=current, resolved=resolved):
                self.assertFalse(supersession_proven(guessed, actual_owner_issued=issued,
                                                    current_replacement=current, contradictions_resolved=resolved))
        verified_fixture = sample_record(contradiction_refs=["record:conflict"], supersedes_refs=["record:old"],
                                         disposition={"action": "SUPERSEDE", "target_ref": "owner:current-replacement"})
        self.assertTrue(supersession_proven(verified_fixture, actual_owner_issued=True,
                                           current_replacement=True, contradictions_resolved=True))
        self.assertFalse(supersession_proven(sample_record(contradiction_refs=["record:conflict"],
                                disposition={"action": "SUPERSEDE", "target_ref": "owner:current-replacement"}),
                                actual_owner_issued=True, current_replacement=True, contradictions_resolved=True))
        self.assertIn("If the successor or authority is UNKNOWN, `BLOCK`", self.standard)

    def test_l2_conceptual_to_wire_mapping_preserves_owner_chain(self) -> None:
        for phrase in ("`ROUTE`", "`CLARIFY`", "`PROMOTE_REF`", "`PROMOTE_BY_OWNER`", "`SUPERSEDE_REF`", "`SUPERSEDE`", "actual current decision", "disposition.target_ref"):
            self.assertIn(phrase, self.standard)
        self.assertIn("actual owner-issued target", self.reference)
        self.assertIn("not proof of promotion", self.standard)

    def test_legacy_optional_refs_and_no_new_state_authority(self) -> None:
        dispatch = json.loads(DISPATCH.read_text(encoding="utf-8"))
        execution = json.loads(EXECUTION.read_text(encoding="utf-8"))
        for schema in (dispatch, execution):
            for optional_field in ("intent_assumption_refs", "skill_metadata_refs"):
                with self.subTest(schema=schema["title"], field=optional_field):
                    self.assertIn(optional_field, schema["properties"])
                    self.assertNotIn(optional_field, schema["required"])
            self.assertNotIn("intent_assumption_record_refs", schema["properties"])
        self.assertIn("`intent_assumption_refs` remain valid", self.standard)
        base_sha = "a" * 40
        legacy_dispatch = {
            "dispatch_id": "old-dispatch", "repository": "example/project", "version": "4.5.0",
            "task": "T-001", "role": "builder", "execution_profile": "LOCAL_BUILDER",
            "branch": "task/legacy", "expected_base_sha": base_sha,
            "pinned_standard_revision": base_sha, "agent_freedom": "F1_BOUNDED_IMPLEMENTATION",
            "dispatch_state": "READY", "task_pack_ref": "docs/task-pack.md",
        }
        legacy_execution = {
            "pack_id": "old-execution", "task_id": "T-001", "repository": "example/project",
            "version": "4.5.0", "base_sha": base_sha, "task_pack_ref": "docs/task-pack.md",
            "branch": "task/legacy", "agent_freedom": "F1_BOUNDED_IMPLEMENTATION",
            "pinned_standard_revision": base_sha, "generated_by": "example:agent",
            "generated_at": "2026-09-30T08:00:00Z",
            "core_artifacts": ["MANIFEST.yaml", "EXECUTION_CONTRACT.md", "TEST_MATRIX.yaml",
                               "FAILURE_MATRIX.yaml", "IMPLEMENTATION_MAP.md", "REVIEW_CHECKLIST.md"],
            "retention": "durable",
        }
        self.assertEqual(validate_subset(legacy_dispatch, dispatch), [])
        self.assertEqual(validate_subset(legacy_execution, execution), [])
        self.assertIn("historical", self.standard.lower())
        self.assertIn("does not", self.standard.lower())

    def test_reference_example_validates_against_t01_contract(self) -> None:
        samples = re.findall(r"```json\n(.*?)\n```", self.reference, flags=re.DOTALL)
        self.assertGreaterEqual(len(samples), 2)
        for raw in samples:
            with self.subTest(example=raw[:25]):
                self.assertEqual(validate_subset(json.loads(raw), self.schema), [])


if __name__ == "__main__":
    unittest.main()
