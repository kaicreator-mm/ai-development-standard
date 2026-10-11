"""V411-T06 focused regression: atomic protected claim and lawful unclaimed
WEB→fresh LOCAL reroute (source-bound admission).

Encodes the frozen V411-T06 Task Pack positive/negative oracles (N01–N06,
P07) as section-scoped textual contract checks binding the owner clauses
added to `standards/EXECUTION_ARCHITECTURE_STANDARD.md` (§27.5 atomic
protected claim generations and lawful unclaimed dispatch reroute; §28.5
reroute responsibility attribution and claim-key integrity), plus
fixture-driven decision assertions against an isolated single-writer claim
admission adapter that owns the durable dispatch/generation/resource facts.
Every claim proposal, reroute and claim passes through that one serialized
admission point; there is no side door. Purely local and deterministic; no
network, no runtime execution, no schema or event-family extension (the
adapter publishes only existing §8.4 `DISPATCH_CLAIMED` /
`DISPATCH_STATE_CHANGED` events).

The adapter below is the test oracle for the documented §27.5/§28.5
boundary, not a runtime artifact. Real GitHub multi-host/current-source
claims need real actor-separated readback and stay out of scope here; any
additive schema field proposal is routed to T11 without being edited here.
"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]

STANDARD = "standards/EXECUTION_ARCHITECTURE_STANDARD.md"

S_27_5 = (
    "### 27.5 Atomic protected claim generations and lawful unclaimed dispatch reroute (v4.11, additive)",
    "## 28. Responsibility and control semantics for delegated execution",
)
S_28_5 = (
    "### 28.5 Reroute responsibility attribution and claim-key integrity (v4.11, additive)",
    "> Numbering note:",
)
S_27_3 = (
    "### 27.3 One all-or-none linearization point for claim plus required resources",
    "### 27.4 Crash/publication ambiguity and replacement admission",
)
S_27_4 = (
    "### 27.4 Crash/publication ambiguity and replacement admission",
    "### 27.5 Atomic protected claim generations",
)
S_11_1_1 = (
    "#### 11.1.1 Derived protected claim key, compatibility groups, and admission generations (v4.10, additive)",
    "The same serialization mode MUST protect the earlier dispatch-reservation step.",
)

# Canonical §8.4 event family members the adapter is allowed to publish.
ADAPTER_EVENTS = {"DISPATCH_CLAIMED", "DISPATCH_STATE_CHANGED"}

# Canonical terminal states of the section 11 dispatch lifecycle.
TERMINALS = {"DONE", "COMPLETED", "FAILED", "CANCELLED", "TIMEOUT", "STALE", "SUPERSEDED"}

# Canonical disposition/reason vocabulary used by the adapter decisions.
DISPOSITIONS = {
    "ACCEPTED", "STALE", "INELIGIBLE", "UNKNOWN", "BLOCKED", "REJECTED",
    "STALE_BASE", "TENANT_MISMATCH", "PACK_IDENTITY_DRIFT",
    "GROUP_GRANT_MISSING", "GROUP_GRANT_EXPIRED", "RESOURCE_EXHAUSTED_OR_UNKNOWN",
    "CONDITIONAL_WRITE_REJECTED", "INCOMPATIBLE_ACTIVE_CLAIM", "TERMINAL_DISPATCH",
    "PUBLICATION_OUTCOME_AMBIGUOUS", "DURABLE_READBACK_UNAVAILABLE",
    "ADMISSION_REF_UNRESOLVABLE", "NOT_LAWFUL_CLAIMED_DISPATCH", "DUPLICATE_TERMINAL",
    "IDEMPOTENT_RESUME", "NO_CURRENT_ACCEPTED_REVIEW_EVIDENCE",
    "CLAIM_IS_NOT_REVIEW_EVIDENCE", "RECONCILED", "CLAIM_KEY_SLOT_MANIPULATION",
    "GENERATION_MISMATCH", "NO_SUCH_DISPATCH", "COMPOSITE_ADMITTED", "CLAIMED",
    "REROUTED", "TERMINAL_RECORDED", "WOKEN", "NOT_LAWFUL_FOR_UNCLAIMED",
    "RECONCILIATION_OPEN",
}


def standard_text() -> str:
    return (ROOT / STANDARD).read_text(encoding="utf-8")


def section(bounds: tuple[str, str], text: str | None = None) -> str:
    body = text if text is not None else standard_text()
    start = body.index(bounds[0])
    end = body.index(bounds[1], start)
    return body[start:end]


# ---------------------------------------------------------------------------
# Fixture world: one serialized claim-admission writer over durable facts.
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Decision:
    status: str
    reason: str = ""
    key: str = ""
    expected_generation: int | None = None
    current_generation: int | None = None
    detail: str = ""

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Decision):
            return NotImplemented
        return self.status == other.status and self.reason == other.reason and self.key == other.key


@dataclass(frozen=True)
class ClaimProposal:
    key: str
    expected_generation: int
    operator: str
    session: str
    origin: str  # provenance only: WEB | LOCAL — never an authority input
    base_sha: str
    head_sha: str
    tenant: str
    pack_ref: str
    role: str = "builder"
    group_grant_ref: str | None = None
    resources: tuple[tuple[str, int], ...] = ()


@dataclass
class ClaimRecord:
    operator: str
    session: str
    generation: int


@dataclass
class DispatchRecord:
    dispatch_id: str
    key: str
    role: str
    origin: str
    generation: int
    state: str
    assigned_operator: str | None = None
    admission_ref: str | None = None
    claim: ClaimRecord | None = None
    terminals: list[str] = field(default_factory=list)


class _ConditionalWriteRejected(Exception):
    """Simulated storage-level rejection of one member's conditional write."""


class ResourceLedger:
    """Durable capacity facts: sum(active accepted units bound to G) <= N."""

    def __init__(self, capacity: dict[str, int]):
        self.capacity = dict(capacity)
        self.active: dict[str, int] = {g: 0 for g in capacity}
        self.fail_commit_for: str | None = None

    def check(self, bindings: tuple[tuple[str, int], ...]) -> str | None:
        for group, units in bindings:
            if group not in self.capacity:
                return "RESOURCE_EXHAUSTED_OR_UNKNOWN"
            if self.active[group] + units > self.capacity[group]:
                return "RESOURCE_EXHAUSTED_OR_UNKNOWN"
        return None

    def commit(self, bindings: tuple[tuple[str, int], ...]) -> None:
        # All-or-none conditional transaction: any member failure rolls back
        # every already-committed member before the caller observes the error.
        committed: list[tuple[str, int]] = []
        try:
            for group, units in bindings:
                if group == self.fail_commit_for:
                    raise _ConditionalWriteRejected(group)
                self.active[group] += units
                committed.append((group, units))
        except _ConditionalWriteRejected:
            for group, units in committed:
                self.active[group] -= units
            raise

    def release(self, bindings: tuple[tuple[str, int], ...]) -> None:
        for group, units in bindings:
            self.active[group] -= units


