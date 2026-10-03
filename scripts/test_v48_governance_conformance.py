"""v4.8 T-010 — Task Learning / Evolution Governance conformance.

Focused deterministic oracle for the already-merged T-004 Task Learning closeout
semantics (`schemas/task-learning-v1.schema.json`,
`references/TASK_LEARNING_EVIDENCE_REFERENCE.md`) and T-005 ADS evolution
governance semantics (`standards/DEVELOPMENT_WORKFLOW.md` §8).

The evaluation helpers below model the owned boundaries so both valid and
invalid routes can be asserted; they are a non-authoritative conformance oracle,
not a second evolution lifecycle, promotion engine or standard-change authority.
Owner files are read as read-only inputs to prevent oracle/owner divergence.
"""

from __future__ import annotations

import copy
import hashlib
import itertools
import json
import re
import unittest
from pathlib import Path
from test_protocol_schemas import assert_supported_schema, load_schema, validate_subset


ROOT = Path(__file__).resolve().parents[1]

# --- read-only owner inputs --------------------------------------------------
TASK_LEARNING_SCHEMA = load_schema("task-learning-v1.schema.json")
TASK_LEARNING_REFERENCE = (ROOT / "references" / "TASK_LEARNING_EVIDENCE_REFERENCE.md").read_text(encoding="utf-8")
WORKFLOW_SECTION_8 = (ROOT / "standards" / "DEVELOPMENT_WORKFLOW.md").read_text(encoding="utf-8").split(
    "## 8. ADS Evolution Feedback / Intake", 1
)[1]

# --- canonical vocabulary (T-001/T-004/T-005 owners; no synonyms) ------------
NONE_MATERIAL = "TASK_LEARNING=NONE_MATERIAL"
CONFIDENCE_LAYERS = ("IDENTITY_BOUND", "BEHAVIOR_SUPPORTED", "INDEPENDENTLY_CHALLENGED")
PROJECT_DEFECT = "PROJECT_DEFECT"
AGENT_EXECUTION_DEFECT = "AGENT_EXECUTION_DEFECT"
ENVIRONMENT_OR_TOOL_DEFECT = "ENVIRONMENT_OR_TOOL_DEFECT"
PROJECT_SPECIFIC_REQUIREMENT = "PROJECT_SPECIFIC_REQUIREMENT"
STANDARD_FRICTION_CANDIDATE = "STANDARD_FRICTION_CANDIDATE"
ADS_EVOLUTION_CANDIDATE = "ADS_EVOLUTION_CANDIDATE"
CLASSIFICATIONS = (
    PROJECT_DEFECT,
    AGENT_EXECUTION_DEFECT,
    ENVIRONMENT_OR_TOOL_DEFECT,
    PROJECT_SPECIFIC_REQUIREMENT,
    STANDARD_FRICTION_CANDIDATE,
    ADS_EVOLUTION_CANDIDATE,
)
NON_PROMOTING_CLASSES = CLASSIFICATIONS[:4]
NO_CHANGE = "NO_CHANGE"
MORE_EVIDENCE = "MORE_EVIDENCE"
FRICTION_DISPOSITIONS = (NO_CHANGE, MORE_EVIDENCE)
OPEN_ADS_INTAKE = "OPEN_ADS_INTAKE"
PROJECT_PRIVATE = "PROJECT_PRIVATE"
RESTRICTED = "RESTRICTED"
PUBLISHABLE = "PUBLISHABLE"
PUBLICATION_CLASSES = (PROJECT_PRIVATE, RESTRICTED, PUBLISHABLE)
ORDINARY_GOVERNANCE_CHAIN = (
    OPEN_ADS_INTAKE,
    "Intake",
    "L1 Product Evidence",
    "PRD / Scope Freeze",
    "L2 Architecture Evidence / Freeze",
    "Task DAG / Task",
    "Implementation",
    "required Validation",
    "applicable fresh Review",
    "normal integration / release authority",
)
CLASSIFICATION_ROUTES = {
    PROJECT_DEFECT: ("ROUTE_PROJECT",),
    AGENT_EXECUTION_DEFECT: ("ROUTE_EXECUTION",),
    ENVIRONMENT_OR_TOOL_DEFECT: ("ROUTE_ENVIRONMENT",),
    PROJECT_SPECIFIC_REQUIREMENT: ("ROUTE_PROJECT_SPECIFIC",),
    STANDARD_FRICTION_CANDIDATE: FRICTION_DISPOSITIONS,
    ADS_EVOLUTION_CANDIDATE: (OPEN_ADS_INTAKE,),
}
OWNER_AUTHORITIES = (
    "Product",
    "Architecture/L2",
    "Task",
    "ADR",
    "Incident",
    "Intent",
    "Skill",
    "Review",
    "Validation",
    "merge",
    "release",
)

