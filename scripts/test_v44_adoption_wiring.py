from __future__ import annotations

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "standard-manifest.json"
COVERAGE = ROOT / "templates/golden/STANDARD_COVERAGE.json"
OVERRIDES = ROOT / "templates/project/.dev-standard/PROJECT_OVERRIDES.md"
ADOPTION = ROOT / "standards/PROJECT_ADOPTION.md"
MIGRATION = ROOT / "docs/implementation/4.4.0/MIGRATION_ADOPTION.md"

OWNERS = (
    "BUILD_ARTIFACT_GOVERNANCE_STANDARD",
    "DISTRIBUTION_GOVERNANCE_STANDARD",
    "DEPLOYMENT_GOVERNANCE_STANDARD",
)
SCHEMAS = (
    "build-manifest-v1.schema.json",
    "artifact-promotion-v1.schema.json",
    "deployment-plan-v1.schema.json",
    "deployment-result-v1.schema.json",
)
FOCUSED = (
    "test_v44_shared_delivery_contracts.py",
    "test_v44_build_artifact.py",
    "test_v44_distribution.py",
    "test_v44_deployment.py",
    "test_v44_adoption_wiring.py",
)


def presence_only_is_not_proof(*, artifact_promoted: bool, publication_recorded: bool, plan_exists: bool, execution_evidence: bool, exact_target: bool, actual_authority: bool) -> bool:
    """Test-only negative oracle; never issues Deployment or Release verdicts."""
    return bool(artifact_promoted and publication_recorded and plan_exists and execution_evidence and exact_target and actual_authority)


class V44AdoptionWiringTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.sections = json.loads(MANIFEST.read_text(encoding="utf-8"))["sections"]
        cls.coverage = json.loads(COVERAGE.read_text(encoding="utf-8"))["coverage"]
        cls.overrides = OVERRIDES.read_text(encoding="utf-8")
        cls.adoption = ADOPTION.read_text(encoding="utf-8")
        cls.migration = MIGRATION.read_text(encoding="utf-8")

    def test_v44_three_normative_owners_and_references_discoverable(self) -> None:
        for owner in OWNERS:
            with self.subTest(owner=owner):
                std = f"standards/{owner}.md"
                ref = f"references/{owner.removesuffix('_STANDARD')}_REFERENCE.md"
                # The three reference names are deliberately owner-specific.
                if owner == "BUILD_ARTIFACT_GOVERNANCE_STANDARD":
                    ref = "references/BUILD_ARTIFACT_REFERENCE.md"
                elif owner == "DISTRIBUTION_GOVERNANCE_STANDARD":
                    ref = "references/DISTRIBUTION_REFERENCE.md"
                elif owner == "DEPLOYMENT_GOVERNANCE_STANDARD":
                    ref = "references/DEPLOYMENT_REFERENCE.md"
                self.assertIn(std, self.sections["normative_standards"])
                self.assertIn(ref, self.sections["references"])
                self.assertTrue((ROOT / std).is_file())
                self.assertTrue((ROOT / ref).is_file())

    def test_four_t01_machine_contracts_are_references_not_new_authority(self) -> None:
        for schema in SCHEMAS:
            rel = f"schemas/{schema}"
            with self.subTest(schema=rel):
                self.assertIn(rel, self.sections["machine_contracts"])
                self.assertTrue((ROOT / rel).is_file())
        self.assertNotIn("schemas/distribution-result-v1.schema.json", self.sections["machine_contracts"])

    def test_owner_and_t07_focused_scripts_discoverable(self) -> None:
        for filename in FOCUSED:
            rel = f"scripts/{filename}"
            self.assertIn(rel, self.sections["verification"])
            self.assertTrue((ROOT / rel).is_file())

    def test_golden_exact_one_row_for_every_active_normative_standard(self) -> None:
        normative = self.sections["normative_standards"]
        coverage_paths = [item["standard"] for item in self.coverage]
        self.assertEqual(len(normative), len(set(normative)))
        self.assertEqual(len(coverage_paths), len(set(coverage_paths)))
        self.assertEqual(set(normative), set(coverage_paths))
        for item in self.coverage:
            for key in ("golden_ref", "forbidden_ref", "rationale_ref"):
                rel = item[key].split("#", 1)[0]
                self.assertTrue((ROOT / rel).is_file(), f"{item['standard']} missing {key}: {rel}")

    def test_new_owner_golden_examples_reference_existing_sections(self) -> None:
        new_rows = [r for r in self.coverage if r["standard"] in {f"standards/{x}.md" for x in OWNERS}]
        self.assertEqual(len(new_rows), 3)
        for row in new_rows:
            self.assertTrue(row["golden_ref"].startswith("references/"))
            self.assertIn("#", row["golden_ref"])
            self.assertIn("#", row["forbidden_ref"])
            self.assertIn("#", row["rationale_ref"])

    def test_project_profile_is_materiality_driven_and_non_weakening(self) -> None:
        for field in ("v4.delivery.build", "v4.delivery.packaging", "v4.delivery.distribution", "v4.delivery.deployment"):
            self.assertIn(field, self.overrides)
        for token in ("NOT_APPLICABLE", "NOT_RUN", "BLOCKED", "Fast Path", "MUST NOT weaken"):
            self.assertIn(token, self.overrides + "\n" + self.migration)
        self.assertIn("standards/PROJECT_ADOPTION.md", self.migration + "\n" + self.adoption + "\n" + self.overrides)

    def test_adoption_and_closure_do_not_claim_unexecuted_result(self) -> None:
        for token in ("Release READY != Deployment SUCCESS", "NOT_RUN", "BLOCKED", "Version Closure"):
            self.assertIn(token, self.migration)
        self.assertFalse(presence_only_is_not_proof(artifact_promoted=True, publication_recorded=True, plan_exists=True,
                                                  execution_evidence=False, exact_target=True, actual_authority=True))
        self.assertFalse(presence_only_is_not_proof(artifact_promoted=True, publication_recorded=True, plan_exists=True,
                                                  execution_evidence=True, exact_target=False, actual_authority=True))
        self.assertFalse(presence_only_is_not_proof(artifact_promoted=True, publication_recorded=True, plan_exists=True,
                                                  execution_evidence=True, exact_target=True, actual_authority=False))
        # True means these illustrative prerequisites exist, not Deployment/Release PASS.
        self.assertTrue(presence_only_is_not_proof(artifact_promoted=True, publication_recorded=True, plan_exists=True,
                                                 execution_evidence=True, exact_target=True, actual_authority=True))


if __name__ == "__main__":
    unittest.main()
