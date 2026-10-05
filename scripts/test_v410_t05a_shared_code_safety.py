"""V410-T05A R3 focused evidence: shared-code/reuse safety under existing owners.

Independent R3 re-execution evidence for issue #858 under a conformant
Execution Pack (`.agent/execution/V410-T05A-R3/`). The Task Pack asks for an
evidence-first residual-gap check over the three current owners; this suite
locks the owning clauses for the four frozen shared-code invariants:

1. importability does not imply a stable/public contract;
2. Task-local work cannot silently widen into project-wide promotion/refactor;
3. public compatibility remains owned by the compatibility authority;
4. textual similarity does not mandate extraction/DRY.

The suite pins the exact owner blob identities declared by the V410-T05A R3
JIT admission and re-read from the exact integration tree at claim time, so
any owner mutation fails closed and must be re-evidenced on its own exact
subject. It also binds the candidate to the R3 pack identity so a successor
cannot silently inherit this evidence after re-basing.

This Task performs NO owner mutation; the evidenced outcome is
`NO_CHANGE_REQUIRED`. Superseded PR #881 (`dba02f4f`) and PR #886
(`0d12bbfa`) are non-authoritative historical input; nothing here transfers
their Validation/Review/merge authority.

Authority: issue #858, Task Pack R1 V410-T05A (@3300f849), L3 Wave B R1
V410-T05A, Frozen L2 #842 §10.1, R3 Execution Pack
(.agent/execution/V410-T05A-R3 @1b6777cc).
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
STANDARDS = ROOT / "standards"
SCHEMAS = ROOT / "schemas"
REGISTRIES = ROOT / "registries"
REFERENCES = ROOT / "references"
PROFILES = ROOT / "profiles"
CHECKLISTS = ROOT / "checklists"
TEMPLATES = ROOT / "templates"
PROMPTS = ROOT / "prompts"
PACK = ROOT / ".agent" / "execution" / "V410-T05A-R3"
MANIFEST = ROOT / "standard-manifest.json"

IQS = STANDARDS / "IMPLEMENTATION_QUALITY_STANDARD.md"
TDS = STANDARDS / "TASK_DECOMPOSITION_STANDARD.md"
ICGS = STANDARDS / "INTERFACE_COMPATIBILITY_GOVERNANCE_STANDARD.md"
RCS = STANDARDS / "REFERENCE_CONVENTION_STANDARD.md"
EPS = STANDARDS / "EXECUTION_PACK_STANDARD.md"
L2 = ROOT / "docs" / "implementation" / "4.10.0" / "L2_ARCHITECTURE_EVIDENCE.md"

# Exact integration baseline and Task Pack identity declared by the V410-T05A
# R3 JIT admission (issue #858) and by the R3 pack manifest.
BASELINE_SHA = "7a0ee000174512df85bf3d2cd611e8b2cf55c840"
TASK_PACK_BLOB = "3300f8494ecb2120d96fff520cd09270b538344b"
TASK_BRANCH = "task/v4.10.0-v410-t05a-shared-code-safety-r3"
CORE_ARTIFACTS = (
    "MANIFEST.yaml",
    "EXECUTION_CONTRACT.md",
    "TEST_MATRIX.yaml",
    "FAILURE_MATRIX.yaml",
    "IMPLEMENTATION_MAP.md",
    "REVIEW_CHECKLIST.md",
)

# Owner blob identities declared by the V410-T05A R3 JIT admission (Issue
# #858) and re-read from the exact integration tree at claim time. A failing
# comparison here means the owner subject moved: this exact-subject evidence
# is stale and a fresh residual-gap re-evidencing is required.
OWNER_BLOBS = {
    IQS: "3beba2d0324d95674b7bad2ef621e2aa81c66563",
    TDS: "f355c020f07828a62ad617ffa80cb40b708ab4d4",
    ICGS: "266aefe32e0990c24fc8c1d6d731c4a3456fc3fc",
}

# The normative corpus the negative scan covers: every durable surface that
# could otherwise carry a reuse/extraction mandate.
CORPUS_DIRS = (STANDARDS, REFERENCES, PROFILES, CHECKLISTS, TEMPLATES, PROMPTS)
CORPUS_SUFFIXES = (".md", ".yaml", ".yml", ".json")
CORPUS_ROOT_FILES = ("README.md", "AGENTS.md", "CHANGELOG.md", "standard-manifest.json")

# A mandate is a rule that *requires* extraction/deduplication/reuse as such.
# The DRY acronym is matched case-sensitively and never inside "dry-run".
MANDATE_PATTERNS = (
    re.compile(r"\bDRY\b(?!\s*-?\s*run\b)"),
    re.compile(r"MUST\s+(?:always\s+)?(?:extract|deduplicat\w*|de-duplicat\w*|factor\s+out|consolidat\w*)", re.IGNORECASE),
    re.compile(r"(?:mandatory|required)\s+(?:extraction|deduplication|de-duplication|code\s+reuse|code\s+sharing)", re.IGNORECASE),
    re.compile(r"(?:extraction|deduplication|code\s+reuse|code\s+sharing)\s+(?:is|are)\s+(?:mandatory|required)", re.IGNORECASE),
    re.compile(r"\bDRY\s+(?:principle|mandate|rule|policy)\b", re.IGNORECASE),
)

# A similarity-triggered extraction rule: the exact rule shape the frozen
# invariant forbids. These must have zero hits anywhere in the corpus.
SIMILARITY_MANDATE_PATTERNS = (
    re.compile(
        r"similar\w*\s+(?:code|logic|implementation\w*|module\w*)[^.]{0,80}\b(?:MUST|SHOULD|shall|is required to)\b[^.]{0,40}\b(?:extract|deduplicat\w*|de-duplicat\w*|shar\w*|consolidat\w*|reus\w*)",
        re.IGNORECASE,
    ),
    re.compile(
        r"(?:duplicat\w*|de-duplicat\w*)\s+(?:code|logic|implementation\w*)[^.]{0,80}\b(?:MUST|SHOULD)\b[^.]{0,40}\b(?:extract|remov\w*|eliminat\w*|factor\w*|consolidat\w*)",
        re.IGNORECASE,
    ),
    re.compile(r"similarity\s+(?:mandates|requires|implies|creates)\s+(?:extraction|DRY|sharing|deduplication)", re.IGNORECASE),
    re.compile(r"(?:extract|factor\s+out|deduplicat\w*|consolidat\w*)\s+(?:any\s+)?(?:similar|duplicated?|shared)\s+(?:code|logic)", re.IGNORECASE),
    re.compile(r"(?:code|logic)\s+(?:reuse|duplication)\s+(?:is|are)\s+(?:MUST|mandatory|required)", re.IGNORECASE),
)

# Context that forbids, rather than requires, an action.
NEGATION_MARKER = re.compile(
    r"\b(?:not|no|never|neither|nor|cannot|can't|MUST\s+NOT|SHOULD\s+NOT|forbidden|forbid\w*|invalid|illegal|"
    r"without|instead\s+of|rather\s+than|prohibit\w*|must\s+never|does\s+not|do\s+not|is\s+not|are\s+not)\b",
    re.IGNORECASE,
)

# A DRY/component owner family is exactly what the frozen R5 disposition
# forbids creating. These names would indicate one appeared anyway.
FORBIDDEN_OWNER_TOKENS = (
    "shared-code",
    "shared code",
    "component registry",
    "shared component",
    "code reuse policy",
    "extraction policy",
)


def normalized_text(path: Path) -> str:
    """Read a repository file as the exact bytes git hashed.

    The working tree may be checked out with CRLF (`core.autocrlf`), so the
    newline form is normalized before any identity computation.
    """
    return path.read_bytes().decode("utf-8").replace("\r\n", "\n")


def git_blob_sha(text: str) -> str:
    payload = text.encode("utf-8")
    return hashlib.sha1(b"blob %d\x00" % len(payload) + payload).hexdigest()


def corpus_files() -> list[Path]:
    files: list[Path] = []
    for directory in CORPUS_DIRS:
        if directory.is_dir():
            files.extend(
                sorted(
                    p
                    for p in directory.rglob("*")
                    if p.is_file() and p.suffix.lower() in CORPUS_SUFFIXES
                )
            )
    for rel in CORPUS_ROOT_FILES:
        path = ROOT / rel
        if path.is_file():
            files.append(path)
    return files


def sentences(text: str) -> list[str]:
    """Split prose into sentence-ish units so a negation in one sentence is
    never read as licensing a mandate in the next."""
    return [s for s in re.split(r"(?<=[.;:!?])\s+|\n\s*[-*]\s+", text) if s.strip()]


def owner_mutation_message(path: Path) -> str:
    return (
        f"{path.name} no longer matches the exact owner blob pinned by the "
        "V410-T05A R3 admission. This suite is exact-subject evidence; a "
        "changed owner requires fresh re-evidencing, not a silent pass."
    )


class ExactSubjectBindingTests(unittest.TestCase):
    """The evidence is bound to one exact owner/baseline/pack subject."""

    def test_owner_blob_identities_are_pinned(self) -> None:
        for path, expected in OWNER_BLOBS.items():
            with self.subTest(owner=path.name):
                self.assertTrue(path.is_file(), f"owner standard missing: {path}")
                self.assertEqual(
                    git_blob_sha(normalized_text(path)),
                    expected,
                    owner_mutation_message(path),
                )

    def test_r3_pack_identity_is_bound(self) -> None:
        self.assertTrue(PACK.is_dir(), f"R3 execution pack missing: {PACK}")
        present = sorted(p.name for p in PACK.iterdir() if p.is_file())
        self.assertEqual(present, sorted(CORE_ARTIFACTS), "R3 pack core inventory is not the exact six-name set")
        manifest = normalized_text(PACK / "MANIFEST.yaml")
        for artifact in CORE_ARTIFACTS:
            self.assertEqual(manifest.count(artifact), 1, f"core artifact not declared exactly once: {artifact}")
        for fact in (
            f"base_sha: {BASELINE_SHA}",
            f"branch: {TASK_BRANCH}",
            f"pinned_standard_revision: {BASELINE_SHA}",
            "task_id: V410-T05A",
            "version: v4.10.0",
            "pack_state_at_generation: PACK_CURRENT",
            'parent_issue: "#858"',
        ):
            self.assertIn(fact, manifest, f"R3 pack manifest does not declare: {fact}")

    def test_frozen_l2_invariants_are_the_evaluated_requirement(self) -> None:
        text = normalized_text(L2)
        self.assertIn("14. **Reuse is semantic, not textual.** Importability is not a public contract and similarity is not a DRY mandate.", text)
        self.assertIn("No Shared Component Product requirement or registry is created.", text)
        self.assertIn("universal component registry is not required.", text)


class ImportabilityIsNotPublicContractTests(unittest.TestCase):
    """Invariant 1: a reusable/importable artifact is not thereby a contract."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.icgs = normalized_text(ICGS)
        cls.iqs = normalized_text(IQS)

    def test_compatibility_requires_explicit_contract_identity(self) -> None:
        # A compatibility claim needs a canonical contract identity; a mutable
        # alias or a derived/generated artifact may not substitute for it.
        self.assertIn("canonical contract kind/identity", self.icgs)
        self.assertIn(
            "A mutable branch name, tag, package alias, generated client name, or current provider state MUST NOT substitute",
            self.icgs,
        )

    def test_no_operation_name_implies_a_universal_result(self) -> None:
        self.assertIn("No operation name implies a universal compatibility result.", self.icgs)
        self.assertIn("`add` does not universally mean compatible;", self.icgs)
        self.assertIn("successful generation does not prove consumer compatibility.", self.icgs)

    def test_unevaluated_is_not_compatible(self) -> None:
        self.assertIn("Absence of a dimension means **not evaluated**, not compatible.", self.icgs)
        self.assertIn("An outcome for one dimension MUST NOT be promoted into another dimension without direct evidence.", self.icgs)

    def test_newest_consumer_success_does_not_cover_older_consumers(self) -> None:
        # Reuse breadth is not evidence: the newest consumer is not the window.
        self.assertIn("A provider and its newest consumer changing together MUST NOT hide breakage for", self.icgs)
        self.assertIn("external consumers outside the producer repository", self.icgs)

    def test_generation_success_is_not_contract_authority(self) -> None:
        self.assertIn("Generated SDKs, clients, stubs, documentation, or codegen output are subordinate derivations of a canonical contract.", self.icgs)
        self.assertIn("`generated client exists -> compatible` is a forbidden inference.", self.icgs)

    def test_forbidden_inference_matrix_preserved(self) -> None:
        for row in (
            "| wire-safe | source compatible |",
            "| schema/checker passes | behavior compatible |",
            "| new provider + new consumer pass | old/external consumer compatible |",
            "| dimension missing or `UNKNOWN` | compatible |",
            "| generated client/codegen succeeds | generated artifact is contract authority or proves compatibility |",
        ):
            self.assertIn(row, self.icgs, f"ICGS §10 matrix row missing: {row}")
        self.assertIn("Implementations and conformance tests MUST preserve these negatives.", self.icgs)

    def test_apparently_additive_edit_cannot_skip_compatibility_evidence(self) -> None:
        # The "I only extracted/moved a helper" reasoning is explicitly barred
        # from using Fast Path to bypass compatibility evidence.
        self.assertIn(
            "a small diff, generated change, documentation-only wrapper, or apparently additive edit MUST NOT use Fast Path to bypass compatibility evidence when a material consumer contract changes.",
            self.icgs,
        )

    def test_unknown_contract_identity_is_not_manufactured_into_compatibility(self) -> None:
        self.assertIn("MUST retain that uncertainty", self.icgs)
        self.assertIn("Missing execution is never a compatibility PASS.", self.icgs)

    def test_cross_module_observable_behavior_requires_an_explicit_contract(self) -> None:
        self.assertIn(
            "When implementation behavior is externally or cross-module observable, public contracts and error behavior MUST be explicit enough",
            self.iqs,
        )
        self.assertIn("Interface compatibility remains owned by the applicable compatibility authority.", self.iqs)

    def test_public_surface_widening_is_the_defect_form(self) -> None:
        self.assertIn("unnecessary public-surface widening or abstraction", self.iqs)
        self.assertIn("Implementation convenience MUST NOT silently narrow an existing compatibility contract", self.iqs)


