"""V410-T05A focused evidence: shared-code/reuse safety under existing owners.

Independent R2 re-execution evidence for issue #858. The Task Pack asks for an
evidence-first residual-gap check over the three current owners; this suite
locks the owning clauses for the four shared-code invariants:

1. importability does not imply a stable/public contract;
2. Task-local work cannot silently widen into project-wide promotion/refactor;
3. public compatibility remains owned by the compatibility authority;
4. textual similarity does not mandate extraction/DRY.

The suite pins the exact owner blob identities declared by the V410-T05A R2
JIT admission, so any owner mutation fails closed and must be re-evidenced on
its own exact subject. This Task performs NO owner mutation; the evidenced
outcome is NO_CHANGE_REQUIRED. Historical PR #881 is non-authoritative input;
nothing here transfers its Validation/Review/merge authority.

Authority: issue #858, Task Pack R1 V410-T05A (@3300f849),
L3 Wave B R1 V410-T05A, R2 Execution Pack (.agent/execution/V410-T05A-R2).
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

IQS = STANDARDS / "IMPLEMENTATION_QUALITY_STANDARD.md"
TDS = STANDARDS / "TASK_DECOMPOSITION_STANDARD.md"
ICGS = STANDARDS / "INTERFACE_COMPATIBILITY_GOVERNANCE_STANDARD.md"
RCS = STANDARDS / "REFERENCE_CONVENTION_STANDARD.md"
EPS = STANDARDS / "EXECUTION_PACK_STANDARD.md"
MANIFEST = ROOT / "standard-manifest.json"

# Owner blob identities declared by the V410-T05A R2 JIT admission (Issue
# #858) and re-read from the exact integration tree at claim time. A failing
# comparison here means the owner subject moved: this exact-subject evidence
# is stale and a fresh residual-gap re-evidencing is required.
OWNER_BLOBS = {
    IQS: "3beba2d0324d95674b7bad2ef621e2aa81c66563",
    TDS: "f355c020f07828a62ad617ffa80cb40b708ab4d4",
    ICGS: "266aefe32e0990c24fc8c1d6d731c4a3456fc3fc",
}


def git_blob_sha(text: str) -> str:
    payload = text.encode("utf-8")
    return hashlib.sha1(b"blob %d\x00" % len(payload) + payload).hexdigest()


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def owner_mutation_message(path: Path) -> str:
    return (
        f"{path.name} no longer matches the exact owner blob pinned by the "
        "V410-T05A R2 admission. This suite is exact-subject evidence; a "
        "changed owner requires fresh re-evidencing, not a silent pass."
    )


class OwnerIdentityTests(unittest.TestCase):
    """The three declared owners are byte-identical to their claimed blobs."""

    def test_owner_blob_identities_are_pinned(self) -> None:
        for path, expected in OWNER_BLOBS.items():
            with self.subTest(owner=path.name):
                self.assertEqual(
                    git_blob_sha(read(path)),
                    expected,
                    owner_mutation_message(path),
                )


class ImportabilityIsNotContractTests(unittest.TestCase):
    """Invariant 1: importability/reuse is not a stable/public contract grant."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.icgs = read(ICGS)
        cls.iqs = read(IQS)

    def test_exact_contract_identity_binding_required(self) -> None:
        # ICGS §3: a compatibility claim must bind canonical contract
        # kind/identity plus both sides of the comparison — an import
        # relationship supplies none of these by itself.
        self.assertIn("1. canonical contract kind/identity;", self.icgs)
        self.assertIn("2. baseline identity;", self.icgs)
        self.assertIn("3. candidate identity;", self.icgs)
        self.assertIn(
            "A mutable branch name, tag, package alias, generated client "
            "name, or current provider state MUST NOT substitute for the "
            "exact baseline/candidate identity when exact identity is material.",
            self.icgs,
        )

    def test_no_operation_name_implies_universal_result(self) -> None:
        # ICGS §4: "we now import it" is a change operation at best, never
        # a compatibility outcome.
        self.assertIn(
            "No operation name implies a universal compatibility result.",
            self.icgs,
        )

    def test_generated_success_is_not_contract_authority(self) -> None:
        # ICGS §7: derived artifacts stay subordinate to the canonical contract.
        self.assertIn(
            "Generated output MAY provide evidence that a tool accepted a "
            "contract. It MUST NOT become the canonical contract authority "
            "merely because generation succeeded.",
            self.icgs,
        )
        self.assertIn(
            "`generated client exists -> compatible` is a forbidden inference.",
            self.icgs,
        )

    def test_forbidden_inference_matrix_preserved(self) -> None:
        # ICGS §10: the normative negatives a reuse story must not bypass.
        self.assertIn("| wire-safe | source compatible |", self.icgs)
        self.assertIn("| schema/checker passes | behavior compatible |", self.icgs)
        self.assertIn(
            "| new provider + new consumer pass | old/external consumer compatible |",
            self.icgs,
        )
        self.assertIn("| dimension missing or `UNKNOWN` | compatible |", self.icgs)
        self.assertIn(
            "| generated client/codegen succeeds | generated artifact is "
            "contract authority or proves compatibility |",
            self.icgs,
        )
        self.assertIn(
            "Implementations and conformance tests MUST preserve these negatives.",
            self.icgs,
        )

    def test_cross_module_observable_requires_explicit_contract(self) -> None:
        # IQS §5: cross-module observability demands explicit contracts; it
        # never says mere importability reaches that bar.
        self.assertIn(
            "When implementation behavior is externally or cross-module "
            "observable, public contracts and error behavior MUST be explicit "
            "enough for callers and tests to distinguish supported outcomes "
            "from technical failures.",
            self.iqs,
        )

    def test_no_importability_grants_contract_inference(self) -> None:
        # Negative corpus check: no owner sentence derives a stable/public
        # contract or compatibility grant from importability/reuse alone.
        pattern = re.compile(
            r"import\w*[^\n]{0,120}\b(?:implies|means|grants|is)\b"
            r"[^\n]{0,60}\b(?:stable|public|contract|compatib)",
            re.IGNORECASE,
        )
        for name, text in (("ICGS", self.icgs), ("IQS", self.iqs)):
            match = pattern.search(text)
            self.assertIsNone(
                match,
                f"{name} appears to grant contract status from "
                f"importability: {match.group(0) if match else ''!r}",
            )


