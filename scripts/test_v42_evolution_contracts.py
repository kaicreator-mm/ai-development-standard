from __future__ import annotations

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
COMPAT = ROOT / "schemas" / "compatibility-record-v1.schema.json"
MIGRATION = ROOT / "schemas" / "migration-transition-v1.schema.json"
VALIDATION = ROOT / "schemas" / "validation-report.schema.json"


class V42EvolutionContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.compat = json.loads(COMPAT.read_text(encoding="utf-8"))
        cls.migration = json.loads(MIGRATION.read_text(encoding="utf-8"))
        cls.validation = json.loads(VALIDATION.read_text(encoding="utf-8"))

    def test_schemas_declare_draft_2020_12(self) -> None:
        for schema in (self.compat, self.migration, self.validation):
            self.assertEqual(schema["$schema"], "https://json-schema.org/draft/2020-12/schema")

    def test_compatibility_requires_exact_subject_sides(self) -> None:
        required = set(self.compat["required"])
        self.assertTrue({"baseline", "candidate", "contract"}.issubset(required))
        identity_required = set(self.compat["$defs"]["subject_identity"]["required"])
        self.assertIn("sha_or_digest", identity_required)

    def test_change_operation_and_outcome_are_orthogonal(self) -> None:
        props = self.compat["properties"]
        self.assertIn("change_operations", props)
        self.assertIn("dimensions", props)
        outcomes = props["dimensions"]["items"]["properties"]["outcome"]["enum"]
        self.assertEqual(
            outcomes,
            ["COMPATIBLE", "CONDITIONALLY_COMPATIBLE", "INCOMPATIBLE", "UNKNOWN", "NOT_APPLICABLE"],
        )
        self.assertNotIn("PASS", outcomes)
        self.assertNotIn("FAIL", outcomes)

    def test_dimensions_are_extensible_and_absence_has_no_default_pass(self) -> None:
        dimension = self.compat["properties"]["dimensions"]["items"]
        self.assertEqual(dimension["properties"]["name"]["type"], "string")
        self.assertNotIn("enum", dimension["properties"]["name"])
        self.assertNotIn("default", dimension["properties"]["outcome"])
        self.assertIn("dimensions", self.compat["required"])

    def test_migration_is_directional_and_has_no_gate_state(self) -> None:
        required = set(self.migration["required"])
        self.assertTrue({"source_state_ref", "target_state_ref", "recovery"}.issubset(required))
        props = self.migration["properties"]
        for forbidden in ("state", "status", "pass", "result"):
            self.assertNotIn(forbidden, props)

    def test_recovery_does_not_require_down_migration(self) -> None:
        recovery = self.migration["properties"]["recovery"]
        self.assertEqual(set(recovery["required"]), {"strategy_class", "strategy_ref", "prerequisites"})
        strategy = recovery["properties"]["strategy_class"]
        self.assertEqual(strategy["type"], "string")
        self.assertNotIn("enum", strategy)
        self.assertNotIn("down_migration", recovery["required"])

    def test_applicability_preserves_runtime_environment_dimensions_without_owning_them(self) -> None:
        applicability = self.migration["properties"]["applicability"]["properties"]
        self.assertIn("datastore_kind", applicability)
        self.assertIn("runtime_or_version", applicability)
        self.assertIn("environment_ref", applicability)
        self.assertNotIn("provider_state", applicability)

    def test_validation_report_adds_only_optional_record_references(self) -> None:
        props = self.validation["properties"]
        self.assertEqual(props["compatibility_record_refs"]["type"], "array")
        self.assertEqual(props["migration_transition_refs"]["type"], "array")
        required = set(self.validation["required"])
        self.assertNotIn("compatibility_record_refs", required)
        self.assertNotIn("migration_transition_refs", required)
        historical_required = {
            "repository",
            "tested_sha",
            "execution_host_role",
            "platform",
            "runtime_toolchain",
            "validation_profile",
            "command",
            "state",
        }
        self.assertTrue(historical_required.issubset(required))


if __name__ == "__main__":
    unittest.main()
