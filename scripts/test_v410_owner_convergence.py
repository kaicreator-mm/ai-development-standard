"""V410-T06A R2 focused regression — owner convergence / discovery / legacy classification.

Executes against the real merged manifest and checkout (never a fixture copy).
Reuses the carried v4.7 resolver (`test_v47_authority_registry.resolve_registry`,
`RegistryError`), the carried v4.8 frozen-inventory guards
(`test_v48_registry_adoption.semantic_registry_problems`,
`section_conformance_problems`) and the carried alias conformance
(`test_v47_compatibility_aliases.validate_current_aliases`) by import, not by
reimplementation.

R2 resolution encoded here (evidence #860@6013810495): the candidate carries
**zero `standard-manifest.json` delta**. The seven material v4.10 owner families
without a discovery row stay recorded as routed gaps in
`references/V410_OWNER_AUTHORITY_CONVERGENCE_REFERENCE.md`; the registration
mechanism is routed to T06B (#861). This suite asserts the zero-delta state
(manifest blob identity), the truthful gap documentation, and the fail-closed
boundaries; if a future authorized amendment (guards + manifest together) lands,
these assertions are the ones that must be consciously updated in that task.

Purely local; no network, no runtime execution.
"""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
import re
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from test_v47_authority_registry import RegistryError, resolve_registry  # noqa: E402
from test_v47_compatibility_aliases import validate_current_aliases  # noqa: E402
import test_v48_registry_adoption as t48  # noqa: E402

MANIFEST = ROOT / "standard-manifest.json"
ENTRY_SCHEMA = ROOT / "schemas" / "authority-applicability-entry-v1.schema.json"
REFERENCE = ROOT / "references" / "V410_OWNER_AUTHORITY_CONVERGENCE_REFERENCE.md"
PACK_R2 = ROOT / ".agent" / "execution" / "V410-T06A-R2"

BASE_SHA = "eea3e69be5ac3e9c1a78f19e9bdf243ad9c58601"
MANIFEST_BLOB = "21730a0251e35e13591d2c84de1c66d6ab2c2408"
R3_HISTORICAL_HEAD = "e03beedd9d02336407365efa66efc43d34e96954"

V47_ENTRY_IDS = {
    "development-lifecycle",
    "github-agent-coordination",
    "execution-state",
    "work-item-contract",
    "validation-evidence",
    "release-qualification",
    "runner-capability",
    "research-demo",
    "task-learning-evidence",
    "logical-agent-capability-profile",
    "agent-capability-evidence",
}

ALIASES = {
    "standards/GITHUB_WORKFLOW.md": "standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md",
    "standards/VERSION_INTEGRATION_WORKFLOW.md": "standards/DEVELOPMENT_WORKFLOW.md",
}

# Material v4.10 owner families with no current discovery row (routed gaps, §1.2).
GAP_FAMILIES = (
    "standards/TASK_DECOMPOSITION_STANDARD.md",
    "standards/TASK_DAG_GOVERNANCE_STANDARD.md",
    "standards/EXECUTION_PACK_STANDARD.md",
    "standards/IMPLEMENTATION_QUALITY_STANDARD.md",
    "standards/INTERFACE_COMPATIBILITY_GOVERNANCE_STANDARD.md",
    "standards/PROJECT_ADOPTION.md",
    "standards/REFERENCE_CONVENTION_STANDARD.md",
)

CORE_OWNERS = (
    "standards/DEVELOPMENT_WORKFLOW.md",
    "standards/EXECUTION_ARCHITECTURE_STANDARD.md",
    "standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md",
    "standards/VALIDATION_STANDARD.md",
    "standards/RELEASE_STANDARD.md",
    "standards/REFERENCE_CONVENTION_STANDARD.md",
    "standard-manifest.json",
)


REQUIREMENT_TOKENS = ("R1 ", "R2 ", "R3 ", "R4 ", "R6 ", "R7 ", "R11 ", "R12 ")


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def reference_text() -> str:
    return REFERENCE.read_text(encoding="utf-8")


