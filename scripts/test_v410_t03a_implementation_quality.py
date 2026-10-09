"""V410-T03A focused regressions: automation-first implementation quality.

Positive coverage: materially risky mutation patterns are reviewable
implementation-quality defects under the quality owner.
Negative coverage: no universal human line-by-line review gate, docs/style
churn alone is not a defect, and automated checks/tests never create
Validation or Release authority.

Authority: issue #854, Task Pack R1 V410-T03A, L3 Wave A R1 V410-T03A,
Frozen L2 #842 §7.
"""

from __future__ import annotations

import re
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
STANDARD = ROOT / "standards" / "IMPLEMENTATION_QUALITY_STANDARD.md"
REFERENCE = ROOT / "references" / "IMPLEMENTATION_QUALITY_REFERENCE.md"

# Ecosystem-specific tool names must stay out of the language-neutral owner.
ECOSYSTEM_TOOL_RE = re.compile(
    r"\b(prettier|eslint|black|gofmt|rustfmt|clang-format|ruff|mypy|tsc|biome)\b",
    re.IGNORECASE,
)


class MaterialChangeHygieneDefectsTests(unittest.TestCase):
    """Positive: the five L2 §7.2 patterns are reviewable defects when material."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.standard = STANDARD.read_text(encoding="utf-8")

    def test_material_change_hygiene_section_exists(self) -> None:
        self.assertIn("## 11. Material change hygiene", self.standard)
        self.assertIn("reviewable implementation-quality defects", self.standard)
        self.assertIn("When material to maintained intent or evidence", self.standard)

    def test_destructive_whole_file_rewrite_is_a_defect(self) -> None:
        self.assertIn("unnecessary whole-file rewrite or mass comment/doc loss that destroys maintained intent", self.standard)

    def test_unrelated_churn_mixed_with_semantic_change_is_a_defect(self) -> None:
        self.assertIn("unrelated formatting or generated churn mixed with a semantic change", self.standard)

    def test_hidden_semantic_change_outside_declared_scope_is_a_defect(self) -> None:
        self.assertIn("a semantic change hidden outside the declared change scope", self.standard)

    def test_direct_generated_output_mutation_ignoring_authority_is_a_defect(self) -> None:
        self.assertIn("direct mutation of generated output that ignores its regeneration authority", self.standard)
        # The v4.3 generated-source authority invariants remain intact.
        self.assertIn("Editing generated output directly does not make that output canonical authority", self.standard)
        self.assertIn("generated file changed successfully -> canonical source and regeneration contract are satisfied", self.standard)

    def test_unnecessary_public_surface_widening_is_a_defect(self) -> None:
        self.assertIn("unnecessary public-surface widening or abstraction", self.standard)
        # Widening hardening composes with, and does not replace, the v4.3 narrowing rule.
        self.assertIn("silently narrow an existing compatibility contract", self.standard)
        self.assertIn("compatibility authority", self.standard)


class AutomationFirstNegativeInvariantsTests(unittest.TestCase):
    """Negative: hygiene hardening must not restore Human Reviewability as a gate."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.standard = STANDARD.read_text(encoding="utf-8")
        cls.reference = REFERENCE.read_text(encoding="utf-8")

    def test_no_universal_human_line_by_line_review_gate(self) -> None:
        self.assertIn("not from a universal requirement that a human read every changed line", self.standard)
        self.assertIn("they do not introduce a universal human line-by-line review gate and MUST NOT be used to restore one", self.standard)
        # Every mention of line-by-line reading appears only in negated context.
        negated = re.compile(r"not\b|MUST NOT|None of these prompts", re.IGNORECASE)
        for line in self.standard.splitlines() + self.reference.splitlines():
            if "line-by-line" in line:
                self.assertIsNotNone(negated.search(line), f"un-negated line-by-line gate: {line!r}")
        self.assertIn("None of these prompts asks for a universal human line-by-line review gate", self.reference)

    def test_docs_style_churn_alone_is_not_a_defect(self) -> None:
        self.assertIn("docs/style churn alone is not automatically a defect", self.standard)
        self.assertIn("Materiality is judged by maintenance and evidence impact", self.standard)

    def test_checks_and_tests_never_create_release_authority(self) -> None:
        self.assertIn("Automated checks and tests remain the primary quality mechanism", self.standard)
        self.assertIn("their passing alone never creates Validation or Release authority", self.standard)
        # v4.3 composition boundary: one mechanism never mints another owner's PASS.
        self.assertIn("MUST NOT manufacture PASS under another owner", self.standard)
        self.assertIn("tool/check result being promoted into Validation or Release truth", self.reference)


class OwnerBoundaryTests(unittest.TestCase):
    """The hardening stays inside the owner: language-neutral, no sibling-owner duplication."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.standard = STANDARD.read_text(encoding="utf-8")

    def test_new_section_stays_language_neutral(self) -> None:
        section = self.standard.split("## 11. Material change hygiene", 1)[1]
        self.assertIsNone(ECOSYSTEM_TOOL_RE.search(section))

    def test_task_decomposition_ownership_is_not_duplicated(self) -> None:
        lower = self.standard.lower()
        for phrase in ("safe parallelism", "split threshold", "task decomposition owner"):
            self.assertNotIn(phrase, lower)

    def test_frozen_coverage_anchors_still_resolve(self) -> None:
        # templates/golden/STANDARD_COVERAGE.json pins these heading anchors.
        self.assertIn("## 1. Purpose", self.standard)
        self.assertIn("## 7. Composition with existing owners", self.standard)


if __name__ == "__main__":
    unittest.main()
