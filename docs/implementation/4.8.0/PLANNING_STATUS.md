# v4.8.0 Planning Status

Status: **PRODUCT FROZEN — L2 REPAIRED / FRESH ARCHITECTURE RE-REVIEW REQUIRED — TASK DAG NOT AUTHORIZED**

## Currentness semantics

This file is descriptive planning metadata. It MUST NOT claim that an embedded commit SHA/tree is the live current planning subject because editing this file changes that subject.

Exact review/freeze subjects are bound after commits exist through durable GitHub review dispatch/result facts plus immutable blob identities.

## Product Freeze

Product Freeze remains unchanged and valid:

- `docs/implementation/4.8.0/PRODUCT_FREEZE.md` blob `8720264f56a23e352b347dd74df966b9416c9129`;
- Frozen PRD blob `f26439580e00de6ed8b2e27d732a3095eb566219`;
- reviewed Product source PR #482 HEAD `b8c3879a65c9159759457744c2a24e7e5777c8c1`, tree `14c1bf8dd4e684b90c633ca50ff1762471f21f1c`;
- Fresh Independent Product Review R3 #490 terminal `5926142930`;
- dogfood basis `#469@5925124956`.

Frozen Product, PRD and L1 were not modified by the L2 repair.

## Architecture review history

- #492: pre-review exact-HEAD dispatch superseded; historical only.
- #494: canonical Fresh Independent Architecture Review R2 on `8e9dc8fe...` / tree `dd68b981...` / L2 blob `f28f123e...`.
- #494 terminal `5926563715` returned `CHANGES_REQUESTED`, P0=0/P1=3/P2=0/P3=0, Product Freeze validity PASS, Research Demo disposition PASS, L2 Freeze authorization NO.
- P1-1: proposed new Agent Exchange owner/family duplicated existing v4.0 Interchange owner and active `interchange-envelope-v1`.
- P1-2: resource scheduling lacked one all-or-none linearization point across work claim + every scarce-resource/capacity binding.
- P1-3: generic Agent Capability Profile overlapped existing `CI_RUNNER_CAPABILITY_STANDARD.md` runner/host platform/toolchain/resource/concurrency ownership.
- #499: bounded L2 repair owns closure of those three findings.

## Repaired architecture

Current repaired L2 semantics are:

1. exactly **three new default machine-contract families**:
   - Task Learning Evidence v1;
   - Logical Agent Capability Profile v1;
   - Agent Capability Evidence v1;
2. existing v4.0 `AGENT_INTERCHANGE.md` + `schemas/interchange-envelope-v1.schema.json` are reused; v4.8 may only make a compatible extension/profile if a real field gap is proven;
3. `ai-dev:event:v2` remains the GitHub writer/admission protocol;
4. `CI_RUNNER_CAPABILITY_STANDARD.md` retains runner/host platform/toolchain/resource/concurrency capability ownership;
5. logical Agent Profile carries logical executor/model/role/semantic claims and references environment/runner requirements rather than copying infrastructure inventory;
6. Availability remains current derived reachability/currentness over applicable owners;
7. Capability Evidence remains historical exact-subject evidence;
8. hard eligibility precedes optional ranking;
9. work claim + all required scarce-resource/capacity reservations require one **all-or-none composite admission linearization point**;
10. capacity-N active accepted bindings may never exceed N; N=1 is exclusive resource;
11. independent per-key CAS/reservations are insufficient;
12. crash/publication ambiguity fails closed and requires durable reconciliation before replacement admission.

## Research Demo disposition

No pre-L2 executable Research Demo is currently required. #494 found all three P1 repairs statically decidable.

This remains true only because the architecture permits one designated `SINGLE_WRITER_ADMISSION` composite critical section and does not depend on an unproven distributed multi-key CAS/lease mechanism. A later implementation choosing a novel distributed mechanism must create a narrow Research Demo/Validation for that mechanism.

## Dogfood evidence boundary

`#469@5925124956` remains the latest material Product/L2 input currently consumed:

```text
ACTUAL_LOW_COST_IMPLEMENTATION_OUTCOME=PARTIALLY_MEASURED_POSITIVE_EXECUTION
ECONOMIC_SAVINGS=NOT_MEASURED
BLANKET_STRONG_TO_LOW_COST_RULE=NOT_SUPPORTED
STANDARD_CHANGE=NOT_AUTHORIZED
PROPOSED_DISPOSITION=MORE_EVIDENCE
```

Provider/model identity remains provenance, not normative routing policy.

## Current gates

- Product: **FROZEN**;
- L2: **REPAIRED CANDIDATE / NOT FROZEN**;
- Fresh Architecture Re-Review: **REQUIRED**;
- Research Demo: **NOT REQUIRED on current repaired architecture**;
- Task DAG: **NOT CREATED / NOT AUTHORIZED**;
- Task Packs / executable Issues / implementation: **NOT AUTHORIZED**.

## Required sequence

```text
#499 bounded L2 repair
-> NEW genuinely fresh exact-subject Architecture Re-Review
-> resolve any P0/P1 or required Research Demo
-> explicit L2 Freeze only if authorized
-> Task DAG
-> Task Packs / L3 / Issue materialization
-> implementation
```

Do not infer L2 Freeze or executable Task authority from the repaired candidate itself.
