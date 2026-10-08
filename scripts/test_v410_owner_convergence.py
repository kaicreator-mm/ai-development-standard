"""V410-T06A R2 focused regression — owner convergence / discovery / legacy classification.

Executes against the real merged manifest and checkout (never a fixture copy).
Reuses the carried v4.7 resolver (`test_v47_authority_registry.resolve_registry`,
`RegistryError`), the carried v4.8 frozen-inventory guards
(`test_v48_registry_adoption.semantic_registry_problems`,
`section_conformance_problems`) and the carried alias conformance
(`test_v47_compatibility_aliases.validate_current_aliases`) by import, not by
reimplementation.

Historical T06A R2 evidence (#860@6013810495) had zero
`standard-manifest.json` delta and routed the seven discovery gaps to T06B.
The current T06B/W13 candidate consciously supersedes that historical premise:
guard + manifest evolved together, six owner-family rows were added (11 -> 17),
the convergence reference and three verification files are registered, and the
reference-convention concern resolves through the explicit composition rule.
This suite now asserts that authorized evolved state while preserving the
carried v4.7/v4.8 invariants and fail-closed boundaries.

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
# Historical pre-W13 manifest blob (T06A-era lineage only; the current candidate
# manifest moved under the authorized #861 W13 co-evolution — see W13 facts).
T06A_HISTORICAL_MANIFEST_BLOB = "21730a0251e35e13591d2c84de1c66d6ab2c2408"
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

# Material v4.10 owner families asserted as the landed W13 state: the first six
# are registered via the authorized #861 W13 evolution (11 -> 17); the seventh
# (reference-convention) resolves by explicit composition (§1.2). Historical
# context: these were the T06A-era discovery rows before that evolution.
W13_GROWTH_OWNER_FAMILIES = (
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

    def test_growth_owner_families_resolved_in_the_reference(self) -> None:
        # W13 resolution: six families registered via the authorized evolution;
        # reference-convention resolves through the explicit L2 §3 composition.
        for owner in W13_GROWTH_OWNER_FAMILIES[:6]:
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

    def test_growth_family_rows_are_registered_verbatim(self) -> None:
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
        # Current truth: the carried v4.8 guards accept exactly the authorized
        # W13 co-evolution while preserving the embedded baseline invariants —
        # guard and manifest moved together (case-H; RA-01 rewrite impossible).
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

    V410-T07B rebind (#863, dispatch V410-T07B-BUILDER-R1, pre-authorized by the
    fast-path handoff #863@6046064159): the T07B successor candidate registered
    its OWN TASK_CANDIDATES entry (base cea2e0cc = merged PR #933 tip, T07B's
    own prefixes) and the active flag moved accordingly — the registry's own
    designed rebind mechanism. Zero removed tests; no other assertion weakened.

    V410-T07A R2 rebind (#862, dispatch V410-T07A-BOUNDED-REPAIR-R2): measuring
    every successor tree against the frozen T06B base with T06B's whole-repo
    allowlist was positional — it structurally failed on the T07A candidate
    (1/23 red at 43edc1f: the 8 T07A add-paths reported as "outside"). Rebound
    successor-aware while preserving the original T06B guard intent: the frozen
    INTEGRATED T06B delta (ab8339f...0518202c, merged PR #927) stays asserted
    against T06B_ALLOWED_PREFIXES, and each task's candidate delta is scoped to
    its OWN registered prefixes via TASK_CANDIDATES, with the active candidate
    measured base -> committed HEAD and failing LOUD when an unregistered
    successor extends the tree. Zero removed tests; no other assertion weakened.

    V410-T07B R2 seam-rebind scoping fold (#863, dispatch
    V410-T07B-BOUNDED-SEAM-REBIND-R2): the authorized seam write set (the T07A
    focused suite + the pin-bearing projection/IMPLEMENTATION_MAP/TEST_MATRIX
    files) is registered into T07B_ALLOWED_PREFIXES exactly as authorized — a
    registry scoping line with disclosure, zero removed tests; the rebound
    T07A suite carries the matching successor-aware registry.

    V410-T08A rebind (#864, dispatch V410-T08A-BUILDER-R1, pre-authorized by
    the fast-path handoff #864@6046066388 and the positional-registry seam
    discipline of the T08A admission #864@6055469682): the T08A successor
    candidate registered its OWN TASK_CANDIDATES entry (base 402bf289 = merged
    PR #934 tip, T08A's own prefixes) and the active flag moved accordingly —
    the registry's own designed rebind mechanism. The registry edits are
    disclosed carried-suite rebinds; zero removed tests; no other assertion
    weakened.
    """

    T06B_BASE_SHA = "ab8339f83a6a2308a5aa39009bd126698320ceee"
    # Merged T06B candidate tip (PR #927): the integration base every successor
    # candidate builds on, and the frozen subject of the historical T06B delta
    # assertion below.
    T06B_INTEGRATED_SHA = "0518202c715dcf91784a694bdf4a8eeeaeb16ab6"

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

    # Surfaces the V410-T07A candidate may touch: the 8 add-paths of its R1
    # candidate expressed as 3 prefixes, plus the one carried-suite path the
    # R2 bounded repair (dispatch V410-T07A-BOUNDED-REPAIR-R2) is authorized
    # to rebind — this guard itself, with zero removed tests.
    T07A_ALLOWED_PREFIXES = (
        ".agent/execution/V410-T07A-R1/",
        "docs/implementation/4.10.0/PRODUCT_ACCEPTANCE_EVIDENCE_PROJECTION_R1.md",
        "scripts/test_v410_t07a_acceptance_projection.py",
        "scripts/test_v410_owner_convergence.py",
    )

    # Surfaces the V410-T07B candidate may touch (its registered successor
    # write set), plus the ONE carried-suite path this pre-authorized rebind
    # itself edits — this guard, with zero removed tests (fast-path handoff
    # #863@6046064159: the successor task registers its own entry; never
    # widen another task's scope).
    #
    # R3 seam-rebind scoping fold (dispatch V410-T07B-BOUNDED-SEAM-REBIND-R2,
    # #863: proposal @6054504547 / admission @6054508480 / claim @6054512382):
    # the four explicitly authorized seam paths are registered here exactly as
    # authorized — a registry scoping line only, mirroring the rebound T07A
    # suite's TASK_CANDIDATES entry; never a widening beyond the disclosure.
    T07B_ALLOWED_PREFIXES = (
        ".agent/execution/V410-T07B-R1/",
        "templates/product-decision-record.md",
        "references/PRODUCT_DECISION_RECORD_REFERENCE.md",
        "checklists/version-closure.md",
        "scripts/test_v410_t07b_decision_record.py",
        "scripts/test_v410_owner_convergence.py",
        "scripts/test_v410_t07a_acceptance_projection.py",
        "docs/implementation/4.10.0/PRODUCT_ACCEPTANCE_EVIDENCE_PROJECTION_R1.md",
        ".agent/execution/V410-T07A-R1/IMPLEMENTATION_MAP.md",
        ".agent/execution/V410-T07A-R1/TEST_MATRIX.yaml",
    )

    # Successor-aware candidate registry (family-style): each task's candidate
    # delta is scoped to its OWN allowed prefixes instead of every successor
    # being measured against T06B's whole-repo allowlist. T06B and T07A are
    # frozen at their integrated tips; the single entry flagged active=True is
    # measured from its base to the CURRENT committed HEAD (fail loud on
    # ancestry loss — never a silent skip). A successor task rebinds by adding
    # its own entry and moving the active flag — never by widening another
    # task's prefixes.
    T07B_BASE_SHA = "cea2e0ccd045e8fcebaf110273129b198ed259fd"
    # V410-T08A candidate base (the merged PR #934 integration tip = T07B
    # INTEGRATED — T08A's own registered base).
    T07B_INTEGRATED_SHA = "402bf2899a7e1cd43eea3e7d78a37c947fe28c46"

    # Surfaces the V410-T08A candidate may touch (its registered successor
    # write set): the runner + focused suite + pack, plus the DISCLOSED
    # registry-rebind and pin-convergence paths of this task
    # (dispatch V410-T08A-BUILDER-R1): the three positional registries
    # (this guard, the T07A suite registry, the T07B suite registered-prefix
    # guard) and the mechanically-forced blob-pin cascade (T07A projection
    # record row R2 + IMPLEMENTATION_MAP row R2 + the T07B reference citation
    # + T07A TEST_MATRIX provenance row). Never a widening of another task's
    # scope — every non-T08A path here is a disclosed convergence line.
    T08A_ALLOWED_PREFIXES = (
        ".agent/execution/V410-T08A-R1/",
        "scripts/run_v410_integration.py",
        "scripts/test_v410_t08a_integration_runner.py",
        "scripts/test_v410_owner_convergence.py",  # disclosed TASK_CANDIDATES registry rebind
        "scripts/test_v410_t07a_acceptance_projection.py",  # disclosed registry rebind
        "scripts/test_v410_t07b_decision_record.py",  # disclosed registry rebind
        "docs/implementation/4.10.0/PRODUCT_ACCEPTANCE_EVIDENCE_PROJECTION_R1.md",  # R2-row pin convergence
        ".agent/execution/V410-T07A-R1/IMPLEMENTATION_MAP.md",  # R2-row pin convergence
        ".agent/execution/V410-T07A-R1/TEST_MATRIX.yaml",  # rebind provenance record
        "references/PRODUCT_DECISION_RECORD_REFERENCE.md",  # index-blob citation convergence
    )

    # Successor-aware candidate registry (family-style): each task's candidate
    # delta is scoped to its OWN allowed prefixes instead of every successor
    # being measured against T06B's whole-repo allowlist. T06B, T07A and T07B
    # are frozen at their integrated tips; the single entry flagged active=True
    # is measured from its base to the CURRENT committed HEAD (fail loud on
    # ancestry loss — never a silent skip). A successor task rebinds by adding
    # its own entry and moving the active flag — never by widening another
    # task's prefixes.
    TASK_CANDIDATES = (
        {
            "task": "V410-T06B",
            "base": T06B_BASE_SHA,
            "integrated": T06B_INTEGRATED_SHA,
            "prefixes": T06B_ALLOWED_PREFIXES,
        },
        {
            "task": "V410-T07A",
            "base": T06B_INTEGRATED_SHA,
            "integrated": T07B_BASE_SHA,
            "r1_tip": "43edc1f325b04977b37c77d3ae5e82a96c75c398",
            "prefixes": T07A_ALLOWED_PREFIXES,
        },
        {
            "task": "V410-T07B",
            "base": T07B_BASE_SHA,
            "integrated": T07B_INTEGRATED_SHA,
            "prefixes": T07B_ALLOWED_PREFIXES,
        },
        {
            "task": "V410-T08A",
            "base": T07B_INTEGRATED_SHA,
            "prefixes": T08A_ALLOWED_PREFIXES,
            "active": True,
        },
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
        # R2 rebind: the ORIGINAL guard intent is preserved on the frozen
        # INTEGRATED T06B delta (merged PR #927) — deterministic regardless of
        # which successor candidate is active, so a mutated prefix list or a
        # fabricated integrated path still fails here.
        changed = self._changed_paths(self.T06B_BASE_SHA, self.T06B_INTEGRATED_SHA)
        outside = sorted(
            path for path in changed if not path.startswith(self.T06B_ALLOWED_PREFIXES)
        )
        self.assertEqual(outside, [])

    def test_t07a_candidate_diff_stays_inside_owned_surfaces(self) -> None:
        # Frozen regression for the recorded V410-T07A R1 candidate tip: its
        # 8 add-paths stay inside T07A's OWN prefixes (never measured against
        # T06B's allowlist).
        entry = self._candidate("V410-T07A")
        changed = self._changed_paths(entry["base"], entry["r1_tip"])
        outside = sorted(path for path in changed if not path.startswith(entry["prefixes"]))
        self.assertEqual(outside, [])

    def test_active_candidate_head_diff_stays_inside_registered_task_prefixes(self) -> None:
        # HEAD-relative successor scoping, fail loud (no silent skip): every
        # path committed since the active candidate's base must be inside the
        # active candidate's own prefixes. A successor candidate that extends
        # the tree without registering its own TASK_CANDIDATES entry fails
        # here with rebind instructions instead of silently passing.
        entry = self._active_candidate()
        if not self._is_ancestor(entry["base"], "HEAD"):
            self.fail(
                f"HEAD does not descend from the active candidate base "
                f"{entry['base']} ({entry['task']}); the active-candidate scope "
                "check cannot run — rebind TASK_CANDIDATES for this lineage "
                "(fail loud, no silent skip)"
            )
        changed = self._changed_paths(entry["base"], "HEAD")
        outside = sorted(path for path in changed if not path.startswith(entry["prefixes"]))
        self.assertEqual(
            outside,
            [],
            "paths outside the active candidate's registered prefixes; the "
            "successor task must rebind this guard by registering its own "
            "TASK_CANDIDATES entry (task/base/prefixes) — never by widening "
            "another task's scope",
        )

    def test_candidate_registry_is_wellformed(self) -> None:
        tasks = [entry["task"] for entry in self.TASK_CANDIDATES]
        self.assertTrue(tasks, "TASK_CANDIDATES must not be empty")
        self.assertEqual(len(tasks), len(set(tasks)), "duplicate task entries in TASK_CANDIDATES")
        self.assertEqual(
            [entry["task"] for entry in self.TASK_CANDIDATES if entry.get("active")],
            ["V410-T08A"],
            "exactly one active candidate entry is required",
        )
        for entry in self.TASK_CANDIDATES:
            with self.subTest(task=entry["task"]):
                self.assertTrue(entry["prefixes"], f"{entry['task']} has empty prefixes")
                for key in ("base", "integrated", "r1_tip"):
                    if key in entry:
                        self.assertTrue(
                            self._commit_exists(entry[key]),
                            f"{entry['task']} {key} {entry[key]} does not resolve to a commit",
                        )

    def _candidate(self, task: str) -> dict:
        return next(entry for entry in self.TASK_CANDIDATES if entry["task"] == task)

    def _active_candidate(self) -> dict:
        return next(entry for entry in self.TASK_CANDIDATES if entry.get("active"))

    def _changed_paths(self, base: str = BASE_SHA, head: str | None = None) -> set[str]:
        # head=None diffs the WORKING TREE against base (semantics kept for the
        # forbidden-surface guard); an explicit head pins a committed range
        # (base...head) for the frozen candidate assertions.
        spec = base if head is None else f"{base}...{head}"
        result = subprocess.run(
            ["git", "diff", "--name-only", spec, "--"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            self.fail(f"cannot diff against {spec}: {result.stderr.strip()}")
        return {line.strip() for line in result.stdout.splitlines() if line.strip()}

    def _is_ancestor(self, ancestor: str, descendant: str) -> bool:
        result = subprocess.run(
            ["git", "merge-base", "--is-ancestor", ancestor, descendant],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        if result.returncode not in (0, 1):
            self.fail(f"cannot test ancestry {ancestor} <- {descendant}: {result.stderr.strip()}")
        return result.returncode == 0

    def _commit_exists(self, sha: str) -> bool:
        result = subprocess.run(
            ["git", "cat-file", "-e", f"{sha}^{{commit}}"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        return result.returncode == 0

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
