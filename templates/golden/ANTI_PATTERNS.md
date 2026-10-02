# Golden Anti-pattern Library

These are intentionally non-conformant examples. They are diagnostic references, not executable templates.

## live-dag-document-as-authority

```text
TASK_DAG_STATUS.md
T-003 = DOING
T-004 = DONE
```

Multiple Agents edit the file and treat it as current truth.

**Forbidden because:** the repository document becomes a second live state authority and concurrent edits can disagree with Issue/PR/evidence facts. Live DAG truth is Task Issues + native Issue Dependencies + durable state/evidence.

## incomplete-executable-issue

```text
Issue body: “Implement caching.”
Chat prompt: use branch X, only edit Y, run commands Z, acceptance is Q.
```

**Forbidden because:** execution depends on hidden ephemeral instructions. The required task-specific facts must be in the Issue or referenced durable authority before dispatch.

## silent-dependency-drift

An Agent changes `T-005` from blocked-by `T-003` to blocked-by `T-004` only in its local reasoning or a Markdown dashboard.

**Forbidden because:** the canonical live dependency graph was not changed and no rationale/event exists.

## gate-result-as-label

```text
Labels: gate:pass, validation:passed
```

**Forbidden because:** Gate truth is evidence-bound and may go stale on exact-head drift; mutable labels are routing metadata, not validation truth.

## stale-pass-label

PR HEAD changes after validation, but a `ci:green` / `review:passed` label is left in place and treated as current evidence.

**Forbidden because:** evidence is bound to exact identity; HEAD drift invalidates the old evidence for the new candidate.

## agent-identity-as-label

```text
agent:chatgpt-web-4
session:review-17
```

**Forbidden because:** operator/session identity is dynamic structured-event provenance, not stable Issue metadata.

## self-asserted-independent-review

The Builder writes `Independent Review PASS` for its own exact-head change when Review Policy is `required`.

**Forbidden because:** required Independent Review must come from an independent reviewer context/operator.

## long-chat-task-contract

```text
完成 Issue #10。Baseline=abc...；改 branch X；只允许改 A/B；运行 pytest ...；验证后 merge ...
```

**Forbidden because:** user-visible trigger has become a second task contract. Persist those facts in GitHub authority and emit only the pointer trigger.

## duplicate-workflow-state

```text
state:ready
state:implementing
```

**Forbidden because:** an active work item must resolve exactly one canonical workflow state.

## invented-state-synonym

```text
status:wip
state:coding
almost-done
```

**Forbidden because:** individual Agent vocabulary prevents deterministic reducers and shared multi-Agent interpretation.

## research-without-evidence-boundary

A Research Issue says “study project X and decide whether it is good” but does not define research question, evidence/source identity, what can be proven, or what remains unproven.

**Forbidden because:** conclusions cannot be audited or constrained to evidence strength.

## compatibility-dimension-collapse

A wire/schema checker passes and the change is recorded as universally compatible, without separately evaluating source, behavior or supported consumer populations that are material.

**Forbidden because:** compatibility is multi-dimensional. `wire-safe` or schema acceptance does not prove source/behavior/consumer compatibility, and a new/new pair cannot erase old/external consumer risk.

## migration-presence-as-execution

A migration file exists or a fresh install succeeds, so an upgrade from source state A to target state B is recorded as successfully migrated.

**Forbidden because:** `fresh install PASS != upgrade PASS` and `migration file exists != migration executed`. Directional transition, runtime applicability and recovery evidence remain separate subjects.

## historical-evidence-retrofit

After adopting v4.2, an old exact-SHA PASS is relabeled as compatibility or migration PASS for a new candidate, consumer population, source/target state or runtime.

**Forbidden because:** historical evidence keeps its original subject identity and meaning. New material subjects require applicable current evidence.

## evolution-evidence-as-deployment-result

Compatibility or migration evidence is used to declare Deployment success, or credential/tool availability is treated as side-effect authority.

**Forbidden because:** v4.2 does not own Deployment result semantics. Deployment execution/result belongs to the applicable Deployment owner; capability is not authorization.