IMMUTABLE_GIT_SUBJECT_RE = re.compile(r"^git:[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+@[0-9a-f]{40}$")
SUBJECT_A = "git:kaicreator-mm/example@1111111111111111111111111111111111111111"
SUBJECT_B = "git:kaicreator-mm/example@2222222222222222222222222222222222222222"

# Sensitive payload categories from the reference/workflow owners; scenario
# fixtures mark them with these explicit category markers.
SENSITIVE_PAYLOAD_MARKERS = (
    "secret:",
    "credential:",
    "password:",
    "api_key:",
    "token:",
    "private_reasoning:",
    "chain_of_thought:",
    "hidden_evaluator:",
    "hidden_validation:",
)

# One fixture sample per sensitive category above; every publication text field
# must reject exactly these categories, so body and summary oracles share them.
SENSITIVE_PAYLOAD_SAMPLES = (
    "secret: SA-DO-NOT-LEAK",
    "credential: admin/hunter2",
    "password: hunter2",
    "api_key: sk-do-not-leak",
    "token: ghp_do_not_leak",
    "private_reasoning: my internal scratch reasoning",
    "chain_of_thought: step 1, then step 2",
    "hidden_evaluator: rubric scoring notes",
    "hidden_validation: hidden validation payload",
)

# Free-text fields the publication oracle evaluates; the public payload emits
# the summary verbatim (bounded), so a sensitive category in any of them fails
# closed, not only in the body.
PUBLICATION_TEXT_FIELDS = ("body", "summary")


def is_immutable_git_subject(value: object) -> bool:
    return isinstance(value, str) and IMMUTABLE_GIT_SUBJECT_RE.fullmatch(value) is not None


def valid_learning() -> dict:
    return {
        "schema_version": "ai-dev/task-learning-v1",
        "learning_id": "learning:T-010:001",
        "repository_ref": "github:kaicreator-mm/ai-development-standard",
        "work_item_ref": "github:kaicreator-mm/ai-development-standard#516",
        "implementation_subject_ref": SUBJECT_A,
        "authority_refs": [
            "task-pack:v4.8.0/T-010",
            "l2:f88c85454e80101a0fdf56050e21f11a05279841",
        ],
        "summary": "Exact-subject learning records reusable contract facts without changing authority.",
        "source_test_validation_review_refs": [
            "test:test_v48_governance_conformance#material-learning-current",
            "validation:pending-exact-head",
        ],
        "confidence_layers": ["IDENTITY_BOUND"],
        "currentness_ref": SUBJECT_A,
        "disposition": "RETAIN_LOCAL",
    }


# --- conformance oracle kernel (pure, non-authoritative) ---------------------


def learning_record_class(record: dict | None, current_subject_ref: str) -> str:
    """CURRENT_EVIDENCE requires schema validity and byte-equal canonical
    immutable triple identity; everything else stays HISTORICAL_ONLY. The
    NONE_MATERIAL fast path is represented by the absence of a record object."""
    if record is None:
        return "NONE_MATERIAL_FAST_PATH"
    if validate_subset(record, TASK_LEARNING_SCHEMA):
        return "HISTORICAL_ONLY"
    subject = record.get("implementation_subject_ref")
    currentness = record.get("currentness_ref")
    if not all(is_immutable_git_subject(value) for value in (subject, currentness, current_subject_ref)):
        return "HISTORICAL_ONLY"
    if not (subject == current_subject_ref == currentness):
        return "HISTORICAL_ONLY"
    return "CURRENT_EVIDENCE"


