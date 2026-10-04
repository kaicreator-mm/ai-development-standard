# T-011 Task Pack — Heterogeneous Multi-Agent / Resource / Transport Dogfood

Status: **FINAL TASK PACK — JIT EXECUTION PACK REQUIRED**

Authority: Frozen Product blob `f26439580e00de6ed8b2e27d732a3095eb566219`; Frozen L2 blob `f88c85454e80101a0fdf56050e21f11a05279841`; Frozen Task DAG R2 commit `d2f18854043c59712c1c9d2518f45843b0ad129c` / blob `21d45c8d1a4ec94621eb8ca6051f21ece8227fdc`; native Issue Dependencies on #517 read back with `blocked_by=0,total_blocked_by=4`; Issue #517.

```yaml
task_id: T-011
lane: orchestration-dogfood
dependencies: [T-007, T-008, T-009, T-017]
integration_target: version/v4.8.0
review_policy: required
validation_scope: exact-subject-scenario-integration
validation_owner: independent-from-builder
l3_requirement: risk-scaled-required
evidence_matrix: required
agent_freedom_ceiling: F2_ENGINEERING_DISCRETION
jit_branch: true
execution_pack: JIT
```

## Scope

T-011 owns the Frozen Product heterogeneous orchestration dogfood only. It must attempt to falsify the already implemented v4.8 semantics across one bounded scenario corpus containing:

- multiple simultaneously READY work items;
- materially different logical Agent profiles;
- fresh and stale/missing Availability facts;
- scarce shared-resource contention including exclusive/capacity-N behavior;
- duplicate/incompatible assignment races;
- reviewer/validator independence conflicts;
- transport duplicate/replay/loss and conflicting replay;
- crash/restart reconstruction from durable facts only;
- T-017 accepted-Claim Start Record / active-ownership visibility / fail-closed timeout or replacement behavior;
- bounded executor success only when hard eligibility permits it;
- escalation when semantic ambiguity or missing authority makes bounded execution unsafe.

Dogfood may falsify Frozen semantics. It MUST NOT silently repair or expand Product/L2/DAG semantics, invent a new scheduler/admission lifecycle, introduce a new Exchange family, convert derived Availability into authority, weaken independence/currentness/security filters, or claim economic savings/universal model ranking.

## Evidence classification

Every scenario result MUST declare one of:

```text
SYNTHETIC_DETERMINISTIC
REPOSITORY_REAL_EXECUTION
REAL_HOST_OR_RUNTIME_VALIDATION
NOT_RUN
BLOCKED
```

Synthetic/reference-model evidence proves only the bounded deterministic semantics exercised by that harness. It must never be relabeled as real host/device/provider/runtime evidence.

Any claim about an external host, device, provider, model runtime, queue, webhook, scheduler service or other non-repository execution environment requires an independent exact-subject Validation record from that environment. If unavailable, preserve `NOT_RUN` or `BLOCKED`; do not infer PASS.

## Builder write set

The JIT Execution Pack may narrow but MUST NOT broaden this Task Pack. Authorized implementation/dogfood paths are:

- `docs/implementation/4.8.0/dogfood/orchestration/**`
- `scripts/test_v48_orchestration_dogfood.py`

Read-only authority/reference inputs include Product/L2/DAG, the T-007/T-008/T-009/T-017 task evidence and tests, `standards/EXECUTION_ARCHITECTURE_STANDARD.md`, `standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md`, v4.0 Interchange authority, current schemas, and existing v4.8 conformance scripts.

Normative standards, schemas, Frozen Product/L2/DAG, Task Packs for completed upstream Tasks, CI/workflows and release/version-closure authority are **not** in the Builder write set.

If the scenario corpus can pass only by changing normative semantics or public machine contracts, stop with `ARCHITECTURE_AMENDMENT_REQUIRED`; T-011 must not absorb the repair.

## Required scenario/evidence matrix

At minimum the Builder must materialize a durable matrix covering these dimensions:

| ID | Scenario | Required oracle | Minimum evidence posture |
|---|---|---|---|
| ODF-01 | multiple READY items + heterogeneous Agent profiles | only hard-eligible candidates reach ranking/admission | synthetic deterministic + repository real execution |
| ODF-02 | fresh vs stale/missing Availability | stale/missing hard requirement => UNKNOWN/ineligible; no ranking override | synthetic deterministic |
| ODF-03 | capacity-N and N=1 contention | active accepted bindings never exceed capacity; loser fails closed | synthetic deterministic + repository real execution |
| ODF-04 | duplicate/incompatible assignment race | one canonical accepted work/resource admission only | synthetic deterministic + repository real execution |
| ODF-05 | reviewer/validator independence conflict | conflicted candidate rejected before optimization | synthetic deterministic |
| ODF-06 | duplicate/replay same identity+payload | replay is idempotent and does not duplicate authority | synthetic deterministic |
| ODF-07 | same replay identity + conflicting payload/digest | fail closed; do not accept latest | synthetic deterministic |
| ODF-08 | transport loss / delayed ACK | delivery/ACK/progress cannot become workflow truth | synthetic deterministic |
| ODF-09 | crash/restart reconstruction | authoritative current state reconstructs from durable facts without transient queue/chat | repository real execution |
| ODF-10 | T-017 start/ownership/replacement | accepted Claim is Start Record; projection is non-authoritative; ambiguous replacement blocked | repository real execution |
| ODF-11 | bounded executor is eligible | bounded path may complete only within exact pack/write-set/authority constraints | repository real execution; provider claim only if separately validated |
| ODF-12 | semantic ambiguity or missing authority | bounded executor escalates/stops rather than guessing or self-elevating | repository real execution |
| ODF-13 | current Task/base drift | stale Task/Execution Pack/base cannot continue as current | synthetic deterministic |
| ODF-14 | unsupported economic/model inference | measured fields remain descriptive; no universal ranking/savings claim | document/oracle inspection |

## Required gates

Before Builder dispatch:

1. `version/v4.8.0` must still equal the exact JIT base bound by the Execution Pack;
2. native dependencies for #517 must remain `blocked_by=0` with canonical total four blockers T-007/#513, T-008/#514, T-009/#515 and T-017/#646 all DONE;
3. this Task Pack and `L3_T11_ORCHESTRATION_DOGFOOD.md` must be pinned by blob;
4. `.agent/execution/T-011/**` must bind base SHA/tree, pack refs, Builder write set, test/failure matrices and independent Validation/Review posture;
5. no implementation path may be modified by the planning/JIT phase.

Builder closeout must bind exact base, Pack HEAD/tree, candidate HEAD/tree and exact write-set diff. It must distinguish synthetic, repository-real and external-real evidence and explicitly state which real-host/provider/runtime dimensions are `NOT_RUN/BLOCKED`.

Required Validation is independent exact-subject scenario/integration Validation. Fresh Independent Review occurs only after qualifying Validation and must re-read the exact current candidate. Builder, Validator and Reviewer identities remain distinct.

PR/Task PASS does not imply T-014, Version Closure, Release Qualification or Release PASS.
