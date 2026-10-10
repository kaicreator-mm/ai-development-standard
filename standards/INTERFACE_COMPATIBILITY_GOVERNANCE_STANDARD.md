# Interface & Compatibility Governance Standard

Status: **Normative — v4.2**

## 1. Purpose

This standard owns interface/contract compatibility semantics. It defines how a change is bound to an explicit contract baseline and candidate, how compatibility is evaluated by evidence-bearing dimensions, and how deprecation/removal is governed without creating a second Validation, Release, Migration, Deployment, or workflow state model.

This owner is intentionally mechanism-neutral. OpenAPI, Protobuf, JSON Schema, RPC IDL, generated SDKs, database APIs, CLIs, message schemas, file formats, and other contract mechanisms MAY provide evidence, but no checker or format is universally mandatory.

## 2. Authority boundary

The following are owned here:

- contract identity and baseline/candidate identity for compatibility analysis;
- change-operation description as a fact distinct from compatibility outcome;
- compatibility outcomes by explicit, extensible dimension;
- producer, consumer, and compatibility-window evidence when material;
- deprecation/removal compatibility obligations.

The following are **not** owned here:

- persistent-state migration and recovery semantics — Data & Migration Governance;
- Validation PASS/FAIL or exact-SHA evidence truth — Validation;
- rollout/deployment result — Deployment;
- Release Qualification — Release;
- canonical workflow/Gate states — existing workflow owners.

A Compatibility Record is evidence about a contract relationship. It is not a Gate result.

## 3. Exact subject and baseline binding

A compatibility claim MUST identify the contract under analysis and MUST bind both sides of the comparison to durable identities sufficient for the mechanism involved.

At minimum, the analysis MUST preserve:

1. canonical contract kind/identity;
2. baseline identity;
3. candidate identity;
4. the change operation(s) actually performed;
5. the compatibility dimension(s) actually evaluated;
6. supporting evidence references.

A mutable branch name, tag, package alias, generated client name, or current provider state MUST NOT substitute for the exact baseline/candidate identity when exact identity is material.

When a material compatibility claim depends on an accepted specification change, the claim MUST additionally bind the accepted specification itself to durable identities: the accepted specification baseline (`spec_baseline_ref`), the accepted delta (`proposed_delta_ref`) with its ADDED/MODIFIED/REMOVED change operations, the acceptance authority (`acceptance_authority_ref`), and the currently effective accepted revision (`accepted_spec_current_ref`). Acceptance or archival of a specification delta is a recorded decision about intent, and MUST NOT substitute for the exact baseline/candidate identity of the actually shipped contract artifacts.

## 4. Change operation is not compatibility outcome

A change operation describes **what changed**. A compatibility outcome describes **what the evidence says about a particular dimension**.

Examples of change operations include add-field, remove-field, rename, widen, narrow, change-default, reorder, add-endpoint, and remove-endpoint. These names MAY vary by contract mechanism.

No operation name implies a universal compatibility result. In particular:

- `add` does not universally mean compatible;
- `wire-safe` does not prove source compatibility;
- `schema-valid` does not prove behavioral compatibility;
- successful generation does not prove consumer compatibility.

The machine representation defined by `schemas/compatibility-record-v1.schema.json` therefore keeps `change_operations` structurally separate from `dimensions[].outcome`.

The same separation governs accepted specifications. An accepted `ADDED` operation does not imply that any producer ships the added surface; an accepted `MODIFIED` operation does not imply that any producer implements the modified behavior; an accepted `REMOVED` operation does not imply that the removal has shipped or that affected consumers have moved. An accepted spec is not code: acceptance is a change fact, never an implementation outcome.

## 5. Compatibility is multi-dimensional and extensible

Compatibility MUST be evaluated only for dimensions that are material to the actual producer/consumer relationship. Dimension names are extensible; this standard does not freeze a universal closed enum.

Common dimensions MAY include:

- wire / serialized representation;
- source / compile-time consumer compatibility;
- runtime / binary compatibility;
- schema validation;
- behavioral / semantic compatibility;
- consumer capability;
- operational or rollout compatibility when used only as an interface concern.

Each evaluated dimension MUST carry an explicit outcome. Absence of a dimension means **not evaluated**, not compatible.

An outcome for one dimension MUST NOT be promoted into another dimension without direct evidence. Therefore:

- wire-compatible **MUST NOT imply** source-compatible;
- schema-compatible **MUST NOT imply** behavior-compatible;
- new-provider/new-consumer success **MUST NOT imply** old-consumer/new-provider compatibility;
- `UNKNOWN` or an omitted material dimension **MUST NOT imply** `COMPATIBLE`.

When an accepted specification change is reconciled against an implementation, the required wire, source, and behavior dimensions MUST be observed on the current producer subject and the affected supported consumer windows, not on a superseded subject.

## 6. Producer, consumer, and window evidence

When compatibility depends on deployed or supported consumers, the evidence MUST identify the relevant producer/consumer population or compatibility window.

