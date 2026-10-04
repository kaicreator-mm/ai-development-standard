from __future__ import annotations

from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
PROFILE_ROOT = ROOT / "profiles" / "archetypes"
FRAMEWORK = (ROOT / "profiles" / "README.md").read_text(encoding="utf-8")


class ArchetypeProfilesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.profiles = {name: (PROFILE_ROOT / f"{name}.md").read_text(encoding="utf-8") for name in ("library", "service", "cli")}

    def test_only_frozen_three_archetypes_and_identity(self) -> None:
        for name, text in self.profiles.items():
            for token in (f"archetype.{name}", "profile_version: 1", "profile_kind: archetype", "applicability:", "core_owner_refs:", "source_or_ecosystem_refs:", "project_check_mappings:", "high_risk_semantics:", "compatibility_notes:"):
                self.assertIn(token, text)
        self.assertFalse(any((PROFILE_ROOT / f"{name}.md").exists() for name in ("web", "frontend", "worker", "sdk", "desktop", "plugin", "monorepo")))

    def test_library_public_package_consumer_without_mandatory_publication(self) -> None:
        text = self.profiles["library"]
        for token in ("public", "consumer baseline", "compatibility", "package", "generated", "Distribution NOT_APPLICABLE", "publication is optional"):
            self.assertIn(token, text)
        self.assertIn("not require every library to be publicly published", text)

    def test_service_runtime_external_config_deployment_observability_are_conditional(self) -> None:
        text = self.profiles["service"]
        for token in ("runtime", "external", "configuration", "secret", "deployment", "observation", "incident", "production Deployment is not mandatory", "sandbox"):
            self.assertIn(token, text)
        self.assertIn("Deployment success is not automatically runtime healthy", text)

    def test_cli_command_build_package_environment_without_installer_mandate(self) -> None:
        text = self.profiles["cli"]
        for token in ("command", "exit", "stdout/stderr", "environment", "package", "installer", "target OS/architecture", "universal installer requirements are prohibited"):
            self.assertIn(token, text)

    def test_language_archetype_composition_cannot_choose_by_discovery_order(self) -> None:
        self.assertIn("Language and archetype profiles are independent axes", FRAMEWORK)
        self.assertIn("PROJECT_OVERRIDES", FRAMEWORK)
        self.assertIn("File/discovery order MUST NOT choose a winner", FRAMEWORK)
        for text in self.profiles.values():
            self.assertIn("PROJECT_OVERRIDES", text)
            self.assertIn("Fast Path", text)
            self.assertIn("order", text)
            self.assertIn("Validation", text)


if __name__ == "__main__":
    unittest.main()
