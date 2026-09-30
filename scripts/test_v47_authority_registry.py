"""v4.7 T02 additive manifest discovery, not a permissions engine.

The checked-in T01 entry schema is the source for each entry's accepted
fields and applicability vocabulary. No network, workflow or credential
probe is performed by this module.
"""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "standard-manifest.json"
ENTRY_SCHEMA = ROOT / "schemas" / "authority-applicability-entry-v1.schema.json"


class RegistryError(ValueError):
    """Invalid discovery metadata must never resolve by insertion order."""


def validate_entry(entry: object, schema: dict) -> None:
    """Execute the bounded, closed properties of the currently merged T01 schema."""
    if not isinstance(entry, dict):
        raise RegistryError("entry must be an object")
    required = set(schema["required"])
    properties = schema["properties"]
    if required - entry.keys():
        raise RegistryError(f"entry missing required: {sorted(required - entry.keys())}")
    if schema.get("additionalProperties") is False and entry.keys() - properties.keys():
        raise RegistryError(f"entry has forbidden fields: {sorted(entry.keys() - properties.keys())}")
    for name, value in entry.items():
        prop = properties[name]
        if "const" in prop and (type(value) is not type(prop["const"]) or value != prop["const"]):
            raise RegistryError(f"{name}: invalid schema version")
        if prop.get("type") == "string":
            if not isinstance(value, str) or len(value) < prop.get("minLength", 0):
                raise RegistryError(f"{name}: invalid string")
        if prop.get("type") == "array":
            item_rule = prop["items"]
            if not isinstance(value, list) or any(
                not isinstance(item, str) or len(item) < item_rule.get("minLength", 0)
                for item in value
            ):
                raise RegistryError(f"{name}: invalid reference array")
            if len(value) != len(set(value)):
                raise RegistryError(f"{name}: duplicate references")
        if "enum" in prop and value not in prop["enum"]:
            raise RegistryError(f"{name}: unknown applicability")


def resolve_registry(manifest: dict, schema: dict, *, root: Path | None = None) -> dict[str, str]:
    """Return concern -> canonical owner only; never return an authorization decision.

    Alias graph is deliberately one-hop. Alias refs can only attach directly
    to canonical normative owners, not to another compatibility alias.
    Consequently an attempted alias chain/cycle is unrepresentable and fails.
    """
    if not isinstance(manifest, dict) or not isinstance(manifest.get("sections"), dict):
        raise RegistryError("missing legacy sections")
    inventory = manifest["sections"]
    normative = inventory.get("normative_standards")
    compatibility = inventory.get("compatibility_entries")
    if not isinstance(normative, list) or not isinstance(compatibility, list):
        raise RegistryError("missing canonical/compatibility inventory")
    if len(normative) != len(set(normative)) or len(compatibility) != len(set(compatibility)):
        raise RegistryError("ambiguous inventory path")
    if set(normative) & set(compatibility):
        raise RegistryError("alias cannot be normative owner")

    optional = manifest.get("semantic_authorities")
    if optional is None:
        return {}  # historical manifest remains valid for legacy readers
    if not isinstance(optional, dict) or set(optional) != {"schema_version", "entries"}:
        raise RegistryError("invalid semantic registry envelope")
    if type(optional["schema_version"]) is not int or optional["schema_version"] != 1:
        raise RegistryError("unsupported semantic registry version")
    entries = optional["entries"]
    if not isinstance(entries, list) or not entries:
        raise RegistryError("empty or invalid semantic registry")

    by_concern: dict[str, str] = {}
    ids: set[str] = set()
    aliases: set[str] = set()
    for entry in entries:
        validate_entry(entry, schema)
        owner = entry["canonical_owner_ref"]
        if entry["entry_id"] in ids:
            raise RegistryError("duplicate entry id")
        ids.add(entry["entry_id"])
        if entry["semantic_concern"] in by_concern:
            raise RegistryError("competing canonical owners for semantic concern")
        if owner not in normative or owner in compatibility:
            raise RegistryError("broken owner/alias target; no fallback owner")
        if root is not None and not (root / owner).is_file():
            raise RegistryError("owner path absent in checkout")
        for ref in entry.get("compatibility_alias_refs", []):
            if ref not in compatibility or ref in normative or ref in aliases or ref == owner:
                raise RegistryError("broken, duplicate or recursive alias")
            if root is not None and not (root / ref).is_file():
                raise RegistryError("alias path absent in checkout")
            aliases.add(ref)
        for ref in entry.get("applicability_refs", []):
            if ref not in normative and ref not in compatibility and ref not in inventory.get("references", []):
                raise RegistryError("unresolved applicability reference")
        note = entry.get("notes_ref")
        if note and (not isinstance(note, str) or root is not None and not (root / note).is_file()):
            raise RegistryError("unresolved notes reference")
        by_concern[entry["semantic_concern"]] = owner
    return by_concern


class AuthorityRegistryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        cls.schema = json.loads(ENTRY_SCHEMA.read_text(encoding="utf-8"))

    def expect_rejected(self, mutant: dict) -> None:
        with self.assertRaises(RegistryError):
            resolve_registry(mutant, self.schema)

    def test_current_registry_is_resolvable_and_sections_still_exposed(self) -> None:
        resolved = resolve_registry(self.manifest, self.schema, root=ROOT)
        self.assertIn("development.lifecycle_and_task_stage", resolved)
        self.assertEqual(self.manifest["schema_version"], 1)
        self.assertTrue(self.manifest["sections"]["verification"])
        self.assertIn("standards/GITHUB_WORKFLOW.md", self.manifest["sections"]["compatibility_entries"])

    def test_historical_manifest_without_optional_registry_still_resolves(self) -> None:
        historical = deepcopy(self.manifest)
        del historical["semantic_authorities"]
        self.assertEqual(resolve_registry(historical, self.schema), {})
        self.assertEqual(historical["sections"], self.manifest["sections"])

    def test_competing_owners_fail_regardless_of_file_or_entry_order(self) -> None:
        mutant = deepcopy(self.manifest)
        contender = deepcopy(mutant["semantic_authorities"]["entries"][0])
        contender["entry_id"] = "competing"
        contender["canonical_owner_ref"] = "standards/RELEASE_STANDARD.md"
        mutant["semantic_authorities"]["entries"].append(contender)
        self.expect_rejected(mutant)
        mutant["semantic_authorities"]["entries"].reverse()
        self.expect_rejected(mutant)

    def test_duplicate_id_and_missing_owner_fail(self) -> None:
        mutant = deepcopy(self.manifest)
        mutant["semantic_authorities"]["entries"][1]["entry_id"] = mutant["semantic_authorities"]["entries"][0]["entry_id"]
        self.expect_rejected(mutant)
        mutant = deepcopy(self.manifest)
        mutant["semantic_authorities"]["entries"][0]["canonical_owner_ref"] = "standards/DOES_NOT_EXIST.md"
        self.expect_rejected(mutant)

    def test_broken_alias_and_attempted_alias_chain_or_cycle_fail(self) -> None:
        mutant = deepcopy(self.manifest)
        mutant["semantic_authorities"]["entries"][0]["compatibility_alias_refs"] = ["standards/DOES_NOT_EXIST.md"]
        self.expect_rejected(mutant)
        mutant = deepcopy(self.manifest)
        # A chain/cycle would require promoting a compatibility alias to an
        # owner; the single-hop registry grammar forbids this completely.
        mutant["semantic_authorities"]["entries"][0]["canonical_owner_ref"] = "standards/GITHUB_WORKFLOW.md"
        self.expect_rejected(mutant)
        mutant = deepcopy(self.manifest)
        mutant["semantic_authorities"]["entries"][1]["compatibility_alias_refs"] = ["standards/VERSION_INTEGRATION_WORKFLOW.md"]
        self.expect_rejected(mutant)

    def test_registry_cannot_grant_mutation_merge_or_release(self) -> None:
        for key in ("mutation_allowed", "merge_allowed", "side_effect_allowed", "release_ready", "normative_body"):
            mutant = deepcopy(self.manifest)
            mutant["semantic_authorities"]["entries"][0][key] = True
            self.expect_rejected(mutant)
        mutant = deepcopy(self.manifest)
        mutant["semantic_authorities"]["authorization"] = "ALLOW"
        self.expect_rejected(mutant)

    def test_optional_and_project_defined_are_discovery_not_adoption(self) -> None:
        self.assertEqual(
            {entry["applicability_posture"] for entry in self.manifest["semantic_authorities"]["entries"]}
            & {"OPTIONAL", "PROJECT_DEFINED"},
            {"OPTIONAL", "PROJECT_DEFINED"},
        )
        self.assertNotIn("adoption_required", self.schema["properties"])
        self.assertTrue(self.schema["additionalProperties"] is False)

    def test_bad_applicability_and_broken_applicability_ref_fail(self) -> None:
        mutant = deepcopy(self.manifest)
        mutant["semantic_authorities"]["entries"][0]["applicability_posture"] = "IMPLICIT_MANDATORY"
        self.expect_rejected(mutant)
        mutant = deepcopy(self.manifest)
        mutant["semantic_authorities"]["entries"][0]["applicability_refs"] = ["missing.md"]
        self.expect_rejected(mutant)


if __name__ == "__main__":
    unittest.main()
