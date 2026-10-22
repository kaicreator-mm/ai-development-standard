#!/usr/bin/env python3
"""T06 bounded source-contract oracles. NOT a production Tool/Claim/Effect engine."""
from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests/fixtures/v416/t06/scenarios.json"
DOC = ROOT / "docs/implementation/4.16.0/G_AGENT_OWNER_CROSSWALK.md"


def interpret_source_example(t: dict) -> str:
    # These are local example classifications, not new canonical ADS statuses.
    if t["historical_v1"]:
        return "HISTORICAL_ONLY"
    if not all(t[k] for k in ("current_task", "profile_current", "capability_evidence_current", "role_eligible")):
        return "REFUSE_STALE_SELECTION"
    intersection = set(t["parent_authority"]) & set(t["task_authority"]) & set(t["role_authority"]) & set(t["external_authority"])
    if not set(t["child_requests"]).issubset(intersection):
        return "REFUSE_AUTHORITY_ESCALATION"
    if not t["claim_accepted"]:
        return "REFUSE_NO_CLAIM"
    if t["conflicting_claim"]:
        return "REFUSE_CONFLICTING_CLAIM"
    if t["cancel_requested"] and t["late_callback"]:
        return "HOLD_LATE_CALLBACK"
    if t["effect_possible"] and not t["provider_commit_witness"]:
        return "HOLD_EFFECT_UNKNOWN"
    if not (t["independent_verifier_pass"] and t["github_readback"]):
        return "STRICT_GATE_UNPROVEN"
    return "RECONSTRUCTIBLE"


class T06SourceOnlyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fixture = json.loads(FIXTURES.read_text(encoding="utf-8"))
        cls.doc = DOC.read_text(encoding="utf-8")

    def test_schema_and_unique_scenarios(self) -> None:
        self.assertEqual(self.fixture["schema"], "ads/v416-t06-source-oracle/v1")
        self.assertEqual(len(self.fixture["cases"]), 13)
        ids = [x["id"] for x in self.fixture["cases"]]
        self.assertEqual(len(ids), len(set(ids)))
        for prefix in ("A03_", "G09_", "G10_", "G11_", "G12_"):
            self.assertTrue(any(x.startswith(prefix) for x in ids), prefix)

    def test_all_fixtures(self) -> None:
        for case in self.fixture["cases"]:
            with self.subTest(case=case["id"]):
                self.assertEqual(interpret_source_example(case["input"]), case["expected"])

    def test_owner_not_duplicated(self) -> None:
        for owner in ("EXECUTION_ARCHITECTURE_STANDARD.md", "EXTERNAL_SYSTEM_EXECUTION_STANDARD.md",
                      "GITHUB_AGENT_INTERACTION_PROTOCOL.md", "§28.1", "§21.2",
                      "ALREADY_DEFINED", "NEEDS_CLARIFICATION", "IMPLEMENTATION_ONLY",
                      "EFFECT_OUTCOME_UNKNOWN", "NOT_RUN"):
            with self.subTest(owner=owner):
                self.assertIn(owner, self.doc)
        self.assertIn("no new mandatory v1 field", self.doc.lower())

    def test_old_profile_never_mints_authority(self) -> None:
        case = next(v for v in self.fixture["cases"] if v["id"].startswith("G12_"))
        self.assertEqual(interpret_source_example(case["input"]), "HISTORICAL_ONLY")


if __name__ == "__main__":
    unittest.main(verbosity=2)
