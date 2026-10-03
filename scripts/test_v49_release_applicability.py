from __future__ import annotations

from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
STANDARD = ROOT / "standards" / "RELEASE_STANDARD.md"
REFERENCE = ROOT / "references" / "RELEASE_APPLICABILITY_REFERENCE.md"


class ReleaseApplicabilityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.standard = STANDARD.read_text(encoding="utf-8")
        cls.reference = REFERENCE.read_text(encoding="utf-8")

    def test_canonical_vocabulary_is_explicit(self) -> None:
        for value in (
            "REQUIRED_NOW",
            "DEFERRED_TO_VERSION_CLOSURE",
            "NOT_APPLICABLE",
            "UNKNOWN",
        ):
            self.assertIn(value, self.standard)
            self.assertIn(value, self.reference)

    def test_release_authority_owns_gate_by_subject_decision(self) -> None:
        self.assertIn("evaluated **per Release-owned gate × exact subject**", self.standard)
        self.assertIn("Release applicability is owned by this Release authority", self.standard)
        for forbidden_minter in ("Orchestrator", "Builder", "Reviewer", "Validator", "CI system"):
            self.assertIn(forbidden_minter, self.standard)

    def test_unknown_is_fail_closed(self) -> None:
        self.assertIn("`UNKNOWN` is fail-closed", self.standard)
        self.assertIn("stronger existing legal release path or produce `BLOCKED`", self.standard)
        self.assertIn("UNKNOWN => NOT_APPLICABLE", self.reference)

    def test_concern_decisions_do_not_aggregate_to_version_truth(self) -> None:
        self.assertIn("CONCERN_NOT_APPLICABLE\n!= VERSION_NOT_APPLICABLE", self.standard)
        self.assertIn("CONCERN_DEFERRED\n!= VERSION_GATE_SATISFIED", self.standard)
        self.assertIn("Version Closure evaluates the composed candidate", self.standard)
        self.assertIn("concern NOT_APPLICABLE => version NOT_APPLICABLE", self.reference)

    def test_deferral_is_not_gate_satisfaction(self) -> None:
        self.assertIn("the requirement is **not removed**", self.standard)
        self.assertIn("fresh Release-owned applicability evaluation at Version Closure", self.standard)
        self.assertIn("DEFERRED_TO_VERSION_CLOSURE => gate satisfied", self.reference)

    def test_migration_is_prospective_and_does_not_shorten_inflight_candidate(self) -> None:
        self.assertIn("A newly adopted applicability rule or profile is prospective", self.standard)
        self.assertIn("MUST NOT retroactively shorten gates", self.standard)
        self.assertIn("pre-existing mandatory release path remains in force", self.standard)

    def test_existing_release_lifecycle_is_preserved(self) -> None:
        for invariant in (
            "thaw/invalidation rules remain unchanged",
            "Hidden Validation remains independent evidence when required",
            "Final Closeout and Release Qualification remain distinct authority-bearing gates",
            "Task/PR PASS still does not imply Release PASS",
            "`NOT_RUN`/`BLOCKED` still cannot be converted to PASS",
        ):
            self.assertIn(invariant, self.standard)

    def test_low_risk_shortcuts_are_not_positive_release_proof(self) -> None:
        for invalid in (
            "risk:low => NOT_APPLICABLE",
            "files_changed=1 => NOT_APPLICABLE",
            "docs-only label => NOT_APPLICABLE",
            "PR PASS => VERSION RELEASE PASS",
        ):
            self.assertIn(invalid, self.reference)


if __name__ == "__main__":
    result = unittest.TextTestRunner(verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromTestCase(ReleaseApplicabilityTests)
    )
    raise SystemExit(0 if result.wasSuccessful() else 1)
