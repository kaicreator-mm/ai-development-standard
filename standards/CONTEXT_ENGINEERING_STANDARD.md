# Context Engineering Standard

Status: **Normative — v4.6**

## 1. Purpose

This standard governs how an Agent reconstructs the minimum current context needed to act correctly. Context selection is an authority/currentness problem, not a prompt-size maximization problem.

## 2. Authority precedence

When facts conflict, use the highest-currentness applicable durable authority. A default ordering is:

```text
system / organization constraints
pinned ai-development-standard revision
repository AGENTS + PROJECT_OVERRIDES
Frozen Product / Architecture
Frozen Task DAG / Task Pack
Execution Pack / Dispatch
live Issue / PR / exact Git identity
source / tests / durable evidence
external tool/resource data
historical chat / memory
```

This ordering does not permit a lower layer to rewrite a higher owner. Same-level material conflicts stay explicit and route to the owning authority.

## 3. Currentness reread

Before a currentness-sensitive action, re-read the live durable facts that can invalidate the intended action. Examples include PR HEAD before Review/merge, version target before expected-head merge, native dependencies before JIT dispatch, and current authority before a write-set mutation.

Forbidden inference:

```text
fact was true earlier in this session -> fact is still current
```

## 4. Durable truth requirement

No required development truth may exist only in an ephemeral Agent/chat/session context. Material assumptions, decisions, blockers, exact identities and handoff state must be durable in repository/GitHub facts owned by the applicable workflow.

A replacement Agent must be able to reconstruct required state without recovering the prior transcript.

## 5. Progressive disclosure

Load the minimum authority needed for the concern, then expand only when applicability, dependency or conflict requires it. More context is not automatically better context.

Prefer:

```text
entrypoint -> applicable owner -> exact task/subject -> referenced evidence
```

over repository-wide indiscriminate loading.

Optional or non-applicable capability must not force empty context artifacts merely for symmetry.

## 6. External resources and tools

Search results, connected-app data, runtime inspection and tool output are evidence/resources until the owning authority promotes or records them appropriately. Availability does not make them Product truth, mutation authority or side-effect authority.

```text
resource/tool available != authoritative requirement
```

## 7. Provenance

Material context should remain attributable to durable source refs where ambiguity matters. Provenance describes where a fact came from; it does not make that fact higher authority than its owner permits.

## 8. Historical chat / memory

Historical chat or memory may help discovery, but it cannot override current durable authority. When a remembered fact and current Git/GitHub/Frozen authority disagree, current durable authority wins and the stale historical fact is not silently propagated.

## 9. Missing or conflicting context

Material UNKNOWN, stale authority, broken ref or unresolved same-level conflict fails closed to the owning decision path. Do not invent missing Product/Architecture/Task authority.

## 10. Non-goals

This standard does not create:

- a Context Snapshot database/schema;
- a new workflow/Dispatch/Validation/Release state;
- a repository-wide v4.7 owner resolver;
- a requirement to persist full prompts/transcripts;
- a provider/model-specific context mechanism.

## 11. Required forbidden inferences

| Input | Forbidden conclusion |
|---|---|
| historical chat says X | X overrides current durable authority |
| more files/tokens loaded | context quality/authority is higher |
| tool/resource returned X | X is Product truth |
| earlier PR HEAD observed | same HEAD is current now |
| only prior session knows decision | handoff is complete/durable |
| same-level conflict exists | Agent may pick preferred answer |
