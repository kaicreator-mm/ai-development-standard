from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import subprocess
import unittest

from test_protocol_schemas import load_schema, validate_subset


ROOT = Path(__file__).resolve().parents[1]
EA = ROOT / "standards" / "EXECUTION_ARCHITECTURE_STANDARD.md"
REFERENCE = ROOT / "references" / "TASK_LEARNING_V2_REFERENCE.md"

BASE_SHA = "ebcaf0c2502cab35edc76aa5af33df41b09fad98"
EA_HEADING = "## 30. Task Learning evidence owner contract (v4.11, additive)"
REF_HEADING = "## v4.11 owner-local admissibility clarification"

SCHEMA_V1 = load_schema("task-learning-v1.schema.json")
SCHEMA_V2 = load_schema("task-learning-v2.schema.json")

SUBJECT_A = "git:kaicreator-mm/example@1111111111111111111111111111111111111111"
SUBJECT_B = "git:kaicreator-mm/example@2222222222222222222222222222222222222222"

AUTHORITY_MUTATIONS = {
    "PRODUCT",
    "L2",
    "TASK",
    "DAG",
    "NORMATIVE_ADS",
    "GATE_PASS",
    "EVOLUTION_APPROVE",
}


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        encoding="utf-8",
        check=check,
    )


def valid_v2_record(*, negative: bool = False) -> dict:
    summary = (
        "Constraint reproduced: stale owner pin caused deterministic currentness rejection."
        if negative
        else "Exact-subject test evidence supports one reusable implementation invariant."
    )
    return {
        "schema_version": "ai-dev/task-learning-v2",
        "owner_family": "task-learning",
        "predecessor_protocol_version": "ai-dev/task-learning-v1",
        "learning_id": "learning:T14:negative" if negative else "learning:T14:positive",
        "repository_ref": "github:kaicreator-mm/ai-development-standard",
        "work_item_ref": "github:kaicreator-mm/ai-development-standard#1017",
        "implementation_subject_ref": SUBJECT_A,
        "authority_refs": ["task-pack:v4.11.0/T14"],
        "summary": summary,
        "source_test_validation_review_refs": [
            "test:test_v411_task_learning#exact-subject",
            "validation:owner-local",
        ],
        "confidence_layers": ["IDENTITY_BOUND", "BEHAVIOR_SUPPORTED"],
        "currentness_ref": SUBJECT_A,
        "disposition": "RETAIN_LOCAL",
    }


def valid_v1_record() -> dict:
    return {
        "schema_version": "ai-dev/task-learning-v1",
        "learning_id": "learning:T14:v1-control",
        "repository_ref": "github:kaicreator-mm/ai-development-standard",
        "work_item_ref": "github:kaicreator-mm/ai-development-standard#1017",
        "implementation_subject_ref": SUBJECT_A,
        "authority_refs": ["task-pack:v4.8.0/control"],
        "summary": "Historical v1 control record.",
        "source_test_validation_review_refs": ["test:test_v48_task_learning#positive"],
        "confidence_layers": ["IDENTITY_BOUND"],
        "currentness_ref": SUBJECT_A,
        "disposition": "RETAIN_LOCAL",
    }


def material_refs(record: dict) -> set[str]:
    refs = {
        record.get("repository_ref"),
        record.get("work_item_ref"),
        record.get("implementation_subject_ref"),
        record.get("currentness_ref"),
    }
    refs.update(record.get("authority_refs", []))
    refs.update(record.get("source_test_validation_review_refs", []))
    return {ref for ref in refs if isinstance(ref, str) and ref}


def assess_learning(
    record: dict,
    *,
    current_subject: str,
    resolvable_refs: set[str],
    provenance: str = "DURABLE_BOUNDARY_EXTERNAL",
    unsupported_inference: bool = False,
    requested_mutation: str | None = None,
) -> dict:
    schema_errors = validate_subset(record, SCHEMA_V2)
    if schema_errors:
        return {
            "decision": "REJECTED",
            "reason": "schema_invalid",
            "authority_side_effects": 0,
        }

    subject = record.get("implementation_subject_ref")
    currentness = record.get("currentness_ref")
    if subject != current_subject or currentness != current_subject:
        return {
            "decision": "HISTORICAL_ONLY",
            "reason": "stale_exact_subject",
            "authority_side_effects": 0,
        }

    unresolved = sorted(material_refs(record) - resolvable_refs)
    if unresolved:
        return {
            "decision": "BLOCKED",
            "reason": "unresolvable_source_ref",
            "unresolved_refs": unresolved,
            "authority_side_effects": 0,
        }

    if provenance == "PRIVATE_DELIBERATION_ONLY":
        return {
            "decision": "REJECTED_UNVERIFIABLE",
            "reason": "private_deliberation_is_not_evidence",
            "authority_side_effects": 0,
        }

    if unsupported_inference:
        return {
            "decision": "REJECTED_UNSUPPORTED_INFERENCE",
            "reason": "claim_exceeds_durable_sources",
            "epistemic": "UNSUPPORTED_INFERRED",
            "authority_side_effects": 0,
        }

    if requested_mutation in AUTHORITY_MUTATIONS:
        return {
            "decision": "BLOCKED_AUTHORITY_BOUNDARY",
            "reason": "task_learning_is_subordinate_evidence_only",
            "authority_side_effects": 0,
        }

    return {
        "decision": "CURRENT_BOUNDED_EVIDENCE",
        "reason": "source_bound_current",
        "epistemic": "FACTUAL_SOURCE_BOUND",
        "consumption_mode": "SUBORDINATE_EVIDENCE_ONLY",
        "authority_side_effects": 0,
    }


