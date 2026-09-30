from __future__ import annotations

from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
STANDARD = ROOT / "standards" / "IMPLEMENTATION_QUALITY_STANDARD.md"
REFERENCE = ROOT / "references" / "IMPLEMENTATION_QUALITY_REFERENCE.md"


class ImplementationQualityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.standard = STANDARD.read_text(encoding="utf-8")
        cls.reference = REFERENCE.read_text(encoding="utf-8")
        cls.lower = cls.standard.lower()

    def test_repository_authoritative_entrypoints_are_explicit(self) -> None:
        self.assertIn("build, test and deterministic check entrypoints", self.standard)
        self.assertIn("Agent's locally installed tool", self.standard)
        self.assertIn("MUST NOT become project authority", self.standard)

    def test_deterministic_checks_are_capability_driven_not_global_tool_mandates(self) -> None:
        self.assertIn("when the selected ecosystem and project support them materially", self.standard)
        for phrase in ("one formatter", "linter", "coverage threshold", "complexity threshold"):
            self.assertIn(phrase, self.lower)

    def test_generated_material_keeps_canonical_source_and_regeneration_authority(self) -> None:
        self.assertIn("regeneration authority or canonical source", self.standard)
        self.assertIn("Editing generated output directly does not make that output canonical authority", self.standard)
        self.assertIn("generated file changed successfully", self.standard)

    def test_public_contract_and_technical_failure_boundaries_are_explicit(self) -> None:
        self.assertIn("public contracts and error behavior", self.standard)
        self.assertIn("technical failure into a successful domain result", self.standard)
        self.assertIn("compatibility authority", self.standard)

    def test_secret_safe_behavior_does_not_grant_side_effect_authority(self) -> None:
        self.assertIn("raw secret values", self.standard)
        self.assertIn("command succeeded with credential present -> side-effect authority granted", self.standard)

    def test_existing_result_owners_are_referenced_not_duplicated(self) -> None:
        for owner in ("Dependency/Toolchain", "Config/Secrets", "Testing", "CI", "Validation", "Release"):
            self.assertIn(owner, self.standard)
        self.assertIn("MUST NOT manufacture PASS under another owner", self.standard)

    def test_profiles_are_subordinate_mappings(self) -> None:
        self.assertIn("profiles are subordinate mapping/default layers", self.lower)
        self.assertIn("MUST NOT weaken Frozen/Core or project authority", self.standard)
        self.assertIn("MUST NOT manufacture a new universal requirement", self.standard)

    def test_fast_path_is_proportional(self) -> None:
        self.assertIn("Fast Path reduces non-material work", self.standard)
        self.assertIn("does not permit bypassing", self.standard)

    def test_reference_keeps_agent_local_tools_subordinate(self) -> None:
        self.assertIn("execution capability, not evidence that the project selected that tool/version", self.reference)
        self.assertIn("tool/check result being promoted into Validation or Release truth", self.reference)


if __name__ == "__main__":
    unittest.main()