A provider and its newest consumer changing together MUST NOT hide breakage for:

- older supported consumers;
- external consumers outside the producer repository;
- asynchronous consumers not upgraded in the same operation;
- consumers whose generated code or runtime capability differs from the tested pair.

A compatibility window MAY be version-, support-line-, time-, deployment-, or contract-policy-based. The chosen window MUST be evidenced; this standard does not mandate one universal version policy.

An accepted specification change that names affected producer/consumer windows MUST have every still-supported affected window evidenced for the required dimensions. A window tested once does not remain current by default: producer, consumer, contract, or accepted-spec drift makes prior evidence stale for exactly the drifted material scope, and the affected current assertions MUST be revalidated before being relied on again. Drift MUST NOT be generalized to unrelated windows, and evidence for prior windows MUST be preserved as history rather than rewritten.

## 7. Generated clients and derived artifacts

Generated SDKs, clients, stubs, documentation, or codegen output are subordinate derivations of a canonical contract.

Generated output MAY provide evidence that a tool accepted a contract. It MUST NOT become the canonical contract authority merely because generation succeeded.

`generated client exists -> compatible` is a forbidden inference.

## 8. Deprecation and removal

Deprecation is a compatibility transition, not an immediate authorization to remove an interface.

A material deprecation/removal decision MUST identify, as applicable:

- the deprecated contract surface;
- affected producer/consumer window;
- replacement or transition path;
- observation/evidence that required consumers have moved or accepted the break;
- explicit authority for the removal decision.

Elapsed time alone, a warning annotation alone, or absence of recent failures MUST NOT manufacture removal authority.

An accepted REMOVED change ships only when the current producer implementation no longer provides the removed surface and every still-supported affected consumer window is evidenced as moved or as incompatible. A new producer/new consumer success MUST NOT be recorded as current removal compatibility while a still-supported window still calls the removed operation; that window remains `INCOMPATIBLE` until it is re-evidenced.

## 9. Fast Path and materiality

Fast Path remains proportional. A change that does not materially alter an externally or internally relied-upon contract need not create empty compatibility records.

Conversely, a small diff, generated change, documentation-only wrapper, or apparently additive edit MUST NOT use Fast Path to bypass compatibility evidence when a material consumer contract changes.

An accepted specification change with no affected producer or consumer MAY receive an explicit proportionate nonmaterial disposition without creating a compatibility record. Archive merge, codegen success, or checker-only GREEN is not materiality evidence and MUST NOT manufacture an implementation or consumer claim.

## 10. Required forbidden-inference matrix

The following negative rules are normative:

| Input fact | Forbidden inferred conclusion |
|---|---|
| wire-safe | source compatible |
| schema/checker passes | behavior compatible |
| new provider + new consumer pass | old/external consumer compatible |
| dimension missing or `UNKNOWN` | compatible |
| generated client/codegen succeeds | generated artifact is contract authority or proves compatibility |

Implementations and conformance tests MUST preserve these negatives.

## 11. Machine-contract relation

`schemas/compatibility-record-v1.schema.json` is the default machine representation for compatibility evidence in v4.2. Its vocabulary is compatibility-domain vocabulary, not Validation/Release state vocabulary.

Tools MAY emit additional mechanism-specific evidence referenced by the record. Such evidence MUST NOT weaken the authority or inference rules in this standard.

Accepted-spec implementation currentness MAY be carried as a proposed evidence projection with the logical fields `spec_baseline_ref`, `proposed_delta_ref`, `acceptance_authority_ref`, `accepted_spec_current_ref`, `implementation_subject_ref`, `affected_producer_consumer_windows`, and `revalidation_refs`, bound to the existing contract/baseline/candidate/change_operations/dimensions vocabulary. These are proposed logical fields only: this standard does not add them to `schemas/compatibility-record-v1.schema.json`, and any additive machine projection is owned by the centrally designated wiring task. Records that are valid under the v1 schema MUST remain readable by v1 readers, and no new mandatory field applies retroactively. A reconciliation disposition is compatibility-domain evidence vocabulary, not a Gate, Validation, or Release state, and it never converts compatibility into release authority.

## 12. Failure handling

If contract identity, baseline/candidate identity, a material compatibility dimension, or required consumer/window evidence is unknown, the system MUST retain that uncertainty (`UNKNOWN`, not evaluated, or BLOCKED in the owning workflow) rather than manufacture compatibility.

A compatibility concern that requires unavailable external consumers/toolchains MAY be handed to an exact-subject Validation task. Missing execution is never a compatibility PASS.

An accepted specification that is not reconciled with an exact current producer implementation subject and evidenced affected consumer windows stays `UNKNOWN`/`BLOCKED`, never implemented. Evidence that was current for a superseded producer, consumer, or specification revision is stale, not false: it remains recorded as history and routes to revalidation for the affected scope. A material consumer that cannot be tested remains explicitly `NOT_RUN` and routes to an exact-subject Validation owner. Current assertions MUST remain distinguishable from historical reports.
