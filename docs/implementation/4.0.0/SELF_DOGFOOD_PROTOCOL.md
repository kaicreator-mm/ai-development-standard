# v4.0 Self-Dogfood Multi-Model Review Protocol

Status: CANDIDATE — T-010 / Issue #82 / R3 #143
Version: 4.0.0
Dogfood subject baseline: `version/v4.0.0@7a8c3c3608bc42325a1ac3c15a335747dea25ddb`

## 1. Purpose

This protocol dogfoods v4's own Assurance / adversarial-review semantics against the v4 architecture and machine-contract set after:

- first dogfood #127 exposed blocker/coverage/validation/release defects;
- second dogfood #135 independently exposed the Validation Report identity/execution blocker plus additional machine gaps;
- R2 machine hardening #140 / PR #141 / Fresh Review #142 closed GR1–GR16 and merged as `7a8c3c3608bc42325a1ac3c15a335747dea25ddb`;
- #142 left non-blocking FIR-1/2/3 carry-forward, which R3 closes before dogfood execution.

It deliberately separates:

```text
blind independent first passes
-> finding union
-> optional cross-challenge
-> conflict classification / executable evidence routing
-> explicit dispositions
-> aggregation
```

It does not use reviewer majority voting, and model diversity does not substitute for executable Validation.

