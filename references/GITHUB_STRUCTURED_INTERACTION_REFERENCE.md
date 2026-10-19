# GitHub Structured Interaction Contract v1 — Markdown + YAML reference

**Scope:** ADS opt-in machine-readable *intent* / *Work Item* carriers and read-only validators; this reference is not new GitHub authority, a mandatory migration, a modified Agent Event v2 schema, or a new Task status.

Normative owners are [GitHub Work Item Contract](../standards/GITHUB_WORK_ITEM_CONTRACT_STANDARD.md) `15 and [GitHub Agent Interaction Protocol](../standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md) `8. Machine envelopes: [GitHub operation intent v1](../schemas/github-structured-interaction-v1.schema.json), [Work Item document v1](../schemas/github-work-item-document-v1.schema.json); existing [Agent Event v2](../schemas/agent-event-v2.schema.json), [Task Contract](../schemas/task-contract.schema.json) and [Task Report Publication v1](../standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md) retain their schemas/meaning.

## 1. Parser profile, version binding and migration

- Text remains normal Markdown. An **opt-in authoritative-form candidate** has exactly one first-line literal marker, followed by exactly one bounded `yaml` fenced block and then any human-readable Markdown. The marker is evidence of *intent to emit*, not proof of admission.
- `<!-- ads:work-item:v1 -->` maps to `ads/work-item/v1` (body contract snapshot); `<!-- ads:github-interaction:v1 -->` maps to `ads/github-structured-interaction/v1` (mutation *intent*). A parser checks marker/source schema and operation-specific payload; it MUST NOT act upon a parser result alone.
- Existing `<!-- ai-dev:event:v2 -->` continues with YAML `ai-dev/event-v2` and the original admitted event writer/Claim/Review rules. Existing `<!-- ads:task-report:v1 -->` remains original KEY=VALUE report comment syntax. No silent rewrite of either into a new event family.
- The reference CLI `python scripts/verify_github_structured_interaction.py example.md --surface intent` checks static shape and prints `SHAPE_VALID_ONLY` or `INVALID_SCHEMA`. A plain unmarked comment is `UNSTRUCTURED_DISCUSSION`, never a normative executable operation.
- The bounded dependency-free YAML profile used by the reference CLI supports two-space nested **mappings**, lists of scalar strings/numbers, quoted/unquoted YAML 1.2-like scalars, bool, int and null; rejects duplicate keys, anchors, aliases, tags, multiline scalars, flow collections, implicit timestamps and complex/list-of-map syntax. For a full YAML producer, use a **safe parser** and reject anything outside the common supported profile. Do not infer unsupported YAML semantics. The subset makes basic typed operation examples verifiable with Python stdlib + ADS's existing Schema subset checker.
- Prose and illustrative YAML embedded *without the top-level marker* are untrusted text, even if they happen to match a Schema. Existing historical Issue bodies/comments **do not need migration**. A consumer selects the explicitly pinned ADS version and historical record type; it does not infer that post-tag main retroactively applies.

## 2. Work Item Markdown — positive type:task

The following is a **fictional document-shape example**. All refs and hashes are placeholders rather than actual current evidence.

```markdown
<!-- ads:work-item:v1 -->
```yaml
schema_version: ads/work-item/v1
work_item_type: type:task
contract:
  task_id: T02
  goal: Capture source-qualified Agent usage without secret tool input
  integration_target: version/v0.1
  baseline_sha: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
  review_policy: recommended
  required_gates:
    - concern
  acceptance:
    - Real source event with per-source timestamp and no invented cost
  task_pack_ref: task-pack:T02
```

# T02 — Collect usage

## Scope
Collect metadata-only events and preserve provider-native request IDs.

## Acceptance
- [ ] One real invocation has an externally resolvable source ref.
- [ ] Missing provider usage is UNKNOWN, never a zero.

## Limitations
This Issue body is the *stable contract*; GitHub labels/dependencies remain live native objects.
```

The inner example is shown as a Markdown block for visibility. An actual Issue starts at the marker **without** an outer Markdown fence. Work Item YAML `work_item_type` MUST agree with canonical native Issue Type / `type:*` label when read; a snapshot mismatch requires reconciliation, not a new authoritative status. For type:task, `contract` MUST satisfy existing `task-contract.schema.json`. For other current Issue types the v1 profile enforces the bounded required keys in `scripts/verify_github_structured_interaction.py`, **only for opted-in new documents**, not frozen historical prose templates.

## 3. Normalized mutation intent — positive label/state metadata

```markdown
<!-- ads:github-interaction:v1 -->
```yaml
schema_version: ads/github-structured-interaction/v1
intent_id: request:example:1
operation: ISSUE_METADATA_CHANGE
target:
  repository: example-org/example-repo
  issue_ref: "#120"
actor:
  actor_role: builder
  operator_kind: codex
  operator_id: codex:worker-01
expected_source_ref: github:example-org/example-repo#120@revision-4
payload:
  field: state
  before: state:ready
  after: state:claimed
```

Reason: propose admission for a ready Task. This document is **not** the accepted Claim.

```

Before a writer mutates native Issue state, it MUST read the real current Work Item, dependencies, admitted Claim/Dispatch and exact source, check expected revision/currentness, actor's **self-declared** role, the lawful state transition and original owner rules, and refuse on conflict. Valid YAML is **not** enough to enter `claimed`. No new credential/Owner check is inferred from the GitHub transport login. The existing v4.12 Claim protocol still supplies the atomic compare-and-set admission source.

## 4. Operation→schema→authority matrix

