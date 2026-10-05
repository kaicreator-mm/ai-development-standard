"""v4.9 T014 downstream dogfood / independent safety-auditor contract kernel.

Deterministic stdlib-unittest evidence-contract kernel for
`references/DOWNSSTREAM_DOGFOOD_AUDIT_CONTRACT_V49.md`, binding TEST_MATRIX
oracles D01-D08 over `fixtures/dogfood-audit-contract/`. Consumes read-only:
Frozen Product §16 (blob a8ec7030a14337a4c2dca853dc474e965679d610), Frozen L2
§14 (blob bd41ea0175b459a6a490fd37ad579e429a58a1c3), the T-010 gate matrix
row M10, and the T-005 Release owner by reference (T-005->T-010->T-014
serialization: NO Release surface is edited).

This is Builder evidence only: it is not independent Validation, not a gate,
and never a source of verdicts. The kernel accepts or rejects a Proportional
Dogfood Report as release-consumable EVIDENCE; every outcome carries
authorizes_execution=false and authorizes_release_qualification=false, and
downstream generality satisfaction is an accounting result, never PASS/READY
(registries/state-dimensions-v1.json F13-F16). Ambiguous predicates fail
closed: unknown enums, missing required fields and model-resolved ambiguous
predicates reject; honest NOT_RUN/BLOCKED stays consumable but can never
satisfy downstream generality.
"""
from __future__ import annotations

import json
import re
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = ROOT / "fixtures" / "dogfood-audit-contract"
CONTRACT_DOC = ROOT / "references" / "DOWNSSTREAM_DOGFOOD_AUDIT_CONTRACT_V49.md"
REGISTRY = ROOT / "registries" / "state-dimensions-v1.json"

BASE_SHA = "d53e943ec7109648485b64a647ed2c7cf553531d"
BASE_TREE = "5ad2dbd8c312a67bb050a3199ab9b29b70c23406"
PACK_HEAD_SHA = "bd55620214ef00e93a307d3b7287837812a75ea4"
FROZEN_PRD_BLOB = "a8ec7030a14337a4c2dca853dc474e965679d610"
FROZEN_L2_BLOB = "bd41ea0175b459a6a490fd37ad579e429a58a1c3"
FROZEN_DAG_V02_BLOB = "b9fe0cc7089f64929b4bcf45f7230d950e864db2"

WRITE_SET = (
    "references/DOWNSSTREAM_DOGFOOD_AUDIT_CONTRACT_V49.md",
    "scripts/test_v49_dogfood_audit_contract.py",
    "fixtures/dogfood-audit-contract/",
)

PLANNING_PATHS = tuple(
    f".agent/execution/T-014/{name}"
    for name in (
        "MANIFEST.yaml",
        "EXECUTION_CONTRACT.md",
        "IMPLEMENTATION_MAP.md",
        "TEST_MATRIX.yaml",
        "FAILURE_MATRIX.yaml",
        "REVIEW_CHECKLIST.md",
    )
)

CANDIDATE_RE = re.compile(r"^candidate:[^@\s]+@sha:[0-9a-f]{40}$")

# PRD §16.5 mechanism families (machine ids; the contract doc §4 binds the mapping).
MECHANISM_VOCAB = {
    "OWNER_PERMITTED_REDUCTION",
    "CROSS_OWNER_FLOOR_COMPOSITION",
    "SAME_CONTAINER_PHASE_COALESCING",
    "GATE_OWNED_EVIDENCE_TRANSFER",
    "FAIL_CLOSED_UNKNOWN_AMBIGUOUS_PREDICATE",
    "NON_DISPATCH_WAIT",
    "PROSPECTIVE_RELEASE_APPLICABILITY_SELECTION",
}

