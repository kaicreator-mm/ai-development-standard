"""ai-dev/event-v2 payload builders for the U02 harness.

All payloads validate against the repository's checked-in
``schemas/agent-event-v2.schema.json``. ``effect_id`` on the DONE
DISPATCH_STATE_CHANGED is a demo-additive field (the schema permits
additional properties, as with the T-017 additive fields); it carries the
external effect identity for lineage, never as a substitute for the real
sink readback.
"""

from __future__ import annotations

import time


def _now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def claim_event(*, operator_id: str, session_ref: str, dispatch_id: str,
                head_sha: str, expected_base_sha: str, work_key: str,
                generation: int, environment: str) -> dict:
    return {
        "schema": "ai-dev/event-v2",
        "event": "DISPATCH_CLAIMED",
        "actor_role": "builder",
        "operator_kind": "claude-code",
        "operator_id": operator_id,
        "session_ref": session_ref,
        "transport_actor": "github:kaicreator-mm",
        "task": "#949",
        "sha": head_sha,
        "dispatch_id": dispatch_id,
        "dispatch_state": "CLAIMED",
        "expected_base_sha": expected_base_sha,
        "execution_profile": "LOCAL_BUILDER",
        "occurred_at": _now(),
        "admission_mode": "SINGLE_WRITER_ADMISSION",
        "protected_claim_key": work_key,
        "claim_generation": generation,
        "environment": environment,
    }


def state_changed_event(*, operator_id: str, dispatch_id: str, head_sha: str,
                        state: str, reason: str, work_key: str,
                        generation: int, environment: str,
                        effect_id: str | None = None,
                        liveness_expired: bool | None = None,
                        release_ambiguous: bool | None = None) -> dict:
    payload = {
        "schema": "ai-dev/event-v2",
        "event": "DISPATCH_STATE_CHANGED",
        "actor_role": "builder",
        "operator_kind": "claude-code",
        "operator_id": operator_id,
        "task": "#949",
        "sha": head_sha,
        "dispatch_id": dispatch_id,
        "dispatch_state": state,
        "reason": reason,
        "occurred_at": _now(),
        "protected_claim_key": work_key,
        "claim_generation": generation,
        "environment": environment,
    }
    if effect_id is not None:
        payload["effect_id"] = effect_id
    if liveness_expired is not None:
        payload["liveness_expired"] = liveness_expired
    if release_ambiguous is not None:
        payload["release_ambiguous"] = release_ambiguous
    return payload


def human_denial_event(*, head_sha: str, work_key: str, reason: str) -> dict:
    return {
        "schema": "ai-dev/event-v2",
        "event": "REVIEW_DECISION",
        "actor_role": "reviewer",
        "operator_kind": "human",
        "operator_id": "human:owner",
        "task": "#949",
        "sha": head_sha,
        "review_policy": "required",
        "status": "FAIL",
        "reason": f"DENY: {reason}",
        "next_state": "blocked",
        "occurred_at": _now(),
        "protected_claim_key": work_key,
    }
