"""v4.9 T007 execution architecture proportional orchestration core kernel.

Deterministic stdlib-unittest semantic kernel for
`standards/EXECUTION_ARCHITECTURE_STANDARD.md` section 28 (v4.9 proportional
orchestration core). It implements the reference reducer/predicate/finding
semantics over `fixtures/execution-core-v49/` and binds TEST_MATRIX oracles
K01-K10, Frozen Product acceptance items E/F/G/K/L/M/N and the Frozen L2
currentness/JIT/adverse negatives to executable, machine-checkable results.

This is Builder evidence only: it is not independent Validation, not a
scheduler, not a state store, and never a source of gate verdicts.
"""
from __future__ import annotations

import copy
import itertools
import json
import re
import subprocess
import unittest
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = ROOT / "fixtures" / "execution-core-v49"
STANDARD = ROOT / "standards" / "EXECUTION_ARCHITECTURE_STANDARD.md"
REFERENCE = ROOT / "references" / "PROPORTIONAL_ORCHESTRATION_REFERENCE.md"
ASSURANCE_STD = ROOT / "standards" / "ASSURANCE_PLAN_STANDARD.md"
RELEASE_STD = ROOT / "standards" / "RELEASE_STANDARD.md"
PRD = ROOT / "docs" / "implementation" / "4.9.0" / "PRD.md"
L2 = ROOT / "docs" / "implementation" / "4.9.0" / "L2_ARCHITECTURE_EVIDENCE.md"
REGISTRY = ROOT / "registries" / "state-dimensions-v1.json"

BASE_SHA = "1fa88bc1a54970af79ce506a056c2ae5e3203be8"
BASE_TREE = "0a261a6227676a046e532f20f497c576f25a5916"
PACK_HEAD_SHA = "4fb3363e2793b8ce608c05ba38c83481e9309a45"
FROZEN_PRD_BLOB = "a8ec7030a14337a4c2dca853dc474e965679d610"
FROZEN_L2_BLOB = "bd41ea0175b459a6a490fd37ad579e429a58a1c3"
FROZEN_DAG_V02_BLOB = "b9fe0cc7089f64929b4bcf45f7230d950e864db2"

WRITE_SET = (
    "standards/EXECUTION_ARCHITECTURE_STANDARD.md",
    "references/PROPORTIONAL_ORCHESTRATION_REFERENCE.md",
    "scripts/test_v49_execution_core.py",
    "fixtures/execution-core-v49/",
)

READ_ONLY_DEPS = (
    "standards/ASSURANCE_PLAN_STANDARD.md",
    "schemas/role-execution-profile-v1.schema.json",
    "registries/state-dimensions-v1.json",
    "schemas/agent-capability-profile-v1.schema.json",
)

# T-011 re-bind (CF-V49-02 #745@5992918366; classification #831@5994177360, K08):
# schemas/dispatch.schema.json is the T-008 DAG-owned surface, legally mutated
# after this lane's base (optional assurance_currentness_ref / role_profile_ref /
# jit_phase_ref additions; the compatibility record
# references/EXECUTION_CONTRACT_REFS_V49_COMPATIBILITY.json pins baseline
# 4607f6cb@base -> candidate 7259cb35). The stale "unchanged since base" pin is
# re-bound to an exact current-blob identity pin below; pin constant only —
# any further mutation of the surface still fails, zero other assertion change.
#
# Post-recovery recompose re-bind (#805 POST_RECOVERY_EXACT_RECOMPOSE, #745):
# the recovery-integrated main merge (4c632256) legally carries the recovered
# v4.6 dispatch wiring (+2 optional array fields intent_assumption_refs /
# skill_metadata_refs, composed as a field union with the T-008 ref fields).
# The pin is re-bound to the exact current composed blob; pin constant only —
# any further mutation of the surface still fails, zero other assertion change.
READ_ONLY_DEPS_REBOUND_BLOBS = {
    "schemas/dispatch.schema.json": "123a66223f6dea42966c4a181dae3cc0776c3ba3",
}

PLANNING_PATHS = tuple(
    f".agent/execution/T-007/{name}"
    for name in (
        "MANIFEST.yaml",
        "EXECUTION_CONTRACT.md",
        "IMPLEMENTATION_MAP.md",
        "TEST_MATRIX.yaml",
        "FAILURE_MATRIX.yaml",
        "REVIEW_CHECKLIST.md",
    )
)

WORKFLOW_STATES = {
    "planned", "ready", "claimed", "implementing", "review-ready", "reviewing",
    "changes-requested", "validation-needed", "merge-ready", "blocked", "done",
}
GATE_STATES = {"PASS", "FAIL", "BLOCKED", "NOT_RUN", "NOT_APPLICABLE"}

BOUND_COMPONENT_KEYS = (
    "subject_identity_ref",
    "owner_authority_digest",
    "proof_input_digest",
    "task_pack_digest",
    "release_decision_digest",
    "unresolved_finding_digest",
)


# ---------------------------------------------------------------------------
# fixture / repository helpers
# ---------------------------------------------------------------------------

def load_fixture(name: str) -> dict:
    return json.loads((FIXTURE_DIR / name).read_text(encoding="utf-8"))


def canonical(value) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def shuffled(value):
    """Return a copy whose dict key order is deterministically reversed."""
    if isinstance(value, dict):
        return {k: shuffled(v) for k, v in sorted(value.items(), reverse=True)}
    if isinstance(value, list):
        return [shuffled(v) for v in reversed(value)]
    return value


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=True, capture_output=True, text=True
    ).stdout.strip()


def git_blob_sha(rev: str, rel_path: str) -> str:
    return git("rev-parse", f"{rev}:{rel_path}")


def git_blob_text(rev: str, rel_path: str) -> str:
    return git("show", f"{rev}:{rel_path}")


def github_anchors(text: str) -> set[str]:
    """GitHub-style heading anchors: lowercase, punctuation stripped, spaces -> dashes."""
    anchors = set()
    for line in text.splitlines():
        match = re.match(r"^(#+) (.+)$", line)
        if match is None:
            continue
        segment = match.group(2).strip()
        segment = segment.lower()
        segment = re.sub(r"[^\w\- ]", "", segment)
        segment = segment.replace(" ", "-")
        anchors.add(segment)
    return anchors


