from __future__ import annotations

import json
from pathlib import Path
import subprocess
import unittest

from test_protocol_schemas import assert_supported_schema, load_schema, validate_subset


ROOT = Path(__file__).resolve().parents[1]
DISPATCH_SCHEMA_PATH = ROOT / "schemas" / "dispatch.schema.json"
COMPAT_SCHEMA_PATH = ROOT / "schemas" / "compatibility-record-v1.schema.json"
COMPAT_PATH = ROOT / "references" / "EXECUTION_CONTRACT_REFS_V49_COMPATIBILITY.json"
REFERENCE_PATH = ROOT / "references" / "EXECUTION_CONTRACT_REFS_V49_REFERENCE.md"

BASE_SHA = "f4fe88542de9d3f5376498e62778e2353391bc57"
EXECUTION_PACK_HEAD = "593bea27380423e95e9ffc45b36e0a57f8b58324"
EXPECTED_BASE_BLOB = "4607f6cb4b690bf68137294a9acf5d6ccc49e6bd"

T008_REF_FIELDS = frozenset(
    {"assurance_currentness_ref", "role_profile_ref", "jit_phase_ref"}
)

# Read-only dependency surfaces: pinned blobs at the v4.9.0 T-008 base.
READ_ONLY_SURFACE_BLOBS = {
    "standards/EXECUTION_ARCHITECTURE_STANDARD.md": "ffe4788beaa342931ddf7c713523fb6f8a53d4c0",
    "standards/ASSURANCE_PLAN_STANDARD.md": "ddc39f2843e7af4b41b1cf2e6b34675c23bcb614",
    "schemas/assurance-plan-v2.schema.json": "92d9c61bc80a3c863aee04f28eebb7ed6291b94a",
    "schemas/role-execution-profile-v1.schema.json": "df96fb14dce9f39c753c80483e21c55b27beb685",
}

# Frozen planning authority: Frozen Product / Frozen L2 / Frozen Task DAG v0.2 /
# immutable Task DAG v0.1 (normative concern for T-008).
FROZEN_PLANNING_BLOBS = {
    "docs/implementation/4.9.0/PRD.md": "a8ec7030a14337a4c2dca853dc474e965679d610",
    "docs/implementation/4.9.0/L2_ARCHITECTURE_EVIDENCE.md": "bd41ea0175b459a6a490fd37ad579e429a58a1c3",
    "docs/implementation/4.9.0/TASK_DAG.md": "b9fe0cc7089f64929b4bcf45f7230d950e864db2",
    "docs/implementation/4.9.0/task-dag-history/TASK_DAG-v0.1-first-candidate.md": "4f358ba2b32e01ae17ddcdf970151cf28e44bb3f",
}

# Immutable JIT execution-pack planning files (pack head 593bea27).
PACK_PLANNING_PATHS = [
    ".agent/execution/T-008/MANIFEST.yaml",
    ".agent/execution/T-008/EXECUTION_CONTRACT.md",
    ".agent/execution/T-008/IMPLEMENTATION_MAP.md",
    ".agent/execution/T-008/TEST_MATRIX.yaml",
    ".agent/execution/T-008/FAILURE_MATRIX.yaml",
    ".agent/execution/T-008/REVIEW_CHECKLIST.md",
]

SCHEMA_V2 = json.loads(DISPATCH_SCHEMA_PATH.read_text(encoding="utf-8"))


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