class ClaimAdmissionAdapter:
    """Test oracle for §27.5/§28.5: the designated single-writer admission
    point. It owns the durable dispatch/generation/resource facts, re-reads
    them before every decision, and fails closed on ambiguity."""

    def __init__(self, capacity: dict[str, int] | None = None):
        self.generations: dict[str, int] = {}
        self.dispatches: dict[str, DispatchRecord] = {}
        self.events: list[dict] = []
        self.resources = ResourceLedger(capacity or {})
        self.bound_resources: dict[str, tuple[tuple[str, int], ...]] = {}
        self.ambiguous_keys: set[str] = set()
        self.readback_unavailable = False
        self.current_subject = {"base": "base-AAA", "tenant": "tenant-1", "pack": "pack-v1"}
        self.group_grants: dict[str, tuple[str, bool]] = {}  # group -> (ref, live)
        self._seq = 0

    # -- durable projections -------------------------------------------------

    def snapshot(self) -> dict:
        return {
            "generations": dict(self.generations),
            "dispatches": {
                i: (
                    d.state,
                    d.generation,
                    None if d.claim is None else (d.claim.operator, d.claim.session, d.claim.generation),
                    tuple(d.terminals),
                )
                for i, d in self.dispatches.items()
            },
            "resource_active": dict(self.resources.active),
            "event_count": len(self.events),
        }

    def current_generation(self, key: str) -> int:
        return self.generations.get(key, 1)

    def active_claim_on(self, key: str) -> DispatchRecord | None:
        for d in self.dispatches.values():
            if d.key == key and d.claim is not None and d.state not in TERMINALS:
                return d
        return None

    # -- helpers -------------------------------------------------------------

    def _next(self, prefix: str) -> str:
        self._seq += 1
        return f"{prefix}-{self._seq:03d}"

    def _publish(self, key: str, role: str, origin: str, generation: int,
                 assigned_operator: str | None, state: str = "DELIVERED") -> DispatchRecord:
        dispatch = DispatchRecord(
            dispatch_id=self._next("d"),
            key=key,
            role=role,
            origin=origin,
            generation=generation,
            state=state,
            assigned_operator=assigned_operator,
            admission_ref=self._next("ref"),
        )
        self.dispatches[dispatch.dispatch_id] = dispatch
        self.events.append({
            "type": "DISPATCH_STATE_CHANGED", "key": key, "dispatch_id": dispatch.dispatch_id,
            "state": state, "generation": generation,
        })
        return dispatch

    def seed_web_dispatch(self, key: str, role: str = "builder",
                          operator: str | None = None, state: str = "ACKNOWLEDGED") -> DispatchRecord:
        generation = self.current_generation(key)
        return self._publish(key, role=role, origin="WEB", generation=generation,
                             assigned_operator=operator, state=state)

    def _currentness_rejection(self, proposal: ClaimProposal) -> str | None:
        if proposal.base_sha != self.current_subject["base"]:
            return "STALE_BASE"
        if proposal.tenant != self.current_subject["tenant"]:
            return "TENANT_MISMATCH"
        if proposal.pack_ref != self.current_subject["pack"]:
            return "PACK_IDENTITY_DRIFT"
        group = proposal.key.rsplit(":", 1)[-1]
        if group != "__default__":
            grant = self.group_grants.get(group)
            if grant is None or proposal.group_grant_ref != grant[0]:
                return "GROUP_GRANT_MISSING"
            if not grant[1]:
                return "GROUP_GRANT_EXPIRED"
        return None

    # -- §27.5 generation-bound composite admission (one serialization point) -

    def admit(self, proposal: ClaimProposal) -> Decision:
        if self.readback_unavailable:
            return Decision("UNKNOWN", "DURABLE_READBACK_UNAVAILABLE", proposal.key,
                            proposal.expected_generation, None)
        if proposal.key in self.ambiguous_keys:
            return Decision("UNKNOWN", "PUBLICATION_OUTCOME_AMBIGUOUS", proposal.key,
                            proposal.expected_generation, self.current_generation(proposal.key))
        current = self.current_generation(proposal.key)
        reason = self._currentness_rejection(proposal)
        if reason is not None:
            return Decision("INELIGIBLE", reason, proposal.key, proposal.expected_generation, current)
        if proposal.expected_generation != current:
            return Decision("STALE", "GENERATION_MISMATCH", proposal.key,
                            proposal.expected_generation, current)
        active = self.active_claim_on(proposal.key)
        if active is not None:
            return Decision("REJECTED", "INCOMPATIBLE_ACTIVE_CLAIM", proposal.key,
                            proposal.expected_generation, current)
        resource_reason = self.resources.check(proposal.resources)
        if resource_reason is not None:
            return Decision("INELIGIBLE", resource_reason, proposal.key,
                            proposal.expected_generation, current)
        try:
            self.resources.commit(proposal.resources)
        except _ConditionalWriteRejected:
            return Decision("REJECTED", "CONDITIONAL_WRITE_REJECTED", proposal.key,
                            proposal.expected_generation, current)
        # One serialization point: generation advance, dispatch reservation and
        # claim acceptance commit together or not at all.
        self.generations[proposal.key] = current + 1
        dispatch = self._publish(proposal.key, role=proposal.role, origin=proposal.origin,
                                 generation=current, assigned_operator=proposal.operator,
                                 state="ACKNOWLEDGED")
        dispatch.claim = ClaimRecord(proposal.operator, proposal.session, current)
        self.bound_resources[dispatch.dispatch_id] = proposal.resources
        self.events.append({
            "type": "DISPATCH_CLAIMED", "key": proposal.key, "dispatch_id": dispatch.dispatch_id,
            "operator": proposal.operator, "generation": current, "origin": proposal.origin,
        })
        return Decision("ACCEPTED", "COMPOSITE_ADMITTED", proposal.key,
                        proposal.expected_generation, current, detail=dispatch.dispatch_id)

    # -- §11 claim admission on an existing dispatch --------------------------

    def claim(self, dispatch_id: str, operator: str, session: str,
              expected_generation: int) -> Decision:
        dispatch = self.dispatches.get(dispatch_id)
        if dispatch is None:
            return Decision("UNKNOWN", "NO_SUCH_DISPATCH")
        if self.readback_unavailable:
            return Decision("UNKNOWN", "DURABLE_READBACK_UNAVAILABLE", dispatch.key,
                            expected_generation, None)
        if dispatch.key in self.ambiguous_keys:
            return Decision("UNKNOWN", "PUBLICATION_OUTCOME_AMBIGUOUS", dispatch.key,
                            expected_generation, self.current_generation(dispatch.key))
        current = self.current_generation(dispatch.key)
        if expected_generation != current:
            return Decision("STALE", "GENERATION_MISMATCH", dispatch.key,
                            expected_generation, current)
        if dispatch.state in TERMINALS:
            return Decision("REJECTED", "TERMINAL_DISPATCH", dispatch.key,
                            expected_generation, current)
        if dispatch.claim is not None:
            if dispatch.claim.operator == operator:
                return Decision("ACCEPTED", "IDEMPOTENT_RESUME", dispatch.key,
                                expected_generation, current, detail=dispatch.dispatch_id)
            return Decision("REJECTED", "INCOMPATIBLE_ACTIVE_CLAIM", dispatch.key,
                            expected_generation, current)
        dispatch.claim = ClaimRecord(operator, session, current)
        dispatch.state = "ACKNOWLEDGED"
        self.events.append({
            "type": "DISPATCH_CLAIMED", "key": dispatch.key, "dispatch_id": dispatch_id,
            "operator": operator, "generation": current, "origin": dispatch.origin,
        })
        return Decision("ACCEPTED", "CLAIMED", dispatch.key, expected_generation, current,
                        detail=dispatch_id)

    # -- §27.5 lawful unclaimed reroute (authorized current single writer) ----

    def reroute_unclaimed(self, actor: str, old_dispatch_id: str, new_origin: str,
                          reason: str) -> Decision:
        old = self.dispatches.get(old_dispatch_id)
        if old is None:
            return Decision("UNKNOWN", "NO_SUCH_DISPATCH")
        key = old.key
        if self.readback_unavailable:
            return Decision("BLOCKED", "DURABLE_READBACK_UNAVAILABLE", key)
        if key in self.ambiguous_keys:
            return Decision("BLOCKED", "PUBLICATION_OUTCOME_AMBIGUOUS", key)
        if old.admission_ref is None:
            return Decision("BLOCKED", "ADMISSION_REF_UNRESOLVABLE", key)
        current = self.current_generation(key)
        if old.claim is not None and old.state not in TERMINALS:
            # No stolen claim: the active claim belongs to its owning
            # cancellation/terminal/recovery authority, not to the reroute.
            return Decision("REJECTED", "NOT_LAWFUL_CLAIMED_DISPATCH", key,
                            old.generation, current)
        if old.state in TERMINALS:
            return Decision("REJECTED", "DUPLICATE_TERMINAL", key, old.generation, current)
        # Durable append-only terminal + generation advance g → g+1.
        old.state = "CANCELLED"
        old.terminals.append("CANCELLED")
        self.generations[key] = current + 1
        self.events.append({
            "type": "DISPATCH_STATE_CHANGED", "key": key, "dispatch_id": old_dispatch_id,
            "state": "CANCELLED", "generation": current, "actor": actor, "reason": reason,
        })
        fresh = self._publish(key, role=old.role, origin=new_origin,
                              generation=current + 1, assigned_operator=None)
        return Decision("ACCEPTED", "REROUTED", key, current, current + 1,
                        detail=fresh.dispatch_id)

    def rename_slot_reroute(self, actor: str, old_dispatch_id: str, new_key: str,
                            new_origin: str) -> Decision:
        """§28.5 probe: a reroute that tries to mint a different claim key."""
        old = self.dispatches.get(old_dispatch_id)
        if old is None:
            return Decision("UNKNOWN", "NO_SUCH_DISPATCH")
        if new_key != old.key:
            return Decision("INELIGIBLE", "CLAIM_KEY_SLOT_MANIPULATION", new_key)
        return self.reroute_unclaimed(actor, old_dispatch_id, new_origin, "legal")

    # -- owning-authority terminal (release path) -----------------------------

    def owning_authority_terminal(self, actor: str, dispatch_id: str, kind: str) -> Decision:
        dispatch = self.dispatches.get(dispatch_id)
        if dispatch is None:
            return Decision("UNKNOWN", "NO_SUCH_DISPATCH")
        if dispatch.state in TERMINALS:
            return Decision("REJECTED", "DUPLICATE_TERMINAL", dispatch.key)
        if dispatch.claim is None:
            return Decision("REJECTED", "NOT_LAWFUL_FOR_UNCLAIMED", dispatch.key)
        current = self.current_generation(dispatch.key)
        dispatch.state = kind
        dispatch.terminals.append(kind)
        # A durable terminal on an active claim is the owning-authority
        # resolution: it advances the generation so late claims at g go STALE.
        self.generations[dispatch.key] = current + 1
        for group, units in self.bound_resources.pop(dispatch_id, ()):
            self.resources.release([(group, units)])
        self.events.append({
            "type": "DISPATCH_STATE_CHANGED", "key": dispatch.key,
            "dispatch_id": dispatch_id, "state": kind, "actor": actor,
            "generation": current,
        })
        return Decision("ACCEPTED", "TERMINAL_RECORDED", dispatch.key, current, current + 1,
                        detail=kind)

    def reconcile_publication(self, key: str, outcome: str) -> Decision:
        if outcome == "unknown":
            self.ambiguous_keys.add(key)
            return Decision("BLOCKED", "RECONCILIATION_OPEN", key)
        self.ambiguous_keys.discard(key)
        return Decision("ACCEPTED", "RECONCILED", key)

    # -- §27.5 bounded liveness: wake/drain of downstream blocked_by ----------

    def attempt_wake(self, dependency_ref: str, evidence: dict | None) -> Decision:
        if evidence is None:
            return Decision("BLOCKED", "NO_CURRENT_ACCEPTED_REVIEW_EVIDENCE", dependency_ref)
        if evidence.get("kind") == "claim":
            return Decision("BLOCKED", "CLAIM_IS_NOT_REVIEW_EVIDENCE", dependency_ref)
        return Decision("ACCEPTED", "WOKEN", dependency_ref, detail=evidence.get("subject", ""))


