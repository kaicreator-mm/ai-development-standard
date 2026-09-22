from __future__ import annotations

import unittest

from test_protocol_schemas import load_schema, validate_subset
from v34_rules import (
    classify_pack_staleness,
    core_artifacts_complete,
    validator_result_matches_dispatch,
)

SHA_A = "a" * 40
SHA_B = "b" * 40
SHA_C = "c" * 40

CORE = [
    "MANIFEST.yaml",
    "EXECUTION_CONTRACT.md",
    "TEST_MATRIX.yaml",
    "FAILURE_MATRIX.yaml",
    "IMPLEMENTATION_MAP.md",
    "REVIEW_CHECKLIST.md",
]


def manifest(**overrides):
    value = {
        "pack_id": "pack-T002-1",
        "task_id": "T-002",
        "repository": "kaicreator-mm/ai-development-standard",
        "version": "3.4.0",
        "base_sha": SHA_A,
        "task_pack_ref": "task-pack:T-002@1",
        "branch": "task/v3.4.0-t002",
        "agent_freedom": "F1_BOUNDED_IMPLEMENTATION",
        "pinned_standard_revision": SHA_C,
        "generated_by": "chatgpt-web:web-a",
        "generated_at": "2026-09-22T00:00:00Z",
        "dependency_completion": [f"T-001@{SHA_B}"],
        "material_paths": ["schemas/", "standards/", "scripts/"],
        "core_artifacts": list(CORE),
        "retention": "durable",
    }
    value.update(overrides)
    return value


def facts(**overrides):
    value = {
        "current_integration_sha": SHA_A,
        "task_pack_ref": "task-pack:T-002@1",
        "branch": "task/v3.4.0-t002",
        "pinned_standard_revision": SHA_C,
        "dependency_completion": [f"T-001@{SHA_B}"],
        "delta_paths": [],
    }
    value.update(overrides)
    return value


def validator_dispatch(**overrides):
    value = {
        "dispatch_id": "validator-001",
        "repository": "kaicreator-mm/ai-development-standard",
        "version": "3.4.0",
        "task": "T-005",
        "role": "validator",
        "execution_profile": "LOCAL_VALIDATOR",
        "branch": "task/example",
        "expected_base_sha": SHA_A,
        "requested_head_sha": SHA_B,
        "validation_profile": "platform",
        "pinned_standard_revision": SHA_C,
        "agent_freedom": "F0_MECHANICAL",
        "dispatch_state": "RUNNING",
        "claimed_by": "codex:validator-01",
    }
    value.update(overrides)
    return value


def validation_report(**overrides):
    value = {
        "repository": "kaicreator-mm/ai-development-standard",
        "version": "3.4.0",
        "task": "T-005",
        "issue": "#59",
        "pr": "#58",
        "dispatch_id": "validator-001",
        "tested_sha": SHA_B,
        "expected_base_sha": SHA_A,
        "requested_sha": SHA_B,
        "actual_checked_out_sha": SHA_B,
        "current_pr_head": SHA_B,
        "working_tree_clean": True,
        "source_modifications_after_validation": False,
        "execution_host_role": "local-validator",
        "platform": "linux-x86_64",
        "runtime_toolchain": "python-3.12",
        "validation_profile": "platform",
        "command": "python scripts/test_v34_review_repairs.py",
        "exit_code": 0,
        "state": "PASS",
    }
    value.update(overrides)
    return value


class ExecutionPackRepairTests(unittest.TestCase):
    def test_schema_wire_shape_interoperates_with_classifier(self) -> None:
        schema = load_schema("execution-pack-manifest.schema.json")
        value = manifest()
        self.assertEqual(validate_subset(value, schema), [])
        self.assertEqual(classify_pack_staleness(value, facts()), "PACK_CURRENT")
        self.assertEqual(
            classify_pack_staleness(
                value,
                facts(current_integration_sha=SHA_C, delta_paths=["README.md"]),
            ),
            "PACK_STALE_NONMATERIAL",
        )

    def test_dependency_identity_drift_is_material(self) -> None:
        self.assertEqual(
            classify_pack_staleness(
                manifest(),
                facts(dependency_completion=[f"T-001@{SHA_C}"]),
            ),
            "PACK_STALE_MATERIAL",
        )

    def test_missing_material_coverage_fails_closed_on_base_drift(self) -> None:
        no_material = manifest()
        del no_material["material_paths"]
        self.assertEqual(
            classify_pack_staleness(
                no_material,
                facts(current_integration_sha=SHA_C, delta_paths=["README.md"]),
            ),
            "PACK_STALE_MATERIAL",
        )
        self.assertEqual(
            classify_pack_staleness(
                manifest(material_paths=[]),
                facts(current_integration_sha=SHA_C, delta_paths=["README.md"]),
            ),
            "PACK_STALE_MATERIAL",
        )

    def test_malformed_dependency_wire_shape_fails_closed(self) -> None:
        schema = load_schema("execution-pack-manifest.schema.json")
        malformed = manifest(dependency_completion=["T-001:not-a-sha"])
        self.assertTrue(validate_subset(malformed, schema))
        self.assertEqual(classify_pack_staleness(malformed, facts()), "PACK_INVALID")

    def test_core_artifacts_semantic_completeness_rejects_duplicates(self) -> None:
        self.assertTrue(core_artifacts_complete(CORE))
        duplicated = ["MANIFEST.yaml"] * 6
        self.assertFalse(core_artifacts_complete(duplicated))
        self.assertEqual(
            classify_pack_staleness(manifest(core_artifacts=duplicated), facts()),
            "PACK_INVALID",
        )


class ValidatorEvidenceRepairTests(unittest.TestCase):
    def test_dispatched_report_requires_exact_identity_fields(self) -> None:
        schema = load_schema("validation-report.schema.json")
        valid = validation_report()
        self.assertEqual(validate_subset(valid, schema), [])
        for field in (
            "expected_base_sha",
            "requested_sha",
            "actual_checked_out_sha",
            "current_pr_head",
            "working_tree_clean",
            "source_modifications_after_validation",
        ):
            invalid = dict(valid)
            del invalid[field]
            with self.subTest(field=field):
                self.assertTrue(validate_subset(invalid, schema), invalid)

    def test_legacy_non_dispatch_report_remains_compatible(self) -> None:
        schema = load_schema("validation-report.schema.json")
        value = validation_report()
        for field in (
            "dispatch_id",
            "expected_base_sha",
            "requested_sha",
            "actual_checked_out_sha",
            "current_pr_head",
            "working_tree_clean",
            "source_modifications_after_validation",
        ):
            value.pop(field, None)
        self.assertEqual(validate_subset(value, schema), [])

    def test_queue_consumption_requires_dispatch_identity_match(self) -> None:
        dispatch = validator_dispatch()
        report = validation_report()
        self.assertTrue(validator_result_matches_dispatch(dispatch, report))

        loose_pass = dict(report)
        loose_pass.pop("dispatch_id")
        self.assertFalse(validator_result_matches_dispatch(dispatch, loose_pass))

        for field, wrong in (
            ("requested_sha", SHA_C),
            ("actual_checked_out_sha", SHA_C),
            ("current_pr_head", SHA_C),
            ("expected_base_sha", SHA_C),
            ("validation_profile", "other"),
        ):
            with self.subTest(field=field):
                self.assertFalse(
                    validator_result_matches_dispatch(dispatch, dict(report, **{field: wrong}))
                )


if __name__ == "__main__":
    unittest.main()
