from __future__ import annotations

import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
STANDARD = ROOT / "standards" / "ASSURANCE_PLAN_STANDARD.md"
REFERENCE = ROOT / "references" / "ASSURANCE_PLAN_V2_REFERENCE.md"
V1 = ROOT / "schemas" / "assurance-plan-v1.schema.json"
V2 = ROOT / "schemas" / "assurance-plan-v2.schema.json"
COMPAT_SCHEMA = ROOT / "schemas" / "compatibility-record-v1.schema.json"
COMPAT = ROOT / "references" / "ASSURANCE_PLAN_V2_COMPATIBILITY.json"

EXPECTED_V1_BLOB = "bd9489097da87024349623cf3f7c1d83e74f6624"


def git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


class AssurancePlanV2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.standard = STANDARD.read_text(encoding="utf-8")
        cls.reference = REFERENCE.read_text(encoding="utf-8")
        cls.v1 = json.loads(V1.read_text(encoding="utf-8"))
        cls.v2 = json.loads(V2.read_text(encoding="utf-8"))
        cls.compat_schema = json.loads(COMPAT_SCHEMA.read_text(encoding="utf-8"))
        cls.compat = json.loads(COMPAT.read_text(encoding="utf-8"))

    def test_same_family_successor_preserves_v1_identity(self) -> None:
        props = self.v2["properties"]
        self.assertEqual(props["protocol_version"]["const"], "ai-dev-assurance/v2")
        self.assertEqual(props["owner_family"]["const"], "assurance-plan")
        self.assertEqual(props["predecessor_protocol_version"]["const"], "ai-dev-assurance/v1")
        self.assertEqual(git_blob_sha(V1), EXPECTED_V1_BLOB)
        self.assertIn("V2_OWNER_FAMILY=assurance-plan", self.standard)
        self.assertIn("same-family versioned successor", self.standard)

    def test_reduction_requires_positive_owner_permission_and_true_proofs(self) -> None:
        concern = self.v2["properties"]["concern_resolutions"]["items"]
        reduction = concern["allOf"][0]
        then = reduction["then"]["properties"]
        owner_decision = then["owner_permission"]["properties"]["decision"]["const"]
        self.assertEqual(owner_decision, "ALLOW_REDUCTION")
        proofs = then["predicate_proofs"]
        self.assertEqual(proofs["minItems"], 1)
        self.assertEqual(proofs["items"]["properties"]["state"]["const"], "TRUE")
        proof_states = concern["properties"]["predicate_proofs"]["items"]["properties"]["state"]["enum"]
        self.assertEqual(proof_states, ["TRUE", "FALSE", "UNKNOWN"])

    def test_proof_basis_excludes_model_judgment_and_weak_signals(self) -> None:
        bases = (
            self.v2["properties"]["concern_resolutions"]["items"]["properties"]
            ["predicate_proofs"]["items"]["properties"]["basis"]["enum"]
        )
        self.assertEqual(bases, ["durable-fact", "deterministic-check", "owner-record"])
        for forbidden in ("model-judgment", "provider-strength", "confidence"):
            self.assertNotIn(forbidden, bases)
        for signal in (
            "docs-only",
            "risk:low",
            "Fast Path",
            "recommended + skip",
            "small file count",
            "model/provider strength",
        ):
            self.assertIn(signal, self.standard)
        self.assertIn("model judgment/provider strength/confidence MUST NOT be the sole proof basis", self.standard)

    def test_cross_owner_composition_is_conjunctive_no_cancellation(self) -> None:
        composition = self.v2["properties"]["cross_owner_composition"]["properties"]
        self.assertEqual(composition["policy"]["const"], "conjunctive-no-cancellation")
        self.assertFalse(composition["cancellation_allowed"]["const"])
        self.assertIn("One owner's permission or local PASS MUST NOT cancel another owner's current requirement", self.standard)

    def test_floor_and_selected_path_are_distinct(self) -> None:
        props = self.v2["properties"]
        self.assertIn("assurance_floor", props)
        self.assertIn("selected_path", props)
        self.assertEqual(props["assurance_floor"]["properties"]["composition"]["const"], "owner-scoped-conjunctive-floor")
        self.assertEqual(
            props["selected_path"]["properties"]["relation_to_floor"]["enum"],
            ["SATISFIES_FLOOR", "STRONGER_THAN_FLOOR", "BLOCKED"],
        )
        self.assertIn("A chosen execution path cannot retroactively redefine the floor", self.standard)

    def test_currentness_binding_covers_all_required_inputs(self) -> None:
        currentness = self.v2["properties"]["currentness_binding"]
        required = set(currentness["required"])
        expected = {
            "subject_identity_ref",
            "owner_authority_refs",
            "owner_authority_digest",
            "proof_input_refs",
            "proof_input_digest",
            "task_pack_ref",
            "task_pack_digest",
            "release_decision_refs",
            "release_decision_digest",
            "unresolved_finding_refs",
            "unresolved_finding_digest",
            "binding_digest",
            "state",
        }
        self.assertTrue(expected.issubset(required))
        self.assertEqual(currentness["properties"]["rule"]["const"], "all-components-exact-current")
        self.assertEqual(currentness["properties"]["state"]["enum"], ["CURRENT", "STALE", "UNKNOWN"])
        self.assertIn("An empty Release-decision or unresolved-finding set is still bound by its digest", self.standard)
        self.assertIn("`STALE` and `UNKNOWN` MUST NOT authorize a lower assurance path", self.standard)

    def test_adverse_findings_and_aggregation_authority_are_preserved(self) -> None:
        self.assertEqual(
            self.v2["properties"]["finding_carry_forward_policy"]["const"],
            "unresolved-valid-findings-carry-forward",
        )
        v1_agg = self.v1["properties"]["aggregation"]["properties"]
        v2_agg = self.v2["properties"]["aggregation"]["properties"]
        for key in ("policy", "blocker_resolution", "majority_vote_for_correctness"):
            self.assertEqual(v1_agg[key]["const"], v2_agg[key]["const"])
        self.assertIn("A new reviewer, new model, new route, or unrelated PASS cannot make a current adverse finding disappear", self.standard)

    def test_v42_compatibility_record_is_identity_bound_and_dimension_specific(self) -> None:
        self.assertTrue(set(self.compat_schema["required"]).issubset(self.compat))
        self.assertEqual(self.compat["contract"]["identity"], "assurance-plan")
        self.assertEqual(self.compat["baseline"]["sha_or_digest"], f"git-blob:{git_blob_sha(V1)}")
        self.assertEqual(self.compat["candidate"]["sha_or_digest"], f"git-blob:{git_blob_sha(V2)}")
        outcomes = {item["name"]: item["outcome"] for item in self.compat["dimensions"]}
        self.assertEqual(outcomes["owner-family-semantics"], "COMPATIBLE")
        self.assertEqual(outcomes["historical-v1-record-validity"], "COMPATIBLE")
        self.assertEqual(outcomes["aggregation-authority"], "COMPATIBLE")
        self.assertEqual(outcomes["v1-parser-accepts-v2-instance"], "INCOMPATIBLE")
        self.assertEqual(outcomes["version-aware-adoption"], "CONDITIONALLY_COMPATIBLE")
        self.assertIn("a v1-only parser is not assumed to accept a v2 instance", self.standard)

    def test_owner_boundaries_do_not_preimplement_sibling_tasks(self) -> None:
        for phrase in (
            "Authority/Applicability or State registry integration (T-003)",
            "execution reducer, JIT, Dispatch/Claim/merge-time recheck (T-007)",
            "gate-owned evidence transfer/currentness integration (T-010)",
            "central manifest/adoption wiring (T-011)",
        ):
            self.assertIn(phrase, self.standard)
        self.assertIn("T-002 does not own", self.reference)


if __name__ == "__main__":
    unittest.main()