# ---------------------------------------------------------------------------
# reference engine: deterministic reducer / predicate semantics (standard §28)
# ---------------------------------------------------------------------------

def findings_digest(findings: list[dict]) -> str:
    """Digest over the CURRENT unresolved-finding set (owner: ASSURANCE_PLAN §12/§13)."""
    unresolved = sorted(f["finding_id"] for f in findings if f["state"] == "UNRESOLVED")
    return "findings:" + "|".join(unresolved)


def plan_currentness(facts: dict) -> tuple[str, list[str]]:
    """Recompute the assurance-plan binding state from current durable facts (§28.1).

    Returns (CURRENT|STALE|UNKNOWN, drift keys). The unresolved-finding digest is
    always recomputed from the facts' unresolved set; a stored value is never
    trusted (no stale latch).
    """
    bound = facts["plan_binding"]["bound_components"]
    current = {
        key: facts["current_dimensions"].get(key) for key in BOUND_COMPONENT_KEYS
    }
    current["unresolved_finding_digest"] = findings_digest(facts["unresolved_findings"])
    unknown: list[str] = []
    stale: list[str] = []
    for key in BOUND_COMPONENT_KEYS:
        if key not in bound or bound[key] is None:
            unknown.append(key)
        elif current[key] is None:
            unknown.append(key)
        elif bound[key] != current[key]:
            stale.append(key)
    if unknown:
        return "UNKNOWN", sorted(unknown)
    if stale:
        return "STALE", sorted(stale)
    return "CURRENT", []


def lineage_posture(facts: dict) -> tuple[str, list[str]]:
    """P2 lineage currentness over required predecessor-owned surfaces (§28.2)."""
    stale: list[str] = []
    unknown: list[str] = []
    failed: list[str] = []
    for ref in facts["lineage_refs"]:
        if ref["status"] == "INTEGRATED_CURRENT":
            continue
        if ref["status"] == "STALE":
            stale.append(ref["surface_ref"])
        elif ref["status"] == "UNKNOWN":
            unknown.append(ref["surface_ref"])
        else:
            failed.append(ref["surface_ref"])
    if failed:
        return "BLOCKED", sorted(failed)
    if stale or unknown:
        return "WAITING_LINEAGE", sorted(stale + unknown)
    return "CURRENT", []


def waiting_lineage_projection(facts: dict) -> dict | None:
    """Derived non-dispatch projection (§28.3). None when lineage is current."""
    posture, reasons = lineage_posture(facts)
    if posture != "WAITING_LINEAGE":
        return None
    return {
        "posture": "WAITING_LINEAGE",
        "reasons": reasons,
        "dispatchable": False,
        "claimable": False,
        "workflow_state": None,
        "gate_verdict": None,
    }


def jit_verdict(phase: dict, facts: dict) -> str:
    """Legal JIT phase predicate in fixed evaluation order (§28.2, reference §3)."""
    deps = phase["dependency_state"]
    if deps == "PENDING":
        return "BLOCKED"
    if deps == "UNKNOWN":
        return "WAITING_LINEAGE"
    posture, _reasons = lineage_posture(facts)
    if posture == "WAITING_LINEAGE":
        return "WAITING_LINEAGE"
    if posture == "BLOCKED":
        return "BLOCKED"
    proof = phase["envelope_proof"]
    if proof["declared_in"] is None:
        return "BLOCKED"
    conditions = proof["envelope_conditions"]
    # Key names the violating property: True = violation present, None = unprovable,
    # False = condition holds. Any violation or unprovable condition fails closed.
    if any(value is True or value is None for value in conditions.values()):
        return "BLOCKED"
    if facts["composite_admission"]["state"] != "AVAILABLE":
        return "BLOCKED"
    return "READY"


def resolve_eligibility(candidate: dict) -> str:
    """§27.2 tri-state hard filters with §28.4 Role Profile hard predicates wired in."""
    hard = candidate["hard_predicates"]
    if any(value is False for value in hard.values()):
        return "INELIGIBLE"
    if any(value is None for value in hard.values()):
        return "UNKNOWN"
    profile = candidate["profile"]
    if profile["projection_state"] in {"BLOCKED_SOURCE_AUTHORITY_CONFLICT", "BLOCKED_SOURCE_REF_UNRESOLVED"}:
        return "INELIGIBLE"
    if profile["eligibility_predicates_pass"] is False:
        return "INELIGIBLE"
    if profile["eligibility_predicates_pass"] is None:
        return "UNKNOWN"
    if not profile["claim_policy_ref_resolves"]:
        return "INELIGIBLE"
    return "ELIGIBLE"


def rank_eligible(candidates: list[dict]) -> list[str]:
    """Hard filters BEFORE ranking: only ELIGIBLE choices may enter ranking (§27.2)."""
    eligible = [c for c in candidates if resolve_eligibility(c) == "ELIGIBLE"]
    return [c["candidate_id"] for c in sorted(eligible, key=lambda c: c["rank"])]


def reduce(facts: dict) -> dict:
    """Deterministic pure projection over one fact plane (§28.6). No latch."""
    plan_state, plan_drift = plan_currentness(facts)
    waiting = waiting_lineage_projection(facts)
    phases = facts.get("phases", {})
    verdicts = {phase_id: jit_verdict(phase, facts) for phase_id, phase in phases.items()}
    blockers = sorted(
        f["finding_id"]
        for f in facts["unresolved_findings"]
        if f["state"] == "UNRESOLVED" and f.get("severity") == "blocker"
    )
    return {
        "plan_currentness": plan_state,
        "plan_drift_keys": plan_drift,
        "lineage": lineage_posture(facts)[0],
        "waiting_lineage": waiting,
        "jit_verdicts": verdicts,
        "unresolved_finding_digest": findings_digest(facts["unresolved_findings"]),
        "unresolved_blockers": blockers,
        "dispatchable": plan_state == "CURRENT" and waiting is None,
    }


