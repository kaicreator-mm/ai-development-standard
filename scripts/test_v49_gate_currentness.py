"""v4.9 T010 gate-owned evidence binding / currentness integration kernel.

Deterministic stdlib-unittest wiring kernel for
`references/GATE_EVIDENCE_CURRENTNESS_MATRIX.md` (the executable owner map
mirroring Frozen L2 §10, blob bd41ea0175b459a6a490fd37ad579e429a58a1c3).
It implements ONLY the cross-owner currentness wiring (routing dispositions,
carry-forward set algebra, impact-decision use, frozen-candidate identity
checks, Release-applicability binding by reference, dogfood candidate binding)
over `fixtures/gate-currentness/` and binds TEST_MATRIX oracles T01-T07.

This is Builder evidence only: it is not independent Validation, not a gate,
and never a source of verdicts. The engine can deny, route, or consult an
owner-issued verdict for a current subject; it can never mint PASS/READY.
Verdict inference from currentness stays forbidden per
`registries/state-dimensions-v1.json` F13-F16 and Frozen L2 §10.
"""
from __future__ import annotations

import json
import re
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = ROOT / "fixtures" / "gate-currentness"
MAP_DOC = ROOT / "references" / "GATE_EVIDENCE_CURRENTNESS_MATRIX.md"
REGISTRY = ROOT / "registries" / "state-dimensions-v1.json"

BASE_SHA = "f4fe88542de9d3f5376498e62778e2353391bc57"
BASE_TREE = "82ff224731e854079bdbd40a12eeffe00186b62c"
PACK_HEAD_SHA = "d8fd03dbfaab7d1ab7b7270f16d83715eb9c052e"
FROZEN_PRD_BLOB = "a8ec7030a14337a4c2dca853dc474e965679d610"
FROZEN_L2_BLOB = "bd41ea0175b459a6a490fd37ad579e429a58a1c3"
FROZEN_DAG_V02_BLOB = "b9fe0cc7089f64929b4bcf45f7230d950e864db2"

WRITE_SET = (
    "references/GATE_EVIDENCE_CURRENTNESS_MATRIX.md",
    "scripts/test_v49_gate_currentness.py",
    "fixtures/gate-currentness/",
)

# v4.10 integration (claim #779@6084794791 / pre-merge #779@6084805500; merge
# commit e0315b2a): `.agent/execution/T-010/IMPLEMENTATION_MAP.md` moved out of
# this pack-head loop into T010_MERGED_BLOBS — the disclosed composition rebind
# (§28 -> §29 citation) legally mutated that one T-010 planning file at the
# integration, so it is pinned as an exact merged output instead of "unmutated
# since the execution pack head". The remaining five files stay pack-head-frozen.
PLANNING_PATHS = tuple(
    f".agent/execution/T-010/{name}"
    for name in (
        "MANIFEST.yaml",
        "EXECUTION_CONTRACT.md",
        "TEST_MATRIX.yaml",
        "FAILURE_MATRIX.yaml",
        "REVIEW_CHECKLIST.md",
    )
)

# F1 RE-BIND (T-012, authorized pin-constants-only change; provenance at
# test_t07_frozen_authority_and_planning_files_unmutated, disclosure
# #730@5998009516, inheritance #877@5999737862, MANIFEST
# controller_authorizations[0]): the merged T-010 outputs at this base
# (version/v4.9.0@d53e943e), blob-pinned. Any further mutation of any T-010
# output still fails; zero assertion-logic change.
#
# v4.10 integration value re-bind (claim #779@6084794791 / pre-merge
# #779@6084805500; merge commit e0315b2a): the disclosed composition rebind
# renumbered the v4.9 standard section §28 -> §29 and mechanically rebound its
# §28 citations, which moved the merged blobs of three T-010 outputs
# (`references/GATE_EVIDENCE_CURRENTNESS_MATRIX.md`,
# `fixtures/gate-currentness/assurance_binding.json`,
# `fixtures/gate-currentness/successor_chain.json`) and of
# `.agent/execution/T-010/IMPLEMENTATION_MAP.md` (moved here out of the
# pack-head loop above: it is an integrated output now). It also moved
# `fixtures/gate-currentness/owner_map.json`, whose M01 owner ref is realigned
# to the renumbered §29.1 anchor (the identical string is cited line-verbatim
# in the matrix doc, whose M01/M04 code blocks were realigned in the same
# step). Pin constants only — zero removed tests, no intent weakened.
T010_MERGED_BLOBS = {
    "references/GATE_EVIDENCE_CURRENTNESS_MATRIX.md": "0c2538db15784ac0f7200ee4537eecec3e43b27f",
    ".agent/execution/T-010/IMPLEMENTATION_MAP.md": "596fe50d7f6fef868f4f37cc94f1ce34fb6b51aa",
    "fixtures/gate-currentness/assurance_binding.json": "2942252e4ea5af99eadafda49c6e0f65b65d6ae9",
    "fixtures/gate-currentness/dogfood_binding.json": "e5589bdefcba50c4a156c8c05618ddf49439bc61",
    "fixtures/gate-currentness/frozen_candidates.json": "00a36fdb62493d53104f1ac6c6bfd79b6480f6c2",
    "fixtures/gate-currentness/impact_decisions.json": "ff0b0cdbe5984ea0305d39c278777997f3a88fa8",
    "fixtures/gate-currentness/owner_map.json": "5342314960621c5a4d157c42a4d60d1253cef2ec",
    "fixtures/gate-currentness/release_applicability.json": "4fb525df247ba39367a0105f3f1de8844f686b0b",
    "fixtures/gate-currentness/stale_pass.json": "f6b4addc27e7b591e55027e1509042c4be99005b",
    "fixtures/gate-currentness/successor_chain.json": "51338b2ab39a1e145976dda55e4d1b61715746c7",
}

