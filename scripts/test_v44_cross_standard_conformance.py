from __future__ import annotations

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

BUILD = (ROOT / "standards/BUILD_ARTIFACT_GOVERNANCE_STANDARD.md").read_text(encoding="utf-8")
DISTRIBUTION = (ROOT / "standards/DISTRIBUTION_GOVERNANCE_STANDARD.md").read_text(encoding="utf-8")
DEPLOYMENT = (ROOT / "standards/DEPLOYMENT_GOVERNANCE_STANDARD.md").read_text(encoding="utf-8")
VALIDATION = (ROOT / "standards/VALIDATION_STANDARD.md").read_text(encoding="utf-8")
RELEASE = (ROOT / "standards/RELEASE_STANDARD.md").read_text(encoding="utf-8")
ADOPTION = (ROOT / "docs/implementation/4.4.0/MIGRATION_ADOPTION.md").read_text(encoding="utf-8")
CLOSURE_INPUT = ROOT / "docs/implementation/4.4.0/closure-inputs/T08_INPUTS.json"


def closure_input_can_be_green(payload: dict) -> bool:
    """Test-only fail-closed projection; never a Candidate Freeze or Release verdict."""
    candidate = payload["exact_candidate_binding"]
    if candidate["status"] != "BOUND":
        return False
    if not candidate.get("candidate_sha") or not candidate.get("candidate_tree"):
        return False

    for item in payload["required_tuples"]:
        if item["required"] and item["status"] != "PASS":
            return False

    for gate in payload["required_gates"]:
        if gate["required"] and gate["status"] != "PASS":
            return False

    for finding in payload["known_findings"]:
        if finding["state"] != "RESOLVED" and finding["severity"] in {"P0", "P1"}:
            return False
    return True


