"""V410-T05A focused regressions: shared-code safety under existing owners.

Disposition: **NO_CHANGE_REQUIRED**.

Evidence-first residual-gap check over the integrated V410-T03A / V410-T03B
owner results plus Interface Compatibility. No concrete residual gap remains
for the four Task Pack invariants, so no owner standard is mutated and no
component registry, generic shared-code subsystem or DRY policy is introduced.

This suite locks the exact owning clauses that already preserve the invariants
and probes the negatives whose presence would indicate Product-scope
re-expansion.

Frozen owner identities proved, read from the exact baseline tree
`9029435c6bb06b583b19070a4ab0863d8f4be012`:

- `standards/IMPLEMENTATION_QUALITY_STANDARD.md` @ `3beba2d0324d95674b7bad2ef621e2aa81c66563`
- `standards/TASK_DECOMPOSITION_STANDARD.md` @ `f355c020f07828a62ad617ffa80cb40b708ab4d4`
- `standards/INTERFACE_COMPATIBILITY_GOVERNANCE_STANDARD.md` @ `266aefe32e0990c24fc8c1d6d731c4a3456fc3fc`

Authority: issue #858, Task Pack R1 V410-T05A, L3 Wave B R1 V410-T05A,
Frozen L2 #842 section 10.1 / 13, Frozen Product PRD section 11.

Negative evidence, stated explicitly:

- importability/reuse is never promoted to stable/public contract status by any
  owner clause; contract status requires explicit kind/identity plus
  baseline/candidate binding under the compatibility owner;
- task-local work cannot silently widen into project-wide promotion/refactor:
  hidden scope widening and unnecessary public-surface widening are reviewable
  implementation-quality defects, and the write set / freedom level of a Task
  cannot be silently widened;
- public compatibility stays with the compatibility authority and creates no
  second Validation/Release/Migration/Deployment/workflow state model;
- no normative standard mandates extraction or deduplication, and textual
  similarity carries no DRY authority;
- no component registry, shared-code semantic authority or shared-code owner
  standard exists or is required.

What is NOT proven here: that no future non-weakening owner evolution could
remove a locked clause. Any such edit fails this suite and must be re-evidenced
on its own exact subject.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "standard-manifest.json"
STANDARDS = ROOT / "standards"

IMPLEMENTATION_QUALITY = STANDARDS / "IMPLEMENTATION_QUALITY_STANDARD.md"
TASK_DECOMPOSITION = STANDARDS / "TASK_DECOMPOSITION_STANDARD.md"
INTERFACE_COMPATIBILITY = STANDARDS / "INTERFACE_COMPATIBILITY_GOVERNANCE_STANDARD.md"
EXECUTION_PACK = STANDARDS / "EXECUTION_PACK_STANDARD.md"

# A mandate would have to be phrased as a normative obligation to be authoritative.
EXTRACTION_MANDATE_RES = {
    "dry_token": re.compile(r"\bDRY\b"),
    "must_extract": re.compile(r"MUST\s+(?:extract|deduplicate|de-duplicate|factor)", re.IGNORECASE),
    "mandatory_extraction": re.compile(
        r"mandatory\s+(?:dry|extraction|deduplication|de-duplication|refactor)", re.IGNORECASE
    ),
    "required_extraction": re.compile(r"required\s+(?:dry|extraction|deduplication)", re.IGNORECASE),
}

# An inference that reuse/import alone mints contract status would appear as a
# positive permission, never as the prohibition these owners state.
CONTRACT_BY_REUSE_RES = {
    "importable_implies_contract": re.compile(
        r"importab\w*[^.\n]{0,60}(?:implies?|creates?|establishes?|makes?)[^.\n]{0,30}contract",
        re.IGNORECASE,
    ),
    "reuse_implies_contract": re.compile(
        r"reuse\w*[^.\n]{0,60}(?:implies?|creates?|establishes?)[^.\n]{0,30}(?:stable|public)\s+contract",
        re.IGNORECASE,
    ),
    "similarity_mandates_extraction": re.compile(
        r"similar\w*[^.\n]{0,60}(?:must|mandat\w+|require\w+)[^.\n]{0,40}(?:extract|deduplicat|shared)",
        re.IGNORECASE,
    ),
}


def standard_texts() -> dict[str, str]:
    return {
        path.name: path.read_text(encoding="utf-8")
        for path in sorted(STANDARDS.glob("*.md"))
    }


class ImportabilityIsNotContractStatusTests(unittest.TestCase):
    """Invariant 1: importability/reuse does not imply a stable/public contract."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.texts = standard_texts()

    def test_contract_status_requires_explicit_identity_and_binding(self) -> None:
        compatibility = self.texts[INTERFACE_COMPATIBILITY.name]
        # Contract status is an explicit act of identification/binding, not an
        # inference from a module being importable or already reused.
        self.assertIn("canonical contract kind/identity", compatibility)
        self.assertIn("A compatibility claim MUST identify the contract under analysis", compatibility)
        self.assertIn(
            "A mutable branch name, tag, package alias, generated client name, or current provider state "
            "MUST NOT substitute for the exact baseline/candidate identity when exact identity is material.",
            compatibility,
        )

    def test_derived_or_working_artifact_never_becomes_contract_authority(self) -> None:
        compatibility = self.texts[INTERFACE_COMPATIBILITY.name]
        self.assertIn(
            "It MUST NOT become the canonical contract authority merely because generation succeeded.",
            compatibility,
        )
        self.assertIn("`generated client exists -> compatible` is a forbidden inference.", compatibility)
        self.assertIn("Implementations and conformance tests MUST preserve these negatives.", compatibility)

    def test_cross_module_observability_does_not_redefine_compatibility_ownership(self) -> None:
        quality = self.texts[IMPLEMENTATION_QUALITY.name]
        self.assertIn("When implementation behavior is externally or cross-module observable", quality)
        self.assertIn(
            "Interface compatibility remains owned by the applicable compatibility authority.", quality
        )

    def test_no_owner_states_that_reuse_or_import_mints_contract_status(self) -> None:
        for name, pattern in CONTRACT_BY_REUSE_RES.items():
            for standard, text in self.texts.items():
                with self.subTest(rule=name, standard=standard):
                    self.assertIsNone(pattern.search(text))


