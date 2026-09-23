from __future__ import annotations

import copy
import json
from pathlib import Path
import unittest

from test_protocol_schemas import load_schema, validate_subset
from test_v40_operation_contracts import (
    SHA_A,
    TREE_A,
    aggregation_example,
    assurance_example,
    finding_example,
)
from v40_rules import (
    fast_path_eligible,
    validate_assurance_aggregation,
    validate_candidate_release_separation,
    validate_review_aggregation,
)

ROOT = Path(__file__).resolve().parents[1]
GOLDEN = ROOT / "templates" / "golden" / "V4_DOGFOOD_HARDENING_EXAMPLES.json"


def base_findings() -> list[dict]:
    return [
        finding_example("F-P2-1", "P2", "covered"),
        finding_example("F-P3-1", "P3", "recorded"),
    ]


class V40DogfoodHardeningTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.examples = json.loads(GOLDEN.read_text(encoding="utf-8"))
        cls.forbidden = cls.examples["forbidden"]

    def test_g1_p0_p1_blocker_class_cannot_be_disabled_by_flag(self) -> None:
        finding = copy.deepcopy(self.forbidden["p0_open_with_false_blocking"])
        self.assertTrue(
            validate_subset(finding, load_schema("review-finding-v1.schema.json")),
            "P0 with blocking=false must be structurally rejected",
        )

        aggregate = aggregation_example()
        aggregate["finding_refs"].append(finding["finding_id"])
        errors = validate_review_aggregation(
            aggregate,
            base_findings() + [finding],
            plan=assurance_example(),
        )
        self.assertTrue(any("PASS forbidden" in error for error in errors), errors)
        self.assertTrue(any("must declare blocking=true" in error for error in errors), errors)
        self.assertTrue(any(finding["finding_id"] in error for error in errors), errors)

    def test_g2_superseded_cannot_weaken_blocker_severity(self) -> None:
        source, target = copy.deepcopy(self.forbidden["p1_superseded_to_p3"])
        aggregate = aggregation_example()
        aggregate["finding_refs"] += [source["finding_id"], target["finding_id"]]
        errors = validate_review_aggregation(
            aggregate,
            base_findings() + [source, target],
            plan=assurance_example(),
        )
        self.assertTrue(any("weakens blocker severity" in error for error in errors), errors)
        self.assertTrue(any("PASS forbidden" in error for error in errors), errors)

    def test_g2_duplicate_cannot_weaken_blocker_severity(self) -> None:
        source, target = copy.deepcopy(self.forbidden["p1_duplicate_to_p3"])
        aggregate = aggregation_example()
        aggregate["finding_refs"] += [source["finding_id"], target["finding_id"]]
        errors = validate_review_aggregation(
            aggregate,
            base_findings() + [source, target],
            plan=assurance_example(),
        )
        self.assertTrue(any("weakens blocker severity" in error for error in errors), errors)
        self.assertTrue(any("PASS forbidden" in error for error in errors), errors)

    def test_g3_required_coverage_dimensions_are_attested(self) -> None:
        aggregate = copy.deepcopy(self.forbidden["aggregation_missing_coverage_dimension"])
        self.assertEqual(
            validate_subset(aggregate, load_schema("review-aggregation-v1.schema.json")),
            [],
        )
        errors = validate_assurance_aggregation(
            assurance_example(), aggregate, base_findings()
        )
        self.assertTrue(any("missing required coverage" in error for error in errors), errors)
        self.assertTrue(any("compatibility" in error for error in errors), errors)

        missing_shape = aggregation_example()
        del missing_shape["activity_results"][0]["coverage"]
        self.assertTrue(
            validate_subset(missing_shape, load_schema("review-aggregation-v1.schema.json"))
        )

    def test_validation_report_pass_requires_exit_zero(self) -> None:
        report = copy.deepcopy(self.forbidden["validation_report_pass_with_failed_exit"])
        errors = validate_subset(report, load_schema("validation-report.schema.json"))
        self.assertTrue(errors, "PASS with exit_code=1 must fail schema validation")

        report["exit_code"] = 0
        self.assertEqual(validate_subset(report, load_schema("validation-report.schema.json")), [])

    def test_release_ready_requires_frozen_candidate(self) -> None:
        case = copy.deepcopy(self.forbidden["release_ready_from_prepared"])
        errors = validate_candidate_release_separation(case["candidate"], case["release"])
        self.assertTrue(any("requires a FROZEN candidate" in error for error in errors), errors)

    def test_verdictive_release_states_remain_identity_bound(self) -> None:
        case = copy.deepcopy(self.forbidden["release_conditional_wrong_identity"])
        errors = validate_candidate_release_separation(case["candidate"], case["release"])
        self.assertTrue(any("candidate identity differs" in error for error in errors), errors)

        valid_release = copy.deepcopy(case["release"])
        valid_release["candidate_sha"] = SHA_A
        valid_release["tree_sha"] = TREE_A
        self.assertEqual(
            validate_candidate_release_separation(case["candidate"], valid_release), []
        )

    def test_ghost_finding_refs_fail_closed(self) -> None:
        aggregate = aggregation_example()
        aggregate["finding_refs"].append(self.forbidden["ghost_finding_ref"])
        errors = validate_review_aggregation(
            aggregate,
            base_findings(),
            plan=assurance_example(),
        )
        self.assertTrue(any("nonexistent finding identities" in error for error in errors), errors)

    def test_fast_path_authority_contradiction_is_disqualifying(self) -> None:
        context = copy.deepcopy(self.forbidden["fast_path_authority_contradiction"])
        self.assertFalse(fast_path_eligible(context))


if __name__ == "__main__":
    unittest.main()
