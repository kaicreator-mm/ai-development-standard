from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "docs/implementation/4.2.0/dogfood/T07_cross_standard_cases.json"
# Run actual T01–T06 owners, not only a T07-local fixture oracle.
OWNER_SUITES = (
    "test_v42_evolution_contracts.py",            # T01
    "test_v42_interface_compatibility.py",       # T02
    "test_v42_data_migration.py",                # T03
    "test_v42_api_compatibility_conformance.py", # T04
    "test_v42_migration_conformance.py",         # T05: real isolated SQLite
    "test_v42_adoption_wiring.py",               # T06
)
HISTORICAL_PROTOCOL_SUITE = "test_protocol_schemas.py"


def allowed(case: dict) -> bool:
    facts = case["facts"]
    category = case["category"]
    if category == "compatibility_proof":
        return (
            facts["tested_baseline"] == facts["required_baseline"]
            and facts["tested_consumer"] == facts["required_consumer"]
            and all(facts["dimensions"].get(d) == "COMPATIBLE" for d in facts["required_dimensions"])
        )
    if category == "evidence_non_inference":
        return not any(
            facts.get(f, False)
            for f in (
                "claim_compatibility_is_validation_pass",
                "claim_migration_is_deployment_success",
                "claim_validation_is_release_ready",
                "claim_risk_exception_is_remediation",
                "claim_risk_exception_is_validation_pass",
                "claim_new_sha_inherits_old_evidence",
                "claim_fresh_install_proves_upgrade",
            )
        )
    if category == "fast_path":
        return not facts["material_evolution_concern"] or facts["owning_profile_satisfied"]
    if category == "authority_conflict":
        return facts["owner_resolved"] and facts["applicable_current_evidence"]
    raise ValueError(f"unknown illustrative category: {category}")


def required_external_evidence_state(*, required: bool, available: bool, executed: bool) -> str:
    # This is only the non-inference boundary. An executed product result
    # still belongs to the independent owning Validation runner.
    if not required:
        return "NOT_APPLICABLE"
    if not available:
        return "BLOCKED"
    if not executed:
        return "NOT_RUN"
    return "EXECUTION_RESULT_OWNED_ELSEWHERE"


class CrossStandardConformanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fixture = json.loads(CASES.read_text(encoding="utf-8"))

    def test_real_owner_regressions_execute(self) -> None:
        self.assertEqual(self.fixture["owner_suites"], list(OWNER_SUITES))
        for name in (*OWNER_SUITES, HISTORICAL_PROTOCOL_SUITE):
            with self.subTest(owner_suite=name):
                path = ROOT / "scripts" / name
                self.assertTrue(path.is_file(), f"missing owner/protocol suite: {path}")
                env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
                completed = subprocess.run(
                    [sys.executable, str(path)], cwd=ROOT, env=env,
                    text=True, capture_output=True, check=False, timeout=120,
                )
                self.assertEqual(
                    completed.returncode, 0,
                    f"{name} failed (not substitutable by T07 fixture):\n"
                    f"{completed.stdout}\n{completed.stderr}",
                )

    def test_cross_owner_adversarial_cases(self) -> None:
        cases = self.fixture["cases"]
        self.assertGreaterEqual(len(cases), 11)
        ids = [c["id"] for c in cases]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertTrue(any(c["expected_allowed"] for c in cases))
        self.assertTrue(any(not c["expected_allowed"] for c in cases))
        for case in cases:
            with self.subTest(case=case["id"]):
                self.assertEqual(allowed(case), case["expected_allowed"])
                self.assertTrue(case["reason"])

    def test_schema_owners_do_not_infer_other_results(self) -> None:
        compat = json.loads((ROOT / "schemas/compatibility-record-v1.schema.json").read_text(encoding="utf-8"))
        migration = json.loads((ROOT / "schemas/migration-transition-v1.schema.json").read_text(encoding="utf-8"))
        validation = json.loads((ROOT / "schemas/validation-report.schema.json").read_text(encoding="utf-8"))
        outcome = compat["properties"]["dimensions"]["items"]["properties"]["outcome"]["enum"]
        self.assertIn("UNKNOWN", outcome)
        self.assertNotIn("PASS", outcome)
        self.assertTrue({"baseline", "candidate", "contract"}.issubset(compat["required"]))
        self.assertTrue({"source_state_ref", "target_state_ref", "recovery"}.issubset(migration["required"]))
        self.assertFalse({"state", "result", "deployment_result"} & set(migration["properties"]))
        for ref in ("compatibility_record_refs", "migration_transition_refs"):
            self.assertIn(ref, validation["properties"])
            self.assertNotIn(ref, validation["required"])

    def test_representative_historical_v4_validation_payload_remains_accepted(self) -> None:
        # A real schema-validator acceptance test, not merely optional-field inspection.
        from test_protocol_schemas import load_schema, validate_subset

        historical = {
            "repository": "example/repo",
            "tested_sha": "a" * 40,
            "execution_host_role": "local-validator",
            "platform": "linux-x64",
            "runtime_toolchain": "python 3.12",
            "validation_profile": "concern",
            "command": "python scripts/test_protocol_schemas.py",
            "state": "BLOCKED",
        }
        self.assertEqual(validate_subset(historical, load_schema("validation-report.schema.json")), [])
        self.assertNotIn("compatibility_record_refs", historical)
        self.assertNotIn("migration_transition_refs", historical)

    def test_required_external_unavailability_and_risk_cannot_be_upgraded(self) -> None:
        self.assertEqual(required_external_evidence_state(required=True, available=False, executed=False), "BLOCKED")
        self.assertEqual(required_external_evidence_state(required=True, available=True, executed=False), "NOT_RUN")
        self.assertEqual(required_external_evidence_state(required=False, available=False, executed=False), "NOT_APPLICABLE")
        self.assertEqual(required_external_evidence_state(required=True, available=True, executed=True), "EXECUTION_RESULT_OWNED_ELSEWHERE")
        self.assertFalse(allowed({"category": "evidence_non_inference", "facts": {"claim_risk_exception_is_validation_pass": True}}))

    def test_dogfood_is_declared_not_extrapolated(self) -> None:
        self.assertEqual(self.fixture["runtime_dogfood_owner"], "test_v42_migration_conformance.py")
        self.assertEqual(self.fixture["runtime_dogfood_engine"], "sqlite")
        self.assertEqual(self.fixture["unexecuted_environment_policy"], "BLOCKED_OR_NOT_RUN")
        self.assertNotIn("RELEASE_READY", self.fixture.get("claimed_verdicts", []))
        self.assertNotIn("DEPLOYMENT_SUCCESS", self.fixture.get("claimed_verdicts", []))


if __name__ == "__main__":
    unittest.main()
