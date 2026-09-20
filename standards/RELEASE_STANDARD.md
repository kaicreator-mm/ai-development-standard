# Release Standard

## 1. Purpose

Release Qualification decides whether one dependency-complete candidate satisfies frozen release authority. Task/PR PASS is not Release PASS.

The execution state model and bounded release/repository controllers are defined by `EXECUTION_ARCHITECTURE_STANDARD.md`; this file owns candidate and release authority.

## 2. Release inputs

Final qualification consumes, as applicable:

- frozen PRD/scope and Architecture/Contract;
- terminal Task DAG and declared deferred items;
- immutable candidate SHA + tree;
- required Validation reports/tuples;
- full regression/integration evidence;
- Critical Journeys;
- Hidden Validation;
- real platform/production build/package/install evidence;
- external boundary evidence;
- project-required Minimal CI/profile evidence;
- architecture/docs reconciliation;
- known limitations/deferred items;
- escaped-defect/Hidden-pack disposition when relevant.

Every mandatory input must trace to Gate Authority. CI is release-required only when frozen/project policy makes it so.

## 3. Candidate Prepared vs Candidate Frozen

```text
PREPARED
= identity/matrix/notes/pack/handoff can be prepared

FROZEN
= all required visible freeze gates PASS on one exact SHA/tree
```

A freeze record SHOULD include:

```text
candidate_sha
candidate_tree
candidate_ref
visible-closure evidence
pinned standard revision
frozen_at
actor/operator
```

Hidden Validation execution normally targets the frozen candidate.

## 4. Operational immutability

`CANDIDATE_FROZEN` is an operational state, not only a SHA variable.

While frozen:

- do not silently commit product/docs/evidence/workflow changes onto or move the declared candidate ref;
- record post-freeze evidence in Issue/events, immutable evidence storage, or independent Hidden storage when possible;
- before Hidden Validation, Release Qualification, and final repository integration, verify declared ref SHA and tree still match the freeze record.

If any required content change is needed:

```text
FROZEN
→ THAWED / INVALIDATED
→ fix/successor candidate
→ affected visible validation
→ new freeze
→ required Hidden Validation
→ new Release Qualification
```

Old evidence remains valid only for its old candidate/pack identities.

## 5. Hidden Validation and escaped defects

Hidden Validation is independent evidence, not proof that a pack is forever complete.

If a material defect is found after a prior Hidden PASS, classify it:

```text
OUT_OF_SCOPE
VISIBLE_TEST_GAP
HIDDEN_PACK_BLIND_SPOT
BOTH_VISIBLE_AND_HIDDEN_GAP
PACK_DEFECT
PRODUCT_DEFECT_NOT_SUITABLE_FOR_HIDDEN
```

A release-significant Hidden blind spot must be explicitly dispositioned before a successor release is READY. If the pack is strengthened:

- target the invariant/failure family independently rather than copy the visible regression fixture/test;
- create a new immutable private pack identity/revision/checksum;
- preserve prior pack/candidate evidence historically;
- distinguish pack defects from product defects;
- expose only public-safe disposition, never private fixture payloads.

`TEST_DATA_AND_SCENARIO_STANDARD.md` owns scenario/provenance/oracle quality.

## 6. Release verdict

Choose exactly one:

### READY
All frozen mandatory blockers are resolved, required gates PASS, implementation/docs/architecture are reconciled, and no undeclared scope gap remains.

### CONDITIONAL
All mandatory gates pass, but a documented non-blocking limitation is explicitly accepted by appropriate authority with impact and follow-up.

### BLOCKED
A release blocker remains, a mandatory gate is BLOCKED/NOT_RUN, candidate identity is not trustworthy, or scope/authority is unresolved.

### FAIL
A mandatory gate actually executed and failed, with no newer valid candidate evidence superseding it.

Never convert NOT_RUN/BLOCKED to PASS or old-candidate evidence to successor PASS.

## 7. Release sequence

Recommended Version Branch sequence:

```text
Integrated baseline
→ Candidate preparation
→ required visible Validation on exact SHA
→ Candidate Freeze
→ Hidden Validation
→ Final Closeout
→ Release Qualification
→ READY/CONDITIONAL/BLOCKED/FAIL
→ Repository Integration
→ immutable release baseline
→ optional tag / GitHub Release
```

Preparation work that does not mutate the future candidate may proceed early.

## 8. Repository Integration

After READY, final repository integration is a distinct bounded step.

Before integration re-read live candidate/main refs. Confirm the frozen candidate still matches its SHA/tree and target branch has not diverged in a way that changes the approved content.

Prefer fast-forward when valid. If a merge commit is required, distinguish:

```text
validated candidate SHA/tree
final main baseline SHA/tree
```

Verify required tree/content equivalence or project-declared final-main sanity. Integration must not smuggle new product changes into a qualified release.

## 9. Release identity

The canonical identity is immutable Git commit SHA (and tree where useful). Tag/GitHub Release are optional aliases/distribution objects.

Record at least:

```text
version
candidate frozen SHA/tree
final immutable baseline SHA/tree
standard version + revision
required Validation/CJ/Hidden/platform results
CI result when release-required
known limitations/deferred
pack/artifact identity when relevant
tag/release name when created
```

## 10. Version Closure checklist

Use `checklists/version-closure.md`. Closure must preserve truthful unresolved states; it may not rename FAIL/BLOCKED/NOT_RUN to manufacture READY.
