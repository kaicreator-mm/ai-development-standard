from __future__ import annotations

import json
from pathlib import Path
import unittest

from test_protocol_schemas import load_schema, validate_subset
import v34_rules
from v34_rules import (
    AGENT_FREEDOM_LEVELS,
    DISPATCH_VOCABULARY_ALIASES,
    baseline_refresh_priority,
    classify_pack_staleness,
    evidence_reusable_on_successor,
    freedom_allows,
    jit_branch_allowed,
    merge_ready,
    package_leaks,
    project_queue,
    queue_item_status,
    rebind_allowed,
    resolve_duplicate_claim,
    resolve_validator_dispatch,
    review_still_valid,
    route_authority_failure,
    validator_may_repair_source,
    validator_outcome,
    worker_recovery_decision,
)

ROOT = Path(__file__).resolve().parents[1]
SHA_A = "a" * 40
SHA_B = "b" * 40
SHA_C = "c" * 40
BASELINE = "1ce6497402c6e1b54b07cc3bc8f8a46444d1af32"


def pack(**overrides):
    value = {
        "pack_id": "pack-T002-1",
        "task_id": "T-002",
        "base_sha": SHA_A,
        "task_pack_ref": "task-pack:T-002@1",
        "branch": "task/v3.4.0-t002",
        "agent_freedom": "F1_BOUNDED_IMPLEMENTATION",
        "pinned_standard_revision": SHA_C,
        "dependency_completion": {"T-001": SHA_B},
        "material_paths": ["schemas/", "standards/", "scripts/"],
    }
    value.update(overrides)
    return value


def facts(**overrides):
    value = {
        "current_integration_sha": SHA_A,
        "task_pack_ref": "task-pack:T-002@1",
        "branch": "task/v3.4.0-t002",
        "pinned_standard_revision": SHA_C,
        "dependency_completion": {"T-001": SHA_B},
        "delta_paths": [],
    }
    value.update(overrides)
    return value


def dispatch(**overrides):
    value = {
        "dispatch_id": "d-001",
        "repository": "kaicreator-mm/ai-development-standard",
        "version": "3.4.0",
        "task": "T-002",
        "role": "builder",
        "execution_profile": "LOCAL_BUILDER",
        "branch": "task/v3.4.0-t002",
        "expected_base_sha": SHA_A,
        "pinned_standard_revision": SHA_C,
        "agent_freedom": "F1_BOUNDED_IMPLEMENTATION",
        "dispatch_state": "READY",
        "task_pack_ref": "task-pack:T-002@1",
    }
    value.update(overrides)
    return value


def claim_event(**overrides):
    value = {
        "schema": "ai-dev/event-v2",
        "event": "DISPATCH_CLAIMED",
        "actor_role": "builder",
        "operator_kind": "claude-code",
        "operator_id": "claude-code:windows-01",
        "session_ref": "builder-run-1",
        "transport_actor": "github:kaicreator-mm",
        "task": "#50",
        "dispatch_id": "d-001",
        "dispatch_state": "CLAIMED",
        "execution_profile": "LOCAL_BUILDER",
        "sha": SHA_A,
    }
    value.update(overrides)
    return value