def dispatch_materialize(facts: dict) -> dict:
    """Dispatch reservation transition: consumes §28.1 currentness before acting."""
    projection = reduce(facts)
    if projection["plan_currentness"] != "CURRENT":
        return {
            "outcome": f"BLOCKED_PLAN_BINDING_{projection['plan_currentness']}",
            "dispatch": None,
            "dispatches_created": 0,
            "recompute_required": True,
        }
    if projection["waiting_lineage"] is not None:
        return {
            "outcome": "WAITING_LINEAGE_NO_DISPATCH",
            "dispatch": None,
            "dispatches_created": 0,
            "recompute_required": False,
        }
    return {
        "outcome": "MATERIALIZED",
        "dispatch": {
            "work_item": facts["work_item"]["work_item_id"],
            "plan_binding_digest": facts["plan_binding"]["binding_digest"],
            "role": "builder",
        },
        "dispatches_created": 1,
        "recompute_required": False,
    }


@dataclass(frozen=True)
class ClaimState:
    """Serialized claim-key state (§11/§11.1). Immutable; only ACCEPTED advances it."""
    generation: int = 0
    accepted: tuple[str, ...] = ()
    protected_key: tuple[str, ...] = ()

    def with_accept(self, operator: str) -> "ClaimState":
        return ClaimState(
            generation=self.generation + 1,
            accepted=self.accepted + (operator,),
            protected_key=self.protected_key,
        )


def claim_attempt(
    state: ClaimState, facts: dict, operator: str, expected_generation: int
) -> tuple[str, ClaimState]:
    """One serialized claim admission; re-reads current facts immediately before CAS."""
    projection = reduce(facts)  # §28.1/§28.6: recompute, never a cached latch
    if projection["plan_currentness"] != "CURRENT":
        return "STALE_PLAN_BINDING_RECOMPUTE", state
    if projection["waiting_lineage"] is not None:
        return "NOT_DISPATCHABLE_WAITING_LINEAGE", state
    if operator in state.accepted:
        return "IDEMPOTENT_RESUME", state
    if state.accepted:
        return "DUPLICATE_INCOMPATIBLE_CLAIM", state
    if expected_generation != state.generation:
        return "STALE_GENERATION", state
    return "ACCEPTED", state.with_accept(operator)


def run_race(ordering: dict, protected_key: tuple[str, ...]) -> tuple[list[tuple[str, str]], ClaimState]:
    state = ClaimState(protected_key=protected_key)
    outcomes: list[tuple[str, str]] = []
    for step in ordering["steps"]:
        facts = load_fixture(step["facts_fixture"])
        if step["inject_drift"]:
            facts = load_fixture("facts_plan_drift.json")
        outcome, state = claim_attempt(state, facts, step["operator"], step["expected_generation"])
        outcomes.append((step["operator"], outcome))
    return outcomes, state


def merge_ready(facts: dict, state: ClaimState, operator: str) -> tuple[bool, str]:
    """Merge/merge-ready transition: §28.1 recheck + §11 canonical claim + §28.5 blockers."""
    projection = reduce(facts)
    if projection["plan_currentness"] != "CURRENT":
        return False, f"PLAN_BINDING_{projection['plan_currentness']}"
    if operator not in state.accepted:
        return False, "NO_ACCEPTED_CLAIM"
    if projection["unresolved_blockers"]:
        return False, "UNRESOLVED_BLOCKING_FINDINGS"
    return True, "MERGE_READY"


def reduce_unresolved(findings: list[dict]) -> list[str]:
    """§28.5 carry-forward: findings leave the set only via sufficient dispositions."""
    surviving = []
    for finding in findings:
        disposition = finding.get("disposition")
        closed = (
            finding["state"] in {"RESOLVED", "NOT_APPLICABLE_TO_SUCCESSOR"}
            and isinstance(disposition, dict)
            and disposition.get("evidence_refs")
            and disposition.get("owning_rule_basis")
        )
        if not closed:
            surviving.append(finding["finding_id"])
    return sorted(surviving)


def apply_chronology(findings: list[dict], chronology: list[dict]) -> list[str]:
    """Verdict chronology (new reviewer/new PASS/new SHA) can NEVER close a finding."""
    del chronology  # deliberately unused: no chronology input may affect the set
    return reduce_unresolved(findings)


def route_re_review(request: dict) -> str:
    """§28.5 no-review-shopping routing. Fail-closed."""
    successor = request.get("successor_subject_ref")
    authorized_by = request.get("authorized_repair_path")
    disposition = request.get("owning_authority_disposition")
    if successor and authorized_by == "authorized_mutable_repair":
        return "ALLOWED_SUCCESSOR_REVIEW"
    if disposition and disposition.get("explicit") and disposition.get("owning_authority"):
        return "ALLOWED_DISPOSITIONED_REVIEW"
    return "REJECTED_REVIEW_SHOPPING"


def transfer_pass(old_pass: dict, successor_subject: str) -> str:
    """L2 negative: stale PASS -> successor PASS without an owner transfer rule."""
    if old_pass["subject_ref"] == successor_subject and old_pass["current"] is True:
        return "TRANSFERRED_CURRENT"
    return "REJECTED_HISTORICAL_ONLY_NO_TRANSFER_RULE"


def classify_topology_change(proposal: dict) -> str:
    """§28.2: material topology change routes to v4.3 governance, never a JIT phase."""
    if proposal["action"] == "new_task":
        return "V43_MUTATION_ADD"
    if proposal["action"] == "add_dependency":
        return "V43_MUTATION_ADD_DEPENDENCY"
    if proposal["action"] == "remove_dependency":
        return "V43_MUTATION_REMOVE_DEPENDENCY"
    return "V43_MUTATION_CLASS_REQUIRED"


def reduction_decision(proof_state: str, model_judgment: str) -> str:
    """Product M: model reasoning can never authorize an unproven reduction."""
    if proof_state == "PROVEN_TRUE":
        return "REDUCED_PER_OWNER_RULE"
    return "STRONGER_EXISTING_PATH_OR_BLOCKED"


# ---------------------------------------------------------------------------
# kernel tests K01-K10
# ---------------------------------------------------------------------------

