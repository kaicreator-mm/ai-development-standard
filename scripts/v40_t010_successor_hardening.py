from __future__ import annotations

import re
from typing import Iterable

HEX40 = re.compile(r"^[0-9a-fA-F]{40}$")
DURABLE_REF = re.compile(
    r"^(?:issue:#\d+|pr:#\d+|actions:[^\s]+|evidence:[^\s]+|file:[^\s]+|ref:[^\s]+|sha:[0-9a-fA-F]{40}|version:#\d+)$"
)
PROJECT_OPERATION_TYPE = re.compile(r"^[a-z][a-z0-9-]*:[a-z][a-z0-9-]*$")
NEXT_OPERATION_EDGE = re.compile(r"^op:[A-Za-z0-9._:/-]+\|work-item:#\d+$")

CORE_OPERATION_TYPES = {
    "product-evidence",
    "product-definition",
    "architecture-research",
    "architecture-definition",
    "task-decomposition",
    "task-materialization",
    "implementation",
    "integration",
    "review",
    "validation",
    "coherence-review",
    "candidate-freeze",
    "hidden-validation",
    "release-qualification",
    "repository-integration",
}

BLOCKER_TERMINAL_CODES = {"FIXED", "INVALIDATED_BY_EVIDENCE"}
VERDICTIVE_RELEASE_STATES = {"READY", "CONDITIONAL", "BLOCKED", "FAIL"}


def _nonempty(value) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _hex40(value) -> bool:
    return isinstance(value, str) and HEX40.fullmatch(value) is not None


def _durable_ref(value) -> bool:
    return isinstance(value, str) and DURABLE_REF.fullmatch(value) is not None


def _nonempty_durable_refs(value) -> bool:
    return isinstance(value, list) and bool(value) and all(_durable_ref(item) for item in value)


def _is_blocker(finding: dict) -> bool:
    return finding.get("severity") in {"P0", "P1"} or finding.get("blocking") is True


def _preserves_blocker(source: dict, target: dict) -> bool:
    source_severity = source.get("severity")
    target_severity = target.get("severity")
    if source_severity == "P0":
        return target_severity == "P0" and target.get("blocking") is True
    if source_severity == "P1":
        return target_severity in {"P0", "P1"} and target.get("blocking") is True
    if source.get("blocking") is True:
        return _is_blocker(target)
    return True


def validate_blocker_resolution_contract(aggregate: dict, findings: Iterable[dict]) -> list[str]:
    """Fail closed on anonymous findings and free-text blocker waivers.

    P0/P1 resolution is machine state, not prose. DISPOSITIONED blockers require a
    bounded terminal code. DUPLICATE/SUPERSEDED must point to a same-subject blocker
    target that is itself effectively resolved; links cannot waive severity.
    """
    errors: list[str] = []
    findings = list(findings)
    for index, finding in enumerate(findings):
        finding_id = finding.get("finding_id") if isinstance(finding, dict) else None
        if not _nonempty(finding_id):
            errors.append(f"finding[{index}] requires non-empty finding_id before aggregation")

    by_id = {
        finding["finding_id"]: finding
        for finding in findings
        if isinstance(finding, dict) and _nonempty(finding.get("finding_id"))
    }

    memo: dict[str, bool] = {}
    visiting: set[str] = set()

    def resolved(finding_id: str) -> bool:
        if finding_id in memo:
            return memo[finding_id]
        if finding_id in visiting:
            return False
        finding = by_id.get(finding_id)
        if finding is None:
            return False
        visiting.add(finding_id)
        status = finding.get("status")
        code = finding.get("resolution_code")
        evidence_ok = _nonempty_durable_refs(finding.get("evidence_refs"))
        result = False
        if status == "DISPOSITIONED":
            result = code in BLOCKER_TERMINAL_CODES and evidence_ok
        elif status in {"DUPLICATE", "SUPERSEDED"}:
            target_field = "duplicate_of" if status == "DUPLICATE" else "superseded_by"
            required_code = "DUPLICATE" if status == "DUPLICATE" else "SUPERSEDED"
            target_id = finding.get(target_field)
            target = by_id.get(target_id)
            result = (
                code == required_code
                and evidence_ok
                and isinstance(target_id, str)
                and target_id != finding_id
                and target is not None
                and target.get("subject_identity_ref") == finding.get("subject_identity_ref")
                and _preserves_blocker(finding, target)
                and resolved(target_id)
            )
        visiting.remove(finding_id)
        memo[finding_id] = result
        return result

    unresolved: list[str] = []
    for finding_id, finding in by_id.items():
        if not _is_blocker(finding):
            continue
        status = finding.get("status")
        if status == "DISPOSITIONED" and finding.get("resolution_code") not in BLOCKER_TERMINAL_CODES:
            errors.append(
                f"{finding_id}: blocker DISPOSITIONED requires resolution_code FIXED or INVALIDATED_BY_EVIDENCE"
            )
        if status == "DUPLICATE" and finding.get("resolution_code") != "DUPLICATE":
            errors.append(f"{finding_id}: blocker duplicate requires resolution_code DUPLICATE")
        if status == "SUPERSEDED" and finding.get("resolution_code") != "SUPERSEDED":
            errors.append(f"{finding_id}: blocker supersession requires resolution_code SUPERSEDED")
        if not resolved(finding_id):
            unresolved.append(finding_id)

    if aggregate.get("judgment") == "PASS" and unresolved:
        errors.append(
            "PASS forbidden while blocker lacks machine-authorized resolution: "
            + ", ".join(sorted(unresolved))
        )
    return errors


