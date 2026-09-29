# T07 — Cross-standard Conformance / Closure Inputs

Depends on: T04 + T05 + T06
Frozen Product: `fc68e869c18cec07e2a72b8fa5e4520ade1dc5a9`
Frozen L2: `ea4532cacf87c03689351e43363580e2a14acd95`
Review policy: required
Validation scope: integration / closure-input
Agent freedom: `F1_BOUNDED_IMPLEMENTATION`

## Goal
Prove the integrated v4.2 semantics compose with existing v4/v4.1 owners and produce truthful inputs for Version Closure.

## Allowed write-set
- v4.2 integration/conformance suites
- closure-input evidence docs under `docs/implementation/4.2.0/`
- narrowly required regression wiring owned by this Task

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