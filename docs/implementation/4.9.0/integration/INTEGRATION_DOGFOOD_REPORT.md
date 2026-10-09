# v4.9 T-015 — Integrated Dogfood Report

Record: `INTEGRATED_DOGFOOD_RECORD_V1` · Issue: kaicreator-mm/ai-development-standard#734 · Parent controller: #745 · Branch: `task/v4.9.0-t15-integrated-dogfood`.

Status: **Builder-produced integrated dogfood EVIDENCE only.** This report is not independent
Validation, not Fresh Review, not a gate, and never a Version Closure or Release Qualification
verdict. Per immutable DAG v0.1 `### T-015` (blob `4f358ba2b32e01ae17ddcdf970151cf28e44bb3f`)
and the T-014 downstream contract (`references/DOWNSSTREAM_DOGFOOD_AUDIT_CONTRACT_V49.md`), it
produces handoff evidence with bounded claims; real external/downstream inability is recorded
`NOT_RUN`/`BLOCKED`, never a guessed green result. Deterministic oracles:
`scripts/test_v49_integrated_dogfood.py` (I01–I06).

## 1. Exact bindings and currentness

- Bound ADS candidate: `candidate:v4.9.0@sha:a4f1debe663813712d4f740ec70c14ca6342b0ac`
  (tree `76e18763c525e357a14e2d21036e597b07151a91`), admitted execution pack head
  `046710a2d8ac55ec3e2e517cc447d7b1accc31f0` (the candidate commit's parent).
- Dispatch: #734@6009462073 (JIT admission). Builder claim: #734@6009482508. Scope:
  IMPLEMENTATION_ONLY; independence from Controller and all prior Builders/Validators/Reviewers.
- Currentness was recomputed by this lane immediately before mutation: `origin/version/v4.9.0`
  resolved to exactly `a4f1debe663813712d4f740ec70c14ca6342b0ac` and the worktree was clean at
  the pack head. The predecessor lineage posture below is this lane's OWN recompute at the
  candidate (`LG_SEQ_FULL` posture verified here), not an inherited verdict.

## 2. Predecessor-lineage exact identity check (oracle I01)

Method: the kernel asserts, at the candidate HEAD, (a) the full integrated lineage ancestry
chain (T-011 merge `d53e943e`, T-012 merge `4322a8cc`, T-014 merge `2484d8df`, recovery
compositions `56137d88` + `4c632256`, post-recovery recompose `c1d7c96d` + `e3a2cc03`,
T-013 rebind `9aa51a7f`, base `a4f1debe`, pack head `046710a2`); (b) exact blob identity pins
for every merged task output and recovered family surface; (c) the frozen authority blobs.

| Surface family | Binding | Result |
|---|---|---|
| Frozen Product (PRD §1–§23, blob `a8ec7030…`) | exact blob at HEAD | identity holds |
| Frozen L2 (blob `bd41ea01…`) | exact blob at HEAD | identity holds |
| Frozen Task DAG v0.2 (blob `b9fe0cc7…`) | exact blob at HEAD | identity holds |
| Immutable DAG v0.1 `### T-015` (blob `4f358ba2…`) | exact blob + acceptance anchors at HEAD | identity holds |
| T-002 (#721) assurance plan v2 | 5 outputs, exact blobs | identity holds |
| T-003 (#722) authority/state registry | 4 outputs, exact blobs | identity holds |
| T-004 (#723) role execution profile v1 | 16 outputs, exact blobs | identity holds |
| T-005 (#724) release applicability | 3 outputs, exact blobs | identity holds |
| T-006 (#725) task learning v2 | 4 outputs, exact blobs | identity holds |
| T-007 (#726) §29 proportional orchestration core | 11 outputs, exact blobs | identity holds |
| T-008 (#727) execution contract refs | 4 outputs, exact blobs | identity holds |
| T-009 (#728) JIT DAG mutation governance | 6 outputs, exact blobs | identity holds |
| T-010 (#729) gate evidence currentness matrix | 10 outputs, exact blobs | identity holds |
| T-011 (#730) registry/manifest/adoption wiring | 5 outputs, exact blobs | identity holds |
| T-012 (#731) conformance suite | 14 outputs, exact blobs | identity holds |
| T-013 (#732) manual / GitHub-native reference flow | 6 outputs, exact blobs | identity holds |
| T-014 (#733) downstream dogfood / auditor contract | 6 outputs, exact blobs | identity holds |
| Recovered v4.4–v4.7 families (97 surfaces) | byte-identical since recovery composition `4c632256` | identity holds |
| Recompose-shared surfaces (8: CHANGELOG/README/VERSION, dispatch schema, v4.8 integration-closure + registry-adoption kernels, standard manifest, golden coverage) | exact current composed blobs; composed-union provenance documented | identity holds |
| `.agent/execution/T-015/**` planning files (6) | unmutated since pack head | identity holds |

Total pinned surfaces: 94 merged v4.9 task outputs + 105 recovered/composed family surfaces +
6 planning files. No stale predecessor or evidence binding is laundered: every binding above is
recomputed from the candidate's own git object database each run; no predecessor gate or
validation verdict is restated as this lane's result.

## 3. Representative orchestration journeys (oracle I02)

All journeys execute deterministically through the merged T-007 §29 owner kernel
(`test_v49_execution_core.py`, imported — never redefined) over its frozen fixtures, plus the
T-012 conformance surface executed green in the same run.

| Journey | PRD §15 scenario | T-007 §29 binding | Expected = observed outcome |
|---|---|---|---|
| J-POS-01 dispatch → claim → merge | baseline legal path | §29.1/§11 (K01) | `MATERIALIZED` → `ACCEPTED` → `MERGE_READY`; in-envelope JIT phase `READY` |
| J-NEG-01 duplicate claim race | F | §29.6/§11 (K07/K09) | exactly one canonical claim; every ordering replays deterministically |
| J-NEG-02 wrong-role / independence | G | §29.4/§27.2 (K04/K09) | `INELIGIBLE` before ranking; ranking inputs cannot rescue |
| J-NEG-03 known sequence block | K | §29.3 (K03/K09) | `WAITING_LINEAGE_NO_DISPATCH`, 0 dispatches; claim `NOT_DISPATCHABLE_WAITING_LINEAGE`; no workflow state, no gate verdict |
| J-NEG-04 out-of-envelope / topology | L | §29.2 (K02/K09) | undeclared/violated phase `BLOCKED`; topology routes `V43_MUTATION_*` |
| J-NEG-05 ambiguous reduction predicate | M | §29.1/§29.4 (K01/K09) | unproven predicate → `STRONGER_EXISTING_PATH_OR_BLOCKED`; proven → `REDUCED_PER_OWNER_RULE` |
| J-NEG-06 adverse finding shopping | N | §29.5 (K05/K09) | `REJECTED_REVIEW_SHOPPING`; R2 chronology cannot close F-101; unresolved blocker blocks merge |
| J-NEG-07 stale binding / stale PASS | I | §29.1/§10 (K01/K10) | `BLOCKED_PLAN_BINDING_STALE` / `STALE_PLAN_BINDING_RECOMPUTE` / `PLAN_BINDING_STALE`; stale PASS `REJECTED_HISTORICAL_ONLY_NO_TRANSFER_RULE` |

Integrated surface execution at the candidate:

- T-012 conformance surface C01–C12: executed green in this run (13 tests, in-process, same
  interpreter); the coverage manifest binds all twelve coverage items.
- Extended integrated regression: 51 recovered and lane kernels re-executed green at the
  candidate (`test_v44_*` ×8, `test_v45_*` ×9, `test_v46_*` ×8, `test_v47_*` ×13, `test_v48_*`
  ×11, `test_v49_manual_reference_flow.py`, `test_v49_dogfood_audit_contract.py`) — the
  recovered v4.4–v4.7 families plus the v4.8 integration-closure, T-013 and T-014 kernels.
- Pinned CI battery: 37 commands executed individually, all exit 0 (see §4).

Scope: these are in-repo kernel/conformance/regression executions only. They are integration
and compatibility evidence; they are NOT a downstream run and can never substitute for one
(T-014 contract §14: synthetic, compatibility-only, or no-op runs cannot substitute for a
qualifying run).

## 4. Reconciliation of normative docs / contracts / tests / registry (oracle I03)

- Pinned battery: `.github/workflows/verify-standard.yml` defines exactly 37 `python scripts/…`
  commands; every command file exists at the candidate; all 37 were executed individually by
  the Builder at the candidate and exited 0.
- Manifest agreement: `standard-manifest.json` declares the integrated normative surfaces
  (execution architecture, assurance plan, release, task learning standards; the v4.9 schemas
  `assurance-plan-v2`, `role-execution-profile-v1`, `task-learning-v2`, `dispatch`; the state
  registry). Manifest-declared files all exist; no duplicate declarations.
- Registry agreement: `registries/state-dimensions-v1.json` binds `waiting_lineage` to its
  canonical owner `standards/EXECUTION_ARCHITECTURE_STANDARD.md` with posture `OWNER_DEFINED`,
  and carries the forbidden inferences F11 and F13–F19 (currentness never mints PASS/READY;
  wait posture never becomes a gate verdict).
- Contract agreement: every consumed authority ref of the T-014 downstream contract (its
  fixture-pinned owner list) resolves at the candidate (path + GitHub anchor); T-010 row M10
  binding refs resolve; T-007 consumed-contract section anchors resolve.
- Task surface agreement: 15 Task Packs exist under `docs/implementation/4.9.0/task-packs/`;
  Frozen DAG v0.2 declares `T-015: deps=[T-011, T-012, T-013, T-014]`; the materialization map
  lists T-001…T-015; the golden coverage template lists the integrated standards.
- Reconciliation observation (open, routed — not repaired in this lane): the manifest's
  verification section does not declare seven late-lane surfaces (`test_v43_conformance_dogfood.py`,
  `test_v48_integration_closure.py`, `test_v49_conformance_suite.py`,
  `test_v49_dogfood_audit_contract.py`, `test_v49_manual_reference_flow.py`,
  `references/MANUAL_REFERENCE_FLOW_V49.md`, `references/DOWNSSTREAM_DOGFOOD_AUDIT_CONTRACT_V49.md`).
  They are executed via the pinned battery / required Builder checks and are pinned exactly by
  the kernel (`UNDECLARED_LATE_LANE_SURFACES`), so any drift is caught; declarative registration
  is owned by the T-011 registry-adoption owner in later maintenance
  (`standard-manifest.json` is outside the T-015 write set).

## 5. Qualifying downstream dogfood: NOT_RUN (missing capability)

Per PRD §16 and the T-014 contract, a qualifying downstream dogfood requires a distinct
product/repository (never ADS itself or a synthetic mirror) with its own durably inspectable
pinned authority artifacts, a legal baseline vs selected proportional workflow with a
decision-value account, exact-candidate binding, an exercised ambiguous-predicate case, an
independent safety audit by an executor that is not the orchestrating/Builder principal, and
manual/GitHub-native viability of at least one qualifying run.

This lane truthfully records the qualifying downstream dogfood as `NOT_RUN`. The exact missing
capabilities, none of which this Builder holds or may self-authorize:

1. No authorized downstream execution container: a Builder implementation lane in the ADS
   repository holds no execution authorization over a distinct downstream product repository,
   and no qualifying downstream project run was dispatched/authorized for T-015.
2. No engaged distinct downstream repository with its own pinned Product/Architecture/Task/
   Review/Validation/Release authority baseline durably inspectable for this run.
3. No measured baseline-vs-selected proportional decision evidence (PRD §16.4/§16.6) from an
   actual downstream execution.
4. No independent safety-auditor session: PRD §16.7 requires an executor that is not the
   orchestrating or Builder principal of the tested decisions; self-attestation is insufficient,
   and the independent audit is later-gate/lane work, not this Builder's.

Consequently the downstream ambiguous-predicate exercise (PRD §16.5 / T-014 §5) is `NOT_RUN`
as well: the kernel-level fail-closed journeys in §3 exercise the owner semantics, but they are
in-repo conformance, not the required downstream exercise, and are never laundered into one.
For the same reason manual/GitHub-native downstream viability is `NOT_EXERCISED` (the in-repo
kernels run by ordinary scripted invocation only; no downstream manual viability was performed).

Per T-014 §14 and DAG v0.1 `### T-015` acceptance: any required exercise honestly `NOT_RUN`/
`BLOCKED` keeps the record consumable as evidence, and downstream generality is
`NOT_SATISFIED` with the explicit reason `QUALIFYING_DOWNSTREAM_RUN_NOT_RUN`.

## 6. Safety-negative account

In-repo deterministic journeys (the only runs used as evidence in this report): zero
safety-negative events. Each counter is bound to an executable owner-kernel guard re-asserted
in the same run (oracle I05):

| Counter | Kernel guard demonstrated |
|---|---|
| `UNAUTHORIZED_GATE_OMISSION` = 0 | undeclared/out-of-envelope JIT phase is `BLOCKED`; transitions consume plan currentness (§29.1/§29.2) |
| `STALE_PASS_TRANSFER` = 0 | stale binding rejected at Dispatch/Claim/merge; stale PASS never transfers (K01/K10) |
| `INDEPENDENCE_LOSS` = 0 | independence-failed candidate `INELIGIBLE` before ranking (§29.4/§27.2) |
| `CROSS_OWNER_REQUIREMENT_CANCELLATION` = 0 | unproven reduction predicate fails closed; conjunctive floors hold (§29.1, ASSURANCE §9/§10 via C01/C02) |
| `ADVERSE_TERMINAL_SUPPRESSION` = 0 | unresolved adverse finding survives chronology and blocks merge; re-review shopping rejected (§29.5) |

The independent safety AUDIT required by PRD §16.7 for downstream generality evidence is
`NOT_RUN` (missing capability §5.4). The in-repo zero counters above are journey-event
accounting for in-repo runs only; they are not a downstream audit and never support a
downstream generality claim.

## 7. Claim boundary and generality posture

- Exercised here: the merged v4.9 owner semantics at kernel/conformance level, the integrated
  regression of all merged lanes, predecessor-lineage identity, and cross-surface reconciliation
  — all bound to `candidate:v4.9.0@sha:a4f1debe663813712d4f740ec70c14ca6342b0ac`.
- Exercised in-repo mechanism matrix (scope `IN_REPO_KERNEL_AND_CONFORMANCE_SURFACES_ONLY`):
  all seven PRD §16.5 families have kernel/conformance-level exercise with proof refs; this
  matrix never supports downstream generality for any mechanism.
- Not exercised: the qualifying downstream dogfood path, the downstream ambiguous-predicate
  exercise, the independent safety audit, downstream manual/GitHub-native viability.
- Downstream generality: `NOT_SATISFIED` (`QUALIFYING_DOWNSTREAM_RUN_NOT_RUN`). No generality,
  closure, or release claim of any kind is made or implied by this report. Version Closure and
  Release Qualification verdict authority remains exclusively with the later gates.

## 8. Machine record

```text
INTEGRATED_DOGFOOD_RECORD_V1
record_id: V49-T015-INTEGRATED-DOGFOOD-001
bound_ads_candidate: candidate:v4.9.0@sha:a4f1debe663813712d4f740ec70c14ca6342b0ac
base_tree: 76e18763c525e357a14e2d21036e597b07151a91
execution_pack_head: 046710a2d8ac55ec3e2e517cc447d7b1accc31f0
lineage_recompute: SELF_RECOMPUTED_AT_CANDIDATE
inrepo_kernel_conformance_mechanism_matrix:
  - mechanism: OWNER_PERMITTED_REDUCTION
    state: EXERCISED
    proof_refs: standards/EXECUTION_ARCHITECTURE_STANDARD.md#29-v49-proportional-orchestration-core, scripts/test_v49_execution_core.py, scripts/test_v49_conformance_suite.py
  - mechanism: CROSS_OWNER_FLOOR_COMPOSITION
    state: EXERCISED
    proof_refs: standards/ASSURANCE_PLAN_STANDARD.md, scripts/test_v49_conformance_suite.py, scripts/test_v49_execution_core.py
  - mechanism: SAME_CONTAINER_PHASE_COALESCING
    state: EXERCISED
    proof_refs: docs/implementation/4.9.0/PRD.md#e-same-durable-container-multiple-independent-phases, scripts/test_v49_execution_core.py
  - mechanism: GATE_OWNED_EVIDENCE_TRANSFER
    state: EXERCISED
    proof_refs: references/GATE_EVIDENCE_CURRENTNESS_MATRIX.md, scripts/test_v49_gate_currentness.py, scripts/test_v49_conformance_suite.py
  - mechanism: FAIL_CLOSED_UNKNOWN_AMBIGUOUS_PREDICATE
    state: EXERCISED
    proof_refs: scripts/test_v49_dogfood_audit_contract.py, fixtures/dogfood-audit-contract/fail_closed.json, scripts/test_v49_execution_core.py
  - mechanism: NON_DISPATCH_WAIT
    state: EXERCISED
    proof_refs: registries/state-dimensions-v1.json, scripts/test_v49_execution_core.py, scripts/test_v49_conformance_suite.py
  - mechanism: PROSPECTIVE_RELEASE_APPLICABILITY_SELECTION
    state: EXERCISED
    proof_refs: standards/RELEASE_STANDARD.md#11-release-applicability-by-gate--subject, scripts/test_v49_release_applicability.py, scripts/test_v49_conformance_suite.py
matrix_scope: IN_REPO_KERNEL_AND_CONFORMANCE_SURFACES_ONLY
qualifying_downstream_dogfood:
  - state: NOT_RUN
    reason_ref: #5-qualifying-downstream-dogfood-not_run-missing-capability
ambiguous_predicate_exercise_downstream:
  - state: NOT_RUN
    reason_ref: #5-qualifying-downstream-dogfood-not_run-missing-capability
independent_safety_audit:
  - state: NOT_RUN
    reason_ref: #6-safety-negative-account
manual_github_native_viability:
  - state: NOT_EXERCISED
    claim_boundary: No qualifying downstream run was executed; the in-repo kernels run by ordinary scripted invocation only; no downstream manual or GitHub-native viability is demonstrated and none may be claimed.
inrepo_journey_safety_negatives:
  - UNAUTHORIZED_GATE_OMISSION: 0
  - STALE_PASS_TRANSFER: 0
  - INDEPENDENCE_LOSS: 0
  - CROSS_OWNER_REQUIREMENT_CANCELLATION: 0
  - ADVERSE_TERMINAL_SUPPRESSION: 0
negative_scope: IN_REPO_DETERMINISTIC_JOURNEYS_ONLY_NOT_A_DOWNSTREAM_AUDIT
downstream_generality: NOT_SATISFIED
generality_reason: QUALIFYING_DOWNSTREAM_RUN_NOT_RUN
authorizes_execution: false
authorizes_release_qualification: false
```

## 9. Evidence refs

- Kernel (deterministic oracles I01–I06): `scripts/test_v49_integrated_dogfood.py`
- T-007 owner kernel: `scripts/test_v49_execution_core.py` over `fixtures/execution-core-v49/`
- T-012 conformance surface: `scripts/test_v49_conformance_suite.py` over `fixtures/conformance-suite/`
- T-014 downstream contract: `references/DOWNSSTREAM_DOGFOOD_AUDIT_CONTRACT_V49.md`
- T-010 gate matrix: `references/GATE_EVIDENCE_CURRENTNESS_MATRIX.md`
- Pinned battery: `.github/workflows/verify-standard.yml` (37 commands)
- Dispatch #734@6009462073; Builder claim #734@6009482508; parent controller #745
