from __future__ import annotations

from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
STANDARD = ROOT / "standards" / "OBSERVABILITY_RUNTIME_EVIDENCE_STANDARD.md"
REFERENCE = ROOT / "references" / "OBSERVABILITY_RUNTIME_REFERENCE.md"


class ObservabilityRuntimeEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.standard = STANDARD.read_text(encoding="utf-8")
        cls.reference = REFERENCE.read_text(encoding="utf-8")

    def test_deployment_success_is_not_runtime_health(self) -> None:
        self.assertIn("DEPLOYMENT_SUCCEEDED != RUNTIME_HEALTHY", self.standard)
        self.assertIn("Deployment succeeded -> runtime healthy", self.reference)

    def test_signal_dimensions_remain_distinct_and_extensible(self) -> None:
        for token in ("health/readiness", "liveness", "performance/resource", "error/failure", "business/domain"):
            self.assertIn(token, self.standard)
        self.assertIn("may map or extend signal classes", self.standard)

    def test_observation_binds_material_identity(self) -> None:
        for token in ("exact artifact/content identity", "deployment/result reference", "environment/tenant/account identity", "observation window/time reference"):
            self.assertIn(token, self.standard)
        self.assertIn("existing v4.4 artifact/deployment/environment identities", self.standard)

    def test_signal_availability_or_silence_is_not_health(self) -> None:
        self.assertIn("no alert observed != healthy", self.standard)
        self.assertIn("backend reachable != runtime healthy", self.standard)
        self.assertIn("Missing, quiet or unavailable telemetry MUST NOT be upgraded", self.standard)

    def test_sensitive_values_are_not_ordinary_evidence(self) -> None:
        for token in ("raw credentials", "tokens", "secrets", "unapproved PII"):
            self.assertIn(token, self.standard)
        self.assertIn("raw credential in log -> acceptable durable evidence", self.reference)

    def test_no_universal_stack_slo_or_result_authority(self) -> None:
        self.assertIn("does not mandate one telemetry vendor", self.standard)
        self.assertIn("does not create Validation PASS/FAIL, Release READY, Deployment result or Task state", self.standard)


if __name__ == "__main__":
    unittest.main()
