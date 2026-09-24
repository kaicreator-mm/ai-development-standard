from __future__ import annotations

import copy
import unittest

from test_protocol_schemas import load_schema, validate_subset
from v40_semantics import (
    validate_assurance_aggregation,
    validate_assurance_semantics,
    validate_repository_integration_event,
    validate_review_aggregation,
)

SHA_A = "a" * 40
TREE_A = "b" * 40
SHA_MERGED = "c" * 40
TREE_MERGED = "d" * 40


def provenance(*, provider: str, family: str, model: str, suffix: str, system: str = "sys", config: str = "cfg") -> dict:
    return {
        "provider": provider,
        "model_family": family,
        "model_id": model,
        "executor_id": f"executor-{suffix}",
        "context_ref": f"context:{suffix}",
        "blind_first_pass_ref": f"evidence:blind-{suffix}",
        "architecture_system": system,
        "configuration_fingerprint": config,
    }


def plan(*, basis: str = "provider-diverse") -> dict:
    return {
        "protocol_version": "ai-dev-assurance/v1",
        "assurance_plan_id": "assurance:t012:pre-release",
        "operation_id": "op:t012:pre-release",
        "subject_ref": "issue:#170",
        "subject_identity_ref": f"sha:{SHA_A}",
        "identity_binding": "exact-sha",
        "finding_disposition_policy": "p2-and-p3-explicit",
        "activities": [
            {
                "assurance_id": "review-mda",
                "kind": "review",
                "policy": "required",
                "mode": "model-diverse-adversarial",
                "coverage": ["pre-release-machine-contract"],
                "independence": {"context": "required", "model": "required", "executor": "required", "evidence": "none"},
                "depends_on": [],
                "blind_first_pass_ref": "evidence:blind-group",
                "model_diversity_basis": basis,
                "independence_basis_ref": "evidence:diversity-basis",
                "collaboration_selected": False,
            }
        ],
        "aggregation": {
            "policy": "finding-union-blocker-dominance",
            "blocker_resolution": "unresolved-valid-blocker-dominates",
            "majority_vote_for_correctness": False,
            "conflict_route": "changes-requested",
        },
        "completion_predicate": "required assurance complete",
    }


def aggregate(records: list[dict]) -> dict:
    return {
        "protocol_version": "ai-dev/review-aggregation-v1",
        "aggregate_id": "agg:t012:pre-release",
        "assurance_plan_id": "assurance:t012:pre-release",
        "subject_identity_ref": f"sha:{SHA_A}",
        "judgment": "PASS",
        "requested_route": "review-ready",
        "requested_route_authority": "NON_AUTHORITATIVE_DERIVED_STATE",
        "aggregation_policy": "finding-union-blocker-dominance",
        "activity_results": [
            {
                "assurance_id": "review-mda",
                "subject_identity_ref": f"sha:{SHA_A}",
                "result_ref": "issue:#170",
                "result_identity_ref": f"sha:{SHA_A}",
                "result_state": "PASS",
                "result_kind": "review",
                "coverage": ["pre-release-machine-contract"],
                "reviewer_provenance": records[0],
                "reviewer_provenances": records,
            }
        ],
        "finding_refs": [],
        "unresolved_blocker_refs": [],
        "conflict_refs": [],
    }


