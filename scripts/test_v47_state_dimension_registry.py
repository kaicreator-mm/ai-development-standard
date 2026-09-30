from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import re
import unittest

from test_protocol_schemas import validate_subset

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "registries/state-dimensions-v1.json"
SCHEMA = ROOT / "schemas/state-dimension-registry-v1.schema.json"
REFERENCE = ROOT / "references/STATE_DIMENSION_REGISTRY_REFERENCE.md"
EXACT_UPSTREAM = re.compile(r"^github:kaicreator-mm/ai-development-standard@[0-9a-f]{40}:[A-Za-z0-9_./-]+$")

REQUIRED_NEGATIVES = {
    "F01_TASK_DONE_NOT_VALIDATION_PASS": ("work_item_workflow", "validation_gate"),
    "F02_REVIEW_PASS_NOT_VALIDATION_PASS": ("review_judgment", "validation_gate"),
    "F03_VALIDATION_PASS_NOT_RELEASE_READY": ("validation_gate", "release_qualification"),
    "F04_RELEASE_READY_NOT_DEPLOYMENT_SUCCESS": ("release_qualification", "deployment_result"),
    "F05_DEPLOYMENT_SUCCESS_NOT_RUNTIME_HEALTH": ("deployment_result", "runtime_health"),
    "F06_RUNNER_AVAILABLE_NOT_MUTATION_AUTHORITY": ("runner_capability", "work_item_workflow"),
    "F07_OLD_SHA_VALIDATION_NOT_SUCCESSOR_PASS": ("validation_gate", "validation_gate"),
    "F08_SANDBOX_PASS_NOT_REAL_ENV_PASS": ("validation_gate", "validation_gate"),
}


def consistency_errors(registry: dict) -> list[str]:
    """A test-only structural oracle; normative admission stays with owning standards."""
    errors = []
    dimensions = registry.get("dimensions", [])
    ids = [d["dimension_id"] for d in dimensions]
    if len(ids) != len(set(ids)):
        errors.append("duplicate dimension")
    for dimension in dimensions:
        owner = dimension["canonical_owner_ref"]
        if owner.startswith("standards/"):
            if not (ROOT / owner).is_file():
                errors.append(f"broken local owner: {owner}")
        elif not EXACT_UPSTREAM.fullmatch(owner):
            errors.append(f"mutable/unqualified upstream owner: {owner}")
        if dimension.get("vocabulary_posture") not in {"CLOSED", "OPEN", "OWNER_DEFINED"}:
            errors.append("unknown vocabulary posture")
    rules = registry.get("forbidden_inferences", [])
    names = [r["rule_id"] for r in rules]
    if len(names) != len(set(names)):
        errors.append("duplicate rule")
    for rule in rules:
        for field in ("source_dimension_ref", "target_dimension_ref"):
            if rule[field] not in ids:
                errors.append(f"unresolved dimension: {rule[field]}")
    return errors


class StateDimensionRegistryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(REGISTRY.read_text(encoding="utf-8"))
        cls.schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        cls.reference = REFERENCE.read_text(encoding="utf-8")

    def test_actual_t01_schema_accepts_real_registry(self) -> None:
        self.assertEqual(validate_subset(self.data, self.schema), [])
        self.assertEqual(consistency_errors(self.data), [])
        self.assertEqual(self.data["schema_version"], 1)

    def test_each_dimension_is_owner_qualified_and_has_no_global_enum(self) -> None:
        ids = [d["dimension_id"] for d in self.data["dimensions"]]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertGreaterEqual(len(ids), 8)
        self.assertNotIn("master", self.data)
        self.assertNotIn("states", self.data)
        self.assertNotIn("transitions", self.data)
        self.assertNotIn("PASS", [d["dimension_id"] for d in self.data["dimensions"]])
        for dimension in self.data["dimensions"]:
            self.assertTrue(dimension["canonical_owner_ref"])
            self.assertNotIn("current_state", dimension)
            self.assertNotIn("mutation_authorized", dimension)

    def test_all_eight_required_negatives_are_machine_readable_and_resolve(self) -> None:
        by_id = {r["rule_id"]: r for r in self.data["forbidden_inferences"]}
        self.assertTrue(set(REQUIRED_NEGATIVES).issubset(by_id))
        for name, expected in REQUIRED_NEGATIVES.items():
            rule = by_id[name]
            self.assertEqual((rule["source_dimension_ref"], rule["target_dimension_ref"]), expected)
            self.assertTrue(rule["source_fact_ref"])
            self.assertTrue(rule["prohibited_conclusion_ref"])
        self.assertEqual(len(by_id), len(self.data["forbidden_inferences"]))
        self.assertEqual(by_id["F02_REVIEW_PASS_NOT_VALIDATION_PASS"]["source_fact_ref"], "PASS")
        self.assertEqual(by_id["F02_REVIEW_PASS_NOT_VALIDATION_PASS"]["prohibited_conclusion_ref"], "PASS")
        self.assertNotEqual(by_id["F07_OLD_SHA_VALIDATION_NOT_SUCCESSOR_PASS"]["source_fact_ref"],
                            by_id["F07_OLD_SHA_VALIDATION_NOT_SUCCESSOR_PASS"]["prohibited_conclusion_ref"])

    def test_schema_rejects_lifecycle_or_grant_fields(self) -> None:
        for illegal in ("current_state", "transition", "mutation_authorized", "release_pass", "deployment_authorized"):
            bad = deepcopy(self.data)
            bad[illegal] = True
            self.assertTrue(validate_subset(bad, self.schema), illegal)
        bad_dimension = deepcopy(self.data)
        bad_dimension["dimensions"][0]["global_pass"] = "PASS"
        self.assertTrue(validate_subset(bad_dimension, self.schema))
        bad_rule = deepcopy(self.data)
        bad_rule["forbidden_inferences"][0]["inference_grant"] = True
        self.assertTrue(validate_subset(bad_rule, self.schema))

    def test_conflicting_owners_and_dangling_rules_fail_closed(self) -> None:
        duplicate = deepcopy(self.data)
        competing = deepcopy(duplicate["dimensions"][0])
        competing["canonical_owner_ref"] = "standards/RELEASE_STANDARD.md"
        duplicate["dimensions"].append(competing)
        self.assertIn("duplicate dimension", consistency_errors(duplicate))
        dangling = deepcopy(self.data)
        dangling["forbidden_inferences"][0]["target_dimension_ref"] = "imaginary_dimension"
        self.assertTrue(any("unresolved dimension" in x for x in consistency_errors(dangling)))
        broken = deepcopy(self.data)
        broken["dimensions"][0]["canonical_owner_ref"] = "standards/DOES_NOT_EXIST.md"
        self.assertTrue(any("broken local owner" in x for x in consistency_errors(broken)))
        mutable = deepcopy(self.data)
        mutable["dimensions"][0]["canonical_owner_ref"] = "github:kaicreator-mm/ai-development-standard@main:standards/RELEASE_STANDARD.md"
        self.assertTrue(any("mutable/unqualified" in x for x in consistency_errors(mutable)))

    def test_upstream_owner_limitations_are_explicit_and_non_authoritative(self) -> None:
        dims = {d["dimension_id"]: d for d in self.data["dimensions"]}
        self.assertRegex(dims["deployment_result"]["canonical_owner_ref"], EXACT_UPSTREAM)
        runtime = dims["runtime_health"]
        self.assertRegex(runtime["canonical_owner_ref"], EXACT_UPSTREAM)
        self.assertIn("L2_ARCHITECTURE_EVIDENCE.md", runtime["canonical_owner_ref"])
        self.assertEqual(runtime["vocabulary_posture"], "OWNER_DEFINED")
        for token in ("BLOCKED until", "not an active local normative Runtime vocabulary", "not a live state store", "does not prove Runtime health"):
            self.assertIn(token, self.reference)
        self.assertIn("not an active local normative Runtime vocabulary", self.reference)

    def test_owner_vocabularies_remain_separate(self) -> None:
        self.assertIn("state:done", (ROOT / "standards/GITHUB_WORK_ITEM_CONTRACT_STANDARD.md").read_text(encoding="utf-8"))
        self.assertIn("PASS / FAIL / BLOCKED / NOT_RUN / NOT_APPLICABLE", (ROOT / "standards/VALIDATION_STANDARD.md").read_text(encoding="utf-8"))
        self.assertIn("PACK_STALE_MATERIAL", (ROOT / "standards/EXECUTION_PACK_STANDARD.md").read_text(encoding="utf-8"))
        self.assertIn("A capability profile is useful for routing", (ROOT / "standards/CI_RUNNER_CAPABILITY_STANDARD.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
