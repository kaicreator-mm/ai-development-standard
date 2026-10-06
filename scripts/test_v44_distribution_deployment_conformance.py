from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import queue
import shutil
import subprocess
import sys
import tempfile
import threading
import unittest
from urllib.request import urlopen

from test_protocol_schemas import validate_subset

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "docs/implementation/4.4.0/dogfood/distribution-deployment"
PLAN_SCHEMA = json.loads((ROOT / "schemas/deployment-plan-v1.schema.json").read_text(encoding="utf-8"))
RESULT_SCHEMA = json.loads((ROOT / "schemas/deployment-result-v1.schema.json").read_text(encoding="utf-8"))


def digest(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def sandbox_plan(artifact: str, environment: str = "sandbox:local-1", authority: str = "authority:sandbox-local-test-only") -> dict:
    return {
        "schema_version": 1,
        "plan_id": "sandbox-plan-001",
        "artifact_ref": artifact,
        "target_environment_ref": environment,
        "rollout_strategy": "local-subprocess-test-only",
        "verification_profile_refs": ["probe:loopback-http-health"],
        "rollback_or_forward_policy_ref": "policy:sandbox-stop-and-restore",
        "side_effect_authority_ref": authority,
    }


def result_for_actual_probe(plan: dict, observed: dict | None, *, authority_current: bool) -> dict | None:
    """Test-only bounded construction; NEVER a real external deployment or Release verdict."""
    if not authority_current or plan["target_environment_ref"] != "sandbox:local-1":
        return None
    if not observed or observed.get("environment_ref") != plan["target_environment_ref"]:
        return None
    if observed.get("artifact_digest") != plan["artifact_ref"]:
        return None
    if observed.get("service_state") != "SANDBOX_RUNNING":
        return None
    return {
        "schema_version": 1,
        "result_id": "sandbox-result-001",
        "plan_ref": plan["plan_id"],
        "artifact_ref": observed["artifact_digest"],
        "target_environment_ref": observed["environment_ref"],
        "result_state": "DEPLOYMENT_SUCCEEDED",
        "evidence_refs": ["local-process:observed-http-probe-test-only"],
    }


def start_sandbox_service(artifact: Path) -> tuple[subprocess.Popen[str], int]:
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    process = subprocess.Popen(
        [sys.executable, "-B", str(FIXTURE / "sandbox_service.py"), str(artifact), "sandbox:local-1"],
        cwd=ROOT, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
    )
    if process.stdout is None:
        raise RuntimeError("sandbox fixture stdout unavailable")
    messages: queue.Queue[str] = queue.Queue(maxsize=1)
    reader = threading.Thread(target=lambda: messages.put(process.stdout.readline()), daemon=True)
    reader.start()
    try:
        first = messages.get(timeout=12)
        port = int(first.strip())
    except (queue.Empty, ValueError) as exc:
        process.kill()
        process.wait(timeout=5)
        raise RuntimeError("sandbox loopback service could not start; preserve BLOCKED, not PASS") from exc
    return process, port


class DistributionDeploymentDogfoodTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.cases = json.loads((FIXTURE / "cases.json").read_text(encoding="utf-8"))
        cls.distribution = (ROOT / "standards/DISTRIBUTION_GOVERNANCE_STANDARD.md").read_text(encoding="utf-8")
        cls.deployment = (ROOT / "standards/DEPLOYMENT_GOVERNANCE_STANDARD.md").read_text(encoding="utf-8")

    def test_adversarial_matrix_covers_original_task_pack(self) -> None:
        expected = {"immutable-digest-vs-repointed-channel", "publication-without-rollout",
                    "plan-vs-observed-result", "partial-vs-success", "staging-vs-production",
                    "credential-capability-vs-authority", "rollback-plan-vs-execution",
                    "artifact-vs-data-rollback", "mock-vs-external-provider"}
        self.assertEqual({c["id"] for c in self.cases["cases"]}, expected)
        self.assertEqual(self.cases["status"], "FIXTURE_ONLY_NOT_AN_EXECUTED_RESULT")

    def test_repointed_publication_alias_does_not_transfer_digest_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            first = root / "artifact-v1.bin"
            second = root / "artifact-v2.bin"
            alias = root / "stable-channel"
            first.write_bytes(b"sandbox-release-1")
            second.write_bytes(b"sandbox-release-2")
            digest_v1, digest_v2 = digest(first.read_bytes()), digest(second.read_bytes())
            shutil.copyfile(first, alias)
            self.assertEqual(digest(alias.read_bytes()), digest_v1)
            shutil.copyfile(second, alias)
            self.assertEqual(digest(alias.read_bytes()), digest_v2)
            self.assertNotEqual(digest_v1, digest_v2)
            self.assertIn("MUST NOT transfer", self.distribution)

    def test_plan_is_schema_valid_but_not_an_executed_result(self) -> None:
        plan = sandbox_plan("sha256:" + "0" * 64)
        self.assertEqual(validate_subset(plan, PLAN_SCHEMA), [])
        self.assertIsNone(result_for_actual_probe(plan, None, authority_current=True))
        self.assertIsNone(result_for_actual_probe(plan, {
            "environment_ref": "sandbox:local-1", "artifact_digest": plan["artifact_ref"],
            "service_state": "SANDBOX_RUNNING"}, authority_current=False))
        self.assertIn("Deployment Plan exists/approved -> Deployment succeeded", self.deployment)

    def test_namespaced_failed_partial_rollback_are_not_release_verdicts(self) -> None:
        enum = RESULT_SCHEMA["properties"]["result_state"]["enum"]
        for state in ("DEPLOYMENT_FAILED", "DEPLOYMENT_PARTIAL", "DEPLOYMENT_ROLLED_BACK",
                      "DEPLOYMENT_BLOCKED", "DEPLOYMENT_NOT_RUN"):
            self.assertIn(state, enum)
        self.assertNotIn("PASS", enum)
        self.assertNotIn("READY", enum)
        self.assertIn("artifact rollback != data/schema rollback", self.deployment)
        self.assertIn("rollback plan exists != rollback executed", self.deployment)

    def test_staging_probe_and_tool_capability_never_grant_production_authority(self) -> None:
        expected = "sha256:" + "1" * 64
        staging = sandbox_plan(expected)
        probe = {"environment_ref": "sandbox:local-1", "artifact_digest": expected,
                 "service_state": "SANDBOX_RUNNING"}
        self.assertIsNone(result_for_actual_probe(sandbox_plan(expected, environment="production:account-x"), probe,
                                                   authority_current=True))
        self.assertIsNone(result_for_actual_probe(staging, probe, authority_current=False))
        self.assertIn("staging success != production success", self.deployment)
        self.assertIn("credential/tool capability != production mutation authority", self.deployment)

    def test_real_separate_process_loopback_service_exact_artifact_probe(self) -> None:
        # A REAL local subprocess and HTTP probe of a temporary publication, but
        # ZERO claim of external registry/cloud/prod rollout or Version Closure.
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            built = root / "build-output.bin"
            published = root / "temporary-registry" / "artifact.bin"
            published.parent.mkdir()
            built.write_bytes(b"sandbox-http-service-payload-v1")
            immutable_digest = digest(built.read_bytes())
            shutil.copyfile(built, published)
            self.assertEqual(digest(published.read_bytes()), immutable_digest)
            plan = sandbox_plan(immutable_digest)
            self.assertEqual(validate_subset(plan, PLAN_SCHEMA), [])
            # Successful temporary publication precedes real process execution;
            # it cannot produce even the sandbox result by itself.
            self.assertIsNone(result_for_actual_probe(plan, None, authority_current=True))
            process, port = start_sandbox_service(published)
            try:
                with urlopen(f"http://127.0.0.1:{port}/health", timeout=7) as response:
                    self.assertEqual(response.status, 200)
                    observed = json.loads(response.read())
                result = result_for_actual_probe(plan, observed, authority_current=True)
                self.assertIsNotNone(result)
                self.assertEqual(validate_subset(result, RESULT_SCHEMA), [])
                self.assertEqual(result["result_state"], "DEPLOYMENT_SUCCEEDED")
                self.assertEqual(result["artifact_ref"], immutable_digest)
                self.assertEqual(result["target_environment_ref"], "sandbox:local-1")
                self.assertIsNone(result_for_actual_probe(sandbox_plan("sha256:" + "f" * 64), observed,
                                                           authority_current=True))
            finally:
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait(timeout=5)


if __name__ == "__main__":
    unittest.main()