def is_current_evidence(record: dict | None, current_subject_ref: str) -> bool:
    return learning_record_class(record, current_subject_ref) == "CURRENT_EVIDENCE"


def implies_validation_pass(layers: list[str]) -> bool:
    """Evidence-strength layers never create current Validation PASS."""
    return False


def implies_review_pass(layers: list[str]) -> bool:
    """Evidence-strength layers never create current Review PASS."""
    return False


def authorizes_merge(record: dict) -> bool:
    """No Task Learning record authorizes a merge."""
    return False


def global_score(layers: list[str]) -> None:
    """Layers do not compose into a global scalar score; always refused."""
    return None


def route_dispositions(classification: str) -> tuple[str, ...]:
    if classification not in CLASSIFICATION_ROUTES:
        raise ValueError(f"unknown classification: {classification!r}")
    return CLASSIFICATION_ROUTES[classification]


def opens_ads_standard_change(classification: str) -> bool:
    """Only ADS_EVOLUTION_CANDIDATE may enter ordinary ADS governance, and only
    as an Intake entry — never as direct standard change."""
    return classification == ADS_EVOLUTION_CANDIDATE


def is_approval(disposition: str) -> bool:
    """No allowed disposition — including OPEN_ADS_INTAKE — is an approval."""
    return False


def attempt_automatic_promotion(classification: str, signal: dict) -> str:
    """§8.2: count/score/rate/cost/latency/provider/model/scheduler/heuristic
    signals are evidence only. The deterministic route never reclassifies from
    a signal and there is no numeric promotion threshold to consult."""
    return classification


def resolve_friction(classification: str, *, ambiguous: bool) -> str | None:
    """Ambiguous friction must route to MORE_EVIDENCE. Unambiguous friction
    still has no kernel-driven termination: NO_CHANGE remains an explicit
    owner decision, so the kernel returns None instead of promoting."""
    if classification != STANDARD_FRICTION_CANDIDATE:
        raise ValueError("resolve_friction applies to STANDARD_FRICTION_CANDIDATE only")
    if ambiguous:
        return MORE_EVIDENCE
    return None


def can_edit_normative_ads(evidence_source: object) -> bool:
    """Telemetry, model/provider output, scheduler/ranking output, Task
    Learning records, CI results and dogfood observations are evidence refs
    only; none may edit normative ADS files."""
    return False


def can_skip_governance_stage(evidence_source: object, stage: str) -> bool:
    """No evidence source may skip any stage of ordinary ADS governance."""
    return False


def effective_publication_class(publication_class: str | None) -> str:
    """§8.3 fail-closed default: absent an explicit class the evidence is
    treated as PROJECT_PRIVATE."""
    return publication_class if publication_class in PUBLICATION_CLASSES else PROJECT_PRIVATE


def is_sensitive_material(payload: str) -> bool:
    lowered = payload.lower()
    return any(marker in lowered for marker in SENSITIVE_PAYLOAD_MARKERS)


def can_publish_evidence(item: dict) -> bool:
    """Publication requires explicit PUBLISHABLE authority AND non-sensitive
    material in every publication text field; sensitive material is never
    publication material even when the surrounding observation is otherwise
    publishable."""
    if effective_publication_class(item.get("publication_class")) != PUBLISHABLE:
        return False
    return not any(
        is_sensitive_material(str(item.get(field, "")))
        for field in PUBLICATION_TEXT_FIELDS
    )


def minimize_for_publication(item: dict) -> dict:
    """Reference-first minimization: emit source ref, body digest and a bounded
    non-sensitive summary. Refuses anything not explicitly publishable and any
    sensitive payload category in any publication text field."""
    if not can_publish_evidence(item):
        raise ValueError("evidence is not publishable (fail-closed or sensitive material)")
    body = str(item.get("body", ""))
    return {
        "source_ref": item["source_ref"],
        "body_digest": hashlib.sha256(body.encode("utf-8")).hexdigest(),
        "summary": str(item["summary"])[:200],
    }


def claim_authority(evidence: object, owner: str) -> None:
    """Learning/governance evidence never substitutes for any owner authority."""
    return None


