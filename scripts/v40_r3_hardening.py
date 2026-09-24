from __future__ import annotations

from typing import Iterable


MDA_BASES = {
    "provider-diverse",
    "model-family-diverse",
    "architecture-system-diverse",
    "project-approved-different-configuration",
}

HIDDEN_STRING_FIELDS = {
    "pack_identity",
    "pack_revision",
    "pack_checksum",
    "coverage_digest",
    "leak_check",
    "evaluator_ref",
    "evidence_ref",
    "occurred_at",
}


def _nonempty_string(value) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _required_mda_activities(plan: dict) -> list[dict]:
    activities = plan.get("activities", []) if isinstance(plan, dict) else []
    return [
        activity
        for activity in activities
        if isinstance(activity, dict)
        and activity.get("policy") == "required"
        and activity.get("mode") == "model-diverse-adversarial"
    ]


def validate_model_diversity_basis(plan: dict, aggregate: dict) -> list[str]:
    """Honor the Assurance Plan's declared model-diversity basis for PASS aggregation.

    R2 already requires complete reviewer provenance. R3 makes the declared basis
    operational instead of treating any distinct provider/family pair as sufficient.
    This remains a risk-control check; it is never correctness or Validation evidence.
    """
    errors: list[str] = []
    if not isinstance(plan, dict):
        return ["model-diversity check requires an Assurance Plan object"]
    if not isinstance(aggregate, dict):
        return ["model-diversity check requires an aggregation object"]
    if aggregate.get("judgment") != "PASS":
        return errors

    required_mda = _required_mda_activities(plan)
    if len(required_mda) < 2:
        # A single composite MDA activity remains compatible with the frozen v4
        # logical contract. When multiple blind lanes are materialized, their
        # declared basis must be machine-enforced below.
        return errors

    result_by_id = {
        result.get("assurance_id"): result
        for result in aggregate.get("activity_results", [])
        if isinstance(result, dict) and _nonempty_string(result.get("assurance_id"))
    }

    provenances: list[dict] = []
    bases: set[str] = set()
    for activity in required_mda:
        assurance_id = activity.get("assurance_id")
        basis = activity.get("model_diversity_basis")
        if basis not in MDA_BASES:
            errors.append(f"{assurance_id}: unknown model_diversity_basis for PASS")
            continue
        bases.add(basis)
        result = result_by_id.get(assurance_id)
        if not isinstance(result, dict):
            errors.append(f"{assurance_id}: required MDA result missing from PASS aggregate")
            continue
        provenance = result.get("reviewer_provenance")
        if not isinstance(provenance, dict):
            errors.append(f"{assurance_id}: required MDA result missing reviewer_provenance")
            continue
        provenances.append(provenance)

    if len(provenances) < 2:
        errors.append("PASS model-diverse review requires at least two durable blind reviewer provenances")
        return errors

    # Exact repeated provenance is never material diversity.
    signatures = [
        (
            p.get("provider"),
            p.get("model_family"),
            p.get("model_id"),
            p.get("executor_id"),
            p.get("context_ref"),
            p.get("blind_first_pass_ref"),
        )
        for p in provenances
    ]
    if len(set(signatures)) < len(signatures):
        errors.append("PASS MDA aggregation contains duplicated reviewer provenance")

    providers = {p.get("provider") for p in provenances if _nonempty_string(p.get("provider"))}
    families = {p.get("model_family") for p in provenances if _nonempty_string(p.get("model_family"))}
    model_ids = {p.get("model_id") for p in provenances if _nonempty_string(p.get("model_id"))}

    if "provider-diverse" in bases:
        if len(providers) < 2:
            errors.append("provider-diverse MDA PASS requires at least two distinct providers")
        if len(model_ids) < 2:
            errors.append("provider-diverse MDA PASS rejects same-model reuse disguised by labels")

    if "model-family-diverse" in bases:
        if len(families) < 2:
            errors.append("model-family-diverse MDA PASS requires at least two distinct model families")
        if len(model_ids) < 2:
            errors.append("model-family-diverse MDA PASS rejects identical model_id reuse")

    if "architecture-system-diverse" in bases:
        systems = [p.get("architecture_system") for p in provenances]
        if not all(_nonempty_string(value) for value in systems):
            errors.append("architecture-system-diverse MDA PASS requires architecture_system provenance")
        elif len(set(systems)) < 2:
            errors.append("architecture-system-diverse MDA PASS requires distinct architecture systems")

    if "project-approved-different-configuration" in bases:
        configs = [p.get("configuration_fingerprint") for p in provenances]
        if not all(_nonempty_string(value) for value in configs):
            errors.append("configuration-diverse MDA PASS requires configuration_fingerprint provenance")
        elif len(set(configs)) < 2:
            errors.append("configuration-diverse MDA PASS requires distinct configuration fingerprints")

    return errors


def validate_hidden_metadata_value_shapes(metadata: dict) -> list[str]:
    """Prevent private structured payloads from hiding under public-safe key names."""
    errors: list[str] = []
    if not isinstance(metadata, dict):
        return ["hidden metadata must be an object"]
    for field in HIDDEN_STRING_FIELDS:
        if field in metadata and not _nonempty_string(metadata.get(field)):
            errors.append(f"hidden shared metadata field {field} must be a non-empty public scalar string")
    return errors


def validate_dict_sequence(value, *, label: str) -> tuple[list[dict], list[str]]:
    """Normalize a reachable semantic collection to structured fail-closed errors."""
    if value is None:
        return [], [f"{label} must be an iterable of objects"]
    if isinstance(value, (str, bytes, dict)):
        return [], [f"{label} must be an iterable of objects"]
    try:
        items = list(value)
    except TypeError:
        return [], [f"{label} must be an iterable of objects"]
    errors = [f"{label}[{index}] must be an object" for index, item in enumerate(items) if not isinstance(item, dict)]
    return [item for item in items if isinstance(item, dict)], errors


def object_guard(value, *, label: str) -> list[str]:
    return [] if isinstance(value, dict) else [f"{label} must be an object"]