class NoSilentTaskLocalWideningTests(unittest.TestCase):
    """Invariant 2: declared scope cannot silently become the project's scope."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.tds = normalized_text(TDS)
        cls.iqs = normalized_text(IQS)
        cls.eps = normalized_text(EPS)

    def test_write_set_and_forbidden_scope_are_required_durable_facts(self) -> None:
        for fact in ("allowed write-set / ownership", "forbidden scope", "primary concern / goal"):
            self.assertIn(fact, self.tds, f"TDS §2 required Task fact missing: {fact}")
        self.assertIn("A Task is **Agent-dispatchable** only when a qualified Agent can resolve identity, allowed scope, required gates and completion from these durable facts", self.tds)

    def test_one_primary_concern_and_no_size_based_boundary(self) -> None:
        self.assertIn("One Task SHOULD have one primary concern that can be described without joining unrelated authority domains", self.tds)
        self.assertIn("File count, line count or estimated token count alone MUST NOT define Task boundaries.", self.tds)

    def test_atomicity_keeps_shared_invariants_together(self) -> None:
        self.assertIn("Keep a concern together when splitting would create one or more of:", self.tds)
        self.assertIn("shared state invariant that only holds after both branches merge", self.tds)

    def test_stacked_pr_and_fake_parallelism_are_bounded(self) -> None:
        self.assertIn("Stacked PR MUST NOT be used as the general representation of the Task DAG.", self.tds)
        self.assertIn("Two Tasks are not safely parallel when each is only correct if the other unmerged branch is present.", self.tds)

    def test_central_wiring_is_not_a_semantic_rewrite_task(self) -> None:
        self.assertIn("Central wiring MUST reference sibling owners rather than become a semantic rewrite task.", self.tds)
        self.assertIn("Central wiring is integration, not semantic ownership.", normalized_text(L2))

    def test_split_and_readiness_anti_patterns_remain_normative(self) -> None:
        self.assertIn("is invalid unless those groups correspond to coherent independently valid concerns.", self.tds)
        self.assertIn(
            "A Task that simultaneously owns unrelated Product semantics, schema policy, CI redesign, UI behavior, deployment and release qualification should be split",
            self.tds,
        )
        self.assertIn("Deleting/ignoring a dependency, creating a branch early, or relabeling a Task READY does not make prerequisite truth exist.", self.tds)

    def test_hidden_scope_change_is_an_implementation_quality_defect(self) -> None:
        self.assertIn("a semantic change hidden outside the declared change scope", self.iqs)
        self.assertIn("unrelated formatting or generated churn mixed with a semantic change", self.iqs)

    def test_execution_pack_declares_and_bounds_the_write_set(self) -> None:
        self.assertIn("subordinate to Task Pack  may narrow, never redefine, task authority", self.eps)
        self.assertIn("allowed write set", self.eps)
        self.assertIn("forbidden scope", self.eps)

    def test_executor_freedom_cannot_be_silently_widened(self) -> None:
        self.assertIn("it MUST NOT be silently widened by an executor.", self.eps)
        self.assertIn("F1_BOUNDED_IMPLEMENTATION public contracts / invariants / test oracle fixed;", self.eps)
        self.assertIn("An executor MUST NOT self-promote F0/F1/F2 work into F3 authority", self.eps)


class CompatibilityAuthorityTests(unittest.TestCase):
    """Invariant 3: compatibility stays with the compatibility owner."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.icgs = normalized_text(ICGS)
        cls.iqs = normalized_text(IQS)

    def test_interface_compatibility_owner_verbatim(self) -> None:
        self.assertIn("Interface compatibility remains owned by the applicable compatibility authority.", self.iqs)

    def test_no_cross_owner_pass_manufacture(self) -> None:
        self.assertIn("A check passing under one owner MUST NOT manufacture PASS under another owner.", self.iqs)
        self.assertIn("Automated checks and tests remain the primary quality mechanism, and their passing alone never creates Validation or Release authority.", self.iqs)

    def test_compatibility_record_is_not_a_gate_result(self) -> None:
        self.assertIn("A Compatibility Record is evidence about a contract relationship. It is not a Gate result.", self.icgs)
        self.assertIn("compatibility outcomes by explicit, extensible dimension", self.icgs)

    def test_no_second_state_model_is_created(self) -> None:
        self.assertIn("without creating a second Validation, Release, Migration, Deployment, or workflow state model", self.icgs)
        self.assertIn("Its vocabulary is compatibility-domain vocabulary, not Validation/Release state vocabulary.", self.icgs)

    def test_authority_boundary_excludes_foreign_owners(self) -> None:
        for excluded in (
            "- Validation PASS/FAIL or exact-SHA evidence truth — Validation;",
            "- Release Qualification — Release;",
            "- canonical workflow/Gate states — existing workflow owners.",
        ):
            self.assertIn(excluded, self.icgs, f"ICGS §2 exclusion missing: {excluded}")