# --- conformance suite --------------------------------------------------------


class OwnerVocabularyTests(unittest.TestCase):
    """Guard oracle/owner divergence: the kernel vocabulary must equal the
    read-only owner artifacts exactly (no synonyms, no parallel lifecycle)."""

    def test_owner_files_carry_canonical_vocabulary(self) -> None:
        assert_supported_schema(TASK_LEARNING_SCHEMA)
        self.assertEqual(
            list(TASK_LEARNING_SCHEMA["properties"]["friction_classification"]["enum"]),
            list(CLASSIFICATIONS),
        )
        self.assertEqual(
            list(TASK_LEARNING_SCHEMA["properties"]["confidence_layers"]["items"]["enum"]),
            list(CONFIDENCE_LAYERS),
        )
        for token in (NONE_MATERIAL, "implementation_subject_ref == current_subject_ref == currentness_ref"):
            self.assertIn(token, TASK_LEARNING_REFERENCE)
        for token in CLASSIFICATIONS:
            self.assertIn(f"`{token}`", WORKFLOW_SECTION_8)
        for token in PUBLICATION_CLASSES:
            self.assertIn(token, WORKFLOW_SECTION_8)
        self.assertIn("There is no universal numeric promotion threshold.", WORKFLOW_SECTION_8)
        self.assertIn("Secrets, credentials, private chain-of-thought and hidden-evaluator/Hidden Validation payloads are never publication material.", WORKFLOW_SECTION_8)

    def test_kernel_defines_no_route_or_lifecycle_beyond_owners(self) -> None:
        self.assertEqual(
            sorted(set(CLASSIFICATION_ROUTES)),
            sorted(CLASSIFICATIONS),
        )
        self.assertEqual(
            sorted(value for routes in CLASSIFICATION_ROUTES.values() for value in routes),
            sorted(
                {
                    "ROUTE_PROJECT",
                    "ROUTE_EXECUTION",
                    "ROUTE_ENVIRONMENT",
                    "ROUTE_PROJECT_SPECIFIC",
                    NO_CHANGE,
                    MORE_EVIDENCE,
                    OPEN_ADS_INTAKE,
                }
            ),
        )
        self.assertEqual(ORDINARY_GOVERNANCE_CHAIN[0], OPEN_ADS_INTAKE)
        self.assertIn("`OPEN_ADS_INTAKE`", WORKFLOW_SECTION_8)
        self.assertIn("Intake -> L1 -> PRD -> L2 -> Task -> Review/Validation", WORKFLOW_SECTION_8)


