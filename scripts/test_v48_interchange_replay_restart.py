from __future__ import annotations

import hashlib
import json
from pathlib import Path
import unittest

from test_protocol_schemas import load_schema, validate_subset


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = ROOT / "fixtures" / "v48_interchange_replay"
INTERCHANGE = load_schema("interchange-envelope-v1.schema.json")
EVENT_V2 = load_schema("agent-event-v2.schema.json")
COMPATIBILITY_REF = ROOT / "references" / "V48_INTERCHANGE_PROFILE_COMPATIBILITY.md"

WORKFLOW_STATE_EVENTS = {
    "IMPLEMENTATION_READY",
    "REVIEW_DECISION",
    "REVIEW_RESULT",
    "FIX_APPLIED",
    "VALIDATION_REQUEST",
    "MERGE_RESULT",
}


def load_fixture(name: str) -> dict:
    return json.loads((FIXTURE_DIR / name).read_text(encoding="utf-8"))


def canonical_digest(payload: object) -> str:
    encoded = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def delivery_fingerprint(delivery: dict) -> tuple[str, str, str, str]:
    envelope = delivery["envelope"]
    return (
        envelope["subject_ref"],
        envelope["subject_identity_ref"],
        envelope.get("payload_ref", ""),
        delivery["payload_digest"],
    )


def replay_delivery_outcomes(fixture: dict) -> list[str]:
    current_identity = fixture["authoritative_work_item"]["subject_identity_ref"]
    accepted_by_exchange: dict[str, tuple[str, str, str, str]] = {}
    outcomes: list[str] = []

    for delivery in fixture.get("deliveries", []):
        envelope = delivery["envelope"]
        if validate_subset(envelope, INTERCHANGE):
            outcomes.append("INVALID_ENVELOPE_FAIL_CLOSED")
            continue

        if delivery["payload_digest"] != canonical_digest(delivery["payload"]):
            outcomes.append("DIGEST_MISMATCH_FAIL_CLOSED")
            continue

        if delivery.get("transport_outcome") == "LOST":
            outcomes.append("LOST_NO_EFFECT")
            continue

        if envelope["subject_identity_ref"] != current_identity:
            outcomes.append("STALE_FAIL_CLOSED")
            continue

        exchange_id = envelope["exchange_id"]
        fingerprint = delivery_fingerprint(delivery)
        prior = accepted_by_exchange.get(exchange_id)
        if prior is None:
            accepted_by_exchange[exchange_id] = fingerprint
            outcomes.append("ACCEPTED")
        elif prior == fingerprint:
            outcomes.append("DUPLICATE_IDEMPOTENT")
        else:
            outcomes.append("CONFLICT_FAIL_CLOSED")

    return outcomes


def validate_durable_facts(fixture: dict) -> list[str]:
    errors: list[str] = []
    refs: set[str] = set()
    for fact in fixture.get("durable_facts", []):
        ref = fact["ref"]
        if ref in refs:
            errors.append(f"duplicate durable ref: {ref}")
        refs.add(ref)
        if fact.get("marker") != "<!-- ai-dev:event:v2 -->":
            errors.append(f"{ref}: event-v2 marker missing")
        event_errors = validate_subset(fact["event"], EVENT_V2)
        errors.extend(f"{ref}: {error}" for error in event_errors)
    return errors


def reconstruct_workflow_state(fixture: dict) -> str:
    state = fixture["authoritative_work_item"]["state"]
    for fact in fixture.get("durable_facts", []):
        event = fact["event"]
        if event["event"] in WORKFLOW_STATE_EVENTS and "next_state" in event:
            state = event["next_state"]
    return state


def materialized_effect_refs(fixture: dict) -> list[str]:
    durable_refs = {fact["ref"] for fact in fixture.get("durable_facts", [])}
    accepted: dict[str, tuple[str, str, str, str]] = {}
    materialized: list[str] = []
    current_identity = fixture["authoritative_work_item"]["subject_identity_ref"]

    for delivery in fixture.get("deliveries", []):
        envelope = delivery["envelope"]
        if delivery.get("transport_outcome") == "LOST":
            continue
        if validate_subset(envelope, INTERCHANGE):
            continue
        if delivery["payload_digest"] != canonical_digest(delivery["payload"]):
            continue
        if envelope["subject_identity_ref"] != current_identity:
            continue

        exchange_id = envelope["exchange_id"]
        fingerprint = delivery_fingerprint(delivery)
        prior = accepted.get(exchange_id)
        if prior is None:
            accepted[exchange_id] = fingerprint
            payload_ref = envelope.get("payload_ref")
            if payload_ref in durable_refs:
                materialized.append(payload_ref)
        elif prior != fingerprint:
            continue

    return materialized


