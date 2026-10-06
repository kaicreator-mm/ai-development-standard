# Context Engineering Standard

Status: **Normative — v4.6**

## 1. Purpose

This standard governs how an Agent reconstructs the minimum current context needed to act correctly. Context selection is an authority/currentness problem, not a prompt-size maximization problem.

## 2. Authority resolution

Context Engineering does not define one universal total ordering across all durable sources. Resolve a material fact by the authority that owns that fact, the override surface that authority permits, and the live currentness required by the next action.

Use this resolution model:

1. System/organization constraints and standard hard constraints cannot be weakened by project or Task material.
2. Identify the semantic owner of the disputed fact before comparing sources.
3. Apply an authorized specialization/override only within the surface the owner permits. For example, `PROJECT_OVERRIDES.md` may specialize standard defaults where allowed, but it cannot weaken a hard constraint.
4. Preserve frozen scope/acceptance authority separately from live execution currentness. Frozen Product/Architecture and Task Packs own their applicable frozen semantics; after Issue-based materialization, GitHub native Issue Dependencies own the canonical live blocked-by topology.
5. Exact PR/HEAD/base, current branch target and other mutable execution identities must be re-read from their live owning surfaces before currentness-sensitive actions.
6. When two applicable sources claim the same owned fact at the same authority/currentness level and materially conflict, fail closed and route to the owner.

Required examples:

- A pinned standard default MUST NOT override a valid project specialization merely because the standard file is globally higher-level; first determine whether the rule is a hard constraint or an overridable default.
- A Frozen Task DAG remains planning/history authority after materialization, but it MUST NOT override the current native Issue Dependency graph for live blocked-by topology.
- A Task Pack continues to own Task scope/acceptance even when live Issue dependencies or PR/HEAD identities change.

No source gains authority merely because it is newer, easier to access, closer to the Agent, or listed earlier in a read sequence.

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

Historical chat or memory may help discovery, but it cannot override current durable authority. When a remembered fact and the applicable current owner/currentness facts disagree, the applicable durable owner wins and the stale historical fact is not silently propagated.

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
| pinned standard default exists | valid PROJECT_OVERRIDES specialization is ignored |
| Frozen Task DAG has edge X | edge X is still live after native dependency materialization/change |
| live Issue dependency changed | Task Pack scope/acceptance changed automatically |
| historical chat says X | X overrides current durable owner/currentness |
| more files/tokens loaded | context quality/authority is higher |
| tool/resource returned X | X is Product truth |
| earlier PR HEAD observed | same HEAD is current now |
| only prior session knows decision | handoff is complete/durable |
| same-level conflict exists | Agent may pick preferred answer |