class LearningCloseoutTests(unittest.TestCase):
    def test_none_material_fast_path(self) -> None:
        self.assertEqual(learning_record_class(None, SUBJECT_A), "NONE_MATERIAL_FAST_PATH")
        self.assertTrue(validate_subset({}, TASK_LEARNING_SCHEMA))

    def test_material_learning_current(self) -> None:
        record = valid_learning()
        self.assertEqual(validate_subset(record, TASK_LEARNING_SCHEMA), [])
        self.assertEqual(learning_record_class(record, SUBJECT_A), "CURRENT_EVIDENCE")
        self.assertTrue(is_current_evidence(record, SUBJECT_A))

    def test_stale_learning_historical_only(self) -> None:
        record = valid_learning()
        self.assertFalse(is_current_evidence(record, SUBJECT_B))
        rebound = copy.deepcopy(record)
        rebound["currentness_ref"] = SUBJECT_B
        self.assertFalse(is_current_evidence(rebound, SUBJECT_B))
        self.assertFalse(is_current_evidence(rebound, SUBJECT_A))

    def test_missing_or_mutable_subject_historical_only(self) -> None:
        mutable_refs = (
            "git:kaicreator-mm/example@main",
            "git:kaicreator-mm/example@refs/heads/main",
            "git:kaicreator-mm/example@v4.8.0",
            "github:kaicreator-mm/example",
            "kaicreator-mm/example",
            "git:kaicreator-mm/example@1111111",
            "git:kaicreator-mm/example@111111111111111111111111111111111111111G",
        )
        for field in ("implementation_subject_ref", "currentness_ref"):
            missing = valid_learning()
            del missing[field]
            self.assertEqual(validate_subset(missing, TASK_LEARNING_SCHEMA), [])
            self.assertFalse(is_current_evidence(missing, SUBJECT_A))
            for ref in mutable_refs:
                with self.subTest(field=field, ref=ref):
                    mutable = valid_learning()
                    mutable[field] = ref
                    self.assertFalse(is_current_evidence(mutable, ref))
        equal_mutable = valid_learning()
        equal_mutable["implementation_subject_ref"] = "git:kaicreator-mm/example@main"
        equal_mutable["currentness_ref"] = "git:kaicreator-mm/example@main"
        self.assertFalse(is_current_evidence(equal_mutable, "git:kaicreator-mm/example@main"))

    def test_confidence_not_current_pass(self) -> None:
        for size in range(len(CONFIDENCE_LAYERS) + 1):
            for layers in itertools.combinations(CONFIDENCE_LAYERS, size):
                with self.subTest(layers=layers):
                    self.assertFalse(implies_validation_pass(list(layers)))
                    self.assertFalse(implies_review_pass(list(layers)))
                    self.assertIsNone(global_score(list(layers)))
        strong = valid_learning()
        strong["confidence_layers"] = list(CONFIDENCE_LAYERS)
        self.assertFalse(implies_validation_pass(strong["confidence_layers"]))
        self.assertFalse(authorizes_merge(strong))

    def test_confidence_layers_are_schema_bounded(self) -> None:
        value = valid_learning()
        value["confidence_layers"] = ["GLOBAL_TRUTH"]
        self.assertTrue(validate_subset(value, TASK_LEARNING_SCHEMA))


class LearningGovernanceBoundaryTests(unittest.TestCase):
    def test_learning_routing_not_authority(self) -> None:
        record = valid_learning()
        record["friction_classification"] = ADS_EVOLUTION_CANDIDATE
        record["disposition"] = OPEN_ADS_INTAKE
        self.assertEqual(validate_subset(record, TASK_LEARNING_SCHEMA), [])
        self.assertFalse(can_edit_normative_ads(record))
        self.assertFalse(authorizes_merge(record))
        for stage in ORDINARY_GOVERNANCE_CHAIN:
            self.assertFalse(can_skip_governance_stage(record, stage))
        self.assertFalse(is_approval(record["disposition"]))

    def test_classification_vocabulary_is_schema_frozen(self) -> None:
        value = valid_learning()
        value["friction_classification"] = "AUTO_STANDARD_CHANGE"
        self.assertTrue(validate_subset(value, TASK_LEARNING_SCHEMA))


