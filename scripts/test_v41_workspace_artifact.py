from __future__ import annotations

from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
STANDARD = ROOT / "standards" / "WORKSPACE_ARTIFACT_STANDARD.md"
REFERENCE = ROOT / "references" / "WORKSPACE_ARTIFACT_REFERENCE.md"

CANONICAL_CLASSES = {
    "SOURCE",
    "GENERATED_SOURCE",
    "BUILD_OUTPUT",
    "CACHE",
    "RUNTIME_STATE",
    "TEST_ARTIFACT",
    "VALIDATION_EVIDENCE",
    "RELEASE_ARTIFACT",
    "SECRET_MATERIAL",
}


def destructive_cleanup_allowed(*, owner_known: bool, class_known: bool, reconstructable: bool) -> bool:
    return owner_known and class_known and reconstructable


def promotion_allowed(*, identity_bound: bool, authority_present: bool, prerequisites_satisfied: bool) -> bool:
    return identity_bound and authority_present and prerequisites_satisfied


class V41WorkspaceArtifactTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.standard = STANDARD.read_text(encoding="utf-8")
        cls.reference = REFERENCE.read_text(encoding="utf-8")

    def test_all_canonical_classes_are_defined(self) -> None:
        for artifact_class in CANONICAL_CLASSES:
            self.assertIn(f"`{artifact_class}`", self.standard)

    def test_cache_cannot_satisfy_evidence_requirement(self) -> None:
        self.assertIn("Cache contents MUST NOT be used as sole proof", self.standard)
        self.assertIn("Cache is not evidence", self.reference)

    def test_build_output_does_not_become_release_artifact_by_presence(self) -> None:
        self.assertIn("MUST NOT by itself constitute release promotion", self.standard)
        self.assertIn("Build output is not release artifact", self.reference)
        self.assertFalse(promotion_allowed(identity_bound=False, authority_present=True, prerequisites_satisfied=True))

    def test_runtime_state_is_not_disposable_cache_by_default(self) -> None:
        self.assertIn("not disposable cache by default", self.standard)
        self.assertIn("local Postgres data directory", self.reference)

    def test_unknown_unowned_state_cannot_be_destructively_cleaned(self) -> None:
        self.assertFalse(destructive_cleanup_allowed(owner_known=False, class_known=True, reconstructable=True))
        self.assertFalse(destructive_cleanup_allowed(owner_known=True, class_known=False, reconstructable=True))
        self.assertIn("Unknown ownership/classification fails closed", self.standard)
        self.assertIn("preserve/isolate/escalate", self.reference)

    def test_authorized_promotion_requires_identity_and_authority(self) -> None:
        self.assertTrue(promotion_allowed(identity_bound=True, authority_present=True, prerequisites_satisfied=True))
        self.assertFalse(promotion_allowed(identity_bound=True, authority_present=False, prerequisites_satisfied=True))
        self.assertFalse(promotion_allowed(identity_bound=False, authority_present=True, prerequisites_satisfied=True))
        self.assertIn("Promotion requires", self.standard)
        self.assertIn("authorized promotion binds digest", self.reference)

    def test_test_artifact_and_validation_evidence_are_distinct(self) -> None:
        self.assertIn("remains `TEST_ARTIFACT` until that binding exists", self.standard)
        self.assertIn("Copying the junit file to `evidence/` without the binding is insufficient", self.reference)

    def test_secret_material_cannot_flow_as_ordinary_evidence(self) -> None:
        self.assertIn("MUST NOT be promoted into ordinary `TEST_ARTIFACT`, `VALIDATION_EVIDENCE` or `RELEASE_ARTIFACT`", self.standard)
        self.assertIn("browser trace contains cookies or bearer tokens", self.reference)

    def test_v44_full_artifact_manifest_scope_is_preserved(self) -> None:
        self.assertIn("does **not** define the future full v4.4 build/package Artifact Manifest", self.standard)


if __name__ == "__main__":
    unittest.main()
