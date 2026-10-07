from __future__ import annotations

from dataclasses import dataclass, field, replace
import json
from pathlib import Path
import sys
import unittest

from v34_rules import (
    authorize_non_default,
    derive_claim_key,
    project_dispatch_environment,
    resolve_non_default_authority,
)

ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class ClaimCell:
    generation: int = 0
    dispatch_id: str | None = None
    operator_id: str | None = None
    phase: str = "EMPTY"


def reserve_dispatch(
    cell: ClaimCell,
    *,
    expected_generation: int,
    dispatch_id: str,
    serialization_available: bool = True,
    compatible_parallel_authorized: bool = False,
) -> tuple[str, ClaimCell]:
    """Reference admission oracle for one (work item, role) protected claim key."""
    if not serialization_available:
        return "BLOCKED_CLAIM_SERIALIZATION_UNAVAILABLE", cell
    if expected_generation != cell.generation:
        return "STALE", cell
    if cell.dispatch_id is not None:
        if cell.dispatch_id == dispatch_id:
            return "IDEMPOTENT", cell
        if compatible_parallel_authorized:
            # Parallel admission is allowed only by explicit durable authority. The
            # compact oracle does not model the sibling cell; it proves the gate.
            return "COMPATIBLE_PARALLEL_AUTHORIZED", cell
        return "DUPLICATE", cell
    return "ACCEPTED", replace(
        cell,
        generation=cell.generation + 1,
        dispatch_id=dispatch_id,
        phase="DISPATCHED",
    )


def claim_dispatch(
    cell: ClaimCell,
    *,
    expected_generation: int,
    dispatch_id: str,
    operator_id: str,
    serialization_available: bool = True,
) -> tuple[str, ClaimCell]:
    """Reference admission oracle for worker claim after one dispatch reservation."""
    if not serialization_available:
        return "BLOCKED_CLAIM_SERIALIZATION_UNAVAILABLE", cell
    if cell.dispatch_id == dispatch_id and cell.operator_id == operator_id and cell.phase == "CLAIMED":
        return "IDEMPOTENT", cell
    if expected_generation != cell.generation:
        return "STALE", cell
    if cell.dispatch_id != dispatch_id:
        return "DUPLICATE", cell
    if cell.operator_id is not None and cell.operator_id != operator_id:
        return "DUPLICATE", cell
    return "ACCEPTED", replace(
        cell,
        generation=cell.generation + 1,
        operator_id=operator_id,
        phase="CLAIMED",
    )


@dataclass(frozen=True)
class KeyedAdmissionState:
    """Keyed extension of the §11 race oracle: one ClaimCell per derived
    protected claim key. Purely derived state; never an authority source."""

    cells: dict[str, ClaimCell] = field(default_factory=dict)


def keyed_reserve(
    state: KeyedAdmissionState,
    dispatch: dict,
    *,
    serialization_available: bool = True,
    authority_grants: dict | None = None,
) -> tuple[str, KeyedAdmissionState]:
    """Keyed serialized-admission oracle (W10, D1/D2/E3/G8 + A8/C2/C3-C5/C7 gates).

    Order is normative: the A8 environment/profile projection verifier fails
    closed first, then the C2 non-default authority format gate (never
    downgraded), then the C3-C5/C7 resolution gate — a non-default group is
    admitted only when its ``compatibility_authority_ref`` resolves through the
    controller-resolved ``authority_grants`` inventory (the owner/controller
    proof path materialized before keyed admission) to a grant of the owning
    authority family applicable to the exact repository+task+role+group tuple;
    a syntactically durable ref alone never authorizes — then the claim key is
    derived from the dispatch identity alone, then the per-key CAS applies.
    Metadata (scheduler origin, execution environment, operator/provider,
    parent/responsibility) never reaches the key.
    """
    project_dispatch_environment(dispatch)
    group = dispatch.get("compatibility_group")
    authorize_non_default(group, dispatch.get("compatibility_authority_ref"))
    resolve_non_default_authority(
        repository=dispatch["repository"],
        task=dispatch["task"],
        role=dispatch["role"],
        compatibility_group=group,
        authority_ref=dispatch.get("compatibility_authority_ref"),
        authority_grants=authority_grants,
    )
    key = derive_claim_key(dispatch["repository"], dispatch["task"], dispatch["role"], group)
    cell = state.cells.get(key, ClaimCell())
    verdict, updated = reserve_dispatch(
        cell,
        expected_generation=dispatch.get("admission_generation", cell.generation),
        dispatch_id=dispatch["dispatch_id"],
        serialization_available=serialization_available,
    )
    cells = dict(state.cells)
    cells[key] = updated
    return verdict, KeyedAdmissionState(cells)