| v1 operation | Typed payload (static checker) | Existing GitHub/ADS authority to verify **after shape** |
| --- | --- | --- |
| `ISSUE_CREATE` | `work_item` object with `ads/work-item/v1`; Issue target and expected ref are null | body readability, source inputs, canonical type and native labels, Work Item completeness |
| `ISSUE_CONTRACT_UPDATE` | new `work_item` + `previous_contract_ref` + `change_reason` | source-bound Issue body amendment, frozen Product/L2/Task Pack authority and current revisions |
| `ISSUE_METADATA_CHANGE` | `field`, `before`, `after`; fields type/state/review_policy/risk/labels/milestone/title | native type/label/state owner; exact currently observed values and legal state/Claim transition; labels not evidence PASS |
| `ISSUE_DEPENDENCY_CHANGE` | `dependency_issue_ref` and `change: ADD/REMOVE` | **native Issue Dependencies** and DAG mutation/currentness/cycle/scope rules; sub-issues are not edges |
| `ISSUE_COMMENT_EVENT` | nested existing `agent-event-v2.schema.json` | *existing* event-v2 marker/writer/identity and Review/Validation/CI source, never comment text alone |
| `ISSUE_COMMENT_REPORT` | Task Report v1 kind, report ID/revision/Attempt, publication key, manifest locator/checksum | existing `ads:task-report:v1` comment and immutable OSS source checks, no raw trace/comment spam |
| `ISSUE_CLOSE` / `ISSUE_REOPEN` | reason and actual `evidence_refs` | canonical Task result/gates/merge/currentness and lawful native Issue state; reopening does not erase history |
| Ordinary discussion/comment reply | No normative marker or operation | plain Markdown; no schema/Claim/Gate authority |

Additional GitHub API operations remain bound by their existing owners; this registry covers **normative Issue mutations**, not raw HTTP verbs nor new GitHub API permissions. This contract DOES NOT silently add an active native label that makes a Task PASS.

## 5. Two independent verdicts

```text
raw Markdown text → marker/version parse → bounded YAML parse
                  → JSON Schema + operation-specific payload validation
                  = SHAPE_VALID_ONLY or INVALID_SCHEMA
SHAPE_VALID_ONLY + current GitHub source readback + appropriate authoritative
dispatch/claim/dependency/gate rules + lawful write
                  = a separately proven accepted native mutation / canonical event
```

Unverified source, missing authorization, stale HEAD, missing CAS, wrong dependencies or unresolved permissions **remain blocked by their original owner** even if the YAML is perfect. A completed tool API request doesn't grant its own review/validation/release truth. The validator has **no write function**.

## 6. Negative and backward-compatibility cases

| Case | Expected disposition |
| --- | --- |
| Marker appears halfway down a normal Markdown discussion or quoted sample | Not admitted; strict parser rejects if treated as structured |
| Repeated top-level marker, two YAML keys of same name or unsupported YAML feature | `INVALID_SCHEMA`; never accept last duplicate key |
| Unknown `operation`, contradictory target/ref, absent actor ID or expected source revision on edits | `INVALID_SCHEMA` |
| `ISSUE_CREATE` pretends to modify existing #N | `INVALID_SCHEMA` |
| `ISSUE_METADATA_CHANGE` has fabricated `state:validated` or equates label to Gate PASS | `INVALID_SCHEMA` or later owner refusal |
| `ISSUE_DEPENDENCY_CHANGE` self-links or invents closure from prose | reject shape or later DAG owner |
| `ISSUE_COMMENT_EVENT` missing actual event-v2 required fields | `INVALID_SCHEMA`; schema-valid raw comment still not an admitted event |
| `ISSUE_COMMENT_REPORT` has mismatched publication key, unsupported kind or checksum | `INVALID_SCHEMA`; manifest validity and GitHub publication require separate I/O |
| Two concurrent agents send individually valid `ISSUE_METADATA_CHANGE` intents from the same old revision | first lawful writer only; second stale/refused by native source/Claim rule |
| Old valid `ai-dev:event:v2`/`ads:task-report:v1` comment | continue reading under its **original** marker/schema; do not reemit a different event-v3 |
| Ordinary public user discussion with no marker | `UNSTRUCTURED_DISCUSSION`, not mandatory Schema |
| Executable new Work Item with incomplete required Task Contract | reject opt-in work-item shape; no READY/Dispatch |
| Forged `HUMAN_APPROVED`, hidden reasoning or untrusted YAML copied into chat | no authority through formatting; protected source decision rules prevail |

## 7. Adoption and limitations

- **Prospective opt-in:** a project may start writing the new markers after explicitly adopting an appropriate exact ADS source version. Templates for older pinned versions are unchanged. Existing Markdown metadata not emitted with the new marker stays historical.
- **Scope of machine checks:** the bundled script proves deterministic **format** validation for the supported YAML subset and the schema/rule lookup. It does *not* integrate with GitHub mutation API, independently fetch canonical remote currentness, grant Agent permissions, read CI/Review evidence, implement CAS or atomically publish comments.
- **Not full YAML:** a full versioned safe YAML library could be introduced by the consumer for extended syntax only after a compatibility decision, rather than silently accepting flow/anchor semantics the reference verifier cannot reproduce.
- **Not every prose report a machine event:** normalized reporting needs a recognized marker/contract. Unstructured brainstorming/Issue discussion remains allowed and is never a Task state transition.
- **Migration:** a subsequent project may choose a template generator or explicit migration plan for all Issue types. Rewriting thousands of previous Issue bodies is not required to make the v1 contract available.
