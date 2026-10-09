"""V410-T02A focused regression — Human + Multi-Agent responsibility/control semantics.

Positive and negative contract for `DELEGATED_SUBWORK` vs `RESPONSIBILITY_HANDOFF`,
authority attenuation, reconstructible responsibility/causation and Human control
points, per frozen L2 §6 (`docs/implementation/4.10.0/L2_ARCHITECTURE_EVIDENCE.md`),
the Wave A L3 pack and `standards/EXECUTION_ARCHITECTURE_STANDARD.md` §28.

The oracle composes the section 11 claim model as attribution only; it MUST NOT
model a second claim/dispatch lifecycle. Machine/event/schema projection belongs
to the successor concern and is asserted absent here.
"""
from __future__ import annotations

from dataclasses import dataclass, field, replace
import glob
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
STANDARD = "standards/EXECUTION_ARCHITECTURE_STANDARD.md"
# V410-T02B (successor concern) owns the machine/event/schema projection of the
# settled §28 semantics; these T02B-owned surfaces carry the mode tokens since
# its integration. The reference boundary and all other schemas stay clean.
T02B_PROJECTION_SURFACES = (
    "standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md",
    "schemas/dispatch.schema.json",
    "schemas/agent-event-v2.schema.json",
    "templates/agent-event-comment.md",
)
NON_PROJECTION_SURFACES = (
    "standards/GITHUB_WORK_ITEM_CONTRACT_STANDARD.md",
    "standards/LOCAL_AGENT_HANDOFF_PROTOCOL.md",
    "schemas/execution-state.schema.json",
    "schemas/local-agent-handoff.schema.json",
    "registries/state-dimensions-v1.json",
)


# --- reference oracle -------------------------------------------------


@dataclass(frozen=True)
class Operator:
    operator_id: str
    role_authority: frozenset[str] = frozenset()
    delegatable: frozenset[str] = frozenset()
    capabilities: frozenset[str] = frozenset()  # execution means, never authority


@dataclass(frozen=True)
class WorkAuthority:
    work_id: str
    work_authority: frozenset[str] = frozenset()
    external_authorization: frozenset[str] = frozenset()


def effective_child_authority(
    delegator: Operator, work: WorkAuthority, child: Operator
) -> frozenset[str]:
    """§28.3 authority attenuation: capability never widens the intersection."""
    return (
        delegator.delegatable
        & work.work_authority
        & child.role_authority
        & work.external_authorization
    )


DELEGATED_SUBWORK = "DELEGATED_SUBWORK"
RESPONSIBILITY_HANDOFF = "RESPONSIBILITY_HANDOFF"

ACCEPTED = "ACCEPTED"
NOT_RESPONSIBILITY_OWNER = "NOT_RESPONSIBILITY_OWNER"
BEYOND_DELEGATABLE_AUTHORITY = "BEYOND_DELEGATABLE_AUTHORITY"
BEYOND_EFFECTIVE_AUTHORITY = "BEYOND_EFFECTIVE_AUTHORITY"
DUPLICATE_HANDOFF = "DUPLICATE_HANDOFF"


@dataclass(frozen=True)
class ResponsibilityFact:
    mode: str
    delegator: str
    child: str
    work_id: str
    scope: frozenset[str]
    evidence_ref: str | None = None  # result/evidence return reference


