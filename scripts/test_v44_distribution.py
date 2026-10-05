from __future__ import annotations

from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
STANDARD = ROOT / "standards" / "DISTRIBUTION_GOVERNANCE_STANDARD.md"
REFERENCE = ROOT / "references" / "DISTRIBUTION_REFERENCE.md"


class DistributionGovernanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.standard = STANDARD.read_text(encoding="utf-8")
        cls.reference = REFERENCE.read_text(encoding="utf-8")

    def test_mutable_alias_is_not_immutable_identity(self) -> None:
        self.assertIn("MUST remain distinguishable from canonical immutable artifact identity", self.standard)
        self.assertIn("tag/channel/package-name points somewhere -> exact qualified bytes established", self.standard)

    def test_publication_binds_immutable_artifact_where_supported(self) -> None:
        self.assertIn(
            "Where the publication system supports immutable binding, a distribution claim MUST bind the publication to the immutable artifact identity",
            self.standard,
        )
        self.assertIn("immutable_binding_evidence_ref", self.reference)

    def test_provider_without_immutable_binding_fails_closed(self) -> None:
        self.assertIn("does not expose an immutable-binding mechanism", self.standard)
        self.assertIn("MUST record that limitation", self.standard)
        self.assertIn("mutable locator alone remains insufficient proof of bytes identity", self.standard)

    def test_repointed_alias_does_not_inherit_prior_qualification(self) -> None:
        self.assertIn("prior qualification/publication evidence for the old immutable artifact MUST NOT transfer", self.standard)
        self.assertIn("qualification for the prior digest does not transfer", self.reference)

    def test_publication_success_is_not_deployment_success(self) -> None:
        self.assertIn("publication success != Deployment success", self.standard)
        self.assertIn("does not prove that any target environment fetched, activated, rolled out or successfully ran", self.standard)

    def test_distribution_can_be_not_applicable(self) -> None:
        self.assertIn("Distribution is not mandatory for every product or change", self.standard)
        self.assertIn("Distribution NOT_APPLICABLE", self.reference)

    def test_no_artifact_release_or_deployment_authority_theft(self) -> None:
        self.assertIn("does not own canonical artifact bytes identity, Release qualification, or Deployment execution", self.standard)
        self.assertIn("v4.4 does not mandate a standalone Distribution schema", self.standard)

    def test_mutable_only_provider_fails_closed(self) -> None:
        self.assertIn("cannot expose immutable binding", self.standard)
        self.assertIn("Do not upgrade mutable locator evidence into canonical bytes identity", self.standard)


if __name__ == "__main__":
    unittest.main()
