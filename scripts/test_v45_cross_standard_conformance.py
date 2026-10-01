from __future__ import annotations

import copy
import json
import re
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

PRD = (ROOT / "docs/implementation/4.5.0/PRD.md").read_text(encoding="utf-8")
L2 = (ROOT / "docs/implementation/4.5.0/L2_ARCHITECTURE_EVIDENCE.md").read_text(encoding="utf-8")
ADOPTION = (ROOT / "docs/implementation/4.5.0/MIGRATION_ADOPTION.md").read_text(encoding="utf-8")
RUNTIME = (ROOT / "standards/OBSERVABILITY_RUNTIME_EVIDENCE_STANDARD.md").read_text(encoding="utf-8")
INCIDENT = (ROOT / "standards/INCIDENT_RECOVERY_FEEDBACK_STANDARD.md").read_text(encoding="utf-8")
MAINTENANCE = (ROOT / "standards/MAINTENANCE_EOL_HOTFIX_STANDARD.md").read_text(encoding="utf-8")
CLOSURE_INPUT = ROOT / "docs/implementation/4.5.0/closure-inputs/T09_INPUTS.json"
SHA40 = re.compile(r"^[0-9a-f]{40}$")

COMPONENT_SUITES = {
    "scripts/test_v45_runtime_observation_conformance.py",
    "scripts/test_v45_incident_feedback_conformance.py",
    "scripts/test_v45_maintenance_hotfix_conformance.py",
    "scripts/test_v45_adoption_wiring.py",
}

NEGATIVE_INFERENCE_FAMILIES = {
    "Deployment SUCCESS -> Runtime Healthy",
    "health endpoint PASS -> business journey PASS",
    "monitoring backend available -> product healthy",
    "no alert -> no incident",
    "incident recovered -> permanent defect fixed",
    "RECOVERED -> VERIFIED",
    "VERIFIED -> all follow-up complete",
    "incident record -> rewrite earlier Release/Deployment evidence",
    "incident closure -> erase prior events/follow-up",
    "telemetry usefulness -> permission to persist secrets/PII",
    "branch/tag exists -> version supported",
    "backport/cherry-pick -> old exact-SHA Validation transfers",
    "hotfix urgency -> release/validation truth waived",
    "mitigation -> follow-up complete",
}


def _exact_tested_tuple_is_bound(item: dict, candidate: dict) -> bool:
    tested = item.get("tested_identity")
    if not isinstance(tested, dict):
        return False
    sha_fields = ("candidate_sha", "candidate_tree", "target_sha", "target_tree", "combined_tree")
    if not all(SHA40.fullmatch(str(tested.get(field, ""))) for field in sha_fields):
        return False
    if tested["candidate_sha"] != candidate["candidate_sha"] or tested["candidate_tree"] != candidate["candidate_tree"]:
        return False
    if not tested.get("environment_ref") or not tested.get("commands_profile_ref"):
        return False
    return tested.get("currentness") == "CURRENT"


def closure_input_can_be_green(payload: dict) -> bool:
    """Fail-closed projection for T09 closure inputs, never a Version Closure verdict."""
    candidate = payload.get("exact_candidate_binding", {})
    if candidate.get("status") != "BOUND":
        return False
    if not SHA40.fullmatch(str(candidate.get("candidate_sha", ""))):
        return False
    if not SHA40.fullmatch(str(candidate.get("candidate_tree", ""))):
        return False

    for item in payload.get("required_tuples", []):
        if not item.get("required"):
            continue
        if item.get("status") != "PASS" or not _exact_tested_tuple_is_bound(item, candidate):
            return False

    for gate in payload.get("required_gates", []):
        if gate.get("required") and gate.get("status") != "PASS":
            return False

    for finding in payload.get("known_findings", []):
        if finding.get("severity") in {"P0", "P1"} and finding.get("state") != "RESOLVED":
            return False
    return True


