from __future__ import annotations

from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
STANDARD = ROOT / "standards" / "DEPLOYMENT_GOVERNANCE_STANDARD.md"
REFERENCE = ROOT / "references" / "DEPLOYMENT_REFERENCE.md"


class DeploymentGovernanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.standard = STANDARD.read_text(encoding="utf-8")
        cls.reference = REFERENCE.read_text(encoding="utf-8")

    def test_plan_and_result_are_separate(self) -> None:
        self.assertIn("Deployment Plan expresses intended action", self.standard)
        self.assertIn("They MUST remain separate durable subjects", self.standard)
        self.assertIn("Deployment Plan exists/approved -> Deployment succeeded", self.standard)

    def test_exact_artifact_environment_and_plan_identity(self) -> None:
        self.assertIn("exact artifact identity and exact material environment identity", self.standard)
        for field in ("plan_ref", "immutable_artifact_ref", "environment_ref"):
            self.assertIn(field, self.reference)

    def test_outcomes_are_namespaced_domain_facts(self) -> None:
        self.assertIn("namespaced `DEPLOYMENT_*` values", self.standard)
        self.assertIn("MUST NOT mint generic `PASS`, `READY`, Validation or Release states", self.standard)

    def test_release_ready_is_not_deployment_success(self) -> None:
        self.assertIn("Release READY != Deployment SUCCESS", self.standard)
        self.assertIn("publication success != deployment success", self.standard)

    def test_staging_does_not_imply_production(self) -> None:
        self.assertIn("staging success != production success", self.standard)
        self.assertIn("does not prove production success", self.reference)

    def test_credentials_do_not_create_side_effect_authority(self) -> None:
        self.assertIn("credential/tool capability != production mutation authority", self.standard)
        self.assertIn("does not demonstrate that the current Task/operator is authorized", self.reference)

    def test_rollback_boundaries_are_explicit(self) -> None:
        self.assertIn("artifact rollback != data/schema rollback", self.standard)
        self.assertIn("rollback plan exists != rollback executed", self.standard)
        self.assertIn("Data recovery/reversion remains governed by Data & Migration authority", self.standard)

    def test_mock_or_unavailable_environment_cannot_be_real_pass(self) -> None:
        self.assertIn("simulated provider response MUST NOT become real production Deployment success", self.standard)
        self.assertIn("BLOCKED/NOT_RUN", self.standard)


if __name__ == "__main__":
    unittest.main()