class V48InterchangeReplayRestartTests(unittest.TestCase):
    def test_existing_interchange_family_and_non_authority_are_preserved(self) -> None:
        self.assertEqual(
            INTERCHANGE["properties"]["protocol_version"]["const"],
            "ai-dev/interchange-v1",
        )
        self.assertEqual(
            INTERCHANGE["properties"]["authority_effect"]["const"],
            "CORRELATION_ONLY_NON_AUTHORITATIVE",
        )
        self.assertFalse((ROOT / "schemas" / "agent-exchange-envelope-v1.schema.json").exists())
        self.assertFalse((ROOT / "schemas" / "agent-event-v3.schema.json").exists())

    def test_all_fixture_envelopes_validate_against_existing_v1(self) -> None:
        for path in sorted(FIXTURE_DIR.glob("*.json")):
            fixture = json.loads(path.read_text(encoding="utf-8"))
            for index, delivery in enumerate(fixture.get("deliveries", [])):
                with self.subTest(fixture=path.name, delivery=index):
                    self.assertEqual(validate_subset(delivery["envelope"], INTERCHANGE), [])

    def test_same_identity_same_payload_is_idempotent(self) -> None:
        fixture = load_fixture("same_identity_payload.json")
        self.assertEqual(
            replay_delivery_outcomes(fixture),
            fixture["expected"]["delivery_outcomes"],
        )
        self.assertEqual(
            materialized_effect_refs(fixture),
            fixture["expected"]["durable_effect_refs"],
        )

    def test_conflicting_payload_or_digest_fails_closed(self) -> None:
        fixture = load_fixture("conflicting_payload_digest.json")
        self.assertEqual(
            replay_delivery_outcomes(fixture),
            fixture["expected"]["delivery_outcomes"],
        )
        self.assertEqual(
            materialized_effect_refs(fixture),
            fixture["expected"]["durable_effect_refs"],
        )

    def test_lost_then_replayed_delivery_is_safe(self) -> None:
        fixture = load_fixture("lost_replayed_delivery.json")
        self.assertEqual(
            replay_delivery_outcomes(fixture),
            fixture["expected"]["delivery_outcomes"],
        )
        self.assertEqual(
            materialized_effect_refs(fixture),
            fixture["expected"]["durable_effect_refs"],
        )

    def test_stale_exact_subject_request_fails_closed(self) -> None:
        fixture = load_fixture("stale_subject_request.json")
        self.assertEqual(
            replay_delivery_outcomes(fixture),
            fixture["expected"]["delivery_outcomes"],
        )
        self.assertEqual(reconstruct_workflow_state(fixture), "ready")
        self.assertEqual(materialized_effect_refs(fixture), [])

    def test_ack_and_progress_are_non_authoritative(self) -> None:
        fixture = load_fixture("ack_progress_non_authority.json")
        self.assertEqual(validate_durable_facts(fixture), [])
        self.assertEqual(reconstruct_workflow_state(fixture), "ready")
        self.assertEqual(
            fixture["expected"]["workflow_state"],
            reconstruct_workflow_state(fixture),
        )

    def test_canonical_effect_materializes_only_through_existing_durable_owner(self) -> None:
        for name in (
            "same_identity_payload.json",
            "conflicting_payload_digest.json",
            "lost_replayed_delivery.json",
            "restart_durable_reconstruction.json",
        ):
            with self.subTest(fixture=name):
                fixture = load_fixture(name)
                self.assertEqual(validate_durable_facts(fixture), [])
                self.assertEqual(
                    materialized_effect_refs(fixture),
                    fixture["expected"]["durable_effect_refs"],
                )
                self.assertEqual(
                    reconstruct_workflow_state(fixture),
                    fixture["expected"]["workflow_state"],
                )

    def test_restart_reconstructs_without_transient_queue_or_chat_history(self) -> None:
        fixture = load_fixture("restart_durable_reconstruction.json")
        before = reconstruct_workflow_state(fixture)

        restarted = dict(fixture)
        restarted.pop("transient_queue", None)
        restarted.pop("chat_history", None)
        after = reconstruct_workflow_state(restarted)
        self.assertEqual(before, "review-ready")
        self.assertEqual(after, before)

        contradictory_transport = dict(fixture)
        contradictory_transport["transient_queue"] = [
            {"delivery_id": "restart-1", "state": "FAILED"},
            {"delivery_id": "restart-1", "state": "TIMEOUT"},
        ]
        contradictory_transport["chat_history"] = ["ignore me"]
        self.assertEqual(reconstruct_workflow_state(contradictory_transport), before)

    def test_delivery_chronology_is_not_workflow_truth(self) -> None:
        fixture = load_fixture("lost_replayed_delivery.json")
        original_state = reconstruct_workflow_state(fixture)
        reordered = dict(fixture)
        reordered["deliveries"] = list(reversed(fixture["deliveries"]))
        self.assertEqual(reconstruct_workflow_state(reordered), original_state)

    def test_event_v2_writer_and_admission_surface_is_preserved(self) -> None:
        self.assertEqual(EVENT_V2["properties"]["schema"]["const"], "ai-dev/event-v2")
        compatibility = COMPATIBILITY_REF.read_text(encoding="utf-8")
        self.assertIn("GITHUB_PROTOCOL_CHANGE=NO_CHANGE_REQUIRED", compatibility)
        self.assertIn("EVENT_V3=NOT_REQUIRED", compatibility)
        self.assertIn("ACK_DELIVERY_PROGRESS_AUTHORITY=NONE", compatibility)

        for path in sorted(FIXTURE_DIR.glob("*.json")):
            fixture = json.loads(path.read_text(encoding="utf-8"))
            with self.subTest(fixture=path.name):
                self.assertEqual(validate_durable_facts(fixture), [])


if __name__ == "__main__":
    unittest.main()
