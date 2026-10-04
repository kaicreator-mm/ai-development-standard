from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import unittest
from typing import Callable

ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = ROOT / "docs" / "implementation" / "4.3.0" / "dogfood" / "fixtures"
NEGATIVE_FIXTURE = FIXTURE_DIR / "shortcut_negative_matrix.json"
DOGFOOD_FIXTURE = FIXTURE_DIR / "planner_bounded_executor.json"

TASK_PACK = ROOT / "docs" / "implementation" / "4.3.0" / "task-packs" / "T11_conformance_dogfood.md"
TASK_DAG = ROOT / "docs" / "implementation" / "4.3.0" / "TASK_DAG.md"
PRODUCT = ROOT / "docs" / "implementation" / "4.3.0" / "PRD.md"
ARCHITECTURE = ROOT / "docs" / "implementation" / "4.3.0" / "L2_ARCHITECTURE_EVIDENCE.md"
L3 = ROOT / "docs" / "implementation" / "4.3.0" / "L3_REFERENCE_PACKS.md"
EXECUTION_DIR = ROOT / ".agent" / "execution" / "_legacy" / "v4.3-sequential" / "T-011"
MANIFEST = EXECUTION_DIR / "MANIFEST.yaml"
EXECUTION_CONTRACT = EXECUTION_DIR / "EXECUTION_CONTRACT.md"
IMPLEMENTATION_MAP = EXECUTION_DIR / "IMPLEMENTATION_MAP.md"
FAILURE_MATRIX = EXECUTION_DIR / "FAILURE_MATRIX.yaml"

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


def git_blob_sha(path: Path) -> str:
    data = path.read_text(encoding="utf-8").encode("utf-8")
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def normalize_authority_item(value: str) -> str:
    return value.replace("`", "").strip()


def parse_top_level_yaml_subset(text: str) -> dict[str, object]:
    result: dict[str, object] = {}
    current_list: str | None = None
    for raw in text.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if raw.startswith("  - ") and current_list:
            value = raw[4:].strip()
            cast = result[current_list]
            if not isinstance(cast, list):
                raise AssertionError(f"{current_list} is not a list")
            cast.append(value)
            continue
        if raw.startswith((" ", "\t")):
            continue
        match = re.fullmatch(r"([A-Za-z0-9_]+):(?:\s*(.*))?", raw)
        if not match:
            current_list = None
            continue
        key, raw_value = match.group(1), (match.group(2) or "").strip()
        if raw_value:
            if (
                len(raw_value) >= 2
                and raw_value[0] == raw_value[-1]
                and raw_value[0] in {'"', "'"}
            ):
                raw_value = raw_value[1:-1]
            result[key] = raw_value
            current_list = None
        else:
            result[key] = []
            current_list = key
    return result


def extract_fenced_yaml(markdown: str) -> dict[str, object]:
    match = re.search(r"```yaml\s*\n(.*?)\n```", markdown, flags=re.DOTALL)
    if not match:
        raise AssertionError("expected fenced yaml authority")
    return parse_top_level_yaml_subset(match.group(1))


def extract_markdown_bullets(markdown: str, heading: str) -> list[str]:
    lines = markdown.splitlines()
    try:
        start = lines.index(heading) + 1
    except ValueError as exc:
        raise AssertionError(f"missing heading: {heading}") from exc

    items: list[str] = []
    for raw in lines[start:]:
        if raw.startswith("## "):
            break
        if raw.startswith("- "):
            items.append(normalize_authority_item(raw[2:]))
    if not items:
        raise AssertionError(f"no bullets under {heading}")
    return items


def extract_single_sha(text: str, label: str) -> str:
    match = re.search(rf"{re.escape(label)}:\s*`([0-9a-f]{{40}})`", text)
    if not match:
        raise AssertionError(f"missing SHA binding: {label}")
    return match.group(1)


