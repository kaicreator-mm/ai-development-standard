# Research Demo Report

## Identity

- Research Issue: `#...`
- Baseline SHA: `<sha>`
- Consumed dependency SHAs: `<sha...>`
- Final research HEAD: `<sha>`
- Evidence Strength: `E1 | E2 | E3`
- Environment/runtime/toolchain: `<...>`

## Hypothesis

<Exact falsifiable hypothesis from the Issue.>

## Result

`PASS | FAIL | BLOCKED`

## Expected vs Actual

| Item | Expected | Actual | Status |
|---|---|---|---|
| ... | ... | ... | PASS/FAIL/BLOCKED |

## Observed Evidence

- counters/state/digests:
- commands:
- test results:
- real environment/process/platform evidence when required:

## Scenario Results

### Positive

...

### Boundary

...

### Negative / Fail Closed

...

### Failure / Recovery

...

## Real Under Test

- ...

## Deterministic Fakes

- ...

## What was proven

- ...

## What was NOT proven

- ...

Do not infer untested production scale, multi-platform behavior, security, performance, distributed consistency or release readiness.

## Findings

### KEEP

- ...

### ADAPT

- ...

### DROP

- ...

## Architecture Implications

<What L2/ADR decision this evidence supports or rejects.>

## Architecture Contradiction

`NONE | REPORTED`

If reported, explain why the contradiction is in the Frozen PRD/product requirement itself rather than merely in the tested technical approach.

## Production Seams / Follow-up Issues

- ...

## Reusable Reference Artifacts

- validated contracts/schemas:
- fixtures/scenarios:
- reference tests:
- failure/recovery semantics:

Do not treat the whole research branch as production code by default.

## Closeout Statement

The research task is complete when required evidence is complete. Unimplemented production API/migration/monitoring/packaging work is outside this Demo unless explicitly part of the Hypothesis.