def _provenance_records(result: dict) -> list[dict]:
    many = result.get("reviewer_provenances")
    if isinstance(many, list) and many:
        return [item for item in many if isinstance(item, dict)]
    one = result.get("reviewer_provenance")
    return [one] if isinstance(one, dict) else []


def validate_mda_cardinality(plan: dict, aggregate: dict) -> list[str]:
    """A model-diverse activity must prove at least two material reviewer systems.

    Multiple required MDA activities may each contribute one provenance. A single
    composite MDA activity must carry `reviewer_provenances` with at least two
    records. This closes the one-reviewer-labelled-model-diverse false PASS class.
    """
    errors: list[str] = []
    if aggregate.get("judgment") != "PASS":
        return errors
    activities = [
        activity
        for activity in plan.get("activities", [])
        if isinstance(activity, dict)
        and activity.get("policy") == "required"
        and activity.get("mode") == "model-diverse-adversarial"
    ]
    if not activities:
        return errors
    result_by_id = {
        result.get("assurance_id"): result
        for result in aggregate.get("activity_results", [])
        if isinstance(result, dict) and _nonempty(result.get("assurance_id"))
    }
    all_provenance: list[dict] = []
    for activity in activities:
        assurance_id = activity.get("assurance_id")
        result = result_by_id.get(assurance_id)
        if not isinstance(result, dict):
            errors.append(f"{assurance_id}: required MDA result missing")
            continue
        records = _provenance_records(result)
        if len(activities) == 1 and len(records) < 2:
            errors.append(
                f"{assurance_id}: single model-diverse activity requires at least two durable reviewer provenances"
            )
        if not records:
            errors.append(f"{assurance_id}: MDA result requires reviewer provenance")
        all_provenance.extend(records)
    if len(all_provenance) < 2:
        errors.append("PASS model-diverse assurance requires at least two reviewer provenances")
        return errors
    providers = {p.get("provider") for p in all_provenance if _nonempty(p.get("provider"))}
    model_ids = {p.get("model_id") for p in all_provenance if _nonempty(p.get("model_id"))}
    bases = {a.get("model_diversity_basis") for a in activities}
    if "provider-diverse" in bases and len(providers) < 2:
        errors.append("provider-diverse MDA PASS requires at least two distinct providers")
    if len(model_ids) < 2:
        errors.append("model-diverse MDA PASS requires at least two distinct model IDs")
    return errors


def validate_validation_activity_execution(plan: dict, aggregate: dict) -> list[str]:
    """Bind required Validation assurance PASS to an executable validation tuple."""
    errors: list[str] = []
    if aggregate.get("judgment") != "PASS":
        return errors
    activities = {
        activity.get("assurance_id"): activity
        for activity in plan.get("activities", [])
        if isinstance(activity, dict) and _nonempty(activity.get("assurance_id"))
    }
    result_by_id = {
        result.get("assurance_id"): result
        for result in aggregate.get("activity_results", [])
        if isinstance(result, dict) and _nonempty(result.get("assurance_id"))
    }
    for assurance_id, activity in activities.items():
        if activity.get("policy") != "required" or activity.get("kind") != "validation":
            continue
        result = result_by_id.get(assurance_id)
        if not isinstance(result, dict):
            errors.append(f"{assurance_id}: required Validation result missing")
            continue
        if result.get("result_state") != "PASS":
            continue
        if result.get("result_kind") != "validation-execution":
            errors.append(f"{assurance_id}: Validation PASS requires result_kind=validation-execution")
        execution = result.get("validation_execution")
        if not isinstance(execution, dict):
            errors.append(f"{assurance_id}: Validation PASS requires validation_execution tuple")
            continue
        required_strings = (
            "requested_sha",
            "tested_sha",
            "actual_checked_out_sha",
            "environment",
            "runtime_toolchain",
            "validation_profile",
            "command",
        )
        for field in required_strings:
            if not _nonempty(execution.get(field)):
                errors.append(f"{assurance_id}: validation_execution missing {field}")
        requested = execution.get("requested_sha")
        tested = execution.get("tested_sha")
        checked = execution.get("actual_checked_out_sha")
        if not (_hex40(requested) and _hex40(tested) and _hex40(checked)):
            errors.append(f"{assurance_id}: Validation execution SHA tuple must be exact 40-hex")
        elif not (requested == tested == checked):
            errors.append(f"{assurance_id}: requested/tested/checked-out Validation SHA must match exactly")
        if execution.get("provider_state") != "AVAILABLE":
            errors.append(f"{assurance_id}: Validation PASS requires provider_state=AVAILABLE")
        if execution.get("working_tree_clean") is not True:
            errors.append(f"{assurance_id}: Validation PASS requires clean working tree")
        if execution.get("source_modifications_after_validation") is not False:
            errors.append(f"{assurance_id}: Validation PASS forbids source modifications after validation")
        if type(execution.get("exit_code")) is not int or execution.get("exit_code") != 0:
            errors.append(f"{assurance_id}: Validation PASS requires integer exit_code=0")
        if execution.get("drift") is not None:
            errors.append(f"{assurance_id}: Validation PASS cannot coexist with drift")
        identity_ref = result.get("result_identity_ref")
        if _hex40(tested) and identity_ref != f"sha:{tested}":
            errors.append(f"{assurance_id}: Validation result identity must bind tested SHA")
    return errors


