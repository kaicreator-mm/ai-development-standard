"""Bounded metamorphic/negative cases of an isolated synthetic PRD model.

No real ADS agent, credentials, authority, evidence store or standard verifier
is exercised. These tests are *model self-consistency* only, NOT P1/P2/P3.
"""
import itertools
import unittest
from product_trace_probe import evaluate

JOBS = tuple(f"J{n:02d}" for n in range(1, 13))
LEVELS = tuple(f"A{n}" for n in range(5))


def trace(jobs=(), adoption="A0", **kwargs):
    data = {"jobs": list(jobs), "adoption": adoption, "verified_evidence": []}
    data.update(kwargs)
    return data


class MetamorphicProductAcceptance(unittest.TestCase):
    def test_all_4096_job_subsets_obligation_union(self):
        """No compound set loses any requirement found in a singleton job."""
        basis = {job: set(evaluate(trace([job]))["required"]) for job in JOBS}
        for bits in range(1 << len(JOBS)):
            subset = [job for i, job in enumerate(JOBS) if bits & (1 << i)]
            expected = set().union(*(basis[job] for job in subset))
            actual = set(evaluate(trace(subset))["required"])
            self.assertEqual(expected, actual, f"jobs={subset!r}")

    def test_all_20480_job_profile_samples_same_hard_floor(self):
        for bits in range(1 << len(JOBS)):
            subset = [job for i, job in enumerate(JOBS) if bits & (1 << i)]
            expected = evaluate(trace(subset, "A0"))["required"]
            for level in LEVELS:
                self.assertEqual(expected, evaluate(trace(subset, level))["required"],
                                 f"job_mask={bits} adoption={level}")

    def test_singletons_pairwise_triples_never_drop_required_evidence(self):
        for n in (1, 2, 3):
            for combo in itertools.combinations(JOBS, n):
                base = set(evaluate(trace(combo))["required"])
                for extra in JOBS:
                    superset = set(evaluate(trace([*combo, extra]))["required"])
                    self.assertTrue(base <= superset, (combo, extra))

    def test_extra_observed_risk_never_deletes_mandatory_gate(self):
        for level in LEVELS:
            base = set(evaluate(trace(["J03", "J05"], level))["required"])
            for key in ("security_sensitive", "persistent_migration", "external_write",
                        "public_contract_delta", "upstream_reuse", "human_approval_required"):
                actual = set(evaluate(trace(["J03", "J05"], level,
                    observed={key: True}))["required"])
                self.assertTrue(base <= actual, (key, level))

    def test_missing_claim_identity_fails_closed_without_crash(self):
        result = evaluate(trace(["J02"], claims=[{"state": "CLAIMED"}]))
        self.assertEqual(result["verdict"], "DEMO_UNVERIFIED")
        self.assertIn("CLAIM_PROTECTED_KEY_MISSING", result["unknowns"])

    def test_unclassified_empty_input_never_permitted(self):
        result = evaluate(trace([]))
        self.assertEqual(result["verdict"], "DEMO_UNVERIFIED")
        self.assertIn("UNCLASSIFIED_EMPTY_TRACE", result["unknowns"])

    def test_unrelated_review_conflict_does_not_block_current_target(self):
        result = evaluate(trace(["J02"], action={"merge": True, "head": "CURRENT"}, reviews=[
            {"head": "UNRELATED", "verdict": "PASS", "current": True, "accepted": True},
            {"head": "UNRELATED", "verdict": "CHANGES_REQUESTED", "current": True,
             "accepted": True}]))
        self.assertEqual(result["verdict"], "DEMO_ALLOW")

    def test_merge_requires_exact_subject_identity(self):
        result = evaluate(trace(["J02"], action={"merge": True}))
        self.assertIn("MERGE_EXACT_HEAD_MISSING", result["unknowns"])
        self.assertEqual(result["verdict"], "DEMO_UNVERIFIED")

    def test_required_review_no_pass_fail_closed(self):
        result = evaluate(trace(["J02"], action={"merge": True, "head": "H",
            "independent_review_required": True}, reviews=[]))
        self.assertIn("REQUIRED_CURRENT_REVIEW_NOT_PROVEN", result["unknowns"])

    def test_current_changes_requested_blocks_merge_even_without_pass(self):
        result = evaluate(trace(["J02"], action={"merge": True, "head": "H"},
            reviews=[{"head": "H", "verdict": "CHANGES_REQUESTED", "accepted": True,
                      "current": True}]))
        self.assertIn("CURRENT_CHANGES_REQUESTED", result["failures"])

    def test_missing_both_job_and_adoption_stays_unverified(self):
        result = evaluate({"jobs": [], "verified_evidence": []})
        self.assertIn("UNKNOWN_ADOPTION_LEVEL", result["unknowns"])
        self.assertIn("UNCLASSIFIED_EMPTY_TRACE", result["unknowns"])

    def test_unknown_job_with_valid_siblings_never_passes(self):
        result = evaluate(trace(["J02", "J99"]))
        self.assertIn("UNKNOWN_JOB_CLASS", result["unknowns"])
        self.assertNotEqual(result["verdict"], "DEMO_ALLOW")

    def test_known_stricter_denial_survives_more_evidence(self):
        condition = dict(jobs=["J07"], adoption="A4",
                         override={"weakens_mandatory_floor": True})
        for evidences in ([], ["independent_security_review"], ["unknown_token"]):
            result = evaluate({**condition, "verified_evidence": evidences})
            self.assertEqual(result["verdict"], "DEMO_DENY")

    def test_human_denial_not_overridden_by_scheduler_or_capability(self):
        result = evaluate(trace(["J08"], action={"mutate_or_release": True},
            human={"decision": "DENY", "successor_ready": True},
            actor={"real_host_evidence_verified": True},
            verified_evidence=["authorized_external_effect"]))
        self.assertIn("HUMAN_DENIAL_NOT_SUPERSEDED", result["failures"])


if __name__ == "__main__":
    unittest.main()
