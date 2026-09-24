from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GOLDEN = ROOT / "templates/golden/V4_ADOPTION_MIGRATION_EXAMPLES.json"
ADOPTION = ROOT / "standards/PROJECT_ADOPTION.md"
OVERRIDES = ROOT / "templates/project/.dev-standard/PROJECT_OVERRIDES.md"
GUIDE = ROOT / "docs/implementation/4.0.0/MIGRATION_ADOPTION_GUIDE.md"
CHECKLIST = ROOT / "checklists/project-init.md"
TASK_PACK = ROOT / "docs/implementation/4.0.0/task-packs/T011_migration_adoption_overrides.md"

LEVELS = [
    "A0_COMPATIBILITY",
    "A1_MANUAL_PROTOCOL",
    "A2_MACHINE_CONTRACTS",
    "A3_DERIVED_AUTOMATION",
    "A4_FULL_ORCHESTRATION",
]

REQUIRED_INVARIANTS = {
    "immutable-standard-pin",
    "durable-authority",
    "exact-subject-identity",
    "actual-required-validation-execution",
    "review-policy-authority",
    "review-not-validation",
    "blocker-dominance",
    "candidate-prepared-not-frozen",
    "pr-pass-not-release-pass",
    "release-ready-not-repository-integration",
    "interchange-correlation-only-non-authoritative",
    "truthful-not-run-blocked-not-applicable",
}

REQUIRED_MIGRATION = {
    "immutable-standard-pin",
    "frozen-product-architecture-authority",
    "task-dag-and-issue-dependencies",
    "task-pack",
    "execution-pack",
    "exact-sha-validation",
    "review-policy-required-recommended-not-required",
    "builder-validator-reviewer-roles",
    "ai-dev-event-v2",
    "fast-path",
    "candidate-freeze",
    "release-qualification",
    "repository-integration",
    "github-durable-facts",
}

REQUIRED_FORBIDDEN = {
    "skip-required-validation",
    "review-majority-is-validation",
    "remove-fast-path-disqualifier",
    "authoritative-interchange",
    "release-ready-implies-merged",
    "branch-latest-replaces-exact-sha",
    "blocked-becomes-not-applicable",
}


def require(text: str, needle: str, source: str) -> None:
    if needle not in text:
        raise AssertionError(f"{source} missing required marker: {needle}")


def main() -> int:
    data = json.loads(GOLDEN.read_text(encoding="utf-8"))
    adoption = ADOPTION.read_text(encoding="utf-8")
    overrides = OVERRIDES.read_text(encoding="utf-8")
    guide = GUIDE.read_text(encoding="utf-8")
    checklist = CHECKLIST.read_text(encoding="utf-8")
    task_pack = TASK_PACK.read_text(encoding="utf-8")

    levels = data["adoption_levels"]
    actual_levels = [entry["level"] for entry in levels]
    assert actual_levels == LEVELS, actual_levels

    previous: set[str] = set()
    for entry in levels:
        capabilities = set(entry["capabilities"])
        assert previous <= capabilities, (
            f"adoption capabilities must be monotonic: {previous} !<= {capabilities}"
        )
        assert entry["required_truth_floor"] == "common_non_weakening_invariants"
        previous = capabilities

    invariants = set(data["common_non_weakening_invariants"])
    assert REQUIRED_INVARIANTS <= invariants, REQUIRED_INVARIANTS - invariants

    migration = {entry["v34"] for entry in data["migration_matrix"]}
    assert REQUIRED_MIGRATION <= migration, REQUIRED_MIGRATION - migration

    forbidden = {entry["name"] for entry in data["forbidden_overrides"]}
    assert REQUIRED_FORBIDDEN <= forbidden, REQUIRED_FORBIDDEN - forbidden

    fast_path = data["fast_path"]
    assert fast_path["orthogonal_to_adoption_level"] is True
    assert fast_path["project_may_disable"] is True
    assert fast_path["project_may_strengthen"] is True
    assert fast_path["project_may_remove_canonical_disqualifiers"] is False
    assert fast_path["low_adoption_level_proves_eligibility"] is False

    history = data["historical_evidence"]
    assert history["migration_rewrites_prior_results"] is False
    assert history["prior_identity_and_status_preserved"] is True

    successor = data["successor_task_boundary"]
    assert successor == {"t011_executes_t012": False, "t011_executes_t013": False}

    profiles = data["reference_profiles"]
    assert profiles["small_project"]["adoption_level"] in {"A0_COMPATIBILITY", "A1_MANUAL_PROTOCOL"}
    assert profiles["substantial_project"]["adoption_level"] in {
        "A2_MACHINE_CONTRACTS",
        "A3_DERIVED_AUTOMATION",
        "A4_FULL_ORCHESTRATION",
    }

    for level in LEVELS:
        require(adoption, level, "PROJECT_ADOPTION.md")
        require(overrides, level, "PROJECT_OVERRIDES.md")
        require(guide, level, "MIGRATION_ADOPTION_GUIDE.md")

    for text, source in [(adoption, "PROJECT_ADOPTION.md"), (guide, "MIGRATION_ADOPTION_GUIDE.md")]:
        require(text, "adoption level", source)
        require(text, "exact", source)
        require(text, "Validation", source)
        require(text, "PR PASS", source)
        require(text, "Release", source)
        require(text, "Interchange", source)
        require(text, "Fast Path", source)

    for needle in [
        "v4.adoption_level",
        "v4.compatibility_mode",
        "v4.assurance.default",
        "v4.model_diversity.default_basis",
        "v4.interchange",
        "v4.reducer",
        "v4.controllers",
        "v4.fast_path",
        "MUST NOT weaken",
    ]:
        require(overrides, needle, "PROJECT_OVERRIDES.md")

    require(checklist, "v4 adoption level", "project-init.md")
    require(checklist, "non-weakening", "project-init.md")
    require(checklist, "historical evidence", "project-init.md")

    require(task_pack, "No v4 runtime/schema/semantic-facade changes", "T-011 Task Pack")
    require(task_pack, "T-012", "T-011 Task Pack")
    require(task_pack, "T-013", "T-011 Task Pack")

    print("v4 adoption/migration regression: PASS")
    print(f"levels={len(levels)} invariants={len(invariants)} migration_entries={len(migration)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
