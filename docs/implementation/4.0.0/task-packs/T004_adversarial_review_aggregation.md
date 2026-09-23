# T-004 Task Pack — Model-Diverse Adversarial Review, Findings and Aggregation

Issue: #76
Parent version: #72
Baseline: `74fa5892481e06f33db186d85e0c6d38a04dc508`
Review Policy: required
Risk: critical
Validation scope: concern
Agent freedom: F1_BOUNDED_IMPLEMENTATION

## Goal

Define adversarial review modes, blind-first-pass, finding union, cross-challenge, conflict resolution, aggregation, coherence review and AR0–AR3 derived semantics without creating a parallel review lifecycle or weakening Validation authority.

## Inputs

- merged T-001 authority / compatibility contract;
- merged T-002 Operation Contract;
- merged T-003 Assurance Plan;
- merged T-005 Agent Interchange contract;
- #98 event-v2 closed-enum compatibility obligation;
- released v3.4 Review/Validation/GitHub interaction authorities.

## Allowed changes

- `docs/implementation/4.0.0/ADVERSARIAL_REVIEW.md`;
- this Task Pack;
- T-004 pointer/metadata in `docs/implementation/4.0.0/TASK_PACKS.json`.

## Forbidden changes

- reducer/controller implementation;
- schema/verifier implementation;
- new event-v2 enum values;
- event-v3 creation;
- Validation truth semantics;
- release qualification implementation.

## Tests / review oracle

A reviewer must verify at least:

1. no-majority-vote correctness;
2. unresolved valid P0/P1 always block PASS;
3. blind-first-pass is defined for claimed independent perspectives;
4. same-model fresh context is not mislabeled model-independent;
5. model diversity is risk control, not evidence;
6. finding union preserves blocking findings and provenance;
7. challenge/conflict routes distinguish fact, authority, applicability, severity and evidence conflicts;
8. factual/runtime conflicts route to executable Validation rather than consensus;
9. Coherence Review does not replace Integration Validation;
10. AR0–AR3 remain expanded convenience profiles rather than hidden machine truth;
11. event-v2 closed enum compatibility constraint from #98 is preserved;
12. ordinary low-risk work is not forced into multi-model ceremony;
13. T-005 interchange ownership remains intact and T-004 does not redefine correlation/envelope semantics.

## Failure handling

- if conflict cannot be resolved from durable authority, route to higher authority/specialist/Validation rather than fabricate aggregation PASS;
- if new machine event semantics appear necessary, record the compatibility/versioning requirement for T-009; do not implement here;
- if required runtime facts are missing, return Validation-requested rather than infer.

## Completion

Repository verifier PASS on final exact HEAD + Fresh Independent Review PASS on same HEAD + focused merge to `version/v4.0.0`.
