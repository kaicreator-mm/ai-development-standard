"""ADS v4.18 G418 source-only planning conformance.

This is an E1 normative-source/reference consistency test, NOT evidence of
real Agent execution, native GitHub Issue mutations, physical Host validation,
human authorization, or measured parallelism gains.
"""

from __future__ import annotations

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
REFERENCE_PATH = ROOT / "references" / "TASK_DECOMPOSITION_REFERENCE.md"
L2_PATH = ROOT / "docs" / "implementation" / "4.18.0" / "L2_ARCHITECTURE_EVIDENCE.md"
COVERAGE_PATH = ROOT / "templates" / "golden" / "STANDARD_COVERAGE.json"
CONFORMANCE_CORPUS = ROOT / "templates" / "golden" / "STANDARD_CONFORMANCE_EXAMPLES.md"

EXPECTED_IDS = {f"G418-{number:02d}" for number in range(1, 8)}


def golden_rows() -> dict[str, tuple[str, str, str]]:
    """Read the existing registered TDS reference; do not invent an alternate owner."""
    document = REFERENCE_PATH.read_text(encoding="utf-8")
    section = document.split("## 10. Optional v4.18 Safe Task DAG Planning Patterns", 1)
    if len(section) != 2:
        raise ValueError("Missing unique v4.18 TDS planning reference heading")
    found: dict[str, tuple[str, str, str]] = {}
    for line in section[1].splitlines():
        if not line.startswith("| G418-"):
            continue
        fields = [part.strip() for part in line.strip().strip("|").split("|")]
        if len(fields) != 4:
            raise ValueError(f"Incorrect G418 table shape: {line!r}")
        golden_id, pattern, positive, forbidden = fields
        if golden_id in found:
            raise ValueError(f"Duplicate G418 ID: {golden_id}")
        found[golden_id] = (pattern, positive, forbidden)
    return found


class PlanningSourceConformance(unittest.TestCase):
    def test_g418_cases_cover_frozen_l2_contract(self) -> None:
        self.assertEqual(set(golden_rows()), EXPECTED_IDS)
        l2 = L2_PATH.read_text(encoding="utf-8")
        for case in sorted(EXPECTED_IDS):
            with self.subTest(case=case):
                self.assertIn(case, l2, "Golden needs an exact L2 acceptance basis")

    def test_positive_and_forbidden_are_concrete_distinct_pairs(self) -> None:
        for case, (pattern, positive, forbidden) in golden_rows().items():
            with self.subTest(case=case):
                self.assertGreater(len(pattern), 5)
                self.assertGreater(len(positive), 40)
                self.assertGreater(len(forbidden), 40)
                self.assertNotEqual(positive, forbidden)
                self.assertNotIn("<placeholder>", positive + forbidden)
                self.assertNotIn("TBD", positive + forbidden)

    def test_options_preserve_native_dependency_and_claim_admission(self) -> None:
        case = golden_rows()["G418-05"]
        self.assertIn("blocked_by", case[1])
        self.assertIn("read-only PREP", case[1])
        self.assertIn("HOLD", case[1])
        self.assertIn("Claim", case[1])
        self.assertIn("ready_builder", case[2])
        self.assertIn("blocked_by", case[2])
        ref = REFERENCE_PATH.read_text(encoding="utf-8")
        self.assertIn("non-authoritative", ref)
        self.assertIn("JIT/Claim", ref)

    def test_scaffold_and_atomicity_are_not_bypassed(self) -> None:
        scaffold = golden_rows()["G418-03"]
        atomic = golden_rows()["G418-06"]
        self.assertIn("MI", scaffold[1])
        self.assertIn("§10A", scaffold[1])
        self.assertIn("two concurrent Tasks", scaffold[2])
        self.assertIn("atomic", atomic[1])
        self.assertIn("partial-invalid", atomic[2])

    def test_risk_roles_and_human_authority_not_self_asserted(self) -> None:
        agent = golden_rows()["G418-04"]
        human = golden_rows()["G418-07"]
        self.assertIn("independent Reviewer", agent[1])
        self.assertIn("self-approves", agent[2])
        self.assertIn("Host PASS", agent[2])
        self.assertIn("protected exact-scope", human[1])
        self.assertIn("HUMAN_APPROVED", human[2])

    def test_registered_single_golden_owner_is_preserved(self) -> None:
        coverage = json.loads(COVERAGE_PATH.read_text(encoding="utf-8"))
        rows = [item for item in coverage["coverage"]
                if item["standard"] == "standards/TASK_DECOMPOSITION_STANDARD.md"]
        self.assertEqual(len(rows), 1)
        self.assertEqual(
            rows[0]["golden_ref"], "references/TASK_DECOMPOSITION_REFERENCE.md"
        )
        corpus = CONFORMANCE_CORPUS.read_text(encoding="utf-8")
        for case in EXPECTED_IDS:
            self.assertNotIn(case, corpus, "Do not duplicate TDS's Golden home")

    def test_source_only_boundary_and_existing_examples(self) -> None:
        ref = REFERENCE_PATH.read_text(encoding="utf-8")
        self.assertIn("E1 source-only", ref)
        self.assertIn("They do not demonstrate multi-Agent runtime execution", ref)
        for section in (
            "## 2. Good parallel split example",
            "## 5. Central wiring checklist",
            "## 7. Decomposition review prompts",
            "## 9. Agent-dispatch worksheet check",
        ):
            self.assertIn(section, ref)


if __name__ == "__main__":
    unittest.main()