class V44CrossStandardConformanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.closure_input = json.loads(CLOSURE_INPUT.read_text(encoding="utf-8"))

    def test_component_suite_inventory_is_real_and_complete(self) -> None:
        expected = {
            "scripts/test_v44_delivery_contracts.py",
            "scripts/test_v44_build_artifact.py",
            "scripts/test_v44_build_package_conformance.py",
            "scripts/test_v44_distribution.py",
            "scripts/test_v44_deployment.py",
            "scripts/test_v44_distribution_deployment_conformance.py",
            "scripts/test_v44_adoption_wiring.py",
        }
        self.assertEqual(set(self.closure_input["component_suites"]), expected)
        for relative in expected:
            self.assertTrue((ROOT / relative).is_file(), relative)

    def test_integrated_negative_inference_matrix_is_owned_by_existing_authorities(self) -> None:
        matrix = {
            "source Validation PASS -> artifact qualified": (VALIDATION, BUILD),
            "build output exists -> promoted artifact": (BUILD,),
            "alias -> immutable bytes": (BUILD, DISTRIBUTION),
            "old artifact qualification -> rebuilt bytes": (BUILD,),
            "publication success -> Deployment success": (DISTRIBUTION, DEPLOYMENT),
            "Release READY -> Deployment success": (DEPLOYMENT, RELEASE),
            "staging -> production": (DEPLOYMENT,),
            "credential -> authority": (DEPLOYMENT,),
            "artifact rollback -> data rollback": (DEPLOYMENT,),
            "rollback plan -> rollback executed": (DEPLOYMENT,),
        }
        self.assertEqual(set(self.closure_input["negative_inference_families"]), set(matrix))
        for family, owners in matrix.items():
            with self.subTest(family=family):
                joined = "\n".join(owners)
                if family == "source Validation PASS -> artifact qualified":
                    self.assertIn("A tuple proves only itself", VALIDATION)
                    self.assertIn("New or rebuilt bytes MUST NOT inherit prior artifact Validation", BUILD)
                elif family == "build output exists -> promoted artifact":
                    self.assertIn("The output does not self-promote", joined)
                elif family == "alias -> immutable bytes":
                    self.assertIn("mutable locator alone is not sufficient proof of bytes identity", joined)
                elif family == "old artifact qualification -> rebuilt bytes":
                    self.assertIn("MUST NOT inherit prior artifact Validation", joined)
                elif family == "publication success -> Deployment success":
                    self.assertIn("publication success != Deployment success", joined)
                elif family == "Release READY -> Deployment success":
                    self.assertIn("Release READY != Deployment SUCCESS", joined)
                elif family == "staging -> production":
                    self.assertIn("staging success != production success", joined)
                elif family == "credential -> authority":
                    self.assertIn("credential/tool capability != production mutation authority", joined)
                elif family == "artifact rollback -> data rollback":
                    self.assertIn("artifact rollback != data/schema rollback", joined)
                elif family == "rollback plan -> rollback executed":
                    self.assertIn("rollback plan exists != rollback executed", joined)

    def test_v41_and_v42_authority_boundaries_are_preserved(self) -> None:
        self.assertIn("v4.1 Configuration/Secrets/External-System authority", DEPLOYMENT)
        self.assertIn("v4.2 Data/Migration semantics", DEPLOYMENT)
        self.assertIn("Deployment rollback and v4.2 data/schema rollback remain different owner decisions", ADOPTION)
        self.assertIn("v4.1 Dependency & Toolchain Governance", BUILD)

    def test_historical_evidence_is_not_retrofitted_or_transferred(self) -> None:
        self.assertIn("No version or stage profile may retroactively rewrite them", ADOPTION)
        self.assertIn("requires its own applicable qualification", ADOPTION)
        self.assertIn("old artifact qualification transfers", BUILD)

    def test_fast_path_is_proportional_but_cannot_hide_material_delivery_work(self) -> None:
        self.assertIn("Fast Path", ADOPTION)
        self.assertIn("smallest truthful profile", ADOPTION)
        self.assertIn("cannot skip its material owner evidence", ADOPTION)
        self.assertIn("Fast Path reduces ceremony but cannot be used", BUILD)

    def bound_payload(self) -> dict:
        payload = json.loads(json.dumps(self.closure_input))
        payload["exact_candidate_binding"] = {
            "status": "BOUND",
            "candidate_sha": "1" * 40,
            "candidate_tree": "2" * 40,
            "evidence_location": "synthetic-test-only",
            "reason": "synthetic-test-only",
        }
        for item in payload["required_tuples"]:
            item["status"] = "PASS"
        for gate in payload["required_gates"]:
            gate["status"] = "PASS"
        payload["known_findings"] = []
        return payload

    def test_required_not_run_or_blocked_tuple_cannot_be_green(self) -> None:
        payload = self.bound_payload()
        for status in ("NOT_RUN", "BLOCKED"):
            with self.subTest(status=status):
                variant = json.loads(json.dumps(payload))
                variant["required_tuples"][0]["status"] = status
                self.assertFalse(closure_input_can_be_green(variant))

    def test_required_gate_not_run_or_blocked_cannot_be_green(self) -> None:
        payload = self.bound_payload()
        for status in ("NOT_RUN", "BLOCKED"):
            with self.subTest(status=status):
                variant = json.loads(json.dumps(payload))
                variant["required_gates"][-1]["status"] = status
                self.assertFalse(closure_input_can_be_green(variant))

    def test_unresolved_p0_or_p1_cannot_be_green(self) -> None:
        payload = self.bound_payload()
        for severity in ("P0", "P1"):
            with self.subTest(severity=severity):
                variant = json.loads(json.dumps(payload))
                variant["known_findings"] = [
                    {"severity": severity, "state": "OPEN", "summary": "synthetic-test-only"}
                ]
                self.assertFalse(closure_input_can_be_green(variant))

    def test_builder_closure_input_is_truthfully_blocked_until_external_exact_candidate_evidence(self) -> None:
        self.assertEqual(self.closure_input["closure_input_state"], "BLOCKED")
        self.assertEqual(self.closure_input["exact_candidate_binding"]["status"], "UNBOUND")
        self.assertFalse(closure_input_can_be_green(self.closure_input))
        self.assertIn("Candidate Freeze", self.closure_input["forbidden_builder_conclusions"])
        self.assertIn("Release READY", self.closure_input["forbidden_builder_conclusions"])
        self.assertIn("Version Closure PASS", self.closure_input["forbidden_builder_conclusions"])

    def test_release_authority_remains_external_to_t08(self) -> None:
        self.assertIn("Task/PR PASS is not Release PASS", RELEASE)
        self.assertIn("Never convert NOT_RUN/BLOCKED to PASS", RELEASE)
        self.assertIn("T08 integrates those results and prepares separate Version Closure inputs", ADOPTION)


if __name__ == "__main__":
    unittest.main()
