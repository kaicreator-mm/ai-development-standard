from __future__ import annotations

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
STANDARD = ROOT / "standards" / "CONFIGURATION_SECRETS_STANDARD.md"
REFERENCE = ROOT / "references" / "CONFIGURATION_SECRETS_REFERENCE.md"
EXECUTION_CONTEXT_SCHEMA = ROOT / "schemas" / "execution-context-v1.schema.json"


def resolve_precedence(sources: list[tuple[int, str, str]]) -> str:
    """Return value from the highest explicit precedence rank."""
    return max(sources, key=lambda item: item[0])[2]


def credential_execution_state(*, required: bool, available: bool, authorized: bool) -> str:
    if not required:
        return "NOT_APPLICABLE"
    if not available or not authorized:
        return "BLOCKED"
    return "READY_TO_EXECUTE"


def contains_obvious_secret_value(record: dict) -> bool:
    forbidden = {"value", "token", "password", "secret", "private_key", "signed_url"}
    return any(key.lower() in forbidden for key in record)


class V41ConfigurationSecretsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.standard = STANDARD.read_text(encoding="utf-8")
        cls.reference = REFERENCE.read_text(encoding="utf-8")
        cls.execution_context = json.loads(EXECUTION_CONTEXT_SCHEMA.read_text(encoding="utf-8"))

    def test_precedence_is_deterministic_not_discovery_order(self) -> None:
        sources = [
            (10, "project-file", "us-east"),
            (30, "dispatch", "eu-west"),
            (20, "environment", "ap-southeast"),
        ]
        self.assertEqual(resolve_precedence(sources), "eu-west")
        self.assertIn("deterministic precedence", self.standard)
        self.assertIn("File discovery order is irrelevant", self.reference)

    def test_execution_context_secret_refs_have_no_value_field(self) -> None:
        secret_ref_props = (
            self.execution_context["properties"]["configuration"]["properties"]["secret_refs"]["items"]["properties"]
        )
        for forbidden in ("value", "token", "password", "private_key", "signed_url"):
            self.assertNotIn(forbidden, secret_ref_props)
        self.assertIn("refs/identity, never plaintext values", self.standard)

    def test_secret_value_shape_is_rejected_by_reference_semantics(self) -> None:
        self.assertFalse(contains_obvious_secret_value({"ref": "vault:path/key", "scope": "read"}))
        self.assertTrue(contains_obvious_secret_value({"ref": "vault:path/key", "token": "abc"}))
        self.assertIn("MUST NOT contain secret values", self.standard)
        self.assertIn("Bad durable record", self.reference)

    def test_unavailable_required_credential_is_blocked(self) -> None:
        self.assertEqual(credential_execution_state(required=True, available=False, authorized=False), "BLOCKED")
        self.assertEqual(credential_execution_state(required=True, available=True, authorized=False), "BLOCKED")
        self.assertEqual(credential_execution_state(required=False, available=False, authorized=False), "NOT_APPLICABLE")
        self.assertIn("execution MUST remain truthful", self.standard)
        self.assertIn("execution BLOCKED / check NOT_RUN", self.reference)

    def test_short_lived_credentials_preferred_but_static_not_prohibited(self) -> None:
        self.assertIn("Short-lived or just-in-time credentials are preferred", self.standard)
        self.assertIn("Static credentials remain permitted", self.standard)
        self.assertIn("not a universal requirement", self.reference)

    def test_no_universal_provider_is_mandated(self) -> None:
        for phrase in ("does not mandate one configuration file", "Vault", "OIDC", "Kubernetes Secrets"):
            self.assertIn(phrase, self.standard)
        self.assertIn("Another project may not use `.env` at all", self.reference)

    def test_encrypted_in_git_exception_is_bounded(self) -> None:
        for phrase in (
            "ciphertext is not directly usable",
            "key/decryption authority is separate",
            "not permission to commit plaintext",
        ):
            self.assertIn(phrase, self.standard)

    def test_redaction_and_least_privilege_are_explicit(self) -> None:
        self.assertIn("minimum practical", self.standard)
        self.assertIn("MUST avoid echoing secret values", self.standard)
        self.assertIn("credential_ref=ci:sandbox-A/write-token", self.reference)


if __name__ == "__main__":
    unittest.main()