class ClassificationRoutingTests(unittest.TestCase):
    def test_first_four_classifications_do_not_promote(self) -> None:
        for classification in NON_PROMOTING_CLASSES:
            with self.subTest(classification=classification):
                self.assertFalse(opens_ads_standard_change(classification))
                self.assertNotIn(OPEN_ADS_INTAKE, route_dispositions(classification))
                self.assertEqual(route_dispositions(classification), CLASSIFICATION_ROUTES[classification])

    def test_project_defect_no_promotion(self) -> None:
        self.assertEqual(route_dispositions(PROJECT_DEFECT), ("ROUTE_PROJECT",))
        self.assertFalse(opens_ads_standard_change(PROJECT_DEFECT))

    def test_agent_execution_defect_no_promotion(self) -> None:
        self.assertEqual(route_dispositions(AGENT_EXECUTION_DEFECT), ("ROUTE_EXECUTION",))
        self.assertFalse(opens_ads_standard_change(AGENT_EXECUTION_DEFECT))

    def test_environment_tool_defect_no_promotion(self) -> None:
        self.assertEqual(route_dispositions(ENVIRONMENT_OR_TOOL_DEFECT), ("ROUTE_ENVIRONMENT",))
        self.assertFalse(opens_ads_standard_change(ENVIRONMENT_OR_TOOL_DEFECT))

    def test_project_specific_no_promotion(self) -> None:
        self.assertEqual(route_dispositions(PROJECT_SPECIFIC_REQUIREMENT), ("ROUTE_PROJECT_SPECIFIC",))
        self.assertFalse(opens_ads_standard_change(PROJECT_SPECIFIC_REQUIREMENT))

    def test_friction_no_change(self) -> None:
        self.assertIn(NO_CHANGE, route_dispositions(STANDARD_FRICTION_CANDIDATE))
        self.assertFalse(opens_ads_standard_change(STANDARD_FRICTION_CANDIDATE))
        self.assertNotIn(OPEN_ADS_INTAKE, route_dispositions(STANDARD_FRICTION_CANDIDATE))

    def test_friction_more_evidence(self) -> None:
        self.assertEqual(resolve_friction(STANDARD_FRICTION_CANDIDATE, ambiguous=True), MORE_EVIDENCE)
        self.assertNotIn(MORE_EVIDENCE, (OPEN_ADS_INTAKE, ADS_EVOLUTION_CANDIDATE))
        self.assertFalse(opens_ads_standard_change(STANDARD_FRICTION_CANDIDATE))

    def test_unambiguous_friction_still_requires_explicit_owner_decision(self) -> None:
        self.assertIsNone(resolve_friction(STANDARD_FRICTION_CANDIDATE, ambiguous=False))
        self.assertEqual(route_dispositions(STANDARD_FRICTION_CANDIDATE), FRICTION_DISPOSITIONS)

    def test_numeric_or_provider_auto_promotion_rejected(self) -> None:
        signals = (
            {"signal": "occurrence_count", "value": 10_000},
            {"signal": "success_rate", "value": 0.999},
            {"signal": "failure_rate", "value": 0.999},
            {"signal": "cost_value", "value": 999_999},
            {"signal": "latency_value", "value": 999_999},
            {"signal": "provider_label", "value": "provider-x"},
            {"signal": "model_label", "value": "model-y"},
            {"signal": "scheduler_ranking", "value": 1},
            {"signal": "heuristic_score", "value": 100},
        )
        for signal in signals:
            with self.subTest(signal=signal["signal"]):
                promoted = attempt_automatic_promotion(STANDARD_FRICTION_CANDIDATE, signal)
                self.assertEqual(promoted, STANDARD_FRICTION_CANDIDATE)
                self.assertFalse(opens_ads_standard_change(promoted))
                self.assertEqual(route_dispositions(promoted), FRICTION_DISPOSITIONS)


class EvolutionPromotionBoundaryTests(unittest.TestCase):
    def test_ads_evolution_intake_only(self) -> None:
        self.assertEqual(route_dispositions(ADS_EVOLUTION_CANDIDATE), (OPEN_ADS_INTAKE,))
        self.assertFalse(is_approval(OPEN_ADS_INTAKE))
        for disposition in route_dispositions(ADS_EVOLUTION_CANDIDATE):
            self.assertFalse(is_approval(disposition))

    def test_ordinary_governance_no_shortcut(self) -> None:
        evidence_sources = (
            "telemetry_ref",
            "model_provider_output",
            "scheduler_ranking_output",
            "task_learning_record",
            "ci_result",
            "dogfood_observation",
        )
        for source in evidence_sources:
            self.assertFalse(can_edit_normative_ads(source))
            for stage in ORDINARY_GOVERNANCE_CHAIN:
                with self.subTest(source=source, stage=stage):
                    self.assertFalse(can_skip_governance_stage(source, stage))


