# Interface & Compatibility Reference

This reference is non-normative guidance for applying `standards/INTERFACE_COMPATIBILITY_GOVERNANCE_STANDARD.md`.

## 1. Minimal analysis shape

A useful compatibility analysis starts from an exact subject, not from a generic label such as “breaking” or “safe”:

```text
contract: payments-api / protobuf service Foo
baseline: v1.8.4 + digest/SHA A
candidate: PR head / digest/SHA B
operations: add field, narrow accepted enum, remove deprecated endpoint
consumers: web@X, mobile support line Y, external partner contract Z
window: current + previous supported client line
```

For each material dimension, record a separate outcome and evidence. Do not copy one checker result into all dimensions.

## 2. Example — additive wire change with source risk

A Protobuf field addition can be wire-compatible for existing parsers while a language-specific generated client or source API may still change in a way relevant to consumers.

Correct posture:

- wire: `COMPATIBLE` with schema/tool evidence;
- source: separately evaluated;
- behavior: separately evaluated if defaults/presence semantics matter;
- consumer: separately evaluated for supported clients.

Incorrect posture: `wire-safe => everything compatible`.

## 3. Example — provider and consumer co-change

If provider HEAD B and consumer HEAD C are upgraded together and integration tests pass, that proves the tested pair only.

If production still supports consumer A, the analysis must preserve A→B compatibility as a separate subject. New/new success cannot erase old/new risk.

## 4. Example — schema checker and behavioral semantics

A JSON/OpenAPI/IDL checker may prove structural acceptance. It does not prove:

- response ordering semantics;
- default-value meaning;
- authorization behavior;
- retry/idempotency behavior;
- latency/resource assumptions;
- application-level invariants.

Record behavioral compatibility only when behavioral evidence exists.

## 5. Deprecation/removal worksheet

For a material removal, capture:

```text
deprecated_surface:
replacement_ref:
supported_consumer_window:
consumer_migration_evidence_refs:
removal_authority_ref:
remaining_unknown_consumers:
```

If `remaining_unknown_consumers` is material and unresolved, do not infer removal safety from elapsed time alone.

## 6. Mechanism-specific evidence

Useful evidence may come from:

- official compiler/schema compatibility tools;
- consumer contract tests;
- historical payload replay;
- source compilation against supported client versions;
- integration/CJ execution;
- production support matrices when they are already authoritative.

Tool output is evidence, not policy authority. The governing standard decides which inference is allowed.

## 7. Fast Path examples

Likely non-material: typo-only internal documentation change with no generated contract output.

Potentially material despite small diff: changing an enum member, default, requiredness, authentication behavior, serialized field number, public function signature, or supported consumer window.

## 8. Review prompts

A reviewer should ask:

1. What exact contract and baseline/candidate are being compared?
2. Which dimensions are material, and which were actually evaluated?
3. Are producer/consumer populations representative of the compatibility claim?
4. Is any result being promoted across dimensions without evidence?
5. Is a generated artifact/checker result being treated as authority?
6. Is deprecation/removal authority explicit?
7. Are unknowns preserved rather than normalized to compatibility?
