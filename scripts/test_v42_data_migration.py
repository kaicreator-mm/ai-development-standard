from __future__ import annotations

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
STANDARD = ROOT / "standards" / "DATA_MIGRATION_GOVERNANCE_STANDARD.md"
REFERENCE = ROOT / "references" / "DATA_MIGRATION_REFERENCE.md"
SCHEMA = ROOT / "schemas" / "migration-transition-v1.schema.json"


class DataMigrationGovernanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.standard = STANDARD.read_text(encoding="utf-8")
        cls.reference = REFERENCE.read_text(encoding="utf-8")
        cls.schema = json.loads(SCHEMA.read_text(encoding="utf-8"))

    def test_source_target_direction_and_recovery_are_required(self) -> None:
        required = set(self.schema["required"])
        self.assertTrue({"source_state_ref", "target_state_ref", "applicability", "recovery"}.issubset(required))
        self.assertIn("A transition is directional: `A -> B` is not evidence for `B -> A`", self.standard)

    def test_fresh_upgrade_and_recovery_subjects_do_not_collapse(self) -> None:
        text = self.standard
        self.assertIn("fresh-install PASS **MUST NOT imply** upgrade PASS", text)
        self.assertIn("successful upgrade **MUST NOT imply** interrupted-recovery PASS", text)
        self.assertIn("one recovery strategy **MUST NOT imply** another strategy is valid", text)

    def test_applicability_preserves_runtime_database_environment_dimensions(self) -> None:
        applicability = self.schema["properties"]["applicability"]["properties"]
        self.assertIn("datastore_kind", applicability)
        self.assertIn("runtime_or_version", applicability)
        self.assertIn("environment_ref", applicability)
        self.assertIn("runtime/database/environment tuples", self.standard)
        self.assertIn("Staging success MUST NOT automatically become production transition evidence", self.standard)

    def test_migration_presence_is_not_execution(self) -> None:
        self.assertIn("migration file exists -> migration executed", self.standard)
        self.assertIn("migration definition/file exists", self.standard)
        self.assertIn("migration was executed", self.standard)
        self.assertIn("target state was verified", self.standard)

    def test_recovery_required_without_universal_down_migration(self) -> None:
        recovery = self.schema["properties"]["recovery"]
        self.assertEqual(set(recovery["required"]), {"strategy_class", "strategy_ref", "prerequisites"})
        self.assertNotIn("enum", recovery["properties"]["strategy_class"])
        self.assertIn("does **not** require every migration to provide an inverse migration", self.standard)
        self.assertIn("`no down migration -> no recovery strategy required` is forbidden", self.standard)

    def test_required_adversarial_inferences_are_rejected(self) -> None:
        required_rows = (
            "| fresh install succeeds | upgrade succeeds |",
            "| `A -> B` succeeds | `B -> A` succeeds |",
            "| migration file/definition exists | migration executed |",
            "| credentials/tool can mutate production | production mutation authorized |",
            "| no down migration exists | no recovery strategy is required |",
        )
        for row in required_rows:
            self.assertIn(row, self.standard)

    def test_production_authority_is_not_inferred_from_credentials(self) -> None:
        self.assertIn("Credential capability is never mutation authority", self.standard)
        self.assertIn("explicit applicable side-effect authority", self.standard)
        self.assertIn("Having `DATABASE_URL`, cloud credentials, or a migration tool installed proves capability only", self.reference)

    def test_fast_path_is_materiality_driven(self) -> None:
        self.assertIn("need not create empty migration records", self.standard)
        self.assertIn("MUST NOT bypass migration evidence", self.standard)

    def test_machine_contract_does_not_create_validation_or_deployment_state(self) -> None:
        props = self.schema["properties"]
        for forbidden in ("status", "pass", "validation_state", "deployment_state"):
            self.assertNotIn(forbidden, props)
        self.assertIn("does not define Validation PASS/FAIL or Deployment result state", self.standard)


if __name__ == "__main__":
    unittest.main()