@dataclass
class ResponsibilityLedger:
    """Append-oriented attribution oracle over existing claim/dispatch facts.

    Exactly one active responsibility owner per work identity; delegation
    keeps the delegator as owner, handoff transfers it explicitly. No second
    lifecycle, no new state dimension.
    """

    facts: list[ResponsibilityFact] = field(default_factory=list)
    requester: dict[str, str] = field(default_factory=dict)
    owner: dict[str, str] = field(default_factory=dict)
    executors: dict[str, set[str]] = field(default_factory=dict)
    handed_off: set[str] = field(default_factory=set)

    def delegate_subwork(
        self,
        delegator: Operator,
        work: WorkAuthority,
        child: Operator,
        scope: frozenset[str],
    ) -> str:
        if self.handed_off_work(work.work_id):
            return NOT_RESPONSIBILITY_OWNER
        if self.owner.get(work.work_id, delegator.operator_id) != delegator.operator_id:
            return NOT_RESPONSIBILITY_OWNER
        if not scope <= effective_child_authority(delegator, work, child):
            return BEYOND_EFFECTIVE_AUTHORITY
        self.requester.setdefault(work.work_id, delegator.operator_id)
        self.owner.setdefault(work.work_id, delegator.operator_id)
        self.executors.setdefault(work.work_id, set()).add(child.operator_id)
        self.facts.append(
            ResponsibilityFact(DELEGATED_SUBWORK, delegator.operator_id, child.operator_id, work.work_id, scope)
        )
        return ACCEPTED

    def handoff(
        self,
        transferring: Operator,
        work: WorkAuthority,
        receiving: Operator,
        scope: frozenset[str],
    ) -> str:
        if work.work_id in self.handed_off:
            return DUPLICATE_HANDOFF
        if self.owner.get(work.work_id, transferring.operator_id) != transferring.operator_id:
            return NOT_RESPONSIBILITY_OWNER
        if not scope <= transferring.delegatable:
            return BEYOND_DELEGATABLE_AUTHORITY
        if not scope <= effective_child_authority(transferring, work, receiving):
            return BEYOND_EFFECTIVE_AUTHORITY
        self.requester.setdefault(work.work_id, transferring.operator_id)
        self.owner[work.work_id] = receiving.operator_id
        self.executors.setdefault(work.work_id, set()).add(receiving.operator_id)
        self.handed_off.add(work.work_id)
        self.facts.append(
            ResponsibilityFact(RESPONSIBILITY_HANDOFF, transferring.operator_id, receiving.operator_id, work.work_id, scope)
        )
        return ACCEPTED

    def return_result(self, work_id: str, child: str, evidence_ref: str) -> str:
        if child not in self.executors.get(work_id, set()):
            return NOT_RESPONSIBILITY_OWNER
        self.facts.append(
            replace(self._last_relation(work_id, child), evidence_ref=evidence_ref)
        )
        return ACCEPTED

    def _last_relation(self, work_id: str, child: str) -> ResponsibilityFact:
        return next(
            fact
            for fact in reversed(self.facts)
            if fact.work_id == work_id and fact.child == child and fact.evidence_ref is None
        )

    def handed_off_work(self, work_id: str) -> bool:
        return work_id in self.handed_off

    def reconstruct(self, work_id: str) -> dict[str, object]:
        """Reconstruct responsibility/causation from durable facts alone."""
        chain = [fact for fact in self.facts if fact.work_id == work_id]
        return {
            "requester": self.requester.get(work_id),
            "responsibility_owner": self.owner.get(work_id),
            "executors": sorted(self.executors.get(work_id, set())),
            "parent_chain": [
                (fact.mode, fact.delegator, fact.child)
                for fact in chain
                if fact.evidence_ref is None
            ],
            "evidence_refs": [fact.evidence_ref for fact in chain if fact.evidence_ref],
        }


ROUTINE_AUTOMATED = frozenset(
    {"poll_ci", "relay_prompt", "compute_ready_set", "copy_results", "deterministic_relay"}
)
AUTHORITY_SENSITIVE = frozenset(
    {
        "product_semantics_change",
        "architecture_contradiction",
        "security_authorization",
        "public_contract_change",
        "gate_authority_change",
        "limitation_acceptance",
        "destructive_action",
        "delegate_authority",
        "redirect_in_flight_execution",
        "pause_stop_cancel_automated_transitions",
    }
)


def routes_to_human_decision(action: str) -> bool:
    """§28.4: humans are not routine relays; authority-sensitive work routes to them."""
    if action in ROUTINE_AUTOMATED:
        return False
    return action in AUTHORITY_SENSITIVE


# --- contract ---------------------------------------------------------


