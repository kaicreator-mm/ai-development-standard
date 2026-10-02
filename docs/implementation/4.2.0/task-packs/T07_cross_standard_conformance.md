# T07 — Cross-standard Conformance / Closure Inputs

Depends on: T04 + T05 + T06
Frozen Product: `fc68e869c18cec07e2a72b8fa5e4520ade1dc5a9`
Frozen L2: `ea4532cacf87c03689351e43363580e2a14acd95`
Review policy: required
Validation scope: integration / closure-input
Agent freedom: `F1_BOUNDED_IMPLEMENTATION`

## Goal
Prove the integrated v4.2 semantics compose with existing v4/v4.1 owners and produce truthful inputs for Version Closure.

## Allowed write-set (explicit T07 authority)

The previously broad v4.2 integration/conformance, closure-document and narrowly required regression-wiring classes are bounded to **exactly** these paths for this Task:

- `scripts/test_v42_cross_standard_conformance.py` — execute integrated v4.2 owner/dogfood/compatibility suites and cross-standard negatives;
- `docs/implementation/4.2.0/dogfood/T07_cross_standard_cases.json` — executable integrated positive/forbidden cases and rationale;
- `docs/implementation/4.2.0/CROSS_STANDARD_CONFORMANCE_STATUS.md` — evidence strength/currentness with no Release verdict;
- `docs/implementation/4.2.0/CLOSURE_INPUTS.md` — durable inputs and outstanding owner gates for Version Closure;
- `scripts/test_verify_standard.py` — **only** narrowly add regression invocation of the T07 integration runner; no verifier policy or unrelated test rewrite.

No other central/verifier/manifest/Golden path is authorized by technical necessity alone. Any newly required path needs a separate authority amendment.

## Required checks
- all Frozen PRD forbidden inferences are executable negatives;
- owner uniqueness for compatibility, migration, Validation, Release and future Deployment;
- historical payload/adoption compatibility;
- Fast Path proportionality;
- exact-SHA/environment evidence currentness;
- API/service + database dogfood evidence consumed without overclaim;
- no Release READY / Deployment SUCCESS inference introduced;
- unresolved P0/P1 blocks closure inputs.

## Forbidden
No Version Closure verdict, no Release Qualification verdict, no T01–T06 semantic rewrite unless a new repair Task/authorized successor is created.

## Completion
Integration Validation + Fresh Independent Review PASS and durable handoff to Version Closure.
