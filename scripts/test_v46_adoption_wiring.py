from __future__ import annotations

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "standard-manifest.json"
COVERAGE = ROOT / "templates" / "golden" / "STANDARD_COVERAGE.json"
PROJECT_OVERRIDES = ROOT / "templates" / "project" / ".dev-standard" / "PROJECT_OVERRIDES.md"
PROJECT_INIT = ROOT / "checklists" / "project-init.md"
PR_REVIEW = ROOT / "checklists" / "pr-review.md"
VERSION_CLOSURE = ROOT / "checklists" / "version-closure.md"
MIGRATION = ROOT / "docs" / "implementation" / "4.6.0" / "MIGRATION_ADOPTION.md"

NEW_STANDARDS = {
    "standards/INTENT_ASSUMPTION_GOVERNANCE_STANDARD.md",
    "standards/CONTEXT_ENGINEERING_STANDARD.md",
    "standards/SKILL_PROCEDURE_GOVERNANCE_STANDARD.md",
}
NEW_MACHINE_FAMILIES = {
    "schemas/intent-assumption-record-v1.schema.json",
    "schemas/skill-metadata-v1.schema.json",
}
V46_REFERENCES = {
    "references/AI_NATIVE_EXISTING_OWNER_INTEGRATION.md",
    "references/INTENT_ASSUMPTION_REFERENCE.md",
    "references/CONTEXT_ENGINEERING_REFERENCE.md",
    "references/SKILL_PROCEDURE_REFERENCE.md",
}
V46_TESTS = {
    "scripts/test_v46_ai_native_contracts.py",
    "scripts/test_v46_intent_assumption.py",
    "scripts/test_v46_context_engineering.py",
    "scripts/test_v46_skill_procedure.py",
    "scripts/test_v46_existing_owner_integration.py",
    "scripts/test_v46_adoption_wiring.py",
}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def ref_path(value: str) -> str:
    return value.split("#", 1)[0]


class V46AdoptionWiringTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = json.loads(read(MANIFEST))
        cls.coverage = json.loads(read(COVERAGE))
        cls.project_overrides = read(PROJECT_OVERRIDES)
        cls.project_init = read(PROJECT_INIT)
        cls.pr_review = read(PR_REVIEW)
        cls.version_closure = read(VERSION_CLOSURE)
        cls.migration = read(MIGRATION)

    def test_manifest_discovers_v46_owners_contracts_references_and_tests(self) -> None:
        sections = self.manifest["sections"]
        self.assertTrue(NEW_STANDARDS.issubset(set(sections["normative_standards"])))
        self.assertTrue(NEW_MACHINE_FAMILIES.issubset(set(sections["machine_contracts"])))
        self.assertTrue(V46_REFERENCES.issubset(set(sections["references"])))
        self.assertTrue(V46_TESTS.issubset(set(sections["verification"])))
        for rel in NEW_STANDARDS | NEW_MACHINE_FAMILIES | V46_REFERENCES | V46_TESTS:
            with self.subTest(path=rel):
                self.assertTrue((ROOT / rel).is_file(), rel)

    def test_golden_coverage_exactly_matches_normative_standard_set(self) -> None:
        normative = self.manifest["sections"]["normative_standards"]
        rows = self.coverage["coverage"]
        covered = [row["standard"] for row in rows]
        self.assertEqual(len(covered), len(set(covered)), "duplicate STANDARD_COVERAGE standard")
        self.assertEqual(set(covered), set(normative))
        for row in rows:
            for key in ("standard", "golden_ref", "forbidden_ref", "rationale_ref"):
                rel = ref_path(row[key])
                with self.subTest(standard=row["standard"], field=key, path=rel):
                    self.assertTrue((ROOT / rel).is_file(), rel)

    def test_new_normative_owners_have_golden_forbidden_and_rationale_refs(self) -> None:
        by_standard = {row["standard"]: row for row in self.coverage["coverage"]}
        for standard in NEW_STANDARDS:
            row = by_standard[standard]
            self.assertTrue(row["golden_ref"])
            self.assertTrue(row["forbidden_ref"])
            self.assertTrue(row["rationale_ref"])

    def test_project_overrides_is_materiality_driven_and_non_weakening(self) -> None:
        for token in (
            "## v4.6 AI-native / Agentic Governance Profile",
            "materiality-driven",
            "v4.ai_native.intent_assumption",
            "v4.ai_native.context_currentness",
            "v4.ai_native.skill_admission",
            "v4.ai_native.durable_truth_surface",
            "Record shape never creates Product/Architecture/Task authority",
            "Installed/discoverable Skill != trusted Skill",
            "references/AI_NATIVE_EXISTING_OWNER_INTEGRATION.md",
            "Fast Path reduces ceremony, not truth",
            "Historical evidence is not retrofitted",
            "repository-wide v4.7 resolver",
        ):
            with self.subTest(token=token):
                self.assertIn(token, self.project_overrides)

    def test_selected_checklists_wire_ai_native_concerns_without_new_state_owner(self) -> None:
        self.assertIn("## v4.6 AI-native Adoption", self.project_init)
        self.assertIn("exactly three new normative owners", self.project_init)
        self.assertIn("Fast Path may omit non-material Intent/Skill records", self.project_init)

        self.assertIn("## v4.6 AI-native Governance (when material)", self.pr_review)
        self.assertIn("does not invent a competing Product/Task/Assurance/Dispatch/Handoff/Validation/Release owner", self.pr_review)
        self.assertIn("AI-native Assurance/Review coverage reuses existing assurance/review owners", self.pr_review)

        self.assertIn("## v4.6 AI-native Cross-standard Reconciliation", self.version_closure)
        self.assertIn("does not create a new Closure gate family", self.version_closure)
        self.assertIn("Assurance/Review, F0–F3, Dispatch/Handoff, Validation and Release continue to use their existing owners", self.version_closure)

    def test_fast_path_does_not_require_empty_records(self) -> None:
        self.assertIn("does not require projects to manufacture empty Intent/Assumption or Skill records", self.project_overrides)
        self.assertIn("does **not** require empty Intent/Assumption or Skill records", self.migration)
        self.assertIn("no empty Skill metadata record is required", self.migration)
        self.assertIn("do not create an empty record merely to satisfy ceremony", self.migration)

    def test_migration_guide_preserves_existing_owner_boundaries_and_history(self) -> None:
        for token in (
            "exactly three new normative owners",
            "exactly two default machine-contract families",
            "references/AI_NATIVE_EXISTING_OWNER_INTEGRATION.md",
            "no AI-native PASS state",
            "no AI-native READY state",
            "Do not retrofit historical evidence",
            "does not implement a repository-wide v4.7 resolver",
            "execute or claim sibling T06 session/operator handoff dogfood evidence",
            "perform Version Closure or Release Qualification",
        ):
            with self.subTest(token=token):
                self.assertIn(token, self.migration)

    def test_no_default_context_snapshot_or_v47_resolver_machine_family(self) -> None:
        machine_paths = set(self.manifest["sections"]["machine_contracts"])
        self.assertFalse(any("context-snapshot" in path.lower() for path in machine_paths))
        self.assertFalse(any("resolver" in path.lower() for path in machine_paths))
        self.assertEqual(len(NEW_MACHINE_FAMILIES), 2)
        self.assertIn("There is no default Context Snapshot contract", self.migration)
        self.assertIn("repository-wide v4.7 resolver", self.migration)


if __name__ == "__main__":
    unittest.main(verbosity=2)
