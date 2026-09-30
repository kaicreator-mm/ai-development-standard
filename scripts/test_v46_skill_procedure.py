from __future__ import annotations

import json
from pathlib import Path
import unittest

from test_protocol_schemas import validate_subset

ROOT = Path(__file__).resolve().parents[1]
STANDARD = ROOT / "standards" / "SKILL_PROCEDURE_GOVERNANCE_STANDARD.md"
REFERENCE = ROOT / "references" / "SKILL_PROCEDURE_REFERENCE.md"
SCHEMA = ROOT / "schemas" / "skill-metadata-v1.schema.json"


def sample_skill(**changes: object) -> dict:
    result = {
        "schema_version": 1,
        "skill_id": "example.dependency-review",
        "skill_version": "1.2.0",
        "purpose": "Read-only dependency review",
        "scope": "task-selected sources only",
        "applicability": "project approval required",
        "source_ref": "repo:example@exact-sha",
        "procedure_ref": "repo:example@exact-sha/procedure.md",
        "failure_escalation_ref": "issue:task-42#owner",
        "maintenance_owner_ref": "team:tools",
        "tool_capability_refs": ["filesystem-read"],
        "side_effect_classes": [],
        "required_authority_refs": ["task-pack:42"],
        "validation_refs": ["fixture-eval:exact-version"],
    }
    result.update(changes)
    return result


def material_invocation_allowed(
    *,
    project_accepted_current_version: bool,
    provenance_trusted: bool,
    current_task_scope_authorized: bool,
    current_dispatch_authorized: bool,
    actual_side_effect_authorized: bool,
    requested_version_compatible: bool,
    sensitive_input_policy_satisfied: bool,
    authority_conflict: bool,
) -> bool:
    """Test-only bounded decision oracle; it issues no real authorization."""
    return (
        project_accepted_current_version
        and provenance_trusted
        and current_task_scope_authorized
        and current_dispatch_authorized
        and actual_side_effect_authorized
        and requested_version_compatible
        and sensitive_input_policy_satisfied
        and not authority_conflict
    )


class SkillProcedureGovernanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.standard = STANDARD.read_text(encoding="utf-8")
        cls.reference = REFERENCE.read_text(encoding="utf-8")
        cls.schema = json.loads(SCHEMA.read_text(encoding="utf-8"))

    def valid_invocation(self, **changes: bool) -> bool:
        conditions = {
            "project_accepted_current_version": True,
            "provenance_trusted": True,
            "current_task_scope_authorized": True,
            "current_dispatch_authorized": True,
            "actual_side_effect_authorized": True,
            "requested_version_compatible": True,
            "sensitive_input_policy_satisfied": True,
            "authority_conflict": False,
        }
        conditions.update(changes)
        return material_invocation_allowed(**conditions)

    def test_existing_t01_schema_accepts_minimal_and_reference_example(self) -> None:
        self.assertEqual(validate_subset(sample_skill(), self.schema), [])
        text = self.reference
        example = text.split("```json\n", 1)[1].split("\n```", 1)[0]
        self.assertEqual(validate_subset(json.loads(example), self.schema), [])
        self.assertEqual(self.schema["$id"].split("/")[-1], "skill-metadata-v1.schema.json")

    def test_missing_required_identity_owner_and_unknown_authority_grant_rejected(self) -> None:
        for required in ("skill_id", "skill_version", "source_ref", "procedure_ref", "failure_escalation_ref", "maintenance_owner_ref"):
            with self.subTest(required=required):
                item = sample_skill()
                item.pop(required)
                self.assertNotEqual(validate_subset(item, self.schema), [])
        self.assertNotEqual(validate_subset(sample_skill(mutation_authorized=True), self.schema), [])

    def test_installed_is_not_trusted_even_with_correct_shape(self) -> None:
        self.assertEqual(validate_subset(sample_skill(), self.schema), [])
        self.assertFalse(self.valid_invocation(project_accepted_current_version=False))
        self.assertFalse(self.valid_invocation(provenance_trusted=False))
        self.assertIn("installed != trusted", self.standard)

    def test_tool_capability_and_valid_token_cannot_grant_side_effects(self) -> None:
        capable = sample_skill(tool_capability_refs=["cloud-deploy"], side_effect_classes=["production-deploy"])
        self.assertEqual(validate_subset(capable, self.schema), [])
        self.assertFalse(self.valid_invocation(actual_side_effect_authorized=False))
        self.assertFalse(self.valid_invocation(current_dispatch_authorized=False))
        self.assertIn("allowed tool capability != side-effect authorization", self.standard)

    def test_skill_instruction_cannot_override_task_or_frozen_authority(self) -> None:
        self.assertFalse(self.valid_invocation(current_task_scope_authorized=False))
        self.assertFalse(self.valid_invocation(authority_conflict=True))
        self.assertIn("Skill says to edit path X != Task Pack permits X", self.standard)
        self.assertIn("Reject that instruction", self.reference)

    def test_one_off_task_exception_does_not_become_reusable_policy(self) -> None:
        self.assertIn("one-off Task decision MUST remain", self.standard)
        self.assertIn("Do not copy its exception", self.reference)
        self.assertFalse(self.valid_invocation(current_task_scope_authorized=False))

    def test_incompatible_version_fails_closed_even_if_installed(self) -> None:
        self.assertEqual(validate_subset(sample_skill(skill_version="3.0.0"), self.schema), [])
        self.assertFalse(self.valid_invocation(requested_version_compatible=False))
        self.assertIn("cannot silently inherit prior acceptance", self.standard)

    def test_secret_policy_and_prompt_injection_do_not_change_authority(self) -> None:
        self.assertFalse(self.valid_invocation(sensitive_input_policy_satisfied=False))
        self.assertFalse(self.valid_invocation(authority_conflict=True))
        self.assertIn("Never embed project credentials", self.standard)
        self.assertIn("prompt injection", self.standard)

    def test_evidence_refs_and_non_applicable_skill_do_not_issue_gate_pass(self) -> None:
        self.assertEqual(validate_subset(sample_skill(validation_refs=["historical:pass"]), self.schema), [])
        self.assertFalse(self.valid_invocation(project_accepted_current_version=False))
        self.assertIn("do not prove", self.standard)
        self.assertIn("Fast Path never bypasses", self.standard)
        self.assertIn("validation_refs", self.schema["properties"])

    def test_only_three_task_owned_surfaces_and_no_parallel_lifecycle(self) -> None:
        for forbidden in ("workflow_state", "release_pass", "deployment_authorized", "context_snapshot"):
            self.assertNotIn(forbidden, self.schema["properties"])
        self.assertIn("only v4.6 default Skill machine-contract family", self.standard)
        self.assertIn("not a new global state machine", self.reference)


if __name__ == "__main__":
    unittest.main()
