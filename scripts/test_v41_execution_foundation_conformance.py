from __future__ import annotations

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "templates" / "golden" / "V41_EXECUTION_FOUNDATION_EXAMPLES.json"
EXECUTION_CONTEXT = ROOT / "schemas" / "execution-context-v1.schema.json"
TOOLCHAIN = ROOT / "schemas" / "dependency-toolchain-profile-v1.schema.json"


def evaluate(case: dict) -> bool:
    facts = case["facts"]
    category = case["category"]

    if category == "fast_path":
        return not facts["material_execution_concerns"] and not facts["optional_contracts_present"]
    if category == "authority":
        return not facts.get("claims_workflow_or_release_authority", False)
    if category == "dependency_toolchain":
        if "agent_claims_repository_minimum" in facts:
            return facts["agent_claims_repository_minimum"] == facts["repository_compatibility"]
        return bool(facts.get("manifest") and facts.get("compatibility") and facts.get("certification_tuple"))
    if category == "configuration":
        return bool(facts.get("secret_ref")) and not facts.get("secret_value_present", False)
    if category == "git_workspace":
        return not facts.get("same_writable_workspace", False)
    if category == "artifact":
        if facts.get("artifact_class") == "CACHE" and facts.get("claimed_validation_pass"):
            return False
        if facts.get("claimed_release_artifact"):
            return bool(facts.get("promotion_authorized") and facts.get("identity_bound") and facts.get("provenance_bound"))
        if facts.get("promoted_class") == "RELEASE_ARTIFACT":
            return bool(facts.get("promotion_authorized") and facts.get("identity_bound") and facts.get("provenance_bound"))
        return True
    if category == "external_system":
        if facts.get("attempted_action") == "write" and facts.get("side_effect_authority") != "write":
            return False
        required = facts.get("required_environment")
        if required and facts.get("environment_class") != required and facts.get("claimed_pass"):
            return False
        return True
    if category == "recovery":
        return bool(facts.get("durable_handoff_present") and facts.get("unpublished_work_protected"))
    if category == "evidence_boundary":
        return not (facts.get("claimed_release_ready") and not facts.get("release_qualification_executed"))
    raise AssertionError(f"unknown category: {category}")


class V41ExecutionFoundationConformanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
        cls.execution_context = json.loads(EXECUTION_CONTEXT.read_text(encoding="utf-8"))
        cls.toolchain = json.loads(TOOLCHAIN.read_text(encoding="utf-8"))
        cls.by_id = {case["id"]: case for case in cls.fixture["cases"]}

    def test_all_golden_cases_match_expected_decision(self) -> None:
        self.assertGreaterEqual(len(self.fixture["cases"]), 16)
        for case in self.fixture["cases"]:
            with self.subTest(case=case["id"]):
                self.assertEqual(evaluate(case), case["expected"]["allowed"])
                self.assertTrue(case["expected"]["reason"])

    def test_execution_context_is_non_authoritative_and_secret_ref_only(self) -> None:
        props = self.execution_context["properties"]
        for forbidden in ("task_state", "gate_state", "review_result", "candidate_state", "release_state"):
            self.assertNotIn(forbidden, props)
        secret_item = props["configuration"]["properties"]["secret_refs"]["items"]
        self.assertEqual(set(secret_item["properties"]), {"ref", "source", "scope"})
        for forbidden in ("value", "token", "password", "key", "signed_url"):
            self.assertNotIn(forbidden, secret_item["properties"])

    def test_toolchain_supports_node_and_non_node_without_collapsing_certification(self) -> None:
        node = self.by_id["node-npm-toolchain"]["facts"]
        py = self.by_id["python-toolchain"]["facts"]
        self.assertEqual({node["ecosystem"], py["ecosystem"]}, {"node", "python"})
        props = self.toolchain["properties"]
        self.assertIn("toolchains", props)
        self.assertIn("certification_tuples", props)
        self.assertNotEqual(node["compatibility"], node["certification_tuple"])
        self.assertNotEqual(py["compatibility"], py["certification_tuple"])

    def test_agent_local_runtime_cannot_narrow_repository_authority(self) -> None:
        case = self.by_id["agent-runtime-does-not-rewrite-repository"]
        self.assertFalse(evaluate(case))
        self.assertNotEqual(case["facts"]["agent_runtime"], case["facts"]["repository_compatibility"])

    def test_workspace_isolation_and_durable_recovery(self) -> None:
        self.assertTrue(evaluate(self.by_id["multi-agent-isolated-workspaces"]))
        self.assertFalse(evaluate(self.by_id["shared-writable-workspace"]))
        self.assertTrue(evaluate(self.by_id["durable-handoff-recovery"]))

    def test_artifact_class_and_promotion_boundaries(self) -> None:
        self.assertFalse(evaluate(self.by_id["cache-is-not-validation-evidence"]))
        self.assertFalse(evaluate(self.by_id["build-output-not-release-artifact"]))
        self.assertTrue(evaluate(self.by_id["authorized-artifact-promotion"]))

    def test_external_fidelity_and_side_effect_authority_do_not_escalate(self) -> None:
        self.assertFalse(evaluate(self.by_id["sandbox-does-not-prove-production"]))
        self.assertFalse(evaluate(self.by_id["credential-does-not-grant-write-authority"]))

    def test_fast_path_remains_lightweight(self) -> None:
        self.assertTrue(evaluate(self.by_id["fast-path-minimal"]))

    def test_task_evidence_is_not_release_qualification(self) -> None:
        self.assertFalse(evaluate(self.by_id["task-pass-not-release-pass"]))


if __name__ == "__main__":
    unittest.main()
