from __future__ import annotations

from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
STANDARD = ROOT / "standards" / "REFERENCE_CONVENTION_STANDARD.md"
REFERENCE = ROOT / "references" / "REFERENCE_CONVENTION_REFERENCE.md"


class ReferenceConventionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.standard = STANDARD.read_text(encoding="utf-8")
        cls.reference = REFERENCE.read_text(encoding="utf-8")

    def test_exact_subject_and_expected_base_meanings_are_distinct(self) -> None:
        for token in ("requested_sha", "tested_sha", "expected_base_sha", "current_head_sha"):
            self.assertIn(token, self.standard)
        self.assertIn("requested subject, actually observed/executed subject and expected/current base", self.reference)

    def test_mutable_ref_cannot_replace_exact_sha(self) -> None:
        self.assertIn("MUST NOT substitute for an exact SHA", self.standard)
        self.assertIn("The branch name is a locator", self.reference)
        self.assertIn("it does not move with the branch", self.reference)

    def test_authority_ref_is_not_capability_ref(self) -> None:
        self.assertIn("capability_ref != authority_ref", self.standard)
        for token in ("credential", "provider", "model", "tool installation"):
            self.assertIn(token, self.standard)
        self.assertIn("Those facts may describe capability or provenance, not authorization", self.reference)

    def test_evidence_does_not_transfer_pass_or_authorize_mutation(self) -> None:
        self.assertIn("old exact-SHA PASS -> successor exact-SHA PASS", self.standard)
        self.assertIn("evidence_ref present != mutation authorized", self.standard)
        self.assertIn("cannot be reused as PASS for SHA B", self.reference)

    def test_provenance_is_not_normative_owner(self) -> None:
        self.assertIn("provenance_ref present != normative owner", self.standard)
        self.assertIn("does not make the builder/tool the normative owner", self.reference)

    def test_existing_owner_specific_names_remain_valid(self) -> None:
        self.assertIn("Existing contracts MAY retain field names", self.standard)
        self.assertIn("does not require historical payloads to rename fields", self.standard)
        self.assertIn("document the compatibility mapping", self.reference)

    def test_no_universal_subject_or_authority_object(self) -> None:
        self.assertIn("a universal Subject Identity object", self.standard)
        self.assertIn("a universal Authority object", self.standard)
        self.assertIn("does not create or require", self.standard)

    def test_cosmetic_normalization_does_not_authorize_rewrite(self) -> None:
        self.assertIn("Cosmetic consistency is not sufficient authority for a wire-format migration", self.standard)
        self.assertIn("historical schema rewrite authorized", self.standard)
        self.assertIn("do not rewrite historical payloads solely for aesthetics", self.reference)


if __name__ == "__main__":
    unittest.main()