class NoTextualSimilarityExtractionMandateTests(unittest.TestCase):
    """Invariant 4: similarity never becomes a DRY/extraction obligation."""

    def test_corpus_has_no_extraction_mandate(self) -> None:
        for path in corpus_files():
            text = normalized_text(path)
            for pattern in MANDATE_PATTERNS:
                match = pattern.search(text)
                self.assertIsNone(
                    match,
                    f"{path.relative_to(ROOT)} mandates extraction/reuse: {match.group(0) if match else ''!r}",
                )

    def test_no_similarity_triggered_extraction_rule(self) -> None:
        for path in corpus_files():
            text = normalized_text(path)
            for pattern in SIMILARITY_MANDATE_PATTERNS:
                match = pattern.search(text)
                self.assertIsNone(
                    match,
                    f"{path.relative_to(ROOT)} makes textual similarity trigger extraction: "
                    f"{match.group(0) if match else ''!r}",
                )

    def test_dry_acronym_is_absent_or_forbidden(self) -> None:
        # The corpus must not use DRY as a governing acronym at all; if a
        # future edit introduces it, it may only appear in a forbidding or
        # explicitly negated sentence.
        for path in corpus_files():
            text = normalized_text(path)
            for sentence in sentences(text):
                if not MANDATE_PATTERNS[0].search(sentence):
                    continue
                self.assertIsNotNone(
                    NEGATION_MARKER.search(sentence),
                    f"{path.relative_to(ROOT)} asserts DRY as a rule: {sentence.strip()!r}",
                )

    def test_similarity_collapse_is_a_forbidden_inference(self) -> None:
        self.assertIn("| two fields look similar | meanings may be globally collapsed |", normalized_text(RCS))

    def test_unnecessary_abstraction_is_the_defect_form(self) -> None:
        # The owner makes the *unnecessary* abstraction the defect, i.e. the
        # opposite of a mandate to extract similar code.
        self.assertIn("unnecessary public-surface widening or abstraction", normalized_text(IQS))

    def test_no_universal_rule_posture_intact(self) -> None:
        iqs = normalized_text(IQS)
        self.assertIn("A missing ecosystem mechanism MUST NOT be replaced by a fabricated universal check.", iqs)
        self.assertIn("route it to the applicable language/archetype profile or project authority rather than inventing a universal rule", iqs)
        self.assertIn("Project overrides may specialize or strengthen applicable mappings; unresolved material conflicts fail closed to the owning project/architecture decision.", iqs)


