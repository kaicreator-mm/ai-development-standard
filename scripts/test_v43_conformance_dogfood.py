from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = ROOT / "docs" / "implementation" / "4.3.0" / "dogfood" / "fixtures"
NEGATIVE_FIXTURE = FIXTURE_DIR / "shortcut_negative_matrix.json"
DOGFOOD_FIXTURE = FIXTURE_DIR / "planner_bounded_executor.json"

REGRESSION_COMMANDS = [
    "scripts/test_v43_dag_mutation_contract.py",
    "scripts/test_v43_profile_framework.py",
    "scripts/test_v43_task_decomposition.py",
    "scripts/test_v43_task_dag_governance.py",
    "scripts/test_v43_implementation_quality.py",
    "scripts/test_v43_ts_python_profiles.py",
    "scripts/test_v43_go_java_rust_profiles.py",
    "scripts/test_v43_archetype_profiles.py",
    "scripts/test_v43_adoption_wiring.py",
    "scripts/test_protocol_schemas.py",
    "scripts/verify_standard.py",
]


def read_text(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class V43ConformanceDogfoodTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.negative = load_json(NEGATIVE_FIXTURE)
        cls.dogfood = load_json(DOGFOOD_FIXTURE)

    def test_N01_N10_shortcut_negative_matrix_is_complete_and_executable(self) -> None:
        cases = self.negative["cases"]
        expected_ids = {f"N{idx:02d}" for idx in range(1, 11)}
        self.assertEqual({case["id"] for case in cases}, expected_ids)

        for case in cases:
            with self.subTest(case=case["id"]):
                self.assertEqual(case["expected_disposition"], "REJECT")
                authority_path = case["authority_ref"]
                authority_text = read_text(authority_path)
                for token in case.get("authority_tokens", []):
                    self.assertIn(token, authority_text)

                required_fields = case.get("schema_required_fields", [])
                if required_fields:
                    schema = json.loads(authority_text)
                    self.assertTrue(set(required_fields).issubset(set(schema["required"])))

    def test_D01_profile_resolution_and_dag_mutation_compose_with_existing_T01_T10(self) -> None:
        failures: list[str] = []
        for rel in REGRESSION_COMMANDS:
            proc = subprocess.run(
                [sys.executable, str(ROOT / rel)],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            if proc.returncode != 0:
                failures.append(
                    f"{rel} rc={proc.returncode}\nSTDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}"
                )
        if failures:
            self.fail("\n\n".join(failures))

    def test_D02_planner_output_is_bounded_executor_consumable_without_redesign(self) -> None:
        subject = self.dogfood["subject"]
        self.assertEqual(
            subject["generation_base_sha"],
            "ea5b39bb27ae36886748420d282350dd1a16476e",
        )
        self.assertEqual(
            subject["execution_pack_head_sha"],
            "d9ac745f0897903e95c09eb33b6c54aa49c84cb5",
        )
        self.assertEqual(self.dogfood["evidence_kind"], "SYNTHETIC")
        self.assertEqual(
            self.dogfood["expected_oracle"],
            "CONSUMABLE_WITHOUT_PRODUCT_OR_ARCHITECTURE_REDESIGN",
        )
        self.assertEqual(self.dogfood["actual_result"], "PASS")
        self.assertEqual(self.dogfood["redesign_needed"], "NO")

        for fact in self.dogfood["durable_fact_checks"]:
            text = read_text(fact["ref"])
            for token in fact["tokens"]:
                self.assertIn(token, text)

        bounded = self.dogfood["bounded_executor_interpretation"]
        self.assertGreaterEqual(len(bounded["allowed_write_set"]), 3)
        self.assertGreaterEqual(len(bounded["forbidden_scope"]), 3)
        self.assertEqual(bounded["clarification_or_escalation"], "NONE_REQUIRED")
        self.assertEqual(bounded["redesign_action"], "FORBIDDEN")

    def test_D03_synthetic_evidence_never_claims_real_execution_pass(self) -> None:
        self.assertEqual(self.dogfood["evidence_kind"], "SYNTHETIC")
        real = self.dogfood["real_execution"]
        self.assertIn(real["status"], {"NOT_RUN", "BLOCKED"})
        self.assertNotEqual(real["status"], "PASS")
        self.assertTrue(real["reason"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
