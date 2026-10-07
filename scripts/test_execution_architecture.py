from __future__ import annotations

from dataclasses import dataclass, field, replace
import hashlib
import json
from pathlib import Path
import sys
import unittest

from test_v47_authority_registry import resolve_registry
from v34_rules import (
    AUTHORITY_GRANT_BLOCK_END,
    AUTHORITY_GRANT_BLOCK_START,
    authorize_non_default,
    derive_claim_key,
    parse_authority_grant_block,
    project_dispatch_environment,
    resolve_non_default_authority,
)

ROOT = Path(__file__).resolve().parents[1]


def _git_blob_id(data: bytes) -> str:
    """Exact git blob identity of byte content (local, deterministic)."""
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def authority_readback(root: Path = ROOT) -> dict:
    """Durable owner/controller readback for the R6 grant-binding contract.

    Reuses the existing verified owner-resolution path — the v4.7 registry
    resolver over the checked-in ``standard-manifest.json`` (owner paths
    verified present in the checkout) — and binds it to the exact durable
    subject: the git blob id of the manifest that was read back. The
    controller materializes this readback before keyed admission; the machine
    boundary verifies each grant against it, so a caller-made mapping without
    the binding manufactures no authority.
    """
    root = Path(root)
    manifest_data = (root / "standard-manifest.json").read_bytes()
    schema = json.loads(
        (root / "schemas" / "authority-applicability-entry-v1.schema.json").read_text(encoding="utf-8")
    )
    owners = resolve_registry(json.loads(manifest_data.decode("utf-8")), schema, root=root)
    return {"owners": owners, "subject": _git_blob_id(manifest_data)}


# R8 (Fresh Review R7 P1-1): the positive authority fixture is a synthetic
# canonical grant record — fixture/oracle data standing in for an
# adapter-materialized durable fact — whose canonical content EXPLICITLY
# carries the machine-readable ``ai-dev:authority-grant v1`` authorization
# block granting validator/windows+linux for the exact repository/task/role
# tuple on #861. The machine proof is that authorization is DERIVED from the
# content (digest recomputation + deterministic parsing), never asserted
# alongside it: the verifier recomputes the content digest and parses the
# grant block out of ``canonical_content``; no trusted-looking projected field
# on a readback record is ever read.
#
# AUTHORITY_FACT_REF below is the REAL durable comment #861@6043191203 (the
# Concern Validation R6 terminal on Issue #861). Its VERBATIM canonical
# content is embedded in ``AUTHORITY_FACT_CONTENT`` (fetched once via the
# API; embedding text is network-free at test time) and grants NEITHER
# validator/windows nor validator/linux — the R7 positive had anchored this
# real ref to a synthetic digest and injected groups the real content never
# granted, manufacturing authorization. It is now the R8 invented-groups
# negative; the review-verified 404 durable-looking ref #861@6000000000
# stays negative-only as well.
AUTHORITY_GRANT_RECORD_REF = "#861@6000000001"

_GRANT_RECORD_DEFAULTS = {
    "authority_family": "VALIDATION",
    "repository": "kaicreator-mm/ai-development-standard",
    "task": "#861",
    "role": "validator",
    "groups": ("validator/windows", "validator/linux"),
}


def _grant_record_content(
    *, authority_family: str, repository: str, task: str, role: str, groups
) -> str:
    """Synthetic canonical grant-record content (fixture/oracle data standing
    in for an adapter-materialized durable fact) whose machine-readable block
    EXPLICITLY grants the exact tuple and group set."""
    return (
        "<!-- ai-dev:event:v2 -->\n"
        "## V410-T06B authority grant record (fixture/oracle data)\n"
        "\n"
        "Fixture canonical durable-fact content standing in for an\n"
        "adapter-materialized durable authority fact; it is NOT a claim that\n"
        "any real durable comment authorizes validator/windows+linux on #861\n"
        "today (same oracle status as the modeled VALIDATION grant). The\n"
        "block below is the machine-readable authorization the verifier\n"
        "derives the grant from.\n"
        "\n"
        "```text\n"
        "ai-dev:authority-grant v1\n"
        f"authority_family: {authority_family}\n"
        f"repository: {repository}\n"
        f"task: {task}\n"
        f"role: {role}\n"
        f"groups: {', '.join(groups)}\n"
        "ai-dev:authority-grant end\n"
        "```\n"
    )


AUTHORITY_GRANT_RECORD_CONTENT = _grant_record_content(**_GRANT_RECORD_DEFAULTS)
AUTHORITY_GRANT_RECORD_DIGEST = hashlib.sha256(
    AUTHORITY_GRANT_RECORD_CONTENT.encode("utf-8")
).hexdigest()

