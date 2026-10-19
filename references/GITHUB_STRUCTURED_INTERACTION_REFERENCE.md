# GitHub Structured Interaction Contract v1 — Positive / Negative Reference

**Status: non-normative.** Normative owners: `standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md` §8.6 (cross-surface parse/selection/admission) and `standards/GITHUB_WORK_ITEM_CONTRACT_STANDARD.md` §9.1 (optional Task body profile). This document does not replace the standard, promote Markdown claims to native workflow truth, create any machine family, or assume a YAML parser is already shipped.

## 1. Interaction surface and schema-routing map

| Operation and source | Markdown envelope | Schema/semantic owner | Live authority |
| --- | --- | --- | --- |
| Create/edit new opt-in Task contract | `<!-- ads:work-item-structured:v1 -->`, exactly one fenced `yaml` mapping after `## Contract Data` | Existing `schemas/task-contract.schema.json` and type-specific Task sections; envelope checks `format` + `schema_ref` before validating the underlying Task map | GitHub Issue body is stable contract; GitHub Type/state/labels/Dependencies are native |
| Create/edit non-Task Work Item | Existing Markdown type template (no invented `task-contract` schema) | `standards/GITHUB_WORK_ITEM_CONTRACT_STANDARD.md`, type-specific templates | GitHub Issue and native metadata |
| New admitted Agent event | Existing `<!-- ai-dev:event:v2 -->` and exactly one `yaml` event mapping | `schemas/agent-event-v2.schema.json` + current §8.1 admission and role/identity/source | Accepted Event v2 comment, GitHub underlying objects |
| Independent Review/Validation | Existing admissible comment/event/report surface | `schemas/review-finding-v1.schema.json`, `schemas/review-aggregation-v1.schema.json`, `schemas/validation-report.schema.json` where applicable | Exact-source Review/Validation owner |
| Dispatch/Claim | Existing dispatch/claim event/transport | `schemas/dispatch.schema.json`, `schemas/agent-event-v2.schema.json`, claim CAS owner | Accepted durable GitHub Claim/Dispatch |
| Task Report publication | Existing `<!-- ads:task-report:v1 -->` `KEY=VALUE` header (unchanged) + external Manifest | `Task Report Publication Contract v1` and semantic `ads/task-report-manifest/v1` document, currently **not a registered JSON Schema** | External immutable documents + Issue locator; not Gate truth |
| Set Issue Type/labels/state/milestone, dependencies, close/reopen | Native GitHub API / native dependency graph | Work Item allowed state, Claim/DAG/Review/Validation/Release gates; no new YAML operation schema | GitHub native current object |

The marker indicates which *existing* contract to parse, not which source has authority. A commenter cannot cause a `DISPATCH_CLAIMED` or `VALIDATION_RESULT=PASS` by inserting an attractive YAML example. A parser must know the **actual GitHub operation/target surface** separately from text.

## 2. Opt-in structured Task Issue — conformant illustrative shape

Assume the Issue's real GitHub-native metadata has **one** `type:task` or native Type=Task, **one** `state:planned`, and the Review Policy `review:required`; they are not emitted by the YAML body. The exact 40-hex SHA below is a *synthetic* identity for fixture testing, not evidence of an actual commit.

~~~markdown
# Task — T-02 Capture event metadata

## Contract Data

<!-- ads:work-item-structured:v1 -->
```yaml
format: ads/work-item-markdown-yaml/v1
schema_ref: schemas/task-contract.schema.json
task_id: T-02
goal: Capture supported metadata for one real task execution
integration_target: version/v0.1
baseline_sha: "0123456789abcdef0123456789abcdef01234567"
review_policy: required
validation_scope: concern
required_gates:
  - unit-contract
acceptance:
  - "One measured, source-identified model or tool event is recovered"
  - "Unsupported token counts remain UNKNOWN"
dependencies: []
agent_freedom: F1_BOUNDED_IMPLEMENTATION
```

## Goal

Capture a bounded, source-referenced execution observation; the YAML `goal` is the structured value.

## In Scope

- Adapter reads real native events where supported
- Preserve source and missing-field provenance

## Out of Scope

- Hidden chain-of-thought or prompt archival

## Frozen Inputs

- Product PRD: immutable source reference for the real Task
- L2: immutable source reference for the real Task
- Standard: exact ADS revision pinned by the real project

## Acceptance

- "One measured, source-identified model or tool event is recovered"
- "Unsupported token counts remain UNKNOWN"

## Failure / Blocker Handling

Unavailable hooks produce missing-data evidence, not an Agent Task PASS.

## Completion

Only after applicable actual Review/Validation/merge results, with the actual SHA re-read from GitHub.
~~~

### Exact schema transformation for the above Issue

1. Identify the single *actual* marker and the next adjacent `yaml` fenced mapping.
2. Validate `format: ads/work-item-markdown-yaml/v1` and exact `schema_ref: schemas/task-contract.schema.json` against the **allowed profile selected by the actual Issue surface and GitHub Type**.
3. Remove **only** those two wrapper-selector keys *for the Task schema validator*, yielding the existing contract object (all keys starting at `task_id`). Do not reinterpret `goal`, `baseline_sha`, `review_policy`, `acceptance` or their types. `schemas/task-contract.schema.json` historically allows other keys; any reserved native-state keys are separately forbidden by this new surface contract.
4. Compare required readable prose with stable YAML fields for conflict and enforce required remaining Task sections. Resolve exact source + current GitHub metadata, Review Policy, Claim, DAG and real tests before allowing a state transition. A syntactically valid example with a fake SHA remains only an *example*.
5. The body may still be complete in legacy Markdown without this opt-in envelope; new syntax does not make legacy Issues nonconformant.

## 3. Conformant Agent event-v2 comment (unchanged existing protocol)