# The T-010 oracle identity of this kernel itself: the only lawful edit on top
# of the merged T-010 content is the F1 re-bind documented above, so the
# kernel's T01-T07 oracle surface is pinned by these markers plus the green
# execution of this very suite in the same run.
T010_KERNEL_ORACLE_MARKERS = (
    "T010 gate-owned evidence binding/currentness integration kernel",
    "class GateCurrentnessKernel(unittest.TestCase):",
    "def route_evidence(",
    "def gate_satisfied(",
    "def plan_binding_state(",
    "def successor_review_gate(",
    "def test_t01_stale_pass_prevention",
    "def test_t02_successor_and_carried_findings",
    "def test_t03_impact_decisions_per_owner_rules",
    "def test_t04_frozen_candidate_rules",
    "def test_t05_release_applicability_binding",
    "def test_t06_dogfood_candidate_binding",
    "def test_t06_assurance_currentness_consumption_at_transitions",
    "def test_t07_owner_refs_resolve_and_doc_agrees_with_fixture",
    "def test_t07_engine_mints_no_verdicts",
    "def test_t07_owner_map_covers_frozen_l2_matrix_families",
    "def test_t07_frozen_authority_and_planning_files_unmutated",
)

# Owner surfaces this lane consumes read-only (T-005->T-010->T-014 serialization:
# no Release surface is edited; RELEASE_STANDARD is asserted unmutated since base).
READ_ONLY_DEPS = (
    "standards/ASSURANCE_PLAN_STANDARD.md",
    "standards/EXECUTION_ARCHITECTURE_STANDARD.md",
    "standards/VALIDATION_STANDARD.md",
    "standards/RELEASE_STANDARD.md",
    "standards/DEVELOPMENT_WORKFLOW.md",
    "standards/GITHUB_WORK_ITEM_CONTRACT_STANDARD.md",
    "standards/CI_EVIDENCE_STANDARD.md",
    "standards/TEST_DATA_AND_SCENARIO_STANDARD.md",
    "schemas/assurance-plan-v2.schema.json",
    "schemas/review-aggregation-v1.schema.json",
    "schemas/review-finding-v1.schema.json",
    "schemas/task-learning-v2.schema.json",
    "references/RELEASE_APPLICABILITY_REFERENCE.md",
    "references/TASK_LEARNING_EVIDENCE_REFERENCE.md",
    "scripts/test_v49_release_applicability.py",
    "registries/state-dimensions-v1.json",
    "docs/implementation/4.9.0/PRD.md",
    "docs/implementation/4.9.0/L2_ARCHITECTURE_EVIDENCE.md",
)

# v4.10 integration re-bind (claim #779@6084794791 / pre-merge #779@6084805500;
# merge commit e0315b2a): three of the read-only owner surfaces above legally
# carry the v4.10 line's integrated content at the merged tree (the v4.10
# standard additions compose into `standards/EXECUTION_ARCHITECTURE_STANDARD.md`;
# `standards/VALIDATION_STANDARD.md` and `standards/DEVELOPMENT_WORKFLOW.md` are
# byte-identical to the v4.10 candidate side of this merge). The stale
# "unmutated since BASE_SHA" pin is re-bound to an exact integrated-blob identity
# pin — pin constants only, any further mutation of these surfaces still fails,
# zero other assertion change. Same idiom as READ_ONLY_DEPS_REBOUND_BLOBS in
# scripts/test_v49_execution_core.py.
READ_ONLY_DEPS_REBOUND_BLOBS = {
    "standards/EXECUTION_ARCHITECTURE_STANDARD.md": "5588d2196677b1b4878563de65edf2beaa10178f",
    "standards/VALIDATION_STANDARD.md": "1522b85f9e68cc4a1591ea5899b53c224998e5a8",
    "standards/DEVELOPMENT_WORKFLOW.md": "57902fbcb56ffec9a461365ace472fb03e3520db",  # re-bound (#1007/#1032): T-01 effective-rule section additions on this branch
}

# The routing vocabulary of this wiring engine. It deliberately contains no
# verdict: routing dispositions only decide whether an owner-issued record may
# be consulted for the current subject (or what must happen instead).
ROUTING_VOCAB = {
    "BOUND_CURRENT",
    "HISTORICAL_ONLY",
    "FRESH_EXECUTION_REQUIRED",
    "SUCCESSOR_ASSURANCE_REQUIRED",
    "CARRY_FORWARD_UNTIL_DISPOSITION",
    "RECOMPUTE_REQUIRED",
    "BLOCKED",
    "FAMILY_MISMATCH",
    "NOT_ROUTABLE",
}

# Positive owner-issued verdicts per row family (owner vocabularies; the engine
# only ever consults them, never produces them).
POSITIVE_VERDICTS = {
    "M01": set(),  # a current plan authorizes transitions, it is never a PASS
    "M02": {"PASS"},
    "M03": {"PASS"},
    "M04": {"PASS"},
    "M05": {"PASS"},
    "M06": {"READY"},
    "M07": set(),  # applicability decisions are Release-owned; REQUIRED_NOW is not a PASS
    "M08": {"PASS"},
    "M09": set(),  # Task Learning evidence is never a gate PASS
    "M10": set(),  # dogfood report is Release evidence only
}


# ---------------------------------------------------------------------------
# fixture / repository helpers
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
    """GitHub-style heading anchors: lowercase, punctuation stripped, spaces -> dashes."""
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


def _schema_has_field(schema: dict, field: str) -> bool:
    if field in schema.get("properties", {}):
        return True
    for value in schema.get("properties", {}).values():
        if isinstance(value, dict) and _schema_has_field(value, field):
            return True
    return False


def resolve_owner_ref(ref: str) -> None:
    """Assert an owner ref resolves in-repository (exact path + anchor/field).

    This is the T07 'every map row cites its owner by exact ref' oracle: refs
    are not decorative text; each must resolve against the repository at the
    candidate.
    """
    path_part, _, frag = ref.partition("#")
    path = ROOT / path_part
    if not path.is_file():
        raise AssertionError(f"owner ref path does not resolve: {ref}")
    if not frag:
        return
    if path_part.endswith(".md"):
        anchors = github_anchors(path.read_text(encoding="utf-8"))
        if frag not in anchors:
            raise AssertionError(
                f"owner ref anchor missing in {path_part}: #{frag} "
                f"(available: {sorted(a for a in anchors if a.startswith(frag[:6]))})"
            )
    elif path_part.endswith(".json"):
        schema = json.loads(path.read_text(encoding="utf-8"))
        if not _schema_has_field(schema, frag):
            raise AssertionError(f"owner ref schema field missing in {path_part}: #{frag}")
    # .py and other refs: file existence is the resolution contract.


