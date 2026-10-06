# v4.6 AI-native Adoption and Cross-standard Wiring Guide

Task: T07 / Issue #310
Authority: Frozen v4.6 Product, L2, Task DAG, L3 and `docs/implementation/4.6.0/task-packs/T07_adoption_wiring.md`

## 1. Scope

v4.6 adds an AI-native governance layer without replacing the existing execution, assurance, handoff, validation or release architecture.

Projects adopting a v4.6 revision wire in exactly three new normative owners:

1. `standards/INTENT_ASSUMPTION_GOVERNANCE_STANDARD.md`
2. `standards/CONTEXT_ENGINEERING_STANDARD.md`
3. `standards/SKILL_PROCEDURE_GOVERNANCE_STANDARD.md`

v4.6 also adds exactly two default machine-contract families:

1. `schemas/intent-assumption-record-v1.schema.json`
2. `schemas/skill-metadata-v1.schema.json`

There is no default Context Snapshot contract. Context is reconstructed from durable owner references plus live currentness reads.

## 2. Existing owners remain authoritative

v4.6 cross-standard adoption is reference-based. Do not copy or replace semantics already owned elsewhere.

| Concern | Existing owner retained | v4.6 relationship |
|---|---|---|
| Agent freedom / autonomy | F0–F3 in existing Task/Execution/Dispatch architecture | v4.6 may reference it; no second autonomy scale |
| Assurance coverage | `schemas/assurance-plan-v1.schema.json` and existing Assurance policy | AI-native concerns use existing coverage mechanisms |
| Review judgment / provenance | `schemas/review-aggregation-v1.schema.json` and existing Review authority | provider/model/context facts remain provenance, not automatic independence |
| Executable handoff | `schemas/dispatch.schema.json` + existing GitHub/Local Agent handoff owners | optional Intent/Skill refs do not replace Task/Dispatch authority |
| Validation | `standards/VALIDATION_STANDARD.md` and exact-subject evidence | no AI-native PASS state |
| Release | `standards/RELEASE_STANDARD.md` | no AI-native READY state |

Use `references/AI_NATIVE_EXISTING_OWNER_INTEGRATION.md` as the non-normative cross-owner map. It is a pointer surface, not a replacement owner.

## 3. Materiality-driven project adoption

v4.6 AI-native adoption is orthogonal to the existing A0–A4 v4 adoption level. A project may be A0, A1, A2, A3 or A4 and still apply the v4.6 governance rules when their concerns are material.

Recommended `PROJECT_OVERRIDES.md` fields are:

```text
v4.ai_native.intent_assumption: materiality-driven
v4.ai_native.context_currentness: canonical
v4.ai_native.skill_admission: disabled | materiality-driven | project-specific stronger policy
v4.ai_native.durable_truth_surface: GitHub/repository refs | project-specific durable owner surfaces
```

These fields specialize implementation posture only. They do not weaken Frozen Product/Architecture/Task authority or any required Review, Validation, Candidate, Release or external side-effect gate.

## 4. Intent / Assumption adoption

Use the Intent/Assumption owner when interpretation, uncertainty or promotion is material to scope, acceptance, safety, public contract, data meaning, security, irreversible side effects or another owning decision.

Rules:

- `USER_INTENT`, `INTERPRETATION`, `ASSUMPTION`, `UNKNOWN`, `DECISION_REQUIRED` and `DURABLE_REQUIREMENT_REF` remain distinct.
- A machine record describes a durable fact; it does not itself issue Product Freeze, Architecture Freeze or Task authority.
- `PROMOTE_BY_OWNER` is not proof of promotion. A durable requirement reference must point to the actual current owner-issued requirement and required promotion authority references.
- Same-level contradiction remains explicit until the owning authority resolves it.
- When no durable machine record is materially needed, do not create an empty record merely to satisfy ceremony.

## 5. Context Engineering adoption

Context adoption is about owner-aware authority, currentness and progressive disclosure.

Projects should:

1. start from the pinned standard/project entrypoint;
2. load the applicable Frozen Product/L2/Task Pack only when material;
3. read live Issue dependencies, branch/base and PR HEAD for currentness-sensitive execution facts;
4. follow referenced source/tests/evidence rather than loading the repository indiscriminately;
5. preserve same-level conflicts and missing required facts as UNKNOWN/BLOCKED/DECISION_REQUIRED under the applicable owner.

Required development truth must be durable outside the current chat/session. Historical chat or memory may help discovery but does not override the current durable owner.

Do not create a project-local Context Snapshot/database as a shortcut. v4.6 deliberately has no default Context Snapshot machine family and does not implement a repository-wide v4.7 resolver.