class DispatchContractTests(unittest.TestCase):
    def test_builder_dispatch_valid(self) -> None:
        schema = load_schema("dispatch.schema.json")
        self.assertEqual(validate_subset(dispatch(), schema), [])

    def test_validator_dispatch_requires_exact_head_and_profile(self) -> None:
        schema = load_schema("dispatch.schema.json")
        valid = dispatch(
            role="validator",
            execution_profile="LOCAL_VALIDATOR",
            requested_head_sha=SHA_B,
            validation_profile="platform",
        )
        self.assertEqual(validate_subset(valid, schema), [])

        for invalid in (
            dispatch(role="validator", execution_profile="LOCAL_VALIDATOR", validation_profile="platform"),
            dispatch(role="validator", execution_profile="LOCAL_VALIDATOR", requested_head_sha=SHA_B),
        ):
            with self.subTest(invalid=invalid):
                self.assertTrue(validate_subset(invalid, schema), invalid)

    def test_reviewer_dispatch_requires_pr(self) -> None:
        schema = load_schema("dispatch.schema.json")
        self.assertEqual(
            validate_subset(dispatch(role="reviewer", execution_profile="WEB_REVIEWER", pr="#77"), schema),
            [],
        )
        self.assertTrue(
            validate_subset(dispatch(role="reviewer", execution_profile="WEB_REVIEWER"), schema)
        )

    def test_terminal_states_require_outcome_fields(self) -> None:
        schema = load_schema("dispatch.schema.json")
        self.assertEqual(
            validate_subset(dispatch(dispatch_state="COMPLETED", result="PASS", claimed_by="claude-code:windows-01"), schema),
            [],
        )
        self.assertTrue(validate_subset(dispatch(dispatch_state="COMPLETED"), schema))
        self.assertTrue(validate_subset(dispatch(dispatch_state="SUPERSEDED"), schema))
        self.assertTrue(
            validate_subset(
                dispatch(dispatch_state="SUPERSEDED", superseded_reason="HEAD_DRIFT: PR advanced to new SHA"),
                schema,
            )
            == []
        )

    def test_claimed_requires_claimed_by(self) -> None:
        schema = load_schema("dispatch.schema.json")
        self.assertTrue(validate_subset(dispatch(dispatch_state="CLAIMED"), schema))
        self.assertEqual(
            validate_subset(dispatch(dispatch_state="CLAIMED", claimed_by="codex:u1"), schema),
            [],
        )

    def test_execution_profile_matches_role(self) -> None:
        schema = load_schema("dispatch.schema.json")
        mismatches = [
            dispatch(execution_profile="LOCAL_BUILDER", role="validator", requested_head_sha=SHA_B, validation_profile="p"),
            dispatch(role="validator", execution_profile="WEB_REVIEWER", pr="#1", requested_head_sha=SHA_B, validation_profile="p"),
            dispatch(role="builder", execution_profile="LOCAL_VALIDATOR"),
            dispatch(role="builder", execution_profile="PLATFORM_VALIDATOR"),
        ]
        for value in mismatches:
            with self.subTest(value=value):
                self.assertTrue(validate_subset(value, schema), value)


