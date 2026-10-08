"""V410-T08A: visible whole-project integration runner oracle.

Focused deterministic suite for ``scripts/run_v410_integration.py`` (oracle
binding: false-green oracle cases F1-F12 from #864@6043181240
(WEB_INTEGRATION_FALSE_GREEN_ORACLE_R1); dryrun-validated runner order +
result-record fields + merge-drain/currentness rules from #864@6040893503
(LOCAL_INTEGRATION_RUNNER_DRYRUN_R1, rebound at the V410-T08A JIT to the
post-#863 integrated candidate 402bf289 / tree 2af7450f); integration-impact
inventory + owner routing from #864@6037701635; fast-path handoff from
#864@6046066388; rebind subject 402bf289 = merged PR #934 tip =
V410-T07B INTEGRATED, predecessor chain 0518202c -> cea2e0cc -> 402bf289).

The suite proves the false-green oracle negatives as record-model mutants
against the runner's own fail-closed validator: a skipped/not-run/zero-collected
suite can never aggregate green (F2/F9); stale or mixed-subject evidence is
rejected (F1/F5); predecessor-chain drift fails (F7); the visible-PASS
disclaimer is mandatory and Hidden/Release-Qualification verdicts are
structurally NOT_CLAIMED (F8); every failure carries an owner-routed defect row
— never silently absorbed (F6); dirty-tree or tree-mutating runs cannot be
green (F4); tested-head and emission-head are carried separately (F10); and
evidence reuse is NONE (F11). Positives: an all-green run produces a
conformant VISIBLE_INTEGRATION_PASS record; a failing suite classifies into a
named owning concern. The three positional candidate registries must agree on
the active T08A successor entry, and the runner inventory carries the
predecessor packs' mandatory commands.

VISIBILITY BOUNDARY (verbatim obligation, enforced on every record): visible
integration PASS is not Hidden Validation or Release Qualification PASS. This
suite grants no Hidden Validation, Release Qualification, Candidate Freeze or
V01 authority, and T08A performs no semantic repair — defects route to their
owning concerns.

Purely local; no network; stdlib only.
"""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(ROOT / "scripts"))

import run_v410_integration as runner  # noqa: E402
from v34_rules import REQUIRED_CORE_ARTIFACTS, core_artifacts_complete  # noqa: E402

PACK_DIR = ROOT / ".agent" / "execution" / "V410-T08A-R1"
RUNNER_SCRIPT = ROOT / "scripts" / "run_v410_integration.py"

# Exact rebind subject of this task (merged #934 integration tip; V410-T07B INTEGRATED).
BASE_SHA = "402bf2899a7e1cd43eea3e7d78a37c947fe28c46"
BASE_TREE = "2af7450ff8312bd8652742996071252c42abe65e"

# Predecessor merge chain (integration-impact inventory #864@6037701635, rebound).
PREDECESSOR_CHAIN = (
    ("#861", "V410-T06B", "0518202c715dcf91784a694bdf4a8eeeaeb16ab6"),
    ("#862", "V410-T07A", "cea2e0ccd045e8fcebaf110273129b198ed259fd"),
    ("#863", "V410-T07B", "402bf2899a7e1cd43eea3e7d78a37c947fe28c46"),
)

DISCLAIMER = "VISIBLE INTEGRATION PASS IS NOT HIDDEN VALIDATION OR RELEASE QUALIFICATION PASS"
NO_HIDING_RULE = "may not hide semantic repairs"

# Mandatory commands of the three predecessor six-core packs (as applicable at
# the integrated candidate) that the whole-project runner must carry.
PREDECESSOR_MANDATORY_COMMANDS = (
    # V410-T06B-R1 TEST_MATRIX (subset applicable to the composed candidate)
    "test_v410_t06b_multi_dispatch_conformance",
    "test_protocol_schemas",
    "test_execution_architecture",
    "test_v410_t06b_core_inventory",
    "test_v410_t04b_review_currentness",
    "verify_standard",
    # V410-T07A-R1 TEST_MATRIX
    "test_v410_t07a_acceptance_projection",
    "test_v410_stage1_lifecycle_contracts",
    "test_v410_t01b_product_projections",
    "test_v410_t02a_collaboration_control",
    "test_v410_t02b_machine_projection",
    "test_v410_t03a_implementation_quality",
    "test_v410_t04a_gate_repair_routing",
    "test_v410_t05a_shared_code_safety",
    "test_v410_owner_convergence",
    "verify_event_writer_surfaces",
    # V410-T07B-R1 TEST_MATRIX
    "test_v410_t07b_decision_record",
)

