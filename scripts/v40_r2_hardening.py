from __future__ import annotations

import re
from typing import Iterable

HEX40 = re.compile(r"^[0-9a-fA-F]{40}$")
DURABLE_REF = re.compile(r"^(?:issue:#\d+|pr:#\d+|actions:[^\s]+|evidence:[^\s]+|file:[^\s]+|ref:[^\s]+|sha:[0-9a-fA-F]{40})$")

FAST_PATH_REQUIRED = {
    "scope_bounded",
    "validation_ownership_known",
    "review_policy_resolved",
}
FAST_PATH_DISQUALIFIERS = {
    "public_contract_change",
    "architecture_change",
    "security_or_trust_boundary_change",
    "migration_or_recovery_complexity",
    "concurrency_or_exactly_once_complexity",
    "cross_repository_or_authority_coupling",
    "unknown_validation_ownership",
    "unresolved_blocking_finding",
    "unresolved_authority_contradiction",
    "model_diverse_or_coherence_assurance_required",
    "nontrivial_execution_pack_required",
    "material_dependency_graph",
}

OPERATION_KIND_BY_TYPE = {
    "product-evidence": "RESEARCH",
    "product-definition": "PRODUCE",
    "architecture-research": "RESEARCH",
    "architecture-definition": "PRODUCE",
    "task-decomposition": "PRODUCE",
    "task-materialization": "CONTROL",
    "implementation": "PRODUCE",
    "integration": "PRODUCE",
    "review": "ASSURE",
    "validation": "ASSURE",
    "coherence-review": "ASSURE",
    "candidate-freeze": "CONTROL",
    "hidden-validation": "ASSURE",
    "release-qualification": "DECIDE",
    "repository-integration": "CONTROL",
}

MIN_BINDING_BY_TYPE = {
    "review": "exact-sha",
    "validation": "validation-tuple",
    "candidate-freeze": "candidate",
    "hidden-validation": "candidate",
    "release-qualification": "candidate",
    "repository-integration": "candidate",
}

BINDING_COMPATIBILITY = {
    "none": {"exact-sha", "validation-tuple", "candidate", "project-defined"},
    "exact-sha": {"exact-sha", "project-defined"},
    "validation-tuple": {"validation-tuple", "project-defined"},
    "candidate": {"candidate", "project-defined"},
}

VERDICTIVE_RELEASE_STATES = {"READY", "CONDITIONAL", "BLOCKED", "FAIL"}
VALID_DRIFT = {"HEAD_DRIFT", "BASE_DRIFT", "MERGE-RESULT_DRIFT", "CANDIDATE_DRIFT"}
HIDDEN_PUBLIC_METADATA_KEYS = {
    "pack_identity",
    "pack_revision",
    "pack_checksum",
    "candidate_sha",
    "coverage_digest",
    "leak_check",
    "evaluator_ref",
    "evidence_ref",
    "occurred_at",
}


def _nonempty(value) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _hex40(value) -> bool:
    return isinstance(value, str) and HEX40.fullmatch(value) is not None


def _durable_ref(value) -> bool:
    return isinstance(value, str) and DURABLE_REF.fullmatch(value) is not None


def validate_fast_path_context(context: dict) -> list[str]:
    errors: list[str] = []
    if not isinstance(context, dict):
        return ["Fast Path context must be an object"]
    allowed = FAST_PATH_REQUIRED | FAST_PATH_DISQUALIFIERS
    unknown = sorted(set(context) - allowed)
    if unknown:
        errors.append("Fast Path context contains unknown keys: " + ", ".join(unknown))
    missing = sorted(allowed - set(context))
    if missing:
        errors.append("Fast Path context must declare every closed-world predicate: " + ", ".join(missing))
    for key in allowed:
        if key in context and type(context[key]) is not bool:
            errors.append(f"Fast Path predicate {key} must be boolean")
    for key in FAST_PATH_REQUIRED:
        if context.get(key) is not True:
            errors.append(f"Fast Path required predicate is not true: {key}")
    for key in FAST_PATH_DISQUALIFIERS:
        if context.get(key) is True:
            errors.append(f"Fast Path disqualified by: {key}")
    return errors


def fast_path_eligible(context: dict) -> bool:
    return not validate_fast_path_context(context)


