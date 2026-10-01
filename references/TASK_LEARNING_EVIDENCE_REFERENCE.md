# Task Learning Evidence v1 Reference

Task Learning is compact durable engineering evidence. It does not own Product, Architecture, Task, ADR, Incident, Review, Validation, merge or release decisions.

## Fast Path

When a completed work item produced no reusable material learning, record only:

```text
TASK_LEARNING=NONE_MATERIAL
```

Do **not** instantiate an empty `task-learning-v1` object to satisfy process ceremony.

## Exact-subject currentness

A learning record that makes a code- or artifact-specific claim should set `implementation_subject_ref` to the immutable subject actually evidenced and `currentness_ref` to the currentness identity used when the record was produced. A consumer may apply that exact-subject claim only when both refs match the subject being evaluated. If the subject drifts, the record remains historical evidence; it is never silently rebound.

A record without enough exact-subject/currentness information may still preserve identity-bound historical context, but it must not be used as current behavioral proof.

## Evidence strength

- `IDENTITY_BOUND` — identity/provenance is durably bound; no behavioral correctness is implied.
- `BEHAVIOR_SUPPORTED` — cited tests/validation support the stated behavior for the evidenced subject and environment.
- `INDEPENDENTLY_CHALLENGED` — cited independent review/validation challenged the relevant claim.

Layers describe evidence strength; they are not a universal score and do not create current Review or Validation PASS.

## Summary and rationale

`summary` and optional `rationale_summary` contain externally useful engineering facts: reusable invariants, clarified constraints, bounded implementation rationale and known limitations. They must never require or preserve private chain-of-thought, hidden evaluator material, credentials, secrets or verbose internal scratch reasoning. Prefer references/digests over copied evidence bodies.

## Authority and evolution boundary

`authority_refs` identify higher authorities the learning was produced under; they do not transfer those authorities into the learning object. `friction_classification` may carry the Frozen v4.8 six-way observation classification, but T-001 does not own promotion semantics. `disposition` is non-empty routing/evidence metadata whose meaning remains subordinate to the applicable governance owner. Neither field can self-amend ADS.

## Minimal material example

```json
{
  "schema_version": "ai-dev/task-learning-v1",
  "learning_id": "learning:T-001:001",
  "repository_ref": "github:kaicreator-mm/ai-development-standard",
  "work_item_ref": "github:kaicreator-mm/ai-development-standard#507",
  "implementation_subject_ref": "git:kaicreator-mm/ai-development-standard@<exact-sha>",
  "authority_refs": ["task-pack:v4.8.0/T-001"],
  "summary": "Exact-subject learning remains historical after code drift.",
  "source_test_validation_review_refs": ["test:<ref>"],
  "confidence_layers": ["IDENTITY_BOUND"],
  "currentness_ref": "git:kaicreator-mm/ai-development-standard@<exact-sha>",
  "disposition": "RETAIN_LOCAL"
}
```
