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

    def test_atomic_claim_duplicate_exclusion(self) -> None:
        execution = self.text("standards/EXECUTION_ARCHITECTURE_STANDARD.md")
        work_item = self.text("standards/GITHUB_WORK_ITEM_CONTRACT_STANDARD.md")

        for token in (
            "At most one incompatible active dispatch MUST exist per `(work item, role)`",
            "Claim admission is a compare-and-set style transition",
            "only the first claim accepted against the still-current predicates may become canonical",
            "MUST be rejected atomically as duplicate/stale",
            "same logical operator re-claiming the same dispatch is idempotent",
        ):
            self.assertIn(token, execution)

        for token in (
            "Claim admission is a compare-and-set operation over current durable GitHub facts",
            "At most one incompatible active claim/dispatch per `(work item, role)` is permitted",
            "A worker MUST NOT create or mutate implementation work before its claim is accepted",
            "TASK_DAG.md` remains a frozen planning/history checkpoint",
            "competing claim MUST be rejected before it can enter RUNNING or mutate implementation work",
        ):
            self.assertIn(token, work_item)

        self.assertIn("claimed", execution.split("### Workflow routing state", 1)[1].split("### Gate state", 1)[0])

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

        protocol = self.text("standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md")
        self.assertIn("All newly emitted structured Agent events MUST use", protocol)
        self.assertIn("New writers MUST NOT emit v1", protocol)
        self.assertIn("scheduler", protocol)
        self.assertIn("repository-integration-controller", protocol)

    def test_event_schema_lifecycle(self) -> None:
        schema = json.loads(self.text("schemas/agent-event-v2.schema.json"))
        events = set(schema["properties"]["event"]["enum"])
        required = {"HANDOFF_READY", "DISPATCH_REQUEST", "DISPATCH_STATE_CHANGED", "CI_INFRA_EXCEPTION", "VALIDATION_IMPACT_DECISION", "CANDIDATE_STATE_CHANGED", "HIDDEN_ESCAPE_DISPOSITION", "RELEASE_QUALIFICATION", "REPOSITORY_INTEGRATION_RESULT"}
        self.assertTrue(required <= events, required - events)

        roles = set(schema["properties"]["actor_role"]["enum"])
        self.assertTrue({"scheduler", "repository-integration-controller"} <= roles)

        review_rule = next(
            rule for rule in schema["allOf"]
            if rule.get("if", {}).get("properties", {}).get("event", {}).get("const") == "REVIEW_DECISION"
        )
        self.assertIn("status", review_rule["then"]["required"])

    def test_small_project_runtime_is_optional(self) -> None:
        text = self.text("standards/EXECUTION_ARCHITECTURE_STANDARD.md")
        self.assertIn("A project is not required to run a centralized service", text)
        self.assertIn("Browser automation", text)
        self.assertIn("non-normative transport choices", text)


if __name__ == "__main__":
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(ExecutionArchitectureRegression))
    raise SystemExit(0 if result.wasSuccessful() else 1)