def make_adapter() -> ClaimAdmissionAdapter:
    return ClaimAdmissionAdapter(capacity={"gpu-batch": 2, "singular-device": 1})


KEY = "kaicreator-mm/ai-development-standard#1013:builder:__default__"
KEY_GROUPED = "kaicreator-mm/ai-development-standard#1013:builder:gpu-shared"
KEY_EVADING = "kaicreator-mm/ai-development-standard#1013:builder:evaded"
CONTROLLER = "ctrl-single-writer"
OP_WEB = "op-web-attempt"
OP_LOCAL = "op-local-fresh"
OP_LOCAL_B = "op-local-second"


def proposal(adapter: ClaimAdmissionAdapter, operator: str = OP_WEB, session: str = "s1",
             key: str = KEY, generation: int | None = None, origin: str = "WEB",
             resources: tuple[tuple[str, int], ...] = (), group_grant_ref: str | None = None,
             base: str | None = None, tenant: str | None = None,
             pack: str | None = None) -> ClaimProposal:
    subject = adapter.current_subject
    return ClaimProposal(
        key=key,
        expected_generation=adapter.current_generation(key) if generation is None else generation,
        operator=operator,
        session=session,
        origin=origin,
        base_sha=subject["base"] if base is None else base,
        head_sha="head-111",
        tenant=subject["tenant"] if tenant is None else tenant,
        pack_ref=subject["pack"] if pack is None else pack,
        group_grant_ref=group_grant_ref,
        resources=resources,
    )


