# Execution Pack Standard

## 1. Purpose and authority boundary

This standard owns the Task Pack and Execution Pack object model: their separate authority and lifecycle, just-in-time generation, exact-base binding, staleness classification, agent freedom contract, semantic/interface seed semantics, retention and package exclusion.

It extends — and does not replace — the v3.3 execution/event/reducer/handoff architecture:

- `EXECUTION_ARCHITECTURE_STANDARD.md` owns durable facts, derived state, ready queues, dispatch lifecycle and controllers;
- `GITHUB_AGENT_INTERACTION_PROTOCOL.md` owns structured Agent events, intent admission and operator attribution;
- `LOCAL_AGENT_HANDOFF_PROTOCOL.md` owns Local Agent handoff execution discipline;
- `VALIDATION_STANDARD.md` owns Gate states, Validation Tuples and evidence meaning;
- `MODEL_USAGE_POLICY.md` owns model/strength routing.

If this document conflicts with Frozen Product/Architecture authority or a higher-authority source, the normal Gate Authority chain applies.

Core invariant:

```text
Task Pack  = durable planning authority (WHAT must be achieved)
Execution Pack = JIT execution authority bound to one exact base (HOW, safely, on this baseline)
Dispatch   = the executable handoff (WHO/WHERE/WHICH IDENTITY)
```

None of the three is a second Product, Architecture, Task or Validation authority.

A user-visible ChatGPT Web task trigger is not an Execution Pack artifact and has no authority to redefine any of the above. User-visible invocation follows `ISSUE_FIRST_TASK_TRIGGER.md` and remains pointer-only.

## 2. Task Pack

A Task Pack answers: *what must this Task achieve?* It is the durable planning authority for one Task.

It contains, at minimum:

```text
Task identity
dependencies
allowed write set
forbidden scope
acceptance criteria
required gates
validation ownership
review policy
L3 requirement
merge target
```

Recommended representation:

```text
docs/implementation/<version>/TASK_PACKS.json
docs/implementation/<version>/task-packs/Txxx_<name>.md
```

Rules:

- A Task Pack MUST NOT contain exact-base-dependent implementation assumptions (file-level maps, base-relative line references, exact-base patches).
- A Task Pack MUST NOT be duplicated inside Issue bodies; the Task Issue references the pack identity and carries only routing/current metadata.
- Frozen Task Pack content changes require an explicit pack revision; contradictions discovered at execution time route upward (section 5) and are never silently resolved by the executor.

## 3. Execution Pack

An Execution Pack answers: *how can an authorized executor safely implement this Task on this exact repository baseline?*

Properties:

```text
JIT-generated             created when the task becomes executable, not at planning time
exact-base-bound          bound to one immutable integration base SHA
Task-specific             one pack per task per base
implementation-oriented   maps contracts/tests/files onto the exact base
subordinate to Task Pack  may narrow, never redefine, task authority
```

Recommended location:

```text
.agent/execution/<task-id>/
```

Required core artifacts:

```text
MANIFEST.yaml
EXECUTION_CONTRACT.md
TEST_MATRIX.yaml
FAILURE_MATRIX.yaml
IMPLEMENTATION_MAP.md
REVIEW_CHECKLIST.md
```

Optional artifacts:

```text
INTERFACE_SEED.*
SEMANTIC_KERNEL_SEED.*
REFERENCE_PATCH.diff
LOCAL_AGENT_PROMPT.md
reference fixtures
```

Empty placeholder artifacts MUST NOT be required. A minimal task MAY satisfy the core with compact content; a trivial Fast Path task MAY skip the Execution Pack entirely (section 11).

### 3.1 `LOCAL_AGENT_PROMPT.md` boundary

`LOCAL_AGENT_PROMPT.md`, when present, is a durable repository artifact subordinate to the Task Pack and Execution Contract. It may contain reusable executor-oriented guidance that is appropriate to version-control with the exact-base-bound pack.

It is **not** the user-visible ChatGPT Web task trigger.

ChatGPT Web MUST NOT copy or regenerate `LOCAL_AGENT_PROMPT.md` into chat as a parallel handoff contract. User-visible invocation remains limited to repository + Issue/PR + optional role/dispatch pointer under `ISSUE_FIRST_TASK_TRIGGER.md`.

If a task-specific instruction exists only in a chat prompt and not in the Issue/Task Pack/Execution Pack/Dispatch authority, the durable contract is incomplete and must be repaired before invocation.

