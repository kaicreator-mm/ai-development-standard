# v4.0 Validation / Freeze / Hidden / Release Integration

Status: CANDIDATE — T-008 / Issue #80
Version: 4.0.0
Baseline: `version/v4.0.0@3a131497527bcc255c152635d42bcdc8cb5ba813`
Owning authorities: `standards/VALIDATION_STANDARD.md` + `standards/RELEASE_STANDARD.md` + `standards/EXECUTION_ARCHITECTURE_STANDARD.md`
Inputs: `OPERATION_CONTRACT.md`, `ASSURANCE_PLAN.md`, `OPERATION_ROUTING_INTEGRATION.md`, `AGENT_INTERCHANGE.md`

## 1. Purpose

This document maps v4 Operation/Assurance semantics onto existing Validation, Candidate Freeze, Hidden Validation, Release Qualification, and Repository Integration authority.

It does not redefine those authorities.

Core invariant:

```text
Operation kind/correlation may explain why evidence or a controller action exists.
It can never manufacture the truth owned by Validation, Candidate Freeze, Hidden Validation,
Release Qualification, or Repository Integration.
```

`PR PASS != Release PASS` remains normative.

## 2. Authority mapping

The following ownership remains unchanged:

```text
Validation truth / Gate state / Validation Tuple  -> VALIDATION_STANDARD
Candidate + Release authority                     -> RELEASE_STANDARD
Routing / controllers / orthogonal state          -> EXECUTION_ARCHITECTURE_STANDARD
Operation composition                             -> OPERATION_CONTRACT
Assurance requirements / independence             -> ASSURANCE_PLAN
Interchange correlation                           -> AGENT_INTERCHANGE
```

v4 maps these authorities into one lifecycle without merging them.

## 3. Validation as ASSURE Operation

A Validation activity may be represented/correlated as an `ASSURE` Operation when material.

That mapping is descriptive and compositional only.

```text
ASSURE operation exists       != Validation executed
Validator dispatch created    != Validation PASS
CI workflow created           != Validation PASS
CI provider success           != unexecuted platform/Hidden/CJ PASS
model/reviewer agreement      != Validation PASS
```

The authoritative Gate states remain:

```text
PASS | FAIL | BLOCKED | NOT_RUN | NOT_APPLICABLE
```

`PASS` still requires actual execution of the required Validation Tuple/profile on the required subject.

## 4. Exact-subject identity remains mandatory

Validation evidence stays bound to the exact identity where execution occurred.

At minimum the owning tuple remains:

```text
<exact tested SHA>
× <real platform/environment>
× <runtime/toolchain>
× <validation profile>
```

Operation/interchange correlation MAY add:

```text
operation_id
assurance_id
dispatch_id
caused_by
work_item_ref
```

Those fields do not replace the tuple.

No Operation, Assurance, or interchange record may rebind an old PASS to a successor SHA, platform, toolchain, profile, candidate, or release.

## 5. Drift and evidence composition

Existing drift classes remain authoritative:

```text
HEAD drift
BASE drift
MERGE-RESULT drift
CANDIDATE drift
```

A v4 Operation relationship does not make drift irrelevant.

Rules:

1. HEAD drift makes an exact-head validation/review dispatch stale for the old requested identity.
2. Base/merge-result drift requires the existing explicit impact/composition discipline when evidence reuse is proposed.
3. Evidence reuse never changes where the original tuple actually executed.
4. Unknown impact fails closed to revalidation.
5. Candidate drift invalidates candidate-bound downstream evidence for the replacement candidate unless an owning standard explicitly defines a valid composition rule.

Operation identity may remain stable across a successor concern; evidence identity does not.

## 6. Validation ownership remains concern / integration / closure

The v4 Operation Protocol does not flatten validation ownership.

```text
concern     -> smallest strict affected evidence intrinsic to the concern
integration -> explicit cross-component/composition owner
closure     -> dependency-complete release candidate and release-level matrix
```

An ASSURE Operation MUST resolve to the owning scope rather than causing every Task to inherit closure validation.

Conversely, a concern cannot defer a platform/runtime gate that is intrinsic to its own acceptance merely because closure also exists.

## 7. Review and Validation remain orthogonal

Review/adversarial aggregation can request Validation, challenge evidence adequacy, or identify missing coverage.

It cannot convert:

```text
NOT_RUN -> PASS
BLOCKED -> PASS
reviewer consensus -> runtime truth
model diversity -> platform evidence
```