class V410T02ASectionSemantics(unittest.TestCase):
    def text(self, rel: str) -> str:
        return (ROOT / rel).read_text(encoding="utf-8")

    def section_28(self) -> str:
        text = self.text(STANDARD)
        return text.split("## 28. Responsibility and control semantics", 1)[1]

    def test_two_responsibility_modes_are_settled(self) -> None:
        s28 = self.section_28()
        for token in (
            "DELEGATED_SUBWORK",
            "RESPONSIBILITY_HANDOFF",
            "delegator retains active responsibility",
            "child performs bounded work and returns result/evidence",
            "active responsibility/control transfers explicitly",
            "within bounded delegatable authority",
        ):
            self.assertIn(token, s28)

    def test_delegation_and_handoff_are_distinct_and_non_duplicative(self) -> None:
        s28 = self.section_28()
        self.assertIn("exactly one operator owns active responsibility at any material point", s28)
        self.assertIn("never transfers responsibility by itself", s28)
        self.assertIn("A returned result/evidence reference closes the child's obligation; it does not move responsibility", s28)
        self.assertIn("a second `RESPONSIBILITY_HANDOFF` of the same work while one is active is a duplicate", s28)

    def test_authority_attenuation_is_explicit(self) -> None:
        s28 = self.section_28()
        for token in (
            "EFFECTIVE_CHILD_AUTHORITY",
            "legally delegatable authority of the transferring/delegating operator",
            "current Task/Work authority (frozen scope, allowed write set, acceptance)",
            "role authority",
            "project/external authorization",
            "Capability, credentials, tool access, environment access, model capability or dispatch delivery NEVER create or expand authority",
            "Delegation chains cannot launder authority",
        ):
            self.assertIn(token, s28)

    def test_reconstructible_responsibility_facts(self) -> None:
        s28 = self.section_28()
        for token in (
            "requester/delegator",
            "responsibility owner at each material point",
            "executor/operator",
            "parent/causal work or dispatch reference",
            "subject/authority scope",
            "result/evidence return reference",
            "handoff/delegation mode",
            "fails closed to the owning authority instead of being guessed",
        ):
            self.assertIn(token, s28)

    def test_human_control_points_compose_existing_mechanisms(self) -> None:
        s28 = self.section_28()
        for token in (
            "Human Decision Queue (section 19)",
            "pause/stop/cancel/redirect",
            "routine deterministic relay/polling work runs without human intervention by default",
            "Human controllability is a hard product behavior. Human line-by-line code reading is not.",
        ):
            self.assertIn(token, s28)
        # The canonical §19 owner text remains intact.
        text = self.text(STANDARD)
        self.assertIn("Do not wake a human merely to copy prompts, poll CI, calculate ready tasks", text)

    def test_no_second_lifecycle_is_declared(self) -> None:
        s28 = self.section_28()
        for token in (
            "no second Claim lifecycle",
            "no second Human approval workflow",
            "not a parallel lifecycle",
            "MUST consume the semantics settled here rather than redefine them",
        ):
            self.assertIn(token, s28)

    def test_no_new_state_dimensions_are_introduced(self) -> None:
        text = self.text(STANDARD)

        def enum_tokens(start: str, end: str) -> set[str]:
            block = text.split(start, 1)[1].split(end, 1)[0]
            return {
                line.strip()
                for line in block.splitlines()
                if line.strip() and not line.strip().startswith("`") and line.strip() != "text"
            }

        self.assertEqual(
            {"planned", "ready", "claimed", "implementing", "review-ready", "reviewing",
             "changes-requested", "validation-needed", "merge-ready", "blocked", "done"},
            enum_tokens("### Workflow routing state", "### Gate state"),
        )
        self.assertEqual(
            {"QUEUED", "DELIVERED", "ACKNOWLEDGED", "RUNNING", "DONE", "FAILED",
             "CANCELLED", "TIMEOUT", "STALE"},
            enum_tokens("### Dispatch state", "Pull workers MAY use"),
        )

    def test_semantics_project_only_through_t02b_owned_surfaces(self) -> None:
        # V410-T02B (successor concern) owns machine/event/schema projection:
        # the settled semantic modes appear on the T02B-owned projection
        # surfaces and nowhere else (reference boundary, other schemas).
        for rel in T02B_PROJECTION_SURFACES:
            self.assertIn("DELEGATED_SUBWORK", self.text(rel))
            self.assertIn("RESPONSIBILITY_HANDOFF", self.text(rel))
        for rel in NON_PROJECTION_SURFACES:
            self.assertNotIn("DELEGATED_SUBWORK", self.text(rel))
            self.assertNotIn("RESPONSIBILITY_HANDOFF", self.text(rel))
        for rel in glob.glob(str(ROOT / "schemas" / "*.json")):
            rel_posix = str(Path(rel).relative_to(ROOT)).replace("\\", "/")
            if rel_posix in T02B_PROJECTION_SURFACES:
                continue
            body = Path(rel).read_text(encoding="utf-8")
            self.assertNotIn("DELEGATED_SUBWORK", body)
            self.assertNotIn("RESPONSIBILITY_HANDOFF", body)

    def test_canonical_claim_ownership_is_preserved(self) -> None:
        text = self.text(STANDARD)
        for token in (
            "At most one incompatible active dispatch MUST exist per `(work item, role)`",
            "Claim admission is a compare-and-set style transition",
            "SINGLE_WRITER_ADMISSION",
            "READY, Dispatch, and Claim remain canonical",
        ):
            self.assertIn(token, text)


