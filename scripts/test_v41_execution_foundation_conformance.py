from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import unittest

from test_v41_external_systems import external_execution_state
from test_v41_git_execution import evidence_reusable_after_rewrite
from test_v41_workspace_artifact import destructive_cleanup_allowed

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "templates" / "golden" / "V41_EXECUTION_FOUNDATION_EXAMPLES.json"
EXECUTION_CONTEXT = ROOT / "schemas" / "execution-context-v1.schema.json"
TOOLCHAIN = ROOT / "schemas" / "dependency-toolchain-profile-v1.schema.json"
RISK_EXCEPTION = ROOT / "schemas" / "dependency-risk-exception-v1.schema.json"
EXTERNAL_STANDARD = ROOT / "standards" / "EXTERNAL_SYSTEM_EXECUTION_STANDARD.md"
WORKSPACE_REFERENCE = ROOT / "references" / "WORKSPACE_ARTIFACT_REFERENCE.md"

# Real owner suites (not a T08-only substitute). The CI workflow invokes
# test_verify_standard.py, which executes this runner and therefore all seven.
OWNER_SUITES = (
    "test_v41_execution_foundation_contracts.py",  # historical v4 payloads included
    "test_v41_dependency_toolchain.py",            # risk exception != PASS
    "test_v41_git_execution.py",                   # local/unpushed Git, rewrite, cleanup
    "test_v41_configuration_secrets.py",
    "test_v41_workspace_artifact.py",              # provenance and unowned cleanup
    "test_v41_external_systems.py",                # BLOCKED/NOT_RUN/fidelity/retry
    "test_v41_adoption_wiring.py",
)


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
    if category == "risk_exception":
        return not (facts.get("claimed_validation_pass") or facts.get("claimed_remediated"))
    if category == "configuration":
        return bool(facts.get("secret_ref")) and not facts.get("secret_value_present", False)
    if category == "git_workspace":
        return not facts.get("same_writable_workspace", False)
    if category == "git_authority":
        return not facts.get("claims_task_claimed_from_local_branch", False)
    if category == "evidence_currentness":
        return (not facts.get("claim_evidence_reusable", False)) or evidence_reusable_after_rewrite(
            facts["tested_sha"], facts["current_sha"]
        )
    if category == "cleanup":
        return destructive_cleanup_allowed(
            owner_known=facts["owner_known"],
            class_known=facts["class_known"],
            reconstructable=facts["reconstructable"],
        )
    if category == "artifact":
        if facts.get("artifact_class") == "CACHE" and facts.get("claimed_validation_pass"):
            return False
        if facts.get("claimed_release_artifact") or facts.get("promoted_class") == "RELEASE_ARTIFACT":
            return all((
                facts.get("promotion_authorized"),
                facts.get("identity_bound"),
                facts.get("provenance_bound"),
                facts.get("producer_source_ref"),
                facts.get("build_ref"),
            ))
        return True
    if category == "external_system":
        if facts.get("attempted_action") == "write" and facts.get("side_effect_authority") != "write":
            return False
        required = facts.get("required_environment")
        if required and facts.get("environment_class") != required and facts.get("claimed_pass"):
            return False
        return True
    if category == "external_availability":
        actual = external_execution_state(
            available=facts["available"], authorized=facts["authorized"],
            executed=facts["executed"], product_failure=facts.get("product_failure", False),
        )
        return actual == facts["claimed_state"]
    if category == "fidelity_mapping":
        mapping = facts.get("project_authorized_mapping", {})
        return bool(mapping) and facts["actual"] in mapping and facts["required"] in mapping and (
            mapping[facts["actual"]] >= mapping[facts["required"]]
        )
    if category == "deadline":
        return bool(facts.get("deadline_authorized")) and (
            0 <= facts["timeout_seconds"] <= facts["overall_deadline_seconds"]
            and 0 <= facts["elapsed_seconds"] <= facts["overall_deadline_seconds"]
            and facts["elapsed_seconds"] + facts["timeout_seconds"] <= facts["overall_deadline_seconds"]
        )
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
        cls.risk_exception = json.loads(RISK_EXCEPTION.read_text(encoding="utf-8"))
        cls.external_standard = EXTERNAL_STANDARD.read_text(encoding="utf-8")
        cls.workspace_reference = WORKSPACE_REFERENCE.read_text(encoding="utf-8")
        cls.by_id = {case["id"]: case for case in cls.fixture["cases"]}

    def test_dependency_complete_real_owner_suites_execute(self) -> None:
        # This is the critical cross-standard regression path: any actual
        # T01-T07 owner-suite regression fails the T08 focused test and CI.
        self.assertEqual(len(OWNER_SUITES), 7)
        for suite in OWNER_SUITES:
            path = ROOT / "scripts" / suite
            with self.subTest(suite=suite):
                self.assertTrue(path.is_file(), f"missing production owner suite {suite}")
                result = subprocess.run(
                    [sys.executable, str(path)], cwd=ROOT,
                    capture_output=True, text=True, check=False,
                )
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertIn("OK", result.stdout + result.stderr)

    def test_all_golden_cases_match_expected_decision(self) -> None:
        self.assertGreaterEqual(len(self.fixture["cases"]), 26)
        self.assertEqual(len(self.by_id), len(self.fixture["cases"]))
        for case in self.fixture["cases"]:
            with self.subTest(case=case["id"]):
                self.assertEqual(bool(evaluate(case)), case["expected"]["allowed"])
                self.assertTrue(case["expected"]["reason"])

    def test_historical_payload_and_risk_exception_proofs_are_owner_bound(self) -> None:
        source = (ROOT / "scripts" / OWNER_SUITES[0]).read_text(encoding="utf-8")
        for name in (
            "test_historical_v4_dispatch_stays_valid_without_v41_refs",
            "test_historical_v4_validation_report_stays_valid_without_v41_refs",
            "test_historical_v4_execution_pack_stays_valid_without_v41_refs",
        ):
            self.assertIn(name, source)
        statuses = self.risk_exception["properties"]["status"]["enum"]
        self.assertIn("accepted-risk", statuses)
        self.assertNotIn("PASS", statuses)
        self.assertFalse(evaluate(self.by_id["accepted-risk-is-not-validation-pass"]))
        self.assertFalse(evaluate(self.by_id["accepted-risk-is-not-remediation"]))

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

    def test_git_unpushed_rewrite_and_unowned_cleanup_negatives(self) -> None:
        for name in ("local-branch-does-not-claim-task", "stale-sha-pass-does-not-transfer", "unowned-state-not-destructively-cleaned"):
            self.assertFalse(evaluate(self.by_id[name]), name)
        self.assertTrue(evaluate(self.by_id["unchanged-sha-evidence-stays-current"]))

    def test_workspace_isolation_and_durable_recovery(self) -> None:
        self.assertTrue(evaluate(self.by_id["multi-agent-isolated-workspaces"]))
        self.assertFalse(evaluate(self.by_id["shared-writable-workspace"]))
        self.assertTrue(evaluate(self.by_id["durable-handoff-recovery"]))

    def test_artifact_class_producer_build_provenance_and_promotion(self) -> None:
        self.assertFalse(evaluate(self.by_id["cache-is-not-validation-evidence"]))
        self.assertFalse(evaluate(self.by_id["build-output-not-release-artifact"]))
        self.assertFalse(evaluate(self.by_id["promotion-without-producer-build-ref"]))
        self.assertTrue(evaluate(self.by_id["authorized-artifact-promotion"]))
        self.assertIn("identify exact source/build provenance", self.workspace_reference)

    def test_external_fidelity_availability_and_side_effect_non_escalation(self) -> None:
        for name in (
            "sandbox-does-not-prove-production", "credential-does-not-grant-write-authority",
            "external-unavailable-not-pass", "unexecuted-external-is-not-pass",
            "custom-fidelity-lower-not-higher",
        ):
            self.assertFalse(evaluate(self.by_id[name]), name)
        self.assertTrue(evaluate(self.by_id["custom-fidelity-authorized-equivalence"]))
        self.assertIn("project-defined equivalents", self.external_standard)
        self.assertIn("not a closed universal enum", self.external_standard)

    def test_bounded_timeout_and_overall_deadline_non_escalation(self) -> None:
        self.assertTrue(evaluate(self.by_id["bounded-timeout-within-deadline"]))
        self.assertFalse(evaluate(self.by_id["timeout-extended-beyond-overall-deadline"]))
        self.assertFalse(evaluate(self.by_id["elapsed-exceeds-overall-deadline"]))
        self.assertFalse(evaluate(self.by_id["remaining-budget-insufficient-for-next-attempt"]))
        self.assertTrue(evaluate(self.by_id["remaining-budget-exact-boundary"]))
        self.assertIn("Retries MUST be bounded", self.external_standard)
        self.assertIn("## 11. Timeouts and deadlines", self.external_standard)

    def test_fast_path_remains_lightweight(self) -> None:
        self.assertTrue(evaluate(self.by_id["fast-path-minimal"]))

    def test_task_evidence_is_not_release_qualification(self) -> None:
        self.assertFalse(evaluate(self.by_id["task-pass-not-release-pass"]))


if __name__ == "__main__":
    unittest.main()