AUTHORITY_FACT_REF = "#861@6043191203"
AUTHORITY_FACT_CONTENT = """\
<!-- ai-dev:event:v2 -->
## V410-T06B Concern Validation R6 — successor validator terminal

```text
V410_T06B_CONCERN_VALIDATION_R6=PASS; HEAD=41df8e5ab2cb01208c1db375cd44c0177a814558; TREE=7822d3ac732e292a177efba9354b79d73d480d39; FINDINGS=P0:0,P1:0,P2:0,P3:0; CURRENTNESS=PASS; NEXT=FRESH_WEB_REVIEW_R6
DISPATCH_ID=V410-T06B-VALIDATOR-R6
TASK=#861 PR=#927
CLAIM=#861@6043125433
ADMISSION=#861@6041610051 (V410-T06B-VALIDATOR-R6-ADMISSION-1)
SOURCE_PROPOSAL=#861@6041603709
NO_VERDICT_TRANSFER=HONORED (Validation R5 PASS and Fresh Review R5 CHANGES_REQUESTED #861@6040083891 are historical evidence input only; no earlier PASS is inherited)
MERGE=NOT_PERFORMED_BY_VALIDATOR
SOURCE_MUTATION=NONE
```

### Exact-subject / currentness

Final live re-read immediately before this terminal: PR #927 is still OPEN, unmerged and mergeable at exact HEAD `41df8e5ab2cb01208c1db375cd44c0177a814558`; independent git readback binds that commit to exact tree `7822d3ac732e292a177efba9354b79d73d480d39`, matching canonical admission #861@6041610051 (REQUESTED_HEAD/REQUESTED_TREE); base remains `ab8339f83a6a2308a5aa39009bd126698320ceee` (`origin/version/v4.10.0` still at base; merge-base readback equals base — integration head has not moved). No competing validator claim or terminal appeared after this validator's claim #861@6043125433. The repository's `verify` GitHub Actions check runs on the exact head `41df8e5` completed SUCCESS (2 runs).

### R6 exact repair delta — PASS boundedness

Independent compare `a7dc1273cfdfc694888367a70d807d1c76e63eaf..41df8e5ab2cb01208c1db375cd44c0177a814558` is exactly one commit and exactly five modified paths, zero add/delete paths — all inside the admitted R6 `EXPECTED_WRITE_SET` (`scripts/v34_rules.py`, `scripts/test_execution_architecture.py`, `scripts/test_v410_t06b_multi_dispatch_conformance.py`, `.agent/execution/V410-T06B-R1/TEST_MATRIX.yaml`, `.agent/execution/V410-T06B-R1/FAILURE_MATRIX.yaml`). The two conditional paths (`schemas/execution-state.schema.json`, `scripts/test_protocol_schemas.py`) are correctly untouched — schema shape did not change. No Product/L2/DAG mutation, no authority/lifecycle creation, no second scheduler/registry, no deleted test definitions (zero removed `def test_` in either test file — no NO_GREEN_BY_DELETION).

### Fresh Review R5 findings — CLOSED (machine-verified on the exact tree)

1. **P1-1 CLOSED — grant inventory bound to the durable owner/controller readback; caller-made mapping manufactures no authority.** `scripts/v34_rules.py` `resolve_non_default_authority` now additionally requires `authority_readback` = `{owners: Mapping[str,str], subject: 40-hex}`; a missing/malformed readback fails `AUTHORITY_UNRESOLVED`; each grant must name an `owner_concern` resolvable in the readback owners map (`AUTHORITY_OWNER_UNRESOLVED`) and carry `readback_subject` equal to the current durable subject (`AUTHORITY_CURRENTNESS_MISMATCH` — registry drift invalidates grants); a grant ref pointing back at the dispatch's own durable refs is rejected (`AUTHORITY_SELF_REFERENCE`, `self_refs` auto-collected from `source_proposal_ref`/`canonical_admission_ref` in `keyed_reserve`). The readback is materialized in `test_execution_architecture.authority_readback()` by reusing the already-verified v4.7 registry resolution (`test_v47_authority_registry.resolve_registry` over the checked-in `standard-manifest.json#semantic_authorities`) plus a local `hashlib` git-blob-id computation — no network inside the pure verifier; the re-read itself remains the controller trust boundary, consistent with `scripts/resolve_standard_read_set.py`. Regressions pin: R5-era self-made grant without readback ⇒ `AUTHORITY_UNRESOLVED`, with readback but no binding ⇒ `AUTHORITY_OWNER_UNRESOLVED`; forged subject ⇒ `AUTHORITY_CURRENTNESS_MISMATCH`; unknown concern ⇒ `AUTHORITY_OWNER_UNRESOLVED`; self-referencing grant ⇒ `AUTHORITY_SELF_REFERENCE`. R5 invariants preserved: unrelated Builder-admission ref `#861@6023707736` still rejected (`AUTHORITY_FAMILY_MISMATCH`), tuple-exact applicability intact, default-group short-circuit unchanged (`test_c3` green).
2. **P2-1 CLOSED — same-work-item active_dispatches enforcement + injection negatives.** `v34_rules.execution_state_projection_problems` now re-parses every row's `protected_claim_key` via `parse_claim_key` and requires the derived repository/task to equal the outer execution-state `repository`/`work_item`, surfacing `ACTIVE_DISPATCH_FOREIGN_WORK_ITEM` (malformed key ⇒ `ACTIVE_DISPATCH_ROW_MALFORMED`). The row contract deliberately drops the raw task field, so the probe is the owned detection surface; the schema subset cannot express the cross-row/outer check and the schema is correctly unchanged. The full-state positive fixture (`ExecutionStateIntegrationTests._source`) is rebased to ONE work item (#861) with distinct roles (builder LOCAL + validator `PLATFORM_VALIDATOR`→null env + reviewer WEB), each derived key mutually distinct per #861 rule 2; `ExecutionStateConformanceTests._rows` likewise rebased; `test_cross_task_injection_is_flagged_by_the_conformance_probe` (#860 into #861 state) and `test_cross_repository_injection_is_flagged_by_the_conformance_probe` both assert exactly `[ACTIVE_DISPATCH_FOREIGN_WORK_ITEM]`. The remaining multi-task rows in `test_exact_subject_refs_are_carried_and_validated` are row-projection unit data, not an execution-state instance — out of P2-1 scope.
3. Matrix updates are truthful: C_SECTION/E_SECTION rows and DISP-C3-C5-AUTHORITY-RESOLUTION extended with the R6 readback/self-reference semantics; new DISP-SAME-WORK-ITEM-PROJECTION disposition; coverage rows enumerate the new R6 negatives exactly as implemented.

### R5 closed findings — still closed (carried, re-verified green)

Default-group schema/helper/oracle agreement (A4b/A4c/A4d), controller-resolved owning-family grants (C3-C5/C7), H2 multi-active singular-null fail-closed (schema conditional + probe), duplicate-active-key probe, keyed CAS/stale/terminal rules, dogfood T1-T5 worked negatives, frozen J guards — all present and passing in the 51-test focused suite and the 28-test W10 oracle; zero test deletions in this round.

### Mandatory LOCAL commands — all green on the exact tree

Executed in a fresh read-only validator worktree pinned at the exact HEAD (`task/v4.10.0-v410-t06b-validator-r6` at `41df8e5`, tree readback `7822d3a…`, working tree clean before and after; Python 3.14.6):

```text
test_v410_t06b_multi_dispatch_conformance.py  51 tests OK
test_execution_architecture.py                28 tests OK (25 + 3 new R6)
test_protocol_schemas.py                      28 tests OK
test_v410_owner_convergence.py                23 tests OK
test_v48_registry_adoption.py                 19 tests OK
test_v410_t06b_core_inventory.py               7 tests OK
verify_standard.py                            PASS (224 manifest files, 41 bootstrap-required)
verify_event_writer_surfaces.py               PASS (95 active writer surfaces)
tools/task-check.sh                           PASS (no package.json, nothing to run)
```

### Environment orthogonality (dogfood)

This validation was executed by a LOCAL tool-capable worker (operator provenance: claude-code:zcode-glm-5.3-flash); environment/provider identity carried no verdict authority — the verdict rests only on the machine evidence above. Per ON_PASS, the successor is a genuinely Fresh WEB Independent Review R6 bound to the unchanged exact HEAD/tree `41df8e5/7822d3a` in a new context not used by any auxiliary WEB lane.
"""
AUTHORITY_FACT_DIGEST = hashlib.sha256(
    AUTHORITY_FACT_CONTENT.encode("utf-8")
).hexdigest()


