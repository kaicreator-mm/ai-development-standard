from __future__ import annotations

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ExecutionArchitectureRegression(unittest.TestCase):
    def text(self, rel: str) -> str:
        return (ROOT / rel).read_text(encoding="utf-8")

    def test_state_dimensions_are_separate(self) -> None:
        text = self.text("standards/EXECUTION_ARCHITECTURE_STANDARD.md")
        for token in ("Workflow routing state", "Gate state", "Execution-channel/provider state", "Dispatch state", "Candidate state", "Release state"):
            self.assertIn(token, text)

    def test_validation_layering_and_drift(self) -> None:
        text = self.text("standards/VALIDATION_STANDARD.md")
        for token in ("concern | integration | closure", "HEAD drift", "BASE / merge-result drift", "VALIDATION_IMPACT_DECISION", "Alternate executor substitution"):
            self.assertIn(token, text)

    def test_candidate_freeze_is_operational(self) -> None:
        text = self.text("standards/RELEASE_STANDARD.md")
        for token in ("Operational immutability", "THAWED / INVALIDATED", "candidate ref", "Repository Integration"):
            self.assertIn(token, text)

    def test_hidden_escape_feedback_exists(self) -> None:
        text = self.text("standards/RELEASE_STANDARD.md") + self.text("standards/EXECUTION_ARCHITECTURE_STANDARD.md")
        for token in ("HIDDEN_PACK_BLIND_SPOT", "PACK_DEFECT", "new immutable private pack identity"):
            self.assertIn(token, text)

    def test_pointer_only_handoff(self) -> None:
        text = self.text("standards/LOCAL_AGENT_HANDOFF_PROTOCOL.md")
        self.assertIn("Pointer-only principle", text)
        self.assertIn("HANDOFF_READY", text)
        self.assertIn("Do not copy the full task contract into chat", text)

    def test_new_writer_surfaces_are_v2(self) -> None:
        for rel in ("standards/GITHUB_WORKFLOW.md", "standards/VERSION_INTEGRATION_WORKFLOW.md", "standards/LOCAL_AGENT_HANDOFF_PROTOCOL.md", "templates/local-agent-handoff-issue.md"):
            text = self.text(rel)
            self.assertIn("ai-dev:event:v2", text)
            self.assertNotIn("publish `ai-dev:event:v1`", text)

    def test_event_schema_lifecycle(self) -> None:
        schema = json.loads(self.text("schemas/agent-event-v2.schema.json"))
        events = set(schema["properties"]["event"]["enum"])
        required = {"HANDOFF_READY", "DISPATCH_REQUEST", "DISPATCH_STATE_CHANGED", "CI_INFRA_EXCEPTION", "VALIDATION_IMPACT_DECISION", "CANDIDATE_STATE_CHANGED", "HIDDEN_ESCAPE_DISPOSITION", "RELEASE_QUALIFICATION", "REPOSITORY_INTEGRATION_RESULT"}
        self.assertTrue(required <= events, required - events)

    def test_small_project_runtime_is_optional(self) -> None:
        text = self.text("standards/EXECUTION_ARCHITECTURE_STANDARD.md")
        self.assertIn("A project is not required to run a centralized service", text)
        self.assertIn("Browser automation", text)
        self.assertIn("non-normative transport choices", text)


if __name__ == "__main__":
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(ExecutionArchitectureRegression))
    raise SystemExit(0 if result.wasSuccessful() else 1)
