from __future__ import annotations

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "standard-manifest.json"
OVERRIDES = ROOT / "templates" / "project" / ".dev-standard" / "PROJECT_OVERRIDES.md"
MIGRATION = ROOT / "docs" / "implementation" / "4.1.0" / "MIGRATION_ADOPTION.md"
PROJECT_INIT = ROOT / "checklists" / "project-init.md"
PR_REVIEW = ROOT / "checklists" / "pr-review.md"
VERSION_CLOSURE = ROOT / "checklists" / "version-closure.md"


class V41AdoptionWiringTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        cls.overrides = OVERRIDES.read_text(encoding="utf-8")
        cls.migration = MIGRATION.read_text(encoding="utf-8")
        cls.project_init = PROJECT_INIT.read_text(encoding="utf-8")
        cls.pr_review = PR_REVIEW.read_text(encoding="utf-8")
        cls.version_closure = VERSION_CLOSURE.read_text(encoding="utf-8")

    def test_manifest_discovers_all_v41_normative_owners(self) -> None:
        owners = set(self.manifest["sections"]["normative_standards"])
        expected = {
            "standards/DEPENDENCY_TOOLCHAIN_GOVERNANCE_STANDARD.md",
            "standards/GIT_EXECUTION_STANDARD.md",
            "standards/CONFIGURATION_SECRETS_STANDARD.md",
            "standards/WORKSPACE_ARTIFACT_STANDARD.md",
            "standards/EXTERNAL_SYSTEM_EXECUTION_STANDARD.md",
        }
        self.assertTrue(expected.issubset(owners))

    def test_manifest_discovers_v41_machine_contracts_and_references(self) -> None:
        contracts = set(self.manifest["sections"]["machine_contracts"])
        self.assertTrue(
            {
                "schemas/execution-context-v1.schema.json",
                "schemas/dependency-toolchain-profile-v1.schema.json",
                "schemas/dependency-risk-exception-v1.schema.json",
            }.issubset(contracts)
        )
        references = set(self.manifest["sections"]["references"])
        for name in (
            "DEPENDENCY_TOOLCHAIN_REFERENCE",
            "GIT_EXECUTION_REFERENCE",
            "CONFIGURATION_SECRETS_REFERENCE",
            "WORKSPACE_ARTIFACT_REFERENCE",
            "EXTERNAL_SYSTEM_EXECUTION_REFERENCE",
        ):
            self.assertTrue(any(name in path for path in references), name)

    def test_execution_foundation_profile_is_materiality_driven(self) -> None:
        self.assertIn("## v4.1 Execution Foundation Profile", self.overrides)
        self.assertIn("execution_foundation.profile", self.overrides)
        self.assertIn("materiality-driven", self.overrides)
        self.assertIn("Execution Context` is non-authoritative", self.overrides)
        self.assertIn("MUST NOT be forced to generate empty/non-applicable machine records", self.overrides)

    def test_migration_guide_preserves_single_owner_and_non_authoritative_context(self) -> None:
        self.assertIn("The shared `Execution Context` is a non-authoritative projection", self.migration)
        self.assertIn("## 4. Owner map", self.migration)
        self.assertIn("risk disposition, never Validation PASS", self.migration)
        self.assertIn("do not retroactively claim old executions", self.migration)

    def test_checklists_surface_execution_facts_without_new_gate_states(self) -> None:
        self.assertIn("Execution Foundation Profile", self.project_init)
        self.assertIn("non-authoritative Execution Context", self.pr_review)
        self.assertIn("Applicable v4.1 execution-foundation owners", self.version_closure)
        combined = "\n".join((self.project_init, self.pr_review, self.version_closure))
        self.assertNotIn("EXECUTION_FOUNDATION_PASS", combined)
        self.assertNotIn("EXECUTION_CONTEXT_PASS", combined)

    def test_fast_path_does_not_require_non_applicable_machine_records(self) -> None:
        for text in (self.overrides, self.migration, self.version_closure):
            self.assertTrue(
                "empty/non-applicable machine" in text
                or "non-applicable machine contracts" in text
                or "do not generate empty" in text
            )

    def test_forbidden_shortcuts_remain_explicit(self) -> None:
        for phrase in (
            "worktree exists -> task state",
            "risk exception -> Validation PASS",
            "credential exists -> side-effect authority",
        ):
            self.assertIn(phrase, self.migration)


if __name__ == "__main__":
    unittest.main()
