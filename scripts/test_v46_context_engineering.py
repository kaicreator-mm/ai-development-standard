from __future__ import annotations

from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
STANDARD = ROOT / "standards" / "CONTEXT_ENGINEERING_STANDARD.md"
REFERENCE = ROOT / "references" / "CONTEXT_ENGINEERING_REFERENCE.md"


class ContextEngineeringTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.standard = STANDARD.read_text(encoding="utf-8")
        cls.reference = REFERENCE.read_text(encoding="utf-8")

    def test_authority_precedence_and_currentness_are_explicit(self) -> None:
        self.assertIn("highest-currentness applicable durable authority", self.standard)
        self.assertIn("Frozen Product / Architecture", self.standard)
        self.assertIn("Frozen Task DAG / Task Pack", self.standard)
        self.assertIn("live Issue / PR / exact Git identity", self.standard)
        self.assertIn("historical chat / memory", self.standard)

    def test_currentness_sensitive_action_requires_live_reread(self) -> None:
        self.assertIn("Before a currentness-sensitive action, re-read the live durable facts", self.standard)
        self.assertIn("fact was true earlier in this session -> fact is still current", self.standard)
        self.assertIn("expected-head merge", self.reference)

    def test_no_required_truth_can_exist_only_in_lost_session(self) -> None:
        self.assertIn("No required development truth may exist only in an ephemeral Agent/chat/session context", self.standard)
        self.assertIn("replacement Agent", self.standard)
        self.assertIn("Lost-session test", self.reference)

    def test_progressive_disclosure_is_not_context_dumping(self) -> None:
        self.assertIn("Load the minimum authority needed for the concern", self.standard)
        self.assertIn("More context is not automatically better context", self.standard)
        self.assertIn("Do not start by loading the whole repository", self.reference)

    def test_external_resource_is_evidence_not_product_truth(self) -> None:
        self.assertIn("are evidence/resources until the owning authority promotes", self.standard)
        self.assertIn("resource/tool available != authoritative requirement", self.standard)

    def test_historical_chat_cannot_override_current_authority(self) -> None:
        self.assertIn("Historical chat or memory may help discovery, but it cannot override current durable authority", self.standard)
        self.assertIn("current durable authority wins", self.standard)

    def test_same_level_conflict_fails_closed(self) -> None:
        self.assertIn("Same-level material conflicts stay explicit", self.standard)
        self.assertIn("fails closed", self.standard)
        self.assertIn("Agent may pick preferred answer", self.standard)

    def test_no_context_snapshot_or_v47_resolver(self) -> None:
        self.assertIn("does not create", self.standard)
        self.assertIn("Context Snapshot database/schema", self.standard)
        self.assertIn("repository-wide v4.7 owner resolver", self.standard)


if __name__ == "__main__":
    unittest.main()
