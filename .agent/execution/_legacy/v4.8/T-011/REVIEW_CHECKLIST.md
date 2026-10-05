# T-011 Fresh Review Checklist

Review applies only after exact-subject independent Validation has qualified the current Builder candidate. The Reviewer must be genuinely independent from Builder and Validator conclusions and must re-read live currentness before terminal publication.

## Identity / currentness

- [ ] PR HEAD/tree exactly match the subject under review.
- [ ] Candidate descends from the JIT base recorded in `.agent/execution/T-011/MANIFEST.yaml` or any rebind is explicitly authorized and reflected in a successor pack.
- [ ] Task Pack blob and L3 blob match the Execution Pack.
- [ ] #517 native dependencies are still canonical and satisfied.
- [ ] Builder diff is limited to `scripts/test_v48_orchestration_dogfood.py` and `docs/implementation/4.8.0/dogfood/orchestration/**`.
- [ ] No Product/L2/DAG, normative standard/schema, CI/workflow, T-014 or release/closure authority was modified.

## Frozen semantic boundaries

- [ ] Hard eligibility runs before optional ranking; INELIGIBLE/UNKNOWN never reaches ranking/admission.
- [ ] Fresh/stale/missing Availability semantics remain derived and fail closed for hard requirements.
- [ ] Reviewer/Validator independence conflict is a hard rejection.
- [ ] Composite work + scarce-resource admission remains all-or-none and capacity-N/N=1 invariants hold.
- [ ] Existing Interchange v1 is reused; duplicate/replay/loss/conflicting replay preserve idempotency/fail-closed semantics.
- [ ] Transport ACK/progress/heartbeat is non-authoritative.
- [ ] Accepted Claim remains T-017 Start Record; current-state projection is derived visibility only.
- [ ] Crash/restart reconstructs authoritative state without transient chat/queue dependence.
- [ ] Timeout/stale replacement remains fail closed on ambiguity.
- [ ] Bounded executor succeeds only when eligible/current/authorized and escalates on semantic ambiguity.
- [ ] No provider/model label becomes authorization, correctness verdict or universal quality score.

## Evidence integrity

- [ ] Every ODF scenario has exact input/oracle/observed outcome and evidence classification.
- [ ] `SYNTHETIC_DETERMINISTIC` is never presented as repository-real or external-real evidence.
- [ ] External host/device/provider/runtime claims have exact-subject independent environment Validation; otherwise they are `NOT_RUN/BLOCKED`.
- [ ] Measurements are descriptive and do not support blanket strong→low-cost routing, universal Agent ranking or savings claims without comparable methodology.
- [ ] Limitations/counterevidence are preserved rather than hidden by a PASS summary.

## Validation / regression

- [ ] Focused T-011 dogfood command passes on exact candidate.
- [ ] T-007 contract/historical compatibility regression remains passing.
- [ ] T-008 scheduling/resource conformance remains passing.
- [ ] T-009 replay/restart conformance remains passing.
- [ ] T-017 execution ownership/start-timeout conformance remains passing.
- [ ] Repository verifier passes.
- [ ] Independent Validation covers repository-real scenario/integration claims and binds exact candidate SHA/tree.

## Terminal boundary

A PASS may authorize T-011 concern completion/integration only. It must not state or imply T-014 PASS, Version Closure, Release Qualification or Release PASS.

If any scenario exposes a Frozen semantic gap that requires authority/public-contract change, Reviewer disposition must preserve the failure and route to `ARCHITECTURE_AMENDMENT_REQUIRED` or separately authorized repair rather than endorsing an in-task semantic patch.