STEP_CLASSES = {"REDUCTION", "COALESCING", "REUSE", "AVOIDED_KNOWN_BLOCKED_DISPATCH"}
ITEM_STATES = {"EXERCISED", "NOT_EXERCISED", "NOT_RUN", "BLOCKED"}
EXERCISE_STATES = {"EXERCISED", "NOT_RUN", "BLOCKED"}
EXERCISE_OUTCOMES = {"STRONGER_PATH", "BLOCKED", "MODEL_JUDGMENT"}

SAFETY_COUNTERS = (
    "UNAUTHORIZED_GATE_OMISSION",
    "STALE_PASS_TRANSFER",
    "INDEPENDENCE_LOSS",
    "CROSS_OWNER_REQUIREMENT_CANCELLATION",
    "ADVERSE_TERMINAL_SUPPRESSION",
)

SELF_AUTHORIZING_FIELDS = (
    "authorization",
    "authorizes_execution",
    "authorizes_release_qualification",
    "release_qualification_verdict",
    "gate_pass",
)

# Required record shape (contract §1). bound_ads_candidate/pinned_authority_refs
# are excluded here: they carry the dedicated D01 rejection reasons. delta_account
# is only required when a nonzero delta is claimed (D02/D04); safety_negatives has
# its dedicated MISSING_SAFETY_NEGATIVE_ACCOUNT check (D05 fail-closed).
REQUIRED_FIELDS = (
    "record_id",
    "downstream_repository",
    "legal_baseline_workflow",
    "selected_proportional_workflow",
    "mechanism_matrix",
    "claimed_mechanisms",
    "ambiguous_predicate_exercise",
    "baseline_vs_selected_delta_nonzero",
    "auditor",
    "manual_github_native_viability",
    "claim_boundary",
)

REJECTION_VOCAB = {
    "MISSING_REQUIRED_FIELD",
    "MISSING_EXACT_ADS_CANDIDATE",
    "MISSING_PINNED_AUTHORITY_REFS",
    "ILLEGAL_BASELINE_CONSTRUCTION",
    "INCONSISTENT_BASELINE_SELECTED",
    "UNACCOUNTED_PROPORTIONAL_DELTA",
    "UNMEASURED_COST_CLAIM",
    "INCOMPLETE_MECHANISM_MATRIX",
    "EXERCISED_WITHOUT_PROOF",
    "UNEXERCISED_CLAIM_BOUNDARY_MISSING",
    "AMBIGUOUS_PREDICATE_MODEL_RESOLVED",
    "AMBIGUOUS_PREDICATE_FAIL_CLOSED",
    "MISSING_SAFETY_NEGATIVE_ACCOUNT",
    "INELIGIBLE_AUDITOR",
    "AUDITOR_IS_TESTED_PRINCIPAL",
    "AUDITOR_PROFILE_REF_NOT_OWNER_SURFACE",
    "SELF_AUTHORIZING_FIELD",
}

