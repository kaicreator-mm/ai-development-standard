from __future__ import annotations

from typing import Iterable

from v40_rules import (
    canonical_semantic_action_key,
    canonical_semantic_action_payload,
    validate_assurance_aggregation as _legacy_validate_assurance_aggregation,
    validate_assurance_semantics as _legacy_validate_assurance_semantics,
    validate_candidate_release_separation,
    validate_finding_disposition,
    validate_review_aggregation as _legacy_validate_review_aggregation,
    validate_subject_identity as _legacy_validate_subject_identity,
    validate_validation_result as _legacy_validate_validation_result,
)
from v40_r2_hardening import (
    fast_path_eligible,
    p3_required_from_plan,
    validate_assurance_aggregation_hardening,
    validate_assurance_plan_hardening,
    validate_candidate_freeze_evidence,
    validate_execution_state_hardening,
    validate_hidden_metadata,
    validate_operation_semantics,
    validate_release_qualification_event,
    validate_review_aggregation_hardening,
    validate_review_decision_hardening,
    validate_subject_identity_hardening,
    validate_validation_report,
    validate_validation_result_hardening,
)


def validate_subject_identity(subject: dict) -> list[str]:
    return _legacy_validate_subject_identity(subject) + validate_subject_identity_hardening(subject)


def validate_assurance_semantics(plan: dict) -> list[str]:
    return _legacy_validate_assurance_semantics(plan) + validate_assurance_plan_hardening(plan)


def validate_assurance_aggregation(
    plan: dict,
    aggregate: dict,
    findings: Iterable[dict],
) -> list[str]:
    findings = list(findings)
    return _legacy_validate_assurance_aggregation(plan, aggregate, findings) + validate_assurance_aggregation_hardening(plan, aggregate)


def validate_review_aggregation(
    aggregate: dict,
    findings: Iterable[dict],
    *,
    p3_required: bool = False,
    plan: dict | None = None,
) -> list[str]:
    findings = list(findings)
    effective_p3 = p3_required or p3_required_from_plan(plan)
    errors = _legacy_validate_review_aggregation(
        aggregate,
        findings,
        p3_required=effective_p3,
        plan=plan,
    )
    errors.extend(validate_review_aggregation_hardening(aggregate, plan=plan))
    return errors


def validate_validation_result(event: dict) -> list[str]:
    return _legacy_validate_validation_result(event) + validate_validation_result_hardening(event)


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
    "validate_operation_semantics",
    "validate_release_qualification_event",
    "validate_review_aggregation",
    "validate_review_decision_hardening",
    "validate_subject_identity",
    "validate_validation_report",
    "validate_validation_result",
]
