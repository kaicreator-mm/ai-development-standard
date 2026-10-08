"""V410-T08A: visible whole-project integration runner (single integration entrypoint).

Executes the dryrun-designed visible regression command family
(#864@6040893503, LOCAL_INTEGRATION_RUNNER_DRYRUN_R1) on ONE exact candidate
and emits ONE machine-readable integration admission record. The runner was
rebound at the V410-T08A JIT to the actual post-#863 integrated candidate
(base 402bf289 / tree 2af7450f): the #861/#862/#863 suites are inserted into
TIER-2 by dependency order (T06B -> T07A -> T07B), exactly as the dryrun's
insertion rule requires.

Deterministic 4-tier order (dryrun-validated, rebound):
  TIER-0 gates (FAIL_FAST): verify_standard + test_protocol_schemas.
  TIER-1 lifecycle/authority (continue-within-tier): stage1, owner_convergence,
      t01b, t02a.
  TIER-2 concern suites (continue-within-tier, batch defect discovery): t02b,
      t03a, v43_task_decomposition, t04a, t04b, t05a, t06b_core_inventory(#861),
      t06b_multi_dispatch_conformance(#861), t07a_acceptance_projection(#862),
      t07b_decision_record(#863), test_execution_architecture,
      test_v34_review_repairs, verify_event_writer_surfaces,
      test_pointer_only_trigger_contract.
  TIER-3 integration-only (runs ONLY if zero defects so far, else HALT before
      integration admission): cross-suite conflict audit (candidate-registry
      agreement across the three positional registries + predecessor-chain
      ancestry + inventory completeness) + clean-tree proof + the integration
      admission record itself.

False-green oracle guards (#864@6043181240, WEB_INTEGRATION_FALSE_GREEN_ORACLE_R1):
  F1/F5 exact-subject equality before/after (stale/mixed evidence rejected);
  F2 required-inventory completeness (a missing or unexecuted suite can never
      aggregate green); F3 cross-suite contradiction audit; F4 clean-tree proof
      (pre-run, per-command, post-run); F6 no repair while validating (the
      runner never writes into the tree; any defect is routed, never absorbed);
      F8 the visible-PASS disclaimer is mandatory on every record and
      Hidden/Release-Qualification/Candidate-Freeze verdicts are structurally
      NOT_CLAIMED; F9 skipped / zero-collected suites are FAIL, never green
      (NOT_APPLICABLE requires owning authority this runner never holds);
      F10 tested_head vs emission head carried separately; F11 evidence reuse
      is NONE by construction (every run re-executes the full inventory).

Owner routing: every failure produces a routing row naming the owning concern
(never silently absorbed). T08A performs NO semantic repair.

VISIBILITY BOUNDARY (verbatim obligation): visible integration PASS is not
Hidden Validation or Release Qualification PASS. This runner grants no
Candidate Freeze, no V01 dispatch, no Release authority.

Purely local; no network; stdlib only.
"""

from __future__ import annotations

import argparse
import json
import platform
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

RUNNER_VERSION = "V410-T08A-R1"
TASK = "V410-T08A"
DISPATCH_ISSUE = "#864"
# Generation-2 successor adoption (dispatch V410-T08A-BUILDER-R2): the audited
# R1 candidate (86830d94, 15 files) is adopted verbatim under the new lawful
# admission->claim chain, closing the R1 FAIL findings P1-PV2/P1-PV1 (#864@6061280237).
PROPOSAL_REF = "#864@6061672692"
ADMISSION_CLAIM_REF = "#864@6061706724"
DRYRUN_DESIGN_REF = "#864@6040893503"
FALSE_GREEN_ORACLE_REF = "#864@6043181240"
IMPACT_INVENTORY_REF = "#864@6037701635"

RECORD_SCHEMA = "v410-integration-runner-result-v1"
INVENTORY_SCHEMA = "v410-integration-runner-inventory-v1"
DISCLAIMER = "VISIBLE INTEGRATION PASS IS NOT HIDDEN VALIDATION OR RELEASE QUALIFICATION PASS"

# Exact rebind subject of this runner (the merged #934 integration tip =
# V410-T07B INTEGRATED = V410-T08A's own base).
BASE_SHA = "402bf2899a7e1cd43eea3e7d78a37c947fe28c46"
BASE_TREE = "2af7450ff8312bd8652742996071252c42abe65e"

