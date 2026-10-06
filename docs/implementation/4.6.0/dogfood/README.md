# v4.6 T06 Session / Operator Handoff Dogfood

Status: **BUILDER STATIC/FIXTURE DOGFOOD IMPLEMENTATION — exact-subject Validation and Fresh Independent Review still required**

## 1. Scope

This dogfood is owned only by T06. It demonstrates the durable handoff shape required by Frozen Product/L2/DAG/L3 without making the originating Builder chat a required input.

Canonical packet:

- `session_operator_handoff_packet.json`
- SHA-256: `33f9c9aad5d28d58e73af52326bc8bffb61a0eb4e44cb9ff49ce16b19ba6f46b`

The packet is intentionally a compact set of exact durable pointers plus the minimum handoff facts. It is not a copied chat transcript or a new lifecycle/authority object.

## 2. Exact Builder starting subject

The pre-write currentness check bound this Builder to:

```text
ISSUE=#309
TASK=T06
TASK_BRANCH=task/309-v46-session-handoff-dogfood
AUTHORIZED_BASE_SHA=0458982cd16ba8539085ee0fcc26d2bf46a60ceb
AUTHORIZED_BASE_TREE=8853d15ab47b884f23a42ceefb9b301b8525a074
INTEGRATION_TARGET=version/v4.6.0
TASK_PACK=docs/implementation/4.6.0/task-packs/T06_session_handoff_dogfood.md
TASK_PACK_BLOB=9fb2c513040d39c63888b090670af789f2f787aa
```

The live #309 Controller dispatch comment is the durable JIT/unblock fact. A later Validator/Reviewer must re-read the PR live HEAD/tree instead of treating this Builder starting SHA as final-subject currentness.

## 3. Fresh logical executor protocol

A fresh logical executor is given only:

1. the canonical packet;
2. the durable repository/GitHub refs named by it;
3. live currentness rereads required by the next action.

It is **not** given the originating chat transcript, private reasoning, or unrecorded session memory.

From those inputs it must reconstruct:

- requested work;
- Frozen/current authority;
- exact subject identity;
- completed evidence;
- findings/blockers;
- remaining work;
- next owner/action;
- forbidden assumptions.

`python scripts/test_v46_session_handoff_dogfood.py` performs the focused deterministic fixture check using that same packet shape.

## 4. Identity boundary

Transport identity and logical operator/context identity are separate dimensions.

```text
same GitHub/API account != same logical operator/context
different provider/model != independence proven
```

This Builder may use the same connected GitHub transport as a future Validator. That does not itself prove or disprove fresh logical-context independence. The independent Validator must establish the required context/executor boundary against the exact PR subject.

## 5. Claim/evidence ledger

| Dimension | Builder result | Meaning |
| --- | --- | --- |
| packet completeness/reconstruction shape | `STATIC_FIXTURE_PASS` after focused test | packet deterministically contains every required handoff field |
| originating chat required as input | `NO` by construction | packet excludes it from required inputs |
| transport vs logical identity distinction | `STATIC_FIXTURE_PASS` | forbidden inference is explicit and test-covered |
| real fresh external Agent/runtime reconstruction | `NOT_RUN` | Builder fixture cannot prove it |
| exact-subject Validation | `NOT_RUN / PENDING` | separate Validator must bind live PR HEAD/tree |
| Fresh Independent Review | `NOT_RUN / PENDING` | separate fresh Reviewer required |
| Version Closure / Release | `NOT_RUN / OUT_OF_SCOPE` | T06 Builder has no authority |
| merge | `NOT_RUN / FORBIDDEN_FOR_BUILDER` | Controller owns later integration decision |

No fixture/static result in this directory may be relabeled as a real-runtime PASS.

## 6. Exact-subject Validation handoff

`REAL_RUNTIME_VALIDATION_REQUEST.md` binds the immutable packet SHA-256 and describes the minimum real fresh-context Validation claim. The Validator must additionally bind the then-current PR HEAD/tree before executing and record whether any real external Agent/runtime dimension was actually run.

If the required real capability is unavailable, record `NOT_RUN/BLOCKED` for that dimension; do not infer it from the focused fixture test.

## 7. Builder boundary

This Task does not:

- rewrite T01-T05 owners;
- absorb T07 adoption wiring;
- introduce v4.7 convergence;
- self-review;
- perform Version Closure;
- merge the PR.