class ExecutionCoreKernel(unittest.TestCase):
    maxDiff = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.standard_text = STANDARD.read_text(encoding="utf-8")
        cls.reference_text = REFERENCE.read_text(encoding="utf-8")
        cls.assurance_text = ASSURANCE_STD.read_text(encoding="utf-8")
        cls.release_text = RELEASE_STD.read_text(encoding="utf-8")
        cls.prd_text = PRD.read_text(encoding="utf-8")
        cls.l2_text = L2.read_text(encoding="utf-8")
        cls.owner_refs = load_fixture("owner_refs.json")
        cls.facts_current = load_fixture("facts_current.json")
        cls.facts_drift = load_fixture("facts_plan_drift.json")
        cls.facts_stale = load_fixture("facts_lineage_stale.json")
        cls.facts_successor = load_fixture("facts_successor.json")
        cls.candidates = load_fixture("candidates.json")["candidates"]
        cls.races = load_fixture("claim_races.json")
        cls.phase_table = load_fixture("phase_table.json")

    # ---------- K01: currentness consumed at Dispatch / Claim / merge ----------

    def test_k01_currentness_consumed_at_dispatch_claim_merge(self) -> None:
        # Dispatch materialization consumes the plan binding.
        ok = dispatch_materialize(self.facts_current)
        self.assertEqual("MATERIALIZED", ok["outcome"])
        drifted = dispatch_materialize(self.facts_drift)
        self.assertEqual("BLOCKED_PLAN_BINDING_STALE", drifted["outcome"])
        self.assertEqual(0, drifted["dispatches_created"])
        self.assertTrue(drifted["recompute_required"])

        # Claim admission recomputes: a finding after Dispatch blocks the Claim.
        state = ClaimState()
        outcome, state = claim_attempt(state, self.facts_current, "op-1", 0)
        self.assertEqual("ACCEPTED", outcome)
        outcome, unchanged = claim_attempt(state, self.facts_drift, "op-2", 1)
        self.assertEqual("STALE_PLAN_BINDING_RECOMPUTE", outcome)
        self.assertEqual(state, unchanged)  # no partial publication

        # Merge transition rechecks; drift blocks the merge of an accepted claim.
        ready, reason = merge_ready(self.facts_current, state, "op-1")
        self.assertTrue(ready)
        ready, reason = merge_ready(self.facts_drift, state, "op-1")
        self.assertFalse(ready)
        self.assertEqual("PLAN_BINDING_STALE", reason)

        # A stale latch cannot survive a recompute point: cached CURRENT/READY from
        # the old fact plane has zero weight against recomputed derived state.
        cached = reduce(self.facts_current)
        live = reduce(self.facts_drift)
        self.assertEqual("CURRENT", cached["plan_currentness"])
        self.assertEqual("STALE", live["plan_currentness"])
        self.assertIn("unresolved_finding_digest", live["plan_drift_keys"])
        self.assertEqual(reduce(self.facts_current), cached)

    # ---------- K02: legal JIT phase predicate truth table ----------

    def expected_jit_verdict(self, deps: str, lineage: str, proof: dict, admission: str) -> str:
        if deps == "PENDING":
            return "BLOCKED"
        if deps == "UNKNOWN":
            return "WAITING_LINEAGE"
        if lineage in ("STALE", "UNKNOWN"):
            return "WAITING_LINEAGE"
        if lineage == "BLOCKED":
            return "BLOCKED"
        if proof["declared_in"] is None:
            return "BLOCKED"
        if any(value is True or value is None for value in proof["envelope_conditions"].values()):
            return "BLOCKED"
        if admission != "AVAILABLE":
            return "BLOCKED"
        return "READY"

    def test_k02_jit_predicate_truth_table_is_complete(self) -> None:
        table = self.phase_table
        combos = list(
            itertools.product(
                table["dependency_states"],
                table["lineage_states"],
                table["envelope_proofs"],
                table["admission_states"],
            )
        )
        self.assertEqual(135, len(combos))
        checked = 0
        for deps, lineage, proof, admission in combos:
            facts = copy.deepcopy(self.facts_current)
            facts["lineage_refs"] = [
                {"surface_ref": "surface:X", "status": {"CURRENT": "INTEGRATED_CURRENT", "STALE": "STALE", "UNKNOWN": "UNKNOWN", "BLOCKED": "FAILED"}[lineage]}
            ]
            facts["composite_admission"] = {"mode": "SINGLE_WRITER_ADMISSION", "state": admission}
            phase = {"dependency_state": deps, "envelope_proof": proof}
            self.assertEqual(
                self.expected_jit_verdict(deps, lineage, proof, admission),
                jit_verdict(phase, facts),
                (deps, lineage, proof["proof_id"], admission),
            )
            checked += 1
        self.assertEqual(135, checked)

        # READY requires everything; the undeclared phase is never in-envelope (L2).
        facts = copy.deepcopy(self.facts_current)
        undeclared = {"dependency_state": "DONE", "envelope_proof": table["envelope_proofs"][2]}
        self.assertEqual("BLOCKED", jit_verdict(undeclared, facts))

    # ---------- K03: WAITING_LINEAGE derived non-dispatch projection ----------

    def test_k03_waiting_lineage_is_derived_non_dispatch_projection(self) -> None:
        projection = reduce(self.facts_stale)
        waiting = projection["waiting_lineage"]
        self.assertIsNotNone(waiting)
        self.assertEqual("WAITING_LINEAGE", waiting["posture"])
        self.assertIn("surface:LG47_REGISTRY", waiting["reasons"])
        # Not a workflow state, not a gate verdict (registry F17-F19).
        self.assertNotIn(waiting["posture"], WORKFLOW_STATES)
        self.assertNotIn(waiting["posture"], GATE_STATES)
        self.assertIsNone(waiting["workflow_state"])
        self.assertIsNone(waiting["gate_verdict"])
        self.assertFalse(waiting["dispatchable"])
        self.assertFalse(waiting["claimable"])

        # F11: dependency completion never confers lineage currentness.
        self.assertEqual("DONE", self.facts_stale["work_item"]["dependencies"][0]["state"])
        self.assertEqual("WAITING_LINEAGE", projection["lineage"])

        # Product K: known sequence block => no dispatch is created at all.
        materialization = dispatch_materialize(self.facts_stale)
        self.assertEqual("WAITING_LINEAGE_NO_DISPATCH", materialization["outcome"])
        self.assertEqual(0, materialization["dispatches_created"])

        # No claim can be admitted from the wait posture.
        outcome, state = claim_attempt(ClaimState(), self.facts_stale, "op-1", 0)
        self.assertEqual("NOT_DISPATCHABLE_WAITING_LINEAGE", outcome)
        self.assertEqual(ClaimState(), state)

        # Recompute drops the posture when the surface becomes integrated/current.
        repaired = copy.deepcopy(self.facts_stale)
        repaired["lineage_refs"][1]["status"] = "INTEGRATED_CURRENT"
        repaired["lineage_refs"][1]["integrated_ref"] = "mirror@1fa88bc1"
        self.assertIsNone(reduce(repaired)["waiting_lineage"])

    # ---------- K04: Role Profile hard predicates wired before ranking ----------

    def test_k04_hard_predicates_before_ranking_and_profile_wiring(self) -> None:
        ranked = rank_eligible(self.candidates)
        self.assertEqual(["c-eligible-low-rank"], ranked)
        # An ineligible profile cannot be ranked into dispatch by any ordering.
        self.assertEqual("INELIGIBLE", resolve_eligibility(self.candidates[1]))  # profile conflict, rank 1
        self.assertEqual("INELIGIBLE", resolve_eligibility(self.candidates[2]))  # independence fail, rank 2
        self.assertEqual("UNKNOWN", resolve_eligibility(self.candidates[3]))  # ambiguous predicate
        self.assertEqual("INELIGIBLE", resolve_eligibility(self.candidates[4]))  # stale profile sources
        self.assertEqual("INELIGIBLE", resolve_eligibility(self.candidates[5]))  # free claim switch
        self.assertEqual("INELIGIBLE", resolve_eligibility(self.candidates[6]))  # reviewer selector conflict

        # Ranking input cannot rescue a blocked candidate: reorder ranks arbitrarily.
        reordered = [dict(c, rank=0) for c in self.candidates]
        self.assertEqual(["c-eligible-low-rank"], rank_eligible(reordered))

        # UNKNOWN fails closed even against otherwise perfect facts.
        unknown = dict(self.candidates[0], hard_predicates=dict(self.candidates[0]["hard_predicates"], security_authorized=None))
        self.assertEqual("UNKNOWN", resolve_eligibility(unknown))

        # Profile presence alone never satisfies a Claim predicate: no route from an
        # ELIGIBLE projection to an accepted claim exists except serialized admission.
        self.assertEqual(ClaimState(), ClaimState())

    # ---------- K05: carry-forward + no-review-shopping routing ----------

    def test_k05_carry_forward_and_no_review_shopping(self) -> None:
        # Product N: R1 blocker stands against any R2 PASS on the same subject.
        shopping = copy.deepcopy(self.facts_drift)
        shopping["verdict_chronology"].append(
            {"reviewer": "R2", "subject_ref": "issue:900", "verdict": "PASS", "evidence_ref": "review-evidence:R2-S1"}
        )
        self.assertEqual(["F-101"], apply_chronology(shopping["unresolved_findings"], shopping["verdict_chronology"]))
        self.assertEqual(["F-101"], reduce_unresolved(shopping["unresolved_findings"]))
        self.assertEqual(
            "REJECTED_REVIEW_SHOPPING",
            route_re_review({"request": "same-subject redispatch to a new reviewer for PASS"}),
        )

        # Authorized repair => successor review is allowed; findings carry forward.
        self.assertEqual(
            "ALLOWED_SUCCESSOR_REVIEW",
            route_re_review({
                "successor_subject_ref": "issue:900@S2",
                "authorized_repair_path": "authorized_mutable_repair",
            }),
        )
        carried = reduce_unresolved(self.facts_successor["unresolved_findings"])
        self.assertEqual(["F-102"], carried)  # F-101 RESOLVED with evidence+basis; F-102 STILL_PRESENT

        # Insufficient dispositions keep findings: STILL_PRESENT, missing evidence, missing rule basis.
        weak = [
            {"finding_id": "F-a", "state": "STILL_PRESENT", "disposition": {"evidence_refs": ["e"], "owning_rule_basis": "b"}},
            {"finding_id": "F-b", "state": "RESOLVED", "disposition": {"evidence_refs": [], "owning_rule_basis": "b"}},
            {"finding_id": "F-c", "state": "RESOLVED", "disposition": {"evidence_refs": ["e"], "owning_rule_basis": None}},
            {"finding_id": "F-d", "state": "RESOLVED", "disposition": None},
        ]
        self.assertEqual(["F-a", "F-b", "F-c", "F-d"], reduce_unresolved(weak))
        self.assertEqual(
            "ALLOWED_DISPOSITIONED_REVIEW",
            route_re_review({"owning_authority_disposition": {"explicit": True, "owning_authority": "review-owner"}}),
        )

        # Aggregation ownership stays with Adversarial Review: an unresolved blocker
        # blocks merge; closing it changes the digest => binding STALE => recompute.
        state = ClaimState()
        outcome, state = claim_attempt(state, self.facts_successor, "op-1", 0)
        self.assertEqual("ACCEPTED", outcome)
        ready, reason = merge_ready(self.facts_successor, state, "op-1")
        self.assertFalse(ready)
        self.assertEqual("UNRESOLVED_BLOCKING_FINDINGS", reason)
        resolved = copy.deepcopy(self.facts_successor)
        resolved["unresolved_findings"][1]["state"] = "RESOLVED"
        projection = reduce(resolved)
        self.assertEqual([], projection["unresolved_blockers"])
        self.assertEqual("STALE", projection["plan_currentness"])  # digest drift forces recompute

    # ---------- K06: deterministic recompute on currentness drift ----------

    def test_k06_deterministic_recompute_no_hidden_latch(self) -> None:
        base_projection = reduce(self.facts_current)
        for _ in range(3):
            self.assertEqual(base_projection, reduce(self.facts_current))
        # Interleaving other fact planes leaves no residue (pure function, no latch).
        self.assertEqual(base_projection, reduce(self.facts_current))
        self.assertEqual(reduce(self.facts_drift), reduce(self.facts_drift))
        self.assertEqual(base_projection, reduce(self.facts_current))

        # Key-order independence: same facts in any JSON ordering => same projection.
        self.assertEqual(base_projection, reduce(shuffled(copy.deepcopy(self.facts_current))))
        self.assertEqual(reduce(self.facts_drift), reduce(shuffled(copy.deepcopy(self.facts_drift))))

        # Drift replay converges: current -> drift -> current yields identical state.
        replay = reduce(self.facts_current)
        drifted = reduce(self.facts_drift)
        self.assertNotEqual(replay, drifted)
        self.assertEqual(replay, reduce(self.facts_current))

        # Deterministic race replay: the same ordering always yields the same outcome.
        protected_key = tuple(self.races["protected_claim_key"])
        for ordering in self.races["orderings"]:
            first = run_race(ordering, protected_key)
            second = run_race(ordering, protected_key)
            self.assertEqual(first, second, ordering["ordering_id"])

    # ---------- K07: race/drift fail-closed simulations ----------

    def test_k07_race_and_drift_fail_closed(self) -> None:
        protected_key = tuple(self.races["protected_claim_key"])
        for ordering in self.races["orderings"]:
            outcomes, final = run_race(ordering, protected_key)
            with self.subTest(ordering=ordering["ordering_id"]):
                accepted = [op for op, outcome in outcomes if outcome == "ACCEPTED"]
                self.assertEqual(ordering["expected"]["accepted"], accepted)
                for op, outcome in outcomes:
                    expected_reason = ordering["expected"]["rejection_reasons"].get(op)
                    if expected_reason is not None:
                        self.assertEqual(expected_reason, outcome)
                self.assertLessEqual(len(final.accepted), 1)
                # Fail-closed invariant: never both-claim, never a silently lost claim.
                if ordering["ordering_id"] == "race-C-drift-races-the-admission-itself":
                    self.assertEqual([], accepted)  # drift during admission => zero claims
                if ordering["ordering_id"] == "race-A-both-before-drift":
                    self.assertEqual(1, len(final.accepted))  # exactly one canonical claim

        # Every rejection publishes nothing: the serialized state is untouched.
        state = ClaimState()
        _, untouched = claim_attempt(state, self.facts_stale, "op-1", 0)
        self.assertEqual(state, untouched)
        # Duplicate exclusion is decided from durable claim facts, not labels.
        _, advanced = claim_attempt(state, self.facts_current, "op-1", 0)
        self.assertEqual(("op-1",), advanced.accepted)
        outcome, untouched = claim_attempt(advanced, self.facts_current, "op-2", 0)
        self.assertEqual("DUPLICATE_INCOMPATIBLE_CLAIM", outcome)
        self.assertEqual(advanced, untouched)

    # ---------- K08: additive composition; no second scheduler ----------

    def test_k08_standard_composes_additively_and_keeps_single_lifecycle(self) -> None:
        # Historical sections §1-§27 are byte-identical to the base; §28 is appended.
        base_text = git_blob_text(BASE_SHA, "standards/EXECUTION_ARCHITECTURE_STANDARD.md")
        self.assertTrue(
            self.standard_text.startswith(base_text),
            "v4.0-v4.8 standard content was rewritten; v4.9 sections must be additive",
        )
        self.assertIn("\n## 28. v4.9 proportional orchestration core\n", self.standard_text)
        for anchor in self.owner_refs["standard_sections"].values():
            self.assertIn(anchor.rsplit("#", 1)[1], github_anchors(self.standard_text), anchor)
        # Canonical vocabularies and the only Claim lifecycle are untouched.
        for token in (
            "READY, Dispatch, and Claim remain canonical",
            "QUEUED → DELIVERED → ACKNOWLEDGED/RUNNING → DONE",
            "All hard predicates are evaluated before ranking",
        ):
            self.assertIn(token, self.standard_text)
        # Reference doc exists and covers the owned surfaces without new authority.
        for token in (
            "reducer state model",
            "JIT phase predicate evaluation",
            "currentness recheck points",
            "WAITING_LINEAGE projection rules",
            "no-review-shopping routing",
            "Normative owner: `standards/EXECUTION_ARCHITECTURE_STANDARD.md` §28",
        ):
            self.assertIn(token, self.reference_text)

    def test_k08_consumed_contract_refs_resolve_at_candidate(self) -> None:
        refs = self.owner_refs["consumed_contracts"]
        assurance_anchors = github_anchors(self.assurance_text)
        self.assertIn(refs["assurance_currentness"].rsplit("#", 1)[1], assurance_anchors)
        self.assertIn(refs["assurance_carry_forward"].rsplit("#", 1)[1], assurance_anchors)
        release_anchors = github_anchors(self.release_text)
        self.assertIn(refs["release_applicability_owner"].rsplit("#", 1)[1], release_anchors)
        plan_schema = json.loads((ROOT / "schemas/assurance-plan-v2.schema.json").read_text(encoding="utf-8"))
        self.assertIn("currentness_binding", plan_schema["properties"])
        self.assertIn("finding_carry_forward_policy", plan_schema["properties"])
        profile_schema = json.loads((ROOT / "schemas/role-execution-profile-v1.schema.json").read_text(encoding="utf-8"))
        self.assertIn("eligibility_predicate_refs", profile_schema["properties"])
        registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        dims = {d["dimension_id"]: d for d in registry["dimensions"]}
        self.assertIn("waiting_lineage", dims)
        self.assertEqual("standards/EXECUTION_ARCHITECTURE_STANDARD.md", dims["waiting_lineage"]["canonical_owner_ref"])
        self.assertEqual("OWNER_DEFINED", dims["waiting_lineage"]["vocabulary_posture"])
        rule_ids = {r["rule_id"] for r in registry["forbidden_inferences"]}
        for rule_id in self.owner_refs["forbidden_inference_ids"]:
            self.assertIn(rule_id, rule_ids)

    def test_k08_write_set_and_frozen_authority_unchanged(self) -> None:
        # Working tree contains only the four Builder write-set paths.
        changed = set()
        for line in git("status", "--porcelain").splitlines():
            if not line.strip():
                continue
            changed.add(line[2:].strip().strip('"'))
        for path in changed:
            with self.subTest(changed_path=path):
                self.assertTrue(
                    any(path == w or path.startswith(w) for w in WRITE_SET),
                    f"path outside Builder write set: {path}",
                )
        # Frozen Product / L2 / DAG blobs resolve unchanged at the candidate.
        self.assertEqual(FROZEN_PRD_BLOB, git_blob_sha("HEAD", "docs/implementation/4.9.0/PRD.md"))
        self.assertEqual(FROZEN_L2_BLOB, git_blob_sha("HEAD", "docs/implementation/4.9.0/L2_ARCHITECTURE_EVIDENCE.md"))
        self.assertEqual(FROZEN_DAG_V02_BLOB, git_blob_sha("HEAD", "docs/implementation/4.9.0/TASK_DAG.md"))
        # Immutable T-007 planning files are unmutated since the execution pack head.
        for rel_path in PLANNING_PATHS:
            with self.subTest(planning_path=rel_path):
                self.assertEqual(git_blob_sha(PACK_HEAD_SHA, rel_path), git_blob_sha("HEAD", rel_path))
        # Read-only dependency refs are unmutated since the base.
        for rel_path in READ_ONLY_DEPS:
            with self.subTest(read_only=rel_path):
                self.assertEqual(git_blob_sha(BASE_SHA, rel_path), git_blob_sha("HEAD", rel_path))
        # T-011 re-bind: the T-008-mutated dispatch surface is pinned to its
        # exact current DAG-owned blob (see READ_ONLY_DEPS_REBOUND_BLOBS).
        for rel_path, pinned_blob in READ_ONLY_DEPS_REBOUND_BLOBS.items():
            with self.subTest(read_only_rebound=rel_path):
                self.assertEqual(pinned_blob, git_blob_sha("HEAD", rel_path))

    # ---------- K09: Frozen Product acceptance items E/F/G/K/L/M/N ----------

    def prd_anchor(self, item: str) -> str:
        anchor = self.owner_refs["prd_acceptance_anchors"][item]
        self.assertIn(anchor, self.prd_text, f"PRD acceptance anchor missing: {item}")
        return anchor

    def test_k09_product_e_multiple_independent_phases_one_container(self) -> None:
        self.prd_anchor("E")
        facts = copy.deepcopy(self.facts_current)
        facts["phases"] = {
            "PH-impl": {
                "dependency_state": "DONE",
                "envelope_proof": self.phase_table["envelope_proofs"][1],  # IN_PACK
            },
            "PH-review": {
                "dependency_state": "DONE",
                "envelope_proof": self.phase_table["envelope_proofs"][0],  # IN_PLAN
            },
        }
        verdicts = reduce(facts)["jit_verdicts"]
        self.assertEqual({"PH-impl": "READY", "PH-review": "READY"}, verdicts)
        # Independence stays distinguishable per phase: a selector conflict blocks only
        # its own phase admission and never collapses the sibling phase.
        candidates = [copy.deepcopy(self.candidates[0]), self.candidates[6]]
        self.assertEqual(["c-eligible-low-rank"], rank_eligible(candidates))
        self.assertEqual("INELIGIBLE", resolve_eligibility(self.candidates[6]))

    def test_k09_product_f_duplicate_claim_race(self) -> None:
        self.prd_anchor("F")
        ordering = next(o for o in self.races["orderings"] if o["ordering_id"] == "race-A-both-before-drift")
        outcomes, final = run_race(ordering, tuple(self.races["protected_claim_key"]))
        self.assertEqual(1, len(final.accepted))
        self.assertEqual(("op-2", "DUPLICATE_INCOMPATIBLE_CLAIM"), outcomes[1])

    def test_k09_product_g_wrong_role_independence_rejection(self) -> None:
        self.prd_anchor("G")
        # The otherwise-capable top-ranked candidates are ineligible on independence
        # and profile grounds alone; ranking cannot promote them.
        ranked = rank_eligible(self.candidates)
        self.assertNotIn("c-independence-fail-high-rank", ranked)
        self.assertNotIn("c-profile-conflict-high-rank", ranked)
        self.assertNotIn("c-reviewer-selector-conflict", ranked)
        self.assertEqual("INELIGIBLE", resolve_eligibility(self.candidates[2]))

    def test_k09_product_k_known_sequence_block(self) -> None:
        self.prd_anchor("K")
        projection = reduce(self.facts_stale)
        self.assertEqual("WAITING_LINEAGE", projection["waiting_lineage"]["posture"])
        materialization = dispatch_materialize(self.facts_stale)
        self.assertEqual(0, materialization["dispatches_created"])
        self.assertNotEqual("BLOCKED", projection["waiting_lineage"]["posture"])

    def test_k09_product_l_task_dag_scope_protection(self) -> None:
        self.prd_anchor("L")
        facts = copy.deepcopy(self.facts_current)
        facts["phases"] = {
            "PH-invent-concern": {
                "dependency_state": "DONE",
                "envelope_proof": self.phase_table["envelope_proofs"][3],  # VIOLATED
            },
        }
        self.assertEqual("BLOCKED", reduce(facts)["jit_verdicts"]["PH-invent-concern"])
        # A material topology change routes to v4.3 governance, never a phase dispatch.
        self.assertEqual("V43_MUTATION_ADD_DEPENDENCY", classify_topology_change({"action": "add_dependency"}))
        self.assertEqual("V43_MUTATION_ADD", classify_topology_change({"action": "new_task"}))

    def test_k09_product_m_ambiguous_reduction_predicate(self) -> None:
        self.prd_anchor("M")
        self.assertEqual("REDUCED_PER_OWNER_RULE", reduction_decision("PROVEN_TRUE", "model agrees"))
        for proof_state in ("PROVEN_FALSE", "UNKNOWN_OR_AMBIGUOUS", "STALE", "CONTRADICTORY"):
            self.assertEqual(
                "STRONGER_EXISTING_PATH_OR_BLOCKED",
                reduction_decision(proof_state, "model reasons it is safe"),
                proof_state,
            )
        # The ambiguous hard predicate fails closed in eligibility as well.
        self.assertEqual("UNKNOWN", resolve_eligibility(self.candidates[3]))
        self.assertNotIn(self.candidates[3]["candidate_id"], rank_eligible(self.candidates))

    def test_k09_product_n_adverse_review_not_shoppable(self) -> None:
        self.prd_anchor("N")
        shopping = copy.deepcopy(self.facts_drift)
        shopping["verdict_chronology"].append(
            {"reviewer": "R2", "subject_ref": "issue:900", "verdict": "PASS", "evidence_ref": "review-evidence:R2-S1"}
        )
        self.assertEqual(
            apply_chronology(self.facts_drift["unresolved_findings"], self.facts_drift["verdict_chronology"]),
            apply_chronology(shopping["unresolved_findings"], shopping["verdict_chronology"]),
        )
        self.assertEqual(
            "REJECTED_REVIEW_SHOPPING",
            route_re_review({"successor_subject_ref": "issue:900", "authorized_repair_path": "redispatch-same-subject"}),
        )

    # ---------- K10: Frozen L2 currentness/JIT/adverse negatives ----------

    def l2_row(self, row: str) -> None:
        self.assertIn(row, self.l2_text, f"L2 negative row missing: {row}")

    def test_k10_l2_stale_plan_claim_merge_continues_rejected(self) -> None:
        self.l2_row("Assurance Plan stale on new finding/proof/authority -> Claim/merge continues")
        state = ClaimState()
        _, state = claim_attempt(state, self.facts_current, "op-1", 0)
        outcome, _ = claim_attempt(state, self.facts_drift, "op-2", 1)
        self.assertEqual("STALE_PLAN_BINDING_RECOMPUTE", outcome)
        ready, reason = merge_ready(self.facts_drift, state, "op-1")
        self.assertFalse(ready)
        self.assertEqual("PLAN_BINDING_STALE", reason)

    def test_k10_l2_stale_pass_not_successor_pass(self) -> None:
        self.l2_row("stale PASS -> successor PASS")
        stale_pass = {"subject_ref": "issue:900@S1", "current": False, "verdict": "PASS"}
        self.assertEqual("REJECTED_HISTORICAL_ONLY_NO_TRANSFER_RULE", transfer_pass(stale_pass, "issue:900@S2"))
        current_same = {"subject_ref": "issue:900@S2", "current": True, "verdict": "PASS"}
        self.assertEqual("TRANSFERRED_CURRENT", transfer_pass(current_same, "issue:900@S2"))

    def test_k10_l2_r2_pass_cannot_erase_r1_blocker(self) -> None:
        self.l2_row("R1 FAIL -> R2 PASS erases R1 blocker")
        findings = self.facts_drift["unresolved_findings"]
        chronology = [
            {"reviewer": "R1", "verdict": "FAIL"},
            {"reviewer": "R2", "verdict": "PASS"},
        ]
        self.assertEqual(["F-101"], apply_chronology(findings, chronology))

    def test_k10_l2_same_subject_redispatch_is_pass_shopping(self) -> None:
        self.l2_row("same-subject reviewer redispatch -> PASS-shopping")
        self.assertEqual(
            "REJECTED_REVIEW_SHOPPING",
            route_re_review({"subject_ref": "issue:900@S1", "new_reviewer": "R2"}),
        )

    def test_k10_l2_undeclared_jit_phase_never_in_envelope(self) -> None:
        self.l2_row("JIT phase not in Assurance Plan/Task Pack -> treated as in-envelope")
        facts = copy.deepcopy(self.facts_current)
        facts["phases"] = {
            "PH-undeclared": {
                "dependency_state": "DONE",
                "envelope_proof": self.phase_table["envelope_proofs"][2],
            },
        }
        self.assertEqual("BLOCKED", reduce(facts)["jit_verdicts"]["PH-undeclared"])

    def test_k10_l2_waiting_lineage_never_canonical_state(self) -> None:
        self.l2_row("WAITING_LINEAGE -> canonical Issue state invented")
        waiting = waiting_lineage_projection(self.facts_stale)
        self.assertNotIn(waiting["posture"], WORKFLOW_STATES)
        self.assertNotIn(waiting["posture"], GATE_STATES)
        registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        dimension_ids = {d["dimension_id"] for d in registry["dimensions"]}
        self.assertNotIn("state:blocked", dimension_ids)
        self.assertFalse(dimension_ids & WORKFLOW_STATES)

    def test_k10_l2_unintegrated_predecessor_blocks_dependent_execution(self) -> None:
        self.l2_row("predecessor not integrated -> generic compatibility rebind starts dependent execution")
        projection = reduce(self.facts_stale)
        self.assertIsNotNone(projection["waiting_lineage"])
        materialization = dispatch_materialize(self.facts_stale)
        self.assertEqual(0, materialization["dispatches_created"])
        outcome, state = claim_attempt(ClaimState(), self.facts_stale, "op-1", 0)
        self.assertEqual("NOT_DISPATCHABLE_WAITING_LINEAGE", outcome)
        self.assertEqual(ClaimState(), state)