def validate_subject_identity_hardening(subject: dict, *, operation_type: str | None = None) -> list[str]:
    errors: list[str] = []
    if not isinstance(subject, dict):
        return ["subject must be an object"]
    binding = subject.get("identity_binding")
    owning = subject.get("owning_required_binding")
    if owning not in BINDING_COMPATIBILITY:
        errors.append(f"unknown owning_required_binding: {owning!r}")
    elif binding not in BINDING_COMPATIBILITY[owning]:
        errors.append(f"identity_binding {binding!r} is weaker/incompatible with owning binding {owning!r}")
    required = MIN_BINDING_BY_TYPE.get(operation_type or "")
    if required is not None and owning != required:
        errors.append(f"operation_type {operation_type} requires owning_required_binding={required}")
    return errors


def validate_operation_semantics(operation: dict) -> list[str]:
    errors: list[str] = []
    if not isinstance(operation, dict):
        return ["Operation must be an object"]
    operation_type = operation.get("operation_type")
    operation_kind = operation.get("operation_kind")
    expected_kind = OPERATION_KIND_BY_TYPE.get(operation_type)
    if expected_kind is not None and operation_kind != expected_kind:
        errors.append(f"operation_type {operation_type} requires operation_kind={expected_kind}")
    if operation.get("operation_binding_authority") != "CORRELATION_ONLY_NON_AUTHORITATIVE":
        errors.append("Operation binding authority marker is required and must remain non-authoritative")
    if operation_kind in {"ASSURE", "DECIDE"} and not _durable_ref(operation.get("assurance_plan_ref")):
        errors.append(f"{operation_kind} Operation requires durable assurance_plan_ref")
    if operation_kind == "DECIDE" and not _nonempty(operation.get("work_item_ref")):
        errors.append("DECIDE Operation requires durable work_item_ref")
    authority_ref = operation.get("authority_ref")
    operation_id = operation.get("operation_id")
    actor_authority = (operation.get("actor_contract") or {}).get("authority_ref")
    if authority_ref == operation_id or actor_authority == operation_id:
        errors.append("Operation cannot manufacture self-authority from operation_id")
    errors.extend(validate_subject_identity_hardening(operation.get("subject", {}), operation_type=operation_type))
    return errors


def validate_assurance_plan_hardening(plan: dict) -> list[str]:
    errors: list[str] = []
    if plan.get("identity_binding") not in {"exact-sha", "validation-tuple", "candidate", "project-defined"}:
        errors.append("Assurance Plan requires explicit identity_binding")
    if plan.get("finding_disposition_policy") not in {"p2-explicit-p3-optional", "p2-and-p3-explicit"}:
        errors.append("Assurance Plan requires finding_disposition_policy")
    for activity in plan.get("activities", []):
        if not isinstance(activity, dict):
            errors.append("Assurance activity must be an object")
            continue
        if activity.get("mode") == "model-diverse-adversarial":
            if activity.get("model_diversity_basis") not in {
                "provider-diverse",
                "model-family-diverse",
                "architecture-system-diverse",
                "project-approved-different-configuration",
            }:
                errors.append(f"{activity.get('assurance_id')}: MDA activity requires explicit model_diversity_basis")
            if not _durable_ref(activity.get("independence_basis_ref")):
                errors.append(f"{activity.get('assurance_id')}: MDA activity requires durable independence_basis_ref")
    return errors


