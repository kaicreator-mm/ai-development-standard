# v4.0 Work Item / Pack / Fast Path Integration

Status: CANDIDATE — T-007 / Issue #79
Version: 4.0.0
Baseline: `version/v4.0.0@acef771c5895d0d4f8b3ee843420ae5ab493b457`
Owning authorities: `standards/GITHUB_WORK_ITEM_CONTRACT_STANDARD.md` + `standards/EXECUTION_PACK_STANDARD.md`
Inputs: `OPERATION_CONTRACT.md`, `OPERATION_ROUTING_INTEGRATION.md`, `AGENT_INTERCHANGE.md`

## 1. Purpose

This document maps the v4 Operation Protocol onto existing GitHub Work Items, Task Packs, Execution Packs, dispatch and Fast Path behavior.

It does not create a new work-item object model or duplicate durable authority.

Core invariant:

```text
Issue / Work Item = stable executable assignment authority
Task Pack         = durable WHAT authority for the Task
Execution Pack    = JIT HOW authority bound to one exact base
Dispatch          = WHO / WHERE / WHICH IDENTITY handoff
Operation         = lifecycle/correlation composition over those authorities
```

An Operation reference may connect these objects. It does not replace them.

## 2. Work Item mapping

A materialized GitHub Task Issue remains the stable executable assignment authority in the GitHub profile.

The Work Item may expose a minimal Operation binding when useful:

```yaml
operation_binding:
  operation_id: <stable logical id or durable ref>
  operation_kind: <PRODUCE|RESEARCH|ASSURE|DECIDE|CONTROL>
  parent_operation_ref: <optional>
```

This binding is correlation metadata. It must not duplicate the Issue contract or become a second workflow state.

The Issue body continues to own/refer to:

```text
Goal
Frozen Inputs / authority
Scope / non-scope
Dependencies
Acceptance
Validation ownership
Review Policy
Risk
Execution constraints
Allowed / forbidden changes
Failure / blocker behavior
Completion rule
Task Pack / Execution references
```

## 3. Canonical live DAG remains Issue Dependencies

Operation composition is not a replacement dependency graph.

```text
Frozen planning checkpoint
→ GitHub Task Issues + native Issue Dependencies
= canonical live execution DAG
```

If an Operation relationship represents a Task dependency, it must resolve to the owning Work Item dependency. Operation-local assurance sequencing may remain local and must not independently mark a Task READY/BLOCKED.

## 4. Where v4 Operation facts belong

Operation facts are stored only where they add information without duplicating authority.

### Work Item / Issue

Appropriate:

- stable Task/Operation correlation;
- operation kind when material to routing/assurance;
- durable refs to Task Pack / Execution Pack / PR / evidence;
- canonical Work Item metadata already owned by the Work Item standard.

Not appropriate:

- copying the full Operation envelope;
- embedding dynamic dispatch/session identity in the stable Issue body;
- storing Gate PASS/FAIL as labels;
- duplicating exact evidence already owned by PR/Validation/Release records.

### Task Pack

Task Pack remains WHAT authority. It may state:

- task/operation intent and concern boundary;
- required operation/assurance constraints;
- dependencies;
- acceptance/gates/review/risk;
- allowed/forbidden scope.

It must not contain exact-base-dependent implementation maps.

### Execution Pack

Execution Pack remains exact-base-bound HOW authority. It may resolve:

- effective Operation/Task identity for this exact base;
- current branch/base SHA;
- current contract/test/file map;
- exact-base failure and review checklist;
- current execution profile and freedom.

It may narrow execution but cannot redefine Product/Architecture/Task/Validation/Review authority.

### Dispatch / events

Dynamic execution identities belong in dispatch/events:

```text
dispatch_id
operation_id / correlation refs
role / profile
operator identity
expected base SHA / requested HEAD SHA
subject identity
causation / exchange refs when applicable
```

## 5. No giant Operation payload requirement

The GitHub profile SHOULD prefer durable references over serialized duplication.

A consumer may reconstruct one logical Operation view from:

```text
Issue + Issue Dependencies
Task Pack
Execution Pack when present
PR/current exact identity
accepted events / evidence
Assurance / Review / Validation facts
controller / merge / release facts
```

A single giant serialized Operation document is optional and non-authoritative unless another owning standard explicitly grants authority.

## 6. Task Pack / Execution Pack separation is preserved

v4 must not blur the existing distinction:

```text
Task Pack      = WHAT must be achieved, stable across executable bases unless revised
Execution Pack = HOW to execute safely on this exact base, JIT and replaceable
```

Adding `operation_id` or other correlation does not change this authority hierarchy.

If execution discovers a contradiction:

```text
Task Pack defect -> route to Task authority
Architecture contradiction -> route to Architecture authority
Execution Pack invalid/stale -> regenerate or fail closed per pack rules
```

The executor does not redesign silently.

## 7. JIT branch and Execution Pack lifecycle

Existing JIT discipline remains normative:

```text
Task Pack frozen
→ dependencies satisfied
→ reducer recomputes ready set
→ read current integration exact SHA
→ create task branch JIT
→ create/bind Execution Pack when needed
→ emit Builder dispatch
→ execute
```

Operation correlation may be attached during this sequence but cannot justify pre-creating long-lived branches or packs before dependencies are satisfied.

Base drift remains governed by Execution Pack staleness and Validation impact rules. Operation identity does not make stale packs current.

## 8. Pointer-only invocation

User-visible invocation remains pointer-only.

Preferred form:

```text
执行 owner/repo Issue #N 当前 READY dispatch。
```

or, when role must be explicit:

```text
执行 owner/repo Issue #N 当前 LOCAL_VALIDATOR dispatch。
```

The receiving Agent reconstructs the durable contract from GitHub/repository authority.

Do not copy Task Pack, Execution Pack, Operation envelope, or durable prompt content into chat as a competing contract.

## 9. Fast Path — operation elision

Fast Path is reduced operations, not reduced truth.

A low-risk bounded change may omit explicit materialization of Product/Architecture/Assurance/Operation objects when those objects would be empty ceremony and the required authority chain is already unambiguous.

A conformant Fast Path still preserves the material chain:

```text
known baseline / authority
→ bounded implementation
→ required executable Validation
→ Review decision under selected policy
→ GitHub durable fact chain
→ release-impact disposition
```

No synthetic empty PRD, Architecture Operation, Assurance Plan, or Execution Pack is required merely to satisfy v4 vocabulary.

## 10. Fast Path eligibility

Fast Path is appropriate only while all material conditions remain bounded and unambiguous, for example:

- scope is small and internally local;
- no new public contract/architecture/security/trust boundary is introduced;
- no material migration/recovery/concurrency/irreversible semantics are introduced;
- validation ownership and required evidence are known;
- dependency topology is simple;
- selected Review Policy remains sufficient for risk;
- no unresolved authority contradiction exists.

Project overrides may impose stricter rules.

## 11. Deterministic escalation from Fast Path

Fast Path must escalate when any material condition makes the reduced representation insufficient.

Escalation triggers include:

```text
scope expands beyond the bounded concern
new or changed public contract / schema / architecture boundary
security / permission / trust-boundary change
migration / recovery / concurrency / exactly-once complexity
cross-repository or cross-authority coupling
unknown validation ownership or material environment requirement
unresolved P0/P1 or authority conflict
required model-diverse/coherence assurance
need for a nontrivial exact-base Execution Pack
Task dependency graph becomes material
```

Escalation behavior:

1. preserve already-produced durable evidence as historical evidence;
2. materialize/repair the required Work Item/Task Pack/Architecture/Assurance authority;
3. recompute risk, Review Policy, Validation ownership and dependencies;
4. bind any new Execution Pack JIT to the current exact base;
5. do not retroactively claim that omitted operations previously executed.

## 12. Workflow metadata compatibility

Existing canonical Work Item workflow states remain unchanged by T-007.

Operation kind/correlation must not be encoded by inventing workflow states such as:

```text
state:produce
state:assure
state:operation-running
```

Likewise `operation_id`, `dispatch_id`, reviewer identity or session identity do not belong in ad-hoc state labels.

T-009 may define machine fields/references, but they remain orthogonal to canonical workflow routing.

## 13. Assurance and Review references

When Assurance is required, the Work Item should reference the selected durable Assurance requirements/results rather than duplicating their content.

A Review request/result binds to the exact subject identity required by the owning policy. Work Item state such as `reviewing` or `merge-ready` remains routing metadata and cannot replace Review evidence.

## 14. Validation references

A Work Item may route to a validation profile/scope, but Validation truth remains in exact executable evidence.

`validation-needed` or an Operation `ASSURE`/Validation correlation is never equivalent to Gate PASS.

## 15. Recovery and reconstruction

A fresh Agent must be able to reconstruct the assignment without chat history from:

```text
pinned standard
Work Item / Issue
canonical Issue Dependencies
Task Pack
Execution Pack if present
current PR/branch/base/HEAD identity
accepted events / evidence
```

If a material task-specific requirement exists only in prior chat, the durable contract is incomplete and must be repaired before dispatch.

## 16. Compatibility and migration rule

Existing v3.4 Work Items remain conformant without a newly serialized Operation object when their durable facts already resolve the required v4 semantics.

Adoption is additive:

- add Operation correlation only where useful;
- do not rewrite historical Issues merely to add ceremony;
- do not change existing workflow labels to Operation kinds;
- preserve current Task Pack/Execution Pack wire contracts until T-009 explicitly versions/enforces machine changes.

## 17. T-007 completion boundary

T-007 freezes the logical integration of Work Item, Task Pack, Execution Pack, dispatch, pointer-only invocation and Fast Path with v4 Operations.

It does not implement:

- T-008 Validation/Candidate Freeze/Hidden/Release changes;
- T-009 schemas, event fields, verifier code or golden regressions;
- a new GitHub object type or a new workflow state machine;
- runtime transport/queue software.