def load_schema() -> dict:
    return json.loads(ENTRY_SCHEMA.read_text(encoding="utf-8"))


def expect_rejected(test: unittest.TestCase, mutant: dict) -> None:
    with test.assertRaises(RegistryError):
        resolve_registry(mutant, load_schema())


class OwnerResolutionTests(unittest.TestCase):
    """P1/P2/P3: unique resolution, truthful coverage, manifest invariants."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        cls.reference = reference_text()

    def test_unique_owner_resolution_is_order_invariant(self) -> None:
        schema = load_schema()
        baseline = resolve_registry(self.manifest, schema, root=ROOT)
        reordered = deepcopy(self.manifest)
        reordered["semantic_authorities"]["entries"].reverse()
        for section, values in reordered["sections"].items():
            reordered["sections"][section] = list(reversed(values))
        self.assertEqual(resolve_registry(reordered, schema, root=ROOT), baseline)

    def test_gap_families_resolved_in_the_reference(self) -> None:
        # W13 resolution: six families registered via the authorized evolution;
        # reference-convention resolves through the explicit L2 §3 composition.
        for owner in GAP_FAMILIES[:6]:
            with self.subTest(owner=owner):
                self.assertIn(owner, self.reference)
        self.assertIn("CURRENT (registry growth, #861 W13)", self.reference)
        self.assertIn("CURRENT (composition)", self.reference)
        self.assertIn("RESOLVED_BY_AUTHORIZED_V410_EVOLUTION", self.reference)
        self.assertIn("guard and the manifest together", self.reference)

    def test_referenced_owner_paths_exist_in_checkout(self) -> None:
        owners = set(re.findall(r"`(standards/[A-Za-z0-9_]+\.md)`", self.reference))
        self.assertTrue(owners)
        for owner in sorted(owners):
            with self.subTest(owner=owner):
                self.assertTrue((ROOT / owner).is_file(), owner)

    def test_core_owners_are_bound_in_the_reference(self) -> None:
        for owner in CORE_OWNERS:
            with self.subTest(owner=owner):
                self.assertIn(owner, self.reference)

    def test_gap_family_rows_are_registered_verbatim(self) -> None:
        entries = self.manifest["semantic_authorities"]["entries"]
        by_id = {entry["entry_id"]: entry for entry in entries}
        expected = {
            "task-decomposition": "standards/TASK_DECOMPOSITION_STANDARD.md",
            "task-dag-governance": "standards/TASK_DAG_GOVERNANCE_STANDARD.md",
            "execution-pack": "standards/EXECUTION_PACK_STANDARD.md",
            "implementation-quality": "standards/IMPLEMENTATION_QUALITY_STANDARD.md",
            "interface-compatibility": "standards/INTERFACE_COMPATIBILITY_GOVERNANCE_STANDARD.md",
            "project-adoption": "standards/PROJECT_ADOPTION.md",
        }
        for entry_id, owner in expected.items():
            with self.subTest(entry_id=entry_id):
                self.assertEqual(by_id[entry_id]["canonical_owner_ref"], owner)
        # composition family: no registry row, resolves via L2 §3 composition
        self.assertNotIn("reference-convention", by_id)

    def test_manifest_growth_preserves_all_carried_invariants(self) -> None:
        # W13 consciously superseded the T06A-era zero-delta pin: the manifest
        # moved under the authorized co-evolution. Invariants that must hold
        # instead: schema_version=1, the 11 legacy entry ids intact, and the
        # six growth rows exactly as authorized.
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        entries = manifest["semantic_authorities"]["entries"]
        self.assertEqual(len(entries), 17)
        self.assertEqual({e["entry_id"] for e in entries[:11]}, V47_ENTRY_IDS)
        growth_ids = ("task-decomposition", "task-dag-governance", "execution-pack",
                      "implementation-quality", "interface-compatibility", "project-adoption")
        self.assertEqual({e["entry_id"] for e in entries[11:]}, set(growth_ids))

    def test_carried_frozen_inventory_guards_pass_on_the_real_manifest(self) -> None:
        # These are the machine reason the candidate carries zero manifest delta.
        self.assertEqual(t48.section_conformance_problems(self.manifest), [])
        self.assertEqual(t48.semantic_registry_problems(self.manifest), [])

    def test_guard_amendment_is_exactly_the_authorized_w13_set(self) -> None:
        # W13: the T06B task IS the authorized amender; the amendment must be
        # exactly the landed set (1 reference + 3 verification files) beyond
        # the historical v4.8 additions, which remain untouched.
        authorized = t48.AUTHORIZED_SECTION_ADDITIONS
        historical_refs = {
            "references/AUTHORITY_APPLICABILITY_REGISTRY_REFERENCE.md",
            "references/COMPATIBILITY_ALIAS_CONFORMANCE.md",
            "references/PROGRESSIVE_DISCLOSURE_ROUTING.md",
            "references/REFERENCE_CONVENTION_REFERENCE.md",
            "references/STATE_DIMENSION_REGISTRY_REFERENCE.md",
            "references/V48_REGISTRY_ADOPTION_REFERENCE.md",
        }
        self.assertEqual(
            authorized.get("references") - historical_refs,
            {"references/V410_OWNER_AUTHORITY_CONVERGENCE_REFERENCE.md"},
        )
        new_ver = authorized.get("verification", set()) & {
            "scripts/test_v410_owner_convergence.py",
            "scripts/test_v410_t06b_multi_dispatch_conformance.py",
            "scripts/test_v410_t06b_core_inventory.py",
        }
        self.assertEqual(len(new_ver), 3)
        self.assertEqual(len(t48.V410_T06A_GROWTH_ENTRIES), 6)

    def test_reference_and_tests_are_manifest_registered(self) -> None:
        # W13 resolution: the discovery surfaces are registered through the
        # authorized evolution (references + verification sections).
        registered = {rel for values in self.manifest["sections"].values() for rel in values}
        self.assertIn("references/V410_OWNER_AUTHORITY_CONVERGENCE_REFERENCE.md", registered)
        self.assertIn("scripts/test_v410_owner_convergence.py", registered)
        self.assertIn("scripts/test_v410_t06b_multi_dispatch_conformance.py", registered)
        self.assertIn("scripts/test_v410_t06b_core_inventory.py", registered)

    def test_registry_is_discovery_metadata_not_authority(self) -> None:
        for entry in self.manifest["semantic_authorities"]["entries"]:
            for forbidden in ("mutation_allowed", "merge_allowed", "release_ready", "normative_body"):
                self.assertNotIn(forbidden, entry)


class AliasBoundaryTests(unittest.TestCase):
    """P4/N7: one-hop aliases, non-owners, deletion cannot pass."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    def test_aliases_resolve_one_hop_and_are_never_owners(self) -> None:
        schema = load_schema()
        resolved = validate_current_aliases(self.manifest, schema, root=ROOT)
        self.assertEqual(resolved, ALIASES)
        normative = set(self.manifest["sections"]["normative_standards"])
        for alias in ALIASES:
            self.assertNotIn(alias, normative)
        for entry in self.manifest["semantic_authorities"]["entries"]:
            self.assertNotIn(entry["canonical_owner_ref"], ALIASES)

    def test_alias_removal_from_both_inventories_cannot_pass(self) -> None:
        mutant = deepcopy(self.manifest)
        mutant["sections"]["compatibility_entries"].remove("standards/GITHUB_WORKFLOW.md")
        mutant["semantic_authorities"]["entries"][1]["compatibility_alias_refs"] = []
        with self.assertRaises(RegistryError):
            validate_current_aliases(mutant, load_schema(), root=ROOT)