OUTCOME_VOCAB = {
    "BOUND_CURRENT",
    "HISTORICAL_ONLY",
    "REJECTED",
    "SATISFIED",
    "NOT_SATISFIED",
    "NOT_EVALUATED",
    "ADS_CANDIDATE_DRIFT",
    "SAFETY_NEGATIVE_VIOLATION",
    "REQUIRED_AMBIGUOUS_EXERCISE_NOT_RUN",
    "MANUAL_VIABILITY_NOT_SATISFIED",
    "UNEXERCISED_MECHANISM_CLAIM_LIMITED",
    "COMPATIBILITY_EVIDENCE_ONLY",
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


def resolve_owner_ref(ref: str) -> None:
    """Assert an owner ref resolves in-repository (exact path + heading anchor)."""
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
    # other ref kinds (py/json): file existence is the resolution contract.


# ---------------------------------------------------------------------------
# kernel: evidence-contract evaluation (accept/reject as evidence; never verdicts)
# ---------------------------------------------------------------------------

def eligible_auditor(auditor: dict, eligible_owner_refs: set[str]) -> tuple[bool, str | None]:
    """D06: auditor eligibility by owner-surface profile refs; identity grants no authority."""
    if not isinstance(auditor, dict):
        return False, "INELIGIBLE_AUDITOR"
    profile_refs = auditor.get("eligibility_profile_refs")
    if not isinstance(profile_refs, list) or not profile_refs:
        return False, "INELIGIBLE_AUDITOR"
    if any(ref not in eligible_owner_refs for ref in profile_refs):
        return False, "AUDITOR_PROFILE_REF_NOT_OWNER_SURFACE"
    tested_principals = auditor.get("tested_decision_principal_ids") or []
    if auditor.get("is_orchestrator_principal") is True or auditor.get("auditor_id") in tested_principals:
        return False, "AUDITOR_IS_TESTED_PRINCIPAL"
    return True, None


def evaluate_report(report: dict, current_ads_candidate: str, eligible_owner_refs: set[str]) -> dict:
    """Accept or reject a Proportional Dogfood Report as release-consumable evidence.

    Deterministic and fail-closed: any unknown enum, missing required field, or
    contradictory state rejects. The result is EVIDENCE accounting only; it
    always carries authorizes_execution=false and
    authorizes_release_qualification=false (contract §8 / Frozen L2 §14).
    """
    result = {
        "accepted_as_release_evidence": False,
        "disposition": "REJECTED",
        "downstream_generality": "NOT_EVALUATED",
        "reason": None,
        "release_owner_reevaluation_required": False,
        "compatibility_evidence_only": False,
        "generality_limited_to_exercised_mechanisms": None,
        "authorizes_execution": False,
        "authorizes_release_qualification": False,
    }

    def reject(reason: str) -> dict:
        # A late rejection (after the BOUND_CURRENT routing branch) must fully
        # reset the evidence posture: the record is not consumable as-is.
        result["accepted_as_release_evidence"] = False
        result["disposition"] = "REJECTED"
        result["downstream_generality"] = "NOT_EVALUATED"
        result["release_owner_reevaluation_required"] = False
        result["reason"] = reason
        return result

    # D07: a self-authorizing record is rejected before anything else; no field
    # of the report can ever mint execution or Release Qualification authority.
    if any(field in report for field in SELF_AUTHORIZING_FIELDS):
        return reject("SELF_AUTHORIZING_FIELD")

    # Fail-closed required record shape (contract §1).
    missing = [name for name in REQUIRED_FIELDS if report.get(name) in (None, "", [], {})]
    if missing:
        return reject("MISSING_REQUIRED_FIELD")

    # D06: independent auditor eligibility (identity can never grant authority).
    ok, reason = eligible_auditor(report["auditor"], eligible_owner_refs)
    if not ok:
        return reject(reason)

    # D01: exact ADS candidate binding.
    if not CANDIDATE_RE.match(str(report.get("bound_ads_candidate") or "")):
        return reject("MISSING_EXACT_ADS_CANDIDATE")
    pinned = report.get("pinned_authority_refs")
    if not isinstance(pinned, list) or not pinned:
        return reject("MISSING_PINNED_AUTHORITY_REFS")

    # D01/M10 routing: exact-candidate match => BOUND_CURRENT; drift => HISTORICAL_ONLY.
    if report["bound_ads_candidate"] != current_ads_candidate:
        result["accepted_as_release_evidence"] = True  # historical truth stays durable
        result["disposition"] = "HISTORICAL_ONLY"
        result["reason"] = "ADS_CANDIDATE_DRIFT"
        result["release_owner_reevaluation_required"] = True
        return result
    result["accepted_as_release_evidence"] = True
    result["disposition"] = "BOUND_CURRENT"

    # D02: legal baseline vs selected accounting.
    baseline = report["legal_baseline_workflow"]
    if baseline.get("legal_under_bound_authority") is not True or baseline.get("invented_maximum_ceremony") is not False:
        return reject("ILLEGAL_BASELINE_CONSTRUCTION")
    if baseline.get("workflow_id") == report["selected_proportional_workflow"].get("workflow_id"):
        if report["baseline_vs_selected_delta_nonzero"] is True:
            return reject("INCONSISTENT_BASELINE_SELECTED")
    delta = report["baseline_vs_selected_delta_nonzero"]
    if delta not in (True, False):
        return reject("AMBIGUOUS_PREDICATE_FAIL_CLOSED")
    if delta is True:
        entries = report["delta_account"]
        if not entries:
            return reject("UNACCOUNTED_PROPORTIONAL_DELTA")
        for entry in entries:
            if not entry.get("step_ref") or not str(entry.get("decision_value_account") or "").strip():
                return reject("UNACCOUNTED_PROPORTIONAL_DELTA")
            if entry.get("mechanism") not in MECHANISM_VOCAB or entry.get("class") not in STEP_CLASSES:
                return reject("AMBIGUOUS_PREDICATE_FAIL_CLOSED")
    cost = report.get("orchestration_cost_claim")
    if cost is not None:
        if cost.get("claim") == "MEASURED" and not (cost.get("proof_refs") or []):
            return reject("UNMEASURED_COST_CLAIM")
        if cost.get("claim") not in ("MEASURED", "NOT_MEASURED"):
            return reject("AMBIGUOUS_PREDICATE_FAIL_CLOSED")

    # D03: mechanism exercise matrix completeness.
    claimed = report["claimed_mechanisms"]
    if any(m not in MECHANISM_VOCAB for m in claimed):
        return reject("AMBIGUOUS_PREDICATE_FAIL_CLOSED")
    matrix = {row.get("mechanism"): row for row in report["mechanism_matrix"]}
    if any(m not in MECHANISM_VOCAB for m in matrix):
        return reject("AMBIGUOUS_PREDICATE_FAIL_CLOSED")
    if any(m not in matrix for m in claimed):
        return reject("INCOMPLETE_MECHANISM_MATRIX")
    for mech, row in matrix.items():
        state = row.get("state")
        if state not in ITEM_STATES:
            return reject("AMBIGUOUS_PREDICATE_FAIL_CLOSED")
        if state == "EXERCISED" and not (row.get("proof_refs") or []):
            return reject("EXERCISED_WITHOUT_PROOF")
        if state == "NOT_EXERCISED" and not str(row.get("claim_boundary") or "").strip():
            return reject("UNEXERCISED_CLAIM_BOUNDARY_MISSING")
        if state in ("NOT_RUN", "BLOCKED") and not str(row.get("reason_ref") or "").strip():
            return reject("MISSING_REQUIRED_FIELD")

    # D05: ambiguous predicate fail-closed exercise (PRD §16.5; L2 §16 U3).
    exercise = report["ambiguous_predicate_exercise"]
    if exercise.get("state") not in EXERCISE_STATES:
        return reject("AMBIGUOUS_PREDICATE_FAIL_CLOSED")
    ambiguous_not_run = exercise["state"] in ("NOT_RUN", "BLOCKED")
    if ambiguous_not_run:
        if not str(exercise.get("reason_ref") or "").strip():
            return reject("MISSING_REQUIRED_FIELD")
    else:
        outcome = exercise.get("outcome")
        if outcome == "MODEL_JUDGMENT":
            return reject("AMBIGUOUS_PREDICATE_MODEL_RESOLVED")
        if outcome not in ("STRONGER_PATH", "BLOCKED"):
            return reject("AMBIGUOUS_PREDICATE_FAIL_CLOSED")

    # Safety-negative account (PRD §16.7): all five counters required.
    negatives = report.get("safety_negatives")
    if not isinstance(negatives, dict) or any(counter not in negatives for counter in SAFETY_COUNTERS):
        return reject("MISSING_SAFETY_NEGATIVE_ACCOUNT")
    violated = [c for c in SAFETY_COUNTERS if negatives[c] != 0]
    if violated:
        result["downstream_generality"] = "NOT_SATISFIED"
        result["reason"] = f"SAFETY_NEGATIVE_VIOLATION:{violated[0]}"
        return result

    # Manual/GitHub-native viability (PRD §16.8).
    manual = report["manual_github_native_viability"]
    if manual.get("state") not in ITEM_STATES:
        return reject("AMBIGUOUS_PREDICATE_FAIL_CLOSED")
    if manual["state"] == "EXERCISED" and not (manual.get("proof_refs") or []):
        return reject("EXERCISED_WITHOUT_PROOF")
    if manual["state"] in ("NOT_RUN", "BLOCKED") and not str(manual.get("reason_ref") or "").strip():
        return reject("MISSING_REQUIRED_FIELD")
    manual_not_satisfied = manual["state"] in ("NOT_EXERCISED", "NOT_RUN", "BLOCKED")

    # Downstream generality accounting (PRD §16.5-§16.9; never a gate verdict).
    if ambiguous_not_run:
        result["downstream_generality"] = "NOT_SATISFIED"
        result["reason"] = "REQUIRED_AMBIGUOUS_EXERCISE_NOT_RUN"
    elif manual_not_satisfied:
        result["downstream_generality"] = "NOT_SATISFIED"
        result["reason"] = "MANUAL_VIABILITY_NOT_SATISFIED"
    elif delta is not True:
        result["downstream_generality"] = "NOT_SATISFIED"
        result["reason"] = "COMPATIBILITY_EVIDENCE_ONLY"
        result["compatibility_evidence_only"] = True
    else:
        result["downstream_generality"] = "SATISFIED"
        unexercised = sorted(m for m, row in matrix.items() if row["state"] != "EXERCISED")
        if unexercised:
            result["reason"] = "UNEXERCISED_MECHANISM_CLAIM_LIMITED"
            result["generality_limited_to_exercised_mechanisms"] = sorted(
                m for m, row in matrix.items() if row["state"] == "EXERCISED"
            )
    return result


# ---------------------------------------------------------------------------
# kernel tests (TEST_MATRIX D01-D08)
# ---------------------------------------------------------------------------

class DogfoodAuditContractKernel(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.doc = CONTRACT_DOC.read_text(encoding="utf-8")
        cls.registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        cls.owner_surfaces = load_fixture("owner_surfaces.json")
        cls.report_acceptance = load_fixture("report_acceptance.json")
        cls.auditor_eligibility = load_fixture("auditor_eligibility.json")
        cls.fail_closed = load_fixture("fail_closed.json")
        cls.eligible_refs = set(cls.owner_surfaces["auditor_eligibility_owner_refs"])
        cls.all_scenarios = (
            cls.report_acceptance["scenarios"] + cls.fail_closed["scenarios"]
        )

    def _evaluate(self, scenario: dict) -> dict:
        return evaluate_report(
            scenario["report"], scenario["current_ads_candidate"], self.eligible_refs
        )

    def _assert_expect(self, scenario: dict, result: dict) -> None:
        expect = scenario["expect"]
        self.assertEqual(
            result["accepted_as_release_evidence"], expect["accepted_as_release_evidence"],
            scenario["scenario_id"],
        )
        self.assertEqual(result["disposition"], expect["disposition"], scenario["scenario_id"])
        self.assertEqual(
            result["downstream_generality"], expect["downstream_generality"], scenario["scenario_id"]
        )
        if "reason" in expect:
            self.assertEqual(result["reason"], expect["reason"], scenario["scenario_id"])
        if expect.get("release_owner_reevaluation_required"):
            self.assertTrue(result["release_owner_reevaluation_required"], scenario["scenario_id"])
        if expect.get("compatibility_evidence_only"):
            self.assertTrue(result["compatibility_evidence_only"], scenario["scenario_id"])
        if expect.get("generality_limited_to_exercised_mechanisms") is not None:
            self.assertEqual(
                result["generality_limited_to_exercised_mechanisms"],
                expect["generality_limited_to_exercised_mechanisms"],
                scenario["scenario_id"],
            )
        if "authorizes_execution" in expect:
            self.assertFalse(result["authorizes_execution"], scenario["scenario_id"])
        if "authorizes_release_qualification" in expect:
            self.assertFalse(result["authorizes_release_qualification"], scenario["scenario_id"])

    # ---------- D01: exact ADS candidate binding ----------

    def test_d01_exact_candidate_binding_or_reject(self) -> None:
        scenarios = [s for s in self.report_acceptance["scenarios"] if s["oracle"] == "D01"]
        self.assertGreaterEqual(len(scenarios), 3)
        for scenario in scenarios:
            with self.subTest(scenario=scenario["scenario_id"]):
                self._assert_expect(scenario, self._evaluate(scenario))

    # ---------- D02: legal baseline vs selected workflow accounting ----------

    def test_d02_baseline_selected_accounting_or_reject(self) -> None:
        scenarios = [s for s in self.report_acceptance["scenarios"] if s["oracle"] == "D02"]
        self.assertGreaterEqual(len(scenarios), 3)
        for scenario in scenarios:
            with self.subTest(scenario=scenario["scenario_id"]):
                self._assert_expect(scenario, self._evaluate(scenario))

    # ---------- D03: mechanism exercise matrix complete ----------

    def test_d03_mechanism_matrix_complete_or_reject(self) -> None:
        scenarios = [s for s in self.report_acceptance["scenarios"] if s["oracle"] == "D03"]
        self.assertGreaterEqual(len(scenarios), 3)
        for scenario in scenarios:
            with self.subTest(scenario=scenario["scenario_id"]):
                self._assert_expect(scenario, self._evaluate(scenario))
        # The seven PRD §16.5 families are the whole mechanism vocabulary and
        # are bound in the contract doc (kernel/doc agreement).
        self.assertEqual(len(MECHANISM_VOCAB), 7)
        for mech in MECHANISM_VOCAB:
            self.assertIn(mech, self.doc)

    # ---------- D04: nonzero proportional delta enforced ----------

    def test_d04_nonzero_delta_required_for_generality(self) -> None:
        scenarios = [s for s in self.report_acceptance["scenarios"] if s["oracle"] == "D04"]
        self.assertGreaterEqual(len(scenarios), 2)
        for scenario in scenarios:
            with self.subTest(scenario=scenario["scenario_id"]):
                result = self._evaluate(scenario)
                self._assert_expect(scenario, result)
        # Zero delta can never satisfy downstream generality, whatever else is perfect.
        base = next(
            s for s in self.report_acceptance["scenarios"]
            if s["scenario_id"] == "D07_POS_perfect_report_still_authorizes_nothing"
        )
        zero = json.loads(json.dumps(base["report"]))
        zero["baseline_vs_selected_delta_nonzero"] = False
        zero["delta_account"] = []
        posture = evaluate_report(zero, base["current_ads_candidate"], self.eligible_refs)
        self.assertEqual(posture["downstream_generality"], "NOT_SATISFIED")
        self.assertEqual(posture["reason"], "COMPATIBILITY_EVIDENCE_ONLY")
        self.assertTrue(posture["compatibility_evidence_only"])

    # ---------- D05: ambiguous predicates fail closed ----------

    def test_d05_ambiguous_predicates_fail_closed(self) -> None:
        self.assertGreaterEqual(len(self.fail_closed["scenarios"]), 6)
        for scenario in self.fail_closed["scenarios"]:
            with self.subTest(scenario=scenario["scenario_id"]):
                self._assert_expect(scenario, self._evaluate(scenario))

    # ---------- D06: independent auditor eligibility/profile ----------

    def test_d06_auditor_eligibility_by_owner_refs(self) -> None:
        for scenario in self.auditor_eligibility["scenarios"]:
            with self.subTest(scenario=scenario["scenario_id"]):
                ok, reason = eligible_auditor(scenario["auditor"], self.eligible_refs)
                expect = scenario["expect"]
                self.assertEqual(ok, expect["eligible"], scenario["scenario_id"])
                if expect.get("reason"):
                    self.assertEqual(reason, expect["reason"], scenario["scenario_id"])
        # Every eligible profile ref resolves in-repository and is a fixture-bound
        # owner surface: eligibility is granted by owners, never by identity.
        for ref in self.auditor_eligibility["eligible_profile_owner_refs"]:
            resolve_owner_ref(ref)
            self.assertIn(ref, self.eligible_refs)
        # Identity alone grants nothing: the eligibility check never outputs authority.
        ok, _ = eligible_auditor({"auditor_id": "release-authority", "eligibility_profile_refs": sorted(self.eligible_refs)[0:1]}, self.eligible_refs)
        self.assertTrue(ok)  # eligible to CHECK the safety-negative account ...
        result = evaluate_report(
            {
                "record_id": "r", "downstream_repository": "d",
                "bound_ads_candidate": "candidate:x@sha:" + "0" * 40,
                "pinned_authority_refs": ["a"], "legal_baseline_workflow": {},
                "selected_proportional_workflow": {}, "mechanism_matrix": [],
                "claimed_mechanisms": [], "ambiguous_predicate_exercise": {},
                "baseline_vs_selected_delta_nonzero": None, "delta_account": [],
                "safety_negatives": {}, "auditor": {"auditor_id": "release-authority"},
                "manual_github_native_viability": {}, "claim_boundary": "",
            },
            "candidate:x@sha:" + "0" * 40,
            self.eligible_refs,
        )
        self.assertFalse(result["authorizes_execution"])
        self.assertFalse(result["authorizes_release_qualification"])

    # ---------- D07: evidence-only posture ----------

    def test_d07_report_cannot_self_authorize(self) -> None:
        scenarios = [s for s in self.report_acceptance["scenarios"] if s["oracle"] == "D07"]
        self.assertGreaterEqual(len(scenarios), 2)
        for scenario in scenarios:
            with self.subTest(scenario=scenario["scenario_id"]):
                self._assert_expect(scenario, self._evaluate(scenario))

    def test_d07_no_outcome_ever_authorizes(self) -> None:
        # Across EVERY scenario in every fixture: no evaluation output ever
        # carries execution or Release Qualification authorization.
        for scenario in self.all_scenarios:
            with self.subTest(scenario=scenario["scenario_id"]):
                result = self._evaluate(scenario)
                self.assertFalse(result["authorizes_execution"])
                self.assertFalse(result["authorizes_release_qualification"])
        # The result vocabulary carries no verdict token.
        for vocab in (OUTCOME_VOCAB, REJECTION_VOCAB):
            self.assertNotIn("PASS", vocab)
            self.assertNotIn("READY", vocab)
            self.assertNotIn("FAIL", vocab)
        # Currentness never mints PASS/READY (registry F13-F16, cited in doc).
        rule_ids = {r["rule_id"] for r in self.registry["forbidden_inferences"]}
        for rule in (
            "F13_ASSURANCE_CURRENT_NOT_VALIDATION_PASS",
            "F14_ASSURANCE_CURRENT_NOT_REVIEW_PASS",
            "F15_ASSURANCE_CURRENT_NOT_RELEASE_READY",
            "F16_ASSURANCE_CURRENT_NOT_TASK_READY",
        ):
            self.assertIn(rule, rule_ids)
        self.assertIn("F13–F16", self.doc)

    # ---------- D08: owner surfaces cited not copied; surfaces unmutated ----------

    def test_d08_owner_refs_resolve_and_are_cited(self) -> None:
        for ref in self.owner_surfaces["consumed_authority_refs"]:
            with self.subTest(ref=ref):
                resolve_owner_ref(ref)
                self.assertIn(f"\n{ref}\n", self.doc, f"owner ref not cited line-verbatim: {ref}")
        for ref in self.owner_surfaces["auditor_eligibility_owner_refs"]:
            with self.subTest(ref=ref):
                resolve_owner_ref(ref)
                self.assertIn(f"\n{ref}\n", self.doc, f"eligibility ref not cited: {ref}")

    def test_d08_owner_text_not_copied_and_no_minting(self) -> None:
        # Owner sentences stay in their owners; this contract paraphrases and cites.
        for sentence in self.owner_surfaces["owner_sentences_must_not_be_copied"]:
            self.assertNotIn(sentence, self.doc)
        for mint in self.owner_surfaces["forbidden_mint_strings"]:
            self.assertNotIn(mint, self.doc)
        # Doc/kernel/fixture vocabulary agreement (contract §13).
        for token in REJECTION_VOCAB | OUTCOME_VOCAB:
            self.assertIn(token, self.doc, f"vocab token missing from contract doc: {token}")
        for scenario in self.all_scenarios:
            reason = scenario["expect"].get("reason")
            if reason:
                self.assertIn(reason.split(":")[0], REJECTION_VOCAB | OUTCOME_VOCAB, scenario["scenario_id"])
        self.assertTrue(self.owner_surfaces["expect"]["owner_surfaces_cited_not_copied"])
        self.assertEqual(self.owner_surfaces["expect"]["release_surface_edits"], 0)
        self.assertEqual(self.owner_surfaces["expect"]["product_l2_dag_mutation"], 0)

    def test_d08_frozen_authority_and_release_surfaces_unmutated(self) -> None:
        # Frozen Product / L2 / DAG blobs resolve unchanged at the candidate.
        self.assertEqual(FROZEN_PRD_BLOB, git_blob_sha("HEAD", "docs/implementation/4.9.0/PRD.md"))
        self.assertEqual(FROZEN_L2_BLOB, git_blob_sha("HEAD", "docs/implementation/4.9.0/L2_ARCHITECTURE_EVIDENCE.md"))
        self.assertEqual(FROZEN_DAG_V02_BLOB, git_blob_sha("HEAD", "docs/implementation/4.9.0/TASK_DAG.md"))
        # The lane builds on the admitted base (lineage anchor).
        self.assertEqual(BASE_TREE, git("rev-parse", f"{BASE_SHA}^{{tree}}"))
        # Immutable T-014 planning files are unmutated since the execution pack head.
        for rel_path in PLANNING_PATHS:
            with self.subTest(planning_path=rel_path):
                self.assertEqual(git_blob_sha(PACK_HEAD_SHA, rel_path), git_blob_sha("HEAD", rel_path))
        # Read-only owner surfaces (incl. every Release surface — T-005->T-010->T-014
        # serialization) are unmutated since the base.
        for rel_path in self.owner_surfaces["unmutated_since_base"]:
            with self.subTest(read_only=rel_path):
                self.assertEqual(git_blob_sha(BASE_SHA, rel_path), git_blob_sha("HEAD", rel_path))

    def test_d08_working_tree_and_candidate_diff_stay_in_write_set(self) -> None:
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
        diff_paths = git("diff", "--name-only", f"{PACK_HEAD_SHA}..HEAD").splitlines()
        for path in diff_paths:
            with self.subTest(diff_path=path):
                self.assertTrue(
                    any(path == w or path.startswith(w) for w in WRITE_SET),
                    f"committed path outside Builder write set: {path}",
                )


if __name__ == "__main__":
    result = unittest.TextTestRunner(verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromTestCase(DogfoodAuditContractKernel)
    )
    raise SystemExit(0 if result.wasSuccessful() else 1)
