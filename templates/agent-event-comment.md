# Agent Event Comment Template

Use this format for machine-readable Planner / Builder / Reviewer / Validator / merge/release-control events in Task, Validation Issue or PR comments.

## Event schema version

New events under standard v3.1+ SHOULD use:

```html
<!-- ai-dev:event:v2 -->
```

Historical `ai-dev:event:v1` comments remain valid history and are read-only compatibility evidence.

## Actor / operator attribution

GitHub comment author is a **transport identity** and may be the same account for ChatGPT Web, Local Agent and human actions. Every v2 event therefore separates workflow role from logical operator identity.

```yaml
schema: ai-dev/event-v2
event: <EVENT_TYPE>

actor_role: <planner | builder | reviewer | validator | merge-controller | release-controller>
operator_kind: <chatgpt-web | codex | claude-code | human | github-actions | woodpecker | other>
operator_id: "<kind>:<project-local-operator-id>"
session_ref: "<opaque session/page/run alias>" # SHOULD be present when concurrent sessions are possible
transport_actor: "github:<account>"            # SHOULD be present when one GitHub account fronts multiple operators

task: "#<issue>"                               # omit when not applicable
pr: "#<pr>"                                    # omit when not applicable
sha: "<40-char-sha>"                           # omit only when no exact code identity applies
status: <PASS | FAIL | BLOCKED | NOT_RUN | NOT_APPLICABLE>
next_state: <planned | ready | implementing | review-ready | reviewing | changes-requested | validation-needed | merge-ready | blocked | done> # omit when not applicable
```

Identity rules:

- `actor_role` = what responsibility this event performs in the workflow.
- `operator_kind` = which execution surface/system actually performed the action.
- `operator_id` = human-readable logical executor identity, stable for the life of that operator context and unique enough within the repository/version execution window.
- `session_ref` = concrete ChatGPT page/conversation alias, local process/run, CI run or worker instance. It is an opaque correlation reference, not a credential.
- `transport_actor` = account/API identity that physically wrote to GitHub. It does **not** prove which logical operator acted.
- Never put tokens, secrets, signed URLs, cookies or other credentials in any identity field.

Recommended operator IDs:

```text
chatgpt-web:web-a
chatgpt-web:web-b
codex:ubuntu-build-01
claude-code:windows-01
woodpecker:runner-01
github-actions:verify-standard
human:owner
```

For two ChatGPT Web pages using the same GitHub account, use distinct `operator_id` and/or `session_ref`, for example:

```text
Builder page  → operator_id=chatgpt-web:web-a, session_ref=forge-v2.9-builder-a
Reviewer page → operator_id=chatgpt-web:web-b, session_ref=forge-v2.9-reviewer-b
```

The same operator MAY act in different roles on different work items. Role and operator identity are different dimensions.

## Role ownership events

For substantial or concurrent work, publish a role claim before beginning:

```yaml
schema: ai-dev/event-v2
event: ROLE_CLAIMED
actor_role: reviewer
operator_kind: chatgpt-web
operator_id: "chatgpt-web:web-b"
session_ref: "reviewer-b-20260918"
transport_actor: "github:kaicreator-mm"
task: "#31"
pr: "#42"
sha: "<head-sha>"
status: NOT_RUN
next_state: reviewing
```

When intentionally handing off or abandoning the role before a normal result event, publish `ROLE_RELEASED` with a short reason.

`ROLE_CLAIMED` is attribution/routing evidence, not a distributed lock. Project policy must explicitly define exclusivity if multiple operators are not allowed to work the same role concurrently.

`TASK_CLAIMED` remains a valid Builder-specific compatibility event; new cross-role flows SHOULD prefer `ROLE_CLAIMED`.

## IMPLEMENTATION_READY example

For a Task whose Review Policy routes to a Reviewer:

```yaml
schema: ai-dev/event-v2
event: IMPLEMENTATION_READY
actor_role: builder
operator_kind: chatgpt-web
operator_id: "chatgpt-web:web-a"
session_ref: "builder-a-20260918"
transport_actor: "github:kaicreator-mm"
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

For `review:not-required`, or `review:recommended` when optional review is explicitly skipped, the Task may route directly toward merge readiness once all other required prerequisites are satisfied. Record the policy/decision rather than fabricating a Review PASS.

## REVIEW_DECISION examples

Recommended review explicitly skipped:

```yaml
schema: ai-dev/event-v2
event: REVIEW_DECISION
actor_role: merge-controller
operator_kind: chatgpt-web
operator_id: "chatgpt-web:web-a"
session_ref: "builder-a-20260918"
transport_actor: "github:kaicreator-mm"
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
schema: ai-dev/event-v2
event: REVIEW_DECISION
actor_role: merge-controller
operator_kind: chatgpt-web
operator_id: "chatgpt-web:web-a"
session_ref: "builder-a-20260918"
transport_actor: "github:kaicreator-mm"
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
schema: ai-dev/event-v2
event: REVIEW_RESULT
actor_role: reviewer
operator_kind: chatgpt-web
operator_id: "chatgpt-web:web-b"
session_ref: "reviewer-b-20260918"
transport_actor: "github:kaicreator-mm"
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

For required Independent Review, Reviewer attribution MUST identify a context independent from the Builder context. The same `transport_actor` is allowed; the logical `operator_id/session_ref` must make the context separation auditable.

## FIX_APPLIED example

```yaml
schema: ai-dev/event-v2
event: FIX_APPLIED
actor_role: builder
operator_kind: codex
operator_id: "codex:ubuntu-build-01"
session_ref: "codex-run-20260918-01"
transport_actor: "github:kaicreator-mm"
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
schema: ai-dev/event-v2
event: VALIDATION_REQUEST
actor_role: reviewer
operator_kind: chatgpt-web
operator_id: "chatgpt-web:web-b"
session_ref: "reviewer-b-20260918"
transport_actor: "github:kaicreator-mm"
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
schema: ai-dev/event-v2
event: VALIDATION_RESULT
actor_role: validator
operator_kind: codex
operator_id: "codex:windows-build-01"
session_ref: "codex-run-20260918-02"
transport_actor: "github:kaicreator-mm"
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
schema: ai-dev/event-v2
event: MERGE_RESULT
actor_role: merge-controller
operator_kind: chatgpt-web
operator_id: "chatgpt-web:web-a"
session_ref: "builder-a-20260918"
transport_actor: "github:kaicreator-mm"
task: "#31"
pr: "#42"
sha: "<merged/integration-sha>"
status: PASS
target: version/v0.1.0
next_state: done
```

Important history SHOULD be append-oriented. Publish a corrective event instead of silently rewriting a materially wrong prior event.