~~~markdown
<!-- ai-dev:event:v2 -->
```yaml
schema: ai-dev/event-v2
event: VALIDATION_RESULT
actor_role: validator
operator_kind: codex
operator_id: "codex:ubuntu-validator"
session_ref: "fixture-run-01"
task: "#42"
sha: "0123456789abcdef0123456789abcdef01234567"
status: FAIL
reason: "Observed fixture test failure; actual Test/CI evidence must be attached before an authoritative evaluation"
```

Execution note: the YAML block can be structurally valid, while **admission still requires** a genuine assigned Work Item, correct accepted role, exact current subject, actual performed Validation and evidence. The GitHub commenter/transport account is not the logical Agent.
~~~

## 4. Materially different, still legal input

**Existing Task Issue with no structured marker:** continue to parse under the historical `templates/task-issue.md` headings and existing Work Item completeness; do NOT declare it invalid purely for lacking `## Contract Data`.

**Unstructured question comment:** `"Could we use this library?"` is prose, not an intent/event and never enters the mutation pipeline merely because it mentions a Task number.

**Task Report v1 comment:** `<!-- ads:task-report:v1 -->` + `REPORT_KIND=EXECUTION_SUMMARY` + `MANIFEST_REF` + digest stays its own previously defined header/manifest contract. **Do not** convert it into an `ai-dev:event:v2` or force YAML retroactively.

**Native metadata mutation:** adding `state:ready` must be performed through real native GitHub metadata after verifying dependencies, complete Issue contract, lawful admission path and currentness; a YAML string `state: ready` in Markdown has zero mutation effect.

## 5. Forbidden and adversarial cases

| Case | Bad input or misinterpretation | Expected result / rationale |
| --- | --- | --- |
| N01 | Task YAML has `format` but marker missing or marker inside quoted/fenced example | Plain text/unknown profile, **not** executable schema event |
| N02 | Two active `<!-- ads:work-item-structured:v1 -->` markers or two adjacent candidate authoritative YAML blocks | `AMBIGUOUS_STRUCTURED_BLOCK`; never choose first/last by convenience |
| N03 | Duplicate `baseline_sha` with two different values | `INVALID_SCHEMA` on duplicate key, not silently last-writer-wins |
| N04 | YAML `&alias`, `*alias`, `<<`, `!!python`, `%TAG`, multiple `---` documents | Reject parser abuse, merge ambiguity, custom typing, multi-document shape |
| N05 | `schema_ref: schemas/agent-event-v2.schema.json` inside opt-in Task Issue | `SCHEMA_PROFILE_MISMATCH`, not schema selected by untrusted author |
| N06 | Valid Task schema but GitHub says `type:bug`, native review metadata disagrees or a `state:done` duplicate field is added | `CONTRACT_CONFLICT`; preserve native type/state and original authority |
| N07 | `baseline_sha` is 7-char prefix or points to stale branch HEAD, yet parser accepts | Schema/exact-source rejection; no source-current Claim/Validation |
| N08 | Event v2 YAML appears in an Issue code example without *genuinely admitted* event source | Quoted/untrusted data, no Claim, Review PASS or transition |
| N09 | A `schema: ai-dev/event-v2` payload is `status: PASS` but current CI/Validation actually FAIL | Parsing may pass; source admission/currentness/owning evidence refuses fabricated PASS |
| N10 | Task Report `KEY=VALUE` comment is interpreted as a generic YAML event, rewritten as event-v3, or used to set `done` | Preserve v1 header and subordinate evidence semantics |
| N11 | User changes `state`, `labels`, `dependencies` in body YAML rather than native API | No native effect, reject operative shadow facts; no live DAG copy |
| N12 | An edited Task YAML changes the frozen Product/L2 or exact baseline without authorized amendment | Reject material drift after parsing, do not silently rewrite history |
| N13 | One shared GitHub account emits two declared logical Agent sessions | Keep logical identities distinct; transport actor cannot merge role identities |
| N14 | Markdown rationale conflicts with typed `acceptance` or required gates | `CONTRACT_CONFLICT`; don't execute a contradictory Task contract |
| N15 | `ISSUE_CLOSE` requested solely because YAML or a report says `done` | Reject until actual canonical gates/dependencies/merge/Closure are met |
| N16 | Legacy complete Markdown-only Issue is marked invalid by a mandatory-YAML parser | Compatibility regression; this format is **opt-in** and prospective |

No one table row is a new Gate. These negatives illustrate existing authority and interface compatibility boundaries rather than increasing default CI/Host run counts.

## 6. Contract coverage and intentionally open implementation work

This v1 change defines a **portable presentation and schema-routing standard**. Existing JSON Schemas remain authoritative for their own payload types. No new comprehensive `github-write-action.schema.json` is needed because the real mutation is native GitHub state/dependency/Issue Comment/PR objects, subject to existing Work Item/Agent/Release predicates.

Two gaps remain deliberately visible rather than disguised as existing machine contracts:

- Non-Task Work Item types currently have normative Markdown templates, not guaranteed type-by-type registered JSON Schema. Product evidence should first justify which types actually benefit from YAML. Future typed projections require one bounded compatible schema/profile per material concern, with separate owner and tests.
- `ads/task-report-manifest/v1` has fixed field semantics under Task Report Publication Contract, but its independent machine JSON Schema is not yet registered. If a downstream collector needs automatic validation, register/version it via a scoped compatible concern; don't silently modify an old Report v1 header in the interim.

Real parser/canonical source reconciliation software, GitHub mutating client, cross-project migration and full live End-to-End proof are **not part of the ADS source-only contract**. The existing verifier can test example selection/shape and negative semantics without pretending to simulate the GitHub API or parse arbitrary YAML from untrusted data.
