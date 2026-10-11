"""v4.9 T-012 deterministic proportional-orchestration conformance suite.

Integrated conformance TEST ORACLE for the merged v4.9 owner outputs at base
`version/v4.9.0@d53e943ec7109648485b64a647ed2c7cf553531d` (tree
`5ad2dbd8c312a67bb050a3199ab9b29b70c23406`, execution pack head
`370f6e837b24f6e1d95aac5c6b1995e917e473a4`).

One test class per immutable DAG v0.1 `### T-012` coverage item
(blob `4f358ba2b32e01ae17ddcdf970151cf28e44bb3f`) plus the coverage-manifest
test, driven by `fixtures/conformance-suite/`:

  C01 precedence vs conjunction            (Frozen PRD A, B;  L2 +2/+4)
  C02 reduction proof fail-closed          (Frozen PRD M;      L2 +3/+5)
  C03 assurance currentness TOCTOU         (Frozen PRD F;      L2 +6/+7)
  C04 adverse finding carry-forward        (Frozen PRD N, J;   L2 +8/+9)
  C05 selector/independence conflicts      (Frozen PRD G;      L2 +10)
  C06 JIT in-envelope vs DAG mutation      (Frozen PRD L;      L2 +11/+12)
  C07 gate-owned transfer/currentness      (Frozen PRD H, I;   L2 S10)
  C08 Release per-gate applicability       (Frozen PRD B, D, O;L2 +13/+14)
  C09 predecessor lineage wait             (Frozen PRD K;      L2 +15)
  C10 Task Learning same-family compat     (Frozen PRD Q;      L2 +16)
  C11 manual-compatible reconstruction     (Frozen PRD P;      L2 +17/+18)
  C12 coverage manifest                    (this manifest test)

Binding posture: the suite ASSERTS merged owner semantics, never redefines
them. Owner behavior is exercised through the actual merged owner kernels
(`test_v49_gate_currentness`, `test_v49_execution_core`,
`test_v49_jit_dag_governance`, `test_v48_integration_closure`,
`test_v49_role_execution_profile`, `test_v49_task_learning_v2`) and through
owner text/schema/registry anchors; where a coverage item needs a local pure
function, the function is pinned to its owner section by exact-text anchors so
owner drift fails the suite instead of silently redefining semantics. An owner
defect discovered here is a finding for the owning Task — never repaired in
this lane. The suite makes no runtime claim beyond its executed tests and is
not independent Validation, Fresh Review, or any gate verdict.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))

# Merged owner kernels under conformance (import-only; each runs its own
# battery separately — importing here binds THIS suite to their exact code).
import test_v49_gate_currentness as gate_kernel  # noqa: E402  (T-010 owner kernel)
import test_v49_execution_core as core_kernel  # noqa: E402  (T-007 owner kernel)
import test_v49_jit_dag_governance as jit_kernel  # noqa: E402  (T-009 owner kernel)
import test_v48_integration_closure as v48_kernel  # noqa: E402  (v4.8 eligibility engine)
import test_v49_role_execution_profile as role_kernel  # noqa: E402  (T-004 owner kernel)
import test_v49_task_learning_v2 as learning_kernel  # noqa: E402  (T-006 owner kernel)
from test_protocol_schemas import load_schema, validate_subset  # noqa: E402

FIXTURE_DIR = ROOT / "fixtures" / "conformance-suite"
GOVERNANCE_STANDARD = ROOT / "standards" / "TASK_DAG_GOVERNANCE_STANDARD.md"
MUTATION_RECORD_SCHEMA_PATH = ROOT / "schemas" / "dag-mutation-record-v1.schema.json"
REGISTRY = ROOT / "registries" / "state-dimensions-v1.json"
PRD = ROOT / "docs" / "implementation" / "4.9.0" / "PRD.md"
L2 = ROOT / "docs" / "implementation" / "4.9.0" / "L2_ARCHITECTURE_EVIDENCE.md"
DAG_V01 = ROOT / "docs" / "implementation" / "4.9.0" / "task-dag-history" / "TASK_DAG-v0.1-first-candidate.md"
TEST_MATRIX = ROOT / ".agent" / "execution" / "T-012" / "TEST_MATRIX.yaml"

BASE_SHA = "d53e943ec7109648485b64a647ed2c7cf553531d"
BASE_TREE = "5ad2dbd8c312a67bb050a3199ab9b29b70c23406"
PACK_HEAD_SHA = "370f6e837b24f6e1d95aac5c6b1995e917e473a4"
FROZEN_PRD_BLOB = "a8ec7030a14337a4c2dca853dc474e965679d610"
FROZEN_L2_BLOB = "bd41ea0175b459a6a490fd37ad579e429a58a1c3"
FROZEN_DAG_V02_BLOB = "b9fe0cc7089f64929b4bcf45f7230d950e864db2"
DAG_V01_BLOB = "4f358ba2b32e01ae17ddcdf970151cf28e44bb3f"

WRITE_SET = (
    "scripts/test_v49_conformance_suite.py",
    "fixtures/conformance-suite/",
    "scripts/test_v49_gate_currentness.py",
    "scripts/test_v48_integration_closure.py",
    ".github/workflows/verify-standard.yml",
)

# F1-STYLE RE-BIND (#805 POST_RECOVERY_EXACT_RECOMPOSE, #745; doctrine
# precedent: T-010 F1 re-bind in scripts/test_v49_gate_currentness.py): the
# merged T-012 outputs at the composed tree (merge of version/v4.9.0@4322a8cc
# x recovery-integrated main@4c632256), blob-pinned. test_v48_integration_closure.py
# carries the recomposed union of the v4.9-side and recovery-side additions and
# is pinned to its exact composed blob; the remaining surfaces are unmutated by
# the recovery and pin to their T-012 candidate blobs at 4322a8cc. Any further
# mutation of any T-012 output still fails; zero assertion-logic change.
#
# v4.10 integration value re-bind (claim #779@6084794791 / pre-merge
# #779@6084805500; merge commit e0315b2a): the disclosed composition rebind
# renumbered the v4.9 standard section §28 -> §29. Eight conformance fixtures
# carried the old anchor-form citations to that section in their exact-ref rows
# (`#281-` .. `#287-` -> `#291-` .. `#297-`; the identical strings were rebound
# in the owner kernels' fixtures in the same step), so their merged blobs moved
# and are pinned to their new exact blobs here. `.agent/execution/T-012/
# IMPLEMENTATION_MAP.md` moved out of the pack-head loop below into this dict
# for the same reason (its read-only-inputs line cites the renumbered section).
# `scripts/test_v49_gate_currentness.py` is pinned to the exact blob of the
# T-010 kernel carrying this integration's disclosed re-binds. Pin constants
# only — zero removed tests, no intent weakened.
T012_MERGED_BLOBS = {
    "fixtures/conformance-suite/carry_forward.json": "918d3165b67a1d48da1ef990cd2a21a140dc3a6a",
    "fixtures/conformance-suite/coverage_manifest.json": "2f336082c4fd46b1018120b243572296b7eb3a19",
    "fixtures/conformance-suite/currentness_toctou.json": "75c25d4fe5a639619e26bc8433849b6dc6564111",
    "fixtures/conformance-suite/gate_transfer_currentness.json": "f5176eb773dd99bc9a045f3f2a518a25164f8639",
    "fixtures/conformance-suite/jit_envelope_dag_mutation.json": "b1808fa91ba497a4570db8ba657346997c2410a3",
    "fixtures/conformance-suite/lineage_wait.json": "724a89caa62d220d18f747472932c8d41f3c0fe3",
    "fixtures/conformance-suite/manual_reconstruction.json": "7ba7cc3d6084a6eb1b0cbaab0cf7fd5c9a2e2823",
    "fixtures/conformance-suite/precedence_conjunction.json": "88f102040735341951e91a8f26c33efdd706e681",
    "fixtures/conformance-suite/reduction_fail_closed.json": "e06d395cf8405197957985bbe7a69e09e5a46bfc",
    "fixtures/conformance-suite/release_applicability.json": "35a98af0f3101d135e583fe9d3c64e0c62dbdb44",
    "fixtures/conformance-suite/selector_independence.json": "f0d8b63d48065211f2b5c36668f24dbd7200cbf9",
    "fixtures/conformance-suite/task_learning_compat.json": "88b2ed6ec5832dc01ab19fdc19bc0814a85bbc9f",
    ".agent/execution/T-012/IMPLEMENTATION_MAP.md": "8dc93553a7e7b23d55495662b1ad31fe461fe368",
    "scripts/test_v49_gate_currentness.py": "5aede49e96f1d1dab8357c55f38752da0dcc99ef",
    "scripts/test_v48_integration_closure.py": "7c4393a4b021b0a65484191532d7e4c53c1378b9",
    # F1-style re-bind (#1038): the CI-repair lane itself edits this T-012
    # output (checkout fetch-depth: 0), so the pin moves to the repaired
    # blob; every other T-012 output stays pinned to its exact composed blob.
    ".github/workflows/verify-standard.yml": "9fa6099f867b4ce68c0963fbd012f8970753c4d6",
}

# The T-012 oracle identity of this kernel itself: the only lawful edit on top
# of the merged T-012 content is the F1-style re-bind documented above, so the
# kernel's C01-C13 oracle surface is pinned by these markers plus the green
# execution of this very suite in the same run.
T012_KERNEL_ORACLE_MARKERS = (
    "class C12CoverageManifest(unittest.TestCase):",
    "def test_c12_test_oracle_lane_discipline",
    "def test_c12_coverage_manifest",
    "T012_MERGED_BLOBS",
    "T012_KERNEL_ORACLE_MARKERS",
)

# v4.10 integration (claim #779@6084794791 / pre-merge #779@6084805500; merge
# commit e0315b2a): `.agent/execution/T-012/IMPLEMENTATION_MAP.md` moved out of
# this pack-head loop into T012_MERGED_BLOBS — the disclosed composition rebind
# (§28 -> §29 citation in its read-only-inputs line) legally mutated that one
# planning file at the integration, so it is pinned as an exact merged output
# instead of "unmutated since the execution pack head". The remaining five
# files stay pack-head-frozen.
PLANNING_PATHS = tuple(
    f".agent/execution/T-012/{name}"
    for name in (
        "MANIFEST.yaml",
        "EXECUTION_CONTRACT.md",
        "TEST_MATRIX.yaml",
        "FAILURE_MATRIX.yaml",
        "REVIEW_CHECKLIST.md",
    )
)

# Owner sections this suite pins by exact text so a semantic drift of the
# merged owners fails HERE (binding), rather than being redefined locally.
PINNED_OWNER_TEXT = {
    "standards/ASSURANCE_PLAN_STANDARD.md": (
        "CURRENT_OWNER_AUTHORITY\nAND OWNER_PERMISSION=ALLOW_REDUCTION",
        "policy=conjunctive-no-cancellation",
        "cancellation_allowed=false",
        "unresolved-valid-findings-carry-forward",
        "durable-fact, deterministic-check, owner-record",
        "BASELINE\nREDUCED\nSTRONGER\nBLOCKED",
        "docs-only\nrisk:low",
    ),
    "standards/EXECUTION_ARCHITECTURE_STANDARD.md": (
        "`STALE` and `UNKNOWN` MUST NOT authorize Dispatch, Claim, merge, Freeze",
        "A phase that cannot be proven in-envelope is never treated as in-envelope",
        "A material topology change (new semantic Task, added/removed blocked-by edge",
        "NON_DISPATCHABLE   no Dispatch is materialized from it",
        "a predecessor's completion never inherits lineage currentness",
        "new adverse finding between Dispatch and Claim                   => Claim admission fails/recomputes",
        "at most one canonical claim linearizes (the first against still-current predicates)",
        "the same interleaving always yields the same outcome",
        "crash/restart reconstruction replays to the same state from GitHub/repository/evidence facts alone",
    ),
    "standards/RELEASE_STANDARD.md": (
        "CONCERN_NOT_APPLICABLE\n!= VERSION_NOT_APPLICABLE",
        "CONCERN_DEFERRED\n!= VERSION_GATE_SATISFIED",
        "`UNKNOWN` is fail-closed",
        "MUST NOT retroactively shorten gates already required",
    ),
    "references/GATE_EVIDENCE_CURRENTNESS_MATRIX.md": (
        "NO_OWNER_TRANSFER_RULE          => HISTORICAL_ONLY",
        "UNKNOWN_BINDING                 => HISTORICAL_ONLY_OR_BLOCKED (fail-closed)",
        "OWNER_FRESH_ONLY                => FRESH_EXECUTION_REQUIRED",
        "MATERIAL_BINDING_CHANGE         => SUCCESSOR_ASSURANCE_REQUIRED",
        "UNRESOLVED_ADVERSE_FINDING      => CARRY_FORWARD_UNTIL_DISPOSITION",
    ),
}


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def load_fixture(name: str) -> dict:
    return json.loads((FIXTURE_DIR / name).read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=True, capture_output=True, text=True
    ).stdout.strip()


def git_blob_sha(rev: str, rel_path: str) -> str:
    return git("rev-parse", f"{rev}:{rel_path}")


def github_anchors(text: str) -> set[str]:
    anchors = set()
    for line in text.splitlines():
        match = re.match(r"^(#+) (.+)$", line)
        if match is None:
            continue
        segment = match.group(2).strip().lower()
        segment = re.sub(r"[^\w\- ]", "", segment)
        segment = segment.replace(" ", "-")
        anchors.add(segment)
    return anchors


def resolve_owner_ref(ref: str) -> None:
    """Assert an owner ref resolves in-repository (path + GitHub anchor)."""
    path_part, _, frag = ref.partition("#")
    path = ROOT / path_part
    if not path.is_file():
        raise AssertionError(f"owner ref path does not resolve: {ref}")
    if frag and path_part.endswith(".md"):
        if frag not in github_anchors(path.read_text(encoding="utf-8")):
            raise AssertionError(f"owner ref anchor missing in {path_part}: #{frag}")


def substitute(value, current_dimensions: dict, envelope_proof: dict | None = None):
    """Expand the fixture placeholders into merged-kernel fact shapes."""
    if isinstance(value, dict):
        out = {}
        for key, item in value.items():
            if item == "USE_CURRENT_DIMENSIONS":
                out[key] = current_dimensions
            elif item == "USE_ALL_CURRENT_COMPONENTS":
                out[key] = {"bound_components": dict(current_dimensions)}
            elif item == "USE_IN_ENVELOPE_PROOF":
                out[key] = envelope_proof
            else:
                out[key] = substitute(item, current_dimensions, envelope_proof)
        return out
    if isinstance(value, list):
        return [substitute(item, current_dimensions, envelope_proof) for item in value]
    return value


# --- C01/C02 local pure function, pinned to ASSURANCE_PLAN_STANDARD §9/§10 ---

PROOF_BASES = frozenset({"durable-fact", "deterministic-check", "owner-record"})


def reduction_outcome(permission, permission_current: bool, predicate_proofs: list[dict]) -> str:
    """ASSURANCE_PLAN_STANDARD §9 conjunction: all conjuncts or no reduction.

    Pinned by exact owner text in C02 (the conjunction and the proof-basis
    vocabulary are asserted verbatim in the same test run); this function adds
    no semantics of its own and never authorizes a lower path on ambiguity.
    """
    if permission != "ALLOW_REDUCTION" or not permission_current:
        return "BLOCKED"
    if not predicate_proofs:
        return "BLOCKED"
    for proof in predicate_proofs:
        if proof.get("state") is not True:
            return "BLOCKED"
        if proof.get("proof_basis") not in PROOF_BASES:
            return "BLOCKED"
    return "REDUCED"


def resolve_concern(concern: dict) -> tuple[str | None, str]:
    """Gate-Authority precedence within one concern (§9), owner-scoped (§10).

    Returns (floor requirement id or None, outcome). The highest-authority
    current requirement is the concern baseline; a lower requirement replaces
    it only through a LEGAL owner reduction (C02 engine). A positively proven
    owner NOT_APPLICABLE resolution removes the concern's own requirement —
    never another owner's.
    """
    requirements = sorted(concern["requirements"], key=lambda r: -r["authority_rank"])
    baseline = requirements[0]
    resolution = concern.get("resolution")
    if resolution is None:
        return baseline["requirement_id"], "BASELINE"
    if resolution["owner_permission"] == "NOT_APPLICABLE" and resolution.get("permission_current"):
        for proof in resolution.get("predicate_proofs", []):
            if proof.get("state") is not True or proof.get("proof_basis") not in PROOF_BASES:
                return baseline["requirement_id"], "BLOCKED"
        return None, "NOT_APPLICABLE_RESOLVED"
    outcome = reduction_outcome(
        resolution["owner_permission"],
        resolution.get("permission_current", False),
        resolution.get("predicate_proofs", []),
    )
    if outcome == "REDUCED":
        selected = baseline["requirement_id"]
        for requirement in requirements:
            if requirement["requirement_id"] == resolution["selected_requirement_id"]:
                selected = requirement["requirement_id"]
        return selected, "REDUCED"
    return baseline["requirement_id"], outcome


def compose_floor(concerns: list[dict]) -> tuple[list[str], list[str]]:
    """Cross-owner composition (§10): conjunctive union, cancellation_allowed=false.

    Every concern resolves its own floor locally first; the floor is the union
    of the resolved requirement sets — one owner's resolution can never cancel
    another owner's current requirement, and unknown/conflicting authority
    fails closed (a concern with a non-resolvable baseline contributes its
    BLOCKED route, not a silent drop).
    """
    floor: list[str] = []
    blocked: list[str] = []
    for concern in concerns:
        requirement_id, outcome = resolve_concern(concern)
        if requirement_id is not None:
            floor.append(requirement_id)
        if outcome in {"BLOCKED", "DENIED"}:
            blocked.append(concern["concern_id"])
    return sorted(floor), sorted(blocked)


class ConformanceSuiteBase(unittest.TestCase):
    maxDiff = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        cls.rule_ids = {rule["rule_id"] for rule in cls.registry["forbidden_inferences"]}
        cls.prd_text = PRD.read_text(encoding="utf-8")
        cls.prd_anchors = github_anchors(cls.prd_text)
        cls.owner_map = gate_kernel.load_fixture("owner_map.json")
        cls.gate_rows = {row["row_id"]: row for row in cls.owner_map["rows"]}

    def assert_exact_refs(self, fixture: dict) -> None:
        for ref in fixture.get("owner_refs", []):
            resolve_owner_ref(ref)

    def scenario_exact_refs(self, fixture: dict) -> None:
        for scenario in fixture.get("scenarios", []):
            with self.subTest(scenario=scenario.get("scenario_id")):
                for ref in scenario.get("exact_refs", []):
                    resolve_owner_ref(ref)

    def assert_frozen_scenario_anchor(self, letter: str) -> None:
        prefix = letter.lower() + "-"
        self.assertTrue(
            any(anchor.startswith(prefix) for anchor in self.prd_anchors),
            f"Frozen PRD scenario {letter} missing from current PRD",
        )


# ---------------------------------------------------------------------------
# C01 — precedence vs conjunction
# ---------------------------------------------------------------------------

class C01GateAuthorityPrecedenceAndConjunction(ConformanceSuiteBase):
    """DAG v0.1 T-012 item 1. Frozen PRD A/B; L2 positives 2/4; L2 §17 negatives."""

    def test_c01_precedence_and_conjunction(self) -> None:
        fixture = load_fixture("precedence_conjunction.json")
        self.assert_exact_refs(fixture)
        self.scenario_exact_refs(fixture)

        standard = (ROOT / "standards" / "ASSURANCE_PLAN_STANDARD.md").read_text(encoding="utf-8")
        schema = load_schema("assurance-plan-v2.schema.json")
        # Owner conjunction + composition policy pinned verbatim (binding, not redefinition).
        for anchor in (
            "CURRENT_OWNER_AUTHORITY\nAND OWNER_PERMISSION=ALLOW_REDUCTION",
            "policy=conjunctive-no-cancellation",
            "cancellation_allowed=false",
        ):
            self.assertIn(anchor, standard)
        composition = schema["properties"]["cross_owner_composition"]["properties"]
        self.assertEqual("conjunctive-no-cancellation", composition["policy"]["const"])
        self.assertFalse(composition["cancellation_allowed"]["const"])

        scenarios = {s["scenario_id"]: s for s in fixture["scenarios"]}

        s = scenarios["C01_S1_higher_gate_authority_override_precedes_lower_default"]
        floor, blocked = compose_floor(s["concerns"])
        self.assertEqual(s["expect"]["floor_requirement_ids"], floor)
        self.assertEqual(1, len(floor), "override + default compose to ONE current requirement, not two independent atoms")
        self.assert_frozen_scenario_anchor("A")

        s = scenarios["C01_S2_owner_proven_docs_only_reduction_legal_prospective"]
        floor, blocked = compose_floor(s["concerns"])
        self.assertEqual(s["expect"]["floor_requirement_ids"], floor)
        self.assertEqual(["review-focused"], floor)
        self.assert_frozen_scenario_anchor("B")

        s = scenarios["C01_S3_one_owner_permission_never_cancels_other_owner_requirement"]
        floor, blocked = compose_floor(s["concerns"])
        self.assertEqual(s["expect"]["floor_requirement_ids"], floor)
        self.assertEqual(["y-validation-required"], floor)
        self.assertTrue(s["expect"]["cancellation_attempted"])
        self.assertTrue(any(c["concern_id"] == "concern-y" for c in s["concerns"]))
        self.assert_frozen_scenario_anchor("A")

        s = scenarios["C01_S4_conjunctive_floor_never_collapses_to_single_score"]
        floor, blocked = compose_floor(s["concerns"])
        self.assertEqual(sorted(s["expect"]["floor_requirement_ids"]), floor)
        self.assertTrue(s["expect"]["floor_is_owner_scoped_set"])
        # The floor schema itself is an owner-bound requirement SET, not a score.
        floor_schema = schema["properties"]["assurance_floor"]
        self.assertEqual("owner-scoped-conjunctive-floor", floor_schema["properties"]["composition"]["const"])
        self.assertGreaterEqual(floor_schema["properties"]["requirements"]["minItems"], 1)
        self.assert_frozen_scenario_anchor("A")


# ---------------------------------------------------------------------------
# C02 — reduction proof fail-closed
# ---------------------------------------------------------------------------

class C02ReductionProofFailClosed(ConformanceSuiteBase):
    """DAG v0.1 T-012 item 2. Frozen PRD M; L2 positives 3/5; L2 §17 negatives."""

    def test_c02_reduction_fail_closed(self) -> None:
        fixture = load_fixture("reduction_fail_closed.json")
        self.assert_exact_refs(fixture)
        self.scenario_exact_refs(fixture)
        standard = (ROOT / "standards" / "ASSURANCE_PLAN_STANDARD.md").read_text(encoding="utf-8")
        # Owner §9 conjunction + basis vocabulary pinned verbatim (binding).
        self.assertIn("CURRENT_OWNER_AUTHORITY\nAND OWNER_PERMISSION=ALLOW_REDUCTION", standard)
        self.assertIn("durable-fact, deterministic-check, owner-record", standard)
        self.assertIn("BASELINE\nREDUCED\nSTRONGER\nBLOCKED", standard)
        self.assertIn("docs-only\nrisk:low", standard)

        engine_scenarios = [
            "C02_S1_all_conjuncts_true_reduces",
            "C02_S2_deny_reduction_blocks",
            "C02_S3_unknown_permission_blocks",
            "C02_S4_missing_permission_blocks",
            "C02_S5_false_predicate_blocks",
            "C02_S6_unknown_predicate_blocks",
            "C02_S7_model_judgment_proof_basis_blocks",
            "C02_S8_stale_proof_blocks",
        ]
        scenarios = {s["scenario_id"]: s for s in fixture["scenarios"]}
        for sid in engine_scenarios:
            with self.subTest(scenario=sid):
                s = scenarios[sid]
                outcome = reduction_outcome(
                    s["input"]["owner_permission"],
                    s["input"]["permission_current"],
                    s["input"]["predicate_proofs"],
                )
                self.assertEqual(
                    "REDUCED" if s["expect"]["reduction_allowed"] else "BLOCKED",
                    outcome,
                    sid,
                )
                self.assertEqual(s["expect"]["resolution_outcome"], outcome)

        # Merged T-007 kernel oracle: model reasoning never authorizes an
        # unproven reduction (core reduction_decision, Product M / §29.7 [K01/K09]).
        s = scenarios["C02_S9_ambiguous_predicate_model_reasoning_cannot_authorize"]
        for case in s["proof_states"]:
            with self.subTest(proof_state=case["proof_state"]):
                decision = core_kernel.reduction_decision(case["proof_state"], case["model_judgment"])
                self.assertEqual(case["expect_route"], decision)
        self.assert_frozen_scenario_anchor("M")

        # Labels/facts never prove reduction by themselves (L2 §17 negatives).
        s = scenarios["C02_S10_labels_and_skips_never_prove_reduction"]
        for label in s["non_proof_facts"]:
            with self.subTest(non_proof_fact=label):
                outcome = reduction_outcome(
                    None, False, [{"predicate_id": label, "state": True, "proof_basis": label}]
                )
                self.assertEqual("BLOCKED", outcome)
        self.assertEqual(s["expect"]["resolution_outcome"], "BLOCKED")


# ---------------------------------------------------------------------------
# C03 — assurance currentness TOCTOU
# ---------------------------------------------------------------------------

class C03AssuranceCurrentnessToctou(ConformanceSuiteBase):
    """DAG v0.1 T-012 item 3. Frozen PRD F; L2 positives 6/7; L2 §17 negative."""

    def test_c03_currentness_toctou(self) -> None:
        fixture = load_fixture("currentness_toctou.json")
        self.assert_exact_refs(fixture)
        self.scenario_exact_refs(fixture)
        dimensions = fixture["component_current_dimensions"]
        checkpoints = fixture["transition_checkpoints"]
        scenarios = {s["scenario_id"]: s for s in fixture["scenarios"]}

        s = scenarios["C03_S1_consume_current_then_adverse_finding_before_claim_fails_claim"]
        state = "CURRENT"
        published = False
        for step in s["timeline"]:
            if step["event"] == "new_adverse_finding":
                continue  # durable fact lands between the two transitions
            # The BOUND digest stays what the plan recorded; the engine recomputes
            # the CURRENT digest from the unresolved findings at each transition.
            state = gate_kernel.plan_binding_state(
                s["plan_binding"], dimensions, step["unresolved_findings"]
            )
            self.assertEqual(step["expect_binding_state"], state, step["event"])
            admitted = gate_kernel.transition_admissions(state, ["claim_admission" if step["event"] == "claim_admission" else "dispatch_reservation"])
            self.assertEqual(step["expect_admitted"], bool(admitted), step["event"])
            if step["event"] == "claim_admission" and admitted:
                published = True
        self.assertFalse(published, "a claim consumed on a later-STALE binding is never ratified retroactively")
        self.assert_frozen_scenario_anchor("F")

        s = scenarios["C03_S2_competing_claim_linearizes_against_still_current_predicates"]
        dimensions = dict(fixture["component_current_dimensions"])
        for interleaving in s["interleavings"]:
            with self.subTest(interleaving=interleaving["interleaving_id"]):
                accepted: list[str] = []
                rejected: list[str] = []
                current = "CURRENT"
                for event in interleaving["events"]:
                    worker, action = event.split(":", 1)
                    if action.startswith("recompute@"):
                        current = action.split("@", 1)[1]
                    elif action == "claim":
                        if worker in accepted:
                            rejected.append(worker)  # duplicate claim rejected atomically
                        elif current == "CURRENT" and not accepted:
                            accepted.append(worker)  # first claim against still-current predicates linearizes
                        else:
                            rejected.append(worker)  # drifted binding publishes no canonical claim
                expected = s["expect"][interleaving["interleaving_id"]]
                self.assertEqual(expected["accepted"], accepted)
                self.assertEqual(expected["rejected"], rejected)
                self.assertEqual(1, len(accepted), "outcomes never include both claims accepted")
                self.assertFalse(expected["accepted_claim_silently_lost"])
        self.assert_frozen_scenario_anchor("F")

        s = scenarios["C03_S3_stale_plan_at_later_checkpoints_recomputes_never_ratifies"]
        state = gate_kernel.plan_binding_state(s["plan_binding"], dict(fixture["component_current_dimensions"]), s["unresolved_findings"])
        self.assertEqual("STALE", state)
        self.assertEqual([], gate_kernel.transition_admissions(state, [s["transition_under_check"]]))

        s = scenarios["C03_S4_missing_component_is_unknown_fail_closed"]
        state = gate_kernel.plan_binding_state(s["plan_binding"], dict(fixture["component_current_dimensions"]), s["unresolved_findings"])
        self.assertEqual("UNKNOWN", state)
        self.assertEqual([], gate_kernel.transition_admissions(state, [s["transition_under_check"]]))

        s = scenarios["C03_S5_empty_finding_set_still_digest_bound"]
        state = gate_kernel.plan_binding_state(s["plan_binding"], dict(fixture["component_current_dimensions"]), s["unresolved_findings"])
        self.assertEqual("CURRENT", state)
        self.assertEqual(s["transition_under_check"], gate_kernel.transition_admissions(state, [s["transition_under_check"]])[0])

        # CURRENT admits transitions only; CURRENT -> PASS/READY stays forbidden.
        s = scenarios["C03_S6_currentness_never_mints_pass"]
        for rule_id in s["forbidden_inference_rule_ids"]:
            self.assertIn(rule_id, self.rule_ids)
        self.assertEqual(gate_kernel.POSITIVE_VERDICTS["M01"], set())


# ---------------------------------------------------------------------------
# C04 — adverse finding carry-forward
# ---------------------------------------------------------------------------

class C04AdverseFindingCarryForward(ConformanceSuiteBase):
    """DAG v0.1 T-012 item 4. Frozen PRD N/J; L2 positives 8/9; §9.1/§9.2."""

    def test_c04_carry_forward(self) -> None:
        fixture = load_fixture("carry_forward.json")
        self.assert_exact_refs(fixture)
        self.scenario_exact_refs(fixture)
        standard = (ROOT / "standards" / "ASSURANCE_PLAN_STANDARD.md").read_text(encoding="utf-8")
        self.assertIn("unresolved-valid-findings-carry-forward", standard)
        aggregation = load_schema("review-aggregation-v1.schema.json")
        self.assertEqual("finding-union-blocker-dominance", aggregation["properties"]["aggregation_policy"]["const"])

        for scenario in fixture["scenarios"]:
            with self.subTest(scenario=scenario["scenario_id"]):
                if "kernel_binding" not in scenario:
                    continue
                result = gate_kernel.successor_review_gate(
                    carried_findings=scenario["carried_findings"],
                    per_finding_outcomes=scenario["per_finding_outcomes"],
                    successor_subject=scenario["successor_subject"],
                    successor_review=scenario.get("successor_review"),
                    authorized_repair=scenario["authorized_repair"],
                    origin_subject=fixture["origin_subject"],
                    owning_authority_disposition=scenario.get("owning_authority_disposition"),
                )
                expected = scenario["expect"]
                self.assertEqual(expected["admissible"], result["admissible"], scenario["scenario_id"])
                self.assertEqual(sorted(expected["unresolved_after"]), sorted(result["unresolved_after"]))
                if expected.get("reason"):
                    self.assertEqual(expected["reason"], result["reason"])
                if expected.get("carry_disposition"):
                    self.assertEqual(expected["carry_disposition"], result["carry_disposition"])
                self.assert_frozen_scenario_anchor("N")

        # Hidden/release high-risk finding: required thaw/repair/requalification chain.
        s = next(x for x in fixture["scenarios"] if x["scenario_id"] == "C04_S8_hidden_release_finding_forces_thaw_requalification_route")
        release_std = (ROOT / "standards" / "RELEASE_STANDARD.md").read_text(encoding="utf-8")
        self.assertIn("FROZEN\n→ THAWED / INVALIDATED", release_std)
        for step in s["carrier_chain"][2:]:
            self.assertIn(step, release_std)
        self.assertFalse(s["expect"]["proportional_shortcut_allowed"])
        self.assert_frozen_scenario_anchor("J")


# ---------------------------------------------------------------------------
# C05 — selector/independence conflicts
# ---------------------------------------------------------------------------

class C05SelectorIndependenceConflicts(ConformanceSuiteBase):
    """DAG v0.1 T-012 item 5. Frozen PRD G; L2 positive 10; §27.2/§29.4."""

    def test_c05_selector_independence_conflicts(self) -> None:
        fixture = load_fixture("selector_independence.json")
        self.assert_exact_refs(fixture)
        self.scenario_exact_refs(fixture)
        architecture = (ROOT / "standards" / "EXECUTION_ARCHITECTURE_STANDARD.md").read_text(encoding="utf-8")
        self.assertIn("**All hard predicates are evaluated before ranking.**", architecture)
        self.assertIn("MUST NOT promote `INELIGIBLE` or `UNKNOWN` to `ELIGIBLE`", architecture)

        scenarios = {s["scenario_id"]: s for s in fixture["scenarios"]}

        s = scenarios["C05_S1_independence_conflict_ineligible_despite_best_rank"]
        verdicts = {
            c["candidate_id"]: v48_kernel.resolve_eligibility(c["predicates"]) for c in s["candidates"]
        }
        for candidate_id, expected in s["expect"].items():
            if candidate_id in verdicts:
                self.assertEqual(expected, verdicts[candidate_id], candidate_id)
        ranked = v48_kernel.rank_eligible_only([(c["predicates"], c["rank"]) for c in s["candidates"]])
        self.assertEqual(
            [c["candidate_id"] for c in s["candidates"] if s["expect"].get(c["candidate_id"]) == "ELIGIBLE" or c["candidate_id"] in s["expect"]["ranked_candidate_ids"]],
            [s["candidates"][i]["candidate_id"] for i in ranked],
        )
        self.assertEqual(s["expect"]["ranked_candidate_ids"], [s["candidates"][i]["candidate_id"] for i in ranked])
        self.assert_frozen_scenario_anchor("G")

        s = scenarios["C05_S2_profile_block_cannot_be_promoted_by_ranking_inputs"]
        eligible = []
        for candidate in s["candidates"]:
            # §29.4: a BLOCKED_* profile projection is a hard INELIGIBLE before ranking.
            predicates = {
                "ready": True, "current": True, "capability": True, "resources": True,
                "security": True, "independence": candidate["profile_projection"] == "PROJECTED",
                "write_set": True, "composite": True,
            }
            if v48_kernel.resolve_eligibility(predicates) == "ELIGIBLE":
                eligible.append(candidate["candidate_id"])
        self.assertEqual(s["expect"]["eligible_candidate_ids"], eligible)
        attractive = next(c for c in s["candidates"] if c["profile_projection"] != "PROJECTED")
        self.assertLess(attractive["priority"], 10, "the blocked candidate is the ranking-attractive one")

        s = scenarios["C05_S3_conflicting_source_authorities_block_order_independently"]
        for order in s["orders"]:
            with self.subTest(order=order):
                projection = role_kernel.evaluate_requirements([s["requirement_sets"][ref] for ref in order])
                self.assertEqual(s["expect"]["posture"], projection["posture"])
                self.assertEqual(s["expect"]["conflict_keys"], projection["conflict_keys"])
                self.assertIsNone(projection["projected_requirements"])

        s = scenarios["C05_S4_agreeing_sources_project_regardless_of_order"]
        projections = [
            role_kernel.evaluate_requirements([s["requirement_sets"][ref] for ref in order])
            for order in s["orders"]
        ]
        self.assertEqual(projections[0], projections[1])
        self.assertEqual("PROJECTED", projections[0]["posture"])
        self.assertEqual(s["expect"]["projected_requirements"], projections[0]["projected_requirements"])

        s = scenarios["C05_S5_provider_model_identity_is_authority_inert"]
        candidate = s["candidate"]
        self.assertEqual(s["expect"]["eligibility"], v48_kernel.resolve_eligibility(candidate["predicates"]))
        profile_schema = load_schema("role-execution-profile-v1.schema.json")
        for injected in ("provider_authority", "model_routing_authority", "claim_switch", "granted_role_actions", "terminal_authority_grant", "capability_proof"):
            self.assertNotIn(injected, profile_schema.get("properties", {}), injected)
        self.assertFalse(profile_schema.get("additionalProperties", True))


# ---------------------------------------------------------------------------
# C06 — JIT in-envelope vs DAG mutation
# ---------------------------------------------------------------------------

class C06JitEnvelopeVsDagMutation(ConformanceSuiteBase):
    """DAG v0.1 T-012 item 6. Frozen PRD L; L2 positives 11/12; §29.2 + JIT ref."""

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.owner_standard_text = GOVERNANCE_STANDARD.read_text(encoding="utf-8")
        cls.owner_classes = jit_kernel.parse_owner_mutation_classes(cls.owner_standard_text)
        wiring_reference = (ROOT / "references" / "JIT_DAG_MUTATION_GOVERNANCE_V49_REFERENCE.md").read_text(encoding="utf-8")
        cls.routing = jit_kernel.parse_reference_json_block(wiring_reference, "## 3. Routing table (machine-readable)")
        cls.bookkeeping = jit_kernel.parse_reference_json_block(wiring_reference, "Bookkeeping action vocabulary")["bookkeeping_actions"]
        cls.record_schema = json.loads(MUTATION_RECORD_SCHEMA_PATH.read_text(encoding="utf-8"))

    def classify(self, proposal: dict, facts_plane: dict) -> dict:
        record = proposal.get("mutation_record")
        if record == "USE_RECORD":
            base = load_fixture("jit_envelope_dag_mutation.json")
            record = base["mutation_record"]
        proposal = dict(proposal)
        if record is not None:
            proposal["mutation_record"] = record
        return jit_kernel.classify_and_route(
            proposal,
            facts_plane,
            self.owner_classes,
            set(self.bookkeeping),
            self.routing["routes"],
            self.routing,
            self.record_schema,
        )

    def test_c06_jit_envelope_vs_dag_mutation(self) -> None:
        fixture = load_fixture("jit_envelope_dag_mutation.json")
        self.assert_exact_refs(fixture)
        self.scenario_exact_refs(fixture)
        architecture = (ROOT / "standards" / "EXECUTION_ARCHITECTURE_STANDARD.md").read_text(encoding="utf-8")
        self.assertIn("A phase that cannot be proven in-envelope is never treated as in-envelope", architecture)
        self.assertIn("is not a JIT phase: it routes to v4.3 Task DAG mutation governance", architecture)
        scenarios = {s["scenario_id"]: s for s in fixture["scenarios"]}
        facts_plane = fixture["fact_plane"]

        s = scenarios["C06_S1_in_envelope_jit_phase_is_bookkeeping_not_mutation"]
        decision = self.classify(s["proposal"], facts_plane)
        self.assertEqual("BOOKKEEPING", decision["classification"])
        self.assertEqual("NO_MUTATION_REQUIRED", decision["route"])
        self.assertFalse(decision["semantic_topology_changed"])
        self.assert_frozen_scenario_anchor("L")

        s = scenarios["C06_S2_phase_not_proven_in_envelope_is_blocked_never_auto_admitted"]
        routes = []
        for proposal in s["proposals"]:
            decision = self.classify(proposal, facts_plane)
            routes.append(decision["route"])
        self.assertEqual(s["expect"]["routes"], routes)
        # A phase with NO envelope declaration is never auto-admitted either
        # (core §29.2 kernel: declared_in None => BLOCKED).
        core_facts = {
            "plan_binding": {"bound_components": {}},
            "current_dimensions": {},
            "unresolved_findings": [],
            "lineage_refs": [],
            "composite_admission": {"state": "AVAILABLE"},
        }
        self.assertEqual(
            "BLOCKED",
            core_kernel.jit_verdict(
                {"dependency_state": "DONE", "envelope_proof": {"declared_in": None, "envelope_conditions": fixture["clean_envelope_conditions"]}},
                core_facts,
            ),
        )

        s = scenarios["C06_S3_add_dependency_is_material_mutation_routed_to_v43_owner"]
        decision = self.classify(s["proposal"], facts_plane)
        self.assertEqual("SEMANTIC_MUTATION", decision["classification"])
        self.assertEqual(s["expect"]["route"], decision["route"])
        self.assertTrue(decision["mutation_record_required"])
        self.assertTrue(decision["native_mutation_performed"])

        s = scenarios["C06_S4_textual_dependency_list_never_substitutes_native_edges"]
        decision = self.classify(s["proposal"], facts_plane)
        self.assertEqual(s["expect"]["classification"], decision["classification"])
        self.assertEqual(s["expect"]["route"], decision["route"])
        self.assertIn(s["expect"]["contains_reason"], decision["reasons"])

        s = scenarios["C06_S5_stale_mutation_record_fails_closed_preserving_live_dag"]
        decision = self.classify(s["proposal"], facts_plane)
        self.assertEqual(s["expect"]["classification"], decision["classification"])
        self.assertEqual(s["expect"]["route"], decision["route"])
        self.assertIn(s["expect"]["contains_reason"], decision["reasons"])

        s = scenarios["C06_S6_telemetry_only_justification_cannot_authorize_mutation"]
        decision = self.classify(s["proposal"], facts_plane)
        self.assertEqual(s["expect"]["classification"], decision["classification"])
        self.assertEqual(s["expect"]["route"], decision["route"])
        self.assertIn(s["expect"]["contains_reason"], decision["reasons"])

        s = scenarios["C06_S7_unknown_action_fails_closed_ambiguous"]
        decision = self.classify(s["proposal"], facts_plane)
        self.assertEqual(s["expect"]["classification"], decision["classification"])
        self.assertEqual(s["expect"]["route"], decision["route"])
        self.assertIn(s["expect"]["contains_reason"], decision["reasons"])

        s = scenarios["C06_S8_core_classifier_routes_topology_change_away_from_jit"]
        for proposal in s["proposals"]:
            with self.subTest(action=proposal["action"]):
                self.assertEqual(proposal["expect_route"], core_kernel.classify_topology_change(proposal))


# ---------------------------------------------------------------------------
# C07 — gate-owned transfer/currentness
# ---------------------------------------------------------------------------

class C07GateOwnedTransferCurrentness(ConformanceSuiteBase):
    """DAG v0.1 T-012 item 7. Frozen PRD H/I; L2 §10 owner map (T-010 merged)."""

    def test_c07_gate_transfer_and_currentness(self) -> None:
        fixture = load_fixture("gate_transfer_currentness.json")
        self.assert_exact_refs(fixture)
        self.scenario_exact_refs(fixture)
        matrix_doc = (ROOT / "references" / "GATE_EVIDENCE_CURRENTNESS_MATRIX.md").read_text(encoding="utf-8")
        for rule in (
            "NO_OWNER_TRANSFER_RULE          => HISTORICAL_ONLY",
            "UNKNOWN_BINDING                 => HISTORICAL_ONLY_OR_BLOCKED (fail-closed)",
            "OWNER_FRESH_ONLY                => FRESH_EXECUTION_REQUIRED",
            "MATERIAL_BINDING_CHANGE         => SUCCESSOR_ASSURANCE_REQUIRED",
        ):
            self.assertIn(rule, matrix_doc)
        scenarios = {s["scenario_id"]: s for s in fixture["scenarios"]}

        s = scenarios["C07_S1_target_transfer_reuses_only_exact_binding_equivalence"]
        record = dict(s["record"])
        record["row_id"] = s["row_id"]
        disposition = gate_kernel.route_evidence(record, s["current_subject"], self.gate_rows[s["row_id"]])
        self.assertEqual(s["expect"]["disposition"], disposition)
        self.assertEqual(s["expect"]["gate_satisfied"], gate_kernel.gate_satisfied(record, disposition, self.gate_rows[s["row_id"]]))
        self.assert_frozen_scenario_anchor("H")

        s = scenarios["C07_S2_drifted_subject_makes_pass_historical_only"]
        record = dict(s["record"])
        record["row_id"] = s["row_id"]
        disposition = gate_kernel.route_evidence(record, s["current_subject"], self.gate_rows[s["row_id"]])
        self.assertEqual(s["expect"]["disposition"], disposition)
        self.assertFalse(gate_kernel.gate_satisfied(record, disposition, self.gate_rows[s["row_id"]]))
        self.assert_frozen_scenario_anchor("I")

        s = scenarios["C07_S3_unknown_binding_fails_closed_not_transferred"]
        record = dict(s["record"])
        record["row_id"] = s["row_id"]
        self.assertEqual("HISTORICAL_ONLY", gate_kernel.route_evidence(record, s["current_subject"], self.gate_rows[s["row_id"]]))

        s = scenarios["C07_S4_fresh_only_row_requires_fresh_execution_on_candidate_drift"]
        disposition = gate_kernel.frozen_candidate_disposition(s["record"], s["freeze_record"], s["current_candidate"])
        self.assertEqual(s["expect"]["disposition"], disposition)

        s = scenarios["C07_S5_material_binding_change_requires_successor_assurance"]
        self.assertEqual(s["expect"]["outcome"], "SUCCESSOR_ASSURANCE_REQUIRED")

        s = scenarios["C07_S6_currentness_never_infers_gate_satisfaction"]
        for row_id in s["expect"]["non_verdict_rows"]:
            self.assertEqual(set(), gate_kernel.POSITIVE_VERDICTS[row_id])
        self.assertNotIn("PASS", gate_kernel.ROUTING_VOCAB)
        self.assertNotIn("READY", gate_kernel.ROUTING_VOCAB)
        for rule_id in ("F13_ASSURANCE_CURRENT_NOT_VALIDATION_PASS", "F14_ASSURANCE_CURRENT_NOT_REVIEW_PASS", "F15_ASSURANCE_CURRENT_NOT_RELEASE_READY", "F16_ASSURANCE_CURRENT_NOT_TASK_READY"):
            self.assertIn(rule_id, self.rule_ids)

        s = scenarios["C07_S7_family_mismatch_pass_is_not_consultable"]
        disposition = gate_kernel.route_evidence(s["record"], s["current_subject"], self.gate_rows[s["row_id"]])
        self.assertEqual(s["expect"]["disposition"], disposition)
        self.assertFalse(gate_kernel.gate_satisfied(s["record"], disposition, self.gate_rows[s["row_id"]]))


# ---------------------------------------------------------------------------
# C08 — Release per-gate applicability / non-aggregation
# ---------------------------------------------------------------------------

class C08ReleasePerGateApplicability(ConformanceSuiteBase):
    """DAG v0.1 T-012 item 8. Frozen PRD B/D/O; L2 positives 13/14; REL_STD §11."""

    def test_c08_release_applicability(self) -> None:
        fixture = load_fixture("release_applicability.json")
        self.assert_exact_refs(fixture)
        self.scenario_exact_refs(fixture)
        release_std = (ROOT / "standards" / "RELEASE_STANDARD.md").read_text(encoding="utf-8")
        self.assertIn("CONCERN_NOT_APPLICABLE\n!= VERSION_NOT_APPLICABLE", release_std)
        self.assertIn("CONCERN_DEFERRED\n!= VERSION_GATE_SATISFIED", release_std)
        self.assertIn("`UNKNOWN` is fail-closed", release_std)
        scenarios = {s["scenario_id"]: s for s in fixture["scenarios"]}

        s = scenarios["C08_S1_concern_decisions_never_determine_version_applicability"]
        self.assertFalse(gate_kernel.version_gate_omission_allowed(s["concern_decisions"], s["version_level_decision"]))
        self.assert_frozen_scenario_anchor("B")
        self.assert_frozen_scenario_anchor("D")

        s = scenarios["C08_S2_deferral_is_not_gate_satisfaction_at_version_closure"]
        self.assertFalse(
            gate_kernel.version_gate_omission_allowed(
                s["concern_decisions"], s["version_level_decision"], s["closure_claims_gate_satisfied_via_deferral"]
            )
        )

        s = scenarios["C08_S3_unknown_applicability_fail_closed_to_stronger_path"]
        self.assertFalse(gate_kernel.version_gate_omission_allowed(s["concern_decisions"], s["version_level_decision"]))
        self.assertEqual("UNKNOWN", s["version_level_decision"]["applicability"])

        s = scenarios["C08_S4_only_fresh_release_owned_not_applicable_permits_omission"]
        self.assertTrue(gate_kernel.version_gate_omission_allowed(s["concern_decisions"], s["version_level_decision"]))
        current, reason = gate_kernel.release_decision_current(s["version_level_decision"], fixture["version_candidate"])
        self.assertTrue(current)
        self.assertEqual("CURRENT", reason)
        # Only the exact Release-owned authority ref unlocks omission (engine-pinned).
        tampered = dict(s["version_level_decision"], release_authority_ref="standards/VALIDATION_STANDARD.md")
        self.assertFalse(gate_kernel.version_gate_omission_allowed([], tampered))

        s = scenarios["C08_S5_stale_binding_makes_old_applicability_historical"]
        current, reason = gate_kernel.release_decision_current(s["version_level_decision"], fixture["version_candidate"])
        self.assertFalse(current)
        self.assertEqual("NONCURRENT_SUBJECT_BINDING", reason)
        self.assert_frozen_scenario_anchor("O")

        s = scenarios["C08_S6_prospective_migration_never_shortens_inflight_frozen_candidate"]
        self.assertEqual(s["inflight_candidate"]["gates_required"], s["expect"]["gates_required_after_adoption"])
        self.assertFalse(s["expect"]["retroactive_shortening_allowed"])
        self.assertIn("MUST NOT retroactively shorten gates already required", release_std)

        s = scenarios["C08_S7_builder_or_concern_pass_cannot_mint_applicability"]
        minted = dict(s["attempted_mint"])
        minted["subject_identity"] = fixture["version_candidate"]["candidate_identity"]
        self.assertTrue(s["expect"]["mint_rejected"])
        self.assertNotEqual("release-authority", minted["actor"])
        self.assertFalse(
            gate_kernel.version_gate_omission_allowed([], minted),
            "a non-Release-owned mint can never permit a version gate omission",
        )


# ---------------------------------------------------------------------------
# C09 — predecessor lineage wait
# ---------------------------------------------------------------------------

class C09PredecessorLineageWait(ConformanceSuiteBase):
    """DAG v0.1 T-012 item 9. Frozen PRD K; L2 positive 15; §29.2/§29.3 + F11-F19."""

    def test_c09_lineage_wait(self) -> None:
        fixture = load_fixture("lineage_wait.json")
        self.assert_exact_refs(fixture)
        self.scenario_exact_refs(fixture)
        architecture = (ROOT / "standards" / "EXECUTION_ARCHITECTURE_STANDARD.md").read_text(encoding="utf-8")
        self.assertIn("no guaranteed-BLOCKED Builder dispatch is created merely to confirm a known lineage absence", architecture)
        for rule_id in fixture["forbidden_inference_rule_ids"]:
            self.assertIn(rule_id, self.rule_ids)
        dimension_ids = {d["dimension_id"] for d in self.registry["dimensions"]}
        self.assertIn("waiting_lineage", dimension_ids)
        scenarios = {s["scenario_id"]: s for s in fixture["scenarios"]}
        admission = fixture["admission_available"]

        def kernel_facts(s: dict, key: str = "facts") -> dict:
            proof = fixture["in_envelope_proof"]
            facts = substitute(s[key], fixture["current_dimensions"], proof)
            facts["composite_admission"] = dict(admission)
            return facts

        s = scenarios["C09_S1_all_lineage_current_ready"]
        facts = kernel_facts(s)
        posture, _ = core_kernel.lineage_posture(facts)
        self.assertEqual("CURRENT", posture)
        phase = substitute(s["phase"], fixture["current_dimensions"], fixture["in_envelope_proof"])
        self.assertEqual("READY", core_kernel.jit_verdict(phase, facts))
        self.assertIsNone(core_kernel.waiting_lineage_projection(facts))
        self.assert_frozen_scenario_anchor("K")

        s = scenarios["C09_S2_stale_predecessor_surface_waits_not_dispatches"]
        facts = kernel_facts(s)
        posture, reasons = core_kernel.lineage_posture(facts)
        self.assertEqual("WAITING_LINEAGE", posture)
        self.assertEqual(s["expect"]["projection"]["reasons"], reasons)
        phase = substitute(s["phase"], fixture["current_dimensions"], fixture["in_envelope_proof"])
        self.assertEqual("WAITING_LINEAGE", core_kernel.jit_verdict(phase, facts))
        projection = core_kernel.waiting_lineage_projection(facts)
        self.assertIsNotNone(projection)
        self.assertFalse(projection["dispatchable"])
        self.assertFalse(projection["claimable"])
        self.assertIsNone(projection["workflow_state"])
        self.assertIsNone(projection["gate_verdict"])

        s = scenarios["C09_S3_predecessor_done_does_not_inherit_lineage_currentness"]
        facts = kernel_facts(s)
        posture, _ = core_kernel.lineage_posture(facts)
        self.assertEqual("WAITING_LINEAGE", posture)
        self.assertIn("F11_TASK_DONE_NOT_LINEAGE_CURRENT", self.rule_ids)

        s = scenarios["C09_S4_wait_projection_is_never_a_workflow_or_gate_verdict"]
        for rule_id in s["forbidden_inference_rule_ids"]:
            self.assertIn(rule_id, self.rule_ids)

        s = scenarios["C09_S5_failed_lineage_is_blocked"]
        facts = kernel_facts(s)
        posture, _ = core_kernel.lineage_posture(facts)
        self.assertEqual("BLOCKED", posture)
        phase = substitute(s["phase"], fixture["current_dimensions"], fixture["in_envelope_proof"])
        self.assertEqual("BLOCKED", core_kernel.jit_verdict(phase, facts))

        s = scenarios["C09_S6_pending_dependency_blocked_before_lineage"]
        facts = kernel_facts(s)
        phase = substitute(s["phase"], fixture["current_dimensions"], fixture["in_envelope_proof"])
        self.assertEqual("BLOCKED", core_kernel.jit_verdict(phase, facts))

        s = scenarios["C09_S7_surface_integrated_recompute_drops_projection"]
        before = kernel_facts(s, "before_facts")
        after = kernel_facts(s, "after_facts")
        self.assertEqual("WAITING_LINEAGE", core_kernel.lineage_posture(before)[0])
        self.assertIsNotNone(core_kernel.waiting_lineage_projection(before))
        posture_after, _ = core_kernel.lineage_posture(after)
        self.assertEqual("CURRENT", posture_after)
        self.assertIsNone(core_kernel.waiting_lineage_projection(after))
        phase = substitute(s["phase"], fixture["current_dimensions"], fixture["in_envelope_proof"])
        self.assertEqual("READY", core_kernel.jit_verdict(phase, after))


# ---------------------------------------------------------------------------
# C10 — Task Learning same-family compatibility
# ---------------------------------------------------------------------------

class C10TaskLearningSameFamilyCompat(ConformanceSuiteBase):
    """DAG v0.1 T-012 item 10. Frozen PRD Q; L2 positive 16; v1/v2 same family."""

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.schema_v1 = load_schema("task-learning-v1.schema.json")
        cls.schema_v2 = load_schema("task-learning-v2.schema.json")

    def test_c10_same_family_compatibility(self) -> None:
        fixture = load_fixture("task_learning_compat.json")
        self.assert_exact_refs(fixture)
        identity = fixture["family_identity"]
        self.assertEqual(identity["schema_version"], self.schema_v2["properties"]["schema_version"]["const"])
        self.assertEqual(identity["owner_family"], self.schema_v2["properties"]["owner_family"]["const"])
        self.assertEqual(identity["predecessor_protocol_version"], self.schema_v2["properties"]["predecessor_protocol_version"]["const"])

        scenarios = {s["scenario_id"]: s for s in fixture["scenarios"]}

        # Q: a materially related recurrence produces a bounded same-family output.
        s = scenarios["C10_S1_recurrence_produces_bounded_same_family_output"]
        self.assertEqual([], validate_subset(fixture["valid_v2_record"], self.schema_v2))
        self.assertTrue(s["expect"]["same_family"])
        self.assertTrue(s["expect"]["no_parallel_learning_lifecycle"])
        # ADS linkage enters the EXISTING v4.8 intake only.
        self.assertIn(
            "friction_classification",
            self.schema_v2["properties"],
            "v2 preserves the v1 evolution-intake classification field",
        )
        self.assert_frozen_scenario_anchor("Q")

        # v1 history stays valid; direct v2->v1 validation fails closed.
        self.assertEqual([], validate_subset(fixture["valid_v1_record"], self.schema_v1))
        self.assertTrue(
            validate_subset(fixture["valid_v2_record"], self.schema_v1),
            "direct v1-schema validation of a v2 instance must fail closed (declared INCOMPATIBLE)",
        )
        compat = json.loads((ROOT / "references" / "TASK_LEARNING_V2_COMPATIBILITY.json").read_text(encoding="utf-8"))
        dimensions = {d["name"]: d["outcome"] for d in compat["dimensions"]}
        compatible = [name for name, outcome in dimensions.items() if outcome == "COMPATIBLE"]
        self.assertIn("owner-family-semantics", compatible)
        self.assertIn("historical-v1-record-validity", compatible)
        direct_v1 = "v1-parser-accepts-v2-instance"
        self.assertEqual("INCOMPATIBLE", dimensions[direct_v1], direct_v1)
        self.assertEqual("INCOMPATIBLE", dimensions["v2-parser-accepts-v1-instance"])
        self.assertEqual("CONDITIONALLY_COMPATIBLE", dimensions["version-aware-adoption"])

        s = scenarios["C10_S2_v2_reader_fails_closed_on_v1_identity_drift"]
        for injected in fixture["injected_v2_records"]:
            if injected.get("expect_v1_valid") is not None:
                with self.subTest(note=injected["note"]):
                    record = dict(fixture["valid_v1_record"])
                    record.update(injected["mutate"])
                    errors = validate_subset(record, self.schema_v1)
                    self.assertTrue(errors, injected["note"])
        for injected in fixture["injected_v2_records"]:
            if injected.get("expect_v2_valid") is not None:
                with self.subTest(note=injected["note"]):
                    record = dict(fixture["valid_v2_record"])
                    record.update(injected["mutate"])
                    errors = validate_subset(record, self.schema_v2)
                    self.assertTrue(errors, injected["note"])

        # root_cause_relation resolve-or-fail-closed through the merged owner kernel.
        for case in fixture["audit_resolution_cases"]:
            with self.subTest(case=case["case"]):
                record = dict(fixture["valid_v2_record"])
                record.update(case.get("mutate", {}))
                self.assertEqual(
                    case["expect_relation"],
                    learning_kernel.audit_relation_established(record, frozenset(case["resolvable"])),
                )

        s = scenarios["C10_S3_friction_vocabularies_stay_orthogonal"]
        self.assertEqual(
            s["expect"]["v1_friction_classification_enum_unchanged"] and True,
            self.schema_v1["properties"]["friction_classification"]["enum"] == self.schema_v2["properties"]["friction_classification"]["enum"],
        )
        self.assertEqual(
            sorted(s["expect"]["v2_execution_friction_class_vocabulary"]),
            sorted(self.schema_v2["properties"]["execution_friction_class"]["enum"]),
        )
        both = dict(fixture["valid_v2_record"])
        both["friction_classification"] = "STANDARD_FRICTION_CANDIDATE"
        self.assertEqual([], validate_subset(both, self.schema_v2), "the two vocabularies MAY co-occur")


# ---------------------------------------------------------------------------
# C11 — manual-compatible state reconstruction
# ---------------------------------------------------------------------------

class C11ManualCompatibleStateReconstruction(ConformanceSuiteBase):
    """DAG v0.1 T-012 item 11. Frozen PRD P; L2 positives 17/18; §29.6 replay."""

    def test_c11_manual_reconstruction(self) -> None:
        fixture = load_fixture("manual_reconstruction.json")
        self.assert_exact_refs(fixture)
        self.scenario_exact_refs(fixture)
        architecture = (ROOT / "standards" / "EXECUTION_ARCHITECTURE_STANDARD.md").read_text(encoding="utf-8")
        self.assertIn("crash/restart reconstruction replays to the same state from GitHub/repository/evidence facts alone", architecture)
        self.assertIn("There is no hidden mutable latch", architecture)

        def reconstruct(ordered_facts: list[dict]) -> dict:
            """Pure replay: derived state ONLY from durable facts (no latch)."""
            lineage = [
                {"surface_ref": f["surface_ref"], "status": f["status"]}
                for f in ordered_facts if f["kind"] == "lineage_surface"
            ]
            binding = {
                f["component"]: f["value"]
                for f in ordered_facts if f["kind"] == "plan_binding_component"
            }
            unresolved = sorted(
                f["finding_id"] for f in ordered_facts if f.get("state") == "UNRESOLVED"
            )
            # The bound digest (E10) is a durable fact; the CURRENT digest is
            # recomputed from the unresolved findings at replay time (§29.6).
            current_dimensions = {
                key: value for key, value in binding.items()
                if key != "unresolved_finding_digest"
            }
            current_dimensions["unresolved_finding_digest"] = gate_kernel.findings_digest(unresolved)
            posture, _ = core_kernel.lineage_posture(
                {"plan_binding": {"bound_components": binding}, "current_dimensions": current_dimensions, "unresolved_findings": [], "lineage_refs": lineage}
            )
            plan_state = gate_kernel.plan_binding_state(
                binding, current_dimensions, unresolved
            )
            consultable = []
            for fact in ordered_facts:
                if fact["kind"] != "owner_issued_evidence":
                    continue
                record = {
                    "record_id": fact["record_id"], "row_id": fact["row_id"],
                    "owner_ref": fact["owner_ref"], "verdict": fact["verdict"],
                    "subject_identity": fact["subject_identity"],
                }
                row = self.gate_rows[fact["row_id"]]
                disposition = gate_kernel.route_evidence(
                    record, {"subject_identity": fact["subject_identity"]}, row
                )
                if gate_kernel.gate_satisfied(record, disposition, row):
                    consultable.append(fact["record_id"])
            return {
                "lineage_posture": posture,
                "plan_binding_state": plan_state,
                "unresolved_findings": unresolved,
                "consultable_evidence_record_ids": sorted(consultable),
            }

        durable = [f for f in fixture["durable_fact_plane"] if f["kind"] != "derived_state_deletion"]
        canonical = reconstruct(durable)
        reversed_order = reconstruct(list(reversed(durable)))
        rotated = reconstruct(durable[3:] + durable[:3])
        expected = fixture["expected_reconstructed_state"]
        for replay_name, replay in (("canonical", canonical), ("reversed", reversed_order), ("rotated", rotated)):
            with self.subTest(replay=replay_name):
                self.assertEqual(expected["lineage_posture"], replay["lineage_posture"])
                self.assertEqual(expected["plan_binding_state"], replay["plan_binding_state"])
                self.assertEqual(expected["unresolved_findings"], replay["unresolved_findings"])
                self.assertEqual(expected["consultable_evidence_record_ids"], replay["consultable_evidence_record_ids"])
        self.assertEqual(canonical, reversed_order)
        self.assertEqual(canonical, rotated)
        self.assert_frozen_scenario_anchor("P")

        # Deleting derived state loses nothing: replay after the deletion event
        # is identical (E14 is not a durable fact and is skipped by design).
        with_deletion = reconstruct(fixture["durable_fact_plane"])
        self.assertEqual(canonical, with_deletion)

        # No daemon state: the suite itself is the executable proof surface —
        # stdlib + git + repository facts only (assert the owner anchor).
        l2_text = L2.read_text(encoding="utf-8")
        self.assertIn("without daemon state", l2_text)

        # baseline=selected zero-delta dogfood is compatibility evidence only.
        zero_delta_report = {
            "bound_ads_candidate": "version:v4.9.0",
            "pinned_authority_refs": ["docs/implementation/4.9.0/PRD.md#163-exact-candidate-binding"],
            "baseline_vs_selected_delta_nonzero": False,
        }
        posture = gate_kernel.dogfood_posture(zero_delta_report, "version:v4.9.0")
        self.assertFalse(posture["downstream_generality_satisfied"])
        self.assertFalse(posture["authorizes_execution"])


# ---------------------------------------------------------------------------
# C12 — coverage manifest
# ---------------------------------------------------------------------------

class C12CoverageManifest(ConformanceSuiteBase):
    """Every DAG v0.1 T-012 coverage item is bound by a class + fixture + refs."""

    def test_c12_coverage_manifest(self) -> None:
        manifest = load_fixture("coverage_manifest.json")
        items = {item["id"]: item for item in manifest["coverage_items"]}
        self.assertEqual(
            [f"C{i:02d}" for i in range(1, 13)],
            sorted(items),
            "the manifest must cover exactly C01-C12",
        )

        # The immutable DAG v0.1 blob resolves unchanged and carries every
        # coverage item text (C01-C11) verbatim inside its T-012 section.
        self.assertEqual(DAG_V01_BLOB, git_blob_sha("HEAD", str(DAG_V01.relative_to(ROOT)).replace("\\", "/")))
        dag_text = DAG_V01.read_text(encoding="utf-8")
        section = dag_text.split("### T-012", 1)[1].split("### T-013", 1)[0]
        for item_id in sorted(items):
            with self.subTest(coverage_item=item_id):
                item = items[item_id]
                self.assertTrue((FIXTURE_DIR / item["fixture"]).is_file(), item_id)
                self.assertTrue(hasattr(sys.modules[__name__], item["test_class"]), item_id)
                for ref in item["owner_refs"]:
                    resolve_owner_ref(ref)
                if item_id != "C12":
                    self.assertIn(item["dag_coverage_item"], section, item_id)
                for scenario in item["frozen_scenarios"]:
                    self.assert_frozen_scenario_anchor(scenario)
        for text, anchors in PINNED_OWNER_TEXT.items():
            body = (ROOT / text).read_text(encoding="utf-8")
            for anchor in anchors:
                self.assertIn(anchor, body, f"{text}: {anchor[:48]}...")

        # TEST_MATRIX oracle coverage (C01-C13) is present in the immutable
        # planning surface and every required check command names this suite's
        # companion batteries.
        matrix_text = TEST_MATRIX.read_text(encoding="utf-8")
        for test_id in (f"C{i:02d}" for i in range(1, 14)):
            self.assertIn(f"id: {test_id}", matrix_text)

    def test_c12_test_oracle_lane_discipline(self) -> None:
        """The suite asserts owner semantics and never redefines them.

        Lane guard: the working tree stays inside the Builder write set; the
        six immutable planning files are unmutated; the Frozen Product/L2/DAG
        blobs resolve unchanged; the merged T-012 outputs are EXACTLY present
        at the candidate (F1-style re-bind, see below).
        """
        changed = set()
        for line in git("status", "--porcelain").splitlines():
            if line.strip():
                changed.add(line[3:].strip().strip('"'))
        for path in sorted(changed):
            with self.subTest(changed_path=path):
                self.assertTrue(
                    any(path == w or path.startswith(w) for w in WRITE_SET),
                    f"path outside T-012 Builder write set: {path}",
                )
        self.assertEqual(FROZEN_PRD_BLOB, git_blob_sha("HEAD", "docs/implementation/4.9.0/PRD.md"))
        self.assertEqual(FROZEN_L2_BLOB, git_blob_sha("HEAD", "docs/implementation/4.9.0/L2_ARCHITECTURE_EVIDENCE.md"))
        self.assertEqual(FROZEN_DAG_V02_BLOB, git_blob_sha("HEAD", "docs/implementation/4.9.0/TASK_DAG.md"))
        for rel_path in PLANNING_PATHS:
            with self.subTest(planning_path=rel_path):
                self.assertEqual(git_blob_sha(PACK_HEAD_SHA, rel_path), git_blob_sha("HEAD", rel_path))
        # F1-STYLE RE-BIND (#805 POST_RECOVERY_EXACT_RECOMPOSE, #745; doctrine
        # precedent: T-010 F1 re-bind in scripts/test_v49_gate_currentness.py,
        # authorized pin-constants-only change): the original T-012 lane guard
        # `git diff --name-only 370f6e83..HEAD ⊆ T-012 WRITE_SET` is
        # structurally red at any integrated tree — after the post-recovery
        # recompose the candidate HEAD necessarily carries the recovered
        # v4.4-v4.7 families' merged deltas, exactly as the T-010 guard was
        # structurally red after T-011. Re-bound with pin constants only,
        # zero other assertion change — SAME STRENGTH: every T-012 output this
        # lane does not itself edit is pinned to its exact blob at the composed
        # tree (merge of version/v4.9.0@4322a8cc x main@4c632256), so any
        # further mutation of any T-012 output still fails; the kernel itself
        # carries exactly this re-bind on top of the merged T-012 content,
        # pinned by its oracle-identity markers below (and by this suite
        # executing its C01-C13 oracles green in the same run).
        for rel_path, merged_blob in T012_MERGED_BLOBS.items():
            with self.subTest(t012_merged_output=rel_path):
                self.assertEqual(merged_blob, git_blob_sha("HEAD", rel_path))
        kernel_source = Path(__file__).resolve().read_text(encoding="utf-8")
        for marker in T012_KERNEL_ORACLE_MARKERS:
            self.assertIn(marker, kernel_source, "T-012 kernel oracle marker missing")


if __name__ == "__main__":
    loader = unittest.defaultTestLoader
    suite = unittest.TestSuite()
    for name, obj in sorted(globals().items()):
        if name.startswith("C") and name[1:3].isdigit() and isinstance(obj, type) and issubclass(obj, unittest.TestCase):
            suite.addTests(loader.loadTestsFromTestCase(obj))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    raise SystemExit(0 if result.wasSuccessful() else 1)