class ExecutionArchitectureRegression(unittest.TestCase):
    def text(self, rel: str) -> str:
        return (ROOT / rel).read_text(encoding="utf-8")

    def test_state_dimensions_are_separate(self) -> None:
        text = self.text("standards/EXECUTION_ARCHITECTURE_STANDARD.md")
        for token in ("Workflow routing state", "Gate state", "Execution-channel/provider state", "Dispatch state", "Candidate state", "Release state"):
            self.assertIn(token, text)

    def test_atomic_claim_duplicate_exclusion(self) -> None:
        execution = self.text("standards/EXECUTION_ARCHITECTURE_STANDARD.md")
        work_item = self.text("standards/GITHUB_WORK_ITEM_CONTRACT_STANDARD.md")

        for token in (
            "At most one incompatible active dispatch MUST exist per `(work item, role)`",
            "Claim admission is a compare-and-set style transition",
            "only the first claim accepted against the still-current predicates may become canonical",
            "MUST be rejected atomically as duplicate/stale",
            "same logical operator re-claiming the same dispatch is idempotent",
            "SINGLE_WRITER_ADMISSION",
            "LINEARIZABLE_CONDITIONAL_WRITE",
            "BLOCKED_CLAIM_SERIALIZATION_UNAVAILABLE",
            "Re-read alone is not an atomic primitive",
        ):
            self.assertIn(token, execution)

        for token in (
            "Claim admission is a compare-and-set operation over current durable GitHub facts",
            "At most one incompatible active claim/dispatch per `(work item, role)` is permitted",
            "A worker MUST NOT create or mutate implementation work before its claim is accepted",
            "TASK_DAG.md` remains a frozen planning/history checkpoint",
            "competing claim MUST be rejected before it can enter RUNNING or mutate implementation work",
        ):
            self.assertIn(token, work_item)

        self.assertIn("claimed", execution.split("### Workflow routing state", 1)[1].split("### Gate state", 1)[0])

    def test_atomic_claim_race_oracle(self) -> None:
        # 1/2. Two schedulers share generation 0: one active dispatch wins.
        initial = ClaimCell()
        result_a, after_a = reserve_dispatch(initial, expected_generation=0, dispatch_id="D-A")
        result_b, after_b = reserve_dispatch(after_a, expected_generation=0, dispatch_id="D-B")
        self.assertEqual("ACCEPTED", result_a)
        self.assertEqual("STALE", result_b)
        self.assertEqual("D-A", after_b.dispatch_id)
        self.assertEqual("DISPATCHED", after_b.phase)

        # A distinct dispatch cannot claim the already-reserved key.
        result_wrong, unchanged = claim_dispatch(
            after_b,
            expected_generation=after_b.generation,
            dispatch_id="D-B",
            operator_id="worker-b",
        )
        self.assertEqual("DUPLICATE", result_wrong)
        self.assertEqual(after_b, unchanged)

        # 1. Two logical operators share the same READY/dispatch snapshot: one claim wins.
        result_claim, claimed = claim_dispatch(
            after_b,
            expected_generation=after_b.generation,
            dispatch_id="D-A",
            operator_id="worker-a",
        )
        self.assertEqual("ACCEPTED", result_claim)
        result_competing, still_claimed = claim_dispatch(
            claimed,
            expected_generation=after_b.generation,
            dispatch_id="D-A",
            operator_id="worker-b",
        )
        self.assertEqual("STALE", result_competing)
        self.assertEqual(claimed, still_claimed)

        # 3. Same dispatch + same operator retry is idempotent and creates no new identity.
        retry_result, retry_state = claim_dispatch(
            claimed,
            expected_generation=claimed.generation,
            dispatch_id="D-A",
            operator_id="worker-a",
        )
        self.assertEqual("IDEMPOTENT", retry_result)
        self.assertEqual(claimed, retry_state)

        # 4. A stale expected snapshot rejects without mutation.
        stale_result, stale_state = reserve_dispatch(
            after_a,
            expected_generation=0,
            dispatch_id="D-stale",
        )
        self.assertEqual("STALE", stale_result)
        self.assertEqual(after_a, stale_state)

        # 5. Without an atomic-admission capability, both dispatch and claim fail closed.
        blocked_dispatch, blocked_dispatch_state = reserve_dispatch(
            initial,
            expected_generation=0,
            dispatch_id="D-blocked",
            serialization_available=False,
        )
        self.assertEqual("BLOCKED_CLAIM_SERIALIZATION_UNAVAILABLE", blocked_dispatch)
        self.assertEqual(initial, blocked_dispatch_state)
        blocked_claim, blocked_claim_state = claim_dispatch(
            after_a,
            expected_generation=after_a.generation,
            dispatch_id="D-A",
            operator_id="worker-blocked",
            serialization_available=False,
        )
        self.assertEqual("BLOCKED_CLAIM_SERIALIZATION_UNAVAILABLE", blocked_claim)
        self.assertEqual(after_a, blocked_claim_state)

        # 6. Incompatible parallelism stays rejected; explicit durable compatibility authority is required.
        incompatible_result, incompatible_state = reserve_dispatch(
            after_a,
            expected_generation=after_a.generation,
            dispatch_id="D-parallel",
            compatible_parallel_authorized=False,
        )
        self.assertEqual("DUPLICATE", incompatible_result)
        self.assertEqual(after_a, incompatible_state)
        compatible_result, compatible_state = reserve_dispatch(
            after_a,
            expected_generation=after_a.generation,
            dispatch_id="D-parallel",
            compatible_parallel_authorized=True,
        )
        self.assertEqual("COMPATIBLE_PARALLEL_AUTHORIZED", compatible_result)
        self.assertEqual(after_a, compatible_state)

    def test_validation_layering_and_drift(self) -> None:
        text = self.text("standards/VALIDATION_STANDARD.md")
        for token in ("concern | integration | closure", "HEAD drift", "BASE / merge-result drift", "VALIDATION_IMPACT_DECISION", "Alternate executor substitution"):
            self.assertIn(token, text)

    def test_candidate_freeze_is_operational(self) -> None:
        text = self.text("standards/RELEASE_STANDARD.md")
        for token in ("Operational immutability", "THAWED / INVALIDATED", "candidate ref", "Repository Integration"):
            self.assertIn(token, text)

    def test_hidden_escape_feedback_exists(self) -> None:
        text = self.text("standards/RELEASE_STANDARD.md") + self.text("standards/EXECUTION_ARCHITECTURE_STANDARD.md")
        for token in ("HIDDEN_PACK_BLIND_SPOT", "PACK_DEFECT", "new immutable private pack identity"):
            self.assertIn(token, text)

    def test_pointer_only_handoff(self) -> None:
        text = self.text("standards/LOCAL_AGENT_HANDOFF_PROTOCOL.md")
        self.assertIn("Pointer-only principle", text)
        self.assertIn("HANDOFF_READY", text)
        self.assertIn("Do not copy the full task contract into chat", text)

    def test_new_writer_surfaces_are_v2(self) -> None:
        for rel in ("standards/GITHUB_WORKFLOW.md", "standards/VERSION_INTEGRATION_WORKFLOW.md", "standards/LOCAL_AGENT_HANDOFF_PROTOCOL.md", "templates/local-agent-handoff-issue.md"):
            text = self.text(rel)
            self.assertIn("ai-dev:event:v2", text)
            self.assertNotIn("publish `ai-dev:event:v1`", text)

        protocol = self.text("standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md")
        self.assertIn("All newly emitted structured Agent events MUST use", protocol)
        self.assertIn("New writers MUST NOT emit v1", protocol)
        self.assertIn("scheduler", protocol)
        self.assertIn("repository-integration-controller", protocol)

    def test_event_schema_lifecycle(self) -> None:
        schema = json.loads(self.text("schemas/agent-event-v2.schema.json"))
        events = set(schema["properties"]["event"]["enum"])
        required = {"HANDOFF_READY", "DISPATCH_REQUEST", "DISPATCH_STATE_CHANGED", "CI_INFRA_EXCEPTION", "VALIDATION_IMPACT_DECISION", "CANDIDATE_STATE_CHANGED", "HIDDEN_ESCAPE_DISPOSITION", "RELEASE_QUALIFICATION", "REPOSITORY_INTEGRATION_RESULT"}
        self.assertTrue(required <= events, required - events)

        roles = set(schema["properties"]["actor_role"]["enum"])
        self.assertTrue({"scheduler", "repository-integration-controller"} <= roles)

        review_rule = next(
            rule for rule in schema["allOf"]
            if rule.get("if", {}).get("properties", {}).get("event", {}).get("const") == "REVIEW_DECISION"
        )
        self.assertIn("status", review_rule["then"]["required"])

    def test_small_project_runtime_is_optional(self) -> None:
        text = self.text("standards/EXECUTION_ARCHITECTURE_STANDARD.md")
        self.assertIn("A project is not required to run a centralized service", text)
        self.assertIn("Browser automation", text)
        self.assertIn("non-normative transport choices", text)


