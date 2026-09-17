# Agent Event Comment Template

Use this format for machine-readable Builder / Reviewer / Validator / merge-control events in Task or Validation Issue comments.

```html
<!-- ai-dev:event:v1 -->
```

```yaml
schema: ai-dev/event-v1
event: <TASK_CLAIMED | IMPLEMENTATION_READY | REVIEW_RESULT | FIX_APPLIED | VALIDATION_REQUEST | VALIDATION_RESULT | BLOCKER_REPORTED | DEPENDENCY_CHANGED | MERGE_RESULT>
actor_role: <builder | reviewer | validator | merge-controller>
task: "#<issue>"
pr: "#<pr>" # omit when not applicable
sha: "<40-char-sha>"
status: <PASS | FAIL | BLOCKED | NOT_RUN | NOT_APPLICABLE>
next_state: <planned | ready | implementing | review-ready | reviewing | changes-requested | validation-needed | merge-ready | blocked | done> # omit when not applicable
```

Then add event-specific fields and human-readable details.

## IMPLEMENTATION_READY example

```yaml
schema: ai-dev/event-v1
event: IMPLEMENTATION_READY
actor_role: builder
task: "#31"
pr: "#42"
sha: "<head-sha>"
status: PASS
validation:
  unit: PASS
  contract: PASS
  integration: NOT_APPLICABLE
next_state: review-ready
```

## REVIEW_RESULT example

```yaml
schema: ai-dev/event-v1
event: REVIEW_RESULT
actor_role: reviewer
task: "#31"
pr: "#42"
sha: "<reviewed-head-sha>"
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