class V45CrossStandardConformanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.closure_input = json.loads(CLOSURE_INPUT.read_text(encoding="utf-8"))

    def test_component_suite_inventory_is_exact_and_real(self) -> None:
        self.assertEqual(set(self.closure_input["component_suites"]), COMPONENT_SUITES)
        for relative in COMPONENT_SUITES:
            self.assertTrue((ROOT / relative).is_file(), relative)

    def test_full_product_l2_forbidden_inference_matrix_is_integrated(self) -> None:
        self.assertEqual(set(self.closure_input["negative_inference_families"]), NEGATIVE_INFERENCE_FAMILIES)

        # Product §11 / L2 §10 remain the source authority; T09 only cross-checks them.
        for phrase in (
            "Deployment SUCCESS -> Runtime Healthy",
            "health endpoint PASS -> business journey PASS",
            "monitoring backend available -> product healthy",
            "no alert -> no incident",
            "incident recovered -> permanent defect fixed",
            "incident record -> rewrite earlier Release/Deployment evidence",
            "telemetry usefulness -> permission to persist secrets/PII",
            "branch/tag exists -> version supported",
            "backport/cherry-pick -> old exact-SHA Validation transfers",
            "hotfix urgency -> release/validation truth waived",
            "mitigation -> follow-up complete",
        ):
            self.assertIn(phrase, PRD)
        for phrase in (
            "RECOVERED -> VERIFIED",
            "VERIFIED -> all follow-up complete",
            "incident closure -> erase prior events/follow-up",
        ):
            self.assertIn(phrase, L2)

        self.assertIn("DEPLOYMENT_SUCCEEDED != RUNTIME_HEALTHY", RUNTIME)
        self.assertIn("RECOVERED != VERIFIED", INCIDENT)
        self.assertIn("VERIFIED != FOLLOW_UP_COMPLETE", INCIDENT)
        self.assertIn("source PASS != backport result PASS", MAINTENANCE)

    def test_v44_deployment_v42_recovery_v41_secret_external_boundaries_are_preserved(self) -> None:
        self.assertIn("v4.5 reuses v4.4 artifact/deployment/environment identity", RUNTIME)
        self.assertIn("It does not mint a second Deployment object", RUNTIME)
        self.assertIn("v4.4 Deployment Governance", INCIDENT)
        self.assertIn("v4.2 Data/Migration Governance", INCIDENT)
        self.assertIn("v4.1 Configuration/Secrets", INCIDENT)
        self.assertIn("external-system mutation requires its applicable side-effect authority", INCIDENT)

    def test_backport_evidence_never_transfers(self) -> None:
        self.assertIn("Source-branch evidence belongs to the source subject", MAINTENANCE)
        self.assertIn("MUST NOT automatically transfer", MAINTENANCE)
        self.assertIn("resulting exact SHA must obtain its own applicable current Testing/Validation/Review/Release evidence", MAINTENANCE)
        self.assertIn("Backport source PASS → result-SHA PASS", ADOPTION)

    def test_historical_compatibility_and_fast_path_are_proportional(self) -> None:
        self.assertIn("Do not reclassify old records, retrofit historical releases/incidents/support policy", ADOPTION)
        self.assertIn("Legacy release/incident/support record", ADOPTION)
        self.assertIn("urgent Fast Path cannot waive required gates", ADOPTION)
        self.assertIn("MUST NOT bypass material exact-subject Validation", MAINTENANCE)

    def bound_payload(self) -> dict:
        payload = copy.deepcopy(self.closure_input)
        payload["exact_candidate_binding"] = {
            "status": "BOUND",
            "candidate_sha": "1" * 40,
            "candidate_tree": "2" * 40,
            "evidence_location": "synthetic-test-only",
            "reason": "synthetic-test-only",
        }
        for item in payload["required_tuples"]:
            item["status"] = "PASS"
            item["tested_identity"] = {
                "candidate_sha": "1" * 40,
                "candidate_tree": "2" * 40,
                "target_sha": "3" * 40,
                "target_tree": "4" * 40,
                "combined_tree": "5" * 40,
                "environment_ref": "synthetic-test-only",
                "commands_profile_ref": "synthetic-test-only",
                "currentness": "CURRENT",
            }
        for gate in payload["required_gates"]:
            gate["status"] = "PASS"
        payload["known_findings"] = []
        return payload

    def test_synthetic_fully_bound_inputs_can_be_green_without_becoming_a_release_verdict(self) -> None:
        self.assertTrue(closure_input_can_be_green(self.bound_payload()))

    def test_required_not_run_or_blocked_tuple_cannot_be_green(self) -> None:
        for status in ("NOT_RUN", "BLOCKED"):
            with self.subTest(status=status):
                payload = self.bound_payload()
                payload["required_tuples"][0]["status"] = status
                self.assertFalse(closure_input_can_be_green(payload))

    def test_pass_without_exact_current_tested_tuple_cannot_be_green(self) -> None:
        mutations = (
            ("candidate_sha", "9" * 40),
            ("target_sha", None),
            ("combined_tree", None),
            ("environment_ref", None),
            ("commands_profile_ref", None),
            ("currentness", "DRIFTED"),
        )
        for field, value in mutations:
            with self.subTest(field=field):
                payload = self.bound_payload()
                payload["required_tuples"][0]["tested_identity"][field] = value
                self.assertFalse(closure_input_can_be_green(payload))

    def test_required_gate_not_run_or_blocked_cannot_be_green(self) -> None:
        for status in ("NOT_RUN", "BLOCKED"):
            with self.subTest(status=status):
                payload = self.bound_payload()
                payload["required_gates"][0]["status"] = status
                self.assertFalse(closure_input_can_be_green(payload))

    def test_unresolved_p0_or_p1_cannot_be_green(self) -> None:
        for severity in ("P0", "P1"):
            with self.subTest(severity=severity):
                payload = self.bound_payload()
                payload["known_findings"] = [
                    {"severity": severity, "state": "OPEN", "summary": "synthetic-test-only"}
                ]
                self.assertFalse(closure_input_can_be_green(payload))

    def test_builder_input_is_blocked_and_does_not_issue_release_truth(self) -> None:
        self.assertEqual(self.closure_input["closure_input_state"], "BLOCKED")
        self.assertEqual(self.closure_input["exact_candidate_binding"]["status"], "UNBOUND")
        self.assertFalse(closure_input_can_be_green(self.closure_input))
        forbidden = set(self.closure_input["forbidden_builder_conclusions"])
        self.assertTrue({
            "Candidate Freeze",
            "Version Closure PASS",
            "Release Qualification PASS",
            "Release READY",
            "merge-ready",
        } <= forbidden)


if __name__ == "__main__":
    unittest.main(verbosity=2)