class ExecutionPackContractTests(unittest.TestCase):
    def test_manifest_schema_positive(self) -> None:
        schema = load_schema("execution-pack-manifest.schema.json")
        valid = {
            "pack_id": "pack-T002-1",
            "task_id": "T-002",
            "repository": "kaicreator-mm/ai-development-standard",
            "version": "3.4.0",
            "base_sha": SHA_A,
            "task_pack_ref": "task-pack:T-002@1",
            "branch": "task/v3.4.0-t002",
            "agent_freedom": "F1_BOUNDED_IMPLEMENTATION",
            "pinned_standard_revision": SHA_C,
            "generated_by": "chatgpt-web:web-a",
            "generated_at": "2026-09-22T00:00:00Z",
            "core_artifacts": [
                "MANIFEST.yaml",
                "EXECUTION_CONTRACT.md",
                "TEST_MATRIX.yaml",
                "FAILURE_MATRIX.yaml",
                "IMPLEMENTATION_MAP.md",
                "REVIEW_CHECKLIST.md",
            ],
            "retention": "durable",
        }
        self.assertEqual(validate_subset(valid, schema), [])
        for invalid in (
            dict(valid, agent_freedom="F4_UNLIMITED"),
            dict(valid, retention="forever"),
            dict(valid, base_sha="main"),
            dict(valid, core_artifacts=valid["core_artifacts"][:5]),
        ):
            with self.subTest(invalid=invalid):
                self.assertTrue(validate_subset(invalid, schema), invalid)

    def test_full_provenance_requires_package_exclusion(self) -> None:
        schema = load_schema("execution-pack-manifest.schema.json")
        valid = {
            "pack_id": "p1",
            "task_id": "T",
            "repository": "r",
            "version": "1.0.0",
            "base_sha": SHA_A,
            "task_pack_ref": "tp",
            "branch": "b",
            "agent_freedom": "F2_ENGINEERING_DISCRETION",
            "pinned_standard_revision": SHA_C,
            "generated_by": "x",
            "generated_at": "t",
            "core_artifacts": ["MANIFEST.yaml", "EXECUTION_CONTRACT.md", "TEST_MATRIX.yaml", "FAILURE_MATRIX.yaml", "IMPLEMENTATION_MAP.md", "REVIEW_CHECKLIST.md"],
            "retention": "full-provenance",
            "package_excluded": True,
        }
        self.assertEqual(validate_subset(valid, schema), [])
        self.assertTrue(validate_subset(dict(valid, package_excluded=False), schema))

    def test_task_contract_freedom_field(self) -> None:
        schema = load_schema("task-contract.schema.json")
        valid = {
            "task_id": "T-002",
            "goal": "contracts",
            "integration_target": "version/v3.4.0",
            "baseline_sha": BASELINE,
            "review_policy": "required",
            "required_gates": ["verify-standard"],
            "acceptance": ["schemas validate"],
            "agent_freedom": "F1_BOUNDED_IMPLEMENTATION",
        }
        self.assertEqual(validate_subset(valid, schema), [])
        self.assertTrue(validate_subset(dict(valid, agent_freedom="F9"), schema))

    def test_f3_requires_independent_review(self) -> None:
        schema = load_schema("task-contract.schema.json")
        base = {
            "task_id": "T-010",
            "goal": "closure",
            "integration_target": "version/v3.4.0",
            "baseline_sha": BASELINE,
            "review_policy": "required",
            "required_gates": ["closure"],
            "acceptance": ["done"],
            "agent_freedom": "F3_ARCHITECTURE_REQUIRED",
        }
        self.assertEqual(validate_subset(base, schema), [])
        self.assertTrue(validate_subset(dict(base, review_policy="not-required"), schema))


class PackStalenessTests(unittest.TestCase):
    def test_pack_current(self) -> None:
        self.assertEqual(classify_pack_staleness(pack(), facts()), "PACK_CURRENT")

    def test_nonmaterial_delta(self) -> None:
        self.assertEqual(
            classify_pack_staleness(pack(), facts(current_integration_sha=SHA_B, delta_paths=["README.md"])),
            "PACK_STALE_NONMATERIAL",
        )

    def test_material_delta(self) -> None:
        self.assertEqual(
            classify_pack_staleness(pack(), facts(current_integration_sha=SHA_B, delta_paths=["schemas/dispatch.schema.json"])),
            "PACK_STALE_MATERIAL",
        )

    def test_unknown_delta_fails_closed(self) -> None:
        self.assertEqual(
            classify_pack_staleness(pack(), facts(current_integration_sha=SHA_B, delta_paths=None)),
            "PACK_STALE_MATERIAL",
        )

    def test_dependency_moved_is_material(self) -> None:
        self.assertEqual(
            classify_pack_staleness(
                pack(),
                facts(dependency_completion={"T-001": SHA_C} | {"T-001": SHA_C}),
            ),
            "PACK_STALE_MATERIAL",
        )

    def test_invalid_pack_forms(self) -> None:
        for bad in (
            pack(task_pack_ref="task-pack:T-999@1"),
            pack(pinned_standard_revision=SHA_A),
            pack(branch="task/other"),
            pack(agent_freedom="F9"),
            pack(base_sha="main"),
            {k: v for k, v in pack().items() if k != "branch"},
        ):
            with self.subTest(bad=bad):
                self.assertEqual(classify_pack_staleness(bad, facts()), "PACK_INVALID")

    def test_rebind_authorization(self) -> None:
        self.assertTrue(rebind_allowed("PACK_CURRENT", explicit_authorization=False))
        self.assertFalse(rebind_allowed("PACK_STALE_NONMATERIAL", explicit_authorization=False))
        self.assertTrue(rebind_allowed("PACK_STALE_NONMATERIAL", explicit_authorization=True))
        self.assertFalse(rebind_allowed("PACK_STALE_MATERIAL", explicit_authorization=True))
        self.assertFalse(rebind_allowed("PACK_INVALID", explicit_authorization=True))