# ---------------------------------------------------------------------------
# Section-scoped textual contracts
# ---------------------------------------------------------------------------


class SectionContractTests(unittest.TestCase):
    """Textual contracts: the decision model binds to the added owner clauses."""

    def test_27_5_binds_generations_and_composite_set_to_one_serialization_point(self) -> None:
        section_27_5 = section(S_27_5)
        self.assertIn("binds the section 11.1.1 admission generations and the §27.3 composite admission set", section_27_5)
        self.assertIn("no second scheduler lifecycle, no new event family, no state database", section_27_5)
        self.assertIn("`execution_environment` / `scheduler_origin` provenance (§11.1.1) never becomes authority", section_27_5)
        self.assertIn("a lawful reroute never mints a different protected claim key for the same `(repository, work item, role)` work", section_27_5)
        block = section_27_5[section_27_5.index("```text"): section_27_5.index("```", section_27_5.index("```text") + 1)]
        for member in (
            "expected admission_generation g for the protected claim key",
            "+ the work claim itself",
            "+ every required resource binding (§27.3 set A)",
            "+ exact subject currentness: base/HEAD, tenant/environment scope,",
            "+ a resolvable, unexpired compatibility-group grant for any",
        ):
            with self.subTest(member=member):
                self.assertIn(member, block)

    def test_27_5_requires_all_or_none_acceptance_and_rejects_partial_chains(self) -> None:
        section_27_5 = section(S_27_5)
        self.assertIn("The decision accepts only when the durable current generation equals `g` AND every member of the set commits at that one point; acceptance advances the key's generation exactly once", section_27_5)
        self.assertIn("zero accepted claims, zero owned resource bindings, no partial canonical publication, and no generation advance", section_27_5)
        self.assertIn("A sequence of individually successful per-key or per-resource conditional writes is never composite proof", section_27_5)
        self.assertIn("a partial-success chain MUST NOT be presented as an accepted atomic admission", section_27_5)

    def test_27_5_binds_the_lawful_reroute_preconditions_and_sequence(self) -> None:
        section_27_5 = section(S_27_5)
        self.assertIn("durably provably unclaimed: delivered/acknowledged", section_27_5)
        self.assertIn("condition label DISPATCHED_UNCLAIMED; not a new lifecycle state", section_27_5)
        self.assertIn("the actor is the authorized current single writer for the protected", section_27_5)
        self.assertIn("durable CANCELLED/SUPERSEDED terminal on the old dispatch at its", section_27_5)
        self.assertIn("generation g (append-only; advances the key generation g → g+1)", section_27_5)
        self.assertIn("→ fresh role-correct dispatch published at generation g+1", section_27_5)
        self.assertIn("→ a distinct, independent operator claims it with DISPATCH_CLAIMED", section_27_5)
        self.assertIn("at g+1 (the accepted Claim is the Start Record; Interaction protocol", section_27_5)

    def test_27_5_binds_late_claim_rejection_and_no_seizure(self) -> None:
        section_27_5 = section(S_27_5)
        self.assertIn("Prior accepted facts remain immutable history; the old dispatch ends with exactly one terminal", section_27_5)
        self.assertIn("a late claim presented at the superseded generation `g` resolves `STALE` with zero canonical mutation, no terminal duplication, and no revival from stale proposals", section_27_5)
        self.assertIn("Cancellation of an unclaimed dispatch never rewrites or releases a prior accepted Claim", section_27_5)
        self.assertIn("there is no automatic timeout seizure", section_27_5)

    def test_27_5_binds_no_stolen_claim_and_unknown_outcome_blocking(self) -> None:
        section_27_5 = section(S_27_5)
        self.assertIn("If durable facts show the old dispatch's generation IS claimed", section_27_5)
        self.assertIn("The controller MUST NOT steal, release, or reassign the active claim through a reroute and MUST NOT admit a second claim on the key", section_27_5)
        self.assertIn("Resolution belongs to the claim's owning cancellation/terminal/recovery authority (§11.2, §19)", section_27_5)
        self.assertIn("when the old dispatch's ACK/publication outcome is ambiguous, its canonical admission reference is missing or unresolvable, or the durable readback is unavailable", section_27_5)
        self.assertIn("MUST NOT by itself create such a blocker for an unrelated legal gate", section_27_5)

    def test_27_5_binds_bounded_liveness_wake_and_drain(self) -> None:
        section_27_5 = section(S_27_5)
        self.assertIn("Re-claiming the same dispatch by the same logical operator at the current generation stays idempotent (§11)", section_27_5)
        self.assertIn("wake/drain of downstream real `blocked_by` dependencies MAY proceed only after accepted current Reviewer/Validator evidence for the successor subject under the existing review policy", section_27_5)
        self.assertIn("An accepted Claim is attribution and a Start Record, never a Review or Validation PASS, and MUST NOT reduce a downstream gate by itself", section_27_5)

    def test_28_5_binds_reroute_responsibility_and_key_integrity(self) -> None:
        section_28_5 = section(S_28_5)
        self.assertIn("responsibility reconstructs from existing durable facts (§28.2)", section_28_5)
        self.assertIn("owns and is durably attributable for that cancellation decision", section_28_5)
        self.assertIn("active responsibility for the work stays with that actor under the existing single-writer admission (§11.1)", section_28_5)
        self.assertIn("the fresh dispatch's accepted Claim starts a new attributable responsibility chain (requesting authority → fresh operator)", section_28_5)
        self.assertIn("never derives a second or parallel protected claim key, admission generation, or fresh claim identity for the same work by renaming role, group, session, or slot-4 key segments", section_28_5)
        self.assertIn("key-slot manipulation that would evade duplicate-claim rejection is an authority violation, not a new claim", section_28_5)

    def test_existing_owner_semantics_are_preserved(self) -> None:
        text = standard_text()
        s_27_3 = section(S_27_3, text)
        self.assertIn("The accepted work claim and **all required resource bindings MUST linearize all-or-none at one admission point**", s_27_3)
        self.assertIn("Independent per-key CAS operations, per-resource leases, or a sequence of individually successful reservations are **not** composite proof", s_27_3)
        self.assertIn("work claim accepted + any required resource missing", s_27_3)
        s_27_4 = section(S_27_4, text)
        self.assertIn("the controller MUST fail closed", s_27_4)
        self.assertIn("MUST NOT guess from transient locks, process memory, queue state, ACK/progress, or individually observed per-key writes", s_27_4)
        s_11_1_1 = section(S_11_1_1, text)
        self.assertIn("the derived key serialization is `repo#task:role:group` and is deterministic", s_11_1_1)
        self.assertIn("`admission_generation` is a monotonic compare-and-set counter", s_11_1_1)
        self.assertIn("an identical operator re-claiming the same dispatch at the current generation is idempotent", s_11_1_1)
        for heading in (
            "## 27. v4.8 eligibility and composite resource admission",
            "### 27.1 Owner composition and derived Availability",
            "### 27.2 Hard filters before ranking",
            "### 27.3 One all-or-none linearization point for claim plus required resources",
            "### 27.4 Crash/publication ambiguity and replacement admission",
            "### 27.5 Atomic protected claim generations and lawful unclaimed dispatch reroute (v4.11, additive)",
            "## 28. Responsibility and control semantics for delegated execution",
            "### 28.1 Delegated subwork and responsibility handoff",
            "### 28.2 Reconstructible responsibility and causation",
            "### 28.3 Authority attenuation",
            "### 28.4 Human control points",
            "### 28.5 Reroute responsibility attribution and claim-key integrity (v4.11, additive)",
            "## 29. v4.9 proportional orchestration core",
        ):
            with self.subTest(heading=heading):
                self.assertIn(heading, text)
        # Scope discipline: the T06 delta adds exactly one subsection per
        # owner section and no new top-level section.
        self.assertNotIn("### 27.6", text)
        self.assertNotIn("### 28.6", text)
        self.assertNotIn("## 30.", text)

    def test_no_new_event_family_or_schema_is_declared(self) -> None:
        text = standard_text()
        delta = section(S_27_5, text) + section(S_28_5, text)
        for invented in ("DISPATCH_REROUTED", "ai-dev:event:v3", "agent-event-v3",
                         "DISPATCHED_UNCLAIMED_EVENT", "reroute.schema.json", "claim-registry"):
            with self.subTest(invented=invented):
                self.assertNotIn(invented, delta)
        # The §27.5/§28.5 clauses use only canonical or plain-English tokens.
        allow = {
            "ACK", "ALL", "AND", "CANCELLED", "DISPATCHED_UNCLAIMED", "DISPATCH_CLAIMED",
            "HEAD", "LOCAL", "MAY", "MUST", "NOT", "PASS", "STALE", "SUPERSEDED", "WEB",
        }
        for name, bounds in (("27.5", S_27_5), ("28.5", S_28_5)):
            tokens = set(re.findall(r"\b[A-Z][A-Z0-9_]{2,}\b", section(bounds, text)))
            with self.subTest(section=name):
                self.assertTrue(tokens, tokens)
                self.assertTrue(tokens <= allow, tokens - allow)

    def test_adapter_decisions_use_canonical_dispositions(self) -> None:
        # Sweep the fixture's decision surface and assert the oracle never
        # invents a status or reason outside the canonical vocabulary.
        canonical_statuses = {"ACCEPTED", "STALE", "INELIGIBLE", "UNKNOWN", "BLOCKED", "REJECTED"}
        decisions: list[Decision] = []
        adapter = make_adapter()
        adapter.group_grants["gpu-shared"] = ("#auth@1", False)
        adapter.reconcile_publication(KEY, outcome="unknown")
        adapter.readback_unavailable = True
        old = adapter.seed_web_dispatch(KEY, operator=OP_WEB)
        decisions.append(adapter.reroute_unclaimed(CONTROLLER, old.dispatch_id, "LOCAL", "r"))
        adapter.readback_unavailable = False
        adapter.reconcile_publication(KEY, outcome="unclaimed")
        decisions.append(adapter.rename_slot_reroute(CONTROLLER, old.dispatch_id, KEY_EVADING, "LOCAL"))
        decisions.append(adapter.admit(proposal(adapter, operator=OP_WEB, base="base-OLD")))
        decisions.append(adapter.admit(proposal(adapter, operator=OP_WEB, tenant="tenant-9")))
        decisions.append(adapter.admit(proposal(adapter, operator=OP_WEB, pack="pack-v0")))
        decisions.append(adapter.admit(proposal(adapter, operator=OP_WEB, key=KEY_GROUPED,
                                                group_grant_ref="#forged@0")))
        decisions.append(adapter.admit(proposal(adapter, operator=OP_WEB, generation=99)))
        decisions.append(adapter.admit(proposal(adapter, operator=OP_LOCAL, origin="LOCAL",
                                                resources=(("fabric-switch", 1),))))
        adapter.resources.fail_commit_for = "singular-device"
        decisions.append(adapter.admit(proposal(adapter, operator=OP_WEB,
                                                resources=(("gpu-batch", 1), ("singular-device", 1)))))
        adapter.resources.fail_commit_for = None
        decisions.append(adapter.claim("d-missing", OP_WEB, "s", 1))
        decisions.append(adapter.claim(old.dispatch_id, OP_LOCAL, "s2", old.generation))
        decisions.append(adapter.owning_authority_terminal(CONTROLLER, old.dispatch_id, "CANCELLED"))
        decisions.append(adapter.reroute_unclaimed(CONTROLLER, old.dispatch_id, "WEB", "again"))
        fresh = adapter.admit(proposal(adapter, operator=OP_LOCAL, origin="LOCAL"))
        decisions.append(fresh)
        decisions.append(adapter.claim(fresh.detail, OP_LOCAL, "s-local-fresh", fresh.current_generation))
        decisions.append(adapter.attempt_wake("dep", {"kind": "claim"}))
        decisions.append(adapter.attempt_wake("dep", None))
        decisions.append(adapter.attempt_wake("dep", {"kind": "review", "subject": "x"}))
        statuses = {d.status for d in decisions}
        reasons = {d.reason for d in decisions}
        self.assertTrue(statuses <= canonical_statuses, statuses - canonical_statuses)
        self.assertTrue(reasons <= DISPOSITIONS, reasons - DISPOSITIONS)
        self.assertGreaterEqual(len(decisions), 15)


