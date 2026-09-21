"""Deterministic v3.4 orchestration rules.

Pure functions implementing the frozen v3.4 architecture decisions
(docs/implementation/3.4.0/ARCHITECTURE_DECISION.md). They are the machine
oracle for scripts/test_v34_lifecycle_contracts.py and MAY be reused by
project-level reducers. Every function is deterministic and fails closed.
"""

from __future__ import annotations

from typing import Iterable, Mapping, Sequence

# ---------------------------------------------------------------------------
# Vocabularies
# ---------------------------------------------------------------------------

AGENT_FREEDOM_LEVELS = (
    "F0_MECHANICAL",
    "F1_BOUNDED_IMPLEMENTATION",
    "F2_ENGINEERING_DISCRETION",
    "F3_ARCHITECTURE_REQUIRED",
)

PACK_STATES = (
    "PACK_CURRENT",
    "PACK_STALE_NONMATERIAL",
    "PACK_STALE_MATERIAL",
    "PACK_INVALID",
)

PULL_DISPATCH_STATES = (
    "READY",
    "CLAIMED",
    "RUNNING",
    "COMPLETED",
    "BLOCKED",
    "SUPERSEDED",
)

# Pull vocabulary aliases onto the v3.3 lifecycle vocabulary. Both describe
# the same dispatch dimension; aliases are projection-only.
DISPATCH_VOCABULARY_ALIASES = {
    "READY": "QUEUED",
    "CLAIMED": "ACKNOWLEDGED",
    "RUNNING": "RUNNING",
    "COMPLETED": "DONE",
    "SUPERSEDED": "STALE",
}

QUEUE_ITEM_STATUSES = (
    "READY",
    "HOLD",
    "RUNNING",
    "PASS",
    "FAIL",
    "BLOCKED",
    "SUPERSEDED",
)

GATE_STATES = ("PASS", "FAIL", "BLOCKED", "NOT_RUN", "NOT_APPLICABLE")

EXECUTION_PACK_ROOTS = (".agent/execution/",)

REQUIRED_PACK_FIELDS = (
    "pack_id",
    "task_id",
    "base_sha",
    "task_pack_ref",
    "branch",
    "agent_freedom",
    "pinned_standard_revision",
)

SHA_LENGTH = 40


# ---------------------------------------------------------------------------
# Execution Pack staleness (fail closed)
# ---------------------------------------------------------------------------


def _is_sha(value: object) -> bool:
    return isinstance(value, str) and len(value) == SHA_LENGTH and all(c in "0123456789abcdefABCDEF" for c in value)


def classify_pack_staleness(pack: Mapping[str, object], facts: Mapping[str, object]) -> str:
    """Classify an Execution Pack against current repository facts.

    pack keys: base_sha, task_pack_ref, branch, pinned_standard_revision,
               dependency_completion (task -> sha), material_paths (list)
    facts keys: current_integration_sha, task_pack_ref, branch,
                pinned_standard_revision, dependency_completion (task -> sha),
                delta_paths (paths changed since pack base; None = unknown)
    """
    for field in REQUIRED_PACK_FIELDS:
        if field not in pack or pack[field] in (None, ""):
            return "PACK_INVALID"

    if not _is_sha(pack["base_sha"]) or not _is_sha(pack["pinned_standard_revision"]):
        return "PACK_INVALID"
    if pack["agent_freedom"] not in AGENT_FREEDOM_LEVELS:
        return "PACK_INVALID"
    if pack["task_pack_ref"] != facts.get("task_pack_ref"):
        return "PACK_INVALID"
    if pack["pinned_standard_revision"] != facts.get("pinned_standard_revision"):
        return "PACK_INVALID"
    if pack["branch"] != facts.get("branch"):
        return "PACK_INVALID"

    pack_deps = pack.get("dependency_completion") or {}
    current_deps = facts.get("dependency_completion") or {}
    if not isinstance(pack_deps, Mapping) or not isinstance(current_deps, Mapping):
        return "PACK_INVALID"
    for task, sha in pack_deps.items():
        if current_deps.get(task) != sha:
            # A dependency the pack was generated against has moved.
            return "PACK_STALE_MATERIAL"

    if pack["base_sha"] == facts.get("current_integration_sha"):
        return "PACK_CURRENT"

    delta_paths = facts.get("delta_paths")
    if delta_paths is None:
        # Unknown impact fails closed to material.
        return "PACK_STALE_MATERIAL"
    if not isinstance(delta_paths, Sequence):
        return "PACK_INVALID"
    material = set(pack.get("material_paths") or ())
    if _delta_touches_material(delta_paths, material):
        return "PACK_STALE_MATERIAL"
    return "PACK_STALE_NONMATERIAL"


