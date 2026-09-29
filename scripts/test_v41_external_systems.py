from __future__ import annotations

from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
STANDARD = ROOT / "standards" / "EXTERNAL_SYSTEM_EXECUTION_STANDARD.md"
REFERENCE = ROOT / "references" / "EXTERNAL_SYSTEM_EXECUTION_REFERENCE.md"

FIDELITY_ORDER = {
    "mock": 0,
    "simulation": 1,
    "local-real": 2,
    "sandbox": 3,
    "staging": 4,
    "production": 5,
}


def fidelity_satisfies(actual: str, required: str) -> bool:
    return FIDELITY_ORDER[actual] >= FIDELITY_ORDER[required]


def side_effect_satisfies(*, actual: str, required: str) -> bool:
    if required == "read":
        return actual in {"read", "write"}
    return actual == "write"


def external_execution_state(*, available: bool, authorized: bool, executed: bool, product_failure: bool = False) -> str:
    if not available or not authorized:
        return "BLOCKED"
    if not executed:
        return "NOT_RUN"
    return "FAIL" if product_failure else "PASS"


def retry_allowed(*, attempts: int, max_attempts: int, idempotent: bool, deduplicated: bool) -> bool:
    if attempts >= max_attempts:
        return False
    return idempotent or deduplicated


class V41ExternalSystemTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.standard = STANDARD.read_text(encoding="utf-8")
        cls.reference = REFERENCE.read_text(encoding="utf-8")

    def test_lower_fidelity_does_not_satisfy_higher_fidelity(self) -> None:
        self.assertFalse(fidelity_satisfies("mock", "sandbox"))
        self.assertFalse(fidelity_satisfies("sandbox", "production"))
        self.assertTrue(fidelity_satisfies("production", "production"))
        self.assertIn("MUST NOT satisfy an unexecuted higher-fidelity requirement", self.standard)
        self.assertIn("Invalid escalation", self.reference)

    def test_read_only_evidence_does_not_prove_write_journey(self) -> None:
        self.assertFalse(side_effect_satisfies(actual="read", required="write"))
        self.assertTrue(side_effect_satisfies(actual="write", required="write"))
        self.assertIn("Read-only access does not prove a write journey", self.standard)

    def test_environment_and_tenant_identity_prevents_substitution(self) -> None:
        self.assertIn("Evidence from environment A MUST NOT be substituted for environment B", self.standard)
        self.assertIn("tenant=customer-sandbox-A", self.reference)
        self.assertIn("tenant=customer-sandbox-B", self.reference)

    def test_infrastructure_unavailability_is_blocked_not_product_fail(self) -> None:
        self.assertEqual(external_execution_state(available=False, authorized=True, executed=False), "BLOCKED")
        self.assertEqual(external_execution_state(available=True, authorized=False, executed=False), "BLOCKED")
        self.assertEqual(external_execution_state(available=True, authorized=True, executed=False), "NOT_RUN")
        self.assertIn("DNS/network/TLS connectivity unavailable", self.standard)
        self.assertIn("not automatically product defects", self.reference)

    def test_valid_executed_product_failure_remains_fail(self) -> None:
        self.assertEqual(
            external_execution_state(available=True, authorized=True, executed=True, product_failure=True),
            "FAIL",
        )
        self.assertIn("real product FAIL", self.reference)

    def test_retries_are_bounded_and_write_retries_require_safety(self) -> None:
        self.assertTrue(retry_allowed(attempts=0, max_attempts=3, idempotent=True, deduplicated=False))
        self.assertFalse(retry_allowed(attempts=3, max_attempts=3, idempotent=True, deduplicated=False))
        self.assertFalse(retry_allowed(attempts=0, max_attempts=3, idempotent=False, deduplicated=False))
        self.assertTrue(retry_allowed(attempts=0, max_attempts=3, idempotent=False, deduplicated=True))
        self.assertIn("Retries MUST be bounded", self.standard)
        self.assertIn("retry forever until green", self.reference)

    def test_provider_taxonomy_is_extensible_not_universal(self) -> None:
        self.assertIn("not a closed universal enum", self.standard)
        self.assertIn("semantic clarity, not a fixed global enum", self.reference)

    def test_credential_reference_not_value_and_write_authority_are_distinct(self) -> None:
        self.assertIn("credential **reference**, not the secret value", self.standard)
        self.assertIn("A credential capable of writing does not by itself authorize a write", self.standard)

    def test_validation_state_owner_is_preserved(self) -> None:
        self.assertIn("`VALIDATION_STANDARD.md` remains authoritative", self.standard)
        self.assertIn("MUST NOT", self.standard)
        self.assertIn("create a new Validation state vocabulary", self.standard)


if __name__ == "__main__":
    unittest.main()
