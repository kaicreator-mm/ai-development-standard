from __future__ import annotations

import json
from pathlib import Path
import subprocess
import unittest

from test_protocol_schemas import assert_supported_schema, load_schema, validate_subset


ROOT = Path(__file__).resolve().parents[1]
V1_PATH = ROOT / "schemas" / "task-learning-v1.schema.json"
V2_PATH = ROOT / "schemas" / "task-learning-v2.schema.json"
COMPAT_SCHEMA_PATH = ROOT / "schemas" / "compatibility-record-v1.schema.json"
COMPAT_PATH = ROOT / "references" / "TASK_LEARNING_V2_COMPATIBILITY.json"
REFERENCE_PATH = ROOT / "references" / "TASK_LEARNING_V2_REFERENCE.md"
V1_OWNER_REFERENCE_PATH = ROOT / "references" / "TASK_LEARNING_EVIDENCE_REFERENCE.md"

BASE_SHA = "df94641e6082dc7a2988e73eafdffd3bf42668b9"
EXPECTED_V1_BLOB = "f4df5ecb531cd577e8a38cd2a9887f73777ee53f"
EXPECTED_V1_OWNER_REFERENCE_BLOB = "205ad5af363816cb1a8d1e2dba07947898be5da0"

SCHEMA_V1 = load_schema("task-learning-v1.schema.json")
SCHEMA_V2 = load_schema("task-learning-v2.schema.json")

SUBJECT_A = "git:kaicreator-mm/example@1111111111111111111111111111111111111111"

V1_FIELD_NAMES = frozenset(SCHEMA_V1["properties"])
V2_IDENTITY_FIELDS = frozenset({"owner_family", "predecessor_protocol_version"})
V2_NEW_FIELDS = frozenset(
    {
        "execution_friction_class",
        "recurrence_refs",
        "root_cause_relation",
        "prevention_point_refs",
        "recurrence_audit_ref",
        "ads_evolution_candidate_ref",
    }
)

PRD_EXECUTION_FRICTION_CLASSES = (
    "workflow_waste",
    "missing_contract",
    "execution_ambiguity",
    "repeated_failure_mode",
    "useful_pattern",
    "bad_pattern",
)