def validate_assurance_aggregation_hardening(plan: dict, aggregate: dict) -> list[str]:
    errors: list[str] = []
    if not isinstance(plan, dict):
        return ["PASS aggregation requires an Assurance Plan"]
    results = aggregate.get("activity_results")
    if aggregate.get("judgment") == "PASS" and (not isinstance(results, list) or not results):
        errors.append("PASS aggregation requires non-empty activity_results")
        return errors
    activities = {
        a.get("assurance_id"): a
        for a in plan.get("activities", [])
        if isinstance(a, dict) and _nonempty(a.get("assurance_id"))
    }
    mda_provenance: list[tuple[str, str]] = []
    for result in results or []:
        assurance_id = result.get("assurance_id") if isinstance(result, dict) else None
        activity = activities.get(assurance_id)
        if not isinstance(result, dict):
            errors.append("activity result must be an object")
            continue
        if aggregate.get("judgment") == "PASS" and result.get("result_state") != "PASS":
            errors.append(f"{assurance_id}: aggregate PASS requires result_state=PASS")
        if result.get("result_identity_ref") != aggregate.get("subject_identity_ref"):
            errors.append(f"{assurance_id}: result_identity_ref differs from aggregate subject")
        if not _durable_ref(result.get("result_ref")):
            errors.append(f"{assurance_id}: result_ref must be a durable resolvable reference")
        if activity and activity.get("mode") == "model-diverse-adversarial":
            provenance = result.get("reviewer_provenance")
            if not isinstance(provenance, dict):
                errors.append(f"{assurance_id}: MDA result requires reviewer_provenance")
                continue
            for field in ("provider", "model_family", "model_id", "executor_id", "context_ref", "blind_first_pass_ref"):
                if not _nonempty(provenance.get(field)):
                    errors.append(f"{assurance_id}: reviewer_provenance missing {field}")
            if _nonempty(provenance.get("provider")) and _nonempty(provenance.get("model_family")):
                mda_provenance.append((provenance["provider"], provenance["model_family"]))
    required_mda = [
        a for a in activities.values()
        if a.get("policy") == "required" and a.get("mode") == "model-diverse-adversarial"
    ]
    if aggregate.get("judgment") == "PASS" and len(required_mda) >= 2:
        if len(set(mda_provenance)) < 2:
            errors.append("PASS MDA aggregation requires materially diverse provider/model-family provenance")
    return errors


def validate_review_aggregation_hardening(aggregate: dict, *, plan: dict | None = None) -> list[str]:
    errors: list[str] = []
    judgment = aggregate.get("judgment")
    route = aggregate.get("requested_route")
    allowed_routes = {
        "PASS": {"none", "review-ready", "merge-ready"},
        "CHANGES_REQUESTED": {"changes-requested"},
        "VALIDATION_REQUESTED": {"validation-needed"},
        "BLOCKED": {"blocked"},
    }
    if judgment in allowed_routes and route not in allowed_routes[judgment]:
        errors.append(f"review judgment {judgment} is incompatible with requested_route {route}")
    if judgment == "PASS" and plan is None:
        errors.append("PASS review aggregation requires owning Assurance Plan")
    if plan is not None:
        errors.extend(validate_assurance_aggregation_hardening(plan, aggregate))
    return errors


def validate_validation_report(report: dict) -> list[str]:
    errors: list[str] = []
    if report.get("state") != "PASS":
        return errors
    required = (
        "tested_sha",
        "actual_checked_out_sha",
        "working_tree_clean",
        "source_modifications_after_validation",
        "provider_state",
        "execution_host_role",
        "platform",
        "runtime_toolchain",
        "validation_profile",
        "command",
        "exit_code",
    )
    for field in required:
        if field not in report or report.get(field) is None:
            errors.append(f"Validation report PASS missing required execution/identity field: {field}")
    if not _hex40(report.get("tested_sha")):
        errors.append("Validation report PASS requires 40-hex tested_sha")
    if not _hex40(report.get("actual_checked_out_sha")):
        errors.append("Validation report PASS requires 40-hex actual_checked_out_sha")
    elif report.get("actual_checked_out_sha") != report.get("tested_sha"):
        errors.append("Validation report PASS actual_checked_out_sha must equal tested_sha")
    if report.get("working_tree_clean") is not True:
        errors.append("Validation report PASS requires clean working tree")
    if report.get("source_modifications_after_validation") is not False:
        errors.append("Validation report PASS forbids source modifications after validation")
    if report.get("provider_state") != "AVAILABLE":
        errors.append("Validation report PASS requires provider_state=AVAILABLE")
    if report.get("drift") is not None:
        errors.append("Validation report PASS cannot coexist with drift")
    if type(report.get("exit_code")) is not int or report.get("exit_code") != 0:
        errors.append("Validation report PASS requires integer exit_code=0")
    return errors


