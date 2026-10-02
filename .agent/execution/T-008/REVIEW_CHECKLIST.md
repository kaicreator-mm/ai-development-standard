# T-008 Fresh Independent Review Checklist

This checklist is guidance for the later required fresh Reviewer. It is not a review result and the JIT Planning Builder does not self-review T08.

## Exact subject and scope

- [ ] Re-read PR live HEAD/tree and `version/v4.6.0` live target immediately before review.
- [ ] Confirm the implementation was admitted from bound base `a4c5fffe6bab178dcb74b5f47afcda4aa0047c27` / tree `6ae5e1a8b33a6127ecc2e94b6db45e0ca6fa30ea`, or verify an explicitly authorized Controller rebind.
- [ ] Distinguish Controller-generated `.agent/execution/T-008/**` from Builder implementation delta; Builder delta after Pack HEAD is limited to the T08 Task Pack write-set.
- [ ] Confirm Task Pack blob `248abb5c468240e702f383b003a93a6f503e4cfa` and L3 blob `c219344d8b902bc5053adbdc2328a3147af8f7bf` still govern the candidate.

## Conformance semantics

- [ ] Product §11 + L2 §13 forbidden-inference union is executable and fail-closed, including ephemeral-only truth.
- [ ] v4.1–v4.5 semantic owners remain separate: no duplicate execution, migration, design/DAG/profile, build/deploy or operations/incident owner is created.
- [ ] F0–F3, Assurance/Review/provenance, Dispatch/Handoff, Validation and Release are referenced rather than reimplemented.
- [ ] Historical evidence retains original identity/schema/result; no retroactive v4.6 records/currentness are manufactured.
- [ ] Fast Path reduces ceremony only; no required authority/currentness/Validation/Review/Candidate/Release/side-effect gate is waived.
- [ ] Non-material Fast Path does not require empty Intent/Assumption or Skill records.

## T06 fidelity

- [ ] Canonical packet SHA-256 remains `33f9c9aad5d28d58e73af52326bc8bffb61a0eb4e44cb9ff49ce16b19ba6f46b` where referenced.
- [ ] Builder fixture/static PASS is not relabeled as the real external execution claim.
- [ ] The actually executed fresh logical reconstruction PASS is bound to its exact T06 subject/evidence.
- [ ] Same transport/provider/model facts are not treated as automatic independence proof.
- [ ] Unexecuted model/provider sweep, fresh transport-account and production side-effect dimensions remain NOT_RUN unless new exact evidence exists.

## Closure-input boundary

- [ ] `CLOSURE_INPUTS.md` records exact subject and owner-issued CI/Validation/Review evidence, not predicted results.
- [ ] Missing/stale evidence and unresolved P0/P1 remain visible as NOT_RUN/BLOCKED/UNKNOWN and are not downgraded.
- [ ] No Candidate Freeze, Version Closure verdict, Release Qualification/READY, repository integration authorization or v4.7 convergence semantics are issued.
- [ ] PR/task PASS is never equated to Version Closure or Release PASS.

## Required evidence before merge authorization

- [ ] Focused integrated T08 conformance passes on the exact candidate HEAD.
- [ ] Applicable verify-standard CI is exact-head current.
- [ ] Separate T08 exact-subject Validation is complete and current.
- [ ] Fresh Independent Review is genuinely independent of Builder/Validator and binds the same exact candidate.
- [ ] P0/P1 handling follows Task Pack failure rules.

Reviewer terminal must report exact reviewed HEAD/tree/live target, scope, evidence bindings, findings by severity, and only the authorization permitted by the governing review/merge protocol. It must not perform Version Closure or Release Qualification.
