"""v4.8 T-014 integrated convergence / version-closure INPUTS conformance.

Deterministic, offline, self-contained integrated oracle over the exact
integrated v4.8 baseline. It implements acceptance oracles C01-C10 of the
frozen T-014 Execution Pack (`.agent/execution/T-014/TEST_MATRIX.yaml`):

  C01 exactly three new v4.8 machine-contract families, identified from the
      Frozen L2/Product (L2 blob f88c85454e80101a0fdf56050e21f11a05279841
      section 4; Frozen Product blob f26439580e00de6ed8b2e27d732a3095eb566219
      section 3), never inferred from test-file counts alone; the count
      assertion fails on any other count;
  C02 Interchange owner reused exactly once, not duplicated;
  C03 owner uniqueness across v4.1-v4.8 inherited inventories;
  C04 hard eligibility-before-ranking on the integrated execution surfaces;
  C05 composite work+resource admission atomicity;
  C06 historical compatibility and Fast Path surfaces valid and present;
  C07 dogfood claims bounded to evidence strength (NOT_MEASURED preserved);
  C08 INTEGRATED_REGRESSION_EVIDENCE.json structure and pinned coverage;
  C09 closure inputs issue no closure/release verdict;
  C10 every carry-forward / NOT_RUN|BLOCKED item carries an exact ref+routing.

This test produces closure INPUTS only. It is not independent Validation,
Fresh Review, Version Closure or Release Qualification; those verdicts remain
with the later closure gates. It never repairs owner semantics.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
import unittest

from test_protocol_schemas import load_schema, validate_subset

ROOT = Path(__file__).resolve().parents[1]

# Exact integrated baseline this candidate is bound to (T-014 MANIFEST.yaml).
V48_BASE_SHA = "6bfb8aecd4c7e533ae4f392dc4e58de1da71d5b4"
V48_BASE_TREE = "593dd5d12890f68e3830419b07b909ccf587dc2b"

EXECUTION_ARCHITECTURE = ROOT / "standards" / "EXECUTION_ARCHITECTURE_STANDARD.md"
L2 = ROOT / "docs" / "implementation" / "4.8.0" / "L2_ARCHITECTURE_EVIDENCE.md"
PRD = ROOT / "docs" / "implementation" / "4.8.0" / "PRD.md"
REGISTRY_ADOPTION = ROOT / "references" / "V48_REGISTRY_ADOPTION_REFERENCE.md"
INTERCHANGE_COMPAT = ROOT / "references" / "V48_INTERCHANGE_PROFILE_COMPATIBILITY.md"
MANIFEST = ROOT / "standard-manifest.json"
CLOSURE_DIR = ROOT / "docs" / "implementation" / "4.8.0" / "closure"
CLOSURE_INPUTS = CLOSURE_DIR / "CLOSURE_INPUTS.md"
REGRESSION_EVIDENCE = CLOSURE_DIR / "INTEGRATED_REGRESSION_EVIDENCE.json"
WORKFLOW = ROOT / ".github" / "workflows" / "verify-standard.yml"

# C01 fixture — the exactly-three new v4.8 default machine-contract families.
# Identity is derived from the Frozen authorities, not from test-file counts:
#   - Frozen L2 section 4: "v4.8 introduces exactly three new default
#     machine-contract families" with candidate files 4.1/4.2/4.3;
#   - Frozen Product section 3 concerns 1/2/5 materialized as machine
#     contracts (Task Learning Evidence; Agent Capability Evidence &
#     Eligibility; evolution feedback stays governance-only, no family);
#   - references/V48_REGISTRY_ADOPTION_REFERENCE.md: MACHINE_FAMILY_TARGET=EXACTLY_3.
THREE_NEW_V48_FAMILIES = {
    "schemas/task-learning-v1.schema.json": {
        "schema_version": "ai-dev/task-learning-v1",
        "semantic_concern": "execution.task_learning_evidence",
        "entry_id": "task-learning-evidence",
        "owner": "standards/EXECUTION_ARCHITECTURE_STANDARD.md",
        "l2_ref": "docs/implementation/4.8.0/L2_ARCHITECTURE_EVIDENCE.md@f88c85454e80101a0fdf56050e21f11a05279841 section 4.1",
    },
    "schemas/agent-capability-profile-v1.schema.json": {
        "schema_version": "ai-dev/agent-capability-profile-v1",
        "semantic_concern": "execution.logical_agent_capability_claim",
        "entry_id": "logical-agent-capability-profile",
        "owner": "standards/EXECUTION_ARCHITECTURE_STANDARD.md",
        "l2_ref": "docs/implementation/4.8.0/L2_ARCHITECTURE_EVIDENCE.md@f88c85454e80101a0fdf56050e21f11a05279841 section 4.2",
    },
    "schemas/agent-capability-evidence-v1.schema.json": {
        "schema_version": "ai-dev/agent-capability-evidence-v1",
        "semantic_concern": "execution.agent_capability_evidence",
        "entry_id": "agent-capability-evidence",
        "owner": "standards/EXECUTION_ARCHITECTURE_STANDARD.md",
        "l2_ref": "docs/implementation/4.8.0/L2_ARCHITECTURE_EVIDENCE.md@f88c85454e80101a0fdf56050e21f11a05279841 section 4.3",
    },
}

# C01/C03 fixture — pre-v4.8 machine-contract inventory carried by the
# v4.1-v4.7 owners at the Frozen L2 planning baseline (main@e75fe834469c5ea9
# f9a384f7d84e38c3a48afa46); registered unchanged in the preserved v4.7
# discovery layer (references/V48_REGISTRY_ADOPTION_REFERENCE.md section 5).
PRE_V48_MACHINE_CONTRACTS = frozenset({
    "schemas/agent-event-v2.schema.json",
    "schemas/assurance-plan-v1.schema.json",
    "schemas/authority-applicability-entry-v1.schema.json",
    "schemas/dispatch.schema.json",
    "schemas/execution-pack-manifest.schema.json",
    "schemas/execution-state.schema.json",
    "schemas/interchange-envelope-v1.schema.json",
    "schemas/local-agent-handoff.schema.json",
    "schemas/operation-binding-v1.schema.json",
    "schemas/operation-v1.schema.json",
    "schemas/repository-integration-v4-precondition.schema.json",
    "schemas/review-aggregation-v1.schema.json",
    "schemas/review-finding-v1.schema.json",
    "schemas/state-dimension-registry-v1.schema.json",
    "schemas/task-contract.schema.json",
    "schemas/validation-report.schema.json",
})

# Sequential-integration composition predecessor machine contracts
# (standard-manifest.json "machine_contracts" at COMPOSITION_BASE_MAIN
# f62930bd3512a463358b8b642b1bbc5993566940). Composition authorization
# #787@5981213563 (rule 5: union of both sides' registrations) authorizes the
# composed manifest to carry these v4.1/v4.2/v4.3-sequential contracts alongside
# the v4.8 candidate inventory. They are predecessor registrations, NOT new v4.8
# families: the exactly-three partition below keeps its full force because any
# path outside pre-v4.8 inventory | predecessor contracts | the three v4.8
# families still fails, as does dropping any of them.
PREDECESSOR_COMPOSITION_MACHINE_CONTRACTS = frozenset({
    "schemas/compatibility-record-v1.schema.json",
    "schemas/dag-mutation-record-v1.schema.json",
    "schemas/dependency-risk-exception-v1.schema.json",
    "schemas/dependency-toolchain-profile-v1.schema.json",
    "schemas/execution-context-v1.schema.json",
    "schemas/migration-transition-v1.schema.json",
})

# F2 RE-BIND (T-012, authorized pin-constants-only change; disclosure
# #730@5998009516, MANIFEST controller_authorizations[1]): the post-T-011
# integrated manifest legally carries the merged v4.9 machine contracts over
# the v4.8-composed inventory (exactly three, registered by the merged T-002 /
# T-004 / T-006 owner outputs at version/v4.9.0@d53e943e). The C01 inventory
# pin is re-bound to the post-T-011 inventory; the exactly-three v4.8
# partition below keeps its full strength — any fourth new family, dropped
# family, rename, or silent v4.9 mutation still fails. Zero assertion-logic
# change.
V49_MERGED_MACHINE_CONTRACTS = frozenset({
    "schemas/assurance-plan-v2.schema.json",
    "schemas/role-execution-profile-v1.schema.json",
    "schemas/task-learning-v2.schema.json",
})

# C03 fixture — inherited v4.1-v4.7 semantic concern -> canonical owner map.
# Concerns and owners are inherited unchanged into v4.8; re-owning any of
# them, or introducing a second owner for any concern, is an integration
# defect (TEST_MATRIX C03; V48_REGISTRY_ADOPTION_REFERENCE.md section 6).
INHERITED_CONCERN_OWNERS = {
    "development-lifecycle": (
        "development.lifecycle_and_task_stage",
        "standards/DEVELOPMENT_WORKFLOW.md",
    ),
    "github-agent-coordination": (
        "github.issue_pr_event_coordination",
        "standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md",
    ),
    "execution-state": (
        "execution.controller_and_dispatch_state",
        "standards/EXECUTION_ARCHITECTURE_STANDARD.md",
    ),
    "work-item-contract": (
        "github.work_item_contract",
        "standards/GITHUB_WORK_ITEM_CONTRACT_STANDARD.md",
    ),
    "validation-evidence": (
        "validation.concern_evidence_and_exact_subject",
        "standards/VALIDATION_STANDARD.md",
    ),
    "release-qualification": (
        "release.qualification_and_candidate_gate",
        "standards/RELEASE_STANDARD.md",
    ),
    "runner-capability": (
        "ci.runner_capability_adoption",
        "standards/CI_RUNNER_CAPABILITY_STANDARD.md",
    ),
    "research-demo": (
        "architecture.research_demo",
        "standards/ARCHITECTURE_RESEARCH_DEMO_STANDARD.md",
    ),
}

# C06 fixture — historical dispatch required set; v4.8 must not add required
# fields (L2 section 10: "Historical Dispatch payloads remain valid").
HISTORICAL_DISPATCH_REQUIRED = [
    "dispatch_id",
    "repository",
    "version",
    "task",
    "role",
    "execution_profile",
    "branch",
    "expected_base_sha",
    "pinned_standard_revision",
    "agent_freedom",
    "dispatch_state",
]

# C06 fixture — minimal historical agent-event-v2 claim (pre-v4.8 shape).
HISTORICAL_EVENT_V2_CLAIM = {
    "schema": "ai-dev/event-v2",
    "event": "DISPATCH_CLAIMED",
    "actor_role": "builder",
    "operator_kind": "chatgpt-web",
    "operator_id": "chatgpt-web:legacy-operator",
    "dispatch_id": "d-legacy-0001",
    "dispatch_state": "CLAIMED",
    "sha": "0123456789abcdef0123456789abcdef01234567",
}

# C06 fixture — minimal historical interchange-envelope-v1 handoff.
HISTORICAL_INTERCHANGE_HANDOFF = {
    "protocol_version": "ai-dev/interchange-v1",
    "exchange_id": "exchange:legacy:0001",
    "exchange_type": "HANDOFF",
    "operation_id": "legacy-op-0001",
    "work_item_ref": "github:kaicreator-mm/ai-development-standard#0",
    "subject_ref": "github:kaicreator-mm/ai-development-standard/pull/0",
    "subject_identity_ref": "git:kaicreator-mm/ai-development-standard@0123456789abcdef0123456789abcdef01234567",
    "identity_binding": "exact-sha",
    "authority_effect": "CORRELATION_ONLY_NON_AUTHORITATIVE",
    "actor": {
        "actor_role": "builder",
        "operator_kind": "chatgpt-web",
        "operator_id": "legacy-operator",
    },
    "causation": {
        "caused_by": "github:kaicreator-mm/ai-development-standard#0",
        "correlation_refs": [],
    },
    "occurred_at": "2026-01-01T00:00:00Z",
}

# C09 fixture — verdict-assignment patterns that must never appear in the
# closure inputs. Prose mentions of the words "closure"/"release" in
# boundary statements are fine; machine-verdict assignments are not.
FORBIDDEN_VERDICT_PATTERNS = (
    "VERSION_CLOSURE=PASS",
    "VERSION_CLOSURE_RESULT=PASS",
    "CLOSURE_VERDICT=PASS",
    "CLOSURE_VERDICT_ISSUED=YES",
    "CLOSURE=APPROVED",
    "CLOSURE_APPROVED",
    "RELEASE_QUALIFICATION=PASS",
    "RELEASE_QUALIFICATION_RESULT=PASS",
    "RELEASE_QUALIFICATION_VERDICT_ISSUED=YES",
    "RELEASE_QUALIFIED=YES",
    "RELEASE_AUTHORIZED=YES",
    "RELEASE_VERDICT=PASS",
    "TAG_AUTHORIZED=YES",
    "MAIN_INTEGRATION=AUTHORIZED",
    "INTEGRATION_VERDICT=PASS",
    "HIDDEN_VALIDATION=PASS",
)

REF_PATTERN = re.compile(r"(#\d+@\d+|#\d+|[0-9a-f]{40})")

# F2 RE-BIND (T-012, authorized pin-constants-only change; disclosure
# #730@5998009516, MANIFEST controller_authorizations[1]): INTEGRATED_-
# REGRESSION_EVIDENCE.json is a frozen v4.8 closure-INPUTS artifact bound to
# its own v4.8 baseline; after T-011 the workflow legally carries the merged
# v4.9 battery and after T-012 the appended conformance command, so the C08
# workflow pin is re-bound two ways with exact-set strength preserved on BOTH
# sides: (1) the evidence must still cover the exact v4.8 baseline workflow
# command set it was generated against; (2) the CURRENT workflow command set
# is pinned exactly (baseline + merged post-baseline additions + the T-012
# append) — any removal, reorder of vocabulary, or unlisted addition fails.
# Zero assertion-logic change otherwise.
V48_BASELINE_WORKFLOW_COMMANDS = (
    "python scripts/verify_standard.py",
    "python scripts/test_verify_standard.py",
    "python scripts/test_verify_project_standard.py",
    "python scripts/test_project_execution_profile.py",
    "python scripts/test_protocol_schemas.py",
    "python scripts/test_v33_lifecycle_contracts.py",
    "python scripts/test_v33_semantic_regressions.py",
    "python scripts/test_v34_lifecycle_contracts.py",
    "python scripts/test_v34_review_repairs.py",
    "python scripts/test_v40_operation_contracts.py",
    "python scripts/test_v40_adoption_migration.py",
    "python scripts/test_v40_final_hardening.py",
    "python scripts/test_v40_dogfood_hardening.py",
    "python scripts/test_v40_r2_machine_hardening.py",
    "python scripts/test_v40_r3_carryforward.py",
    "python scripts/test_v40_t010_successor_hardening.py",
    "python scripts/test_v40_t010_canonical_surface.py",
    "python scripts/test_v40_t012_pre_release_hardening.py",
    "python scripts/test_v40_reference_flows.py",
    "python scripts/test_pointer_only_trigger_contract.py",
    "python scripts/test_work_item_contract_and_golden_templates.py",
    "python scripts/test_task_dag_lane_parallelism.py",
    "python scripts/verify_event_writer_surfaces.py",
    "python scripts/test_execution_architecture.py",
    "python scripts/verify_runner_capability_reference.py",
)

CURRENT_WORKFLOW_COMMANDS = V48_BASELINE_WORKFLOW_COMMANDS + (
    "python scripts/test_v43_conformance_dogfood.py",
    "python scripts/test_v49_execution_core.py",
    "python scripts/test_v49_authority_state_registry.py",
    "python scripts/test_v49_role_execution_profile.py",
    "python scripts/test_v49_task_learning_v2.py",
    "python scripts/test_v49_gate_currentness.py",
    "python scripts/test_v49_execution_contract_refs.py",
    "python scripts/test_v49_jit_dag_governance.py",
    "python scripts/test_v49_assurance_plan_v2.py",
    "python scripts/test_v49_assurance_owner.py",
    "python scripts/test_v49_release_applicability.py",
    "python scripts/test_v49_conformance_suite.py",
)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_manifest() -> dict:
    return json.loads(read(MANIFEST))


def pinned_workflow_commands() -> list[str]:
    """Every pinned `run:` command of .github/workflows/verify-standard.yml."""
    commands = []
    for line in read(WORKFLOW).splitlines():
        stripped = line.strip()
        match = re.fullmatch(r"- run: (.+)", stripped)
        if match:
            commands.append(match.group(1).strip())
    return commands


# --- C04 behavioral helper: hard eligibility strictly before ranking --------

def resolve_eligibility(predicates: dict[str, bool | None]) -> str:
    """Tri-state hard-filter oracle per EXECUTION_ARCHITECTURE_STANDARD 27.2.

    A known failed predicate is INELIGIBLE; a missing/unknown material fact
    (None) fails closed as UNKNOWN; only all-True yields ELIGIBLE.
    """
    values = tuple(predicates.values())
    if any(value is False for value in values):
        return "INELIGIBLE"
    if any(value is None for value in values):
        return "UNKNOWN"
    return "ELIGIBLE"


def rank_eligible_only(candidates: list[tuple[dict[str, bool | None], int]]) -> list[int]:
    """Optional ranking sees ELIGIBLE candidates only, ordered by rank."""
    eligible = [
        (rank, index)
        for index, (predicates, rank) in enumerate(candidates)
        if resolve_eligibility(predicates) == "ELIGIBLE"
    ]
    return [index for _rank, index in sorted(eligible)]


# --- C05 behavioral helper: composite all-or-none admission -----------------

FORBIDDEN_PARTIAL_STATES = (
    "work claim accepted + any required resource missing",
    "resource bound + corresponding work claim not accepted",
    "only a subset of required resources accepted",
    "capacity-N active accepted bindings exceeding N",
)


class CompositeAdmissionState:
    """Minimal SINGLE_WRITER_ADMISSION model over the protected set A.

    A = {work_claim_key} + every required (resource_group, units). The whole
    set linearizes all-or-none at one point (EXECUTION_ARCHITECTURE_STANDARD
    section 27.3); no partial canonical state is ever published.
    """

    def __init__(
        self,
        capacity: dict[str, int],
        claims: frozenset[str] = frozenset(),
        bindings: tuple[tuple[str, str, int], ...] = (),
    ) -> None:
        self.capacity = dict(capacity)
        self.claims = claims
        self.bindings = bindings

    def active_units(self, resource_group: str) -> int:
        return sum(units for group, _claim, units in self.bindings if group == resource_group)

    def admit(self, claim_key: str, required: dict[str, int]) -> tuple[str, "CompositeAdmissionState"]:
        if claim_key in self.claims:
            return "DUPLICATE_CLAIM", self
        # One critical section: evaluate the full protected set first.
        for group, units in required.items():
            if group not in self.capacity:
                return "UNKNOWN_RESOURCE_GROUP", self
            if self.active_units(group) + units > self.capacity[group]:
                return "CAPACITY_EXCEEDED", self
        # All-or-none publication: claim and every binding commit together.
        bindings = self.bindings + tuple(
            (group, claim_key, units) for group, units in sorted(required.items())
        )
        return "ACCEPTED", CompositeAdmissionState(
            capacity=self.capacity,
            claims=self.claims | {claim_key},
            bindings=bindings,
        )


# --- C07 dogfood evidence surfaces ------------------------------------------

DOGFOOD_469_RESULT = ROOT / "docs" / "implementation" / "4.8.0" / "dogfood" / "469" / "RESULT.md"
DOGFOOD_469_MATRIX = ROOT / "docs" / "implementation" / "4.8.0" / "dogfood" / "469" / "EVIDENCE_MATRIX.md"
DOGFOOD_EVOLUTION_MATRIX = ROOT / "docs" / "implementation" / "4.8.0" / "dogfood" / "evolution" / "EVIDENCE_MATRIX.json"
DOGFOOD_ORCHESTRATION_REPORT = ROOT / "docs" / "implementation" / "4.8.0" / "dogfood" / "orchestration" / "RESULT_REPORT.md"

UNSUPPORTED_CLAIM_PATTERNS = (
    "ECONOMIC_SAVINGS=MEASURED",
    "ECONOMIC_SAVINGS=PROVEN",
    "ECONOMIC_SAVINGS=OBSERVED",
    "ECONOMIC_SAVINGS=POSITIVE",
    "BLANKET_STRONG_TO_LOW_COST_RULE=SUPPORTED",
    "UNIVERSAL_ROUTING=SUPPORTED",
    "savings demonstrated",
    "savings proven",
    "proves economic",
)


class V48IntegrationClosureInputs(unittest.TestCase):
    """Integrated acceptance oracles C01-C10 (T-014 TEST_MATRIX.yaml)."""

    # ---- C01 --------------------------------------------------------------

    def test_c01_exactly_three_new_v48_machine_families(self) -> None:
        """C01: count and identities come from Frozen L2/Product, not test counts."""
        manifest = load_manifest()
        registered = manifest["sections"]["machine_contracts"]
        # F2 RE-BIND (T-012, pin constants only; provenance at
        # V49_MERGED_MACHINE_CONTRACTS above): the inventory-size pin is
        # re-bound to the post-T-011 inventory (v4.8 composed inventory plus
        # the three merged v4.9 machine contracts).
        self.assertEqual(
            19 + len(PREDECESSOR_COMPOSITION_MACHINE_CONTRACTS) + len(V49_MERGED_MACHINE_CONTRACTS),
            len(registered),
            "machine-contract inventory size drifted; re-derive the family count from Frozen L2",
        )
        self.assertEqual([], [path for path in registered if registered.count(path) != 1])
        registered_set = set(registered)
        new_family_paths = set(THREE_NEW_V48_FAMILIES)
        # The set algebra fails on ANY other new-family count: a fourth new
        # family, a dropped family or a rename all break the exact partition.
        self.assertEqual(
            frozenset(registered_set - new_family_paths),
            PRE_V48_MACHINE_CONTRACTS
            | PREDECESSOR_COMPOSITION_MACHINE_CONTRACTS
            | V49_MERGED_MACHINE_CONTRACTS,
            "registered machine contracts outside the three v4.8 families must equal the pre-v4.8 inventory plus the composed predecessor inventory plus the three merged v4.9 contracts",
        )
        self.assertEqual(
            3,
            len(registered_set & new_family_paths),
            "exactly three new v4.8 machine-contract families are authorized (Frozen L2 section 4)",
        )
        self.assertEqual(
            new_family_paths,
            registered_set & new_family_paths,
            "the three registered v4.8 families must be exactly the Frozen-L2-identified ones",
        )
        # Each family identity is pinned: file, schema_version const, registry
        # entry, canonical owner.
        entries = {
            entry["entry_id"]: entry
            for entry in manifest["semantic_authorities"]["entries"]
        }
        for path, identity in THREE_NEW_V48_FAMILIES.items():
            schema = load_schema(Path(path).name)
            self.assertEqual(identity["schema_version"], schema["properties"]["schema_version"]["const"], path)
            self.assertIn(path, registered)
            entry = entries.get(identity["entry_id"])
            self.assertIsNotNone(entry, path)
            self.assertEqual(identity["semantic_concern"], entry["semantic_concern"])
            self.assertEqual(identity["owner"], entry["canonical_owner_ref"])
            self.assertTrue((ROOT / path).is_file(), path)
        # Frozen-authority anchors: the count statement itself, per family.
        l2_text = read(L2)
        self.assertIn("v4.8 introduces exactly **three new default machine-contract families**", l2_text)
        for path in THREE_NEW_V48_FAMILIES:
            self.assertIn(f"Candidate file: `{path}`", l2_text)
        adoption_text = read(REGISTRY_ADOPTION)
        self.assertIn("MACHINE_FAMILY_TARGET=EXACTLY_3", adoption_text)
        for path in THREE_NEW_V48_FAMILIES:
            self.assertIn(f"`{path}`", adoption_text)
        # Negative: Availability is a derived view, never a fourth family.
        self.assertFalse(
            any("availability" in path for path in registered),
            "no Availability machine family may exist (L2 UNKNOWN U2 / section 6)",
        )
        self.assertFalse(list((ROOT / "schemas").glob("*availability*")))

    # ---- C02 --------------------------------------------------------------

    def test_c02_interchange_owner_reused_exactly_once(self) -> None:
        """C02: the existing Interchange v1 family is reused, never duplicated."""
        manifest_text = read(MANIFEST)
        manifest = load_manifest()
        self.assertEqual(
            1,
            manifest_text.count("schemas/interchange-envelope-v1.schema.json"),
            "Interchange v1 must be registered exactly once in the manifest",
        )
        self.assertIn("schemas/interchange-envelope-v1.schema.json", manifest["sections"]["machine_contracts"])
        # Single canonical envelope surface; no v2 envelope, no parallel family.
        envelope_files = sorted(path.name for path in (ROOT / "schemas").glob("*interchange*"))
        self.assertEqual(["interchange-envelope-v1.schema.json"], envelope_files)
        self.assertFalse(list(ROOT.rglob("AGENT_EXCHANGE_BINDING_STANDARD.md")))
        self.assertTrue((ROOT / "docs" / "implementation" / "4.0.0" / "AGENT_INTERCHANGE.md").is_file())
        envelope = load_schema("interchange-envelope-v1.schema.json")
        self.assertEqual("ai-dev/interchange-v1", envelope["properties"]["protocol_version"]["const"])
        self.assertEqual("CORRELATION_ONLY_NON_AUTHORITATIVE", envelope["properties"]["authority_effect"]["const"])
        self.assertFalse(envelope["additionalProperties"], "envelope stays closed against ad-hoc authority fields")
        # Reuse dispositions are recorded on the integrated surfaces.
        adoption_text = read(REGISTRY_ADOPTION)
        self.assertIn("INTERCHANGE_POLICY=REUSE_EXISTING_V1_EXACTLY_ONCE", adoption_text)
        self.assertIn("No v2 envelope, second interchange owner or parallel exchange family is created", adoption_text)
        compat_text = read(INTERCHANGE_COMPAT)
        for anchor in (
            "NO_CHANGE_REQUIRED",
            "NEW_EXCHANGE_FAMILY=FORBIDDEN",
            "EVENT_V3=NOT_REQUIRED",
            "T015_PROFILE_OWNER=REFERENCED_NOT_COPIED",
        ):
            self.assertIn(anchor, compat_text)
        l2_text = read(L2)
        self.assertIn("no new Agent Exchange Envelope family and no new `AGENT_EXCHANGE_BINDING_STANDARD.md`", l2_text)

    # ---- C03 --------------------------------------------------------------

    def test_c03_owner_uniqueness_across_v4_1_to_v4_8(self) -> None:
        """C03: no semantic concern has two canonical owners; inheritance unchanged."""
        manifest = load_manifest()
        entries = manifest["semantic_authorities"]["entries"]
        entry_ids = [entry["entry_id"] for entry in entries]
        concerns = [entry["semantic_concern"] for entry in entries]
        self.assertEqual(len(entry_ids), len(set(entry_ids)), "duplicate entry_id in semantic_authorities")
        self.assertEqual(len(concerns), len(set(concerns)), "duplicate semantic_concern in semantic_authorities")
        for entry in entries:
            owner = entry["canonical_owner_ref"]
            self.assertTrue((ROOT / owner).is_file(), f"canonical owner missing on disk: {owner}")
            for alias in entry.get("compatibility_alias_refs") or []:
                self.assertTrue((ROOT / alias).is_file(), f"compatibility alias missing on disk: {alias}")
        # Inherited v4.1-v4.7 concerns keep their exact inherited owner.
        by_id = {entry["entry_id"]: entry for entry in entries}
        for entry_id, (concern, owner) in INHERITED_CONCERN_OWNERS.items():
            entry = by_id[entry_id]
            self.assertEqual(concern, entry["semantic_concern"], entry_id)
            self.assertEqual(owner, entry["canonical_owner_ref"], entry_id)
        # Each new v4.8 concern has exactly one canonical owner and does not
        # re-own or shadow any inherited concern.
        for identity in THREE_NEW_V48_FAMILIES.values():
            entry = by_id[identity["entry_id"]]
            self.assertEqual(identity["semantic_concern"], entry["semantic_concern"])
            self.assertEqual(identity["owner"], entry["canonical_owner_ref"])
            self.assertIn(identity["semantic_concern"], concerns)
        # State-dimension registry: one owner per dimension, uniqueness holds,
        # and Availability stays absent from the durable registry.
        state_registry = json.loads(read(ROOT / "registries" / "state-dimensions-v1.json"))
        dimension_ids = [dimension["dimension_id"] for dimension in state_registry["dimensions"]]
        self.assertEqual(len(dimension_ids), len(set(dimension_ids)), "duplicate state dimension_id")
        for dimension in state_registry["dimensions"]:
            owner_ref = dimension["canonical_owner_ref"]
            # Owner refs are repo-relative paths or exact-subject pinned refs
            # of the form github:<owner>/<repo>@<40-hex>:<path> (e.g.
            # deployment_result, runtime_health, pinned at their frozen
            # upstream subject). Local owners must exist in this tree;
            # pinned upstream owners must be structurally immutable.
            if owner_ref.startswith("standards/"):
                self.assertTrue((ROOT / owner_ref).is_file(), dimension["dimension_id"])
            else:
                self.assertRegex(
                    owner_ref,
                    r"^github:kaicreator-mm/ai-development-standard@[0-9a-f]{40}:[A-Za-z0-9_./-]+$",
                    dimension["dimension_id"],
                )
        self.assertNotIn("availability", dimension_ids)
        self.assertIn("forbidden_inferences", state_registry)

    # ---- C04 --------------------------------------------------------------

    def test_c04_hard_eligibility_precedes_ranking(self) -> None:
        """C04: ranking sees ELIGIBLE only and can never promote INELIGIBLE/UNKNOWN."""
        architecture = read(EXECUTION_ARCHITECTURE)
        for anchor in (
            "### 27.2 Hard filters before ranking",
            "ELIGIBLE\nINELIGIBLE\nUNKNOWN",
            "**All hard predicates are evaluated before ranking.**",
            "Only `ELIGIBLE` choices may enter optional ranking.",
            "MUST NOT promote `INELIGIBLE` or `UNKNOWN` to `ELIGIBLE`",
        ):
            self.assertIn(anchor, architecture)
        l2_text = read(L2)
        for anchor in (
            "Hard eligibility precedes optimization; ranking cannot make an ineligible or unknown choice eligible.",
            "Only ELIGIBLE candidates enter optional ranking.",
            "Ranking cannot change INELIGIBLE/UNKNOWN to ELIGIBLE.",
        ):
            self.assertIn(anchor, l2_text)
        prd_text = read(PRD)
        self.assertIn("No cost/latency/priority rule may make an ineligible executor eligible.", prd_text)
        # Behavioral identity: a top-ranked candidate with any failed or
        # unknown hard predicate never enters the ranked feasible set.
        fully_eligible = {
            "ready": True, "current": True, "capability": True, "resources": True,
            "security": True, "independence": True, "write_set": True, "composite": True,
        }
        ineligible_but_attractive = {**fully_eligible, "independence": False}
        unknown_capability = {**fully_eligible, "capability": None}
        ranked = rank_eligible_only([
            (ineligible_but_attractive, 0),  # best rank, must be excluded
            (unknown_capability, 1),         # second rank, must be excluded
            (fully_eligible, 9),             # worst rank, only feasible choice
        ])
        self.assertEqual([2], ranked)
        self.assertEqual("INELIGIBLE", resolve_eligibility(ineligible_but_attractive))
        self.assertEqual("UNKNOWN", resolve_eligibility(unknown_capability))
        self.assertEqual("ELIGIBLE", resolve_eligibility(fully_eligible))

    # ---- C05 --------------------------------------------------------------

    def test_c05_composite_resource_admission_is_atomic(self) -> None:
        """C05: claim + every required resource linearizes all-or-none."""
        architecture = read(EXECUTION_ARCHITECTURE)
        for anchor in (
            "### 27.3 One all-or-none linearization point for claim plus required resources",
            "MUST linearize all-or-none at one admission point",
            "Independent per-key CAS operations, per-resource leases, or a sequence of individually successful reservations are **not** composite proof",
            "sum(active accepted units bound to G) <= N",
            "Exclusive capacity is `N=1`",
            "### 27.4 Crash/publication ambiguity and replacement admission",
            "MUST NOT guess from transient locks, process memory, queue state, ACK/progress, or individually observed per-key writes",
        ):
            self.assertIn(anchor, architecture)
        for forbidden in FORBIDDEN_PARTIAL_STATES:
            self.assertIn(forbidden, architecture)
        l2_text = read(L2)
        for anchor in (
            "All members of A MUST be admitted through one all-or-none linearization point.",
            "Independent per-key successful writes are insufficient for composite admission.",
            "Capacity-N active accepted bindings MUST never exceed N; exclusive resource is N=1.",
        ):
            self.assertIn(anchor, l2_text)
        # Behavioral identity: failure of any member of A rejects the whole
        # admission and publishes no partial canonical state.
        state = CompositeAdmissionState(capacity={"gpu-build-01": 1, "license-seat": 2})
        decision, admitted = state.admit("claim-a", {"gpu-build-01": 1, "license-seat": 1})
        self.assertEqual("ACCEPTED", decision)
        self.assertIn("claim-a", admitted.claims)
        self.assertEqual(1, admitted.active_units("gpu-build-01"))
        # Capacity exhaustion on the second member rejects the entire set:
        # no claim, and not even a subset binding.
        decision, rejected = admitted.admit("claim-b", {"gpu-build-01": 1, "license-seat": 1})
        self.assertEqual("CAPACITY_EXCEEDED", decision)
        self.assertNotIn("claim-b", rejected.claims)
        self.assertEqual(0, rejected.active_units("license-seat") - admitted.active_units("license-seat"))
        self.assertEqual(
            sum(units for _g, claim, _u in rejected.bindings if claim == "claim-b"),
            0,
            "no partial resource binding may exist for a rejected composite admission",
        )
        self.assertEqual(admitted.bindings, rejected.bindings)
        # Exclusive capacity N=1 races serialize: exactly one winner.
        exclusive = CompositeAdmissionState(capacity={"exclusive-device": 1})
        decision, first = exclusive.admit("claim-1", {"exclusive-device": 1})
        self.assertEqual("ACCEPTED", decision)
        decision, second = first.admit("claim-2", {"exclusive-device": 1})
        self.assertEqual("CAPACITY_EXCEEDED", decision)
        self.assertEqual(first.bindings, second.bindings)
        # Duplicate claim keys cannot double-bind the same capacity.
        decision, duplicate = first.admit("claim-1", {"exclusive-device": 1})
        self.assertEqual("DUPLICATE_CLAIM", decision)
        self.assertEqual(first.bindings, duplicate.bindings)

    # ---- C06 --------------------------------------------------------------

    def test_c06_historical_compatibility_and_fast_path(self) -> None:
        """C06: historical payloads stay valid; Fast Path stays proportional."""
        event_schema = load_schema("agent-event-v2.schema.json")
        self.assertEqual([], validate_subset(HISTORICAL_EVENT_V2_CLAIM, event_schema))
        self.assertIn("DISPATCH_CLAIMED", event_schema["properties"]["event"]["enum"])
        envelope = load_schema("interchange-envelope-v1.schema.json")
        self.assertEqual([], validate_subset(HISTORICAL_INTERCHANGE_HANDOFF, envelope))
        dispatch = load_schema("dispatch.schema.json")
        self.assertEqual(sorted(HISTORICAL_DISPATCH_REQUIRED), sorted(dispatch["required"]))
        # The v4.8 L2 section 10 candidate optional refs never became required.
        for optional_ref in (
            "agent_capability_profile_ref",
            "capability_evidence_refs",
            "runner_or_environment_capability_refs",
            "eligibility_basis_ref",
            "resource_binding_refs",
            "assignment_policy_ref",
        ):
            self.assertNotIn(optional_ref, dispatch["required"])
        l2_text = read(L2)
        self.assertIn(
            "historical Task Packs, Execution Packs, Dispatches, `interchange-envelope-v1`, `ai-dev:event:v2` and Validation/Review payloads remain valid",
            l2_text,
        )
        # Fast Path surfaces remain present and proportional.
        self.assertIn("## 7. 快速路径", read(ROOT / "standards" / "DEVELOPMENT_WORKFLOW.md"))
        adoption_text = read(ROOT / "standards" / "PROJECT_ADOPTION.md")
        self.assertIn("`TASK_LEARNING=NONE_MATERIAL` 是合法完整结果", adoption_text)
        learning_reference = read(ROOT / "references" / "TASK_LEARNING_EVIDENCE_REFERENCE.md")
        self.assertIn("## Fast Path", learning_reference)
        self.assertIn("TASK_LEARNING=NONE_MATERIAL", learning_reference)
        self.assertIn("Do **not** instantiate an empty `task-learning-v1` object", learning_reference)
        adoption_reference = read(REGISTRY_ADOPTION)
        self.assertIn("Fast Path remains lightweight and orthogonal to adoption level", adoption_reference)
        self.assertIn("`TASK_LEARNING=NONE_MATERIAL` is a valid complete outcome", adoption_reference)
        self.assertIn("v4.8 is not successful if it makes trivial maintenance materially harder.", read(PRD))

    # ---- C07 --------------------------------------------------------------

    def test_c07_dogfood_claims_bounded_not_measured_preserved(self) -> None:
        """C07: economics/universal-routing stay NOT_MEASURED/unsupported."""
        result_text = read(DOGFOOD_469_RESULT)
        for anchor in (
            "ECONOMIC_SAVINGS=NOT_MEASURED",
            "BLANKET_STRONG_TO_LOW_COST_RULE=NOT_SUPPORTED",
            "DISPOSITION=MORE_EVIDENCE",
            "STANDARD_CHANGE=NOT_AUTHORIZED",
            "No economic conclusion",
        ):
            self.assertIn(anchor, result_text)
        matrix_text = read(DOGFOOD_469_MATRIX)
        self.assertIn("the only permitted economic conclusion is `ECONOMIC_SAVINGS=NOT_MEASURED`", matrix_text)
        self.assertIn("Missing evidence is never normalized to zero", matrix_text)
        evolution = json.loads(read(DOGFOOD_EVOLUTION_MATRIX))
        boundaries = evolution["claim_boundaries"]
        self.assertEqual("NOT_MEASURED", boundaries["economic_savings"])
        self.assertEqual("NOT_SUPPORTED", boundaries["blanket_strong_to_low_cost_rule"])
        self.assertEqual("PROHIBITED", boundaries["standard_auto_amendment"])
        self.assertFalse(boundaries["public_or_github_visibility_implies_publishable"])
        self.assertFalse(boundaries["external_generalized_claims_authorized"])
        self.assertTrue(evolution["streams"])
        for stream in evolution["streams"]:
            self.assertFalse(stream["external_claim_eligible"], stream["stream_id"])
            self.assertEqual("REAL", stream["evidence_kind"], stream["stream_id"])
            self.assertIn(stream["disposition"], {"MORE_EVIDENCE", "NO_CHANGE"}, stream["stream_id"])
        orchestration_text = read(DOGFOOD_ORCHESTRATION_REPORT)
        for anchor in (
            "no universal Agent ranking",
            "no blanket strong-to-low-cost routing",
            "no savings claim",
        ):
            self.assertIn(anchor, orchestration_text)
        # No merged dogfood evidence converts NOT_MEASURED into a claim.
        for path in (DOGFOOD_469_RESULT, DOGFOOD_469_MATRIX, DOGFOOD_ORCHESTRATION_REPORT):
            text = read(path).lower()
            for pattern in UNSUPPORTED_CLAIM_PATTERNS:
                self.assertNotIn(pattern.lower(), text, f"{path.name}: unsupported claim pattern {pattern!r}")

    # ---- C08 --------------------------------------------------------------

    def test_c08_regression_evidence_covers_pinned_commands(self) -> None:
        """C08: evidence binds the base and every pinned run: command with exits."""
        evidence = json.loads(read(REGRESSION_EVIDENCE))
        self.assertEqual(V48_BASE_SHA, evidence["base_sha"])
        self.assertEqual(V48_BASE_TREE, evidence["base_tree"])
        for field in ("generated_at", "host"):
            self.assertIn(field, evidence)
        for field in ("os", "git_version", "python_version"):
            self.assertIn(field, evidence["host"])
        commands = evidence["commands"]
        self.assertTrue(commands)
        recorded = [row["command"] for row in commands]
        self.assertEqual(len(recorded), len(set(recorded)), "duplicate command row in regression evidence")
        for row in commands:
            self.assertIn("exit", row)
            self.assertIn("summary", row)
            self.assertEqual(0, row["exit"], row["command"])
            self.assertTrue(row["summary"].strip(), row["command"])
        # verify_standard both in -B form and as pinned, plus the focused test.
        self.assertIn("python -B scripts/verify_standard.py", recorded)
        self.assertIn("python scripts/verify_standard.py", recorded)
        self.assertIn("python -B scripts/test_v48_integration_closure.py", recorded)
        # Every pinned `run:` command from the workflow is present verbatim.
        # F2 RE-BIND (T-012; provenance at V48_BASELINE_WORKFLOW_COMMANDS):
        # the frozen v4.8 evidence is pinned against the exact v4.8 baseline
        # workflow command set it was generated against, and the current
        # workflow command set is pinned exactly (post-T-011 battery plus the
        # T-012 conformance append) — exact-set strength preserved on both
        # sides.
        pinned = pinned_workflow_commands()
        self.assertGreaterEqual(len(pinned), 25)
        missing = [
            command for command in V48_BASELINE_WORKFLOW_COMMANDS if command not in recorded
        ]
        self.assertEqual([], missing, f"pinned regression commands missing from evidence: {missing}")
        self.assertEqual(
            sorted(CURRENT_WORKFLOW_COMMANDS),
            sorted(pinned),
            "workflow command set drifted; only an authorized re-bind may move this pin",
        )
        # NOT_RUN rows are honest: only allowed with an exact reason.
        for row in evidence.get("not_run", []):
            self.assertIn("reason", row)
            self.assertTrue(str(row["reason"]).strip())

    # ---- C09 --------------------------------------------------------------

    def test_c09_closure_inputs_issue_no_verdict(self) -> None:
        """C09: closure inputs stay inputs; no closure/release verdict appears."""
        closure_text = read(CLOSURE_INPUTS)
        evidence_text = read(REGRESSION_EVIDENCE)
        for text, name in ((closure_text, CLOSURE_INPUTS.name), (evidence_text, REGRESSION_EVIDENCE.name)):
            for pattern in FORBIDDEN_VERDICT_PATTERNS:
                self.assertNotIn(pattern, text, f"{name} must not contain verdict assignment {pattern!r}")
        for anchor in (
            "closure INPUTS only",
            "CLOSURE_VERDICT_ISSUED=NO",
            "RELEASE_QUALIFICATION_VERDICT_ISSUED=NO",
            "Version Closure verdict authority remains with the later closure gates",
        ):
            self.assertIn(anchor, closure_text)

    # ---- C10 --------------------------------------------------------------

    def test_c10_carry_forwards_and_not_run_items_have_refs_and_routing(self) -> None:
        """C10: every unresolved finding / NOT_RUN|BLOCKED item has ref+routing."""
        closure_text = read(CLOSURE_INPUTS)
        self.assertIn("## 5. Carry-forwards and routed findings", closure_text)
        self.assertIn("P3-01", closure_text)
        self.assertIn("#763@5974751546", closure_text)
        self.assertIn("docs/implementation/4.8.0/dogfood/evolution/", closure_text)
        # The v4.9 analogue stays out of scope for v4.8 closure inputs.
        self.assertIn("#764", closure_text)
        self.assertIn("out of scope", closure_text)
        carry_rows = [
            line
            for line in closure_text.splitlines()
            if line.startswith("| CF-")
        ]
        self.assertTrue(carry_rows, "at least one carry-forward row must be listed")
        for row in carry_rows:
            self.assertLessEqual(len(row.split("|")), 8, f"carry-forward row malformed: {row!r}")
            self.assertTrue(REF_PATTERN.search(row), f"carry-forward row lacks exact ref: {row!r}")
            cells = [cell.strip() for cell in row.split("|")]
            # Row shape: | CF-xx | finding | exact ref | routing |  -> cells[-2] is routing.
            self.assertTrue(cells[-2], f"carry-forward row lacks routing: {row!r}")
        # NOT_RUN / BLOCKED inventory is explicit (sentinel, or rows with refs).
        self.assertIn("## 6. NOT_RUN / BLOCKED items", closure_text)
        self.assertRegex(closure_text, r"NOT_RUN_ITEMS=(NONE|.+)")
        self.assertRegex(closure_text, r"BLOCKED_ITEMS=(NONE|.+)")
        evidence = json.loads(read(REGRESSION_EVIDENCE))
        self.assertIsInstance(evidence.get("not_run", []), list)


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(V48IntegrationClosureInputs)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    raise SystemExit(0 if result.wasSuccessful() else 1)