class CorroboratingOwnerSurfaceNegativesTests(unittest.TestCase):
    """No shared-code/component owner family, registry or authority exists."""

    def test_no_component_registry_in_machine_contracts(self) -> None:
        self.assertFalse(
            [p.name for p in SCHEMAS.glob("*") if "component" in p.name or "shared" in p.name],
            "a component/shared-code machine contract appeared under schemas/",
        )
        self.assertFalse(
            [p.name for p in REGISTRIES.glob("*") if "component" in p.name or "shared" in p.name],
            "a component/shared-code registry appeared under registries/",
        )

    def test_manifest_has_no_shared_code_authority(self) -> None:
        manifest = json.loads(normalized_text(MANIFEST))
        authorities = manifest.get("semantic_authorities", {})
        entries = authorities.get("entries", []) if isinstance(authorities, dict) else []
        haystack = " ".join(
            f"{entry.get('entry_id', '')} {entry.get('semantic_concern', '')} {entry.get('canonical_owner_ref', '')}"
            for entry in entries
            if isinstance(entry, dict)
        ).lower()
        for token in ("shared", "component", "reuse"):
            self.assertNotIn(token, haystack, f"standard-manifest.json declares a shared/component semantic authority: {token}")

    def test_no_shared_code_owner_standard(self) -> None:
        offenders = [
            p.name
            for p in STANDARDS.glob("*.md")
            if any(token in p.name.lower().replace("_", "-") for token in ("shared", "component", "reuse"))
        ]
        self.assertFalse(offenders, f"a shared-code/component owner standard appeared: {offenders}")

    def test_no_shared_code_owner_language_in_declared_surfaces(self) -> None:
        for rel in ("README.md", "AGENTS.md", "standard-manifest.json"):
            text = normalized_text(ROOT / rel).lower()
            for token in FORBIDDEN_OWNER_TOKENS:
                self.assertNotIn(token, text, f"{rel} declares a forbidden owner surface: {token}")

    def test_existing_compatibility_owner_still_declares_its_scope(self) -> None:
        icgs = normalized_text(ICGS)
        self.assertIn("## 1. Purpose", icgs)
        self.assertIn("This standard owns interface/contract compatibility semantics.", icgs)
        self.assertIn("This owner is intentionally mechanism-neutral.", icgs)


if __name__ == "__main__":
    unittest.main()