def extract_execution_forbidden_scope(text: str) -> list[str]:
    match = re.search(
        r"The Builder MUST NOT modify (.*?)\.\s*(?:\n|$)",
        text,
        flags=re.DOTALL,
    )
    if not match:
        raise AssertionError("Execution Contract forbidden scope is missing")
    body = normalize_authority_item(match.group(1)).replace(", or ", ", ")
    items = [item.strip() for item in body.split(", ") if item.strip()]
    if len(items) < 3:
        raise AssertionError("Execution Contract forbidden scope is unexpectedly weak")
    return items


def extract_failure_actions(text: str) -> list[str]:
    actions = re.findall(r"^\s+action:\s*(\S+)\s*$", text, flags=re.MULTILINE)
    if not actions:
        raise AssertionError("failure matrix has no actions")
    return actions


def derive_d02_authority() -> dict[str, object]:
    task_pack_text = TASK_PACK.read_text(encoding="utf-8")
    task_pack = extract_fenced_yaml(task_pack_text)
    manifest_text = MANIFEST.read_text(encoding="utf-8")
    manifest = parse_top_level_yaml_subset(manifest_text)
    execution_text = EXECUTION_CONTRACT.read_text(encoding="utf-8")
    implementation_map_text = IMPLEMENTATION_MAP.read_text(encoding="utf-8")
    failure_text = FAILURE_MATRIX.read_text(encoding="utf-8")
    dag_text = TASK_DAG.read_text(encoding="utf-8")
    product_text = PRODUCT.read_text(encoding="utf-8")
    architecture_text = ARCHITECTURE.read_text(encoding="utf-8")
    l3_text = L3.read_text(encoding="utf-8")

    frozen_product = extract_single_sha(task_pack_text, "Frozen Product")
    frozen_l2 = extract_single_sha(task_pack_text, "Frozen L2")

    if f"Frozen Product Authority: `{frozen_product}`" not in dag_text:
        raise AssertionError("Task DAG Product binding disagrees with Task Pack")
    if f"Frozen L2 Architecture: `{frozen_l2}`" not in dag_text:
        raise AssertionError("Task DAG L2 binding disagrees with Task Pack")
    if "T11 requires T10." not in dag_text:
        raise AssertionError("Task DAG no longer binds T11 to T10")
    if f"Integration target: `{manifest['integration_target']}`" not in dag_text:
        raise AssertionError("Task DAG integration target disagrees with Execution Manifest")
    if "Status: **FROZEN PRODUCT AUTHORITY**" not in product_text:
        raise AssertionError("Product authority is not frozen")
    if "Status: **FROZEN L2 ARCHITECTURE AUTHORITY" not in architecture_text:
        raise AssertionError("L2 authority is not frozen")
    if f"Frozen Product Authority: `{frozen_product}`" not in architecture_text:
        raise AssertionError("L2 Product binding disagrees with Task Pack")
    if "## T11 — Conformance & Dogfood" not in l3_text:
        raise AssertionError("L3 T11 reference is missing")

    actual_task_pack_blob = git_blob_sha(TASK_PACK)
    actual_l3_blob = git_blob_sha(L3)
    if actual_task_pack_blob != manifest["task_pack_blob"]:
        raise AssertionError("Task Pack blob disagrees with Execution Manifest")
    if actual_l3_blob != manifest["l3_blob"]:
        raise AssertionError("L3 blob disagrees with Execution Manifest")

    for token in (
        str(manifest["task_pack_blob"]),
        str(manifest["l3_blob"]),
        str(manifest["base_sha"]),
    ):
        if token not in execution_text:
            raise AssertionError(f"Execution Contract lost exact authority binding: {token}")

    for token in (
        "If satisfying an oracle requires changing an existing semantic owner, stop and raise an owner finding",
        "Selected dogfood must expose durable Product/Architecture/Task-Pack facts",
        "Any hidden redesign means FAIL/route upward, not oracle weakening.",
    ):
        if token not in implementation_map_text:
            raise AssertionError(f"Implementation Map lost D02 boundary: {token}")

    allowed_write_set = extract_markdown_bullets(
        execution_text, "## Builder implementation write set"
    )
    required_actions = extract_markdown_bullets(
        execution_text, "## Required semantic kernel"
    )

    forbidden_scope = task_pack.get("forbidden_scope")
    acceptance = task_pack.get("acceptance")
    required_gates = task_pack.get("required_gates")
    failure_handling = task_pack.get("failure_handling")
    if not all(
        isinstance(value, list)
        for value in (forbidden_scope, acceptance, required_gates, failure_handling)
    ):
        raise AssertionError("Task Pack required list authority is malformed")

    dependency_completion = manifest.get("dependency_completion")
    if dependency_completion != ["T10/#256: done"]:
        raise AssertionError("Execution Manifest dependency completion drifted")

    core_artifacts = manifest.get("core_artifacts")
    if not isinstance(core_artifacts, list) or not core_artifacts:
        raise AssertionError("Execution Manifest core_artifacts is missing")
    execution_core_artifact_blobs = {
        f".agent/execution/_legacy/v4.3-sequential/T-011/{name}": git_blob_sha(EXECUTION_DIR / str(name))
        for name in core_artifacts
    }

    selected_exact_bindings = {
        "repository": manifest["repository"],
        "task_id": manifest["task_id"],
        "issue": manifest["issue"],
        "integration_target": manifest["integration_target"],
        "generation_base_sha": manifest["base_sha"],
        "generation_base_tree": manifest["base_tree"],
        "frozen_product_sha": frozen_product,
        "frozen_l2_sha": frozen_l2,
        "product_ref": "docs/implementation/4.3.0/PRD.md",
        "product_blob": git_blob_sha(PRODUCT),
        "architecture_ref": "docs/implementation/4.3.0/L2_ARCHITECTURE_EVIDENCE.md",
        "architecture_blob": git_blob_sha(ARCHITECTURE),
        "task_dag_ref": "docs/implementation/4.3.0/TASK_DAG.md",
        "task_dag_blob": git_blob_sha(TASK_DAG),
        "task_dag_dependency": "T10",
        "task_pack_ref": manifest["task_pack_ref"],
        "task_pack_blob": actual_task_pack_blob,
        "l3_ref": manifest["l3_ref"],
        "l3_blob": actual_l3_blob,
        "execution_manifest_ref": ".agent/execution/_legacy/v4.3-sequential/T-011/MANIFEST.yaml",
        "execution_manifest_blob": git_blob_sha(MANIFEST),
        "execution_contract_ref": ".agent/execution/_legacy/v4.3-sequential/T-011/EXECUTION_CONTRACT.md",
        "execution_contract_blob": git_blob_sha(EXECUTION_CONTRACT),
        "implementation_map_ref": ".agent/execution/_legacy/v4.3-sequential/T-011/IMPLEMENTATION_MAP.md",
        "implementation_map_blob": git_blob_sha(IMPLEMENTATION_MAP),
        "failure_matrix_ref": ".agent/execution/_legacy/v4.3-sequential/T-011/FAILURE_MATRIX.yaml",
        "failure_matrix_blob": git_blob_sha(FAILURE_MATRIX),
        "execution_core_artifact_blobs": execution_core_artifact_blobs,
        "dependency_completion": dependency_completion,
    }

    subject = {
        "repository": manifest["repository"],
        "integration_target": manifest["integration_target"],
        "generation_base_sha": manifest["base_sha"],
        "generation_base_tree": manifest["base_tree"],
        "task_pack_ref": manifest["task_pack_ref"],
        "execution_contract_ref": ".agent/execution/_legacy/v4.3-sequential/T-011/EXECUTION_CONTRACT.md",
    }

    return {
        "subject": subject,
        "allowed_write_set": allowed_write_set,
        "forbidden_scope": forbidden_scope,
        "execution_forbidden_scope": extract_execution_forbidden_scope(execution_text),
        "acceptance": acceptance,
        "required_actions": required_actions,
        "required_gates": required_gates,
        "failure_handling": failure_handling,
        "failure_actions": extract_failure_actions(failure_text),
        "selected_exact_bindings": selected_exact_bindings,
        "clarification_or_escalation": "NONE_REQUIRED",
        "redesign_action": "FORBIDDEN",
    }


