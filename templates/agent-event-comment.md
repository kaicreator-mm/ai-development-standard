# Agent Event Comment Template

Use this format for machine-readable Builder / Reviewer / Validator / merge-control events in Task or Validation Issue comments.

```html
<!-- ai-dev:event:v1 -->
```

```yaml
schema: ai-dev/event-v1
event: <TASK_CLAIMED | IMPLEMENTATION_READY | REVIEW_DECISION | REVIEW_RESULT | FIX_APPLIED | VALIDATION_REQUEST | VALIDATION_RESULT | BLOCKER_REPORTED | DEPENDENCY_CHANGED | MERGE_RESULT>
actor_role: <builder | reviewer | validator | merge-controller>
task: "#<issue>"
pr: "#<pr>" # omit when not applicable
sha: "<40-char-sha>"
status: <PASS | FAIL | BLOCKED | NOT_RUN | NOT_APPLICABLE>
next_state: <planned | ready | implementing | review-ready | reviewing | changes-requested | validation-needed | merge-ready | blocked | done> # omit when not applicable
```

Then add event-specific fields and human-readable details.

## IMPLEMENTATION_READY example

For a Task whose Review Policy routes to a Reviewer:

```yaml
schema: ai-dev/event-v1
event: IMPLEMENTATION_READY
actor_role: builder
task: "#31"
pr: "#42"
sha: "<head-sha>"
status: PASS
review_policy: required
validation:
  unit: PASS
  contract: PASS
  integration: NOT_APPLICABLE
next_state: review-ready
```

For `review:not-required`, or `review:recommended` when the optional review is explicitly skipped, the Task may route directly toward merge readiness once all other required prerequisites are satisfied. Record the policy/decision rather than fabricating a Review PASS.

## REVIEW_DECISION examples

Recommended review explicitly skipped:

```yaml
schema: ai-dev/event-v1
event: REVIEW_DECISION
actor_role: merge-controller
task: "#31"
pr: "#42"
sha: "<head-sha>"
review_policy: recommended
decision: skipped
status: NOT_RUN
reason: <why optional review is not being invoked for this merge candidate>
next_state: merge-ready
```

Review not required by declared policy:

```yaml
schema: ai-dev/event-v1
event: REVIEW_DECISION
actor_role: merge-controller
task: "#31"
pr: "#42"
sha: "<head-sha>"
review_policy: not-required
decision: not-applicable
status: NOT_APPLICABLE
reason: <authority/risk rationale or Task policy reference>
next_state: merge-ready
```

`next_state: merge-ready` is valid only when all other required merge prerequisites are satisfied.

## REVIEW_RESULT example

```yaml
schema: ai-dev/event-v1
event: REVIEW_RESULT
actor_role: reviewer
task: "#31"
pr: "#42"
sha: "<reviewed-head-sha>"
review_policy: required
status: FAIL
findings:
  p0: 0
  p1: 1
  p2: 2
  p3: 0
local_validation_required: false
next_state: changes-requested
```

Human-readable finding details SHOULD follow the payload:

```text
P1 — <finding title>
Location: <file:line or evidence ref>
Expected: <expected contract/behavior>
Actual: <actual implementation/behavior>
Required change: <minimal corrective action>
```

A `recommended` review that is actually performed uses the same `REVIEW_RESULT` event with `review_policy: recommended`. Valid release-significant findings remain engineering facts and must be resolved, explicitly accepted, or deferred according to project authority; they are not erased merely because the review was optional.

## FIX_APPLIED example

```yaml
schema: ai-dev/event-v1
event: FIX_APPLIED
actor_role: builder
task: "#31"
pr: "#42"
sha: "<new-head-sha>"
previous_sha: "<previous-reviewed-sha>"
addresses:
  - P1-1
status: PASS
next_state: review-ready
```

When Review Policy is `not-required`, or optional review will not be resumed, `next_state` SHOULD follow the actual workflow instead of mechanically returning to `review-ready`.

## VALIDATION_REQUEST example

```yaml
schema: ai-dev/event-v1
event: VALIDATION_REQUEST
actor_role: reviewer
task: "#31"
pr: "#42"
sha: "<target-sha>"
status: BLOCKED
gate: platform
environment: windows
reason: <why static review cannot establish the fact>
next_state: validation-needed
```

## VALIDATION_RESULT example

```yaml
schema: ai-dev/event-v1
event: VALIDATION_RESULT
actor_role: validator
task: "#31"
pr: "#42"
sha: "<tested-sha>"
status: PASS
gate: platform
environment: windows
command: <exact command or canonical entrypoint>
exit_code: 0
evidence: <report/log/ref>
next_state: review-ready
```

After validation, route back to `review-ready` only when the Task Review Policy still requires/resumes review. Otherwise route according to the remaining required gates and merge policy.

## MERGE_RESULT example

```yaml
schema: ai-dev/event-v1
event: MERGE_RESULT
actor_role: merge-controller
task: "#31"
pr: "#42"
sha: "<merged/integration-sha>"
status: PASS
target: version/v0.1.0
next_state: done
```

Important history SHOULD be append-oriented. Publish a corrective event instead of silently rewriting a materially wrong prior event.