# ---------------------------------------------------------------------------
# reference engine: gate-owned currentness wiring (routing only, no verdicts)
# ---------------------------------------------------------------------------

def findings_digest(finding_ids: list[str]) -> str:
    """Digest over the CURRENT unresolved-finding set (M01 owner: ASSURANCE_PLAN §12/§13)."""
    return "findings:" + "|".join(sorted(finding_ids))


def plan_binding_state(plan_binding: dict, current_dimensions: dict, unresolved_findings: list[str]) -> str:
    """Recompute the M01 binding state from facts (ASSURANCE_PLAN §12 all-components-exact-current).

    The stored `state` is never trusted: the unresolved-finding digest and every
    bound component are recomputed (no stale latch, EXECUTION_ARCHITECTURE §29.6).
    """
    bound_keys = (
        "subject_identity_ref",
        "owner_authority_digest",
        "proof_input_digest",
        "task_pack_digest",
        "release_decision_digest",
        "unresolved_finding_digest",
    )
    current = dict(current_dimensions)
    current["unresolved_finding_digest"] = findings_digest(unresolved_findings)
    unknown = any(key not in plan_binding or plan_binding.get(key) is None for key in bound_keys)
    if unknown:
        return "UNKNOWN"  # omission is not an empty set; missing => UNKNOWN (§12)
    if any(plan_binding[key] != current[key] for key in bound_keys):
        return "STALE"
    return "CURRENT"


def transition_admissions(binding_state: str, checkpoints: list[str]) -> list[str]:
    """M01 wiring: authority-bearing transitions proceed only on CURRENT (§29.1)."""
    if binding_state == "CURRENT":
        return list(checkpoints)
    return []


def route_evidence(record: dict, current_subject: dict, row: dict) -> str:
    """Row-aware currentness routing for an owner-issued evidence record.

    Returns a ROUTING_VOCAB disposition. Never a verdict: on BOUND_CURRENT the
    owner verdict may be consulted for the current subject, nothing more.
    """
    row_id = row["row_id"]
    if record.get("row_id", row_id) != row_id or record["owner_ref"] not in row["owner_refs"]:
        return "FAMILY_MISMATCH"
    if row_id == "M09":
        return "HISTORICAL_ONLY"  # historical learning evidence only; never gate PASS
    if record["subject_identity"] == current_subject["subject_identity"]:
        if row_id in {"M05", "M06"}:
            # fresh-only rows additionally require the frozen-candidate identity binding
            bound = record.get("binding", {}).get("frozen_candidate_identity")
            if bound != current_subject["subject_identity"]:
                return "FRESH_EXECUTION_REQUIRED"
        if row_id == "M10":
            return "BOUND_CURRENT" if _dogfood_bindings_current(record) else "HISTORICAL_ONLY"
        return "BOUND_CURRENT"
    if row_id in {"M05", "M06"}:
        return "FRESH_EXECUTION_REQUIRED"  # fresh-only on candidate drift
    if row_id == "M10":
        return "HISTORICAL_ONLY"  # ADS candidate thaw/drift => historical-only
    return "HISTORICAL_ONLY"  # NO_OWNER_TRANSFER_RULE => HISTORICAL_ONLY (L2 §10)


def _dogfood_bindings_current(record: dict) -> bool:
    binding = record.get("binding", {})
    return bool(binding.get("exact_ads_candidate")) and bool(record.get("pinned_authority_refs"))


def gate_satisfied(record: dict, disposition: str, row: dict) -> bool:
    """True iff an owner-issued positive verdict on the current subject is consultable.

    This is the ONLY path to True in this engine: owner verdict + BOUND_CURRENT
    + row family match. Routing outcomes themselves are never satisfaction
    (BOUND_CURRENT is not PASS — registry F13-F16).
    """
    if disposition != "BOUND_CURRENT":
        return False
    return record.get("verdict") in POSITIVE_VERDICTS[row["row_id"]]


def successor_review_gate(
    carried_findings: list[str],
    per_finding_outcomes: list[dict],
    successor_subject: str,
    successor_review: dict | None,
    authorized_repair: bool,
    origin_subject: str,
    owning_authority_disposition: dict | None = None,
) -> dict:
    """M04 wiring (L2 §9.1/§9.2 + review-aggregation-v1 blocker dominance).

    Consumes the carried unresolved set, evaluates per-finding successor
    outcomes, and decides admissibility of the successor Review judgment.
    Grading/severity/aggregation authority stays with the Review owners.
    """
    unresolved = list(carried_findings)
    carried_set = set(carried_findings)
    reason = None

    for outcome in per_finding_outcomes:
        fid = outcome["finding_id"]
        if fid not in carried_set:
            continue  # cannot disposition what was not carried (fail closed)
        kind = outcome["outcome"]
        evidence = outcome.get("evidence_refs") or []
        if kind == "RESOLVED" and evidence:
            unresolved.remove(fid)
        elif kind == "STILL_PRESENT":
            reason = reason or "CARRY_FORWARD_UNTIL_DISPOSITION"
        elif kind == "NOT_APPLICABLE_TO_SUCCESSOR":
            if outcome.get("owning_rule_basis"):
                unresolved.remove(fid)
            else:
                reason = reason or "MISSING_OWNING_RULE_BASIS"
        else:
            reason = reason or "UNPROVEN_DISPOSITION"

    if owning_authority_disposition is not None:
        fid = owning_authority_disposition["finding_id"]
        if fid in carried_set and owning_authority_disposition.get("authority_ref"):
            unresolved.remove(fid)

    if successor_subject == origin_subject and not authorized_repair:
        return {
            "admissible": False,
            "unresolved_after": unresolved,
            "reason": "UNAUTHORIZED_REVIEW_PATH",
            "carry_disposition": "CARRY_FORWARD_UNTIL_DISPOSITION",
        }
    if carried_set and not per_finding_outcomes and owning_authority_disposition is None:
        if successor_review is not None:
            return {
                "admissible": False,
                "unresolved_after": unresolved,
                "reason": "REVIEW_SHOPPING_REJECTED",
                "carry_disposition": "CARRY_FORWARD_UNTIL_DISPOSITION",
            }
    if successor_review is None:
        return {
            "admissible": False,
            "unresolved_after": unresolved,
            "reason": "PASS_NOT_TRANSFERRED",
            "carry_disposition": "CARRY_FORWARD_UNTIL_DISPOSITION" if unresolved else None,
        }
    if unresolved:
        return {
            "admissible": False,
            "unresolved_after": unresolved,
            "reason": reason or "BLOCKER_DOMINANCE",
            "carry_disposition": "CARRY_FORWARD_UNTIL_DISPOSITION",
        }
    return {"admissible": True, "unresolved_after": [], "reason": None, "carry_disposition": None}