FAKE_HEAD = "c" * 40
FAKE_TREE = "d" * 40


def all_green_record() -> dict:
    """A synthetic, fully executed, all-green runner result (model-level)."""
    rows = []
    for tier, suite, script, _owner in runner.COMMAND_INVENTORY:
        rows.append(
            {
                "suite": suite,
                "exact_command": f"python {script}",
                "tier": tier,
                "candidate_sha": FAKE_HEAD,
                "candidate_tree": FAKE_TREE,
                "exit_code": 0,
                "duration_s": 0.4,
                "tests_collected": None if suite in runner.VERIFIER_SUITES else 11,
                "verdict": "PASS",
                "artifact_writing_flag": "NONE",
                "output_tail": "OK",
                "timestamp": "2026-10-08T00:00:00Z",
                "owner_concern": _owner,
            }
        )
    return {
        "record_schema": runner.RECORD_SCHEMA,
        "runner_version": runner.RUNNER_VERSION,
        "task": runner.TASK,
        "dispatch_ref": runner.DISPATCH_ISSUE,
        "admission_refs": {"proposal": runner.PROPOSAL_REF, "admission_claim": runner.ADMISSION_CLAIM_REF},
        "exact_subject": {
            "base_sha": runner.BASE_SHA,
            "base_tree": runner.BASE_TREE,
            "tested_head_sha": FAKE_HEAD,
            "tested_head_tree": FAKE_TREE,
            "head_at_emission_sha": FAKE_HEAD,
            "base_is_ancestor_of_head": True,
        },
        "predecessor_chain": [
            dict(entry, integrated=True, ancestor_of_head=True) for entry in runner.PREDECESSOR_CHAIN
        ],
        "predecessor_chain_intact": True,
        "executor_identity": {"runner": "scripts/run_v410_integration.py", "platform": "synthetic", "python": "3"},
        "started_at": "2026-10-08T00:00:00Z",
        "finished_at": "2026-10-08T00:00:10Z",
        "tier_results": [],
        "suite_rows": rows,
        "executed_count": len(rows),
        "required_count": len(runner.COMMAND_INVENTORY),
        "inventory_complete": True,
        "clean_tree_proof": {
            "pre_run_clean": True,
            "post_run_clean": True,
            "per_command_clean": True,
            "porcelain_lines_post": 0,
            "source_modifications_after_validation": False,
        },
        "oracle_checks": {
            "F1_F5_exact_subject_equality": "ENFORCED",
            "F2_inventory_complete": "ENFORCED",
            "F3_cross_suite_audit": "PASS",
            "F4_clean_tree": "PASS",
            "F6_no_repair_while_validating": "ENFORCED",
            "F8_no_hidden_rq_claim": "ENFORCED",
            "F9_zero_collected_guard": "ENFORCED",
            "F10_tested_head_separation": "CARRIED",
            "F11_no_evidence_reuse": "ENFORCED",
        },
        "cross_suite_audit": {"verdict": "PASS", "findings": [], "registries_checked": ["synthetic"]},
        "defect_routes": [],
        "halted_at": None,
        "integration_verdict": "VISIBLE_INTEGRATION_PASS",
        "hidden_validation_verdict": "NOT_CLAIMED",
        "release_qualification_verdict": "NOT_CLAIMED",
        "candidate_freeze_verdict": "NOT_CLAIMED",
        "v01_dispatch_gate": "NOT_DISPATCHABLE_BY_THIS_RUNNER",
        "evidence_reuse": "NONE",
        "integration_admission": "RECORDED",
        "disclaimer": DISCLAIMER,
    }


def fail_row(record: dict, suite: str) -> dict:
    for row in record["suite_rows"]:
        if row["suite"] == suite:
            row["verdict"] = "FAIL"
            row["exit_code"] = 1
            row["tests_collected"] = None if suite in runner.VERIFIER_SUITES else 3
            return row
    raise AssertionError(f"suite not in inventory: {suite}")


