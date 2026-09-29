# v4.3.0 Task DAG — Engineering Design & Implementation Profiles

Status: **FROZEN TASK DAG — 2026-09-30; contract-metadata repair after #223 review, topology unchanged**

Freeze inputs:

- Frozen Product Authority: `68ce6fd157a0b932651c42f67627e9dc0b8880c3`
- Frozen L2 Architecture: `b90f9b698edcc426051a93569634fcef7a74e644`
- Integration target: `version/v4.3.0`

## 1. DAG

```text
T01 DAG Mutation Machine Contract          T02 Profile Framework
          │                                      │
          ▼                                      ▼
T05 Task DAG Governance              T06 Implementation Quality
                                                 │
                          ┌──────────────────────┼──────────────────────┐
                          ▼                      ▼                      ▼
                 T07 TypeScript+Python   T08 Go+Java+Rust      T09 Archetype Profiles

T03 Architecture Design ───────────────┐
T04 Task Decomposition ────────────────┤
T05 Task DAG Governance ───────────────┤
T07 Language Profiles A ───────────────┤
T08 Language Profiles B ───────────────┤→ T10 Adoption & Wiring
T09 Archetype Profiles ────────────────┘
                                                │
                                                ▼
                                    T11 Conformance & Dogfood
                                                │
                                                ▼
                                         Version Closure
```

T03 and T04 have no implementation dependency on T01/T02 after planning integration and may start JIT in parallel with T01/T02. T05 requires T01. T06 requires T02. T07/T08 require T06. T09 requires T02 + T06. T10 requires T03/T04/T05/T07/T08/T09. T11 requires T10.

## 2. Task definitions

### T01 — DAG Mutation Machine Contract
Own only `schemas/dag-mutation-record-v1.schema.json` plus focused schema/backward-compatibility tests and narrowly required optional references. No DAG policy prose.

### T02 — Profile Framework
Own profile information architecture and deterministic applicability/composition guidance:

- `profiles/README.md`
- profile metadata/section conventions
- focused profile-resolution tests/reference helpers

No language-specific profile content and no repository-wide v4.7 resolver.

### T03 — Architecture Design Standard
Own:

- `standards/ARCHITECTURE_DESIGN_STANDARD.md`
- `references/ARCHITECTURE_DECISION_REFERENCE.md`
- focused semantic tests

Preserve L2 as research workflow and v4.2 as compatibility/migration semantic owner.

### T04 — Task Decomposition Standard
Own:

- `standards/TASK_DECOMPOSITION_STANDARD.md`
- `references/TASK_DECOMPOSITION_REFERENCE.md`
- focused Task Pack/Issue decomposition tests

Freeze minimum coherent concern + maximum safe parallelism without arbitrary size/file thresholds.

### T05 — Task DAG Governance Standard
Depends on T01. Own:

- `standards/TASK_DAG_GOVERNANCE_STANDARD.md`
- `references/TASK_DAG_GOVERNANCE_REFERENCE.md`
- focused semantic tests consuming DAG mutation schema

GitHub Issue Dependencies remain canonical live DAG.

### T06 — Implementation Quality Standard
Depends on T02. Own:

- `standards/IMPLEMENTATION_QUALITY_STANDARD.md`
- `references/IMPLEMENTATION_QUALITY_REFERENCE.md`
- focused language-neutral conformance tests

Defines neutral requirements and profile composition boundary, not exact ecosystem tool mandates.

### T07 — TypeScript + Python Language Profiles
Depends on T06. Own only:

- `profiles/languages/typescript.md`
- `profiles/languages/python.md`
- focused profile fixture/tests

Maps neutral requirements to ecosystem facts without copying style guides.

### T08 — Go + Java + Rust Language Profiles
Depends on T06. Own only:

- `profiles/languages/go.md`
- `profiles/languages/java.md`
- `profiles/languages/rust.md`
- focused profile fixture/tests

### T09 — Archetype Profiles
Depends on T02 + T06. Own:

- `profiles/archetypes/library.md`
- `profiles/archetypes/service.md`
- `profiles/archetypes/cli.md`
- focused archetype composition tests

No web/frontend/worker/desktop/profile explosion in v4.3 initial scope.

