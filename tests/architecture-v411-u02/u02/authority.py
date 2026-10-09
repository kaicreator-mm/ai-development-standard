"""Successor authorization decision logic — the architecture under test.

Implements the U02 hypothesis against current durable facts only:

IF an authorized agent issued one non-idempotent external mutation with
unique effect identity and the ACK was lost after the mutation may have
committed, THEN a distinct successor consuming current canonical
Work/Dispatch/Claim/authority lineage must NOT issue a second unsafe
mutation unless externally-grounded reconciliation (a real, current sink
readback), proven dedup/idempotency, or authorized compensation has been
completed and is exact-current.

Fail-closed: a second claim without enough currentness, an exact-current
human DENY, a changed environment/tenant, a forged (schema-invalid) event,
a corrupt/unreadable plane, or a stale expected HEAD all block. Timeout
alone converts nothing: without a real readback the outcome is UNKNOWN.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .plane import GitFactPlane, PlaneError, ZERO_SHA

ACTIVE_STATES = frozenset({"CLAIMED", "RUNNING"})
TERMINAL_STATES = frozenset({"DONE", "FAILED", "CANCELLED", "TIMEOUT", "STALE", "SUPERSEDED"})

# Decision codes
ACCEPTED = "ACCEPTED"
RESUMED = "RESUMED"
COMMITTED_ALREADY = "COMMITTED_ALREADY"          # durable effect record current; no mutation
RECONCILED_COMMITTED = "RECONCILED_COMMITTED"    # sink readback proves committed; no mutation
RECONCILED_NOT_COMMITTED = "RECONCILED_NOT_COMMITTED"  # sink readback proves absent; legal attempt
RETRY_VIA_DEDUP = "RETRY_VIA_DEDUP"              # adapter-proven dedup; never double-counts
BLOCKED_STALE_HEAD = "BLOCKED_STALE_HEAD"
BLOCKED_TENANT = "BLOCKED_TENANT"
BLOCKED_DENIED = "BLOCKED_DENIED"
BLOCKED_DUPLICATE_CLAIM = "BLOCKED_DUPLICATE_CLAIM"
BLOCKED_PRIOR_OWNERSHIP_ACTIVE = "BLOCKED_PRIOR_OWNERSHIP_ACTIVE"
BLOCKED_AMBIGUOUS_RELEASE = "BLOCKED_AMBIGUOUS_RELEASE"
BLOCKED_OUTCOME_UNKNOWN = "BLOCKED_OUTCOME_UNKNOWN"
BLOCKED_UNVERIFIED = "BLOCKED_UNVERIFIED"
BLOCKED_NO_EFFECT_IDENTITY = "BLOCKED_NO_EFFECT_IDENTITY"
BLOCKED_NO_CLAIM = "BLOCKED_NO_CLAIM"

BLOCKED = "BLOCKED"


@dataclass
class Facts:
    head_sha: str = ZERO_SHA
    claim: dict | None = None            # latest DISPATCH_CLAIMED payload
    claim_terminal: str | None = None    # terminal dispatch_state if released
    release_ambiguous: bool = False
    liveness_expired: bool = False
    human_denial: dict | None = None     # latest exact-current REVIEW_DECISION status=FAIL
    effect_records: list[dict] = field(default_factory=list)  # DONE events carrying effect_id
    plane_broken: str | None = None


def derive_facts(plane: GitFactPlane, work_key: str) -> Facts:
    """Recompute current canonical facts from durable events (fail closed)."""
    facts = Facts(head_sha=ZERO_SHA)
    try:
        facts.head_sha = plane.head_sha()
        events = plane.read_events(work_key)
    except PlaneError as exc:
        facts.plane_broken = str(exc)
        return facts

    denial: dict | None = None
    for ev in events:
        if ev["event"] == "REVIEW_DECISION" and ev.get("status") == "FAIL":
            denial = ev  # latest wins; exact-current by HEAD construction
    facts.human_denial = denial

    claim: dict | None = None
    terminal: str | None = None
    effects: list[dict] = []
    for ev in events:
        if ev["event"] == "DISPATCH_CLAIMED":
            claim = ev
            terminal = None
            effects = []
        elif ev["event"] == "DISPATCH_STATE_CHANGED" and claim is not None:
            state = ev.get("dispatch_state")
            if state in ACTIVE_STATES:
                claim = {**claim, "dispatch_state": state}
                terminal = None
            elif state in TERMINAL_STATES:
                terminal = state
                if state == "DONE" and ev.get("effect_id"):
                    effects.append(ev)
    facts.claim = claim
    facts.claim_terminal = terminal
    facts.effect_records = effects
    if claim is not None:
        facts.release_ambiguous = bool(claim.get("release_ambiguous", False)) and terminal is None
        facts.liveness_expired = bool(claim.get("liveness_expired", False)) and terminal is None
    return facts


@dataclass
class Decision:
    code: str
    may_mutate: bool
    reason: str
    facts: Facts | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "code": self.code,
            "may_mutate": self.may_mutate,
            "reason": self.reason,
            "head_sha": self.facts.head_sha if self.facts else None,
        }


def successor_decision(
    *,
    facts: Facts,
    candidate_operator: str,
    candidate_dispatch: str,
    expected_head_sha: str,
    environment: str,
    authorized_environment: str,
    effect_id: str,
    sink_readback: dict | None = None,
    dedup_proven: bool = False,
) -> Decision:
    """One fail-closed successor decision from exact-current durable facts."""
    if facts.plane_broken is not None:
        return Decision(BLOCKED_UNVERIFIED, False, f"plane unreadable: {facts.plane_broken}", facts)

    if expected_head_sha != facts.head_sha:
        return Decision(
            BLOCKED_STALE_HEAD, False,
            f"stale expected HEAD {expected_head_sha[:12]} != current {facts.head_sha[:12]}", facts,
        )

    if environment != authorized_environment:
        return Decision(
            BLOCKED_TENANT, False,
            f"environment/tenant changed: authorized={authorized_environment} got={environment}", facts,
        )

    if facts.human_denial is not None:
        return Decision(
            BLOCKED_DENIED, False,
            f"exact-current human DENY by {facts.human_denial.get('operator_id')}", facts,
        )

    claim = facts.claim
    active = (
        claim is not None
        and facts.claim_terminal is None
        and claim.get("dispatch_state") in ACTIVE_STATES
    )
    if active:
        same_actor = (
            claim.get("operator_id") == candidate_operator
            and claim.get("dispatch_id") == candidate_dispatch
        )
        if same_actor:
            return Decision(RESUMED, False, "same operator+dispatch: resume, no second mutation", facts)
        if facts.release_ambiguous:
            return Decision(BLOCKED_AMBIGUOUS_RELEASE, False, "release outcome ambiguous: fail closed", facts)
        if facts.liveness_expired:
            return Decision(
                BLOCKED_PRIOR_OWNERSHIP_ACTIVE, False,
                "prior ownership liveness-expired without durable release: fail closed", facts,
            )
        return Decision(
            BLOCKED_DUPLICATE_CLAIM, False,
            f"active claim held by {claim.get('operator_id')} ({claim.get('dispatch_id')})", facts,
        )

    # No active claim. Close the outcome from durable facts first.
    if facts.effect_records:
        recorded = {e.get("effect_id") for e in facts.effect_records}
        if effect_id in recorded:
            return Decision(
                COMMITTED_ALREADY, False,
                "durable effect record exact-current for this effect identity; no repeat", facts,
            )

    # Outcome uncertain (lost ACK domain). Timeout alone converts nothing.
    if sink_readback is None:
        return Decision(
            BLOCKED_OUTCOME_UNKNOWN, False,
            "prior attempt outcome unknown and no externally-grounded readback: UNKNOWN, blocked", facts,
        )
    if effect_id in sink_readback.get("effect_ids", []):
        return Decision(
            RECONCILED_COMMITTED, False,
            f"sink readback proves effect committed (count={sink_readback['count']}): no repeat", facts,
        )
    if dedup_proven:
        return Decision(
            RETRY_VIA_DEDUP, True,
            "adapter-proven effect-ID dedup: legal retry, cannot double-count", facts,
        )
    return Decision(
        RECONCILED_NOT_COMMITTED, True,
        f"sink readback proves effect absent (count={sink_readback['count']}): legal attempt after fresh claim", facts,
    )
