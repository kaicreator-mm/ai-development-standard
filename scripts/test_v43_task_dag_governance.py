from __future__ import annotations

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
STANDARD = ROOT / "standards" / "TASK_DAG_GOVERNANCE_STANDARD.md"
REFERENCE = ROOT / "references" / "TASK_DAG_GOVERNANCE_REFERENCE.md"
SCHEMA = ROOT / "schemas" / "dag-mutation-record-v1.schema.json"


class TaskDAGGovernanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.standard = STANDARD.read_text(encoding="utf-8")
        cls.reference = REFERENCE.read_text(encoding="utf-8")
        cls.schema = json.loads(SCHEMA.read_text(encoding="utf-8"))

    def test_planning_and_live_dag_are_distinct(self) -> None:
        self.assertIn("TASK_DAG.md", self.standard)
        self.assertIn("GitHub Issue Dependencies represent the current live", self.standard)
        self.assertIn("MUST NOT substitute for native live dependency edges", self.standard)

    def test_required_mutation_classes_are_representable(self) -> None:
        for value in ("ADD", "SPLIT", "MERGE", "SUPERSEDE", "ADD_DEPENDENCY", "REMOVE_DEPENDENCY", "CHANGE_LANE", "CHANGE_INTEGRATION_OWNER", "DEFER"):
            self.assertIn(value, self.standard)
        self.assertNotIn("enum", self.schema["properties"]["mutation_class"])

    def test_mutation_evidence_matches_t01_contract(self) -> None:
        required = set(self.schema["required"])
        for field in (
            "requested_by", "approved_by", "reason", "affected_task_refs",
            "old_topology_ref", "new_topology_ref", "old_edges", "new_edges",
            "scope_impact", "release_impact", "task_pack_impact_refs",
            "review_impact", "validation_impact_ref",
        ):
            self.assertIn(field, required)

    def test_task_identity_cannot_silently_absorb_materially_different_work(self) -> None:
        self.assertIn("may not silently absorb materially different work", self.standard)
        self.assertIn("SPLIT/ADD/SUPERSEDE", self.reference)

    def test_dependency_removal_cannot_fabricate_readiness(self) -> None:
        self.assertIn("MUST NOT fabricate readiness", self.standard)
        self.assertIn("removing the edge to make T05 READY is invalid", self.reference)
        self.assertIn("re-evaluate", self.standard)

    def test_pr_stack_or_cherry_pick_is_not_dag_authority(self) -> None:
        self.assertIn("Stacked PRs", self.standard)
        self.assertIn("do not replace Task DAG dependencies", self.standard)
        self.assertIn("cherry-pick order", self.standard)

    def test_schema_records_but_does_not_perform_native_mutation(self) -> None:
        props = self.schema["properties"]
        for forbidden in ("apply_mutation", "ready_state", "native_mutation", "github_token", "workflow_state"):
            self.assertNotIn(forbidden, props)
        self.assertIn("does **not** perform native GitHub mutation", self.standard)

    def test_unavailable_native_mutation_requires_controller_handoff(self) -> None:
        self.assertIn("create an explicit controller/local handoff", self.standard)
        self.assertIn("read-back equality check", self.reference)
        self.assertIn("preserve the prior live DAG", self.standard)


if __name__ == "__main__":
    unittest.main()
