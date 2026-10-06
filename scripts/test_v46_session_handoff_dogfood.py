from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
DOGFOOD = ROOT / "docs" / "implementation" / "4.6.0" / "dogfood"
PACKET_PATH = DOGFOOD / "session_operator_handoff_packet.json"
README_PATH = DOGFOOD / "README.md"
VALIDATION_REQUEST_PATH = DOGFOOD / "REAL_RUNTIME_VALIDATION_REQUEST.md"

SHA1_RE = re.compile(r"^[0-9a-f]{40}$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


def load_packet() -> dict:
    return json.loads(PACKET_PATH.read_text(encoding="utf-8"))


def packet_sha256() -> str:
    return hashlib.sha256(PACKET_PATH.read_bytes()).hexdigest()


def reconstruct(packet: dict) -> dict:
    """Stateless reconstruction using only durable packet fields."""
    return {
        "requested_work": "v4.6 T06 session/operator handoff dogfood only",
        "frozen_current_authority": [
            "Frozen Product",
            "Frozen L2",
            "Frozen Task DAG",
            "Frozen L3",
            "T06 Task Pack",
            "merged T02/T03/T04/T05 owner surfaces",
            "live #309 dispatch/currentness facts",
        ],
        "exact_subject_identity": (
            f"{packet['subject']['repository']}#{packet['subject']['issue_number']} "
            f"at authorized base {packet['subject']['authorized_base_sha']} "
            f"on {packet['subject']['task_branch']} "
            f"targeting {packet['subject']['integration_target']}"
        ),
        "completed_evidence_ids": [item["id"] for item in packet["completed_evidence"]],
        "open_finding_ids": [item["id"] for item in packet["findings_blockers"]],
        "next_owner": packet["next_owner_action"]["owner"],
        "next_action": packet["next_owner_action"]["action"],
        "forbidden_assumption_count": len(packet["forbidden_assumptions"]),
    }


class SessionOperatorHandoffDogfoodTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.packet = load_packet()
        cls.readme = README_PATH.read_text(encoding="utf-8")
        cls.validation_request = VALIDATION_REQUEST_PATH.read_text(encoding="utf-8")

    def test_exact_authorized_subject_is_pinned(self) -> None:
        subject = self.packet["subject"]
        self.assertEqual(subject["repository"], "kaicreator-mm/ai-development-standard")
        self.assertEqual(subject["task"], "T06")
        self.assertEqual(subject["issue_number"], 309)
        self.assertEqual(subject["integration_target"], "version/v4.6.0")
        self.assertEqual(subject["task_branch"], "task/309-v46-session-handoff-dogfood")
        self.assertEqual(
            subject["authorized_base_sha"],
            "0458982cd16ba8539085ee0fcc26d2bf46a60ceb",
        )
        self.assertEqual(
            subject["authorized_base_tree"],
            "8853d15ab47b884f23a42ceefb9b301b8525a074",
        )
        self.assertTrue(SHA1_RE.fullmatch(subject["task_pack"]["blob_sha"]))

    def test_authority_refs_are_durable_exact_pointers(self) -> None:
        expected_keys = {
            "frozen_product",
            "frozen_l2",
            "frozen_task_dag",
            "frozen_l3",
            "t02_intent_owner",
            "t03_context_owner",
            "t04_skill_owner",
            "t05_existing_owner_integration",
        }
        self.assertEqual(set(self.packet["authority_refs"]), expected_keys)
        for ref in self.packet["authority_refs"].values():
            self.assertIsInstance(ref["path"], str)
            self.assertTrue(ref["path"])
            self.assertTrue(SHA1_RE.fullmatch(ref["blob_sha"]))

    def test_stateless_reconstruction_matches_expected(self) -> None:
        self.assertEqual(reconstruct(self.packet), self.packet["expected_reconstruction"])

    def test_originating_chat_is_not_required_authority(self) -> None:
        excluded = set(self.packet["fresh_executor_input"]["explicitly_excluded_inputs"])
        self.assertIn("originating chat transcript", excluded)
        self.assertIn("private chain-of-thought", excluded)
        self.assertIn("unrecorded session memory", excluded)
        self.assertNotIn("chat_transcript", self.packet)
        self.assertNotIn("conversation_history", self.packet)

    def test_transport_identity_is_not_logical_independence(self) -> None:
        forbidden = self.packet["forbidden_assumptions"]
        self.assertIn(
            "same GitHub/API transport account => same logical operator/context",
            forbidden,
        )
        self.assertIn(
            "different provider/model metadata => independence proven",
            forbidden,
        )
        self.assertIn("same GitHub/API account != same logical operator/context", self.readme)
        self.assertIn("different provider/model != independence proven", self.readme)

    def test_fixture_result_cannot_be_promoted_to_real_runtime_pass(self) -> None:
        self.assertEqual(
            self.packet["claim_scope"]["fixture_claim"],
            "STATIC_FIXTURE_ONLY",
        )
        self.assertIn(
            "REAL_EXTERNAL_AGENT_RUNTIME_PASS",
            self.packet["claim_scope"]["does_not_prove"],
        )
        finding = self.packet["findings_blockers"][0]
        self.assertEqual(finding["id"], "real-fresh-agent-validation")
        self.assertEqual(finding["status"], "NOT_RUN")
        self.assertIn("No fixture/static result", self.readme)

    def test_validation_request_is_exact_packet_bound_but_requires_live_pr_reread(self) -> None:
        digest = packet_sha256()
        self.assertTrue(SHA256_RE.fullmatch(digest))
        self.assertIn(f"PACKET_SHA256={digest}", self.validation_request)
        self.assertIn("MUST re-read and record the PR live HEAD/tree", self.validation_request)
        self.assertIn("Builder status: `NOT_RUN`", self.validation_request)

    def test_builder_scope_does_not_absorb_downstream_gates(self) -> None:
        forbidden = set(self.packet["request"]["forbidden_scope"])
        self.assertTrue(
            {
                "rewrite T01-T05 owners",
                "absorb T07 adoption wiring",
                "implement v4.7 convergence",
                "self-review",
                "Version Closure",
                "merge",
            }.issubset(forbidden)
        )
        self.assertIn("Controller decides integration/merge", self.packet["remaining_work"][-1])
        self.assertIn("Fresh Independent Review", " ".join(self.packet["remaining_work"]))


if __name__ == "__main__":
    unittest.main()