def validate_requested_validation_report_identity(report: dict) -> list[str]:
    errors: list[str] = []
    if report.get("state") != "PASS":
        return errors
    requested = report.get("requested_sha")
    tested = report.get("tested_sha")
    if not _hex40(requested):
        errors.append("Validation report PASS requires exact requested_sha")
    elif requested != tested:
        errors.append("Validation report PASS requested_sha must equal tested_sha")
    return errors


def validate_requested_validation_event_identity(event: dict) -> list[str]:
    errors: list[str] = []
    if event.get("event") != "VALIDATION_RESULT" or event.get("status") != "PASS":
        return errors
    requested = event.get("requested_head_sha")
    sha = event.get("sha")
    if not _hex40(requested):
        errors.append("Validation PASS requires exact requested_head_sha")
    elif requested != sha:
        errors.append("Validation PASS requested_head_sha must equal sha")
    return errors


def validate_release_freeze_evidence_binding(event: dict) -> list[str]:
    errors: list[str] = []
    if event.get("event") != "RELEASE_QUALIFICATION" or event.get("release_state") not in VERDICTIVE_RELEASE_STATES:
        return errors
    candidate_sha = event.get("candidate_sha")
    tree_sha = event.get("tree_sha")
    if not _durable_ref(event.get("candidate_freeze_ref")):
        errors.append("verdictive Release Qualification requires durable candidate_freeze_ref")
    expected = f"candidate:{candidate_sha}:{tree_sha}"
    if event.get("candidate_freeze_identity") != expected:
        errors.append("verdictive Release Qualification candidate_freeze_identity must bind exact candidate SHA/tree")
    if not _durable_ref(event.get("visible_closure_evidence_ref")):
        errors.append("verdictive Release Qualification requires durable visible_closure_evidence_ref")
    return errors


def validate_candidate_freeze_sha_format(event: dict) -> list[str]:
    errors: list[str] = []
    if event.get("event") == "CANDIDATE_STATE_CHANGED" and event.get("candidate_state") == "FROZEN":
        if not _hex40(event.get("candidate_sha")):
            errors.append("FROZEN candidate requires exact 40-hex candidate_sha")
        if not _hex40(event.get("tree_sha")):
            errors.append("FROZEN candidate requires exact 40-hex tree_sha")
    return errors


def validate_operation_machine_edges(operation: dict) -> list[str]:
    """Harden authority/type/successor metadata without creating a second DAG."""
    errors: list[str] = []
    operation_type = operation.get("operation_type")
    if operation_type not in CORE_OPERATION_TYPES:
        if not isinstance(operation_type, str) or PROJECT_OPERATION_TYPE.fullmatch(operation_type) is None:
            errors.append("operation_type must be canonical core type or project-namespaced type")
    if not _durable_ref(operation.get("authority_ref")):
        errors.append("Operation authority_ref must be a durable authority reference")
    actor = operation.get("actor_contract")
    actor_authority = actor.get("authority_ref") if isinstance(actor, dict) else None
    if not _durable_ref(actor_authority):
        errors.append("actor_contract.authority_ref must be a durable authority reference")
    next_operations = operation.get("next_operations", [])
    if not isinstance(next_operations, list):
        errors.append("next_operations must be a list")
    else:
        for edge in next_operations:
            if not isinstance(edge, str) or NEXT_OPERATION_EDGE.fullmatch(edge) is None:
                errors.append(
                    "next_operations entries must bind successor Operation correlation to owning Work Item as op:<id>|work-item:#N"
                )
    return errors


def validate_decision_interchange_binding(envelope: dict) -> list[str]:
    errors: list[str] = []
    if envelope.get("exchange_type") != "DECISION":
        return errors
    actor = envelope.get("actor") if isinstance(envelope.get("actor"), dict) else {}
    role = actor.get("actor_role")
    payload_class = envelope.get("payload_class")
    if role == "release-controller" and payload_class != "release-decision":
        errors.append("release-controller DECISION requires payload_class=release-decision")
    elif role == "human-authority" and payload_class != "authority-decision":
        errors.append("human-authority DECISION requires payload_class=authority-decision")
    elif role not in {"release-controller", "human-authority"}:
        errors.append("DECISION interchange requires authority-bearing release-controller or human-authority role")
    return errors