class InventoryBindingTests(unittest.TestCase):
    """The deterministic complete command inventory and its exact bindings."""

    def test_required_inventory_is_deterministic_and_tiered(self) -> None:
        self.assertEqual(len(runner.COMMAND_INVENTORY), 20)
        tiers = {}
        for tier, suite, _script, _owner in runner.COMMAND_INVENTORY:
            tiers.setdefault(tier, []).append(suite)
        self.assertEqual(sorted(tiers), [0, 1, 2])
        self.assertEqual(len(tiers[0]), 2)
        self.assertEqual(len(tiers[1]), 4)
        self.assertEqual(len(tiers[2]), 14)
        self.assertEqual(len(runner.REQUIRED_SUITES), 20)
        self.assertEqual(runner.TIER_POLICIES[0], "FAIL_FAST")
        self.assertEqual(runner.TIER_POLICIES[3], "INTEGRATION_ONLY")

    def test_every_required_suite_exists_on_disk(self) -> None:
        for _tier, _suite, script, _owner in runner.COMMAND_INVENTORY:
            self.assertTrue((ROOT / script).is_file(), script)

    def test_unittest_suites_report_collected_tests(self) -> None:
        # F9 mechanics depend on this: every non-verifier suite must be a
        # unittest runner emitting "Ran N tests".
        for _tier, suite, script, _owner in runner.COMMAND_INVENTORY:
            if suite in runner.VERIFIER_SUITES:
                continue
            self.assertIn("unittest", (ROOT / script).read_text(encoding="utf-8"), script)

    def test_owner_map_covers_every_suite_with_controller_catch_all(self) -> None:
        for _tier, suite, _script, owner in runner.COMMAND_INVENTORY:
            self.assertTrue(owner, suite)
            self.assertEqual(runner.suite_owner(suite), owner)
        self.assertIn(runner.CONTROLLER_ARBITRATION, runner.KNOWN_OWNERS)
        self.assertEqual(runner.suite_owner("suite_not_in_inventory"), runner.CONTROLLER_ARBITRATION)

    def test_predecessor_mandatory_commands_are_carried(self) -> None:
        for suite in PREDECESSOR_MANDATORY_COMMANDS:
            self.assertIn(suite, runner.REQUIRED_SUITES, suite)

    def test_base_binding_is_exact(self) -> None:
        self.assertEqual(runner.BASE_SHA, BASE_SHA)
        self.assertEqual(runner.BASE_TREE, BASE_TREE)

    def test_predecessor_chain_binds_the_full_merge_lineage(self) -> None:
        self.assertEqual(
            [(entry["merge"], entry["task"], entry["sha"]) for entry in runner.PREDECESSOR_CHAIN],
            [tuple(entry) for entry in PREDECESSOR_CHAIN],
        )
        # The chain is ordered and its last element IS the rebind base.
        self.assertEqual(runner.PREDECESSOR_CHAIN[-1]["sha"], runner.BASE_SHA)

    def test_disclaimer_is_verbatim_and_boundary_verdicts_not_claimed(self) -> None:
        self.assertEqual(runner.DISCLAIMER, DISCLAIMER)
        self.assertEqual(runner.NOT_CLAIMED, "NOT_CLAIMED")
        self.assertEqual(
            runner.INTEGRATION_VERDICTS,
            {"VISIBLE_INTEGRATION_PASS", "VISIBLE_INTEGRATION_FAIL"},
        )