class NoSilentWideningTests(unittest.TestCase):
    """Invariant 2: Task-local work cannot silently widen project-wide."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.tds = read(TDS)
        cls.iqs = read(IQS)
        cls.eps = read(EPS)

    def test_task_pack_write_set_facts_required(self) -> None:
        # TDS §2: allowed write-set and forbidden scope are required durable
        # Task facts, so widening has a declared boundary to violate.
        self.assertIn("allowed write-set / ownership", self.tds)
        self.assertIn("forbidden scope", self.tds)

    def test_primary_concern_boundary(self) -> None:
        # TDS §3: one primary concern per Task.
        self.assertIn("One Task SHOULD have one primary concern", self.tds)

    def test_central_wiring_references_sibling_owners(self) -> None:
        # TDS §8: central wiring references owners; it is not a rewrite vehicle.
        self.assertIn(
            "Central wiring MUST reference sibling owners rather than become "
            "a semantic rewrite task.",
            self.tds,
        )

    def test_giant_mixed_authority_task_is_antipattern(self) -> None:
        # TDS §10.2: smuggling promotion/refactor into a Task is an anti-pattern.
        self.assertIn("### 10.2 Giant mixed-authority Task", self.tds)
        self.assertIn(
            "should be split unless one atomic invariant truly requires them together.",
            self.tds,
        )

    def test_hidden_scope_widening_is_defect(self) -> None:
        # IQS §11: both widening forms are reviewable implementation-quality
        # defects when material.
        self.assertIn(
            "a semantic change hidden outside the declared change scope;",
            self.iqs,
        )
        self.assertIn(
            "unnecessary public-surface widening or abstraction.",
            self.iqs,
        )

    def test_execution_pack_declares_write_set(self) -> None:
        # EXECUTION_PACK_STANDARD §2: packs must declare allowed/forbidden scope.
        self.assertIn("allowed write set", self.eps)
        self.assertIn("forbidden scope", self.eps)

    def test_freedom_cannot_be_silently_widened(self) -> None:
        # EXECUTION_PACK_STANDARD §8: the executor cannot raise its own freedom.
        self.assertIn(
            "The freedom level is set by Task Pack / Execution Pack authority, "
            "not chosen by the executor.",
            self.eps,
        )
        self.assertIn(
            "A freedom level may be narrowed per dispatch; it MUST NOT be "
            "silently widened by an executor.",
            self.eps,
        )


class CompatibilityAuthorityTests(unittest.TestCase):
    """Invariant 3: public compatibility stays with the compatibility authority."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.iqs = read(IQS)
        cls.icgs = read(ICGS)

    def test_interface_compatibility_owner_verbatim(self) -> None:
        # IQS §5: the ownership sentence stays verbatim.
        self.assertIn(
            "Interface compatibility remains owned by the applicable "
            "compatibility authority.",
            self.iqs,
        )

    def test_no_cross_owner_pass_manufacture(self) -> None:
        # IQS §7: one owner's check cannot mint another owner's PASS.
        self.assertIn(
            "A check passing under one owner MUST NOT manufacture PASS under "
            "another owner.",
            self.iqs,
        )

    def test_compatibility_record_is_not_gate_result(self) -> None:
        # ICGS §2: compatibility evidence is not a Gate result.
        self.assertIn(
            "A Compatibility Record is evidence about a contract relationship. "
            "It is not a Gate result.",
            self.icgs,
        )

    def test_no_second_state_model(self) -> None:
        # ICGS §1: no second Validation/Release/Migration/Deployment/workflow
        # state model is created by the compatibility owner.
        self.assertIn(
            "without creating a second Validation, Release, Migration, "
            "Deployment, or workflow state model",
            self.icgs,
        )


