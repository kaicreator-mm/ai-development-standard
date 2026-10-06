"""v4.9 T003 authority/state registry integration verifier.

Additive conformance for the v4.9 semantic-authority entries and the
proof/currentness + WAITING_LINEAGE state-dimension registrations on top of the
inherited v4.7 registries. This module reuses the inherited resolver and
schema-subset validators (no second resolver), and enforces the TEST_MATRIX
R01-R12 oracles / #722 preflight N01-N14 negative oracles. It is deterministic
discovery-metadata conformance evidence, not a permission engine, not a live
state store, and never a source of Validation/Review/Release verdicts.
"""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import re
import unittest

from test_protocol_schemas import validate_subset
from test_v47_authority_registry import RegistryError, resolve_registry, validate_entry
from test_v47_state_dimension_registry import (
    EXACT_UPSTREAM,
    REQUIRED_NEGATIVES as INHERITED_REQUIRED_NEGATIVES,
    consistency_errors,
    runtime_owner_errors,
)
from test_work_item_contract_and_golden_templates import (
    CANONICAL_STATES,
    markdown_anchors,
    validate_ref,
)

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "standard-manifest.json"
STATE_REGISTRY = ROOT / "registries/state-dimensions-v1.json"
ENTRY_SCHEMA = ROOT / "schemas/authority-applicability-entry-v1.schema.json"
STATE_SCHEMA = ROOT / "schemas/state-dimension-registry-v1.schema.json"
COVERAGE = ROOT / "templates/golden/STANDARD_COVERAGE.json"
AUTHORITY_REFERENCE = ROOT / "references/AUTHORITY_APPLICABILITY_REGISTRY_REFERENCE.md"
STATE_REFERENCE = ROOT / "references/STATE_DIMENSION_REGISTRY_REFERENCE.md"
ASSURANCE_STANDARD = "standards/ASSURANCE_PLAN_STANDARD.md"

# Frozen base (version/v4.9.0@df94641e / tree a8c86675) inherited inventory that
# T-003 must carry verbatim. Pinned structurally so a candidate regression in
# any carried entry fails here independently of the v4.8-candidate suite.
INHERITED_NORMATIVE_STANDARDS = [
    "standards/ARCHITECTURE_DESIGN_STANDARD.md",
    "standards/ARCHITECTURE_RESEARCH_DEMO_STANDARD.md",
    "standards/CHATGPT_WEB_ROLE.md",
    "standards/CI_EVIDENCE_STANDARD.md",
    "standards/CI_EXECUTION_STANDARD.md",
    "standards/CI_RUNNER_CAPABILITY_STANDARD.md",
    "standards/CODEX_HANDOFF_PROTOCOL.md",
    "standards/CODEX_ROLE.md",
    "standards/CONFIGURATION_SECRETS_STANDARD.md",
    "standards/DATA_MIGRATION_GOVERNANCE_STANDARD.md",
    "standards/DEPENDENCY_TOOLCHAIN_GOVERNANCE_STANDARD.md",
    "standards/DEVELOPMENT_WORKFLOW.md",
    "standards/DOCUMENTATION_STANDARD.md",
    "standards/EXECUTION_ARCHITECTURE_STANDARD.md",
    "standards/EXECUTION_PACK_STANDARD.md",
    "standards/EXTERNAL_SYSTEM_EXECUTION_STANDARD.md",
    "standards/GIT_EXECUTION_STANDARD.md",
    "standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md",
    "standards/GITHUB_CAPABILITY_FALLBACK.md",
    "standards/GITHUB_WORK_ITEM_CONTRACT_STANDARD.md",
    "standards/GOLDEN_TEMPLATE_STANDARD.md",
    "standards/IMPLEMENTATION_QUALITY_STANDARD.md",
    "standards/INTERFACE_COMPATIBILITY_GOVERNANCE_STANDARD.md",
    "standards/ISSUE_FIRST_TASK_TRIGGER.md",
    "standards/LOCAL_AGENT_HANDOFF_PROTOCOL.md",
    "standards/MODEL_USAGE_POLICY.md",
    "standards/PROJECT_ADOPTION.md",
    "standards/PROJECT_STRUCTURE.md",
    "standards/RELEASE_STANDARD.md",
    "standards/REPOSITORY_STANDARD.md",
    "standards/TASK_DAG_GOVERNANCE_STANDARD.md",
    "standards/TASK_DECOMPOSITION_STANDARD.md",
    "standards/TESTING_STANDARD.md",
    "standards/TEST_DATA_AND_SCENARIO_STANDARD.md",
    "standards/VALIDATION_STANDARD.md",
    "standards/WORKSPACE_ARTIFACT_STANDARD.md",
    # Post-recovery recompose re-bind (#805 POST_RECOVERY_EXACT_RECOMPOSE,
    # #745): the recovery-integrated main merge (4c632256) carries the
    # recovered v4.4-v4.7 normative families into the composed tree, so the
    # inherited inventory the registry must carry grows by exactly these nine
    # recovered standards. Constant extension only — the assertion stays an
    # exact closed-set equality, so any other inventory mutation still fails.
    "standards/BUILD_ARTIFACT_GOVERNANCE_STANDARD.md",
    "standards/CONTEXT_ENGINEERING_STANDARD.md",
    "standards/DEPLOYMENT_GOVERNANCE_STANDARD.md",
    "standards/DISTRIBUTION_GOVERNANCE_STANDARD.md",
    "standards/INCIDENT_RECOVERY_FEEDBACK_STANDARD.md",
    "standards/INTENT_ASSUMPTION_GOVERNANCE_STANDARD.md",
    "standards/MAINTENANCE_EOL_HOTFIX_STANDARD.md",
    "standards/OBSERVABILITY_RUNTIME_EVIDENCE_STANDARD.md",
    "standards/SKILL_PROCEDURE_GOVERNANCE_STANDARD.md",
]