class RegistryAgreementTests(unittest.TestCase):
    """Cross-suite conflict audit mechanics: the three positional registries agree."""

    def test_three_registries_agree_on_the_active_t08a_candidate(self) -> None:
        import test_v410_owner_convergence as oc
        import test_v410_t07a_acceptance_projection as t07a
        import test_v410_t07b_decision_record as t07b

        registries = {
            "test_v410_owner_convergence": oc.CandidateShapeTests.TASK_CANDIDATES,
            "test_v410_t07a_acceptance_projection": t07a.ProjectionSurfaceConformanceTests.TASK_CANDIDATES,
            "test_v410_t07b_decision_record": t07b.PackAndCandidateSurfaceTests.TASK_CANDIDATES,
        }
        for name, candidates in registries.items():
            actives = [entry["task"] for entry in candidates if entry.get("active")]
            self.assertEqual(actives, ["V410-T08A"], name)
            entry = next(e for e in candidates if e.get("active"))
            self.assertEqual(entry["base"], BASE_SHA, name)
            self.assertTrue(entry["prefixes"], name)

    def test_t08a_prefix_sets_are_consistent_across_registries(self) -> None:
        import test_v410_owner_convergence as oc
        import test_v410_t07a_acceptance_projection as t07a
        import test_v410_t07b_decision_record as t07b

        t08a_oc = next(e for e in oc.CandidateShapeTests.TASK_CANDIDATES if e["task"] == "V410-T08A")
        t08a_t07a = next(e for e in t07a.ProjectionSurfaceConformanceTests.TASK_CANDIDATES if e["task"] == "V410-T08A")
        t08a_t07b = next(e for e in t07b.PackAndCandidateSurfaceTests.TASK_CANDIDATES if e["task"] == "V410-T08A")
        self.assertEqual(set(t08a_oc["prefixes"]), set(t08a_t07a["prefixes"]))
        self.assertEqual(set(t08a_oc["prefixes"]), set(t08a_t07b["prefixes"]))
        self.assertEqual(set(t08a_oc["prefixes"]), set(t07b.PackAndCandidateSurfaceTests.T08A_ALLOWED_PREFIXES))

    def test_this_candidate_diff_stays_inside_the_registered_t08a_prefixes(self) -> None:
        result = subprocess.run(
            ["git", "diff", "--name-only", f"{BASE_SHA}...HEAD", "--"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            self.fail(f"cannot diff against {BASE_SHA}...HEAD: {result.stderr.strip()}")
        changed = {line.strip() for line in result.stdout.splitlines() if line.strip()}
        import test_v410_owner_convergence as oc

        t08a = next(e for e in oc.CandidateShapeTests.TASK_CANDIDATES if e["task"] == "V410-T08A")
        outside = sorted(p for p in changed if not p.startswith(t08a["prefixes"]))
        self.assertEqual(outside, [], "T08A candidate paths must stay inside the registered prefixes")


class RecordModelPositiveTests(unittest.TestCase):
    """Positive runner-result cases: all-green conformant; routed failures classified."""

    def test_all_green_record_validates_clean(self) -> None:
        self.assertEqual(runner.validate_result(all_green_record()), [])

    def test_all_green_record_carries_visible_only_verdicts(self) -> None:
        record = all_green_record()
        self.assertEqual(record["integration_verdict"], "VISIBLE_INTEGRATION_PASS")
        self.assertEqual(record["integration_admission"], "RECORDED")
        for field in ("hidden_validation_verdict", "release_qualification_verdict", "candidate_freeze_verdict"):
            self.assertEqual(record[field], "NOT_CLAIMED")

    def test_fail_record_with_complete_routes_validates_as_fail(self) -> None:
        record = all_green_record()
        row = fail_row(record, "test_v410_t06b_multi_dispatch_conformance")
        route = runner.build_route("DEF-1", row["suite"], row["tier"], "SUITE_FAILURE", "P1")
        record["defect_routes"] = [route]
        record["integration_verdict"] = "VISIBLE_INTEGRATION_FAIL"
        record["integration_admission"] = "REFUSED"
        record["inventory_complete"] = False
        record["cross_suite_audit"] = None
        self.assertEqual(runner.validate_result(record), [])
        self.assertEqual(route["owning_concern"], "V410-T06B (#861)")

    def test_owner_routing_classifies_each_predecessor_owner(self) -> None:
        expectations = {
            "test_v410_t06b_core_inventory": "V410-T06B (#861)",
            "test_v410_t06b_multi_dispatch_conformance": "V410-T06B (#861)",
            "test_v410_t07a_acceptance_projection": "V410-T07A (#862)",
            "test_v410_t07b_decision_record": "V410-T07B (#863)",
            "test_v410_owner_convergence": "V410-T06A (#860)",
            "test_v410_t04b_review_currentness": "V410-T04B (#857)",
            "test_v410_t04a_gate_repair_routing": "V410-T04A (#854)",
            "verify_standard": runner.CONTROLLER_ARBITRATION,
        }
        for suite, owner in expectations.items():
            self.assertEqual(runner.suite_owner(suite), owner, suite)

    def test_verifier_and_gate_failures_route_with_p0_severity_design(self) -> None:
        # TIER-0 gate failures are classified P0 by the runner's execute path;
        # the vocabulary admits exactly the documented classes.
        self.assertIn("SUITE_FAILURE", runner.DEFECT_CLASSES)
        self.assertIn("ZERO_TESTS_COLLECTED", runner.DEFECT_CLASSES)
        self.assertIn("TREE_MUTATION", runner.DEFECT_CLASSES)
        self.assertIn("CANDIDATE_DRIFT", runner.DEFECT_CLASSES)
        self.assertIn("PREDECESSOR_CHAIN_DRIFT", runner.DEFECT_CLASSES)
        self.assertIn("CROSS_SUITE_CONTRADICTION", runner.DEFECT_CLASSES)
        self.assertIn("PRE_RUN_REFUSAL", runner.DEFECT_CLASSES)
        self.assertIn("INVENTORY_MISSING", runner.DEFECT_CLASSES)


class FalseGreenOracleNegativeTests(unittest.TestCase):
    """F1-F12 mutants (#864@6043181240): every false green fails closed."""

    def _expect_problem(self, record: dict, token: str) -> None:
        problems = runner.validate_result(record)
        self.assertTrue(
            any(token in problem for problem in problems),
            f"expected a problem containing {token!r}, got {problems}",
        )

    # F2 — a required suite disappears from the inventory while the rest pass.
    def test_f2_pass_aggregate_with_missing_suite_row_is_rejected(self) -> None:
        record = all_green_record()
        record["suite_rows"] = [r for r in record["suite_rows"] if r["suite"] != "test_v410_t07b_decision_record"]
        record["executed_count"] = len(record["suite_rows"])
        self._expect_problem(record, "required suite missing")

    def test_f2_row_outside_the_registered_inventory_is_rejected(self) -> None:
        record = all_green_record()
        record["suite_rows"].append(
            {
                "suite": "test_some_unregistered_suite",
                "exact_command": "python scripts/test_some_unregistered_suite.py",
                "tier": 2,
                "candidate_sha": FAKE_HEAD,
                "candidate_tree": FAKE_TREE,
                "exit_code": 0,
                "duration_s": 0.1,
                "tests_collected": 3,
                "verdict": "PASS",
                "artifact_writing_flag": "NONE",
                "timestamp": "2026-10-08T00:00:00Z",
            }
        )
        record["executed_count"] = len(record["suite_rows"])
        self._expect_problem(record, "outside the registered inventory")

    def test_f2_duplicate_rows_are_rejected(self) -> None:
        record = all_green_record()
        record["suite_rows"].append(dict(record["suite_rows"][0]))
        record["executed_count"] = len(record["suite_rows"])
        self._expect_problem(record, "duplicate suite rows")

    # F9 — skipped / zero-collected / not-run encoded green.
    def test_f9_zero_collected_pass_row_is_rejected(self) -> None:
        record = all_green_record()
        row = next(r for r in record["suite_rows"] if r["suite"] == "test_v410_t04b_review_currentness")
        row["tests_collected"] = 0
        self._expect_problem(record, "zero/unknown tests collected")

    def test_f9_unknown_collected_count_pass_row_is_rejected(self) -> None:
        record = all_green_record()
        row = next(r for r in record["suite_rows"] if r["suite"] == "test_v410_t05a_shared_code_safety")
        row["tests_collected"] = None
        self._expect_problem(record, "zero/unknown tests collected")

    def test_f9_not_run_row_inside_pass_aggregate_is_rejected(self) -> None:
        record = all_green_record()
        row = next(r for r in record["suite_rows"] if r["suite"] == "test_v410_t02a_collaboration_control")
        row["verdict"] = "NOT_RUN"
        self._expect_problem(record, "NOT_RUN row inside a PASS aggregate")

    def test_f9_pass_row_with_failing_exit_code_is_rejected(self) -> None:
        record = all_green_record()
        row = next(r for r in record["suite_rows"] if r["suite"] == "test_v410_t03a_implementation_quality")
        row["exit_code"] = 2
        self._expect_problem(record, "non-zero exit_code")

    def test_f9_unhalted_fail_must_account_for_the_full_inventory(self) -> None:
        record = all_green_record()
        record["suite_rows"] = record["suite_rows"][:5]
        record["executed_count"] = 5
        record["inventory_complete"] = False
        record["integration_verdict"] = "VISIBLE_INTEGRATION_FAIL"
        record["integration_admission"] = "REFUSED"
        record["cross_suite_audit"] = None
        row = record["suite_rows"][-1]
        row["verdict"] = "FAIL"
        row["exit_code"] = 1
        record["defect_routes"] = [runner.build_route("DEF-1", row["suite"], row["tier"], "SUITE_FAILURE", "P1")]
        self._expect_problem(record, "un-halted FAIL record did not execute the complete inventory")

    # F1/F5 — stale or mixed-subject evidence.
    def test_f1_stale_base_binding_is_rejected(self) -> None:
        record = all_green_record()
        record["exact_subject"]["base_sha"] = "0" * 40
        self._expect_problem(record, "F1 stale subject rejected")

    def test_f1_stale_base_tree_binding_is_rejected(self) -> None:
        record = all_green_record()
        record["exact_subject"]["base_tree"] = "0" * 40
        self._expect_problem(record, "F1 stale subject rejected")

    def test_f5_row_bound_to_a_different_subject_is_rejected(self) -> None:
        record = all_green_record()
        record["suite_rows"][3]["candidate_sha"] = "e" * 40
        self._expect_problem(record, "different subject")

    def test_f5_mixed_head_tree_evidence_is_rejected(self) -> None:
        record = all_green_record()
        record["exact_subject"]["tested_head_tree"] = "not-a-tree"
        self._expect_problem(record, "40-hex")

    # F7 — predecessor identity drift.
    def test_f7_predecessor_sha_drift_is_rejected(self) -> None:
        record = all_green_record()
        record["predecessor_chain"][0]["sha"] = "a" * 40
        self._expect_problem(record, "predecessor chain drift")

    def test_f7_unintegrated_predecessor_row_is_rejected(self) -> None:
        record = all_green_record()
        record["predecessor_chain"][1]["integrated"] = False
        self._expect_problem(record, "predecessor chain drift")

    def test_f7_chain_intact_false_is_rejected(self) -> None:
        record = all_green_record()
        record["predecessor_chain_intact"] = False
        self._expect_problem(record, "predecessor_chain_intact")

    # F8 — visible PASS is not Hidden Validation or Release Qualification PASS.
    def test_f8_missing_or_altered_disclaimer_is_rejected(self) -> None:
        record = all_green_record()
        record["disclaimer"] = "integration green, ship it"
        self._expect_problem(record, "disclaimer is mandatory")

    def test_f8_hidden_validation_claim_is_rejected(self) -> None:
        record = all_green_record()
        record["hidden_validation_verdict"] = "PASS"
        self._expect_problem(record, "NOT_CLAIMED")

    def test_f8_release_qualification_claim_is_rejected(self) -> None:
        record = all_green_record()
        record["release_qualification_verdict"] = "PASS"
        self._expect_problem(record, "NOT_CLAIMED")

    def test_f8_candidate_freeze_claim_is_rejected(self) -> None:
        record = all_green_record()
        record["candidate_freeze_verdict"] = "FROZEN"
        self._expect_problem(record, "NOT_CLAIMED")

    def test_f8_hidden_verdict_vocabulary_is_rejected(self) -> None:
        record = all_green_record()
        record["integration_verdict"] = "RELEASE_QUALIFICATION_PASS"
        self._expect_problem(record, "never a Hidden/RQ verdict")

    # F6 — no silent absorption; owner routing mandatory.
    def test_f6_fail_row_without_route_is_rejected(self) -> None:
        record = all_green_record()
        fail_row(record, "test_v410_t01b_product_projections")
        record["integration_verdict"] = "VISIBLE_INTEGRATION_FAIL"
        record["integration_admission"] = "REFUSED"
        record["cross_suite_audit"] = None
        record["inventory_complete"] = False
        self._expect_problem(record, "without an owner-routed defect row")

    def test_f6_pass_aggregate_with_open_routes_is_rejected(self) -> None:
        record = all_green_record()
        record["defect_routes"] = [
            runner.build_route("DEF-1", "test_v410_t02b_machine_projection", 2, "SUITE_FAILURE", "P1")
        ]
        self._expect_problem(record, "open defect routes")

    def test_f6_route_with_unknown_owner_is_rejected(self) -> None:
        record = all_green_record()
        fail_row(record, "test_v410_t02b_machine_projection")
        route = runner.build_route("DEF-1", "test_v410_t02b_machine_projection", 2, "SUITE_FAILURE", "P1")
        route["owning_concern"] = "V410-T99X (nonexistent owner)"
        record["defect_routes"] = [route]
        record["integration_verdict"] = "VISIBLE_INTEGRATION_FAIL"
        record["integration_admission"] = "REFUSED"
        record["cross_suite_audit"] = None
        record["inventory_complete"] = False
        self._expect_problem(record, "known owning concern")

    def test_f6_route_with_unknown_defect_class_is_rejected(self) -> None:
        record = all_green_record()
        fail_row(record, "test_v410_t02b_machine_projection")
        route = runner.build_route("DEF-1", "test_v410_t02b_machine_projection", 2, "SILENT_ABSORPTION", "P1")
        record["defect_routes"] = [route]
        record["integration_verdict"] = "VISIBLE_INTEGRATION_FAIL"
        record["integration_admission"] = "REFUSED"
        record["cross_suite_audit"] = None
        record["inventory_complete"] = False
        self._expect_problem(record, "unknown defect_class")

    def test_f6_route_without_repair_dispatch_ref_is_rejected(self) -> None:
        record = all_green_record()
        fail_row(record, "test_v410_t02b_machine_projection")
        route = runner.build_route("DEF-1", "test_v410_t02b_machine_projection", 2, "SUITE_FAILURE", "P1")
        del route["repair_dispatch_ref"]
        record["defect_routes"] = [route]
        record["integration_verdict"] = "VISIBLE_INTEGRATION_FAIL"
        record["integration_admission"] = "REFUSED"
        record["cross_suite_audit"] = None
        record["inventory_complete"] = False
        self._expect_problem(record, "repair_dispatch_ref")

    # F4 — dirty/uncommitted validation tree or tree mutation cannot be green.
    def test_f4_dirty_post_run_tree_is_rejected_on_pass(self) -> None:
        record = all_green_record()
        record["clean_tree_proof"]["post_run_clean"] = False
        record["clean_tree_proof"]["porcelain_lines_post"] = 2
        self._expect_problem(record, "proven-clean tree")

    def test_f4_dirty_pre_run_tree_is_rejected_on_pass(self) -> None:
        record = all_green_record()
        record["clean_tree_proof"]["pre_run_clean"] = False
        self._expect_problem(record, "proven-clean tree")

    def test_f4_tree_mutating_command_cannot_be_pass(self) -> None:
        record = all_green_record()
        row = next(r for r in record["suite_rows"] if r["suite"] == "test_v410_stage1_lifecycle_contracts")
        row["artifact_writing_flag"] = "TREE_MUTATED"
        self._expect_problem(record, "tree-mutating command")

    def test_f4_post_validation_source_modification_is_rejected_on_pass(self) -> None:
        record = all_green_record()
        record["clean_tree_proof"]["source_modifications_after_validation"] = True
        self._expect_problem(record, "post-validation source modification")

    # F3 — cross-suite contradiction audit must pass on a green aggregate.
    def test_f3_failing_cross_suite_audit_blocks_pass(self) -> None:
        record = all_green_record()
        record["cross_suite_audit"] = {"verdict": "FAIL", "findings": ["registry disagreement"], "registries_checked": []}
        record["oracle_checks"]["F3_cross_suite_audit"] = "FAIL"
        self._expect_problem(record, "PASS cross-suite audit")

    # F10 — tested head and evidence-only head carried separately.
    def test_f10_missing_tested_head_is_rejected(self) -> None:
        record = all_green_record()
        del record["exact_subject"]["tested_head_sha"]
        self._expect_problem(record, "tested_head_sha")

    def test_f10_missing_emission_head_is_rejected(self) -> None:
        record = all_green_record()
        del record["exact_subject"]["head_at_emission_sha"]
        self._expect_problem(record, "head_at_emission_sha")

    # F11 — prior concern evidence reuse.
    def test_f11_evidence_reuse_is_rejected(self) -> None:
        record = all_green_record()
        record["evidence_reuse"] = "PRIOR_CONCERN_RUN"
        self._expect_problem(record, "evidence_reuse must be NONE")

    # Halt/admission consistency.
    def test_halted_pass_is_rejected(self) -> None:
        record = all_green_record()
        record["halted_at"] = "TIER-0"
        self._expect_problem(record, "halted_at")

    def test_admission_recorded_on_fail_is_rejected(self) -> None:
        record = all_green_record()
        fail_row(record, "test_v410_owner_convergence")
        route = runner.build_route("DEF-1", "test_v410_owner_convergence", 1, "SUITE_FAILURE", "P1")
        record["defect_routes"] = [route]
        record["integration_verdict"] = "VISIBLE_INTEGRATION_FAIL"
        record["cross_suite_audit"] = None
        record["inventory_complete"] = False
        # integration_admission stays RECORDED — must be rejected.
        self._expect_problem(record, "integration admission may only be RECORDED on a visible PASS")

    def test_pending_oracle_check_blocks_pass(self) -> None:
        record = all_green_record()
        record["oracle_checks"]["F4_clean_tree"] = "PENDING"
        self._expect_problem(record, "oracle check F4_clean_tree is PENDING")


class RunnerSmokeTests(unittest.TestCase):
    """The real runner binds its subject and inventory without executing."""

    def test_print_inventory_binds_subject_chain_and_disclaimer(self) -> None:
        result = subprocess.run(
            [sys.executable, str(RUNNER_SCRIPT), "--print-inventory"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["record_schema"], runner.INVENTORY_SCHEMA)
        self.assertEqual(payload["exact_subject"]["base_sha"], BASE_SHA)
        self.assertEqual(payload["exact_subject"]["base_tree"], BASE_TREE)
        self.assertEqual(
            [entry["sha"] for entry in payload["predecessor_chain"]],
            [sha for _merge, _task, sha in PREDECESSOR_CHAIN],
        )
        self.assertEqual(payload["required_count"], 20)
        self.assertEqual(payload["disclaimer"], DISCLAIMER)
        self.assertEqual(payload["verdict_vocabulary"]["hidden_validation_verdict"], "NOT_CLAIMED")
        self.assertEqual(payload["verdict_vocabulary"]["release_qualification_verdict"], "NOT_CLAIMED")
        self.assertIn("catch_all", payload["owner_routing"])

    def test_runner_module_imports_stdlib_only(self) -> None:
        text = RUNNER_SCRIPT.read_text(encoding="utf-8")
        for banned in ("import requests", "import urllib.request", "import http.client", "import socket"):
            self.assertNotIn(banned, text, banned)


class PackSurfaceTests(unittest.TestCase):
    """Pack inventory, subject binding, verbatim boundary obligations."""

    def test_pack_core_inventory_exact_set(self) -> None:
        text = (PACK_DIR / "MANIFEST.yaml").read_text(encoding="utf-8")
        lines = text.splitlines()
        start = lines.index("core_artifacts:")
        items: list[str] = []
        for line in lines[start + 1 :]:
            if not line.startswith("  - "):
                break
            items.append(line[4:].strip())
        self.assertTrue(core_artifacts_complete(items))
        self.assertEqual(set(items), set(REQUIRED_CORE_ARTIFACTS))

    def test_pack_manifest_binds_exact_rebind_subject_and_dependency_identity(self) -> None:
        text = (PACK_DIR / "MANIFEST.yaml").read_text(encoding="utf-8")
        self.assertIn(f"base_sha: {BASE_SHA}", text)
        self.assertIn(f"base_tree: {BASE_TREE}", text)
        self.assertIn("task_id: V410-T08A", text)
        self.assertIn("V410-T07B@402bf2899a7e1cd43eea3e7d78a37c947fe28c46 INTEGRATED", text)
        for sha in ("0518202c715dcf91784a694bdf4a8eeeaeb16ab6", "cea2e0ccd045e8fcebaf110273129b198ed259fd"):
            self.assertIn(sha, text)
        self.assertIn("F1_BOUNDED_IMPLEMENTATION", text)
        self.assertIn("validation_scope: integration", text)

    def test_contract_states_the_visibility_boundary_verbatim(self) -> None:
        text = (PACK_DIR / "EXECUTION_CONTRACT.md").read_text(encoding="utf-8")
        lowered = " ".join(text.split()).lower()
        self.assertIn("visible integration pass is not hidden validation or release qualification pass", lowered)
        self.assertIn(NO_HIDING_RULE, lowered)
        self.assertIn("route", lowered)
        self.assertIn("owner", lowered)

    def test_test_matrix_maps_the_false_green_oracle_cases(self) -> None:
        text = (PACK_DIR / "TEST_MATRIX.yaml").read_text(encoding="utf-8")
        for token in ("F2", "F4", "F5", "F8", "F9", "#864@6043181240", "#864@6040893503", "run_v410_integration.py"):
            self.assertIn(token, text, token)

    def test_failure_matrix_carries_owner_routing(self) -> None:
        text = (PACK_DIR / "FAILURE_MATRIX.yaml").read_text(encoding="utf-8")
        for token in ("V410-T06B", "V410-T07A", "V410-T07B", "CONTROLLER_ARBITRATION", "TO_BE_ISSUED_BY_CONTROLLER"):
            self.assertIn(token, text, token)

    def test_deliverable_files_present(self) -> None:
        for name in (
            "MANIFEST.yaml",
            "EXECUTION_CONTRACT.md",
            "TEST_MATRIX.yaml",
            "FAILURE_MATRIX.yaml",
            "IMPLEMENTATION_MAP.md",
            "REVIEW_CHECKLIST.md",
        ):
            self.assertTrue((PACK_DIR / name).is_file(), name)


if __name__ == "__main__":
    result = unittest.TextTestRunner(verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
    )
    raise SystemExit(0 if result.wasSuccessful() else 1)
