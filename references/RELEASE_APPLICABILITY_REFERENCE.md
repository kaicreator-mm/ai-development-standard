# Release Applicability Reference

This reference illustrates `RELEASE_STANDARD.md` §11. It does not create Release authority or a parallel lifecycle.

## Canonical decision vocabulary

```text
REQUIRED_NOW
DEFERRED_TO_VERSION_CLOSURE
NOT_APPLICABLE
UNKNOWN
```

Every decision is Release-owned and bound to a specific gate × subject. A concern-level decision is never a version-level release verdict.

## Positive examples

### Required now

A change alters a release-significant compatibility contract and the current Release rule requires Hidden Validation before qualification:

```text
gate_id=hidden-validation
subject_ref=pr:123
subject_identity=sha:<exact>
applicability=REQUIRED_NOW
release_authority_ref=standards/RELEASE_STANDARD.md
basis_or_proof_refs=[<current authority/evidence>]
```

The gate must run for the bound subject. Another concern's `NOT_APPLICABLE` decision cannot cancel it.

### Deferred to Version Closure

A bounded concern may proceed without a version-level release gate when Release authority positively permits deferral:

```text
gate_id=release-qualification
subject_ref=issue:456
applicability=DEFERRED_TO_VERSION_CLOSURE
```

This is not a PASS and not a permanent omission. Version Closure must freshly evaluate the composed version candidate.

### Not applicable

A Release-owned deterministic rule proves that a specific gate does not apply to an exact subject:

```text
applicability=NOT_APPLICABLE
basis_or_proof_refs=[release-rule:<id>, deterministic-proof:<id>]
```

The result is valid only while all bindings required by Release authority remain current.

## Negative examples

The following are invalid reductions:

```text
risk:low => NOT_APPLICABLE
files_changed=1 => NOT_APPLICABLE
docs-only label => NOT_APPLICABLE
PR PASS => VERSION RELEASE PASS
concern NOT_APPLICABLE => version NOT_APPLICABLE
UNKNOWN => NOT_APPLICABLE
DEFERRED_TO_VERSION_CLOSURE => gate satisfied
```

A Builder, Reviewer, Validator, scheduler/orchestrator, CI job, or model cannot mint Release applicability merely because its local concern passed.

## Currentness examples

A previously valid applicability record becomes historical when a required binding materially changes, including candidate identity, Release authority/rule, proof evidence, unresolved release-significant findings, migration state, or composed version scope.

Re-evaluation produces a new attributable decision. It does not edit old history into current permission.

## Migration example

A project may prospectively adopt a newer Release applicability profile through the owning migration/adoption authority. That adoption cannot retroactively remove gates already bound to an in-flight Frozen or qualified candidate.

## Fail-closed rule

```text
UNKNOWN_OR_AMBIGUOUS_OWNER
OR UNKNOWN_OR_AMBIGUOUS_GRANULARITY
OR MISSING_OR_STALE_PROOF
OR NONCURRENT_SUBJECT_BINDING
=> STRONGER_EXISTING_RELEASE_PATH_OR_BLOCKED
```

Existing thaw, Hidden Validation, Final Closeout and Release Qualification rules remain authoritative whenever applicable.