class T012PreReleaseHardeningTests(unittest.TestCase):
    def test_u4_exact_sha_identity_is_machine_bound(self) -> None:
        good = plan()
        self.assertEqual(validate_assurance_semantics(good), [])
        bad = copy.deepcopy(good)
        bad["subject_identity_ref"] = "not-a-sha"
        self.assertTrue(any("sha:<40-hex>" in error for error in validate_assurance_semantics(bad)))

        schema = load_schema("assurance-plan-v1.schema.json")
        self.assertEqual(validate_subset(good, schema), [])
        self.assertTrue(validate_subset(bad, schema))

    def test_u5_depends_on_requires_existing_acyclic_activities(self) -> None:
        unknown = plan()
        unknown["activities"][0]["depends_on"] = ["ghost"]
        self.assertTrue(any("unknown assurance activity" in error for error in validate_assurance_semantics(unknown)))

        cyclic = plan()
        cyclic["activities"].append({
            "assurance_id": "review-b",
            "kind": "review",
            "policy": "required",
            "mode": "single-independent",
            "coverage": ["coherence"],
            "independence": {"context": "required", "model": "none", "executor": "required", "evidence": "none"},
            "depends_on": ["review-mda"],
            "collaboration_selected": False,
        })
        cyclic["activities"][0]["depends_on"] = ["review-b"]
        self.assertTrue(any("acyclic" in error for error in validate_assurance_semantics(cyclic)))

    def test_u7_unknown_aggregation_judgment_fails_closed(self) -> None:
        p = plan()
        a = aggregate([
            provenance(provider="provider-a", family="family-a", model="model-a", suffix="a"),
            provenance(provider="provider-b", family="family-b", model="model-b", suffix="b"),
        ])
        a["judgment"] = "MAYBE_PASS"
        self.assertTrue(any("judgment" in error for error in validate_assurance_aggregation(p, a, [])))
        self.assertTrue(any("judgment" in error for error in validate_review_aggregation(a, [], plan=p)))

    def test_u8_single_composite_mda_enforces_every_declared_basis(self) -> None:
        cases = {
            "provider-diverse": (
                provenance(provider="same", family="family-a", model="model-a", suffix="a"),
                provenance(provider="same", family="family-b", model="model-b", suffix="b"),
                "distinct providers",
            ),
            "model-family-diverse": (
                provenance(provider="provider-a", family="same", model="model-a", suffix="a"),
                provenance(provider="provider-b", family="same", model="model-b", suffix="b"),
                "distinct model families",
            ),
            "architecture-system-diverse": (
                provenance(provider="provider-a", family="family-a", model="model-a", suffix="a", system="same"),
                provenance(provider="provider-b", family="family-b", model="model-b", suffix="b", system="same"),
                "distinct architecture systems",
            ),
            "project-approved-different-configuration": (
                provenance(provider="provider-a", family="family-a", model="model-a", suffix="a", config="same"),
                provenance(provider="provider-b", family="family-b", model="model-b", suffix="b", config="same"),
                "distinct configuration fingerprints",
            ),
        }
        for basis, (left, right, expected) in cases.items():
            with self.subTest(basis=basis):
                errors = validate_assurance_aggregation(plan(basis=basis), aggregate([left, right]), [])
                self.assertTrue(any(expected in error for error in errors), errors)

        positives = {
            "provider-diverse": [
                provenance(provider="provider-a", family="family-a", model="model-a", suffix="a"),
                provenance(provider="provider-b", family="family-b", model="model-b", suffix="b"),
            ],
            "model-family-diverse": [
                provenance(provider="provider-a", family="family-a", model="model-a", suffix="a"),
                provenance(provider="provider-a", family="family-b", model="model-b", suffix="b"),
            ],
            "architecture-system-diverse": [
                provenance(provider="provider-a", family="family-a", model="model-a", suffix="a", system="system-a"),
                provenance(provider="provider-a", family="family-b", model="model-b", suffix="b", system="system-b"),
            ],
            "project-approved-different-configuration": [
                provenance(provider="provider-a", family="family-a", model="model-a", suffix="a", config="config-a"),
                provenance(provider="provider-a", family="family-b", model="model-b", suffix="b", config="config-b"),
            ],
        }
        for basis, records in positives.items():
            with self.subTest(positive_basis=basis):
                self.assertEqual(validate_assurance_aggregation(plan(basis=basis), aggregate(records), []), [])

    def test_u6_repository_integration_requires_release_precondition_link(self) -> None:
        event = {
            "schema": "ai-dev/event-v2",
            "event": "REPOSITORY_INTEGRATION_RESULT",
            "candidate_sha": SHA_A,
            "tree_sha": TREE_A,
            "merge_result_sha": SHA_MERGED,
            "merge_result_tree": TREE_MERGED,
            "evidence": "evidence:integration-v4",
            "release_qualification_ref": "issue:#85",
            "release_qualification_state": "READY",
            "release_candidate_identity": f"candidate:{SHA_A}:{TREE_A}",
        }
        self.assertEqual(validate_repository_integration_event(event), [])
        schema = load_schema("repository-integration-v4-precondition.schema.json")
        self.assertEqual(validate_subset(event, schema), [])

        missing = copy.deepcopy(event)
        missing.pop("release_qualification_ref")
        self.assertTrue(any("release_qualification_ref" in error for error in validate_repository_integration_event(missing)))
        self.assertTrue(validate_subset(missing, schema))

        stale = copy.deepcopy(event)
        stale["release_candidate_identity"] = f"candidate:{'e' * 40}:{TREE_A}"
        self.assertTrue(any("same frozen candidate" in error for error in validate_repository_integration_event(stale)))

        not_ready = copy.deepcopy(event)
        not_ready["release_qualification_state"] = "BLOCKED"
        self.assertTrue(any("READY or CONDITIONAL" in error for error in validate_repository_integration_event(not_ready)))
        self.assertTrue(validate_subset(not_ready, schema))


if __name__ == "__main__":
    unittest.main()
