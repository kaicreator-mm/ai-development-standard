#!/usr/bin/env python3
"""T05 deterministic source examples; NOT live GitHub/Host validation."""
from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests/fixtures/v416/t05/scenarios.json"
DOC = ROOT / "references/ADS_V416_WEB_FIRST_WRITEBACK.md"


def route_source_step(step: dict) -> str:
    if not step["task_current"] or not step["claim_accepted"]:
        return "HOLD_NO_SOURCE_AUTHORITY"
    if step["prior_claim_ambiguous"] or step["competing_active_writer"]:
        return "HOLD_COMPETING_WRITER"
    if step["needs_physical"]:
        return "PHYSICAL_WITNESSED" if step["physical_witnessed"] else "LOCAL_PHYSICAL_REMAINDER"
    if step["web_capable"]:
        return "WEB_EXECUTABLE"
    if step["ci_capable"]:
        return "CI_EXECUTABLE"
    return "CAPABILITY_UNAVAILABLE"


def classify_native_writeback(ev: dict) -> str:
    if not ev["native_comment_id"] or not ev["native_readback"]:
        return "NOT_PUBLISHED"
    if not (ev["exact_subject_sha"] and ev["environment"] and ev["command"] and ev["exit_code"] is not None):
        return "UNQUALIFIED_TEST_TUPLE"
    if ev["event_kind"] == "REVIEW_RESULT":
        if not (ev["schema_shape_valid"] and ev["canonical_admitted"] and ev["independent_context"]):
            return "UNADMITTED_MACHINE_EVENT"
    return "NATIVE_EVIDENCE_RECONSTRUCTIBLE"


class T05SourceOnlyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.examples = json.loads(FIXTURES.read_text(encoding="utf-8"))
        cls.reference = DOC.read_text(encoding="utf-8")

    def test_unique_discriminator_coverage(self):
        self.assertEqual(self.examples["schema"], "ads/v416-t05-source-oracle/v1")
        cases = self.examples["routes"] + self.examples["evidence"]
        self.assertEqual(len(cases), 17)
        ids = [x["id"] for x in cases]
        self.assertEqual(len(ids), len(set(ids)))
        for prefix in ("C15_", "C16_"):
            self.assertTrue(any(x.startswith(prefix) for x in ids), prefix)

    def test_c15_step_capability_and_claim(self):
        for case in self.examples["routes"]:
            with self.subTest(case=case["id"]):
                self.assertEqual(route_source_step(case["input"]), case["expected"])

    def test_c16_native_writeback_and_independence(self):
        for case in self.examples["evidence"]:
            with self.subTest(case=case["id"]):
                self.assertEqual(classify_native_writeback(case["input"]), case["expected"])

    def test_existing_authority_is_explicit(self):
        for token in ("EXECUTION_PACK_STANDARD.md", "LOCAL_AGENT_HANDOFF_PROTOCOL.md",
                      "GITHUB_AGENT_INTERACTION_PROTOCOL.md", "VALIDATION_STANDARD.md",
                      "SINGLE_WRITER", "REVIEW_RESULT", "NOT_PUBLISHED", "NOT_RUN",
                      "pointer-only", "no new event subtype"):
            with self.subTest(token=token):
                self.assertIn(token.lower(), self.reference.lower())


if __name__ == "__main__":
    unittest.main(verbosity=2)