class PublicationPrivacyTests(unittest.TestCase):
    def publishable_item(self) -> dict:
        return {
            "publication_class": PUBLISHABLE,
            "source_ref": "github:kaicreator-mm/ai-development-standard#516",
            "summary": "Friction observation reduced to a non-sensitive engineering fact.",
            "body": "Plain observation text with no sensitive category markers.",
        }

    def test_publication_fail_closed(self) -> None:
        missing = self.publishable_item()
        del missing["publication_class"]
        self.assertEqual(effective_publication_class(None), PROJECT_PRIVATE)
        self.assertFalse(can_publish_evidence(missing))
        for publication_class in (PROJECT_PRIVATE, RESTRICTED):
            with self.subTest(publication_class=publication_class):
                item = self.publishable_item()
                item["publication_class"] = publication_class
                self.assertFalse(can_publish_evidence(item))
                with self.assertRaises(ValueError):
                    minimize_for_publication(item)

    def test_publication_independent_of_strength(self) -> None:
        item = self.publishable_item()
        item["friction_classification"] = STANDARD_FRICTION_CANDIDATE
        item["confidence_layers"] = ["BEHAVIOR_SUPPORTED"]
        for publication_class in PUBLICATION_CLASSES:
            with self.subTest(publication_class=publication_class):
                item["publication_class"] = publication_class
                self.assertEqual(
                    route_dispositions(item["friction_classification"]), FRICTION_DISPOSITIONS
                )
                self.assertFalse(opens_ads_standard_change(item["friction_classification"]))
        self.assertFalse(implies_validation_pass(item["confidence_layers"]))

    def test_sensitive_material_never_publishable(self) -> None:
        for body in SENSITIVE_PAYLOAD_SAMPLES:
            with self.subTest(body=body):
                item = self.publishable_item()
                item["body"] = body
                self.assertTrue(is_sensitive_material(body))
                self.assertFalse(can_publish_evidence(item))
                with self.assertRaises(ValueError):
                    minimize_for_publication(item)

    def test_sensitive_material_in_summary_never_publishable(self) -> None:
        for summary in SENSITIVE_PAYLOAD_SAMPLES:
            with self.subTest(summary=summary):
                item = self.publishable_item()
                item["summary"] = summary
                self.assertTrue(is_sensitive_material(summary))
                self.assertFalse(can_publish_evidence(item))
                with self.assertRaises(ValueError):
                    minimize_for_publication(item)

    def test_reference_first_minimization(self) -> None:
        item = self.publishable_item()
        minimized = minimize_for_publication(item)
        self.assertEqual(set(minimized), {"source_ref", "body_digest", "summary"})
        self.assertNotIn(item["body"], json.dumps(minimized))
        self.assertFalse(is_sensitive_material(minimized["summary"]))
        self.assertEqual(
            minimized["body_digest"], hashlib.sha256(item["body"].encode("utf-8")).hexdigest()
        )
        self.assertLessEqual(len(minimized["summary"]), 200)


class OwnerPreservationTests(unittest.TestCase):
    def strongest_record(self) -> dict:
        record = valid_learning()
        record["confidence_layers"] = list(CONFIDENCE_LAYERS)
        record["friction_classification"] = ADS_EVOLUTION_CANDIDATE
        record["disposition"] = OPEN_ADS_INTAKE
        return record

    def test_owner_preservation(self) -> None:
        record = self.strongest_record()
        for owner in OWNER_AUTHORITIES:
            with self.subTest(owner=owner):
                self.assertIsNone(claim_authority(record, owner))
        self.assertFalse(authorizes_merge(record))
        self.assertFalse(implies_review_pass(record["confidence_layers"]))
        self.assertFalse(implies_validation_pass(record["confidence_layers"]))

    def test_authority_substitution_fields_are_rejected_by_schema(self) -> None:
        for field in (
            "product_authority",
            "architecture_authority",
            "task_state",
            "adr_authority",
            "incident_authority",
            "review_result",
            "validation_result",
            "merge_authorization",
            "release_authorization",
        ):
            with self.subTest(field=field):
                value = self.strongest_record()
                value[field] = "APPROVED"
                self.assertTrue(validate_subset(value, TASK_LEARNING_SCHEMA))

    def test_no_new_evolution_lifecycle(self) -> None:
        record = self.strongest_record()
        self.assertFalse(can_edit_normative_ads(record))
        self.assertFalse(opens_ads_standard_change(STANDARD_FRICTION_CANDIDATE))
        promoted = attempt_automatic_promotion(
            STANDARD_FRICTION_CANDIDATE, {"signal": "heuristic_score", "value": 100}
        )
        self.assertEqual(promoted, STANDARD_FRICTION_CANDIDATE)
        self.assertEqual(sorted(set(CLASSIFICATION_ROUTES)), sorted(CLASSIFICATIONS))


if __name__ == "__main__":
    unittest.main()