class ExactShaValidationTests(unittest.TestCase):
    def test_head_drift_supersedes(self) -> None:
        self.assertEqual(resolve_validator_dispatch(SHA_A, SHA_A), "EXECUTE")
        self.assertEqual(resolve_validator_dispatch(SHA_A, SHA_B), "HEAD_DRIFT_SUPERSEDED")
        self.assertEqual(resolve_validator_dispatch(None, SHA_A), "HEAD_DRIFT_SUPERSEDED")
        self.assertEqual(resolve_validator_dispatch(SHA_A, None), "HEAD_DRIFT_SUPERSEDED")

    def test_validator_outcome_semantics(self) -> None:
        self.assertEqual(
            validator_outcome(executed=True, required_checks_failed=False, environment_unavailable=False),
            "PASS",
        )
        self.assertEqual(
            validator_outcome(executed=True, required_checks_failed=True, environment_unavailable=False),
            "FAIL",
        )
        self.assertEqual(
            validator_outcome(executed=True, required_checks_failed=True, environment_unavailable=True),
            "BLOCKED",
        )
        self.assertEqual(
            validator_outcome(executed=False, required_checks_failed=False, environment_unavailable=False),
            "NOT_RUN",
        )

    def test_validator_never_repairs_source(self) -> None:
        self.assertFalse(validator_may_repair_source("validator"))
        self.assertTrue(validator_may_repair_source("builder"))

    def test_pass_never_moves_to_successor(self) -> None:
        self.assertTrue(evidence_reusable_on_successor({"validation_impact": "none", "evidence_reusable": True}))
        for decision in (
            {"validation_impact": "affected", "evidence_reusable": True},
            {"validation_impact": "none", "evidence_reusable": False},
            {"validation_impact": "unknown"},
            {},
        ):
            with self.subTest(decision=decision):
                self.assertFalse(evidence_reusable_on_successor(decision))

    def test_validation_result_head_drift_event_cannot_be_pass(self) -> None:
        schema = load_schema("agent-event-v2.schema.json")
        base = {
            "schema": "ai-dev/event-v2",
            "event": "VALIDATION_RESULT",
            "actor_role": "validator",
            "operator_kind": "codex",
            "operator_id": "codex:ubuntu-build-01",
            "sha": SHA_B,
            "gate": "platform",
            "environment": "ubuntu",
            "command": "make check",
            "exit_code": 0,
            "evidence": "run-url",
            "status": "BLOCKED",
            "drift": "HEAD_DRIFT",
            "dispatch_id": "d-9",
            "requested_head_sha": SHA_A,
            "current_pr_head": SHA_B,
        }
        self.assertEqual(validate_subset(base, schema), [])
        self.assertTrue(validate_subset(dict(base, status="PASS"), schema))


