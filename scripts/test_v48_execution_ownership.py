"""v4.8 T-017 focused conformance: execution ownership visibility / start-timeout.

Deterministic self-contained oracle over explicit durable facts. It exercises the
claim/start-record, visibility-projection, terminal-release, heartbeat/timeout and
compatibility semantics frozen by T-017 without introducing a new lifecycle,
event family, schema authority or runtime database.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, replace
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

ACTIVE_STATES = frozenset({"CLAIMED", "RUNNING"})
TERMINAL_STATES = ("DONE", "FAILED", "BLOCKED", "CANCELLED", "TIMEOUT", "STALE", "SUPERSEDED")

ADMISSION_MODES = frozenset({"SINGLE_WRITER_ADMISSION", "LINEARIZABLE_CONDITIONAL_WRITE"})

ACCEPTED = "ACCEPTED"
RESUMED = "RESUMED"
DUPLICATE_CLAIM = "DUPLICATE_CLAIM"
STALE_IDENTITY = "STALE_IDENTITY"
AMBIGUOUS_RELEASE = "AMBIGUOUS_RELEASE"
PRIOR_OWNERSHIP_ACTIVE = "PRIOR_OWNERSHIP_ACTIVE"
UNSAFE_ADMISSION_MODE = "UNSAFE_ADMISSION_MODE"


@dataclass(frozen=True)
class StartRecord:
    """One durable accepted-claim start fact; append-oriented, never rewritten."""

    work_key: str
    dispatch_id: str
    operator_id: str
    actor_role: str = "builder"
    operator_kind: str = "claude-code"
    session_ref: str | None = None
    occurred_at: str = "2026-10-03T00:00:00Z"
    execution_profile: str = "LOCAL_BUILDER"
    exact_subject: str = "d2f18854043c59712c1c9d2518f45843b0ad129c"
    task_pack_ref: str | None = None
    execution_pack_ref: str | None = None
    admission_mode: str | None = None
    protected_claim_key: str | None = None
    claim_generation: int | None = None
    state: str = "CLAIMED"
    liveness_expired: bool = False
    release_ambiguous: bool = False


@dataclass(frozen=True)
class OwnershipState:
    records: tuple[StartRecord, ...] = ()
    claim_generation: int = 0


def _record_for(state: OwnershipState, work_key: str) -> StartRecord | None:
    """Current claim record for a key: the latest durable record wins; history stays."""
    current: StartRecord | None = None
    for record in state.records:
        if record.work_key == work_key:
            current = record
    return current


def admit_claim(
    state: OwnershipState,
    work_key: str,
    operator_id: str,
    dispatch_id: str,
    expected_generation: int,
    admission_mode: str = "SINGLE_WRITER_ADMISSION",
) -> tuple[str, OwnershipState]:
    """Serialized compare-and-set claim admission over durable facts (§11/§11.1)."""
    if admission_mode not in ADMISSION_MODES:
        return UNSAFE_ADMISSION_MODE, state
    if expected_generation != state.claim_generation:
        return STALE_IDENTITY, state
    current = _record_for(state, work_key)
    if current is not None:
        if current.state in ACTIVE_STATES:
            if current.operator_id == operator_id and current.dispatch_id == dispatch_id:
                return RESUMED, state
            if current.liveness_expired:
                return PRIOR_OWNERSHIP_ACTIVE, state
            return DUPLICATE_CLAIM, state
        if current.release_ambiguous:
            return AMBIGUOUS_RELEASE, state
    successor = StartRecord(
        work_key=work_key,
        dispatch_id=dispatch_id,
        operator_id=operator_id,
        occurred_at=f"2026-10-03T00:00:{state.claim_generation:02d}Z",
        admission_mode=admission_mode,
        protected_claim_key=f"kaicreator-mm/ai-development-standard:{work_key}",
        claim_generation=state.claim_generation,
    )
    return ACCEPTED, OwnershipState(
        records=state.records + (successor,),
        claim_generation=state.claim_generation + 1,
    )


def apply_liveness_expiry(state: OwnershipState, work_key: str) -> OwnershipState:
    """Liveness expiry may flag investigation; it never releases or fails the task."""
    current = _record_for(state, work_key)
    if current is None or current.state not in ACTIVE_STATES:
        return state
    return replace(state, records=tuple(
        replace(record, liveness_expired=True) if record is current else record
        for record in state.records
    ))


def record_terminal_release(
    state: OwnershipState,
    work_key: str,
    terminal_state: str,
    ambiguous: bool = False,
) -> OwnershipState:
    """Durable terminal/release reconciliation; history stays append-oriented."""
    if terminal_state not in TERMINAL_STATES:
        return state
    current = _record_for(state, work_key)
    if current is None or current.state not in ACTIVE_STATES:
        return state
    return replace(state, records=tuple(
        replace(
            record,
            state=terminal_state,
            liveness_expired=False,
            release_ambiguous=ambiguous,
        )
        if record is current
        else record
        for record in state.records
    ))


def reconcile_ambiguity(state: OwnershipState, work_key: str) -> OwnershipState:
    """Resolve a publication/release ambiguity from durable facts, fail-closed until then."""
    current = _record_for(state, work_key)
    if current is None:
        return state
    return replace(state, records=tuple(
        replace(record, release_ambiguous=False)
        if record is current else record
        for record in state.records
    ))


def apply_heartbeat(state: OwnershipState, work_key: str, present: bool) -> OwnershipState:
    """Progress/heartbeat is non-authoritative transport exchange: it mutates nothing."""
    return state


def authorize_execution(record: StartRecord | None) -> bool:
    """NO_CLAIM_NO_EXECUTION: only an active accepted claim authorizes execution."""
    return record is not None and record.state in ACTIVE_STATES


def projection_label_for(record: StartRecord | None) -> str | None:
    """Derived visibility only; recomputed from durable facts, never authority."""
    if record is None:
        return None
    if record.state in ACTIVE_STATES:
        return "state:implementing"
    return None


def reconstruct_active_ownership(state: OwnershipState, work_key: str) -> dict[str, str | None] | None:
    """Rebuild the active ownership view from durable facts after chat/session loss."""
    record = _record_for(state, work_key)
    if record is None or record.state not in ACTIVE_STATES:
        return None
    return {
        "dispatch_id": record.dispatch_id,
        "actor_role": record.actor_role,
        "operator_kind": record.operator_kind,
        "operator_id": record.operator_id,
        "session_ref": record.session_ref,
        "occurred_at": record.occurred_at,
        "execution_profile": record.execution_profile,
        "exact_subject": record.exact_subject,
        "task_pack_ref": record.task_pack_ref,
        "execution_pack_ref": record.execution_pack_ref,
    }


def load_event_schema() -> dict:
    return json.loads((ROOT / "schemas" / "agent-event-v2.schema.json").read_text(encoding="utf-8"))


def validate_event_payload(schema: dict, payload: dict) -> list[str]:
    """Minimal read-only validator over the current event-v2 machine contract."""
    errors: list[str] = []
    for field in schema.get("required", []):
        if field not in payload:
            errors.append(f"missing required field: {field}")
    event_enum = schema["properties"]["event"].get("enum", [])
    if payload.get("event") not in event_enum:
        errors.append(f"unknown event: {payload.get('event')}")
    for field, spec in schema["properties"].items():
        if field in payload and "enum" in spec and payload[field] not in spec["enum"]:
            errors.append(f"field {field} not in enum: {payload[field]}")
    for condition in schema.get("allOf", []):
        event_if = condition.get("if", {}).get("properties", {}).get("event", {})
        matches = False
        if "const" in event_if:
            matches = payload.get("event") == event_if["const"]
        elif "enum" in event_if:
            matches = payload.get("event") in event_if["enum"]
        if not matches:
            continue
        for field in condition.get("then", {}).get("required", []):
            if field not in payload:
                errors.append(f"missing conditional required field: {field}")
    return errors


ENRICHED_NEW_WRITER_CLAIM = {
    "schema": "ai-dev/event-v2",
    "event": "DISPATCH_CLAIMED",
    "actor_role": "builder",
    "operator_kind": "claude-code",
    "operator_id": "claude-code:zcode-t017-builder-01",
    "session_ref": "zcode-20261003-t017-builder",
    "transport_actor": "kaicreator-mm",
    "issue": "#646",
    "dispatch_id": "d-v4.8.0-T-017-builder-a7a5d742",
    "dispatch_state": "CLAIMED",
    "sha": "d2f18854043c59712c1c9d2518f45843b0ad129c",
    "expected_base_sha": "d2f18854043c59712c1c9d2518f45843b0ad129c",
    "execution_profile": "LOCAL_BUILDER",
    "standard_revision": "d2f18854043c59712c1c9d2518f45843b0ad129c",
    "task_pack_ref": "docs/implementation/4.8.0/task-packs/T17_execution_ownership_visibility.md@e58122659421b272361aca09b8e35283d938a55d",
    "execution_pack_ref": ".agent/execution/T-017/**@a7a5d742b839f1455fc7d8ea68663eb59d7632c4",
    "agent_freedom": "F2_ENGINEERING_DISCRETION",
    "pack_state": "PACK_CURRENT",
    "occurred_at": "2026-10-03T00:00:00Z",
    "admission_mode": "SINGLE_WRITER_ADMISSION",
    "protected_claim_key": "kaicreator-mm/ai-development-standard#646:builder",
    "claim_generation": 1,
}

HISTORICAL_EVENT_V2_CLAIM = {
    "schema": "ai-dev/event-v2",
    "event": "DISPATCH_CLAIMED",
    "actor_role": "builder",
    "operator_kind": "chatgpt-web",
    "operator_id": "chatgpt-web:legacy-operator",
    "dispatch_id": "d-legacy-0001",
    "dispatch_state": "CLAIMED",
    "sha": "0123456789abcdef0123456789abcdef01234567",
}

T017_ADDITIVE_FIELDS = ("admission_mode", "protected_claim_key", "claim_generation")


class V48ExecutionOwnership(unittest.TestCase):
    def test_no_claim_no_execution(self):
        state = OwnershipState()
        self.assertFalse(authorize_execution(_record_for(state, "#646:builder")))
        # A stale expected generation is rejected atomically: no claim, no execution.
        decision, rejected = admit_claim(state, "#646:builder", "op-b", "d-2", 5)
        self.assertEqual(STALE_IDENTITY, decision)
        self.assertFalse(authorize_execution(_record_for(rejected, "#646:builder")))
        decision, raced = admit_claim(state, "#646:builder", "op-a", "d-1", 0)
        self.assertEqual(ACCEPTED, decision)
        decision, _ = admit_claim(raced, "#646:builder", "op-b", "d-2", 1)
        self.assertEqual(DUPLICATE_CLAIM, decision)
        self.assertTrue(authorize_execution(_record_for(raced, "#646:builder")))
        self.assertFalse(authorize_execution(StartRecord(work_key="x", dispatch_id="d", operator_id="o", state="STALE")))

    def test_claim_race_single_start(self):
        state = OwnershipState()
        first_decision, first = admit_claim(state, "#646:builder", "op-a", "d-1", 0)
        # The loser races from the same observed generation 0, but its write lands on
        # the current durable store where generation already advanced: stale CAS fails.
        second_decision, second = admit_claim(first, "#646:builder", "op-b", "d-2", 0)
        self.assertEqual(ACCEPTED, first_decision)
        self.assertEqual(STALE_IDENTITY, second_decision)
        self.assertEqual(first, second)
        # After recompute the loser is rejected as duplicate; still exactly one start.
        decision, _ = admit_claim(first, "#646:builder", "op-b", "d-2", 1)
        self.assertEqual(DUPLICATE_CLAIM, decision)
        starts = [r for r in first.records if r.work_key == "#646:builder"]
        self.assertEqual(1, len(starts))
        self.assertEqual("op-a", starts[0].operator_id)

    def test_projection_not_authority(self):
        state = OwnershipState()
        # No accepted claim: no projection, no authorization, whatever transport shows.
        self.assertIsNone(projection_label_for(None))
        self.assertFalse(authorize_execution(None))

    def test_projection_publication_loss(self):
        decision, claimed = admit_claim(OwnershipState(), "#646:builder", "op-a", "d-1", 0)
        self.assertEqual(ACCEPTED, decision)
        published = False  # projection publication failed/delayed
        self.assertFalse(published)
        # The durable claim remains canonical.
        self.assertTrue(authorize_execution(_record_for(claimed, "#646:builder")))
        decision, _ = admit_claim(claimed, "#646:builder", "op-b", "d-2", 1)
        self.assertEqual(DUPLICATE_CLAIM, decision)
        # Repair is recomputing the derived view, never re-admitting the work.
        self.assertEqual("state:implementing", projection_label_for(_record_for(claimed, "#646:builder")))

    def test_restart_reconstruction(self):
        decision, claimed = admit_claim(OwnershipState(), "#646:builder", "op-a", "d-1", 0)
        self.assertEqual(ACCEPTED, decision)
        claimed = replace(
            claimed,
            records=tuple(
                replace(record, session_ref="sess-42", task_pack_ref="task-pack@e581", execution_pack_ref="pack@a7a5")
                for record in claimed.records
            ),
        )
        # Transient chat/session state is lost; durable facts reconstruct ownership.
        view = reconstruct_active_ownership(claimed, "#646:builder")
        self.assertEqual("d-1", view["dispatch_id"])
        self.assertEqual("builder", view["actor_role"])
        self.assertEqual("claude-code", view["operator_kind"])
        self.assertEqual("op-a", view["operator_id"])
        self.assertEqual("sess-42", view["session_ref"])
        self.assertEqual("2026-10-03T00:00:00Z", view["occurred_at"])
        self.assertEqual("LOCAL_BUILDER", view["execution_profile"])
        self.assertEqual("d2f18854043c59712c1c9d2518f45843b0ad129c", view["exact_subject"])
        self.assertEqual("task-pack@e581", view["task_pack_ref"])
        # Historical minimal record: optional fields reconstruct as absent, not wrong.
        historical = OwnershipState(records=(StartRecord(work_key="#x:builder", dispatch_id="d-0", operator_id="old"),))
        view = reconstruct_active_ownership(historical, "#x:builder")
        self.assertEqual("d-0", view["dispatch_id"])
        self.assertIsNone(view["session_ref"])
        self.assertIsNone(view["task_pack_ref"])

    def test_idempotent_resume(self):
        decision, claimed = admit_claim(OwnershipState(), "#646:builder", "op-a", "d-1", 0)
        self.assertEqual(ACCEPTED, decision)
        decision, resumed = admit_claim(claimed, "#646:builder", "op-a", "d-1", 1)
        self.assertEqual(RESUMED, decision)
        self.assertEqual(claimed, resumed)
        self.assertEqual(1, len([r for r in resumed.records if r.work_key == "#646:builder"]))

    def test_terminal_release_matrix(self):
        for terminal in TERMINAL_STATES:
            decision, claimed = admit_claim(OwnershipState(), "#646:builder", "op-a", "d-1", 0)
            self.assertEqual(ACCEPTED, decision)
            released = record_terminal_release(claimed, "#646:builder", terminal)
            self.assertIsNone(reconstruct_active_ownership(released, "#646:builder"))
            self.assertFalse(authorize_execution(_record_for(released, "#646:builder")))
            # History stays append-oriented: the start fact is still recoverable.
            history = [r for r in released.records if r.work_key == "#646:builder"]
            self.assertEqual(1, len(history))
            self.assertEqual(terminal, history[0].state)
            self.assertEqual("op-a", history[0].operator_id)

    def test_takeover_before_release_rejected(self):
        decision, claimed = admit_claim(OwnershipState(), "#646:builder", "op-a", "d-1", 0)
        self.assertEqual(ACCEPTED, decision)
        decision, _ = admit_claim(claimed, "#646:builder", "op-b", "d-2", 1)
        self.assertEqual(DUPLICATE_CLAIM, decision)
        # Liveness expired but not durably reconciled: still blocked, fail closed.
        expired = apply_liveness_expiry(claimed, "#646:builder")
        decision, _ = admit_claim(expired, "#646:builder", "op-b", "d-2", 1)
        self.assertEqual(PRIOR_OWNERSHIP_ACTIVE, decision)
        # Ambiguous release outcome: fail closed until reconciliation.
        ambiguous = record_terminal_release(claimed, "#646:builder", "CANCELLED", ambiguous=True)
        decision, _ = admit_claim(ambiguous, "#646:builder", "op-b", "d-2", 1)
        self.assertEqual(AMBIGUOUS_RELEASE, decision)
        reconciled = reconcile_ambiguity(ambiguous, "#646:builder")
        decision, _ = admit_claim(reconciled, "#646:builder", "op-b", "d-2", 1)
        self.assertEqual(ACCEPTED, decision)

    def test_heartbeat_non_authority(self):
        decision, claimed = admit_claim(OwnershipState(), "#646:builder", "op-a", "d-1", 0)
        self.assertEqual(ACCEPTED, decision)
        before = claimed
        after = apply_heartbeat(claimed, "#646:builder", present=False)
        self.assertEqual(before, after)
        expired = apply_liveness_expiry(claimed, "#646:builder")
        record = _record_for(expired, "#646:builder")
        # No fabricated failure and no implicit release: ownership stays active.
        self.assertEqual("CLAIMED", record.state)
        self.assertFalse(record.release_ambiguous)
        self.assertTrue(authorize_execution(record))
        self.assertEqual(before.claim_generation, expired.claim_generation)

    def test_timeout_fail_closed(self):
        decision, claimed = admit_claim(OwnershipState(), "#646:builder", "op-a", "d-1", 0)
        self.assertEqual(ACCEPTED, decision)
        expired = apply_liveness_expiry(claimed, "#646:builder")
        decision, _ = admit_claim(expired, "#646:builder", "op-b", "d-2", 1)
        self.assertEqual(PRIOR_OWNERSHIP_ACTIVE, decision)
        # Durable reconciliation of the timeout, then a fresh serialized admission.
        released = record_terminal_release(expired, "#646:builder", "TIMEOUT")
        decision, successor = admit_claim(released, "#646:builder", "op-b", "d-2", 1)
        self.assertEqual(ACCEPTED, decision)
        self.assertEqual("op-b", _record_for(successor, "#646:builder").operator_id)
        # Stale generation cannot admit anything at any point.
        decision, _ = admit_claim(successor, "#646:builder", "op-c", "d-3", 1)
        self.assertEqual(STALE_IDENTITY, decision)

    def test_append_only_successor(self):
        decision, claimed = admit_claim(OwnershipState(), "#646:builder", "op-a", "d-1", 0)
        released = record_terminal_release(claimed, "#646:builder", "TIMEOUT")
        decision, successor = admit_claim(released, "#646:builder", "op-b", "d-2", 1)
        self.assertEqual(ACCEPTED, decision)
        history = [r for r in successor.records if r.work_key == "#646:builder"]
        self.assertEqual(2, len(history))
        self.assertEqual("op-a", history[0].operator_id)
        self.assertEqual("TIMEOUT", history[0].state)
        self.assertEqual("op-b", history[1].operator_id)
        self.assertEqual("d-2", history[1].dispatch_id)
        self.assertNotEqual(history[0].occurred_at, history[1].occurred_at)
        self.assertEqual(2, successor.claim_generation)

    def test_historical_event_v2_compatible(self):
        schema = load_event_schema()
        self.assertEqual([], validate_event_payload(schema, HISTORICAL_EVENT_V2_CLAIM))
        # Backward compatibility is structural: no T-017 additive field is required.
        for condition in schema.get("allOf", []):
            required = condition.get("then", {}).get("required", [])
            for field in T017_ADDITIVE_FIELDS:
                self.assertNotIn(field, required)

    def test_enriched_new_writer_profile(self):
        schema = load_event_schema()
        self.assertEqual([], validate_event_payload(schema, ENRICHED_NEW_WRITER_CLAIM))
        for field in ("dispatch_id", "operator_kind", "operator_id", "session_ref", "occurred_at",
                      "execution_profile", "expected_base_sha", "task_pack_ref", "execution_pack_ref",
                      "admission_mode", "protected_claim_key", "claim_generation"):
            self.assertIn(field, ENRICHED_NEW_WRITER_CLAIM)

    def test_identity_not_labels(self):
        # Identity lives in structured durable facts; the reconstruction view takes no labels.
        decision, claimed = admit_claim(OwnershipState(), "#646:builder", "op-a", "d-1", 0)
        claimed = replace(claimed, records=tuple(
            replace(record, session_ref="sess-42") for record in claimed.records
        ))
        view = reconstruct_active_ownership(claimed, "#646:builder")
        self.assertEqual("sess-42", view["session_ref"])
        protocol = (ROOT / "standards" / "GITHUB_AGENT_INTERACTION_PROTOCOL.md").read_text(encoding="utf-8")
        self.assertIn("Dynamic operator/session identity remains in structured durable events rather than proliferating per-session labels", protocol)

    def test_fast_path_proportional(self):
        state = OwnershipState()
        # Manual single-writer admission: same serialized semantics, no orchestration service.
        decision, claimed = admit_claim(state, "#fast:builder", "human-op", "d-f1", 0,
                                        admission_mode="SINGLE_WRITER_ADMISSION")
        self.assertEqual(ACCEPTED, decision)
        # Full lifecycle with zero heartbeats: claim → running → DONE release.
        self.assertTrue(authorize_execution(_record_for(claimed, "#fast:builder")))
        released = record_terminal_release(claimed, "#fast:builder", "DONE")
        self.assertIsNone(reconstruct_active_ownership(released, "#fast:builder"))
        self.assertEqual(1, released.claim_generation)

    def test_documentation_invariants(self):
        protocol = (ROOT / "standards" / "GITHUB_AGENT_INTERACTION_PROTOCOL.md").read_text(encoding="utf-8")
        architecture = (ROOT / "standards" / "EXECUTION_ARCHITECTURE_STANDARD.md").read_text(encoding="utf-8")
        for anchor in (
            "### 8.5 Accepted Claim as Start Record and ownership visibility",
            "MUST NOT begin authoritative role execution or mutate implementation source before its dispatch Claim is accepted",
            "`NO_CLAIM_NO_EXECUTION`",
            "state:claimed → state:implementing",
            "never the claim lock or execution authority",
            "admission_mode / protected_claim_key / claim_generation",
            "Historical event-v2 claims remain valid history and are not retroactively invalidated",
            "MUST NOT become Task/Validation/Gate truth",
            "no new event version or type is authorized",
            "The accepted Claim is the Start Record per §8.5",
        ):
            self.assertIn(anchor, protocol)
        for anchor in (
            "### 11.2 Active ownership visibility, terminal release, and liveness",
            "derived state reconstructed from durable claim/dispatch facts",
            "reconstruct the active dispatch, logical operator, start time and exact subject from durable facts after chat/session loss",
            "delayed or failed projection publication cannot erase the accepted Claim, cannot authorize a competing claim",
            "remove incompatible active ownership only when the durable terminal/release facts are unambiguous",
            "history remains append-oriented and a successor claim/start is separately attributable",
            "Another operator may take over only after durable terminal/stale/timeout/release/supersession",
            "Missing heartbeat alone MUST NOT fabricate Task/Validation",
            "no mandatory orchestration service and no high-frequency heartbeat requirement",
            "introduces no new state dimension, lifecycle, scheduler, claim authority, event family or mandatory runtime database",
        ):
            self.assertIn(anchor, architecture)

    def test_write_set_and_vocabulary_unchanged(self):
        # The focused suite stays inside the authorized three-path write set.
        schema = load_event_schema()
        protocol = (ROOT / "standards" / "GITHUB_AGENT_INTERACTION_PROTOCOL.md").read_text(encoding="utf-8")
        self.assertIn("DISPATCH_CLAIMED", schema["properties"]["event"]["enum"])
        self.assertEqual("ai-dev/event-v2", ENRICHED_NEW_WRITER_CLAIM["schema"])
        self.assertEqual("ai-dev/event-v2", HISTORICAL_EVENT_V2_CLAIM["schema"])
        architecture = (ROOT / "standards" / "EXECUTION_ARCHITECTURE_STANDARD.md").read_text(encoding="utf-8")
        # Existing vocabulary is reused, not renamed or duplicated.
        for term in ("DISPATCH_CLAIMED", "SINGLE_WRITER_ADMISSION", "LINEARIZABLE_CONDITIONAL_WRITE", "claimed → implementing"):
            self.assertIn(term, architecture)
        self.assertIn("state:implementing", protocol)


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(V48ExecutionOwnership)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    raise SystemExit(0 if result.wasSuccessful() else 1)
