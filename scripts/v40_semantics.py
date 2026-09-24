from __future__ import annotations

from typing import Iterable

from v40_rules import (
    canonical_semantic_action_key,
    canonical_semantic_action_payload,
    validate_assurance_aggregation as _legacy_validate_assurance_aggregation,
    validate_assurance_semantics as _legacy_validate_assurance_semantics,
    validate_candidate_release_separation as _legacy_validate_candidate_release_separation,
    validate_finding_disposition as _legacy_validate_finding_disposition,
    validate_review_aggregation as _legacy_validate_review_aggregation,
    validate_subject_identity as _legacy_validate_subject_identity,
    validate_validation_result as _legacy_validate_validation_result,
)
from v40_r2_hardening import (
    fast_path_eligible,
    p3_required_from_plan,
    validate_assurance_aggregation_hardening,
    validate_assurance_plan_hardening,
    validate_candidate_freeze_evidence as _r2_validate_candidate_freeze_evidence,
    validate_execution_state_hardening as _r2_validate_execution_state_hardening,
    validate_hidden_metadata as _r2_validate_hidden_metadata,
    validate_operation_semantics as _r2_validate_operation_semantics,
    validate_release_qualification_event as _r2_validate_release_qualification_event,
    validate_review_aggregation_hardening,
    validate_review_decision_hardening as _r2_validate_review_decision_hardening,
    validate_subject_identity_hardening,
    validate_validation_report as _r2_validate_validation_report,
    validate_validation_result_hardening,
)
from v40_r3_hardening import (
    object_guard,
    validate_dict_sequence,
    validate_hidden_metadata_value_shapes,
    validate_model_diversity_basis,
)
from v40_t010_successor_hardening import (
    validate_blocker_resolution_contract,
    validate_candidate_freeze_sha_format,
    validate_decision_interchange_binding,
    validate_mda_cardinality,
    validate_operation_machine_edges,
    validate_release_freeze_evidence_binding,
    validate_requested_validation_event_identity,
    validate_requested_validation_report_identity,
    validate_validation_activity_execution,
)
from v40_t012_pre_release_hardening import (
    validate_aggregation_judgment,
    validate_assurance_plan_pre_release_hardening,
    validate_mda_declared_bases,
    validate_repository_integration_precondition,
)


def validate_subject_identity(subject: dict) -> list[str]:
    guard = object_guard(subject, label="subject")
    if guard:
        return guard
    return _legacy_validate_subject_identity(subject) + validate_subject_identity_hardening(subject)


def validate_operation_semantics(operation: dict) -> list[str]:
    guard = object_guard(operation, label="Operation")
    if guard:
        return guard
    return _r2_validate_operation_semantics(operation) + validate_operation_machine_edges(operation)


def validate_assurance_semantics(plan: dict) -> list[str]:
    guard = object_guard(plan, label="Assurance Plan")
    if guard:
        return guard
    _, activity_errors = validate_dict_sequence(plan.get("activities", []), label="Assurance Plan activities")
    if activity_errors:
        return activity_errors + validate_assurance_plan_hardening(plan) + validate_assurance_plan_pre_release_hardening(plan)
    return (
        _legacy_validate_assurance_semantics(plan)
        + validate_assurance_plan_hardening(plan)
        + validate_assurance_plan_pre_release_hardening(plan)
    )


def validate_assurance_aggregation(
    plan: dict,
    aggregate: dict,
    findings: Iterable[dict],
) -> list[str]:
    errors: list[str] = []
    errors.extend(object_guard(plan, label="Assurance Plan"))
    errors.extend(object_guard(aggregate, label="review aggregation"))
    normalized_findings, finding_errors = validate_dict_sequence(findings, label="findings")
    errors.extend(finding_errors)
    if errors:
        return errors
    return (
        validate_aggregation_judgment(aggregate)
        + validate_assurance_plan_pre_release_hardening(plan)
        + _legacy_validate_assurance_aggregation(plan, aggregate, normalized_findings)
        + validate_assurance_aggregation_hardening(plan, aggregate)
        + validate_model_diversity_basis(plan, aggregate)
        + validate_mda_cardinality(plan, aggregate)
        + validate_mda_declared_bases(plan, aggregate)
        + validate_validation_activity_execution(plan, aggregate)
    )