def validate_validation_result_hardening(event: dict) -> list[str]:
    errors: list[str] = []
    if event.get("event") != "VALIDATION_RESULT" or event.get("status") != "PASS":
        return errors
    if type(event.get("exit_code")) is not int or event.get("exit_code") != 0:
        errors.append("Validation PASS requires integer exit_code=0")
    sha = event.get("sha")
    if not _hex40(sha):
        errors.append("Validation PASS requires exact 40-hex sha")
    if event.get("drift") is not None:
        errors.append("Validation PASS cannot carry any drift token")
    for field in ("gate", "environment", "command", "evidence", "validation_profile", "actual_checked_out_sha"):
        if not _nonempty(event.get(field)):
            errors.append(f"Validation PASS missing exact tuple field: {field}")
    checked = event.get("actual_checked_out_sha")
    if checked is not None and (not _hex40(checked) or checked != sha):
        errors.append("Validation PASS actual_checked_out_sha must equal sha")
    current_head = event.get("current_pr_head")
    if current_head is not None and (not _hex40(current_head) or current_head != sha):
        errors.append("Validation PASS current_pr_head mismatch requires drift/non-PASS handling")
    provider_state = event.get("provider_state")
    if provider_state is not None and provider_state != "AVAILABLE":
        errors.append("Validation PASS cannot coexist with non-AVAILABLE provider_state")
    return errors


def validate_hidden_metadata(metadata: dict) -> list[str]:
    errors: list[str] = []
    if not isinstance(metadata, dict):
        return ["hidden metadata must be an object"]
    required = {"pack_identity", "pack_revision", "pack_checksum", "candidate_sha"}
    missing = sorted(required - set(metadata))
    if missing:
        errors.append("hidden metadata missing canonical fields: " + ", ".join(missing))
    unknown = sorted(set(metadata) - HIDDEN_PUBLIC_METADATA_KEYS)
    if unknown:
        errors.append("hidden shared metadata contains non-public field(s): " + ", ".join(unknown))
    if "candidate_sha" in metadata and not _hex40(metadata.get("candidate_sha")):
        errors.append("hidden metadata candidate_sha must be exact 40-hex")
    return errors


def validate_execution_state_hardening(state: dict) -> list[str]:
    errors: list[str] = []
    if state.get("release_state") in VERDICTIVE_RELEASE_STATES and state.get("candidate_state") != "FROZEN":
        errors.append("verdictive release_state requires candidate_state=FROZEN")
    return errors


def validate_release_qualification_event(event: dict) -> list[str]:
    errors: list[str] = []
    if event.get("event") != "RELEASE_QUALIFICATION":
        return errors
    if event.get("release_state") in VERDICTIVE_RELEASE_STATES:
        if event.get("candidate_state") != "FROZEN":
            errors.append("verdictive RELEASE_QUALIFICATION requires candidate_state=FROZEN")
        if not _nonempty(event.get("candidate_ref")):
            errors.append("verdictive RELEASE_QUALIFICATION requires candidate_ref")
        if not _hex40(event.get("candidate_sha")) or not _hex40(event.get("tree_sha")):
            errors.append("verdictive RELEASE_QUALIFICATION requires exact candidate/tree identity")
    return errors


def validate_candidate_freeze_evidence(event: dict) -> list[str]:
    errors: list[str] = []
    if event.get("event") != "CANDIDATE_STATE_CHANGED" or event.get("candidate_state") != "FROZEN":
        return errors
    evidence_ref = event.get("visible_closure_evidence")
    if not _durable_ref(evidence_ref):
        errors.append("FROZEN candidate requires durable visible_closure_evidence ref")
    expected_identity = f"candidate:{event.get('candidate_sha')}:{event.get('tree_sha')}"
    if event.get("visible_closure_evidence_identity") != expected_identity:
        errors.append("FROZEN candidate closure evidence must bind exact candidate SHA/tree")
    return errors


def validate_review_decision_hardening(event: dict) -> list[str]:
    errors: list[str] = []
    if event.get("event") == "REVIEW_DECISION" and event.get("review_policy") == "recommended" and event.get("decision") == "skipped":
        if not _nonempty(event.get("policy_basis")):
            errors.append("recommended review skip requires durable policy_basis")
    return errors


def p3_required_from_plan(plan: dict | None) -> bool:
    return bool(plan and plan.get("finding_disposition_policy") == "p2-and-p3-explicit")