class StandardBindingTests(unittest.TestCase):
    """Bindings between the normative text and the kernel vocabulary."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.standard_text = STANDARD.read_text(encoding="utf-8")

    def test_standard_section_28_binds_kernel_semantics(self) -> None:
        for token in (
            "Assurance Plan currentness consumption at architecture-owned transitions",
            "Legal JIT phase predicate",
            "WAITING_LINEAGE derived non-dispatch projection",
            "Role Profile hard predicates in v4.8 eligibility",
            "Adverse-finding carry-forward and no-review-shopping routing",
            "Deterministic recompute on currentness drift; race/drift fail-closed",
            "Acceptance bindings",
            "all of P1-P3 (with E1 or E2, and no envelope violation)  => READY",
            "any input missing/unknown, or P2 lineage not current      => WAITING_LINEAGE (derived, §28.3)",
            "NON_DISPATCHABLE   no Dispatch is materialized from it; no Claim can be admitted from it",
            "same-subject re-dispatch/re-review merely to obtain PASS        => rejected",
            "no rule below creates a second scheduler, second claim lifecycle, runtime authority store",
        ):
            self.assertIn(token, self.standard_text, token)

    def test_kernel_vocabulary_matches_standard(self) -> None:
        for verdict in ("READY", "WAITING_LINEAGE", "BLOCKED"):
            self.assertIn(verdict, self.standard_text)
        for state in ("CURRENT", "STALE", "UNKNOWN"):
            self.assertIn(state, self.standard_text)
        self.assertIn("finding_carry_forward_policy=unresolved-valid-findings-carry-forward", self.standard_text)
        self.assertIn("registries/state-dimensions-v1.json", self.standard_text)
        self.assertIn("schemas/role-execution-profile-v1.schema.json", self.standard_text)


if __name__ == "__main__":
    import sys

    suite = unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    raise SystemExit(0 if result.wasSuccessful() else 1)