def authority_fact_readbacks(**overrides) -> dict:
    """Durable-fact readback inventory keyed by the durable ref (R8).

    Models the controller/authority-reader adapter output at the trust
    boundary: the adapter live-resolves the durable ref and materializes
    identity (``ref``), existence/currentness (``exists``), and the content
    binding — ``canonical_content`` plus ``content_digest``, the SHA-256 of
    that exact content. It carries NO authorization fields: family/tuple/
    groups are derived by the verifier from the canonical content alone.
    Semantic overrides (``authority_family``/``repository``/``task``/
    ``role``/``groups``) regenerate the content and recompute the digest, so
    the evidence stays mechanically consistent unless the binding itself is
    what a test corrupts (``content_digest``/``canonical_content`` overrides).
    Purely local; the verifier consumes the evidence without network access.
    """
    semantic = {
        key: overrides.pop(key)
        for key in ("authority_family", "repository", "task", "role", "groups")
        if key in overrides
    }
    params = {**_GRANT_RECORD_DEFAULTS, **semantic}
    if "canonical_content" in overrides:
        content = overrides.pop("canonical_content")
    else:
        content = _grant_record_content(**params)
    fact = {
        "ref": overrides.pop("ref", AUTHORITY_GRANT_RECORD_REF),
        "exists": overrides.pop("exists", True),
        "canonical_content": content,
        "content_digest": overrides.pop(
            "content_digest",
            hashlib.sha256(content.encode("utf-8")).hexdigest()
            if isinstance(content, str)
            else AUTHORITY_GRANT_RECORD_DIGEST,
        ),
    }
    if overrides:
        raise TypeError(f"unknown authority-fact-readback overrides: {sorted(overrides)}")
    return {fact["ref"]: fact}


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
    readback: dict | None = None,
    fact_readbacks: dict | None = None,
) -> tuple[str, KeyedAdmissionState]:
    """Keyed serialized-admission oracle (W10, D1/D2/E3/G8 + A8/C2/C3-C5/C7 gates).

    Order is normative: the A8 environment/profile projection verifier fails
    closed first, then the C2 non-default authority format gate (never
    downgraded), then the C3-C5/C7 resolution gate — a non-default group is
    admitted only when its ``compatibility_authority_ref`` is bound by the
    trusted durable-fact readback (R8: the controller/authority-reader
    adapter-materialized evidence carrying the exact ref identity,
    existence/currentness, the canonical fact content and its content-addressed
    digest — recomputed, never trusted — with the owning authority family, the
    exact repository+task+role applicability and the explicit authorization
    content DERIVED by deterministically parsing the ``ai-dev:authority-grant
    v1`` block out of that content; authorization is derived from the content
    alone and a caller grant drifting from it is rejected), bound to
    the controller-resolved ``authority_grants`` inventory projection (the
    owner/controller proof path materialized before keyed admission) to a
    grant of the owning authority family applicable to the exact
    repository+task+role+group tuple, and bound to the durable
    owner/controller ``readback`` (R6: owner_concern resolvable in the
    readback owners map + readback_subject equal to the current durable
    subject; a self-referencing grant ref — one of the dispatch's own durable
    refs — is rejected);
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
        authority_readback=readback,
        authority_fact_readbacks=fact_readbacks,
        self_refs=tuple(
            ref
            for ref in (dispatch.get("source_proposal_ref"), dispatch.get("canonical_admission_ref"))
            if isinstance(ref, str)
        ) or None,
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
    ``v34_rules.resolve_non_default_authority`` gate each keyed admission (R5/R6:
    a non-default group additionally requires a controller-resolved owning-family
    grant bound to the durable owner/controller readback — owner_concern
    resolvable in the readback owners map, readback_subject equal to the
    current durable subject, no self-referencing grant ref — so a test-internal
    self-made mapping manufactures no authority; syntax-only durable refs no
    longer pass the C2 gate). Mutation sensitivity: if scheduler origin,
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
    # validator/windows+linux on #861 today. R6: a grant additionally binds to
    # the durable owner/controller readback — owner_concern resolved through
    # the checked-in registry readback and readback_subject equal to the
    # current durable manifest blob id — so a test-internal self-made mapping
    # without that binding manufactures no authority. R7: the grant is only a
    # projection — its authorization fields must equal the derived grant, and
    # authorization itself is derived from evidence, never asserted. R8: the
    # evidence is the canonical durable-fact CONTENT: the positive fixture
    # cites AUTHORITY_GRANT_RECORD_REF, the synthetic oracle grant record whose
    # content explicitly carries the ai-dev:authority-grant block for this
    # exact tuple; the real durable comment AUTHORITY_FACT_REF
    # (#861@6043191203) grants no such groups and is the invented-groups
    # negative (test_r8_*).
    def validation_grant(self, **overrides) -> dict:
        grant = {
            "ref": AUTHORITY_GRANT_RECORD_REF,
            "authority_family": "VALIDATION",
            "owner_concern": "validation.concern_evidence_and_exact_subject",
            "readback_subject": authority_readback()["subject"],
            "repository": "kaicreator-mm/ai-development-standard",
            "task": "#861",
            "role": "validator",
            "groups": ["validator/windows", "validator/linux"],
        }
        grant.update(overrides)
        return grant

    def test_c6_h3_authorized_non_default_groups_run_parallel(self) -> None:
        grants = {AUTHORITY_GRANT_RECORD_REF: self.validation_grant()}
        readback = authority_readback()
        facts = authority_fact_readbacks()
        windows = self._dispatch(
            dispatch_id="D-win",
            role="validator",
            execution_profile="LOCAL_VALIDATOR",
            compatibility_group="validator/windows",
            compatibility_authority_ref=AUTHORITY_GRANT_RECORD_REF,
        )
        linux = self._dispatch(
            dispatch_id="D-linux",
            role="validator",
            execution_profile="LOCAL_VALIDATOR",
            compatibility_group="validator/linux",
            compatibility_authority_ref=AUTHORITY_GRANT_RECORD_REF,
        )
        first, after_first = keyed_reserve(
            KeyedAdmissionState(), windows,
            authority_grants=grants, readback=readback, fact_readbacks=facts,
        )
        second, after_second = keyed_reserve(
            after_first, linux,
            authority_grants=grants, readback=readback, fact_readbacks=facts,
        )
        self.assertEqual("ACCEPTED", first)
        self.assertEqual("ACCEPTED", second)
        self.assertEqual(2, len(after_second.cells))

    def test_r6_self_made_grant_without_readback_binding_manufactures_no_authority(self) -> None:
        # Exact Fresh-Review-R5 P1-1 regression: the R5-era C6/H3 fixture was a
        # caller-made mapping with a fabricated ref — it passed because the
        # inventory was caller-asserted. Now the same self-made grant is
        # rejected: no durable owner/controller readback supplied, and even
        # with one it names no owner_concern / readback_subject binding.
        self_made = {
            "ref": AUTHORITY_GRANT_RECORD_REF,
            "authority_family": "VALIDATION",
            "repository": "kaicreator-mm/ai-development-standard",
            "task": "#861",
            "role": "validator",
            "groups": ["validator/windows", "validator/linux"],
        }
        grants = {AUTHORITY_GRANT_RECORD_REF: self_made}
        dispatch = self._dispatch(
            dispatch_id="D-win",
            role="validator",
            execution_profile="LOCAL_VALIDATOR",
            compatibility_group="validator/windows",
            compatibility_authority_ref=AUTHORITY_GRANT_RECORD_REF,
        )
        with self.assertRaises(ValueError) as caught:
            keyed_reserve(KeyedAdmissionState(), dispatch, authority_grants=grants)
        self.assertIn("AUTHORITY_UNRESOLVED", str(caught.exception))
        with self.assertRaises(ValueError) as caught:
            keyed_reserve(
                KeyedAdmissionState(), dispatch,
                authority_grants=grants, readback=authority_readback(),
                fact_readbacks=authority_fact_readbacks(),
            )
        self.assertIn("AUTHORITY_OWNER_UNRESOLVED", str(caught.exception))

    def test_r6_stale_or_unknown_readback_binding_fails_closed(self) -> None:
        readback = authority_readback()
        dispatch = self._dispatch(
            dispatch_id="D-win",
            role="validator",
            execution_profile="LOCAL_VALIDATOR",
            compatibility_group="validator/windows",
            compatibility_authority_ref=AUTHORITY_GRANT_RECORD_REF,
        )
        stale = {AUTHORITY_GRANT_RECORD_REF: self.validation_grant(readback_subject="0" * 40)}
        with self.assertRaises(ValueError) as caught:
            keyed_reserve(
                KeyedAdmissionState(), dispatch,
                authority_grants=stale, readback=readback,
                fact_readbacks=authority_fact_readbacks(),
            )
        self.assertIn("AUTHORITY_CURRENTNESS_MISMATCH", str(caught.exception))
        unknown_concern = {AUTHORITY_GRANT_RECORD_REF: self.validation_grant(owner_concern="no.such_concern")}
        with self.assertRaises(ValueError) as caught:
            keyed_reserve(
                KeyedAdmissionState(), dispatch,
                authority_grants=unknown_concern, readback=readback,
                fact_readbacks=authority_fact_readbacks(),
            )
        self.assertIn("AUTHORITY_OWNER_UNRESOLVED", str(caught.exception))
        # The re-read that produces the readback is the controller trust
        # boundary (per scripts/resolve_standard_read_set.py): the machine
        # layer verifies the grant against the supplied durable readback, so
        # producing the readback from the real checkout is what a caller-made
        # mapping cannot fake without knowing current durable state.

    def test_r7_decorated_grant_without_durable_fact_readback_manufactures_no_authority(self) -> None:
        # Exact Fresh-Review-R6 P1-1 regression (REQUIRED_FIX_2): a caller
        # grant carrying a valid current registry subject, a valid
        # owner_concern and the correct tuple still manufactures no authority
        # when the referenced durable fact is not bound by trusted readback
        # evidence. #861@6000000000 is the review-verified 404 durable-looking
        # ref and stays negative-only.
        nonexistent_ref = "#861@6000000000"
        decorated = self.validation_grant(ref=nonexistent_ref)
        grants = {nonexistent_ref: decorated}
        readback = authority_readback()
        dispatch = self._dispatch(
            dispatch_id="D-win",
            role="validator",
            execution_profile="LOCAL_VALIDATOR",
            compatibility_group="validator/windows",
            compatibility_authority_ref=nonexistent_ref,
        )
        # No fact-readback inventory at all.
        with self.assertRaises(ValueError) as caught:
            keyed_reserve(
                KeyedAdmissionState(), dispatch,
                authority_grants=grants, readback=readback,
            )
        self.assertIn("AUTHORITY_UNRESOLVED", str(caught.exception))
        # Inventory present but the exact ref was never materialized.
        with self.assertRaises(ValueError) as caught:
            keyed_reserve(
                KeyedAdmissionState(), dispatch,
                authority_grants=grants, readback=readback,
                fact_readbacks=authority_fact_readbacks(),
            )
        self.assertIn("AUTHORITY_UNRESOLVED", str(caught.exception))
        # The adapter live-read the ref and it does not exist (404).
        with self.assertRaises(ValueError) as caught:
            keyed_reserve(
                KeyedAdmissionState(), dispatch,
                authority_grants=grants, readback=readback,
                fact_readbacks=authority_fact_readbacks(
                    ref=nonexistent_ref, exists=False, content_digest="a" * 64,
                ),
            )
        self.assertIn("AUTHORITY_UNRESOLVED", str(caught.exception))
        # Readback without the content-addressed binding to the fact content.
        with self.assertRaises(ValueError) as caught:
            keyed_reserve(
                KeyedAdmissionState(), dispatch,
                authority_grants=grants, readback=readback,
                fact_readbacks=authority_fact_readbacks(
                    ref=nonexistent_ref, content_digest="not-a-digest",
                ),
            )
        self.assertIn("AUTHORITY_UNRESOLVED", str(caught.exception))

    def test_r7_non_authorizing_or_drifting_durable_fact_fails_closed(self) -> None:
        # REQUIRED_FIX_2 (R7) + R8 semantics: with the fact bound, a decorated
        # caller grant still fails when the durable fact content does not
        # explicitly authorize the group, carries the wrong family, or the
        # grant drifts from the content-derived authorization.
        readback = authority_readback()
        grants = {AUTHORITY_GRANT_RECORD_REF: self.validation_grant()}
        dispatch = self._dispatch(
            dispatch_id="D-win",
            role="validator",
            execution_profile="LOCAL_VALIDATOR",
            compatibility_group="validator/windows",
            compatibility_authority_ref=AUTHORITY_GRANT_RECORD_REF,
        )
        # Durable fact content exists but does not authorize this group (the
        # semantic override regenerates the canonical content and its digest,
        # so the mutated grant block is what the machine parses).
        with self.assertRaises(ValueError) as caught:
            keyed_reserve(
                KeyedAdmissionState(), dispatch,
                authority_grants=grants, readback=readback,
                fact_readbacks=authority_fact_readbacks(groups=["validator/macos"]),
            )
        self.assertIn("AUTHORITY_NOT_APPLICABLE", str(caught.exception))
        # Durable fact content carries the wrong authority family for the role.
        with self.assertRaises(ValueError) as caught:
            keyed_reserve(
                KeyedAdmissionState(), dispatch,
                authority_grants=grants, readback=readback,
                fact_readbacks=authority_fact_readbacks(authority_family="TASK_PACK"),
            )
        self.assertIn("AUTHORITY_FAMILY_MISMATCH", str(caught.exception))
        # A grant drifting from the content-derived authorization projects nothing.
        drifting = {AUTHORITY_GRANT_RECORD_REF: self.validation_grant(groups=["validator/windows", "validator/linux", "validator/macos"])}
        with self.assertRaises(ValueError) as caught:
            keyed_reserve(
                KeyedAdmissionState(), dispatch,
                authority_grants=drifting, readback=readback,
                fact_readbacks=authority_fact_readbacks(),
            )
        self.assertIn("AUTHORITY_GRANT_DRIFT", str(caught.exception))
        drifting_family = {AUTHORITY_GRANT_RECORD_REF: self.validation_grant(authority_family="REVIEW_POLICY")}
        with self.assertRaises(ValueError) as caught:
            keyed_reserve(
                KeyedAdmissionState(), dispatch,
                authority_grants=drifting_family, readback=readback,
                fact_readbacks=authority_fact_readbacks(),
            )
            self.assertIn("AUTHORITY_GRANT_DRIFT", str(caught.exception))

    def test_r8_real_durable_fact_with_invented_groups_fails_closed(self) -> None:
        # Exact Fresh-Review-R7 P1-1 regression: the exact real durable ref
        # AUTHORITY_FACT_REF (#861@6043191203) exists, its VERBATIM canonical
        # content is supplied, and the digest binds exactly that content — but
        # the true content grants nothing: it carries no ai-dev:authority-grant
        # block and never mentions validator/windows or validator/linux. A
        # readback that decorates the real fact with invented trusted-looking
        # authorization fields (the R7 positive's manufacture pattern), and a
        # caller grant repeating the same invention, manufacture no authority:
        # the machine derives from the true content and fails closed.
        self.assertIn("V410_T06B_CONCERN_VALIDATION_R6=PASS", AUTHORITY_FACT_CONTENT)
        self.assertNotIn("validator/windows", AUTHORITY_FACT_CONTENT)
        self.assertNotIn("validator/linux", AUTHORITY_FACT_CONTENT)
        self.assertNotIn(AUTHORITY_GRANT_BLOCK_START, AUTHORITY_FACT_CONTENT)
        self.assertNotEqual(AUTHORITY_FACT_REF, AUTHORITY_GRANT_RECORD_REF)
        # Direct parser pin: the true content derives no grant at all.
        with self.assertRaises(ValueError) as caught:
            parse_authority_grant_block(AUTHORITY_FACT_CONTENT)
        self.assertIn("AUTHORITY_NOT_APPLICABLE", str(caught.exception))
        # End to end: real ref + real content + real digest, decorated with
        # the R7-style invented projections the machine must never trust.
        real_fact = {
            "ref": AUTHORITY_FACT_REF,
            "exists": True,
            "canonical_content": AUTHORITY_FACT_CONTENT,
            "content_digest": AUTHORITY_FACT_DIGEST,
            "authority_family": "VALIDATION",
            "repository": "kaicreator-mm/ai-development-standard",
            "task": "#861",
            "role": "validator",
            "groups": ["validator/windows", "validator/linux"],
        }
        grants = {AUTHORITY_FACT_REF: self.validation_grant(ref=AUTHORITY_FACT_REF)}
        dispatch = self._dispatch(
            dispatch_id="D-win",
            role="validator",
            execution_profile="LOCAL_VALIDATOR",
            compatibility_group="validator/windows",
            compatibility_authority_ref=AUTHORITY_FACT_REF,
        )
        with self.assertRaises(ValueError) as caught:
            keyed_reserve(
                KeyedAdmissionState(), dispatch,
                authority_grants=grants, readback=authority_readback(),
                fact_readbacks={AUTHORITY_FACT_REF: real_fact},
            )
        self.assertIn("AUTHORITY_NOT_APPLICABLE", str(caught.exception))

    def test_r8_content_digest_mismatch_fails_closed(self) -> None:
        # R8: the digest is RECOMPUTED from the supplied canonical content —
        # the R7 shape-only 64-hex check alone admitted any well-formed value.
        readback = authority_readback()
        grants = {AUTHORITY_GRANT_RECORD_REF: self.validation_grant()}
        dispatch = self._dispatch(
            dispatch_id="D-win",
            role="validator",
            execution_profile="LOCAL_VALIDATOR",
            compatibility_group="validator/windows",
            compatibility_authority_ref=AUTHORITY_GRANT_RECORD_REF,
        )
        # Shape-valid 64-hex digest that does not bind the supplied content.
        with self.assertRaises(ValueError) as caught:
            keyed_reserve(
                KeyedAdmissionState(), dispatch,
                authority_grants=grants, readback=readback,
                fact_readbacks=authority_fact_readbacks(content_digest="b" * 64),
            )
        self.assertIn("AUTHORITY_DIGEST_MISMATCH", str(caught.exception))
        # A digest of DIFFERENT content while claiming this content.
        other_digest = hashlib.sha256(b"unrelated durable fact content").hexdigest()
        with self.assertRaises(ValueError) as caught:
            keyed_reserve(
                KeyedAdmissionState(), dispatch,
                authority_grants=grants, readback=readback,
                fact_readbacks=authority_fact_readbacks(content_digest=other_digest),
            )
        self.assertIn("AUTHORITY_DIGEST_MISMATCH", str(caught.exception))
        # No canonical content at all: nothing to verify the binding against.
        with self.assertRaises(ValueError) as caught:
            keyed_reserve(
                KeyedAdmissionState(), dispatch,
                authority_grants=grants, readback=readback,
                fact_readbacks=authority_fact_readbacks(
                    canonical_content=None, content_digest=AUTHORITY_GRANT_RECORD_DIGEST,
                ),
            )
        self.assertIn("AUTHORITY_DIGEST_MISMATCH", str(caught.exception))
        # Sanity: the honest binding — digest recomputed from the exact
        # supplied content — is accepted; the gate is mechanical, not decor.
        verdict, _ = keyed_reserve(
            KeyedAdmissionState(), dispatch,
            authority_grants=grants, readback=readback,
            fact_readbacks=authority_fact_readbacks(
                canonical_content=AUTHORITY_GRANT_RECORD_CONTENT,
                content_digest=AUTHORITY_GRANT_RECORD_DIGEST,
            ),
        )
        self.assertEqual("ACCEPTED", verdict)

    def test_r8_malformed_or_missing_authorization_block_fails_closed(self) -> None:
        # R8: grants are DERIVED by deterministic parsing — canonical content
        # without a parsable ai-dev:authority-grant v1 block grants nothing,
        # whatever the caller grant claims.
        readback = authority_readback()
        grants = {AUTHORITY_GRANT_RECORD_REF: self.validation_grant()}
        dispatch = self._dispatch(
            dispatch_id="D-win",
            role="validator",
            execution_profile="LOCAL_VALIDATOR",
            compatibility_group="validator/windows",
            compatibility_authority_ref=AUTHORITY_GRANT_RECORD_REF,
        )
        mutated_content = [
            ("no block", "prose without any authorization block\n"),
            (
                "unterminated block",
                AUTHORITY_GRANT_BLOCK_START + "\nrole: validator\n",
            ),
            (
                "missing fields",
                AUTHORITY_GRANT_BLOCK_START + "\nrole: validator\n" + AUTHORITY_GRANT_BLOCK_END + "\n",
            ),
            (
                "unknown field",
                AUTHORITY_GRANT_BLOCK_START + "\n"
                "authority_family: VALIDATION\n"
                "repository: kaicreator-mm/ai-development-standard\n"
                "task: #861\n"
                "role: validator\n"
                "groups: validator/windows\n"
                "answer: 42\n" + AUTHORITY_GRANT_BLOCK_END + "\n",
            ),
            (
                "duplicate field",
                AUTHORITY_GRANT_BLOCK_START + "\n"
                "authority_family: VALIDATION\n"
                "repository: kaicreator-mm/ai-development-standard\n"
                "task: #861\n"
                "role: validator\n"
                "role: builder\n"
                "groups: validator/windows\n" + AUTHORITY_GRANT_BLOCK_END + "\n",
            ),
            (
                "empty groups",
                AUTHORITY_GRANT_BLOCK_START + "\n"
                "authority_family: VALIDATION\n"
                "repository: kaicreator-mm/ai-development-standard\n"
                "task: #861\n"
                "role: validator\n"
                "groups: , ,\n" + AUTHORITY_GRANT_BLOCK_END + "\n",
            ),
        ]
        for label, content in mutated_content:
            with self.subTest(case=label):
                with self.assertRaises(ValueError) as caught:
                    keyed_reserve(
                        KeyedAdmissionState(), dispatch,
                        authority_grants=grants, readback=readback,
                        fact_readbacks=authority_fact_readbacks(canonical_content=content),
                    )
                self.assertIn("AUTHORITY_NOT_APPLICABLE", str(caught.exception))
                with self.assertRaises(ValueError) as caught:
                    parse_authority_grant_block(content)
                self.assertIn("AUTHORITY_NOT_APPLICABLE", str(caught.exception))

    def test_r6_self_referencing_grant_ref_is_rejected(self) -> None:
        # A dispatch never authorizes itself: a grant whose durable ref points
        # back at the dispatch's own admission comment is self-reference.
        readback = authority_readback()
        grants = {"#861@6099999999": self.validation_grant(ref="#861@6099999999")}
        dispatch = self._dispatch(
            dispatch_id="D-win",
            role="validator",
            execution_profile="LOCAL_VALIDATOR",
            compatibility_group="validator/windows",
            compatibility_authority_ref="#861@6099999999",
            canonical_admission_ref="#861@6099999999",
        )
        with self.assertRaises(ValueError) as caught:
            keyed_reserve(KeyedAdmissionState(), dispatch, authority_grants=grants, readback=readback)
        self.assertIn("AUTHORITY_SELF_REFERENCE", str(caught.exception))

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
        # R7: the trusted fact readback faithfully materializes the real
        # durable fact — a Builder admission, TASK_PACK family — so the
        # mismatch is derived from the evidence itself, before any caller
        # grant is consulted.
        builder_facts = authority_fact_readbacks(
            ref=builder_ref,
            authority_family="TASK_PACK",
            role="builder",
        )
        with self.assertRaises(ValueError) as caught:
            keyed_reserve(
                KeyedAdmissionState(), unauthorized,
                authority_grants=builder_grants, readback=authority_readback(),
                fact_readbacks=builder_facts,
            )
        self.assertIn("AUTHORITY_FAMILY_MISMATCH", str(caught.exception))

    def test_c4_grant_applicability_is_tuple_exact(self) -> None:
        grants = {AUTHORITY_GRANT_RECORD_REF: self.validation_grant()}
        readback = authority_readback()
        facts = authority_fact_readbacks()
        other_repo = self._dispatch(
            dispatch_id="D-other-repo",
            role="validator",
            execution_profile="LOCAL_VALIDATOR",
            compatibility_group="validator/windows",
            compatibility_authority_ref=AUTHORITY_GRANT_RECORD_REF,
            repository="other/repo",
        )
        with self.assertRaises(ValueError) as caught:
            keyed_reserve(
                KeyedAdmissionState(), other_repo,
                authority_grants=grants, readback=readback, fact_readbacks=facts,
            )
        self.assertIn("AUTHORITY_NOT_APPLICABLE", str(caught.exception))
        other_group = self._dispatch(
            dispatch_id="D-other-group",
            role="validator",
            execution_profile="LOCAL_VALIDATOR",
            compatibility_group="validator/macos",
            compatibility_authority_ref=AUTHORITY_GRANT_RECORD_REF,
        )
        with self.assertRaises(ValueError) as caught:
            keyed_reserve(
                KeyedAdmissionState(), other_group,
                authority_grants=grants, readback=readback, fact_readbacks=facts,
            )
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