def git_json_at(rev: str, rel: str) -> dict:
    result = subprocess.run(
        ["git", "show", f"{rev}:{rel}"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(result.stdout)


def base_dispatch_schema() -> dict:
    """Dispatch schema blob at the T-008 base (v1 authority)."""
    return git_json_at(BASE_SHA, "schemas/dispatch.schema.json")


def then_required_fields(schema: dict) -> set[str]:
    """Every property name some then-branch can require (top-level included)."""
    fields = set(schema.get("required", []))
    for clause in schema.get("allOf", []):
        then = clause.get("then", {})
        fields |= set(then.get("required", []))
    return fields


def builder_dispatch_fixture() -> dict:
    """v1-shaped builder dispatch: no T-008 reference fields."""
    return {
        "dispatch_id": "d-v4.9.0-T-008-builder-fixture",
        "repository": "kaicreator-mm/ai-development-standard",
        "version": "4.9.0",
        "task": "T-008",
        "issue": "#727",
        "role": "builder",
        "execution_profile": "LOCAL_BUILDER",
        "branch": "task/v4.9.0-t08-execution-contract-refs",
        "expected_base_sha": BASE_SHA,
        "pinned_standard_revision": BASE_SHA,
        "agent_freedom": "F1_BOUNDED_IMPLEMENTATION",
        "dispatch_state": "READY",
        "task_pack_ref": "docs/implementation/4.9.0/task-packs/T08_execution_contract_refs.md",
    }


def validator_dispatch_fixture() -> dict:
    """v1-shaped validator dispatch in CLAIMED state (claim-time rules apply)."""
    return {
        "dispatch_id": "d-v4.9.0-T-008-validator-fixture",
        "repository": "kaicreator-mm/ai-development-standard",
        "version": "4.9.0",
        "task": "T-008",
        "issue": "#727",
        "role": "validator",
        "execution_profile": "LOCAL_VALIDATOR",
        "branch": "task/v4.9.0-t08-execution-contract-refs",
        "expected_base_sha": BASE_SHA,
        "requested_head_sha": EXECUTION_PACK_HEAD,
        "validation_profile": "schema-compat-and-claim-binding",
        "pinned_standard_revision": BASE_SHA,
        "agent_freedom": "F1_BOUNDED_IMPLEMENTATION",
        "dispatch_state": "CLAIMED",
        "claimed_by": "validator:independent-v49-t008",
        "execution_pack_ref": ".agent/execution/T-008/EXECUTION_CONTRACT.md",
    }


def reviewer_dispatch_fixture() -> dict:
    """v1-shaped reviewer dispatch."""
    return {
        "dispatch_id": "d-v4.9.0-T-008-reviewer-fixture",
        "repository": "kaicreator-mm/ai-development-standard",
        "version": "4.9.0",
        "task": "T-008",
        "issue": "#727",
        "pr": "#727",
        "role": "reviewer",
        "execution_profile": "WEB_REVIEWER",
        "branch": "task/v4.9.0-t08-execution-contract-refs",
        "expected_base_sha": BASE_SHA,
        "pinned_standard_revision": BASE_SHA,
        "agent_freedom": "F1_BOUNDED_IMPLEMENTATION",
        "dispatch_state": "READY",
    }


def populated_refs() -> dict:
    return {
        "assurance_currentness_ref": "assurance-plan:v4.9.0/T-008#/currentness_binding",
        "role_profile_ref": "role-profile:v4.9.0/local-builder-primary",
        "jit_phase_ref": "jit-phase:v4.9.0/T-008#implementation",
    }


def claim_time_ref_binding(dispatch: dict, resolvable: frozenset[str]) -> dict | None:
    """Consumer-side resolve-or-fail-closed rule for the T-008 reference fields.

    Returns {field: ref} only when every declared reference field resolves
    against `resolvable`; otherwise returns None. A stale or missing reference
    never becomes a default and never passes currentness — the caller must fail
    the claim-time admission closed (section 28.1/28.6 recompute).
    """
    binding: dict[str, str] = {}
    for field in sorted(T008_REF_FIELDS):
        if field not in dispatch:
            continue
        ref = dispatch[field]
        if not isinstance(ref, str) or not ref or ref not in resolvable:
            return None
        binding[field] = ref
    return binding


class ExecutionContractRefsV49BackwardCompatibilityTests(unittest.TestCase):
    """W01 — all pre-existing dispatch instances remain schema-valid."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.base_schema = base_dispatch_schema()

    def test_dispatch_schema_uses_repository_supported_subset(self) -> None:
        assert_supported_schema(SCHEMA_V2)

    def test_schema_change_is_purely_additive(self) -> None:
        base_props = self.base_schema["properties"]
        cand_props = SCHEMA_V2["properties"]
        self.assertEqual(set(cand_props) - set(base_props), set(T008_REF_FIELDS))
        self.assertTrue(set(base_props) <= set(cand_props))
        for name, definition in base_props.items():
            self.assertEqual(
                definition,
                cand_props[name],
                f"pre-existing property {name!r} must be byte-identical",
            )
        self.assertEqual(self.base_schema["required"], SCHEMA_V2["required"])
        self.assertEqual(self.base_schema["allOf"], SCHEMA_V2["allOf"])
        self.assertEqual(
            self.base_schema.get("additionalProperties"),
            SCHEMA_V2.get("additionalProperties"),
        )
        self.assertEqual(self.base_schema.get("type"), SCHEMA_V2.get("type"))

    def test_v1_fixtures_remain_valid_under_base_and_candidate(self) -> None:
        for fixture in (
            builder_dispatch_fixture(),
            validator_dispatch_fixture(),
            reviewer_dispatch_fixture(),
        ):
            with self.subTest(dispatch_id=fixture["dispatch_id"]):
                self.assertEqual(validate_subset(fixture, self.base_schema), [])
                self.assertEqual(validate_subset(fixture, SCHEMA_V2), [])

    def test_v1_fixture_with_new_fields_still_accepted_by_v1_parser(self) -> None:
        instance = dict(builder_dispatch_fixture(), **populated_refs())
        self.assertEqual(validate_subset(instance, self.base_schema), [])


class ExecutionContractRefsV49OptionalFieldsTests(unittest.TestCase):
    """W02 — new optional reference fields populate/consume; no REQUIRED added."""

    def test_new_fields_are_optional(self) -> None:
        minimal = builder_dispatch_fixture()
        self.assertEqual(validate_subset(minimal, SCHEMA_V2), [])
        for field in sorted(T008_REF_FIELDS):
            with self.subTest(field=field):
                value = dict(minimal)
                value[field] = populated_refs()[field]
                self.assertEqual(validate_subset(value, SCHEMA_V2), [])
        full = dict(minimal, **populated_refs())
        self.assertEqual(validate_subset(full, SCHEMA_V2), [])

    def test_no_requiredness_introduced_for_new_fields(self) -> None:
        self.assertTrue(T008_REF_FIELDS.isdisjoint(then_required_fields(SCHEMA_V2)))
        self.assertEqual(
            then_required_fields(base_dispatch_schema()),
            then_required_fields(SCHEMA_V2),
            "required-ness surface must be unchanged",
        )
        for clause in SCHEMA_V2["allOf"]:
            then = clause.get("then", {})
            self.assertTrue(T008_REF_FIELDS.isdisjoint(then.get("required", [])))

    def test_populated_fields_round_trip(self) -> None:
        instance = dict(builder_dispatch_fixture(), **populated_refs())
        self.assertEqual(validate_subset(instance, SCHEMA_V2), [])
        binding = claim_time_ref_binding(
            instance,
            frozenset(populated_refs().values()),
        )
        self.assertEqual(binding, populated_refs())

    def test_field_inventory_is_bounded(self) -> None:
        expected = set(base_dispatch_schema()["properties"]) | set(T008_REF_FIELDS)
        self.assertEqual(set(SCHEMA_V2["properties"]), expected)


class ExecutionContractRefsV49ClaimBindingTests(unittest.TestCase):
    """W03 — refs resolve-or-fail-closed; stale ref cannot pass claim time."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.reference = REFERENCE_PATH.read_text(encoding="utf-8")

    def test_declared_refs_resolve_or_fail_closed(self) -> None:
        resolvable = frozenset(populated_refs().values())
        claimed = validator_dispatch_fixture()
        claimed.update(populated_refs())
        self.assertEqual(claim_time_ref_binding(claimed, resolvable), populated_refs())
        stale = dict(claimed)
        stale["assurance_currentness_ref"] = "assurance-plan:retired#/currentness_binding"
        self.assertIsNone(claim_time_ref_binding(stale, resolvable))
        missing = dict(claimed)
        missing["role_profile_ref"] = "role-profile:v4.9.0/never-materialized"
        self.assertIsNone(claim_time_ref_binding(missing, resolvable))
        unbound = validator_dispatch_fixture()
        self.assertEqual(claim_time_ref_binding(unbound, resolvable), {})

    def test_stale_currentness_ref_cannot_pass_claim_time(self) -> None:
        resolvable = frozenset(populated_refs().values())
        claimed = validator_dispatch_fixture()
        claimed.update(populated_refs())
        self.assertEqual(validate_subset(claimed, SCHEMA_V2), [])
        stale = dict(claimed)
        stale["assurance_currentness_ref"] = "assurance-plan:drifted@deadbeef#/currentness_binding"
        self.assertEqual(validate_subset(stale, SCHEMA_V2), [])
        self.assertIsNone(claim_time_ref_binding(stale, resolvable))
        self.assertIn(
            "A stale or missing reference never becomes a default",
            self.reference,
        )
        self.assertIn("never passes currentness", self.reference)

    def test_empty_refs_are_schema_invalid(self) -> None:
        for field in sorted(T008_REF_FIELDS):
            with self.subTest(field=field):
                value = builder_dispatch_fixture()
                value[field] = ""
                self.assertTrue(validate_subset(value, SCHEMA_V2))

    def test_reference_doc_states_recompute_discipline(self) -> None:
        for needle in (
            "resolve-or-fail-closed",
            "recompute point",
            "never ratified retroactively",
        ):
            with self.subTest(needle=needle):
                self.assertIn(needle, self.reference)


class ExecutionContractRefsV49CompatibilityRecordTests(unittest.TestCase):
    """W04 — compatibility record machine-checkable and truthful."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.compat = json.loads(COMPAT_PATH.read_text(encoding="utf-8"))
        cls.compat_schema = json.loads(COMPAT_SCHEMA_PATH.read_text(encoding="utf-8"))
        cls.dimensions = {item["name"]: item for item in cls.compat["dimensions"]}

    def test_compatibility_record_is_machine_checkable(self) -> None:
        self.assertEqual(validate_subset(self.compat, self.compat_schema), [])
        self.assertEqual(self.compat["record_id"], "v49-t008-execution-contract-refs")
        self.assertEqual(self.compat["contract"]["kind"], "json-schema")
        self.assertEqual(self.compat["contract"]["identity"], "dispatch")
        self.assertEqual(
            self.compat["baseline"]["sha_or_digest"],
            f"git-blob:{git_blob_sha(DISPATCH_SCHEMA_PATH, rev=BASE_SHA)}",
        )
        self.assertEqual(
            self.compat["baseline"]["sha_or_digest"],
            f"git-blob:{EXPECTED_BASE_BLOB}",
        )
        self.assertEqual(
            self.compat["candidate"]["sha_or_digest"],
            f"git-blob:{git_blob_sha(DISPATCH_SCHEMA_PATH)}",
        )

    def test_change_operations_declare_exactly_the_new_fields(self) -> None:
        operations = self.compat["change_operations"]
        self.assertEqual(
            operations,
            [
                "add-optional-assurance-currentness-ref",
                "add-optional-role-profile-ref",
                "add-optional-jit-phase-ref",
            ],
        )
        declared = {
            operation.removeprefix("add-optional-").removesuffix("-ref").replace("-", "_") + "_ref"
            for operation in operations
        }
        self.assertEqual(declared, set(T008_REF_FIELDS))

    def test_compatibility_dimensions_are_truthful(self) -> None:
        expected_outcomes = {
            "v1-instance-validity-at-candidate": "COMPATIBLE",
            "candidate-parser-accepts-v1-instance": "COMPATIBLE",
            "v1-parser-accepts-candidate-instance": "COMPATIBLE",
            "required-field-and-vocabulary-stability": "COMPATIBLE",
            "assurance-currentness-reference-semantics": "COMPATIBLE",
            "role-profile-reference-semantics": "COMPATIBLE",
            "jit-phase-reference-semantics": "COMPATIBLE",
            "authority-and-gate-boundaries": "COMPATIBLE",
            "material-change-declaration": "COMPATIBLE",
        }
        self.assertEqual(set(self.dimensions), set(expected_outcomes))
        for name, outcome in expected_outcomes.items():
            self.assertEqual(self.dimensions[name]["outcome"], outcome, name)
        self.assertNotIn("UNKNOWN", {item["outcome"] for item in self.dimensions.values()})
        for name, item in self.dimensions.items():
            with self.subTest(dimension=name):
                self.assertTrue(item["evidence_refs"], name)
                for ref in item["evidence_refs"]:
                    file_part = ref.split("#", 1)[0]
                    self.assertTrue((ROOT / file_part).exists(), ref)

    def test_declared_incompatible_dimensions_fail_closed(self) -> None:
        """An INCOMPATIBLE declaration must match executable failing probes."""
        v1_fixture = builder_dispatch_fixture()
        probes = {
            "candidate-parser-accepts-v1-instance": lambda: validate_subset(v1_fixture, SCHEMA_V2) == [],
            "v1-parser-accepts-candidate-instance": lambda: validate_subset(
                dict(v1_fixture, **populated_refs()), base_dispatch_schema()
            )
            == [],
        }
        for name, probe in probes.items():
            with self.subTest(dimension=name):
                declared = self.dimensions[name]["outcome"]
                if declared == "INCOMPATIBLE":
                    self.assertFalse(probe(), f"{name} declared INCOMPATIBLE but probe passes")
                else:
                    self.assertTrue(probe(), f"{name} probe must pass when declared {declared}")


class ExecutionContractRefsV49AuthorityBoundaryTests(unittest.TestCase):
    """W05 — no duplicate Task scope, Claim authority or gate truth."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.base_schema = base_dispatch_schema()
        cls.reference = REFERENCE_PATH.read_text(encoding="utf-8")

    def test_authority_and_gate_vocabulary_unchanged(self) -> None:
        for field in (
            "dispatch_state",
            "result",
            "role",
            "execution_profile",
            "agent_freedom",
        ):
            with self.subTest(field=field):
                self.assertEqual(
                    self.base_schema["properties"][field],
                    SCHEMA_V2["properties"][field],
                    f"{field} vocabulary must stay frozen byte-for-byte",
                )

    def test_new_fields_carry_identity_not_semantics(self) -> None:
        for field in sorted(T008_REF_FIELDS):
            with self.subTest(field=field):
                definition = SCHEMA_V2["properties"][field]
                self.assertNotIn("enum", definition)
                self.assertNotIn("const", definition)
                self.assertEqual(definition["type"], ["string", "null"])
                self.assertIn("Reference only", definition["description"])
                self.assertIn("never", definition["description"])

    def test_reference_doc_states_authority_boundaries(self) -> None:
        for needle in (
            "carry identity only",
            "never duplicate Task scope, Claim authority or gate truth",
            "never grants role actions, terminal authority, executor capability or a claim-policy switch",
            "never widens the Task envelope",
        ):
            with self.subTest(needle=needle):
                self.assertIn(needle, self.reference)

    def test_no_new_authority_fields_added(self) -> None:
        self.assertEqual(
            set(SCHEMA_V2["properties"]) - set(self.base_schema["properties"]),
            set(T008_REF_FIELDS),
        )


class ExecutionContractRefsV49LifecycleBoundaryTests(unittest.TestCase):
    """W06 — no second lifecycle/workflow state; read-only surfaces unmutated."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.reference = REFERENCE_PATH.read_text(encoding="utf-8")

    def test_reference_doc_states_non_goals(self) -> None:
        for needle in (
            "a second lifecycle",
            "a new scheduler",
            "workflow state",
            "a runtime authority store",
        ):
            with self.subTest(needle=needle):
                self.assertIn(needle, self.reference)

    def test_new_fields_introduce_no_state_vocabulary(self) -> None:
        for field in sorted(T008_REF_FIELDS):
            with self.subTest(field=field):
                definition = SCHEMA_V2["properties"][field]
                self.assertEqual(set(definition) - {"description"}, {"type", "minLength"})

    def test_reference_doc_anchors_resolve(self) -> None:
        for anchor in (
            "## Field semantics",
            "## Claim-time and currentness consistency",
            "## Authority and gate boundaries",
            "## Backward compatibility",
            "## Material change declaration",
            "## Non-goals",
        ):
            with self.subTest(anchor=anchor):
                self.assertIn(anchor, self.reference)

    def test_read_only_dependency_surfaces_unmutated(self) -> None:
        for rel, blob in READ_ONLY_SURFACE_BLOBS.items():
            with self.subTest(path=rel):
                self.assertEqual(git_blob_sha(ROOT / rel), blob)
                self.assertEqual(git_blob_sha(ROOT / rel, rev=BASE_SHA), blob)

    def test_frozen_planning_blobs_resolve_unchanged(self) -> None:
        for rel, blob in FROZEN_PLANNING_BLOBS.items():
            with self.subTest(path=rel):
                self.assertEqual(git_blob_sha(ROOT / rel), blob)
                self.assertEqual(git_blob_sha(ROOT / rel, rev=BASE_SHA), blob)

    def test_execution_pack_planning_files_immutable(self) -> None:
        for rel in PACK_PLANNING_PATHS:
            with self.subTest(path=rel):
                self.assertEqual(
                    git_blob_sha(ROOT / rel),
                    git_blob_sha(ROOT / rel, rev=EXECUTION_PACK_HEAD),
                )

    def test_task_pack_and_l3_unchanged_since_pack_head(self) -> None:
        for rel in (
            "docs/implementation/4.9.0/task-packs/T08_execution_contract_refs.md",
            "docs/implementation/4.9.0/L3_REFERENCE_PACKS.md",
        ):
            with self.subTest(path=rel):
                self.assertEqual(
                    git_blob_sha(ROOT / rel),
                    git_blob_sha(ROOT / rel, rev=EXECUTION_PACK_HEAD),
                )


if __name__ == "__main__":
    import sys

    result = unittest.TextTestRunner(verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
    )
    raise SystemExit(0 if result.wasSuccessful() else 1)
