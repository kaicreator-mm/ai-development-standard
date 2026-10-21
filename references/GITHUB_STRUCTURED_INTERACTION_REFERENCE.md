# GitHub Structured Interaction — v3 operations and v4 reports

**Current source:** [GitHub Agent Interaction Protocol §16](../standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md). Under a v4.15 effective pin, new ADS consumers emit **one** canonical Markdown+YAML form for a Work Item body, an Issue mutation intent, a canonical Agent Event comment, or a Task Report comment. V3 Work Item/Intent/Event stay current; v3 reports are historical read-only and new reports use v4. Older v1/v2 wrappers remain unsupported, with no automatic migration requirement. Existing GitHub native data, Review/Validation/Release evidence and Task/Dispatch/Claim rules remain authoritative.

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

\`kind\` selects the machine contract; \`data\` contains **only the kind's fields**. For these non-report operations, \`schema\` remains \`ads/github/v3\`; v4.15 reports alone use \`ads/github/v4\`. The minimal common envelope is validated by \`schemas/github/v4.14/structured-interaction.schema.json\`, not a separate schema per REST verb. The direct Task payload is validated by the existing \`schemas/task-contract.schema.json\`. Nine other Issue profiles use declared `oneOf` contract definitions in the canonical Draft 2020-12 Schema, not Python-only required-field maps. Historical Issue bodies need not be rewritten.

The reference verifier uses **safe nested YAML mappings/lists** with duplicate-key, alias, anchor, unsafe-tag, timestamp and input-size checks, rather than a hand-built YAML dialect. It rejects duplicate keys, unsafe tags, aliases, anchors, implicit timestamps and malformed syntax; ordinary YAML flow mappings/sequences are accepted if they satisfy the same JSON Schema. Long human explanations belong after the structured block as Markdown.

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

## 4. Report — v4.15 strict observational profiles

The exact executable examples are [summary](../tests/fixtures/v415/summary.json), [manifest-free feedback](../tests/fixtures/v415/feedback.json), and [correction notice](../tests/fixtures/v415/correction.json). They are **offline illustrative fixtures**, not observed GitHub publications or runtime PASS. Serialize each as one leading `<!-- ads:github -->` and one YAML fence with exactly schema/kind/data. Human Markdown follows the fence and is never machine authority. Exact required keys/typing are owned by [the v4 report-only schema](../schemas/github/v4.15/report.schema.json) and Protocol §16.5.

The summary has explicit UNKNOWN/null cost and per-metric epistemic/currentness, leaf aggregation, actual-subject verifier references and private immutable manifest ref/digest. Feedback carries actual publisher/ADS SHAs and distinct use phase, with no manifest. A correction carries only target+reason+notice; it does not authenticate cancellation ownership or replace facts. Same GitHub transport login is not logical publisher ownership.

V3 `EVIDENCE_UPDATE` and `TASK_LEARNING` map to a new immutable revision of an existing v4 summary with the same report_id/Attempt, a new manifest ref/hash and late source / Task Learning v2 refs. Missing predecessor is INSUFFICIENT_EVIDENCE. Correction is a separate notice and replacement is a source-profile revision. Level-1 `TASK_LEARNING=NONE_MATERIAL | ref` remains unchanged.

Compute public `SHA256(RFC8785_JCS(validated data))` into the external readback receipt/index; never place a self digest or own future comment URL/ID in data. Dedupe identity includes owning Issue, namespace, report_id, revision and kind. Edited/conflicting same-comment/key evidence fails closed; unknown edit/original evidence remains UNKNOWN. The private manifest hash is separate and is not validated by this public digest. Tally's GitHub-only reader neither needs nor may fetch private task-meta contents.

The unchanged v3 report schema/examples at the v4.14 immutable pin remain historical read-only for v4.15. Do not emit new v3 reports under v4.15; do not migrate live v3 Task/Intent/Event or mutate their offline registry.

## 5. Machine-checkable operation and authority boundaries

| \`kind\` | Current data contract | Last authority/source check |
| --- | --- | --- |
| \`work_item\` | Profile-required keys; Task Contract Schema for task | Owning Issue body plus GitHub native Type/Labels/Dependencies/Claim |
| \`intent\` | \`schemas/github/v4.14/structured-interaction.schema.json\`, operation-specific payload, prior source ref | Existing GitHub Work Item transition/DAG/Claim rules; API write outcome |
| \`event\` | Direct existing Agent Event v2 schema | Existing §8.1 admission and source-specific Review/Validation truth |
| \`report\` | \`schemas/github/v4.15/report.schema.json\`, strict summary/feedback/correction profiles (v3 reports historical-only) | OSS/object readback/ACL, real GitHub comment readback, published revisions |

The parser never invokes a GitHub API mutation. Its CLI is:

\`\`\`text
python scripts/verify_github_structured_interaction.py file.md --kind work_item
python scripts/verify_github_structured_interaction.py file.md --kind event
\`\`\`

## 6. Failure and optimization oracles

1. Current v3 work item/event/intent, or v4 report with the common marker and correct pair → \`SHAPE_VALID_ONLY\`; never \`PASS\` or \`MUTATED\`.
2. Wrong first-line marker, old wrapper, duplicate marker, unknown kind, arbitrary YAML aliases/tags/duplicate keys or invalid nested value → \`INVALID_SCHEMA\`.
3. Old free-text Markdown discussion is still just \`UNSTRUCTURED_DISCUSSION\`, **not** an alternative normative operation.
4. Task Contract missing baseline/goal/gates or other profile missing required keys → invalid, even if Markdown prose mentions those values.
5. Existing Issue mutation without source-currentness/ref, malformed canonical native state, forbidden \`gate:pass\` label, no-op status, self-dependency → invalid.
6. \`kind: intent\` with \`ISSUE_COMMENT_EVENT\` or \`ISSUE_COMMENT_REPORT\` → invalid. Canonical comments are direct kinds, not separate operation proposals.
7. Event \`data\` lacks required original Event v2 fields or mismatches the actual Issue target → invalid.
8. Report contains duplicate arbitrary publication key field, invalid digest, unsupported report kind, v4 correction without its typed target/notice or short-lived signing secret in locator → invalid.
9. Two apparently valid simultaneous source-change intents → static shape can pass **both**; only the existing authorized GitHub writer may commit one from the current state; other must be rejected or retried after re-read.
10. Report comment POST timeout/duplicate after actual GitHub acceptance → derive key from source Issue/id/revision, read back real comments, reuse identical manifest digest or detect conflict. No false exactly-once guarantee.
11. A malicious quoted YAML block in human prose is merely untrusted content, not a canonical admitted event.
12. No old adapter/readback implementation, bulk migration, per-tool Issue spam or duplicate Task status storage is required.

**Intentional limit:** real GitHub source admission and OSS write/retry are implementation responsibilities (e.g. future task-meta), not proven by schema shape/CI. A consumer must resolve its exact effective immutable pin and per-kind wire disposition; Schema never activates an adoption.


## 7. Reproducible v4.15 source checks

```text
python tests/test_v415_report.py
python scripts/test_github_structured_interaction.py
python scripts/verify_github_structured_interaction.py report.md --kind report --effective-pin v4.15 --writing --data-digest
```

The first command executes RFC8785 vectors, strict positive/negative profiles, original v3 blob identity/offline registry, compatibility, immutable revisions and edit/conflict behavior. The second retains the existing v4.14 conformance suite. Neither performs a real publication, reads private manifests, proves Tally/task-meta runtime, authenticates correction authority or passes a Task/Release gate. Native CI coverage is only the commands actually present in its workflow; a source-bound CI success does not imply the new standalone test command ran there.

## 8. GitHub-only consumer and feedback conformance (S03)

Normative owner: Protocol §16.6. Detailed source contract:
[`GITHUB_ONLY_CONSUMER_CONTRACT.md`](../docs/implementation/4.15.0/GITHUB_ONLY_CONSUMER_CONTRACT.md).

```text
python tests/test_v415_consumer.py
```

This exercises existing wire/digest/disposition helpers and a tests-only finite
oracle for complete pagination, bounded retries, native edit/conflict/currentness,
source/namespace/Issue/Task-bound correction and manifest-free feedback. Its
positive outputs are observations, never engineering PASS or real runtime proof.
Negative cases include shape-valid wrong-target notices, shared-login different
publishers, unavailable effective grants and missing egress/readback evidence.
No verifier/schema change or private fetch is introduced. S02's correction shape
finding remains OPEN; consumer application checks do not repair that helper.
Downstream same-build TypeScript/grant/egress evidence remains deferred NOT_RUN.
These standalone cases require actual explicit execution; generic native CI
success does not imply this command ran.
