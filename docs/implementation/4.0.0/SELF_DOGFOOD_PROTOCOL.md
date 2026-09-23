# v4.0 Self-Dogfood Multi-Model Review Protocol

Status: CANDIDATE — T-010 / Issue #82 / R2 #133
Version: 4.0.0
Dogfood subject baseline: `version/v4.0.0@123c80420c6ae519e18647a76b30e489d52a8fe7`

## 1. Purpose

This protocol dogfoods v4's own Assurance / adversarial-review semantics against the v4 architecture and machine-contract set after the first dogfood #127 exposed blocker/coverage/validation/release defects and hardening PR #131 merged them.

It deliberately separates:

```text
blind independent first passes
-> finding union
-> optional cross-challenge
-> conflict classification / evidence routing
-> explicit dispositions
-> aggregation
```

It does not use reviewer majority voting, and model diversity does not substitute for executable Validation.

The first dogfood #127/#128/#129 remains historical `CHANGES_REQUESTED` evidence. R2 does not relabel it PASS; it reviews the new post-hardening subject from scratch.

## 2. Frozen subject

The review subject is the exact repository tree at:

```text
repository: kaicreator-mm/ai-development-standard
ref: version/v4.0.0
subject_sha: 123c80420c6ae519e18647a76b30e489d52a8fe7
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
- `scripts/v40_rules.py`
- `scripts/test_v40_operation_contracts.py`
- `scripts/test_v40_final_hardening.py`
- `scripts/test_v40_dogfood_hardening.py`
- `templates/golden/V4_DOGFOOD_HARDENING_EXAMPLES.json`

T-010 R2 branch changes are not part of the dogfood subject. This avoids evidence becoming stale merely because T-010 records the evidence.

## 3. Assurance Plan

Logical plan:

```yaml
assurance_plan_id: dogfood:v4:t010:r2
operation_id: op:v4:t010:dogfood:r2
subject_identity_ref: sha:123c80420c6ae519e18647a76b30e489d52a8fe7
activities:
  - assurance_id: dogfood:r2:blind-a
    kind: review
    policy: required
    mode: model-diverse-adversarial
    coverage: [authority, operation, assurance, aggregation, exchange, routing, validation-release, fast-path, machine-contract, compatibility]
    independence:
      context: required
      model: required
      executor: required
      evidence: none
  - assurance_id: dogfood:r2:blind-b
    kind: review
    policy: required
    mode: model-diverse-adversarial
    coverage: [authority, operation, assurance, aggregation, exchange, routing, validation-release, fast-path, machine-contract, compatibility]
    independence:
      context: required
      model: required
      executor: required
      evidence: none
  - assurance_id: dogfood:r2:aggregate
    kind: review
    policy: required
    mode: cross-peer
    depends_on: [dogfood:r2:blind-a, dogfood:r2:blind-b]
aggregation:
  policy: finding-union-blocker-dominance
  majority_vote_for_correctness: false
```

The actual durable result must record the model-diversity basis (for example provider-diverse or model-family-diverse). Two prompts to one continuing model/session do not satisfy this plan.

## 4. Blind first-pass rules

Each blind reviewer receives only:

1. exact subject SHA and subject file set;
2. frozen authority refs;
3. coverage matrix below;
4. exact review question;
5. existing executable verifier evidence for the subject, when relevant as evidence input;
6. first-dogfood findings only as named regression targets after the reviewer has independently attempted the corresponding falsification class, so the blind pass is not reduced to checking known fixes.

Before its first-pass finding set is durable, a reviewer MUST NOT read:

- sibling review conclusions;
- sibling findings;
- proposed aggregation;
- proposed fixes based on sibling review.

The first-pass record must state that sibling conclusions were not consumed before publication.

## 5. Coverage matrix

Both blind passes must independently assess:

| Dimension | Falsification goal |
|---|---|
| authority | find any path where a lower-level Operation/Agent manufactures higher authority |
| lifecycle | find any second lifecycle / flat-state collapse / third execution DAG |
| Operation | find ambiguity between kind/type/subject/authority/correlation |
| Assurance | find missing separation of policy/mode/coverage/independence/aggregation |
| model diversity | find false independence claims or collaborative work mislabeled blind/model-diverse |
| findings | find silent finding erasure, identity collision, invalid duplicate/superseded resolution, severity-dominance bypass |
| aggregation | find any majority-vote, blocker-waiver, ghost-ref, or required-coverage bypass |
| exchange | find transport/ACK/interchange becoming workflow/Gate/Validation truth |
| routing | find derived route state overriding owning truth dimensions |
| Validation | find any PASS without actual execution or identity binding, including validation-report path |
| Candidate/Release | find collapse of preparation/freeze/hidden/release/integration or verdictive release over non-frozen/wrong identity |
| Fast Path | find reduced-truth path disguised as reduced ceremony, including unresolved authority contradiction |
| machine contract | find prose invariant not enforced or schema/verifier contradiction |
| compatibility | find v3.4 invariant weakened by v4 hardening |

## 6. Finding record

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

## 7. Cross-challenge

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

## 8. Aggregation

The final dogfood aggregate must:

1. bind to the exact frozen subject SHA;
2. include durable results for both required blind activities;
3. attest every required coverage dimension for each required activity;
4. preserve the full finding union and reject ghost finding refs;
5. explicitly disposition every P2 and every P3 when complete disposition is selected;
6. keep every unresolved valid P0/P1 in `unresolved_blocker_refs` by severity, irrespective of a contradictory blocking flag;
7. reject duplicate finding IDs and any duplicate/superseded severity weakening;
8. keep `requested_route_authority = NON_AUTHORITATIVE_DERIVED_STATE`;
9. never use majority vote for correctness;
10. record any executable Validation request rather than inventing runtime truth;
11. yield one of `PASS | CHANGES_REQUESTED | VALIDATION_REQUESTED | BLOCKED`.

## 9. Durable GitHub evidence layout

T-010 R2 uses GitHub durable records rather than hidden chat state:

```text
R2 Dogfood coordinator Issue
  -> Blind Review A durable child/ref
  -> Blind Review B durable child/ref
  -> optional cross-challenge comments/refs
  -> aggregate result record
```

The two first-pass records must be separately durable before cross-reading is allowed. A coordinator may orchestrate the exercise, but it must not write both independent reviews from one model/context and call that model diversity.

## 10. Acceptance

Dogfood PASS for T-010 R2 requires:

- two blind first-pass results meeting the declared context/model/executor independence;
- complete required coverage attestation or explicit non-PASS for missing coverage;
- durable finding union and conflict/disposition records;
- no unresolved P0/P1;
- exact subject identity preserved;
- aggregation satisfying current post-hardening machine semantics;
- any runtime claim supported by owning executable evidence rather than review consensus;
- the known #127 blocker classes no longer reproduce, without assuming that this proves absence of new defects.

T-010 completion additionally requires normal exact-head repository validation and required Fresh Independent Review of the final T-010 PR itself. Dogfood review is evidence about the v4 subject; it does not replace PR Review or CI.

## 11. Intentionally collaborative mode

If reviewers intentionally collaborate before independent first passes, the activity must change mode/independence claim (for example `cross-peer` collaborative analysis with no model-independence claim). It must not retain `model-diverse-adversarial` blind-independence semantics.

This explicitly carries forward #110's requirement that collaborative review and blind independent review are distinguishable and auditable.

## 12. Boundary

This protocol creates T-010 dogfood evidence only. It does not perform T-012 version closure review or T-013 Release Qualification.