def git_blob_sha(path: Path, rev: str = "HEAD") -> str:
    # Identity must come from the committed Git object, not working-tree bytes:
    # checkout EOL/filter transforms (e.g. core.autocrlf=true) change disk bytes
    # and would break blob-identity assertions spuriously.
    spec = f"{rev}:{path.relative_to(ROOT).as_posix()}"
    result = subprocess.run(
        ["git", "rev-parse", spec],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def valid_v2_record() -> dict:
    return {
        "schema_version": "ai-dev/task-learning-v2",
        "owner_family": "task-learning",
        "predecessor_protocol_version": "ai-dev/task-learning-v1",
        "learning_id": "learning:T-006:001",
        "repository_ref": "github:kaicreator-mm/ai-development-standard",
        "work_item_ref": "github:kaicreator-mm/ai-development-standard#725",
        "implementation_subject_ref": SUBJECT_A,
        "authority_refs": ["task-pack:v4.9.0/T-006"],
        "summary": "Repeated missing-contract friction traced to one prevention point.",
        "source_test_validation_review_refs": ["test:test_v49_task_learning_v2#positive"],
        "confidence_layers": ["IDENTITY_BOUND"],
        "friction_classification": "ADS_EVOLUTION_CANDIDATE",
        "execution_friction_class": "missing_contract",
        "recurrence_refs": ["learning:T-001:001"],
        "root_cause_relation": "SAME",
        "recurrence_audit_ref": "audit:v4.9.0/recurrence-t006",
        "prevention_point_refs": ["task-pack:v4.9.0/T-006"],
        "ads_evolution_candidate_ref": "evolution-intake:ADS-CAND-001",
        "disposition": "MORE_EVIDENCE",
    }


def minimal_v2_record() -> dict:
    """v2 successor instance using only required fields (all v4.9 fields optional)."""
    return {
        "schema_version": "ai-dev/task-learning-v2",
        "owner_family": "task-learning",
        "predecessor_protocol_version": "ai-dev/task-learning-v1",
        "learning_id": "learning:T-006:002",
        "repository_ref": "github:kaicreator-mm/ai-development-standard",
        "work_item_ref": "github:kaicreator-mm/ai-development-standard#725",
        "authority_refs": ["task-pack:v4.9.0/T-006"],
        "summary": "Compact reusable learning without v4.9 recurrence fields.",
        "source_test_validation_review_refs": ["test:test_v49_task_learning_v2#minimal"],
        "confidence_layers": ["IDENTITY_BOUND"],
        "disposition": "RETAIN_LOCAL",
    }


def v1_fixture() -> dict:
    """Unchanged v4.8-shaped record: v1 fields only, no v2 identity/extension fields."""
    return {
        "schema_version": "ai-dev/task-learning-v1",
        "learning_id": "learning:T-001:001",
        "repository_ref": "github:kaicreator-mm/ai-development-standard",
        "work_item_ref": "github:kaicreator-mm/ai-development-standard#507",
        "implementation_subject_ref": SUBJECT_A,
        "authority_refs": ["task-pack:v4.8.0/T-001"],
        "summary": "Exact-subject learning remains historical after code drift.",
        "source_test_validation_review_refs": ["test:test_v48_task_learning#positive"],
        "confidence_layers": ["IDENTITY_BOUND"],
        "currentness_ref": SUBJECT_A,
        "disposition": "RETAIN_LOCAL",
    }


def audit_relation_established(record: dict, resolvable: frozenset[str]):
    """Consumer-side resolve-or-fail-closed rule for root_cause_relation.

    Returns the declared relation only when the audit ref and every recurrence
    ref resolve; otherwise returns None. A stale/missing reference never
    defaults to UNKNOWN or any other value — it fails closed.
    """
    relation = record.get("root_cause_relation")
    audit = record.get("recurrence_audit_ref")
    refs = record.get("recurrence_refs")
    if not isinstance(relation, str) or not isinstance(audit, str) or not isinstance(refs, list):
        return None
    if audit not in resolvable:
        return None
    if not refs or any(ref not in resolvable for ref in refs):
        return None
    return relation


class TaskLearningV2SameFamilySuccessorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.reference = REFERENCE_PATH.read_text(encoding="utf-8")
        cls.compat = json.loads(COMPAT_PATH.read_text(encoding="utf-8"))

    # L01 — successor validates; v1 fixtures stay v1-valid and un-reinterpreted.

    def test_v2_schema_uses_repository_supported_subset(self) -> None:
        assert_supported_schema(SCHEMA_V2)

    def test_v2_validates_successor_instances(self) -> None:
        self.assertEqual(validate_subset(valid_v2_record(), SCHEMA_V2), [])
        self.assertEqual(validate_subset(minimal_v2_record(), SCHEMA_V2), [])

    def test_v1_owner_surface_unmutated_at_candidate(self) -> None:
        self.assertEqual(git_blob_sha(V1_PATH), EXPECTED_V1_BLOB)
        self.assertEqual(git_blob_sha(V1_PATH, rev=BASE_SHA), EXPECTED_V1_BLOB)
        self.assertEqual(git_blob_sha(V1_OWNER_REFERENCE_PATH), EXPECTED_V1_OWNER_REFERENCE_BLOB)
        self.assertEqual(git_blob_sha(V1_OWNER_REFERENCE_PATH, rev=BASE_SHA), EXPECTED_V1_OWNER_REFERENCE_BLOB)

    def test_v1_fixture_remains_v1_valid(self) -> None:
        self.assertEqual(validate_subset(v1_fixture(), SCHEMA_V1), [])
        self.assertEqual(
            set(SCHEMA_V1["properties"]),
            V1_FIELD_NAMES,
            "v1 property inventory must be unchanged",
        )

    def test_v2_rejects_unknown_fields(self) -> None:
        for field in ("learning_db_ref", "intake_state", "workflow_state", "chain_of_thought"):
            with self.subTest(field=field):
                value = valid_v2_record()
                value[field] = "x"
                self.assertTrue(validate_subset(value, SCHEMA_V2))

    def test_none_material_fast_path_does_not_use_empty_record(self) -> None:
        self.assertTrue(validate_subset({}, SCHEMA_V2))
        self.assertIn("TASK_LEARNING=NONE_MATERIAL", self.reference)

    # L02 — execution_friction_class optional and orthogonal to friction_classification.

    def test_execution_friction_class_is_optional(self) -> None:
        self.assertNotIn("execution_friction_class", set(minimal_v2_record()))
        self.assertEqual(validate_subset(minimal_v2_record(), SCHEMA_V2), [])

    def test_execution_friction_class_vocabulary_is_prd_scoped(self) -> None:
        self.assertEqual(
            SCHEMA_V2["properties"]["execution_friction_class"]["enum"],
            list(PRD_EXECUTION_FRICTION_CLASSES),
        )
        for category in PRD_EXECUTION_FRICTION_CLASSES:
            with self.subTest(category=category):
                value = minimal_v2_record()
                value["execution_friction_class"] = category
                self.assertEqual(validate_subset(value, SCHEMA_V2), [])
        value = minimal_v2_record()
        value["execution_friction_class"] = "ADS_EVOLUTION_CANDIDATE"
        self.assertTrue(validate_subset(value, SCHEMA_V2))

    def test_execution_friction_class_is_orthogonal_to_friction_classification(self) -> None:
        v1_enum = set(SCHEMA_V1["properties"]["friction_classification"]["enum"])
        self.assertEqual(
            SCHEMA_V2["properties"]["friction_classification"]["enum"],
            SCHEMA_V1["properties"]["friction_classification"]["enum"],
            "friction_classification vocabulary must stay frozen byte-for-byte",
        )
        v2_friction_enum = set(SCHEMA_V2["properties"]["execution_friction_class"]["enum"])
        self.assertEqual(
            v1_enum & v2_friction_enum,
            set(),
            "no overlap claim: the vocabularies must be disjoint",
        )
        value = minimal_v2_record()
        value["friction_classification"] = "STANDARD_FRICTION_CANDIDATE"
        value["execution_friction_class"] = "workflow_waste"
        self.assertEqual(
            validate_subset(value, SCHEMA_V2),
            [],
            "the orthogonal fields MAY co-occur",
        )
        self.assertIn(
            "neither redefines, maps onto, nor overlaps",
            self.reference,
        )

    # L03 — refs resolve-or-fail-closed; stale/missing refs never become defaults.

    def test_reference_fields_reject_empty_refs(self) -> None:
        value = valid_v2_record()
        value["recurrence_refs"] = [""]
        self.assertTrue(validate_subset(value, SCHEMA_V2))
        value = valid_v2_record()
        value["prevention_point_refs"] = [""]
        self.assertTrue(validate_subset(value, SCHEMA_V2))
        value = valid_v2_record()
        value["recurrence_audit_ref"] = ""
        self.assertTrue(validate_subset(value, SCHEMA_V2))

    def test_root_cause_relation_requires_audit_and_recurrence_evidence(self) -> None:
        orphan = minimal_v2_record()
        orphan["root_cause_relation"] = "SAME"
        self.assertTrue(validate_subset(orphan, SCHEMA_V2))
        audit_only = minimal_v2_record()
        audit_only["root_cause_relation"] = "SAME"
        audit_only["recurrence_audit_ref"] = "audit:v4.9.0/r1"
        self.assertTrue(validate_subset(audit_only, SCHEMA_V2))
        refs_only = minimal_v2_record()
        refs_only["root_cause_relation"] = "SAME"
        refs_only["recurrence_refs"] = ["learning:T-001:001"]
        self.assertTrue(validate_subset(refs_only, SCHEMA_V2))
        grounded = minimal_v2_record()
        grounded["root_cause_relation"] = "SAME"
        grounded["recurrence_audit_ref"] = "audit:v4.9.0/r1"
        grounded["recurrence_refs"] = ["learning:T-001:001"]
        self.assertEqual(validate_subset(grounded, SCHEMA_V2), [])

    def test_relations_resolve_or_fail_closed_without_defaults(self) -> None:
        resolvable = frozenset({"learning:T-001:001", "audit:v4.9.0/recurrence-t006"})
        record = valid_v2_record()
        self.assertEqual(audit_relation_established(record, resolvable), "SAME")
        self.assertIsNone(audit_relation_established(record, frozenset(resolvable - {"audit:v4.9.0/recurrence-t006"})))
        self.assertIsNone(audit_relation_established(record, frozenset(resolvable - {"learning:T-001:001"})))
        stale = valid_v2_record()
        stale["recurrence_refs"] = ["learning:retired:999"]
        self.assertIsNone(audit_relation_established(stale, resolvable))
        missing = minimal_v2_record()
        self.assertIsNone(audit_relation_established(missing, resolvable))
        self.assertIn(
            "A stale or missing reference never becomes a default",
            self.reference,
        )

    # L04 — no authority, no automatic ADS mutation, no gate replacement.

    def test_learning_evidence_cannot_become_authority(self) -> None:
        for field in (
            "product_authority",
            "review_result",
            "validation_result",
            "release_decision",
            "task_state",
            "evolution_intake_decision",
            "promotion_decision",
        ):
            with self.subTest(field=field):
                value = valid_v2_record()
                value[field] = "PASS"
                self.assertTrue(validate_subset(value, SCHEMA_V2))

    def test_no_automatic_ads_mutation_fields(self) -> None:
        for field in ("ads_mutation", "auto_promote", "auto_file_intake", "gate_bypass"):
            with self.subTest(field=field):
                value = valid_v2_record()
                value[field] = True
                self.assertTrue(validate_subset(value, SCHEMA_V2))
        description = SCHEMA_V2["properties"]["ads_evolution_candidate_ref"]["description"]
        self.assertIn("existing", description)
        self.assertIn("Does not create, approve or auto-promote", description)

    def test_ads_evolution_link_stays_on_existing_vocabulary(self) -> None:
        unclassified = minimal_v2_record()
        unclassified["ads_evolution_candidate_ref"] = "evolution-intake:ADS-CAND-001"
        self.assertTrue(validate_subset(unclassified, SCHEMA_V2))
        mismatched = minimal_v2_record()
        mismatched["ads_evolution_candidate_ref"] = "evolution-intake:ADS-CAND-001"
        mismatched["friction_classification"] = "PROJECT_DEFECT"
        self.assertTrue(validate_subset(mismatched, SCHEMA_V2))
        linked = minimal_v2_record()
        linked["ads_evolution_candidate_ref"] = "evolution-intake:ADS-CAND-001"
        linked["friction_classification"] = "ADS_EVOLUTION_CANDIDATE"
        self.assertEqual(validate_subset(linked, SCHEMA_V2), [])

    def test_reference_doc_states_authority_boundaries(self) -> None:
        for needle in (
            "evidence refs only",
            "MUST NOT edit normative ADS files",
            "never Gate PASS",
            "`UNKNOWN` (and `DIFFERENT`) never self-promote standard change",
            "cannot become authority by accumulation",
        ):
            self.assertIn(needle, self.reference)

    # L05 — no learning DB, no new intake lifecycle, no workflow state.

    def test_field_inventory_is_bounded(self) -> None:
        expected = V1_FIELD_NAMES | V2_IDENTITY_FIELDS | V2_NEW_FIELDS
        self.assertEqual(set(SCHEMA_V2["properties"]), expected)

    def test_reference_doc_states_non_goals(self) -> None:
        for needle in (
            "a learning database",
            "a new intake lifecycle",
            "workflow state",
            "automatic ADS mutation",
        ):
            with self.subTest(needle=needle):
                self.assertIn(needle, self.reference)

    # L06 — compatibility record machine-checkable and truthful.

    def test_compatibility_record_is_machine_checkable(self) -> None:
        compat_schema = json.loads(COMPAT_SCHEMA_PATH.read_text(encoding="utf-8"))
        self.assertEqual(validate_subset(self.compat, compat_schema), [])
        self.assertEqual(self.compat["record_id"], "v49-t006-task-learning-v2")
        self.assertEqual(self.compat["contract"]["identity"], "task-learning")
        self.assertEqual(self.compat["baseline"]["version_ref"], "ai-dev/task-learning-v1")
        self.assertEqual(self.compat["baseline"]["sha_or_digest"], f"git-blob:{git_blob_sha(V1_PATH)}")
        self.assertEqual(
            self.compat["baseline"]["sha_or_digest"],
            f"git-blob:{EXPECTED_V1_BLOB}",
        )
        self.assertEqual(self.compat["candidate"]["version_ref"], "ai-dev/task-learning-v2")
        self.assertEqual(self.compat["candidate"]["sha_or_digest"], f"git-blob:{git_blob_sha(V2_PATH)}")

    def test_compatibility_dimensions_are_truthful(self) -> None:
        dimensions = {item["name"]: item for item in self.compat["dimensions"]}
        expected_outcomes = {
            "owner-family-semantics": "COMPATIBLE",
            "historical-v1-record-validity": "COMPATIBLE",
            "v1-core-field-semantics": "COMPATIBLE",
            "friction-classification-vocabulary": "COMPATIBLE",
            "execution-friction-class-orthogonality": "COMPATIBLE",
            "v1-parser-accepts-v2-instance": "INCOMPATIBLE",
            "v2-parser-accepts-v1-instance": "INCOMPATIBLE",
            "authority-and-gate-boundaries": "COMPATIBLE",
            "version-aware-adoption": "CONDITIONALLY_COMPATIBLE",
        }
        self.assertEqual(set(dimensions), set(expected_outcomes))
        for name, outcome in expected_outcomes.items():
            self.assertEqual(dimensions[name]["outcome"], outcome, name)
        for name, item in dimensions.items():
            with self.subTest(dimension=name):
                self.assertTrue(item["evidence_refs"], name)
                for ref in item["evidence_refs"]:
                    file_part = ref.split("#", 1)[0]
                    self.assertTrue((ROOT / file_part).exists(), ref)
        self.assertNotIn("UNKNOWN", {item["outcome"] for item in self.compat["dimensions"]})

    def test_incompatible_claims_fail_closed_executable(self) -> None:
        self.assertTrue(
            validate_subset(valid_v2_record(), SCHEMA_V1),
            "v1 schema must reject a v2 instance (declared INCOMPATIBLE)",
        )
        self.assertTrue(
            validate_subset(v1_fixture(), SCHEMA_V2),
            "v2 schema must fail closed on a v1 instance (declared INCOMPATIBLE)",
        )
        self.assertIn("a v1-only parser is not assumed to accept a v2 instance", self.reference)
        self.assertIn("no silent reinterpretation", self.reference)


if __name__ == "__main__":
    unittest.main()
