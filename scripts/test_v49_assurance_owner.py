from __future__ import annotations

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
CANONICAL = ROOT / "standards" / "ASSURANCE_PLAN_STANDARD.md"
LEGACY = ROOT / "docs" / "implementation" / "4.0.0" / "ASSURANCE_PLAN.md"
ADVERSARIAL = ROOT / "docs" / "implementation" / "4.0.0" / "ADVERSARIAL_REVIEW.md"
V1_SCHEMA = ROOT / "schemas" / "assurance-plan-v1.schema.json"
AGG_SCHEMA = ROOT / "schemas" / "review-aggregation-v1.schema.json"
REFERENCE = ROOT / "references" / "ASSURANCE_PLAN_OWNER_REFERENCE.md"


class AssuranceOwnerCanonicalizationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.canonical = CANONICAL.read_text(encoding="utf-8")
        cls.legacy = LEGACY.read_text(encoding="utf-8")
        cls.adversarial = ADVERSARIAL.read_text(encoding="utf-8")
        cls.reference = REFERENCE.read_text(encoding="utf-8")
        cls.v1 = json.loads(V1_SCHEMA.read_text(encoding="utf-8"))
        cls.aggregation = json.loads(AGG_SCHEMA.read_text(encoding="utf-8"))

    def test_exact_owner_continuity_is_declared(self) -> None:
        self.assertIn("CANONICAL_OWNER_ID=assurance-plan", self.canonical)
        self.assertIn("LEGACY_AUTHORITY=docs/implementation/4.0.0/ASSURANCE_PLAN.md", self.canonical)
        self.assertIn("V1_SCHEMA=schemas/assurance-plan-v1.schema.json", self.canonical)
        self.assertIn("OWNER_CONTINUITY=SAME_FAMILY", self.canonical)
        self.assertIn("same `assurance-plan` family", self.reference)

    def test_v1_machine_contract_remains_the_same_family(self) -> None:
        self.assertEqual(self.v1["title"], "AI Development Assurance Plan v1")
        self.assertEqual(self.v1["properties"]["protocol_version"]["const"], "ai-dev-assurance/v1")
        agg = self.v1["properties"]["aggregation"]["properties"]
        self.assertEqual(agg["policy"]["const"], "finding-union-blocker-dominance")
        self.assertEqual(agg["blocker_resolution"]["const"], "unresolved-valid-blocker-dominates")
        self.assertFalse(agg["majority_vote_for_correctness"]["const"])

    def test_aggregation_authority_is_preserved_not_redefined(self) -> None:
        self.assertIn("finding-union-blocker-dominance", self.canonical)
        self.assertIn("unresolved-valid-blocker-dominates", self.canonical)
        self.assertIn("aggregation.majority_vote_for_correctness=false", self.canonical)
        self.assertIn("a PASS from one reviewer cannot delete another reviewer's valid blocker", self.adversarial)
        self.assertIn("unresolved valid blocking findings cannot be canceled by unrelated PASS results", self.legacy)
        self.assertEqual(
            self.aggregation["properties"]["policy"]["const"],
            "finding-union-blocker-dominance",
        )

    def test_canonicalization_does_not_steal_gate_authority(self) -> None:
        for required in (
            "VALIDATION_STANDARD.md` owns executable Validation truth",
            "RELEASE_STANDARD.md` owns candidate/release authority",
            "Product, Architecture and Task authority are not granted by an Assurance Plan",
            "does not create a new assurance lifecycle",
        ):
            self.assertIn(required, self.canonical)

    def test_parallel_owner_and_majority_vote_are_forbidden(self) -> None:
        self.assertIn("creating a second `proportional-assurance` owner", self.canonical)
        self.assertIn("making majority vote an acceptance predicate", self.canonical)
        self.assertIn("invalidating historical v1 records", self.canonical)
        self.assertIn("FAIL_CLOSED / AUTHORITY_OR_ARCHITECTURE_ROUTING", self.reference)

    def test_t002_successor_scope_is_not_preimplemented(self) -> None:
        self.assertIn("v4.9 T-002 owns any authorized v2 proof/composition/currentness contract", self.canonical)
        self.assertIn("does not pre-authorize those semantics", self.canonical)
        self.assertNotIn("ASSURANCE_FLOOR =", self.canonical)


if __name__ == "__main__":
    result = unittest.TextTestRunner(verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromTestCase(AssuranceOwnerCanonicalizationTests)
    )
    raise SystemExit(0 if result.wasSuccessful() else 1)