### T10 — Adoption & Cross-standard Wiring
Depends on T03/T04/T05/T07/T08/T09. Own central integration only:

- `standard-manifest.json`
- selected Task Pack / Execution Pack / PROJECT_OVERRIDES adoption guidance
- deterministic profile discovery/index wiring
- migration/adoption notes
- focused integration tests

Must not redesign T01–T09 semantics or implement v4.7 unified resolver.

### T11 — Conformance & Dogfood / Closure Inputs
Depends on T10. Own cross-standard negatives, profile-resolution regression, DAG-mutation conformance and a dogfood planning exercise where a high-capability planner produces concern-sized parallel Tasks consumable by bounded lower-cost executors.

No Version Closure verdict itself.

## 3. Native Issue dependency graph

After materialization, GitHub Issue Dependencies are canonical live execution topology. Expected edges:

```text
T05 blocked by T01
T06 blocked by T02
T07 blocked by T06
T08 blocked by T06
T09 blocked by T02 + T06
T10 blocked by T03 + T04 + T05 + T07 + T08 + T09
T11 blocked by T10
```

T01/T02/T03/T04 are initial parallel roots.

## 4. Integration / branch posture

Planning branch/PR integrates Frozen Product/L2/DAG/L3/Task Packs first. The single execution integration target is `version/v4.3.0`, created only after planning integration under repository authority. Execution Task branches are JIT from the current `version/v4.3.0` exact SHA only after native dependencies are satisfied.

One concern per PR. Stacked PR only for real unmerged code-baseline dependency; the DAG above is not implemented as a PR stack.

## 5. Per-Task risk and executor/model suitability

These routing defaults do not change Task authority or allow an executor to self-promote `agent_freedom`.

| Task | Risk | Suitable builder/executor | Review posture |
|---|---|---|---|
| T01 | high | bounded lower-cost/local builder after exact contract is frozen; Strong model for semantic repair | required Fresh Independent Review |
| T02 | high | Strong/Web for profile-composition semantics; bounded executor for mechanical fixtures | required Fresh Independent Review |
| T03 | high | Strong/Web because it creates normative architecture-design semantics | required Fresh Independent Review |
| T04 | high | Strong/Web because decomposition changes planning authority boundaries | required Fresh Independent Review |
| T05 | high | Strong/Web or bounded builder with exact T01 contract; native GitHub mutation may require controller/local capability | required Fresh Independent Review |
| T06 | high | Strong/Web for normative neutral quality contract; bounded executor for deterministic tests | required Fresh Independent Review |
| T07 | medium | bounded lower-cost/local builder using official TypeScript/Python evidence; escalate semantic conflict | required Fresh Independent Review |
| T08 | medium | bounded lower-cost/local builder using official Go/Java/Rust evidence; escalate semantic conflict | required Fresh Independent Review |
| T09 | medium | bounded lower-cost/Web builder inside frozen three-archetype set | required Fresh Independent Review |
| T10 | high | Strong/Web integration owner; mechanical wiring may be delegated | required Fresh Independent Review + integration Validation |
| T11 | high | Strong planner + independent validator/reviewer; bounded lower-cost interpretation is a dogfood subject, not authority | required integration Review/Validation |

Profile-scope evidence is indexed in `docs/implementation/4.3.0/PROFILE_SCOPE_EVIDENCE.md`.

## 6. Review / Validation posture

T01–T06: required concern Validation + Fresh Independent Review.

T07–T09: required Review because incorrect profile mappings can silently create toolchain/authority rules; Validation can batch ecosystem profile checks while retaining per-Task evidence identity.

T10: required Review/Validation due central wiring.

T11: required integration Review/Validation and durable handoff to Version Closure.

## 7. Local environment posture

Planning and T01–T06 are expected to be repository/Web/CI executable.

T07/T08 may require ecosystem toolchain probes only if profile claims cannot be established from repository/official source evidence. If a required compiler/runtime probe is unavailable, create an exact-scope local Validation handoff per profile/Task; do not infer PASS from installed Agent tooling.

T11 dogfood may use existing repository task materialization; no local environment is assumed unless executable profile proof is explicitly required.

`LOCAL_ENV=NOT_REQUIRED` at Task DAG Freeze and at this #223 metadata repair.
