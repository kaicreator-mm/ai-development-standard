from __future__ import annotations

import copy
import json
from pathlib import Path
import re
import unittest

from test_protocol_schemas import load_schema, validate_subset


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = ROOT / "fixtures" / "v48_contract_compatibility" / "cases.json"

TASK_LEARNING = load_schema("task-learning-v1.schema.json")
AGENT_PROFILE = load_schema("agent-capability-profile-v1.schema.json")
CAPABILITY_EVIDENCE = load_schema("agent-capability-evidence-v1.schema.json")
INTERCHANGE = load_schema("interchange-envelope-v1.schema.json")

IMMUTABLE_GIT_SUBJECT_RE = re.compile(
    r"^git:[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+@[0-9a-f]{40}$"
)


def load_cases() -> dict:
    return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))


def task_learning_applies_to_subject(learning: dict, current_subject_ref: str) -> bool:
    """Frozen T-001 currentness oracle: all exact Git identities must be immutable and equal."""
    refs = (
        learning.get("implementation_subject_ref"),
        learning.get("currentness_ref"),
        current_subject_ref,
    )
    return all(
        isinstance(value, str) and IMMUTABLE_GIT_SUBJECT_RE.fullmatch(value)
        for value in refs
    ) and refs[0] == refs[1] == refs[2]


def capability_evidence_applies_to_subject(evidence: dict, current_subject_ref: str) -> bool:
    """Frozen T-016 currentness oracle: historical evidence never silently rebinds."""
    exact_subject_ref = evidence.get("exact_subject_ref")
    return (
        isinstance(exact_subject_ref, str)
        and bool(exact_subject_ref)
        and exact_subject_ref == current_subject_ref
    )


class V48ContractHistoricalCompatibilityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.cases = load_cases()

    def assert_schema_valid(self, value: dict, schema: dict) -> None:
        self.assertEqual(validate_subset(value, schema), [])

    def assert_schema_rejects_field(
        self, value: dict, schema: dict, field: str, replacement: object
    ) -> None:
        mutated = copy.deepcopy(value)
        mutated[field] = replacement
        self.assertTrue(
            validate_subset(mutated, schema),
            msg=f"{field!r} unexpectedly became part of the owning contract",
        )

    def test_three_v48_contract_families_validate_independently(self) -> None:
        current = self.cases["current_contracts"]
        self.assertEqual(
            set(current),
            {"task_learning", "agent_capability_profile", "agent_capability_evidence"},
        )
        self.assert_schema_valid(current["task_learning"], TASK_LEARNING)
        self.assert_schema_valid(current["agent_capability_profile"], AGENT_PROFILE)
        self.assert_schema_valid(current["agent_capability_evidence"], CAPABILITY_EVIDENCE)

        self.assertEqual(
            {
                TASK_LEARNING["properties"]["schema_version"]["const"],
                AGENT_PROFILE["properties"]["schema_version"]["const"],
                CAPABILITY_EVIDENCE["properties"]["schema_version"]["const"],
            },
            {
                "ai-dev/task-learning-v1",
                "ai-dev/agent-capability-profile-v1",
                "ai-dev/agent-capability-evidence-v1",
            },
        )

    def test_capability_claim_is_not_capability_proof(self) -> None:
        profile = self.cases["current_contracts"]["agent_capability_profile"]
        self.assert_schema_valid(profile, AGENT_PROFILE)
        self.assertIn("reasoning_or_semantic_capability_claims", profile)
        for field in self.cases["negative_fields"]["claim_to_proof"]:
            with self.subTest(field=field):
                self.assert_schema_rejects_field(
                    profile, AGENT_PROFILE, field, ["schema-contract-authoring"]
                )

    def test_capability_evidence_is_not_current_review_validation_or_availability(self) -> None:
        evidence = self.cases["current_contracts"]["agent_capability_evidence"]
        self.assert_schema_valid(evidence, CAPABILITY_EVIDENCE)
        self.assertIn("validation_refs", evidence)
        self.assertIn("review_refs", evidence)
        for field in self.cases["negative_fields"]["evidence_to_current_pass"]:
            with self.subTest(field=field):
                self.assert_schema_rejects_field(
                    evidence, CAPABILITY_EVIDENCE, field, "PASS"
                )

    def test_provider_model_provenance_never_becomes_authority(self) -> None:
        current = self.cases["current_contracts"]
        for owner, schema in (
            ("agent_capability_profile", AGENT_PROFILE),
            ("agent_capability_evidence", CAPABILITY_EVIDENCE),
        ):
            value = current[owner]
            self.assertIn("provider_model_provenance", value)
            self.assert_schema_valid(value, schema)
            for field in self.cases["negative_fields"]["provider_model_to_authority"]:
                with self.subTest(owner=owner, field=field):
                    self.assert_schema_rejects_field(value, schema, field, "AUTHORIZED")

    def test_infrastructure_owner_facts_are_referenced_not_captured(self) -> None:
        current = self.cases["current_contracts"]
        profile = current["agent_capability_profile"]
        evidence = current["agent_capability_evidence"]
        self.assertIn("environment_or_runner_requirement_refs", profile)
        self.assertIn("environment_ref", evidence)
        self.assertIn("runner_or_resource_capability_ref", evidence)
        for field in self.cases["negative_fields"]["infrastructure_owner_capture"]:
            with self.subTest(owner="profile", field=field):
                self.assert_schema_rejects_field(
                    profile, AGENT_PROFILE, field, "copied-owner-fact"
                )
            with self.subTest(owner="evidence", field=field):
                self.assert_schema_rejects_field(
                    evidence, CAPABILITY_EVIDENCE, field, "copied-owner-fact"
                )

    def test_no_fourth_availability_or_exchange_family(self) -> None:
        schema_dir = ROOT / "schemas"
        family_consts: dict[str, str] = {}
        for path in schema_dir.glob("*.schema.json"):
            schema = json.loads(path.read_text(encoding="utf-8"))
            properties = schema.get("properties", {})
            for key in ("schema_version", "protocol_version"):
                const = properties.get(key, {}).get("const")
                if isinstance(const, str):
                    family_consts[path.name] = const

        availability_families = {
            name: const
            for name, const in family_consts.items()
            if "availability" in name.lower() or "availability" in const.lower()
        }
        parallel_exchange_families = {
            name: const
            for name, const in family_consts.items()
            if "agent-exchange" in name.lower() or "agent-exchange" in const.lower()
        }
        self.assertEqual(availability_families, {})
        self.assertEqual(parallel_exchange_families, {})
        self.assertEqual(
            INTERCHANGE["properties"]["protocol_version"]["const"],
            "ai-dev/interchange-v1",
        )
        self.assertFalse(
            (ROOT / "standards" / "AGENT_EXCHANGE_BINDING_STANDARD.md").exists()
        )

    def test_stale_exact_subject_records_remain_historical_and_do_not_rebind(self) -> None:
        current = self.cases["current_contracts"]
        subjects = self.cases["subjects"]
        learning = current["task_learning"]
        evidence = current["agent_capability_evidence"]

        self.assert_schema_valid(learning, TASK_LEARNING)
        self.assert_schema_valid(evidence, CAPABILITY_EVIDENCE)
        self.assertTrue(
            task_learning_applies_to_subject(learning, subjects["observed"])
        )
        self.assertFalse(
            task_learning_applies_to_subject(learning, subjects["successor"])
        )
        self.assertTrue(
            capability_evidence_applies_to_subject(evidence, subjects["observed"])
        )
        self.assertFalse(
            capability_evidence_applies_to_subject(evidence, subjects["successor"])
        )

        stale = copy.deepcopy(evidence)
        stale["exact_subject_ref"] = subjects["stale"]
        self.assert_schema_valid(stale, CAPABILITY_EVIDENCE)
        self.assertFalse(
            capability_evidence_applies_to_subject(stale, subjects["observed"])
        )
        self.assertFalse(
            capability_evidence_applies_to_subject(stale, subjects["successor"])
        )

    def test_task_learning_allows_bounded_rationale_but_rejects_private_cot(self) -> None:
        learning = self.cases["current_contracts"]["task_learning"]
        self.assertIn("rationale_summary", learning)
        self.assert_schema_valid(learning, TASK_LEARNING)
        for field in self.cases["negative_fields"]["private_cot"]:
            with self.subTest(field=field):
                self.assert_schema_rejects_field(
                    learning, TASK_LEARNING, field, "private internal reasoning"
                )

    def test_historical_v4_interchange_payload_remains_valid(self) -> None:
        historical = self.cases["historical_v4"]["interchange_handoff"]
        self.assert_schema_valid(historical, INTERCHANGE)
        self.assertNotIn("agent_capability_profile_ref", historical)
        self.assertNotIn("availability_state", historical)
        self.assertEqual(
            historical["authority_effect"], "CORRELATION_ONLY_NON_AUTHORITATIVE"
        )

    def test_frozen_v4_migration_compatibility_sentinels_remain_intact(self) -> None:
        adoption = json.loads(
            (ROOT / "templates" / "golden" / "V4_ADOPTION_MIGRATION_EXAMPLES.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(adoption["schema"], "ai-dev/v4-adoption-migration-examples:1")
        self.assertFalse(adoption["historical_evidence"]["migration_rewrites_prior_results"])
        self.assertTrue(adoption["historical_evidence"]["prior_identity_and_status_preserved"])

        preserved = {
            row["v34"]: row["v4"] for row in adoption["migration_matrix"]
        }
        self.assertEqual(preserved["task-pack"], "preserved")
        self.assertEqual(preserved["execution-pack"], "preserved-optional")
        self.assertEqual(preserved["ai-dev-event-v2"], "preserved")
        self.assertIn(
            "interchange-correlation-only-non-authoritative",
            adoption["common_non_weakening_invariants"],
        )


if __name__ == "__main__":
    unittest.main()
