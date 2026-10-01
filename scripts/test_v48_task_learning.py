from __future__ import annotations

import copy
import unittest

from test_protocol_schemas import assert_supported_schema, load_schema, validate_subset


SCHEMA = load_schema("task-learning-v1.schema.json")
SUBJECT_A = "git:kaicreator-mm/example@1111111111111111111111111111111111111111"
SUBJECT_B = "git:kaicreator-mm/example@2222222222222222222222222222222222222222"


def valid_learning() -> dict:
    return {
        "schema_version": "ai-dev/task-learning-v1",
        "learning_id": "learning:T-001:001",
        "repository_ref": "github:kaicreator-mm/ai-development-standard",
        "work_item_ref": "github:kaicreator-mm/ai-development-standard#507",
        "implementation_subject_ref": SUBJECT_A,
        "authority_refs": [
            "task-pack:v4.8.0/T-001",
            "l2:f88c85454e80101a0fdf56050e21f11a05279841",
        ],
        "summary": "Exact-subject learning records reusable contract facts without changing authority.",
        "rationale_summary": "Exact identity prevents stale evidence from silently rebinding successor code.",
        "reusable_invariant_refs": ["L2#task-learning-currentness"],
        "known_limitation_refs": ["not-validation-authority"],
        "source_test_validation_review_refs": [
            "test:test_v48_task_learning#positive",
            "validation:pending-exact-head",
        ],
        "confidence_layers": ["IDENTITY_BOUND"],
        "currentness_ref": SUBJECT_A,
        "disposition": "RETAIN_LOCAL",
    }


def learning_applies_to_subject(learning: dict, current_subject_ref: str) -> bool:
    """Reference currentness rule: exact-subject claims never inherit across drift."""
    subject = learning.get("implementation_subject_ref")
    currentness = learning.get("currentness_ref")
    if subject is None or currentness is None:
        return False
    return subject == current_subject_ref == currentness


class TaskLearningSchemaTests(unittest.TestCase):
    def test_schema_uses_repository_supported_subset(self) -> None:
        assert_supported_schema(SCHEMA)

    def test_material_learning_positive(self) -> None:
        self.assertEqual(validate_subset(valid_learning(), SCHEMA), [])

    def test_none_material_fast_path_does_not_use_empty_record(self) -> None:
        self.assertTrue(validate_subset({}, SCHEMA))

    def test_private_chain_of_thought_field_is_rejected(self) -> None:
        value = valid_learning()
        value["chain_of_thought"] = "private reasoning"
        self.assertTrue(validate_subset(value, SCHEMA))

    def test_authority_substitution_fields_are_rejected(self) -> None:
        for field in ("product_authority", "review_result", "validation_result", "task_state"):
            with self.subTest(field=field):
                value = valid_learning()
                value[field] = "PASS"
                self.assertTrue(validate_subset(value, SCHEMA))

    def test_missing_evidence_or_authority_binding_fails_closed(self) -> None:
        for field in ("authority_refs", "source_test_validation_review_refs", "work_item_ref"):
            with self.subTest(field=field):
                value = valid_learning()
                del value[field]
                self.assertTrue(validate_subset(value, SCHEMA))

    def test_stale_exact_subject_is_historical_only(self) -> None:
        value = valid_learning()
        self.assertTrue(learning_applies_to_subject(value, SUBJECT_A))
        self.assertFalse(learning_applies_to_subject(value, SUBJECT_B))
        stale = copy.deepcopy(value)
        stale["currentness_ref"] = SUBJECT_B
        self.assertFalse(learning_applies_to_subject(stale, SUBJECT_A))
        self.assertFalse(learning_applies_to_subject(stale, SUBJECT_B))

    def test_confidence_layers_are_bounded(self) -> None:
        value = valid_learning()
        value["confidence_layers"] = ["GLOBAL_TRUTH"]
        self.assertTrue(validate_subset(value, SCHEMA))

    def test_friction_classification_is_frozen_but_disposition_is_not_governance_authority(self) -> None:
        value = valid_learning()
        value["friction_classification"] = "AUTO_STANDARD_CHANGE"
        self.assertTrue(validate_subset(value, SCHEMA))
        value = valid_learning()
        value["disposition"] = ""
        self.assertTrue(validate_subset(value, SCHEMA))


if __name__ == "__main__":
    unittest.main()
