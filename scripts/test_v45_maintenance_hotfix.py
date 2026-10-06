from __future__ import annotations

from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
STANDARD = ROOT / "standards" / "MAINTENANCE_EOL_HOTFIX_STANDARD.md"
REFERENCE = ROOT / "references" / "MAINTENANCE_EOL_HOTFIX_REFERENCE.md"


class MaintenanceHotfixTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.standard = STANDARD.read_text(encoding="utf-8")
        cls.reference = REFERENCE.read_text(encoding="utf-8")

    def test_support_line_is_explicit_authority_not_branch_existence(self) -> None:
        self.assertIn("MUST be established by durable project/product maintenance authority", self.standard)
        for token in ("branch exists != line is supported", "tag exists != line is supported", "package downloadable != line is supported"):
            self.assertIn(token, self.standard)

    def test_support_vocabulary_is_extensible(self) -> None:
        self.assertIn("project-mappable/extensible", self.standard)
        self.assertIn("does not impose a universal lifecycle enum", self.standard)

    def test_deprecation_eol_and_upgrade_refs_are_representable(self) -> None:
        self.assertIn("Deprecation/EOL decisions MUST have durable authority", self.standard)
        self.assertIn("replacement/upgrade/migration guidance", self.standard)

    def test_backport_provenance_binds_source_baseline_and_result(self) -> None:
        for token in ("source change/reference", "target support line", "target baseline before change", "resulting exact SHA/artifact identity"):
            self.assertIn(token, self.standard)
        for token in ("source_ref", "target_baseline_ref", "result_sha_ref", "validation_refs"):
            self.assertIn(token, self.reference)

    def test_source_pass_does_not_transfer_to_backport(self) -> None:
        self.assertIn("source PASS != backport result PASS", self.standard)
        self.assertIn("same patch text != same validated subject", self.standard)
        self.assertIn("must obtain its own applicable current Testing/Validation/Review/Release evidence", self.standard)

    def test_hotfix_fast_path_cannot_skip_required_gates(self) -> None:
        self.assertIn("MAY reduce only ceremony", self.standard)
        self.assertIn("MUST NOT bypass material exact-subject Validation", self.standard)
        self.assertIn("does not convert required exact-SHA gates into optional gates", self.reference)


if __name__ == "__main__":
    unittest.main()
