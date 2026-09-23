from __future__ import annotations

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
FLOWS = ROOT / "templates" / "golden" / "V4_REFERENCE_FLOWS.json"

EXPECTED_SCENARIOS = {
    "major-product-definition",
    "major-architecture-freeze",
    "bounded-implementation",
    "high-risk-contract-security",
    "cross-artifact-coherence",
    "version-closure-release",
    "fast-path",
    "stale-identity-conflict-recovery",
}
ALLOWED_KINDS = {"PRODUCE", "RESEARCH", "ASSURE", "DECIDE", "CONTROL"}
ALLOWED_BINDINGS = {"exact-sha", "candidate", "project-defined"}
REQUIRED_ASSURANCE_KEYS = {
    "policy",
    "modes",
    "coverage",
    "independence_axes",
    "aggregation",
}


class V40ReferenceFlowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(FLOWS.read_text(encoding="utf-8"))
        cls.by_id = {scenario["id"]: scenario for scenario in cls.data["scenarios"]}

    def test_protocol_and_exact_scenario_set(self) -> None:
        self.assertEqual(self.data["schema"], "ai-dev/v4-reference-flows:1")
        self.assertEqual(set(self.by_id), EXPECTED_SCENARIOS)
        self.assertEqual(len(self.data["scenarios"]), len(EXPECTED_SCENARIOS))

    def test_every_scenario_exposes_orthogonal_contract_shape(self) -> None:
        for scenario_id, scenario in self.by_id.items():
            with self.subTest(scenario=scenario_id):
                self.assertTrue(scenario["operation_kinds"])
                self.assertTrue(set(scenario["operation_kinds"]).issubset(ALLOWED_KINDS))
                self.assertIn(scenario["identity_binding"], ALLOWED_BINDINGS)
                self.assertTrue(REQUIRED_ASSURANCE_KEYS.issubset(scenario["assurance"]))
                self.assertEqual(
                    scenario["assurance"]["aggregation"],
                    "finding-union-blocker-dominance",
                )
                self.assertTrue(scenario["assurance"]["coverage"])
                self.assertTrue(scenario["truth_dimensions"])
                self.assertTrue(scenario["non_substitution"].strip())
                self.assertTrue(scenario["failure_routes"])

    def test_bounded_implementation_keeps_routing_validation_review_separate(self) -> None:
        scenario = self.by_id["bounded-implementation"]
        self.assertEqual(scenario["identity_binding"], "exact-sha")
        self.assertIn("routing", scenario["truth_dimensions"])
        self.assertIn("validation", scenario["truth_dimensions"])
        self.assertIn("review-policy", scenario["truth_dimensions"])
        self.assertNotIn("model-diverse-adversarial", scenario["assurance"]["modes"])

    def test_high_risk_contract_requires_model_diverse_and_executable_assurance(self) -> None:
        scenario = self.by_id["high-risk-contract-security"]
        self.assertIn("model-diverse-adversarial", scenario["assurance"]["modes"])
        self.assertIn("executable-validation", scenario["assurance"]["modes"])
        self.assertIn("model", scenario["assurance"]["independence_axes"])
        self.assertIn("executor", scenario["assurance"]["independence_axes"])
        self.assertIn("evidence", scenario["assurance"]["independence_axes"])
        self.assertIn("model diversity", scenario["non_substitution"])

    def test_coherence_review_does_not_claim_integration_validation(self) -> None:
        scenario = self.by_id["cross-artifact-coherence"]
        self.assertIn("coherence-review", scenario["assurance"]["modes"])
        self.assertIn("executable-validation", scenario["assurance"]["modes"])
        self.assertIn("does not substitute", scenario["non_substitution"])

    def test_release_flow_keeps_candidate_release_and_repository_truth_distinct(self) -> None:
        scenario = self.by_id["version-closure-release"]
        self.assertEqual(scenario["identity_binding"], "candidate")
        self.assertIn("CONTROL", scenario["operation_kinds"])
        self.assertIn("DECIDE", scenario["operation_kinds"])
        self.assertIn("candidate", scenario["truth_dimensions"])
        self.assertIn("release", scenario["truth_dimensions"])
        self.assertIn("PR PASS", scenario["non_substitution"])

    def test_fast_path_elides_ceremony_not_truth(self) -> None:
        scenario = self.by_id["fast-path"]
        self.assertEqual(scenario["operation_kinds"], ["PRODUCE", "ASSURE", "CONTROL"])
        self.assertEqual(scenario["assurance"]["modes"], ["executable-validation"])
        self.assertIn("never required truth", scenario["non_substitution"])

    def test_stale_identity_recovery_preserves_history_and_route_non_authority(self) -> None:
        scenario = self.by_id["stale-identity-conflict-recovery"]
        self.assertIn("STALE_IDENTITY", scenario["failure_routes"])
        self.assertIn("VALIDATION_NEEDED", scenario["failure_routes"])
        self.assertIn("stale evidence remains historical", scenario["non_substitution"])
        self.assertIn("non-authoritative derived state", scenario["non_substitution"])

    def test_dogfood_plan_is_blind_model_diverse_and_not_majority_voting(self) -> None:
        dogfood = self.data["dogfood"]
        self.assertEqual(
            dogfood["subject_identity_ref"],
            f"sha:{self.data['subject_baseline']}",
        )
        self.assertEqual(dogfood["blind_first_pass_count"], 2)
        self.assertEqual(dogfood["mode"], "model-diverse-adversarial")
        self.assertEqual(dogfood["context_independence"], "required")
        self.assertEqual(dogfood["model_independence"], "required")
        self.assertEqual(dogfood["executor_independence"], "required")
        self.assertFalse(dogfood["collaboration_before_first_pass"])
        self.assertFalse(dogfood["majority_vote_for_correctness"])
        self.assertEqual(
            dogfood["aggregation"],
            "finding-union-blocker-dominance",
        )
        self.assertEqual(
            dogfood["requested_route_authority"],
            "NON_AUTHORITATIVE_DERIVED_STATE",
        )


if __name__ == "__main__":
    unittest.main()