def _delta_touches_material(delta_paths: Sequence[str], material: set[str]) -> bool:
    """A delta path touches material when it equals, falls under, or covers a
    declared material path. Conservative overlap fails closed to MATERIAL."""
    for delta in delta_paths:
        if not isinstance(delta, str):
            continue
        for path in material:
            if delta == path or delta.startswith(path) or path.startswith(delta):
                return True
    return False


def rebind_allowed(classification: str, explicit_authorization: bool) -> bool:
    """Only PACK_CURRENT executes freely; NONMATERIAL continues solely via an
    explicitly authorized impact/rebind action recording both identities."""
    if classification == "PACK_CURRENT":
        return True
    if classification == "PACK_STALE_NONMATERIAL":
        return explicit_authorization
    return False


# ---------------------------------------------------------------------------
# Exact-SHA validation dispatch rules
# ---------------------------------------------------------------------------


def resolve_validator_dispatch(requested_head_sha: object, current_pr_head: object) -> str:
    if requested_head_sha is None or current_pr_head is None:
        return "HEAD_DRIFT_SUPERSEDED"
    if requested_head_sha == current_pr_head:
        return "EXECUTE"
    return "HEAD_DRIFT_SUPERSEDED"


def validator_outcome(
    *,
    executed: bool,
    required_checks_failed: bool,
    environment_unavailable: bool,
) -> str:
    """Real defect -> FAIL; environment inability -> BLOCKED; clean run -> PASS."""
    if environment_unavailable:
        return "BLOCKED"
    if not executed:
        return "NOT_RUN"
    if required_checks_failed:
        return "FAIL"
    return "PASS"


def validator_may_repair_source(dispatch_role: str) -> bool:
    """A Validator never implicitly repairs product source; repair requires a
    separate Builder dispatch."""
    return dispatch_role == "builder"


def evidence_identity(*, tested_sha: str, environment: str, profile: str, commands: Sequence[str]) -> Mapping[str, object]:
    return {
        "tested_sha": tested_sha,
        "environment": environment,
        "validation_profile": profile,
        "commands": list(commands),
    }


def evidence_reusable_on_successor(decision: Mapping[str, object]) -> bool:
    """PASS is never rewritten onto a successor SHA; reuse is only explicit
    impact-discipline composition (validation_impact=none)."""
    return decision.get("validation_impact") == "none" and decision.get("evidence_reusable") is True


# ---------------------------------------------------------------------------
# JIT branch rule
# ---------------------------------------------------------------------------


def jit_branch_allowed(*, dependencies_merged: bool, stacked_code_dependency: bool) -> bool:
    return dependencies_merged or bool(stacked_code_dependency)


# ---------------------------------------------------------------------------
# Agent freedom (no self-promotion)
# ---------------------------------------------------------------------------


def freedom_allows(granted: str, needed: str) -> bool:
    if granted not in AGENT_FREEDOM_LEVELS or needed not in AGENT_FREEDOM_LEVELS:
        return False
    return AGENT_FREEDOM_LEVELS.index(needed) <= AGENT_FREEDOM_LEVELS.index(granted)


def route_authority_failure(kind: str) -> str:
    valid = ("TASK_PACK_DEFECT", "ARCHITECTURE_CONTRADICTION", "EXECUTION_PACK_INVALID")
    if kind not in valid:
        raise ValueError(f"unknown failure kind: {kind}")
    return "STOP_AND_ROUTE_UPWARD"


# ---------------------------------------------------------------------------
# Queue projection (derived, never authoritative)
# ---------------------------------------------------------------------------


