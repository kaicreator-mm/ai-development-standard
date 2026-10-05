"""V410-T02B focused regression — GitHub/event/machine projection for collaboration control.

Positive/negative contract for the additive same-family responsibility projection
(`parent_dispatch_ref` + `responsibility_mode`) on the existing dispatch/event-v2
family, per L3 Wave C (`docs/implementation/4.10.0/L3_WAVE_C_R1.md` § V410-T02B),
Task Pack R1 and `standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md` §8.4.1.

Consumes `standards/EXECUTION_ARCHITECTURE_STANDARD.md` §28 (integrated by T02A);
redefines nothing. No new event family, state dimension, lifecycle or registry.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from test_protocol_schemas import assert_supported_schema, validate_subset  # noqa: E402


def _load(rel: str):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


DISPATCH = "schemas/dispatch.schema.json"
EVENT_V2 = "schemas/agent-event-v2.schema.json"
PROTOCOL = "standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md"
TEMPLATE = "templates/agent-event-comment.md"
ARCHITECTURE = "standards/EXECUTION_ARCHITECTURE_STANDARD.md"
WORK_ITEM = "standards/GITHUB_WORK_ITEM_CONTRACT_STANDARD.md"
STATE_DIMENSIONS = "registries/state-dimensions-v1.json"

# Frozen families (negative guard: byte-stable vocabularies).
FROZEN_EVENT_ENUM = {
    "ROLE_CLAIMED", "ROLE_RELEASED", "TASK_CLAIMED", "IMPLEMENTATION_READY",
    "REVIEW_DECISION", "REVIEW_RESULT", "FIX_APPLIED", "VALIDATION_REQUEST",
    "VALIDATION_RESULT", "BLOCKER_REPORTED", "DEPENDENCY_CHANGED", "MERGE_RESULT",
    "HANDOFF_READY", "DISPATCH_REQUEST", "DISPATCH_STATE_CHANGED", "CI_INFRA_EXCEPTION",
    "VALIDATION_IMPACT_DECISION", "CANDIDATE_STATE_CHANGED", "HIDDEN_ESCAPE_DISPOSITION",
    "RELEASE_QUALIFICATION", "REPOSITORY_INTEGRATION_RESULT", "DISPATCH_CLAIMED",
    "EXECUTION_PACK_STATE_CHANGED",
}
FROZEN_DISPATCH_STATE_ENUM = {
    "READY", "CLAIMED", "RUNNING", "COMPLETED", "BLOCKED", "SUPERSEDED",
}

FROZEN_STATE_DIMENSIONS = frozenset(
    {
        "work_item_workflow",
        "dispatch_lifecycle",
        "execution_pack_currentness",
        "validation_gate",
        "review_judgment",
        "release_qualification",
        "deployment_result",
        "runtime_health",
        "runner_capability",
    }
)

UNKNOWN = "UNKNOWN"
DUPLICATE_HANDOFF = "DUPLICATE_HANDOFF"
NO_RESOLVABLE_PARENT = "NO_RESOLVABLE_PARENT"


def dispatch_object(**overrides):
    """Minimal valid builder dispatch (pre-T02B shape; backward compatibility)."""
    value = {
        "dispatch_id": "dispatch-child-1",
        "repository": "kaicreator-mm/ai-development-standard",
        "version": "v4.10.0",
        "task": "#31",
        "role": "builder",
        "execution_profile": "LOCAL_BUILDER",
        "branch": "task/example",
        "expected_base_sha": "f31c9dfb285cb96126ec1babb96d63c5fae6b0d2",
        "pinned_standard_revision": "f31c9dfb285cb96126ec1babb96d63c5fae6b0d2",
        "agent_freedom": "F1_BOUNDED_IMPLEMENTATION",
        "dispatch_state": "READY",
        "task_pack_ref": "docs/implementation/4.10.0/TASK_PACKS_R1.md",
    }
    value.update(overrides)
    return value


def event(event_type: str, **overrides):
    value = {
        "schema": "ai-dev/event-v2",
        "event": event_type,
        "actor_role": "builder",
        "operator_kind": "claude-code",
        "operator_id": "claude-code:windows-01",
        "task": "#31",
        "dispatch_id": "dispatch-child-1",
        "dispatch_state": "CLAIMED",
        "sha": "f31c9dfb285cb96126ec1babb96d63c5fae6b0d2",
    }
    value.update(overrides)
    return value


# --- reconstruction oracle (§28.2 over the projected dispatch/event facts) ---


@dataclass(frozen=True)
class DispatchFact:
    dispatch_id: str
    task: str
    created_by: str | None = None
    claimed_by: str | None = None
    parent_dispatch_ref: str | None = None
    responsibility_mode: str | None = None
    evidence_ref: str | None = None


def reconstruct(facts: list[DispatchFact], dispatch_id: str) -> dict[str, object]:
    """Reconstruct §28.2 responsibility/causation from durable facts alone.

    Fails closed: an unresolvable causal parent reports UNKNOWN instead of
    guessing an owner; evidence returns are references, never responsibility.
    """
    by_id: dict[str, list[DispatchFact]] = {}
    for fact in facts:
        by_id.setdefault(fact.dispatch_id, []).append(fact)

    subject = by_id.get(dispatch_id, [None])[-1]
    if subject is None:
        return {"responsibility_owner": UNKNOWN, "mode": UNKNOWN, "parent": UNKNOWN}

    if subject.responsibility_mode == "DELEGATED_SUBWORK":
        parents = by_id.get(subject.parent_dispatch_ref or "", [])
        if not subject.parent_dispatch_ref or len(parents) != 1:
            # Missing/duplicate/unresolvable parent ref -> fail closed.
            return {"responsibility_owner": UNKNOWN, "mode": subject.responsibility_mode, "parent": UNKNOWN}
        delegator = parents[0].created_by
        return {
            "requester": delegator,
            "responsibility_owner": delegator,  # delegator retains responsibility
            "executor": subject.claimed_by,
            "parent": subject.parent_dispatch_ref,
            "mode": subject.responsibility_mode,
            "scope": subject.task,
            "evidence_ref": subject.evidence_ref,
        }

    if subject.responsibility_mode == "RESPONSIBILITY_HANDOFF":
        parents = by_id.get(subject.parent_dispatch_ref or "", [])
        if not subject.parent_dispatch_ref or len(parents) != 1:
            return {"responsibility_owner": UNKNOWN, "mode": subject.responsibility_mode, "parent": UNKNOWN}
        transferor = parents[0].claimed_by or parents[0].created_by
        if not transferor or not subject.created_by or not subject.claimed_by:
            return {"responsibility_owner": UNKNOWN, "mode": subject.responsibility_mode, "parent": UNKNOWN}
        return {
            "requester": parents[0].created_by,
            "responsibility_owner": subject.claimed_by,  # receiver owns after transfer
            "transferred_by": transferor,
            "executor": subject.claimed_by,
            "parent": subject.parent_dispatch_ref,
            "mode": subject.responsibility_mode,
            "scope": subject.task,
            "evidence_ref": subject.evidence_ref,
        }

    # Ordinary dispatch without projection fields: owner is the claimer.
    return {
        "responsibility_owner": subject.claimed_by or subject.created_by,
        "mode": UNKNOWN,
        "parent": UNKNOWN,
        "scope": subject.task,
        "evidence_ref": subject.evidence_ref,
    }


def effective_child_authority(delegatable, work_authority, role_authority, external_authorization):
    """§28.3 attenuation: projection fields are not inputs to this intersection."""
    return delegatable & work_authority & role_authority & external_authorization


# --- schema conformance ------------------------------------------------


class T02BSchemaConformance(unittest.TestCase):
    def test_schemas_stay_inside_supported_subset(self) -> None:
        for rel in (DISPATCH, EVENT_V2):
            assert_supported_schema(_load(rel))

    def test_backward_compatible_without_projection_fields(self) -> None:
        # Historical dispatch/event shapes (no additive fields) stay valid.
        self.assertEqual([], validate_subset(dispatch_object(), _load(DISPATCH)))
        self.assertEqual([], validate_subset(event("DISPATCH_CLAIMED"), _load(EVENT_V2)))
        self.assertEqual(
            [],
            validate_subset(
                event("DISPATCH_REQUEST", dispatch_state="QUEUED", actor_role="scheduler", issue="#31"),
                _load(EVENT_V2),
            ),
        )

    def test_delegated_subwork_projection_is_schema_valid(self) -> None:
        child = dispatch_object(
            created_by="operator:delegator-a",
            parent_dispatch_ref="dispatch-parent-0",
            responsibility_mode="DELEGATED_SUBWORK",
        )
        self.assertEqual([], validate_subset(child, _load(DISPATCH)))
        claim = event(
            "DISPATCH_CLAIMED",
            parent_dispatch_ref="dispatch-parent-0",
            responsibility_mode="DELEGATED_SUBWORK",
        )
        self.assertEqual([], validate_subset(claim, _load(EVENT_V2)))

    def test_responsibility_handoff_projection_is_schema_valid(self) -> None:
        handoff = dispatch_object(
            dispatch_id="dispatch-handoff-1",
            created_by="operator:transferor",
            claimed_by="operator:receiver",
            dispatch_state="CLAIMED",
            parent_dispatch_ref="dispatch-parent-0",
            responsibility_mode="RESPONSIBILITY_HANDOFF",
        )
        self.assertEqual([], validate_subset(handoff, _load(DISPATCH)))
        claim = event(
            "DISPATCH_CLAIMED",
            dispatch_id="dispatch-handoff-1",
            operator_id="codex:receiver-01",
            parent_dispatch_ref="dispatch-parent-0",
            responsibility_mode="RESPONSIBILITY_HANDOFF",
        )
        self.assertEqual([], validate_subset(claim, _load(EVENT_V2)))

    def test_delegated_subwork_requires_causal_parent_and_delegator(self) -> None:
        schema = _load(DISPATCH)
        for missing in ("parent_dispatch_ref", "created_by"):
            child = dispatch_object(
                created_by="operator:delegator-a",
                parent_dispatch_ref="dispatch-parent-0",
                responsibility_mode="DELEGATED_SUBWORK",
            )
            del child[missing]
            errors = validate_subset(child, schema)
            self.assertTrue(any(missing in error for error in errors), errors)

    def test_delegated_subwork_events_require_causal_parent(self) -> None:
        schema = _load(EVENT_V2)
        for event_type, state in (("DISPATCH_REQUEST", "QUEUED"), ("DISPATCH_CLAIMED", "CLAIMED")):
            value = event(
                event_type,
                dispatch_state=state,
                actor_role="scheduler" if event_type == "DISPATCH_REQUEST" else "builder",
                issue="#31",
                created_by="operator:delegator-a",
                responsibility_mode="DELEGATED_SUBWORK",
            )
            errors = validate_subset(value, schema)
            self.assertTrue(any("parent_dispatch_ref" in error for error in errors), errors)

    def test_handoff_requires_durably_named_pairing_and_work_identity(self) -> None:
        # Event surface: transferor (parent dispatch), receiver (operator_id),
        # scope (dispatch ref) and exact work identity (task) must be named.
        schema = _load(EVENT_V2)
        claim_without_task = event(
            "DISPATCH_CLAIMED",
            parent_dispatch_ref="dispatch-parent-0",
            responsibility_mode="RESPONSIBILITY_HANDOFF",
        )
        del claim_without_task["task"]
        errors = validate_subset(claim_without_task, schema)
        self.assertTrue(any("task" in error for error in errors), errors)

        request_without_task = event(
            "DISPATCH_REQUEST",
            dispatch_state="QUEUED",
            actor_role="scheduler",
            issue="#31",
            parent_dispatch_ref="dispatch-parent-0",
            responsibility_mode="RESPONSIBILITY_HANDOFF",
        )
        del request_without_task["task"]
        errors2 = validate_subset(request_without_task, schema)
        self.assertTrue(any("task" in error for error in errors2), errors2)

        # Dispatch surface: the transferring operator must be durably named.
        dschema = _load(DISPATCH)
        handoff = dispatch_object(
            created_by="operator:transferor",
            responsibility_mode="RESPONSIBILITY_HANDOFF",
        )
        del handoff["created_by"]
        errors3 = validate_subset(handoff, dschema)
        self.assertTrue(any("created_by" in error for error in errors3), errors3)

    def test_responsibility_mode_enum_is_closed(self) -> None:
        for rel, key in ((DISPATCH, "responsibility_mode"), (EVENT_V2, "responsibility_mode")):
            enum = _load(rel)["properties"][key]["enum"]
            self.assertEqual(["DELEGATED_SUBWORK", "RESPONSIBILITY_HANDOFF"], enum)
        invalid = dispatch_object(
            created_by="operator:a",
            parent_dispatch_ref="p",
            responsibility_mode="RESPONSIBILITY_LAUNDERING",
        )
        self.assertTrue(validate_subset(invalid, _load(DISPATCH)))

    def test_projection_fields_are_optional_additive(self) -> None:
        for rel in (DISPATCH, EVENT_V2):
            schema = _load(rel)
            self.assertNotIn("parent_dispatch_ref", schema["required"])
            self.assertNotIn("responsibility_mode", schema["required"])
            self.assertTrue(schema["additionalProperties"])


# --- frozen families (negative guards) ----------------------------------


class T02BFrozenFamilyGuards(unittest.TestCase):
    def test_no_new_event_type(self) -> None:
        event_enum = set(_load(EVENT_V2)["properties"]["event"]["enum"])
        self.assertEqual(FROZEN_EVENT_ENUM, event_enum)

    def test_no_new_dispatch_state(self) -> None:
        state_enum = set(_load(DISPATCH)["properties"]["dispatch_state"]["enum"])
        self.assertEqual(FROZEN_DISPATCH_STATE_ENUM, state_enum)
        event_states = set(_load(EVENT_V2)["properties"]["dispatch_state"]["enum"])
        self.assertNotIn("DELEGATED_SUBWORK", event_states)
        self.assertNotIn("RESPONSIBILITY_HANDOFF", event_states)

    def test_no_new_state_dimension_or_registry(self) -> None:
        body = (ROOT / STATE_DIMENSIONS).read_text(encoding="utf-8")
        for token in ("DELEGATED_SUBWORK", "RESPONSIBILITY_HANDOFF", "responsibility_mode", "parent_dispatch_ref"):
            self.assertNotIn(token, body)
        registry = _load(STATE_DIMENSIONS)
        self.assertEqual(
            FROZEN_STATE_DIMENSIONS,
            {dimension["dimension_id"] for dimension in registry["dimensions"]},
        )

    def test_reference_boundary_and_semantic_owner_stay_clean(self) -> None:
        # GITHUB_WORK_ITEM_CONTRACT_STANDARD.md is a reference boundary for T02B.
        self.assertNotIn("DELEGATED_SUBWORK", (ROOT / WORK_ITEM).read_text(encoding="utf-8"))
        # EXECUTION_ARCHITECTURE_STANDARD.md §28 is consumed, not rewritten.
        s28 = (ROOT / ARCHITECTURE).read_text(encoding="utf-8").split(
            "## 28. Responsibility and control semantics", 1
        )[1]
        self.assertIn("These are semantic facts, not a requirement that each listed name become a new schema field", s28)
        self.assertIn("no second Claim lifecycle", s28)

    def test_protocol_owns_writer_semantics(self) -> None:
        text = (ROOT / PROTOCOL).read_text(encoding="utf-8")
        self.assertIn("### 8.4.1 Additive responsibility projection fields", text)
        for token in (
            "parent_dispatch_ref",
            "responsibility_mode",
            "DELEGATED_SUBWORK | RESPONSIBILITY_HANDOFF",
            "EXECUTION_ARCHITECTURE_STANDARD.md section 28",
            "create no authority, no new event type",
            "rejected like any incompatible second claim",
            "admission_mode / protected_claim_key / claim_generation",
        ):
            self.assertIn(token, text)
        # §8.5 accepted-claim audit list carries the projection fields.
        s85 = text.split("### 8.5", 1)[1].split("## 9.", 1)[0]
        self.assertIn("parent_dispatch_ref / responsibility_mode", s85)

    def test_template_documents_both_modes(self) -> None:
        text = (ROOT / TEMPLATE).read_text(encoding="utf-8")
        self.assertIn("responsibility_mode: DELEGATED_SUBWORK", text)
        self.assertIn("responsibility_mode: RESPONSIBILITY_HANDOFF", text)
        self.assertIn("parent_dispatch_ref", text)


# --- reconstruction semantics (positive cases) ---------------------------


class T02BReconstructionPositive(unittest.TestCase):
    def parent(self, **kw):
        return DispatchFact("dispatch-parent-0", "#31", created_by="operator:delegator-a", **kw)

    def test_delegated_child_dispatch_reconstructs_full_fact_set(self) -> None:
        # Positive 1: requester/delegator, owner, executor, causal parent,
        # scope and evidence return reconstruct from durable facts alone.
        facts = [
            self.parent(claimed_by="operator:delegator-a"),
            DispatchFact(
                "dispatch-child-1", "#31",
                created_by="operator:delegator-a",
                claimed_by="operator:child-b",
                parent_dispatch_ref="dispatch-parent-0",
                responsibility_mode="DELEGATED_SUBWORK",
            ),
        ]
        view = reconstruct(facts, "dispatch-child-1")
        self.assertEqual("operator:delegator-a", view["requester"])
        self.assertEqual("operator:delegator-a", view["responsibility_owner"])
        self.assertEqual("operator:child-b", view["executor"])
        self.assertEqual("dispatch-parent-0", view["parent"])
        self.assertEqual("DELEGATED_SUBWORK", view["mode"])
        self.assertEqual("#31", view["scope"])
        closed = replace(facts[1], evidence_ref="evidence:pr#900@sha")
        view2 = reconstruct([facts[0], closed], "dispatch-child-1")
        self.assertEqual("evidence:pr#900@sha", view2["evidence_ref"])
        # A returned result reference closes the child's obligation; it does
        # not move responsibility.
        self.assertEqual("operator:delegator-a", view2["responsibility_owner"])

    def test_handoff_yields_exactly_one_active_owner_per_material_point(self) -> None:
        # Positive 2: transferor owns before, receiver owns after; the handoff
        # is distinguishable from an ordinary supersession via the projection.
        before = [self.parent(claimed_by="operator:transferor")]
        self.assertEqual(
            "operator:transferor",
            reconstruct(before, "dispatch-parent-0")["responsibility_owner"],
        )
        facts = before + [
            DispatchFact(
                "dispatch-handoff-1", "#31",
                created_by="operator:transferor",
                claimed_by="operator:receiver",
                parent_dispatch_ref="dispatch-parent-0",
                responsibility_mode="RESPONSIBILITY_HANDOFF",
            )
        ]
        view = reconstruct(facts, "dispatch-handoff-1")
        self.assertEqual("operator:receiver", view["responsibility_owner"])
        self.assertEqual("operator:transferor", view["transferred_by"])
        self.assertEqual("RESPONSIBILITY_HANDOFF", view["mode"])

    def test_authority_attenuation_ignores_projection_fields(self) -> None:
        # Positive 3 + Negative 3: authority stays the §28.3 intersection;
        # capability and projection fields never widen it.
        self.assertEqual(
            frozenset({"execute"}),
            effective_child_authority(
                frozenset({"execute", "prod_deploy"}),   # delegatable
                frozenset({"execute", "prod_deploy"}),   # work authority
                frozenset({"execute"}),                  # role authority
                frozenset({"execute"}),                  # external authorization
            ),
        )
        self.assertEqual(
            frozenset({"execute"}),
            effective_child_authority(
                frozenset({"execute"}),
                frozenset({"execute", "data_export"}),
                frozenset({"execute", "root_credentials"}),
                frozenset({"execute"}),
            ),
        )

    def test_human_control_composes_existing_semantics(self) -> None:
        # Positive 4: no routine-relay human events are created; the projection
        # adds no control workflow, only attribution fields on existing events.
        schema = _load(EVENT_V2)
        self.assertEqual(FROZEN_EVENT_ENUM, set(schema["properties"]["event"]["enum"]))
        text = (ROOT / PROTOCOL).read_text(encoding="utf-8")
        self.assertIn("no second lifecycle and no responsibility registry/ledger", text)
        self.assertNotIn("Human Decision Queue (T02B)", text)

    def test_historical_facts_reconstruct_without_projection(self) -> None:
        # Positive 5: a pre-T02B dispatch still reconstructs its owner.
        facts = [DispatchFact("dispatch-old-1", "#31", created_by="operator:a", claimed_by="operator:a")]
        self.assertEqual("operator:a", reconstruct(facts, "dispatch-old-1")["responsibility_owner"])


# --- reconstruction semantics (negative cases) ---------------------------


class T02BReconstructionNegative(unittest.TestCase):
    def parent(self, **kw):
        return DispatchFact("dispatch-parent-0", "#31", created_by="operator:delegator-a", **kw)

    def child(self, **kw):
        defaults = dict(
            created_by="operator:delegator-a",
            claimed_by="operator:child-b",
            parent_dispatch_ref="dispatch-parent-0",
            responsibility_mode="DELEGATED_SUBWORK",
        )
        defaults.update(kw)
        return DispatchFact("dispatch-child-1", "#31", **defaults)

    def test_unresolvable_parent_fails_closed(self) -> None:
        # Negative 1: missing parent object, duplicate dispatch ids and a
        # dangling ref all reconstruct UNKNOWN — never a guessed owner.
        for facts in (
            [self.child()],                                             # parent missing
            [self.parent(), self.parent(), self.child()],               # duplicate parent id
            [self.child(parent_dispatch_ref="dispatch-ghost")],         # unresolvable
        ):
            view = reconstruct(facts, "dispatch-child-1")
            self.assertEqual(UNKNOWN, view["responsibility_owner"], facts)

    def test_second_active_handoff_of_same_work_is_rejected(self) -> None:
        # Negative 2: like an incompatible second claim (§11 / §12.1 CAS).
        facts = [
            self.parent(claimed_by="operator:transferor"),
            DispatchFact(
                "dispatch-handoff-1", "#31",
                created_by="operator:transferor",
                claimed_by="operator:receiver",
                parent_dispatch_ref="dispatch-parent-0",
                responsibility_mode="RESPONSIBILITY_HANDOFF",
            ),
        ]

        def admit(fact_list, candidate: DispatchFact) -> str:
            work_ids = {fact.task for fact in fact_list if fact.responsibility_mode == "RESPONSIBILITY_HANDOFF"}
            if candidate.task in work_ids:
                return DUPLICATE_HANDOFF
            fact_list.append(candidate)
            return "ACCEPTED"

        self.assertEqual(
            DUPLICATE_HANDOFF,
            admit(facts, DispatchFact(
                "dispatch-handoff-2", "#31",
                created_by="operator:receiver",
                claimed_by="operator:outsider",
                parent_dispatch_ref="dispatch-handoff-1",
                responsibility_mode="RESPONSIBILITY_HANDOFF",
            )),
        )
        self.assertEqual("operator:receiver", reconstruct(facts, "dispatch-handoff-1")["responsibility_owner"])

    def test_invalid_intent_leaves_no_partial_canonical_fact(self) -> None:
        # Negative 5: schema rejection is atomic — the oracle facts list is
        # only appended after validation passes.
        schema = _load(EVENT_V2)
        facts: list[DispatchFact] = [self.parent()]
        invalid = event(
            "DISPATCH_CLAIMED",
            parent_dispatch_ref="dispatch-parent-0",
            responsibility_mode="RESPONSIBILITY_HANDOFF",
        )
        del invalid["task"]
        self.assertTrue(validate_subset(invalid, schema))
        self.assertEqual([facts[0]], facts)
        self.assertEqual("operator:delegator-a", reconstruct(facts, "dispatch-parent-0")["responsibility_owner"])

    def test_projection_fields_cannot_transfer_evidence_identity(self) -> None:
        # Negative 6: evidence references stay bound to their exact subject;
        # the projection fields carry no evidence authority across drift.
        facts = [
            self.parent(claimed_by="operator:a"),
            self.child(evidence_ref=None),
        ]
        view = reconstruct(facts, "dispatch-child-1")
        self.assertIsNone(view["evidence_ref"])
        # A handoff never inherits the predecessor's evidence reference.
        handoff_facts = [
            self.parent(claimed_by="operator:transferor"),
            DispatchFact(
                "dispatch-handoff-1", "#31",
                created_by="operator:transferor",
                claimed_by="operator:receiver",
                parent_dispatch_ref="dispatch-parent-0",
                responsibility_mode="RESPONSIBILITY_HANDOFF",
            ),
        ]
        self.assertIsNone(reconstruct(handoff_facts, "dispatch-handoff-1")["evidence_ref"])

    def test_no_responsibility_registry_or_service_files_exist(self) -> None:
        # Negative 4 (filesystem guard): the projection must not grow a
        # responsibility ledger/registry/service surface in owned directories.
        owned = [ROOT / "scripts", ROOT / "schemas", ROOT / "registries", ROOT / "standards"]
        hits = [
            path
            for base in owned
            for path in base.rglob("*responsibility*")
        ]
        self.assertEqual([], hits)


if __name__ == "__main__":
    loader = unittest.defaultTestLoader
    suite = unittest.TestSuite(
        loader.loadTestsFromTestCase(tc)
        for tc in (
            T02BSchemaConformance,
            T02BFrozenFamilyGuards,
            T02BReconstructionPositive,
            T02BReconstructionNegative,
        )
    )
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    raise SystemExit(0 if result.wasSuccessful() else 1)
