# Agent Capability Evidence v1 Reference

Agent Capability Evidence records bounded **historical exact-subject observations** about a logical Agent/task capability. Positive and negative observations are equally valid evidence. This family is not current Availability, authorization, routing authority, Validation PASS, Review PASS or a universal quality score.

## Identity and currentness

`exact_subject_ref` binds evidence to the artifact/code actually observed. For code/artifact subjects in this contract it is a canonical immutable Git identity of the form `git:<owner>/<repository>@<40-lowercase-hex-commit-sha>`. Mutable branches, symbolic refs, tag/ref aliases, repository-only references, short SHAs and malformed/non-hex SHAs are not exact subjects and must fail closed rather than establish current applicability.

`observed_at_or_currentness_scope` states the temporal/currentness scope. When the implementation subject, environment or other material input drifts, the old record remains historical; a consumer must not silently rebind it to the successor. In particular, textual equality of a mutable alias such as `@main` is never sufficient proof that two observations refer to the same artifact/code generation.

Agent/profile, runner/environment/resource and pack identities are **references**. Their owner facts stay in their canonical owners rather than being copied into capability evidence.

## Evidence strength

- `IDENTITY_BOUND` — provenance and subject identity are known.
- `BEHAVIOR_SUPPORTED` — cited result/validation evidence supports the bounded behavior claim.
- `INDEPENDENTLY_CHALLENGED` — cited independent Validation/Review challenged the relevant claim.

These layers are not a scalar rank. Historical `INDEPENDENTLY_CHALLENGED` evidence still does not become current Review/Validation PASS.

## Positive and negative evidence

`observation_kind` is `POSITIVE`, `NEGATIVE` or `MIXED`. Negative observations must not be discarded merely because later attempts succeed; they are useful for eligibility policy, escalation and failure-boundary learning when current and applicable.

## Economic/performance non-inference

`economic_measurement_status` distinguishes `NOT_MEASURED`, `MEASURED_COMPARABLE` and `MEASURED_NONCOMPARABLE`. A savings, latency-superiority or routing-policy conclusion requires an actually comparable methodology and the supporting refs outside this schema. `NOT_MEASURED` and non-comparable measurements cannot be promoted into an economic benefit claim. Provider/model identity is provenance only.

## Example

```json
{
  "schema_version": "ai-dev/agent-capability-evidence-v1",
  "evidence_id": "cap-evidence:T-016:001",
  "logical_operator_or_executor_ref": "operator:builder-a",
  "task_class_or_capability_class": "schema-contract-authoring",
  "role": "builder",
  "exact_subject_ref": "git:kaicreator-mm/ai-development-standard@1111111111111111111111111111111111111111",
  "result_refs": ["result:<ref>"],
  "evidence_strength": "IDENTITY_BOUND",
  "observed_at_or_currentness_scope": "historical:exact-subject-only",
  "observation_kind": "POSITIVE",
  "economic_measurement_status": "NOT_MEASURED"
}
```