class DispatchClaimEventTests(unittest.TestCase):
    def test_claim_event_valid_for_worker_roles(self) -> None:
        schema = load_schema("agent-event-v2.schema.json")
        for role, kind in (("builder", "claude-code"), ("validator", "codex"), ("reviewer", "chatgpt-web")):
            with self.subTest(role=role):
                value = claim_event(actor_role=role, operator_kind=kind, dispatch_id=f"d-{role}")
                self.assertEqual(validate_subset(value, schema), [])

    def test_claim_event_rejects_non_worker_roles_and_wrong_state(self) -> None:
        schema = load_schema("agent-event-v2.schema.json")
        invalid = [
            claim_event(actor_role="scheduler"),
            claim_event(actor_role="merge-controller"),
            claim_event(dispatch_state="READY"),
            claim_event(dispatch_state="COMPLETED"),
            {k: v for k, v in claim_event().items() if k != "dispatch_id"},
            {k: v for k, v in claim_event().items() if k != "sha"},
        ]
        for value in invalid:
            with self.subTest(value=value.get("actor_role"), state=value.get("dispatch_state")):
                self.assertTrue(validate_subset(value, schema), value)

    def test_pack_state_event(self) -> None:
        schema = load_schema("agent-event-v2.schema.json")
        valid = {
            "schema": "ai-dev/event-v2",
            "event": "EXECUTION_PACK_STATE_CHANGED",
            "actor_role": "scheduler",
            "operator_kind": "chatgpt-web",
            "operator_id": "chatgpt-web:web-a",
            "task": "#50",
            "execution_pack_ref": "pack-T002-1",
            "pack_state": "PACK_STALE_MATERIAL",
            "reason": "integration advanced past material inputs",
        }
        self.assertEqual(validate_subset(valid, schema), [])
        for invalid in (
            dict(valid, actor_role="validator"),
            dict(valid, actor_role="reviewer"),
            dict(valid, pack_state="PACK_GREEN"),
            {k: v for k, v in valid.items() if k != "reason"},
            {k: v for k, v in valid.items() if k != "execution_pack_ref"},
        ):
            with self.subTest(invalid=invalid):
                self.assertTrue(validate_subset(invalid, schema), invalid)

    def test_legacy_dispatch_vocabulary_still_valid(self) -> None:
        schema = load_schema("agent-event-v2.schema.json")
        for state in ("QUEUED", "DELIVERED", "ACKNOWLEDGED", "RUNNING", "DONE", "FAILED", "CANCELLED", "TIMEOUT", "STALE", "READY", "CLAIMED", "COMPLETED", "SUPERSEDED"):
            with self.subTest(state=state):
                value = {
                    "schema": "ai-dev/event-v2",
                    "event": "DISPATCH_STATE_CHANGED",
                    "actor_role": "scheduler",
                    "operator_kind": "chatgpt-web",
                    "operator_id": "web-a",
                    "dispatch_id": "d-1",
                    "dispatch_state": state,
                }
                self.assertEqual(validate_subset(value, schema), [])

    def test_vocabulary_aliases(self) -> None:
        self.assertEqual(DISPATCH_VOCABULARY_ALIASES["READY"], "QUEUED")
        self.assertEqual(DISPATCH_VOCABULARY_ALIASES["CLAIMED"], "ACKNOWLEDGED")
        self.assertEqual(DISPATCH_VOCABULARY_ALIASES["COMPLETED"], "DONE")
        self.assertEqual(DISPATCH_VOCABULARY_ALIASES["SUPERSEDED"], "STALE")


