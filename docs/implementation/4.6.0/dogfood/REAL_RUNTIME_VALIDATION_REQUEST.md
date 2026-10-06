# T06 Exact-subject Fresh-context Validation Request

Status: **REQUESTED — NOT_RUN by Builder**

## Immutable packet binding

```text
REPOSITORY=kaicreator-mm/ai-development-standard
ISSUE=#309
TASK=T06
PACKET=docs/implementation/4.6.0/dogfood/session_operator_handoff_packet.json
PACKET_SHA256=33f9c9aad5d28d58e73af52326bc8bffb61a0eb4e44cb9ff49ce16b19ba6f46b
AUTHORIZED_BUILDER_BASE=0458982cd16ba8539085ee0fcc26d2bf46a60ceb
INTEGRATION_TARGET=version/v4.6.0
```

The packet digest above binds the exact handoff fixture. It does **not** bind the future PR final HEAD/tree. The independent Validator MUST re-read and record the PR live HEAD/tree immediately before Validation.

## Required validator context boundary

Use a fresh logical context that does not receive:

- the originating Builder chat transcript;
- Builder private chain-of-thought;
- unrecorded Builder session memory.

The same GitHub/API transport account is allowed and is not, by itself, evidence for or against logical-context independence.

## Validation claim

Using only the immutable packet, its named durable repository/GitHub refs, and required live currentness rereads, independently reconstruct:

1. requested work;
2. Frozen/current authority;
3. exact PR subject identity;
4. completed evidence;
5. open findings/blockers;
6. remaining work;
7. next owner/action;
8. forbidden assumptions.

Compare the reconstruction to the packet's `expected_reconstruction` and record discrepancies as findings.

## Required negatives

Explicitly reject these inferences:

- same transport account => same logical operator/context;
- different provider/model => independence proven;
- fixture/static PASS => real external Agent/runtime PASS;
- historical chat/memory => current durable authority;
- tool/model capability => side-effect/merge authority;
- PR exists => Validation/Review/Closure/Release/merge PASS.

## Real external Agent/runtime dimension

Builder status: `NOT_RUN`.

Only mark a real external Agent/runtime dimension PASS if the Validator actually executes that dimension against the exact packet and live PR subject and records its runtime/executor/context evidence. If that capability is unavailable, keep that dimension `NOT_RUN` or `BLOCKED`; the static fixture test is not a substitute.

## Downstream gate

Validation evidence is input to a separate Fresh Independent Review. This request grants no self-review, Version Closure, Release or merge authority.