INHERITED_SEMANTIC_ENTRIES = [
    ("development-lifecycle", "development.lifecycle_and_task_stage", "standards/DEVELOPMENT_WORKFLOW.md", "ALWAYS"),
    ("github-agent-coordination", "github.issue_pr_event_coordination", "standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md", "MATERIALITY_DRIVEN"),
    ("execution-state", "execution.controller_and_dispatch_state", "standards/EXECUTION_ARCHITECTURE_STANDARD.md", "MATERIALITY_DRIVEN"),
    ("work-item-contract", "github.work_item_contract", "standards/GITHUB_WORK_ITEM_CONTRACT_STANDARD.md", "MATERIALITY_DRIVEN"),
    ("validation-evidence", "validation.concern_evidence_and_exact_subject", "standards/VALIDATION_STANDARD.md", "MATERIALITY_DRIVEN"),
    ("release-qualification", "release.qualification_and_candidate_gate", "standards/RELEASE_STANDARD.md", "MATERIALITY_DRIVEN"),
    ("runner-capability", "ci.runner_capability_adoption", "standards/CI_RUNNER_CAPABILITY_STANDARD.md", "PROJECT_DEFINED"),
    ("research-demo", "architecture.research_demo", "standards/ARCHITECTURE_RESEARCH_DEMO_STANDARD.md", "OPTIONAL"),
    ("task-learning-evidence", "execution.task_learning_evidence", "standards/EXECUTION_ARCHITECTURE_STANDARD.md", "MATERIALITY_DRIVEN"),
    ("logical-agent-capability-profile", "execution.logical_agent_capability_claim", "standards/EXECUTION_ARCHITECTURE_STANDARD.md", "MATERIALITY_DRIVEN"),
    ("agent-capability-evidence", "execution.agent_capability_evidence", "standards/EXECUTION_ARCHITECTURE_STANDARD.md", "MATERIALITY_DRIVEN"),
]

# Frozen DAG v0.1 `### T-003` "Own" set: one canonical entry per new v4.9
# semantic concern (Frozen L2 §3 canonical owner map, §3.1, §6, §10).
V49_SEMANTIC_ENTRIES = [
    ("assurance-proof-currentness", "assurance.proof_composition_and_currentness", ASSURANCE_STANDARD, "MATERIALITY_DRIVEN"),
    ("role-execution-profile", "execution.role_execution_profile_projection", "standards/EXECUTION_ARCHITECTURE_STANDARD.md", "MATERIALITY_DRIVEN"),
    ("release-applicability", "release.per_gate_subject_applicability", "standards/RELEASE_STANDARD.md", "MATERIALITY_DRIVEN"),
]