def none_material() -> dict:
    return {"task_learning": "NONE_MATERIAL", "record": None}


def automatic_numeric_promotion(*, count: int, score: float) -> bool:
    _ = (count, score)
    return False


def already_satisfied(*, exact_production_source: bool, current_executable_tests: bool, full_r11_equivalence: bool) -> bool:
    return exact_production_source and current_executable_tests and full_r11_equivalence


class OwnerBoundaryTests(unittest.TestCase):
    def test_exact_three_path_owner_write_set_and_clean_tree(self):
        self.assertEqual(git("merge-base", "--is-ancestor", BASE_SHA, "HEAD", check=False).returncode, 0)
        changed = set(git("diff", "--name-only", BASE_SHA, "HEAD").stdout.splitlines())
        self.assertEqual(
            changed,
            {
                "standards/EXECUTION_ARCHITECTURE_STANDARD.md",
                "references/TASK_LEARNING_V2_REFERENCE.md",
                "scripts/test_v411_task_learning.py",
            },
        )
        self.assertEqual(git("status", "--porcelain").stdout, "")

    def test_preexisting_execution_architecture_is_byte_identical(self):
        current = EA.read_text(encoding="utf-8")
        self.assertEqual(current.count(EA_HEADING), 1)
        prefix = current[: current.index(EA_HEADING)].rstrip()
        prior = git("show", f"{BASE_SHA}:standards/EXECUTION_ARCHITECTURE_STANDARD.md").stdout.rstrip()
        self.assertEqual(prefix, prior)

    def test_reference_change_is_append_only(self):
        current = REFERENCE.read_text(encoding="utf-8")
        self.assertEqual(current.count(REF_HEADING), 1)
        prefix = current[: current.index(REF_HEADING)].rstrip()
        prior = git("show", f"{BASE_SHA}:references/TASK_LEARNING_V2_REFERENCE.md").stdout.rstrip()
        self.assertEqual(prefix, prior)

    def test_owner_section_keeps_authority_and_schema_boundaries(self):
        text = EA.read_text(encoding="utf-8")
        section = text[text.index(EA_HEADING):]
        for phrase in (
            "creates no new schema fields",
            "historical evidence only",
            "UNSUPPORTED_INFERRED",
            "SUBORDINATE_EVIDENCE_ONLY",
            "ALREADY_SATISFIED",
            "T11 exclusively owns",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, section)


class P01FactualCurrentEvidenceTests(unittest.TestCase):
    def test_positive_factual_record_is_current_bounded_evidence(self):
        record = valid_v2_record()
        result = assess_learning(
            record,
            current_subject=SUBJECT_A,
            resolvable_refs=material_refs(record),
        )
        self.assertEqual(result["decision"], "CURRENT_BOUNDED_EVIDENCE")
        self.assertEqual(result["epistemic"], "FACTUAL_SOURCE_BOUND")
        self.assertEqual(result["consumption_mode"], "SUBORDINATE_EVIDENCE_ONLY")
        self.assertEqual(result["authority_side_effects"], 0)


class P02NoneMaterialTests(unittest.TestCase):
    def test_none_material_fast_path_has_no_empty_record(self):
        result = none_material()
        self.assertEqual(result["task_learning"], "NONE_MATERIAL")
        self.assertIsNone(result["record"])
        self.assertTrue(validate_subset({}, SCHEMA_V2))


class P03SubordinateConsumptionTests(unittest.TestCase):
    def test_later_work_consumes_evidence_without_mutating_authority(self):
        record = valid_v2_record()
        result = assess_learning(
            record,
            current_subject=SUBJECT_A,
            resolvable_refs=material_refs(record),
        )
        self.assertEqual(result["consumption_mode"], "SUBORDINATE_EVIDENCE_ONLY")
        self.assertEqual(result["authority_side_effects"], 0)

    def test_evolution_candidate_ref_never_approves_intake(self):
        record = valid_v2_record()
        record["friction_classification"] = "ADS_EVOLUTION_CANDIDATE"
        record["ads_evolution_candidate_ref"] = "evolution-intake:ADS-CAND-001"
        refs = material_refs(record) | {"evolution-intake:ADS-CAND-001"}
        result = assess_learning(
            record,
            current_subject=SUBJECT_A,
            resolvable_refs=refs,
            requested_mutation="EVOLUTION_APPROVE",
        )
        self.assertEqual(result["decision"], "BLOCKED_AUTHORITY_BOUNDARY")


