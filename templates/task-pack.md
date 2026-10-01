# Task Pack — <task-id> <name>

> Durable planning authority. Exact-base execution detail belongs to the JIT Execution Pack (`.agent/execution/<task-id>/`), not here.

```yaml
task_id:
repository:
version:
integration_target:            # e.g. version/vX.Y.Z
merge_target:
task_pack_ref:                 # stable identity of this pack
authority_refs: []             # applicable Frozen/Core normative owner pointers; reference, do not restate semantics
implementation_profile_refs: [] # applicable pinned profiles/languages/* and/or profiles/archetypes/* paths; empty only with truthful non-applicability
project_overrides_ref:         # .dev-standard/PROJECT_OVERRIDES.md selection/specialization pointer or not-required — <reason>
dependencies: []               # task ids; live execution DAG = Issue Dependencies
allowed_write_set: []          # path prefixes the executor may touch
forbidden_scope: []            # explicit prohibitions
acceptance: []                 # verifiable criteria
required_gates: []
validation_scope:              # concern | integration | closure
validation_owner:
review_policy:                 # required | recommended | not-required
l3_requirement:                # L3 Reference Pack pointer or not-required — <reason>
agent_freedom:                 # F0_MECHANICAL | F1_BOUNDED_IMPLEMENTATION | F2_ENGINEERING_DISCRETION | F3_ARCHITECTURE_REQUIRED
jit_branch: true               # task branch created only after dependencies merge
execution_pack:                # "JIT" | "not-required — <reason>"
```

## v4.3 authority / profile consumption

This template extends the existing Task Pack; it MUST NOT create a duplicate Task object/schema.

- `authority_refs` points to the applicable Frozen/Core owners rather than copying or redefining their semantics.
- `implementation_profile_refs` consumes explicit profile paths from the pinned v4.3 catalog. Profiles are mapping/default layers, not new Task or Product/Architecture authority.
- `project_overrides_ref` identifies the project selection/specialization/strengthening source when profiles are material. `PROJECT_OVERRIDES` MUST NOT weaken Frozen/Core or Task authority. Use `references/IMPLEMENTATION_PROFILE_ADOPTION_REFERENCE.md` for the canonical lightweight v4.3 PROJECT_OVERRIDES block shape.
- A historical Task Pack is not rewritten merely because v4.3 becomes available. New profile references are prospective when an implementation-profile decision is material.
- Fast Path/non-material work may keep profile references empty only with a truthful non-applicability rationale; reduced ceremony never weakens authority.
- Material post-materialization live-DAG changes follow `standards/TASK_DAG_GOVERNANCE_STANDARD.md` and `schemas/dag-mutation-record-v1.schema.json`; do not rewrite planning history to fabricate readiness.
- Ambiguous applicability or conflicting profile defaults fail closed to the owning planning/architecture/project authority. File/discovery order MUST NOT choose a winner.

## Why

<one paragraph: rationale, risk, planning decision this task encodes>

## Acceptance detail

<expand each acceptance criterion into a verifiable statement>

## Out of scope

<explicit non-goals; contradictions discovered at execution time route upward as TASK_PACK_DEFECT / ARCHITECTURE_CONTRADICTION / EXECUTION_PACK_INVALID — never silently resolved>