def validate_review_aggregation(
    aggregate: dict,
    findings: Iterable[dict],
    *,
    p3_required: bool = False,
    plan: dict | None = None,
) -> list[str]:
    errors = object_guard(aggregate, label="review aggregation")
    normalized_findings, finding_errors = validate_dict_sequence(findings, label="findings")
    errors.extend(finding_errors)
    if plan is not None:
        errors.extend(object_guard(plan, label="Assurance Plan"))
    if errors:
        return errors

    errors.extend(validate_aggregation_judgment(aggregate))
    if plan is not None:
        errors.extend(validate_assurance_plan_pre_release_hardening(plan))
    effective_p3 = p3_required or p3_required_from_plan(plan)
    errors.extend(
        _legacy_validate_review_aggregation(
            aggregate,
            normalized_findings,
            p3_required=effective_p3,
            plan=plan,
        )
    )
    errors.extend(validate_review_aggregation_hardening(aggregate, plan=plan))
    errors.extend(validate_blocker_resolution_contract(aggregate, normalized_findings))
    if plan is not None:
        errors.extend(validate_model_diversity_basis(plan, aggregate))
        errors.extend(validate_mda_cardinality(plan, aggregate))
        errors.extend(validate_mda_declared_bases(plan, aggregate))
        errors.extend(validate_validation_activity_execution(plan, aggregate))
    return errors


def validate_validation_report(report: dict) -> list[str]:
    guard = object_guard(report, label="Validation report")
    if guard:
        return guard
    return _r2_validate_validation_report(report) + validate_requested_validation_report_identity(report)


def validate_validation_result(event: dict) -> list[str]:
    guard = object_guard(event, label="Validation event")
    if guard:
        return guard
    return (
        _legacy_validate_validation_result(event)
        + validate_validation_result_hardening(event)
        + validate_requested_validation_event_identity(event)
    )


def validate_hidden_metadata(metadata: dict) -> list[str]:
    guard = object_guard(metadata, label="hidden metadata")
    if guard:
        return guard
    return _r2_validate_hidden_metadata(metadata) + validate_hidden_metadata_value_shapes(metadata)


def validate_candidate_freeze_evidence(event: dict) -> list[str]:
    guard = object_guard(event, label="Candidate Freeze event")
    if guard:
        return guard
    return _r2_validate_candidate_freeze_evidence(event) + validate_candidate_freeze_sha_format(event)


def validate_execution_state_hardening(state: dict) -> list[str]:
    guard = object_guard(state, label="execution state")
    if guard:
        return guard
    return _r2_validate_execution_state_hardening(state)


def validate_release_qualification_event(event: dict) -> list[str]:
    guard = object_guard(event, label="Release Qualification event")
    if guard:
        return guard
    return _r2_validate_release_qualification_event(event) + validate_release_freeze_evidence_binding(event)


def validate_repository_integration_event(event: dict) -> list[str]:
    guard = object_guard(event, label="Repository Integration event")
    if guard:
        return guard
    return validate_repository_integration_precondition(event)


def validate_review_decision_hardening(event: dict) -> list[str]:
    guard = object_guard(event, label="Review Decision event")
    if guard:
        return guard
    return _r2_validate_review_decision_hardening(event)


def validate_finding_disposition(finding: dict, *, p3_required: bool = False) -> list[str]:
    guard = object_guard(finding, label="finding")
    if guard:
        return guard
    return _legacy_validate_finding_disposition(finding, p3_required=p3_required)


def validate_candidate_release_separation(candidate_event: dict, release_event: dict | None = None) -> list[str]:
    guard = object_guard(candidate_event, label="Candidate event")
    if guard:
        return guard
    if release_event is not None:
        release_guard = object_guard(release_event, label="Release event")
        if release_guard:
            return release_guard
    return _legacy_validate_candidate_release_separation(candidate_event, release_event)


def validate_interchange_semantics(envelope: dict) -> list[str]:
    guard = object_guard(envelope, label="interchange envelope")
    if guard:
        return guard
    return validate_decision_interchange_binding(envelope)


__all__ = [
    "canonical_semantic_action_key",
    "canonical_semantic_action_payload",
    "fast_path_eligible",
    "validate_assurance_aggregation",
    "validate_assurance_semantics",
    "validate_candidate_freeze_evidence",
    "validate_candidate_release_separation",
    "validate_execution_state_hardening",
    "validate_finding_disposition",
    "validate_hidden_metadata",
    "validate_interchange_semantics",
    "validate_operation_semantics",
    "validate_release_qualification_event",
    "validate_repository_integration_event",
    "validate_review_aggregation",
    "validate_review_decision_hardening",
    "validate_subject_identity",
    "validate_validation_report",
    "validate_validation_result",
]