INHERITED_DIMENSIONS = [
    ("work_item_workflow", "standards/GITHUB_WORK_ITEM_CONTRACT_STANDARD.md", "CLOSED"),
    ("dispatch_lifecycle", "standards/EXECUTION_ARCHITECTURE_STANDARD.md", "CLOSED"),
    ("execution_pack_currentness", "standards/EXECUTION_PACK_STANDARD.md", "CLOSED"),
    ("validation_gate", "standards/VALIDATION_STANDARD.md", "CLOSED"),
    ("review_judgment", "standards/EXECUTION_ARCHITECTURE_STANDARD.md", "OWNER_DEFINED"),
    ("release_qualification", "standards/RELEASE_STANDARD.md", "CLOSED"),
    ("deployment_result", "github:kaicreator-mm/ai-development-standard@88f5ba907513338192c6ae27d48880de13f1b98e:standards/DEPLOYMENT_GOVERNANCE_STANDARD.md", "CLOSED"),
    ("runtime_health", "github:kaicreator-mm/ai-development-standard@c9ee9249999aa5463ce880bc7674b732979009b3:standards/OBSERVABILITY_RUNTIME_EVIDENCE_STANDARD.md", "OWNER_DEFINED"),
    ("runner_capability", "standards/CI_RUNNER_CAPABILITY_STANDARD.md", "OWNER_DEFINED"),
]

# v4.9 forbidden inferences (F11=N03, F12=N06, F13-F16=N07, F17-F19=N08/L2 §8.3).
V49_REQUIRED_NEGATIVES = {
    "F11_TASK_DONE_NOT_LINEAGE_CURRENT":
        ("work_item_workflow", "state:done", "waiting_lineage", "LINEAGE_CURRENT"),
    "F12_CONCERN_RELEASE_APPLICABILITY_NOT_VERSION_APPLICABLE":
        ("release_qualification", "RELEASE-APPLICABLE@concern-gate-x-subject", "release_qualification", "RELEASE-APPLICABLE@version-candidate"),
    "F13_ASSURANCE_CURRENT_NOT_VALIDATION_PASS":
        ("assurance_proof_currentness", "CURRENT", "validation_gate", "PASS"),
    "F14_ASSURANCE_CURRENT_NOT_REVIEW_PASS":
        ("assurance_proof_currentness", "CURRENT", "review_judgment", "PASS"),
    "F15_ASSURANCE_CURRENT_NOT_RELEASE_READY":
        ("assurance_proof_currentness", "CURRENT", "release_qualification", "READY"),
    "F16_ASSURANCE_CURRENT_NOT_TASK_READY":
        ("assurance_proof_currentness", "CURRENT", "work_item_workflow", "state:ready"),
    "F17_WAITING_LINEAGE_NOT_WORKFLOW_BLOCKED":
        ("waiting_lineage", "derived-wait-posture", "work_item_workflow", "state:blocked"),
    "F18_WAITING_LINEAGE_NOT_GATE_PASS":
        ("waiting_lineage", "derived-wait-posture", "validation_gate", "PASS"),
    "F19_WAITING_LINEAGE_NOT_GATE_FAIL":
        ("waiting_lineage", "derived-wait-posture", "validation_gate", "FAIL"),
}

GRANT_LIKE_ENTRY_FIELDS = (
    "mutation_allowed", "merge_allowed", "side_effect_allowed", "dispatch_authorized",
    "review_pass", "validation_pass", "release_ready", "release_applicable",
    "capability_proven", "authority_granted", "lineage_current",
)

GRANT_LIKE_TOKEN = re.compile(r"allowed_actions|terminal_authority|mutation_authorized|grants?_authority")


def required_negative_errors(registry: dict) -> list[str]:
    """Every inherited F01-F10 and new v4.9 rule must exist with its exact tuple."""
    errors = []
    by_id = {rule["rule_id"]: rule for rule in registry.get("forbidden_inferences", [])}
    if len(by_id) != len(registry.get("forbidden_inferences", [])):
        errors.append("duplicate rule id")
    for name, expected in {**INHERITED_RULE_TUPLES, **V49_REQUIRED_NEGATIVES}.items():
        rule = by_id.get(name)
        if rule is None:
            errors.append(f"missing required negative: {name}")
            continue
        actual = (
            rule["source_dimension_ref"], rule["source_fact_ref"],
            rule["target_dimension_ref"], rule["prohibited_conclusion_ref"],
        )
        if actual != expected:
            errors.append(f"weakened/retargeted negative {name}: {actual} != {expected}")
    return errors


