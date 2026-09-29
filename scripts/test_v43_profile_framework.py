from __future__ import annotations

from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
FRAMEWORK = ROOT / "profiles" / "README.md"


class ProfileFrameworkTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.text = FRAMEWORK.read_text(encoding="utf-8")
        cls.lower = cls.text.lower()

    def test_stable_profile_identity_fields_are_documented(self) -> None:
        for field in (
            "profile_id",
            "profile_version",
            "profile_kind",
            "applicability",
            "core_owner_refs",
            "project_check_mappings",
            "high_risk_semantics",
        ):
            self.assertIn(field, self.text)

    def test_language_archetype_and_project_overrides_compose_deterministically(self) -> None:
        self.assertIn("Frozen/Core normative authority", self.text)
        self.assertIn("applicable language profile mapping", self.text)
        self.assertIn("applicable archetype profile mapping", self.text)
        self.assertIn("PROJECT_OVERRIDES specialization/strengthening", self.text)
        self.assertIn("File/discovery order MUST NOT choose a winner", self.text)

    def test_profiles_are_mapping_layers_not_normative_owners(self) -> None:
        self.assertIn("not independent lifecycle or Product/Architecture authorities", self.text)
        self.assertIn("Profiles map/default; they do not weaken or replace Core requirements", self.text)

    def test_project_specialization_cannot_weaken_core(self) -> None:
        self.assertIn("MUST NOT silently weaken Frozen/Core authority", self.text)
        self.assertIn("fails closed", self.lower)

    def test_agent_local_tooling_is_not_profile_authority(self) -> None:
        self.assertIn("Agent-local tooling is execution capability/evidence, never profile authority", self.text)
        self.assertIn("tool installed -> project selected that tool", self.text)

    def test_profile_framework_does_not_become_v47_resolver(self) -> None:
        self.assertIn("not** the repository-wide owner/applicability resolver", self.text)
        self.assertIn("belong to v4.7", self.text)

    def test_fast_path_and_non_applicable_profiles_are_lightweight(self) -> None:
        self.assertIn("MUST NOT be forced to instantiate language/archetype profile records", self.text)
        self.assertIn("Fast Path reduces ceremony, not authority", self.text)


if __name__ == "__main__":
    unittest.main()