# Full predecessor merge chain (integration-impact inventory #864@6037701635,
# rebound: #861@0518202c -> #862@cea2e0cc -> #863@402bf289). Drift anywhere in
# this chain fails the record (F1/F7) — never silently absorbed.
PREDECESSOR_CHAIN = (
    {"merge": "#861", "task": "V410-T06B", "sha": "0518202c715dcf91784a694bdf4a8eeeaeb16ab6"},
    {"merge": "#862", "task": "V410-T07A", "sha": "cea2e0ccd045e8fcebaf110273129b198ed259fd"},
    {"merge": "#863", "task": "V410-T07B", "sha": "402bf2899a7e1cd43eea3e7d78a37c947fe28c46"},
)

TIER_POLICIES = {0: "FAIL_FAST", 1: "CONTINUE_WITHIN_TIER", 2: "CONTINUE_WITHIN_TIER", 3: "INTEGRATION_ONLY"}

# Routing vocabulary (integration-impact inventory #864@6037701635 OWNER_ROUTING
# + false-green oracle OWNER_ROUTING #864@6043181240). The catch-all routes to
# Controller arbitration — a defect is never silently absorbed. Defined before
# COMMAND_INVENTORY because the inventory itself names each suite's owner.
CONTROLLER_ARBITRATION = "CONTROLLER_ARBITRATION (merge/validation owner)"

# unittest-style suites report "Ran N tests"; verifier scripts do not. A
# zero-collected unittest run is FAIL (F9): a skipped or empty required suite
# is never green — NOT_APPLICABLE would need owning authority this runner
# never grants.
VERIFIER_SUITES = frozenset({"verify_standard", "verify_event_writer_surfaces"})

RAN_TESTS_RE = re.compile(r"^Ran (\d+) tests?", re.MULTILINE)

COMMAND_INVENTORY = (
    # (tier, suite, script, owning_concern)
    (0, "verify_standard", "scripts/verify_standard.py",
     CONTROLLER_ARBITRATION),
    (0, "test_protocol_schemas", "scripts/test_protocol_schemas.py",
     "V410-T06B (#861)"),
    (1, "test_v410_stage1_lifecycle_contracts", "scripts/test_v410_stage1_lifecycle_contracts.py",
     "V410-T01A (Stage-1 lifecycle owners)"),
    (1, "test_v410_owner_convergence", "scripts/test_v410_owner_convergence.py",
     "V410-T06A (#860)"),
    (1, "test_v410_t01b_product_projections", "scripts/test_v410_t01b_product_projections.py",
     "V410-T01B (#856 lineage)"),
    (1, "test_v410_t02a_collaboration_control", "scripts/test_v410_t02a_collaboration_control.py",
     "V410-T02A"),
    (2, "test_v410_t02b_machine_projection", "scripts/test_v410_t02b_machine_projection.py",
     "V410-T02B"),
    (2, "test_v410_t03a_implementation_quality", "scripts/test_v410_t03a_implementation_quality.py",
     "V410-T03A"),
    (2, "test_v43_task_decomposition", "scripts/test_v43_task_decomposition.py",
     "v4.3 TASK_DECOMPOSITION_STANDARD owner"),
    (2, "test_v410_t04a_gate_repair_routing", "scripts/test_v410_t04a_gate_repair_routing.py",
     "V410-T04A (#854)"),
    (2, "test_v410_t04b_review_currentness", "scripts/test_v410_t04b_review_currentness.py",
     "V410-T04B (#857)"),
    (2, "test_v410_t05a_shared_code_safety", "scripts/test_v410_t05a_shared_code_safety.py",
     "V410-T05A"),
    (2, "test_v410_t06b_core_inventory", "scripts/test_v410_t06b_core_inventory.py",
     "V410-T06B (#861)"),
    (2, "test_v410_t06b_multi_dispatch_conformance", "scripts/test_v410_t06b_multi_dispatch_conformance.py",
     "V410-T06B (#861)"),
    (2, "test_v410_t07a_acceptance_projection", "scripts/test_v410_t07a_acceptance_projection.py",
     "V410-T07A (#862)"),
    (2, "test_v410_t07b_decision_record", "scripts/test_v410_t07b_decision_record.py",
     "V410-T07B (#863)"),
    (2, "test_execution_architecture", "scripts/test_execution_architecture.py",
     "V410-T06B (#861) + EXECUTION_ARCHITECTURE_STANDARD owner"),
    (2, "test_v34_review_repairs", "scripts/test_v34_review_repairs.py",
     "v3.4 lifecycle/review-repair owner"),
    (2, "verify_event_writer_surfaces", "scripts/verify_event_writer_surfaces.py",
     "V410-T02B (event-v2 machine projection) + historical event-v1 reference owners"),
    (2, "test_pointer_only_trigger_contract", "scripts/test_pointer_only_trigger_contract.py",
     "v4.0 pointer-only execution-foundation owner"),
)

