# Task Decomposition Standard

Status: **Normative — v4.3**

## 1. Purpose

This standard owns how planned implementation work is decomposed into executable Tasks.

Core principle:

> **Minimum coherent concern + maximum safe parallelism.**

A Task should be small enough to execute/review/validate independently, but large enough to preserve one coherent authority/invariant boundary.

## 2. Required durable Task facts

Every material execution Task MUST make these facts recoverable from durable planning authority:

```text
Task identity
primary concern / goal
Frozen/Product/Architecture inputs
expected output
allowed write-set / ownership
forbidden scope
acceptance criteria
required gates
Validation scope / owner
Review policy
integration / merge target
dependencies
L3 / implementation reference when required
agent freedom / executor constraints
failure / escalation handling
```

Issue text may point to a Frozen Task Pack rather than duplicate the whole contract. The durable authority must still exist and be current.

A Task is **Agent-dispatchable** only when a qualified Agent can resolve identity, allowed scope, required gates and completion from these durable facts plus the frozen authority they reference, without hidden conversation or chat context. A decomposition that depends on undocumented side-channel context to execute, validate or review correctly is not a valid Task boundary.

## 3. Primary concern boundary

One Task SHOULD have one primary concern that can be described without joining unrelated authority domains with “and also”.

A concern may span multiple files when those files jointly implement one invariant/contract.

Conversely, one file may legitimately be touched by multiple sequential Tasks when different concerns own different changes and conflict is explicitly controlled.

File count, line count or estimated token count alone MUST NOT define Task boundaries. Time or effort estimates carry the same prohibition and MUST NOT define Task boundaries alone.

## 4. Safe parallelism

Parallelize Tasks when all of the following are sufficiently true:

- each Task has independent authority/write ownership;
- there is no unmerged code baseline required from the sibling;
- shared contract/invariant has already been frozen or isolated behind a prior dependency;
- their Validation/Review subjects can be identified independently;
- central wiring/shared mutable surfaces are deferred to an explicit integration Task when appropriate.

Do not fake parallelism by splitting an atomic invariant across branches that must be understood/merged together before either is valid.

## 5. Atomicity and shared invariants

Keep a concern together when splitting would create one or more of:

- partially defined public contract;
- schema/prose mismatch where neither Task can be independently correct;
- shared state invariant that only holds after both branches merge;
- security/authorization rule split across independently mutable halves;
- migration step whose safety depends on an unmerged sibling implementation;
- circular review/validation dependency.

If the atomic unit is large, improve internal structure/tests or create prerequisite contracts rather than pretending independent Tasks exist.

## 6. Dependencies

A Task dependency exists when one Task genuinely requires another Task's **completed durable result or integrated code baseline**.

Do not add dependencies merely because work is conceptually related or expected to happen earlier in conversation order.

Do not remove a dependency merely to make a Task appear READY.

Dependency removal after materialization is a material DAG mutation owned by `TASK_DAG_GOVERNANCE_STANDARD.md`, not a Task-side planning convenience.

After materialization, GitHub Issue Dependencies are the canonical live Task DAG. Body text, labels or chat descriptions are not substitutes for native dependency truth.

## 7. Stacked PR boundary

Stacked PR is appropriate only when a Task genuinely needs code from an unmerged predecessor branch and waiting for predecessor merge is intentionally avoided.

Stacked PR MUST NOT be used as the general representation of the Task DAG.

If sibling Tasks can start from the same current integration SHA and integrate independently, use independent branches/PRs rather than a stack.

## 8. Central wiring pattern

When many sibling Tasks own independent normative/implementation concerns but share manifest, registry, adoption, router, composition-root or common configuration surfaces, prefer:

```text
independent concern Tasks
        ↓
explicit central wiring / integration Task
```

This reduces write collisions and prevents each sibling from redefining shared discovery/adoption semantics.

Central wiring MUST reference sibling owners rather than become a semantic rewrite task.

## 9. Task lanes are advisory

Labels such as contract/core/integration/UI/validation/research may help humans and Agents reason about decomposition, but no fixed lane taxonomy is universally mandatory.

Concern ownership and real dependencies decide the DAG, not the label name.

## 10. Anti-patterns

### 10.1 File-count split

```text
T1 = edit files 1-5
T2 = edit files 6-10
```

is invalid unless those groups correspond to coherent independently valid concerns.

### 10.2 Giant mixed-authority Task

A Task that simultaneously owns unrelated Product semantics, schema policy, CI redesign, UI behavior, deployment and release qualification should be split unless one atomic invariant truly requires them together.

### 10.3 Fake parallelism

Two Tasks are not safely parallel when each is only correct if the other unmerged branch is present.

### 10.4 Readiness fabrication

Deleting/ignoring a dependency, creating a branch early, or relabeling a Task READY does not make prerequisite truth exist.

## 11. Validation / Review decomposition

A good Task boundary supports a stable exact subject for its required evidence.

Where concern Validation or Fresh Independent Review is required, the reviewer/validator should not need unrelated sibling changes merely to determine whether the Task passed.

Integration-wide properties belong in a later integration/conformance Task rather than being silently pushed into every sibling.

## 12. Fast Path

Fast Path may represent a genuinely small coherent concern as a single Task/PR with reduced planning ceremony when applicable policy allows.

Fast Path MUST NOT combine multiple unrelated authorities merely to avoid Task materialization, nor remove real dependencies/gates.

## 13. Decomposition decision prompts

Before freezing a Task, ask:

1. What single concern/invariant does it own?
2. What exact files/surfaces may it mutate?
3. Can it be correct, validated and reviewed without an unmerged sibling?
4. Which facts truly require predecessor completion?
5. Is a shared contract better frozen as a prerequisite Task?
6. Are central wiring/shared mutable surfaces isolated?
7. Would splitting create partial-invalid states or circular dependencies?
8. Is a stacked PR really required by code-baseline dependency?
9. Could a qualified Agent dispatch, execute and validate this Task from the durable facts alone?

## 14. Failure handling

If concern ownership or atomicity is ambiguous, keep the work unresolved or together until planning authority decides; do not force parallelism.

If removing a dependency would fabricate readiness, reject the decomposition change and use the applicable DAG mutation governance path.
