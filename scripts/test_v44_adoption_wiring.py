from __future__ import annotations

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

OWNERS = {
    "standards/BUILD_ARTIFACT_GOVERNANCE_STANDARD.md": "references/BUILD_ARTIFACT_REFERENCE.md",
    "standards/DISTRIBUTION_GOVERNANCE_STANDARD.md": "references/DISTRIBUTION_REFERENCE.md",
    "standards/DEPLOYMENT_GOVERNANCE_STANDARD.md": "references/DEPLOYMENT_REFERENCE.md",
}
CONTRACTS = {
    "schemas/build-manifest-v1.schema.json",
    "schemas/artifact-promotion-v1.schema.json",
    "schemas/deployment-plan-v1.schema.json",
    "schemas/deployment-result-v1.schema.json",
}
TESTS = {
    "scripts/test_v44_delivery_contracts.py",
    "scripts/test_v44_build_artifact.py",
    "scripts/test_v44_distribution.py",
    "scripts/test_v44_deployment.py",
    "scripts/test_v44_distribution_deployment_conformance.py",
    "scripts/test_v44_adoption_wiring.py",
}


def deployment_prerequisites_visible(*, artifact_promoted: bool, published: bool,
                                    plan_exists: bool, executed: bool,
                                    exact_environment: bool, side_effect_authorized: bool) -> bool:
    """Test-only illustrative prerequisite conjunction, never a real deployment/Release PASS."""
    return all((artifact_promoted, published, plan_exists, executed, exact_environment,
                side_effect_authorized))


class V44AdoptionWiringTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.sections = json.loads((ROOT / "standard-manifest.json").read_text(encoding="utf-8"))["sections"]
        cls.coverage = json.loads((ROOT / "templates/golden/STANDARD_COVERAGE.json").read_text(encoding="utf-8"))["coverage"]
        cls.overrides = (ROOT / "templates/project/.dev-standard/PROJECT_OVERRIDES.md").read_text(encoding="utf-8")
        cls.migration = (ROOT / "docs/implementation/4.4.0/MIGRATION_ADOPTION.md").read_text(encoding="utf-8")

    def test_exact_three_normative_owners_and_reference_discovery(self) -> None:
        for owner, reference in OWNERS.items():
            with self.subTest(owner=owner):
                self.assertIn(owner, self.sections["normative_standards"])
                self.assertIn(reference, self.sections["references"])
                self.assertTrue((ROOT / owner).is_file())
                self.assertTrue((ROOT / reference).is_file())

    def test_four_existing_delivery_contracts_and_actual_t01_owner_test(self) -> None:
        for rel in CONTRACTS:
            self.assertIn(rel, self.sections["machine_contracts"])
            self.assertTrue((ROOT / rel).is_file())
        self.assertNotIn("schemas/distribution-result-v1.schema.json", self.sections["machine_contracts"])
        for rel in TESTS:
            self.assertIn(rel, self.sections["verification"])
            self.assertTrue((ROOT / rel).is_file())

    def test_exact_golden_coverage_and_existing_positive_negative_rationale_refs(self) -> None:
        active = self.sections["normative_standards"]
        coverage_paths = [row["standard"] for row in self.coverage]
        self.assertEqual(len(active), len(set(active)))
        self.assertEqual(len(coverage_paths), len(set(coverage_paths)))
        self.assertEqual(set(active), set(coverage_paths))
        for row in self.coverage:
            for field in ("golden_ref", "forbidden_ref", "rationale_ref"):
                path = row[field].split("#", 1)[0]
                self.assertTrue((ROOT / path).is_file(), f"{row['standard']} {field}: {path}")
        for owner in OWNERS:
            row = next(item for item in self.coverage if item["standard"] == owner)
            self.assertTrue(row["golden_ref"].startswith("references/"))
            self.assertTrue(all("#" in row[key] for key in ("golden_ref", "forbidden_ref", "rationale_ref")))

    def test_materiality_driven_project_profile_and_nondeployed_fast_path(self) -> None:
        for key in ("v4.delivery.build", "v4.delivery.packaging", "v4.delivery.distribution", "v4.delivery.deployment"):
            self.assertIn(key, self.overrides)
        for term in ("NOT_APPLICABLE", "NOT_RUN", "BLOCKED", "Fast Path", "MUST NOT weaken"):
            self.assertIn(term, self.overrides + self.migration)

    def test_no_fake_deployment_or_release_conclusion(self) -> None:
        for term in ("Release READY != Deployment SUCCESS", "Version Closure", "NOT_RUN", "BLOCKED"):
            self.assertIn(term, self.migration)
        arguments = dict(artifact_promoted=True, published=True, plan_exists=True,
                         executed=True, exact_environment=True, side_effect_authorized=True)
        self.assertTrue(deployment_prerequisites_visible(**arguments))
        for missing in ("executed", "exact_environment", "side_effect_authorized"):
            variant = {**arguments, missing: False}
            self.assertFalse(deployment_prerequisites_visible(**variant))


if __name__ == "__main__":
    unittest.main()