The manifest identifies at least:

```text
pack_id, task_id, repository, version
base_sha (the exact integration base bound at generation)
task_pack_ref (Task Pack identity)
branch (JIT task branch)
agent_freedom
pinned standard revision
generator identity (logical operator)
generation time
core + optional artifact inventory
dependency completion identities
retention class
```

When dependency identities are serialized in the v3.4 manifest wire format, each entry is:

```text
<task-id>@<40-hex completion/merge SHA>
```

`material_paths` is positive impact coverage used only to prove `PACK_STALE_NONMATERIAL` after the integration base advances. If a pack needs that optimization it SHOULD declare the source/contract/test/fixture/toolchain paths whose delta can materially affect execution. Missing, empty or malformed material coverage MUST NEVER be interpreted as proof of nonmaterial drift.

The six core artifact names are a set contract, not merely an array-length contract. Claim-time semantic verification MUST establish that each required core name is present exactly once; duplicates do not satisfy completeness.

Machine contract: `schemas/execution-pack-manifest.schema.json`. Deterministic claim-time semantics: `scripts/v34_rules.py`.

## 4. Dispatch binding

A Dispatch is the executable handoff from the canonical dispatch architecture (`EXECUTION_ARCHITECTURE_STANDARD.md`). It references Task Pack identity and, when generated, Execution Pack identity, plus role, execution profile, branch, expected base SHA, requested HEAD SHA when applicable, validation profile, pinned standard revision and operator freedom.

Machine contract: `schemas/dispatch.schema.json`.

Execution profiles (`LOCAL_BUILDER`, `LOCAL_VALIDATOR`, `WEB_REVIEWER`, `PLATFORM_VALIDATOR`, `CLOSURE_VALIDATOR`) configure execution authority. They do not introduce separate lifecycle models; all profiles share the canonical dispatch lifecycle and event protocol.

## 5. Authority hierarchy and contradiction routing

The normative hierarchy remains:

```text
Frozen Product Authority
> Frozen Architecture Authority
> Task DAG
> Task Pack
> Execution Contract
> Semantic / Interface Seed
> Agent implementation choice
```

An Execution Pack MAY narrow execution freedom (tighter write set, stricter checks). It MUST NOT redefine:

```text
PRD                       Architecture
Task scope                public contract
required invariant        validation ownership
review requirement
```

Contradictions route upward as explicit failure classes:

```text
TASK_PACK_DEFECT          the Task Pack itself is wrong/incomplete/contradictory
ARCHITECTURE_CONTRADICTION the pack conflicts with Frozen Architecture authority
EXECUTION_PACK_INVALID    the pack is malformed, mis-bound or untrusted
```

A lower-cost Local Agent MUST NOT silently resolve these by redesigning the system. Execution stops on the affected path; the failure is published (structured event or Issue comment) and routed to the owning authority. Independent work continues.

## 6. Just-in-time execution lifecycle

Queued Tasks SHOULD NOT receive long-lived implementation branches before their dependencies are complete.

Default lifecycle:

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

Exceptions are allowed only when a real stacked-code dependency requires an earlier branch; the stack remains a code-baseline fact and does not replace Issue Dependencies.

This eliminates the recurring `ahead N / behind M / refresh / revalidate / rereview` pattern caused by premature branching.

## 7. Execution Pack staleness

At execution claim time the worker verifies:

```text
Execution Pack base SHA
current integration SHA
Task Pack identity
dependency completion identities
pinned standard revision
branch identity
core artifact completeness
```

Canonical classification (deterministic, fail closed):

```text
PACK_CURRENT              execution may proceed

PACK_STALE_NONMATERIAL    integration advanced but the delta does not touch the
                          pack's declared material inputs; only an explicitly
                          authorized impact/rebind action may continue execution;
                          the original base identity remains historical evidence

PACK_STALE_MATERIAL       the delta touches the pack's material inputs, dependency
                          identities changed, delta impact is unknown, or positive
                          material coverage is absent; regenerate affected pack
                          material before execution

PACK_INVALID              pack malformed, mis-bound, wrong task/branch, duplicate/
                          incomplete core inventory, malformed dependency identities,
                          or pinned-standard mismatch; fail closed
```

