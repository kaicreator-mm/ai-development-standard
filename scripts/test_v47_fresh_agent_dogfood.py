"""v4.7 T08 fresh-Agent self-dogfood deterministic checks.

This suite validates only committed STATIC_OR_RECONSTRUCTION evidence and the
fail-closed rules needed by the Frozen T08 scenario. Passing this suite is not
proof that a REAL_FRESH_SESSION executed and is not Validation/Review/Release
authority.
"""
from __future__ import annotations

import json
from pathlib import Path
import re
import unittest
from typing import Any, Mapping

ROOT = Path(__file__).resolve().parents[1]
DOGFOOD = ROOT / "docs" / "implementation" / "4.7.0" / "dogfood"
FIXTURE = DOGFOOD / "reconstruction.json"
VALIDATION_REQUEST = DOGFOOD / "VALIDATION_REQUEST.md"
TASK_PACK = ROOT / "docs" / "implementation" / "4.7.0" / "task-packs" / "T08_fresh_agent_self_dogfood.md"
EXECUTION_PACK = ROOT / ".agent" / "execution" / "T-008" / "MANIFEST.yaml"
SHA40 = re.compile(r"^[0-9a-f]{40}$")

EXPECTED_BASE = "3e9c24b671c5619b6024ec79a90b20f6eb1b9346"
EXPECTED_PACK_HEAD = "92a516c05400fae5c57d70a57c5c36dc085dd1cd"
EXPECTED_TASK_PACK_BLOB = "168acd4acf3e23fbb3ca3f6197e4192cb05a9f50"
EXPECTED_L3_BLOB = "6a2000cf9b8bf8024450eb5f0f0704960140095f"
EXPECTED_ISSUE = "https://github.com/kaicreator-mm/ai-development-standard/issues/352"
EXPECTED_PR = "https://github.com/kaicreator-mm/ai-development-standard/pull/624"
EXPECTED_BRANCH = "task/352-v47-fresh-agent-self-dogfood"


