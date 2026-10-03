"""T-006 focused verifier: v4.8 registry / discoverability / adoption wiring.

Verifies the exact T-006 candidate state on the current checkout only:

1. exactly the three new v4.8 machine-contract families are discoverable;
2. existing Interchange v1 is reused and listed exactly once (no new family);
3. owner references and focused verification paths are discoverable exactly once;
4. every registered path exists on this checkout;
5. adoption/reference/migration text preserves metadata-only, Fast Path and
   no-authority boundaries;
6. the manifest inventory equals the frozen pre-T006 baseline plus exactly the
   expected v4.8 additions (no removals, no fourth family);
7. v4.7 branch-only registry machinery is recorded as lineage only and is not
   reinvented in the current manifest.

This script is deterministic repository-local evidence (standard library, no
network, no provider). It is NOT a permission engine, NOT Validation and NOT
Review: registry/discovery presence never grants mutation, merge, Validation
PASS, Review PASS or Release READY. The frozen baseline constants describe the
exact T-006 candidate and do not freeze future additive manifest changes;
authorization for any later change remains with its owning change.
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "standard-manifest.json"

T006_REFERENCE = ROOT / "references" / "V48_REGISTRY_ADOPTION_REFERENCE.md"
T006_ADOPTION = ROOT / "standards" / "PROJECT_ADOPTION.md"
T006_MIGRATION = ROOT / "docs" / "implementation" / "4.8.0" / "MIGRATION_ADOPTION.md"

EXPECTED_V48_MACHINE_CONTRACTS = [
    "schemas/agent-capability-evidence-v1.schema.json",
    "schemas/agent-capability-profile-v1.schema.json",
    "schemas/task-learning-v1.schema.json",
]

INTERCHANGE_V1 = "schemas/interchange-envelope-v1.schema.json"

EXPECTED_V48_REFERENCES = [
    "references/AGENT_CAPABILITY_EVIDENCE_REFERENCE.md",
    "references/AGENT_CAPABILITY_PROFILE_REFERENCE.md",
    "references/TASK_LEARNING_EVIDENCE_REFERENCE.md",
    "references/V48_INTERCHANGE_PROFILE_COMPATIBILITY.md",
    "references/V48_REGISTRY_ADOPTION_REFERENCE.md",
]

EXPECTED_V48_VERIFICATION = [
    "scripts/test_v48_agent_capability_evidence.py",
    "scripts/test_v48_agent_capability_profile.py",
    "scripts/test_v48_interchange_profile.py",
    "scripts/test_v48_registry_adoption.py",
    "scripts/test_v48_task_learning.py",
]

# Branch-only v4.7 lineage artifacts: read-only design inputs, never current
# v4.8 owners, never to be re-created by T-006.
V47_LINEAGE_ONLY_PATHS = [
    "references/AUTHORITY_APPLICABILITY_REGISTRY_REFERENCE.md",
    "references/PROGRESSIVE_DISCLOSURE_ROUTING.md",
]

# Frozen pre-T006 baseline inventory (version/v4.8.0@257e95531551960cb163a3e20
# ab2b3d13f415d3c, tree 1171de2c8afb08d6f793a258ffd0b586007e9dbf). Encoded as
# the expected diff base for the T-006 candidate: candidate section == baseline
# section + exactly the expected additions.
BASELINE_MACHINE_CONTRACTS = [
    "schemas/agent-event-v2.schema.json",
    "schemas/assurance-plan-v1.schema.json",
    "schemas/dispatch.schema.json",
    "schemas/execution-pack-manifest.schema.json",
    "schemas/execution-state.schema.json",
    "schemas/interchange-envelope-v1.schema.json",
    "schemas/local-agent-handoff.schema.json",
    "schemas/operation-binding-v1.schema.json",
    "schemas/operation-v1.schema.json",
    "schemas/repository-integration-v4-precondition.schema.json",
    "schemas/review-aggregation-v1.schema.json",
    "schemas/review-finding-v1.schema.json",
    "schemas/task-contract.schema.json",
    "schemas/validation-report.schema.json",
]
BASELINE_REFERENCES = [
    "references/CI_EVIDENCE_REFERENCE_VALIDATION.md",
    "references/GITHUB_ENGINEERING_REFERENCES.md",
    "references/TEST_DATA_ENGINEERING_REFERENCES.md",
    "references/WOODPECKER_LOCAL_BACKEND_REFERENCE.md",
    "references/WOODPECKER_UBUNTU_BUILD_01_CAPABILITY_2026-09-18.yaml",
]
BASELINE_VERIFICATION = [
    ".github/workflows/verify-standard.yml",
    "scripts/test_execution_architecture.py",
    "scripts/test_pointer_only_trigger_contract.py",
    "scripts/test_project_execution_profile.py",
    "scripts/test_protocol_schemas.py",
    "scripts/test_task_dag_lane_parallelism.py",
    "scripts/test_v33_lifecycle_contracts.py",
    "scripts/test_v33_semantic_regressions.py",
    "scripts/test_v34_lifecycle_contracts.py",
    "scripts/test_v34_review_repairs.py",
    "scripts/test_v40_adoption_migration.py",
    "scripts/test_v40_dogfood_hardening.py",
    "scripts/test_v40_final_hardening.py",
    "scripts/test_v40_operation_contracts.py",
    "scripts/test_v40_r2_machine_hardening.py",
    "scripts/test_v40_r3_carryforward.py",
    "scripts/test_v40_reference_flows.py",
    "scripts/test_v40_t010_canonical_surface.py",
    "scripts/test_v40_t010_successor_hardening.py",
    "scripts/test_v40_t012_pre_release_hardening.py",
    "scripts/test_verify_project_standard.py",
    "scripts/test_verify_standard.py",
    "scripts/test_work_item_contract_and_golden_templates.py",
    "scripts/v34_rules.py",
    "scripts/v40_r2_hardening.py",
    "scripts/v40_r3_hardening.py",
    "scripts/v40_rules.py",
    "scripts/v40_semantics.py",
    "scripts/v40_t010_successor_hardening.py",
    "scripts/v40_t012_pre_release_hardening.py",
    "scripts/verify_event_writer_surfaces.py",
    "scripts/verify_project_execution_profile.py",
    "scripts/verify_project_standard.py",
    "scripts/verify_runner_capability_reference.py",
    "scripts/verify_standard.py",
]

# Controlled result-semantics tokens the T-006 surfaces must state verbatim.
REQUIRED_REFERENCE_TOKENS = [
    "authority_effect=NONE",
    "gate_effect=NONE",
    "mutation_authorized=false",
    "REGISTRY_AUTHORITY_EFFECT=NONE",
    "INTERCHANGE_REUSED=YES",
    "V48_MACHINE_FAMILY_COUNT=3",
    "V47_LINEAGE=LINEAGE_ONLY_NOT_CURRENT_V4_8_AUTHORITY",
    "PROVIDER_IDENTITY=NOT_AUTHORITY",
    "CAPABILITY_EVIDENCE=NOT_CURRENT_VALIDATION_REVIEW_TRUTH",
    "TASK_LEARNING=NONE_MATERIAL",
    "FAST_PATH=LIGHTWEIGHT",
]
FORBIDDEN_GRANT_TOKENS = [
    "authority_effect=GRANT",
    "gate_effect=PASS",
    "mutation_authorized=true",
    "registry grants merge",
    "registry grants Validation",
    "registry grants Release",
]
REQUIRED_ADOPTION_TOKENS = [
    "references/V48_REGISTRY_ADOPTION_REFERENCE.md",
    "standard-manifest.json",
    "materiality-driven",
    "TASK_LEARNING=NONE_MATERIAL",
]
REQUIRED_MIGRATION_TOKENS = [
    "NO_DESTRUCTIVE_REWRITE",
    "NO_NEW_INTERCHANGE_FAMILY",
    "TASK_LEARNING=NONE_MATERIAL",
    "HISTORICAL_COMPATIBILITY=PRESERVED",
    "STOP_ESCALATION_OWNER_GAP",
]


def load_manifest() -> dict:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def section(manifest: dict, name: str) -> list[str]:
    values = manifest["sections"][name]
    assert isinstance(values, list)
    return [str(value) for value in values]


def count_exact(values: list[str], target: str) -> int:
    return sum(1 for value in values if value == target)


def assert_exactly_once(testcase: unittest.TestCase, values: list[str], target: str) -> None:
    occurrences = count_exact(values, target)
    testcase.assertEqual(
        occurrences,
        1,
        f"{target!r} must be discoverable exactly once in the manifest (found {occurrences})",
    )


def assert_section_is_baseline_plus_additions(
    testcase: unittest.TestCase,
    candidate: list[str],
    baseline: list[str],
    additions: list[str],
    label: str,
) -> None:
    expected = sorted(baseline + additions)
    actual = sorted(candidate)
    removed = sorted(set(baseline) - set(actual))
    testcase.assertEqual(
        removed,
        [],
        f"{label}: historical inventory must not be removed, missing={removed}",
    )
    unexpected = sorted(set(actual) - set(expected))
    testcase.assertEqual(
        unexpected,
        [],
        f"{label}: only the intended T-006 additions are authorized, unexpected={unexpected}",
    )
    testcase.assertEqual(
        actual,
        expected,
        f"{label}: inventory must equal baseline plus the intended T-006 additions exactly once",
    )


class RegistryAdoptionManifestTests(unittest.TestCase):
    """RA-01/02/03/09 plus negatives RA-N01/N02/N07/N08."""

    def setUp(self) -> None:
        self.manifest = load_manifest()
        self.sections = self.manifest["sections"]

    def test_manifest_shape_is_unchanged(self) -> None:
        self.assertEqual(self.manifest.get("schema_version"), 1)
        self.assertEqual(
            sorted(self.sections.keys()),
            sorted(
                [
                    "authority",
                    "normative_standards",
                    "compatibility_entries",
                    "templates",
                    "checklists",
                    "prompts",
                    "machine_contracts",
                    "references",
                    "verification",
                ]
            ),
        )

    def test_three_v48_machine_families_discoverable_exactly_once(self) -> None:
        contracts = section(self.manifest, "machine_contracts")
        for family in EXPECTED_V48_MACHINE_CONTRACTS:
            assert_exactly_once(self, contracts, family)

    def test_interchange_v1_reused_exactly_once_and_no_new_owner(self) -> None:
        contracts = section(self.manifest, "machine_contracts")
        assert_exactly_once(self, contracts, INTERCHANGE_V1)
        interchange_like = [path for path in contracts if "interchange" in path.lower()]
        self.assertEqual(
            interchange_like,
            [INTERCHANGE_V1],
            "no second/new Interchange family or version may be registered",
        )

    def test_no_fourth_t006_machine_family(self) -> None:
        contracts = section(self.manifest, "machine_contracts")
        self.assertEqual(len(contracts), len(set(contracts)), "duplicate manifest entries are forbidden")
        assert_section_is_baseline_plus_additions(
            self,
            contracts,
            BASELINE_MACHINE_CONTRACTS,
            EXPECTED_V48_MACHINE_CONTRACTS,
            "machine_contracts",
        )

    def test_owner_references_discoverable_exactly_once(self) -> None:
        references = section(self.manifest, "references")
        for reference in EXPECTED_V48_REFERENCES:
            assert_exactly_once(self, references, reference)

    def test_focused_verification_discoverable_exactly_once(self) -> None:
        verification = section(self.manifest, "verification")
        for script in EXPECTED_V48_VERIFICATION:
            assert_exactly_once(self, verification, script)

    def test_references_section_is_baseline_plus_additions(self) -> None:
        assert_section_is_baseline_plus_additions(
            self,
            section(self.manifest, "references"),
            BASELINE_REFERENCES,
            EXPECTED_V48_REFERENCES,
            "references",
        )

    def test_verification_section_is_baseline_plus_additions(self) -> None:
        assert_section_is_baseline_plus_additions(
            self,
            section(self.manifest, "verification"),
            BASELINE_VERIFICATION,
            EXPECTED_V48_VERIFICATION,
            "verification",
        )

    def test_untouched_historical_sections_preserved(self) -> None:
        for name, minimum in (
            ("authority", 5),
            ("normative_standards", 25),
            ("compatibility_entries", 2),
            ("templates", 40),
            ("checklists", 5),
            ("prompts", 10),
        ):
            values = section(self.manifest, name)
            self.assertGreaterEqual(
                len(values),
                minimum,
                f"{name}: historical inventory must not be removed",
            )

    def test_every_registered_path_exists_on_checkout(self) -> None:
        missing: list[str] = []
        for name in self.sections:
            for rel in section(self.manifest, name):
                if not (ROOT / rel).is_file():
                    missing.append(rel)
        self.assertEqual(missing, [], "every registered path must exist on the exact candidate checkout")

    def test_no_v47_authority_store_reinvented(self) -> None:
        self.assertNotIn(
            "semantic_authorities",
            self.manifest,
            "T-006 must not reinvent the v4.7 branch-only semantic-authority manifest model",
        )
        for rel in V47_LINEAGE_ONLY_PATHS:
            self.assertNotIn(rel, section(self.manifest, "references"))
            self.assertFalse(
                (ROOT / rel).exists(),
                f"v4.7 branch-only lineage artifact must not be copied into v4.8: {rel}",
            )


class RegistryAdoptionTextBoundaryTests(unittest.TestCase):
    """RA-04/05/07/08 plus negatives RA-N03/N04/N05/N06."""

    def setUp(self) -> None:
        self.reference = read_text(T006_REFERENCE)
        self.adoption = read_text(T006_ADOPTION)
        self.migration = read_text(T006_MIGRATION)

    def test_reference_states_explicit_metadata_only_semantics(self) -> None:
        for token in REQUIRED_REFERENCE_TOKENS:
            self.assertIn(token, self.reference, f"T-006 reference must state: {token}")

    def test_reference_contains_no_granting_semantics(self) -> None:
        for token in FORBIDDEN_GRANT_TOKENS:
            self.assertNotIn(token, self.reference, f"T-006 reference must not grant authority: {token}")

    def test_reference_maps_families_to_owners_without_restating_semantics(self) -> None:
        for rel in EXPECTED_V48_MACHINE_CONTRACTS + EXPECTED_V48_REFERENCES[:4]:
            self.assertIn(rel, self.reference, f"T-006 reference must route discovery to: {rel}")
        self.assertIn(INTERCHANGE_V1, self.reference)

    def test_reference_records_v47_lineage_boundary_honestly(self) -> None:
        for rel in V47_LINEAGE_ONLY_PATHS:
            self.assertIn(
                Path(rel).name,
                self.reference,
                f"T-006 reference must name the v4.7 lineage-only artifact: {rel}",
            )

    def test_project_adoption_exposes_bounded_discovery(self) -> None:
        for token in REQUIRED_ADOPTION_TOKENS:
            self.assertIn(token, self.adoption, f"PROJECT_ADOPTION must expose bounded discovery: {token}")
        for family in EXPECTED_V48_MACHINE_CONTRACTS:
            self.assertIn(family, self.adoption, f"PROJECT_ADOPTION must name the new family: {family}")

    def test_optional_families_are_not_globally_mandatory(self) -> None:
        self.assertIn("MAY", self.adoption, "adoption of optional v4.8 families must stay per-project optional")
        self.assertIn("authority_effect=NONE", self.adoption)
        for token in FORBIDDEN_GRANT_TOKENS:
            self.assertNotIn(token, self.adoption)

    def test_fast_path_remains_lightweight(self) -> None:
        for label, text in (("reference", self.reference), ("adoption", self.adoption), ("migration", self.migration)):
            self.assertIn("Fast Path", text, f"{label} must preserve the lightweight Fast Path")
            self.assertIn(
                "TASK_LEARNING=NONE_MATERIAL",
                text,
                f"{label} must keep TASK_LEARNING=NONE_MATERIAL a valid Fast Path outcome",
            )

    def test_migration_is_additive_and_preserves_history(self) -> None:
        for token in REQUIRED_MIGRATION_TOKENS:
            self.assertIn(token, self.migration, f"migration note must state: {token}")
        for token in FORBIDDEN_GRANT_TOKENS:
            self.assertNotIn(token, self.migration)
        self.assertIn(INTERCHANGE_V1, self.migration)


if __name__ == "__main__":
    unittest.main()