# ---------------------------------------------------------------------------
# T06-N01: duplicate protected keys across scheduler origins
# ---------------------------------------------------------------------------


class DuplicateKeyRaceTests(unittest.TestCase):
    """N01 + positive: one protected key, racing schedulers, WEB vs LOCAL."""

    def test_n01_same_key_race_admits_exactly_one_claim_regardless_of_origin(self) -> None:
        for first_origin, second_origin in (("WEB", "LOCAL"), ("LOCAL", "WEB")):
            with self.subTest(first=first_origin, second=second_origin):
                adapter = make_adapter()
                # Both schedulers observed the same READY state at generation 1
                # and then race the one serialized admission point.
                first = proposal(adapter, operator=OP_WEB, origin=first_origin)
                second = proposal(adapter, operator=OP_LOCAL, origin=second_origin)
                self.assertEqual(1, first.expected_generation)
                self.assertEqual(1, second.expected_generation)
                winner = adapter.admit(first)
                self.assertEqual(Decision("ACCEPTED", "COMPOSITE_ADMITTED", KEY), winner)
                self.assertEqual(1, winner.current_generation)
                mid = adapter.snapshot()
                loser = adapter.admit(second)
                self.assertEqual(Decision("STALE", "GENERATION_MISMATCH", KEY), loser)
                self.assertEqual(1, loser.expected_generation)
                self.assertEqual(2, loser.current_generation)
                self.assertEqual(mid, adapter.snapshot())  # loser mutated nothing
                claims = [d for d in adapter.dispatches.values() if d.claim is not None]
                self.assertEqual(1, len(claims))
                self.assertEqual(first_origin, claims[0].origin)
                self.assertEqual(2, adapter.current_generation(KEY))

    def test_n01_positive_authorized_group_keys_still_admit_one_claim(self) -> None:
        adapter = make_adapter()
        adapter.group_grants["gpu-shared"] = ("#auth@1", True)
        first = adapter.admit(proposal(adapter, operator=OP_LOCAL, key=KEY_GROUPED,
                                       group_grant_ref="#auth@1", origin="LOCAL"))
        self.assertEqual("ACCEPTED", first.status)
        second = adapter.admit(proposal(adapter, operator=OP_LOCAL_B, session="s2",
                                        key=KEY_GROUPED, group_grant_ref="#auth@1",
                                        origin="LOCAL"))
        # Same semantic key → one active claim; an authorized compatibility
        # group never turns the claim itself into parallel claim keys.
        self.assertEqual(Decision("REJECTED", "INCOMPATIBLE_ACTIVE_CLAIM", KEY_GROUPED), second)