class TaskLocalWorkCannotSilentlyWidenTests(unittest.TestCase):
    """Invariant 2: a Task cannot silently widen into project-wide promotion."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.texts = standard_texts()

    def test_hidden_scope_widening_is_a_reviewable_implementation_quality_defect(self) -> None:
        quality = self.texts[IMPLEMENTATION_QUALITY.name]
        self.assertIn("the following mutation patterns are reviewable implementation-quality defects", quality)
        self.assertIn("- a semantic change hidden outside the declared change scope;", quality)

    def test_unnecessary_public_surface_widening_is_a_reviewable_defect(self) -> None:
        quality = self.texts[IMPLEMENTATION_QUALITY.name]
        self.assertIn("- unnecessary public-surface widening or abstraction.", quality)

    def test_decomposition_owner_keeps_concern_boundary_and_central_wiring_pattern(self) -> None:
        decomposition = self.texts[TASK_DECOMPOSITION.name]
        self.assertIn("One Task SHOULD have one primary concern", decomposition)
        self.assertIn(
            "Central wiring MUST reference sibling owners rather than become a semantic rewrite task.",
            decomposition,
        )
        self.assertIn("### 10.2 Giant mixed-authority Task", decomposition)

    def test_write_set_and_freedom_level_cannot_be_silently_widened(self) -> None:
        pack = self.texts[EXECUTION_PACK.name]
        self.assertIn("allowed write set", pack)
        self.assertIn("forbidden scope", pack)
        self.assertIn("it MUST NOT be silently widened by an executor", pack)


class PublicCompatibilityOwnershipTests(unittest.TestCase):
    """Invariant 3: public compatibility stays with compatibility authority."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.texts = standard_texts()

    def test_interface_compatibility_ownership_is_explicit_in_quality_owner(self) -> None:
        self.assertIn(
            "Interface compatibility remains owned by the applicable compatibility authority.",
            self.texts[IMPLEMENTATION_QUALITY.name],
        )

    def test_compatibility_record_is_evidence_not_a_gate_result(self) -> None:
        compatibility = self.texts[INTERFACE_COMPATIBILITY.name]
        self.assertIn(
            "A Compatibility Record is evidence about a contract relationship. It is not a Gate result.",
            compatibility,
        )
        self.assertIn("The following are **not** owned here:", compatibility)

    def test_no_second_validation_release_or_workflow_state_model(self) -> None:
        compatibility = self.texts[INTERFACE_COMPATIBILITY.name]
        self.assertIn(
            "without creating a second Validation, Release, Migration, Deployment, or workflow state model",
            compatibility,
        )


