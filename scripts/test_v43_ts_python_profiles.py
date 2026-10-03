from __future__ import annotations

from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
PROFILES = ROOT / "profiles" / "languages"
FRAMEWORK = ROOT / "profiles" / "README.md"


class TypeScriptPythonProfileTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.ts = (PROFILES / "typescript.md").read_text(encoding="utf-8")
        cls.py = (PROFILES / "python.md").read_text(encoding="utf-8")
        cls.framework = FRAMEWORK.read_text(encoding="utf-8")

    def test_stable_profile_identity_and_subordination(self) -> None:
        for text, identity in ((self.ts, "language.typescript"), (self.py, "language.python")):
            for token in (identity, "profile_version: 1", "profile_kind: language", "core_owner_refs:", "source_or_ecosystem_refs:", "project_check_mappings:", "high_risk_semantics:", "compatibility_notes:", "PROJECT_OVERRIDES"):
                self.assertIn(token, text)
            self.assertIn("Frozen/Core", text)
        self.assertIn("File/discovery order MUST NOT choose a winner", self.framework)

    def test_ts_manifest_lock_runtime_and_module_mapping(self) -> None:
        for token in ("package.json", "lockfile", "npm", "pnpm", "Yarn", "runtime compatibility", "preferred developer Node version", "certified build/deployment tuple", "tsconfig", "ESM/CJS", "module resolution"):
            self.assertIn(token, self.ts)
        self.assertIn("locally installed Node/npm does not narrow repository compatibility", self.ts)

    def test_ts_check_and_generated_output_boundaries(self) -> None:
        for token in ("typecheck", "build", "test", "runtime execution", "Generated `.d.ts`", "regeneration authority", "ESLint", "examples only", "not globally required"):
            self.assertIn(token, self.ts)

    def test_python_manifest_interpreter_and_package_mapping(self) -> None:
        for token in ("pyproject.toml", "requirements", "lockfile", "Poetry", "uv", "pip", "interpreter compatibility", "preferred developer interpreter", "certified build/test/deployment", "namespace/import", "wheel/sdist"):
            self.assertIn(token, self.py)
        self.assertIn("locally installed Python cannot redefine repository compatibility", self.py)

    def test_python_tools_are_examples_not_mandates(self) -> None:
        for token in ("pytest/unittest", "mypy/pyright", "Ruff", "none is universally mandatory", "UNKNOWN", "Validation request"):
            self.assertIn(token, self.py)

    def test_no_host_preference_or_profile_conflict_escalation(self) -> None:
        for profile in (self.ts, self.py):
            self.assertIn("UNKNOWN", profile)
            self.assertIn("Fast Path", profile)
            self.assertIn("file order", profile)
            self.assertIn("Agent", profile)
        self.assertIn("tool installed -> project selected that tool", self.framework)


if __name__ == "__main__":
    unittest.main()
