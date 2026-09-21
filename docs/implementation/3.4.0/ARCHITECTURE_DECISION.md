# v3.4 Architecture Decision — Authority Convergence (T-001)

Status: FROZEN (version planning checkpoint)
Version: 3.4.0
Baseline: `main@1ce6497402c6e1b54b07cc3bc8f8a46444d1af32` (immutable v3.3.0)
Inputs: #45 (Task/Execution Pack + dual-agent pull orchestration), #46 (version-scoped Validation Handoff Queue)

This document freezes the single v3.4 architecture that absorbs #45 and #46. It is subordinate to the v3.3 standard authorities it extends and introduces no parallel scheduler, lifecycle, state authority or validation truth model.

## 1. One execution architecture, not two queues

#45 and #46 converge into one dispatch architecture. There are no independent Builder/Validator/Reviewer queue state machines. The canonical model is:

```text
Canonical Task / Execution State
        ↓
Canonical Dispatch (role + execution profile)
        ↓
Derived ready-set projections
  BuilderReadySet / ValidatorReadySet / ReviewerReadySet
```

A dispatch carries `dispatch.role = builder | validator | reviewer` plus an execution profile. Ready sets and the version-scoped Validation Handoff Queue are derived projections of canonical dispatch/gate facts — never a second workflow authority.

## 2. Canonical objects

### 2.1 Task Pack — durable planning authority

Answers: *what must this Task achieve?* Contains task identity, dependencies, allowed write set, forbidden scope, acceptance criteria, required gates, validation ownership, review policy, L3 requirement, merge target. Representation: `docs/implementation/<version>/TASK_PACKS.json` + `task-packs/Txxx_<name>.md`. A Task Pack MUST NOT contain exact-base-dependent implementation assumptions.

### 2.2 Execution Pack — JIT, exact-base-bound execution authority

Answers: *how can an authorized executor safely implement this Task on this exact repository baseline?* Generated just-in-time after dependencies merge, bound to the exact integration base SHA, subordinate to the Task Pack. Location: `.agent/execution/<task-id>/`. Required core: `MANIFEST.yaml`, `EXECUTION_CONTRACT.md`, `TEST_MATRIX.yaml`, `FAILURE_MATRIX.yaml`, `IMPLEMENTATION_MAP.md`, `REVIEW_CHECKLIST.md`. Optional: interface/semantic-kernel seeds, reference patch, local agent prompt, reference fixtures. Empty placeholder artifacts MUST NOT be required.

### 2.3 Dispatch — the executable handoff

Identifies: dispatch_id, repository, version, task, parent Issue, PR when applicable, role, execution profile, branch, expected base SHA, requested HEAD SHA when applicable, Task Pack identity, Execution Pack identity when applicable, validation profile, pinned standard revision, operator freedom.

Canonical execution profiles:

```text
LOCAL_BUILDER
LOCAL_VALIDATOR
WEB_REVIEWER
PLATFORM_VALIDATOR
CLOSURE_VALIDATOR
```

Profiles configure execution authority; they do not introduce separate lifecycle models.

### 2.4 Validation Handoff Queue — version-scoped projection

The #46 queue becomes a version-scoped projection/index of Validator dispatches (`[Validation Handoff] <version> ... exact-SHA Build Host validation queue`). It provides a stable Local Validator entrypoint, READY/HOLD discovery, exact-SHA identity, provenance, restart/recovery surface and pointer-only invocation. The queue Issue is not validation authority, not Task authority and not an independent workflow state machine. Canonical truth remains the parent Task/PR + canonical events/evidence.

## 3. Authority hierarchy

```text
Frozen Product Authority
> Frozen Architecture Authority
> Task DAG
> Task Pack
> Execution Contract
> Semantic / Interface Seed
> Agent implementation choice
```

An Execution Pack MAY narrow execution freedom. It MUST NOT redefine PRD, Architecture, Task scope, public contract, required invariant, validation ownership or review requirement. Contradictions route upward as explicit failures: `TASK_PACK_DEFECT`, `ARCHITECTURE_CONTRADICTION`, `EXECUTION_PACK_INVALID`. A lower-cost Local Agent MUST NOT silently resolve these by redesigning the system.

## 4. JIT execution lifecycle

Queued Tasks do not receive long-lived implementation branches before dependencies complete:

```text
Task Pack frozen
→ WAITING_DEPENDENCY
→ dependencies merged
→ recompute ready set
→ read current integration exact SHA
→ create task branch JIT
→ create/bind Execution Pack
→ emit Builder dispatch
→ READY
```