INHERITED_RULE_TUPLES = {
    "F01_TASK_DONE_NOT_VALIDATION_PASS": ("work_item_workflow", "state:done", "validation_gate", "PASS"),
    "F02_REVIEW_PASS_NOT_VALIDATION_PASS": ("review_judgment", "PASS", "validation_gate", "PASS"),
    "F03_VALIDATION_PASS_NOT_RELEASE_READY": ("validation_gate", "PASS", "release_qualification", "READY"),
    "F04_RELEASE_READY_NOT_DEPLOYMENT_SUCCESS": ("release_qualification", "READY", "deployment_result", "DEPLOYMENT_SUCCEEDED"),
    "F05_DEPLOYMENT_SUCCESS_NOT_RUNTIME_HEALTH": ("deployment_result", "DEPLOYMENT_SUCCEEDED", "runtime_health", "runtime-health-established"),
    "F06_RUNNER_AVAILABLE_NOT_MUTATION_AUTHORITY": ("runner_capability", "observed-or-declared-AVAILABLE", "work_item_workflow", "task-mutation-authorized"),
    "F07_OLD_SHA_VALIDATION_NOT_SUCCESSOR_PASS": ("validation_gate", "PASS@original-exact-SHA", "validation_gate", "PASS@successor-exact-SHA"),
    "F08_SANDBOX_PASS_NOT_REAL_ENV_PASS": ("validation_gate", "PASS@sandbox-tuple", "validation_gate", "PASS@unexecuted-real-environment-tuple"),
    "F09_DISPATCH_COMPLETED_NOT_RELEASE_READY": ("dispatch_lifecycle", "COMPLETED", "release_qualification", "READY"),
    "F10_PACK_CURRENT_NOT_VALIDATION_PASS": ("execution_pack_currentness", "PACK_CURRENT", "validation_gate", "PASS"),
}


def reference_resolution_errors(registry: dict) -> list[str]:
    """All local pointer refs (owner files, vocabulary/notes refs) must resolve.

    Anchors are validated with the repository's own golden validate_ref
    mechanics; github-pinned upstream refs are checked for exact-SHA shape only
    (their currentness is not provable locally and must fail closed elsewhere).
    """
    errors = []
    for dimension in registry.get("dimensions", []):
        owner = dimension["canonical_owner_ref"]
        if owner.startswith("standards/"):
            if not (ROOT / owner).is_file():
                errors.append(f"broken local owner: {owner}")
        elif not EXACT_UPSTREAM.fullmatch(owner):
            errors.append(f"mutable/unqualified owner: {owner}")
        for key in ("vocabulary_ref", "notes_ref"):
            ref = dimension.get(key)
            if ref and not ref.startswith("github:"):
                try:
                    validate_ref(ref)
                except (AssertionError, OSError) as exc:
                    errors.append(f"{dimension['dimension_id']} {key} unresolved: {exc}")
    for rule in registry.get("forbidden_inferences", []):
        rationale = rule.get("rationale_ref")
        if rationale and not rationale.startswith("github:"):
            try:
                validate_ref(rationale)
            except (AssertionError, OSError) as exc:
                errors.append(f"{rule['rule_id']} rationale_ref unresolved: {exc}")
    return errors


def semantic_entry_tuples(entries: list) -> list:
    return [
        (e["entry_id"], e["semantic_concern"], e["canonical_owner_ref"], e["applicability_posture"])
        for e in entries
    ]


