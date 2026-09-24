from __future__ import annotations

import re

HEX40 = re.compile(r"^[0-9a-fA-F]{40}$")
DURABLE_REF = re.compile(
    r"^(?:issue:#\d+|pr:#\d+|actions:[^\s]+|evidence:[^\s]+|file:[^\s]+|ref:[^\s]+|sha:[0-9a-fA-F]{40}|version:#\d+)$"
)
JUDGMENTS = {"PASS", "CHANGES_REQUESTED", "VALIDATION_REQUESTED", "BLOCKED"}
MDA_BASES = {
    "provider-diverse",
    "model-family-diverse",
    "architecture-system-diverse",
    "project-approved-different-configuration",
}


def _nonempty(value) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _hex40(value) -> bool:
    return isinstance(value, str) and HEX40.fullmatch(value) is not None


def _durable_ref(value) -> bool:
    return isinstance(value, str) and DURABLE_REF.fullmatch(value) is not None


def _provenances(result: dict, *, composite: bool) -> list[dict]:
    if composite:
        many = result.get("reviewer_provenances")
        if isinstance(many, list) and many:
            return [item for item in many if isinstance(item, dict)]
    one = result.get("reviewer_provenance")
    return [one] if isinstance(one, dict) else []


def validate_assurance_plan_pre_release_hardening(plan: dict) -> list[str]:
    errors: list[str] = []
    if not isinstance(plan, dict):
        return ["Assurance Plan must be an object"]

    binding = plan.get("identity_binding")
    identity_ref = plan.get("subject_identity_ref")
    if binding == "exact-sha":
        if not isinstance(identity_ref, str) or not identity_ref.startswith("sha:") or not _hex40(identity_ref[4:]):
            errors.append("exact-sha Assurance Plan requires subject_identity_ref=sha:<40-hex>")

    activities = plan.get("activities")
    if not isinstance(activities, list):
        return errors + ["Assurance Plan activities must be a list"]

    ids: list[str] = []
    for index, activity in enumerate(activities):
        if not isinstance(activity, dict):
            continue
        assurance_id = activity.get("assurance_id")
        if not _nonempty(assurance_id):
            errors.append(f"Assurance Plan activity[{index}] requires assurance_id")
            continue
        ids.append(assurance_id)
    duplicates = sorted({item for item in ids if ids.count(item) > 1})
    if duplicates:
        errors.append("Assurance Plan assurance_id values must be unique: " + ", ".join(duplicates))

    declared = set(ids)
    graph: dict[str, list[str]] = {}
    for activity in activities:
        if not isinstance(activity, dict) or not _nonempty(activity.get("assurance_id")):
            continue
        assurance_id = activity["assurance_id"]
        deps = activity.get("depends_on", [])
        if not isinstance(deps, list):
            errors.append(f"{assurance_id}: depends_on must be a list")
            continue
        normalized: list[str] = []
        for dep in deps:
            if not _nonempty(dep):
                errors.append(f"{assurance_id}: depends_on entries must be non-empty assurance IDs")
                continue
            normalized.append(dep)
            if dep not in declared:
                errors.append(f"{assurance_id}: depends_on references unknown assurance activity {dep}")
        graph[assurance_id] = normalized

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str) -> None:
        if node in visited:
            return
        if node in visiting:
            errors.append("Assurance Plan depends_on graph must be acyclic")
            return
        visiting.add(node)
        for dep in graph.get(node, []):
            if dep in graph:
                visit(dep)
        visiting.remove(node)
        visited.add(node)

    for node in graph:
        visit(node)
    return errors


def validate_aggregation_judgment(aggregate: dict) -> list[str]:
    if not isinstance(aggregate, dict):
        return ["review aggregation must be an object"]
    judgment = aggregate.get("judgment")
    if judgment not in JUDGMENTS:
        return [f"review aggregation judgment must be one of {sorted(JUDGMENTS)}"]
    return []


def validate_mda_declared_bases(plan: dict, aggregate: dict) -> list[str]:
    errors: list[str] = []
    if not isinstance(plan, dict) or not isinstance(aggregate, dict):
        return errors
    if aggregate.get("judgment") != "PASS":
        return errors

    results = {
        item.get("assurance_id"): item
        for item in aggregate.get("activity_results", [])
        if isinstance(item, dict) and _nonempty(item.get("assurance_id"))
    }
    activities = [
        item
        for item in plan.get("activities", [])
        if isinstance(item, dict)
        and item.get("policy") == "required"
        and item.get("mode") == "model-diverse-adversarial"
    ]
    if not activities:
        return errors

    composite = len(activities) == 1
    basis_records: dict[str, list[dict]] = {basis: [] for basis in MDA_BASES}
    for activity in activities:
        assurance_id = activity.get("assurance_id")
        basis = activity.get("model_diversity_basis")
        if basis not in MDA_BASES:
            errors.append(f"{assurance_id}: unsupported model_diversity_basis")
            continue
        result = results.get(assurance_id)
        if not isinstance(result, dict):
            errors.append(f"{assurance_id}: required MDA result missing")
            continue
        records = _provenances(result, composite=composite)
        if composite and len(records) < 2:
            errors.append(f"{assurance_id}: single-composite MDA requires at least two reviewer provenances")
        basis_records[basis].extend(records)

    declared_bases = {
        item.get("model_diversity_basis")
        for item in activities
        if item.get("model_diversity_basis") in MDA_BASES
    }
    for basis in declared_bases:
        records = basis_records[basis]
        if len(records) < 2:
            errors.append(f"{basis}: MDA PASS requires at least two provenance records")
            continue
        model_ids = [item.get("model_id") for item in records]
        if not all(_nonempty(value) for value in model_ids) or len(set(model_ids)) < 2:
            errors.append(f"{basis}: MDA PASS requires at least two distinct model IDs")
        if basis == "provider-diverse":
            values = [item.get("provider") for item in records]
            label = "providers"
        elif basis == "model-family-diverse":
            values = [item.get("model_family") for item in records]
            label = "model families"
        elif basis == "architecture-system-diverse":
            values = [item.get("architecture_system") for item in records]
            label = "architecture systems"
        else:
            values = [item.get("configuration_fingerprint") for item in records]
            label = "configuration fingerprints"
        if not all(_nonempty(value) for value in values):
            errors.append(f"{basis}: MDA PASS requires complete {label} provenance")
        elif len(set(values)) < 2:
            errors.append(f"{basis}: MDA PASS requires distinct {label}")
    return errors


def validate_repository_integration_precondition(event: dict) -> list[str]:
    errors: list[str] = []
    if not isinstance(event, dict):
        return ["Repository Integration event must be an object"]
    if event.get("event") != "REPOSITORY_INTEGRATION_RESULT":
        return errors

    candidate_sha = event.get("candidate_sha")
    tree_sha = event.get("tree_sha")
    if not _hex40(candidate_sha) or not _hex40(tree_sha):
        errors.append("Repository Integration requires exact candidate SHA/tree")
    if not _durable_ref(event.get("release_qualification_ref")):
        errors.append("Repository Integration requires durable release_qualification_ref")
    if event.get("release_qualification_state") not in {"READY", "CONDITIONAL"}:
        errors.append("Repository Integration requires authorized Release READY or CONDITIONAL precondition")
    expected = f"candidate:{candidate_sha}:{tree_sha}"
    if event.get("release_candidate_identity") != expected:
        errors.append("Repository Integration release_candidate_identity must bind the same frozen candidate SHA/tree")
    return errors
