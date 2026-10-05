# Task Learning Evidence v2 Reference

Task Learning Evidence v2 (`schemas/task-learning-v2.schema.json`) is a **versioned same-family successor of Task Learning Evidence v1**. The v4.8 Task Learning owner family is preserved: v2 adds only the bounded v4.9 execution-friction/recurrence fields (Frozen L2 §7.3, PRD §13) and creates no parallel learning family, evolution-intake lifecycle or authority path.

Historical v4.8 records stay valid under `schemas/task-learning-v1.schema.json` exactly as written; they are never re-interpreted, migrated or retro-fitted into v2.

## Fast Path (unchanged)

When a completed work item produced no reusable material learning, record only:

```text
TASK_LEARNING=NONE_MATERIAL
```

Do **not** instantiate an empty `task-learning-v1` or `task-learning-v2` object to satisfy process ceremony. Simple work may continue to record `NONE_MATERIAL` under the v4.8 owner.

## Family identity

A v2 record states its family identity explicitly:

```text
schema_version                  = ai-dev/task-learning-v2
owner_family                    = task-learning
predecessor_protocol_version    = ai-dev/task-learning-v1
```

All v1 core fields (`learning_id`, `repository_ref`, `work_item_ref`, `implementation_subject_ref`, `authority_refs`, `summary`, `rationale_summary`, `unexpected_constraint_refs`, `task_pack_or_l3_clarification_refs`, `reusable_invariant_refs`, `known_limitation_refs`, `source_test_validation_review_refs`, `confidence_layers`, `currentness_ref`, `disposition`) keep their v1 semantics unchanged, including the exact-subject currentness rule of the v1 reference.

## New v4.9 fields (optional, references only)

| Field | Meaning |
|---|---|
| `execution_friction_class` | v4.9 execution-friction category: `workflow_waste`, `missing_contract`, `execution_ambiguity`, `repeated_failure_mode`, `useful_pattern`, `bad_pattern`. |
| `recurrence_refs[]` | Prior Task Learning records or durable evidence of materially related recurrence. |
| `root_cause_relation` | Bounded recurrence-audit outcome: `SAME` (same root cause), `RELATED` (related root cause), `UNKNOWN` (unknown relation), `DIFFERENT` (different/superficial similarity). Schema-enforced: a declared relation requires `recurrence_audit_ref` and non-empty `recurrence_refs`. |
| `prevention_point_refs[]` | Candidate earliest reliable prevention/detection points (Task Pack/L3/template, schema/contract, deterministic checker, policy rule, orchestration rule, Product/Architecture gap). |
| `recurrence_audit_ref` | The bounded recurrence-audit evidence that produced `root_cause_relation`. |
| `ads_evolution_candidate_ref` | Binds this record's friction/recurrence evidence to an entry on the **existing** v4.8 ADS Evolution Intake path. Schema-enforced: requires `friction_classification=ADS_EVOLUTION_CANDIDATE`. |

Every new field is a reference or observation label. None of them carries decision authority, state, or a lifecycle.

## Orthogonality to friction_classification

`execution_friction_class` is orthogonal to the frozen v4.8 `friction_classification` vocabulary: it neither redefines, maps onto, nor overlaps the six-way classification, and no translation between the two vocabularies is claimed. The fields **MAY co-occur** in one record; neither field implies the other. `friction_classification` keeps its v1 enum, semantics and v4.8 ownership byte-for-byte.

## Resolve-or-fail-closed

All reference-bearing fields (`recurrence_refs`, `prevention_point_refs`, `recurrence_audit_ref`, `ads_evolution_candidate_ref`, and the v1 ref fields) are **resolve-or-fail-closed**: a consumer must resolve each reference against its owning surface or fail closed for that claim. A stale or missing reference never becomes a default, never silently narrows an obligation, and never supplies a relation value. `root_cause_relation` without resolvable `recurrence_audit_ref` evidence establishes nothing.

## Authority and routing boundaries

Task Learning records — v1 and v2 alike — are evidence refs only. They MUST NOT edit normative ADS files, mark an evolution candidate approved, or bypass any Review/Validation/Release stage. A v2 record is historical learning evidence only; it is never Gate PASS.

- Recurrence or friction evidence cannot become authority by accumulation; there is no numeric promotion threshold.
- `UNKNOWN` (and `DIFFERENT`) never self-promote standard change; a materially related recurrence only produces evidence for the **existing** Evolution Intake through the v1 `friction_classification=ADS_EVOLUTION_CANDIDATE` / `ads_evolution_candidate_ref` linkage.
- Promotion still enters ordinary ADS Intake → L1 → PRD → L2 → Task governance; `ads_evolution_candidate_ref` points at an intake entry, it does not create, approve or auto-promote one.

## v1/v2 compatibility

v1 and v2 share the same semantic owner and preserve the v1 core field vocabulary. v2 intentionally uses an explicit `schema_version` and adds optional v4.9 fields; a v1-only parser is not assumed to accept a v2 instance, and a v2 parser fails closed on v1 instances (no silent reinterpretation in either direction).

Therefore compatibility is version-aware:

- historical v1 record validity: preserved (v1 schema and owner reference unmutated);
- owner-family semantics: preserved (`owner_family=task-learning`);
- v2 reader support for explicit v2 records: new capability;
- direct validation of a v2 instance against the v1 schema: not claimed (fails closed);
- adoption by v1-only consumers: requires explicit version negotiation/update, not silent reinterpretation.

See `references/TASK_LEARNING_V2_COMPATIBILITY.json` for the v4.2 Compatibility Record.

## Non-goals

Task Learning v2 does not authorize: a learning database, a new intake lifecycle, workflow state, automatic ADS mutation, private chain-of-thought capture, or a parallel Task Learning/Evolution record family. Any such expansion requires separate Product authority.

## Ownership boundaries

T-006 does not own:

- authority/applicability or State-Dimension registry entries — T-003;
- execution reducer / JIT / Dispatch / Claim integration — T-007;
- gate evidence transfer and successor wiring — T-010;
- registry/manifest adoption wiring — T-011;
- ADS Evolution Intake semantics — existing v4.8 owner.

If those surfaces are required to make this contract appear functional, stop and route to the owning Task rather than extending T-006 scope.

## Minimal material example

```json
{
  "schema_version": "ai-dev/task-learning-v2",
  "owner_family": "task-learning",
  "predecessor_protocol_version": "ai-dev/task-learning-v1",
  "learning_id": "learning:T-006:001",
  "repository_ref": "github:kaicreator-mm/ai-development-standard",
  "work_item_ref": "github:kaicreator-mm/ai-development-standard#725",
  "implementation_subject_ref": "git:kaicreator-mm/ai-development-standard@0123456789abcdef0123456789abcdef01234567",
  "authority_refs": ["task-pack:v4.9.0/T-006"],
  "summary": "Repeated missing-contract friction traced to one prevention point.",
  "source_test_validation_review_refs": ["test:test_v49_task_learning_v2#positive"],
  "confidence_layers": ["IDENTITY_BOUND"],
  "friction_classification": "ADS_EVOLUTION_CANDIDATE",
  "execution_friction_class": "missing_contract",
  "recurrence_refs": ["learning:T-001:001"],
  "root_cause_relation": "SAME",
  "recurrence_audit_ref": "audit:v4.9.0/recurrence-t006",
  "prevention_point_refs": ["task-pack:v4.9.0/T-006"],
  "ads_evolution_candidate_ref": "evolution-intake:ADS-CAND-001",
  "disposition": "MORE_EVIDENCE"
}
```