A conceptual `VALIDATION_REQUESTED` review outcome is routing intent only. The owning Validation gate remains `NOT_RUN` until execution.

A valid Review PASS may coexist with required Validation `NOT_RUN/BLOCKED`; merge/release routing must preserve both facts.

## 8. Candidate PREPARED vs FROZEN remains separate

Candidate states remain:

```text
PREPARED
FROZEN
THAWED
INVALIDATED
```

`PREPARED` means candidate identity/matrix/notes/handoffs can be assembled.

`FROZEN` means all required visible freeze gates have PASS evidence on one exact candidate SHA/tree and the Candidate Freeze Controller has recorded that identity.

An Operation `CONTROL` record for candidate preparation is not a freeze.

A freeze record remains bound to at least:

```text
candidate_sha
candidate_tree
candidate_ref
visible-closure evidence
pinned standard revision
controller/operator identity
freeze time
```

## 9. Candidate Freeze as bounded CONTROL

Candidate Freeze may be represented as a `CONTROL` Operation/controller action.

That mapping does not merge Candidate Freeze with Release Qualification.

Before freeze the controller MUST re-read:

```text
candidate ref / SHA / tree
required visible Gate states
Review/closure prerequisites
current authority / pinned standard
absence of unresolved freeze-blocking findings
```

Freeze is a semantic controller effect and remains subject to stable idempotency/precondition identity from T-006.

A duplicate freeze request for the same already-frozen exact identity must not create a second semantic freeze.

A stale freeze request fails closed.

## 10. Operational immutability after freeze

While candidate state is `FROZEN`:

- do not silently move or mutate the declared candidate ref/tree;
- do not commit product/docs/evidence changes onto the frozen candidate merely to record later results;
- store post-freeze evidence in Issue/events/immutable evidence/independent Hidden storage where appropriate;
- re-check candidate SHA/tree before Hidden Validation, Release Qualification, and Repository Integration.

If required candidate content changes:

```text
FROZEN
-> THAWED / INVALIDATED
-> successor candidate
-> affected visible validation
-> new freeze
-> required Hidden Validation
-> new Release Qualification
```

Old evidence remains historical for the old candidate/pack identity.

## 11. Hidden Validation remains independent evidence

Hidden Validation may be represented as an `ASSURE` Operation, but its independence properties remain owned by Validation/Release/Test Scenario authority.

Requirements:

1. Hidden fixture/scenario/oracle content must not be exposed to the implementation context merely to satisfy Operation visibility.
2. Public/shared GitHub facts may record safe metadata such as packet/revision/digest/coverage class/leak-check/result/evidence ref.
3. The private Hidden packet identity/revision/checksum remains immutable for the evidence it produced.
4. Hidden PASS proves only the scenarios actually executed on the exact frozen candidate.
5. Reviewer/model agreement is not Hidden execution evidence.
6. A Hidden result is candidate-bound and cannot be moved to a successor candidate by correlation.

Transport-neutral interchange does not authorize copying private Hidden payloads into shared transport.

## 12. Hidden escaped-defect feedback remains append-oriented

If a material defect escapes an earlier Hidden PASS, retain the existing classification vocabulary:

```text
OUT_OF_SCOPE
VISIBLE_TEST_GAP
HIDDEN_PACK_BLIND_SPOT
BOTH_VISIBLE_AND_HIDDEN_GAP
PACK_DEFECT
PRODUCT_DEFECT_NOT_SUITABLE_FOR_HIDDEN
```

Rules:

- preserve the old Hidden PASS as historical evidence for its actual candidate/pack;
- record the escaped-defect classification separately;
- a release-significant blind spot requires disposition before successor READY;
- strengthening a private pack creates a new immutable pack identity/revision/checksum;
- strengthen the invariant/failure family independently rather than copy a visible regression fixture;
- keep private fixture contents private while publishing public-safe disposition metadata.

## 13. Release Qualification as DECIDE Operation

Release Qualification may be represented as a `DECIDE` Operation.

`DECIDE` identifies the authority-bearing decision activity; it does not predetermine the verdict.

Authoritative release verdict remains exactly one of:

```text
READY
CONDITIONAL
BLOCKED
FAIL
```

The Release Controller consumes the current frozen candidate and all mandatory release inputs required by frozen authority.

Rules:

1. `READY` requires every mandatory blocker resolved and required gates actually PASS.
2. `CONDITIONAL` requires mandatory gates PASS plus explicitly accepted non-blocking limitation under proper authority.
3. `BLOCKED` preserves mandatory NOT_RUN/BLOCKED/untrustworthy-identity/unresolved-authority conditions.
4. `FAIL` requires an actually executed mandatory failure not superseded by valid newer candidate evidence.
5. No Assurance aggregation or Operation completion can coerce a release verdict.

## 14. PR/Task PASS is not Release PASS

A Task/PR may satisfy concern-level implementation, Validation, and Review while the version candidate remains not release-ready.

Examples of still-missing release evidence can include:

```text
full regression
integration validation
Critical Journeys
real platform/production build
packaging/installability
Hidden Validation
external boundary checks
release docs/reconciliation
escaped-defect disposition
```

Therefore:

```text
PR merge readiness != candidate freeze readiness
candidate frozen     != release READY
release READY        != repository integration already completed
```

## 15. Repository Integration as CONTROL Operation

Repository Integration after a qualified release may be represented as a `CONTROL` Operation.

It remains distinct from Release Qualification.

Before mutation, the Repository Integration Controller MUST re-read:

```text
Release Qualification verdict
frozen candidate ref/SHA/tree
current target/main identity
expected integration topology
required tree/content-equivalence or final-main sanity policy
semantic-action idempotency/preconditions
```

It must not smuggle new product/content changes into a qualified release.

If integration creates a distinct merge commit, record both:

```text
validated frozen candidate SHA/tree
final immutable main baseline SHA/tree
```

The immutable commit identity remains canonical; tag/GitHub Release are optional aliases.

## 16. Operation lifecycle does not collapse candidate/release state

Forbidden flat-state interpretations include:

```text
operation=done -> candidate=FROZEN
operation=done -> release=READY
review=PASS -> release=READY
hidden dispatch=DONE -> Hidden PASS
repository integration requested -> release READY
```

Reducer/controller projections must keep workflow, Gate/Validation, provider, dispatch, candidate, and release dimensions orthogonal.

## 17. Evidence and interchange boundaries

Interchange may correlate Validation/Freeze/Hidden/Release records with:

```text
operation_id
exchange_id
dispatch_id
work_item_ref
subject identity
causation refs
operator attribution
```

But authority-bearing payloads remain owned by their standards.

A transport ACK, duplicate message, newer timestamp, or majority count cannot override exact evidence or release authority.

Corrections and supersession remain append-oriented.

## 18. Fast Path interaction

Fast Path does not erase release impact.

A bounded low-risk concern may omit ceremonial Operation materialization, but still must produce the required concern Validation/Review evidence and an explicit release-impact disposition.

Fast Path cannot be used to bypass:

- required candidate closure;
- required platform/CJ/Hidden gates;
- Candidate Freeze;
- Release Qualification;
- final integration safety when those apply to the version/release.

## 19. Machine-contract obligations for T-009

T-009 must encode/golden-test at least these non-weakening rules:

1. no PASS without actual Validation execution;
2. exact subject/profile identity cannot be weakened by `operation_id`/`identity_binding`/correlation;
3. review judgment/requested route cannot become Validation truth;
4. PREPARED/FROZEN/THAWED/INVALIDATED remain separate from release verdict;
5. candidate freeze requires exact SHA/tree + visible gate evidence;
6. frozen candidate mutation requires thaw/invalidate + successor flow;
7. Hidden evidence remains candidate/pack-bound and private payload is not required in shared interchange;
8. Release Qualification consumes the frozen candidate and mandatory evidence, and preserves NOT_RUN/BLOCKED;
9. `PR PASS != Release PASS` golden/forbidden cases;
10. Repository Integration requires READY + exact frozen identity preflight and cannot introduce unqualified content;
11. semantic controller idempotency/precondition rules apply to freeze/release/integration effects;
12. old evidence is never rewritten onto successor identities.

## 20. T-008 completion boundary

T-008 freezes the logical Validation/Freeze/Hidden/Release integration semantics only.

It does not implement:

- JSON schema changes;
- reducer/controller code;
- event-v2 enum changes or event-v3;
- Hidden fixtures/pack content;
- actual Candidate Freeze or Release Qualification for v4.0.0;
- T-009 verifier regressions;
- T-010 dogfood scenarios;
- T-012 closure;
- T-013 release integration.

The owning standards remain `VALIDATION_STANDARD.md`, `RELEASE_STANDARD.md`, and `EXECUTION_ARCHITECTURE_STANDARD.md`.