class T06BKeyedAdmissionOracleTests(unittest.TestCase):
    """W10 (R2 repair): keyed ClaimCell race oracle + non-vacuous invariance.

    Replaces the R1 placeholder whose env/origin loop never fed the function
    under test. Every variant below flows through the REAL reducer surfaces:
    ``v34_rules.derive_claim_key`` derives keys from full dispatch objects, and
    ``v34_rules.project_dispatch_environment`` / ``authorize_non_default`` /
    ``resolve_non_default_authority`` gate each keyed admission (R5: a
    non-default group additionally requires a controller-resolved owning-family
    grant; syntax-only durable refs no longer pass the C2 gate). Mutation sensitivity: if scheduler origin,
    execution environment, operator/provider identity, parent/responsibility
    metadata ever leaked into key derivation, the invariance assertion fails
    AND the race tests would show two accepted cells instead of
    winner + zero-mutation loser.
    """

    def _dispatch(self, **overrides) -> dict:
        value = {
            "dispatch_id": "D-A",
            "repository": "kaicreator-mm/ai-development-standard",
            "task": "#861",
            "role": "builder",
            "execution_profile": "LOCAL_BUILDER",
            "dispatch_state": "READY",
            "admission_generation": 0,
            "scheduler_origin": "LOCAL",
            "execution_environment": "LOCAL",
            "operator_id": "claude-code:worker-a",
            "parent_dispatch_ref": None,
            "responsibility_mode": None,
        }
        value.update(overrides)
        return value

    def test_claim_key_is_environment_and_origin_invariant(self) -> None:
        # The metadata dimensions vary through REAL dispatch objects; the
        # derived key never moves. Group is the only slot-4 dimension.
        base = self._dispatch()
        base_key = derive_claim_key(base["repository"], base["task"], base["role"], base.get("compatibility_group"))
        variants = [
            self._dispatch(scheduler_origin="WEB"),
            self._dispatch(execution_environment="WEB"),
            self._dispatch(operator_id="codex:worker-b"),
            self._dispatch(operator_id="claude-code:worker-a", dispatch_id="D-A2"),
            self._dispatch(parent_dispatch_ref="D-parent", responsibility_mode="DELEGATED_SUBWORK"),
            self._dispatch(responsibility_mode="RESPONSIBILITY_HANDOFF"),
        ]
        for variant in variants:
            with self.subTest(dispatch_id=variant["dispatch_id"], operator_id=variant["operator_id"]):
                self.assertEqual(
                    derive_claim_key(variant["repository"], variant["task"], variant["role"], variant.get("compatibility_group")),
                    base_key,
                )
        self.assertNotEqual(
            derive_claim_key(base["repository"], base["task"], base["role"], "interop"),
            base_key,
        )

    def test_d1_web_and_local_scheduler_race_one_default_key(self) -> None:
        web = self._dispatch(dispatch_id="D-web", scheduler_origin="WEB")
        local = self._dispatch(dispatch_id="D-local", scheduler_origin="LOCAL")
        self.assertEqual(
            derive_claim_key(web["repository"], web["task"], web["role"], web.get("compatibility_group")),
            derive_claim_key(local["repository"], local["task"], local["role"], local.get("compatibility_group")),
        )
        first, after_first = keyed_reserve(KeyedAdmissionState(), web)
        self.assertEqual("ACCEPTED", first)
        second, after_second = keyed_reserve(after_first, local)
        self.assertEqual("STALE", second)
        # Zero canonical mutation for the loser: the winner's cell is untouched
        # and no second cell exists (origin never manufactures a key).
        self.assertEqual(after_first.cells, after_second.cells)
        self.assertEqual(1, len(after_second.cells))

    def test_e3_origin_race_is_order_independent(self) -> None:
        for first_dispatch, second_dispatch in (
            (self._dispatch(dispatch_id="D-web", scheduler_origin="WEB"), self._dispatch(dispatch_id="D-local", scheduler_origin="LOCAL")),
            (self._dispatch(dispatch_id="D-local", scheduler_origin="LOCAL"), self._dispatch(dispatch_id="D-web", scheduler_origin="WEB")),
        ):
            verdict_a, state_a = keyed_reserve(KeyedAdmissionState(), first_dispatch)
            verdict_b, state_b = keyed_reserve(state_a, second_dispatch)
            with self.subTest(winner=first_dispatch["dispatch_id"]):
                self.assertEqual("ACCEPTED", verdict_a)
                self.assertEqual("STALE", verdict_b)
                self.assertEqual(1, len(state_b.cells))

    def test_d2_stale_generation_is_rejected_with_zero_mutation(self) -> None:
        verdict, state = keyed_reserve(KeyedAdmissionState(), self._dispatch())
        self.assertEqual("ACCEPTED", verdict)
        stale, unchanged = keyed_reserve(
            state,
            self._dispatch(dispatch_id="D-stale", admission_generation=0),
        )
        self.assertEqual("STALE", stale)
        self.assertEqual(state.cells, unchanged.cells)

    def test_d3_f2_idempotent_replay_creates_no_new_identity(self) -> None:
        verdict, state = keyed_reserve(KeyedAdmissionState(), self._dispatch())
        self.assertEqual("ACCEPTED", verdict)
        replay, replayed = keyed_reserve(
            state,
            self._dispatch(admission_generation=1),
        )
        self.assertEqual("IDEMPOTENT", replay)
        self.assertEqual(state.cells, replayed.cells)

    def test_d4_terminal_release_never_decrements_generation(self) -> None:
        # Same carried semantics as the v4.8 ownership oracle's
        # record_terminal_release: phase moves to a terminal state, the
        # per-key generation is never written backwards.
        verdict, state = keyed_reserve(KeyedAdmissionState(), self._dispatch())
        self.assertEqual("ACCEPTED", verdict)
        key = derive_claim_key("kaicreator-mm/ai-development-standard", "#861", "builder")
        released = replace(state.cells[key], phase="TERMINAL")
        self.assertEqual(state.cells[key].generation, released.generation)
        self.assertEqual("TERMINAL", released.phase)
        terminal_state = KeyedAdmissionState(cells={key: released})
        stale_successor, unchanged = keyed_reserve(
            terminal_state,
            self._dispatch(dispatch_id="D-succ", admission_generation=0),
        )
        self.assertEqual("STALE", stale_successor)
        self.assertEqual(terminal_state.cells, unchanged.cells)
        same_generation_replay, still = keyed_reserve(
            terminal_state,
            self._dispatch(admission_generation=1),
        )
        self.assertEqual("IDEMPOTENT", same_generation_replay)
        self.assertEqual(terminal_state.cells, still.cells)

    def test_g8_parent_child_cannot_widen_compatibility(self) -> None:
        verdict, state = keyed_reserve(KeyedAdmissionState(), self._dispatch())
        self.assertEqual("ACCEPTED", verdict)
        child = self._dispatch(
            dispatch_id="D-child",
            admission_generation=1,
            parent_dispatch_ref="D-A",
            responsibility_mode="DELEGATED_SUBWORK",
        )
        self.assertEqual(
            derive_claim_key("kaicreator-mm/ai-development-standard", "#861", "builder"),
            derive_claim_key("kaicreator-mm/ai-development-standard", "#861", "builder", None),
        )
        child_verdict, child_state = keyed_reserve(state, child)
        self.assertEqual("DUPLICATE", child_verdict)
        self.assertEqual(state.cells, child_state.cells)
        self.assertEqual(1, len(child_state.cells))

    def test_g3_provider_identity_never_manufactures_parallelism(self) -> None:
        verdict, state = keyed_reserve(KeyedAdmissionState(), self._dispatch())
        self.assertEqual("ACCEPTED", verdict)
        other_provider = self._dispatch(
            dispatch_id="D-provider-b",
            admission_generation=1,
            operator_id="codex:worker-b",
        )
        competitor, competed = keyed_reserve(state, other_provider)
        self.assertEqual("DUPLICATE", competitor)
        self.assertEqual(state.cells, competed.cells)

    def test_n1_h6_two_default_group_builders_admit_exactly_one(self) -> None:
        verdict, state = keyed_reserve(KeyedAdmissionState(), self._dispatch(dispatch_id="D-b1"))
        self.assertEqual("ACCEPTED", verdict)
        second, after = keyed_reserve(
            state,
            self._dispatch(dispatch_id="D-b2", admission_generation=1),
        )
        self.assertEqual("DUPLICATE", second)
        self.assertEqual(1, len(after.cells))

    # Controller-resolved grant inventory modeled for the keyed oracle. This
    # is oracle data exercising the C3-C5/C7 resolution mechanics (the
    # owner/controller proof path materialized before keyed admission); it is
    # NOT a claim that any real GitHub comment authorizes
    # validator/windows+linux on #861 today.
    VALIDATION_GRANT = {
        "ref": "#861@6000000000",
        "authority_family": "VALIDATION",
        "repository": "kaicreator-mm/ai-development-standard",
        "task": "#861",
        "role": "validator",
        "groups": ["validator/windows", "validator/linux"],
    }

    def test_c6_h3_authorized_non_default_groups_run_parallel(self) -> None:
        grants = {"#861@6000000000": dict(self.VALIDATION_GRANT)}
        windows = self._dispatch(
            dispatch_id="D-win",
            role="validator",
            execution_profile="LOCAL_VALIDATOR",
            compatibility_group="validator/windows",
            compatibility_authority_ref="#861@6000000000",
        )
        linux = self._dispatch(
            dispatch_id="D-linux",
            role="validator",
            execution_profile="LOCAL_VALIDATOR",
            compatibility_group="validator/linux",
            compatibility_authority_ref="#861@6000000000",
        )
        first, after_first = keyed_reserve(KeyedAdmissionState(), windows, authority_grants=grants)
        second, after_second = keyed_reserve(after_first, linux, authority_grants=grants)
        self.assertEqual("ACCEPTED", first)
        self.assertEqual("ACCEPTED", second)
        self.assertEqual(2, len(after_second.cells))

    def test_c4_c5_c7_unrelated_builder_admission_ref_never_authorizes_validator_parallelism(self) -> None:
        # Exact Fresh-Review-R4 P1-2 regression: the historical R2
        # bounded-repair Builder admission #861@6023707736 is a syntactically
        # durable ref, but it is not a Validation authority for
        # validator/windows+linux and MUST be rejected at the keyed admission
        # boundary instead of unlocking duplicate exclusion.
        builder_ref = "#861@6023707736"
        unauthorized = self._dispatch(
            dispatch_id="D-win",
            role="validator",
            execution_profile="LOCAL_VALIDATOR",
            compatibility_group="validator/windows",
            compatibility_authority_ref=builder_ref,
        )
        for grants in (None, {}):
            with self.subTest(grants=grants):
                with self.assertRaises(ValueError) as caught:
                    keyed_reserve(KeyedAdmissionState(), unauthorized, authority_grants=grants)
                self.assertIn("AUTHORITY_UNRESOLVED", str(caught.exception))
        builder_grants = {
            builder_ref: {
                "ref": builder_ref,
                "authority_family": "TASK_PACK",
                "repository": "kaicreator-mm/ai-development-standard",
                "task": "#861",
                "role": "builder",
                "groups": ["validator/windows", "validator/linux"],
            }
        }
        with self.assertRaises(ValueError) as caught:
            keyed_reserve(KeyedAdmissionState(), unauthorized, authority_grants=builder_grants)
        self.assertIn("AUTHORITY_FAMILY_MISMATCH", str(caught.exception))

    def test_c4_grant_applicability_is_tuple_exact(self) -> None:
        grants = {"#861@6000000000": dict(self.VALIDATION_GRANT)}
        other_repo = self._dispatch(
            dispatch_id="D-other-repo",
            role="validator",
            execution_profile="LOCAL_VALIDATOR",
            compatibility_group="validator/windows",
            compatibility_authority_ref="#861@6000000000",
            repository="other/repo",
        )
        with self.assertRaises(ValueError) as caught:
            keyed_reserve(KeyedAdmissionState(), other_repo, authority_grants=grants)
        self.assertIn("AUTHORITY_NOT_APPLICABLE", str(caught.exception))
        other_group = self._dispatch(
            dispatch_id="D-other-group",
            role="validator",
            execution_profile="LOCAL_VALIDATOR",
            compatibility_group="validator/macos",
            compatibility_authority_ref="#861@6000000000",
        )
        with self.assertRaises(ValueError) as caught:
            keyed_reserve(KeyedAdmissionState(), other_group, authority_grants=grants)
        self.assertIn("AUTHORITY_NOT_APPLICABLE", str(caught.exception))

    def test_c3_default_group_needs_no_grant_inventory(self) -> None:
        # Default-group dispatches stay readable without any authority data.
        verdict, state = keyed_reserve(KeyedAdmissionState(), self._dispatch(dispatch_id="D-def"))
        self.assertEqual("ACCEPTED", verdict)
        self.assertEqual(1, len(state.cells))

    def test_c2_non_default_without_authority_fails_closed_before_cas(self) -> None:
        unauthorized = self._dispatch(
            dispatch_id="D-unauth",
            role="validator",
            execution_profile="LOCAL_VALIDATOR",
            compatibility_group="validator/windows",
            compatibility_authority_ref=None,
        )
        with self.assertRaises(ValueError):
            keyed_reserve(KeyedAdmissionState(), unauthorized)

    def test_a8_contradiction_is_rejected_before_any_admission(self) -> None:
        contradicted = self._dispatch(execution_environment="WEB")
        with self.assertRaises(ValueError) as caught:
            keyed_reserve(KeyedAdmissionState(), contradicted)
        self.assertIn("ENVIRONMENT_PROFILE_CONTRADICTION", str(caught.exception))


if __name__ == "__main__":
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__]))
    raise SystemExit(0 if result.wasSuccessful() else 1)
