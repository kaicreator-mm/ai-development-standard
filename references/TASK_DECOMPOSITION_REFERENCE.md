# Task Decomposition Reference

Non-normative companion to `standards/TASK_DECOMPOSITION_STANDARD.md`.

## 1. Compact Task worksheet

```text
Task ID / concern:
Frozen authority refs:
Goal / expected output:
Allowed write-set:
Forbidden scope:
Acceptance:
Required gates:
Validation owner/scope:
Review policy:
Integration target:
Dependencies:
L3/reference:
Agent freedom:
Failure/escalation:
```

## 2. Good parallel split example

A shared machine contract is frozen first. Then three normative standards that consume the contract but own disjoint files can run as sibling Tasks from the same integration SHA. A later adoption/wiring Task owns the manifest/common project surfaces.

This is safe parallelism because each sibling can be implemented/reviewed independently and central mutable wiring is isolated.

## 3. Bad file-count split

Splitting one public protocol change into “schema files” and “semantic tests/prose” on unrelated branches is unsafe if neither branch is independently correct. Keep the invariant together or freeze a prerequisite contract first.

## 4. Real stacked dependency

A stacked PR can be justified when T2 must compile against new APIs implemented by an unmerged T1 and delaying T2 until T1 merge is intentionally undesirable. The stack is a code-baseline convenience; the Task dependency remains represented by the live Issue DAG.

## 5. Central wiring checklist

When siblings all want to touch the same registry/manifest/router/config file, ask whether that surface is semantic ownership or only integration wiring. If it is wiring, reserve it for an explicit integration Task rather than letting each sibling race and duplicate owner semantics.

## 6. Dependency test

A useful dependency question is:

> If predecessor code/evidence did not yet exist, could this Task still be correctly implemented, validated and reviewed from the same current integration baseline?

If yes, a dependency may be unnecessary. If no because a real contract/baseline/result is required, the dependency is material.

Conceptual ordering alone is not a dependency.

## 7. Decomposition review prompts

- Is there one primary concern?
- Are write ownership and forbidden scope explicit?
- Can the Task produce a stable exact review/Validation subject?
- Are shared invariants atomic or prerequisite-frozen?
- Are central mutable surfaces isolated?
- Are dependencies real rather than conversational?
- Is any dependency being removed solely to manufacture READY?
- Is a stacked PR justified by actual unmerged code-baseline dependence?
- Could a qualified Agent dispatch, execute and validate this Task from the durable facts alone?

## 8. Sequential single-file ownership

Two Tasks may touch the same file when each owns a different concern and the second builds on the first's merged result: for example, one Task migrates a schema definition and a later Task adds the feature that consumes it. The later Task declares a real dependency on the earlier one's integrated baseline, and the live DAG carries the ordering.

This is legitimate because concerns are distinct and conflict is explicitly controlled through the dependency. Running the same two Tasks as “parallel” branches that both edit the file would be fake parallelism.

## 9. Agent-dispatch worksheet check

Before freezing a Task, resolve every dispatch fact from the §1 worksheet into durable authority: identity/concern, frozen authority refs, expected output, allowed write-set, forbidden scope, acceptance, gates, validation owner, review policy, integration target, dependencies, failure/escalation.

If a required fact lives only in a conversation, thread or someone's memory, either freeze it into durable authority or keep the work unplanned. The v4.10 JIT Execution Pack (TASK/PLAN/CONTEXT/DOD/COMMANDS/HANDOFF per Task, bound to an exact integration baseline and owner blob) is the current dogfood of this pattern.
