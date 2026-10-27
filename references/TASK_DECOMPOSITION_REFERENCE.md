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


## 10. Optional v4.18 Safe Task DAG Planning Patterns — E1 source-only

This is a **non-normative companion to the existing Task Decomposition owner**, not a second execution graph, new permission, issue-label state, Agent registry or Review/Release gate. Examples below are **fictitious E1 planning oracles** derived from frozen v4.18 Product/L2. They do not demonstrate multi-Agent runtime execution, accepted real SF/MI, physical Host tests, genuine protected human approval or measured time savings.

### Pattern selection (non-authoritative)

- **Fan-out / Fan-in:** freeze common contracts first; parallel concerns only when their native blockers and effective writer scopes actually allow; central integration consumes accepted results.
- **Vertical Slice:** a capability's whole acceptance may be independently useful; do not turn each step or source directory into an Issue.
- **Parallel Pipelines:** different capability Lanes may carry their own ordered Contract/Implementation/Test steps while unrelated Lanes run concurrently.
- **Contract-first / Platform + Plugins:** stable shared ABI enables independent adapters; unresolved shared semantic ownership stays prerequisite or atomic.
- **Evidence Parallel:** independent read-only research/preflight is not authority for a blocked source-writing Builder.
- **Migration / Strangler:** prepare compatible streams independently but keep the cutover and data invariant under one accepted integration owner.
- **Atomic Invariant:** concurrency is inappropriate where it splits transaction, security or state-machine consistency.
- **Optional Source Scaffold feedback:** reason about actual accepted module/anchor boundaries before Freeze; SF/DF/MI §10A remains the sole mapping authority when adopted. Without accepted SF, mark NOT_APPLICABLE.

### Paired source-only Golden and forbidden examples

| ID | Planning pattern | Positive E1 oracle | Forbidden E1 oracle |
| --- | --- | --- | --- |
| G418-01 | Capability-first vertical slices | Email and SMS outcomes become coherent concerns in separate Lanes, with local steps and one shared Contract owner | Treat global Contract → Core → UI phase order as compulsory native serialization for unrelated capability Issues |
| G418-02 | Fan-out / Fan-in topology comparison | Compare A ∥ B ∥ C → I → R with a longer serial candidate; preserve all real native blocked_by edges and report speedup UNKNOWN | Delete a real native blocked_by edge or claim unmeasured 2× speedup to maximize apparent concurrency |
| G418-03 | Qualified Source Scaffold feedback | Accepted SF modules and anchors suggest disjoint writers before Freeze, then validate actual SF↔DF mapping and MI under §10A | Unaccepted SF Anchor grants Builder permission, or two concurrent Tasks write the same effective Anchor without lawful mutation |
| G418-04 | Agent and evidence fit | Choose risk-qualified WEB/CI/LOCAL role capability, distinct independent Reviewer, and hand off only unproved real physical evidence | Builder self-approves a required independent Review, or Web reading masquerades as verified real Host PASS |
| G418-05 | Native dependency / JIT boundary | Task blocked_by a predecessor may perform lawful read-only PREP; Builder source remains HOLD until native dependency and accepted Claim permit | Annotate a blocked Task as merge-only and declare ready_builder or source-writing permission while real blocked_by remains |
| G418-06 | Atomic invariant rationale | Keep one serial transaction/security concern atomic with a specific invariant; no artificial parallelism quota | Split an indivisible consistency rule into partial-invalid sibling source writers for better concurrency statistics |
| G418-07 | Genuine human decision / assistance | Request only a protected exact-scope decision or real device action when needed, then resume accepted remaining work | Accept a text-only HUMAN_APPROVED token as protected consent or require a person for routine CI polling |

**Planning evidence rule:** Candidate edge reasons (contract/code, writer, evidence, integration, scarce resource) are *annotations* only. They never reclassify live GitHub Issue Dependencies, grant `ready_builder`, bypass JIT/Claim, authorize overlapping writes, waive independent Review or decide Release applicability. A mostly-serial plan may be correct with an explicit atomicity rationale. No positive example is a claim that actual task execution or cost improvement occurred.

## 11. v4.19 issue-derived feasibility and coordination cases (prospective)

**False prerequisite ([DomainHarness #530](https://github.com/kaicreator-mm/domain-harness/issues/530)).** A new major refactor can implement an independently frozen contract before the previous version finishes source integration, if each new work concern can be correct on its own branch and the legitimate prior-version compatibility proof is owned by the later join. **Forbidden:** erase real native `blocked_by` or launch a source-writing Builder before accepted Claim. **Golden:** explain the upstream version's actual dependency role, permit only lawfully independent Task lanes, and keep one compatibility/integration join.

**Material package migration ([#1354](https://github.com/kaicreator-mm/domain-harness/issues/1354)).** Before freezing fine-grained package manifest/dist/CI owners, use cheap available source/packaging feasibility to locate shared writers and required actual dependency order. **Forbidden:** invent an early manifest-only Task that breaks clean legacy consumer or requires prohibited generated writes just to preserve the original DAG. **Golden:** route actual BUILD vs legacy Compiler cutover decisions to L2/DAG owner and keep source/merge authorization separate.

**Verification coordination ([#586](https://github.com/kaicreator-mm/domain-harness/issues/586)).** One cross-cutting verification campaign can keep sequential checkpoints as comments/evidence under its existing Issue. Distinct bounded defects may spawn separate authorized repair Tasks. **Forbidden:** one new executable Issue, Claim, Review and CI per unchanged campaign checkpoint; or Builder self-certification of required independent Review.

These are positive/forbidden **decision examples**, not GitHub Task replays or measured speedups. They do not change G418-01..07, which remain v4.18's qualified planning examples; live native Issue Dependencies and Claim always control actual readiness.
