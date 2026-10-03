# v4.9.0 Product Review Handoff

Status: **READY FOR INDEPENDENT ADVERSARIAL PRODUCT REVIEW — SUCCESSOR CANDIDATE REQUIRED**

This handoff defines review scope only. The dedicated Product Review Issue must pin the current exact PR #698 HEAD/tree before execution.

The author-side adversarial pre-review at PR #698 comment `5961233246` is **not independent** and must not satisfy this gate. It found `P0=0 / P1=6 / P2=3`; the PRD/L1 candidate was revised in response. The independent reviewer should try to falsify the corrections rather than assume they are sufficient.

## Reviewer identity

Use a genuinely independent high-capability Product reviewer that did not author or revise the v4.9 Draft PRD/L1 candidate.

Default mode: **READ-ONLY**.

The reviewer must not edit PRD/L1/branch/PR, create L2/Task DAG/implementation, perform Product Freeze, or silently switch to a successor HEAD.

## Required inputs

Read at minimum:

1. dedicated Product Review Issue and its pinned exact PR #698 HEAD/tree;
2. current PR #698 changed files;
3. `docs/implementation/4.9.0/PRD.md`;
4. `docs/implementation/4.9.0/L1_PRODUCT_EVIDENCE.md`;
5. `docs/implementation/4.9.0/PLANNING_STATUS.md`;
6. #680 full planning/PRACTICE-01/adaptive-orchestration/recurrence thread;
7. #697 planning parent;
8. PR #698 author-side pre-review comment `5961233246` only as historical finding/disposition context, not independent evidence;
9. current main Development Workflow, Execution Architecture, GitHub interaction/work-item, model, Review, Validation and Release standards as needed;
10. v4.8 Frozen Product/L2 and #646/T-017 where capability/scheduling/Dispatch/Claim/execution ownership overlaps.

## Adversarial objectives

### A. Evidence and generality

- Is orchestration amplification a real Product problem?
- Is L1 appropriately honest that `DOWNSTREAM_GENERALITY=PARTIAL`?
- Is downstream manual/GitHub-native dogfood before release an adequate safeguard against an ADS-self-only optimization?
- Are unsupported cost/performance claims avoided?

### B. Product coherence and size

- Do P1 Proportional Assurance, P2 Adaptive Orchestration, P3 Agent Operating Model and bounded P4 Execution Learning form one coherent loop?
- Does bounding P4 to lightweight learning/recurrence escalation keep v4.9 coherent for one minor version?
- If still too large, identify a coherent narrower boundary rather than arbitrary feature cutting.

### C. Monotonic assurance / authority safety

Try to break the revised `ASSURANCE_FLOOR` rule:

- Can a strong model still turn its own materiality judgment into gate-omission authority?
- Does reduction require **positive permission** from higher authority rather than mere absence of prohibition?
- Does UNKNOWN/ambiguity fail closed or escalate?
- Can project overrides or dynamic profiles weaken Frozen/current authority?
- Can the Orchestrator accidentally become Product/Architecture/Review/Validation/Release authority?

### D. Release path preservation

- Is current/pinned Release authority unequivocally the owner of release applicability?
- Can the Orchestrator label work `not release-significant` and escape currently mandatory Stage1/Freeze/Hidden/Closeout/RQ?
- Are older pinned project semantics preserved?
- Does unknown release applicability fail closed?

### E. Typed evidence transfer / currentness

Try to falsify the new positive-transfer model:

- Are gate-specific binding dimensions necessary and sufficient?
- Can disjoint paths, unchanged HEAD/tree or ancestor topology still launder stale PASS?
- Does `NO_TRANSFER_RULE => HISTORICAL_ONLY` hold?
- Can a changed base/target/merge-result/authority/profile/environment/private-pack/predecessor binding escape detection?
- Can a Gate Authority declare evidence non-transferable even if structural identity appears equivalent?

### F. Independence under phase coalescing

Try to demonstrate independence laundering:

- Is distinct session identity incorrectly accepted as principal/executor independence?
- Are model/context/executor/evidence/environment/Hidden-holder/author-reviewer dimensions preserved where required?
- Can one durable Issue still carry independent phases without ambiguous role/claim/terminal history?
- When must a separate durable container/environment remain mandatory?

### G. Task DAG and runtime scope

- Can adaptive orchestration invent a new semantic implementation concern, ownership boundary or dependency without amendment?
- Is JIT materialization clearly limited to authorized role phases/gates/containers inside current Task authority?
- Does this remain compatible with GitHub Issue Dependencies as canonical live execution DAG?

### H. v4.8 ownership preservation

- Does v4.9 reuse capability/availability/eligibility/resource selection and Dispatch/Claim rather than create another scheduler/lease/task lifecycle?
- Does the Agent Operating Model add role behavior without stealing v4.8 authority?

### I. Role model quality

- Are Role vs Agent, Builder vs Reviewer, Reviewer vs Validator, Controller vs gate authority sufficiently distinct?
- Are Base Contract + Role Profile dimensions machine-checkable enough without hard-coding providers/tools?
- Are Planner/Product Researcher, Architect, Integration, Hidden, Release Qualifier and specialized roles extensible while still declaring terminal authority, mutation class, environment and independence policy?

### J. Learning/recurrence boundary

- Is P4 genuinely lightweight?
- Can recurrence evidence create false root-cause equivalence, surveillance/logging explosion or automatic standard mutation?
- Is a universal recurrence-mining/database platform clearly out of scope?

### K. Compatibility/adoption

- Can a downstream project remain manual/GitHub-native without a scheduler daemon?
- Are historical v4.x durable facts and pinned older authority preserved?
- Can transport mappings such as A2A remain non-authoritative for ADS Review/Validation/Release truth?

## Severity

```text
P0 = Product unsafe/contradictory/unfreezable
P1 = material Product requirement/boundary missing or wrong; must fix before Freeze
P2 = important clarification/improvement; disposition required before/at Freeze
P3 = nonblocking editorial/future refinement
```

## Fixed terminal

```text
V49_ADVERSARIAL_PRODUCT_REVIEW=PASS|FAIL|BLOCKED
REVIEW_MODE=READ_ONLY
INDEPENDENCE=PASS|FAIL
SUBJECT_HEAD=<exact sha>
SUBJECT_TREE=<exact tree>
CURRENTNESS=PASS|FAIL|BLOCKED
L1_EVIDENCE=SUFFICIENT|PARTIAL|INSUFFICIENT
DOWNSTREAM_GENERALITY=SUFFICIENT_FOR_PRODUCT_FREEZE_WITH_RELEASE_DOGFOOD|INSUFFICIENT
PRODUCT_PROBLEM=SUPPORTED|PARTIAL|UNSUPPORTED
PRODUCT_COHERENCE=PASS|FAIL
ASSURANCE_FLOOR_SAFETY=PASS|FAIL
V48_OWNERSHIP_PRESERVED=PASS|FAIL|BLOCKED
AUTHORITY_GUARDRAILS=PASS|FAIL
TASK_DAG_SCOPE_BOUNDARY=PASS|FAIL
ROLE_MODEL=PASS|FAIL
INDEPENDENCE_MODEL=PASS|FAIL
EVIDENCE_TRANSFER_SAFETY=PASS|FAIL
RELEASE_PATH_PRESERVATION=PASS|FAIL
P4_SCOPE_BOUNDARY=PASS|FAIL
COMPATIBILITY=PASS|FAIL|PARTIAL
SCOPE_SIZE=COHERENT|TOO_LARGE|TOO_SMALL
P0=<n>
P1=<n>
P2=<n>
P3=<n>
PRODUCT_FREEZE_RECOMMENDATION=READY_AFTER_FINDINGS|NOT_READY
FINDINGS=<numbered findings with evidence and required correction>
VERDICT=PASS|FAIL|BLOCKED
NEXT=PRODUCT_FINDING_DISPOSITION|PRODUCT_FREEZE_CONTROLLER|BLOCKED
```

A PASS recommends Product Freeze readiness only after any required disposition. Reviewer itself does not freeze Product authority.