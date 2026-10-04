from __future__ import annotations

from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
STANDARD = ROOT / "standards" / "TASK_DECOMPOSITION_STANDARD.md"
REFERENCE = ROOT / "references" / "TASK_DECOMPOSITION_REFERENCE.md"


class TaskDecompositionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.standard = STANDARD.read_text(encoding="utf-8")
        cls.reference = REFERENCE.read_text(encoding="utf-8")

    def test_minimum_coherent_concern_and_max_safe_parallelism(self) -> None:
        self.assertIn("Minimum coherent concern + maximum safe parallelism", self.standard)
        self.assertIn("one primary concern", self.standard)

    def test_required_task_facts_are_present(self) -> None:
        for phrase in (
            "allowed write-set / ownership",
            "forbidden scope",
            "acceptance criteria",
            "required gates",
            "Validation scope / owner",
            "Review policy",
            "integration / merge target",
            "dependencies",
            "agent freedom / executor constraints",
            "failure / escalation handling",
        ):
            self.assertIn(phrase, self.standard)

    def test_file_count_only_split_is_rejected(self) -> None:
        self.assertIn("File count, line count or estimated token count alone MUST NOT define Task boundaries", self.standard)
        self.assertIn("Bad file-count split", self.reference)

    def test_atomic_shared_invariant_is_not_fake_parallelized(self) -> None:
        self.assertIn("Do not fake parallelism", self.standard)
        self.assertIn("shared state invariant that only holds after both branches merge", self.standard)
        self.assertIn("Fake parallelism", self.standard)

    def test_stacked_pr_requires_real_unmerged_code_baseline(self) -> None:
        self.assertIn("Stacked PR is appropriate only when a Task genuinely needs code from an unmerged predecessor branch", self.standard)
        self.assertIn("MUST NOT be used as the general representation of the Task DAG", self.standard)

    def test_native_issue_dependencies_remain_live_dag(self) -> None:
        self.assertIn("GitHub Issue Dependencies are the canonical live Task DAG", self.standard)
        self.assertIn("Body text, labels or chat descriptions are not substitutes", self.standard)

    def test_central_wiring_pattern_preserves_sibling_ownership(self) -> None:
        self.assertIn("explicit central wiring / integration Task", self.standard)
        self.assertIn("must reference sibling owners rather than become a semantic rewrite task", self.standard.lower())

    def test_lane_taxonomy_is_advisory(self) -> None:
        self.assertIn("no fixed lane taxonomy is universally mandatory", self.standard)
        self.assertIn("Concern ownership and real dependencies decide the DAG", self.standard)

    def test_dependency_removal_cannot_fabricate_ready(self) -> None:
        self.assertIn("Do not remove a dependency merely to make a Task appear READY", self.standard)
        self.assertIn("manufacture READY", self.reference)


if __name__ == "__main__":
    unittest.main()