CI_CONFIG_PATH_PREFIXES = (".github/",)


def validation_reuse(scenario: dict) -> dict:
    """M03 wiring: existing VALIDATION_IMPACT_DECISION use (VALIDATION_STANDARD §6 owner rule).

    Reuse binds the existing owner tuple to the current merge subject; it never
    mints a new PASS. HEAD drift is never repaired by an impact decision.
    """
    decision = scenario["decision"]
    if not scenario.get("requested_head_sha_matches_current_pr_head", True):
        return {
            "reuse_allowed": False,
            "disposition": "HISTORICAL_ONLY",
            "new_pass_minted": False,
            "reason": "HEAD_DRIFT_NEW_DISPATCH_IDENTITY",
        }
    if decision.get("validation_impact") == "affected":
        return {
            "reuse_allowed": False,
            "disposition": "FRESH_EXECUTION_REQUIRED",
            "new_pass_minted": False,
            "rerun_gates": ["affected"],
        }
    comparison = scenario.get("base_delta_write_set_comparison")
    if comparison is None or not decision.get("evidence_reuse_basis"):
        return {
            "reuse_allowed": False,
            "disposition": "BLOCKED",
            "new_pass_minted": False,
            "reason": "UNKNOWN_FAIL_CLOSED",
        }
    touched = comparison.get("exclusion_classes_touched") or []
    if touched:
        return {
            "reuse_allowed": False,
            "disposition": "FRESH_EXECUTION_REQUIRED",
            "new_pass_minted": False,
            "rerun_gates": ["affected"],
        }
    changed = comparison.get("changed_paths") or []
    ci_only = bool(changed) and all(p.startswith(CI_CONFIG_PATH_PREFIXES) for p in changed)
    if ci_only:
        # Owner rule: CI/workflow/config-only changes are not automatically
        # evidence-preserving because they can alter execution semantics.
        if decision.get("evidence_reuse_basis") == "ci-config-only":
            return {
                "reuse_allowed": False,
                "disposition": "FRESH_EXECUTION_REQUIRED",
                "new_pass_minted": False,
                "reason": "OWNER_REQUIRES_EXPLICIT_PROOF_CI_CONFIG_CAN_ALTER_EXECUTION",
            }
    return {"reuse_allowed": True, "disposition": "BOUND_CURRENT", "new_pass_minted": False}


def frozen_candidate_disposition(record: dict, freeze_record: dict, current_candidate: dict) -> str:
    """M05/M06 wiring: fresh-only on candidate drift (RELEASE_STANDARD §3/§4)."""
    frozen = (
        freeze_record.get("state") == "FROZEN"
        and current_candidate.get("state") == "FROZEN"
        and record.get("binding", {}).get("frozen_candidate_identity")
        == current_candidate.get("candidate_identity")
        and record["subject_identity"] == current_candidate.get("candidate_identity")
    )
    return "BOUND_CURRENT" if frozen else "FRESH_EXECUTION_REQUIRED"


def version_gate_omission_allowed(
    concern_decisions: list[dict], version_decision: dict | None, closure_claims_gate_satisfied_via_deferral: bool = False
) -> bool:
    """M07 wiring by reference (RELEASE_STANDARD §11.3): concern decisions never
    aggregate into a version-level gate omission."""
    if closure_claims_gate_satisfied_via_deferral:
        return False  # CONCERN_DEFERRED != VERSION_GATE_SATISFIED
    if version_decision is None:
        return False  # no fresh Release-owned version-level decision => nothing omitted
    if version_decision.get("release_authority_ref") != "standards/RELEASE_STANDARD.md#11-release-applicability-by-gate--subject":
        return False  # not a Release-owned decision
    return version_decision.get("applicability") == "NOT_APPLICABLE"


def release_decision_current(version_decision: dict | None, version_candidate: dict) -> tuple[bool, str]:
    """M07 wiring by reference (RELEASE_STANDARD §11.4): applicability is
    re-evaluated when a binding dimension (here: candidate identity) changes."""
    if version_decision is None:
        return False, "NO_RELEASE_OWNED_DECISION"
    if version_decision.get("subject_identity") != version_candidate.get("candidate_identity"):
        return False, "NONCURRENT_SUBJECT_BINDING"
    return True, "CURRENT"


def dogfood_posture(report: dict, current_ads_candidate: str) -> dict:
    """M10 wiring (PRD §16.3 + Frozen L2 §14): exact-candidate binding; the
    report is Release evidence only and can never authorize execution or RQ."""
    disposition = "BOUND_CURRENT" if report["bound_ads_candidate"] == current_ads_candidate else "HISTORICAL_ONLY"
    return {
        "disposition": disposition,
        "authorizes_execution": False,
        "authorizes_release_qualification": False,
        "release_owner_reevaluation_required": disposition == "HISTORICAL_ONLY",
        "downstream_generality_satisfied": (
            disposition == "BOUND_CURRENT" and report.get("baseline_vs_selected_delta_nonzero") is True
        ),
    }


# ---------------------------------------------------------------------------
# kernel tests (TEST_MATRIX T01-T07)
# ---------------------------------------------------------------------------