## 6. Skill / reusable procedure adoption

Adopt Skill governance when a reusable Agent procedure is materially used or maintained.

Before material invocation, establish:

- exact Skill identity/version/source/procedure reference;
- maintenance owner and provenance;
- project acceptance/applicability;
- current Task/Execution/Dispatch authority and allowed write/side-effect scope;
- compatibility/evaluation/security references where required;
- durable output/result surface and failure/escalation path.

Never infer:

```text
installed Skill -> trusted Skill
available tool/credential -> side-effect authorization
Skill instruction -> Product/Architecture/Task override
prior Skill evaluation -> current invocation Validation PASS
newer Skill version -> silently compatible/currently accepted
```

If the project does not materially adopt reusable Skills, no empty Skill metadata record is required.

## 7. Fast Path

Fast Path remains proportional:

> Reduce ceremony, not truth.

For a genuinely small/non-material concern, v4.6 does **not** require empty Intent/Assumption or Skill records. Context may also remain a minimal set of durable pointers.

Fast Path still cannot bypass:

- applicable scope/authority;
- exact subject identity/currentness;
- material unresolved intent/assumption/conflict;
- required Validation or Review;
- Candidate/Release/Repository Integration separation;
- applicable side-effect authority.

A low A0/A1 adoption level or absence of AI-native records is not evidence that work is low risk.

## 8. Historical evidence

Do not retrofit historical evidence.

Existing v3.4/v4/v4.1–v4.5 Issues, PRs, Dispatch records, Execution Packs, Reviews and Validation results keep their original subject identity, schema/version and result. Adopting v4.6 does not mean they were produced under Intent/Assumption or Skill metadata contracts.

New v4.6 records may reference relevant historical facts as background where current authority permits, but must not relabel old evidence or manufacture currentness.

## 9. Recommended migration sequence

1. Pin the exact v4.6 standard revision in `.dev-standard/VERSION` after the version is released/available for project adoption.
2. Keep the existing A0–A4 adoption level truthful; do not raise it solely because v4.6 files exist.
3. Add/confirm the v4.6 AI-native profile in `.dev-standard/PROJECT_OVERRIDES.md`.
4. Identify which of Intent/Assumption and Skill governance are materially applicable to the project; keep non-material record families uninstantiated.
5. Confirm Context Engineering currentness/durable-truth handling for current project workflows.
6. Reference `references/AI_NATIVE_EXISTING_OWNER_INTEGRATION.md` rather than duplicating Assurance/Review/Dispatch/Handoff/Validation/Release semantics.
7. Preserve all historical evidence identities/results.
8. Run the project verifier and project-required exact-subject validation/review for the adoption change.

## 10. Migration examples

### Example A — Fast Path documentation correction

A typo correction has no material intent ambiguity and uses no reusable Skill. The project may keep both Intent/Assumption and Skill machine records absent. It still binds the change to the real repository/PR subject and follows any applicable review/validation policy.

### Example B — material interpretation changes public behavior

A user statement is ambiguous about externally visible behavior. Record the Agent interpretation separately from user intent, route the material question to the existing Product owner and wait for a durable owner decision. Do not promote the interpretation by writing a schema-valid record.

### Example C — reusable deployment procedure is available

A deployment Skill is installed and a cloud credential exists. The Skill metadata may describe tool/side-effect classes, but the current Task and external-system owner must separately authorize the deployment. Installation plus credential availability is not permission.

## 11. Non-goals and boundaries

This guide does not:

- create a fourth v4.6 normative AI-native owner;
- create a Context Snapshot/database family;
- create another autonomy, Assurance, Review, Dispatch, Handoff, Validation or Release state model;
- implement a repository-wide v4.7 resolver;
- require provider/model-specific project policy;
- require empty Intent/Assumption or Skill records on Fast Path;
- reinterpret historical evidence;
- execute or claim sibling T06 session/operator handoff dogfood evidence;
- perform Version Closure or Release Qualification.

## 12. Adoption verification

For a v4.6 adoption/wiring change, verify at least:

```text
manifest contains all three normative owners
manifest contains both machine families
manifest exposes the four v4.6 references and focused tests
Golden coverage standard set == manifest normative standard set
PROJECT_OVERRIDES v4.6 profile is materiality-driven and non-weakening
selected project/review/closure checklists reference existing owners rather than duplicating them
Fast Path does not require empty records
historical evidence is not retrofitted
no Context Snapshot/database or v4.7 repository-wide resolver is introduced
```

Concern Validation and Fresh Independent Review must bind to the exact candidate HEAD required by the Task. This guide itself is not a Validation or Review verdict.