class HandoffSchemaTests(unittest.TestCase):
    def test_dispatched_validator_handoff_requires_requested_head(self) -> None:
        schema = load_schema("local-agent-handoff.schema.json")
        base = {
            "repository": "kaicreator-mm/repo",
            "issue": "#10",
            "standard_version": "3.4.0",
            "standard_revision": SHA_C,
            "integration_target": "version/v3.4.0",
            "baseline_sha": BASELINE,
            "role": "validator",
            "execution_profile": "LOCAL_VALIDATOR",
            "scope": ["platform validation"],
            "frozen_inputs": ["PRD"],
            "existing_evidence": ["review PASS"],
            "remaining_work": ["run platform matrix"],
            "required_gates": ["platform"],
            "validation_tuples": ["windows x python3.12 x platform"],
            "validation_profile": "platform",
            "execution_environment": "Windows Build Host",
            "canonical_entrypoints": ["scripts/check.ps1"],
            "allowed_changes": ["none"],
            "forbidden_changes": ["product source"],
            "completion_rule": "all gates PASS",
            "blocker_rule": "publish BLOCKED",
            "expected_output": ["validation report"],
            "handoff_state": "DISPATCHED",
            "dispatch_id": "d-5",
            "requested_head_sha": SHA_B,
        }
        self.assertEqual(validate_subset(base, schema), [])
        missing = {k: v for k, v in base.items() if k != "requested_head_sha"}
        self.assertTrue(validate_subset(missing, schema))

    def test_validation_report_identity_fields(self) -> None:
        schema = load_schema("validation-report.schema.json")
        valid = {
            "repository": "kaicreator-mm/repo",
            "version": "3.4.0",
            "task": "T-005",
            "issue": "#51",
            "pr": "#60",
            "dispatch_id": "d-5",
            "tested_sha": SHA_B,
            "expected_base_sha": SHA_A,
            "requested_sha": SHA_B,
            "actual_checked_out_sha": SHA_B,
            "current_pr_head": SHA_B,
            "focused_tests": {"passed": 12, "failed": 0},
            "working_tree_clean": True,
            "source_modifications_after_validation": False,
            "execution_host_role": "local-validator",
            "platform": "windows",
            "runtime_toolchain": "Python 3.12",
            "validation_profile": "platform",
            "command": "pytest -q",
            "exit_code": 0,
            "state": "PASS",
        }
        self.assertEqual(validate_subset(valid, schema), [])
        self.assertTrue(validate_subset(dict(valid, state="GREEN"), schema))
        self.assertTrue(validate_subset(dict(valid, tested_sha="head"), schema))


class QueueProjectionTests(unittest.TestCase):
    def test_queue_item_status_matrix(self) -> None:
        cases = [
            ("READY", None, True, "READY"),
            ("READY", None, False, "HOLD"),
            ("CLAIMED", None, True, "RUNNING"),
            ("RUNNING", None, True, "RUNNING"),
            ("COMPLETED", "PASS", True, "PASS"),
            ("COMPLETED", "FAIL", True, "FAIL"),
            ("COMPLETED", "BLOCKED", True, "BLOCKED"),
            ("COMPLETED", None, True, "BLOCKED"),
            ("BLOCKED", None, True, "BLOCKED"),
            ("SUPERSEDED", None, True, "SUPERSEDED"),
        ]
        for state, result, prereq, expected in cases:
            with self.subTest(state=state, result=result):
                self.assertEqual(
                    queue_item_status(dispatch_state=state, result=result, prerequisites_satisfied=prereq),
                    expected,
                )

    def test_queue_rejects_unknown_state(self) -> None:
        with self.assertRaises(ValueError):
            queue_item_status(dispatch_state="DONE-ISH")

    def test_projection_deterministic_with_mixed_items(self) -> None:
        items = [
            {"dispatch_id": "d-1", "task": "T-002", "dispatch_state": "READY", "prerequisites_satisfied": True},
            {"dispatch_id": "d-2", "task": "T-004", "dispatch_state": "READY", "prerequisites_satisfied": False},
            {"dispatch_id": "d-3", "task": "T-005", "dispatch_state": "SUPERSEDED"},
            {"dispatch_id": "d-4", "task": "T-006", "dispatch_state": "COMPLETED", "result": "PASS"},
        ]
        projection = project_queue(items)
        self.assertEqual([row["status"] for row in projection], ["READY", "HOLD", "SUPERSEDED", "PASS"])
        for row in projection:
            self.assertEqual(row["non_authoritative"], "NON_AUTHORITATIVE_DERIVED_STATE")
        self.assertEqual(project_queue(items), project_queue(items))


class ScenarioATests(unittest.TestCase):
    """Full local builder positive flow."""

    def test_jit_branch_rule(self) -> None:
        self.assertTrue(jit_branch_allowed(dependencies_merged=True, stacked_code_dependency=False))
        self.assertFalse(jit_branch_allowed(dependencies_merged=False, stacked_code_dependency=False))
        self.assertTrue(jit_branch_allowed(dependencies_merged=False, stacked_code_dependency=True))

    def test_positive_flow(self) -> None:
        self.assertEqual(classify_pack_staleness(pack(), facts()), "PACK_CURRENT")
        self.assertTrue(
            merge_ready(
                required_gates_pass=True,
                review_condition_satisfied=True,
                dependencies_satisfied=True,
                topology_valid=True,
                unresolved_release_significant_findings=0,
            )
        )