def load_fixture() -> dict[str, Any]:
    value = json.loads(FIXTURE.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise AssertionError("dogfood fixture must be an object")
    return value


def choose_current_fact(*, durable: str | None, lower_authority: str | None) -> tuple[str, str | None]:
    """Model T08's minimum precedence rule without becoming an authority owner."""
    if durable:
        return "DURABLE", durable
    if lower_authority:
        return "BLOCKED", None
    return "BLOCKED", None


def subject_currentness(expected: Mapping[str, str], observed: Mapping[str, str]) -> list[str]:
    """Return precise currentness errors for an externally bound exact subject."""
    errors: list[str] = []
    for key in ("issue", "pr", "branch", "head_sha", "tree_sha", "base_sha"):
        expected_value = expected.get(key)
        observed_value = observed.get(key)
        if expected_value != observed_value:
            errors.append(f"{key}: expected {expected_value!r}, observed {observed_value!r}")
    for key in ("head_sha", "tree_sha", "base_sha"):
        value = observed.get(key, "")
        if not SHA40.fullmatch(value):
            errors.append(f"{key}: not an exact 40-char sha")
    return errors


def logical_freshness_eligible(attestation: Mapping[str, Any]) -> bool:
    """Account/transport identity is intentionally irrelevant to logical freshness."""
    return (
        attestation.get("new_logical_session") is True
        and attestation.get("starting_context") == "DURABLE_POINTERS_ONLY"
        and attestation.get("hidden_prior_task_context_used") is False
    )


def real_claim_allowed(*, real_executed: bool, attestation: Mapping[str, Any]) -> bool:
    """STATIC PASS is deliberately not an input to REAL claim admission."""
    return real_executed and logical_freshness_eligible(attestation)


def recursive_keys(value: Any) -> set[str]:
    keys: set[str] = set()
    if isinstance(value, dict):
        for key, child in value.items():
            keys.add(str(key).lower())
            keys.update(recursive_keys(child))
    elif isinstance(value, list):
        for child in value:
            keys.update(recursive_keys(child))
    return keys


class FreshAgentDogfoodTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fixture = load_fixture()

    def test_static_fixture_is_truthfully_classified_and_real_remains_not_run(self) -> None:
        self.assertEqual(self.fixture["evidence_class"], "STATIC_OR_RECONSTRUCTION")
        self.assertEqual(self.fixture["authority_effect"], "NONE")
        self.assertEqual(self.fixture["gate_effect"], "NONE")
        self.assertEqual(self.fixture["real_fresh_session"]["state"], "NOT_RUN")
        self.assertIn("fresh logical Agent/session", self.fixture["real_fresh_session"]["reason"])

    def test_durable_starting_pointers_are_complete_and_do_not_require_chat(self) -> None:
        pointers = self.fixture["starting_pointers"]
        self.assertEqual(pointers["task_issue"], EXPECTED_ISSUE)
        self.assertEqual(pointers["pull_request"], EXPECTED_PR)
        self.assertEqual(pointers["task_branch"], EXPECTED_BRANCH)
        self.assertEqual(pointers["integration_target"], "version/v4.7.0")
        self.assertEqual(
            pointers["task_pack"],
            "docs/implementation/4.7.0/task-packs/T08_fresh_agent_self_dogfood.md",
        )
        self.assertEqual(pointers["execution_pack"], ".agent/execution/T-008/MANIFEST.yaml")
        serialized = json.dumps(pointers, sort_keys=True).lower()
        self.assertNotIn("prior_chat", serialized)
        self.assertNotIn("memory", serialized)

    def test_planning_identity_is_exact_and_self_consistent(self) -> None:
        identity = self.fixture["bound_planning_identity"]
        self.assertEqual(identity["base_sha"], EXPECTED_BASE)
        self.assertEqual(identity["pack_head"], EXPECTED_PACK_HEAD)
        self.assertEqual(identity["task_pack_blob"], EXPECTED_TASK_PACK_BLOB)
        self.assertEqual(identity["l3_blob"], EXPECTED_L3_BLOB)
        for key in ("base_sha", "base_tree", "pack_head", "pack_tree", "task_pack_blob", "l3_blob"):
            self.assertRegex(identity[key], SHA40)

    def test_reconstruction_covers_all_frozen_recovery_outputs(self) -> None:
        recover = self.fixture["recover"]
        expected = {
            "pinned_ads_and_current_authority",
            "canonical_owners",
            "applicable_profiles_and_overrides",
            "task_pr_exact_sha_base",
            "allowed_mutation_and_side_effects",
            "required_gates",
            "next_action_or_blocker",
        }
        self.assertEqual(set(recover), expected)
        self.assertEqual(
            recover["required_gates"],
            [
                "builder-implementation",
                "exact-subject-independent-validation",
                "fresh-independent-review-after-validation-pass",
                "controller-currentness-and-expected-head-merge-authorization",
            ],
        )

    def test_t05_and_t07_are_composed_as_read_only_owner_inputs(self) -> None:
        inputs = self.fixture["composition_inputs"]
        expected_paths = {
            "references/PROGRESSIVE_DISCLOSURE_ROUTING.md",
            "scripts/resolve_standard_read_set.py",
            "references/V47_SEMANTIC_CONFORMANCE_MATRIX.md",
            "scripts/v47_conformance.py",
            "scripts/test_v47_semantic_conformance.py",
        }
        actual_paths = set(inputs["progressive_disclosure_owner"]) | set(inputs["semantic_conformance_owner"])
        self.assertEqual(actual_paths, expected_paths)
        for relative in expected_paths:
            path = ROOT / relative
            self.assertTrue(path.is_file(), relative)
            self.assertTrue(path.read_text(encoding="utf-8").strip(), relative)

    def test_lower_authority_chat_or_memory_cannot_override_durable_fact(self) -> None:
        source, value = choose_current_fact(durable="live-pr-head", lower_authority="stale-chat-head")
        self.assertEqual((source, value), ("DURABLE", "live-pr-head"))
        source, value = choose_current_fact(durable=None, lower_authority="chat-only-value")
        self.assertEqual((source, value), ("BLOCKED", None))

    def test_stale_exact_subject_fails_closed(self) -> None:
        expected = {
            "issue": EXPECTED_ISSUE,
            "pr": EXPECTED_PR,
            "branch": EXPECTED_BRANCH,
            "head_sha": "a" * 40,
            "tree_sha": "b" * 40,
            "base_sha": EXPECTED_BASE,
        }
        self.assertEqual(subject_currentness(expected, dict(expected)), [])
        stale = dict(expected)
        stale["head_sha"] = "c" * 40
        errors = subject_currentness(expected, stale)
        self.assertTrue(any(error.startswith("head_sha:") for error in errors), errors)
        malformed = dict(expected)
        malformed["tree_sha"] = "not-a-sha"
        errors = subject_currentness(expected, malformed)
        self.assertTrue(any("not an exact 40-char sha" in error for error in errors), errors)

    def test_transport_or_account_sameness_is_not_freshness_proof(self) -> None:
        attestation = {
            "new_logical_session": True,
            "starting_context": "DURABLE_POINTERS_ONLY",
            "hidden_prior_task_context_used": False,
            "same_user_account": True,
            "same_transport": True,
        }
        self.assertTrue(logical_freshness_eligible(attestation))
        not_fresh = dict(attestation)
        not_fresh["new_logical_session"] = False
        self.assertFalse(logical_freshness_eligible(not_fresh))
        hidden_context = dict(attestation)
        hidden_context["hidden_prior_task_context_used"] = True
        self.assertFalse(logical_freshness_eligible(hidden_context))

    def test_static_pass_cannot_promote_real_session_claim(self) -> None:
        attestation = {
            "new_logical_session": True,
            "starting_context": "DURABLE_POINTERS_ONLY",
            "hidden_prior_task_context_used": False,
        }
        static_result = "PASS"
        self.assertEqual(static_result, "PASS")
        self.assertFalse(real_claim_allowed(real_executed=False, attestation=attestation))
        self.assertTrue(real_claim_allowed(real_executed=True, attestation=attestation))

    def test_task_and_execution_pack_preserve_write_set_and_gate_boundaries(self) -> None:
        task_pack = TASK_PACK.read_text(encoding="utf-8")
        execution_pack = EXECUTION_PACK.read_text(encoding="utf-8")
        for required in (
            "docs/implementation/4.7.0/dogfood/**",
            "scripts/test_v47_fresh_agent_dogfood.py",
            "exact-subject Validation",
            "Fresh Independent Review",
        ):
            self.assertIn(required, task_pack)
        self.assertIn('base_sha: "3e9c24b671c5619b6024ec79a90b20f6eb1b9346"', execution_pack)
        self.assertIn('review_policy: "required"', execution_pack)

    def test_validation_request_requires_external_exact_subject_and_real_evidence(self) -> None:
        request = VALIDATION_REQUEST.read_text(encoding="utf-8")
        for required in (
            "exact final PR HEAD",
            "REAL_FRESH_SESSION",
            "NOT_RUN/BLOCKED",
            "T08_VALIDATION_RESULT=PASS|FAIL|BLOCKED",
            "FRESH_REVIEW_ADMISSION=YES|NO",
            "Validation never grants merge, Version Closure, or Release authority",
        ):
            self.assertIn(required, request)

    def test_no_private_chain_of_thought_capture_is_required(self) -> None:
        keys = recursive_keys(self.fixture)
        forbidden_keys = {"chain_of_thought", "reasoning_trace", "private_cot", "cot"}
        self.assertTrue(keys.isdisjoint(forbidden_keys), keys & forbidden_keys)
        self.assertFalse(self.fixture["privacy"]["private_chain_of_thought_required"])


if __name__ == "__main__":
    unittest.main()
