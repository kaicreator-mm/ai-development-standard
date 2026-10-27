"""Proposed ADS v4.19 E1 issue-prevention source conformance.

This checks only committed source/fixture integrity and miniature negative
illustrations, NOT real DomainHarness tests, exact-SHA CI, Agent execution,
physical Host evidence, Product Freeze, or release qualification.
Run from repo root: python -m unittest discover -s tests -p test_v419_issue_prevention.py -v
"""
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CASE = ROOT / "docs/intake/issue-cases/domain-harness-decision-pilot-r0.json"

OWNERS = {
    "standards/TESTING_STANDARD.md": (
        "### 6.1 Executed-test discovery",
        "### 6.2 Selected public path",
        "DomainHarness #162",
    ),
    "standards/TASK_DECOMPOSITION_STANDARD.md": (
        "### 13.1 Feasibility, evidence barriers",
        "actual artifact prerequisites",
        "DomainHarness #530",
    ),
    "standards/ARCHITECTURE_DESIGN_STANDARD.md": (
        "selected executable composition path",
        "selected-path acceptance",
        "DomainHarness v0.8 integration #1013",
    ),
    "standards/IMPLEMENTATION_QUALITY_STANDARD.md": (
        "EXPORTED_OR_LOADED",
        "actual selected-path invocation",
        "DomainHarness #139",
    ),
    "standards/DEVELOPMENT_WORKFLOW.md": (
        "minimum sufficient correction",
        "现有 Issue/PR",
        "DomainHarness A5 #1354",
    ),
}

def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")

def cases() -> list[dict]:
    return json.loads(CASE.read_text(encoding="utf-8"))["cases"]


class IssuePreventionSourceOnly(unittest.TestCase):
    def test_actual_owner_rules_exist_on_real_standards(self) -> None:
        for filename, markers in OWNERS.items():
            source = read(filename)
            for marker in markers:
                with self.subTest(owner=filename, marker=marker):
                    self.assertIn(marker, source)

    def test_existing_golden_owners_and_no_second_standard_registry(self) -> None:
        index = json.loads(read("templates/golden/STANDARD_COVERAGE.json"))
        for filename in OWNERS:
            rows = [row for row in index["coverage"] if row["standard"] == filename]
            with self.subTest(owner=filename):
                self.assertEqual(len(rows), 1)
                self.assertTrue(rows[0]["golden_ref"])
                self.assertTrue(rows[0]["forbidden_ref"])
        self.assertIn("minimum sufficient correction",
                      read("templates/golden/STANDARD_CONFORMANCE_EXAMPLES.md"))
        self.assertIn("actual discovered/executed test inventory",
                      read("templates/golden/STANDARD_CONFORMANCE_EXAMPLES.md"))

    def test_real_case_links_unique_and_pair_targets_present(self) -> None:
        rows = cases()
        ids = [row["id"] for row in rows]
        self.assertEqual(len(rows), 18)
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(sum(r["assessment_window"] == "practice-good-example"
                             for r in rows), 3)
        for row in rows:
            with self.subTest(case=row["id"]):
                self.assertTrue(row["origin_issue"].startswith(
                    "https://github.com/kaicreator-mm/domain-harness/issues/"))
                self.assertTrue(row["input_known_fact"])
                self.assertTrue(row["proposed_expected"]["bounded_decision"])
                self.assertTrue(row["proposed_expected"]["must_not"])
                self.assertEqual(row["evaluation_status"],
                                 "PROPOSED_NOT_INDEPENDENTLY_ADJUDICATED")
                if row.get("paired_control"):
                    self.assertIn(row["paired_control"], ids)

    def test_positive_controls_prevent_more_gates_is_always_better(self) -> None:
        by_id = {row["id"]: row for row in cases()}
        for case_id in ("DH-V07-VERIFY-CAMPAIGN",
                        "DH-V09-SCOPE",
                        "DH-V101-EVIDENCE-REUSE"):
            row = by_id[case_id]
            with self.subTest(case=case_id):
                self.assertEqual(row["assessment_window"],
                                 "practice-good-example")
                self.assertTrue(row["proposed_expected"]["must_not"])

    def test_nested_test_glob_can_omit_declared_required_suite(self) -> None:
        # Synthetic E1 filesystem negative; NOT execution of npm/Node/CI.
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "tests" / "execution").mkdir(parents=True)
            (root / "tests" / "root.test.ts").write_text("", encoding="utf-8")
            nested = root / "tests" / "execution" / "recovery.test.ts"
            nested.write_text("", encoding="utf-8")
            expected = {str(p.relative_to(root)) for p
                        in root.rglob("*.test.ts")}
            discovered = {str(p.relative_to(root)) for p
                          in (root / "tests").glob("*.test.ts")}
            self.assertIn("tests/execution/recovery.test.ts", expected)
            self.assertNotIn("tests/execution/recovery.test.ts", discovered)
            self.assertTrue(expected - discovered,
                            "green command alone cannot prove missing tests ran")

    def test_imported_hook_does_not_imply_selected_call(self) -> None:
        # Synthetic E1 semantic negative; NOT DomainHarness physical execution.
        calls = []
        def hook(value: int) -> int:
            calls.append(value)
            return value + 1
        registry = {"demo.hook": hook}  # selected/imported
        self.assertIn("demo.hook", registry)
        self.assertEqual(calls, [], "loaded is not invoked")
        result = registry["demo.hook"](2)  # actual selected call
        self.assertEqual(result, 3)
        self.assertEqual(calls, [2])

    def test_source_only_examples_do_not_forge_workflow_authority(self) -> None:
        corpus = read("docs/intake/2026-10-28-issue-derived-ads-evaluation-pilot.md")
        for token in ("not a second Task Learning authority",
                      "NOT_RECONSTRUCTABLE",
                      "read-only",
                      "NOT_MEASURED"):
            with self.subTest(token=token):
                self.assertIn(token, corpus)
        rules = read("standards/TASK_DECOMPOSITION_STANDARD.md")
        self.assertIn("accepted Claim", rules)
        self.assertIn("native", rules)
        self.assertIn("not a new scheduler", rules)

    def test_forbidden_examples_cover_three_historical_failure_classes(self) -> None:
        forbidden = read("templates/golden/ANTI_PATTERNS.md")
        for section in ("## actual-test-discovery-missing",
                        "## loaded-extension-as-functional-proof",
                        "## compatibility-join-as-universal-source-prerequisite",
                        "## endless-repair-issues-for-one-root"):
            with self.subTest(section=section):
                self.assertIn(section, forbidden)


if __name__ == "__main__":
    unittest.main()