class V49AuthorityStateRegistryTests(unittest.TestCase):
    maxDiff = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        cls.registry = json.loads(STATE_REGISTRY.read_text(encoding="utf-8"))
        cls.entry_schema = json.loads(ENTRY_SCHEMA.read_text(encoding="utf-8"))
        cls.state_schema = json.loads(STATE_SCHEMA.read_text(encoding="utf-8"))
        cls.coverage = json.loads(COVERAGE.read_text(encoding="utf-8"))
        cls.authority_reference = AUTHORITY_REFERENCE.read_text(encoding="utf-8")
        cls.state_reference = STATE_REFERENCE.read_text(encoding="utf-8")
        cls.entries = cls.manifest["semantic_authorities"]["entries"]

    def expect_rejected(self, mutant_manifest: dict) -> None:
        with self.assertRaises(RegistryError):
            resolve_registry(mutant_manifest, self.entry_schema)

    # ------------------------------------------------------------------
    # R12 / R01 base conformance: schema + inherited resolver + refs.
    # ------------------------------------------------------------------
    def test_r12_both_registries_validate_against_inherited_v1_schemas(self) -> None:
        self.assertEqual(validate_subset(self.registry, self.state_schema), [])
        self.assertEqual(consistency_errors(self.registry), [])
        self.assertEqual(runtime_owner_errors(self.registry), [])
        self.assertEqual(self.registry["schema_version"], 1)
        for entry in self.entries:
            validate_entry(entry, self.entry_schema)
        resolved = resolve_registry(self.manifest, self.entry_schema, root=ROOT)
        self.assertTrue(resolved)
        self.assertEqual(reference_resolution_errors(self.registry), [])

    # ------------------------------------------------------------------
    # R12 / N14: inherited surfaces preserved verbatim and non-weakened.
    # ------------------------------------------------------------------
    def test_r12_inherited_inventory_and_entries_are_carried_verbatim(self) -> None:
        normative = self.manifest["sections"]["normative_standards"]
        self.assertEqual(len(normative), len(set(normative)))
        self.assertEqual(set(normative), set(INHERITED_NORMATIVE_STANDARDS) | {ASSURANCE_STANDARD})
        self.assertEqual(semantic_entry_tuples(self.entries[: len(INHERITED_SEMANTIC_ENTRIES)]), INHERITED_SEMANTIC_ENTRIES)
        inherited_dims = {
            (d["dimension_id"], d["canonical_owner_ref"], d["vocabulary_posture"])
            for d in self.registry["dimensions"]
        }
        for tuple_ in INHERITED_DIMENSIONS:
            self.assertIn(tuple_, inherited_dims)
        self.assertEqual(required_negative_errors(self.registry), [])

    # ------------------------------------------------------------------
    # R01 / N01: exactly one canonical entry per v4.9 concern, zero duplicates.
    # ------------------------------------------------------------------
    def test_r01_every_v49_concern_has_exactly_one_canonical_entry(self) -> None:
        by_id = {entry["entry_id"]: entry for entry in self.entries}
        self.assertEqual(len(by_id), len(self.entries))
        for entry_id, concern, owner, posture in V49_SEMANTIC_ENTRIES:
            matches = [e for e in self.entries if e["semantic_concern"] == concern]
            self.assertEqual(len(matches), 1, concern)
            entry = by_id[entry_id]
            self.assertEqual(entry["semantic_concern"], concern)
            self.assertEqual(entry["canonical_owner_ref"], owner)
            self.assertEqual(entry["applicability_posture"], posture)
            self.assertEqual(entry["schema_version"], 1)
        self.assertEqual(len(self.entries), len(INHERITED_SEMANTIC_ENTRIES) + len(V49_SEMANTIC_ENTRIES))
        resolved = resolve_registry(self.manifest, self.entry_schema)
        for _, concern, owner, _ in V49_SEMANTIC_ENTRIES:
            self.assertEqual(resolved[concern], owner)

    def test_r01_n01_duplicate_concern_or_id_fails_regardless_of_order(self) -> None:
        contender = deepcopy(self.entries[-1])
        contender["entry_id"] = "competing-discovery-only"
        mutant = deepcopy(self.manifest)
        mutant["semantic_authorities"]["entries"].append(contender)
        self.expect_rejected(mutant)
        mutant["semantic_authorities"]["entries"].reverse()
        self.expect_rejected(mutant)
        duplicate_id = deepcopy(self.manifest)
        duplicate_id["semantic_authorities"]["entries"][-1]["entry_id"] = duplicate_id["semantic_authorities"]["entries"][0]["entry_id"]
        self.expect_rejected(duplicate_id)

    # ------------------------------------------------------------------
    # R01 currentness binding: normative registration + golden coverage twin.
    # ------------------------------------------------------------------
    def test_r01_assurance_owner_is_normatively_registered_with_coverage_twin(self) -> None:
        self.assertIn(ASSURANCE_STANDARD, self.manifest["sections"]["normative_standards"])
        self.assertTrue((ROOT / ASSURANCE_STANDARD).is_file())
        normative = set(self.manifest["sections"]["normative_standards"])
        records = self.coverage["coverage"]
        standards = [record["standard"] for record in records]
        self.assertEqual(len(standards), len(set(standards)))
        self.assertEqual(set(standards), normative)
        record = next(r for r in records if r["standard"] == ASSURANCE_STANDARD)
        self.assertEqual(
            (record["golden_ref"], record["forbidden_ref"], record["rationale_ref"]),
            (
                "references/ASSURANCE_PLAN_OWNER_REFERENCE.md",
                f"{ASSURANCE_STANDARD}#6-forbidden-interpretations",
                f"{ASSURANCE_STANDARD}#1-purpose-and-owner-continuity",
            ),
        )
        for key in ("golden_ref", "forbidden_ref", "rationale_ref"):
            validate_ref(record[key])

    # ------------------------------------------------------------------
    # R02 / N02: discovery metadata can never grant authority.
    # ------------------------------------------------------------------
    def test_r02_n02_grant_like_metadata_fails_closed_everywhere(self) -> None:
        for key in GRANT_LIKE_ENTRY_FIELDS:
            mutant = deepcopy(self.manifest)
            mutant["semantic_authorities"]["entries"][0][key] = True
            self.expect_rejected(mutant)
        for key in ("authorization", "mutation_allowed", "release_ready"):
            mutant = deepcopy(self.manifest)
            mutant["semantic_authorities"][key] = "ALLOW"
            self.expect_rejected(mutant)
        for key in ("current_state", "transition", "mutation_authorized", "release_pass",
                    "validation_pass", "deployment_authorized", "lineage_current"):
            bad = deepcopy(self.registry)
            bad[key] = True
            self.assertTrue(validate_subset(bad, self.state_schema), key)
        bad_rule = deepcopy(self.registry)
        bad_rule["forbidden_inferences"][0]["inference_grant"] = True
        self.assertTrue(validate_subset(bad_rule, self.state_schema))
        self.assertIn("REGISTRY_AUTHORITY_EFFECT=NONE", self.authority_reference)

    # ------------------------------------------------------------------
    # R03 / N03: task DONE never implies lineage current.
    # ------------------------------------------------------------------
    def test_r03_n03_done_never_implies_lineage_current(self) -> None:
        self.assertEqual(required_negative_errors(self.registry), [])  # F11 exact
        self.assertNotIn(
            ("work_item_workflow", "LINEAGE_CURRENT"),
            [(r["source_dimension_ref"], r["prohibited_conclusion_ref"])
             for r in self.registry["forbidden_inferences"]
             if r["rule_id"] != "F11_TASK_DONE_NOT_LINEAGE_CURRENT" and r["target_dimension_ref"] == "waiting_lineage"],
        )
        resolved = resolve_registry(self.manifest, self.entry_schema, root=ROOT)
        self.assertNotIn("lineage.currentness", resolved)

    # ------------------------------------------------------------------
    # R04 / N04+N05: Role Profile is projection-only; capability stays v4.8-owned.
    # ------------------------------------------------------------------
    def test_r04_n04_role_profile_presence_never_implies_capability_proven(self) -> None:
        role_entry = next(e for e in self.entries if e["entry_id"] == "role-execution-profile")
        self.assertEqual(role_entry["canonical_owner_ref"], "standards/EXECUTION_ARCHITECTURE_STANDARD.md")
        self.assertEqual(role_entry["semantic_concern"], "execution.role_execution_profile_projection")
        concerns = {e["semantic_concern"] for e in self.entries}
        self.assertFalse(concerns & {"execution.agent_capability_proven", "execution.role_capability_proof"})
        self.assertTrue(
            {"execution.logical_agent_capability_claim", "execution.agent_capability_evidence"}.issubset(concerns)
        )
        self.assertIn("never capability proof", self.authority_reference)

    def test_r04_n05_no_role_action_or_terminal_authority_grant_exists(self) -> None:
        surfaces = json.dumps(self.manifest["semantic_authorities"]) + json.dumps(self.registry)
        self.assertIsNone(GRANT_LIKE_TOKEN.search(surfaces))
        self.assertNotIn("terminal_authority_ref", surfaces)
        self.assertNotIn("allowed_actions", surfaces)

    # ------------------------------------------------------------------
    # R05 / N06: concern-level Release applicability never aggregates to version.
    # ------------------------------------------------------------------
    def test_r05_n06_concern_release_applicability_not_version_applicable(self) -> None:
        self.assertEqual(required_negative_errors(self.registry), [])  # F12 exact
        release_entry = next(e for e in self.entries if e["entry_id"] == "release-applicability")
        self.assertEqual(release_entry["semantic_concern"], "release.per_gate_subject_applicability")
        self.assertEqual(release_entry["canonical_owner_ref"], "standards/RELEASE_STANDARD.md")
        self.assertIn("never aggregates to version-level", self.authority_reference)

    # ------------------------------------------------------------------
    # R06 / N07: proof/currentness CURRENT never implies gate verdicts or Task READY.
    # ------------------------------------------------------------------
    def test_r06_n07_assurance_current_not_gate_pass_or_task_ready(self) -> None:
        self.assertEqual(required_negative_errors(self.registry), [])  # F13-F16 exact
        dimension_ids = {d["dimension_id"] for d in self.registry["dimensions"]}
        self.assertIn("assurance_proof_currentness", dimension_ids)
        self.assertIn("STALE", self.state_reference)
        self.assertIn("UNKNOWN", self.state_reference)

    # ------------------------------------------------------------------
    # R07 / N08: WAITING_LINEAGE stays a derived, non-dispatch projection.
    # ------------------------------------------------------------------
    def test_r07_n08_waiting_lineage_is_derived_projection_not_workflow_state(self) -> None:
        self.assertEqual(required_negative_errors(self.registry), [])  # F17-F19 exact
        dims = {d["dimension_id"]: d for d in self.registry["dimensions"]}
        waiting = dims["waiting_lineage"]
        self.assertEqual(waiting["canonical_owner_ref"], "standards/EXECUTION_ARCHITECTURE_STANDARD.md")
        self.assertEqual(waiting["vocabulary_posture"], "OWNER_DEFINED")
        dimension_ids = set(dims)
        self.assertFalse(dimension_ids & CANONICAL_STATES)
        self.assertNotIn("state:blocked", dimension_ids)
        workflow_owner = dims["work_item_workflow"]["canonical_owner_ref"]
        self.assertNotEqual(waiting["canonical_owner_ref"], workflow_owner)
        for illegal in ("states", "transitions", "master", "current_state"):
            self.assertNotIn(illegal, self.registry)
        self.assertIn("not a canonical Issue state", self.state_reference)
        self.assertIn("no guaranteed-blocked dispatch", self.state_reference)

    # ------------------------------------------------------------------
    # R08 / N09: stale/broken/ambiguous refs fail closed; no fallback owner.
    # ------------------------------------------------------------------
    def test_r08_n09_broken_or_ambiguous_owner_refs_fail_closed(self) -> None:
        not_normative = deepcopy(self.manifest)
        not_normative["semantic_authorities"]["entries"][-1]["canonical_owner_ref"] = "standards/GITHUB_WORKFLOW.md"
        self.expect_rejected(not_normative)
        missing = deepcopy(self.manifest)
        missing["semantic_authorities"]["entries"][-1]["canonical_owner_ref"] = "standards/DOES_NOT_EXIST.md"
        self.expect_rejected(missing)
        absent_file = deepcopy(self.manifest)
        absent_file["semantic_authorities"]["entries"][-1]["canonical_owner_ref"] = "standards/UNREGISTERED_MISSING.md"
        absent_file["sections"]["normative_standards"].append("standards/UNREGISTERED_MISSING.md")
        with self.assertRaises(RegistryError):
            resolve_registry(absent_file, self.entry_schema, root=ROOT)
        broken_note = deepcopy(self.manifest)
        broken_note["semantic_authorities"]["entries"][-1]["notes_ref"] = "references/DEFINITELY_MISSING.md"
        with self.assertRaises(RegistryError):
            resolve_registry(broken_note, self.entry_schema, root=ROOT)
        broken_registry_ref = deepcopy(self.registry)
        broken_registry_ref["dimensions"][-1]["notes_ref"] = "docs/implementation/4.9.0/L2_ARCHITECTURE_EVIDENCE.md#definitely-missing-anchor"
        self.assertTrue(any("unresolved" in e for e in reference_resolution_errors(broken_registry_ref)))
        resolved = resolve_registry(self.manifest, self.entry_schema)
        normative = set(self.manifest["sections"]["normative_standards"])
        self.assertTrue(set(resolved.values()).issubset(normative))

    # ------------------------------------------------------------------
    # R09 / N10: old-SHA PASS / snapshot transfer stays prohibited.
    # ------------------------------------------------------------------
    def test_r09_n10_old_sha_pass_and_snapshot_transfer_remain_prohibited(self) -> None:
        by_id = {r["rule_id"]: r for r in self.registry["forbidden_inferences"]}
        self.assertEqual(by_id["F07_OLD_SHA_VALIDATION_NOT_SUCCESSOR_PASS"]["source_fact_ref"], "PASS@original-exact-SHA")
        self.assertEqual(by_id["F07_OLD_SHA_VALIDATION_NOT_SUCCESSOR_PASS"]["prohibited_conclusion_ref"], "PASS@successor-exact-SHA")
        self.assertEqual(by_id["F08_SANDBOX_PASS_NOT_REAL_ENV_PASS"]["prohibited_conclusion_ref"], "PASS@unexecuted-real-environment-tuple")
        mutant = deepcopy(self.manifest)
        mutant["semantic_authorities"]["snapshot_transfer_allowed"] = True
        self.expect_rejected(mutant)
        mutant = deepcopy(self.manifest)
        mutant["semantic_authorities"]["entries"][0]["transferable_pass"] = True
        self.expect_rejected(mutant)

    # ------------------------------------------------------------------
    # R10 / N11: provider/model/tool/runtime availability never becomes authority.
    # ------------------------------------------------------------------
    def test_r10_n11_availability_facts_never_become_authority(self) -> None:
        self.assertEqual(required_negative_errors(self.registry), [])  # F06 exact
        dimension_ids = {d["dimension_id"] for d in self.registry["dimensions"]}
        for forbidden in ("model_availability", "provider_availability", "runtime_availability"):
            self.assertNotIn(forbidden, dimension_ids)
        surfaces = json.dumps(self.manifest["semantic_authorities"]) + json.dumps(self.registry)
        self.assertNotIn("availability_authority", surfaces)
        self.assertNotIn("model_grants_authority", surfaces)
        resolved = resolve_registry(self.manifest, self.entry_schema)
        self.assertNotIn("execution.model_authority", resolved)

    # ------------------------------------------------------------------
    # R11 / N12: single discovery surface; no second table/resolver; no lifecycle.
    # ------------------------------------------------------------------
    def test_r11_n12_no_second_discovery_table_or_workflow_lifecycle(self) -> None:
        registry_files = sorted(p.name for p in (ROOT / "registries").glob("*.json"))
        self.assertEqual(registry_files, ["state-dimensions-v1.json"])
        self.assertEqual(
            sorted(self.manifest["sections"]),
            sorted([
                "authority", "normative_standards", "compatibility_entries", "templates",
                "checklists", "prompts", "machine_contracts", "profiles", "references",
                "verification", "discovery_standards", "registries",
            ]),
        )
        envelope = self.manifest["semantic_authorities"]
        self.assertEqual(set(envelope), {"schema_version", "entries"})
        self.assertEqual(envelope["schema_version"], 1)
        self.assertNotIn("semantic_registries", self.manifest["sections"])
        self.assertEqual(required_negative_errors(self.registry), [])
        dimension_ids = {d["dimension_id"] for d in self.registry["dimensions"]}
        self.assertFalse(dimension_ids & CANONICAL_STATES)

    # ------------------------------------------------------------------
    # N13: v4.8 registry/adoption metadata is never a semantic authority.
    # ------------------------------------------------------------------
    def test_n13_v48_adoption_metadata_is_not_a_semantic_authority(self) -> None:
        adoption_reference = "references/V48_REGISTRY_ADOPTION_REFERENCE.md"
        self.assertIn(adoption_reference, self.manifest["sections"]["references"])
        self.assertNotIn(adoption_reference, self.manifest["sections"]["normative_standards"])
        for entry in self.entries:
            self.assertNotEqual(entry["canonical_owner_ref"], adoption_reference)
            self.assertNotIn("v48", entry["semantic_concern"])
        self.assertNotIn("v48", json.dumps(self.registry))

    # ------------------------------------------------------------------
    # Reference docs: descriptive-only v4.9 sections resolve and stay bounded.
    # ------------------------------------------------------------------
    def test_reference_docs_document_v49_additions_without_granting_authority(self) -> None:
        self.assertIn("v49-semantic-authority-entries", markdown_anchors(self.authority_reference))
        self.assertIn("v49-dimensions-and-forbidden-inferences", markdown_anchors(self.state_reference))
        for entry_id, _, _, _ in V49_SEMANTIC_ENTRIES:
            self.assertIn(entry_id, self.authority_reference)
        for rule_id in ("F11", "F12", "F13", "F14", "F15", "F16", "F17", "F18", "F19"):
            self.assertIn(rule_id, self.state_reference)
        self.assertIn("authority effect is none", self.state_reference)
        self.assertNotIn("BLOCKED until", self.state_reference)
        for _, _, owner, _ in V49_SEMANTIC_ENTRIES:
            self.assertTrue((ROOT / owner).is_file(), owner)


if __name__ == "__main__":
    unittest.main()
