from __future__ import annotations

from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
STANDARD = ROOT / "standards" / "BUILD_ARTIFACT_GOVERNANCE_STANDARD.md"
REFERENCE = ROOT / "references" / "BUILD_ARTIFACT_REFERENCE.md"


class BuildArtifactGovernanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.standard = STANDARD.read_text(encoding="utf-8")
        cls.reference = REFERENCE.read_text(encoding="utf-8")
        cls.lower = cls.standard.lower()

    def test_exact_build_subject_is_required(self) -> None:
        for phrase in ("exact source revision", "build profile", "toolchain/runtime", "build output identity"):
            self.assertIn(phrase, self.lower)

    def test_material_profiles_are_distinct_build_subjects(self) -> None:
        self.assertIn("Materially different build profiles MUST remain distinct build subjects", self.standard)
        self.assertIn("debug vs release", self.standard)

    def test_build_output_cannot_self_promote(self) -> None:
        self.assertIn("build output. The output does not self-promote", self.standard)
        self.assertIn("build command succeeded -> artifact qualified/promoted", self.standard)

    def test_immutable_identity_is_not_mutable_alias(self) -> None:
        self.assertIn("Mutable names, filenames, tags, channels", self.standard)
        self.assertIn("same tag/channel/name -> same artifact bytes", self.standard)
        self.assertIn("locator, not immutable identity", self.reference)

    def test_rebuilt_bytes_do_not_inherit_old_qualification(self) -> None:
        self.assertIn("New or rebuilt bytes MUST NOT inherit prior artifact Validation", self.standard)
        self.assertIn("evidence for B1 does not transfer to B2", self.reference)

    def test_package_content_policy_rejects_material_leakage(self) -> None:
        for phrase in (
            "secret or credential values",
            "local caches and temporary build state",
            "runtime state/databases",
            "Agent/session-only files",
            "private keys/signing material",
        ):
            self.assertIn(phrase, self.standard)

    def test_no_release_distribution_or_deployment_authority(self) -> None:
        self.assertIn("does not own Release Qualification, Distribution publication, Deployment result", self.standard)
        self.assertIn("Neither object is a Release verdict", self.standard)
        self.assertIn("artifact exists | Distribution or Deployment succeeded", self.standard)

    def test_provider_specific_mechanism_is_not_global_mandate(self) -> None:
        self.assertIn("does not impose one universal reproducible-build level or provider mechanism", self.standard)
        self.assertIn("remain profile/project authority", self.standard)


if __name__ == "__main__":
    unittest.main()