Classification inputs are facts (SHAs, dependency identities, declared material-path comparisons); they are not executor discretion. When classification is undeterminable, fail closed to `PACK_STALE_MATERIAL` unless the pack itself is malformed, in which case use `PACK_INVALID`.

A base change can be classified `PACK_STALE_NONMATERIAL` only with positive material-impact coverage. An empty/missing `material_paths` set can never establish NONMATERIAL.

The executor MUST NOT silently rewrite `base_sha`. Rebinding is an explicit, attributable action that records both identities.

Derived pack state is exposed through `EXECUTION_PACK_STATE_CHANGED` events and the derived execution state; it is a projection, not a second lifecycle.

## 8. Agent freedom contract

Bounded executor freedom is machine-readable:

```text
F0_MECHANICAL             repository wiring, imports, fixtures, exact contract
                          implementation, non-semantic compile/type/lint repair;
                          no design discretion
F1_BOUNDED_IMPLEMENTATION public contracts / invariants / test oracle fixed;
                          internal implementation may vary
F2_ENGINEERING_DISCRETION low-risk internal engineering choices inside frozen scope
F3_ARCHITECTURE_REQUIRED  must return to Strong Model / architecture authority
```

Rules:

- The freedom level is set by Task Pack / Execution Pack authority, not chosen by the executor.
- An executor MUST NOT self-promote F0/F1/F2 work into F3 authority; discovered needs above the granted level route upward as section-5 failures.
- A freedom level may be narrowed per dispatch; it MUST NOT be silently widened by an executor.

## 9. Semantic and interface seeds

For high-risk semantic concerns, a Web/Strong model MAY prepare compact seed material inside the Execution Pack:

```text
domain/public contracts         identity/digest rules
state-transition predicates     authority boundaries
binding/pinning rules           fail-closed validators
ordering/concurrency invariants critical ports/interfaces
negative test oracle
```

Seeds are subordinate to the Execution Contract and Frozen Architecture. Local agents then own repository integration, adapters, fixtures, workspace wiring, compile/type/lint repair, packaging, platform integration and real-host execution. This extends `MODEL_USAGE_POLICY.md`; it creates no second model-routing standard.

Seeds MUST NOT contain private chain-of-thought; they contain verifiable contracts, predicates and oracles.

## 10. Retention and package exclusion

Durable by default:

```text
MANIFEST
final Execution Contract
TEST_MATRIX
FAILURE_MATRIX
REVIEW_CHECKLIST
critical semantic/interface seeds where they explain authority
```

Potentially transient:

```text
verbose repository-owned prompts
debug notes
temporary hints
scratch artifacts
```

Even when retained, prompt artifacts remain repository evidence/guidance; they do not become user-visible chat authority.

Projects MAY retain complete Execution Packs for provenance. Execution Packs and `.agent/execution/` MUST be excludable from shipped package/product artifacts; a project's packaging gates MUST be able to exclude them without weakening product content. Package leakage of execution-pack material into shipped artifacts is a packaging-gate defect.

## 11. Fast Path

Small, low-risk, mechanical tasks remain valid without full orchestration. Fast Path MAY omit:

```text
large Execution Pack        Semantic Kernel Seed
version validation queue    dedicated local worker
Independent Review when policy does not require it
```

while retaining required truth:

```text
authority          exact identity
validation         evidence
merge safety
```

Complexity must be proportional to risk. Progressive adoption levels from `EXECUTION_ARCHITECTURE_STANDARD.md` apply unchanged.

## 12. Machine contracts

```text
schemas/execution-pack-manifest.schema.json   Execution Pack manifest identity
schemas/dispatch.schema.json                  canonical dispatch object
schemas/task-contract.schema.json             agent_freedom + pack binding fields
schemas/agent-event-v2.schema.json            DISPATCH_CLAIMED / EXECUTION_PACK_STATE_CHANGED
schemas/execution-state.schema.json           derived pack/queue projections
schemas/validation-report.schema.json         exact-SHA validation evidence identity
scripts/v34_rules.py                          claim-time fail-closed semantic oracle
```

The repository's supported JSON-Schema subset and verifier regressions apply to all of them.

## 13. Non-goals

This standard does not require a centralized scheduler, does not create Builder/Validator/Reviewer state machines, does not make Build Host validation mandatory per task, does not make Independent Review universal, does not authorize Local Agent architecture redesign by default, does not turn the Execution Pack into a second Product/Architecture authority, and does not make any prompt artifact a parallel chat task authority.