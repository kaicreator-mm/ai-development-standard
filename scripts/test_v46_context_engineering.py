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

    def test_authority_resolution_uses_owner_override_and_currentness(self) -> None:
        self.assertIn("does not define one universal total ordering", self.standard)
        self.assertIn("semantic owner", self.standard)
        self.assertIn("override surface", self.standard)
        self.assertIn("live currentness", self.standard)
        self.assertIn("This is a read sequence, not a universal authority ranking", self.reference)

    def test_project_overrides_can_specialize_defaults_without_weakening_hard_constraints(self) -> None:
        self.assertIn("PROJECT_OVERRIDES.md", self.standard)
        self.assertIn("may specialize standard defaults where allowed", self.standard)
        self.assertIn("cannot weaken a hard constraint", self.standard)
        self.assertIn("pinned standard default exists | valid PROJECT_OVERRIDES specialization is ignored", self.standard)

    def test_native_dependencies_own_live_topology_after_materialization(self) -> None:
        self.assertIn("GitHub native Issue Dependencies own the canonical live blocked-by topology", self.standard)
        self.assertIn("Frozen Task DAG remains planning/history authority", self.standard)
        self.assertIn("MUST NOT override the current native Issue Dependency graph", self.standard)
        self.assertIn("Frozen Task DAG has edge X | edge X is still live after native dependency materialization/change", self.standard)

    def test_task_pack_scope_is_not_rewritten_by_live_topology(self) -> None:
        self.assertIn("Task Pack continues to own Task scope/acceptance", self.standard)
        self.assertIn("live Issue dependency changed | Task Pack scope/acceptance changed automatically", self.standard)

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
        self.assertIn("applicable durable owner wins", self.standard)

    def test_same_level_conflict_fails_closed(self) -> None:
        self.assertIn("same authority/currentness level", self.standard)
        self.assertIn("fail closed", self.standard)
        self.assertIn("Agent may pick preferred answer", self.standard)

    def test_no_context_snapshot_or_v47_resolver(self) -> None:
        self.assertIn("does not create", self.standard)
        self.assertIn("Context Snapshot database/schema", self.standard)
        self.assertIn("repository-wide v4.7 owner resolver", self.standard)


if __name__ == "__main__":
    unittest.main()