class ScenarioDAndClaimTests(unittest.TestCase):
    def test_duplicate_claim_resolution(self) -> None:
        self.assertEqual(resolve_duplicate_claim(existing_claim_operator=None, incoming_operator="codex:u1"), "CLAIM")
        self.assertEqual(resolve_duplicate_claim(existing_claim_operator="codex:u1", incoming_operator="codex:u1"), "IDEMPOTENT_RECLAIM")
        self.assertEqual(resolve_duplicate_claim(existing_claim_operator="codex:u1", incoming_operator="codex:u2"), "REJECT_CONCURRENT_CLAIM")

    def test_review_invalidation_on_head_change(self) -> None:
        self.assertTrue(review_still_valid(reviewed_sha=SHA_A, current_head=SHA_A))
        self.assertFalse(review_still_valid(reviewed_sha=SHA_A, current_head=SHA_B))
        self.assertFalse(review_still_valid(reviewed_sha=None, current_head=SHA_B))


class ScenarioGTests(unittest.TestCase):
    """Worker restart recovery from GitHub facts alone."""

    def test_recovery_matrix(self) -> None:
        self.assertEqual(
            worker_recovery_decision(
                dispatch_state="COMPLETED", result_published=True, claimed_by="codex:u1", replacement_operator="codex:u2"
            ),
            "NOTHING_TO_DO",
        )
        self.assertEqual(
            worker_recovery_decision(
                dispatch_state="RUNNING", result_published=False, claimed_by="codex:u1", replacement_operator="codex:u1"
            ),
            "RESUME",
        )
        self.assertEqual(
            worker_recovery_decision(
                dispatch_state="CLAIMED", result_published=False, claimed_by="codex:u1", replacement_operator="codex:u2"
            ),
            "SUPERSEDE_AND_REDISPATCH",
        )
        self.assertEqual(
            worker_recovery_decision(
                dispatch_state="READY", result_published=False, claimed_by=None, replacement_operator="codex:u2"
            ),
            "SUPERSEDE_OR_NEW_DISPATCH",
        )
        self.assertEqual(
            worker_recovery_decision(
                dispatch_state="BLOCKED", result_published=False, claimed_by="codex:u1", replacement_operator="codex:u1"
            ),
            "AWAIT_UNBLOCK_OR_SUPERSEDE",
        )


class FreedomAndAuthorityTests(unittest.TestCase):
    def test_no_self_promotion(self) -> None:
        self.assertTrue(freedom_allows("F3_ARCHITECTURE_REQUIRED", "F0_MECHANICAL"))
        self.assertTrue(freedom_allows("F1_BOUNDED_IMPLEMENTATION", "F1_BOUNDED_IMPLEMENTATION"))
        self.assertFalse(freedom_allows("F1_BOUNDED_IMPLEMENTATION", "F2_ENGINEERING_DISCRETION"))
        self.assertFalse(freedom_allows("F0_MECHANICAL", "F1_BOUNDED_IMPLEMENTATION"))
        self.assertFalse(freedom_allows("F9", "F0_MECHANICAL"))

    def test_authority_failures_route_upward(self) -> None:
        for kind in ("TASK_PACK_DEFECT", "ARCHITECTURE_CONTRADICTION", "EXECUTION_PACK_INVALID"):
            self.assertEqual(route_authority_failure(kind), "STOP_AND_ROUTE_UPWARD")
        with self.assertRaises(ValueError):
            route_authority_failure("JUST_REDESIGN_LOCALLY")

    def test_freedom_levels_complete(self) -> None:
        self.assertEqual(
            AGENT_FREEDOM_LEVELS,
            ("F0_MECHANICAL", "F1_BOUNDED_IMPLEMENTATION", "F2_ENGINEERING_DISCRETION", "F3_ARCHITECTURE_REQUIRED"),
        )