class V410T02AResponsibilityOracle(unittest.TestCase):
    def operators(self) -> tuple[Operator, Operator, Operator]:
        delegator = Operator(
            "delegator-a",
            role_authority=frozenset({"execute", "review_assignment"}),
            delegatable=frozenset({"execute"}),
        )
        child = Operator(
            "child-b",
            role_authority=frozenset({"execute"}),
            capabilities=frozenset({"root_credentials", "prod_deploy_tool"}),
        )
        outsider = Operator("outsider-c", role_authority=frozenset({"observe"}))
        return delegator, child, outsider

    def work(self, work_id: str = "T-1") -> WorkAuthority:
        return WorkAuthority(
            work_id,
            work_authority=frozenset({"execute", "review_assignment"}),
            external_authorization=frozenset({"execute"}),
        )

    def test_delegated_subwork_keeps_delegator_responsible(self) -> None:
        delegator, child, _ = self.operators()
        ledger = ResponsibilityLedger()
        self.assertEqual(ACCEPTED, ledger.delegate_subwork(delegator, self.work(), child, frozenset({"execute"})))
        self.assertEqual(ACCEPTED, ledger.return_result("T-1", "child-b", "evidence:pr#900@sha"))
        view = ledger.reconstruct("T-1")
        # Delegator retains responsibility after the child's bounded result.
        self.assertEqual("delegator-a", view["responsibility_owner"])
        self.assertEqual("delegator-a", view["requester"])
        self.assertEqual(["child-b"], view["executors"])
        self.assertEqual([(DELEGATED_SUBWORK, "delegator-a", "child-b")], view["parent_chain"])
        self.assertEqual(["evidence:pr#900@sha"], view["evidence_refs"])

    def test_responsibility_handoff_transfers_explicitly_within_delegatable(self) -> None:
        delegator, child, _ = self.operators()
        ledger = ResponsibilityLedger()
        self.assertEqual(ACCEPTED, ledger.handoff(delegator, self.work(), child, frozenset({"execute"})))
        view = ledger.reconstruct("T-1")
        # Active responsibility moved to the child, explicitly and durably.
        self.assertEqual("child-b", view["responsibility_owner"])
        self.assertEqual("delegator-a", view["requester"])
        self.assertEqual([(RESPONSIBILITY_HANDOFF, "delegator-a", "child-b")], view["parent_chain"])

    def test_handoff_beyond_delegatable_authority_fails_closed(self) -> None:
        delegator, child, _ = self.operators()
        overreaching = replace(delegator, delegatable=frozenset())
        ledger = ResponsibilityLedger()
        self.assertEqual(
            BEYOND_DELEGATABLE_AUTHORITY,
            ledger.handoff(overreaching, self.work(), child, frozenset({"execute"})),
        )
        view = ledger.reconstruct("T-1")
        # Rejection publishes no canonical fact: responsibility did not move
        # and reconstruction does not guess an owner.
        self.assertIsNone(view["responsibility_owner"])
        self.assertEqual([], view["parent_chain"])

    def test_capability_never_expands_authority(self) -> None:
        delegator, child, _ = self.operators()
        # Child holds root credentials and a prod deploy tool, but the
        # role/project intersection does not include prod deployment.
        prod_work = WorkAuthority(
            "PROD-1",
            work_authority=frozenset({"execute", "prod_deploy"}),
            external_authorization=frozenset({"execute"}),
        )
        self.assertEqual(
            frozenset({"execute"}),
            effective_child_authority(delegator, prod_work, child),
        )
        # Even a delegator legally allowed to delegate prod deployment cannot
        # push that scope through: capability possession is not authorization.
        capable_delegator = replace(delegator, delegatable=frozenset({"execute", "prod_deploy"}))
        ledger = ResponsibilityLedger()
        self.assertEqual(
            BEYOND_EFFECTIVE_AUTHORITY,
            ledger.delegate_subwork(capable_delegator, prod_work, child, frozenset({"prod_deploy"})),
        )
        self.assertEqual(
            BEYOND_EFFECTIVE_AUTHORITY,
            ledger.handoff(capable_delegator, prod_work, child, frozenset({"prod_deploy"})),
        )
        self.assertIsNone(ledger.reconstruct("PROD-1")["responsibility_owner"])

    def test_external_authorization_bounds_the_intersection(self) -> None:
        delegator, child, _ = self.operators()
        # Task and role allow export, but external/project authorization does not.
        restricted = WorkAuthority(
            "T-EXP",
            work_authority=frozenset({"execute", "data_export"}),
            external_authorization=frozenset({"execute"}),
        )
        self.assertEqual(
            frozenset({"execute"}),
            effective_child_authority(delegator, restricted, child),
        )

    def test_second_active_handoff_of_same_work_is_rejected(self) -> None:
        delegator, child, outsider = self.operators()
        ledger = ResponsibilityLedger()
        self.assertEqual(ACCEPTED, ledger.handoff(delegator, self.work(), child, frozenset({"execute"})))
        # The original delegator is no longer the responsibility owner...
        self.assertEqual(
            NOT_RESPONSIBILITY_OWNER,
            ledger.delegate_subwork(delegator, self.work(), outsider, frozenset({"execute"})),
        )
        # ...and no competing handoff of the same work may linearize after it.
        self.assertEqual(
            DUPLICATE_HANDOFF,
            ledger.handoff(delegator, self.work(), outsider, frozenset({"execute"})),
        )
        self.assertEqual("child-b", ledger.reconstruct("T-1")["responsibility_owner"])

    def test_parallel_delegated_subwork_keeps_single_owner(self) -> None:
        delegator, child, outsider = self.operators()
        outsider_worker = replace(outsider, role_authority=frozenset({"execute"}))
        ledger = ResponsibilityLedger()
        self.assertEqual(ACCEPTED, ledger.delegate_subwork(delegator, self.work(), child, frozenset({"execute"})))
        self.assertEqual(ACCEPTED, ledger.delegate_subwork(delegator, self.work(), outsider_worker, frozenset({"execute"})))
        view = ledger.reconstruct("T-1")
        self.assertEqual("delegator-a", view["responsibility_owner"])
        self.assertEqual(["child-b", "outsider-c"], view["executors"])
        self.assertEqual(
            [(DELEGATED_SUBWORK, "delegator-a", "child-b"), (DELEGATED_SUBWORK, "delegator-a", "outsider-c")],
            view["parent_chain"],
        )

    def test_reconstruction_fails_closed_when_owner_gap_is_unknown(self) -> None:
        # No facts recorded: reconstruction must not guess an owner.
        self.assertIsNone(ResponsibilityLedger().reconstruct("UNKNOWN-1")["responsibility_owner"])


class V410T02AHumanControlRouting(unittest.TestCase):
    def test_routine_deterministic_relay_needs_no_human(self) -> None:
        for action in ("poll_ci", "relay_prompt", "compute_ready_set", "copy_results", "deterministic_relay"):
            self.assertFalse(routes_to_human_decision(action), action)

    def test_authority_sensitive_actions_route_to_human(self) -> None:
        for action in (
            "product_semantics_change",
            "security_authorization",
            "gate_authority_change",
            "destructive_action",
            "delegate_authority",
            "pause_stop_cancel_automated_transitions",
        ):
            self.assertTrue(routes_to_human_decision(action), action)


if __name__ == "__main__":
    loader = unittest.defaultTestLoader
    suite = unittest.TestSuite(
        loader.loadTestsFromTestCase(tc)
        for tc in (V410T02ASectionSemantics, V410T02AResponsibilityOracle, V410T02AHumanControlRouting)
    )
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    raise SystemExit(0 if result.wasSuccessful() else 1)