class FailClosedMutantTests(unittest.TestCase):
    """N1/N2/N3/N4: fail closed, no fallback winner, no guessed owner."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    def test_competing_owner_fails_both_orders(self) -> None:
        for reverse in (False, True):
            with self.subTest(reverse=reverse):
                mutant = deepcopy(self.manifest)
                contender = deepcopy(mutant["semantic_authorities"]["entries"][0])
                contender["entry_id"] = "competing"
                contender["canonical_owner_ref"] = "standards/RELEASE_STANDARD.md"
                mutant["semantic_authorities"]["entries"].append(contender)
                if reverse:
                    mutant["semantic_authorities"]["entries"].reverse()
                expect_rejected(self, mutant)

    def test_broken_targets_fail_closed(self) -> None:
        variants = []
        missing_owner = deepcopy(self.manifest)
        missing_owner["semantic_authorities"]["entries"][0]["canonical_owner_ref"] = "standards/DOES_NOT_EXIST.md"
        variants.append(missing_owner)
        alias_promoted = deepcopy(self.manifest)
        alias_promoted["semantic_authorities"]["entries"][0]["canonical_owner_ref"] = "standards/GITHUB_WORKFLOW.md"
        variants.append(alias_promoted)
        alias_double_claim = deepcopy(self.manifest)
        alias_double_claim["semantic_authorities"]["entries"][1]["compatibility_alias_refs"] = [
            "standards/VERSION_INTEGRATION_WORKFLOW.md"
        ]
        variants.append(alias_double_claim)
        escaping = deepcopy(self.manifest)
        escaping["semantic_authorities"]["entries"][3]["canonical_owner_ref"] = "../standards/X.md"
        variants.append(escaping)
        for mutant in variants:
            with self.subTest(owner=mutant["semantic_authorities"]["entries"][0]["canonical_owner_ref"]):
                expect_rejected(self, mutant)

    def test_historical_surface_never_wins_current_owner_resolution(self) -> None:
        # N3: a version-labelled historical reference is not a normative owner.
        mutant = deepcopy(self.manifest)
        mutant["semantic_authorities"]["entries"][0]["canonical_owner_ref"] = (
            "references/V48_REGISTRY_ADOPTION_REFERENCE.md"
        )
        expect_rejected(self, mutant)
        reference = reference_text()
        self.assertIn(R3_HISTORICAL_HEAD, reference)
        self.assertIn("HISTORICAL", reference)
        self.assertIn("never current authority", reference)

    def test_registry_growth_is_authorized_and_complete(self) -> None:
        reference = reference_text()
        self.assertIn("RESOLVED by the authorized W13 evolution", reference)
        self.assertIn("guard and the manifest together", reference)
        self.assertIn("a builder never amends a guard unilaterally", reference)
        # The growth is real: exactly six registered rows + one composition.
        entries = self.manifest["semantic_authorities"]["entries"]
        self.assertEqual(len(entries), len(V47_ENTRY_IDS) + 6)
        self.assertNotIn("reference-convention", {e["entry_id"] for e in entries})


class NonAuthorityBoundaryTests(unittest.TestCase):
    """N5/N6/P8: declarations, no resolver/runtime claims, reconstructibility."""

    def test_non_authority_declarations_present(self) -> None:
        reference = reference_text()
        for token in ("authority_effect=NONE", "gate_effect=NONE", "mutation_authorized=false"):
            self.assertIn(token, reference)
        self.assertIn("not** a runtime registry", reference)
        self.assertIn("does not supersede", reference)

    def test_no_executable_resolution_contract_in_reference(self) -> None:
        reference = reference_text()
        for forbidden in ("MUST resolve", "authoritative registry", "precedence over", "runtime contract is"):
            self.assertNotIn(forbidden, reference)

    def test_fresh_observer_requirement_tokens_present(self) -> None:
        reference = reference_text()
        for token in REQUIREMENT_TOKENS:
            with self.subTest(token=token):
                self.assertIn(token, reference)

    def test_extension_points_are_declared_for_conformance_owners(self) -> None:
        reference = reference_text()
        self.assertIn("T06B(#861)", reference)
        self.assertIn("NO_GREEN_BY_DELETION", reference)


class CandidateShapeTests(unittest.TestCase):
    """P9/N9: candidate diffs stay inside owned surfaces; upstream owners untouched.

    T06A-history note: this assertion originally pinned the exact 14-path T06A
    candidate diff on `task/v4.10.0-v410-t06a-owner-convergence` (merged as PR
    #925, base eea3e69). V410-T06B (#861, base ab8339f) consciously re-scopes it
    per the T06A-routed registry-growth disposition: successor candidates assert
    forbidden-surface exclusion plus an explicit owned-path allowlist instead of
    an exact closed set, because the T06B candidate intentionally evolves schemas,
    prose, verifier and (under its W13 authorized co-evolution) the manifest and
    carried guards.
    """

    T06B_BASE_SHA = "ab8339f83a6a2308a5aa39009bd126698320ceee"

    # Surfaces the T06B candidate may touch (write set of
    # .agent/execution/V410-T06B-R1/EXECUTION_CONTRACT.md, plus its own pack).
    T06B_ALLOWED_PREFIXES = (
        ".agent/execution/V410-T06B-R1/",
        "schemas/dispatch.schema.json",
        "schemas/execution-state.schema.json",
        "schemas/agent-event-v2.schema.json",
        "standards/EXECUTION_ARCHITECTURE_STANDARD.md",
        "standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md",
        "templates/agent-event-comment.md",
        "scripts/v34_rules.py",
        "scripts/test_v410_t06b_multi_dispatch_conformance.py",
        "scripts/test_v410_t06b_core_inventory.py",
        "scripts/test_protocol_schemas.py",
        "scripts/test_execution_architecture.py",
        "scripts/test_v34_lifecycle_contracts.py",
        "scripts/verify_standard.py",
        "standard-manifest.json",
        "scripts/test_v48_registry_adoption.py",
        "scripts/test_v410_owner_convergence.py",
        "references/V410_OWNER_AUTHORITY_CONVERGENCE_REFERENCE.md",
    )

    # Upstream semantic-owner standards and frozen authorities that must never
    # appear in ANY successor candidate diff (N9).
    FORBIDDEN_PATHS = (
        "standards/DEVELOPMENT_WORKFLOW.md",
        "standards/TASK_DECOMPOSITION_STANDARD.md",
        "standards/TASK_DAG_GOVERNANCE_STANDARD.md",
        "standards/IMPLEMENTATION_QUALITY_STANDARD.md",
        "standards/INTERFACE_COMPATIBILITY_GOVERNANCE_STANDARD.md",
        "standards/PROJECT_ADOPTION.md",
        "standards/VALIDATION_STANDARD.md",
        "standards/RELEASE_STANDARD.md",
        "docs/implementation/4.10.0/L2_ARCHITECTURE_EVIDENCE.md",
        "docs/implementation/4.10.0/TASK_PACKS_R1.md",
    )

    def test_candidate_diff_never_touches_forbidden_surfaces(self) -> None:
        changed = self._changed_paths()
        violations = sorted(changed & set(self.FORBIDDEN_PATHS))
        self.assertEqual(violations, [])

    def test_t06b_candidate_diff_stays_inside_owned_surfaces(self) -> None:
        changed = self._changed_paths(self.T06B_BASE_SHA)
        outside = sorted(
            path for path in changed if not path.startswith(self.T06B_ALLOWED_PREFIXES)
        )
        self.assertEqual(outside, [])

    def _changed_paths(self, base: str = BASE_SHA) -> set[str]:
        result = subprocess.run(
            ["git", "diff", "--name-only", base, "--"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            self.fail(f"cannot diff against {base}: {result.stderr.strip()}")
        return {line.strip() for line in result.stdout.splitlines() if line.strip()}

    def test_pack_r2_core_inventory_is_complete(self) -> None:
        for rel in (
            "MANIFEST.yaml",
            "EXECUTION_CONTRACT.md",
            "TEST_MATRIX.yaml",
            "FAILURE_MATRIX.yaml",
            "IMPLEMENTATION_MAP.md",
            "REVIEW_CHECKLIST.md",
        ):
            with self.subTest(rel=rel):
                self.assertTrue((PACK_R2 / rel).is_file())


if __name__ == "__main__":
    result = unittest.TextTestRunner(verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
    )
    raise SystemExit(0 if result.wasSuccessful() else 1)
