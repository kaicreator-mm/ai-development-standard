from __future__ import annotations

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "standard-manifest.json"
PROFILE_INDEX = ROOT / "profiles" / "README.md"
TASK_PACK = ROOT / "templates" / "task-pack.md"
EXECUTION_CONTRACT = ROOT / "templates" / "execution-pack" / "EXECUTION_CONTRACT.md"
PROJECT_OVERRIDES = ROOT / "templates" / "project" / ".dev-standard" / "PROJECT_OVERRIDES.md"
PROFILE_ADOPTION_REFERENCE = ROOT / "references" / "IMPLEMENTATION_PROFILE_ADOPTION_REFERENCE.md"

FOUR_OWNERS = [
    "standards/ARCHITECTURE_DESIGN_STANDARD.md",
    "standards/TASK_DECOMPOSITION_STANDARD.md",
    "standards/TASK_DAG_GOVERNANCE_STANDARD.md",
    "standards/IMPLEMENTATION_QUALITY_STANDARD.md",
]

PROFILE_PATHS = [
    "profiles/README.md",
    "profiles/languages/typescript.md",
    "profiles/languages/python.md",
    "profiles/languages/go.md",
    "profiles/languages/java.md",
    "profiles/languages/rust.md",
    "profiles/archetypes/library.md",
    "profiles/archetypes/service.md",
    "profiles/archetypes/cli.md",
]

V43_REFERENCES = [
    "references/ARCHITECTURE_DECISION_REFERENCE.md",
    "references/TASK_DECOMPOSITION_REFERENCE.md",
    "references/TASK_DAG_GOVERNANCE_REFERENCE.md",
    "references/IMPLEMENTATION_PROFILE_ADOPTION_REFERENCE.md",
    "references/IMPLEMENTATION_QUALITY_REFERENCE.md",
]

V43_VERIFICATION = [
    "scripts/test_v43_adoption_wiring.py",
    "scripts/test_v43_archetype_profiles.py",
    "scripts/test_v43_architecture_design.py",
    "scripts/test_v43_dag_mutation_contract.py",
    "scripts/test_v43_go_java_rust_profiles.py",
    "scripts/test_v43_implementation_quality.py",
    "scripts/test_v43_profile_framework.py",
    "scripts/test_v43_task_dag_governance.py",
    "scripts/test_v43_task_decomposition.py",
    "scripts/test_v43_ts_python_profiles.py",
]


class V43AdoptionWiringTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        cls.profile_index = PROFILE_INDEX.read_text(encoding="utf-8")
        cls.task_pack = TASK_PACK.read_text(encoding="utf-8")
        cls.execution_contract = EXECUTION_CONTRACT.read_text(encoding="utf-8")
        cls.project_overrides = PROJECT_OVERRIDES.read_text(encoding="utf-8")
        cls.profile_adoption = PROFILE_ADOPTION_REFERENCE.read_text(encoding="utf-8")

    def test_manifest_discovers_v43_normative_owners_and_dag_contract(self) -> None:
        standards = self.manifest["sections"]["normative_standards"]
        for path in FOUR_OWNERS:
            self.assertIn(path, standards)
            self.assertTrue((ROOT / path).is_file(), path)

        schema = "schemas/dag-mutation-record-v1.schema.json"
        self.assertIn(schema, self.manifest["sections"]["machine_contracts"])
        self.assertTrue((ROOT / schema).is_file())

    def test_manifest_has_deterministic_initial_profile_catalog(self) -> None:
        self.assertEqual(self.manifest["sections"]["profiles"], PROFILE_PATHS)
        for path in PROFILE_PATHS:
            self.assertTrue((ROOT / path).is_file(), path)

    def test_manifest_discovers_v43_references_and_verification(self) -> None:
        references = self.manifest["sections"]["references"]
        verification = self.manifest["sections"]["verification"]
        for path in V43_REFERENCES:
            self.assertIn(path, references)
            self.assertTrue((ROOT / path).is_file(), path)
        for path in V43_VERIFICATION:
            self.assertIn(path, verification)
            self.assertTrue((ROOT / path).is_file(), path)

    def test_task_and_execution_packs_consume_refs_without_duplicate_task_object(self) -> None:
        for text in (self.task_pack, self.execution_contract):
            self.assertIn("authority_refs", text)
            self.assertIn("implementation_profile_refs", text)
            self.assertIn("project_overrides_ref", text)
            self.assertIn("MUST NOT create a duplicate Task object/schema", text)
            self.assertNotIn("task-v2", text.lower())

    def test_project_override_composition_is_non_weakening_and_fail_closed(self) -> None:
        self.assertIn("PROJECT_OVERRIDES` may select, specialize or strengthen", self.profile_index)
        self.assertIn("MUST NOT silently weaken Frozen/Core authority", self.profile_index)
        self.assertIn("File/discovery order MUST NOT choose a winner", self.profile_index)
        self.assertIn("Language profile refs", self.profile_adoption)
        self.assertIn("Archetype profile refs", self.profile_adoption)
        self.assertIn("Applicability evidence refs", self.profile_adoption)
        self.assertIn("Specialization / strengthening", self.profile_adoption)
        self.assertIn("MUST NOT weaken Frozen/Core", self.profile_adoption)
        self.assertIn("Discovery order MUST NOT choose a winner", self.profile_adoption)
        self.assertIn("Project overrides **MUST NOT weaken**", self.project_overrides)
        self.assertIn("`BLOCKED`", self.project_overrides)

    def test_discovery_is_static_not_v47_resolver_and_adoption_is_progressive(self) -> None:
        self.assertIn("canonical static discovery index", self.profile_index)
        self.assertIn("does not create a repository-wide resolver", self.profile_index)
        self.assertIn("historical Task/Validation/Review evidence remain valid", self.profile_index)
        self.assertIn("Fast Path and genuinely non-material changes remain lightweight", self.profile_index)


if __name__ == "__main__":
    unittest.main()
