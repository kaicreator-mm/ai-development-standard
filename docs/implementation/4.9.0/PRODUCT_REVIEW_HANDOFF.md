# v4.9.0 Product Review Handoff

Status: **READY FOR INDEPENDENT ADVERSARIAL PRODUCT REVIEW**

This handoff defines review scope only. The dedicated GitHub Product Review Issue must pin the exact Draft PR HEAD/tree before execution.

## Reviewer identity

Use a genuinely independent high-capability Product reviewer that did not author the v4.9 Draft PRD/L1 candidate.

Default mode: **READ-ONLY**.

The reviewer must not edit the PRD, L1, branch or PR; must not create L2/Task DAG/implementation; and must not declare Product Freeze itself.

## Required inputs

Read at minimum:

1. dedicated Product Review Issue and its pinned exact PR HEAD/tree;
2. `docs/implementation/4.9.0/PRD.md`;
3. `docs/implementation/4.9.0/L1_PRODUCT_EVIDENCE.md`;
4. `docs/implementation/4.9.0/PLANNING_STATUS.md`;
5. planning input/dogfood `#680` including PRACTICE-01/adaptive-orchestration/recurrence evidence;
6. planning parent `#697`;
7. current main `standards/DEVELOPMENT_WORKFLOW.md`;
8. current execution/interaction/model/review/validation/release standards as needed;
9. v4.8 Frozen Product/L2 and T-017/#646 where ownership overlap is material.

## Adversarial objectives

Attack the Product candidate rather than merely proofreading it.

At minimum determine:

### A. Problem/evidence validity
- Is task/gate explosion sufficiently evidenced as a general ADS Product problem rather than repository-local inconvenience?
- Do PRACTICE-01 examples actually support reduced orchestration without hidden assurance loss?
- Are unsupported economic/performance claims avoided?

### B. Product coherence
- Do P1 Proportional Assurance, P2 Adaptive Orchestration, P3 Agent Operating Model and P4 Execution Learning form one coherent Product loop?
- Is v4.9 too large for one minor version? If so, identify a coherent narrower Product boundary rather than arbitrary feature cutting.

### C. Authority safety
- Can an Orchestrator optimistically down-classify risk or waive Frozen authority?
- Can phase coalescing hide required actor/session independence?
- Can evidence equivalence launder stale PASS after material change?
- Are full release/Hidden/Closeout/RQ paths still unequivocally preserved when required?

### D. Ownership overlap
- Does v4.9 duplicate or contradict v4.8 capability/eligibility/scheduling/Dispatch/Claim ownership?
- Does the Agent Operating Model correctly extend accepted Claim/start semantics rather than create another lifecycle?
- Does Task-DAG reinterpretation conflict with canonical live Issue Dependency semantics?

### E. Role model quality
- Are Role vs Agent, Reviewer vs Validator, Builder vs Reviewer, Controller vs independent gate authority sufficiently distinct?
- Are the Base Contract + Role Profile semantics machine-checkable enough to be useful without hard-coding vendors/tools?
- Are specialized/project roles still extensible?

### F. Currentness / evidence reuse
- Are fail-closed boundaries strong enough?
- What counterexamples make path-disjointness or unchanged HEAD insufficient evidence equivalence?
- Which Product-level invariants must be explicit before L2 is allowed to design the mechanism?

### G. Learning/recurrence
- Can recurrence detection create false root-cause equivalence or surveillance/logging overhead?
- Does learning remain evidence rather than self-amending authority?

### H. Compatibility/adoption
- Can downstream projects remain manual/GitHub-native without deploying a scheduler service?
- Is additive compatibility with historical v4.x durable facts credible?

## Severity

Use:

```text
P0 = Product unsafe/contradictory/unfreezable
P1 = material Product requirement/boundary missing or wrong; must fix before Freeze
P2 = important clarification/improvement; disposition required before/at Freeze
P3 = nonblocking editorial/future refinement
```

## Fixed terminal

Return a durable terminal in this shape:

```text
V49_ADVERSARIAL_PRODUCT_REVIEW=PASS|FAIL|BLOCKED
REVIEW_MODE=READ_ONLY
INDEPENDENCE=PASS|FAIL
SUBJECT_HEAD=<exact sha>
SUBJECT_TREE=<exact tree>
CURRENTNESS=PASS|FAIL|BLOCKED
L1_EVIDENCE=SUFFICIENT|PARTIAL|INSUFFICIENT
PRODUCT_PROBLEM=SUPPORTED|PARTIAL|UNSUPPORTED
PRODUCT_COHERENCE=PASS|FAIL
V48_OWNERSHIP_PRESERVED=PASS|FAIL|BLOCKED
AUTHORITY_GUARDRAILS=PASS|FAIL
ROLE_MODEL=PASS|FAIL
EVIDENCE_REUSE_SAFETY=PASS|FAIL
RELEASE_PATH_PRESERVATION=PASS|FAIL
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

A PASS review recommends Freeze readiness only; the independent reviewer does not perform Product Freeze.