class P04NegativeLearningTests(unittest.TestCase):
    def test_factual_negative_lesson_uses_same_acceptance_rules(self):
        record = valid_v2_record(negative=True)
        result = assess_learning(
            record,
            current_subject=SUBJECT_A,
            resolvable_refs=material_refs(record),
        )
        self.assertEqual(result["decision"], "CURRENT_BOUNDED_EVIDENCE")
        self.assertEqual(result["epistemic"], "FACTUAL_SOURCE_BOUND")


class P05CompatibilityTests(unittest.TestCase):
    def test_v1_and_v2_validate_only_under_their_explicit_versions(self):
        v1 = valid_v1_record()
        v2 = valid_v2_record()
        self.assertEqual(validate_subset(v1, SCHEMA_V1), [])
        self.assertEqual(validate_subset(v2, SCHEMA_V2), [])
        self.assertTrue(validate_subset(v1, SCHEMA_V2))
        self.assertTrue(validate_subset(v2, SCHEMA_V1))


class N01StaleSubjectTests(unittest.TestCase):
    def test_stale_record_demotes_to_historical_only_without_rebind(self):
        record = valid_v2_record()
        result = assess_learning(
            record,
            current_subject=SUBJECT_B,
            resolvable_refs=material_refs(record) | {SUBJECT_B},
        )
        self.assertEqual(result["decision"], "HISTORICAL_ONLY")
        self.assertEqual(result["authority_side_effects"], 0)


class N02PrivateDeliberationTests(unittest.TestCase):
    def test_private_deliberation_only_is_rejected_as_evidence(self):
        record = valid_v2_record()
        result = assess_learning(
            record,
            current_subject=SUBJECT_A,
            resolvable_refs=material_refs(record),
            provenance="PRIVATE_DELIBERATION_ONLY",
        )
        self.assertEqual(result["decision"], "REJECTED_UNVERIFIABLE")


class N03UnsupportedInferenceTests(unittest.TestCase):
    def test_unresolvable_reference_fails_closed(self):
        record = valid_v2_record()
        refs = material_refs(record)
        refs.remove("validation:owner-local")
        result = assess_learning(record, current_subject=SUBJECT_A, resolvable_refs=refs)
        self.assertEqual(result["decision"], "BLOCKED")
        self.assertIn("validation:owner-local", result["unresolved_refs"])

    def test_inference_beyond_cited_sources_is_not_factual(self):
        record = valid_v2_record()
        result = assess_learning(
            record,
            current_subject=SUBJECT_A,
            resolvable_refs=material_refs(record),
            unsupported_inference=True,
        )
        self.assertEqual(result["decision"], "REJECTED_UNSUPPORTED_INFERENCE")
        self.assertEqual(result["epistemic"], "UNSUPPORTED_INFERRED")


class N04AuthorityBoundaryTests(unittest.TestCase):
    def test_learning_record_cannot_mutate_product_l2_task_dag_or_ads(self):
        record = valid_v2_record()
        refs = material_refs(record)
        for mutation in sorted(AUTHORITY_MUTATIONS):
            with self.subTest(mutation=mutation):
                result = assess_learning(
                    record,
                    current_subject=SUBJECT_A,
                    resolvable_refs=refs,
                    requested_mutation=mutation,
                )
                self.assertEqual(result["decision"], "BLOCKED_AUTHORITY_BOUNDARY")
                self.assertEqual(result["authority_side_effects"], 0)


class N05NumericPromotionTests(unittest.TestCase):
    def test_no_count_or_score_auto_promotes_evidence_to_authority(self):
        for count, score in ((1, 1.0), (10, 0.99), (1000000, 100.0)):
            with self.subTest(count=count, score=score):
                self.assertFalse(automatic_numeric_promotion(count=count, score=score))


class N06AlreadySatisfiedTests(unittest.TestCase):
    def test_already_satisfied_requires_exact_source_current_tests_and_full_equivalence(self):
        self.assertTrue(
            already_satisfied(
                exact_production_source=True,
                current_executable_tests=True,
                full_r11_equivalence=True,
            )
        )
        cases = (
            (False, True, True),
            (True, False, True),
            (True, True, False),
            (False, False, False),
        )
        for exact_source, current_tests, full in cases:
            with self.subTest(exact_source=exact_source, current_tests=current_tests, full=full):
                self.assertFalse(
                    already_satisfied(
                        exact_production_source=exact_source,
                        current_executable_tests=current_tests,
                        full_r11_equivalence=full,
                    )
                )


if __name__ == "__main__":
    unittest.main()