REQUIRED_SUITES = frozenset(entry[1] for entry in COMMAND_INVENTORY)
SUITES_BY_NAME = {entry[1]: entry for entry in COMMAND_INVENTORY}

# Routing vocabulary continued: every suite in the inventory names its owning
# concern; the catch-all is CONTROLLER_ARBITRATION.
KNOWN_OWNERS = frozenset(entry[3] for entry in COMMAND_INVENTORY) | {CONTROLLER_ARBITRATION}

DEFECT_CLASSES = frozenset(
    {
        "SUITE_FAILURE",
        "INVENTORY_MISSING",
        "ZERO_TESTS_COLLECTED",
        "TREE_MUTATION",
        "CANDIDATE_DRIFT",
        "PREDECESSOR_CHAIN_DRIFT",
        "CROSS_SUITE_CONTRADICTION",
        "PRE_RUN_REFUSAL",
    }
)
SEVERITIES = frozenset({"P0", "P1", "P2", "P3"})
INTEGRATION_VERDICTS = frozenset({"VISIBLE_INTEGRATION_PASS", "VISIBLE_INTEGRATION_FAIL"})
NOT_CLAIMED = "NOT_CLAIMED"


def _git(args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(["git"] + args, cwd=ROOT, capture_output=True, text=True)


def git_head() -> tuple[str, str]:
    result = _git(["rev-parse", "HEAD"])
    if result.returncode != 0:
        raise RuntimeError(f"cannot resolve HEAD: {result.stderr.strip()}")
    head = result.stdout.strip()
    tree = _git(["rev-parse", "HEAD^{tree}"]).stdout.strip()
    return head, tree


def porcelain_lines() -> int:
    result = _git(["status", "--porcelain"])
    return len([line for line in result.stdout.splitlines() if line.strip()])


def is_ancestor(ancestor: str, descendant: str) -> bool:
    return _git(["merge-base", "--is-ancestor", ancestor, descendant]).returncode == 0


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def suite_owner(suite: str) -> str:
    entry = SUITES_BY_NAME.get(suite)
    return entry[3] if entry else CONTROLLER_ARBITRATION


def build_route(
    defect_id: str,
    discovered_by_suite: str,
    tier: int,
    defect_class: str,
    severity: str,
) -> dict:
    """Owner-routed failure classification — never silently absorbed."""
    return {
        "defect_id": defect_id,
        "discovered_by_suite": discovered_by_suite,
        "tier": tier,
        "defect_class": defect_class,
        "owning_concern": suite_owner(discovered_by_suite),
        "severity": severity,
        "repair_dispatch_ref": "TO_BE_ISSUED_BY_CONTROLLER",
        "revalidation_scope": "affected suite + TIER-0 re-gate + dependent tiers on the repaired candidate",
    }


def empty_oracle_checks() -> dict:
    return {
        "F1_F5_exact_subject_equality": "PENDING",
        "F2_inventory_complete": "PENDING",
        "F3_cross_suite_audit": "PENDING",
        "F4_clean_tree": "PENDING",
        "F6_no_repair_while_validating": "PENDING",
        "F8_no_hidden_rq_claim": "ENFORCED",
        "F9_zero_collected_guard": "PENDING",
        "F10_tested_head_separation": "CARRIED",
        "F11_no_evidence_reuse": "ENFORCED",
    }


def build_record(head: str, tree: str) -> dict:
    return {
        "record_schema": RECORD_SCHEMA,
        "runner_version": RUNNER_VERSION,
        "task": TASK,
        "dispatch_ref": DISPATCH_ISSUE,
        "admission_refs": {"proposal": PROPOSAL_REF, "admission_claim": ADMISSION_CLAIM_REF},
        "design_refs": {"runner_order": DRYRUN_DESIGN_REF, "false_green_oracle": FALSE_GREEN_ORACLE_REF,
                         "impact_inventory": IMPACT_INVENTORY_REF},
        "exact_subject": {
            "base_sha": BASE_SHA,
            "base_tree": BASE_TREE,
            "tested_head_sha": head,
            "tested_head_tree": tree,
            "head_at_emission_sha": head,
            "base_is_ancestor_of_head": True,
        },
        "predecessor_chain": [
            {**entry, "integrated": True, "ancestor_of_head": True} for entry in PREDECESSOR_CHAIN
        ],
        "predecessor_chain_intact": True,
        "executor_identity": {
            "runner": "scripts/run_v410_integration.py",
            "platform": platform.platform(),
            "python": platform.python_version(),
        },
        "started_at": utc_now(),
        "finished_at": None,
        "tier_results": [],
        "suite_rows": [],
        "executed_count": 0,
        "required_count": len(COMMAND_INVENTORY),
        "inventory_complete": False,
        "clean_tree_proof": {
            "pre_run_clean": False,
            "post_run_clean": False,
            "per_command_clean": True,
            "porcelain_lines_post": None,
            "source_modifications_after_validation": False,
        },
        "oracle_checks": empty_oracle_checks(),
        "cross_suite_audit": None,
        "defect_routes": [],
        "halted_at": None,
        "integration_verdict": "VISIBLE_INTEGRATION_FAIL",
        "hidden_validation_verdict": NOT_CLAIMED,
        "release_qualification_verdict": NOT_CLAIMED,
        "candidate_freeze_verdict": NOT_CLAIMED,
        "v01_dispatch_gate": "NOT_DISPATCHABLE_BY_THIS_RUNNER",
        "evidence_reuse": "NONE",
        "integration_admission": "REFUSED",
        "disclaimer": DISCLAIMER,
    }


def run_suite_command(entry: tuple, head: str, tree: str) -> tuple[dict, bool]:
    """Execute one command; returns (row, tree_still_clean)."""
    tier, suite, script, _owner = entry
    command = [sys.executable, script]
    started = time.perf_counter()
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
    duration = round(time.perf_counter() - started, 3)
    # unittest's TextTestRunner writes the "Ran N tests" summary and the
    # per-test list to STDERR by default (stdout stays empty for unittest
    # suites). F9 therefore scans the combined output — exit codes still carry
    # the verdict, this only makes collected-test detection truthful.
    combined = (result.stdout or "") + (result.stderr or "")
    ran = RAN_TESTS_RE.search(combined)
    tests_collected = int(ran.group(1)) if ran else None
    if suite in VERIFIER_SUITES:
        output_ok = bool(combined.strip())
    else:
        output_ok = tests_collected is not None and tests_collected > 0
    clean = porcelain_lines() == 0
    verdict = "PASS" if (result.returncode == 0 and output_ok and clean) else "FAIL"
    row = {
        "suite": suite,
        "exact_command": f"{sys.executable} {script}",
        "tier": tier,
        "candidate_sha": head,
        "candidate_tree": tree,
        "exit_code": result.returncode,
        "duration_s": duration,
        "tests_collected": tests_collected,
        "verdict": verdict,
        "artifact_writing_flag": "NONE" if clean else "TREE_MUTATED",
        "output_tail": "\n".join(combined.strip().splitlines()[-3:]),
        "timestamp": utc_now(),
        "owner_concern": entry[3],
    }
    return row, clean


def cross_suite_audit(record: dict) -> tuple[bool, dict, list[dict]]:
    """TIER-3 integration-only conflict audit (no semantic repair, read-only)."""
    findings: list[str] = []
    sys.path.insert(0, str(ROOT / "scripts"))
    expected_active = TASK
    registries = {}
    try:
        import test_v410_owner_convergence as oc  # noqa: E402
        import test_v410_t07a_acceptance_projection as t07a  # noqa: E402
        import test_v410_t07b_decision_record as t07b  # noqa: E402

        registries["test_v410_owner_convergence"] = oc.CandidateShapeTests.TASK_CANDIDATES
        registries["test_v410_t07a_acceptance_projection"] = t07a.ProjectionSurfaceConformanceTests.TASK_CANDIDATES
        registries["test_v410_t07b_decision_record"] = t07b.PackAndCandidateSurfaceTests.TASK_CANDIDATES
    except Exception as exc:  # pragma: no cover - import environment failure is a defect, not a crash
        findings.append(f"candidate-registry import failed: {exc}")
        registries = {}

    for name, candidates in registries.items():
        actives = [entry["task"] for entry in candidates if entry.get("active")]
        if actives != [expected_active]:
            findings.append(
                f"{name}: active candidate registry disagrees (active={actives}, expected=['{expected_active}'])"
            )
        for entry in candidates:
            if entry.get("active") and entry.get("base") != BASE_SHA:
                findings.append(f"{name}: active candidate base {entry.get('base')} != {BASE_SHA}")

    head, tree = git_head()
    if (head, tree) != (
        record["exact_subject"]["tested_head_sha"],
        record["exact_subject"]["tested_head_tree"],
    ):
        findings.append("candidate drift between suite execution and TIER-3 audit (F1/F5)")
    for entry in PREDECESSOR_CHAIN:
        if not is_ancestor(entry["sha"], head):
            findings.append(f"predecessor {entry['merge']} ({entry['task']}) not an ancestor of HEAD")
    if record["executed_count"] != record["required_count"]:
        findings.append("required inventory was not fully executed before the audit")

    audit = {
        "audit": "cross-suite conflict audit (registry agreement + subject equality + predecessor ancestry)",
        "registries_checked": sorted(registries),
        "findings": findings,
        "verdict": "PASS" if not findings else "FAIL",
    }
    routes = []
    if findings:
        routes.append(build_route("DEF-CROSS-SUITE", "cross_suite_audit", 3, "CROSS_SUITE_CONTRADICTION", "P1"))
    return not findings, audit, routes


def validate_result(record: dict) -> list[str]:
    """Fail-closed record-model validator (the runner refuses to emit a
    non-conformant record; the focused suite stress-tests it with mutants)."""
    problems: list[str] = []
    if record.get("record_schema") != RECORD_SCHEMA:
        problems.append("record_schema must be " + RECORD_SCHEMA)
    if record.get("disclaimer") != DISCLAIMER:
        problems.append("the visible-PASS disclaimer is mandatory and verbatim (F8)")
    for field in ("hidden_validation_verdict", "release_qualification_verdict", "candidate_freeze_verdict"):
        if record.get(field) != NOT_CLAIMED:
            problems.append(f"{field} must be {NOT_CLAIMED} on every visible-integration record (F8)")
    if record.get("integration_verdict") not in INTEGRATION_VERDICTS:
        problems.append("integration_verdict must be a VISIBLE_INTEGRATION_* verdict, never a Hidden/RQ verdict (F8)")
    if record.get("evidence_reuse") != "NONE":
        problems.append("evidence_reuse must be NONE: prior concern evidence is never reused (F11)")

    subject = record.get("exact_subject") or {}
    if subject.get("base_sha") != BASE_SHA or subject.get("base_tree") != BASE_TREE:
        problems.append("exact_subject must bind the rebind base " + f"{BASE_SHA}/{BASE_TREE} (F1 stale subject rejected)")
    for field in ("tested_head_sha", "tested_head_tree", "head_at_emission_sha"):
        value = subject.get(field, "")
        if not (isinstance(value, str) and re.fullmatch(r"[0-9a-f]{40}", value or "")):
            problems.append(f"exact_subject.{field} must be a 40-hex sha (F5 mixed-subject evidence rejected)")

    chain = record.get("predecessor_chain")
    expected_chain = [dict(entry, integrated=True, ancestor_of_head=True) for entry in PREDECESSOR_CHAIN]
    if chain != expected_chain:
        problems.append("predecessor chain drift (F1/F7): chain must equal " + repr(PREDECESSOR_CHAIN))
    if record.get("predecessor_chain_intact") is not True:
        problems.append("predecessor_chain_intact must be true (F7)")

    rows = record.get("suite_rows") or []
    by_suite: dict[str, list[dict]] = {}
    for row in rows:
        by_suite.setdefault(row.get("suite"), []).append(row)
    missing = sorted(REQUIRED_SUITES - set(by_suite))
    extra = sorted(set(by_suite) - REQUIRED_SUITES)
    if len(rows) != len(set(row.get("suite") for row in rows)):
        problems.append("duplicate suite rows in the record (F2)")
    if extra:
        problems.append(f"suite row outside the registered inventory (F2): {extra}")
    if record.get("integration_verdict") == "VISIBLE_INTEGRATION_PASS":
        if missing:
            problems.append(f"required suite missing from the executed inventory (F2): {missing}")
    elif missing and record.get("halted_at") is None:
        # An un-halted FAIL must still account for the complete inventory; a
        # halted FAIL legitimately leaves the post-halt remainder unexecuted.
        problems.append(f"un-halted FAIL record did not execute the complete inventory (F2): {missing}")

    verdict = record.get("integration_verdict")
    routes = record.get("defect_routes") or []
    clean = record.get("clean_tree_proof") or {}
    all_pass = bool(rows) and all(row.get("verdict") == "PASS" for row in rows)
    for row in rows:
        suite = row.get("suite")
        if suite not in REQUIRED_SUITES:
            continue
        row_verdict = row.get("verdict")
        if row_verdict == "PASS":
            if row.get("exit_code") != 0:
                problems.append(f"{suite}: PASS row with non-zero exit_code (false green)")
            if row.get("artifact_writing_flag") != "NONE":
                problems.append(f"{suite}: PASS row with a tree-mutating command (F4/F6)")
            if row.get("candidate_sha") != subject.get("tested_head_sha") or row.get("candidate_tree") != subject.get("tested_head_tree"):
                problems.append(f"{suite}: PASS row bound to a different subject than the record (F5)")
            if suite not in VERIFIER_SUITES and not (isinstance(row.get("tests_collected"), int) and row["tests_collected"] > 0):
                problems.append(f"{suite}: PASS row with zero/unknown tests collected (F9 — skipped is never green)")
        elif row_verdict == "NOT_RUN":
            if verdict == "VISIBLE_INTEGRATION_PASS":
                problems.append(f"{suite}: NOT_RUN row inside a PASS aggregate (F2/F9 — a skipped suite is never green)")
        elif row_verdict == "FAIL":
            if not any(route.get("discovered_by_suite") == suite for route in routes):
                problems.append(f"{suite}: FAIL row without an owner-routed defect row (F6 — never silently absorbed)")
        else:
            problems.append(f"{suite}: unknown row verdict {row_verdict!r}")
        if row.get("tier") != SUITES_BY_NAME[suite][0]:
            problems.append(f"{suite}: row tier does not match the registered tier")

    if verdict == "VISIBLE_INTEGRATION_PASS":
        if not all_pass:
            problems.append("VISIBLE_INTEGRATION_PASS requires every required suite row PASS (F2/F9)")
        if routes:
            problems.append("VISIBLE_INTEGRATION_PASS with open defect routes (F6 — defects are never absorbed)")
        if record.get("inventory_complete") is not True or record.get("executed_count") != record.get("required_count"):
            problems.append("VISIBLE_INTEGRATION_PASS requires the complete inventory executed (F2)")
        if record.get("halted_at") is not None:
            problems.append("VISIBLE_INTEGRATION_PASS with halted_at set")
        if clean.get("pre_run_clean") is not True or clean.get("post_run_clean") is not True:
            problems.append("VISIBLE_INTEGRATION_PASS requires a proven-clean tree (F4)")
        if clean.get("porcelain_lines_post") != 0:
            problems.append("VISIBLE_INTEGRATION_PASS requires 0 porcelain lines post-run (F4)")
        if clean.get("source_modifications_after_validation") is not False:
            problems.append("VISIBLE_INTEGRATION_PASS forbids post-validation source modification (F6)")
        if record.get("cross_suite_audit") is None or record["cross_suite_audit"].get("verdict") != "PASS":
            problems.append("VISIBLE_INTEGRATION_PASS requires a PASS cross-suite audit (F3)")
        oracle = record.get("oracle_checks") or {}
        for key, value in oracle.items():
            if value in ("PENDING", "VIOLATED", "FAIL"):
                problems.append(f"oracle check {key} is {value} on a PASS record")

    if verdict == "VISIBLE_INTEGRATION_FAIL":
        if not routes:
            problems.append("VISIBLE_INTEGRATION_FAIL without any defect route (classification mandatory)")
    for route in routes:
        if route.get("defect_class") not in DEFECT_CLASSES:
            problems.append(f"defect route {route.get('defect_id')} has unknown defect_class {route.get('defect_class')!r}")
        if route.get("severity") not in SEVERITIES:
            problems.append(f"defect route {route.get('defect_id')} has unknown severity {route.get('severity')!r}")
        if not route.get("owning_concern") or route.get("owning_concern") not in KNOWN_OWNERS:
            problems.append(f"defect route {route.get('defect_id')} must name a known owning concern (never absorbed)")
        if not route.get("repair_dispatch_ref"):
            problems.append(f"defect route {route.get('defect_id')} lacks repair_dispatch_ref")
    if record.get("integration_admission") not in ("RECORDED", "REFUSED"):
        problems.append("integration_admission must be RECORDED or REFUSED")
    if record.get("integration_admission") == "RECORDED" and verdict != "VISIBLE_INTEGRATION_PASS":
        problems.append("integration admission may only be RECORDED on a visible PASS")
    return problems


def execute(head: str, tree: str, ancestry_ok: bool, chain_intact: bool, pre_clean: bool) -> dict:
    record = build_record(head, tree)
    record["exact_subject"]["base_is_ancestor_of_head"] = ancestry_ok
    record["predecessor_chain_intact"] = chain_intact
    record["clean_tree_proof"]["pre_run_clean"] = pre_clean
    record["oracle_checks"]["F1_F5_exact_subject_equality"] = "ENFORCED" if ancestry_ok else "VIOLATED"
    record["oracle_checks"]["F4_clean_tree"] = "PASS" if pre_clean else "VIOLATED"
    record["started_at"] = utc_now()

    # Pre-run refusal: a dirty/uncommitted validation tree or a candidate that
    # lost the base/predecessor lineage is invalid exact-candidate evidence
    # (F4/F1/F7) — refuse before running anything.
    refusals: list[tuple[str, str, str]] = []
    if not pre_clean:
        refusals.append(("validation tree is dirty (F4)", "PRE_RUN_REFUSAL", "P0"))
    if not ancestry_ok:
        refusals.append(("HEAD does not descend from the rebind base (F1)", "CANDIDATE_DRIFT", "P0"))
    if not chain_intact:
        refusals.append(("predecessor merge chain drifted (F7)", "PREDECESSOR_CHAIN_DRIFT", "P0"))
    if refusals:
        for message, defect_class, severity in refusals:
            record["defect_routes"].append(build_route(f"DEF-PRE-{len(record['defect_routes']) + 1}", "pre_run_gate", 0, defect_class, severity))
        record["halted_at"] = "PRE_RUN_GATE"
        record["finished_at"] = utc_now()
        record["inventory_complete"] = False
        record["oracle_checks"]["F2_inventory_complete"] = "VIOLATED"
        record["integration_admission"] = "REFUSED"
        return record

    defects = 0
    halted = False
    for tier in (0, 1, 2):
        entries = [entry for entry in COMMAND_INVENTORY if entry[0] == tier]
        tier_defects = 0
        for entry in entries:
            row, clean = run_suite_command(entry, head, tree)
            record["suite_rows"].append(row)
            record["executed_count"] += 1
            if not clean:
                record["clean_tree_proof"]["per_command_clean"] = False
            if row["verdict"] != "PASS":
                tier_defects += 1
                defects += 1
                if not clean:
                    defect_class, severity = "TREE_MUTATION", "P0"
                elif row["exit_code"] == 0 and entry[1] not in VERIFIER_SUITES and not row["tests_collected"]:
                    defect_class, severity = "ZERO_TESTS_COLLECTED", "P1"
                elif entry[1] in ("verify_standard", "test_protocol_schemas"):
                    defect_class, severity = "SUITE_FAILURE", "P0"
                else:
                    defect_class, severity = "SUITE_FAILURE", "P1"
                record["defect_routes"].append(build_route(f"DEF-{defects}", entry[1], tier, defect_class, severity))
        tier_record = {
            "tier": tier,
            "policy": TIER_POLICIES[tier],
            "suites": [entry[1] for entry in entries],
            "defects": tier_defects,
        }
        record["tier_results"].append(tier_record)
        if tier == 0 and tier_defects:
            halted = True
            record["halted_at"] = "TIER-0"
            break
    if defects and not halted:
        record["halted_at"] = "BEFORE_TIER_3"

    record["clean_tree_proof"]["post_run_clean"] = porcelain_lines() == 0
    record["clean_tree_proof"]["porcelain_lines_post"] = porcelain_lines()
    if record["clean_tree_proof"]["post_run_clean"] and record["clean_tree_proof"]["per_command_clean"]:
        record["oracle_checks"]["F4_clean_tree"] = "PASS"
        record["clean_tree_proof"]["source_modifications_after_validation"] = False
    else:
        record["oracle_checks"]["F4_clean_tree"] = "VIOLATED"
        record["clean_tree_proof"]["source_modifications_after_validation"] = True
        if not any(route["defect_class"] == "TREE_MUTATION" for route in record["defect_routes"]):
            record["defect_routes"].append(build_route("DEF-TREE", "post_run_proof", 2, "TREE_MUTATION", "P0"))
            record["defect_routes"][-1]["owning_concern"] = CONTROLLER_ARBITRATION
            defects += 1
    head_now, tree_now = git_head()
    if (head_now, tree_now) != (head, tree):
        record["exact_subject"]["head_at_emission_sha"] = head_now
        record["oracle_checks"]["F1_F5_exact_subject_equality"] = "VIOLATED"
        if not any(route["defect_class"] == "CANDIDATE_DRIFT" for route in record["defect_routes"]):
            record["defect_routes"].append(build_route("DEF-DRIFT", "post_run_proof", 2, "CANDIDATE_DRIFT", "P0"))
            record["defect_routes"][-1]["owning_concern"] = CONTROLLER_ARBITRATION
            defects += 1

    if defects == 0:
        audit_ok, audit, audit_routes = cross_suite_audit(record)
        record["cross_suite_audit"] = audit
        record["oracle_checks"]["F3_cross_suite_audit"] = "PASS" if audit_ok else "FAIL"
        record["defect_routes"].extend(audit_routes)
        defects += len(audit_routes)
        if not audit_ok:
            record["halted_at"] = "TIER-3"

    record["inventory_complete"] = record["executed_count"] == record["required_count"] and not record["halted_at"]
    record["oracle_checks"]["F2_inventory_complete"] = "ENFORCED" if record["inventory_complete"] else "VIOLATED"
    zero_collected = [
        row["suite"]
        for row in record["suite_rows"]
        if row["verdict"] == "PASS" and row["suite"] not in VERIFIER_SUITES and not row["tests_collected"]
    ]
    record["oracle_checks"]["F9_zero_collected_guard"] = "ENFORCED" if not zero_collected else "VIOLATED"
    record["oracle_checks"]["F6_no_repair_while_validating"] = "ENFORCED"
    record["finished_at"] = utc_now()
    if defects == 0 and not record["halted_at"]:
        record["integration_verdict"] = "VISIBLE_INTEGRATION_PASS"
        record["integration_admission"] = "RECORDED"
    else:
        record["integration_verdict"] = "VISIBLE_INTEGRATION_FAIL"
        record["integration_admission"] = "REFUSED"
    return record


def print_inventory() -> dict:
    head, tree = git_head()
    return {
        "record_schema": INVENTORY_SCHEMA,
        "runner_version": RUNNER_VERSION,
        "task": TASK,
        "design_refs": {"runner_order": DRYRUN_DESIGN_REF, "false_green_oracle": FALSE_GREEN_ORACLE_REF,
                         "impact_inventory": IMPACT_INVENTORY_REF},
        "exact_subject": {
            "base_sha": BASE_SHA,
            "base_tree": BASE_TREE,
            "head_sha": head,
            "head_tree": tree,
            "base_is_ancestor_of_head": is_ancestor(BASE_SHA, head),
        },
        "predecessor_chain": [dict(entry) for entry in PREDECESSOR_CHAIN],
        "tier_policies": {str(tier): policy for tier, policy in TIER_POLICIES.items()},
        "required_commands": [
            {"tier": tier, "suite": suite, "exact_command": f"python {script}", "owning_concern": owner}
            for tier, suite, script, owner in COMMAND_INVENTORY
        ],
        "required_count": len(COMMAND_INVENTORY),
        "owner_routing": {
            "vocabulary": sorted(KNOWN_OWNERS),
            "catch_all": CONTROLLER_ARBITRATION,
            "rule": "every defect routes to a named owning concern; T08A performs no semantic repair",
        },
        "verdict_vocabulary": {
            "integration_verdict": sorted(INTEGRATION_VERDICTS),
            "hidden_validation_verdict": NOT_CLAIMED,
            "release_qualification_verdict": NOT_CLAIMED,
            "candidate_freeze_verdict": NOT_CLAIMED,
            "v01_dispatch_gate": "NOT_DISPATCHABLE_BY_THIS_RUNNER",
        },
        "disclaimer": DISCLAIMER,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="V410-T08A visible whole-project integration runner")
    parser.add_argument("--print-inventory", action="store_true",
                        help="emit the bound inventory + subject binding without executing anything")
    args = parser.parse_args(argv)

    if args.print_inventory:
        print(json.dumps(print_inventory(), indent=2))
        return 0

    pre_clean = porcelain_lines() == 0
    head, tree = git_head()
    ancestry_ok = is_ancestor(BASE_SHA, head)
    chain_intact = all(is_ancestor(entry["sha"], head) for entry in PREDECESSOR_CHAIN)
    record = execute(head, tree, ancestry_ok, chain_intact, pre_clean)

    problems = validate_result(record)
    if problems:
        # The runner never emits a non-conformant record: a model violation is
        # itself a P0 defect routed to Controller arbitration.
        record["integration_verdict"] = "VISIBLE_INTEGRATION_FAIL"
        record["integration_admission"] = "REFUSED"
        record["defect_routes"].append(
            {**build_route("DEF-RECORD-MODEL", "record_model_validator", 3, "CROSS_SUITE_CONTRADICTION", "P0"),
             "owning_concern": CONTROLLER_ARBITRATION,
             "revalidation_scope": "; ".join(problems)[:500]}
        )
    print(json.dumps(record, indent=2))
    return 0 if record["integration_verdict"] == "VISIBLE_INTEGRATION_PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