# ---------------------------------------------------------------------------
# T06-N02 / T06-N03: reroute legality
# ---------------------------------------------------------------------------


class RerouteLegalityTests(unittest.TestCase):
    """N02: no stolen claim. N03: lawful unclaimed WEB→fresh LOCAL trace."""

    def test_n02_claimed_web_dispatch_cannot_be_stolen_by_reroute(self) -> None:
        adapter = make_adapter()
        old = adapter.seed_web_dispatch(KEY, operator=OP_WEB)
        claimed = adapter.claim(old.dispatch_id, OP_WEB, "s-web", old.generation)
        self.assertEqual("ACCEPTED", claimed.status)
        before = adapter.snapshot()
        stolen = adapter.reroute_unclaimed(CONTROLLER, old.dispatch_id, "LOCAL", "provenance")
        self.assertEqual(Decision("REJECTED", "NOT_LAWFUL_CLAIMED_DISPATCH", KEY), stolen)
        self.assertEqual(1, stolen.expected_generation)
        self.assertEqual(before, adapter.snapshot())
        # No second LOCAL claim can appear on the key while the claim is active.
        second = adapter.admit(proposal(adapter, operator=OP_LOCAL, origin="LOCAL"))
        self.assertEqual(Decision("REJECTED", "INCOMPATIBLE_ACTIVE_CLAIM", KEY), second)

    def test_n02_positive_only_the_owning_authority_resolves_a_claimed_dispatch(self) -> None:
        adapter = make_adapter()
        old = adapter.seed_web_dispatch(KEY, operator=OP_WEB)
        adapter.claim(old.dispatch_id, OP_WEB, "s-web", old.generation)
        released = adapter.owning_authority_terminal(CONTROLLER, old.dispatch_id, "CANCELLED")
        self.assertEqual("ACCEPTED", released.status)
        self.assertEqual(["CANCELLED"], old.terminals)
        self.assertEqual(2, adapter.current_generation(KEY))
        # After the durable owning-authority terminal, the key is free again.
        fresh = adapter.admit(proposal(adapter, operator=OP_LOCAL, origin="LOCAL"))
        self.assertEqual("ACCEPTED", fresh.status)

    def test_n03_lawful_unclaimed_web_to_fresh_local_reroute_full_trace(self) -> None:
        adapter = make_adapter()
        old = adapter.seed_web_dispatch(KEY, operator=OP_WEB)
        self.assertIsNone(old.claim)  # durably provably unclaimed
        events_before = deepcopy(adapter.events)
        rerouted = adapter.reroute_unclaimed(CONTROLLER, old.dispatch_id, "LOCAL",
                                             "unclaimed web proposal; work must run LOCAL")
        self.assertEqual(Decision("ACCEPTED", "REROUTED", KEY), rerouted)
        self.assertEqual(1, rerouted.expected_generation)
        self.assertEqual(2, rerouted.current_generation)
        # Old dispatch: exactly one durable append-only terminal, history kept.
        self.assertEqual(["CANCELLED"], old.terminals)
        self.assertEqual("CANCELLED", old.state)
        fresh = adapter.dispatches[rerouted.detail]
        self.assertEqual("LOCAL", fresh.origin)
        self.assertEqual("builder", fresh.role)  # role-correct successor
        self.assertEqual(KEY, fresh.key)  # same protected key, same semantic slots
        self.assertEqual(2, fresh.generation)
        self.assertEqual(2, adapter.current_generation(KEY))
        # Prior events remain historical: prefix unchanged, append-only.
        self.assertEqual(events_before, adapter.events[: len(events_before)])
        # A distinct, independent fresh LOCAL operator claims at g+1.
        claimed = adapter.claim(fresh.dispatch_id, OP_LOCAL, "s-local-fresh", 2)
        self.assertEqual(Decision("ACCEPTED", "CLAIMED", KEY), claimed)
        self.assertNotEqual(OP_WEB, fresh.claim.operator)
        self.assertNotEqual(CONTROLLER, fresh.claim.operator)
        # Late WEB claim at the superseded generation g resolves STALE.
        late = adapter.claim(fresh.dispatch_id, OP_WEB, "s-web", 1)
        self.assertEqual(Decision("STALE", "GENERATION_MISMATCH", KEY), late)
        self.assertEqual(1, late.expected_generation)
        self.assertEqual(2, late.current_generation)
        # No duplicate terminal on the old dispatch; no revival.
        duplicate = adapter.reroute_unclaimed(CONTROLLER, old.dispatch_id, "WEB", "again")
        self.assertEqual(Decision("REJECTED", "DUPLICATE_TERMINAL", KEY), duplicate)
        self.assertEqual(["CANCELLED"], old.terminals)

    def test_n03b_reroute_cannot_mint_a_parallel_claim_key_by_renaming(self) -> None:
        adapter = make_adapter()
        old = adapter.seed_web_dispatch(KEY, operator=OP_WEB)
        before = adapter.snapshot()
        manipulated = adapter.rename_slot_reroute(CONTROLLER, old.dispatch_id,
                                                  KEY_EVADING, "LOCAL")
        self.assertEqual(Decision("INELIGIBLE", "CLAIM_KEY_SLOT_MANIPULATION", KEY_EVADING),
                         manipulated)
        self.assertEqual(before, adapter.snapshot())


