# Research Demo Validation Checklist

Use this checklist before accepting a Research Demo as Architecture Evidence.

## A. Trigger / Scope

- [ ] The Demo resolves a material Architecture UNKNOWN.
- [ ] Static/source/design evidence was insufficient.
- [ ] The Demo is not being created merely because every Task is expected to have one.
- [ ] Frozen PRD / candidate architecture references are explicit.
- [ ] Baseline SHA and research branch are explicit.
- [ ] In scope / out of scope are explicit.

## B. Hypothesis

- [ ] The Hypothesis is falsifiable.
- [ ] Expected observable behavior is explicit.
- [ ] PASS/FAIL/BLOCKED can be determined objectively.
- [ ] The Issue does not use vague goals such as “see if it works” as the acceptance criterion.

## C. Real boundary

- [ ] The actual boundary/component under test is real.
- [ ] Only unrelated dependencies are replaced with deterministic fakes.
- [ ] The report lists Real Under Test and Deterministic Fakes.
- [ ] An in-memory/same-process substitute is not being used to claim real persistence/process/platform evidence.

## D. Determinism / Observability

- [ ] Inputs are controlled.
- [ ] Model/tool behavior is deterministic unless real provider behavior is the subject of the test.
- [ ] Relevant clocks/randomness are controlled where needed.
- [ ] Counters/state/digests directly prove the target invariant.
- [ ] Assertions do more than compare a final return value.

## E. Scenario coverage

- [ ] Positive/happy path executed.
- [ ] Boundary case executed.
- [ ] Negative/invalid case executed.
- [ ] Fail-closed authority behavior tested where relevant.
- [ ] Failure path executed.
- [ ] Recovery/retry path executed when durability/recovery is part of the hypothesis.

## F. Evidence Strength

- [ ] Evidence Strength is declared: E1 / E2 / E3.
- [ ] E1 uses focused executable tests and exact-SHA clean/repository validation.
- [ ] E2 uses the real internal integration seams under test.
- [ ] E3 uses the required real process/persistence/platform/Build Host environment.
- [ ] The evidence level is sufficient for the claim and not artificially weakened for convenience.

## G. Identity

- [ ] Source baseline exact SHA recorded.
- [ ] Consumed dependency/research exact SHAs recorded.
- [ ] Final research HEAD exact SHA recorded.
- [ ] Relevant runtime/toolchain/platform identity recorded for E2/E3.
- [ ] Evidence belongs to the final HEAD; old-SHA PASS was not inherited silently.

## H. Research scope integrity

- [ ] Production runtime/public contract was not silently rewritten.
- [ ] Unrelated features were not added.
- [ ] Missing production seams are recorded as follow-up Issues.
- [ ] Tests/assertions/gates were not weakened to obtain PASS.
- [ ] Completion is based on Evidence complete, not Feature complete.

## I. Report quality

- [ ] Result is PASS / FAIL / BLOCKED.
- [ ] Expected vs Actual is documented.
- [ ] What was proven is documented.
- [ ] **What was NOT proven is documented.**
- [ ] Negative/failure evidence is documented.
- [ ] KEEP / ADAPT / DROP is documented.
- [ ] Architecture implication is documented without overclaiming.
- [ ] Any Architecture Contradiction is distinguished from failure of one technical approach.

## J. Promotion / Reuse

- [ ] Reusable invariant/contract/fixture/reference test is identified.
- [ ] The whole research branch is not assumed to be production code.
- [ ] L2/ADR references exact evidence identity.
- [ ] Production implementation will follow Frozen L2/Task contracts and revalidate production behavior.

## Acceptance

A Research Demo is acceptable Architecture Evidence only when the checklist is materially satisfied for the claim being made.

Missing Hypothesis, real-boundary evidence, negative/failure evidence, exact identity, or `What was NOT proven` is normally blocking for Architecture Evidence acceptance.
