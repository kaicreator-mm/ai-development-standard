"""Verifier for V410-T06A-LOCAL-TEST-COMMAND-MAP-R1.

Checks the preparation unit's pack inventory and the integrity of
TEST_COMMAND_MAP.md: every cited command entrypoint and owner/surface path
must exist at the pinned base, the four T06A surface classes must each have
at least one verifying command row, and negative stale-owner coverage must be
present. Fails closed on any dangling citation or omission.
"""
from __future__ import annotations

import json
from pathlib import Path
import re
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / ".agent" / "execution" / "V410-T06A-LOCAL-TEST-COMMAND-MAP-R1"
MAP = PACK / "TEST_COMMAND_MAP.md"

CORE_ARTIFACTS = [
    "MANIFEST.yaml",
    "EXECUTION_CONTRACT.md",
    "TEST_MATRIX.yaml",
    "FAILURE_MATRIX.yaml",
    "IMPLEMENTATION_MAP.md",
    "REVIEW_CHECKLIST.md",
]

GATE_COMMANDS = [
    "scripts/verify_standard.py",
    "scripts/test_verify_standard.py",
    "scripts/test_protocol_schemas.py",
    "scripts/test_v47_reference_conventions.py",
    "scripts/test_v47_authority_registry.py",
    "scripts/test_v47_compatibility_aliases.py",
    "scripts/test_v47_convergence_metadata_contracts.py",
    "scripts/test_v47_state_dimension_registry.py",
    "scripts/test_v47_progressive_disclosure.py",
    "scripts/test_v48_registry_adoption.py",
    "scripts/test_v48_ads_evolution_governance.py",
    "scripts/test_execution_architecture.py",
]

SURFACE_PATHS = [
    "standard-manifest.json",
    "standards/REFERENCE_CONVENTION_STANDARD.md",
    "references/REFERENCE_CONVENTION_REFERENCE.md",
    "references/AUTHORITY_APPLICABILITY_REGISTRY_REFERENCE.md",
    "references/PROGRESSIVE_DISCLOSURE_ROUTING.md",
    "references/STATE_DIMENSION_REGISTRY_REFERENCE.md",
    "registries/state-dimensions-v1.json",
    "schemas/authority-applicability-entry-v1.schema.json",
    "schemas/state-dimension-registry-v1.schema.json",
    "standards/GITHUB_WORKFLOW.md",
    "standards/VERSION_INTEGRATION_WORKFLOW.md",
]

SURFACE_CLASS_HEADERS = [
    "CLASS_1", "CLASS_2", "CLASS_3", "CLASS_4",
]

IMPORT_ONLY = "scripts/resolve_standard_read_set.py"

NEGATIVE_TOKENS = [
    "silent removal",
    "unindexed legacy alias",
    "unknown alias",
    "alias cannot be a normative owner",
]


class TestCommandMapVerifier(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.map_text = MAP.read_text(encoding="utf-8")
        cls.manifest = json.loads((ROOT / "standard-manifest.json").read_text(encoding="utf-8"))
        cls.alias_source = (ROOT / "scripts" / "test_v47_compatibility_aliases.py").read_text(encoding="utf-8")

    def test_pack_core_inventory_present(self) -> None:
        for name in CORE_ARTIFACTS:
            self.assertTrue((PACK / name).is_file(), f"missing core artifact: {name}")
        self.assertTrue(MAP.is_file(), "missing primary deliverable TEST_COMMAND_MAP.md")

    def test_manifest_binds_discovery_and_registry_sections(self) -> None:
        sections = self.manifest["sections"]
        for key in ("discovery_standards", "registries", "compatibility_entries"):
            self.assertIn(key, sections, f"manifest missing section: {key}")
        self.assertEqual(sections["discovery_standards"], ["standards/REFERENCE_CONVENTION_STANDARD.md"])
        self.assertIn("registries/state-dimensions-v1.json", sections["registries"])
        self.assertIn("semantic_authorities", self.manifest)

    def test_every_gate_command_entrypoint_exists(self) -> None:
        for rel in GATE_COMMANDS:
            self.assertTrue((ROOT / rel).is_file(), f"dangling command entrypoint: {rel}")

    def test_every_cited_surface_path_exists(self) -> None:
        for rel in SURFACE_PATHS:
            self.assertTrue((ROOT / rel).is_file(), f"dangling surface path: {rel}")
            self.assertIn(rel, self.map_text, f"surface not cited in map: {rel}")

    def test_all_four_surface_classes_covered(self) -> None:
        for token in SURFACE_CLASS_HEADERS:
            self.assertIn(token, self.map_text, f"missing surface class: {token}")
        for rel in GATE_COMMANDS:
            self.assertIn(rel, self.map_text, f"command not cited in map: {rel}")

    def test_negative_stale_owner_coverage_is_real(self) -> None:
        lowered = self.map_text.lower()
        self.assertIn("negative stale-owner", lowered)
        for token in NEGATIVE_TOKENS:
            self.assertIn(token, lowered, f"map missing negative token: {token}")
        for probe in (
            "silent_removal",
            "unindexed_legacy_alias",
            "unknown_alias",
            "normative_owner",
        ):
            self.assertIn(probe, self.alias_source, f"alias suite missing negative probe: {probe}")

    def test_import_only_module_not_cited_as_gate(self) -> None:
        gate_section = self.map_text.split("## Observed command matrix")[0]
        for line in gate_section.splitlines():
            if IMPORT_ONLY in line and "library" not in line.lower() and "import-only" not in line.lower():
                self.fail(f"import-only module cited as gate: {line.strip()}")

    def test_no_acceptance_gate_claim(self) -> None:
        for banned in (
            "concern Validation: PASS",
            "Independent Review PASS claimed",
            "T06A acceptance: PASS",
        ):
            self.assertNotIn(banned, self.map_text)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCommandMapVerifier)
    result = unittest.TextTestRunner(verbosity=1).run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)
