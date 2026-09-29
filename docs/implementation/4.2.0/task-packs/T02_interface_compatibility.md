# T02 — Interface & Compatibility Governance

Depends on: T01
Frozen Product: `fc68e869c18cec07e2a72b8fa5e4520ade1dc5a9`
Frozen L2: `ea4532cacf87c03689351e43363580e2a14acd95`
Review policy: required
Validation scope: concern
Agent freedom: `F1_BOUNDED_IMPLEMENTATION`

## Goal
Create the single normative owner for contract baseline/change-operation and compatibility outcomes by dimension.

## Allowed write-set
- `standards/INTERFACE_COMPATIBILITY_GOVERNANCE_STANDARD.md`
- `references/INTERFACE_COMPATIBILITY_REFERENCE.md`
- `scripts/test_v42_interface_compatibility.py`

## Required semantics
- explicit contract/baseline identity;
- operation kind separate from outcome;
- multi-dimensional/extensible compatibility;
- producer/consumer/window evidence when material;
- schema/wire result cannot manufacture source/behavior/consumer result;
- provider+consumer co-change cannot mask older/external consumer break;
- generated SDK/codegen subordinate to canonical contract;
- deprecation/removal authority explicit;
- Fast Path/materiality preserved.

## Forbidden
No migration ownership, no Validation state vocabulary, no deployment state, no central manifest wiring, no mandatory API style/checker.

## Required adversarial tests
`wire-safe -> source compatible`, `schema PASS -> behavior PASS`, `new/new -> old/new compatible`, unknown dimension -> compatible, generated client -> authority MUST all be rejected.

## Implementation reference
See `L3_REFERENCE_PACKS.md#t02--interface--compatibility-governance`.

## Completion
Exact-HEAD concern Validation + Fresh Independent Review PASS, then merge.