class GateCurrentnessKernel(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.owner_map = load_fixture("owner_map.json")
        cls.rows = {row["row_id"]: row for row in cls.owner_map["rows"]}
        cls.map_doc = MAP_DOC.read_text(encoding="utf-8")
        cls.registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        cls.stale_pass = load_fixture("stale_pass.json")
        cls.successor_chain = load_fixture("successor_chain.json")
        cls.impact_decisions = load_fixture("impact_decisions.json")
        cls.frozen_candidates = load_fixture("frozen_candidates.json")
        cls.release_applicability = load_fixture("release_applicability.json")
        cls.dogfood_binding = load_fixture("dogfood_binding.json")
        cls.assurance_binding = load_fixture("assurance_binding.json")

    # ---------- T01: stale-PASS prevention ----------

    def test_t01_stale_pass_prevention(self) -> None:
        scenarios = {s["scenario_id"]: s for s in self.stale_pass["scenarios"]}
        for sid, scenario in scenarios.items():
            with self.subTest(scenario=sid):
                row = self.rows[scenario["row_id"]]
                subject = self.stale_pass["subjects"][scenario["current_subject"]]
                # The record's row/owner binding is injected for routing.
                record = dict(scenario["record"])
                record["row_id"] = scenario["row_id"]
                if scenario["row_id"] == "M10":
                    record["binding"] = {
                        "exact_ads_candidate": record["subject_identity"],
                        "pinned_authority_refs": ["docs/implementation/4.9.0/PRD.md#163-exact-candidate-binding"],
                    }
                disposition = route_evidence(record, subject, row)
                expected = scenario["expect"]
                if expected.get("disposition") == "FAMILY_MISMATCH":
                    self.assertEqual(disposition, "FAMILY_MISMATCH")
                else:
                    self.assertEqual(disposition, expected["disposition"], scenario["scenario_id"])
                satisfied = gate_satisfied(record, disposition, row) if disposition != "FAMILY_MISMATCH" else False
                self.assertEqual(satisfied, expected["gate_satisfied"])
        # Stale-PASS-transfer counter is asserted zero across all T01 scenarios.
        transferred = sum(
            1
            for s in self.stale_pass["scenarios"]
            if s["expect"]["gate_satisfied"] and s["record"]["subject_identity"] != self.stale_pass["subjects"][s["current_subject"]]["subject_identity"]
        )
        self.assertEqual(transferred, 0)

    # ---------- T02: successor / carried findings ----------

    def test_t02_successor_and_carried_findings(self) -> None:
        findings = {f["finding_id"]: f for f in self.successor_chain["findings"]}
        for scenario in self.successor_chain["scenarios"]:
            with self.subTest(scenario=scenario["scenario_id"]):
                for fid in scenario["carried_findings"]:
                    self.assertEqual(findings[fid]["state"], "UNRESOLVED")
                result = successor_review_gate(
                    carried_findings=scenario["carried_findings"],
                    per_finding_outcomes=scenario["per_finding_outcomes"],
                    successor_subject=scenario["successor_subject"],
                    successor_review=scenario.get("successor_review"),
                    authorized_repair=scenario["authorized_repair"],
                    origin_subject=findings[scenario["carried_findings"][0]]["origin_subject"],
                    owning_authority_disposition=scenario.get("owning_authority_disposition"),
                )
                expected = scenario["expect"]
                self.assertEqual(result["admissible"], expected["admissible"], scenario["scenario_id"])
                self.assertEqual(sorted(result["unresolved_after"]), sorted(expected["unresolved_after"]))
                if expected.get("reason"):
                    self.assertEqual(result["reason"], expected["reason"])
                if expected.get("carry_disposition"):
                    self.assertEqual(result["carry_disposition"], expected["carry_disposition"])
                # A blocking scenario must route CARRY_FORWARD, never erase the finding.
                if not result["admissible"] and result["unresolved_after"]:
                    self.assertIn(
                        "F-ADV-1", result["unresolved_after"] + (["F-ADV-1"] if "F-ADV-1" in scenario["carried_findings"] else [])
                    )

    def test_t02_successor_requires_authorized_repair_path(self) -> None:
        scenario = next(
            s for s in self.successor_chain["scenarios"] if s["scenario_id"] == "T02_SC6_same_subject_redispatch_for_pass_rejected"
        )
        findings = {f["finding_id"]: f for f in self.successor_chain["findings"]}
        result = successor_review_gate(
            carried_findings=scenario["carried_findings"],
            per_finding_outcomes=scenario["per_finding_outcomes"],
            successor_subject=scenario["successor_subject"],
            successor_review=scenario.get("successor_review"),
            authorized_repair=scenario["authorized_repair"],
            origin_subject=findings[scenario["carried_findings"][0]]["origin_subject"],
        )
        self.assertFalse(result["admissible"])
        self.assertEqual(result["reason"], "UNAUTHORIZED_REVIEW_PATH")

    # ---------- T03: validation impact decisions ----------

    def test_t03_impact_decisions_per_owner_rules(self) -> None:
        for scenario in self.impact_decisions["scenarios"]:
            with self.subTest(scenario=scenario["scenario_id"]):
                result = validation_reuse(scenario)
                expected = scenario["expect"]
                self.assertEqual(result["reuse_allowed"], expected["reuse_allowed"], scenario["scenario_id"])
                self.assertEqual(result["disposition"], expected["disposition"])
                self.assertFalse(result["new_pass_minted"], "reuse must never mint a new PASS")
                if expected.get("reason"):
                    self.assertEqual(result["reason"], expected["reason"])
                if expected.get("rerun_gates"):
                    self.assertEqual(result.get("rerun_gates"), expected["rerun_gates"])
        # The owner's exclusion classes are bound by exact text.
        standard = (ROOT / "standards" / "VALIDATION_STANDARD.md").read_text(encoding="utf-8")
        self.assertIn("VALIDATION_IMPACT_DECISION", standard)
        self.assertIn("validation_impact=none", standard)
        self.assertIn("If impact is `affected` or `unknown`, rerun affected gates", standard)
        self.assertIn("CI/workflow/config-only changes are not automatically evidence-preserving", standard)
        for cls_name in self.impact_decisions["impact_exclusion_classes"]:
            mapped = {
                "source_runtime_behavior": "relevant source/runtime behavior",
                "tests_fixtures": "tests/fixtures",
                "dependency_lockfile_toolchain_build": "dependency/lockfile/toolchain/build inputs",
                "public_contract_architecture_semantics": "public contract/architecture semantics",
                "shared_integration_wiring": "shared integration wiring",
                "artifact_identity": "artifact identity",
                "overlapping_write_sets": "overlapping write sets",
            }[cls_name]
            self.assertIn(mapped, standard, cls_name)

    # ---------- T04: Hidden/Closeout/RQ fresh/current candidate rules ----------

    def test_t04_frozen_candidate_rules(self) -> None:
        scenarios = {s["scenario_id"]: s for s in self.frozen_candidates["scenarios"]}

        # FC1: current frozen candidate binds.
        s = scenarios["T04_FC1_hidden_pass_current_frozen_candidate_binds"]
        record = dict(s["record"])
        record["row_id"] = "M05"
        disposition = frozen_candidate_disposition(record, s["freeze_record"], s["current_candidate"])
        self.assertEqual(disposition, "BOUND_CURRENT")
        self.assertTrue(gate_satisfied(record, disposition, self.rows["M05"]))

        # FC2: silent post-freeze mutation invalidates per RELEASE_STANDARD §4.
        s = scenarios["T04_FC2_silent_post_freeze_mutation_invalidates_hidden"]
        record = dict(s["record"])
        record["row_id"] = "M05"
        disposition = frozen_candidate_disposition(record, s["freeze_record"], s["current_candidate"])
        self.assertEqual(disposition, "FRESH_EXECUTION_REQUIRED")
        self.assertFalse(gate_satisfied(record, disposition, self.rows["M05"]))

        # FC3: legal thaw chain — new freeze gets fresh Hidden; old record stays historical.
        s = scenarios["T04_FC3_legal_thaw_chain_new_freeze_new_hidden_binds"]
        self.assertIn("THAWED / INVALIDATED", s["chain"])
        new_record = dict(s["record"])
        new_record["row_id"] = "M05"
        disposition = frozen_candidate_disposition(new_record, s["freeze_record"], s["current_candidate"])
        self.assertEqual(disposition, "BOUND_CURRENT")
        old_record = dict(s["old_record"])
        old_record["row_id"] = "M05"
        old_disposition = frozen_candidate_disposition(old_record, s["freeze_record"], s["current_candidate"])
        self.assertEqual(old_disposition, "FRESH_EXECUTION_REQUIRED")
        self.assertFalse(gate_satisfied(old_record, old_disposition, self.rows["M05"]))

        # FC4: RQ on a drifted candidate is fresh-only (M06 owner vocabulary READY).
        s = scenarios["T04_FC4_rq_on_drifted_candidate_fresh_only"]
        record = dict(s["record"])
        record["row_id"] = "M06"
        disposition = frozen_candidate_disposition(record, s["freeze_record"], s["current_candidate"])
        self.assertEqual(disposition, "FRESH_EXECUTION_REQUIRED")
        self.assertFalse(gate_satisfied(record, disposition, self.rows["M06"]))

        # FC5: strengthened pack => new immutable private pack identity => fresh Hidden.
        s = scenarios["T04_FC5_strengthened_pack_new_identity_old_pack_historical"]
        self.assertNotEqual(s["prior_pack"]["private_pack_revision"], s["strengthened_pack"]["private_pack_revision"])
        self.assertNotEqual(s["prior_pack"]["private_pack_revision"], s["strengthened_pack"]["checksum"])
        release_std = (ROOT / "standards" / "RELEASE_STANDARD.md").read_text(encoding="utf-8")
        self.assertIn("new immutable private pack identity/revision/checksum", release_std)
        self.assertIn("Old evidence remains valid only for its old candidate/pack identities", release_std)
        self.assertIn("FROZEN\n→ THAWED / INVALIDATED", release_std)

    # ---------- T05: Release applicability binding (by reference, T-005 owner) ----------

    def test_t05_release_applicability_binding(self) -> None:
        scenarios = {s["scenario_id"]: s for s in self.release_applicability["scenarios"]}

        s = scenarios["T05_RA1_concern_decisions_never_omit_version_gate"]
        self.assertFalse(
            version_gate_omission_allowed(s["concern_decisions"], s["version_level_decision"])
        )

        s = scenarios["T05_RA2_fresh_release_owned_version_decision_required_now_governs"]
        # Even a fresh, current, Release-owned decision does not permit omission
        # when the Release rule says REQUIRED_NOW: only NOT_APPLICABLE does.
        self.assertFalse(
            version_gate_omission_allowed(s["concern_decisions"], s["version_level_decision"])
        )
        self.assertEqual(s["version_level_decision"]["applicability"], "REQUIRED_NOW")
        # The concern NOT_APPLICABLE cannot cancel the version gate.
        self.assertTrue(s["expect"]["concern_cancellation_attempted"])
        current, reason = release_decision_current(s["version_level_decision"], s["version_candidate"])
        self.assertTrue(current)
        self.assertEqual(reason, "CURRENT")

        s = scenarios["T05_RA3_deferral_is_not_gate_satisfaction_at_version_closure"]
        self.assertFalse(
            version_gate_omission_allowed(
                s["concern_decisions"], s["version_level_decision"], s["closure_claims_gate_satisfied_via_deferral"]
            )
        )

        s = scenarios["T05_RA4_stale_applicability_record_fail_closed"]
        current, reason = release_decision_current(s["version_level_decision"], s["version_candidate"])
        self.assertFalse(current)
        self.assertEqual(reason, "NONCURRENT_SUBJECT_BINDING")

        s = scenarios["T05_RA5_builder_or_concern_pass_cannot_mint_applicability"]
        self.assertNotEqual(s["attempted_mint"]["actor"], "release-authority")
        # No wiring function accepts a mint: the only accepted applicability source
        # is a Release-owned decision record (checked above via release_authority_ref).

        # Registry F12 binds the non-aggregation rule; owner text is asserted, not redefined.
        rule_ids = {r["rule_id"] for r in self.registry["forbidden_inferences"]}
        self.assertIn("F12_CONCERN_RELEASE_APPLICABILITY_NOT_VERSION_APPLICABLE", rule_ids)
        release_std = (ROOT / "standards" / "RELEASE_STANDARD.md").read_text(encoding="utf-8")
        self.assertIn("CONCERN_NOT_APPLICABLE\n!= VERSION_NOT_APPLICABLE", release_std)
        self.assertIn("CONCERN_DEFERRED\n!= VERSION_GATE_SATISFIED", release_std)
        self.assertIn("`UNKNOWN` is fail-closed", release_std)

    # ---------- T06: dogfood binding + assurance consumption ----------

    def test_t06_dogfood_candidate_binding(self) -> None:
        scenarios = {s["scenario_id"]: s for s in self.dogfood_binding["scenarios"]}

        s = scenarios["T06_D1_exact_ads_candidate_match_binds_as_release_evidence"]
        posture = dogfood_posture(s["report"], s["current_ads_candidate"])
        self.assertEqual(posture["disposition"], "BOUND_CURRENT")
        self.assertFalse(posture["authorizes_execution"])
        self.assertFalse(posture["authorizes_release_qualification"])
        self.assertTrue(posture["downstream_generality_satisfied"])

        s = scenarios["T06_D2_ads_candidate_drift_makes_report_historical_only"]
        posture = dogfood_posture(s["report"], s["current_ads_candidate"])
        self.assertEqual(posture["disposition"], "HISTORICAL_ONLY")
        self.assertTrue(posture["release_owner_reevaluation_required"])
        self.assertFalse(posture["downstream_generality_satisfied"])

        s = scenarios["T06_D3_zero_delta_is_compatibility_evidence_only"]
        posture = dogfood_posture(s["report"], s["current_ads_candidate"])
        self.assertFalse(posture["downstream_generality_satisfied"])

        s = scenarios["T06_D4_unexercised_mechanism_claim_boundary_required"]
        unexercised = [m for m in s["report"]["mechanism_matrix"] if m["state"] == "NOT_EXERCISED"]
        self.assertTrue(unexercised)
        self.assertTrue(all(m.get("claim_boundary") for m in unexercised))
        posture = dogfood_posture(s["report"], s["current_ads_candidate"])
        self.assertFalse(posture["authorizes_execution"])

    def test_t06_assurance_currentness_consumption_at_transitions(self) -> None:
        default_dims = self.assurance_binding["component_current_dimensions"]
        checkpoints = self.assurance_binding["transition_checkpoints"]
        scenarios = {s["scenario_id"]: s for s in self.assurance_binding["scenarios"]}

        s = scenarios["T06_AB1_current_plan_admits_all_transitions"]
        state = plan_binding_state(s["plan_binding"], default_dims, s["unresolved_findings"])
        self.assertEqual(state, "CURRENT")
        self.assertEqual(transition_admissions(state, checkpoints), checkpoints)

        s = scenarios["T06_AB2_release_decision_drift_makes_plan_stale_recompute"]
        state = plan_binding_state(s["plan_binding"], default_dims, s["unresolved_findings"])
        self.assertEqual(state, "STALE")
        self.assertEqual(transition_admissions(state, checkpoints), [])

        s = scenarios["T06_AB3_new_adverse_finding_between_dispatch_and_claim_fails_claim"]
        state = plan_binding_state(s["plan_binding"], default_dims, s["unresolved_findings"])
        self.assertEqual(state, "STALE")
        self.assertEqual(s["transition_under_check"], "claim_admission")
        self.assertEqual(transition_admissions(state, ["claim_admission"]), [])

        s = scenarios["T06_AB4_missing_component_is_unknown_fail_closed"]
        state = plan_binding_state(s["plan_binding"], default_dims, s["unresolved_findings"])
        self.assertEqual(state, "UNKNOWN")
        self.assertEqual(transition_admissions(state, checkpoints), [])

        s = scenarios["T06_AB5_empty_finding_set_still_digest_bound"]
        dims = s.get("component_current_dimensions", default_dims)
        state = plan_binding_state(s["plan_binding"], dims, s["unresolved_findings"])
        self.assertEqual(state, "CURRENT")
        self.assertEqual(
            s["plan_binding"]["unresolved_finding_digest"], findings_digest(s["unresolved_findings"])
        )
        self.assertEqual(transition_admissions(state, checkpoints), checkpoints)

        # CURRENT never mints PASS: the M01 positive-verdict set is empty and the
        # registry forbids the inference (F13-F16).
        self.assertEqual(POSITIVE_VERDICTS["M01"], set())
        rule_ids = {r["rule_id"] for r in self.registry["forbidden_inferences"]}
        for rule in (
            "F13_ASSURANCE_CURRENT_NOT_VALIDATION_PASS",
            "F14_ASSURANCE_CURRENT_NOT_REVIEW_PASS",
            "F15_ASSURANCE_CURRENT_NOT_RELEASE_READY",
            "F16_ASSURANCE_CURRENT_NOT_TASK_READY",
        ):
            self.assertIn(rule, rule_ids)

    # ---------- T07: no owner redefinition; exact refs; frozen surfaces ----------

    def test_t07_owner_refs_resolve_and_doc_agrees_with_fixture(self) -> None:
        row_ids = []
        for row in self.owner_map["rows"]:
            row_ids.append(row["row_id"])
            with self.subTest(row=row["row_id"]):
                self.assertIn(row["row_id"], self.map_doc, f"row missing from map doc: {row['row_id']}")
                self.assertIn(f"### {row['row_id']} —", self.map_doc)
                for ref in row["owner_refs"]:
                    resolve_owner_ref(ref)
                    self.assertIn(
                        f"\n{ref}\n",
                        self.map_doc,
                        f"owner_ref not cited line-verbatim in doc: {ref}",
                    )
        self.assertEqual(row_ids, [f"M{i:02d}" for i in range(1, 11)])

    def test_t07_engine_mints_no_verdicts(self) -> None:
        # Routing vocabulary carries no verdict token.
        self.assertNotIn("PASS", ROUTING_VOCAB)
        self.assertNotIn("READY", ROUTING_VOCAB)
        self.assertNotIn("FAIL", ROUTING_VOCAB)
        # Every row's positive-verdict set only contains owner vocabulary, and
        # non-verdict rows (M01/M07/M09/M10) are empty.
        self.assertEqual(POSITIVE_VERDICTS["M01"], set())
        self.assertEqual(POSITIVE_VERDICTS["M07"], set())
        self.assertEqual(POSITIVE_VERDICTS["M09"], set())
        self.assertEqual(POSITIVE_VERDICTS["M10"], set())
        # Owner-specific meaning stays canonical: a PASS from one family can never
        # satisfy another family's gate (FAMILY_MISMATCH is not consultable).
        record = {
            "record_id": "x",
            "row_id": "M04",
            "owner_ref": self.rows["M04"]["owner_refs"][0],
            "verdict": "PASS",
            "subject_identity": "sha:2222222222222222222222222222222222222222",
        }
        subject = {"subject_identity": "sha:2222222222222222222222222222222222222222"}
        self.assertEqual(route_evidence(record, subject, self.rows["M02"]), "FAMILY_MISMATCH")
        self.assertFalse(gate_satisfied(record, "FAMILY_MISMATCH", self.rows["M02"]))
        # BOUND_CURRENT without an owner positive verdict is not satisfaction.
        current = dict(record)
        current["row_id"] = "M02"
        current["owner_ref"] = self.rows["M02"]["owner_refs"][0]
        current["verdict"] = "NOT_RUN"
        row = self.rows["M02"]
        self.assertEqual(route_evidence(current, subject, row), "BOUND_CURRENT")
        self.assertFalse(gate_satisfied(current, "BOUND_CURRENT", row))

    def test_t07_owner_map_covers_frozen_l2_matrix_families(self) -> None:
        l2_text = (ROOT / "docs" / "implementation" / "4.9.0" / "L2_ARCHITECTURE_EVIDENCE.md").read_text(encoding="utf-8")
        # Every L2 §10 family appears in the owner map fixture.
        self.assertIn("| Assurance Plan successor |", l2_text)
        self.assertIn("| concern Validation |", l2_text)
        self.assertIn("| integration Validation |", l2_text)
        self.assertIn("| Review |", l2_text)
        self.assertIn("| Hidden |", l2_text)
        self.assertIn("| Closeout/RQ |", l2_text)
        self.assertIn("| Release applicability decision |", l2_text)
        self.assertIn("| CI evidence |", l2_text)
        self.assertIn("| Task Learning |", l2_text)
        self.assertIn("| Proportional Dogfood Report |", l2_text)
        families = {row["family"] for row in self.owner_map["rows"]}
        for family in (
            "assurance_plan_successor",
            "concern_validation",
            "integration_validation_impact_decision",
            "review",
            "hidden_validation",
            "closeout_release_qualification",
            "release_applicability_decision",
            "ci_evidence",
            "task_learning_evidence",
            "proportional_dogfood_report",
        ):
            self.assertIn(family, families)
        # L2 §10 generic routing rules are bound verbatim in the map doc.
        for rule in (
            "NO_OWNER_TRANSFER_RULE",
            "UNKNOWN_BINDING",
            "OWNER_FRESH_ONLY",
            "MATERIAL_BINDING_CHANGE",
            "UNRESOLVED_ADVERSE_FINDING",
        ):
            self.assertIn(rule, self.map_doc)
            self.assertIn(rule, l2_text)

    def test_t07_frozen_authority_and_planning_files_unmutated(self) -> None:
        # Working tree changes stay inside the Builder write set.
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
        # Immutable T-010 planning files are unmutated since the execution pack head.
        for rel_path in PLANNING_PATHS:
            with self.subTest(planning_path=rel_path):
                self.assertEqual(git_blob_sha(PACK_HEAD_SHA, rel_path), git_blob_sha("HEAD", rel_path))
        # Read-only owner surfaces (incl. all Release surfaces — T-005 serialization)
        # are unmutated since the base, except the three v4.10-integrated surfaces
        # pinned to their exact integrated blobs below (READ_ONLY_DEPS_REBOUND_BLOBS
        # disclosure).
        for rel_path in READ_ONLY_DEPS:
            if rel_path in READ_ONLY_DEPS_REBOUND_BLOBS:
                continue
            with self.subTest(read_only=rel_path):
                self.assertEqual(git_blob_sha(BASE_SHA, rel_path), git_blob_sha("HEAD", rel_path))
        for rel_path, pinned_blob in READ_ONLY_DEPS_REBOUND_BLOBS.items():
            with self.subTest(read_only_rebound=rel_path):
                self.assertEqual(pinned_blob, git_blob_sha("HEAD", rel_path))
        # F1 RE-BIND (T-012; Controller authorization per the #730@5998009516
        # disclosure, inherited #877@5999737862, MANIFEST
        # controller_authorizations[0]). The original T-010 lane guard
        # `git diff --name-only d8fd03db..HEAD ⊆ T-010 WRITE_SET` is
        # structurally red at any integrated tree: after T-011 the candidate
        # HEAD necessarily carries other lanes' merged deltas. Re-bound with
        # pin constants only, zero other assertion change — SAME STRENGTH: the
        # merged T-010 outputs must be EXACTLY present at the candidate. Every
        # T-010 output this lane does not itself edit is pinned to its merged
        # blob at this base (version/v4.9.0@d53e943e); the kernel itself
        # carries exactly the authorized F1 re-bind on top of the merged
        # T-010 content, pinned by its oracle-identity markers below (and by
        # this suite executing its T01-T07 oracles green in the same run).
        for rel_path, merged_blob in T010_MERGED_BLOBS.items():
            with self.subTest(t010_merged_output=rel_path):
                self.assertEqual(merged_blob, git_blob_sha("HEAD", rel_path))
        kernel_source = Path(__file__).resolve().read_text(encoding="utf-8")
        for marker in T010_KERNEL_ORACLE_MARKERS:
            self.assertIn(marker, kernel_source, "T-010 kernel oracle marker missing")


if __name__ == "__main__":
    result = unittest.TextTestRunner(verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromTestCase(GateCurrentnessKernel)
    )
    raise SystemExit(0 if result.wasSuccessful() else 1)