class NoTextualSimilarityExtractionMandateTests(unittest.TestCase):
    """Invariant 4: textual similarity does not mandate extraction/DRY."""

    MANDATE_VERB = re.compile(
        r"\b(?:MUST|mandatory|requires|obligat\w+)\b", re.IGNORECASE
    )
    NEGATION = re.compile(
        r"MUST NOT|does not|do not|no universal|not automatic|MAY be",
        re.IGNORECASE,
    )
    SIMILARITY_TRIGGER = re.compile(
        r"textual\w* similar\w*|similar\w* (?:code|text|implementation)",
        re.IGNORECASE,
    )

    @classmethod
    def setUpClass(cls) -> None:
        cls.corpus: dict[str, str] = {
            path.name: read(path) for path in sorted(STANDARDS.glob("*.md"))
        }

    def sentences(self) -> "list[tuple[str, str]]":
        # Sentence-scoped so a negated clause elsewhere on the same line
        # cannot mask a mandate that sits in its own sentence.
        pairs = []
        for name, text in self.corpus.items():
            for line in text.splitlines():
                for sentence in re.split(r"(?<=\.)\s+", line):
                    if sentence.strip():
                        pairs.append((name, sentence))
        return pairs

    def flagged(self, pattern: re.Pattern[str]) -> list[str]:
        return [
            f"{name}: {sentence.strip()}"
            for name, sentence in self.sentences()
            if pattern.search(sentence) and not self.NEGATION.search(sentence)
        ]

    def test_no_mandatory_extraction_language(self) -> None:
        # No standard binds a mandate verb to the extraction family. A
        # negated/optional mention is fine; a mandate is the residual gap.
        self.assertEqual(
            [],
            self.flagged(
                re.compile(
                    self.MANDATE_VERB.pattern + r"[^\n]{0,120}"
                    r"\b(?:extract|deduplicat|factor)",
                    re.IGNORECASE,
                )
            ),
            "found a mandatory-extraction style mandate",
        )
        self.assertEqual(
            [],
            self.flagged(
                re.compile(
                    r"\bDRY\b[^\n]{0,120}" + self.MANDATE_VERB.pattern,
                    re.IGNORECASE,
                )
            ),
            "found a DRY mandate",
        )

    def test_no_similarity_triggered_extraction_rule(self) -> None:
        # No standard turns textual similarity itself into an extraction
        # authority; similarity is never the trigger of a MUST.
        pattern = re.compile(
            self.SIMILARITY_TRIGGER.pattern
            + r"[^\n]{0,120}(?:MUST|mandatory|extract)",
            re.IGNORECASE,
        )
        self.assertEqual([], self.flagged(pattern))

    def test_similarity_collapse_is_a_forbidden_inference(self) -> None:
        # REFERENCE_CONVENTION §8: "look similar -> globally collapsed" is a
        # normative forbidden inference, the inverse of an extraction mandate.
        rcs = read(RCS)
        self.assertIn(
            "| two fields look similar | meanings may be globally collapsed |",
            rcs,
        )
        self.assertIn("Do not normalize by guessing.", rcs)

    def test_unnecessary_abstraction_is_the_defect_form(self) -> None:
        # IQS §11: the quality owner's defect form is the *unnecessary*
        # abstraction — a mandated extraction would contradict the owner.
        self.assertIn(
            "unnecessary public-surface widening or abstraction.",
            self.corpus[IQS.name],
        )

    def test_no_universal_rule_posture_intact(self) -> None:
        # IQS §3/§10: the no-universal-mandate posture stays in place.
        iqs = self.corpus[IQS.name]
        self.assertIn(
            "This standard does not mandate one formatter, linter, compiler, "
            "type checker, warning policy, coverage threshold, complexity "
            "threshold or build system globally.",
            iqs,
        )
        self.assertIn(
            "rather than inventing a universal rule",
            iqs,
        )


