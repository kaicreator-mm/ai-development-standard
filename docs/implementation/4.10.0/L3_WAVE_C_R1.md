# v4.10.0 Wave C L3 Reference Pack R1

Status: **DURABLE PRE-ADMISSION L3 — JIT EXECUTION PACK REQUIRED**

Authority: Frozen Product #837, Frozen L2 #842, refined DAG Freeze #848, Task Packs R1 #849, native DAG #866, predecessor V410-T02A/#852 DONE and integrated by PR #879.

## V410-T02B / #853 — GitHub/event/machine projection for collaboration control

### Tests
Positive cases MUST prove:
1. a delegated child dispatch can reconstruct requester/delegator, active responsibility owner, executor/operator, causal parent, bounded authority scope and result/evidence return from durable facts;
2. `RESPONSIBILITY_HANDOFF` produces exactly one active responsibility owner across transfer;
3. authority attenuation remains bounded by delegatable authority ∩ current Task/Work ∩ role ∩ project/external authorization;
4. Human control remains routed through existing control/HDQ semantics without creating routine relay events;
5. historical dispatch/events without additive projection fields remain valid;
6. existing protocol/schema/event writer suites remain green.

Negative cases MUST reject:
1. ambiguous or unresolved parent/causal refs being guessed;
2. a second active handoff for the same work identity;
3. capability/credential/tool access widening authority;
4. any new event family, state dimension, lifecycle, responsibility registry/ledger or scheduler;
5. partial canonical facts after invalid/stale/unauthorized intent;
6. transfer of Validation/Review evidence across successor HEAD drift.

### Contract / invariant
Consume the integrated V410-T02A responsibility/control semantics; do not redefine them. Existing refs already reconstruct requester, owner, executor, scope and evidence return. The only proven machine-projection gaps are deterministic parent/causal dispatch linkage and explicit responsibility mode/handoff pairing. Any new machine fields MUST be optional, additive, same-family and backward compatible. Projection creates no authority. Ambiguity fails closed.

### Implementation seam
Primary owner: `standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md`.
Allowed bounded projections: `schemas/dispatch.schema.json`, `schemas/agent-event-v2.schema.json`, `templates/agent-event-comment.md`, and directly-owned focused tests. `standards/EXECUTION_ARCHITECTURE_STANDARD.md` is a consumed semantic owner, not a rewrite target for T02B. `standards/GITHUB_WORK_ITEM_CONTRACT_STANDARD.md`, execution-state schema, local-agent-handoff schema and state-dimensions registry are reference/negative-boundary surfaces unless a concrete contradiction is found.

Minimal preferred projection: optional `parent_dispatch_ref` plus optional `responsibility_mode` (`DELEGATED_SUBWORK | RESPONSIBILITY_HANDOFF`) on existing dispatch/event-v2 structures; handoff must be reconstructible with transferor, receiver, scope and exact work identity. No new event type or state dimension.

### Failure handling
If deterministic reconstruction requires a new lifecycle/event/state/registry family, stop with `ARCHITECTURE_CONTRADICTION` / `TASK_PACK_DEFECT`. If integrated T02A semantics differ materially from the Web preplan assumptions, stop and re-plan rather than redefining the owner. Central manifest/conformance wiring routes to T06A/T06B. Baseline/owner drift at claim requires JIT rebind from the exact tree.

### Currentness seed
Post-merge baseline before this L3 checkpoint: `2276afe7fdd057f300386ab19925ae37a4065684`.
Observed owner blobs on that exact baseline:
- `standards/EXECUTION_ARCHITECTURE_STANDARD.md` @ `180efe4e1bc589f6a1f67473ff988f479f6be900`
- `standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md` @ `3fc300861a579c26f60e6c554f3f20675375c966`
- `standards/GITHUB_WORK_ITEM_CONTRACT_STANDARD.md` @ `196f7d9372bcffd6ff801a70e1c1fffb204f4336`
- `schemas/agent-event-v2.schema.json` @ `fefba14f338bc2e9bf67c16bae1918c1b34005a0`
- `schemas/dispatch.schema.json` @ `4607f6cb4b690bf68137294a9acf5d6ccc49e6bd`
- `templates/agent-event-comment.md` @ `fb98bb45827223235bb8d76f193cb1f250242211`

JIT admission MUST re-read the integration HEAD after this L3 commit and rebind owner blobs from that exact tree. Web preplan #853@6000907838 is planning evidence only, not execution admission or a gate verdict.
