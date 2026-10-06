"""v4.7 T09 adoption / migration wiring tests.

These tests cover non-authoritative central wiring only. They do not create
Validation, Review, Closure, Release, or mutation authority.
"""
from __future__ import annotations

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
TASK_PACK = "docs/implementation/4.7.0/task-packs/T09_adoption_migration_wiring.md"
EXPECTED_WRITE_SET = {
    "templates/golden/STANDARD_COVERAGE.json",
    "templates/project/.dev-standard/PROJECT_OVERRIDES.md",
    "checklists/project-init.md",
    "checklists/pr-review.md",
    "checklists/version-closure.md",
    "docs/implementation/4.7.0/MIGRATION_ADOPTION.md",
    "docs/implementation/4.7.0/FUTURE_MAJOR_REGISTER.md",
    "scripts/test_v47_adoption_wiring.py",
}


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def parse_allowed_write_set(text: str) -> set[str]:
    lines = text.splitlines()
    start = next(i for i, line in enumerate(lines) if line.strip() == "allowed_write_set:")
    paths: list[str] = []
    for raw in lines[start + 1 :]:
        if raw.startswith("  - "):
            paths.append(raw[4:].strip())
            continue
        if raw and not raw.startswith((" ", "\t")):
            break
    if not paths or len(paths) != len(set(paths)):
        raise AssertionError("T09 allowed_write_set is empty or duplicated")
    return set(paths)


def ref_path(ref: str) -> str:
    return ref.split("#", 1)[0]


class AdoptionMigrationWiringTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.task_pack = read(TASK_PACK)
        cls.coverage = json.loads(read("templates/golden/STANDARD_COVERAGE.json"))
        cls.overrides = read("templates/project/.dev-standard/PROJECT_OVERRIDES.md")
        cls.project_init = read("checklists/project-init.md")
        cls.pr_review = read("checklists/pr-review.md")
        cls.version_closure = read("checklists/version-closure.md")
        cls.migration = read("docs/implementation/4.7.0/MIGRATION_ADOPTION.md")
        cls.future_major = read("docs/implementation/4.7.0/FUTURE_MAJOR_REGISTER.md")
        cls.manifest = json.loads(read("standard-manifest.json"))

    def test_t09_write_authority_is_exact_and_cannot_expand_by_necessity(self) -> None:
        allowed = parse_allowed_write_set(self.task_pack)
        self.assertEqual(allowed, EXPECTED_WRITE_SET)
        self.assertNotIn("standard-manifest.json", allowed)
        self.assertNotIn("registries/state-dimensions-v1.json", allowed)
        self.assertNotIn("scripts/v47_conformance.py", allowed)

    def test_golden_coverage_is_discovery_only(self) -> None:
        wiring = self.coverage["semantic_discovery"]
        self.assertEqual(wiring["status"], "NON_AUTHORITATIVE_WIRING_ONLY")
        self.assertFalse(wiring["mutation_authority"])
        self.assertFalse(wiring["gate_authority"])
        expected_refs = {
            "canonical_owner_registry_ref": "standard-manifest.json#semantic_authorities",
            "state_dimension_registry_ref": "registries/state-dimensions-v1.json",
            "read_routing_helper_ref": "scripts/resolve_standard_read_set.py",
            "project_specialization_ref": "templates/project/.dev-standard/PROJECT_OVERRIDES.md",
            "migration_adoption_ref": "docs/implementation/4.7.0/MIGRATION_ADOPTION.md",
            "future_major_register_ref": "docs/implementation/4.7.0/FUTURE_MAJOR_REGISTER.md",
        }
        for key, expected in expected_refs.items():
            self.assertEqual(wiring[key], expected)
            self.assertTrue((ROOT / ref_path(expected)).is_file(), expected)

    def test_project_and_checklists_route_to_canonical_discovery(self) -> None:
        self.assertIn("v4.7 Convergence Discovery (non-authoritative wiring)", self.overrides)
        for text in (self.overrides, self.project_init, self.pr_review):
            self.assertIn("standard-manifest.json#semantic_authorities", text)
        self.assertIn("docs/implementation/4.7.0/MIGRATION_ADOPTION.md", self.project_init)
        self.assertIn("docs/implementation/4.7.0/FUTURE_MAJOR_REGISTER.md", self.pr_review)
        self.assertIn("docs/implementation/4.7.0/FUTURE_MAJOR_REGISTER.md", self.version_closure)

    def test_project_overrides_remain_non_weakening_and_optional(self) -> None:
        required = (
            "discovery/read surfaces only",
            "MUST NOT grant mutation, Validation, Review, Closure, or Release authority",
            "Load optional v4.7 registries/profiles only when they are applicable",
            "Fast Path proportionality",
        )
        for token in required:
            self.assertIn(token, self.overrides)
        self.assertIn("Project overrides **MUST NOT weaken**", self.overrides)

    def test_migration_wiring_preserves_compatibility_and_proportionality(self) -> None:
        required = (
            "AUTHORITY_EFFECT=NONE",
            "MUTATION_AUTHORITY=NONE",
            "GATE_EFFECT=NONE",
            "standards/GITHUB_WORKFLOW.md",
            "standards/VERSION_INTEGRATION_WORKFLOW.md",
            "Do not perform physical standard/reference path migration as part of T09.",
            "Optional/non-applicable capability stays optional/non-applicable.",
            "Fast Path proportionality remains intact",
            "independent exact-head/current-target integration Validation",
            "genuinely new Fresh Independent Review",
        )
        for token in required:
            self.assertIn(token, self.migration)

    def test_future_major_register_is_planning_input_not_authority(self) -> None:
        required = (
            "T09 PLANNING INPUT ONLY — NON-AUTHORITATIVE",
            "AUTHORITY_EFFECT=NONE",
            "MUTATION_AUTHORITY=NONE",
            "GATE_EFFECT=NONE",
            "RELEASE_EFFECT=NONE",
            "PRD.md#14-future-major-register",
            "technical need does not expand a current Task Pack write-set",
            "register entry does not authorize path movement",
        )
        lower = self.future_major.lower()
        for token in required:
            self.assertIn(token.lower(), lower)
        self.assertNotIn("CONVERGENCE_PASS=PASS", self.future_major)

    def test_stable_compatibility_aliases_remain_non_owners(self) -> None:
        sections = self.manifest["sections"]
        compatibility = set(sections["compatibility_entries"])
        normative = set(sections["normative_standards"])
        aliases = {
            alias
            for entry in self.manifest["semantic_authorities"]["entries"]
            for alias in entry.get("compatibility_alias_refs", [])
        }
        self.assertEqual(
            compatibility,
            {"standards/GITHUB_WORKFLOW.md", "standards/VERSION_INTEGRATION_WORKFLOW.md"},
        )
        self.assertEqual(aliases, compatibility)
        self.assertFalse(compatibility & normative)
        for alias in compatibility:
            self.assertTrue((ROOT / alias).is_file(), alias)

    def test_t09_wiring_does_not_manufacture_convergence_gate(self) -> None:
        central_texts = (
            self.overrides,
            self.project_init,
            self.pr_review,
            self.version_closure,
            self.migration,
            self.future_major,
        )
        for text in central_texts:
            self.assertNotIn("CONVERGENCE_PASS=PASS", text)
        self.assertIn("T07 remains the owner of unified semantic conformance", self.migration)


if __name__ == "__main__":
    unittest.main()