class NoMandatoryExtractionOrDryAuthorityTests(unittest.TestCase):
    """Invariant 4: textual similarity does not mandate extraction/DRY."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.texts = standard_texts()

    def test_no_normative_standard_mandates_extraction_or_deduplication(self) -> None:
        for rule, pattern in EXTRACTION_MANDATE_RES.items():
            for standard, text in self.texts.items():
                with self.subTest(rule=rule, standard=standard):
                    self.assertIsNone(pattern.search(text))

    def test_abstraction_is_only_a_defect_when_unnecessary(self) -> None:
        # The owner form is the defect, not a mandate: extraction by similarity
        # alone produces an unnecessary abstraction and is reviewable as such.
        self.assertIn(
            "- unnecessary public-surface widening or abstraction.",
            self.texts[IMPLEMENTATION_QUALITY.name],
        )

    def test_quality_owner_keeps_no_universal_mandate_posture(self) -> None:
        quality = self.texts[IMPLEMENTATION_QUALITY.name]
        self.assertIn(
            "This standard does not mandate one formatter, linter, compiler, type checker, warning policy, "
            "coverage threshold, complexity threshold or build system globally.",
            quality,
        )
        self.assertIn("rather than inventing a universal rule", quality)


class NoSharedCodeSubsystemReExpansionTests(unittest.TestCase):
    """R5 stays EXISTING_OWNER_ONLY: no registry, subsystem or new owner."""

    def test_no_component_registry_artifact_exists(self) -> None:
        for surface in ("schemas", "registries"):
            for path in sorted((ROOT / surface).iterdir()):
                with self.subTest(surface=surface, path=path.name):
                    self.assertNotIn("component", path.name.lower())
                    self.assertNotIn("shared", path.name.lower())

    def test_no_shared_code_semantic_authority_entry_exists(self) -> None:
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        entries = manifest["semantic_authorities"]["entries"]
        self.assertTrue(entries)
        forbidden = ("shared", "component", "reuse", "dedup", "dry")
        for entry in entries:
            haystack = " ".join(
                str(entry.get(key, ""))
                for key in ("entry_id", "semantic_concern", "canonical_owner_ref")
            ).lower()
            with self.subTest(entry=entry.get("entry_id")):
                for token in forbidden:
                    self.assertNotIn(token, haystack)

    def test_no_shared_code_owner_standard_exists(self) -> None:
        for path in sorted(STANDARDS.glob("*.md")):
            name = path.name.lower()
            with self.subTest(standard=path.name):
                self.assertNotIn("shared_component", name)
                self.assertNotIn("shared-code", name)
                self.assertNotIn("reuse", name)

    def test_no_component_registry_language_in_normative_surface(self) -> None:
        pattern = re.compile(r"component[ _-]?registry|shared[ _-]component", re.IGNORECASE)
        for standard, text in standard_texts().items():
            with self.subTest(standard=standard):
                self.assertIsNone(pattern.search(text))


if __name__ == "__main__":
    unittest.main()