# ---------------------------------------------------------------------------
# T06-N04: composite all-or-none across claim key and resources
# ---------------------------------------------------------------------------


class CompositeAtomicityTests(unittest.TestCase):
    """N04 + positive: {claim_key, R1, R2} commits or nothing commits."""

    def test_n04_exhausted_resource_rejects_whole_admission_with_zero_mutation(self) -> None:
        adapter = make_adapter()
        # The singular-device unit is consumed under a different authorized
        # key, so the default key under test stays claim-free: the rejection
        # below is purely the composite resource member failing.
        adapter.group_grants["gpu-shared"] = ("#auth@1", True)
        holder_key = KEY_GROUPED
        other = adapter.admit(proposal(adapter, operator=OP_LOCAL, key=holder_key,
                                       group_grant_ref="#auth@1", origin="LOCAL",
                                       resources=(("singular-device", 1),)))
        self.assertEqual("ACCEPTED", other.status)
        before = adapter.snapshot()
        denied = adapter.admit(proposal(adapter, operator=OP_WEB,
                                        resources=(("gpu-batch", 2), ("singular-device", 1))))
        self.assertEqual(Decision("INELIGIBLE", "RESOURCE_EXHAUSTED_OR_UNKNOWN", KEY, 1, 1), denied)
        self.assertEqual(before, adapter.snapshot())
        self.assertEqual(1, adapter.current_generation(KEY))  # no generation advance

    def test_n04_unknown_resource_rejects_whole_admission(self) -> None:
        adapter = make_adapter()
        before = adapter.snapshot()
        denied = adapter.admit(proposal(adapter, operator=OP_WEB,
                                        resources=(("gpu-batch", 1), ("fabric-switch", 1))))
        self.assertEqual(Decision("INELIGIBLE", "RESOURCE_EXHAUSTED_OR_UNKNOWN", KEY), denied)
        self.assertEqual(before, adapter.snapshot())

    def test_n04_mid_commit_conditional_failure_leaves_zero_partial_bindings(self) -> None:
        adapter = make_adapter()
        adapter.resources.fail_commit_for = "singular-device"
        denied = adapter.admit(proposal(adapter, operator=OP_WEB,
                                        resources=(("gpu-batch", 2), ("singular-device", 1))))
        self.assertEqual(Decision("REJECTED", "CONDITIONAL_WRITE_REJECTED", KEY), denied)
        # The R1 units that committed first were rolled back: no partial chain.
        self.assertEqual({"gpu-batch": 0, "singular-device": 0}, adapter.resources.active)
        self.assertEqual(1, adapter.current_generation(KEY))
        self.assertEqual([], [e for e in adapter.events if e["type"] == "DISPATCH_CLAIMED"])

    def test_n04_positive_full_composite_set_commits_at_one_point(self) -> None:
        adapter = make_adapter()
        accepted = adapter.admit(proposal(adapter, operator=OP_LOCAL, origin="LOCAL",
                                          resources=(("gpu-batch", 2), ("singular-device", 1))))
        self.assertEqual("ACCEPTED", accepted.status)
        self.assertEqual({"gpu-batch": 2, "singular-device": 1}, adapter.resources.active)
        self.assertEqual(2, adapter.current_generation(KEY))
        claimed_events = [e for e in adapter.events if e["type"] == "DISPATCH_CLAIMED"]
        self.assertEqual(1, len(claimed_events))


# ---------------------------------------------------------------------------
# T06-N05: stale subject / forged grants / late generations
# ---------------------------------------------------------------------------


class CurrentnessAndForgeryTests(unittest.TestCase):
    """N05: stale base/HEAD, tenant, pack identity, grants, generations."""

    def test_n05_stale_base_head_is_ineligible_with_zero_mutation(self) -> None:
        adapter = make_adapter()
        before = adapter.snapshot()
        denied = adapter.admit(proposal(adapter, operator=OP_WEB, base="base-OLD"))
        self.assertEqual(Decision("INELIGIBLE", "STALE_BASE", KEY, 1, 1), denied)
        self.assertEqual(before, adapter.snapshot())

    def test_n05_tenant_mismatch_is_ineligible_with_zero_mutation(self) -> None:
        adapter = make_adapter()
        before = adapter.snapshot()
        denied = adapter.admit(proposal(adapter, operator=OP_WEB, tenant="tenant-9"))
        self.assertEqual(Decision("INELIGIBLE", "TENANT_MISMATCH", KEY, 1, 1), denied)
        self.assertEqual(before, adapter.snapshot())

    def test_n05_pack_identity_drift_is_ineligible_with_zero_mutation(self) -> None:
        adapter = make_adapter()
        before = adapter.snapshot()
        denied = adapter.admit(proposal(adapter, operator=OP_WEB, pack="pack-v0"))
        self.assertEqual(Decision("INELIGIBLE", "PACK_IDENTITY_DRIFT", KEY, 1, 1), denied)
        self.assertEqual(before, adapter.snapshot())

    def test_n05_forged_or_expired_group_grant_is_ineligible(self) -> None:
        adapter = make_adapter()
        before = adapter.snapshot()
        forged = adapter.admit(proposal(adapter, operator=OP_WEB, key=KEY_GROUPED,
                                        group_grant_ref="#forged@0"))
        self.assertEqual(Decision("INELIGIBLE", "GROUP_GRANT_MISSING", KEY_GROUPED), forged)
        adapter.group_grants["gpu-shared"] = ("#auth@1", False)
        expired = adapter.admit(proposal(adapter, operator=OP_WEB, key=KEY_GROUPED,
                                         group_grant_ref="#auth@1"))
        self.assertEqual(Decision("INELIGIBLE", "GROUP_GRANT_EXPIRED", KEY_GROUPED), expired)
        self.assertEqual(before, adapter.snapshot())

    def test_n05_late_old_generation_resolves_stale_with_zero_mutation(self) -> None:
        adapter = make_adapter()
        adapter.admit(proposal(adapter, operator=OP_LOCAL, origin="LOCAL"))
        before = adapter.snapshot()
        late = adapter.admit(proposal(adapter, operator=OP_WEB, generation=1))
        self.assertEqual(Decision("STALE", "GENERATION_MISMATCH", KEY), late)
        self.assertEqual(before, adapter.snapshot())


