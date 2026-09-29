# v4.2.0 Task DAG — Evolution Governance

Status: **FROZEN TASK DAG — 2026-09-30**

Freeze inputs:

- Frozen Product Authority: `fc68e869c18cec07e2a72b8fa5e4520ade1dc5a9`
- Frozen L2 Architecture: `ea4532cacf87c03689351e43363580e2a14acd95`

## 1. DAG

```text
T01 Shared Evolution Machine Contracts
        │
        ├───────────────┐
        ▼               ▼
T02 Interface &      T03 Data & Migration
Compatibility        Governance
        │               │
        ▼               ▼
T04 API/Service      T05 Stateful DB
Conformance/Dogfood  Conformance/Dogfood
        │               │
        └──────┬────────┘
               │
        T06 Adoption & Wiring
               │
               ▼
        T07 Cross-standard
        Conformance / Closure Inputs
               │
               ▼
        Version Closure
```

T06 also requires both T02 and T03 even if T04/T05 are still executing; T07 requires T04 + T05 + T06.

## 2. Task definitions

### T01 — Shared Evolution Machine Contracts

Owns only:

- `schemas/compatibility-record-v1.schema.json`
- `schemas/migration-transition-v1.schema.json`
- compatibility-preserving optional references in existing evidence schemas where L2 requires them
- focused schema/backward-compatibility tests

Must not define domain normative policy beyond what schemas need to encode.

### T02 — Interface & Compatibility Governance

Owns:

- `standards/INTERFACE_COMPATIBILITY_GOVERNANCE_STANDARD.md`
- `references/INTERFACE_COMPATIBILITY_REFERENCE.md`
- focused semantic tests

Must preserve operation-vs-outcome separation, multi-dimensional compatibility, baseline/producer/consumer truth, deprecation/removal authority, and non-inference rules.

### T03 — Data & Migration Governance

Owns:

- `standards/DATA_MIGRATION_GOVERNANCE_STANDARD.md`
- `references/DATA_MIGRATION_REFERENCE.md`
- focused semantic tests

Must preserve directional source→target transition identity, fresh/upgrade/recovery distinctions, recovery-strategy flexibility, environment applicability and production authority boundary.

### T04 — API/Service Conformance & Dogfood

Owns conformance fixtures/scenarios only for interface evolution:

- additive compatible case;
- wire-safe but application/source incompatible negative;
- producer/consumer co-change masking negative;
- exact baseline/consumer identity tests.

No new normative owner.

### T05 — Stateful Database Conformance & Dogfood

Owns persistent-state conformance scenarios:

- fresh install vs upgrade distinction;
- A→B directional transition;
- interrupted/failure recovery;
- alternate recovery strategy without mandatory down migration;
- environment/runtime non-substitution.

If required proof cannot be established without a real database/runtime, create explicit local/external Validation handoff; do not fake execution.

### T06 — Adoption & Cross-standard Wiring

Owns central integration only:

- `standard-manifest.json` additions;
- selected project override/adoption guidance;
- compatibility/migration references from Validation/Release/testing surfaces where additive and justified;
- migration/adoption notes.

Must not rewrite T01–T05 semantics.

### T07 — Cross-standard Conformance / Closure Inputs

Owns:

- cross-standard negative inference tests;
- historical payload/adoption compatibility;
- Fast Path proportionality;
- v4.4 deployment-boundary checks;
- closure evidence inputs.

Must not perform Version Closure verdict itself.

## 3. Dependency semantics

After materialization, GitHub Issue Dependencies become the canonical live execution DAG. This file remains frozen planning/history authority.

Expected native edges:

```text
T02 blocked by T01
T03 blocked by T01
T04 blocked by T02
T05 blocked by T03
T06 blocked by T02 + T03
T07 blocked by T04 + T05 + T06
```

Task branches are JIT from the current integration target only when native dependencies are satisfied.

## 4. Integration target

Create `version/v4.2.0` only after the planning PR containing Frozen Product/L2/DAG/Task Packs is merged to `main` or otherwise integrated according to current repository authority.

Task PRs target `version/v4.2.0` and use one concern per PR.

## 5. Review / Validation posture

- T01–T03: `review:required`, concern Validation required.
- T04–T05: `review:required` because conformance truth can silently overclaim compatibility/migration evidence.
- T06: required Review because it touches central manifest/adoption wiring.
- T07: required Review and integration-level Validation inputs.

Exact review/validation evidence binds immutable subject identity and becomes stale on material HEAD drift.

## 6. Local environment posture

Planning/T01–T03 are expected to be repository-executable without special external systems.

T04 may use static/protocol fixtures unless a real service is required by the chosen dogfood subject.

T05 is the first likely local/external gate. If a real database transition is required, create a dedicated handoff Issue containing exact SHA, database/runtime tuple, fixture authority, allowed mutation and cleanup semantics before local execution.

`LOCAL_ENV=NOT_REQUIRED` at DAG Freeze.