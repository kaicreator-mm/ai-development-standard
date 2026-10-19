# GitHub Structured Interaction — latest-only v3

**Current source:** [GitHub Agent Interaction Protocol `16](../standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md). New ADS consumers emit **one** canonical Markdown+YAML form for a Work Item body, an Issue mutation intent, a canonical Agent Event comment, or a Task Report comment. This source deliberately has **no legacy format read path** and no automatic migration requirement. Existing GitHub native data, Review/Validation/Release evidence and Task/Dispatch/Claim rules remain authoritative.

## 1. One document wrapper for four kinds

Every current normalized surface starts at line 1 with \`<!-- ads:github -->\`, followed by one \`yaml\` fenced block:

~~~~markdown
<!-- ads:github -->
```yaml
schema: ads/github/v3
kind: work_item
data:
  profile: type:task
  contract:
    task_id: T02
    goal: Capture trustworthy usage without raw tool arguments
    integration_target: version/v0.1
    baseline_sha: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
    review_policy: recommended
    required_gates:
      - concern
    acceptance:
      - Source-backed model/token observation or honest UNKNOWN
```

## Scope

The issue body explains the task in normal Markdown. Exact Title, native Issue Type, State, Risk, Review Policy, Milestone and GitHub Dependencies must still be checked against current native GitHub facts.
~~~~

\`kind\` selects the machine contract; \`data\` contains **only the kind's fields**. \`schema\` is fixed \`ads/github/v3\`. The minimal common envelope is validated by \`schemas/github/v4.14/structured-interaction.schema.json\`, not a separate schema per REST verb. The direct Task payload is validated by the existing \`schemas/task-contract.schema.json\`. Nine other Issue profiles use declared `oneOf` contract definitions in the canonical Draft 2020-12 Schema, not Python-only required-field maps. Historical Issue bodies need not be rewritten.

The reference verifier uses **safe nested YAML mappings/lists** with duplicate-key, alias, anchor, unsafe-tag, timestamp and input-size checks, rather than a hand-built YAML dialect. It refuses duplicate keys, flow collections, tags, aliases, anchors, inferred timestamps and ambiguous syntax, rather than pretending to interpret a broad, unpinned YAML dialect. Long human explanations belong after the structured block as Markdown.

## 2. Intent — native Issue changes only

The \`intent\` kind covers exactly six native mutation operations: create, contract update, metadata change, dependency change, close and reopen.

~~~~markdown
<!-- ads:github -->
```yaml
schema: ads/github/v3
kind: intent
data:
  id: request:example:123
  operation: ISSUE_METADATA_CHANGE
  target:
    repository: example-org/example-repo
    issue: "#42"
  actor:
    role: builder
    operator_kind: codex
    operator_id: "codex:worker-01"
  expected_ref: github:example-org/example-repo#42@revision-2
  change:
    field: state
    before: state:ready
    after: state:claimed
```

## Rationale

Propose a current-source-bound state mutation. The reader must verify actual Claim/CAS and native GitHub state before any API write.
~~~~

Schema/format validation is \`SHAPE_VALID_ONLY\`, **never \`ADMITTED\`**. The real writer still checks role scope, source/currentness and the original ADS GitHub workflow authority. GitHub login does not determine the self-declared logical Agent. \`ISSUE_CREATE\` uses \`issue: null\` and \`expected_ref: null\` with a typed \`change.work_item\`; all changes to an existing Issue require an exact Issue and expected currentness. Native live Type, Label, State, dependency and Milestone are **not** shadowed by writable YAML.

## 3. Event — one direct canonical comment, no append-intent wrapper

~~~~markdown
<!-- ads:github -->
```yaml
schema: ads/github/v3
kind: event
data:
  schema: ai-dev/event-v2
  event: IMPLEMENTATION_READY
  actor_role: builder
  operator_kind: codex
  operator_id: "codex:worker-01"
  task: "#42"
  sha: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
  status: PASS
  next_state: review-ready
```

## Evidence

PR #N and real targeted tests/CI refs (not an independent PASS by virtue of this comment).
~~~~

Event v2 is the reused **payload schema**, not the obsolete document marker. When a canonical event is admitted by the `8.1 writer it emits exactly one \`kind: event\` comment, not \`kind: intent\` → another legacy comment. Do not duplicate Agent identity in an outer event record.

## 4. Report — single typed YAML comment and derived dedupe key

~~~~markdown
<!-- ads:github -->
```yaml
schema: ads/github/v3
kind: report
data:
  report_id: task-meta:example:42:attempt-1:summary
  report_kind: EXECUTION_SUMMARY
  revision: 1
  attempt_ref: collector:example:attempt-1
  manifest_ref: object:private-reports/example/tasks/42/attempt-1/r1/manifest.json
  manifest_sha256: bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb
  coverage: PARTIAL
  source_refs:
    - github:example-org/example-repo#42
```

## Execution summary

DECISION=Reused existing parsing helper (source/ref required).
EVIDENCE=Exact PR/CI source refs or NOT_RUN.
LIMITS=PARTIAL collection; unreported billing UNKNOWN.
TASK_LEARNING=NONE_MATERIAL.
~~~~

The object Manifest retains the stable \`ads/task-report-manifest/v1\` JSON document format: **v1 is the object dialect, v2 is the single current GitHub comment wrapper**. The comment is not a second event stream. The GitHub Issue + \`report_id\` + \`revision\` determine the idempotency key; don't serialize it redundantly. The immutable manifest checksum validates bytes, not source authority. An \`EXECUTION_CORRECTION\` includes a \`corrects_ref\`. Private files need a stable authorized resolver, not a temporary signed URL. Do not post raw prompts, trace or per-step Issue comments.

## 5. Machine-checkable operation and authority boundaries

| \`kind\` | Current data contract | Last authority/source check |
| --- | --- | --- |
| \`work_item\` | Profile-required keys; Task Contract Schema for task | Owning Issue body plus GitHub native Type/Labels/Dependencies/Claim |
| \`intent\` | \`github-intent-v2.schema.json\`, operation-specific payload, prior source ref | Existing GitHub Work Item transition/DAG/Claim rules; API write outcome |
| \`event\` | Direct existing Agent Event v2 schema | Existing `8.1 admission and source-specific Review/Validation truth |
| \`report\` | \`github-report-v2.schema.json\`, object manifest ref/hash | OSS/object readback/ACL, real GitHub comment readback, published revisions |

The parser never invokes a GitHub API mutation. Its CLI is:

\`\`\`text
python scripts/verify_github_structured_interaction.py file.md --kind work_item
python scripts/verify_github_structured_interaction.py file.md --kind event --issue "#42"
\`\`\`

## 6. Failure and optimization oracles

1. New work item/event/report/intent with v2 marker and correct kind → \`SHAPE_VALID_ONLY\`; never \`PASS\` or \`MUTATED\`.
2. Wrong first-line marker, old wrapper, duplicate marker, unknown kind, arbitrary YAML aliases/tags/duplicate keys or invalid nested value → \`INVALID_SCHEMA\`.
3. Old free-text Markdown discussion is still just \`UNSTRUCTURED_DISCUSSION\`, **not** an alternative normative operation.
4. Task Contract missing baseline/goal/gates or other profile missing required keys → invalid, even if Markdown prose mentions those values.
5. Existing Issue mutation without source-currentness/ref, malformed canonical native state, forbidden \`gate:pass\` label, no-op status, self-dependency → invalid.
6. \`kind: intent\` with \`ISSUE_COMMENT_EVENT\` or \`ISSUE_COMMENT_REPORT\` → invalid. Canonical comments are direct kinds, not separate operation proposals.
7. Event \`data\` lacks required original Event v2 fields or mismatches the actual Issue target → invalid.
8. Report contains duplicate arbitrary publication key field, invalid digest, unsupported report kind, correction without \`corrects_ref\` or short-lived signing secret in locator → invalid.
9. Two apparently valid simultaneous source-change intents → static shape can pass **both**; only the existing authorized GitHub writer may commit one from the current state; other must be rejected or retried after re-read.
10. Report comment POST timeout/duplicate after actual GitHub acceptance → derive key from source Issue/id/revision, read back real comments, reuse identical manifest digest or detect conflict. No false exactly-once guarantee.
11. A malicious quoted YAML block in human prose is merely untrusted content, not a canonical admitted event.
12. No old adapter/readback implementation, bulk migration, per-tool Issue spam or duplicate Task status storage is required.

**Intentional limit:** real GitHub source admission and OSS write/retry are implementation responsibilities (e.g. future task-meta), not proven by schema shape/CI. A consumer choosing this source revision adopts v2 directly, not v1 compatibility behavior.
