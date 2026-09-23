# T-008 Task Pack — Validation, Candidate Freeze, Hidden Validation and Release Integration

Issue: #80
Parent version: #72
Baseline: `3a131497527bcc255c152635d42bcdc8cb5ba813`
Review Policy: required
Risk: critical
Validation scope: concern
Agent freedom: F1_BOUNDED_IMPLEMENTATION

## Goal

Map v4 Operation/Assurance semantics onto existing Validation, Candidate Freeze, Hidden Validation, Release Qualification and Repository Integration authority without weakening exact-execution truth or candidate/release identity.

## Inputs

- merged T-001..T-007 v4 artifacts;
- `standards/VALIDATION_STANDARD.md`;
- `standards/RELEASE_STANDARD.md`;
- `standards/EXECUTION_ARCHITECTURE_STANDARD.md`;
- all T-006/T-007 orthogonality, idempotency, exact-identity and Fast Path invariants.

## Allowed changes

- `docs/implementation/4.0.0/VALIDATION_RELEASE_INTEGRATION.md`;
- this Task Pack;
- T-008 pointer in `docs/implementation/4.0.0/TASK_PACKS.json`.

## Forbidden changes

- JSON schemas/verifier code/event enums;
- reducer/controller implementation;
- Hidden private fixtures/packet contents;
- actual v4 Candidate Freeze/Release Qualification;
- T-009/T-010/T-012/T-013 execution scope.

## Review oracle

Reviewer must verify at least:

1. Validation PASS still requires actual execution;
2. ASSURE/Operation completion cannot manufacture Gate truth;
3. exact SHA/platform/toolchain/profile binding remains authoritative;
4. old evidence is never rebound to successor identity;
5. concern/integration/closure ownership remains distinct;
6. Review/model agreement is not runtime/Hidden evidence;
7. PREPARED and FROZEN remain distinct candidate states;
8. Freeze binds exact candidate SHA/tree and visible closure evidence;
9. frozen candidate content mutation requires thaw/invalidate/successor flow;
10. Hidden Validation remains independent, private-payload-safe, candidate/pack-bound evidence;
11. escaped Hidden defects remain append-oriented and pack/product defects are distinct;
12. Release Qualification as DECIDE does not predetermine READY/CONDITIONAL/BLOCKED/FAIL;
13. `PR PASS != Release PASS` is explicit;
14. Repository Integration as CONTROL remains distinct from Release Qualification;
15. final integration records candidate and final main identities separately when they differ;
16. Fast Path cannot bypass required closure/Hidden/freeze/release gates;
17. no schema/verifier/actual release execution scope is entered.

## Failure handling

- missing executable truth -> preserve `NOT_RUN`/`BLOCKED`; never infer PASS;
- identity drift -> stale/superseded handling under existing Validation/Release authority;
- candidate content change after freeze -> thaw/invalidate and successor flow;
- private Hidden evidence exposure risk -> fail closed and record only public-safe metadata;
- unresolved machine representation -> route to T-009, do not invent a second protocol here.

## Completion

Exact-head repository verifier PASS + Fresh Independent Review PASS on the same HEAD + focused merge to `version/v4.0.0`.