"""Deterministic v3.4 orchestration rules.

Pure functions implementing the frozen v3.4 architecture decisions
(docs/implementation/3.4.0/ARCHITECTURE_DECISION.md). They are the machine
oracle for scripts/test_v34_lifecycle_contracts.py and MAY be reused by
project-level reducers. Every function is deterministic and fails closed.
"""

from __future__ import annotations

from typing import Iterable, Mapping, Sequence

import re

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

REQUIRED_CORE_ARTIFACTS = (
    "MANIFEST.yaml",
    "EXECUTION_CONTRACT.md",
    "TEST_MATRIX.yaml",
    "FAILURE_MATRIX.yaml",
    "IMPLEMENTATION_MAP.md",
    "REVIEW_CHECKLIST.md",
)

SHA_LENGTH = 40


# ---------------------------------------------------------------------------
# Execution Pack staleness (fail closed)
# ---------------------------------------------------------------------------


def _is_sha(value: object) -> bool:
    return isinstance(value, str) and len(value) == SHA_LENGTH and all(c in "0123456789abcdefABCDEF" for c in value)


def _dependency_completion_map(value: object) -> dict[str, str] | None:
    """Normalize dependency identities from either the manifest wire shape
    (['T-001@<sha>', ...]) or an internal mapping.

    Returning None means malformed/unknown. Duplicate task identities fail
    closed even when they repeat the same SHA so provenance stays unambiguous.
    """
    if value is None:
        return {}
    if isinstance(value, Mapping):
        normalized: dict[str, str] = {}
        for task, sha in value.items():
            if not isinstance(task, str) or not task or not _is_sha(sha):
                return None
            normalized[task] = str(sha)
        return normalized
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        normalized = {}
        for item in value:
            if not isinstance(item, str) or "@" not in item:
                return None
            task, sha = item.rsplit("@", 1)
            if not task or not _is_sha(sha) or task in normalized:
                return None
            normalized[task] = sha
        return normalized
    return None


def core_artifacts_complete(value: object) -> bool:
    """Semantic completeness check for the six required pack artifacts.

    The repository's dependency-free JSON-Schema subset does not implement
    uniqueItems, so claim-time semantics enforce exact set equality.
    """
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes, bytearray)):
        return False
    items = list(value)
    return len(items) == len(REQUIRED_CORE_ARTIFACTS) and set(items) == set(REQUIRED_CORE_ARTIFACTS)


def _normalize_impact_path(value: object) -> str | None:
    """Normalize a repository-relative impact path or return None if unknown.

    NONMATERIAL classification needs positive comparable path evidence. Empty,
    non-string, traversal-like, or root-only facts are therefore not ignored;
    callers fail closed to PACK_STALE_MATERIAL when normalization returns None.
    """
    if not isinstance(value, str):
        return None
    normalized = value.strip().replace("\\", "/").strip("/")
    if not normalized:
        return None
    segments = normalized.split("/")
    if any(segment in ("", ".", "..") for segment in segments):
        return None
    return "/".join(segments)


