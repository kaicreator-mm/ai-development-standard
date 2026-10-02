from __future__ import annotations

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "standard-manifest.json"
COVERAGE = ROOT / "templates" / "golden" / "STANDARD_COVERAGE.json"
EXAMPLES = ROOT / "templates" / "golden" / "STANDARD_CONFORMANCE_EXAMPLES.md"
ANTI = ROOT / "templates" / "golden" / "ANTI_PATTERNS.md"
OVERRIDES = ROOT / "templates" / "project" / ".dev-standard" / "PROJECT_OVERRIDES.md"
MIGRATION = ROOT / "docs" / "implementation" / "4.2.0" / "MIGRATION_ADOPTION.md"

STANDARDS = {
    "standards/INTERFACE_COMPATIBILITY_GOVERNANCE_STANDARD.md": "interface-compatibility-governance-standard",
    "standards/DATA_MIGRATION_GOVERNANCE_STANDARD.md": "data-migration-governance-standard",
}


class V42AdoptionWiringTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        cls.coverage = json.loads(COVERAGE.read_text(encoding="utf-8"))
        cls.examples = EXAMPLES.read_text(encoding="utf-8")
        cls.anti = ANTI.read_text(encoding="utf-8")
        cls.overrides = OVERRIDES.read_text(encoding="utf-8")
        cls.migration = MIGRATION.read_text(encoding="utf-8")

    def test_v42_normative_and_machine_assets_are_discoverable(self) -> None:
        sections = self.manifest["sections"]
        for standard in STANDARDS:
            self.assertIn(standard, sections["normative_standards"])
        self.assertIn("schemas/compatibility-record-v1.schema.json", sections["machine_contracts"])
        self.assertIn("schemas/migration-transition-v1.schema.json", sections["machine_contracts"])
        self.assertIn("references/INTERFACE_COMPATIBILITY_REFERENCE.md", sections["references"])
        self.assertIn("references/DATA_MIGRATION_REFERENCE.md", sections["references"])
        self.assertIn("scripts/test_v42_interface_compatibility.py", sections["verification"])
        self.assertIn("scripts/test_v42_data_migration.py", sections["verification"])
        self.assertIn("scripts/test_v42_adoption_wiring.py", sections["verification"])

    def test_each_v42_standard_has_exactly_one_golden_coverage_record(self) -> None:
        records = self.coverage["coverage"]
        for standard, anchor in STANDARDS.items():
            matched = [item for item in records if item["standard"] == standard]
            self.assertEqual(len(matched), 1)
            record = matched[0]
            self.assertEqual(record["golden_ref"], f"templates/golden/STANDARD_CONFORMANCE_EXAMPLES.md#{anchor}")
            self.assertTrue(record["forbidden_ref"])
            self.assertTrue(record["rationale_ref"])
            self.assertIn(f"## {anchor}", self.examples)

    def test_golden_guidance_contains_required_non_inferences(self) -> None:
        for phrase in (
            "wire-safe",
            "new/new",
            "fresh install",
            "migration file exists",
            "Deployment success",
            "historical evidence",
        ):
            self.assertIn(phrase, self.examples + self.anti + self.migration)

    def test_project_override_profile_is_materiality_driven_and_non_weakening(self) -> None:
        text = self.overrides
        self.assertIn("Evolution Governance Profile", text)
        self.assertIn("evolution.compatibility", text)
        self.assertIn("evolution.migration", text)
        self.assertIn("materiality-driven", text)
        self.assertIn("MUST NOT weaken", text)
        self.assertIn("Deployment", text)

    def test_historical_evidence_is_not_retroactively_rewritten(self) -> None:
        self.assertIn("historical v4 payloads and evidence retain their original subject identity and meaning", self.migration)
        self.assertIn("MUST NOT be relabeled", self.migration)
        self.assertIn("new exact SHA", self.migration)

    def test_fast_path_does_not_force_empty_evolution_records(self) -> None:
        self.assertIn("need not create empty v4.2 records", self.migration)
        self.assertIn("Fast Path reduces non-material ceremony", self.migration)

    def test_v42_does_not_absorb_deployment_or_result_authority(self) -> None:
        self.assertIn("Deployment rollout/result semantics remain outside v4.2", self.migration)
        self.assertIn("v4.4 Deployment owner", self.migration)
        self.assertIn("Validation PASS != Release READY", self.migration)

    def test_discovery_and_golden_surfaces_do_not_grant_mutation_authority(self) -> None:
        self.assertIn("second semantic owner or mutation authority", self.migration)
        self.assertIn("do not grant mutation authority", self.migration)
        self.assertNotIn("templates/GOLDEN_INDEX.md", self.manifest["sections"]["verification"])


if __name__ == "__main__":
    unittest.main()