def queue_item_status(
    *,
    dispatch_state: str,
    result: object = None,
    prerequisites_satisfied: bool = True,
) -> str:
    if dispatch_state not in PULL_DISPATCH_STATES:
        raise ValueError(f"unknown dispatch state: {dispatch_state}")
    if dispatch_state == "READY" and not prerequisites_satisfied:
        return "HOLD"
    if dispatch_state == "READY":
        return "READY"
    if dispatch_state == "RUNNING":
        return "RUNNING"
    if dispatch_state == "CLAIMED":
        return "RUNNING"
    if dispatch_state == "BLOCKED":
        return "BLOCKED"
    if dispatch_state == "SUPERSEDED":
        return "SUPERSEDED"
    if dispatch_state == "COMPLETED":
        if result == "PASS":
            return "PASS"
        if result == "FAIL":
            return "FAIL"
        return "BLOCKED"
    raise ValueError(dispatch_state)


def project_queue(items: Iterable[Mapping[str, object]]) -> list[Mapping[str, object]]:
    """Deterministic queue projection: stable input order, one row per item."""
    projection = []
    for item in items:
        projection.append(
            {
                "dispatch_id": item.get("dispatch_id"),
                "task": item.get("task"),
                "issue": item.get("issue"),
                "pr": item.get("pr"),
                "expected_base_sha": item.get("expected_base_sha"),
                "requested_head_sha": item.get("requested_head_sha"),
                "validation_profile": item.get("validation_profile"),
                "status": queue_item_status(
                    dispatch_state=item["dispatch_state"],
                    result=item.get("result"),
                    prerequisites_satisfied=item.get("prerequisites_satisfied", True),
                ),
                "non_authoritative": "NON_AUTHORITATIVE_DERIVED_STATE",
            }
        )
    return projection


# ---------------------------------------------------------------------------
# Claims, review, merge, recovery
# ---------------------------------------------------------------------------


def resolve_duplicate_claim(*, existing_claim_operator: object, incoming_operator: str) -> str:
    if existing_claim_operator is None:
        return "CLAIM"
    if existing_claim_operator == incoming_operator:
        return "IDEMPOTENT_RECLAIM"
    return "REJECT_CONCURRENT_CLAIM"


def review_still_valid(*, reviewed_sha: object, current_head: object) -> bool:
    return reviewed_sha is not None and reviewed_sha == current_head


def merge_ready(
    *,
    required_gates_pass: bool,
    review_condition_satisfied: bool,
    dependencies_satisfied: bool,
    topology_valid: bool,
    unresolved_release_significant_findings: int,
) -> bool:
    return (
        required_gates_pass
        and review_condition_satisfied
        and dependencies_satisfied
        and topology_valid
        and unresolved_release_significant_findings == 0
    )


def worker_recovery_decision(
    *,
    dispatch_state: str,
    result_published: bool,
    claimed_by: object,
    replacement_operator: str,
) -> str:
    """Recoverable from GitHub facts alone."""
    if dispatch_state == "COMPLETED" and result_published:
        return "NOTHING_TO_DO"
    if dispatch_state in ("READY", "SUPERSEDED"):
        return "SUPERSEDE_OR_NEW_DISPATCH"
    if dispatch_state in ("CLAIMED", "RUNNING"):
        if claimed_by == replacement_operator:
            return "RESUME"
        return "SUPERSEDE_AND_REDISPATCH"
    if dispatch_state == "BLOCKED":
        return "AWAIT_UNBLOCK_OR_SUPERSEDE"
    raise ValueError(dispatch_state)


def baseline_refresh_priority(*, blocking: Mapping[str, Sequence[str]]) -> list[str]:
    """Order final authoritative validation so blockers are validated first.

    blocking maps candidate -> candidates it blocks. Deterministic by
    (blocks_count desc, name) so equal candidates keep stable order.
    """
    names = sorted(blocking)
    ranked = sorted(names, key=lambda name: (-len(blocking.get(name, ())), name))
    return ranked


# ---------------------------------------------------------------------------
# Retention / package exclusion
# ---------------------------------------------------------------------------


def package_leaks(packaged_paths: Iterable[str], roots: Sequence[str] = EXECUTION_PACK_ROOTS) -> list[str]:
    return [path for path in packaged_paths if any(path.startswith(root) for root in roots)]
