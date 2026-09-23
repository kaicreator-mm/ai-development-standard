from __future__ import annotations

import hashlib
import json
import re
from typing import Iterable

HEX40 = re.compile(r"^[0-9a-fA-F]{40}$")

FAST_PATH_DISQUALIFIERS = (
    "public_contract_change",
    "architecture_change",
    "security_or_trust_boundary_change",
    "migration_or_recovery_complexity",
    "concurrency_or_exactly_once_complexity",
    "cross_repository_or_authority_coupling",
    "unknown_validation_ownership",
    "unresolved_blocking_finding",
    "model_diverse_or_coherence_assurance_required",
    "nontrivial_execution_pack_required",
    "material_dependency_graph",
)

IDENTITY_REQUIREMENTS = {
    "none": (),
    "exact-sha": ("sha",),
    "validation-tuple": ("tested_sha", "environment", "runtime_toolchain", "validation_profile"),
    "candidate": ("candidate_sha", "tree_sha"),
}


def validate_subject_identity(subject: dict) -> list[str]:
    """Enforce non-weakening identity semantics for Operation subjects."""
    errors: list[str] = []
    binding = subject.get("identity_binding")
    owning = subject.get("owning_required_binding", "none")
    identity = subject.get("identity")
    if not isinstance(identity, dict):
        return ["subject.identity must be an object"]

    required = IDENTITY_REQUIREMENTS.get(owning)
    if required is None:
        return [f"unknown owning_required_binding: {owning!r}"]

    for field in required:
        value = identity.get(field)
        if not isinstance(value, str) or not value:
            errors.append(
                f"identity binding {binding!r} weakens owning {owning!r}: missing {field}"
            )

    if owning in {"exact-sha", "validation-tuple"}:
        sha_field = "sha" if owning == "exact-sha" else "tested_sha"
        value = identity.get(sha_field)
        if isinstance(value, str) and value and not HEX40.fullmatch(value):
            errors.append(f"{sha_field} must be a 40-hex commit SHA")
    if owning == "candidate":
        for sha_field in ("candidate_sha", "tree_sha"):
            value = identity.get(sha_field)
            if isinstance(value, str) and value and not HEX40.fullmatch(value):
                errors.append(f"{sha_field} must be a 40-hex SHA")

    if binding == "project-defined" and owning != "none" and errors:
        errors.append("project-defined identity may extend but never weaken owning identity")
    return errors


def canonical_semantic_action_payload(action: dict) -> dict:
    """Return the stable semantic-action basis; transport/exchange IDs are intentionally excluded."""
    required = (
        "controller_kind",
        "authority_ref",
        "subject_identity",
        "expected_precondition",
        "effect_target",
    )
    missing = [field for field in required if field not in action]
    if missing:
        raise ValueError(f"missing semantic action fields: {', '.join(missing)}")
    return {field: action[field] for field in required}


def canonical_semantic_action_key(action: dict) -> str:
    payload = canonical_semantic_action_payload(action)
    serialized = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def validate_assurance_semantics(plan: dict) -> list[str]:
    errors: list[str] = []
    aggregation = plan.get("aggregation", {})
    if aggregation.get("majority_vote_for_correctness") is not False:
        errors.append("majority voting for correctness is forbidden")
    if aggregation.get("policy") != "finding-union-blocker-dominance":
        errors.append("aggregation must use finding union + blocker dominance")

    seen: set[str] = set()
    for activity in plan.get("activities", []):
        assurance_id = activity.get("assurance_id")
        if assurance_id in seen:
            errors.append(f"duplicate assurance_id: {assurance_id}")
        if assurance_id:
            seen.add(assurance_id)

        mode = activity.get("mode")
        collaboration = activity.get("collaboration_selected")
        blind_ref = activity.get("blind_first_pass_ref")
        independence = activity.get("independence", {})

        if mode == "model-diverse-adversarial":
            if collaboration is True:
                errors.append(
                    f"{assurance_id}: collaborative execution cannot retain model-diverse-adversarial independence label"
                )
            if not isinstance(blind_ref, str) or not blind_ref:
                errors.append(
                    f"{assurance_id}: model-diverse-adversarial activity requires durable blind first pass"
                )
            if independence.get("context") != "required" or independence.get("model") != "required":
                errors.append(
                    f"{assurance_id}: model-diverse-adversarial requires context+model independence"
                )
    return errors


