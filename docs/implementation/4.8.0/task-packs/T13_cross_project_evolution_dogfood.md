# T-013 Task Pack — Cross-Project ADS Evolution Dogfood

Status: **CANDIDATE TASK PACK — NOT BUILDER READY**

Authority: Frozen DAG R1 blob `72dfeee93c092296004c7083b71fdd877d7f1b34`; Issue #519.

```yaml
task_id: T-013
dependencies: [T-004, T-005, T-006, T-010]
integration_target: version/v4.8.0
review_policy: required
validation_scope: cross-project-evidence
validation_owner: independent-from-evidence-author
l3_requirement: required
agent_freedom: F1
jit_branch: true
execution_pack: JIT
```

Allowed write set: `docs/implementation/4.8.0/dogfood/evolution/**` and bounded evidence references. Forbidden: single-project universal inference, self-amending change, private project evidence publication.

Acceptance: use at least two materially distinct project/task streams when available; exercise classification/false-positive prevention/repeated-friction; reject project-specific/environment/Agent defects as standard changes; exercise `MORE_EVIDENCE`/`NO_CHANGE` and justified ADS evolution handoff with privacy boundaries.

Required evidence matrix: every evaluated stream/scenario must record at least `evidence_kind=SYNTHETIC|REAL`, exact subject/evidence-stream identity, source project/task, material environment/runtime identity, expected oracle, actual result, privacy/publication classification, and `external_claim_eligible=YES|NO` with supporting reference. Synthetic evidence must remain labeled synthetic and cannot satisfy a real-world runtime/provider/project claim. Any real/external claim requires exact-subject external or independent evidence appropriate to the claim; unavailable required real evidence is `NOT_RUN|BLOCKED` with an explicit validation handoff, never synthetic PASS.

Required Validation: cross-project currentness/privacy/evidence-strength validation. Fresh Review required. Validation must confirm that external claims do not exceed the strongest eligible REAL evidence in the matrix.