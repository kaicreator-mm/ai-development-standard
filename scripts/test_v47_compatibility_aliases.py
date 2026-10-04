"""v4.7 T06 compatibility/alias conformance (derived, never authority).

The T02 registry and the merged T01 entry schema own the input vocabulary;
this test-only checker adds the Frozen T06 stable-path retention and complete
compatibility-inventory checks. It never moves paths or grants permissions.
"""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path, PurePosixPath
import unittest

from test_v47_authority_registry import RegistryError, resolve_registry

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "standard-manifest.json"
ENTRY_SCHEMA_PATH = ROOT / "schemas" / "authority-applicability-entry-v1.schema.json"

# These are the actual compatibility paths at this Task's reviewed JIT base.
# A future removal/replacement must be explicitly authorized and requalified;
# silently deleting both inventory and routing metadata cannot pass this suite.
STABLE_COMPATIBILITY_PATHS = frozenset(
    ("standards/GITHUB_WORKFLOW.md", "standards/VERSION_INTEGRATION_WORKFLOW.md")
)


class AliasConformanceError(RegistryError):
    """Fail closed rather than infer a unique compatible owner by file order."""


def _safe_repo_ref(ref: object) -> bool:
    """Accept only canonical POSIX repository-relative paths, not host paths."""
    if not isinstance(ref, str) or not ref or "\\" in ref or "\x00" in ref:
        return False
    path = PurePosixPath(ref)
    return (
        not path.is_absolute()
        and ref == path.as_posix()
        and ref != "."
        and ".." not in path.parts
        and ":" not in path.parts[0]
    )


def validate_current_aliases(
    manifest: object, entry_schema: dict, *, root: Path | None = None
) -> dict[str, str]:
    """Return stable alias -> canonical owner metadata, never an authority grant.

    Unlike the backwards-compatible T02 resolver, *current* T06 conformance
    requires an explicit usable v4.7 registry. Historic absent-field payloads
    remain readable by legacy consumers but cannot prove current alias safety.
    """
    if not isinstance(manifest, dict) or not isinstance(manifest.get("sections"), dict):
        raise AliasConformanceError("missing historical manifest inventory")
    sections = manifest["sections"]
    canonical = sections.get("normative_standards")
    compatibility = sections.get("compatibility_entries")
    if not isinstance(canonical, list) or not isinstance(compatibility, list):
        raise AliasConformanceError("missing normative or compatibility inventory")
    if any(not _safe_repo_ref(ref) for ref in canonical + compatibility):
        raise AliasConformanceError("noncanonical or unsafe repository path")
    if len(compatibility) != len(set(compatibility)):
        raise AliasConformanceError("duplicate legacy compatibility path")
    if not STABLE_COMPATIBILITY_PATHS.issubset(set(compatibility)):
        raise AliasConformanceError("stable pre-v4.7 compatibility entry removed")
    if set(canonical) & set(compatibility):
        raise AliasConformanceError("compatibility path promoted to normative owner")
    if "semantic_authorities" not in manifest:
        raise AliasConformanceError("current alias routing not present")

    # Reuse the *real* T02 schema/owner/one-hop resolver, no competing engine.
    # It rejects explicit-null envelopes, invalid entry fields, guessed owner,
    # duplicate aliases, recursion, unresolved applicability and absent files.
    resolve_registry(manifest, entry_schema, root=root)
    entries = manifest["semantic_authorities"]["entries"]
    mapping: dict[str, str] = {}
    for entry in entries:
        owner = entry["canonical_owner_ref"]
        if not _safe_repo_ref(owner):
            raise AliasConformanceError("unsafe canonical owner path")
        for alias in entry.get("compatibility_alias_refs", []):
            if not _safe_repo_ref(alias):
                raise AliasConformanceError("unsafe compatibility alias path")
            if alias in mapping:
                raise AliasConformanceError("alias claimed by multiple entries")
            if alias not in compatibility or owner not in canonical or alias == owner:
                raise AliasConformanceError("broken or non-normative alias route")
            mapping[alias] = owner

    if set(mapping) != set(compatibility):
        raise AliasConformanceError("unindexed compatibility entry or stray alias")
    if root is not None:
        for alias, owner in mapping.items():
            if not (root / alias).is_file() or not (root / owner).is_file():
                raise AliasConformanceError("broken on-disk stable alias or target")
    return dict(sorted(mapping.items()))


class CompatibilityAliasConformanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        cls.schema = json.loads(ENTRY_SCHEMA_PATH.read_text(encoding="utf-8"))

    def rejected(self, mutant: dict) -> None:
        with self.assertRaises(RegistryError):
            validate_current_aliases(mutant, self.schema)

    def test_live_inventory_every_alias_has_real_single_owner(self) -> None:
        result = validate_current_aliases(self.manifest, self.schema, root=ROOT)
        self.assertEqual(set(result), set(self.manifest["sections"]["compatibility_entries"]))
        self.assertEqual(set(result), STABLE_COMPATIBILITY_PATHS)
        self.assertEqual(
            result["standards/GITHUB_WORKFLOW.md"],
            "standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md",
        )
        self.assertEqual(
            result["standards/VERSION_INTEGRATION_WORKFLOW.md"],
            "standards/DEVELOPMENT_WORKFLOW.md",
        )
        self.assertTrue(set(result.values()).issubset(set(self.manifest["sections"]["normative_standards"])))

    def test_inventory_and_registry_iteration_order_cannot_choose_winner(self) -> None:
        reordered = deepcopy(self.manifest)
        reordered["sections"]["compatibility_entries"].reverse()
        reordered["semantic_authorities"]["entries"].reverse()
        self.assertEqual(
            validate_current_aliases(reordered, self.schema),
            validate_current_aliases(self.manifest, self.schema),
        )

    def test_silent_removal_from_both_inventory_and_metadata_still_fails(self) -> None:
        mutant = deepcopy(self.manifest)
        path = "standards/GITHUB_WORKFLOW.md"
        mutant["sections"]["compatibility_entries"].remove(path)
        for entry in mutant["semantic_authorities"]["entries"]:
            if path in entry.get("compatibility_alias_refs", []):
                entry["compatibility_alias_refs"].remove(path)
        self.rejected(mutant)  # original baseline commitment cannot disappear

    def test_unindexed_legacy_alias_fails_even_if_file_exists(self) -> None:
        mutant = deepcopy(self.manifest)
        for entry in mutant["semantic_authorities"]["entries"]:
            if "standards/GITHUB_WORKFLOW.md" in entry.get("compatibility_alias_refs", []):
                entry["compatibility_alias_refs"].remove("standards/GITHUB_WORKFLOW.md")
        self.rejected(mutant)

    def test_unknown_alias_fails_instead_of_guessing_existing_owner(self) -> None:
        mutant = deepcopy(self.manifest)
        mutant["sections"]["compatibility_entries"].append("standards/NEVER_COMMITTED.md")
        self.rejected(mutant)
        mutant["semantic_authorities"]["entries"][0]["compatibility_alias_refs"].append(
            "standards/NEVER_COMMITTED.md"
        )
        # Syntactically indexed but absent on disk: no presumed migration success.
        with self.assertRaises(RegistryError):
            validate_current_aliases(mutant, self.schema, root=ROOT)

    def test_alias_cannot_be_normative_owner(self) -> None:
        mutant = deepcopy(self.manifest)
        mutant["sections"]["normative_standards"].append("standards/GITHUB_WORKFLOW.md")
        self.rejected(mutant)
        mutant = deepcopy(self.manifest)
        mutant["semantic_authorities"]["entries"][1]["canonical_owner_ref"] = "standards/GITHUB_WORKFLOW.md"
        self.rejected(mutant)

    def test_alias_chain_cycle_and_duplicate_claim_fail(self) -> None:
        mutant = deepcopy(self.manifest)
        mutant["semantic_authorities"]["entries"][0]["canonical_owner_ref"] = (
            "standards/GITHUB_WORKFLOW.md"
        )
        self.rejected(mutant)  # a would-be chain/cycle requires alias-as-owner
        mutant = deepcopy(self.manifest)
        mutant["semantic_authorities"]["entries"][1]["compatibility_alias_refs"] = [
            "standards/VERSION_INTEGRATION_WORKFLOW.md"
        ]
        self.rejected(mutant)  # duplicate ownership regardless of entry order
        mutant["semantic_authorities"]["entries"].reverse()
        self.rejected(mutant)

    def test_disjoint_inventory_and_duplicate_legacy_paths_are_required(self) -> None:
        mutant = deepcopy(self.manifest)
        mutant["sections"]["compatibility_entries"].append("standards/GITHUB_WORKFLOW.md")
        self.rejected(mutant)
        mutant = deepcopy(self.manifest)
        mutant["sections"]["normative_standards"].append("standards/VERSION_INTEGRATION_WORKFLOW.md")
        self.rejected(mutant)

    def test_repo_path_traversal_and_noncanonical_spellings_fail(self) -> None:
        for path in ("../../escape.md", "/etc/shadow", "standards//extra.md", "standards\\extra.md", "C:/fake.md"):
            mutant = deepcopy(self.manifest)
            mutant["sections"]["compatibility_entries"].append(path)
            self.rejected(mutant)
            self.assertFalse(_safe_repo_ref(path))

    def test_explicit_null_and_historically_missing_registry_are_distinct(self) -> None:
        mutant = deepcopy(self.manifest)
        mutant["semantic_authorities"] = None
        self.rejected(mutant)
        historical = deepcopy(self.manifest)
        del historical["semantic_authorities"]
        self.rejected(historical)  # current conformance cannot guess aliases
        self.assertEqual(resolve_registry(historical, self.schema), {})  # legacy read still works

    def test_alias_metadata_never_authorizes_mutation_or_retirement(self) -> None:
        current = validate_current_aliases(self.manifest, self.schema)
        self.assertEqual(len(current), 2)
        for forbidden in ("is_normative_owner", "may_delete_legacy_path", "mutation_allowed", "release_ready"):
            mutant = deepcopy(self.manifest)
            mutant["semantic_authorities"]["entries"][0][forbidden] = True
            self.rejected(mutant)
        self.assertTrue(self.schema["additionalProperties"] is False)

    def test_reference_is_restricted_to_conformance_not_repository_move(self) -> None:
        reference = (ROOT / "references" / "COMPATIBILITY_ALIAS_CONFORMANCE.md").read_text(encoding="utf-8")
        for required in ("does **not** authorize moving", "separately authorized compatibility/migration", "cannot silently delete"):
            self.assertIn(required, reference)
        self.assertNotIn("physical_move_authorized", self.schema["properties"])


if __name__ == "__main__":
    unittest.main()