class CorroboratingNegativeSurfaceTests(unittest.TestCase):
    """No shared-code subsystem/registry authority exists anywhere else."""

    def test_no_component_registry_artifact(self) -> None:
        schema_names = {path.name for path in SCHEMAS.glob("*.json")}
        registry_names = {path.name for path in REGISTRIES.glob("*.json")}
        self.assertEqual(
            {"state-dimensions-v1.json"},
            registry_names,
            "registries/ gained an unexpected registry artifact",
        )
        for names, label in ((schema_names, "schemas/"), (registry_names, "registries/")):
            intruders = [
                name
                for name in names
                if re.search(r"component|shared[-_]?code", name, re.IGNORECASE)
            ]
            self.assertEqual(
                [], intruders, f"{label} gained a shared-code/component artifact"
            )

    def test_manifest_has_no_shared_code_authority(self) -> None:
        manifest = json.loads(read(MANIFEST))
        entries = manifest["semantic_authorities"]["entries"]
        pattern = re.compile(r"shared|component|reuse", re.IGNORECASE)
        for entry in entries:
            searchable = " ".join(
                str(entry.get(key, ""))
                for key in ("entry_id", "semantic_concern", "canonical_owner_ref")
            )
            self.assertIsNone(
                pattern.search(searchable),
                f"semantic_authorities gained a shared-code entry: {searchable!r}",
            )

    def test_no_shared_code_owner_standard(self) -> None:
        intruders = [
            path.name
            for path in STANDARDS.glob("*.md")
            if re.search(r"component|shared[-_]?code", path.name, re.IGNORECASE)
        ]
        self.assertEqual([], intruders, "a shared-code owner standard appeared")


if __name__ == "__main__":
    unittest.main()