class RetentionAndBaselineTests(unittest.TestCase):
    def test_package_leakage_detection(self) -> None:
        packaged = [
            "dist/app.js",
            ".agent/execution/T-002/MANIFEST.yaml",
            ".agent/execution/T-002/EXECUTION_CONTRACT.md",
            "README.md",
        ]
        self.assertEqual(
            package_leaks(packaged),
            [".agent/execution/T-002/MANIFEST.yaml", ".agent/execution/T-002/EXECUTION_CONTRACT.md"],
        )
        self.assertEqual(package_leaks(["dist/app.js"]), [])

    def test_baseline_refresh_prioritizes_blockers(self) -> None:
        order = baseline_refresh_priority(blocking={"PR-A": ["PR-B"], "PR-B": []})
        self.assertEqual(order, ["PR-A", "PR-B"])
        order = baseline_refresh_priority(blocking={"PR-B": [], "PR-A": ["PR-B", "PR-C"], "PR-C": []})
        self.assertEqual(order[0], "PR-A")


class RepositoryPlanningInvariantTests(unittest.TestCase):
    def test_task_packs_index_is_wellformed(self) -> None:
        index = json.loads((ROOT / "docs/implementation/3.4.0/TASK_PACKS.json").read_text(encoding="utf-8"))
        self.assertEqual(index["version"], "3.4.0")
        self.assertEqual(index["baseline_sha"], BASELINE)
        tasks = index["tasks"]
        self.assertEqual(len(tasks), 10)
        ids = {task["task_id"] for task in tasks}
        self.assertEqual(len(ids), 10)

        by_id = {task["task_id"]: task for task in tasks}
        for task in tasks:
            with self.subTest(task=task["task_id"]):
                self.assertEqual(task["integration_target"], "version/v3.4.0")
                self.assertEqual(task["baseline_sha"], BASELINE)
                self.assertTrue(task["acceptance"])
                self.assertIn(task["agent_freedom"], AGENT_FREEDOM_LEVELS)
                for dep in task.get("dependencies", []):
                    self.assertIn(dep, ids)

        # closure task depends on regression task; regression covers T-002..T-008
        self.assertEqual(by_id["T-010"]["dependencies"], ["T-009"])
        self.assertIn("T-002", by_id["T-009"]["dependencies"])

        # acyclic
        visiting: set[str] = set()
        done: set[str] = set()

        def visit(task_id: str) -> None:
            self.assertNotIn(task_id, visiting, f"cycle at {task_id}")
            if task_id in done:
                return
            visiting.add(task_id)
            for dep in by_id[task_id].get("dependencies", []):
                visit(dep)
            visiting.discard(task_id)
            done.add(task_id)

        for task_id in sorted(ids):
            visit(task_id)

    def test_each_task_pack_entry_matches_task_contract_schema(self) -> None:
        schema = load_schema("task-contract.schema.json")
        index = json.loads((ROOT / "docs/implementation/3.4.0/TASK_PACKS.json").read_text(encoding="utf-8"))
        for task in index["tasks"]:
            with self.subTest(task=task["task_id"]):
                self.assertEqual(validate_subset(task, schema), [])


if __name__ == "__main__":
    loader = unittest.defaultTestLoader
    suite = unittest.TestSuite()
    for case in (
        DispatchContractTests,
        ExecutionPackContractTests,
        PackStalenessTests,
        ExactShaValidationTests,
        DispatchClaimEventTests,
        HandoffSchemaTests,
        QueueProjectionTests,
        ScenarioATests,
        ScenarioDAndClaimTests,
        ScenarioGTests,
        FreedomAndAuthorityTests,
        RetentionAndBaselineTests,
        RepositoryPlanningInvariantTests,
    ):
        suite.addTests(loader.loadTestsFromTestCase(case))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    raise SystemExit(0 if result.wasSuccessful() else 1)