def classify_pack_staleness(pack: Mapping[str, object], facts: Mapping[str, object]) -> str:
    """Classify an Execution Pack against current repository facts.

    Manifest dependency_completion wire entries use '<task-id>@<40-hex-sha>'.
    Internal callers may supply a task->sha mapping; both normalize to the same
    identity model. material_paths is positive impact coverage: if the base
    moved and this coverage is absent/malformed, classification fails closed to
    PACK_STALE_MATERIAL rather than assuming the delta is nonmaterial.
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

    # A real manifest always carries core_artifacts. Keep compatibility with
    # narrow historical/unit callers that model only staleness inputs, but fail
    # closed when the field is present and incomplete/duplicated.
    if "core_artifacts" in pack and not core_artifacts_complete(pack.get("core_artifacts")):
        return "PACK_INVALID"

    pack_deps = _dependency_completion_map(pack.get("dependency_completion"))
    if pack_deps is None:
        return "PACK_INVALID"
    current_deps = _dependency_completion_map(facts.get("dependency_completion"))
    if current_deps is None:
        return "PACK_STALE_MATERIAL"
    if pack_deps != current_deps:
        return "PACK_STALE_MATERIAL"

    if pack["base_sha"] == facts.get("current_integration_sha"):
        return "PACK_CURRENT"

    delta_paths = facts.get("delta_paths")
    if delta_paths is None:
        # Unknown impact fails closed to material.
        return "PACK_STALE_MATERIAL"
    if not isinstance(delta_paths, Sequence) or isinstance(delta_paths, (str, bytes, bytearray)):
        return "PACK_STALE_MATERIAL"

    material_paths = pack.get("material_paths")
    if (
        not isinstance(material_paths, Sequence)
        or isinstance(material_paths, (str, bytes, bytearray))
        or not material_paths
    ):
        # NONMATERIAL requires positive declared impact coverage.
        return "PACK_STALE_MATERIAL"

    normalized_delta: list[str] = []
    for delta in delta_paths:
        normalized = _normalize_impact_path(delta)
        if normalized is None:
            # Malformed/unknown delta facts are not positive NONMATERIAL proof.
            return "PACK_STALE_MATERIAL"
        normalized_delta.append(normalized)

    normalized_material: set[str] = set()
    for path in material_paths:
        normalized = _normalize_impact_path(path)
        if normalized is None:
            return "PACK_STALE_MATERIAL"
        normalized_material.add(normalized)

    if _delta_touches_material(normalized_delta, normalized_material):
        return "PACK_STALE_MATERIAL"
    return "PACK_STALE_NONMATERIAL"


def _delta_touches_material(delta_paths: Sequence[str], material: set[str]) -> bool:
    """Conservative path-overlap check with normalized segment boundaries."""
    for delta in delta_paths:
        for path in material:
            if (
                delta == path
                or delta.startswith(path + "/")
                or path.startswith(delta + "/")
            ):
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


def validator_result_matches_dispatch(dispatch: Mapping[str, object], result: Mapping[str, object]) -> bool:
    """Return True only when Validator evidence is bound to its exact dispatch.

    This is the canonical consumption rule for a version-scoped Validation
    Handoff Queue. A loose/legacy VALIDATION_RESULT may remain valid history,
    but it cannot complete a v3.4 Validator dispatch unless this identity tuple
    matches. Both Validation Report naming (`tested_sha`, `requested_sha`) and
    event naming (`sha`, `requested_head_sha`) are accepted.
    """
    if dispatch.get("role") != "validator":
        return False
    dispatch_id = dispatch.get("dispatch_id")
    requested = dispatch.get("requested_head_sha")
    expected_base = dispatch.get("expected_base_sha")
    profile = dispatch.get("validation_profile")
    if not dispatch_id or not _is_sha(requested) or not _is_sha(expected_base) or not profile:
        return False

    tested = result.get("tested_sha", result.get("sha"))
    result_requested = result.get("requested_sha", result.get("requested_head_sha"))
    actual = result.get("actual_checked_out_sha")
    current = result.get("current_pr_head")
    result_expected_base = result.get("expected_base_sha")
    result_profile = result.get("validation_profile")

    return (
        result.get("dispatch_id") == dispatch_id
        and tested == requested
        and result_requested == requested
        and actual == requested
        and current == requested
        and result_expected_base == expected_base
        and result_profile == profile
    )


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


# ---------------------------------------------------------------------------
# v4.10 T06B — serialized-admission helpers (additive; EXECUTION_ARCHITECTURE
# §11.1.1, GITHUB_AGENT_INTERACTION_PROTOCOL §8.4.2). Pure functions; fail
# closed on malformed input; never grant authority.
# ---------------------------------------------------------------------------

DEFAULT_COMPATIBILITY_GROUP = "__default__"

ENVIRONMENT_PROFILE_CONTRADICTION = "ENVIRONMENT_PROFILE_CONTRADICTION"

# A7: the historical profiles whose unambiguous legacy mapping projects the
# coarse execution environment. PLATFORM_VALIDATOR/CLOSURE_VALIDATOR are
# environment-orthogonal (A9/A10) and map through the explicit field only.
EXECUTION_PROFILE_ENVIRONMENTS = {
    "LOCAL_BUILDER": "LOCAL",
    "LOCAL_VALIDATOR": "LOCAL",
    "WEB_REVIEWER": "WEB",
}

ENVIRONMENT_ORTHOGONAL_PROFILES = ("PLATFORM_VALIDATOR", "CLOSURE_VALIDATOR")


def project_dispatch_environment(dispatch: Mapping[str, object]) -> str:
    """A7/A8/A9/A10/FC1 projection verifier for one dispatch record.

    Returns the routable execution environment: ``"LOCAL"``/``"WEB"`` for an
    unambiguous profile (A7), the explicit environment for an
    environment-orthogonal profile (A9), or ``"UNKNOWN"`` when the record is
    not routable by environment (A10/FC1; never guessed). A current writer
    whose explicit environment contradicts the unambiguous legacy mapping is
    rejected with ``ENVIRONMENT_PROFILE_CONTRADICTION`` (A8) instead of being
    silently reinterpreted. Malformed input fails closed.
    """
    profile = dispatch.get("execution_profile")
    if not isinstance(profile, str) or not profile:
        raise ValueError("execution_profile is required and must be a non-empty string")
    environment = dispatch.get("execution_environment")
    if environment is not None and environment not in ("WEB", "LOCAL"):
        raise ValueError(f"invalid execution_environment: {environment!r}")
    mapped = EXECUTION_PROFILE_ENVIRONMENTS.get(profile)
    if mapped is not None:
        if environment is not None and environment != mapped:
            raise ValueError(
                f"{ENVIRONMENT_PROFILE_CONTRADICTION}: execution_profile={profile!r} "
                f"maps to execution_environment={mapped!r} but the writer supplied "
                f"execution_environment={environment!r}; no silent reinterpretation"
            )
        return mapped
    if profile in ENVIRONMENT_ORTHOGONAL_PROFILES:
        return environment if environment is not None else "UNKNOWN"
    return "UNKNOWN"


def protected_claim_key_conforms(dispatch: Mapping[str, object]) -> bool:
    """B5/B6: the persisted protected claim key is audit provenance, never trusted.

    Returns True only when the dispatch carries no scheduler/user-supplied
    ``claim_key`` authority field (B6: the key is reducer-derived only) and any
    persisted ``protected_claim_key`` equals the deterministic re-derivation
    from the dispatch identity (B5). Malformed identities fail closed to False.
    """
    if "claim_key" in dispatch:
        return False
    persisted = dispatch.get("protected_claim_key")
    if persisted is None:
        return True
    try:
        derived = derive_claim_key(
            dispatch.get("repository"),
            dispatch.get("task"),
            dispatch.get("role"),
            dispatch.get("compatibility_group"),
        )
    except (TypeError, ValueError):
        return False
    return persisted == derived


def normalize_group(compatibility_group: object) -> str:
    """Normalize an omitted/null/empty compatibility group to ``__default__``.

    Non-string non-null values fail closed (TypeError) rather than guessing.
    """
    if compatibility_group is None:
        return DEFAULT_COMPATIBILITY_GROUP
    if not isinstance(compatibility_group, str):
        raise TypeError("compatibility_group must be a string or null")
    if not compatibility_group.strip():
        return DEFAULT_COMPATIBILITY_GROUP
    return compatibility_group


def derive_claim_key(
    repository: str, task: str, role: str, compatibility_group: object = None
) -> str:
    """Serialize the deterministic protected claim key ``repo#task:role:group``.

    Slot 4 is the normalized compatibility group; revision/session identifiers
    are never valid there. Any malformed input fails closed.
    """
    for name, value in (("repository", repository), ("role", role)):
        if not isinstance(value, str) or not value or any(ch in value for ch in "#:"):
            raise ValueError(f"invalid claim-key segment {name}: {value!r}")
    if not isinstance(task, str) or not task or not task.startswith("#") or ":" in task:
        raise ValueError(f"task must be '#<id>': {task!r}")
    group = normalize_group(compatibility_group)
    if any(ch in group for ch in "#:"):
        raise ValueError(f"invalid compatibility_group: {group!r}")
    return f"{repository}{task}:{role}:{group}"


def parse_claim_key(key: object) -> dict:
    """Reparse a serialized claim key; fails closed unless it roundtrips."""
    if not isinstance(key, str) or not key:
        raise ValueError("claim key must be a non-empty string")
    head, _, rest = key.partition("#")
    if not head or ":" not in rest:
        raise ValueError(f"malformed claim key: {key!r}")
    task, role_group = rest.split(":", 1)
    if ":" not in role_group:
        raise ValueError(f"malformed claim key (missing group slot): {key!r}")
    role, group = role_group.rsplit(":", 1)
    rebuilt = derive_claim_key(head, f"#{task}", role, group)
    if rebuilt != key:
        raise ValueError(f"claim key does not roundtrip: {key!r}")
    return {"repository": head, "task": f"#{task}", "role": role, "group": group}


def authorize_non_default(compatibility_group: object, authority_ref: object) -> bool:
    """Check the durable explicit-authorization input for a non-default group.

    Returns True only for a non-default group with a durable ``#<issue>@<id>``
    authority reference. Never downgrades to ``__default__``; malformed inputs
    fail closed instead of guessing.
    """
    group = normalize_group(compatibility_group)
    if group == DEFAULT_COMPATIBILITY_GROUP:
        return authority_ref is None or (
            isinstance(authority_ref, str) and bool(authority_ref)
        )
    if not isinstance(authority_ref, str) or not re.fullmatch(r"#\d+@\d+", authority_ref):
        raise ValueError(
            "non-default compatibility_group requires a durable #<issue>@<comment-id> authority ref"
        )
    return True


# Owning authority family per role for non-default compatibility groups
# (#861 machine-model rules 3/8: builders need Task Pack/DAG authority,
# validators need Validation-profile authority, reviewers need Review-policy
# authority; a durable ref of any other family is not authorization).
NON_DEFAULT_AUTHORITY_FAMILIES = {
    "builder": "TASK_PACK",
    "validator": "VALIDATION",
    "reviewer": "REVIEW_POLICY",
}

AUTHORITY_UNRESOLVED = "AUTHORITY_UNRESOLVED"
AUTHORITY_FAMILY_MISMATCH = "AUTHORITY_FAMILY_MISMATCH"
AUTHORITY_NOT_APPLICABLE = "AUTHORITY_NOT_APPLICABLE"
# R6 (Fresh Review R5 P1-1): the grant inventory must be bound to the durable
# owner/controller readback contract; an arbitrary caller-made mapping without
# that binding manufactures no authority.
AUTHORITY_OWNER_UNRESOLVED = "AUTHORITY_OWNER_UNRESOLVED"
AUTHORITY_CURRENTNESS_MISMATCH = "AUTHORITY_CURRENTNESS_MISMATCH"
AUTHORITY_SELF_REFERENCE = "AUTHORITY_SELF_REFERENCE"
# R7 (Fresh Review R6 P1-1): the referenced durable authority fact itself must
# be bound by trusted readback evidence (identity, existence/currentness,
# content-addressed digest, owner family, exact tuple, explicit authorization
# content); caller-supplied grant fields alone manufacture no authority and a
# grant drifting from the fact readback is rejected.
AUTHORITY_GRANT_DRIFT = "AUTHORITY_GRANT_DRIFT"

_SHA40 = re.compile(r"[0-9a-f]{40}")
_SHA256_HEX = re.compile(r"[0-9a-f]{64}")


def resolve_non_default_authority(
    *,
    repository: object,
    task: object,
    role: object,
    compatibility_group: object,
    authority_ref: object,
    authority_grants: object,
    authority_readback: object = None,
    authority_fact_readbacks: object = None,
    self_refs: object = None,
) -> bool:
    """Deterministically resolve the durable authority behind a non-default group.

    Machine half of the C3-C5/C7 boundary (#861). ``authority_grants`` is the
    controller-resolved grant inventory — the existing owner/controller proof
    path materialized before keyed admission — keyed by durable
    ``#<issue>@<id>`` ref, and ``authority_fact_readbacks`` is the trusted
    per-ref readback of the referenced durable authority fact itself,
    materialized by the controller/authority-reader adapter before keyed
    admission.

    R7 (Fresh Review R6 P1-1): authorization is derived from the trusted
    durable-fact readback, not from caller-supplied grant fields. Each
    fact readback MUST carry, for the exact ref: the durable identity
    (``ref``), existence/currentness (``exists`` — a ref that does not
    resolve, e.g. a 404 durable-looking ref, fails closed), the
    content-addressed binding to the exact durable fact content
    (``content_digest``, 64-hex SHA-256 of the canonical fact content), the
    owning ``authority_family``, the exact ``repository``/``task``/``role``
    applicability, and the explicit authorization content projected as
    ``groups``. A non-default group is admitted only when the fact readback
    carries the owning family for the role and covers the exact
    repository+task+role+group tuple. The caller grant inventory is only a
    projection: every authorization field of
    ``authority_grants[authority_ref]`` MUST equal the fact-readback-derived
    grant, otherwise ``AUTHORITY_GRANT_DRIFT`` fails closed — an arbitrarily
    decorated caller mapping (valid registry subject, valid owner_concern,
    correct tuple) manufactures no authority when the referenced durable fact
    is missing, stale, mismatched, or does not authorize the group.

    R6 (Fresh Review R5 P1-1): the inventory is additionally bound to the
    durable owner/controller readback contract — the same checked-in registry
    readback the owner-resolution path already verifies
    (``standard-manifest.json#semantic_authorities`` resolved concern -> owner,
    per ``test_v47_authority_registry.resolve_registry``). Each grant MUST name
    the semantic owner concern it resolves through (``owner_concern``, present
    in the supplied readback's owners map) and MUST carry the exact readback
    subject (``readback_subject``, the durable manifest blob id) it was
    resolved against; a stale/fabricated binding fails closed with
    ``AUTHORITY_OWNER_UNRESOLVED``/``AUTHORITY_CURRENTNESS_MISMATCH``. A grant
    whose durable ref equals one of the dispatch's own refs (``self_refs`` —
    e.g. the grant points back at this dispatch's own admission/claim comment)
    is self-reference and fails closed with ``AUTHORITY_SELF_REFERENCE``.
    Default-group dispatches need no authority and short-circuit to True.
    Purely local; no network; every ambiguity fails closed instead of guessing.
    """
    group = normalize_group(compatibility_group)
    if group == DEFAULT_COMPATIBILITY_GROUP:
        return True
    if not isinstance(authority_ref, str) or not re.fullmatch(r"#\d+@\d+", authority_ref):
        raise ValueError(
            "non-default compatibility_group requires a durable #<issue>@<comment-id> authority ref"
        )
    if self_refs is not None:
        if isinstance(self_refs, (str, bytes)) or not isinstance(self_refs, Iterable):
            raise ValueError(f"{AUTHORITY_SELF_REFERENCE}: self_refs must be an iterable of durable refs")
        if authority_ref in set(self_refs):
            raise ValueError(
                f"{AUTHORITY_SELF_REFERENCE}: grant ref {authority_ref} points back at the "
                "dispatch's own durable comment; a dispatch never authorizes itself"
            )
    if not isinstance(authority_grants, Mapping):
        raise ValueError(
            f"{AUTHORITY_UNRESOLVED}: no controller-resolved authority grant "
            f"inventory was supplied for {authority_ref}"
        )
    if not isinstance(authority_readback, Mapping):
        raise ValueError(
            f"{AUTHORITY_UNRESOLVED}: no durable owner/controller readback was "
            f"supplied to bind the grant inventory for {authority_ref}"
        )
    owners = authority_readback.get("owners")
    subject = authority_readback.get("subject")
    if (
        not isinstance(owners, Mapping)
        or any(not isinstance(k, str) or not isinstance(v, str) or not k or not v for k, v in owners.items())
        or not isinstance(subject, str)
        or not _SHA40.fullmatch(subject)
    ):
        raise ValueError(
            f"{AUTHORITY_UNRESOLVED}: authority_readback is not a durable "
            "owner/controller readback (owners mapping + exact 40-hex subject)"
        )
    if not isinstance(authority_fact_readbacks, Mapping):
        raise ValueError(
            f"{AUTHORITY_UNRESOLVED}: no trusted durable-fact readback inventory "
            f"was supplied to bind {authority_ref}"
        )
    fact = authority_fact_readbacks.get(authority_ref)
    if not isinstance(fact, Mapping):
        raise ValueError(
            f"{AUTHORITY_UNRESOLVED}: {authority_ref} has no trusted durable-fact "
            "readback; a caller-made grant inventory never manufactures the "
            "referenced authority fact"
        )
    if fact.get("ref") != authority_ref:
        raise ValueError(
            f"{AUTHORITY_UNRESOLVED}: durable-fact readback identity does not "
            f"bind {authority_ref}"
        )
    if fact.get("exists") is not True:
        raise ValueError(
            f"{AUTHORITY_UNRESOLVED}: {authority_ref} does not resolve to an "
            "existing durable fact (existence/currentness evidence is missing "
            "or negative)"
        )
    digest = fact.get("content_digest")
    if not isinstance(digest, str) or not _SHA256_HEX.fullmatch(digest):
        raise ValueError(
            f"{AUTHORITY_UNRESOLVED}: the durable-fact readback for {authority_ref} "
            "carries no content-addressed binding (64-hex content_digest of the "
            "canonical fact content required)"
        )
    grant = authority_grants.get(authority_ref)
    if not isinstance(grant, Mapping):
        raise ValueError(f"{AUTHORITY_UNRESOLVED}: {authority_ref} resolves to no durable grant")
    if grant.get("ref") != authority_ref:
        raise ValueError(f"{AUTHORITY_UNRESOLVED}: grant identity does not bind {authority_ref}")
    # Authorization is derived from the trusted durable-fact readback only.
    expected_family = NON_DEFAULT_AUTHORITY_FAMILIES.get(role)
    if expected_family is None or fact.get("authority_family") != expected_family:
        raise ValueError(
            f"{AUTHORITY_FAMILY_MISMATCH}: the durable fact behind {authority_ref} "
            f"carries {fact.get('authority_family')!r}, the owning family for role "
            f"{role!r} is {expected_family!r}"
        )
    for field, value in (("repository", repository), ("task", task), ("role", role)):
        if fact.get(field) != value:
            raise ValueError(
                f"{AUTHORITY_NOT_APPLICABLE}: the durable fact behind {authority_ref} "
                f"does not cover {field}={value!r}"
            )
    fact_groups = fact.get("groups")
    if not isinstance(fact_groups, Sequence) or isinstance(fact_groups, str) or group not in fact_groups:
        raise ValueError(
            f"{AUTHORITY_NOT_APPLICABLE}: the durable fact behind {authority_ref} "
            f"does not explicitly authorize compatibility group {group!r}"
        )
    # The caller grant inventory is a projection only: it must equal the
    # fact-readback-derived grant field by field or it manufactures nothing.
    for field, derived_value in (
        ("authority_family", fact.get("authority_family")),
        ("repository", fact.get("repository")),
        ("task", fact.get("task")),
        ("role", fact.get("role")),
        ("groups", list(fact_groups)),
    ):
        observed_value = grant.get(field)
        if isinstance(observed_value, Sequence) and not isinstance(observed_value, str):
            observed_value = list(observed_value)
        if observed_value != derived_value:
            raise ValueError(
                f"{AUTHORITY_GRANT_DRIFT}: grant {authority_ref} field {field!r} is "
                f"{observed_value!r}, but the trusted durable-fact readback derives "
                f"{derived_value!r}; caller-supplied grant fields never manufacture "
                "authority"
            )
    owner_concern = grant.get("owner_concern")
    if not isinstance(owner_concern, str) or owner_concern not in owners:
        raise ValueError(
            f"{AUTHORITY_OWNER_UNRESOLVED}: grant {authority_ref} names "
            f"{owner_concern!r}, which does not resolve through the durable "
            "owner/controller readback"
        )
    if grant.get("readback_subject") != subject:
        raise ValueError(
            f"{AUTHORITY_CURRENTNESS_MISMATCH}: grant {authority_ref} was resolved "
            f"against readback subject {grant.get('readback_subject')!r}, current "
            f"durable subject is {subject!r}"
        )
    return True


def admission_generation_conforms(
    *, reserved_generation: object, claimed_generation: object
) -> str:
    """CAS semantics: reserve g -> g+1, claim requires current, stale fails.

    Returns ``"IDEMPOTENT"`` for a re-presented current generation,
    ``"CLAIMED"`` for the reserved next generation, ``"STALE"`` for a stale
    writer (zero canonical mutation). Malformed/non-integer input raises.
    """
    for value in (reserved_generation, claimed_generation):
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            raise ValueError("admission generations must be non-negative integers")
    if claimed_generation == reserved_generation:
        return "IDEMPOTENT"
    if claimed_generation == reserved_generation + 1:
        return "CLAIMED"
    return "STALE"


def project_active_dispatches(entries: Sequence[Mapping[str, object]]) -> list[dict]:
    """Project the NON_AUTHORITATIVE active_dispatches rows stably.

    Input-only routing fields (repository/task/execution_profile) are used to
    derive the protected claim key and the projected environment but are never
    emitted. Every output row is the contracted W2 schema projection: the
    profile-aware environment (A7/A9; legacy LOCAL_BUILDER/LOCAL_VALIDATOR/
    WEB_REVIEWER project through ``project_dispatch_environment``), the
    normalized compatibility group, the deterministically re-derived claim key,
    nullable claimer, plus exact subject refs when supplied. A persisted
    ``protected_claim_key`` (or scheduler-supplied ``claim_key``) that does not
    match the re-derivation fails closed (B5/B6) instead of being copied.
    """
    rows: list[tuple[str, str, dict]] = []
    for entry in entries:
        if not isinstance(entry, Mapping):
            raise ValueError("active dispatch rows must be mappings")
        dispatch_id = entry.get("dispatch_id")
        role = entry.get("role")
        if not isinstance(dispatch_id, str) or not dispatch_id:
            raise ValueError("active dispatch row missing dispatch_id")
        if role not in {"builder", "validator", "reviewer"}:
            raise ValueError(f"active dispatch row has invalid role: {role!r}")
        repository = entry.get("repository")
        task = entry.get("task")
        if not isinstance(repository, str) or not repository:
            raise ValueError("active dispatch row missing repository")
        if not isinstance(task, str) or not task:
            raise ValueError("active dispatch row missing task")

        # A7/A9: the emitted environment always comes from the profile-aware
        # projection, never from the raw field. The helper-internal UNKNOWN
        # sentinel is emitted as null: the row contract permits WEB|LOCAL|null.
        environment = project_dispatch_environment(entry)
        compatibility_group = normalize_group(entry.get("compatibility_group"))
        claimed_by = entry.get("claimed_by")
        if claimed_by is not None and (
            not isinstance(claimed_by, str) or not claimed_by
        ):
            raise ValueError(f"active dispatch row has invalid claimed_by: {claimed_by!r}")

        key = derive_claim_key(repository, task, str(role), compatibility_group)
        # B5/B6: a persisted key is audit provenance only; it must equal the
        # deterministic re-derivation or the reducer fails closed (a supplied
        # claim_key authority field is rejected outright by the helper).
        if not protected_claim_key_conforms(entry):
            raise ValueError(
                f"active dispatch row {dispatch_id!r} carries a stale, mismatched "
                "or scheduler-supplied protected_claim_key; fail closed (B5/B6)"
            )
        row = {
            "dispatch_id": dispatch_id,
            "role": role,
            "execution_environment": None if environment == "UNKNOWN" else environment,
            "compatibility_group": compatibility_group,
            "protected_claim_key": key,
            "claimed_by": claimed_by,
        }
        for ref_field in ("issue", "pr"):
            ref = entry.get(ref_field)
            if ref is not None and (
                not isinstance(ref, str) or not re.fullmatch(r"#\d+", ref)
            ):
                raise ValueError(
                    f"active dispatch row has invalid exact subject ref {ref_field}: {ref!r}"
                )
            if ref_field in entry:
                row[ref_field] = ref
        rows.append((key, dispatch_id, row))
    rows.sort(key=lambda item: (item[0], item[1]))
    return [item[2] for item in rows]


H2_SINGULAR_PRIMARY_WITH_MULTI_ACTIVE = "H2_SINGULAR_PRIMARY_WITH_MULTI_ACTIVE"
DUPLICATE_ACTIVE_CLAIM_KEY = "DUPLICATE_ACTIVE_CLAIM_KEY"
ACTIVE_DISPATCH_ROW_MALFORMED = "ACTIVE_DISPATCH_ROW_MALFORMED"
# R6 (Fresh Review R5 P2-1): active_dispatches is the projection of THIS work
# item's active dispatches; a row whose derived key carries another
# repository/task is a cross-work-item leak and must be surfaced.
ACTIVE_DISPATCH_FOREIGN_WORK_ITEM = "ACTIVE_DISPATCH_FOREIGN_WORK_ITEM"


def execution_state_projection_problems(state: Mapping[str, object]) -> list[str]:
    """Fail-closed conformance probe for the derived execution-state surface.

    Machine-enforces the derived-state rules the projection boundary owns:
    H2 — when ``active_dispatches`` carries more than one row, the legacy
    singular ``active_dispatch`` / ``active_dispatch_role`` fields MUST be
    null/omitted (no arbitrary primary is projected); #861 machine-model
    rule 2 — two active rows deriving the same protected claim key are
    incompatible and MUST serialize, so canonical active state never presents
    both; and R6 same-work-item safety (Fresh Review R5 P2-1) — every row's
    protected claim key is re-parsed and its derived repository/task MUST equal
    the outer execution-state ``repository``/``work_item``: ``active_dispatches``
    is the projection of this work item's active dispatches, so a row carrying
    another task's key is rejected here (the row contract deliberately drops
    the raw task field, making this probe the owned detection surface).
    Returns the problem codes found; an empty list means conformant.
    Malformed rows fail closed instead of guessing.
    """
    rows = state.get("active_dispatches") or []
    if not isinstance(rows, Sequence) or isinstance(rows, str):
        return [ACTIVE_DISPATCH_ROW_MALFORMED]
    problems: list[str] = []
    keys: list[str] = []
    foreign = False
    for row in rows:
        if (
            not isinstance(row, Mapping)
            or not isinstance(row.get("protected_claim_key"), str)
            or not row["protected_claim_key"]
        ):
            return [ACTIVE_DISPATCH_ROW_MALFORMED]
        key = row["protected_claim_key"]
        try:
            parsed = parse_claim_key(key)
        except (TypeError, ValueError):
            return [ACTIVE_DISPATCH_ROW_MALFORMED]
        if (
            parsed["repository"] != state.get("repository")
            or parsed["task"] != state.get("work_item")
        ):
            foreign = True
        keys.append(key)
    if foreign:
        problems.append(ACTIVE_DISPATCH_FOREIGN_WORK_ITEM)
    if len(rows) > 1:
        if any(state.get(field) is not None for field in ("active_dispatch", "active_dispatch_role")):
            problems.append(H2_SINGULAR_PRIMARY_WITH_MULTI_ACTIVE)
        if len(set(keys)) != len(keys):
            problems.append(DUPLICATE_ACTIVE_CLAIM_KEY)
    return problems


def lineage_refs_present(event: Mapping[str, object], *, current_writer: bool) -> bool:
    """T3: current admission/claim writers carry durable proposal+admission refs.

    ``source_proposal_ref``/``canonical_admission_ref`` must be durable
    ``#<issue>@<comment-id>`` forms; prose references are not durable.
    Historical events (``current_writer=False``) are exempt.
    """
    if not current_writer:
        return True
    for field in ("source_proposal_ref", "canonical_admission_ref"):
        value = event.get(field)
        if not isinstance(value, str) or not re.fullmatch(r"#\d+@\d+", value):
            return False
    return True


def target_environment_agreement(
    *, execution_environment: object, target_environment: object
) -> str:
    """T4: TARGET_ENVIRONMENT is a proposal-era alias; disagreement fails closed.

    Returns the canonical environment. A present-but-disagreeing alias raises
    ValueError instead of guessing.
    """
    canonical = execution_environment if execution_environment in {"WEB", "LOCAL"} else None
    if target_environment is None:
        if canonical is None:
            raise ValueError("execution_environment must be WEB or LOCAL")
        return canonical
    if target_environment not in {"WEB", "LOCAL"}:
        raise ValueError(f"unknown TARGET_ENVIRONMENT alias: {target_environment!r}")
    if canonical is None:
        return target_environment
    if canonical != target_environment:
        raise ValueError(
            f"TARGET_ENVIRONMENT {target_environment!r} disagrees with "
            f"execution_environment {canonical!r}"
        )
    return canonical


def terminal_precedence(actions: Sequence[Mapping[str, object]]) -> dict:
    """T5: accepted canonical terminal facts take precedence over proposals.

    ``actions`` are coordination records with ``kind`` in {"proposal",
    "admission", "claim", "checkpoint", "terminal"} and a ``dispatch_id``.
    The reducer returns the authoritative action: a terminal beats everything
    for its dispatch; canonical admission/claim facts beat proposals and
    checkpoints. Ties resolve deterministically by (kind rank, sequence
    position) — never by count, recency-of-proposal or brand.
    """
    if not actions:
        raise ValueError("no coordination actions to reduce")
    rank = {"terminal": 0, "claim": 1, "admission": 2, "checkpoint": 3, "proposal": 4}
    for index, action in enumerate(actions):
        if not isinstance(action, Mapping) or action.get("kind") not in rank:
            raise ValueError(f"malformed coordination action at {index}")
    best = min(
        enumerate(actions),
        key=lambda pair: (rank[pair[1]["kind"]], pair[0]),
    )
    return dict(best[1])
