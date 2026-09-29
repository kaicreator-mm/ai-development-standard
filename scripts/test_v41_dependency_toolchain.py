from __future__ import annotations

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
STANDARD = ROOT / "standards" / "DEPENDENCY_TOOLCHAIN_GOVERNANCE_STANDARD.md"
REFERENCE = ROOT / "references" / "DEPENDENCY_TOOLCHAIN_REFERENCE.md"
PROFILE_SCHEMA = ROOT / "schemas" / "dependency-toolchain-profile-v1.schema.json"
EXCEPTION_SCHEMA = ROOT / "schemas" / "dependency-risk-exception-v1.schema.json"


def dependency_change_requires_impact(delta: dict[str, bool]) -> bool:
    material_keys = {
        "runtime_resolution_changed",
        "lock_changed",
        "registry_changed",
        "toolchain_requirement_changed",
        "generated_output_changed",
        "class_or_exposure_changed",
    }
    return any(bool(delta.get(key)) for key in material_keys)


def risk_disposition(*, dependency_class: str, exposure: str, applicability: str) -> dict[str, str]:
    return {
        "dependency_class": dependency_class,
        "exposure": exposure,
        "applicability": applicability,
    }


class V41DependencyToolchainTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.standard = STANDARD.read_text(encoding="utf-8")
        cls.reference = REFERENCE.read_text(encoding="utf-8")
        cls.profile = json.loads(PROFILE_SCHEMA.read_text(encoding="utf-8"))
        cls.exception = json.loads(EXCEPTION_SCHEMA.read_text(encoding="utf-8"))

    def test_standard_preserves_distinct_toolchain_dimensions(self) -> None:
        for phrase in (
            "compatibility requirement",
            "supported line(s)",
            "preferred development version",
            "certification tuple",
            "deployment identity",
        ):
            self.assertIn(phrase, self.standard)
        props = self.profile["properties"]
        tool_props = props["toolchains"]["items"]["properties"]
        self.assertIn("compatibility", tool_props)
        self.assertIn("preferred_development", tool_props)
        self.assertIn("deployment_identity", tool_props)
        self.assertIn("certification_tuples", props)

    def test_agent_local_runtime_cannot_invent_repository_requirement(self) -> None:
        self.assertIn("Local availability is execution evidence only", self.standard)
        self.assertIn("Agent-local version", self.standard)
        self.assertIn("cannot rewrite the project", self.reference)

    def test_dependency_class_path_and_exposure_survive_risk_disposition(self) -> None:
        result = risk_disposition(
            dependency_class="test",
            exposure="test-only",
            applicability="not-runtime-reachable",
        )
        self.assertEqual(result["dependency_class"], "test")
        self.assertEqual(result["exposure"], "test-only")
        self.assertIn("dependency path/chain", self.standard)
        self.assertIn("A scanner severity alone", self.standard)

    def test_material_dependency_or_toolchain_delta_requires_validation_impact(self) -> None:
        self.assertTrue(dependency_change_requires_impact({"lock_changed": True}))
        self.assertTrue(dependency_change_requires_impact({"registry_changed": True}))
        self.assertTrue(dependency_change_requires_impact({"toolchain_requirement_changed": True}))
        self.assertFalse(dependency_change_requires_impact({"documentation_only": True}))
        self.assertIn("VALIDATION_IMPACT_DECISION", self.standard)

    def test_risk_exception_cannot_encode_pass(self) -> None:
        statuses = self.exception["properties"]["status"]["enum"]
        self.assertNotIn("PASS", statuses)
        self.assertNotIn("pass", statuses)
        self.assertIn("accepted-risk", statuses)
        self.assertIn("It is **not** Validation PASS", self.standard)
        self.assertIn("does not mean the vulnerability was remediated", self.reference)

    def test_examples_cover_node_and_non_node_ecosystems(self) -> None:
        self.assertIn("Node/npm example", self.reference)
        self.assertIn("Python example", self.reference)
        self.assertIn("Rust example", self.reference)
        self.assertIn("npm ci", self.reference)
        self.assertIn("not a universal command", self.reference)

    def test_policy_is_authority_driven_not_universal_blocker(self) -> None:
        for phrase in ("provenance", "license", "SBOM", "project/risk-authoritative"):
            self.assertIn(phrase, self.standard)
        self.assertIn("does not make every project", self.standard)

    def test_missing_required_toolchain_is_blocked_not_requirement_rewrite(self) -> None:
        self.assertIn("execution is truthfully `BLOCKED`", self.standard)
        self.assertIn("MUST NOT rewrite the project requirement", self.standard)


if __name__ == "__main__":
    unittest.main()