# ---------------------------------------------------------------------------
# T06-N06: unknown publication outcomes block replacement
# ---------------------------------------------------------------------------


class PublicationAmbiguityTests(unittest.TestCase):
    """N06: ambiguous ACK/readback blocks replacement until reconciliation."""

    def test_n06_ambiguous_publication_blocks_admission_and_reroute(self) -> None:
        adapter = make_adapter()
        old = adapter.seed_web_dispatch(KEY, operator=OP_WEB)
        adapter.reconcile_publication(KEY, outcome="unknown")
        before = adapter.snapshot()
        blocked_admit = adapter.admit(proposal(adapter, operator=OP_LOCAL, origin="LOCAL"))
        self.assertEqual(Decision("UNKNOWN", "PUBLICATION_OUTCOME_AMBIGUOUS", KEY, 1, 1),
                         blocked_admit)
        blocked_reroute = adapter.reroute_unclaimed(CONTROLLER, old.dispatch_id, "LOCAL", "r")
        self.assertEqual(Decision("BLOCKED", "PUBLICATION_OUTCOME_AMBIGUOUS", KEY), blocked_reroute)
        self.assertEqual(before, adapter.snapshot())

    def test_n06_unavailable_readback_fails_closed_until_reconciled(self) -> None:
        adapter = make_adapter()
        old = adapter.seed_web_dispatch(KEY, operator=OP_WEB)
        adapter.readback_unavailable = True
        self.assertEqual("UNKNOWN", adapter.admit(proposal(adapter, operator=OP_LOCAL)).status)
        self.assertEqual("BLOCKED", adapter.reroute_unclaimed(
            CONTROLLER, old.dispatch_id, "LOCAL", "r").status)
        # Durable reconciliation reopens the lawful path.
        adapter.readback_unavailable = False
        adapter.reconcile_publication(KEY, outcome="unclaimed")
        rerouted = adapter.reroute_unclaimed(CONTROLLER, old.dispatch_id, "LOCAL", "r")
        self.assertEqual("ACCEPTED", rerouted.status)

    def test_n06_unresolvable_admission_reference_blocks_reroute(self) -> None:
        adapter = make_adapter()
        old = adapter.seed_web_dispatch(KEY, operator=OP_WEB)
        old.admission_ref = None
        before = adapter.snapshot()
        blocked = adapter.reroute_unclaimed(CONTROLLER, old.dispatch_id, "LOCAL", "r")
        self.assertEqual(Decision("BLOCKED", "ADMISSION_REF_UNRESOLVABLE", KEY), blocked)
        self.assertEqual(before, adapter.snapshot())

    def test_n06_advisory_queue_state_never_blocks_an_unrelated_legal_gate(self) -> None:
        adapter = make_adapter()
        adapter.seed_web_dispatch(KEY, operator=OP_WEB)
        adapter.reconcile_publication(KEY, outcome="unknown")  # advisory open item on KEY
        other_key = "kaicreator-mm/ai-development-standard#1014:builder:__default__"
        unrelated = adapter.admit(proposal(adapter, operator=OP_LOCAL, key=other_key,
                                           origin="LOCAL"))
        self.assertEqual("ACCEPTED", unrelated.status)


# ---------------------------------------------------------------------------
# T06-P07: idempotent resume and evidence-gated wake/drain
# ---------------------------------------------------------------------------


class LivenessWakeDrainTests(unittest.TestCase):
    """P07: idempotent same-operator resume; evidence-gated downstream wake."""

    def test_p07_same_operator_same_dispatch_resume_is_idempotent(self) -> None:
        adapter = make_adapter()
        old = adapter.seed_web_dispatch(KEY, operator=OP_WEB)
        first = adapter.claim(old.dispatch_id, OP_WEB, "s-web", old.generation)
        self.assertEqual("ACCEPTED", first.status)
        second = adapter.claim(old.dispatch_id, OP_WEB, "s-web", old.generation)
        self.assertEqual(Decision("ACCEPTED", "IDEMPOTENT_RESUME", KEY), second)
        claims = [d for d in adapter.dispatches.values() if d.claim is not None]
        self.assertEqual(1, len(claims))
        self.assertEqual(1, len([e for e in adapter.events if e["type"] == "DISPATCH_CLAIMED"]))

    def test_p07_accepted_claim_alone_never_wakes_downstream_blocked_by(self) -> None:
        adapter = make_adapter()
        accepted = adapter.admit(proposal(adapter, operator=OP_LOCAL, origin="LOCAL"))
        self.assertEqual("ACCEPTED", accepted.status)
        with_claim = adapter.attempt_wake("dep-v411-t07", {"kind": "claim"})
        self.assertEqual(Decision("BLOCKED", "CLAIM_IS_NOT_REVIEW_EVIDENCE", "dep-v411-t07"),
                         with_claim)
        without_evidence = adapter.attempt_wake("dep-v411-t07", None)
        self.assertEqual(Decision("BLOCKED", "NO_CURRENT_ACCEPTED_REVIEW_EVIDENCE", "dep-v411-t07"),
                         without_evidence)

    def test_p07_accepted_current_review_evidence_lets_the_legal_terminal_wake_drain(self) -> None:
        adapter = make_adapter()
        old = adapter.seed_web_dispatch(KEY, operator=OP_WEB)
        rerouted = adapter.reroute_unclaimed(CONTROLLER, old.dispatch_id, "LOCAL", "r")
        adapter.claim(rerouted.detail, OP_LOCAL, "s-local-fresh", 2)
        # The reroute cancellation is the legal fresh terminal; only accepted
        # current Review/Validator evidence on the successor subject wakes the
        # downstream real blocked_by dependency.
        woken = adapter.attempt_wake("dep-v411-t07", {
            "kind": "review", "subject": rerouted.detail, "status": "PASS",
        })
        self.assertEqual(Decision("ACCEPTED", "WOKEN", "dep-v411-t07"), woken)


if __name__ == "__main__":
    import sys

    result = unittest.TextTestRunner(verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
    )
    raise SystemExit(0 if result.wasSuccessful() else 1)