def evaluate_d02(candidate: dict) -> tuple[bool, list[str]]:
    expected = derive_d02_authority()
    errors: list[str] = []

    subject = candidate.get("subject")
    if not isinstance(subject, dict):
        errors.append("subject:missing")
    else:
        for key, value in expected["subject"].items():
            if subject.get(key) != value:
                errors.append(f"subject.{key}")

    bounded = candidate.get("bounded_executor_interpretation")
    if not isinstance(bounded, dict):
        errors.append("bounded_executor_interpretation:missing")
        return False, errors

    for key in (
        "allowed_write_set",
        "forbidden_scope",
        "execution_forbidden_scope",
        "acceptance",
        "required_actions",
        "required_gates",
        "failure_handling",
        "failure_actions",
        "selected_exact_bindings",
        "clarification_or_escalation",
        "redesign_action",
    ):
        if bounded.get(key) != expected[key]:
            errors.append(key)

    if candidate.get("evidence_kind") != "SYNTHETIC":
        errors.append("evidence_kind")
    if (
        candidate.get("expected_oracle")
        != "CONSUMABLE_WITHOUT_PRODUCT_OR_ARCHITECTURE_REDESIGN"
    ):
        errors.append("expected_oracle")

    # Deliberately do not read candidate["actual_result"] or candidate["redesign_needed"].
    # They are report fields, never the D02 oracle.
    return not errors, errors


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

    def test_D02_planner_output_is_authority_derived_and_exact(self) -> None:
        passed, errors = evaluate_d02(self.dogfood)
        self.assertTrue(passed, f"authority-derived D02 mismatch: {errors}")
        self.assertEqual(self.dogfood["actual_result"], "PASS")
        self.assertEqual(self.dogfood["redesign_needed"], "NO")

    def test_D02_negative_probes_fail_closed_even_when_fixture_claims_pass(self) -> None:
        probes: list[tuple[str, Callable[[dict], None]]] = [
            (
                "unauthorized_allowed_path",
                lambda doc: doc["bounded_executor_interpretation"]["allowed_write_set"].append(
                    "standards/UNAUTHORIZED.md"
                ),
            ),
            (
                "weakened_forbidden_scope",
                lambda doc: doc["bounded_executor_interpretation"]["forbidden_scope"].remove(
                    "Product/Architecture redesign"
                ),
            ),
            (
                "wrong_required_action",
                lambda doc: doc["bounded_executor_interpretation"]["required_actions"].__setitem__(
                    0, "claim success from fixture self-assertion"
                ),
            ),
            (
                "missing_required_gate",
                lambda doc: doc["bounded_executor_interpretation"]["required_gates"].pop(),
            ),
            (
                "weakened_failure_handling",
                lambda doc: doc["bounded_executor_interpretation"]["failure_handling"].__setitem__(
                    1, "dogfood needing Product/Architecture redesign => continue anyway"
                ),
            ),
            (
                "mismatched_exact_subject_binding",
                lambda doc: doc["bounded_executor_interpretation"]["selected_exact_bindings"].__setitem__(
                    "generation_base_sha", "0" * 40
                ),
            ),
        ]

        for name, mutate in probes:
            with self.subTest(probe=name):
                candidate = copy.deepcopy(self.dogfood)
                candidate["actual_result"] = "PASS"
                candidate["redesign_needed"] = "NO"
                mutate(candidate)
                passed, errors = evaluate_d02(candidate)
                self.assertFalse(passed, f"{name} unexpectedly passed")
                self.assertTrue(errors, f"{name} produced no fail-closed reason")
                self.assertEqual(candidate["actual_result"], "PASS")
                self.assertEqual(candidate["redesign_needed"], "NO")

    def test_D03_synthetic_evidence_never_claims_real_execution_pass(self) -> None:
        self.assertEqual(self.dogfood["evidence_kind"], "SYNTHETIC")
        real = self.dogfood["real_execution"]
        self.assertIn(real["status"], {"NOT_RUN", "BLOCKED"})
        self.assertNotEqual(real["status"], "PASS")
        self.assertTrue(real["reason"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