The first and second dogfood records (#127 and #135) remain historical `CHANGES_REQUESTED` evidence. R3 does not relabel either PASS; it reviews the new post-hardening subject from scratch.

## 2. Frozen subject

The review subject is the exact repository tree at:

```text
repository: kaicreator-mm/ai-development-standard
ref: version/v4.0.0
subject_sha: 7a8c3c3608bc42325a1ac3c15a335747dea25ddb
```

Required subject set:

- `docs/implementation/4.0.0/ARCHITECTURE_DECISION.md`
- `docs/implementation/4.0.0/OPERATION_CONTRACT.md`
- `docs/implementation/4.0.0/ASSURANCE_PLAN.md`
- `docs/implementation/4.0.0/ADVERSARIAL_REVIEW.md`
- `docs/implementation/4.0.0/AGENT_INTERCHANGE.md`
- `docs/implementation/4.0.0/OPERATION_ROUTING_INTEGRATION.md`
- `docs/implementation/4.0.0/WORK_ITEM_OPERATION_INTEGRATION.md`
- `docs/implementation/4.0.0/VALIDATION_RELEASE_INTEGRATION.md`
- v4 machine schemas registered in `standard-manifest.json`
- `scripts/v40_rules.py` as legacy primitives
- `scripts/v40_r2_hardening.py`
- `scripts/v40_semantics.py` as the canonical v4 semantic facade
- `scripts/test_v40_operation_contracts.py`
- `scripts/test_v40_final_hardening.py`
- `scripts/test_v40_dogfood_hardening.py`
- `scripts/test_v40_r2_machine_hardening.py`
- `templates/golden/V4_DOGFOOD_HARDENING_EXAMPLES.json`
- `templates/golden/V4_R2_MACHINE_HARDENING_EXAMPLES.json`

The moving T-010 R3 branch changes are not part of the dogfood subject. Recording dogfood evidence must not invalidate the evidence itself.

## 3. R3 pre-dogfood hardening

Before any R3 blind dispatch, Stage A must prove the three #142 carry-forward items are closed on the R3 candidate:

1. `model_diversity_basis` is machine-enforced when multiple materialized MDA lanes exist; `provider-diverse` requires distinct providers and rejects same-model reuse disguised by family labels.
2. Hidden shared-metadata allow-listed values are public scalar metadata, not structured containers capable of carrying fixture/oracle payload.
3. malformed canonical semantic inputs return structured fail-closed errors instead of uncaught exceptions.

These changes are candidate/protocol hardening. The dogfood subject remains the exact integrated baseline above so the review evaluates the hardened integration state that existed before T-010 evidence-recording commits.

## 4. Assurance Plan

R3 materializes two independent blind lanes under one declared basis. The default R3 basis is **provider-diverse** because it is directly auditable and was already feasible in R2.

Logical plan:

```yaml
assurance_plan_id: dogfood:v4:t010:r3
operation_id: op:v4:t010:dogfood:r3
subject_identity_ref: sha:7a8c3c3608bc42325a1ac3c15a335747dea25ddb
identity_binding: exact-sha
finding_disposition_policy: p2-and-p3-explicit
activities:
  - assurance_id: dogfood:r3:blind-a
    kind: review
    policy: required
    mode: model-diverse-adversarial
    model_diversity_basis: provider-diverse
    blind_first_pass_ref: <durable ref after publication>
    independence_basis_ref: <durable provenance ref>
    coverage: [authority, lifecycle, operation, assurance, model-diversity, findings, aggregation, exchange, routing, validation, candidate-release, fast-path, machine-contract, compatibility]
    independence:
      context: required
      model: required
      executor: required
      evidence: none
  - assurance_id: dogfood:r3:blind-b
    kind: review
    policy: required
    mode: model-diverse-adversarial
    model_diversity_basis: provider-diverse
    blind_first_pass_ref: <durable ref after publication>
    independence_basis_ref: <durable provenance ref>
    coverage: [authority, lifecycle, operation, assurance, model-diversity, findings, aggregation, exchange, routing, validation, candidate-release, fast-path, machine-contract, compatibility]
    independence:
      context: required
      model: required
      executor: required
      evidence: none
  - assurance_id: dogfood:r3:aggregate
    kind: review
    policy: required
    mode: cross-peer
    depends_on: [dogfood:r3:blind-a, dogfood:r3:blind-b]
aggregation:
  policy: finding-union-blocker-dominance
  majority_vote_for_correctness: false
```

The durable first-pass result for each blind lane must record at least:

```text
provider
model_family
model_id
executor_id
context_ref
blind_first_pass_ref
```

For `provider-diverse`, aggregate PASS requires at least two distinct providers and at least two distinct model IDs. A family-label change does not make identical model execution materially diverse.

If the coordinator cannot obtain genuine provider diversity, it must publish `BLOCKED_MODEL_DIVERSITY`. It may not silently change the declared basis after seeing reviewer outputs merely to obtain PASS.

## 5. Blind first-pass rules

Each blind reviewer receives only:

1. exact subject SHA and subject file set;
2. frozen authority refs;
3. coverage matrix below;
4. exact review question/falsification goal;
5. existing executable verifier evidence for the frozen subject when relevant as evidence input.

Before its first-pass finding set is durable, a reviewer MUST NOT read:

- sibling R3 review conclusions/findings;
- coordinator aggregation;
- detailed historical findings, probes, proposed fixes or severity settlements from #127/#128/#129/#135/#138/#139/#142.

A reviewer may know only that earlier dogfood rounds produced hardening. This prevents R3 from becoming a checklist replay of known answers.

After both R3 first passes are durable, the coordinator may expose sibling reviews and historical detailed findings for cross-challenge and regression comparison.

The first-pass record must state that sibling and historical detailed conclusions were not consumed before publication.

## 6. Coverage matrix

Both blind passes must independently assess:

| Dimension | Falsification goal |
|---|---|
| authority | find any path where a lower-level Operation/Agent manufactures higher authority |
| lifecycle | find any second lifecycle / flat-state collapse / third execution DAG |
| Operation | find ambiguity between kind/type/subject/authority/correlation |
| Assurance | find missing separation of policy/mode/coverage/independence/aggregation |
| model diversity | find false independence claims, basis mismatch, same-model reuse, or collaborative work mislabeled blind/model-diverse |
| findings | find silent finding erasure, identity collision, invalid duplicate/superseded resolution, severity-dominance bypass |
| aggregation | find majority-vote, blocker-waiver, ghost-ref, plan/result/provenance or required-coverage bypass |
| exchange | find transport/ACK/interchange becoming workflow/Gate/Validation truth |
| routing | find derived route state overriding owning truth dimensions |
| Validation | find PASS without actual execution or exact identity, including report/event paths and malformed-input handling |
| Candidate/Release | find collapse of preparation/freeze/hidden/release/integration or verdictive release over non-frozen/wrong identity |
| Fast Path | find reduced-truth path disguised as reduced ceremony, including unknown/misspelled predicates or authority contradiction |
| machine contract | find prose invariant not enforced, schema/facade contradiction, or bypass through legacy primitives |
| compatibility | find released v3.4 invariant weakened by v4 hardening |

## 7. Finding record

Each material first-pass finding must be durable and contain at least:

```text
finding_id
reviewer/assurance ref
subject_identity_ref
coverage dimension
severity P0/P1/P2/P3
bounded claim
evidence refs
counterexample/failure mode when applicable
proposed disposition when available
```

Finding IDs must be globally unique across both blind passes. Duplicate finding identities are invalid machine input; semantically equivalent claims keep distinct source IDs and may later be linked/grouped.

P0/P1 are blocker-class by severity. A contradictory `blocking=false` is invalid input and cannot waive blocker dominance.

## 8. Cross-challenge

Cross-challenge occurs only after both first passes are durable.

For each disputed finding, record:

```text
challenged finding id
specific disputed claim
counter-evidence/counterexample
conflict class
requested resolution route
```

Conflict classes:

- `FACT_CONFLICT`
- `AUTHORITY_INTERPRETATION_CONFLICT`
- `APPLICABILITY_CONFLICT`
- `SEVERITY_CONFLICT`
- `EVIDENCE_ADEQUACY_CONFLICT`
- `DUPLICATE_OR_OVERLAP`

Factual/runtime uncertainty routes to executable Validation; it is not settled by reviewer agreement.

## 9. Aggregation

The final dogfood aggregate must:

1. bind to exact subject `7a8c3c3608bc42325a1ac3c15a335747dea25ddb`;
2. include durable PASS/non-PASS results for both required blind activities;
3. satisfy the declared `provider-diverse` basis with durable provenance before aggregate PASS is possible;
4. attest every required coverage dimension for each required activity;
5. preserve the full finding union and reject ghost/duplicate finding identities;
6. explicitly disposition every P2 and every P3 for this exercise;
7. keep every unresolved valid P0/P1 in `unresolved_blocker_refs` by severity;
8. reject duplicate/superseded severity weakening;
9. keep `requested_route_authority = NON_AUTHORITATIVE_DERIVED_STATE`;
10. never use majority vote for correctness;
11. record any executable Validation request instead of inventing runtime truth;
12. yield exactly one of `PASS | CHANGES_REQUESTED | VALIDATION_REQUESTED | BLOCKED`.

## 10. Historical regression comparison

Only after both R3 blind first passes are durable, compare the R3 union against prior blocker/hardening classes from #127 and #135/#142.

The comparison must answer whether prior defects reproduce on the frozen subject, but non-reproduction of known defects is never proof that no new defect exists.

Historical findings remain immutable and retain their original outcomes.

## 11. Durable GitHub evidence layout

R3 uses GitHub durable records rather than hidden chat state:

```text
R3 Dogfood coordinator Issue
  -> Blind Review A durable child/ref
  -> Blind Review B durable child/ref
  -> optional cross-challenge comments/refs
  -> aggregate result record
```

The two first-pass records must be separately durable before cross-reading is allowed. A coordinator may orchestrate the exercise, but it must not write both independent reviews from one model/context and call that model diversity.

## 12. Acceptance

Dogfood PASS for T-010 R3 requires:

- two blind first-pass results meeting declared context/model/executor independence;
- exact `provider-diverse` basis satisfied by durable provenance;
- complete required coverage attestation;
- durable finding union and conflict/disposition records;
- no unresolved P0/P1;
- every P2/P3 explicitly dispositioned;
- exact frozen subject identity preserved;
- aggregation satisfying current machine semantics;
- any runtime claim supported by owning executable evidence rather than review consensus;
- prior dogfood blocker classes checked after blind publication without assuming known-regression success proves global correctness.

T-010 completion additionally requires normal exact-head repository validation and required Fresh Independent Review of the final T-010 PR itself. Dogfood review is evidence about the frozen v4 subject; it does not replace PR Review or CI.

## 13. Intentionally collaborative mode

If reviewers intentionally collaborate before independent first passes, the activity must change mode/independence claim (for example `cross-peer` collaborative analysis with no model-independence claim). It must not retain `model-diverse-adversarial` blind-independence semantics.

## 14. Boundary

This protocol creates T-010 dogfood evidence only. It does not perform T-011 migration/adoption, T-012 version closure review, or T-013 Release Qualification/repository integration.
