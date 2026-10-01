#!/usr/bin/env python3
"""v4.7 T07 unified semantic conformance.

This module is an executable conformance oracle over already-owned v4.7
metadata, standards, Task authority and historical compatibility surfaces.
It never grants mutation, Validation, Review, Release or Version Closure
authority and it does not create a new lifecycle/Gate state.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from copy import deepcopy
import json
import subprocess
import sys
from typing import Iterable, Mapping, Sequence

ROOT = Path(__file__).resolve().parents[1]

T07_TASK_PACK = "docs/implementation/4.7.0/task-packs/T07_unified_semantic_conformance.md"
T07_WRITE_SET = frozenset(
    {
        "references/V47_SEMANTIC_CONFORMANCE_MATRIX.md",
        "scripts/test_v47_semantic_conformance.py",
        "scripts/v47_conformance.py",
    }
)

DEPENDENCY_TEST_SCRIPTS = (
    "scripts/test_v47_convergence_metadata_contracts.py",
    "scripts/test_v47_authority_registry.py",
    "scripts/test_v47_state_dimension_registry.py",
    "scripts/test_v47_reference_conventions.py",
    "scripts/test_v47_progressive_disclosure.py",
    "scripts/test_v47_compatibility_aliases.py",
)

RUNTIME_OWNER_REF = (
    "github:kaicreator-mm/ai-development-standard@"
    "c9ee9249999aa5463ce880bc7674b732979009b3:"
    "standards/OBSERVABILITY_RUNTIME_EVIDENCE_STANDARD.md"
)

STATE_RULE_EXPECTATIONS: Mapping[str, tuple[str, str, str, str]] = {
    "F01_TASK_DONE_NOT_VALIDATION_PASS": (
        "work_item_workflow", "state:done", "validation_gate", "PASS"
    ),
    "F02_REVIEW_PASS_NOT_VALIDATION_PASS": (
        "review_judgment", "PASS", "validation_gate", "PASS"
    ),
    "F03_VALIDATION_PASS_NOT_RELEASE_READY": (
        "validation_gate", "PASS", "release_qualification", "READY"
    ),
    "F04_RELEASE_READY_NOT_DEPLOYMENT_SUCCESS": (
        "release_qualification", "READY", "deployment_result", "DEPLOYMENT_SUCCEEDED"
    ),
    "F05_DEPLOYMENT_SUCCESS_NOT_RUNTIME_HEALTH": (
        "deployment_result", "DEPLOYMENT_SUCCEEDED", "runtime_health",
        "runtime-health-established"
    ),
    "F06_RUNNER_AVAILABLE_NOT_MUTATION_AUTHORITY": (
        "runner_capability", "observed-or-declared-AVAILABLE", "work_item_workflow",
        "task-mutation-authorized"
    ),
    "F07_OLD_SHA_VALIDATION_NOT_SUCCESSOR_PASS": (
        "validation_gate", "PASS@original-exact-SHA", "validation_gate",
        "PASS@successor-exact-SHA"
    ),
    "F08_SANDBOX_PASS_NOT_REAL_ENV_PASS": (
        "validation_gate", "PASS@sandbox-tuple", "validation_gate",
        "PASS@unexecuted-real-environment-tuple"
    ),
    "F09_DISPATCH_COMPLETED_NOT_RELEASE_READY": (
        "dispatch_lifecycle", "COMPLETED", "release_qualification", "READY"
    ),
    "F10_PACK_CURRENT_NOT_VALIDATION_PASS": (
        "execution_pack_currentness", "PACK_CURRENT", "validation_gate", "PASS"
    ),
}

# Frozen Product v4.7 §6 is the canonical authority for these identities. This
# executable catalog is only a conformance surface and MUST stay set-equal to
# the owner-derived §6 set below; it does not become a second Product owner.
FROZEN_PRODUCT_NEGATIVE_COUNT = 21
FROZEN_PRODUCT_SECTION6_HEADING = "## 6. Required forbidden inferences"
FROZEN_PRODUCT_NEGATIVES = (
    "Task DONE -> Validation PASS",
    "Review PASS -> Validation PASS",
    "Validation PASS -> Release READY",
    "PR merged -> Release READY",
    "Release READY -> Deployment SUCCESS",
    "Deployment SUCCESS -> Runtime Healthy",
    "Dispatch COMPLETED -> product/release PASS",
    "PACK_CURRENT -> implementation correct",
    "old exact-SHA PASS -> successor exact-SHA PASS",
    "provider/tool/credential AVAILABLE -> mutation authority",
    "waiver/exception -> PASS",
    "fresh DB/install PASS -> upgrade PASS",
    "wire/schema compatible -> behavior/source/consumer compatible",
    "mock/sandbox PASS -> higher-fidelity PASS",
    "artifact alias/tag -> immutable artifact identity",
    "incident RECOVERED -> permanent fix/follow-up closed",
    "branch/package exists -> maintenance-supported",
    "Skill installed/capable -> trusted/authorized",
    "Intent/Assumption record -> Frozen Product authority",
    "historical chat/memory -> current durable authority",
    "technical necessity -> Task Pack write authority",
)


@dataclass(frozen=True)
class EvidenceTuple:
    """Identity tuple used only to test non-transfer.

    Equality is deliberately strict. Owning Validation/Review/Release contracts
    decide whether evidence is required or sufficient; this helper only proves
    that materially different tuples are not silently treated as identical.
    """

    exact_sha: str
    environment: str
    profile: str
    evidence_kind: str = "validation"


def evidence_applies_to(source: EvidenceTuple, target: EvidenceTuple) -> bool:
    """Return True only for the exact same evidence tuple."""
    return source == target


def _load_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def parse_allowed_write_set(task_pack_text: str) -> tuple[str, ...]:
    """Extract the Frozen Task Pack allowed_write_set without YAML dependencies."""
    lines = task_pack_text.splitlines()
    start = next(
        (index for index, line in enumerate(lines) if line.strip() == "allowed_write_set:"),
        None,
    )
    if start is None:
        raise ValueError("Task Pack missing allowed_write_set")
    paths: list[str] = []
    for raw in lines[start + 1 :]:
        if raw.startswith("  - "):
            paths.append(raw[4:].strip())
            continue
        if raw and not raw.startswith((" ", "\t")):
            break
    if not paths or len(paths) != len(set(paths)):
        raise ValueError("Task Pack allowed_write_set is empty or duplicated")
    return tuple(paths)


def mutation_authorized_by_task_pack(
    task_pack_text: str, requested_paths: Iterable[str]
) -> bool:
    """Check file mutation only against Task Pack write authority.

    Registry presence, owner discovery, tool/provider capability and test/CI
    outcomes are intentionally not inputs to this function.
    """
    allowed = set(parse_allowed_write_set(task_pack_text))
    requested = set(requested_paths)
    return bool(requested) and requested.issubset(allowed)


def manifest_conformance_errors(root: Path, manifest: dict) -> list[str]:
    """Cross-check owner uniqueness and compatibility routing without owning it."""
    errors: list[str] = []
    sections = manifest.get("sections")
    if not isinstance(sections, dict):
        return ["U01: missing manifest sections"]
    normative = sections.get("normative_standards")
    compatibility = sections.get("compatibility_entries")
    if not isinstance(normative, list) or not isinstance(compatibility, list):
        return ["U01: malformed normative/compatibility inventory"]
    if len(normative) != len(set(normative)):
        errors.append("U01: duplicate normative owner path")
    if len(compatibility) != len(set(compatibility)):
        errors.append("U01: duplicate compatibility path")
    if set(normative) & set(compatibility):
        errors.append("U01: compatibility alias promoted to normative owner")

    semantic = manifest.get("semantic_authorities")
    if semantic is None:
        # Historical manifests remain readable, but cannot prove current v4.7
        # semantic owner/alias conformance.
        return errors + ["U01: current semantic_authorities registry missing"]
    if not isinstance(semantic, dict) or semantic.get("schema_version") != 1:
        return errors + ["U01: malformed semantic_authorities envelope"]
    entries = semantic.get("entries")
    if not isinstance(entries, list) or not entries:
        return errors + ["U01: semantic_authorities entries missing"]

    concerns: set[str] = set()
    entry_ids: set[str] = set()
    aliases: set[str] = set()
    for entry in entries:
        if not isinstance(entry, dict):
            errors.append("U01: semantic entry is not an object")
            continue
        concern = entry.get("semantic_concern")
        entry_id = entry.get("entry_id")
        owner = entry.get("canonical_owner_ref")
        if concern in concerns:
            errors.append(f"U01: competing canonical owner for {concern}")
        concerns.add(concern)
        if entry_id in entry_ids:
            errors.append(f"U01: duplicate semantic entry id {entry_id}")
        entry_ids.add(entry_id)
        if owner not in normative:
            errors.append(f"U01: owner is not canonical normative inventory: {owner}")
        elif not (root / owner).is_file():
            errors.append(f"U01: canonical owner path absent: {owner}")
        for alias in entry.get("compatibility_alias_refs", []):
            if alias not in compatibility:
                errors.append(f"U06: alias absent from compatibility inventory: {alias}")
            if alias in normative or alias == owner:
                errors.append(f"U06: alias became/equals normative owner: {alias}")
            if alias in aliases:
                errors.append(f"U06: alias claimed by multiple entries: {alias}")
            aliases.add(alias)
            if not (root / alias).is_file():
                errors.append(f"U06: compatibility path absent: {alias}")

    # T06 currently requires every compatibility entry to have one registry route.
    if aliases != set(compatibility):
        errors.append("U06: compatibility inventory and semantic alias routes differ")
    return errors


def state_registry_conformance_errors(registry: dict) -> list[str]:
    """Check qualified dimensions and exact T03 forbidden-inference identities."""
    errors: list[str] = []
    dimensions = registry.get("dimensions")
    rules = registry.get("forbidden_inferences")
    if not isinstance(dimensions, list) or not isinstance(rules, list):
        return ["U03: malformed state registry"]

    by_dimension: dict[str, dict] = {}
    for dimension in dimensions:
        if not isinstance(dimension, dict):
            errors.append("U03: dimension is not an object")
            continue
        dimension_id = dimension.get("dimension_id")
        if dimension_id in by_dimension:
            errors.append(f"U03: duplicate dimension {dimension_id}")
        by_dimension[dimension_id] = dimension
        if not dimension.get("canonical_owner_ref"):
            errors.append(f"U03: unqualified dimension {dimension_id}")
        for forbidden_field in ("current_state", "transition", "mutation_authorized"):
            if forbidden_field in dimension:
                errors.append(f"U03: live state/authority field on {dimension_id}: {forbidden_field}")

    runtime = by_dimension.get("runtime_health", {})
    if runtime.get("canonical_owner_ref") != RUNTIME_OWNER_REF:
        errors.append("U03: runtime_health is not pinned to corrected merged v4.5 owner")

    by_rule: dict[str, dict] = {}
    for rule in rules:
        if not isinstance(rule, dict):
            errors.append("U03: forbidden-inference rule is not an object")
            continue
        rule_id = rule.get("rule_id")
        if rule_id in by_rule:
            errors.append(f"U03: duplicate forbidden-inference rule {rule_id}")
        by_rule[rule_id] = rule
        if rule.get("source_dimension_ref") not in by_dimension:
            errors.append(f"U03: unresolved source dimension for {rule_id}")
        if rule.get("target_dimension_ref") not in by_dimension:
            errors.append(f"U03: unresolved target dimension for {rule_id}")

    for rule_id, expected in STATE_RULE_EXPECTATIONS.items():
        rule = by_rule.get(rule_id)
        if rule is None:
            errors.append(f"U03: missing required rule {rule_id}")
            continue
        actual = (
            rule.get("source_dimension_ref"),
            rule.get("source_fact_ref"),
            rule.get("target_dimension_ref"),
            rule.get("prohibited_conclusion_ref"),
        )
        if actual != expected:
            errors.append(f"U03: {rule_id} changed semantic identity: {actual!r}")
    return errors


def parse_frozen_product_section6_negatives(prd_text: str) -> tuple[str, ...]:
    """Read the authoritative forbidden-inference identities from Frozen Product §6."""
    lines = prd_text.splitlines()
    try:
        heading_index = lines.index(FROZEN_PRODUCT_SECTION6_HEADING)
    except ValueError as exc:
        raise ValueError("Frozen Product §6 heading missing") from exc

    section_end = next(
        (
            index
            for index in range(heading_index + 1, len(lines))
            if lines[index].startswith("## ")
        ),
        None,
    )
    if section_end is None:
        raise ValueError("Frozen Product §6 next section boundary missing")

    section_lines = lines[heading_index + 1 : section_end]
    fence_start = next(
        (
            index
            for index, line in enumerate(section_lines)
            if line.strip() == "```text"
        ),
        None,
    )
    if fence_start is None:
        raise ValueError("Frozen Product §6 text fence missing")
    fence_end = next(
        (
            index
            for index in range(fence_start + 1, len(section_lines))
            if section_lines[index].strip() == "```"
        ),
        None,
    )
    if fence_end is None:
        raise ValueError("Frozen Product §6 text fence is unterminated")

    negatives = tuple(
        line.strip()
        for line in section_lines[fence_start + 1 : fence_end]
        if line.strip()
    )
    if not negatives:
        raise ValueError("Frozen Product §6 forbidden-inference set is empty")
    if len(negatives) != len(set(negatives)):
        raise ValueError("Frozen Product §6 forbidden-inference set contains duplicates")
    return negatives


def frozen_product_conformance_errors(prd_text: str) -> list[str]:
    errors: list[str] = []
    try:
        product_negatives = parse_frozen_product_section6_negatives(prd_text)
    except ValueError as exc:
        return [f"U08: {exc}"]

    if len(product_negatives) != FROZEN_PRODUCT_NEGATIVE_COUNT:
        errors.append(
            "U08: Frozen Product §6 negative cardinality drift: "
            f"expected {FROZEN_PRODUCT_NEGATIVE_COUNT}, got {len(product_negatives)}"
        )
    if len(FROZEN_PRODUCT_NEGATIVES) != FROZEN_PRODUCT_NEGATIVE_COUNT:
        errors.append(
            "U08: Frozen Product executable negative catalog cardinality drift: "
            f"expected {FROZEN_PRODUCT_NEGATIVE_COUNT}, "
            f"got {len(FROZEN_PRODUCT_NEGATIVES)}"
        )
    if len(set(FROZEN_PRODUCT_NEGATIVES)) != len(FROZEN_PRODUCT_NEGATIVES):
        errors.append("U08: Frozen Product executable negative catalog contains duplicates")

    product_set = set(product_negatives)
    executable_set = set(FROZEN_PRODUCT_NEGATIVES)
    for negative in sorted(product_set - executable_set):
        errors.append(
            "U08: Product §6 required negative missing from executable catalog: "
            f"{negative}"
        )
    for negative in sorted(executable_set - product_set):
        errors.append(
            "U08: executable negative absent from Product §6 authority: "
            f"{negative}"
        )
    return errors


def reference_conformance_errors(reference_standard: str) -> list[str]:
    required = (
        "old exact-SHA PASS -> successor exact-SHA PASS",
        "capability_ref != authority_ref",
        "evidence_ref present != mutation authorized",
        "provenance_ref present != normative owner",
        "MUST NOT substitute for an exact SHA",
    )
    return [
        f"U04: reference convention missing: {token}"
        for token in required
        if token not in reference_standard
    ]


def routing_conformance_errors(root: Path) -> list[str]:
    """Assert T05 keeps profiles/overrides derived and fail-closed."""
    resolver = (root / "scripts/resolve_standard_read_set.py").read_text(encoding="utf-8")
    template = (
        root / "templates/project/.dev-standard/PROJECT_OVERRIDES.md"
    ).read_text(encoding="utf-8")
    required_resolver = (
        'PROFILE_KEYS = {"language_profile_ref", "archetype_profile_ref"}',
        "CONFLICTING_PROJECT_OVERRIDE",
        "DUPLICATE_PROJECT_OVERRIDE",
        "MUTATION_AUTHORITY_NOT_PROVEN",
        "EXACT_SUBJECT_DRIFT",
        '"mutation_authorized": False',
    )
    required_template = (
        "Project overrides **MUST NOT weaken**",
        "Exact-SHA/current-subject binding remains mandatory",
        "PR PASS != Release PASS",
    )
    errors = [
        f"U05: progressive resolver contract missing: {token}"
        for token in required_resolver
        if token not in resolver
    ]
    errors.extend(
        f"U05: PROJECT_OVERRIDES non-weakening contract missing: {token}"
        for token in required_template
        if token not in template
    )
    return errors


def historical_manifest_compatible(manifest: dict) -> bool:
    """Legacy `sections` remain consumable without optional semantic metadata."""
    historical = deepcopy(manifest)
    historical.pop("semantic_authorities", None)
    sections = historical.get("sections")
    return (
        historical.get("schema_version") == 1
        and isinstance(sections, dict)
        and isinstance(sections.get("normative_standards"), list)
        and isinstance(sections.get("compatibility_entries"), list)
    )


def current_repo_conformance_errors(root: Path = ROOT) -> list[str]:
    """Run deterministic repository semantic checks; no external/live claims."""
    manifest = _load_json(root / "standard-manifest.json")
    state_registry = _load_json(root / "registries/state-dimensions-v1.json")
    task_pack = (root / T07_TASK_PACK).read_text(encoding="utf-8")
    prd = (root / "docs/implementation/4.7.0/PRD.md").read_text(encoding="utf-8")
    reference_standard = (
        root / "standards/REFERENCE_CONVENTION_STANDARD.md"
    ).read_text(encoding="utf-8")

    errors: list[str] = []
    errors.extend(manifest_conformance_errors(root, manifest))
    errors.extend(state_registry_conformance_errors(state_registry))
    errors.extend(frozen_product_conformance_errors(prd))
    errors.extend(reference_conformance_errors(reference_standard))
    errors.extend(routing_conformance_errors(root))

    try:
        actual_write_set = frozenset(parse_allowed_write_set(task_pack))
    except ValueError as exc:
        errors.append(f"U02: {exc}")
    else:
        if actual_write_set != T07_WRITE_SET:
            errors.append(
                f"U02: T07 write-set drift: expected {sorted(T07_WRITE_SET)}, "
                f"got {sorted(actual_write_set)}"
            )
        if mutation_authorized_by_task_pack(
            task_pack, ["standards/DEVELOPMENT_WORKFLOW.md"]
        ):
            errors.append("U02: canonical owner discovery incorrectly grants mutation")
        if not mutation_authorized_by_task_pack(task_pack, T07_WRITE_SET):
            errors.append("U02: Frozen T07 write-set is not recognized exactly")

    if not historical_manifest_compatible(manifest):
        errors.append("U06: historical sections-only manifest compatibility lost")
    return errors


def run_dependency_suites(
    root: Path = ROOT, scripts: Sequence[str] = DEPENDENCY_TEST_SCRIPTS
) -> dict[str, int]:
    """Execute T01-T06 focused suites as composition evidence."""
    results: dict[str, int] = {}
    for relative in scripts:
        process = subprocess.run(
            [sys.executable, str(root / relative)],
            cwd=root,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=60,
        )
        results[relative] = process.returncode
        if process.returncode:
            # Keep the precise dependency identity visible without promoting this
            # runner into Validation/Review authority.
            sys.stderr.write(f"[{relative}]\n{process.stdout}\n")
    return results


def main() -> int:
    errors = current_repo_conformance_errors(ROOT)
    dependency_results = run_dependency_suites(ROOT)
    payload = {
        "ok": not errors and all(code == 0 for code in dependency_results.values()),
        "authority_effect": "NONE",
        "gate_effect": "NONE",
        "errors": errors,
        "dependency_test_exit_codes": dependency_results,
        "note": (
            "Ordinary deterministic test evidence only; integration Validation, "
            "Fresh Independent Review, Release Qualification and Version Closure "
            "remain separately owned."
        ),
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if payload["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