Exceptions only when a real stacked-code dependency requires an earlier branch.

## 5. Execution Pack staleness (fail closed)

Verified at claim time against: pack base SHA vs current integration SHA, Task Pack identity, dependency completion identities, pinned standard revision, branch identity.

```text
PACK_CURRENT           execution may proceed
PACK_STALE_NONMATERIAL only an explicitly authorized impact/rebind action may continue;
                       original base identity remains historical evidence
PACK_STALE_MATERIAL    regenerate affected pack material before execution
PACK_INVALID           fail closed
```

The executor MUST NOT silently rewrite `base_sha`.

## 6. Agent freedom contract

```text
F0_MECHANICAL            repository wiring, imports, fixtures, exact contract implementation,
                         non-semantic compile/type/lint repair; no design discretion
F1_BOUNDED_IMPLEMENTATION public contracts/invariants/test oracle fixed; internal implementation may vary
F2_ENGINEERING_DISCRETION low-risk internal engineering choices inside frozen scope
F3_ARCHITECTURE_REQUIRED  must return to Strong Model / architecture authority
```

An executor MUST NOT self-promote F0/F1/F2 work into F3 authority. Machine-readable via `agent_freedom` on Task Contract / Dispatch / Execution Pack manifest.

## 7. Unified state dimensions (unchanged separation)

Workflow state, dispatch state (pull vocabulary: `READY / CLAIMED / RUNNING / COMPLETED / BLOCKED / SUPERSEDED`, mapping onto the v3.3 lifecycle vocabulary), validation gate state (`PASS / FAIL / BLOCKED / NOT_RUN / NOT_APPLICABLE`), provider state (`AVAILABLE / INFRA_BLOCKED / TIMED_OUT / CANCELLED`) remain separate dimensions and MUST NOT be collapsed into one overloaded `status`. Queue-item status (`READY / HOLD / RUNNING / PASS / FAIL / BLOCKED / SUPERSEDED`) is derived only.

## 8. Exact-SHA validation rule

Before Validator execution: `requested_head_sha == current PR HEAD`, else `HEAD_DRIFT` → dispatch stale/superseded, no execution as PASS evidence. A new candidate requires a new dispatch identity. PASS remains attached to tested SHA × environment × validation profile × commands and MUST NOT be rewritten onto a successor SHA.

## 9. Role authority boundaries

- **Builder** (LOCAL_BUILDER / Web builder): implements, validates locally, publishes stable exact HEAD + evidence, requests Independent Review when required; MUST NOT self-assert Independent Review PASS.
- **Validator** (LOCAL_VALIDATOR / PLATFORM_VALIDATOR / CLOSURE_VALIDATOR): clean checkout, verify exact SHA + current PR HEAD/base, execute declared profile, capture environment + commands + exit codes, publish exact-SHA evidence; MUST NOT modify product source, repair defects, redesign, weaken tests, change Frozen Authority, merge, close implementation Issues, or validate an undispatched replacement SHA. Real defect → `FAIL`; environment inability → `BLOCKED`.
- **Reviewer** (WEB_REVIEWER): pointer-driven from GitHub facts; re-reads current PR exact HEAD/base, verifies evidence SHA identity, classifies P0–P3; results: `REVIEW_PASS / CHANGES_REQUESTED / VALIDATION_REQUESTED / BLOCKED`; MUST NOT modify product code in the same review role/session.

## 10. Model preparation split

High-risk semantic concerns allow Web/Strong preparation of a compact Semantic Kernel (domain/public contracts, identity/digest rules, state-transition predicates, authority boundaries, binding/pinning rules, fail-closed validators, ordering/concurrency invariants, critical ports, negative test oracle). Local agents own repository integration, adapters, fixtures, workspace wiring, compile/type/lint repair, packaging, platform integration, real-host execution. This extends the existing Model Usage Policy; no second model-routing standard.

## 11. Non-goals carried from the version contract

No centralized scheduler requirement; no separate role state machines; no universal Build Host validation; no CI-as-debug-loop; no universal Independent Review; no Local Agent architecture redesign by default; no weakened exact-SHA evidence; no PASS reuse across SHA changes; no Validator opportunistic repair; no Execution Pack as second Product/Architecture authority; no Task Pack duplication inside Issue bodies; no mandatory large packs for trivial tasks (Fast Path preserved).