def validate_finding_disposition(finding: dict, *, p3_required: bool = False) -> list[str]:
    errors: list[str] = []
    severity = finding.get("severity")
    status = finding.get("status")
    disposition = finding.get("disposition")
    if severity == "P2":
        if status != "DISPOSITIONED" or not isinstance(disposition, str) or not disposition:
            errors.append("P2 finding requires durable explicit disposition")
    if severity == "P3" and p3_required:
        if status != "DISPOSITIONED" or not isinstance(disposition, str) or not disposition:
            errors.append("P3 finding requires durable explicit disposition when policy requires it")
    if status == "DUPLICATE" and not finding.get("duplicate_of"):
        errors.append("duplicate finding must preserve duplicate_of identity")
    return errors


def validate_review_aggregation(
    aggregate: dict,
    findings: Iterable[dict],
    *,
    p3_required: bool = False,
) -> list[str]:
    errors: list[str] = []
    findings = list(findings)
    by_id = {f.get("finding_id"): f for f in findings if f.get("finding_id")}
    refs = aggregate.get("finding_refs", [])
    missing = sorted(set(by_id) - set(refs))
    if missing:
        errors.append("aggregation silently dropped finding identities: " + ", ".join(missing))

    unresolved_blockers = [
        f["finding_id"]
        for f in findings
        if f.get("finding_id")
        and f.get("blocking") is True
        and f.get("status") not in {"DISPOSITIONED", "SUPERSEDED"}
    ]
    if unresolved_blockers and aggregate.get("judgment") == "PASS":
        errors.append("PASS forbidden while unresolved valid blocker exists")

    declared = set(aggregate.get("unresolved_blocker_refs", []))
    missing_blockers = sorted(set(unresolved_blockers) - declared)
    if missing_blockers:
        errors.append("unresolved blockers missing from aggregate: " + ", ".join(missing_blockers))

    for finding in findings:
        errors.extend(validate_finding_disposition(finding, p3_required=p3_required))
    return errors


def fast_path_eligible(context: dict) -> bool:
    if context.get("scope_bounded") is not True:
        return False
    if context.get("validation_ownership_known") is not True:
        return False
    if context.get("review_policy_resolved") is not True:
        return False
    return not any(context.get(flag) is True for flag in FAST_PATH_DISQUALIFIERS)


def validate_validation_result(event: dict) -> list[str]:
    """v4 semantic guard over the backwards-compatible event-v2 wire shape."""
    errors: list[str] = []
    if event.get("event") != "VALIDATION_RESULT":
        return errors
    if event.get("status") == "PASS":
        if event.get("exit_code") != 0:
            errors.append("Validation PASS requires successful executed command (exit_code=0)")
        for field in ("sha", "command", "evidence", "gate", "environment"):
            if not event.get(field):
                errors.append(f"Validation PASS missing execution evidence field: {field}")
        drift = event.get("drift")
        if drift in {"HEAD_DRIFT", "BASE_DRIFT", "MERGE-RESULT_DRIFT", "CANDIDATE_DRIFT"}:
            errors.append("drifted validation evidence cannot be PASS")
    return errors


def validate_candidate_release_separation(candidate_event: dict, release_event: dict | None = None) -> list[str]:
    errors: list[str] = []
    if candidate_event.get("event") == "CANDIDATE_STATE_CHANGED":
        if candidate_event.get("candidate_state") == "FROZEN":
            for field in ("candidate_sha", "tree_sha", "candidate_ref", "visible_closure_evidence"):
                if not candidate_event.get(field):
                    errors.append(f"frozen candidate missing {field}")
    if release_event is not None and release_event.get("event") == "RELEASE_QUALIFICATION":
        if release_event.get("release_state") == "READY":
            if release_event.get("candidate_sha") != candidate_event.get("candidate_sha"):
                errors.append("release READY candidate identity differs from frozen candidate")
            if release_event.get("tree_sha") != candidate_event.get("tree_sha"):
                errors.append("release READY tree identity differs from frozen candidate")
    return errors


def validate_hidden_metadata(metadata: dict) -> list[str]:
    errors: list[str] = []
    for field in ("pack_identity", "pack_revision", "pack_checksum", "candidate_sha"):
        value = metadata.get(field)
        if not isinstance(value, str) or not value:
            errors.append(f"hidden metadata missing canonical {field}")
    forbidden = ("fixture", "scenario_payload", "oracle_payload", "packet_payload")
    for field in forbidden:
        if field in metadata:
            errors.append(f"hidden private payload must not appear in shared metadata: {field}")
    return errors
